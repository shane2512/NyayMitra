import json
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight, parse_request_body
from agents.conversation_agent import ConversationAgent

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function for batch chat processing.
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
        
        questions = data.get('questions', [])
        session_id = data.get('session_id')
        contract_context = data.get('contract_context')
        
        if not questions:
            return create_error_response("No questions provided", 400)
        
        if not isinstance(questions, list):
            return create_error_response("Questions must be provided as a list", 400)
        
        # Initialize conversation agent
        conversation_agent = ConversationAgent()
        
        # Process batch
        result = conversation_agent.process_batch(questions, session_id, contract_context)
        
        return create_response(result)
        
    except Exception as e:
        print(f"[Chat Batch API] Error: {e}")
        return create_error_response(f"Batch processing failed: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'POST',
        'headers': {'content-type': 'application/json'},
        'body': json.dumps({
            'questions': [
                'What are the payment terms?',
                'What are the termination clauses?',
                'Are there any liability limitations?'
            ],
            'session_id': 'test_batch_session'
        }),
        'isBase64Encoded': False
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
