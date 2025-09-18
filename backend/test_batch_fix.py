#!/usr/bin/env python3
"""
Test script to verify the batch_analyze_clauses method fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.api_optimizer import GeminiAPIOptimizer
from config import Config

def test_batch_method_exists():
    """Test that the batch_analyze_clauses method exists and is callable"""
    
    print("🔧 Testing GeminiAPIOptimizer batch method fix...")
    
    try:
        # Initialize the optimizer
        optimizer = GeminiAPIOptimizer(Config.GEMINI_API_KEY)
        
        # Check if the method exists
        if hasattr(optimizer, 'batch_analyze_clauses'):
            print("✅ batch_analyze_clauses method exists")
        else:
            print("❌ batch_analyze_clauses method is missing")
            return False
        
        # Check if the method is callable
        if callable(getattr(optimizer, 'batch_analyze_clauses')):
            print("✅ batch_analyze_clauses method is callable")
        else:
            print("❌ batch_analyze_clauses method is not callable")
            return False
        
        # Test with empty clauses (should return empty dict)
        result = optimizer.batch_analyze_clauses([])
        if result == {}:
            print("✅ Empty clauses test passed")
        else:
            print(f"❌ Empty clauses test failed: {result}")
            return False
        
        print("🎉 All tests passed! The batch method fix is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_batch_method_exists()
    if success:
        print("\n✅ Fix verified successfully!")
        print("The 'batch_analyze_clauses' method is now available and should resolve the error.")
    else:
        print("\n❌ Fix verification failed!")
        print("There may be additional issues that need to be addressed.")
