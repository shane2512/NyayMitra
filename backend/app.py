from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.moderator import ModeratorAgent
from agents.rate_limiter import rate_limiter
from agents.conversation_agent import ConversationAgent
from agents.conversation_moderator import ConversationModerator
from config import Config
import os
import time
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # Enable CORS for React frontend

# Register voice_api Blueprint
from voice_api import voice_api
app.register_blueprint(voice_api)


# Configuration
UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'pdf'}
API_KEY = Config.GEMINI_API_KEY

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize moderator
moderator = ModeratorAgent(API_KEY)
conversation_moderator = ConversationModerator()
conversation_agent = ConversationAgent()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze', methods=['POST'])
def analyze():
    print("=== ANALYZE ENDPOINT CALLED ===")
    print(f"Request files: {request.files}")
    print(f"Request form: {request.form}")
    
    if 'file' not in request.files:
        print("ERROR: No file part in request")
        return jsonify({"error": "No file part", "status": "error"}), 400

    file = request.files['file']
    print(f"File object: {file}")
    print(f"Filename: {file.filename}")
    print(f"Content type: {file.content_type}")
    
    if file.filename == '':
        print("ERROR: No filename provided")
        return jsonify({"error": "No selected file", "status": "error"}), 400

    if not allowed_file(file.filename):
        print(f"ERROR: File type not allowed: {file.filename}")
        return jsonify({"error": "Only PDF files are allowed", "status": "error"}), 400

    try:
        # Save the uploaded PDF temporarily
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        # Use absolute path to avoid issues with relative paths
        pdf_path = os.path.abspath(pdf_path)
        print(f"Saving file to: {pdf_path}")
        
        file.save(pdf_path)
        
        # Check file size after saving
        file_size = os.path.getsize(pdf_path)
        print(f"Saved file size: {file_size} bytes")
        
        if file_size == 0:
            print("ERROR: File size is 0 bytes")
            return jsonify({"error": "File is empty", "status": "error"}), 400

        # Use the Moderator Agent to analyze the contract
        print("Starting analysis...")
        result = moderator.analyze_contract(pdf_path)
        print(f"Analysis result status: {result.get('status', 'unknown')}")
        print(f"Analysis result keys: {list(result.keys()) if isinstance(result, dict) else 'not a dict'}")

        # Clean up temporary file
        os.remove(pdf_path)
        print("Temporary file cleaned up")

        # Ensure we return a proper JSON response
        try:
            json_response = jsonify(result)
            print("JSON response created successfully")
            return json_response
        except Exception as json_error:
            print(f"Error creating JSON response: {json_error}")
            return jsonify({
                "error": "Failed to serialize response",
                "status": "error",
                "details": str(json_error)
            }), 500
    except Exception as e:
        print(f"ERROR in analyze endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "NyayMitra API Server is running!", "version": "1.0", "endpoints": ["/health", "/analyze"]})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": time.time()})

@app.route('/test', methods=['GET'])
def test():
    """Simple test endpoint"""
    return jsonify({
        "message": "Test endpoint working",
        "status": "success",
        "config": {
            "model": Config.GEMINI_MODEL,
            "api_key_present": bool(Config.GEMINI_API_KEY)
        }
    })

