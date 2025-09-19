import google.generativeai as genai
from typing import Dict, Any, Optional
from config import Config

class SummarizerAgent:
    """
    Serverless-compatible contract summarizer agent.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model_name = Config.GEMINI_MODEL
    
    def generate_summary(self, contract_text: str) -> Dict[str, Any]:
        """
        Generate a concise summary of the contract.
        """
        try:
            print("[Summarizer] Starting summary generation...")
            
            # Validate input
            if not contract_text or len(contract_text.strip()) < 100:
                return {
                    "error": "Insufficient contract text for analysis",
                    "status": "error"
                }
            
            # Truncate if too long (Gemini has token limits)
            max_chars = 30000  # Conservative limit
            if len(contract_text) > max_chars:
                contract_text = contract_text[:max_chars] + "..."
                print(f"[Summarizer] Truncated text to {max_chars} characters")
            
            # Create the prompt for concise summary
            prompt = f"""
            You are a legal expert specializing in contract analysis. Please provide a CONCISE summary of this contract in exactly 200-300 words.

            Focus on these key areas:
            1. Contract Type & Purpose
            2. Key Parties Involved
            3. Main Obligations & Responsibilities
            4. Important Terms & Conditions
            5. Critical Dates & Deadlines
            6. Financial Terms (if any)
            7. Termination Conditions
            8. Notable Risks or Concerns

            Contract Text:
            {contract_text}

            Provide a professional, structured summary that a business person can quickly understand. Be concise but comprehensive.
            """
            
            # Generate summary using Gemini
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            if not response or not response.text:
                return {
                    "error": "Failed to generate summary - empty response from AI",
                    "status": "error"
                }
            
            summary_text = response.text.strip()
            
            # Validate summary length
            word_count = len(summary_text.split())
            if word_count > 400:
                # Truncate if too long
                words = summary_text.split()[:350]
                summary_text = " ".join(words) + "..."
            
            print(f"[Summarizer] Generated summary with {len(summary_text.split())} words")
            
            return {
                "summary": summary_text,
                "word_count": len(summary_text.split()),
                "status": "success"
            }
            
        except Exception as e:
            print(f"[Summarizer] Error generating summary: {e}")
            return {
                "error": f"Summary generation failed: {str(e)}",
                "status": "error"
            }
    
    def extract_key_clauses(self, contract_text: str) -> Dict[str, Any]:
        """
        Extract key clauses from the contract.
        """
        try:
            print("[Summarizer] Extracting key clauses...")
            
            prompt = f"""
            Analyze this contract and extract the most important clauses. 
            Focus on:
            1. Termination clauses
            2. Liability and indemnification
            3. Payment terms
            4. Confidentiality provisions
            5. Dispute resolution
            6. Force majeure
            7. Intellectual property rights
            8. Non-compete or non-disclosure

            For each clause found, provide:
            - Clause type
            - Brief description
            - Potential impact/importance

            Contract Text:
            {contract_text[:20000]}

            Format as a structured list.
            """
            
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            if not response or not response.text:
                return {
                    "error": "Failed to extract clauses",
                    "status": "error"
                }
            
            return {
                "key_clauses": response.text.strip(),
                "status": "success"
            }
            
        except Exception as e:
            print(f"[Summarizer] Error extracting clauses: {e}")
            return {
                "error": f"Clause extraction failed: {str(e)}",
                "status": "error"
            }
