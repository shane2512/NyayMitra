import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # Supported languages for contract analysis
            languages = {
                'en': {
                    'name': 'English',
                    'native_name': 'English',
                    'code': 'en',
                    'supported_features': ['analysis', 'translation', 'tts', 'stt'],
                    'default': True
                },
                'hi': {
                    'name': 'Hindi',
                    'native_name': 'हिन्दी',
                    'code': 'hi',
                    'supported_features': ['analysis', 'translation', 'tts'],
                    'default': False
                },
                'bn': {
                    'name': 'Bengali',
                    'native_name': 'বাংলা',
                    'code': 'bn',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'te': {
                    'name': 'Telugu',
                    'native_name': 'తెలుగు',
                    'code': 'te',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'ta': {
                    'name': 'Tamil',
                    'native_name': 'தமிழ்',
                    'code': 'ta',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'mr': {
                    'name': 'Marathi',
                    'native_name': 'मराठी',
                    'code': 'mr',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'gu': {
                    'name': 'Gujarati',
                    'native_name': 'ગુજરાતી',
                    'code': 'gu',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'kn': {
                    'name': 'Kannada',
                    'native_name': 'ಕನ್ನಡ',
                    'code': 'kn',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'ml': {
                    'name': 'Malayalam',
                    'native_name': 'മലയാളം',
                    'code': 'ml',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'pa': {
                    'name': 'Punjabi',
                    'native_name': 'ਪੰਜਾਬੀ',
                    'code': 'pa',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'or': {
                    'name': 'Odia',
                    'native_name': 'ଓଡ଼ିଆ',
                    'code': 'or',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'as': {
                    'name': 'Assamese',
                    'native_name': 'অসমীয়া',
                    'code': 'as',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'ur': {
                    'name': 'Urdu',
                    'native_name': 'اردو',
                    'code': 'ur',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'es': {
                    'name': 'Spanish',
                    'native_name': 'Español',
                    'code': 'es',
                    'supported_features': ['analysis', 'translation', 'tts'],
                    'default': False
                },
                'fr': {
                    'name': 'French',
                    'native_name': 'Français',
                    'code': 'fr',
                    'supported_features': ['analysis', 'translation', 'tts'],
                    'default': False
                },
                'de': {
                    'name': 'German',
                    'native_name': 'Deutsch',
                    'code': 'de',
                    'supported_features': ['analysis', 'translation', 'tts'],
                    'default': False
                },
                'zh': {
                    'name': 'Chinese (Simplified)',
                    'native_name': '中文 (简体)',
                    'code': 'zh',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'ja': {
                    'name': 'Japanese',
                    'native_name': '日本語',
                    'code': 'ja',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'ko': {
                    'name': 'Korean',
                    'native_name': '한국어',
                    'code': 'ko',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'ar': {
                    'name': 'Arabic',
                    'native_name': 'العربية',
                    'code': 'ar',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'pt': {
                    'name': 'Portuguese',
                    'native_name': 'Português',
                    'code': 'pt',
                    'supported_features': ['analysis', 'translation', 'tts'],
                    'default': False
                },
                'ru': {
                    'name': 'Russian',
                    'native_name': 'Русский',
                    'code': 'ru',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'it': {
                    'name': 'Italian',
                    'native_name': 'Italiano',
                    'code': 'it',
                    'supported_features': ['analysis', 'translation', 'tts'],
                    'default': False
                },
                'nl': {
                    'name': 'Dutch',
                    'native_name': 'Nederlands',
                    'code': 'nl',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'pl': {
                    'name': 'Polish',
                    'native_name': 'Polski',
                    'code': 'pl',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                },
                'sv': {
                    'name': 'Swedish',
                    'native_name': 'Svenska',
                    'code': 'sv',
                    'supported_features': ['analysis', 'translation'],
                    'default': False
                }
            }
            
            response_data = {
                'status': 'success',
                'languages': languages,
                'total_count': len(languages),
                'default_language': 'en',
                'features': {
                    'analysis': 'Contract risk analysis',
                    'translation': 'Multi-language translation',
                    'tts': 'Text-to-speech synthesis',
                    'stt': 'Speech-to-text transcription'
                }
            }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response_data)
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    'error': f'Languages endpoint error: {str(e)}',
                    'status': 'error'
                })
            }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({
            'error': 'Method not allowed',
            'status': 'error'
        })
    }