#!/usr/bin/env python3
"""
Test script to verify the response format and JSON serialization
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.moderator import ModeratorAgent
from config import Config

def test_response_format():
    """Test that the response can be properly JSON serialized"""
    
    print("🧪 Testing Response Format and JSON Serialization")
    print("=" * 60)
    
    try:
        # Create a simple test contract
        test_contract = """
        EMPLOYMENT AGREEMENT
        
        1. TERMINATION: Either party may terminate this agreement with 30 days notice.
        2. CONFIDENTIALITY: Employee agrees to maintain confidentiality.
        3. LIABILITY: Company shall not be liable for damages exceeding $1000.
        """
        
        # Initialize moderator
        moderator = ModeratorAgent()
        
        # Create a temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_contract)
            temp_file = f.name
        
        print(f"📄 Created test file: {temp_file}")
        
        # Test the analysis
        print("🔍 Running analysis...")
        result = moderator.analyze_contract_text(test_contract)
        
        print(f"✅ Analysis completed")
        print(f"📊 Result type: {type(result)}")
        print(f"📊 Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if 'status' in result:
            print(f"📊 Status: {result['status']}")
        
        if 'summary' in result:
            print(f"📊 Summary length: {len(result['summary'])} characters")
            print(f"📊 Summary preview: {result['summary'][:100]}...")
        
        # Test JSON serialization
        print("\n🔧 Testing JSON serialization...")
        try:
            json_str = json.dumps(result, indent=2)
            print(f"✅ JSON serialization successful")
            print(f"📊 JSON length: {len(json_str)} characters")
            
            # Test deserialization
            parsed_result = json.loads(json_str)
            print(f"✅ JSON deserialization successful")
            print(f"📊 Parsed keys: {list(parsed_result.keys())}")
            
        except Exception as json_error:
            print(f"❌ JSON serialization failed: {json_error}")
            print(f"🔍 Problematic data types:")
            for key, value in result.items():
                print(f"   {key}: {type(value)}")
            return False
        
        # Clean up
        os.unlink(temp_file)
        
        print("\n🎉 All tests passed!")
        print("✅ Response format is correct and JSON serializable")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_response_format()
    sys.exit(0 if success else 1)
