import json
import os
import google.generativeai as genai
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import time
import hashlib
import base64

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available in serverless environment

# Try to import ElevenLabs for TTS
try:
    import requests
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

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
            voice_mode = data.get('voice_mode', False)
            
            if not message:
                return {'error': 'No message provided', 'status': 'error'}
            
            # Generate AI response
            if voice_mode:
                ai_response = self.generate_voice_optimized_response(message, contract_context)
            else:
                ai_response = self.generate_legal_response(message, contract_context)
            
            # Generate contextual suggestions based on message type
            suggestions = self.generate_suggestions(message, contract_context)
            
            response_data = {
                'response': ai_response,
                'session_id': session_id,
                'suggestions': suggestions,
                'status': 'success',
                'timestamp': time.time(),
                'message_type': self.classify_message_type(message)
            }
            
            # Generate TTS audio for voice mode
            if voice_mode:
                print(f"Voice mode detected - generating TTS for response length: {len(ai_response)}")
                tts_audio = self.generate_speech_with_elevenlabs(ai_response)
                if tts_audio:
                    print("Successfully generated ElevenLabs TTS audio")
                    response_data.update(tts_audio)
                    response_data['tts_method'] = 'elevenlabs'
                else:
                    print("ElevenLabs TTS failed - browser fallback will be used")
                    response_data['tts_status'] = 'elevenlabs_failed'
                    response_data['tts_method'] = 'browser_fallback'
                    # Add helpful info for frontend to handle fallback
                    response_data['fallback_reason'] = 'ElevenLabs TTS unavailable'
            
            return response_data
            
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
        """Handle voice message processing with enhanced features"""
        try:
            message = data.get('message', '')
            session_id = data.get('session_id', 'default')
            contract_context = data.get('contract_context')
            audio_data = data.get('audio_data')  # Base64 encoded audio
            
            if not message and not audio_data:
                return {'error': 'No message or audio data provided', 'status': 'error'}
            
            # If audio data is provided, process it first
            if audio_data and not message:
                # Decode and process audio (placeholder for now)
                try:
                    # This would integrate with speech recognition service
                    message = "Voice message received - transcription feature coming soon"
                except Exception as audio_error:
                    return {'error': f'Audio processing failed: {str(audio_error)}', 'status': 'error'}
            
            # Generate voice-optimized response
            ai_response = self.generate_voice_optimized_response(message, contract_context)
            
            # Generate ElevenLabs TTS audio for the AI response
            print(f"Voice message: Attempting ElevenLabs TTS for response...")
            tts_audio = self.generate_speech_with_elevenlabs(ai_response)
            
            response_data = {
                'answer': ai_response,
                'response': ai_response,  # For compatibility
                'transcript': message,
                'session_id': session_id,
                'status': 'success',
                'voice_enabled': True,
                'suggestions': self.generate_voice_suggestions(message)
            }
            
            # Add TTS audio if available
            if tts_audio:
                print("Voice message: ElevenLabs TTS audio generated successfully")
                response_data.update(tts_audio)
                response_data['audio_url'] = None  # Clear old placeholder
            else:
                print("Voice message: ElevenLabs TTS failed, browser fallback will be used")
                response_data['tts_status'] = 'elevenlabs_failed'
                response_data['audio_url'] = None
            
            return response_data
            
        except Exception as e:
            return {'error': str(e), 'status': 'error'}

    def generate_voice_optimized_response(self, message, contract_context=None):
        """Generate response optimized for voice interaction"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                return self.get_voice_fallback_response(message, contract_context)
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Voice-specific system prompt
            voice_system_prompt = """You are NyayMitra AI, a voice-enabled legal assistant. Respond as if speaking to the user directly.

Voice Response Guidelines:
- Use conversational, natural speech patterns
- Keep responses under 150 words for comfortable listening
- Use "you" and "your" to address the user directly
- Avoid complex sentences; use clear, simple language
- Include brief pauses with natural punctuation
- End with a clear next step or question when appropriate
- Be warm and professional, as if speaking face-to-face"""

            context_info = ""
            if contract_context:
                context_info = "\n\nThe user has uploaded a contract that you can reference in your response."

            voice_prompt = f"""{voice_system_prompt}{context_info}

User said: "{message}"

