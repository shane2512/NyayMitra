import json
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight
from config import Config

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function for testing API connectivity.
    """
    try:
        # Handle CORS preflight
        cors_response = handle_cors_preflight(event)
        if cors_response:
            return cors_response
        
        # Check if this is a GET request
        if event.get('httpMethod') != 'GET':
            return create_error_response("Method not allowed", 405)
        
        # Test configuration and connectivity
        test_data = {
            "message": "NyayMitra Serverless API Test Endpoint",
            "status": "success",
            "timestamp": "2025-09-19T21:38:21+05:30",
            "config": {
                "model": Config.GEMINI_MODEL,
                "api_key_present": bool(Config.GEMINI_API_KEY),
                "api_key_length": len(Config.GEMINI_API_KEY) if Config.GEMINI_API_KEY else 0,
                "eleven_api_configured": bool(Config.ELEVEN_API_KEY),
                "rate_limit_config": {
                    "max_requests_per_minute": Config.MAX_REQUESTS_PER_MINUTE,
                    "sleep_between_requests": Config.SLEEP_BETWEEN_REQUESTS,
                    "circuit_breaker_failures": Config.CIRCUIT_BREAKER_FAILURES
                }
            },
            "serverless_info": {
                "temp_dir": Config.TEMP_DIR,
                "max_file_size": Config.MAX_FILE_SIZE,
                "allowed_extensions": list(Config.ALLOWED_EXTENSIONS)
            }
        }
        
        # Test Gemini API connection (basic check)
        try:
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            test_data["gemini_connection"] = "configured"
        except Exception as e:
            test_data["gemini_connection"] = f"error: {str(e)}"
            test_data["status"] = "partial"
        
        return create_response(test_data)
        
    except Exception as e:
        print(f"[Test API] Error: {e}")
        return create_error_response(f"Test endpoint failed: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'GET'
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
