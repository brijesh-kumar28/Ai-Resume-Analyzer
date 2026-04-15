# Resume Parser Service

Real resume text extraction from PDF and DOCX files.

## Overview

The parser service handles extracting plain text from resume files for further analysis and processing.

## Files

```
backend/
├── services/
│   ├── __init__.py
│   └── parser.py          # Text extraction functions
└── main.py                # Updated to use parser
```

## Functions

### `extract_text_from_pdf(file_bytes: bytes) -> str`

Extracts text from a PDF file.

**Parameters:**
- `file_bytes` (bytes): PDF file content

**Returns:**
- `str`: Extracted text from all pages

**Raises:**
- `ValueError`: If PDF is invalid or has no extractable text

**Example:**
```python
from services.parser import extract_text_from_pdf

with open('resume.pdf', 'rb') as f:
    pdf_bytes = f.read()
    text = extract_text_from_pdf(pdf_bytes)
    print(text)
```

---

### `extract_text_from_docx(file_bytes: bytes) -> str`

Extracts text from a DOCX (Word) file.

**Parameters:**
- `file_bytes` (bytes): DOCX file content

**Returns:**
- `str`: Extracted text from all paragraphs

**Raises:**
- `ValueError`: If DOCX is invalid or has no extractable text

**Example:**
```python
from services.parser import extract_text_from_docx

with open('resume.docx', 'rb') as f:
    docx_bytes = f.read()
    text = extract_text_from_docx(docx_bytes)
    print(text)
```

---

### `extract_text_from_file(file_bytes: bytes, file_type: str) -> str`

Extracts text from a file based on MIME type.

**Parameters:**
- `file_bytes` (bytes): File content
- `file_type` (str): MIME type of file

**Returns:**
- `str`: Extracted text

**Raises:**
- `ValueError`: If file type is unsupported

**Supported MIME Types:**
- `application/pdf` → PDF files
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document` → DOCX files

**Example:**
```python
from services.parser import extract_text_from_file

file_bytes = b'...'  # File content
mime_type = 'application/pdf'
text = extract_text_from_file(file_bytes, mime_type)
```

---

## Dependencies

### New Libraries

**pdfplumber** (v0.10.3)
- Extracts text from PDF files
- Handles multi-page PDFs
- Robust PDF parsing

**python-docx** (v0.8.11)
- Extracts text from DOCX files
- Reads all paragraphs
- Supports formatted Word documents

### Installation

```bash
pip install -r requirements.txt
```

Or individually:
```bash
pip install pdfplumber==0.10.3
pip install python-docx==0.8.11
```

---

## Updated API Response

### POST `/analyze`

Now includes extracted text in response (for verification).

**Response:**
```json
{
  "score": 75,
  "skills": ["Python", "React"],
  "missing_skills": ["Docker", "AWS"],
  "extracted_text": "John Doe\nSoftware Engineer\n..."
}
```

New field:
- `extracted_text` (string): Full text extracted from resume (for debugging/verification)

---

## Error Handling

### PDF Extraction Errors

- **Invalid PDF**: Catches malformed PDF files
- **No Pages**: Detects PDFs with no pages
- **No Text**: Returns error if PDF has no extractable text

### DOCX Extraction Errors

- **Invalid DOCX**: Catches malformed Word documents
- **No Content**: Returns error if DOCX has no extractable text

### Custom Error Messages

All errors are wrapped in `ValueError` with descriptive messages:
```
"Failed to extract text from PDF: ..."
"Failed to extract text from DOCX: ..."
"Unsupported file type: ..."
```

---

## Implementation Details

### PDF Extraction

1. Opens PDF from bytes using `io.BytesIO`
2. Uses `pdfplumber.open()` to read PDF
3. Iterates through all pages
4. Extracts text from each page using `page.extract_text()`
5. Combines text from all pages with newlines

### DOCX Extraction

1. Opens DOCX from bytes using `io.BytesIO`
2. Uses `Document()` to read DOCX
3. Iterates through all paragraphs
4. Extracts text from each paragraph
5. Combines text with newlines
6. Skips empty paragraphs

---

## Testing

### Test with cURL

```bash
# Test PDF upload
curl -X POST http://localhost:8000/analyze \
  -F "file=@resume.pdf"

