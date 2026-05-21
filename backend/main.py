from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json

from models import JobDescription, ScreeningResponse
from parser import extract_text_from_multiple
from screener import screen_all_resumes

app = FastAPI(
    title="LLM Resume Screener",
    description="AI-powered resume ranking using Claude",
    version="1.0.0"
)

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok", "message": "Resume Screener API running"}


@app.post("/screen", response_model=ScreeningResponse)
async def screen_resumes(
    resumes: List[UploadFile] = File(..., description="Upload one or more PDF resumes"),
    job_title: str = Form(...),
    job_description: str = Form(...),
    required_skills: str = Form(..., description="Comma-separated required skills"),
    preferred_skills: str = Form("", description="Comma-separated preferred skills"),
    experience_years: int = Form(0),
):
    """
    Main endpoint: accepts resumes + JD fields, returns ranked results.
    """
    if not resumes:
        raise HTTPException(status_code=400, detail="No resumes uploaded")

    # Parse JD
    jd = JobDescription(
        title=job_title,
        description=job_description,
        required_skills=[s.strip() for s in required_skills.split(",") if s.strip()],
        preferred_skills=[s.strip() for s in preferred_skills.split(",") if s.strip()],
        experience_years=experience_years,
    )

    # Read all PDFs
    file_data = []
    for upload in resumes:
        content = await upload.read()
        file_data.append((upload.filename, content))

    # Extract text
    resume_texts = extract_text_from_multiple(file_data)

    # Screen with Claude
    results = screen_all_resumes(jd, resume_texts)

    return ScreeningResponse(
        job_title=job_title,
        total_resumes=len(results),
        results=results,
    )


@app.post("/screen-demo")
async def screen_demo():
    """
    Demo endpoint with synthetic data — no PDFs needed.
    Tests the Claude integration end-to-end.
    """
    from models import ResumeResult
    from screener import screen_single_resume

    jd = JobDescription(
        title="Senior Python Developer",
        description="Build scalable backend APIs for our fintech platform.",
        required_skills=["Python", "FastAPI", "PostgreSQL", "REST APIs"],
        preferred_skills=["Redis", "Docker", "AWS"],
        experience_years=3,
    )

    demo_resume = """
    John Doe | john@example.com | github.com/johndoe
    
    EXPERIENCE
    Software Engineer @ TechCorp (2021–Present)
    - Built REST APIs using FastAPI and PostgreSQL
    - Deployed services on AWS ECS with Docker
    - Reduced query latency 40% with Redis caching
    
    Junior Developer @ StartupXYZ (2019–2021)
    - Python Django backend for e-commerce platform
    - Wrote unit tests with pytest
    
    SKILLS: Python, FastAPI, Django, PostgreSQL, Redis, Docker, AWS, Git
    EDUCATION: B.Tech Computer Science, 2019
    """

    result = screen_single_resume(jd, "john_doe.pdf", demo_resume)
    return result
