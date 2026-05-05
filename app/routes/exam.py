
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta, timezone # 🕒 Time Logic

from app.database import get_db
from app.models.exam import Exam
from app.models.university import University
from app.models.question import Question
from app.models.student import Student
from app.models.exam_registration import ExamRegistration
from app.core.security import get_current_university
from pydantic import BaseModel

router = APIRouter()

PENALTIES = {
    "mobile_phone": 30,
    "tab_switch": 25,
    "multiple_faces": 40,
    "looking_away": 10,
    "no_face": 15,
    "head_turn": 10,
    "audio_detected": 15
}

# --- SCHEMAS ---
class ExamCreate(BaseModel):
    name: str
    duration_minutes: int
    description: str
    start_time: datetime # 📅 Admin Date/Time bhejega

class QuestionCreate(BaseModel):
    question_text: str
    options: List[str]
    correct_answer: str

class AssignExamRequest(BaseModel):
    student_email: str
    exam_id: int

class SubmitExamRequest(BaseModel):
    exam_id: int
    answers: List[dict]

# --- 1. CREATE EXAM (SCHEDULED) ---
@router.post("/")
def create_exam(
    exam_data: ExamCreate, 
    db: Session = Depends(get_db), 
    current_uni: University = Depends(get_current_university)
):
    # End Time calculate karein
    calculated_end_time = exam_data.start_time + timedelta(minutes=exam_data.duration_minutes)

    new_exam = Exam(
        name=exam_data.name,
        duration_minutes=exam_data.duration_minutes,
        description=exam_data.description,
        start_time=exam_data.start_time,
        end_time=calculated_end_time,
        university_id=current_uni.id
    )
    
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    return {"message": "Exam scheduled successfully", "id": new_exam.id}


