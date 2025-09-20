import json
import os
import tempfile
import base64
import google.generativeai as genai
from http.server import BaseHTTPRequestHandler
import cgi
import io

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_POST(self):
        try:
            # Handle CORS
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Parse multipart form data for audio file
            content_type = self.headers.get('Content-Type', '')
            if content_type.startswith('multipart/form-data'):
                # Parse form data with audio file
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                
                if 'audio' in form:
                    audio_file = form['audio']
                    audio_data = audio_file.file.read()
                    
                    # Process audio transcription
                    result = self.transcribe_audio(audio_data)
                    self.wfile.write(json.dumps(result).encode())
                else:
                    error_response = {
                        'error': 'No audio file provided',
                        'status': 'error'
                    }
                    self.wfile.write(json.dumps(error_response).encode())
            else:
                # Handle JSON request (for demo/testing)
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    body = self.rfile.read(content_length).decode('utf-8')
                    try:
                        data = json.loads(body)
                        # Demo transcription
                        demo_transcript = data.get('demo_text', 'Hello, this is a test voice message about contract terms.')
                        result = self.generate_voice_response(demo_transcript)
                        self.wfile.write(json.dumps(result).encode())
                    except:
                        error_response = {'error': 'Invalid JSON', 'status': 'error'}
                        self.wfile.write(json.dumps(error_response).encode())
                else:
                    error_response = {'error': 'No data provided', 'status': 'error'}
                    self.wfile.write(json.dumps(error_response).encode())
                
        except Exception as e:
            try:
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                error_response = {
                    'error': f'Transcription error: {str(e)}',
                    'status': 'error'
                }
                
                print(f"Transcription error: {str(e)}")
                self.wfile.write(json.dumps(error_response).encode())
            except:
                pass

    def transcribe_audio(self, audio_data):
        """Transcribe audio using available services"""
        try:
            # Option 1: Try Google Gemini Audio (if supported)
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                try:
                    # Note: This is a placeholder for Gemini audio processing
                    # Actual implementation would depend on Gemini's audio capabilities
                    return self.transcribe_with_gemini(audio_data, api_key)
                except Exception as gemini_error:
                    print(f"Gemini transcription failed: {gemini_error}")
            
            # Option 2: Try OpenAI Whisper API (if available)
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key:
                try:
                    return self.transcribe_with_whisper(audio_data, openai_key)
                except Exception as whisper_error:
                    print(f"Whisper transcription failed: {whisper_error}")
            
            # Option 3: Browser-based transcription simulation
            return self.simulate_transcription(audio_data)
            
        except Exception as e:
            print(f"Audio transcription error: {e}")
            return {
                'error': f'Audio processing failed: {str(e)}',
                'status': 'error'
            }

    def transcribe_with_gemini(self, audio_data, api_key):
        """Attempt transcription with Gemini (placeholder)"""
        # This is a placeholder - actual Gemini audio API integration would go here
        return {
            'transcript': 'Gemini audio transcription not yet implemented. Please use text input.',
            'confidence': 0.0,
            'status': 'success',
            'method': 'gemini_placeholder'
        }

    def transcribe_with_whisper(self, audio_data, api_key):
        """Transcribe using OpenAI Whisper API"""
        try:
            import requests
            
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            # Send to OpenAI Whisper API
            with open(temp_audio_path, 'rb') as audio_file:
                response = requests.post(
                    'https://api.openai.com/v1/audio/transcriptions',
                    headers={'Authorization': f'Bearer {api_key}'},
                    files={'file': audio_file},
                    data={'model': 'whisper-1'}
                )
            
            # Clean up temp file
            os.unlink(temp_audio_path)
            
            if response.status_code == 200:
                result = response.json()
                transcript = result.get('text', '')
                
                # Generate AI response to the transcribed text
                ai_response = self.generate_voice_response(transcript)
                
                return {
                    'transcript': transcript,
                    'ai_response': ai_response,
                    'status': 'success',
                    'method': 'whisper'
                }
            else:
                return {
                    'error': 'Whisper API error',
                    'status': 'error'
                }
                
        except Exception as e:
            return {
                'error': f'Whisper transcription failed: {str(e)}',
                'status': 'error'
            }

    def simulate_transcription(self, audio_data):
        """Simulate transcription for demo purposes"""
        # Analyze audio characteristics for a more realistic simulation
        audio_length = len(audio_data)
        
        if audio_length < 1000:
            simulated_transcript = "What are the key risks in this contract?"
        elif audio_length < 5000:
            simulated_transcript = "Can you explain the termination clause in my employment agreement?"
        elif audio_length < 10000:
            simulated_transcript = "I'm concerned about the confidentiality terms. Are they too broad?"
        else:
            simulated_transcript = "Please review the intellectual property section and tell me if there are any issues I should be aware of."
        
        # Generate AI response
        ai_response = self.generate_voice_response(simulated_transcript)
        
        return {
            'transcript': simulated_transcript,
            'ai_response': ai_response,
            'recognized_text': simulated_transcript,  # For compatibility
            'confidence': 0.85,
            'status': 'success',
            'method': 'simulation',
            'note': 'This is a simulated transcription for demo purposes. Integrate with actual speech recognition service for production.'
        }

    def generate_voice_response(self, transcript):
        """Generate AI response to transcribed voice input"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                return self.get_fallback_voice_response(transcript)
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Create voice-optimized prompt
            voice_prompt = f"""You are NyayMitra AI, a legal assistant. The user asked via voice: "{transcript}"

