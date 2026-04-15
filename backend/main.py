from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.parser import extract_text_from_file

app = FastAPI(title="Resume Analyzer API", version="0.1.0")

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response Schema
class AnalysisResponse(BaseModel):
    score: int
    skills: list[str]
    missing_skills: list[str]
    extracted_text: str  # For debugging/verification


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Resume Analyzer API"}


@app.get("/test")
def test_route():
    """Test endpoint to verify backend is running"""
    return {"message": "Backend running"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze a resume file
    
    Args:
        file: Resume file (PDF or DOCX)
    
    Returns:
        AnalysisResponse: Score, skills found, and missing skills
    """
    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed"
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size (max 5MB)
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5MB"
        )
    
    # Extract text from file
    try:
        extracted_text = extract_text_from_file(content, file.content_type)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to process resume file"
        )
    
    # Log extracted text (for debugging)
    print(f"\n{'='*60}")
    print(f"Extracted Text from {file.filename}:")
    print(f"{'='*60}")
    print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
    print(f"{'='*60}\n")
    
    # TODO: Implement actual skill extraction and scoring from extracted_text
    # For now, return dummy response with real extracted text
    return AnalysisResponse(
        score=75,
        skills=["Python", "React"],
        missing_skills=["Docker", "AWS"],
        extracted_text=extracted_text  # Include for verification
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
