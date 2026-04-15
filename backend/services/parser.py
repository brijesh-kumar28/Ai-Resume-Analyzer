"""
Resume text extraction service.

Handles extracting text from PDF and DOCX files.
"""

import io
import pdfplumber
from docx import Document


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from PDF file.
    
    Args:
        file_bytes: PDF file content as bytes
        
    Returns:
        Extracted text from PDF
        
    Raises:
        ValueError: If PDF is invalid or empty
    """
    try:
        # Open PDF from bytes
        pdf_file = io.BytesIO(file_bytes)
        
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            if len(pdf.pages) == 0:
                raise ValueError("PDF has no pages")
            
            # Extract text from all pages
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if not text.strip():
            raise ValueError("No text found in PDF")
        
        return text.strip()
    
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extract text from DOCX file.
    
    Args:
        file_bytes: DOCX file content as bytes
        
    Returns:
        Extracted text from DOCX
        
    Raises:
        ValueError: If DOCX is invalid or empty
    """
    try:
        # Open DOCX from bytes
        docx_file = io.BytesIO(file_bytes)
        doc = Document(docx_file)
        
        # Extract text from all paragraphs
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
        
        if not text.strip():
            raise ValueError("No text found in DOCX")
        
        return text.strip()
    
    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")


def extract_text_from_file(file_bytes: bytes, file_type: str) -> str:
    """
    Extract text from file based on file type.
    
    Args:
        file_bytes: File content as bytes
        file_type: MIME type of file (application/pdf or word document)
        
    Returns:
        Extracted text from file
        
    Raises:
        ValueError: If file type is unsupported or extraction fails
    """
    if file_type == "application/pdf":
        return extract_text_from_pdf(file_bytes)
    
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file_bytes)
    
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
