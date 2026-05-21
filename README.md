# Resume Screener — AI-Powered Candidate Ranking

An intelligent resume screening tool that ranks candidates against a job description using LLM. Built with FastAPI + Groq AI + vanilla HTML frontend.

---

## What It Does

- HR uploads multiple PDF resumes
- System parses and extracts text from each PDF
- Groq AI scores every candidate from 0–100
- Returns ranked results with strengths, skill gaps, and reasoning
- Clean professional UI — no login required

---

## Project Structure

```
resume-screener/
├── index.html           ← Frontend UI (open in browser)
├── backend/
│   ├── main.py          ← FastAPI routes
│   ├── models.py        ← Pydantic data models
│   ├── parser.py        ← PDF text extraction (PyMuPDF)
│   ├── screener.py      ← Groq AI ranking logic
│   └── requirements.txt ← Python dependencies
├── render.yaml          ← Render deployment config
├── .gitignore
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI |
| AI Model | Groq (LLaMA 3.3 70B) |
| PDF Parsing | PyMuPDF |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render (backend), GitHub Pages (frontend) |

---

## How It Works

```
HR uploads PDF resumes + fills Job Description
              ↓
    FastAPI receives files
              ↓
    PyMuPDF extracts text from PDFs
              ↓
    Groq AI scores each resume (0–100)
              ↓
    Results sorted by score (highest first)
              ↓
    Frontend shows ranked candidates with analysis
```

---

## Scoring System

| Score | Grade | Decision |
|-------|-------|----------|
| 85–100 | A | Shortlist |
| 70–84 | B | Shortlist |
| 55–69 | C | Maybe |
| 40–54 | D | Maybe |
| 0–39 | F | Reject |

---

## Local Setup

### Step 1 — Get Groq API Key (Free)
1. Go to → https://console.groq.com
2. Sign up → API Keys → Create Key
3. Copy the key

### Step 2 — Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3 — Set API key

**Windows PowerShell:**
```powershell
$env:GROQ_API_KEY="your_key_here"
```

**Mac/Linux:**
```bash
export GROQ_API_KEY=your_key_here
```

Or create `backend/.env` file:
```
GROQ_API_KEY=your_key_here
```

### Step 4 — Run backend

```bash
python -m uvicorn main:app --reload --port 8000
```

### Step 5 — Open frontend

Double-click `index.html` or open in browser.

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | / | Health check |
| POST | /screen | Upload resumes + JD → ranked results |
| GET | /docs | Swagger UI |

---

## Deployment

**Backend → Render (Free)**
1. Connect GitHub repo on https://render.com
2. Add environment variable: `GROQ_API_KEY`
3. Deploy — auto-detected via `render.yaml`

**Frontend → GitHub Pages**
1. Go to repo Settings → Pages
2. Source: Deploy from branch → main → / (root)
3. Update `BACKEND` URL in `index.html` to your Render URL

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `Connection refused` | Backend not running — start uvicorn |
| `GROQ_API_KEY not set` | Set key in same terminal as uvicorn |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| PDF parse error | Make sure file is a real PDF, not renamed |
| Port 8000 in use | Use `--port 8001`, update `index.html` BACKEND url |

---

## Future Improvements

- Export results to CSV/Excel
- Save screening history to database
- HR login and authentication
- Email shortlisted candidates automatically
- Batch async processing for large resume sets

---

## Author

**Rohit Gaware**
GitHub: [@RohitGaware15](https://github.com/RohitGaware15)