# Test DOCX upload
curl -X POST http://localhost:8000/analyze \
  -F "file=@resume.docx"
```

### Backend Console Output

When analyzing a file, the backend prints:

```
============================================================
Extracted Text from resume.pdf:
============================================================
[First 500 characters of extracted text...]
============================================================
```

This helps verify the extraction is working correctly.

---

## Console/Terminal Output Example

```
Extracted Text from john_doe_resume.pdf:
============================================================
JOHN DOE
Software Engineer

EXPERIENCE
Senior Backend Engineer at TechCorp (2021-2024)
- Developed Python REST APIs using FastAPI
- Managed PostgreSQL databases
- Implemented microservices architecture

SKILLS
Python, FastAPI, React, Docker, PostgreSQL, AWS

EDUCATION
Bachelor of Science in Computer Science
University of California (2020)
============================================================
```

---

## Architecture

### Separation of Concerns

**services/parser.py**
- Pure text extraction logic
- No I/O or networking
- Reusable functions
- Type hints for clarity

**main.py**
- API endpoint handling
- File validation
- Error wrapping for HTTP
- Response formatting

### Why This Structure?

1. **Reusability** - Parser can be used elsewhere without FastAPI
2. **Testing** - Easy to unit test parser functions
3. **Maintainability** - Clear separation of concerns
4. **Scalability** - Easy to add new extraction methods

---

## Future Enhancements

### Text Cleaning

```python
# Remove extra whitespace
text = ' '.join(text.split())

# Remove special characters
import re
text = re.sub(r'[^\w\s]', '', text)
```

### Text Preprocessing

- Case normalization
- Tokenization
- Stop word removal
- Lemmatization

### Caching

- Cache extracted text to avoid re-extraction
- Store in database for history

### OCR Support

- For scanned PDFs without selectable text
- Use library: `pytesseract` or `paddleocr`

---

## Common Issues

### Issue: "No module named 'pdfplumber'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Empty extracted text

**Possible causes**:
- Scanned PDF (no selectable text)
- Encrypted PDF
- DOCX with only images/tables

**Solution**: Check file format, might need OCR

### Issue: Garbled text from PDF

**Possible causes**:
- PDF encoding issues
- Font not embedded

**Solution**: Re-export PDF from source

---

## Performance Notes

- PDF extraction: ~100-500ms per page (depends on size)
- DOCX extraction: ~10-50ms (usually faster)
- File size max: 5MB (enforced at API level)

---

## Code Example: Using Parser Directly

```python
from services.parser import extract_text_from_pdf, extract_text_from_docx

# PDF
pdf_content = open('resume.pdf', 'rb').read()
text = extract_text_from_pdf(pdf_content)
print(f"Extracted {len(text)} characters from PDF")

# DOCX
docx_content = open('resume.docx', 'rb').read()
text = extract_text_from_docx(docx_content)
print(f"Extracted {len(text)} characters from DOCX")

# Generic
file_content = open('resume.pdf', 'rb').read()
text = extract_text_from_file(file_content, 'application/pdf')
```

---

## Next Steps

1. **Skill Extraction** - Parse extracted text for skills
2. **Job Matching** - Match skills to job descriptions
3. **Scoring Algorithm** - Calculate resume score
4. **Feedback** - Generate improvement suggestions

---

## References

- **pdfplumber**: https://github.com/jsvine/pdfplumber
- **python-docx**: https://github.com/python-openxml/python-docx
- **FastAPI File Upload**: https://fastapi.tiangolo.com/tutorial/request-files/
