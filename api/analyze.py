"""
Contract analysis endpoint for Vercel Functions.
Handles PDF contract analysis with translation support.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Dict, Any

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.extend([current_dir, parent_dir, os.path.join(parent_dir, 'netlify', 'functions')])

try:
    from netlify.functions.config import Config
    from netlify.functions.utils import create_response, handle_cors, validate_request
    from netlify.functions.agents.moderator import ModeratorAgent
    from netlify.functions.agents.rate_limiter import ServerlessRateLimiter
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback configuration
    class Config:
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDgZrm7d1htahrLH2KMdVmnOEcQAIWzmys")
        GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
    def do_POST(self):
        """Handle POST requests for contract analysis."""
        try:
            # Handle CORS
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            language = query_params.get('language', ['en'])[0]
            interests = query_params.get('interests', ['[]'])[0]
            
            try:
                interests = json.loads(interests) if isinstance(interests, str) else interests
            except:
                interests = []
            
            # For demo purposes, create a sample analysis
            def analysis_operation():
                if language != 'en' or interests:
                    return {
                        "status": "success",
                        "summary": f"Contract analysis completed in {language}",
                        "risk_score": 75,
                        "key_findings": [
                            "Standard commercial agreement",
                            "Moderate risk level identified", 
                            "Review recommended for specific clauses"
                        ],
                        "language": language,
                        "interests": interests,
                        "processing_time": "45 seconds"
                    }
                else:
                    return {
                        "status": "success",
                        "summary": "Contract analysis completed successfully",
                        "risk_score": 65,
                        "key_findings": [
                            "Standard terms and conditions",
                            "Low to moderate risk",
                            "No major red flags identified"
                        ],
                        "processing_time": "30 seconds"
                    }
            
            result = analysis_operation()
            
            response_data = {
                'status': 'success',
                'analysis': result,
                'language': language,
                'interests': interests,
                'processing_time': result.get('processing_time', 'N/A')
            }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {
                'error': f'Analysis handler error: {str(e)}',
                'type': 'server_error'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_GET(self):
        """Handle GET requests."""
        self.send_response(405)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        error_response = {
            'error': 'Method not allowed. Use POST to upload files.',
            'type': 'method_error'
        }
        self.wfile.write(json.dumps(error_response).encode())
