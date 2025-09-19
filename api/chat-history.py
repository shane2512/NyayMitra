import json
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight, get_query_params
from agents.conversation_agent import ConversationAgent

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function to get chat history for a session.
    """
    try:
        # Handle CORS preflight
        cors_response = handle_cors_preflight(event)
        if cors_response:
            return cors_response
        
        # Check if this is a GET request
        if event.get('httpMethod') != 'GET':
            return create_error_response("Method not allowed", 405)
        
        # Get query parameters
        query_params = get_query_params(event)
        session_id = query_params.get('session_id')
        
        if not session_id:
            return create_error_response("Session ID is required", 400)
        
        # Initialize conversation agent
        conversation_agent = ConversationAgent()
        
        # Get session history
        history = conversation_agent.get_session_history(session_id)
        
        result = {
            "history": history,
            "session_id": session_id,
            "status": "success"
        }
        
        return create_response(result)
        
    except Exception as e:
        print(f"[Chat History API] Error: {e}")
        return create_error_response(f"Failed to get chat history: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'GET',
        'queryStringParameters': {
            'session_id': 'test_session'
        }
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
