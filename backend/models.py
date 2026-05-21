from pydantic import BaseModel
from typing import List, Optional


class JobDescription(BaseModel):
    title: str
    description: str
    required_skills: List[str]
    preferred_skills: Optional[List[str]] = []
    experience_years: Optional[int] = 0


class ResumeResult(BaseModel):
    filename: str
    candidate_name: str
    score: int  # 0-100
    grade: str  # A/B/C/D/F
    strengths: List[str]
    gaps: List[str]
    reasoning: str
    recommendation: str  # "Shortlist" / "Maybe" / "Reject"


class ScreeningResponse(BaseModel):
    job_title: str
    total_resumes: int
    results: List[ResumeResult]
