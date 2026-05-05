from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    
    score = Column(Float)       # Kitne number aaye (e.g., 8.0)
    total_marks = Column(Float) # Total number (e.g., 10.0)

    student = relationship("Student")
    exam = relationship("Exam")