from sqlalchemy import Column, Integer, String, ForeignKey ,DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    duration_minutes = Column(Integer)
    university_id = Column(Integer, ForeignKey("universities.id"))
# 📅 Scheduled Exams ke liye 2 naye columns
    start_time = Column(DateTime)
    end_time = Column(DateTime)


# relations
    creator = relationship("University", back_populates="exams")
    registrations = relationship("ExamRegistration", back_populates="exam")

    questions = relationship("Question", back_populates="exam")
    # submissions = relationship("Submission", back_populates="exam")