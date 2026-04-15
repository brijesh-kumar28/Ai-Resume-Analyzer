# Backend Development Guide

## Overview

FastAPI backend for AI Resume Analyzer with file upload handling and CORS support.

## Project Structure

```
backend/
├── services/
│   ├── __init__.py
│   └── parser.py           # Resume text extraction
├── main.py                 # Main app with all endpoints
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── README.md               # Backend setup guide
└── PARSER.md               # Parser service documentation
```

## Dependencies

See `requirements.txt`:
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **python-multipart** - File upload support
- **python-dotenv** - Environment variables
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX text extraction

## Architecture

### Main Components

**FastAPI App** (`main.py`)
- CORS middleware configuration
- Response schemas with Pydantic
- Three endpoints: `/`, `/test`, `/analyze`
- Error handling

### Endpoints

#### 1. GET `/`
Root endpoint - returns API info

#### 2. GET `/test`
Test endpoint - verifies backend is running

#### 3. POST `/analyze`
Main endpoint for resume analysis

**Request**:
- Multipart form data with `file` field
- Accepted types: PDF, DOCX
- Max size: 5MB

**Validation**:
```python
- File type validation (allowed MIME types)
- File size validation (max 5MB)
- Raises HTTPException for invalid files
```

**Response** (AnalysisResponse schema):
```python
class AnalysisResponse(BaseModel):
    score: int
    skills: list[str]
    missing_skills: list[str]
```

**Currently Returns** (dummy response):
```json
{
  "score": 75,
  "skills": ["Python", "React"],
  "missing_skills": ["Docker", "AWS"]
}
```

## Code Structure

### Imports
```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
```

### CORS Configuration
```python
origins = [
    "http://localhost:3000",  # Frontend
    "http://localhost:8000",  # API docs
]
app.add_middleware(CORSMiddleware, ...)
```

### Validation Logic
```python
# File type validation
allowed_types = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

# File size validation (5MB max)
if len(content) > 5 * 1024 * 1024:
    raise HTTPException(status_code=400, ...)
```

### Text Extraction

The `analyze_resume` endpoint now:
1. Validates file type and size
2. Reads file content
3. Calls `extract_text_from_file()` from parser service
4. Logs extracted text (first 500 chars)
5. Returns response with extracted_text included

**Parser Service** (`services/parser.py`):
```python
def extract_text_from_file(file_bytes: bytes, file_type: str) -> str:
    # Routes to PDF or DOCX extraction function
    if file_type == "application/pdf":
        return extract_text_from_pdf(file_bytes)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file_bytes)
```

## Setup & Installation

### Create Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Server

```bash
# Basic run
python main.py

# With auto-reload (development)
uvicorn main:app --reload

# Specify host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing

### Using cURL

```bash
# Test endpoint
curl http://localhost:8000/test

# Analyze resume
curl -X POST http://localhost:8000/analyze \
  -F "file=@/path/to/resume.pdf"
```

### Using Python

```python
import requests

# Test
response = requests.get('http://localhost:8000/test')
print(response.json())

# Upload
with open('resume.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/analyze',
        files=files
    )
    print(response.json())
```

### Using Browser

1. Navigate to `http://localhost:8000/docs` (Swagger UI)
2. Click "Try it out" on `/analyze` endpoint
3. Upload a file using the interface

### FastAPI Auto-Generated Docs

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Error Handling

### Invalid File Type
```
Status: 400
Message: "Only PDF and DOCX files are allowed"
```

### File Too Large
```
Status: 400
Message: "File size must be less than 5MB"
```

### Missing File Parameter
```
Status: 422
Message: Field validation error
```

## Development Workflow

### Adding New Endpoint

1. Define request/response schema (if needed)
```python
class MyRequest(BaseModel):
   Current Features (v0.2)

### Text Extraction ✅
- PDF text extraction using **pdfplumber**
- DOCX text extraction using **python-docx**
- Multi-page PDF support
- Error handling for invalid files
- Extracted text returned in API response

### Output
```json
{
  "score": 75,
  "skills": ["Python", "React"],
  "missing_skills": ["Docker", "AWS"],
  "extracted_text": "Full resume text here..."
}
```

---

## Future Enhancement Ideas # Logic here
    return {"result": "data"}
```

3. Test with docs at `/docs`

### Adding Dependencies

1. Install package: `pip install package-name`
2.Next phase: Extract skills from extracted_text
# Will need: NLP library or skill database
from sklearn.feature_extraction.text import TfidfVectorizer
# or use spacy for better NLP
import spacy

## Future Enhancement Ideas

### Resume Parsing
```python
# Will need: PyPDF2, python-docx, or pypdf
import PyPDF2
import docx
```

### Skill Extraction
```python
# Will need: NLP library or vector database
from sklearn.feature_extraction.text import TfidfVectorizer
```

### Database Integration
```python
# Will need: SQLAlchemy, databases
from sqlalchemy import create_engine
```

### Authentication
```python
# Will need: python-jose, passlib
from jose import JWTError
from fastapi.security import HTTPBearer
```

## File Allowed MIME Types

- **PDF**: `application/pdf`
- **DOCX**: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`

## Environment Variables

Copy `.env.example` to `.env` and fill in values:
```
DATABASE_URL=
API_KEY=
```

## Production Deployment

### Before Deployment

- [ ] Update CORS origins to production URLs
- [ ] Set `debug=False` in FastAPI
- [ ] Use environment variables for sensitive data
- [ ] Set up logging
- [ ] Add rate limiting
- [ ] Add authentication

### Deployment Options

- Heroku, Railway, Render (easy)
- AWS Lambda, Google Cloud Run (serverless)
- DigitalOcean, Linode (traditional)

## Performance Tips

- Implement file streaming for large files
- Add caching for repeated analyses
- Use async operations where possible
- Implement request timeouts
- Add database indexing
