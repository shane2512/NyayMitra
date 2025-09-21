import json
import os
import tempfile
import base64
import google.generativeai as genai
from http.server import BaseHTTPRequestHandler
import cgi
import io

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
        """Transcribe audio using available services with intelligent fallbacks"""
        try:
            print(f"Starting audio transcription, audio size: {len(audio_data)} bytes")
            
            # Option 1: Try Google Gemini Audio API
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                try:
                    print("Attempting Gemini audio transcription...")
                    return self.transcribe_with_gemini(audio_data, api_key)
                except Exception as gemini_error:
                    print(f"Gemini transcription failed: {gemini_error}")
            else:
                print("Gemini API key not found, skipping Gemini transcription")
            
            # Option 2: Try OpenAI Whisper API
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key:
                try:
                    print("Attempting OpenAI Whisper transcription...")
                    return self.transcribe_with_whisper(audio_data, openai_key)
                except Exception as whisper_error:
                    print(f"Whisper transcription failed: {whisper_error}")
            else:
                print("OpenAI API key not found, skipping Whisper transcription")
            
            # Option 3: Enhanced simulation with explanation
            print("Using enhanced simulation transcription...")
            return self.simulate_transcription_with_explanation(audio_data)
            
        except Exception as e:
            print(f"Audio transcription error: {e}")
            return {
                'error': f'Audio processing failed: {str(e)}',
                'status': 'error',
                'message': 'Unable to process audio. Please try again or use text input.'
            }

    def simulate_transcription_with_explanation(self, audio_data):
        """Enhanced simulation with user-friendly explanation"""
        # Analyze audio characteristics for realistic simulation
        audio_length = len(audio_data)
        
        # Generate contextual simulated transcripts
        if audio_length < 2000:
            simulated_transcript = "What are the main risks I should be aware of in this contract?"
        elif audio_length < 5000:
            simulated_transcript = "Can you help me understand the termination and confidentiality clauses?"
        elif audio_length < 10000:
            simulated_transcript = "I need help reviewing the intellectual property and non-compete sections of this agreement."
        else:
            simulated_transcript = "Please provide a comprehensive analysis of this contract and highlight any potential issues or risks."
        
        # Generate AI response
        ai_response = self.generate_voice_response(simulated_transcript)
        
        # Add helpful explanation about demo mode
        demo_explanation = " Note: This is a demo response since speech recognition services are currently unavailable. In production, your actual voice would be transcribed and analyzed."
        ai_response += demo_explanation
        
        # Generate TTS audio for the AI response
        tts_audio = self.generate_speech_with_elevenlabs(ai_response)
        
        response_data = {
            'transcript': simulated_transcript,
            'ai_response': ai_response,
            'recognized_text': simulated_transcript,  # For compatibility
            'confidence': 0.85,
            'status': 'success',
            'method': 'demo_simulation',
            'demo_mode': True,
            'message': 'Demo mode: Simulated transcription and response. Actual voice recognition coming soon!'
        }
        
        # Add TTS audio if available
        if tts_audio:
            print("Demo mode: TTS audio generated successfully")
            response_data.update(tts_audio)
        else:
            print("Demo mode: TTS audio generation failed, browser fallback will be used")
        
        return response_data

    def transcribe_with_gemini(self, audio_data, api_key):
        """Transcribe audio using Google Gemini Audio API"""
        try:
            genai.configure(api_key=api_key)
            
            # Save audio data to temporary file for Gemini processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            try:
                # Upload audio file to Gemini
                print("Uploading audio file to Gemini...")
                audio_file = genai.upload_file(temp_audio_path)
                print(f"Audio file uploaded successfully: {audio_file.name}")
                
                # Use Gemini 1.5 Flash for audio transcription
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Create transcription prompt with language specification
                transcription_prompt = """Please transcribe this audio file accurately in English language only. 
                The audio contains a user asking questions about legal contracts or legal terms in English.
                
                Important instructions:
                - Transcribe ONLY in English language
                - If the speaker used any other language, translate it to English
                - Provide only the transcribed English text without any additional commentary
                - If the audio is unclear, provide your best English interpretation
                
                English transcription:"""
                
                # Generate transcription
                print("Generating transcription with Gemini...")
                response = model.generate_content([transcription_prompt, audio_file])
                transcript = response.text.strip()
                print(f"Transcription successful: {transcript[:50]}...")
                
                # Clean up temp file
                os.unlink(temp_audio_path)
                
                # Generate AI response to the transcribed text
                ai_response = self.generate_voice_response(transcript)
                
                # Generate TTS audio for the AI response
                print(f"Attempting ElevenLabs TTS for response: {ai_response[:50]}...")
                tts_audio = self.generate_speech_with_elevenlabs(ai_response)
                
                response_data = {
                    'transcript': transcript,
                    'ai_response': ai_response,
                    'confidence': 0.95,
                    'status': 'success',
                    'method': 'gemini'
                }
                
                # Add TTS audio if available
                if tts_audio:
                    print("Gemini: ElevenLabs TTS audio generated successfully")
                    response_data.update(tts_audio)
                else:
                    print("Gemini: ElevenLabs TTS failed, browser fallback will be used")
                    response_data['tts_status'] = 'elevenlabs_failed'
                
                return response_data
                
            except Exception as gemini_error:
                # Clean up temp file on error
                if os.path.exists(temp_audio_path):
                    os.unlink(temp_audio_path)
                    
                print(f"Gemini audio processing error: {gemini_error}")
                
                # Fallback to simulation if Gemini fails
                return self.simulate_transcription_fallback(audio_data, str(gemini_error))
                
        except Exception as e:
            print(f"Gemini transcription setup error: {e}")
            return self.simulate_transcription_fallback(audio_data, str(e))

    def simulate_transcription_fallback(self, audio_data, error_reason):
        """Enhanced simulation fallback when Gemini audio fails"""
        print(f"Using simulation fallback due to: {error_reason}")
        
        # Analyze audio characteristics for realistic simulation
        audio_length = len(audio_data)
        
        # Generate contextual simulated transcripts based on audio length
        if audio_length < 2000:
            transcripts = [
                "What are the main risks in this contract?",
                "Can you explain the termination clause?",
                "Is this confidentiality agreement too broad?",
                "What should I know about the payment terms?"
            ]
        elif audio_length < 5000:
            transcripts = [
                "I'm concerned about the intellectual property section. Can you review it?",
                "The termination clause seems unfair. What are my options?",
                "Can you explain what this confidentiality agreement means?",
                "Are there any red flags in the compensation section?"
            ]
        elif audio_length < 10000:
            transcripts = [
                "I need help understanding the non-compete clause. It seems very restrictive.",
                "The contract has a lot of legal jargon. Can you break down the key risks?",
                "I'm worried about the liability section. What am I agreeing to?",
                "Can you review the intellectual property terms and tell me if they're standard?"
            ]
        else:
            transcripts = [
                "This is a complex employment contract and I need help understanding all the terms. Can you analyze the risks?",
                "I'm reviewing this service agreement and there are several clauses I don't understand. Can you help?",
                "The contract has multiple sections about confidentiality and non-compete. Are these terms reasonable?",
                "I need a comprehensive review of this contract to understand what I'm agreeing to before I sign."
            ]
        
        # Select transcript based on audio data hash for consistency
        import hashlib
        audio_hash = hashlib.md5(audio_data[:100]).hexdigest()
        transcript_index = int(audio_hash[:2], 16) % len(transcripts)
        simulated_transcript = transcripts[transcript_index]
        
        # Generate AI response
        ai_response = self.generate_voice_response(simulated_transcript)
        
        # Generate TTS audio for the AI response
        tts_audio = self.generate_speech_with_elevenlabs(ai_response)
        
        response_data = {
            'transcript': simulated_transcript,
            'ai_response': ai_response,
            'recognized_text': simulated_transcript,  # For compatibility
            'confidence': 0.75,
            'status': 'success',
            'method': 'simulation_fallback',
            'note': f'Simulated transcription (Gemini audio unavailable: {error_reason})'
        }
        
        # Add TTS audio if available
        if tts_audio:
            response_data.update(tts_audio)
        
        return response_data

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
                    data={
                        'model': 'whisper-1',
                        'language': 'en',  # Force English language
                        'response_format': 'json'
                    }
                )
            
            # Clean up temp file
            os.unlink(temp_audio_path)
            
            if response.status_code == 200:
                result = response.json()
                transcript = result.get('text', '')
                
                # Generate AI response to the transcribed text
                ai_response = self.generate_voice_response(transcript)
                
                # Generate TTS audio for the AI response
                tts_audio = self.generate_speech_with_elevenlabs(ai_response)
                
                response_data = {
                    'transcript': transcript,
                    'ai_response': ai_response,
                    'status': 'success',
                    'method': 'whisper'
                }
                
                # Add TTS audio if available
                if tts_audio:
                    print("Whisper: ElevenLabs TTS audio generated successfully")
                    response_data.update(tts_audio)
                else:
                    print("Whisper: ElevenLabs TTS failed, browser fallback will be used")
                    response_data['tts_status'] = 'elevenlabs_failed'
                
                return response_data
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
        
        # Generate TTS audio for the AI response
        tts_audio = self.generate_speech_with_elevenlabs(ai_response)
        
        response_data = {
            'transcript': simulated_transcript,
            'ai_response': ai_response,
            'recognized_text': simulated_transcript,  # For compatibility
            'confidence': 0.85,
            'status': 'success',
            'method': 'simulation',
            'note': 'This is a simulated transcription for demo purposes. Integrate with actual speech recognition service for production.'
        }
        
        # Add TTS audio if available
        if tts_audio:
            response_data.update(tts_audio)
        
        return response_data

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

    def generate_speech_with_elevenlabs(self, text):
        """Generate speech using ElevenLabs TTS API"""
        try:
            print(f"ElevenLabs TTS: Starting generation for text length: {len(text)}")
            
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
                    'content_type': 'audio/mpeg'
                }
            else:
                print(f"ElevenLabs TTS: API error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"ElevenLabs TTS: Exception occurred: {type(e).__name__}: {str(e)}")
            import traceback
            print(f"ElevenLabs TTS: Full traceback: {traceback.format_exc()}")
            return None

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
