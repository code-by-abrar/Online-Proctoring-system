from pydantic import BaseModel
from typing import List
from typing import Optional
class ExamCreate(BaseModel):
    name: str
    duration_minutes: int
    description: Optional[str]= None
class ExamResponse(BaseModel):
    id: int
    name: str
    university_id: int
    class Config:
        from_attributes = True


# >> YEH WALA CLASS ADD KAREIN (Assign ke liye)
class AssignExamRequest(BaseModel):
    exam_id: int
    student_ids: List[int]