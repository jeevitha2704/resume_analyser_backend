from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.database import get_db
from app.api.auth import get_current_user_id
from app.models import Resume, JobMatch
from app.schemas import JobMatchCreate, JobMatchResponse
from app.services.ai_analyzer import AIAnalyzer

router = APIRouter()
security = HTTPBearer()

@router.post("/match/{resume_id}", response_model=JobMatchResponse)
async def match_with_job_description(
    resume_id: int,
    job_data: JobMatchCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user_id = await get_current_user_id(credentials, db)
    
    # Get resume
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == user_id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Perform job matching
    analyzer = AIAnalyzer()
    
    try:
        # Compare resume with job description
        match_analysis = analyzer.compare_with_job_description(
            resume.resume_text, 
            job_data.job_description
        )
        
        # Save job match results
        job_match = JobMatch(
            resume_id=resume_id,
            job_description=job_data.job_description,
            job_title=job_data.job_title,
            match_score=match_analysis["match_score"],
            missing_skills=json.dumps(match_analysis["missing_skills"]),
            overlapping_skills=json.dumps(match_analysis["overlapping_skills"]),
            suggestions=json.dumps(match_analysis["suggestions"])
        )
        
        db.add(job_match)
        db.commit()
        db.refresh(job_match)
        
        return job_match
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error matching with job description: {str(e)}"
        )

@router.get("/{resume_id}/matches", response_model=List[JobMatchResponse])
async def get_job_matches(
    resume_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user_id = await get_current_user_id(credentials, db)
    
    # Verify resume ownership
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == user_id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Get all job matches for this resume
    matches = db.query(JobMatch).filter(
        JobMatch.resume_id == resume_id
    ).order_by(JobMatch.created_at.desc()).all()
    
    return matches

@router.get("/matches", response_model=List[JobMatchResponse])
async def get_all_job_matches(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user_id = await get_current_user_id(credentials, db)
    
    # Get all resumes for this user
    user_resumes = db.query(Resume).filter(Resume.user_id == user_id).all()
    resume_ids = [resume.id for resume in user_resumes]
    
    # Get all job matches for user's resumes
    matches = db.query(JobMatch).filter(
        JobMatch.resume_id.in_(resume_ids)
    ).order_by(JobMatch.created_at.desc()).all()
    
    return matches

@router.get("/match/{match_id}", response_model=JobMatchResponse)
async def get_job_match_details(
    match_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user_id = await get_current_user_id(credentials, db)
    
    # Get job match and verify ownership
    match = db.query(JobMatch).join(Resume).filter(
        JobMatch.id == match_id,
        Resume.user_id == user_id
    ).first()
    
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job match not found"
        )
    
    return match
