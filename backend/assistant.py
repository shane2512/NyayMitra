"""
NyayMitra Assistant - Enhanced PDF Processing & OCR System

This enhanced version efficiently reads PDFs, performs OCR, extracts data,
and sends it to models for legal document analysis.
"""

import os
import sys
import json
import argparse
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import logging
import io

# PDF processing libraries
try:
    import PyPDF2
    import pdfplumber
    import fitz  # PyMuPDF
except ImportError:
    print("Installing required PDF libraries...")
    os.system("pip install PyPDF2 pdfplumber PyMuPDF")

# OCR libraries
try:
    import easyocr
    import cv2
    import numpy as np
    from PIL import Image
except ImportError:
    print("Installing required OCR libraries...")
    os.system("pip install easyocr opencv-python pillow")

# AI/ML libraries
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
except ImportError:
    print("Installing required AI libraries...")
    os.system("pip install transformers torch")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AssistantMeta:
    name: str = "NyayMitraAssistant"
    version: str = "2.0.0"
    description: str = "Enhanced PDF processing, OCR, and legal analysis assistant"


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


class OCRProcessor:
    """Handles OCR processing for images and PDFs"""
    
    def __init__(self):
        try:
            # Initialize EasyOCR with English
            self.reader = easyocr.Reader(['en'])
            logger.info("EasyOCR initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {e}")
            self.reader = None
    
    def process_pdf_pages(self, file_path: str, pages_to_process: Optional[List[int]] = None) -> str:
        """Convert PDF pages to images and perform OCR"""
        if not self.reader:
            return "OCR not available"
        
        try:
            doc = fitz.open(file_path)
            ocr_results = []
            
            # Determine which pages to process
            if pages_to_process is None:
                pages_to_process = range(len(doc))
            
            for page_num in pages_to_process:
                if page_num >= len(doc):
                    continue
                
                page = doc[page_num]
                # Convert page to image
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
                img_data = pix.tobytes("png")
                
                # Convert to PIL Image
                img = Image.open(io.BytesIO(img_data))
                
                # Perform OCR
                results = self.reader.readtext(np.array(img))
                
                # Extract text from results
                page_text = ' '.join([result[1] for result in results])
                ocr_results.append(f"Page {page_num + 1}: {page_text}")
            
            doc.close()
            return '\n'.join(ocr_results)
            
        except Exception as e:
            logger.error(f"OCR processing failed: {e}")
            return f"OCR processing failed: {e}"
    
    def process_image(self, image_path: str) -> str:
        """Perform OCR on a single image"""
        if not self.reader:
            return "OCR not available"
        
        try:
            results = self.reader.readtext(image_path)
            return ' '.join([result[1] for result in results])
        except Exception as e:
            logger.error(f"Image OCR failed: {e}")
            return f"Image OCR failed: {e}"


class LegalAnalyzer:
    """Analyzes legal documents using AI models"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize AI models for legal analysis"""
        try:
            # Initialize a legal document classification model
            model_name = "nlpaueb/legal-bert-base-uncased"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            logger.info("Legal BERT model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load Legal BERT model: {e}")
            # Fallback to rule-based analysis
            self.model = None
    
    def analyze_document(self, document_data: DocumentData) -> List[Dict[str, Any]]:
        """Analyze legal document and return risk assessment"""
        if self.model:
            return self._ai_analysis(document_data)
        else:
            return self._rule_based_analysis(document_data)
    
    def _ai_analysis(self, document_data: DocumentData) -> List[Dict[str, Any]]:
        """Use AI model for analysis"""
        try:
            analyses = []
            for i, clause in enumerate(document_data.extracted_clauses):
                # Tokenize and predict
                inputs = self.tokenizer(clause, return_tensors="pt", truncation=True, max_length=512)
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    probabilities = torch.softmax(outputs.logits, dim=1)
                
                # Simple risk scoring based on model confidence
                risk_score = int((1 - probabilities.max().item()) * 100)
                
                analysis = {
                    "id": i + 1,
                    "clause": clause,
                    "risk_score": risk_score,
                    "color": self._score_color(risk_score),
                    "ai_confidence": float(probabilities.max().item()),
                    "analysis_type": "AI-powered"
                }
                analyses.append(analysis)
            
            return analyses
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._rule_based_analysis(document_data)
    
    def _rule_based_analysis(self, document_data: DocumentData) -> List[Dict[str, Any]]:
        """Fallback to rule-based analysis"""
        analyses = []
        for i, clause in enumerate(document_data.extracted_clauses):
            risk_score = self._heuristic_risk_score(clause)
            analyses.append({
                "id": i + 1,
                "clause": clause,
                "risk_score": risk_score,
                "color": self._score_color(risk_score),
                "analysis_type": "Rule-based",
                "keywords_found": self._extract_keywords(clause)
            })
        return analyses
    
    def _heuristic_risk_score(self, clause: str) -> int:
        """Calculate risk score based on keywords and patterns"""
        score = 10
        c = clause.lower()
        
        # High-risk keywords
        high_risk = ["penalty", "liquidated", "forfeit", "terminate without", "unilateral"]
        for keyword in high_risk:
            if keyword in c:
                score += 30
        
        # Medium-risk keywords
        medium_risk = ["guarantee", "indemn", "arbitration", "waiver", "limitation"]
        for keyword in medium_risk:
            if keyword in c:
                score += 20
        
        # Length penalty
        if len(clause) > 200:
            score += 10
        
        return max(0, min(100, score))
    
    def _score_color(self, score: int) -> str:
        if score >= 75:
            return "red"
        elif score >= 40:
            return "orange"
        else:
            return "green"
    
    def _extract_keywords(self, clause: str) -> List[str]:
        """Extract legal keywords from clause"""
        keywords = []
        legal_terms = [
            "penalty", "liquidated", "damages", "termination", "breach",
            "indemnification", "warranty", "liability", "arbitration",
            "governing law", "jurisdiction", "force majeure"
        ]
        
        for term in legal_terms:
            if term.lower() in clause.lower():
                keywords.append(term)
        
        return keywords


