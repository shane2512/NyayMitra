"""
PDF Processor Module for NyayMitra Assistant

Handles PDF reading, text extraction, and metadata extraction using multiple methods
for maximum compatibility and accuracy.
"""

import os
import logging
from typing import List, Dict, Any
from dataclasses import dataclass

# PDF processing libraries
try:
    import PyPDF2
    import pdfplumber
    import fitz  # PyMuPDF
except ImportError:
    print("Installing required PDF libraries...")
    import subprocess
    subprocess.run(["pip", "install", "PyPDF2", "pdfplumber", "PyMuPDF"], check=True)
    import PyPDF2
    import pdfplumber
    import fitz

logger = logging.getLogger(__name__)


@dataclass
class DocumentData:
    """Structured data extracted from documents"""
    text_content: str
    ocr_text: str
    metadata: Dict[str, Any]
    pages: List[Dict[str, Any]]
    extracted_clauses: List[str]
    risk_analysis: List[Dict[str, Any]]


class PDFProcessor:
    """Handles PDF reading and text extraction"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def read_pdf(self, file_path: str) -> DocumentData:
        """Read PDF and extract text using multiple methods for best results"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        logger.info(f"Processing PDF: {file_path}")
        
        # Extract text using different methods
        text_content = self._extract_text_pypdf2(file_path)
        pdfplumber_text = self._extract_text_pdfplumber(file_path)
        pymupdf_text = self._extract_text_pymupdf(file_path)
        
        # Combine text from different methods
        combined_text = self._combine_text_methods(text_content, pdfplumber_text, pymupdf_text)
        
        # Extract metadata
        metadata = self._extract_metadata(file_path)
        
        # Extract pages
        pages = self._extract_pages(file_path)
        
        # Extract clauses
        extracted_clauses = self._extract_clauses(combined_text)
        
        return DocumentData(
            text_content=combined_text,
            ocr_text="",  # Will be filled by OCR processor
            metadata=metadata,
            pages=pages,
            extracted_clauses=extracted_clauses,
            risk_analysis=[]
        )
    
    def _extract_text_pypdf2(self, file_path: str) -> str:
        """Extract text using PyPDF2"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {e}")
            return ""
    
    def _extract_text_pdfplumber(self, file_path: str) -> str:
        """Extract text using pdfplumber"""
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {e}")
            return ""
    
    def _extract_text_pymupdf(self, file_path: str) -> str:
        """Extract text using PyMuPDF"""
        try:
            text = ""
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            return text
        except Exception as e:
            logger.warning(f"PyMuPDF extraction failed: {e}")
            return ""
    
    def _combine_text_methods(self, *texts: str) -> str:
        """Combine text from different extraction methods"""
        # Remove empty texts and combine
        valid_texts = [t for t in texts if t and t.strip()]
        if not valid_texts:
            return ""
        
        # Use the longest text as base, or combine if they're similar
        if len(valid_texts) == 1:
            return valid_texts[0]
        
        # Simple combination strategy
        combined = "\n".join(valid_texts)
        # Remove duplicate lines
        lines = combined.split('\n')
        unique_lines = []
        seen = set()
        for line in lines:
            line_clean = line.strip()
            if line_clean and line_clean not in seen:
                unique_lines.append(line)
                seen.add(line_clean)
        
        return '\n'.join(unique_lines)
    
    def _extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract PDF metadata"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                info = reader.metadata
                return {
                    'title': info.get('/Title', ''),
                    'author': info.get('/Author', ''),
                    'subject': info.get('/Subject', ''),
                    'creator': info.get('/Creator', ''),
                    'producer': info.get('/Producer', ''),
                    'pages': len(reader.pages),
                    'file_size': os.path.getsize(file_path)
                }
        except Exception as e:
            logger.warning(f"Metadata extraction failed: {e}")
            return {}
    
    def _extract_pages(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract individual page information"""
        try:
            pages = []
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_data = {
                        'page_number': i + 1,
                        'text': page.extract_text() or '',
                        'width': page.width,
                        'height': page.height
                    }
                    pages.append(page_data)
            return pages
        except Exception as e:
            logger.warning(f"Page extraction failed: {e}")
            return []
    
    def _extract_clauses(self, text: str) -> List[str]:
        """Extract legal clauses from text"""
        import re
        
        # Split by common legal document separators
        clause_patterns = [
            r'(?<=\.)\s*(?=[A-Z][a-z])',  # Period followed by capital letter
            r'(?<=\.)\s*(?=\d+\.)',       # Period followed by number
            r'(?<=\.)\s*(?=Section)',     # Period followed by Section
            r'(?<=\.)\s*(?=Article)',     # Period followed by Article
            r'(?<=\.)\s*(?=Clause)',      # Period followed by Clause
        ]
        
        clauses = []
        for pattern in clause_patterns:
            parts = re.split(pattern, text)
            clauses.extend([p.strip() for p in parts if p.strip() and len(p.strip()) > 20])
        
        # Remove duplicates and sort by length
        unique_clauses = list(set(clauses))
        unique_clauses.sort(key=len, reverse=True)
        
        return unique_clauses[:50]  # Limit to top 50 clauses
