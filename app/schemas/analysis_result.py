from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class AnalysisResultResponse(BaseModel):
    id: int
    resume_id: int
    ats_score: float
    skills: List[str]
    feedback: Dict[str, Any]
    suggestions: List[str]
    grammar_score: Optional[float] = None
    formatting_score: Optional[float] = None
    keyword_score: Optional[float] = None
    analyzed_at: datetime
    
    class Config:
        from_attributes = True

class ATSAnalysis(BaseModel):
    score: float
    keyword_optimization: float
    formatting_issues: List[str]
    missing_sections: List[str]
    grammar_clarity: float

class SkillExtraction(BaseModel):
    technical_skills: List[str]
    soft_skills: List[str]
    tools: List[str]
    certifications: List[str]

class ResumeSuggestions(BaseModel):
    bullet_improvements: List[str]
    skill_additions: List[str]
    project_suggestions: List[str]
    summary_rewrite: Optional[str] = None
    role_specific: Dict[str, List[str]]
