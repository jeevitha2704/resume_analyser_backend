from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    ats_score = Column(Float, nullable=False)
    skills = Column(Text)  # JSON string of extracted skills
    feedback = Column(Text)  # JSON string of AI feedback
    suggestions = Column(Text)  # JSON string of improvement suggestions
    grammar_score = Column(Float)
    formatting_score = Column(Float)
    keyword_score = Column(Float)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    resume = relationship("Resume", back_populates="analysis_results")
