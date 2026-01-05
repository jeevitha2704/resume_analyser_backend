import re
import json
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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
        
        self.tech_skills = [
            "python", "java", "javascript", "react", "node.js", "sql", "mongodb",
            "aws", "docker", "kubernetes", "git", "machine learning", "ai",
            "data science", "tensorflow", "pytorch", "html", "css", "typescript",
            "angular", "vue.js", "express", "django", "flask", "postgresql",
            "mysql", "redis", "elasticsearch", "jenkins", "ci/cd", "agile",
            "scrum", "rest api", "graphql", "microservices", "devops"
        ]
    
    def analyze_resume(self, resume_text: str, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive AI analysis of resume"""
        
        # ATS Compatibility Analysis
        ats_score = self._calculate_ats_score(resume_text)
        
        # Skills Analysis
        skills_analysis = self._analyze_skills(resume_text, parsed_data)
        
        # Grammar and Clarity
        grammar_score = self._analyze_grammar(resume_text)
        
        # Formatting Analysis
        formatting_score = self._analyze_formatting(resume_text)
        
        # Keyword Optimization
        keyword_score = self._analyze_keywords(resume_text)
        
        # Generate Feedback
        feedback = self._generate_feedback(
            ats_score, grammar_score, formatting_score, keyword_score, parsed_data
        )
        
        # Generate Suggestions
        suggestions = self._generate_suggestions(
            resume_text, parsed_data, ats_score, skills_analysis
        )
        
        return {
            "ats_score": ats_score,
            "skills": skills_analysis,
            "feedback": feedback,
            "suggestions": suggestions,
            "grammar_score": grammar_score,
            "formatting_score": formatting_score,
            "keyword_score": keyword_score
        }
    
    def _calculate_ats_score(self, text: str) -> float:
        """Calculate ATS compatibility score (0-100)"""
        score = 0.0
        
        # Check for action verbs (30 points)
        action_verb_count = sum(1 for verb in self.action_verbs if verb.lower() in text.lower())
        score += min(action_verb_count * 2, 30)
        
        # Check for quantifiable achievements (20 points)
        achievements = re.findall(r'\b\d+%|\b\d+\s*(million|billion|thousand|k|m)\b', text.lower())
        score += min(len(achievements) * 4, 20)
        
        # Check for sections (25 points)
        sections = ["experience", "education", "skills", "projects"]
        section_count = sum(1 for section in sections if section.lower() in text.lower())
        score += section_count * 6.25
        
        # Check for contact info (15 points)
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        has_phone = bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text))
        if has_email:
            score += 7.5
        if has_phone:
            score += 7.5
        
        # Check for length (10 points)
        word_count = len(text.split())
        if 300 <= word_count <= 800:
            score += 10
        elif 200 <= word_count <= 1000:
            score += 5
        
        return min(score, 100.0)
    
    def _analyze_skills(self, text: str, parsed_data: Dict[str, Any]) -> List[str]:
        """Extract and categorize skills"""
        found_skills = set()
        text_lower = text.lower()
        
        # Extract from parsed data
        if "skills" in parsed_data:
            found_skills.update(parsed_data["skills"])
        
        # Extract from text
        for skill in self.tech_skills:
            if skill.lower() in text_lower:
                found_skills.add(skill)
        
        return list(found_skills)
    
    def _analyze_grammar(self, text: str) -> float:
        """Analyze grammar and clarity (simplified version)"""
        score = 70.0  # Base score
        
        # Check for common grammar issues
        issues = 0
        
        # Check for sentence fragments (very basic)
        sentences = text.split('.')
        short_sentences = sum(1 for s in sentences if len(s.strip()) < 10)
        issues += min(short_sentences * 2, 20)
        
        # Check for repetitive words
        words = text.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Only check longer words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        repetitions = sum(1 for freq in word_freq.values() if freq > 5)
        issues += min(repetitions * 3, 10)
        
        score = max(0, score - issues)
        return min(score, 100.0)
    
    def _analyze_formatting(self, text: str) -> float:
        """Analyze resume formatting"""
        score = 80.0  # Base score
        
        lines = text.split('\n')
        
        # Check for consistent formatting
        issues = 0
        
        # Too many bullet points in one section
        bullet_sections = [line for line in lines if line.strip().startswith('•') or line.strip().startswith('-')]
        if len(bullet_sections) > 20:
            issues += 10
        
        # Inconsistent spacing
        empty_lines = sum(1 for line in lines if not line.strip())
        if empty_lines > len(lines) * 0.3:
            issues += 15
        
        # Very long lines
        long_lines = sum(1 for line in lines if len(line) > 200)
        if long_lines > 5:
            issues += 10
        
        score = max(0, score - issues)
        return min(score, 100.0)
    
    def _analyze_keywords(self, text: str) -> float:
        """Analyze keyword optimization"""
        score = 0.0
        
        text_lower = text.lower()
        
        # ATS keywords (40 points)
        ats_matches = sum(1 for keyword in self.ats_keywords if keyword in text_lower)
        score += min(ats_matches * 2, 40)
        
        # Tech skills (40 points)
        tech_matches = sum(1 for skill in self.tech_skills if skill.lower() in text_lower)
        score += min(tech_matches * 1.5, 40)
        
        # Industry terms (20 points)
        industry_terms = ["stakeholder", "roadmap", "pipeline", "scalable", "robust", "efficient"]
        industry_matches = sum(1 for term in industry_terms if term in text_lower)
        score += min(industry_matches * 4, 20)
        
        return min(score, 100.0)
    
    def _generate_feedback(self, ats_score: float, grammar_score: float, 
                          formatting_score: float, keyword_score: float, 
                          parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured feedback"""
        feedback = {
            "overall_score": (ats_score + grammar_score + formatting_score + keyword_score) / 4,
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        # Strengths
        if ats_score >= 80:
            feedback["strengths"].append("Strong ATS compatibility with good action verbs and quantifiable results")
        if grammar_score >= 80:
            feedback["strengths"].append("Well-written with good grammar and clarity")
        if keyword_score >= 80:
            feedback["strengths"].append("Excellent keyword optimization for ATS systems")
        
        # Weaknesses
        if ats_score < 60:
            feedback["weaknesses"].append("Low ATS compatibility - add more action verbs and quantifiable achievements")
        if grammar_score < 60:
            feedback["weaknesses"].append("Grammar and clarity issues detected")
        if keyword_score < 60:
            feedback["weaknesses"].append("Poor keyword optimization - add more relevant skills and keywords")
        
        # Missing sections
        required_sections = ["experience", "education", "skills"]
        resume_text = str(parsed_data).lower()
        for section in required_sections:
            if section not in resume_text:
                feedback["recommendations"].append(f"Add a {section.title()} section")
        
        return feedback
    
    def _generate_suggestions(self, text: str, parsed_data: Dict[str, Any], 
                             ats_score: float, skills: List[str]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # ATS improvements
        if ats_score < 70:
            suggestions.append("Add more action verbs like 'achieved', 'improved', 'managed' to describe your experience")
            suggestions.append("Include quantifiable achievements with numbers and percentages")
        
        # Skills improvements
        if len(skills) < 5:
            suggestions.append("Add more technical skills to increase keyword relevance")
        
        # Content improvements
        if len(text.split()) < 300:
            suggestions.append("Expand your resume with more detailed descriptions of your experience")
        elif len(text.split()) > 800:
            suggestions.append("Consider condensing your resume to focus on the most relevant experience")
        
        # Section-specific suggestions
        if not parsed_data.get("projects"):
            suggestions.append("Add a projects section to showcase your work")
        
        if not parsed_data.get("certifications"):
            suggestions.append("Include relevant certifications to boost credibility")
        
        # Formatting suggestions
        suggestions.append("Use consistent bullet points and formatting throughout")
        suggestions.append("Ensure your contact information is clearly visible at the top")
        
        return suggestions
    
    def compare_with_job_description(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Compare resume with job description"""
        
        # Extract skills from both
        resume_skills = self._analyze_skills(resume_text, {})
        job_skills = self._analyze_skills(job_description, {})
        
        # Calculate similarity using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            match_score = similarity * 100
        except:
            match_score = 0.0
        
        # Find missing and overlapping skills
        missing_skills = [skill for skill in job_skills if skill not in resume_skills]
        overlapping_skills = [skill for skill in resume_skills if skill in job_skills]
        
        # Generate suggestions
        suggestions = []
        if match_score < 50:
            suggestions.append("Your resume has low match with this job description")
            suggestions.append("Add more keywords from the job description to improve matching")
        
        if missing_skills:
            suggestions.append(f"Consider highlighting or gaining experience in: {', '.join(missing_skills[:5])}")
        
        if not overlapping_skills:
            suggestions.append("Focus on aligning your skills with job requirements")
        
        return {
            "match_score": match_score,
            "missing_skills": missing_skills,
            "overlapping_skills": overlapping_skills,
            "suggestions": suggestions
        }
