#!/usr/bin/env python3
"""
Quick test script to verify API endpoints are working correctly.
"""

import requests
import json
import sys
import time

# Test configuration
BASE_URL = "http://localhost:3000/api"  # Vercel dev server
# For production testing, change to your Vercel deployment URL

def test_health_check():
    """Test the admin health check endpoint."""
    try:
        print("🔍 Testing health check endpoint...")
        response = requests.get(f"{BASE_URL}/admin?action=health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_languages_endpoint():
    """Test the languages endpoint."""
    try:
        print("🔍 Testing languages endpoint...")
        response = requests.get(f"{BASE_URL}/languages", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            lang_count = data.get('total_count', 0)
            print(f"✅ Languages endpoint passed: {lang_count} languages supported")
            return True
        else:
            print(f"❌ Languages endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Languages endpoint error: {e}")
        return False

def test_chat_endpoint():
    """Test the basic chat endpoint."""
    try:
        print("🔍 Testing chat endpoint...")
        
        test_message = "What is a contract?"
        payload = {
            "message": test_message,
            "session_id": "test_session",
            "contract_context": None
        }
        
        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success' and data.get('response'):
                print(f"✅ Chat endpoint passed: Got AI response")
                return True
            else:
                print(f"❌ Chat endpoint failed: Invalid response format")
                return False
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        return False

def test_analyze_endpoint():
    """Test the analyze endpoint with a simple test."""
    try:
        print("🔍 Testing analyze endpoint...")
        
        # Create a simple test file
        test_content = b"This is a test contract document for testing purposes."
        files = {
            'file': ('test_contract.txt', test_content, 'text/plain')
        }
        data = {
            'language': 'en',
            'interests': json.dumps([])
        }
        
        response = requests.post(
            f"{BASE_URL}/analyze",
            files=files,
            data=data,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"✅ Analyze endpoint passed: Contract analysis completed")
                return True
            else:
                print(f"❌ Analyze endpoint failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Analyze endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Analyze endpoint error: {e}")
        return False

def main():
    """Run all API endpoint tests."""
    print("🚀 Starting NyayMitra API Endpoint Tests")
    print(f"📍 Testing against: {BASE_URL}")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Languages", test_languages_endpoint),
        ("Chat", test_chat_endpoint),
        ("Analyze", test_analyze_endpoint)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<15} {status}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n📈 Overall: {passed}/{total} tests passed ({100*passed//total}%)")
    
    if passed == total:
        print("🎉 All tests passed! API is ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)