# Conversation endpoints
@app.route('/chat', methods=['POST'])
def chat():
    """Handle single chat message"""
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id')
        contract_context = data.get('contract_context')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Set contract context if provided
        if contract_context:
            conversation_moderator.set_contract_context(contract_context)
        
        # Process message
        result = conversation_moderator.process_message(message, session_id)
        return jsonify(result)
        
    except Exception as e:
        print(f"[Chat] Error: {e}")
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/chat/batch', methods=['POST'])
def chat_batch():
    """Handle batch questions"""
    try:
        data = request.json
        questions = data.get('questions', [])
        session_id = data.get('session_id')
        contract_context = data.get('contract_context')
        
        if not questions:
            return jsonify({"error": "No questions provided"}), 400
        
        # Set contract context if provided
        if contract_context:
            conversation_moderator.set_contract_context(contract_context)
        
        # Process batch
        result = conversation_moderator.process_batch(questions, session_id)
        return jsonify(result)
        
    except Exception as e:
        print(f"[Chat Batch] Error: {e}")
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/chat/history', methods=['GET'])
def chat_history():
    """Get chat history for a session"""
    try:
        session_id = request.args.get('session_id')
        history = conversation_moderator.get_session_history(session_id)
        return jsonify({"history": history, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/chat/clear', methods=['POST'])
def chat_clear():
    """Clear chat session"""
    try:
        data = request.json
        session_id = data.get('session_id')
        conversation_moderator.clear_session(session_id)
        return jsonify({"status": "success", "message": "Session cleared"})
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/rate_limit/status', methods=['GET'])
def rate_limit_status():
    """Get current rate limit status"""
    try:
        stats = rate_limiter.get_statistics()
        
        # Calculate remaining requests
        stats['remaining_minute_requests'] = max(0, stats['minute_limit'] - stats['current_minute_requests'])
        stats['remaining_daily_requests'] = max(0, stats['daily_limit'] - stats['current_daily_requests'])
        
        # Add warning levels
        minute_usage_percent = (stats['current_minute_requests'] / stats['minute_limit']) * 100
        daily_usage_percent = (stats['current_daily_requests'] / stats['daily_limit']) * 100
        
        stats['warnings'] = []
        if minute_usage_percent > 80:
            stats['warnings'].append(f"Approaching minute limit: {minute_usage_percent:.0f}% used")
        if daily_usage_percent > 80:
            stats['warnings'].append(f"Approaching daily limit: {daily_usage_percent:.0f}% used")
        if stats['circuit_breaker_open']:
            stats['warnings'].append("Circuit breaker is open - requests are being throttled")
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/rate_limit/reset', methods=['POST'])
def rate_limit_reset():
    """Reset rate limit statistics (for testing only)"""
    try:
        # Only allow in debug mode
        if app.debug:
            rate_limiter.reset_statistics()
            return jsonify({"status": "success", "message": "Rate limit statistics reset"})
        else:
            return jsonify({"error": "Only available in debug mode"}), 403
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500


    """
    Accepts audio (multipart/form-data), runs ElevenLabs STT, Gemini, and ElevenLabs TTS.
    Returns recognized_text, answer, and audio_url.
    """
    import tempfile, shutil, uuid
    from agents.voice_elevenlabs_pipeline import voice_conversation_elevenlabs_pipeline
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided.", "status": "error"}), 400
        audio_file = request.files['audio']
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            audio_file.save(tmp.name)
            wav_path = tmp.name
        result = voice_conversation_elevenlabs_pipeline(wav_path)
        os.remove(wav_path)
        if result.get('status') != 'success':
            return jsonify(result), 400
        # Save TTS audio to static dir
        audio_path = result.get('audio_path')
        static_dir = os.path.join(os.path.dirname(__file__), 'static', 'voice')
        os.makedirs(static_dir, exist_ok=True)
        audio_filename = f"response_{uuid.uuid4().hex}.mp3"
        static_audio_path = os.path.join(static_dir, audio_filename)
        shutil.copy(audio_path, static_audio_path)
        audio_url = f"/static/voice/{audio_filename}"
        response_json = {
            'recognized_text': result.get('recognized_text'),
            'answer': result.get('answer'),
            'audio_url': audio_url,
            'status': 'success'
        }
        return jsonify(response_json)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500



    """
    Accepts raw audio (octet-stream or multipart), samplerate, and sample_width.
    Returns recognized text, Gemini answer, suggestions, session_id, and audio_url (not direct file).
    """
    import shutil, uuid
    try:
        if 'audio' in request.files:
            audio = request.files['audio'].read()
            samplerate = int(request.form.get('samplerate', 16000))
            sample_width = int(request.form.get('sample_width', 2))
        else:
            audio = request.data
            samplerate = int(request.headers.get('X-Sample-Rate', 16000))
            sample_width = int(request.headers.get('X-Sample-Width', 2))
        session_id = request.form.get('session_id') if 'audio' in request.files else request.headers.get('X-Session-Id')
        result = conversation_moderator.process_voice_message(audio, samplerate, sample_width, session_id)
        if result.get('status') != 'success':
            return jsonify(result), 400
        # Save audio to static directory and return URL
        audio_path = result.get('audio_path') or result.get('answer_audio_path')
        static_dir = os.path.join(os.path.dirname(__file__), 'static', 'voice')
        os.makedirs(static_dir, exist_ok=True)
        audio_filename = f"response_{uuid.uuid4().hex}.mp3"
        static_audio_path = os.path.join(static_dir, audio_filename)
        shutil.copy(audio_path, static_audio_path)
        audio_url = f"/static/voice/{audio_filename}"
        response_json = {
            'recognized_text': result.get('recognized_text'),
            'answer': result.get('response'),
            'suggestions': result.get('suggestions'),
            'session_id': result.get('session_id'),
            'audio_url': audio_url,
            'status': 'success'
        }
        return jsonify(response_json)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

# === Voice/Transcription endpoints ===
@app.route('/chat/transcribe', methods=['POST'])
def chat_transcribe():
    """
    Accepts audio (multipart/form-data), runs STT, returns transcript.
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided.', 'status': 'error'}), 400
        
        audio_file = request.files['audio']
        
        # Check file type
        if not audio_file.filename.lower().endswith('.wav'):
            return jsonify({'error': 'Only WAV files are supported.', 'status': 'error'}), 400
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            audio_file.save(tmp.name)
            wav_path = tmp.name
        
        try:
            # Test ElevenLabs API key first
            api_test = conversation_agent.test_elevenlabs_api_key()
            print(f"[Transcribe] ElevenLabs API test: {api_test}")
            
            transcript = conversation_agent.transcribe_audio(wav_path)
            
            if transcript:
                return jsonify({'transcript': transcript, 'status': 'success'})
            else:
                return jsonify({'error': 'No speech detected in audio', 'status': 'error'}), 400
                
        finally:
            # Clean up temp file
            if os.path.exists(wav_path):
                os.remove(wav_path)
                
    except Exception as e:
        print(f"[Transcribe] Error: {e}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/chat/voice', methods=['POST'])
def chat_voice():
    """
    Accepts text or transcript, returns Gemini response and TTS audio URL.
    """
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id')
        contract_context = data.get('contract_context')
        if not message:
            return jsonify({'error': 'No message provided.', 'status': 'error'}), 400
        from agents.conversation_moderator import ConversationModeratorAgent
        moderation = ConversationModeratorAgent().filter_message(message)
        if not moderation['allowed']:
            return jsonify({'error': moderation['reason'], 'status': 'blocked'}), 403
        # Generate AI response
        response_text = conversation_agent.generate_response(message)
        # Generate TTS audio
        tts_audio_bytes = conversation_agent.synthesize_speech(response_text)
        if not tts_audio_bytes:
            return jsonify({'error': 'TTS failed', 'status': 'error'}), 500
        
        # Save TTS audio to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
            tmp.write(tts_audio_bytes)
            tts_path = tmp.name
        static_dir = os.path.join(os.path.dirname(__file__), 'static', 'voice')
        os.makedirs(static_dir, exist_ok=True)
        import uuid, shutil
        audio_filename = f"response_{uuid.uuid4().hex}.mp3"
        static_audio_path = os.path.join(static_dir, audio_filename)
        shutil.copy(tts_path, static_audio_path)
        audio_url = f"/static/voice/{audio_filename}"
        print(f"[ChatVoice] audio_filename: {audio_filename}")
        print(f"[ChatVoice] audio_url returned: {audio_url}")
        print(f"[ChatVoice] static_audio_path: {static_audio_path}")
        return jsonify({'audio_url': audio_url, 'answer': response_text, 'status': 'success'})
    except Exception as e:
        print(f"[ChatVoice] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/debug/api-keys', methods=['GET'])
def debug_api_keys():
    """Debug endpoint to check API key status"""
    try:
        # Test ElevenLabs API key
        elevenlabs_test = conversation_agent.test_elevenlabs_api_key()
        
        # Test Gemini API key (simple check)
        gemini_configured = bool(conversation_agent.gemini_api_key)
        
        return jsonify({
            "elevenlabs": elevenlabs_test,
            "gemini_configured": gemini_configured,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)