from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.database import get_db
from app.api.auth import get_current_user_id
from app.models import Resume, AnalysisResult
from app.schemas import ResumeResponse, AnalysisResultResponse
from app.services.resume_parser import ResumeParser
from app.services.ai_analyzer import AIAnalyzer

router = APIRouter()
security = HTTPBearer()

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user_id = await get_current_user_id(credentials, db)
    
    # Check file type - be more lenient
    filename = file.filename.lower()
    if not (filename.endswith('.pdf') or filename.endswith('.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are supported"
        )
    
    # Determine file type
    file_type = "pdf" if filename.endswith('.pdf') else "docx"
    
    # Read file content
    file_content = await file.read()
    
    # Parse resume
    parser = ResumeParser()
    
    try:
        if file_type == "pdf":
            resume_text = parser.extract_text_from_pdf(file_content)
        else:
            resume_text = parser.extract_text_from_docx(file_content)
        
        # Parse structured data
        parsed_data = parser.parse_resume_text(resume_text)
        
        # Save to database
        resume = Resume(
            user_id=user_id,
            filename=file.filename,
            file_type=file_type,
            resume_text=resume_text,
            parsed_data=json.dumps(parsed_data)
        )
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return resume
        
    except Exception as e:
        print(f"Error processing resume: {str(e)}")  # Debug logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        )

@router.post("/analyze/{resume_id}", response_model=AnalysisResultResponse)
async def analyze_resume(
    resume_id: int,
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
    
    # Check if already analyzed
    existing_analysis = db.query(AnalysisResult).filter(
        AnalysisResult.resume_id == resume_id
    ).first()
    
    if existing_analysis:
        return existing_analysis
    
    # Perform AI analysis
    analyzer = AIAnalyzer()
    
    try:
        parsed_data = json.loads(resume.parsed_data) if resume.parsed_data else {}
        
        # Analyze resume
        analysis = analyzer.analyze_resume(resume.resume_text, parsed_data)
        
        # Save analysis results
        analysis_result = AnalysisResult(
            resume_id=resume_id,
            ats_score=analysis["ats_score"],
            skills=json.dumps(analysis["skills"]),
            feedback=json.dumps(analysis["feedback"]),
            suggestions=json.dumps(analysis["suggestions"]),
            grammar_score=analysis.get("grammar_score"),
            formatting_score=analysis.get("formatting_score"),
            keyword_score=analysis.get("keyword_score")
        )
        
        db.add(analysis_result)
        db.commit()
        db.refresh(analysis_result)
        
        return analysis_result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing resume: {str(e)}"
        )

@router.get("/", response_model=List[ResumeResponse])
async def get_user_resumes(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user_id = await get_current_user_id(credentials, db)
    
    resumes = db.query(Resume).filter(Resume.user_id == user_id).all()
    return resumes

@router.get("/{resume_id}/analysis", response_model=AnalysisResultResponse)
async def get_resume_analysis(
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
    
    # Get analysis
    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.resume_id == resume_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found. Please analyze the resume first."
        )
    
    return analysis
