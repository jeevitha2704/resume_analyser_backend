from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, docx
    resume_text = Column(Text, nullable=False)
    parsed_data = Column(Text)  # JSON string of parsed resume data
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    analysis_results = relationship("AnalysisResult", back_populates="resume")
    job_matches = relationship("JobMatch", back_populates="resume")
