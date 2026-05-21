# LLM Resume Screener — Full Setup Guide

## Project Structure

```
resume-screener/
├── backend/
│   ├── main.py          ← FastAPI app (API routes)
│   ├── models.py        ← Pydantic data models
│   ├── parser.py        ← PDF text extraction
│   ├── screener.py      ← Claude AI ranking logic
│   └── requirements.txt ← Python dependencies
├── frontend/
│   └── index.html       ← Full UI (open in browser)
└── README.md
```

---

## How It Works

```
HR uploads PDFs
      ↓
FastAPI receives files + JD
      ↓
PyMuPDF extracts text from PDFs
      ↓
Claude API scores each resume (0–100)
      ↓
Returns ranked list with reasoning
      ↓
Frontend shows results with strengths/gaps
```

---

## Step-by-Step Setup

### Step 1 — Get your Anthropic API key

1. Go to https://console.anthropic.com
2. Create account → API Keys → Create Key
3. Copy the key (starts with `sk-ant-...`)

---

### Step 2 — Create the project folder

Open terminal and run:

```bash
mkdir resume-screener
cd resume-screener
mkdir backend frontend
```

---

### Step 3 — Create backend files

**File 1: backend/requirements.txt**
```
fastapi==0.111.0
uvicorn==0.29.0
python-multipart==0.0.9
anthropic==0.25.0
pymupdf==1.24.3
pydantic==2.7.1
python-dotenv==1.0.1
```

**File 2: backend/models.py**
— Pydantic schemas for request/response types

**File 3: backend/parser.py**
— PDF text extractor using PyMuPDF

**File 4: backend/screener.py**
— Claude API call with structured JSON prompt

**File 5: backend/main.py**
— FastAPI routes: POST /screen, GET /

**File 6: frontend/index.html**
— Full UI, drag-drop upload, results dashboard

(All files provided — copy them exactly as given)

---

### Step 4 — Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

If using Python 3.10+:
```bash
pip3 install -r requirements.txt
```

---

### Step 5 — Set your API key

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-YOUR_KEY_HERE"
```

Optional — create a `.env` file in backend/:
```
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

---

### Step 6 — Run the backend server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

Test it: open http://localhost:8000 in browser
You should see: `{"status":"ok","message":"Resume Screener API running"}`

---

### Step 7 — Open the frontend

Simply open `frontend/index.html` in your browser.

**Mac:**
```bash
open frontend/index.html
```

**Windows:**
```cmd
start frontend/index.html
```

Or just double-click the file in File Explorer / Finder.

---

### Step 8 — Use the app

1. Fill in job title, description, required skills
2. Drag and drop PDF resumes (multiple allowed)
3. Click "Screen Resumes"
4. Backend sends PDFs to Claude → returns ranked results
5. See scores, grades, strengths, gaps, reasoning for each candidate

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | / | Health check |
| POST | /screen | Upload resumes + JD → ranked results |
| POST | /screen-demo | Test with synthetic data (no PDFs) |
| GET | /docs | Swagger UI (auto-generated) |

### Test with curl:
```bash
curl http://localhost:8000/

# Full test with demo data:
curl -X POST http://localhost:8000/screen-demo
```

---

## Scoring System

| Score | Grade | Recommendation |
|-------|-------|----------------|
| 85–100 | A | Shortlist |
| 70–84  | B | Shortlist |
| 55–69  | C | Maybe |
| 40–54  | D | Maybe |
| 0–39   | F | Reject |

---

## Troubleshooting

**"Connection refused" error in frontend:**
→ Backend not running. Run `uvicorn main:app --reload --port 8000`

**"ANTHROPIC_API_KEY not set":**
→ Run `export ANTHROPIC_API_KEY=sk-ant-...` in same terminal as uvicorn

**PDF parse error:**
→ Make sure files are actual PDFs, not renamed images

**CORS error in browser:**
→ Already handled in main.py with allow_origins=["*"]

**Port 8000 in use:**
→ Run `uvicorn main:app --reload --port 8001` and update BACKEND variable in index.html line 1

---

## Extend the Project

| Feature | How |
|---------|-----|
| Save results to DB | Add SQLite with SQLModel in main.py |
| Export to CSV | Add pandas, return CSV endpoint |
| Auth for HR login | Add FastAPI-Users |
| Email shortlisted | Integrate SendGrid API |
| Batch async processing | Use FastAPI BackgroundTasks |
| Deploy | Railway / Render for backend, Vercel for frontend |
