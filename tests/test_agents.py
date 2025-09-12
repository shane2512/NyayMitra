import unittest
from backend.agents.risk_analyzer import RiskAnalyzerAgent
from backend.agents.summarizer import SummarizerAgent
from backend.agents.simulation import SimulationAgent
from backend.agents.moderator import ModeratorAgent

class TestNyayMitraAgents(unittest.TestCase):

    def setUp(self):
        self.risk_analyzer = RiskAnalyzerAgent()
        self.summarizer = SummarizerAgent()
        self.simulation = SimulationAgent()
        self.moderator = ModeratorAgent()

    def test_risk_analyzer(self):
        pdf_path = "sample_contracts/sample_contract.pdf"
        report = self.risk_analyzer.process(pdf_path)
        self.assertIsInstance(report, dict)
        self.assertIn("Clause 1", report)
        self.assertIn("analysis", report["Clause 1"])
        self.assertIn("risk_level", report["Clause 1"]["analysis"])

    def test_summarizer(self):
        risk_report = {
            "Clause 1": {
                "text": "Sample clause text.",
                "analysis": {
                    "analysis": "This clause is risky.",
                    "risk_level": "High"
                }
            }
        }
        summary = self.summarizer.summarize(risk_report)
        self.assertIsInstance(summary, str)
        self.assertIn("Sample clause text", summary)

    def test_simulation(self):
        risk_report = {
            "Clause 1": {
                "text": "Sample clause text.",
                "analysis": {
                    "analysis": "This clause is risky.",
                    "risk_level": "High"
                }
            },
            "Clause 2": {
                "text": "Another clause text.",
                "analysis": {
                    "analysis": "This clause is safe.",
                    "risk_level": "Low"
                }
            }
        }
        result = self.simulation.analyze_risks(risk_report)
        self.assertIn("safety_index", result)
        self.assertIn("risk_distribution", result)

    def test_moderator(self):
        pdf_path = "sample_contracts/sample_contract.pdf"
        results = self.moderator.analyze_contract(pdf_path)
        self.assertIn("risk_report", results)
        self.assertIn("summary", results)
        self.assertIn("simulation", results)

if __name__ == '__main__':
    unittest.main()