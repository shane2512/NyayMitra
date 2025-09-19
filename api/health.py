import json
import time
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight
from config import Config

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function for health checks.
    """
    try:
        # Handle CORS preflight
        cors_response = handle_cors_preflight(event)
        if cors_response:
            return cors_response
        
        # Check if this is a GET request
        if event.get('httpMethod') != 'GET':
            return create_error_response("Method not allowed", 405)
        
        # Basic health check
        health_data = {
            "status": "healthy",
            "timestamp": time.time(),
            "service": "NyayMitra Serverless API",
            "version": "2.0.0",
            "environment": "serverless",
            "checks": {
                "api_key_configured": bool(Config.GEMINI_API_KEY),
                "model_configured": bool(Config.GEMINI_MODEL),
                "temp_directory": Config.TEMP_DIR
            }
        }
        
        # Check if all critical components are configured
        all_healthy = all(health_data["checks"].values())
        if not all_healthy:
            health_data["status"] = "degraded"
            health_data["warnings"] = []
            
            if not Config.GEMINI_API_KEY:
                health_data["warnings"].append("Gemini API key not configured")
            if not Config.GEMINI_MODEL:
                health_data["warnings"].append("Gemini model not configured")
        
        return create_response(health_data)
        
    except Exception as e:
        print(f"[Health API] Error: {e}")
        return create_error_response(f"Health check failed: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'GET'
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
