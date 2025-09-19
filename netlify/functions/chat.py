"""
Chat functionality for Netlify Functions.
Handles: chat, chat-batch, chat-history, chat-clear, chat-transcribe, chat-voice
"""

import json
import os
import sys
import tempfile
import time
import base64
from urllib.parse import parse_qs

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from utils import create_response, handle_cors, validate_request
from agents.conversation_agent import ConversationAgent
from agents.rate_limiter import ServerlessRateLimiter

# ElevenLabs integration
try:
    from elevenlabs import generate, save, set_api_key
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

# Note: Using ElevenLabs for TTS only. Transcription uses placeholder implementation.

# Initialize components
conversation_agent = ConversationAgent()
rate_limiter = ServerlessRateLimiter()

# ElevenLabs helper functions
def synthesize_speech(text: str, voice_id: str = None) -> dict:
    """Synthesize speech using ElevenLabs API."""
    if not ELEVENLABS_AVAILABLE:
        raise Exception("ElevenLabs library not available")
    
    if not Config.ELEVEN_API_KEY:
        raise Exception("ElevenLabs API key not configured")
    
    try:
        # Set API key
        set_api_key(Config.ELEVEN_API_KEY)
        
        # Use provided voice_id or default
        voice_id = voice_id or Config.VOICE_ID
        
        # Generate audio
        audio = generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )
        
        # Convert to base64 for JSON response
        audio_base64 = base64.b64encode(audio).decode('utf-8')
        
        return {
            'audio_base64': audio_base64,
            'voice_id': voice_id,
            'text': text,
            'timestamp': time.time()
        }
        
    except Exception as e:
        raise Exception(f"Speech synthesis failed: {str(e)}")

def transcribe_audio(audio_data: bytes) -> dict:
    """Placeholder for audio transcription - can be extended with any STT service."""
    try:
        # Simple placeholder implementation
        # You can integrate with any speech-to-text service here:
        # - Google Speech-to-Text
        # - Azure Speech Services  
        # - AWS Transcribe
        # - Or keep as placeholder for client-side transcription
        
        return {
            'transcription': 'Audio transcription feature available - integrate with your preferred STT service',
            'confidence': 0.0,
            'duration': 0.0,
            'timestamp': time.time(),
            'note': 'Placeholder implementation - ready for STT service integration',
            'supported_formats': ['mp3', 'wav', 'ogg', 'm4a']
        }
        
    except Exception as e:
        raise Exception(f"Audio transcription failed: {str(e)}")

def main(event, context):
    """
    Netlify function handler for chat functionality.
    """
    try:
        # Handle CORS
        if event.get('httpMethod') == 'OPTIONS':
            return handle_cors()
        
        # Get the path to determine which function to execute
        path = event.get('path', '')
        method = event.get('httpMethod', 'GET')
        
        # Route based on path or query parameter
        action = event.get('queryStringParameters', {}).get('action', 'chat')
        
        if action == 'batch':
            return handle_chat_batch(event, context)
        elif action == 'history':
            return handle_chat_history(event, context)
        elif action == 'clear':
            return handle_chat_clear(event, context)
        elif action == 'transcribe':
            return handle_chat_transcribe(event, context)
        elif action == 'voice':
            return handle_chat_voice(event, context)
        else:
            return handle_chat_single(event, context)
            
    except Exception as e:
        return create_response({
            'error': f'Chat handler error: {str(e)}',
            'type': 'server_error'
        }, 500)

def handle_chat_single(event, context):
    """Handle single chat message."""
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        message = body.get('message', '').strip()
        session_id = body.get('session_id')
        contract_context = body.get('contract_context')
        
        if not message:
            return create_response({'error': 'Message cannot be empty'}, 400)
        
        # Process with rate limiting
        def chat_operation():
            return conversation_agent.process_message(
                message=message,
                session_id=session_id,
                contract_context=contract_context
            )
        
        result = rate_limiter.execute_with_rate_limit(chat_operation)
        
        return create_response({
            'status': 'success',
            'response': result.get('response'),
            'session_id': result.get('session_id'),
            'suggestions': result.get('suggestions', []),
            'timestamp': result.get('timestamp')
        })
        
    except Exception as e:
        return create_response({
            'error': f'Chat processing failed: {str(e)}',
            'type': 'processing_error'
        }, 500)

