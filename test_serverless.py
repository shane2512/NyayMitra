#!/usr/bin/env python3
"""
Test script for NyayMitra serverless functions.
This script tests all API endpoints to ensure they work correctly.
"""

import json
import requests
import time
import os
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:3000/api"  # For local testing with vercel dev
# BASE_URL = "https://your-vercel-app.vercel.app/api"  # For production testing

class ServerlessAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 30
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, message: str = "", data: Any = None):
        """Log test result."""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": time.time(),
            "data": data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if data and not success:
            print(f"   Error details: {json.dumps(data, indent=2)}")
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        try:
            response = self.session.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get('body'):
                    data = json.loads(data['body'])
                
                if data.get('status') == 'healthy':
                    self.log_test("Health Check", True, "Service is healthy", data)
                    return True
                else:
                    self.log_test("Health Check", False, "Service not healthy", data)
                    return False
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Health Check", False, f"Request failed: {str(e)}")
            return False
    
    def test_test_endpoint(self):
        """Test the test endpoint."""
        try:
            response = self.session.get(f"{self.base_url}/test")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get('body'):
                    data = json.loads(data['body'])
                
                if data.get('status') == 'success':
                    self.log_test("Test Endpoint", True, "Configuration verified", {
                        "model": data.get('config', {}).get('model'),
                        "api_key_present": data.get('config', {}).get('api_key_present')
                    })
                    return True
                else:
                    self.log_test("Test Endpoint", False, "Configuration issues", data)
                    return False
            else:
                self.log_test("Test Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Test Endpoint", False, f"Request failed: {str(e)}")
            return False
    
    def test_chat_endpoint(self):
        """Test chat functionality."""
        try:
            payload = {
                "message": "What is a contract?",
                "session_id": "test_session_123"
            }
            
            response = self.session.post(
                f"{self.base_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get('body'):
                    data = json.loads(data['body'])
                
                if data.get('status') == 'success' and data.get('response'):
                    self.log_test("Chat Endpoint", True, "Chat response generated", {
                        "response_length": len(data.get('response', '')),
                        "session_id": data.get('session_id'),
                        "suggestions_count": len(data.get('suggestions', []))
                    })
                    return True
                else:
                    self.log_test("Chat Endpoint", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Chat Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Chat Endpoint", False, f"Request failed: {str(e)}")
            return False
    
    def test_batch_chat_endpoint(self):
        """Test batch chat functionality."""
        try:
            payload = {
                "questions": [
                    "What are the key elements of a contract?",
                    "What is consideration in contract law?",
                    "What makes a contract legally binding?"
                ],
                "session_id": "test_batch_session_123"
            }
            
            response = self.session.post(
                f"{self.base_url}/chat-batch",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get('body'):
                    data = json.loads(data['body'])
                
                if data.get('status') == 'success' and data.get('responses'):
                    responses = data.get('responses', [])
                    self.log_test("Batch Chat Endpoint", True, "Batch responses generated", {
                        "question_count": data.get('question_count'),
                        "response_count": len(responses),
                        "session_id": data.get('session_id')
                    })
                    return True
                else:
                    self.log_test("Batch Chat Endpoint", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Batch Chat Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Batch Chat Endpoint", False, f"Request failed: {str(e)}")
            return False
    
    def test_languages_endpoint(self):
        """Test supported languages endpoint."""
        try:
            response = self.session.get(f"{self.base_url}/languages")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get('body'):
                    data = json.loads(data['body'])
                
                if data.get('status') == 'success' and data.get('supported_languages'):
                    languages = data.get('supported_languages', {})
                    self.log_test("Languages Endpoint", True, "Languages retrieved", {
                        "language_count": len(languages),
                        "total_languages": data.get('total_languages'),
                        "sample_languages": list(languages.keys())[:5]
                    })
                    return True
                else:
                    self.log_test("Languages Endpoint", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Languages Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Languages Endpoint", False, f"Request failed: {str(e)}")
            return False
    
    def test_rate_limit_status_endpoint(self):
        """Test rate limit status endpoint."""
        try:
            response = self.session.get(f"{self.base_url}/rate-limit-status")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get('body'):
                    data = json.loads(data['body'])
                
                required_fields = ['current_minute_requests', 'current_daily_requests', 
                                 'minute_limit', 'daily_limit', 'circuit_breaker_open']
                
                if all(field in data for field in required_fields):
                    self.log_test("Rate Limit Status", True, "Rate limit status retrieved", {
                        "minute_usage": f"{data.get('current_minute_requests')}/{data.get('minute_limit')}",
                        "daily_usage": f"{data.get('current_daily_requests')}/{data.get('daily_limit')}",
                        "circuit_breaker_open": data.get('circuit_breaker_open'),
                        "warnings": data.get('warnings', [])
                    })
                    return True
                else:
                    self.log_test("Rate Limit Status", False, "Missing required fields", data)
                    return False
            else:
                self.log_test("Rate Limit Status", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Rate Limit Status", False, f"Request failed: {str(e)}")
            return False
    
    def test_translator_metrics_endpoint(self):
        """Test translator metrics endpoint."""
        try:
            response = self.session.get(f"{self.base_url}/translator-metrics")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get('body'):
                    data = json.loads(data['body'])
                
                if data.get('service_status') == 'active':
                    self.log_test("Translator Metrics", True, "Translator metrics retrieved", {
                        "supported_languages": data.get('supported_languages'),
                        "interest_areas_count": len(data.get('interest_areas', [])),
                        "service_status": data.get('service_status')
                    })
                    return True
                else:
                    self.log_test("Translator Metrics", False, "Service not active", data)
                    return False
            else:
                self.log_test("Translator Metrics", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Translator Metrics", False, f"Request failed: {str(e)}")
            return False
    
    def test_index_endpoint(self):
        """Test index/root endpoint."""
        try:
            response = self.session.get(f"{self.base_url}/index")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get('body'):
                    data = json.loads(data['body'])
                
                if data.get('message') and 'NyayMitra' in data.get('message', ''):
                    self.log_test("Index Endpoint", True, "API info retrieved", {
                        "version": data.get('version'),
                        "architecture": data.get('architecture'),
                        "endpoint_count": len(data.get('endpoints', [])),
                        "feature_count": len(data.get('features', []))
                    })
                    return True
                else:
                    self.log_test("Index Endpoint", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Index Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Index Endpoint", False, f"Request failed: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests and generate report."""
        print("🚀 Starting NyayMitra Serverless API Tests")
        print("=" * 50)
        
        # List of tests to run
        tests = [
            ("Index Endpoint", self.test_index_endpoint),
            ("Health Check", self.test_health_endpoint),
            ("Test Endpoint", self.test_test_endpoint),
            ("Chat Endpoint", self.test_chat_endpoint),
            ("Batch Chat", self.test_batch_chat_endpoint),
            ("Languages", self.test_languages_endpoint),
            ("Rate Limit Status", self.test_rate_limit_status_endpoint),
            ("Translator Metrics", self.test_translator_metrics_endpoint)
        ]
        
        # Run tests
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test execution failed: {str(e)}")
        
        # Generate summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! Serverless API is working correctly.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check the details above.")
        
        return passed == total
    
    def save_test_report(self, filename: str = "serverless_test_report.json"):
        """Save detailed test report to file."""
        report = {
            "timestamp": time.time(),
            "base_url": self.base_url,
            "total_tests": len(self.test_results),
            "passed_tests": len([r for r in self.test_results if r['success']]),
            "failed_tests": len([r for r in self.test_results if not r['success']]),
            "results": self.test_results
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed test report saved to: {filename}")

def main():
    """Main test execution."""
    print("NyayMitra Serverless API Test Suite")
    print("Testing URL:", BASE_URL)
    print()
    
    # Create tester instance
    tester = ServerlessAPITester(BASE_URL)
    
    # Run all tests
    success = tester.run_all_tests()
    
    # Save report
    tester.save_test_report()
    
    # Exit with appropriate code
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
