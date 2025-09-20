import json
import os
import google.generativeai as genai
from urllib.parse import parse_qs

def handler(request, context):
    """Vercel serverless function handler for chat conversations."""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({})
        }
    
    try:
        # Get query parameters to determine action
        query_params = {}
        if hasattr(request, 'args'):
            query_params = request.args
        elif hasattr(request, 'query_string') and request.query_string:
            query_params = parse_qs(request.query_string)
            # Convert list values to single values
            query_params = {k: v[0] if isinstance(v, list) and v else v for k, v in query_params.items()}
        
        action = query_params.get('action', 'chat')
        
        if action == 'batch':
            return handle_chat_batch(request, headers)
        elif action == 'history':
            return handle_chat_history(request, headers)
        elif action == 'clear':
            return handle_chat_clear(request, headers)
        elif action == 'transcribe':
            return handle_chat_transcribe(request, headers)
        elif action == 'voice':
            return handle_chat_voice(request, headers)
        else:
            return handle_chat_single(request, headers)
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': f'Chat handler error: {str(e)}',
                'status': 'error'
            })
        }

def handle_chat_single(request, headers):
    """Handle single chat message."""
    if request.method == 'POST':
        try:
            # Get the request body
            if hasattr(request, 'json') and request.json:
                data = request.json
            else:
                body = request.body
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                data = json.loads(body)
            
            message = data.get('message', '')
            session_id = data.get('session_id')
            contract_context = data.get('contract_context')
            
            if not message:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'No message provided', 'status': 'error'})
                }
            
            # Configure Gemini
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({
                        'error': 'GEMINI_API_KEY environment variable not set',
                        'status': 'error'
                    })
                }
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Build prompt with context
            system_prompt = """You are NyayMitra AI, a helpful legal assistant specializing in contract analysis and legal guidance.
You provide clear, accurate, and practical legal information while being conversational and friendly.
Important guidelines:
- Provide practical, actionable advice
- Use simple language, avoid legal jargon unless necessary
- Be concise but thorough
- If discussing contracts, focus on risk assessment and practical implications
- Always remind users that for binding legal advice, they should consult a qualified lawyer
- Be helpful and empathetic to users' legal concerns"""

            context_info = ""
            if contract_context:
                context_info = f"\n\nContract Context Available: The user has uploaded a contract for analysis. You can reference this context when answering questions about their specific contract."

            full_prompt = f"""{system_prompt}{context_info}

User: {message}

Please provide a helpful, conversational response:"""

            # Generate response
            response = model.generate_content(full_prompt)
            ai_response = response.text
            
            # Generate suggestions (simple example)
            suggestions = [
                "What are common contract risks?",
                "How should I review employment terms?",
                "What clauses should I pay attention to?"
            ]
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'response': ai_response,
                    'session_id': session_id or 'default',
                    'suggestions': suggestions,
                    'status': 'success'
                })
            }
            
        except Exception as e:
            print(f"Chat error: {e}")
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    'error': str(e),
                    'status': 'error'
                })
            }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed', 'status': 'error'})
    }

def handle_chat_batch(request, headers):
    """Handle batch chat processing."""
    if request.method == 'POST':
        try:
            # Get the request body
            if hasattr(request, 'json') and request.json:
                data = request.json
            else:
                body = request.body
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                data = json.loads(body)
            
            questions = data.get('questions', [])
            session_id = data.get('session_id')
            contract_context = data.get('contract_context')
            
            if not questions or not isinstance(questions, list):
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Questions must be a non-empty list', 'status': 'error'})
                }
            
            if len(questions) > 10:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Maximum 10 questions allowed per batch', 'status': 'error'})
                }
            
            # Configure Gemini
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({
                        'error': 'GEMINI_API_KEY environment variable not set',
                        'status': 'error'
                    })
                }
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            responses = []
            for i, question in enumerate(questions):
                try:
                    system_prompt = f"""You are NyayMitra AI, a helpful legal assistant. This is question {i+1} of {len(questions)} in a batch.
Provide a concise but helpful answer to: {question}"""
                    
                    response = model.generate_content(system_prompt)
                    responses.append(response.text)
                except Exception as e:
                    responses.append(f"Error processing question {i+1}: {str(e)}")
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'responses': responses,
                    'session_id': session_id or 'default',
                    'question_count': len(questions),
                    'status': 'success'
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    'error': str(e),
                    'status': 'error'
                })
            }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed', 'status': 'error'})
    }

def handle_chat_history(request, headers):
    """Handle chat history retrieval."""
    if request.method == 'GET':
        try:
            # For now, return empty history (can be enhanced with actual storage)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'history': [],
                    'session_id': 'default',
                    'message_count': 0,
                    'status': 'success'
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    'error': str(e),
                    'status': 'error'
                })
            }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed', 'status': 'error'})
    }

def handle_chat_clear(request, headers):
    """Handle chat session clearing."""
    if request.method == 'POST':
        try:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'success',
                    'session_id': 'default',
                    'cleared': True,
                    'message': 'Session cleared successfully'
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    'error': str(e),
                    'status': 'error'
                })
            }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed', 'status': 'error'})
    }

def handle_chat_transcribe(request, headers):
    """Handle audio transcription."""
    if request.method == 'POST':
        try:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'transcription': 'Audio transcription feature coming soon',
                    'confidence': 0.0,
                    'status': 'success'
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    'error': str(e),
                    'status': 'error'
                })
            }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed', 'status': 'error'})
    }

def handle_chat_voice(request, headers):
    """Handle voice synthesis."""
    if request.method == 'POST':
        try:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'audio_url': None,
                    'message': 'Voice synthesis feature coming soon',
                    'status': 'success'
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    'error': str(e),
                    'status': 'error'
                })
            }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed', 'status': 'error'})
    }