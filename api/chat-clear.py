import json
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight, parse_request_body
from agents.conversation_agent import ConversationAgent

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function to clear chat session.
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
        session_id = data.get('session_id')
        
        if not session_id:
            return create_error_response("Session ID is required", 400)
        
        # Initialize conversation agent
        conversation_agent = ConversationAgent()
        
        # Clear session
        success = conversation_agent.clear_session(session_id)
        
        if success:
            result = {
                "status": "success",
                "message": "Session cleared successfully",
                "session_id": session_id
            }
        else:
            result = {
                "status": "warning",
                "message": "Session not found or already cleared",
                "session_id": session_id
            }
        
        return create_response(result)
        
    except Exception as e:
        print(f"[Chat Clear API] Error: {e}")
        return create_error_response(f"Failed to clear session: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'POST',
        'headers': {'content-type': 'application/json'},
        'body': json.dumps({
            'session_id': 'test_session'
        }),
        'isBase64Encoded': False
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
