# API Documentation

## Resume Analyzer API

FastAPI backend for analyzing resumes.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Root Endpoint

**GET** `/`

Returns API information.

**Response:**
```json
{
  "message": "Resume Analyzer API"
}
```

---

### 2. Test Endpoint

**GET** `/test`

Verifies backend is running.

**Response:**
```json
{
  "message": "Backend running"
}
```

---

### 3. Analyze Resume

**POST** `/analyze`

Analyzes a resume file and returns a score, found skills, and missing skills.

**Request:**

- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file` (required): Resume file (PDF or DOCX)
  - Max size: 5MB

**Response:**

```json
{
  "score": 75,
  "skills": ["Python", "React"],
  "missing_skills": ["Docker", "AWS"]
}
```

**Response Schema:**
- `score` (integer): Resume score from 0-100
- `skills` (array): List of skills found in resume
- `missing_skills` (array): List of recommended missing skills

**Error Responses:**

- **400 Bad Request**: Invalid file type or file too large
  ```json
  {
    "detail": "Only PDF and DOCX files are allowed"
  }
  ```

- **400 Bad Request**: File size exceeds limit
  ```json
  {
    "detail": "File size must be less than 5MB"
  }
  ```

- **422 Unprocessable Entity**: Missing file parameter
  ```json
  {
    "detail": [
      {
        "loc": ["body", "file"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

---

## Examples

### Using cURL

```bash
# Test backend
curl http://localhost:8000/test

# Analyze resume
curl -X POST http://localhost:8000/analyze \
  -F "file=@/path/to/resume.pdf"
```

### Using Python

```python
import requests

# Analyze resume
with open('resume.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/analyze',
        files=files
    )
    print(response.json())
```

### Using JavaScript/Fetch

```javascript
const file = document.getElementById('fileInput').files[0]
const formData = new FormData()
formData.append('file', file)

fetch('http://localhost:8000/analyze', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err))
```

---

## File Types

Supported file formats:
- **PDF**: `.pdf` (MIME type: `application/pdf`)
- **Word**: `.docx` (MIME type: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`)

---

## Development Notes

- Currently returns **dummy response** - no actual parsing implemented
- File validation checks type and size only
- Ready for integration with real resume parsing libraries (e.g., PyPDF2, python-docx)

## Future Enhancements

- [ ] Implement actual PDF/DOCX parsing
- [ ] Extract text from document
- [ ] Perform actual skill extraction
- [ ] Calculate real score based on content
- [ ] Store analysis history
- [ ] Add authentication