def handle_chat_batch(event, context):
    """Handle batch chat processing."""
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        questions = body.get('questions', [])
        session_id = body.get('session_id')
        contract_context = body.get('contract_context')
        
        if not questions or not isinstance(questions, list):
            return create_response({'error': 'Questions must be a non-empty list'}, 400)
        
        if len(questions) > 10:
            return create_response({'error': 'Maximum 10 questions allowed per batch'}, 400)
        
        # Process batch with rate limiting
        def batch_operation():
            return conversation_agent.process_batch_questions(
                questions=questions,
                session_id=session_id,
                contract_context=contract_context
            )
        
        result = rate_limiter.execute_with_rate_limit(batch_operation)
        
        return create_response({
            'status': 'success',
            'responses': result.get('responses', []),
            'session_id': result.get('session_id'),
            'question_count': len(questions),
            'timestamp': result.get('timestamp')
        })
        
    except Exception as e:
        return create_response({
            'error': f'Batch chat processing failed: {str(e)}',
            'type': 'processing_error'
        }, 500)

def handle_chat_history(event, context):
    """Handle chat history retrieval."""
    try:
        query_params = event.get('queryStringParameters') or {}
        session_id = query_params.get('session_id')
        
        if not session_id:
            return create_response({'error': 'session_id parameter required'}, 400)
        
        history = conversation_agent.get_conversation_history(session_id)
        
        return create_response({
            'status': 'success',
            'session_id': session_id,
            'history': history,
            'message_count': len(history)
        })
        
    except Exception as e:
        return create_response({
            'error': f'Failed to retrieve chat history: {str(e)}',
            'type': 'retrieval_error'
        }, 500)

def handle_chat_clear(event, context):
    """Handle chat session clearing."""
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        session_id = body.get('session_id')
        
        if not session_id:
            return create_response({'error': 'Missing required field: session_id'}, 400)
        
        success = conversation_agent.clear_conversation_history(session_id)
        
        return create_response({
            'status': 'success' if success else 'failed',
            'session_id': session_id,
            'cleared': success,
            'message': 'Session cleared successfully' if success else 'Session not found'
        })
        
    except Exception as e:
        return create_response({
            'error': f'Failed to clear chat session: {str(e)}',
            'type': 'clear_error'
        }, 500)

def handle_chat_transcribe(event, context):
    """Handle audio transcription using OpenAI Whisper."""
    try:
        # Check if audio file is provided
        body = event.get('body', '')
        if event.get('isBase64Encoded'):
            body = base64.b64decode(body)
        
        if not body:
            return create_response({
                'error': 'No audio file provided',
                'supported_formats': ['mp3', 'wav', 'ogg', 'm4a']
            }, 400)
        
        # Process with rate limiting
        def transcription_operation():
            return transcribe_audio(body)
        
        result = rate_limiter.execute_with_rate_limit(transcription_operation)
        
        return create_response({
            'status': 'success',
            'transcription': result.get('transcription'),
            'confidence': result.get('confidence', 0.0),
            'duration': result.get('duration', 0.0),
            'timestamp': result.get('timestamp')
        })
        
    except Exception as e:
        return create_response({
            'error': f'Audio transcription failed: {str(e)}',
            'type': 'transcription_error'
        }, 500)

def handle_chat_voice(event, context):
    """Handle text-to-speech conversion using ElevenLabs."""
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        message = body.get('message', '').strip()
        voice_id = body.get('voice_id', Config.VOICE_ID)
        
        if not message:
            return create_response({'error': 'Message cannot be empty'}, 400)
        
        if not Config.ELEVEN_API_KEY:
            return create_response({
                'error': 'ElevenLabs API key not configured',
                'type': 'configuration_error'
            }, 500)
        
        # Process with rate limiting
        def voice_operation():
            return synthesize_speech(message, voice_id)
        
        result = rate_limiter.execute_with_rate_limit(voice_operation)
        
        return create_response({
            'status': 'success',
            'audio_url': result.get('audio_url'),
            'audio_base64': result.get('audio_base64'),
            'voice_id': voice_id,
            'message': message[:100] + '...' if len(message) > 100 else message,
            'timestamp': result.get('timestamp')
        })
        
    except Exception as e:
        return create_response({
            'error': f'Voice synthesis failed: {str(e)}',
            'type': 'voice_error'
        }, 500)

# Netlify Functions entry point
handler = main
