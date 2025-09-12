import fitz  # PyMuPDF for PDF text extraction
import re
import os
import google.generativeai as genai
import json
from .api_optimizer import GeminiAPIOptimizer

from config import Config

class RiskAnalyzerAgent:
    def __init__(self, api_key=None, model_name=None):
        api_key = api_key or Config.GEMINI_API_KEY
        model_name = model_name or Config.GEMINI_MODEL
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.api_optimizer = GeminiAPIOptimizer(api_key, model_name=model_name)

    def extract_text(self, pdf_path):
        """Extract raw text from PDF"""
        print(f"[RiskAnalyzer] Attempting to open PDF: '{pdf_path}'")
        print(f"[RiskAnalyzer] Path type: {type(pdf_path)}")
        print(f"[RiskAnalyzer] Path exists: {os.path.exists(pdf_path)}")
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"[RiskAnalyzer] Error opening PDF: {e}")
            raise FileNotFoundError(f"Could not open {pdf_path}: {e}")
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text

    def split_clauses(self, text):
        """Split contract into clauses"""
        clauses = re.split(r"\n\d+\.|\n- ", text)
        return [c.strip() for c in clauses if len(c.strip()) > 20]

    def analyze_clause(self, clause):
        """Send clause to Gemini AI for real risk analysis with optimization"""
        try:
            prompt = f"""
You are an expert contract risk analyzer. Analyze the following contract clause and provide:

1. Risk Level: High, Medium, or Low
2. Brief analysis explaining the risk factors

Contract Clause:
"{clause}"

Please analyze this clause for:
- Legal liability exposure
- Financial risk
- Operational constraints
- Compliance requirements
- Termination risks
- Indemnification clauses
- Limitation of liability
- Intellectual property issues
- Data protection concerns
- Dispute resolution mechanisms

Respond in this exact JSON format:
{{
    "risk_level": "High|Medium|Low",
    "analysis": "Brief explanation of the risk factors and concerns"
}}

Be strict in your analysis - only mark as Low risk if the clause is truly standard and poses minimal risk.
"""

            print(f"[RiskAnalyzer] Sending clause to Gemini AI: {clause[:100]}...")
            
            # Use optimized API call with retry logic
            response_text = self.api_optimizer.optimized_generate_content(prompt)
            print(f"[RiskAnalyzer] AI Response: {response_text}")
            
            # Parse the JSON response
            try:
                # Clean up the response to extract JSON
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                elif '```' in response_text:
                    response_text = response_text.split('```')[1].split('```')[0]
                
                result = json.loads(response_text.strip())
                
                # Validate the response format
                if 'risk_level' not in result or 'analysis' not in result:
                    raise ValueError("Invalid response format")
                
                # Ensure risk_level is one of the expected values
                if result['risk_level'] not in ['High', 'Medium', 'Low']:
                    result['risk_level'] = 'Medium'  # Default fallback
                
                return result
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"[RiskAnalyzer] Error parsing AI response: {e}")
                # Fallback analysis based on clause content
                return self._fallback_analysis(clause)
                
        except Exception as e:
            print(f"[RiskAnalyzer] Error calling Gemini AI: {e}")
            # Fallback to rule-based analysis
            return self._fallback_analysis(clause)

    def _fallback_analysis(self, clause):
        """Fallback rule-based analysis when AI fails"""
        clause_lower = clause.lower()
        
        # High risk indicators
        high_risk_patterns = [
            'indemnify', 'indemnification', 'hold harmless', 'waive', 'waiver',
            'unlimited liability', 'personal guarantee', 'solely responsible',
            'at your own risk', 'non-compete', 'restraint of trade',
            'exclusive', 'irrevocable', 'perpetual', 'liquidated damages',
            'penalty', 'forfeit', 'termination without cause', 'immediate termination'
        ]
        
        # Medium risk indicators  
        medium_risk_patterns = [
            'reasonable efforts', 'best efforts', 'material breach',
            'cure period', 'payment terms', 'delivery schedule',
            'intellectual property', 'confidentiality', 'warranty',
            'limitation of liability', 'governing law', 'arbitration'
        ]
        
        # Check for high risk patterns
        for pattern in high_risk_patterns:
            if pattern in clause_lower:
                return {
                    "risk_level": "High",
                    "analysis": f"Contains high-risk language: '{pattern}'. This clause may expose significant legal or financial liability."
                }
        
        # Check for medium risk patterns
        for pattern in medium_risk_patterns:
            if pattern in clause_lower:
                return {
                    "risk_level": "Medium", 
                    "analysis": f"Contains moderate-risk terms: '{pattern}'. Review recommended to ensure acceptable terms."
                }
        
        # Default to low risk if no patterns match
        return {
            "risk_level": "Low",
            "analysis": "Standard contractual language with minimal apparent risk factors."
        }

    def analyze_contract(self, pdf_path):
        """Main method to analyze entire contract using optimized batch processing"""
        print(f"[RiskAnalyzer] Starting optimized analysis of: {pdf_path}")
        
        # Extract text from PDF
        text = self.extract_text(pdf_path)
        print(f"[RiskAnalyzer] Extracted {len(text)} characters of text")
        
        # Split into clauses
        clauses = self.split_clauses(text)
        substantial_clauses = [clause for clause in clauses if len(clause.strip()) > 50]
        print(f"[RiskAnalyzer] Found {len(substantial_clauses)} substantial clauses for analysis")
        
        if not substantial_clauses:
            print("[RiskAnalyzer] No substantial clauses found")
            return {}
        
        # Use batch processing to analyze all clauses in fewer API calls
        try:
            print(f"[RiskAnalyzer] Using batch processing for {len(substantial_clauses)} clauses...")
            batch_results = self.api_optimizer.batch_analyze_clauses(substantial_clauses, "risk")
            
            # Add original clause text to results
            for i, (clause_id, result) in enumerate(batch_results.items()):
                if i < len(substantial_clauses):
                    original_clause = substantial_clauses[i]
                    result["text"] = original_clause[:500] + "..." if len(original_clause) > 500 else original_clause
            
            print(f"[RiskAnalyzer] Batch analysis completed for {len(batch_results)} clauses")
            return batch_results
            
        except Exception as e:
            print(f"[RiskAnalyzer] Batch processing failed: {e}, falling back to individual analysis")
            # Fallback to individual analysis with rate limiting
            return self._analyze_clauses_individually(substantial_clauses)
    
    def _analyze_clauses_individually(self, clauses):
        """Fallback method for individual clause analysis with rate limiting"""
        analysis_results = {}
        for i, clause in enumerate(clauses, 1):
            clause_id = f"Clause {i}"
            print(f"[RiskAnalyzer] Analyzing {clause_id} individually...")
            
            try:
                analysis = self.analyze_clause(clause)
                analysis_results[clause_id] = {
                    "text": clause[:500] + "..." if len(clause) > 500 else clause,
                    "analysis": analysis
                }
            except Exception as e:
                print(f"[RiskAnalyzer] Error analyzing {clause_id}: {e}")
                analysis_results[clause_id] = {
                    "text": clause[:500] + "..." if len(clause) > 500 else clause,
                    "analysis": self._fallback_analysis(clause)
                }
        
        return analysis_results