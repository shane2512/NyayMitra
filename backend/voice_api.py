from flask import Blueprint, request, jsonify, send_file, send_from_directory
from agents.voice_utils import recognize_speech_from_file, synthesize_speech
from agents.voice_conversation_agent import voice_conversation_pipeline
import os
import time

voice_api = Blueprint('voice_api', __name__)

# Ensure temp directory exists
os.makedirs('temp', exist_ok=True)

@voice_api.route('/voice/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        audio_file = request.files['audio']
        # Save to temp file
        temp_path = os.path.join('temp', audio_file.filename)
        audio_file.save(temp_path)
        text = recognize_speech_from_file(temp_path)
        os.remove(temp_path)
        if text:
            return jsonify({'text': text, 'status': 'success'})
        else:
            return jsonify({'error': 'Could not recognize speech', 'status': 'error'}), 400
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@voice_api.route('/voice/synthesize', methods=['POST'])
def synthesize():
    try:
        data = request.json
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        audio_path = synthesize_speech(text)
        # Return file as download
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        os.remove(audio_path)
        return (audio_data, 200, {'Content-Type': 'audio/mpeg', 'Content-Disposition': 'attachment; filename="output.mp3"'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@voice_api.route('/voice/ai', methods=['POST'])
def voice_ai():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        audio_file = request.files['audio']
        import tempfile
        from pydub import AudioSegment
        # Save uploaded audio to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.input') as tmp:
            audio_file.save(tmp.name)
            input_path = tmp.name
        # Convert to WAV using pydub
        try:
            wav_path = input_path + '.wav'
            audio = AudioSegment.from_file(input_path)
            audio.export(wav_path, format='wav')
        except Exception as e:
            os.remove(input_path)
            return jsonify({'error': f'Could not convert audio to WAV: {e}', 'status': 'error'}), 400
        # Run pipeline on WAV
        result = voice_conversation_pipeline(wav_path)
        os.remove(input_path)
        os.remove(wav_path)
        if result['status'] != 'success':
            return jsonify(result), 400
        audio_path = result['audio_path']
        # Save audio to a temp directory for frontend playback
        temp_dir = os.path.join('temp', 'voice_responses')
        os.makedirs(temp_dir, exist_ok=True)
        out_name = f"voice_response_{int(time.time())}.mp3"
        temp_audio_path = os.path.join(temp_dir, out_name)
        import shutil
        # Copy from system temp to our project temp directory
        shutil.copy(audio_path, temp_audio_path)
        # Clean up the original temp file
        if os.path.exists(audio_path):
            os.remove(audio_path)
        audio_url = f"/temp/voice_responses/{out_name}"
        response = {
            'recognized_text': result['recognized_text'],
            'answer': result['answer'],
            'audio_url': audio_url,
            'status': 'success'
        }
        print(f"[VoiceAPI] Returning response: {response}")  # Debug log
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

# Serve temp audio files for playback
@voice_api.route('/temp/voice_responses/<filename>')
def serve_temp_audio(filename):
    try:
        temp_dir = os.path.join('temp', 'voice_responses')
        file_path = os.path.join(temp_dir, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'Audio file not found'}), 404
        
        # Serve with proper headers for audio playback
        response = send_from_directory(temp_dir, filename)
        response.headers['Content-Type'] = 'audio/mpeg'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Cache-Control'] = 'no-cache'
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to delete all temp audios after conversation ends
@voice_api.route('/voice/cleanup', methods=['POST'])
def cleanup_temp_audio():
    import shutil
    temp_dir = os.path.join('temp', 'voice_responses')
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)
        return jsonify({'status': 'success', 'message': 'All temp audios deleted.'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})


    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500
