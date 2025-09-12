import google.generativeai as genai

from .api_optimizer import GeminiAPIOptimizer
from config import Config

class SummarizerAgent:
    def __init__(self, api_key=None, model_name=None):
        api_key = api_key or Config.GEMINI_API_KEY
        model_name = model_name or Config.GEMINI_MODEL
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.api_optimizer = GeminiAPIOptimizer(api_key, model_name=model_name)

    def summarize(self, risk_report):
        """Generate AI-powered plain language summary of the contract analysis"""
        try:
            # Prepare the risk analysis data for the AI
            text_input = "Contract Risk Analysis Results:\n\n"
            high_risk_clauses = []
            medium_risk_clauses = []
            low_risk_clauses = []
            
            for clause, details in risk_report.items():
                risk_level = details.get('analysis', {}).get('risk_level', 'Medium')
                analysis = details.get('analysis', {}).get('analysis', 'No analysis available')
                clause_text = details.get('text', '')[:200] + "..." if len(details.get('text', '')) > 200 else details.get('text', '')
                
                clause_info = f"- {clause} ({risk_level} Risk): {analysis}\n  Clause Text: {clause_text}\n"
                
                if risk_level == 'High':
                    high_risk_clauses.append(clause_info)
                elif risk_level == 'Medium':
                    medium_risk_clauses.append(clause_info)
                else:
                    low_risk_clauses.append(clause_info)

            # Build the input text
            if high_risk_clauses:
                text_input += f"\nHIGH RISK CLAUSES ({len(high_risk_clauses)}):\n" + "".join(high_risk_clauses)
            if medium_risk_clauses:
                text_input += f"\nMEDIUM RISK CLAUSES ({len(medium_risk_clauses)}):\n" + "".join(medium_risk_clauses)
            if low_risk_clauses:
                text_input += f"\nLOW RISK CLAUSES ({len(low_risk_clauses)}):\n" + "".join(low_risk_clauses)

            prompt = f"""
You are a legal expert who explains complex contract terms in simple, plain language for non-lawyers.

Please provide a clear, concise summary of this contract risk analysis that:
1. Explains the overall risk level of the contract
2. Highlights the most important concerns in everyday language
3. Provides actionable recommendations
4. Uses a conversational, helpful tone
5. Avoids legal jargon

{text_input}

Please write a summary that a regular person can understand, focusing on what they should know and what actions they should take.
"""

            print(f"[Summarizer] Generating AI summary...")
            
            # Use only GeminiAPIOptimizer for all Gemini API calls
            summary = self.api_optimizer.optimized_generate_content(prompt)
            print(f"[Summarizer] AI Summary generated: {len(summary)} characters")
            return summary if summary else self._fallback_summary(risk_report)
            
        except Exception as e:
            print(f"[Summarizer] Error generating AI summary: {e}")
            # Fallback to rule-based summary
            return self._fallback_summary(risk_report)

    def _fallback_summary(self, risk_report):
        """Fallback summary when AI fails"""
        high_count = sum(1 for clause, details in risk_report.items() 
                        if details.get('analysis', {}).get('risk_level') == 'High')
        medium_count = sum(1 for clause, details in risk_report.items() 
                          if details.get('analysis', {}).get('risk_level') == 'Medium')
        low_count = sum(1 for clause, details in risk_report.items() 
                       if details.get('analysis', {}).get('risk_level') == 'Low')
        total_count = len(risk_report)
        
        if high_count > total_count * 0.4:
            return f"⚠️ HIGH RISK CONTRACT ⚠️\n\nThis contract contains {high_count} high-risk clauses out of {total_count} total clauses analyzed. We strongly recommend having a lawyer review this contract before signing. The high-risk areas may expose you to significant legal or financial liability.\n\nKey concerns likely include liability limitations, termination clauses, or indemnification requirements. Consider negotiating these terms or seeking legal counsel."
        elif high_count > 0:
            return f"⚠️ MODERATE RISK CONTRACT\n\nThis contract has {high_count} high-risk and {medium_count} medium-risk clauses that need attention out of {total_count} total clauses. While manageable, you should carefully review the flagged sections and consider negotiating better terms.\n\nMost of the contract appears standard, but the identified risk areas could impact your rights or obligations."
        else:
            return f"✅ GENERALLY ACCEPTABLE CONTRACT\n\nThis contract appears relatively balanced with {total_count} clauses analyzed. While {medium_count} clauses require some attention, no major red flags were identified.\n\nYou should still read through the document carefully, but the overall risk level appears manageable for most situations."