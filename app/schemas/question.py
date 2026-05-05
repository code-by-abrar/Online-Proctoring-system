from pydantic import BaseModel
from typing import List

class QuestionCreate(BaseModel):
    question_text: str
    options: List[str]  # Example: ["A", "B", "C", "D"]
    correct_answer: str

class QuestionResponse(QuestionCreate):
    id: int
    exam_id: int
    class Config:
        from_attributes = True