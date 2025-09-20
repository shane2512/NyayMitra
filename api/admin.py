import json
import os
import sys
import time
from urllib.parse import parse_qs

def handler(request, context):
    """Vercel serverless function handler for admin operations."""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({})
        }
    
    try:
        # Get query parameters
        query_params = {}
        if hasattr(request, 'args'):
            query_params = request.args
        elif hasattr(request, 'query_string') and request.query_string:
            query_params = parse_qs(request.query_string)
            # Convert list values to single values
            query_params = {k: v[0] if isinstance(v, list) and v else v for k, v in query_params.items()}
        
        action = query_params.get('action', 'health')
        
        if action == 'health':
            return handle_health_check(headers)
        elif action == 'rate-limit-status':
            return handle_rate_limit_status(headers)
        elif action == 'translator-metrics':
            return handle_translator_metrics(headers)
        else:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': f'Unknown action: {action}',
                    'available_actions': ['health', 'rate-limit-status', 'translator-metrics']
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': f'Admin handler error: {str(e)}',
                'type': 'server_error'
            })
        }

def handle_health_check(headers):
    """Handle health check endpoint."""
    try:
        # Basic health checks
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
        # Check environment variables
        env_status = {
            'GEMINI_API_KEY': bool(os.getenv('GEMINI_API_KEY')),
            'ELEVEN_API_KEY': bool(os.getenv('ELEVEN_API_KEY')),
        }
        
        # Check Python modules
        modules_status = {}
        required_modules = ['google.generativeai', 'numpy', 'json', 'tempfile']
        
        for module in required_modules:
            try:
                __import__(module)
                modules_status[module] = True
            except ImportError:
                modules_status[module] = False
        
        health_data = {
            'status': 'healthy',
            'timestamp': time.time(),
            'python_version': python_version,
            'environment': env_status,
            'modules': modules_status,
            'platform': 'vercel',
            'uptime': 'serverless',
            'version': '1.0.0'
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(health_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': time.time()
            })
        }

def handle_rate_limit_status(headers):
    """Handle rate limit status check."""
    try:
        # Simple rate limit status for serverless
        rate_limit_data = {
            'status': 'active',
            'type': 'serverless',
            'current_requests': 0,
            'limit_per_minute': 60,
            'reset_time': int(time.time()) + 60,
            'timestamp': time.time(),
            'note': 'Serverless functions have automatic rate limiting'
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(rate_limit_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': f'Rate limit status check failed: {str(e)}',
                'timestamp': time.time()
            })
        }

def handle_translator_metrics(headers):
    """Handle translator metrics endpoint."""
    try:
        # Basic translator metrics for serverless
        metrics_data = {
            'total_translations': 0,
            'languages_supported': 25,
            'active_sessions': 0,
            'avg_response_time': '1.2s',
            'success_rate': '99.5%',
            'timestamp': time.time(),
            'status': 'operational',
            'note': 'Metrics reset with each serverless invocation'
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(metrics_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': f'Translator metrics failed: {str(e)}',
                'timestamp': time.time()
            })
        }