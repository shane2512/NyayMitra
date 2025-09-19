import json
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight
from agents.translator import TranslatorAgent

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function to get translator metrics and statistics.
    """
    try:
        # Handle CORS preflight
        cors_response = handle_cors_preflight(event)
        if cors_response:
            return cors_response
        
        # Check if this is a GET request
        if event.get('httpMethod') != 'GET':
            return create_error_response("Method not allowed", 405)
        
        # Initialize translator agent
        translator = TranslatorAgent()
        
        # Get translation metrics
        metrics = translator.get_translation_metrics()
        
        return create_response(metrics)
        
    except Exception as e:
        print(f"[Translator Metrics API] Error: {e}")
        return create_error_response(f"Failed to get translator metrics: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'GET'
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
