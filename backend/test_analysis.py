#!/usr/bin/env python3
"""
Test script to verify contract analysis is working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.moderator import ModeratorAgent
from config import Config
import tempfile

def test_analysis():
    """Test the contract analysis pipeline"""
    
    print("🧪 Testing Contract Analysis Pipeline")
    print("=" * 50)
    
    print(f"📋 Configuration:")
    print(f"   API Key: {Config.GEMINI_API_KEY[:20]}...{Config.GEMINI_API_KEY[-10:]}")
    print(f"   Model: {Config.GEMINI_MODEL}")
    print()
    
    try:
        # Initialize moderator
        print("🔧 Initializing ModeratorAgent...")
        moderator = ModeratorAgent()
        print("✅ ModeratorAgent initialized successfully")
        
        # Test with a simple text file (since we don't have a PDF)
        print("\n📄 Creating test contract file...")
        test_contract = """
        EMPLOYMENT AGREEMENT
        
        This Employment Agreement is entered into between Company ABC and Employee John Doe.
        
        1. TERMINATION: Either party may terminate this agreement with 30 days notice.
        
        2. CONFIDENTIALITY: Employee agrees to maintain confidentiality of all company information.
        
        3. LIABILITY: Company shall not be liable for any damages exceeding $1000.
        
        4. INDEMNIFICATION: Employee agrees to indemnify company against all claims.
        
        5. NON-COMPETE: Employee agrees not to compete for 2 years after termination.
        """
        
        # Create a temporary text file (simulating PDF extraction)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_contract)
            temp_file = f.name
        
        print(f"✅ Test contract created: {temp_file}")
        
        # Test individual components
        print("\n🔍 Testing Risk Analyzer...")
        try:
            risk_report = moderator.risk_analyzer.analyze_contract_text(test_contract)
            print(f"✅ Risk analysis completed: {len(risk_report)} clauses")
        except Exception as e:
            print(f"❌ Risk analysis failed: {e}")
            return False
        
        print("\n📝 Testing Summarizer...")
        try:
            summary = moderator.summarizer.summarize(risk_report)
            print(f"✅ Summary generated: {len(summary)} characters")
            print(f"Summary preview: {summary[:100]}...")
        except Exception as e:
            print(f"❌ Summary generation failed: {e}")
            return False
        
        print("\n📊 Testing Simulation...")
        try:
            simulation = moderator.simulation_agent.analyze_risks(risk_report)
            print(f"✅ Simulation completed")
        except Exception as e:
            print(f"❌ Simulation failed: {e}")
            return False
        
        # Clean up
        os.unlink(temp_file)
        
        print("\n🎉 All tests passed!")
        print("✅ Contract analysis pipeline is working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_analysis()
    sys.exit(0 if success else 1)
