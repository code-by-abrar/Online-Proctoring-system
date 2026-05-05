from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class ExamRegistration(Base):
    __tablename__ = "exam_registrations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    exam_id = Column(Integer, ForeignKey("exams.id"))
    status = Column(String, default="assigned")
    score = Column(Integer, default=0)

    student = relationship("Student", back_populates="registrations")
    exam = relationship("Exam", back_populates="registrations")