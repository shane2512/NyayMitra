import json
import os
import base64
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight, save_uploaded_file, cleanup_temp_file
from agents.moderator import ModeratorAgent
from config import Config

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function to analyze contract PDFs.
    """
    try:
        # Handle CORS preflight
        cors_response = handle_cors_preflight(event)
        if cors_response:
            return cors_response
        
        # Check if this is a POST request
        if event.get('httpMethod') != 'POST':
            return create_error_response("Method not allowed", 405)
        
        # Parse multipart form data
        content_type = event.get('headers', {}).get('content-type', '')
        if 'multipart/form-data' not in content_type:
            return create_error_response("Content-Type must be multipart/form-data", 400)
        
        # Get file data from event body
        body = event.get('body', '')
        is_base64 = event.get('isBase64Encoded', False)
        
        if not body:
            return create_error_response("No file data provided", 400)
        
        # Parse multipart data (simplified for serverless)
        try:
            if is_base64:
                file_data = base64.b64decode(body)
            else:
                file_data = body.encode('utf-8')
            
            # For simplicity, assume the entire body is the PDF file
            # In production, you'd want proper multipart parsing
            filename = "uploaded_contract.pdf"
            
            # Save file temporarily
            temp_path = save_uploaded_file(file_data, filename)
            
            # Get additional parameters from query string
            query_params = event.get('queryStringParameters') or {}
            language = query_params.get('language', 'en')
            interests = query_params.get('interests', '').split(',') if query_params.get('interests') else []
            
            # Initialize moderator and analyze
            moderator = ModeratorAgent()
            
            if language != 'en' or interests:
                result = moderator.analyze_contract_with_translation(temp_path, language, interests)
            else:
                result = moderator.analyze_contract(temp_path)
            
            # Clean up temporary file
            cleanup_temp_file(temp_path)
            
            return create_response(result)
            
        except Exception as parse_error:
            return create_error_response(f"Failed to parse file data: {str(parse_error)}", 400)
        
    except Exception as e:
        print(f"[Analyze API] Error: {e}")
        return create_error_response(f"Analysis failed: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    # Test event
    test_event = {
        'httpMethod': 'POST',
        'headers': {'content-type': 'multipart/form-data'},
        'body': '',
        'isBase64Encoded': False
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
