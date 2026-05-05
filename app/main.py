from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Models create karne ke liye
from app.models import university, student, exam, exam_registration, violation, question, submission

# Routes Import karein
from app.routes import auth, exam, student, proctoring

# Database Tables Create (Agar nahi bane)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS (Frontend ke liye zaroori) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTERS REGISTER KAREIN ---

# 1. Auth Router (Login/Register)
# Note: Yahan se 'prefix' hata diya hai kyun ke auth.py khud paths sambhal raha hai
app.include_router(auth.router, prefix="/auth" ,tags=["Auth"]) 

# 2. Exam Router
app.include_router(exam.router, prefix="/exam", tags=["Exams"])

# 3. Student Router (Profile wagera)
app.include_router(student.router, prefix="/student", tags=["Students"])

# 4. Proctoring Router (AI Checks)
app.include_router(proctoring.router, prefix="/proctoring", tags=["AI Proctoring"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Online Proctoring System API"}