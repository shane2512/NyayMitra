import json
import os
import tempfile
from typing import Dict, Any, Optional
from werkzeug.utils import secure_filename
from config import Config

def create_response(data: Dict[str, Any], status_code: int = 200) -> tuple:
    """Create a standardized API response."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps(data)
    }

def create_error_response(error: str, status_code: int = 500) -> tuple:
    """Create a standardized error response."""
    return create_response({
        "error": error,
        "status": "error"
    }, status_code)

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_uploaded_file(file_content: bytes, filename: str) -> str:
    """Save uploaded file to temporary directory and return path."""
    if not allowed_file(filename):
        raise ValueError("File type not allowed")
    
    secure_name = secure_filename(filename)
    temp_path = os.path.join(Config.TEMP_DIR, secure_name)
    
    with open(temp_path, 'wb') as f:
        f.write(file_content)
    
    return temp_path

def cleanup_temp_file(file_path: str) -> None:
    """Clean up temporary file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass  # Ignore cleanup errors

def parse_request_body(event: Dict[str, Any]) -> Dict[str, Any]:
    """Parse request body from Vercel event."""
    try:
        if event.get('body'):
            if event.get('isBase64Encoded'):
                import base64
                body = base64.b64decode(event['body']).decode('utf-8')
            else:
                body = event['body']
            return json.loads(body)
        return {}
    except (json.JSONDecodeError, ValueError):
        return {}

def get_query_params(event: Dict[str, Any]) -> Dict[str, str]:
    """Get query parameters from Vercel event."""
    return event.get('queryStringParameters') or {}

def handle_cors_preflight(event: Dict[str, Any]) -> Optional[tuple]:
    """Handle CORS preflight requests."""
    if event.get('httpMethod') == 'OPTIONS':
        return create_response({}, 200)
    return None
