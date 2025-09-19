import json
import os
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight
from agents.rate_limiter import rate_limiter
from config import Config

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function to reset rate limit statistics (debug only).
    """
    try:
        # Handle CORS preflight
        cors_response = handle_cors_preflight(event)
        if cors_response:
            return cors_response
        
        # Check if this is a POST request
        if event.get('httpMethod') != 'POST':
            return create_error_response("Method not allowed", 405)
        
        # Only allow in debug mode or development environment
        if not Config.DEBUG and os.getenv('VERCEL_ENV') == 'production':
            return create_error_response("Rate limit reset only available in debug mode", 403)
        
        # Reset rate limit statistics
        rate_limiter.reset_statistics()
        
        result = {
            "status": "success",
            "message": "Rate limit statistics reset successfully",
            "debug_mode": Config.DEBUG,
            "environment": os.getenv('VERCEL_ENV', 'development')
        }
        
        return create_response(result)
        
    except Exception as e:
        print(f"[Rate Limit Reset API] Error: {e}")
        return create_error_response(f"Failed to reset rate limits: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'POST'
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
