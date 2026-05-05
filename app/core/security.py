from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.university import University
from app.models.student import Student

# --- CONFIGURATION ---
SECRET_KEY = "supersecretkey"  # Asli app mein environment variable use karein
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

# --- PASSWORD HASHING ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. University ka Lock 🔓
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/university/login",
    scheme_name="University_Auth"  # <--- YEH NAME ZAROORI HAI
)

# 2. Student ka Lock 🔓
oauth2_scheme_student = OAuth2PasswordBearer(
    tokenUrl="/student/login",
    scheme_name="Student_Auth"     # <--- YEH NAME ZAROORI HAI
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- GET CURRENT USER FUNCTIONS ---

# 1. UNIVERSITY check karne ke liye
def get_current_university(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(University).filter(University.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# 2. STUDENT check karne ke liye (Ab yeh naye raste se token lega)
def get_current_student(token: str = Depends(oauth2_scheme_student), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Student).filter(Student.email == email).first()
    if user is None:
        raise credentials_exception
    return user