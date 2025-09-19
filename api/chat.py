import json
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight, parse_request_body
from agents.conversation_agent import ConversationAgent

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function for single chat messages.
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
        
        # Process message
        result = conversation_agent.process_message(message, session_id, contract_context)
        
        return create_response(result)
        
    except Exception as e:
        print(f"[Chat API] Error: {e}")
        return create_error_response(f"Chat processing failed: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'POST',
        'headers': {'content-type': 'application/json'},
        'body': json.dumps({
            'message': 'What are the key terms in this contract?',
            'session_id': 'test_session'
        }),
        'isBase64Encoded': False
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
