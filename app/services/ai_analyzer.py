import re
import json
import random
from typing import Dict, Any, List

class AIAnalyzer:
    def __init__(self):
        self.ats_keywords = [
            "experience", "skills", "education", "project", "developed", "managed",
            "led", "created", "implemented", "designed", "optimized", "improved",
            "achieved", "coordinated", "collaborated", "analyzed", "researched"
        ]
        
        self.action_verbs = [
            "achieved", "improved", "managed", "led", "developed", "created",
            "implemented", "designed", "optimized", "launched", "grew",
            "reduced", "increased", "streamlined", "automated", "coordinated"
        ]
        
        self.tech_keywords = [
            "python", "javascript", "react", "node", "sql", "aws", "docker",
            "kubernetes", "git", "api", "rest", "graphql", "mongodb", "postgresql"
        ]

    def calculate_ats_score(self, resume_text: str) -> Dict[str, Any]:
        """Calculate ATS score based on keywords and structure"""
        text_lower = resume_text.lower()
        
        # Count ATS keywords
        keyword_count = sum(1 for keyword in self.ats_keywords if keyword in text_lower)
        keyword_score = min((keyword_count / len(self.ats_keywords)) * 100, 100)
        
        # Count action verbs
        action_count = sum(1 for verb in self.action_verbs if verb in text_lower)
        action_score = min((action_count / len(self.action_verbs)) * 100, 100)
        
        # Count tech keywords
        tech_count = sum(1 for tech in self.tech_keywords if tech in text_lower)
        tech_score = min((tech_count / len(self.tech_keywords)) * 100, 100)
        
        # Calculate overall score
        overall_score = (keyword_score * 0.4 + action_score * 0.3 + tech_score * 0.3)
        
        return {
            "ats_score": round(overall_score, 1),
            "keyword_score": round(keyword_score, 1),
            "action_score": round(action_score, 1),
            "tech_score": round(tech_score, 1),
            "keywords_found": [kw for kw in self.ats_keywords if kw in text_lower],
            "actions_found": [av for av in self.action_verbs if av in text_lower],
            "tech_found": [tk for tk in self.tech_keywords if tk in text_lower]
        }

    def extract_skills(self, resume_text: str) -> List[str]:
        """Extract skills from resume text"""
        text_lower = resume_text.lower()
        found_skills = []
        
        # Common tech skills
        tech_skills = [
            "python", "javascript", "react", "node.js", "nodejs", "sql", "mysql", 
            "postgresql", "mongodb", "aws", "amazon web services", "docker", 
            "kubernetes", "k8s", "git", "github", "gitlab", "ci/cd",
            "html", "css", "typescript", "java", "c++", "c#", "php",
            "angular", "vue", "flask", "django", "fastapi", "express",
            "rest api", "graphql", "api", "linux", "ubuntu", "windows"
        ]
        
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))

    def analyze_grammar(self, resume_text: str) -> Dict[str, Any]:
        """Basic grammar and formatting analysis"""
        sentences = re.split(r'[.!?]+', resume_text)
        word_count = len(resume_text.split())
        
        # Basic checks
        has_bullet_points = '•' in resume_text or '-' in resume_text
        has_consistent_formatting = len(re.findall(r'\b[A-Z][a-z]+:', resume_text)) > 0
        
        grammar_score = 85 + random.randint(-5, 10)  # Base score with some variation
        if has_bullet_points:
            grammar_score += 5
        if has_consistent_formatting:
            grammar_score += 5
            
        grammar_score = min(grammar_score, 100)
        
        return {
            "grammar_score": round(grammar_score, 1),
            "word_count": word_count,
            "sentence_count": len([s for s in sentences if s.strip()]),
            "has_bullet_points": has_bullet_points,
            "has_consistent_formatting": has_consistent_formatting
        }

    def generate_suggestions(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions based on analysis"""
        suggestions = []
        
        ats_score = analysis_result.get("ats_score", 0)
        skills = analysis_result.get("skills", [])
        
        if ats_score < 80:
            suggestions.append("Add more ATS keywords and action verbs to improve your resume score")
        
        if len(skills) < 5:
            suggestions.append("Include more technical skills to showcase your expertise")
        
        suggestions.append("Quantify your achievements with specific metrics and numbers")
        suggestions.append("Tailor your resume for each job application")
        suggestions.append("Include a professional summary at the top of your resume")
        
        return suggestions

    def analyze_resume(self, resume_text: str, job_description: str = None) -> Dict[str, Any]:
        """Complete resume analysis"""
        # ATS Analysis
        ats_analysis = self.calculate_ats_score(resume_text)
        
        # Skills Extraction
        skills = self.extract_skills(resume_text)
        
        # Grammar Analysis
        grammar_analysis = self.analyze_grammar(resume_text)
        
        # Generate suggestions
        suggestions = self.generate_suggestions({
            "ats_score": ats_analysis["ats_score"],
            "skills": skills
        })
        
        # Job matching (if job description provided)
        job_match = None
        if job_description:
            job_match = self.match_with_job(resume_text, job_description)
        
        return {
            "ats_score": ats_analysis["ats_score"],
            "grammar_score": grammar_analysis["grammar_score"],
            "formatting_score": 85 + random.randint(-5, 10),  # Simulated formatting score
            "skills": skills,
            "suggestions": suggestions,
            "job_match": job_match,
            "analysis_details": {
                "keyword_analysis": ats_analysis,
                "grammar_analysis": grammar_analysis
            }
        }

    def match_with_job(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Match resume with job description"""
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Extract skills from both
        resume_skills = self.extract_skills(resume_text)
        
        # Common job requirements
        job_requirements = []
        for skill in self.tech_keywords:
            if skill in job_lower:
                job_requirements.append(skill.title())
        
        # Calculate overlap
        matching_skills = [skill for skill in resume_skills if skill.lower() in [req.lower() for req in job_requirements]]
        missing_skills = [req for req in job_requirements if req.lower() not in [skill.lower() for skill in resume_skills]]
        
        # Calculate match score
        if len(job_requirements) > 0:
            match_percentage = (len(matching_skills) / len(job_requirements)) * 100
        else:
            match_percentage = 50  # Default if no clear requirements found
        
        return {
            "match_score": round(match_percentage, 1),
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "job_requirements": job_requirements,
            "suggestions": [
                f"Learn {skill}" for skill in missing_skills[:3]
            ] + [
                "Highlight your relevant experience with the required skills",
                "Add specific projects that demonstrate these skills"
            ]
        }
