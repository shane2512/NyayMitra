import os
import time
from typing import Dict, Any, Optional
import google.generativeai as genai
from .rate_limiter import ServerlessRateLimiter
from .summarizer import SummarizerAgent
from .risk_analyzer import RiskAnalyzerAgent
from .translator import TranslatorAgent
from config import Config

class ModeratorAgent:
    """
    Serverless-compatible moderator agent that orchestrates contract analysis.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        
        # Initialize sub-agents
        self.summarizer = SummarizerAgent(self.api_key)
        self.risk_analyzer = RiskAnalyzerAgent(self.api_key)
        self.translator = TranslatorAgent(self.api_key)
        self.rate_limiter = ServerlessRateLimiter()
        
        self.model_name = Config.GEMINI_MODEL
    
    def analyze_contract(self, pdf_path: str) -> Dict[str, Any]:
        """
        Analyze a contract PDF and return comprehensive analysis.
        """
        try:
            print(f"[Moderator] Starting analysis of: {pdf_path}")
            
            # Extract text from PDF
            contract_text = self._extract_pdf_text(pdf_path)
            if not contract_text or len(contract_text.strip()) < 100:
                return {
                    "error": "Could not extract sufficient text from PDF. Please ensure the PDF contains readable text.",
                    "status": "error"
                }
            
            print(f"[Moderator] Extracted {len(contract_text)} characters from PDF")
            
            # Perform analysis with rate limiting
            analysis_results = {}
            
            # 1. Generate summary
            try:
                summary_result = self.rate_limiter.execute_with_rate_limit(
                    self.summarizer.generate_summary, contract_text
                )
                analysis_results["summary"] = summary_result
                print("[Moderator] Summary generated successfully")
            except Exception as e:
                print(f"[Moderator] Summary generation failed: {e}")
                analysis_results["summary"] = {
                    "error": f"Summary generation failed: {str(e)}",
                    "status": "error"
                }
            
            # 2. Analyze risks
            try:
                risk_result = self.rate_limiter.execute_with_rate_limit(
                    self.risk_analyzer.analyze_risks, contract_text
                )
                analysis_results["risks"] = risk_result
                print("[Moderator] Risk analysis completed successfully")
            except Exception as e:
                print(f"[Moderator] Risk analysis failed: {e}")
                analysis_results["risks"] = {
                    "error": f"Risk analysis failed: {str(e)}",
                    "status": "error"
                }
            
            # 3. Overall status
            if analysis_results.get("summary", {}).get("status") == "success" or \
               analysis_results.get("risks", {}).get("status") == "success":
                analysis_results["status"] = "success"
                analysis_results["message"] = "Contract analysis completed"
            else:
                analysis_results["status"] = "partial_success"
                analysis_results["message"] = "Some analysis components failed"
            
            return analysis_results
            
        except Exception as e:
            print(f"[Moderator] Analysis failed: {e}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "status": "error"
            }
    
    def analyze_contract_with_translation(self, pdf_path: str, language: str = "en", 
                                        interests: Optional[list] = None) -> Dict[str, Any]:
        """
        Analyze contract with translation support.
        """
        try:
            # First perform standard analysis
            analysis_result = self.analyze_contract(pdf_path)
            
            if analysis_result.get("status") == "error":
                return analysis_result
            
            # If language is not English, add translation
            if language != "en":
                try:
                    contract_text = self._extract_pdf_text(pdf_path)
                    translation_result = self.rate_limiter.execute_with_rate_limit(
                        self.translator.translate_summary, 
                        contract_text, language, interests or []
                    )
                    analysis_result["translation"] = translation_result
                    print(f"[Moderator] Translation to {language} completed")
                except Exception as e:
                    print(f"[Moderator] Translation failed: {e}")
                    analysis_result["translation"] = {
                        "error": f"Translation failed: {str(e)}",
                        "status": "error"
                    }
            
            return analysis_result
            
        except Exception as e:
            print(f"[Moderator] Translation analysis failed: {e}")
            return {
                "error": f"Translation analysis failed: {str(e)}",
                "status": "error"
            }
    
    def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF file using PyPDF2."""
        try:
            import PyPDF2
            
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            
            return text.strip()
            
        except Exception as e:
            print(f"[Moderator] PDF extraction failed: {e}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def validate_contract_text(self, text: str) -> Dict[str, Any]:
        """Validate if the extracted text looks like a contract."""
        if not text or len(text.strip()) < 100:
            return {
                "valid": False,
                "reason": "Insufficient text content"
            }
        
        # Check for common contract keywords
        contract_keywords = [
            "agreement", "contract", "party", "parties", "terms", "conditions",
            "obligations", "rights", "liability", "termination", "clause"
        ]
        
        text_lower = text.lower()
        keyword_count = sum(1 for keyword in contract_keywords if keyword in text_lower)
        
        if keyword_count < 3:
            return {
                "valid": False,
                "reason": "Text does not appear to be a legal contract"
            }
        
        return {
            "valid": True,
            "keyword_matches": keyword_count
        }
