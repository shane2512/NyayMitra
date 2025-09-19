"""
Languages endpoint for Netlify Functions.
Returns supported languages for translation.
"""

import json
import os
import sys

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from utils import create_response, handle_cors

def main(event, context):
    """
    Netlify function handler for supported languages.
    """
    try:
        # Handle CORS preflight requests
        if event.get('httpMethod') == 'OPTIONS':
            return handle_cors()
        
        languages = {
            'supported_languages': {
                'en': 'English',
                'hi': 'Hindi',
                'es': 'Spanish', 
                'fr': 'French',
                'de': 'German',
                'zh': 'Chinese',
                'ja': 'Japanese',
                'ko': 'Korean',
                'ar': 'Arabic',
                'pt': 'Portuguese',
                'ru': 'Russian',
                'it': 'Italian'
            },
            'default_language': 'en',
            'total_languages': 12
        }
        
        return create_response(languages)
        
    except Exception as e:
        return create_response({
            'error': f'Languages handler error: {str(e)}',
            'type': 'server_error'
        }, 500)

# Netlify Functions entry point
handler = main
