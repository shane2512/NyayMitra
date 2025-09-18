#!/usr/bin/env python3
"""
Comprehensive debugging script to identify the frontend-backend communication issue
"""

import requests
import json
import sys
import os
import time

def test_backend_endpoints():
    """Test all backend endpoints"""
    
    print("🔍 NyayMitra Backend-Frontend Communication Debug")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Basic connectivity
    print("\n1️⃣ Testing Basic Connectivity...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Test endpoint
    print("\n2️⃣ Testing Configuration...")
    try:
        response = requests.get(f"{base_url}/test", timeout=10)
        data = response.json()
        print(f"✅ Test endpoint: {response.status_code}")
        print(f"   Model: {data.get('config', {}).get('model', 'Unknown')}")
        print(f"   API Key Present: {data.get('config', {}).get('api_key_present', False)}")
    except Exception as e:
        print(f"❌ Test endpoint failed: {e}")
    
    # Test 3: File upload simulation
    print("\n3️⃣ Testing File Upload (Simulate Frontend)...")
    
    # Create a simple test PDF content
    test_content = """Sample Rental Agreement
1. The Tenant must vacate the property within 7 days if the Landlord demands so.
2. The security deposit of 2 months' rent is non-refundable under any circumstances.
3. The Tenant shall not sublet the property without written permission from the Landlord.
4. The Landlord may increase the rent at any time without prior notice.
5. In case of dispute, arbitration will take place only in the Landlord's city."""
    
    # Create a temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        # Simulate the exact request the frontend makes
        files = {'file': ('test_contract.txt', open(temp_file, 'rb'), 'text/plain')}
        data = {
            'language': 'en',
            'interests': json.dumps([])
        }
        
        print(f"📤 Making POST request to {base_url}/analyze...")
        print(f"   File: test_contract.txt ({os.path.getsize(temp_file)} bytes)")
        print(f"   Language: en")
        print(f"   Interests: []")
        
        start_time = time.time()
        response = requests.post(
            f"{base_url}/analyze", 
            files=files, 
            data=data, 
            timeout=300  # 5 minutes
        )
        elapsed = time.time() - start_time
        
        print(f"📥 Response received in {elapsed:.1f}s")
        print(f"   Status Code: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
        print(f"   Content-Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ JSON parsing successful")
                print(f"   Response Type: {type(result)}")
                print(f"   Response Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                
                if 'status' in result:
                    print(f"   Status: {result['status']}")
                    
                    if result['status'] == 'success':
                        print(f"   ✅ Analysis Status: SUCCESS")
                        print(f"   📊 Clauses Analyzed: {result.get('total_clauses_analyzed', 'Unknown')}")
                        print(f"   ⏱️  Processing Time: {result.get('processing_time', 'Unknown')}s")
                        
                        if 'summary' in result:
                            summary_len = len(result['summary'])
                            print(f"   📝 Summary Length: {summary_len} characters")
                            print(f"   📝 Summary Preview: {result['summary'][:100]}...")
                        
                        if 'risk_report' in result:
                            risk_count = len(result['risk_report'])
                            print(f"   ⚠️  Risk Report Entries: {risk_count}")
                        
                        print(f"\n🎉 BACKEND IS WORKING CORRECTLY!")
                        print(f"   The issue is likely in the frontend handling of the response.")
                        
                    else:
                        print(f"   ❌ Analysis Status: {result['status']}")
                        print(f"   Error: {result.get('error', 'Unknown error')}")
                        
                else:
                    print(f"   ❌ No status field in response")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"   Response content (first 500 chars): {response.text[:500]}")
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
    
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out (5 minutes)")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    print("\n" + "=" * 60)
    print("🔍 Debug Summary:")
    print("1. If backend tests pass but frontend fails, the issue is in React/axios handling")
    print("2. Check browser console for detailed error messages")
    print("3. Verify CORS headers are properly set")
    print("4. Check if response size is causing issues")
    print("5. Ensure frontend timeout is sufficient (3+ minutes)")

if __name__ == "__main__":
    test_backend_endpoints()