Provide a natural, conversational spoken response:"""

            response = model.generate_content(voice_prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Voice response error: {e}")
            return self.get_voice_fallback_response(message, contract_context)

    def get_voice_fallback_response(self, message, contract_context):
        """Voice-optimized fallback responses"""
        message_lower = message.lower()
        
        # Voice-friendly responses for common topics
        if 'risk' in message_lower or 'dangerous' in message_lower or 'problem' in message_lower:
            return "I understand you're concerned about risks in your contract. The main areas to watch are termination terms, liability clauses, and intellectual property rights. These can really impact your future. Would you like me to explain any specific section?"
        
        elif 'termination' in message_lower or 'quit' in message_lower or 'fired' in message_lower:
            return "Termination clauses are super important to understand. Most contracts need two to four weeks notice, but yours might be different. Look for severance terms and any restrictions after you leave. What specific part worries you most?"
        
        elif 'confidential' in message_lower or 'nda' in message_lower or 'secret' in message_lower:
            return "Confidentiality terms protect company secrets, but they shouldn't be too broad. You should still be able to use your general skills at future jobs. The key is making sure it's reasonable in scope and time. Does yours seem overly restrictive?"
        
        elif 'money' in message_lower or 'salary' in message_lower or 'payment' in message_lower or 'pay' in message_lower:
            return "Payment terms should be crystal clear in your contract. Make sure you understand the exact amounts, when you get paid, and any performance bonuses. Also check expense policies and benefit contributions. Is there something specific about the payment terms that concerns you?"
        
        elif 'negotiate' in message_lower or 'change' in message_lower or 'better' in message_lower:
            return "Good thinking about negotiation! Focus on what matters most to you - maybe salary, flexible work, or better termination terms. Come prepared with specific alternatives and be ready to explain why they're fair. What's your top priority to negotiate?"
        
        else:
            response = f"Thanks for asking about your contract. I'm here to help you understand the legal terms and spot any issues. "
            if contract_context:
                response += "Since you've uploaded a contract, I can give you specific advice about your document. "
            response += "What specific part would you like me to explain first?"
            return response

    def generate_speech_with_elevenlabs(self, text):
        """Generate speech using ElevenLabs TTS API - primary TTS method"""
        try:
            print(f"ElevenLabs TTS: Starting generation for text length: {len(text)}")
            
            # Check if text is too long (ElevenLabs has limits)
            if len(text) > 2500:
                print("ElevenLabs TTS: Text too long, truncating...")
                text = text[:2400] + "..."
            
            if not ELEVENLABS_AVAILABLE:
                print("ElevenLabs TTS: requests module not available")
                return None
                
            api_key = os.getenv('ELEVEN_API_KEY') or os.getenv('ELEVENLABS_API_KEY')
            if not api_key:
                print("ElevenLabs TTS: API key not found. Checked ELEVEN_API_KEY and ELEVENLABS_API_KEY")
                return None
            
            print(f"ElevenLabs TTS: API key found (first 8 chars): {api_key[:8]}...")
            print(f"ElevenLabs TTS: Generating for text: {text[:100]}...")
            
            # ElevenLabs API endpoint and voice
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice (professional female)
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.3,
                    "use_speaker_boost": True
                }
            }
            
            print("ElevenLabs TTS: Making API request...")
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            print(f"ElevenLabs TTS: Response status: {response.status_code}")
            print(f"ElevenLabs TTS: Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                audio_size = len(response.content)
                print(f"ElevenLabs TTS: Success - audio size: {audio_size} bytes")
                
                if audio_size == 0:
                    print("ElevenLabs TTS: Warning - empty audio response")
                    return None
                
                # Return base64 encoded audio
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                print(f"ElevenLabs TTS: Base64 encoded audio length: {len(audio_base64)}")
                
                return {
                    'audio_data': audio_base64,
                    'audio_format': 'mp3',
                    'content_type': 'audio/mpeg',
                    'tts_provider': 'elevenlabs'
                }
            elif response.status_code == 401:
                print("ElevenLabs TTS: Authentication failed - check API key")
                return None
            elif response.status_code == 422:
                print(f"ElevenLabs TTS: Validation error - {response.text}")
                return None
            else:
                print(f"ElevenLabs TTS: API error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("ElevenLabs TTS: Request timeout - API is slow or unavailable")
            return None
        except requests.exceptions.ConnectionError:
            print("ElevenLabs TTS: Connection error - check internet connection")
            return None
        except Exception as e:
            print(f"ElevenLabs TTS: Exception occurred: {type(e).__name__}: {str(e)}")
            import traceback
            print(f"ElevenLabs TTS: Full traceback: {traceback.format_exc()}")
            return None

    def generate_voice_suggestions(self, message):
        """Generate voice-friendly suggestions"""
        message_type = self.classify_message_type(message)
        
        voice_suggestions = {
            'risk_assessment': [
                "What's the biggest risk in my contract?",
                "Should I be worried about any clauses?",
                "How can I protect myself better?"
            ],
            'termination': [
                "How much notice do I need to give?",
                "What happens if I get fired?",
                "Are there any restrictions after I leave?"
            ],
            'compensation': [
                "Are my payment terms fair?",
                "When exactly do I get paid?",
                "What about bonuses and benefits?"
            ],
            'confidentiality': [
                "What can't I tell people?",
                "How long do these rules last?",
                "Can I still use my skills elsewhere?"
            ],
            'negotiation': [
                "What should I try to negotiate?",
                "How do I ask for better terms?",
                "What's reasonable to request?"
            ],
            'general': [
                "What should I know about this contract?",
                "Are there any red flags?",
                "What questions should I ask?"
            ]
        }
        
        return voice_suggestions.get(message_type, voice_suggestions['general'])

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