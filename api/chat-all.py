"""
Consolidated chat endpoints to reduce function count for Vercel Hobby plan.
Handles: chat, chat-batch, chat-history, chat-clear, chat-transcribe, chat-voice
"""

import json
import os
import sys
from urllib.parse import parse_qs

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from utils import create_response, handle_cors, validate_request
from agents.conversation_agent import ConversationAgent
from agents.rate_limiter import ServerlessRateLimiter

# Initialize components
conversation_agent = ConversationAgent()
rate_limiter = ServerlessRateLimiter()

def handler(event, context):
    """
    Consolidated chat handler for multiple endpoints.
    Routes based on the path parameter.
    """
    try:
        # Handle CORS
        if event.get('httpMethod') == 'OPTIONS':
            return handle_cors()
        
        # Get the path to determine which function to execute
        path = event.get('path', '')
        method = event.get('httpMethod', 'GET')
        
        # Route to appropriate function based on path
        if '/chat-batch' in path:
            return handle_chat_batch(event, context)
        elif '/chat-history' in path:
            return handle_chat_history(event, context)
        elif '/chat-clear' in path:
            return handle_chat_clear(event, context)
        elif '/chat-transcribe' in path:
            return handle_chat_transcribe(event, context)
        elif '/chat-voice' in path:
            return handle_chat_voice(event, context)
        elif '/chat' in path:
            return handle_chat_single(event, context)
        else:
            return create_response({
                'error': 'Invalid chat endpoint',
                'available_endpoints': [
                    '/api/chat-all/chat',
                    '/api/chat-all/chat-batch', 
                    '/api/chat-all/chat-history',
                    '/api/chat-all/chat-clear',
                    '/api/chat-all/chat-transcribe',
                    '/api/chat-all/chat-voice'
                ]
            }, 404)
            
    except Exception as e:
        return create_response({
            'error': f'Chat handler error: {str(e)}',
            'type': 'server_error'
        }, 500)

def handle_chat_single(event, context):
    """Handle single chat message."""
    try:
        # Validate request
        if not validate_request(event, ['message']):
            return create_response({'error': 'Missing required field: message'}, 400)
        
        body = json.loads(event.get('body', '{}'))
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
        if not validate_request(event, ['questions']):
            return create_response({'error': 'Missing required field: questions'}, 400)
        
        body = json.loads(event.get('body', '{}'))
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
        query_params = parse_qs(event.get('queryStringParameters') or {})
        session_id = query_params.get('session_id', [None])[0]
        
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
        if not validate_request(event, ['session_id']):
            return create_response({'error': 'Missing required field: session_id'}, 400)
        
        body = json.loads(event.get('body', '{}'))
        session_id = body.get('session_id')
        
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
    """Handle audio transcription (placeholder - requires ElevenLabs integration)."""
    try:
        return create_response({
            'status': 'success',
            'message': 'Audio transcription endpoint available',
            'note': 'Upload audio file for transcription',
            'supported_formats': ['mp3', 'wav', 'ogg', 'm4a']
        })
        
    except Exception as e:
        return create_response({
            'error': f'Transcription service error: {str(e)}',
            'type': 'transcription_error'
        }, 500)

def handle_chat_voice(event, context):
    """Handle text-to-speech conversion (placeholder - requires ElevenLabs integration)."""
    try:
        return create_response({
            'status': 'success',
            'message': 'Text-to-speech endpoint available',
            'note': 'Send text for voice synthesis',
            'voice_id': Config.VOICE_ID or 'default'
        })
        
    except Exception as e:
        return create_response({
            'error': f'Voice synthesis service error: {str(e)}',
            'type': 'voice_error'
        }, 500)
