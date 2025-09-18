from agents.conversation_agent import ConversationAgent
from agents.conversation_moderator import ConversationModeratorAgent

# ... (rest of your imports and app setup)

# Initialize conversation agent and moderator
conversation_moderator = ConversationModeratorAgent()
conversation_agent = ConversationAgent(moderator=conversation_moderator)

@app.route('/chat/transcribe', methods=['POST'])
def chat_transcribe():
    """
    Accepts audio (multipart/form-data), runs ElevenLabs STT, returns transcript.
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided.', 'status': 'error'}), 400
        audio_file = request.files['audio']
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            audio_file.save(tmp.name)
            wav_path = tmp.name
        transcript = conversation_agent.transcribe_audio(wav_path)
        os.remove(wav_path)
        return jsonify({'transcript': transcript, 'status': 'success'})
    except Exception as e:
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
        moderation = conversation_moderator.filter_message(message)
        if not moderation['allowed']:
            return jsonify({'error': moderation['reason'], 'status': 'blocked'}), 403
        result = conversation_agent.moderate_and_send(message)
        if 'error' in result:
            return jsonify({'error': result['error'], 'status': 'error'}), 500
        response_text = result['response']
        # Generate TTS audio
        tts_path = conversation_agent.text_to_speech(response_text)
        static_dir = os.path.join(os.path.dirname(__file__), 'static', 'voice')
        os.makedirs(static_dir, exist_ok=True)
        import uuid, shutil
        audio_filename = f"response_{uuid.uuid4().hex}.mp3"
        static_audio_path = os.path.join(static_dir, audio_filename)
        shutil.copy(tts_path, static_audio_path)
        audio_url = f"/static/voice/{audio_filename}"
        return jsonify({'audio_url': audio_url, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500
