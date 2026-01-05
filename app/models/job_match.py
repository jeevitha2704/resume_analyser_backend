from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class JobMatch(Base):
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_description = Column(Text, nullable=False)
    job_title = Column(String)
    match_score = Column(Float, nullable=False)
    missing_skills = Column(Text)  # JSON string of missing skills
    overlapping_skills = Column(Text)  # JSON string of overlapping skills
    suggestions = Column(Text)  # JSON string of job-specific suggestions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    resume = relationship("Resume", back_populates="job_matches")