class NyayMitraAssistant:
    """Enhanced legal document analysis assistant"""
    
    def __init__(self):
        self.meta = AssistantMeta()
        self.pdf_processor = PDFProcessor()
        self.ocr_processor = OCRProcessor()
        self.legal_analyzer = LegalAnalyzer()
    
    def info(self) -> Dict[str, Any]:
        return asdict(self.meta)
    
    def process_document(self, file_path: str, use_ocr: bool = True) -> Dict[str, Any]:
        """Main method to process a document end-to-end"""
        try:
            logger.info(f"Starting document processing: {file_path}")
            
            # Extract text from PDF
            document_data = self.pdf_processor.read_pdf(file_path)
            
            # Perform OCR if requested
            if use_ocr:
                logger.info("Performing OCR on document pages...")
                document_data.ocr_text = self.ocr_processor.process_pdf_pages(file_path)
            
            # Analyze legal content
            logger.info("Analyzing legal content...")
            document_data.risk_analysis = self.legal_analyzer.analyze_document(document_data)
            
            # Prepare results
            results = {
                "file_path": file_path,
                "metadata": document_data.metadata,
                "text_extraction": {
                    "pdf_text_length": len(document_data.text_content),
                    "ocr_text_length": len(document_data.ocr_text),
                    "extracted_clauses_count": len(document_data.extracted_clauses)
                },
                "risk_analysis": document_data.risk_analysis,
                "summary": self._generate_summary(document_data),
                "recommendations": self._generate_recommendations(document_data.risk_analysis)
            }
            
            logger.info("Document processing completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            return {"error": str(e), "file_path": file_path}
    
    def _generate_summary(self, document_data: DocumentData) -> Dict[str, Any]:
        """Generate document summary"""
        total_clauses = len(document_data.extracted_clauses)
        high_risk_count = sum(1 for analysis in document_data.risk_analysis if analysis["risk_score"] >= 75)
        medium_risk_count = sum(1 for analysis in document_data.risk_analysis if 40 <= analysis["risk_score"] < 75)
        
        return {
            "total_clauses": total_clauses,
            "high_risk_clauses": high_risk_count,
            "medium_risk_clauses": medium_risk_count,
            "low_risk_clauses": total_clauses - high_risk_count - medium_risk_count,
            "overall_risk_level": "high" if high_risk_count > total_clauses * 0.3 else "medium" if medium_risk_count > total_clauses * 0.3 else "low"
        }
    
    def _generate_recommendations(self, risk_analysis: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on risk analysis"""
        recommendations = []
        
        high_risk_clauses = [a for a in risk_analysis if a["risk_score"] >= 75]
        if high_risk_clauses:
            recommendations.append(f"Review {len(high_risk_clauses)} high-risk clauses carefully")
            recommendations.append("Consider legal consultation for high-risk terms")
        
        medium_risk_clauses = [a for a in risk_analysis if 40 <= a["risk_score"] < 75]
        if medium_risk_clauses:
            recommendations.append(f"Negotiate {len(medium_risk_clauses)} medium-risk clauses")
            recommendations.append("Request modifications for unclear terms")
        
        if not recommendations:
            recommendations.append("Document appears to have standard terms")
            recommendations.append("Review for understanding and compliance")
        
        return recommendations


def main(argv=None):
    parser = argparse.ArgumentParser(description="NyayMitraAssistant - Enhanced PDF Processing & OCR")
    sub = parser.add_subparsers(dest="cmd")
    
    sub.add_parser("info", help="Show assistant metadata")
    
    p_process = sub.add_parser("process", help="Process a PDF document")
    p_process.add_argument("file", help="PDF file path to process")
    p_process.add_argument("--no-ocr", action="store_true", help="Skip OCR processing")
    p_process.add_argument("--output", help="Output JSON file path")
    
    p_ocr = sub.add_parser("ocr", help="Perform OCR on PDF pages")
    p_ocr.add_argument("file", help="PDF file path")
    p_ocr.add_argument("--pages", nargs="+", type=int, help="Specific pages to OCR (0-indexed)")
    
    args = parser.parse_args(argv)
    assistant = NyayMitraAssistant()
    
    if args.cmd == "info":
        print(json.dumps(assistant.info(), indent=2))
        return
    
    if args.cmd == "process":
        results = assistant.process_document(args.file, use_ocr=not args.no_ocr)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2))
        return
    
    if args.cmd == "ocr":
        ocr_text = assistant.ocr_processor.process_pdf_pages(args.file, args.pages)
        print(ocr_text)
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
