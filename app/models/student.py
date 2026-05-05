# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database import Base

# class Student(Base):
#     __tablename__ = "students"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String, unique=True, index=True)
#     university_id = Column(Integer, ForeignKey("universities.id"))

#     university = relationship("University", back_populates="students")
#     registrations = relationship("ExamRegistration", back_populates="student")
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    
    # >> YEH LINE ADD KAREIN (Ye miss thi):
    hashed_password = Column(String) 
    
    university_id = Column(Integer, ForeignKey("universities.id"))

    # Relationships
    university = relationship("University", back_populates="students")
    registrations = relationship("ExamRegistration", back_populates="student")