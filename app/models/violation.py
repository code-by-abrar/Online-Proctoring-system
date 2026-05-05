from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    exam_id = Column(Integer, ForeignKey("exams.id"))
    
    # Types: "mobile_phone", "multiple_faces", "looking_away", "audio_detected"
    violation_type = Column(String) 
    
    confidence = Column(Float)  # AI kitna sure hai (e.g., 0.95)
    proof_image = Column(String, nullable=True) # Base64 string ya image URL
    timestamp = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student")
    exam = relationship("Exam")