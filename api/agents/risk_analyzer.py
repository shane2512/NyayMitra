import google.generativeai as genai
from typing import Dict, Any, Optional, List
from config import Config

class RiskAnalyzerAgent:
    """
    Serverless-compatible risk analyzer agent for contract analysis.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model_name = Config.GEMINI_MODEL
    
    def analyze_risks(self, contract_text: str) -> Dict[str, Any]:
        """
        Analyze potential risks in the contract.
        """
        try:
            print("[RiskAnalyzer] Starting risk analysis...")
            
            # Validate input
            if not contract_text or len(contract_text.strip()) < 100:
                return {
                    "error": "Insufficient contract text for risk analysis",
                    "status": "error"
                }
            
            # Truncate if too long
            max_chars = 25000
            if len(contract_text) > max_chars:
                contract_text = contract_text[:max_chars] + "..."
            
            # Create risk analysis prompt
            prompt = f"""
            You are a legal risk assessment expert. Analyze this contract and identify potential risks and concerns.

            Please categorize risks into:

            1. HIGH RISK (Critical issues that could cause significant problems):
               - Unfavorable termination clauses
               - Excessive liability exposure
               - Unclear payment terms
               - Missing force majeure protections
               - Problematic intellectual property clauses

            2. MEDIUM RISK (Important issues to address):
               - Ambiguous language
               - Missing standard protections
               - Potentially unfavorable terms
               - Compliance concerns

            3. LOW RISK (Minor issues for consideration):
               - Formatting inconsistencies
               - Minor ambiguities
               - Standard but noteworthy clauses

            For each risk identified, provide:
            - Risk level (High/Medium/Low)
            - Description of the risk
            - Potential impact
            - Recommended action

            Contract Text:
            {contract_text}

            Provide a structured analysis focusing on actionable insights.
            """
            
            # Generate risk analysis
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            if not response or not response.text:
                return {
                    "error": "Failed to generate risk analysis - empty response",
                    "status": "error"
                }
            
            risk_analysis = response.text.strip()
            
            # Parse and structure the response
            structured_risks = self._parse_risk_analysis(risk_analysis)
            
            print(f"[RiskAnalyzer] Identified {len(structured_risks.get('high_risks', []))} high risks")
            
            return {
                "risk_analysis": risk_analysis,
                "structured_risks": structured_risks,
                "risk_summary": self._generate_risk_summary(structured_risks),
                "status": "success"
            }
            
        except Exception as e:
            print(f"[RiskAnalyzer] Error analyzing risks: {e}")
            return {
                "error": f"Risk analysis failed: {str(e)}",
                "status": "error"
            }
    
    def _parse_risk_analysis(self, analysis_text: str) -> Dict[str, List[str]]:
        """
        Parse the risk analysis text into structured categories.
        """
        try:
            lines = analysis_text.split('\n')
            current_category = None
            structured = {
                'high_risks': [],
                'medium_risks': [],
                'low_risks': []
            }
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect category headers
                if 'HIGH RISK' in line.upper():
                    current_category = 'high_risks'
                elif 'MEDIUM RISK' in line.upper():
                    current_category = 'medium_risks'
                elif 'LOW RISK' in line.upper():
                    current_category = 'low_risks'
                elif current_category and line.startswith('-'):
                    # Add risk item to current category
                    structured[current_category].append(line[1:].strip())
            
            return structured
            
        except Exception:
            # If parsing fails, return empty structure
            return {
                'high_risks': [],
                'medium_risks': [],
                'low_risks': []
            }
    
    def _generate_risk_summary(self, structured_risks: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Generate a summary of the risk analysis.
        """
        high_count = len(structured_risks.get('high_risks', []))
        medium_count = len(structured_risks.get('medium_risks', []))
        low_count = len(structured_risks.get('low_risks', []))
        total_risks = high_count + medium_count + low_count
        
        # Determine overall risk level
        if high_count >= 3:
            overall_risk = "HIGH"
            recommendation = "Significant concerns identified. Recommend legal review before signing."
        elif high_count >= 1 or medium_count >= 3:
            overall_risk = "MEDIUM"
            recommendation = "Some concerns identified. Review and negotiate key terms."
        else:
            overall_risk = "LOW"
            recommendation = "Minimal concerns. Standard contract review recommended."
        
        return {
            "total_risks": total_risks,
            "high_risk_count": high_count,
            "medium_risk_count": medium_count,
            "low_risk_count": low_count,
            "overall_risk_level": overall_risk,
            "recommendation": recommendation
        }
    
    def analyze_specific_clauses(self, contract_text: str, clause_types: List[str]) -> Dict[str, Any]:
        """
        Analyze specific types of clauses in the contract.
        """
        try:
            clause_list = ", ".join(clause_types)
            
            prompt = f"""
            Analyze this contract specifically for the following types of clauses: {clause_list}

            For each clause type requested:
            1. Identify if it exists in the contract
            2. Summarize the key terms
            3. Assess if the terms are favorable, neutral, or unfavorable
            4. Note any missing standard protections

            Contract Text:
            {contract_text[:20000]}

            Provide a structured analysis for each requested clause type.
            """
            
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            if not response or not response.text:
                return {
                    "error": "Failed to analyze specific clauses",
                    "status": "error"
                }
            
            return {
                "clause_analysis": response.text.strip(),
                "analyzed_clauses": clause_types,
                "status": "success"
            }
            
        except Exception as e:
            print(f"[RiskAnalyzer] Error analyzing clauses: {e}")
            return {
                "error": f"Clause analysis failed: {str(e)}",
                "status": "error"
            }
