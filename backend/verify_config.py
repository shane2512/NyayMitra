#!/usr/bin/env python3
"""
Verification script to ensure all agents use API key and model from .env file
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from agents.risk_analyzer import RiskAnalyzerAgent
from agents.summarizer import SummarizerAgent
from agents.simulation import SimulationAgent
from agents.conversation_agent import ConversationAgent
from agents.conversation_agent_simple import ConversationAgent as SimpleConversationAgent
from agents.voice_conversation_agent import VoiceConversationAgent
from agents.api_optimizer import GeminiAPIOptimizer

def verify_config():
    """Verify that all agents are using the correct API key and model from .env"""
    
    print("🔍 Verifying Configuration Usage Across All Agents")
    print("=" * 60)
    
    # Print current config values
    print(f"📋 Current Config Values:")
    print(f"   API Key: {Config.GEMINI_API_KEY[:20]}...{Config.GEMINI_API_KEY[-10:]}")
    print(f"   Model: {Config.GEMINI_MODEL}")
    print()
    
    agents_to_test = [
        ("RiskAnalyzerAgent", RiskAnalyzerAgent),
        ("SummarizerAgent", SummarizerAgent),
        ("SimulationAgent", SimulationAgent),
        ("ConversationAgent", ConversationAgent),
        ("SimpleConversationAgent", SimpleConversationAgent),
        ("VoiceConversationAgent", VoiceConversationAgent),
        ("GeminiAPIOptimizer", GeminiAPIOptimizer)
    ]
    
    all_passed = True
    
    for agent_name, agent_class in agents_to_test:
        print(f"🧪 Testing {agent_name}...")
        
        try:
            # Initialize agent
            if agent_name == "GeminiAPIOptimizer":
                agent = agent_class(Config.GEMINI_API_KEY)
            elif agent_name in ["SimpleConversationAgent", "VoiceConversationAgent"]:
                agent = agent_class()
            else:
                agent = agent_class()
            
            # Check API key
            if hasattr(agent, 'api_key'):
                if agent.api_key == Config.GEMINI_API_KEY:
                    print(f"   ✅ API Key: Correctly using config value")
                else:
                    print(f"   ❌ API Key: Using {agent.api_key[:20]}... instead of config")
                    all_passed = False
            elif hasattr(agent, 'gemini_api_key'):
                if agent.gemini_api_key == Config.GEMINI_API_KEY:
                    print(f"   ✅ API Key: Correctly using config value")
                else:
                    print(f"   ❌ API Key: Using {agent.gemini_api_key[:20]}... instead of config")
                    all_passed = False
            else:
                print(f"   ⚠️  API Key: No api_key attribute found")
            
            # Check model
            if hasattr(agent, 'model_name'):
                if agent.model_name == Config.GEMINI_MODEL:
                    print(f"   ✅ Model: Correctly using {agent.model_name}")
                else:
                    print(f"   ❌ Model: Using {agent.model_name} instead of {Config.GEMINI_MODEL}")
                    all_passed = False
            elif hasattr(agent, 'model') and hasattr(agent.model, '_model_name'):
                if agent.model._model_name == Config.GEMINI_MODEL:
                    print(f"   ✅ Model: Correctly using {agent.model._model_name}")
                else:
                    print(f"   ❌ Model: Using {agent.model._model_name} instead of {Config.GEMINI_MODEL}")
                    all_passed = False
            else:
                print(f"   ⚠️  Model: No model_name attribute found")
            
            print(f"   ✅ {agent_name} initialized successfully")
            
        except Exception as e:
            print(f"   ❌ {agent_name} failed to initialize: {e}")
            all_passed = False
        
        print()
    
    print("=" * 60)
    if all_passed:
        print("🎉 All agents are correctly using configuration from .env file!")
        print("✅ API Key and Model consistency verified across all components")
    else:
        print("❌ Some agents are not using the correct configuration")
        print("⚠️  Please check the issues listed above")
    
    return all_passed

if __name__ == "__main__":
    success = verify_config()
    sys.exit(0 if success else 1)
