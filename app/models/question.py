from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    
    question_text = Column(String)  # Sawal: "Capital of Pakistan?"
    options = Column(JSON)          # Options: ["Lahore", "Karachi", "Islamabad"]
    correct_answer = Column(String) # Jawab: "Islamabad"

    exam = relationship("Exam", back_populates="questions")