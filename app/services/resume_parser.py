import re
import json
from typing import Dict, Any, List
from PyPDF2 import PdfReader
from docx import Document

class ResumeParser:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'\b(?:\+?(\d{1,3})?)?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b'
        
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            from io import BytesIO
            reader = PdfReader(BytesIO(pdf_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def extract_text_from_docx(self, docx_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            from io import BytesIO
            doc = Document(BytesIO(docx_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    def parse_resume_text(self, text: str) -> Dict[str, Any]:
        """Parse resume text into structured data"""
        parsed_data = {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "education": self._extract_education(text),
            "skills": self._extract_skills(text),
            "experience": self._extract_experience(text),
            "projects": self._extract_projects(text),
            "certifications": self._extract_certifications(text)
        }
        return parsed_data
    
    def _extract_name(self, text: str) -> str:
        """Extract name from resume text"""
        lines = text.split('\n')
        # Usually name is in the first few lines
        for i, line in enumerate(lines[:5]):
            line = line.strip()
            if len(line.split()) >= 2 and len(line) < 50:
                # Check if it looks like a name (no numbers, special chars)
                if not re.search(r'\d|@|\.com|\.edu', line):
                    return line
        return ""
    
    def _extract_email(self, text: str) -> str:
        """Extract email from resume text"""
        match = re.search(self.email_pattern, text)
        return match.group() if match else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from resume text"""
        match = re.search(self.phone_pattern, text)
        return match.group() if match else ""
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education_keywords = [
            "Bachelor", "Master", "PhD", "Doctorate", "MBA", "B.S.", "M.S.", 
            "B.Sc", "M.Sc", "University", "College", "Institute", "School"
        ]
        
        education_lines = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword.lower() in line.lower() for keyword in education_keywords):
                # Get this line and next few lines for context
                context = line.strip()
                for j in range(1, 4):
                    if i + j < len(lines):
                        next_line = lines[i + j].strip()
                        if next_line and len(next_line) < 200:
                            context += " " + next_line
                        else:
                            break
                education_lines.append(context)
        
        return education_lines[:5]  # Limit to top 5 education entries
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        # Common tech skills and keywords
        tech_skills = [
            "Python", "Java", "JavaScript", "React", "Node.js", "SQL", "MongoDB",
            "AWS", "Docker", "Kubernetes", "Git", "Machine Learning", "AI",
            "Data Science", "TensorFlow", "PyTorch", "HTML", "CSS", "TypeScript",
            "Angular", "Vue.js", "Express", "Django", "Flask", "PostgreSQL",
            "MySQL", "Redis", "Elasticsearch", "Jenkins", "CI/CD", "Agile",
            "Scrum", "REST API", "GraphQL", "Microservices", "DevOps"
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in tech_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract work experience"""
        experience_keywords = [
            "experience", "work", "job", "position", "role", "company",
            "employment", "career", "professional", "intern", "developer"
        ]
        
        experience_lines = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword.lower() in line.lower() for keyword in experience_keywords):
                # Get context around experience mentions
                context = line.strip()
                for j in range(1, 6):
                    if i + j < len(lines):
                        next_line = lines[i + j].strip()
                        if next_line and len(next_line) < 300:
                            context += " " + next_line
                        else:
                            break
                experience_lines.append(context)
        
        return experience_lines[:5]  # Limit to top 5 experience entries
    
    def _extract_projects(self, text: str) -> List[str]:
        """Extract project information"""
        project_keywords = ["project", "portfolio", "developed", "built", "created", "designed"]
        
        project_lines = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword.lower() in line.lower() for keyword in project_keywords):
                context = line.strip()
                for j in range(1, 4):
                    if i + j < len(lines):
                        next_line = lines[i + j].strip()
                        if next_line and len(next_line) < 200:
                            context += " " + next_line
                        else:
                            break
                project_lines.append(context)
        
        return project_lines[:5]  # Limit to top 5 projects
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_keywords = ["certified", "certification", "certificate", "license", "aws certified", "google certified"]
        
        cert_lines = []
        lines = text.split('\n')
        
        for line in lines:
            if any(keyword.lower() in line.lower() for keyword in cert_keywords):
                cert_lines.append(line.strip())
        
        return cert_lines[:5]  # Limit to top 5 certifications
