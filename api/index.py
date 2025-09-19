import json
import time
from typing import Dict, Any
from utils import create_response, handle_cors_preflight

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function for the root endpoint.
    """
    try:
        # Handle CORS preflight
        cors_response = handle_cors_preflight(event)
        if cors_response:
            return cors_response
        
        # Check if this is a GET request
        if event.get('httpMethod') != 'GET':
            return create_response({
                "message": "NyayMitra Serverless API",
                "version": "2.0.0",
                "status": "success"
            })
        
        # Root endpoint response
        result = {
            "message": "NyayMitra Serverless API is running!",
            "version": "2.0.0",
            "architecture": "serverless",
            "timestamp": time.time(),
            "endpoints": [
                "/api/health",
                "/api/test", 
                "/api/analyze",
                "/api/chat",
                "/api/chat-batch",
                "/api/chat-history",
                "/api/chat-clear",
                "/api/chat-transcribe",
                "/api/chat-voice",
                "/api/rate-limit-status",
                "/api/rate-limit-reset",
                "/api/languages",
                "/api/translator-metrics"
            ],
            "features": [
                "Contract Analysis",
                "AI Chat Assistant", 
                "Multi-language Translation",
                "Voice Transcription",
                "Text-to-Speech",
                "Rate Limiting",
                "Risk Analysis"
            ]
        }
        
        return create_response(result)
        
    except Exception as e:
        print(f"[Index API] Error: {e}")
        return create_response({
            "error": f"Root endpoint error: {str(e)}",
            "status": "error"
        }, 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'GET'
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
