import json
import os
import google.generativeai as genai
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_POST(self):
        try:
            # Handle CORS
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Get request data
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length).decode('utf-8')
                try:
                    data = json.loads(body)
                except:
                    data = {}
            else:
                data = {}
            
            message = data.get('message', '')
            session_id = data.get('session_id', 'default')
            contract_context = data.get('contract_context')
            
            if not message:
                error_response = {'error': 'No message provided', 'status': 'error'}
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Simple demo response for now
            ai_response = f"Thank you for your message: '{message}'. This is a demo response from NyayMitra AI. I'm here to help with your legal contract questions. For actual AI responses, please configure the GEMINI_API_KEY environment variable."
            
            # Try to use Gemini if API key is available
            try:
                api_key = os.getenv('GEMINI_API_KEY')
                if api_key:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    system_prompt = """You are NyayMitra AI, a helpful legal assistant specializing in contract analysis and legal guidance.
You provide clear, accurate, and practical legal information while being conversational and friendly.
Important guidelines:
- Provide practical, actionable advice
- Use simple language, avoid legal jargon unless necessary
- Be concise but thorough
- If discussing contracts, focus on risk assessment and practical implications
- Always remind users that for binding legal advice, they should consult a qualified lawyer
- Be helpful and empathetic to users' legal concerns"""

                    context_info = ""
                    if contract_context:
                        context_info = f"\n\nContract Context Available: The user has uploaded a contract for analysis. You can reference this context when answering questions about their specific contract."

                    full_prompt = f"""{system_prompt}{context_info}

User: {message}

Please provide a helpful, conversational response:"""

                    response = model.generate_content(full_prompt)
                    ai_response = response.text
            except Exception as ai_error:
                # If AI fails, continue with demo response
                print(f"AI error (using demo response): {ai_error}")
            
            # Generate suggestions
            suggestions = [
                "What are common contract risks?",
                "How should I review employment terms?", 
                "What clauses should I pay attention to?"
            ]
            
            response_data = {
                'response': ai_response,
                'session_id': session_id,
                'suggestions': suggestions,
                'status': 'success'
            }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            try:
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                error_response = {
                    'error': f'Chat error: {str(e)}',
                    'status': 'error'
                }
                
                print(f"Chat error: {str(e)}")
                self.wfile.write(json.dumps(error_response).encode())
            except:
                pass

    def do_GET(self):
        self.send_response(405)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        error_response = {
            'error': 'Method not allowed. Use POST for chat.',
            'status': 'error'
        }
        self.wfile.write(json.dumps(error_response).encode())