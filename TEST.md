# Quick Test Guide

Fast setup and testing for AI Resume Analyzer.

## One-Command Setup

### Terminal 1 - Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python main.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
```

**Both services running:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

## Test Scenarios

### 1. Test Backend is Running

In browser or using cURL:
```bash
curl http://localhost:8000/test
```

Expected response:
```json
{"message": "Backend running"}
```

---

### 2. Test Frontend Homepage

Open browser: `http://localhost:3000`

Expected:
- "Resume Analyzer" title
- "Start Analysis" button

Click button → should navigate to `/upload`

---

### 3. Test Upload Flow (Manual)

1. Go to http://localhost:3000/upload
2. Click file input
3. Try to upload a non-PDF/non-DOCX file
   - Expected: Error message "Only PDF and DOCX files are allowed"
4. Select a PDF or DOCX file
   - Expected: File name appears below input
5. Click "Analyze Resume"
   - Expected: Button shows loading ("Analyzing...")
   - Expected: Results appear after 1-2 seconds

---

### 4. Test API Directly with cURL

#### Upload PDF
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@C:/path/to/resume.pdf"
```

#### Expected Response
```json
{
  "score": 75,
  "skills": ["Python", "React"],
  "missing_skills": ["Docker", "AWS"]
}
```

---

### 5. Test with Postman

1. **Download Postman** (optional)
2. **Create POST request**
   - URL: `http://localhost:8000/analyze`
   - Body: form-data
   - Key: `file` (type: File)
   - Value: Select a PDF or DOCX file
3. **Send** → See JSON response

---

### 6. Test Error Scenarios

#### Invalid File Type
```bash
# Try uploading .txt file
curl -X POST http://localhost:8000/analyze \
  -F "file=@test.txt"
```

Expected: 400 error
```json
{"detail": "Only PDF and DOCX files are allowed"}
```

#### Missing File
```bash
curl -X POST http://localhost:8000/analyze
```

Expected: 422 error (validation error)

---

## Browser DevTools Testing

### Open Frontend Console (F12)

#### Test file selection
```javascript
// Simulate file selection in browser console
const input = document.querySelector('input[type="file"]')
console.log(input)
```

#### Monitor Network (Network Tab)
1. Open DevTools → Network tab
2. Upload a file
3. Watch POST request to http://localhost:8000/analyze
4. Check response in Response tab

---

## Debug Tips

### Frontend Issues

**Problem**: "Cannot POST http://localhost:8000/analyze"
- **Check**: Backend is running
- **Check**: Correct backend URL in code
- **Check**: CORS is enabled

**Problem**: Loading state never ends
- **Check**: Backend server is responding
- **Check**: Network tab in DevTools
- **Check**: Console for errors

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Activate venv first: `.\venv\Scripts\activate`

**Problem**: Port 8000 already in use
- **Check**: Kill existing process on port 8000
- **Or**: Run on different port: `python main.py --port 8001`

**Problem**: CORS error in frontend
- **Check**: Backend CORS origins include `http://localhost:3000`
- **Check**: Backend is running

---

## Automated Testing (Future)

### Frontend Tests
```bash
npm test  # (Not yet set up)
```

### Backend Tests
```bash
pytest  # (Not yet installed)
```

---

## File Upload Formats

### Valid Files
- PDF documents (`.pdf`)
- Word documents (`.docx`)
- File size: max 5MB

### Invalid Files
- `.txt`, `.doc` (old Word), `.pages`, etc.
- Files larger than 5MB

---

## API Response Structure

All responses contain:

**Success (200)**:
```json
{
  "score": 75,
  "skills": ["Python", "React"],
  "missing_skills": ["Docker", "AWS"]
}
```

**Error (400/422)**:
```json
{
  "detail": "Error message here"
}
```

---

## Performance Notes

- Frontend: Next.js auto-reload on file changes
- Backend: Manual reload (use `uvicorn main:app --reload` for auto-reload)
- File upload: Should complete in <2 seconds

---

## Logs to Watch

### Backend Logs
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
INFO:     POST /analyze
INFO:     Completed request [200 OK]
```

### Frontend Logs (Browser Console)
```
Response: {score: 75, skills: Array(2), missing_skills: Array(2)}
```

---

## Reset & Clean

### Clear Frontend Build
```bash
cd frontend
rm -r .next node_modules
npm install
npm run dev
```

### Clear Backend
```bash
cd backend
rm -r venv __pycache__
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## Next: Adding Real Resume Parsing

Replace dummy response in `backend/main.py`:

```python
# TODO: Implement actual resume parsing
# Currently returns dummy response
```

With actual implementation:
- Extract text from PDF/DOCX
- Parse skills from text
- Calculate actual score
- Return real results
