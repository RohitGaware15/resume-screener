from groq import Groq
import json
import os
from models import JobDescription, ResumeResult
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])


def build_prompt(jd: JobDescription, resume_text: str, filename: str) -> str:
    return f"""You are an expert HR recruiter. Evaluate this resume against the job description.

JOB TITLE: {jd.title}
DESCRIPTION: {jd.description}
REQUIRED SKILLS: {", ".join(jd.required_skills)}
PREFERRED SKILLS: {", ".join(jd.preferred_skills or [])}
EXPERIENCE REQUIRED: {jd.experience_years}+ years

RESUME ({filename}):
{resume_text[:4000]}

Return ONLY a JSON object, no markdown, no extra text:
{{
  "candidate_name": "name from resume or Unknown",
  "score": <0-100>,
  "grade": "<A|B|C|D|F>",
  "strengths": ["str1", "str2", "str3"],
  "gaps": ["gap1", "gap2"],
  "reasoning": "2-3 sentences explaining score",
  "recommendation": "<Shortlist|Maybe|Reject>"
}}

Score guide: 85-100=A=Shortlist, 70-84=B=Shortlist, 55-69=C=Maybe, 40-54=D=Maybe, 0-39=F=Reject"""


def screen_single_resume(jd: JobDescription, filename: str, resume_text: str) -> ResumeResult:
    prompt = build_prompt(jd, resume_text, filename)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.replace("```json", "").replace("```", "").strip()

    data = json.loads(raw)

    return ResumeResult(
        filename=filename,
        candidate_name=data.get("candidate_name", "Unknown"),
        score=int(data.get("score", 0)),
        grade=data.get("grade", "F"),
        strengths=data.get("strengths", []),
        gaps=data.get("gaps", []),
        reasoning=data.get("reasoning", ""),
        recommendation=data.get("recommendation", "Reject")
    )


def screen_all_resumes(jd, resume_texts):
    results = []
    for filename, text in resume_texts:
        if text.startswith("[ERROR"):
            results.append(ResumeResult(
                filename=filename,
                candidate_name="Unknown",
                score=0, grade="F",
                strengths=[],
                gaps=["Could not parse PDF"],
                reasoning="PDF extraction failed.",
                recommendation="Reject"
            ))
        else:
            result = screen_single_resume(jd, filename, text)
            results.append(result)

    results.sort(key=lambda r: r.score, reverse=True)
    return results