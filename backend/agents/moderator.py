from .risk_analyzer import RiskAnalyzerAgent
from .summarizer import SummarizerAgent
from .simulation import SimulationAgent
import os
import time

from config import Config

class ModeratorAgent:
    def __init__(self, api_key=None, model_name=None):
        api_key = api_key or Config.GEMINI_API_KEY
        model_name = model_name or Config.GEMINI_MODEL
        self.api_key = api_key
        self.model_name = model_name
        self.risk_analyzer = RiskAnalyzerAgent(api_key, model_name)
        self.summarizer = SummarizerAgent(api_key, model_name)
        self.simulation_agent = SimulationAgent(api_key, model_name)

    def analyze_contract(self, pdf_path):
        try:
            print(f"[Moderator] Starting comprehensive contract analysis for: {pdf_path}")
            start_time = time.time()
            
            # Step 1: Extract and validate contract text
            contract_text = self.risk_analyzer.extract_text(pdf_path)
            if not contract_text or len(contract_text.strip()) < 100:
                raise ValueError("Contract text is too short or empty. Please ensure the PDF contains readable text.")
            
            print(f"[Moderator] Contract text extracted: {len(contract_text)} characters")
            
            # Step 2: Analyze the contract using the Risk Analyzer Agent
            print(f"[Moderator] Starting risk analysis...")
            risk_report = self.risk_analyzer.analyze_contract(pdf_path)
            print(f"[Moderator] Risk analysis completed: {len(risk_report)} clauses analyzed")

            # Step 3: Generate AI-powered summary
            print(f"[Moderator] Generating AI summary...")
            summary = self.summarizer.summarize(risk_report)
            print(f"[Moderator] Summary generated: {len(summary)} characters")

            # Step 4: Run simulation analysis
            print(f"[Moderator] Running simulation analysis...")
            simulation_results = self.simulation_agent.analyze_risks(risk_report)
            print(f"[Moderator] Simulation completed")

            # Calculate processing time
            processing_time = round(time.time() - start_time, 2)
            
            # Combine results into a structured JSON response
            response = {
                "risk_report": risk_report,
                "summary": summary,
                "simulation": simulation_results,
                "contract_text": contract_text[:1000] + "..." if len(contract_text) > 1000 else contract_text,  # Truncate for response size
                "processing_time": processing_time,
                "total_clauses_analyzed": len(risk_report),
                "status": "success"
            }
            
            print(f"[Moderator] Analysis complete in {processing_time}s. Status: success")
            return response
            
        except Exception as e:
            print(f"[Moderator] Error during analysis: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "error": str(e),
                "status": "error",
                "details": "Contract analysis failed. Please ensure the PDF is readable and contains contract text."
            }