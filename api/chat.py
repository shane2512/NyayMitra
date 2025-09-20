import json
import os
import google.generativeai as genai
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import time
import hashlib

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
            
            # Parse query parameters for action
            query_components = dict(parse_qs(urlparse(self.path).query))
            action = query_components.get('action', ['chat'])[0]
            
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
            
            # Route to appropriate handler based on action
            if action == 'batch':
                response_data = self.handle_batch_chat(data)
            elif action == 'history':
                response_data = self.handle_chat_history(data)
            elif action == 'clear':
                response_data = self.handle_clear_session(data)
            elif action == 'transcribe':
                response_data = self.handle_transcribe(data)
            elif action == 'voice':
                response_data = self.handle_voice_message(data)
            else:
                response_data = self.handle_single_chat(data)
            
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

    def handle_single_chat(self, data):
        """Handle single chat message with enhanced legal assistance"""
        try:
            message = data.get('message', '')
            session_id = data.get('session_id', 'default')
            contract_context = data.get('contract_context')
            
            if not message:
                return {'error': 'No message provided', 'status': 'error'}
            
            # Generate AI response
            ai_response = self.generate_legal_response(message, contract_context)
            
            # Generate contextual suggestions based on message type
            suggestions = self.generate_suggestions(message, contract_context)
            
            return {
                'response': ai_response,
                'session_id': session_id,
                'suggestions': suggestions,
                'status': 'success',
                'timestamp': time.time(),
                'message_type': self.classify_message_type(message)
            }
            
        except Exception as e:
            print(f"Single chat error: {e}")
            return {'error': str(e), 'status': 'error'}

    def handle_batch_chat(self, data):
        """Handle batch questions for comprehensive analysis"""
        try:
            questions = data.get('questions', [])
            session_id = data.get('session_id', 'default')
            contract_context = data.get('contract_context')
            
            if not questions or not isinstance(questions, list):
                return {'error': 'Questions must be a non-empty list', 'status': 'error'}
            
            if len(questions) > 10:
                return {'error': 'Maximum 10 questions allowed per batch', 'status': 'error'}
            
            responses = []
            for i, question in enumerate(questions):
                try:
                    response = self.generate_legal_response(question, contract_context, batch_mode=True)
                    responses.append(response)
                except Exception as e:
                    responses.append(f"Error processing question {i+1}: {str(e)}")
            
            return {
                'responses': responses,
                'session_id': session_id,
                'question_count': len(questions),
                'status': 'success'
            }
            
        except Exception as e:
            return {'error': str(e), 'status': 'error'}

    def handle_chat_history(self, data):
        """Handle chat history retrieval"""
        try:
            return {
                'history': [],
                'session_id': data.get('session_id', 'default'),
                'message_count': 0,
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}

    def handle_clear_session(self, data):
        """Handle session clearing"""
        try:
            return {
                'status': 'success',
                'session_id': data.get('session_id', 'default'),
                'cleared': True,
                'message': 'Session cleared successfully'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}

    def handle_transcribe(self, data):
        """Handle audio transcription (placeholder)"""
        try:
            return {
                'transcription': 'Audio transcription feature coming soon',
                'confidence': 0.0,
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}

    def handle_voice_message(self, data):
        """Handle voice message processing"""
        try:
            message = data.get('message', '')
            session_id = data.get('session_id', 'default')
            contract_context = data.get('contract_context')
            
            # Generate response (same as text)
            ai_response = self.generate_legal_response(message, contract_context)
            
            return {
                'answer': ai_response,
                'audio_url': None,  # Voice synthesis coming soon
                'message': 'Voice synthesis feature coming soon',
                'session_id': session_id,
                'status': 'success'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}

    def generate_legal_response(self, message, contract_context=None, batch_mode=False):
        """Generate intelligent legal response using Gemini"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                return self.get_fallback_response(message, contract_context)
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Build comprehensive prompt
            system_prompt = self.build_system_prompt(contract_context, batch_mode)
            context_info = self.build_context_info(contract_context)
            
            full_prompt = f"""{system_prompt}{context_info}

User Question: {message}

Please provide a helpful, accurate, and practical response:"""

            response = model.generate_content(full_prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Gemini error: {e}")
            return self.get_fallback_response(message, contract_context)

    def build_system_prompt(self, contract_context, batch_mode=False):
        """Build comprehensive system prompt for legal assistant"""
        base_prompt = """You are NyayMitra AI, an expert legal assistant specializing in contract analysis and legal guidance.

Your expertise includes:
- Contract risk assessment and analysis
- Employment law and workplace rights
- Business agreements and commercial contracts
- Intellectual property and confidentiality terms
- Termination clauses and dispute resolution
- Compliance and regulatory matters
- Negotiation strategies and recommendations

