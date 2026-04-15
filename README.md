# AI Resume Analyzer Platform

A monorepo containing the frontend and backend for an AI-powered resume analysis platform.

## Project Structure

```
Ai-Resume-Analyzer/
├── frontend/              # Next.js 14 frontend
│   ├── app/
│   │   ├── page.tsx      # Home page with Start Analysis button
│   │   ├── upload/       # Upload page
│   │   │   └── page.tsx  # Resume upload form
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
├── backend/              # FastAPI backend
│   ├── main.py          # API with /analyze endpoint
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## Features

### Frontend
- ✅ Home page with navigation to upload
- ✅ Resume upload page with file input (PDF, DOCX)
- ✅ File validation and error handling
- ✅ Loading state during analysis
- ✅ Results display with:
  - Score (0-100)
  - Skills found
  - Missing skills
- ✅ Tailwind CSS styling

### Backend
- ✅ POST `/analyze` endpoint for resume analysis
- ✅ File upload handling with validation
- ✅ Error handling for invalid files
- ✅ Dummy response (ready for real parsing)
- ✅ CORS middleware configured

## Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs on `http://localhost:3000`

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# OR run with auto-reload
uvicorn main:app --reload
```

Backend runs on `http://localhost:8000`

## Running Both Services

**Terminal 1 (Frontend):**
```bash
cd frontend
npm run dev
```

**Terminal 2 (Backend):**
```bash
cd backend
.\venv\Scripts\activate  # Windows activation
pip install -r requirements.txt
python main.py
```

Visit `http://localhost:3000` to see the frontend.

## API Endpoints

### Backend Routes

- `GET /` - Root endpoint
- `GET /test` - Test endpoint
- `POST /analyze` - Analyze resume file
  - **Body**: Multipart form data with `file` field
  - **Accepts**: PDF (.pdf), Word (.docx)
  - **Response**:
    ```json
    {
      "score": 75,
      "skills": ["Python", "React"],
      "missing_skills": ["Docker", "AWS"]
    }
    ```

## Testing

1. **Start both services** (see Running Both Services section)
2. **Visit frontend**: http://localhost:3000
3. **Click "Start Analysis"** or navigate to `/upload`
4. **Upload a resume file** (PDF or DOCX)
5. **View results** with score and skills

### Test API with cURL

```bash
# Test backend is running
curl http://localhost:8000/test

# Test file upload (replace path/to/resume.pdf)
curl -X POST http://localhost:8000/analyze \
  -F "file=@path/to/resume.pdf"
```

## Development

- **Frontend**: Auto-reload via Next.js hot reload
- **Backend**: Install uvicorn reload with `uvicorn main:app --reload`

## Code Structure

### Frontend (`frontend/app/`)
- `page.tsx` - Home page with navigation
- `upload/page.tsx` - Upload form with:
  - File input with validation
  - Loading state management
  - Result display with score, skills, missing_skills

### Backend (`backend/main.py`)
- FastAPI app with CORS middleware
- `/analyze` endpoint that:
  - Validates file type (PDF, DOCX)
  - Validates file size (max 5MB)
  - Returns dummy analysis response

## Next Steps (Future)

- [ ] Implement real resume parsing (PDF/DOCX extraction)
- [ ] Add actual skill extraction logic
- [ ] Integrate with ML model for resume analysis
- [ ] Database integration for storing results
- [ ] User authentication and history
- [ ] Advanced analytics dashboard
- [ ] Export results as PDF
