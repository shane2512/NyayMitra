import json
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight
from agents.translator import TranslatorAgent

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function to get supported languages for translation.
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
        
        # Get supported languages and interest areas
        result = {
            "supported_languages": translator.get_supported_languages(),
            "interest_areas": translator.interest_areas,
            "total_languages": len(translator.supported_languages),
            "status": "success"
        }
        
        return create_response(result)
        
    except Exception as e:
        print(f"[Languages API] Error: {e}")
        return create_error_response(f"Failed to get languages: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'GET'
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
