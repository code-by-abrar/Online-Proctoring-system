from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    exams = relationship("Exam", back_populates="creator")
    students = relationship("Student", back_populates="university")