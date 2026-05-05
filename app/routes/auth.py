from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.university import University
from app.models.student import Student
from app.schemas.university import UniversityCreate
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

# --- REGISTER UNIVERSITY ---
@router.post("/university/register", status_code=201)
def register(uni: UniversityCreate, db: Session = Depends(get_db)):
    # Check duplicate
    if db.query(University).filter(University.email == uni.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_uni = University(
        name=uni.name,
        email=uni.email,
        hashed_password=get_password_hash(uni.password)
    )
    db.add(new_uni)
    db.commit()
    db.refresh(new_uni)
    return {"message": "University registered successfully", "id": new_uni.id}

# --- UNIVERSITY LOGIN ---
@router.post("/university/login")
def login_university(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(University).filter(University.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- STUDENT LOGIN ---
@router.post("/student/login")
def login_student(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == form_data.username).first()
    
    # Note: Ensure Student model mein password field ka naam 'password' hi hai
    if not student or not verify_password(form_data.password, student.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": student.email})
    return {"access_token": access_token, "token_type": "bearer"}


# app/routes/auth.py
from pydantic import BaseModel
# Router (Iska prefix main.py mein "/auth" hoga)
# router = APIRouter()

# --- SCHEMA ---
class StudentRegister(BaseModel):
    name: str
    email: str
    password: str

# --- REGISTER ROUTE ---
# Final URL banega: /auth/student/register
@router.post("/student/register")
def register_student(student: StudentRegister, db: Session = Depends(get_db)):
    # 1. Duplicate Check
    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Save New Student
    new_student = Student(
        name=student.name,
        email=student.email,
        hashed_password=get_password_hash(student.password)
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return {"message": "Account created successfully", "id": new_student.id}