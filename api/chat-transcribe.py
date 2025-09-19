import json
import os
import base64
import tempfile
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight
from config import Config

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function for audio transcription using ElevenLabs STT.
    """
    try:
        # Handle CORS preflight
        cors_response = handle_cors_preflight(event)
        if cors_response:
            return cors_response
        
        # Check if this is a POST request
        if event.get('httpMethod') != 'POST':
            return create_error_response("Method not allowed", 405)
        
        # Check content type
        content_type = event.get('headers', {}).get('content-type', '')
        if 'multipart/form-data' not in content_type:
            return create_error_response("Content-Type must be multipart/form-data", 400)
        
        # Get audio data from event body
        body = event.get('body', '')
        is_base64 = event.get('isBase64Encoded', False)
        
        if not body:
            return create_error_response("No audio file provided", 400)
        
        try:
            # Decode audio data
            if is_base64:
                audio_data = base64.b64decode(body)
            else:
                audio_data = body.encode('utf-8')
            
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                tmp.write(audio_data)
                wav_path = tmp.name
            
            try:
                # Transcribe audio using ElevenLabs
                transcript = transcribe_audio_elevenlabs(wav_path)
                
                if transcript:
                    result = {
                        'transcript': transcript,
                        'status': 'success'
                    }
                else:
                    result = {
                        'error': 'No speech detected in audio',
                        'status': 'error'
                    }
                
                return create_response(result)
                
            finally:
                # Clean up temp file
                if os.path.exists(wav_path):
                    os.remove(wav_path)
                
        except Exception as parse_error:
            return create_error_response(f"Failed to process audio: {str(parse_error)}", 400)
        
    except Exception as e:
        print(f"[Transcribe API] Error: {e}")
        return create_error_response(f"Transcription failed: {str(e)}", 500)

def transcribe_audio_elevenlabs(audio_path: str) -> str:
    """
    Transcribe audio using ElevenLabs Speech-to-Text API.
    """
    try:
        import requests
        
        if not Config.ELEVEN_API_KEY:
            raise Exception("ElevenLabs API key not configured")
        
        # ElevenLabs STT endpoint
        url = "https://api.elevenlabs.io/v1/speech-to-text"
        
        headers = {
            "xi-api-key": Config.ELEVEN_API_KEY
        }
        
        # Read audio file
        with open(audio_path, 'rb') as audio_file:
            files = {
                'audio': audio_file,
                'model_id': (None, 'whisper-1')
            }
            
            response = requests.post(url, headers=headers, files=files)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('text', '').strip()
        else:
            print(f"ElevenLabs STT error: {response.status_code} - {response.text}")
            return ""
            
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'POST',
        'headers': {'content-type': 'multipart/form-data'},
        'body': '',
        'isBase64Encoded': False
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
