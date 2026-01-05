from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ResumeBase(BaseModel):
    filename: str
    file_type: str

class ResumeCreate(ResumeBase):
    resume_text: str
    parsed_data: Optional[str] = None

class ResumeResponse(ResumeBase):
    id: int
    user_id: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

class ParsedResumeData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    education: list = []
    skills: list = []
    experience: list = []
    projects: list = []
    certifications: list = []
