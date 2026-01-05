from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class JobMatchCreate(BaseModel):
    job_description: str
    job_title: Optional[str] = None

class JobMatchResponse(BaseModel):
    id: int
    resume_id: int
    job_description: str
    job_title: Optional[str] = None
    match_score: float
    missing_skills: List[str]
    overlapping_skills: List[str]
    suggestions: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class SkillMatchAnalysis(BaseModel):
    match_percentage: float
    missing_skills: List[str]
    overlapping_skills: List[str]
    skill_gap_analysis: Dict[str, Any]

class JobMatchSuggestions(BaseModel):
    resume_improvements: List[str]
    skill_additions: List[str]
    experience_highlights: List[str]
    keyword_optimizations: List[str]
