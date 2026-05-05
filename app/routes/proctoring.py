from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.violation import Violation # Model zaroor import karein
from app.models.exam import Exam
from app.core.security import get_current_student
from app.models.student import Student
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ViolationRequest(BaseModel):
    exam_id: int
    violation_type: str
    confidence: float
    proof_image: Optional[str] = None

# URL: /proctoring/log
@router.post("/log")
def log_violation(
    data: ViolationRequest,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    # 1. Check karo Exam exist karta hai?
    exam = db.query(Exam).filter(Exam.id == data.exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    print(f"📷 Proctoring: Detected {data.violation_type} for {current_student.name}")

    # 2. Database mein save karo
    new_violation = Violation(
        student_id=current_student.id,
        exam_id=data.exam_id,
        violation_type=data.violation_type,
        confidence=data.confidence,
        proof_image=data.proof_image
    )
    
    db.add(new_violation)
    db.commit()
    return {"message": "Violation logged"}