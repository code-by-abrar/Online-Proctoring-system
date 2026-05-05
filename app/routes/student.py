
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import get_db
from app.models.student import Student
from app.models.exam_registration import ExamRegistration
from app.models.exam import Exam
from app.models.violation import Violation
from app.core.security import get_password_hash, get_current_student

router = APIRouter()

@router.get("/my-exams")
def get_my_exams(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    # Student ki sari registrations nikalo
    registrations = db.query(ExamRegistration).filter(
        ExamRegistration.student_id == current_student.id
    ).all()
    
    exam_list = []
    
    for reg in registrations:
        exam = db.query(Exam).filter(Exam.id == reg.exam_id).first()
        
        # 👇 CHECK: Kitni Violations ki hain?
        violation_count = db.query(Violation).filter(
            Violation.exam_id == exam.id,
            Violation.student_id == current_student.id
        ).count()
        
        exam_list.append({
            "id": exam.id,
            "name": exam.name,
            "duration": exam.duration_minutes,
            "start_time": exam.start_time,
            "status": reg.status,  # "assigned" ya "submitted"
            "score": reg.score,    # Marks
            "violations": violation_count # 🚨 Cheating Count
        })
        
    return exam_list