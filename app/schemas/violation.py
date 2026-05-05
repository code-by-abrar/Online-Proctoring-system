from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ViolationCreate(BaseModel):
    exam_id: int
    violation_type: str
    confidence: float
    proof_image: Optional[str] = None # Snapshot (Base64)

class ViolationResponse(BaseModel):
    id: int
    violation_type: str
    confidence: float
    timestamp: datetime
    
    class Config:
        from_attributes = True