import json
import os
import tempfile
import uuid
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight, parse_request_body
from agents.conversation_agent import ConversationAgent
from config import Config

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function for text-to-speech conversion of chat responses.
    """
    try:
        # Handle CORS preflight
        cors_response = handle_cors_preflight(event)
        if cors_response:
            return cors_response
        
        # Check if this is a POST request
        if event.get('httpMethod') != 'POST':
            return create_error_response("Method not allowed", 405)
        
        # Parse request body
        data = parse_request_body(event)
        
        message = data.get('message', '')
        session_id = data.get('session_id')
        contract_context = data.get('contract_context')
        
        if not message:
            return create_error_response("No message provided", 400)
        
        # Initialize conversation agent
        conversation_agent = ConversationAgent()
        
        # Generate AI response
        chat_result = conversation_agent.process_message(message, session_id, contract_context)
        
        if chat_result.get('status') != 'success':
            return create_response(chat_result)
        
        response_text = chat_result.get('response', '')
        
        # Generate TTS audio
        try:
            audio_url = synthesize_speech_elevenlabs(response_text)
            
            result = {
                'answer': response_text,
                'audio_url': audio_url,
                'suggestions': chat_result.get('suggestions', []),
                'session_id': chat_result.get('session_id'),
                'status': 'success'
            }
            
            return create_response(result)
            
        except Exception as tts_error:
            # Return text response even if TTS fails
            result = {
                'answer': response_text,
                'audio_url': None,
                'suggestions': chat_result.get('suggestions', []),
                'session_id': chat_result.get('session_id'),
                'tts_error': str(tts_error),
                'status': 'partial_success'
            }
            
            return create_response(result)
        
    except Exception as e:
        print(f"[Chat Voice API] Error: {e}")
        return create_error_response(f"Voice chat failed: {str(e)}", 500)

def synthesize_speech_elevenlabs(text: str) -> str:
    """
    Convert text to speech using ElevenLabs TTS API and return audio URL.
    """
    try:
        import requests
        
        if not Config.ELEVEN_API_KEY or not Config.VOICE_ID:
            raise Exception("ElevenLabs API key or Voice ID not configured")
        
        # ElevenLabs TTS endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{Config.VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": Config.ELEVEN_API_KEY
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save audio to temporary file and return a placeholder URL
            # In a real serverless environment, you'd upload to cloud storage
            audio_filename = f"response_{uuid.uuid4().hex}.mp3"
            
            # For serverless, we'd typically upload to S3/CloudFlare/etc
            # For now, return a placeholder URL
            audio_url = f"/api/audio/{audio_filename}"
            
            # In production, save to cloud storage here
            # save_audio_to_storage(response.content, audio_filename)
            
            return audio_url
        else:
            print(f"ElevenLabs TTS error: {response.status_code} - {response.text}")
            raise Exception(f"TTS API error: {response.status_code}")
            
    except Exception as e:
        print(f"TTS synthesis error: {e}")
        raise e

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'POST',
        'headers': {'content-type': 'application/json'},
        'body': json.dumps({
            'message': 'What are the key terms in this contract?',
            'session_id': 'test_voice_session'
        }),
        'isBase64Encoded': False
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