@router.get("/{exam_id}")
def get_exam_details(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # ✅ FIX: Simple 'now()' use karein (Aapke laptop ka time)
    # Koi timezone, koi utc nahi.
    current_time = datetime.now()

    # Debugging ke liye print karwayen (Console mein time show hoga)
    print(f"👉 Server Time: {current_time} | Exam Start: {exam.start_time}")

    if current_time < exam.start_time:
        raise HTTPException(status_code=400, detail=f"Exam not started. Starts at: {exam.start_time}")

    if current_time > exam.end_time:
        raise HTTPException(status_code=400, detail="Exam has ended!")
    
    # ... (Exam dhoondne ke baad) ...
    
    # 🛑 FIX: Agar start_time database mein NULL hai to check karein
    if exam.start_time is None:
        raise HTTPException(status_code=400, detail="Exam Start Time is invalid (NULL). Please delete this exam and create a new one.")

    # Ab compare karein (Crash nahi hoga)
    if current_time < exam.start_time:
        raise HTTPException(status_code=400, detail=f"Exam not started. Starts at: {exam.start_time}")
    remaining_seconds = (exam.end_time - current_time).total_seconds()

    return {
        "id": exam.id,
        "name": exam.name,
        "remaining_seconds": remaining_seconds, 
        "description": exam.description
    }


# --- 3. GET QUESTIONS ---
@router.get("/{exam_id}/questions")
def get_questions(exam_id: int, db: Session = Depends(get_db)):
    questions = db.query(Question).filter(Question.exam_id == exam_id).all()
    return questions

# --- 4. ADD SINGLE QUESTION ---
@router.post("/{exam_id}/questions")
def add_question(
    exam_id: int, 
    q: QuestionCreate, 
    db: Session = Depends(get_db),
    current_uni: University = Depends(get_current_university)
):
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.university_id == current_uni.id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found or permission denied")
    
    new_q = Question(
        exam_id=exam_id,
        question_text=q.question_text,
        options=q.options,
        correct_answer=q.correct_answer
    )
    db.add(new_q)
    db.commit()
    return {"message": "Question added"}

# --- 5. BULK UPLOAD QUESTIONS ---
@router.post("/{exam_id}/questions/bulk")
def add_bulk_questions(
    exam_id: int, 
    questions: List[QuestionCreate], 
    db: Session = Depends(get_db),
    current_uni: University = Depends(get_current_university)
):
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.university_id == current_uni.id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found or access denied")

    count = 0
    for q in questions:
        new_q = Question(
            exam_id=exam_id,
            question_text=q.question_text,
            options=q.options,
            correct_answer=q.correct_answer
        )
        db.add(new_q)
        count += 1
    
    db.commit()
    return {"message": f"Successfully added {count} questions"}

# --- 6. ASSIGN EXAM ---
@router.post("/assign")
def assign_exam(
    data: AssignExamRequest, 
    db: Session = Depends(get_db), 
    current_uni: University = Depends(get_current_university)
):
    student = db.query(Student).filter(Student.email == data.student_email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student email not found")

    exam = db.query(Exam).filter(Exam.id == data.exam_id, Exam.university_id == current_uni.id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found or permission denied")

    exists = db.query(ExamRegistration).filter(
        ExamRegistration.exam_id == data.exam_id, 
        ExamRegistration.student_id == student.id
    ).first()
    
    if exists:
        return {"message": "Exam already assigned"}

    reg = ExamRegistration(exam_id=data.exam_id, student_id=student.id, status="assigned")
    db.add(reg)
    db.commit()
    return {"message": f"Assigned to {student.name}"}


from app.core.security import get_current_student
from app.models.exam_registration import ExamRegistration 

# --- 7. SUBMIT EXAM (FIXED) ---
@router.post("/submit")
def submit_exam(
    data: SubmitExamRequest, 
    db: Session = Depends(get_db),
    # 👇 Yeh line add karein taake student ki pehchan ho sake
    current_student: Student = Depends(get_current_student) 
):
    # 1. Score Calculate (Aapka purana logic)
    score = 0
    total = 0
    
    correct_answers = {}
    questions = db.query(Question).filter(Question.exam_id == data.exam_id).all()
    for q in questions:
        # Lowercase aur Strip zaroori hai taake spelling match ho
        correct_answers[q.id] = q.correct_answer.strip().lower()
        total += 1
    
    for ans in data.answers:
        qid = ans['question_id']
        # Check: Agar bache ne option select kiya hai
        if ans['selected_option']:
            selected = ans['selected_option'].strip().lower()
            if qid in correct_answers and correct_answers[qid] == selected:
                score += 1
            
    # 2. ✅ DATABASE UPDATE (YEH MISSING THA)
    # Registration dhoondo is student aur exam ki
    reg = db.query(ExamRegistration).filter(
        ExamRegistration.exam_id == data.exam_id,
        ExamRegistration.student_id == current_student.id
    ).first()

    if reg:
        reg.score = score          # Score update kiya
        reg.status = "submitted"   # Status badla "submitted"
        db.commit()                # Save kiya
        print(f"✅ Exam Submitted for {current_student.name}. Score: {score}")
    else:
        # Agar assign nahi tha to naya bana do (Safety Case)
        new_reg = ExamRegistration(
            exam_id=data.exam_id,
            student_id=current_student.id,
            score=score,
            status="submitted"
        )
        db.add(new_reg)
        db.commit()

    return {"message": "Submitted", "score": score, "total": total}

from app.models.violation import Violation

@router.get("/{exam_id}/results")
def get_exam_results(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    registrations = db.query(ExamRegistration).filter(ExamRegistration.exam_id == exam_id).all()
    results_list = []

    for reg in registrations:
        student = db.query(Student).filter(Student.id == reg.student_id).first()
        
        # 1. Is bache ki saari violations nikalo
        logs = db.query(Violation).filter(
            Violation.exam_id == exam_id,
            Violation.student_id == reg.student_id
        ).all()

        # 2. TRUST SCORE CALCULATION (Wohi logic)
        total_score = 100
        deductions = 0
        
        for log in logs:
            penalty = PENALTIES.get(log.violation_type, 5) # Agar unknown ho to 5 kato
            deductions += penalty
        
        trust_score = max(0, total_score - deductions) # 0 se neeche na jaye

        # 3. Status set karo
        status_msg = "Clean"
        if trust_score < 50: status_msg = "HIGH RISK 🚨"
        elif trust_score < 80: status_msg = "Suspicious ⚠️"

        results_list.append({
            "student_name": student.name,
            "email": student.email,
            "score": reg.score,
            "status": reg.status,    
            "violations_count": len(logs),
            "trust_score": trust_score,  # 🆕 Calculated Score
            "risk_status": status_msg    # 🆕 Risk Label
        })

    return results_list