Guidelines:
- Provide practical, actionable legal advice
- Use clear, simple language while maintaining accuracy
- Focus on risk assessment and practical implications
- Cite relevant legal principles when appropriate
- Always remind users to consult qualified lawyers for binding advice
- Be thorough but concise in your explanations
- Highlight potential red flags and risks
- Suggest specific improvements or alternatives"""

        if batch_mode:
            base_prompt += "\n- This is part of a batch analysis, so be concise but comprehensive"
        
        if contract_context:
            base_prompt += "\n- Reference the user's uploaded contract when relevant to their question"
        
        return base_prompt

    def build_context_info(self, contract_context):
        """Build context information for the AI"""
        if not contract_context:
            return ""
        
        context_info = "\n\nCONTRACT CONTEXT AVAILABLE:"
        context_info += "\nThe user has uploaded a contract for analysis. You can reference this contract when answering their questions."
        context_info += "\nWhen relevant, provide specific insights about their contract terms, risks, and recommendations."
        
        return context_info

    def classify_message_type(self, message):
        """Classify the type of legal question"""
        message_lower = message.lower()
        
        if any(term in message_lower for term in ['risk', 'dangerous', 'problem', 'issue']):
            return 'risk_assessment'
        elif any(term in message_lower for term in ['termination', 'end', 'quit', 'fire']):
            return 'termination'
        elif any(term in message_lower for term in ['payment', 'salary', 'compensation', 'money']):
            return 'compensation'
        elif any(term in message_lower for term in ['confidential', 'nda', 'secret', 'proprietary']):
            return 'confidentiality'
        elif any(term in message_lower for term in ['negotiate', 'change', 'modify', 'improve']):
            return 'negotiation'
        else:
            return 'general'

    def generate_suggestions(self, message, contract_context):
        """Generate contextual suggestions based on message and context"""
        message_type = self.classify_message_type(message)
        
        suggestions_map = {
            'risk_assessment': [
                "What are the highest risk clauses in my contract?",
                "How can I mitigate these contract risks?",
                "What should I negotiate to reduce risks?"
            ],
            'termination': [
                "What are my termination rights?",
                "How much notice is required for termination?",
                "What happens to my benefits if terminated?"
            ],
            'compensation': [
                "Are the payment terms fair and standard?",
                "What protections do I have for salary payments?",
                "Can I negotiate better compensation terms?"
            ],
            'confidentiality': [
                "What information must I keep confidential?",
                "How long do confidentiality obligations last?",
                "What are the penalties for disclosure?"
            ],
            'negotiation': [
                "Which terms should I prioritize in negotiations?",
                "What are common negotiation points?",
                "How can I strengthen my position?"
            ],
            'general': [
                "What are the key risks in this contract?",
                "Which clauses need the most attention?",
                "How does this compare to standard contracts?"
            ]
        }
        
        base_suggestions = suggestions_map.get(message_type, suggestions_map['general'])
        
        if contract_context:
            return base_suggestions
        else:
            return [
                "What should I look for in employment contracts?",
                "How can I identify risky contract terms?",
                "What are common contract negotiation strategies?"
            ]

    def get_fallback_response(self, message, contract_context):
        """Provide intelligent fallback response when Gemini is unavailable"""
        message_type = self.classify_message_type(message)
        
        fallback_responses = {
            'risk_assessment': "I'd be happy to help you assess contract risks. Common high-risk areas include unlimited liability clauses, overly broad confidentiality terms, unfair termination conditions, and intellectual property assignments. For a detailed analysis of your specific contract, I'd recommend uploading the document for comprehensive review.",
            
            'termination': "Termination clauses are crucial to understand. Key points to review include: notice periods required, grounds for immediate termination, severance obligations, and post-termination restrictions. Most employment contracts require 2-4 weeks notice, but this varies by jurisdiction and seniority level.",
            
            'compensation': "Payment terms should be clear and protected. Look for: guaranteed salary amounts, payment schedules, expense reimbursement policies, and protections against delayed payments. Ensure any performance-based compensation has objective, measurable criteria.",
            
            'confidentiality': "Confidentiality obligations typically cover proprietary information, trade secrets, customer data, and business strategies. These obligations usually extend beyond employment termination. Ensure the scope is reasonable and doesn't prevent you from using general skills and knowledge in future roles.",
            
            'negotiation': "Successful contract negotiation focuses on mutual benefit. Key areas to address: compensation and benefits, work conditions and flexibility, intellectual property rights, non-compete restrictions, and termination terms. Prepare alternatives and understand your leverage points.",
            
            'general': "I'm here to help with your legal contract questions. I can assist with risk assessment, clause interpretation, negotiation strategies, and general legal guidance. While I provide practical insights, always consult with a qualified attorney for binding legal advice on important matters."
        }
        
        base_response = fallback_responses.get(message_type, fallback_responses['general'])
        
        if contract_context:
            base_response += " Since you have a contract uploaded, I can provide more specific insights if you share particular clauses or sections you're concerned about."
        
        base_response += "\n\n⚖️ Remember: This is general legal information. For binding legal advice specific to your situation, please consult with a qualified attorney."
        
        return base_response

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