Provide a conversational, voice-friendly response that:
- Directly answers their question
- Uses natural, spoken language (not written)
- Keeps responses under 200 words for voice playback
- Focuses on key points they need to know
- Includes a brief disclaimer about consulting lawyers for binding advice

Response:"""

            response = model.generate_content(voice_prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Voice response generation error: {e}")
            return self.get_fallback_voice_response(transcript)

    def get_fallback_voice_response(self, transcript):
        """Provide intelligent fallback voice response"""
        transcript_lower = transcript.lower()
        
        # Analyze transcript for key topics
        if 'risk' in transcript_lower or 'dangerous' in transcript_lower:
            return "Great question about contract risks. Key areas to watch include termination terms, liability clauses, and intellectual property assignments. These can significantly impact your rights and obligations. I'd recommend having a lawyer review any concerning sections before signing."
        
        elif 'termination' in transcript_lower or 'quit' in transcript_lower or 'fire' in transcript_lower:
            return "Termination clauses are crucial to understand. Look for notice requirements, severance terms, and any post-employment restrictions. Most contracts require two to four weeks notice, but this varies. Make sure the terms are fair and reasonable for your situation."
        
        elif 'confidential' in transcript_lower or 'nda' in transcript_lower:
            return "Confidentiality terms protect company information but shouldn't be overly broad. They should clearly define what's confidential and allow you to use general skills and knowledge in future roles. Be cautious of indefinite time periods or unclear scope."
        
        elif 'intellectual property' in transcript_lower or 'ip' in transcript_lower:
            return "Intellectual property clauses determine who owns work you create. Company ownership of work-related inventions is standard, but be careful of clauses claiming personal projects or pre-existing IP. Ensure the scope is reasonable and job-related."
        
        elif 'payment' in transcript_lower or 'salary' in transcript_lower:
            return "Payment terms should be clear and protected. Look for guaranteed amounts, payment schedules, and expense policies. Ensure any performance-based pay has objective criteria. You should also understand overtime policies and benefit contributions."
        
        else:
            return f"Thanks for your question about {transcript}. I'm here to help with contract analysis and legal guidance. For detailed advice on your specific situation, I recommend uploading your contract for comprehensive review, or consulting with a qualified attorney for binding legal advice."

    def do_GET(self):
        self.send_response(405)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        error_response = {
            'error': 'Method not allowed. Use POST for audio transcription.',
            'status': 'error'
        }
        self.wfile.write(json.dumps(error_response).encode())
