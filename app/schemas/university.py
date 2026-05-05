from pydantic import BaseModel

class UniversityCreate(BaseModel):
    name: str
    email: str
    password: str

class UniversityResponse(BaseModel):
    id: int
    email: str
    class Config:
        from_attributes = True