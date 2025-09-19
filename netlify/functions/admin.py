"""
Admin endpoints for Netlify Functions.
Handles: health, test, rate-limit-status, translator-metrics
"""

import json
import os
import sys
from urllib.parse import parse_qs

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from utils import create_response, handle_cors
from agents.rate_limiter import ServerlessRateLimiter

# Initialize components
rate_limiter = ServerlessRateLimiter()

def main(event, context):
    """
    Netlify function handler for admin functionality.
    """
    try:
        # Handle CORS
        if event.get('httpMethod') == 'OPTIONS':
            return handle_cors()
        
        # Route based on query parameter
        action = event.get('queryStringParameters', {}).get('action', 'health')
        
        if action == 'rate-limit-status':
            return handle_rate_limit_status(event, context)
        elif action == 'rate-limit-reset':
            return handle_rate_limit_reset(event, context)
        elif action == 'translator-metrics':
            return handle_translator_metrics(event, context)
        elif action == 'test':
            return handle_test(event, context)
        else:
            return handle_health(event, context)
            
    except Exception as e:
        return create_response({
            'error': f'Admin handler error: {str(e)}',
            'type': 'server_error'
        }, 500)

def handle_rate_limit_status(event, context):
    """Handle rate limit status check."""
    try:
        status = rate_limiter.get_status()
        
        # Add warnings if approaching limits
        warnings = []
        if status['current_minute_requests'] >= status['minute_limit'] * 0.8:
            warnings.append('Approaching per-minute rate limit')
        if status['current_daily_requests'] >= status['daily_limit'] * 0.9:
            warnings.append('Approaching daily rate limit')
        
        return create_response({
            **status,
            'warnings': warnings,
            'status': 'healthy' if not status['circuit_breaker_open'] else 'degraded'
        })
        
    except Exception as e:
        return create_response({
            'error': f'Failed to get rate limit status: {str(e)}',
            'type': 'status_error'
        }, 500)

def handle_rate_limit_reset(event, context):
    """Handle rate limit reset (debug only)."""
    try:
        # Only allow in development/debug mode
        if Config.DEBUG:
            rate_limiter.reset_limits()
            return create_response({
                'status': 'success',
                'message': 'Rate limits reset successfully',
                'timestamp': rate_limiter.get_current_time()
            })
        else:
            return create_response({
                'error': 'Rate limit reset not allowed in production',
                'type': 'permission_denied'
            }, 403)
            
    except Exception as e:
        return create_response({
            'error': f'Failed to reset rate limits: {str(e)}',
            'type': 'reset_error'
        }, 500)

def handle_translator_metrics(event, context):
    """Handle translator metrics retrieval."""
    try:
        metrics = {
            'service_status': 'active',
            'supported_languages': 12,
            'available_languages': {
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
            'interest_areas': [
                'financial_obligations',
                'termination_clauses',
                'liability_limitations',
                'intellectual_property',
                'confidentiality',
                'dispute_resolution',
                'compliance_requirements',
                'payment_terms',
                'delivery_schedules',
                'warranty_provisions',
                'indemnification',
                'force_majeure'
            ],
            'rate_limiting': {
                'requests_per_minute': 8,
                'daily_limit': 1200,
                'circuit_breaker_enabled': True
            }
        }
        
        return create_response(metrics)
        
    except Exception as e:
        return create_response({
            'error': f'Failed to get translator metrics: {str(e)}',
            'type': 'metrics_error'
        }, 500)

def handle_health(event, context):
    """Handle health check."""
    try:
        # Check system components
        health_status = {
            'status': 'healthy',
            'timestamp': rate_limiter.get_current_time(),
            'version': '2.0.0-netlify',
            'environment': 'production' if not Config.DEBUG else 'development',
            'components': {
                'rate_limiter': 'healthy',
                'translator': 'healthy',
                'gemini_api': 'configured' if Config.GEMINI_API_KEY else 'not_configured',
                'elevenlabs_api': 'configured' if Config.ELEVEN_API_KEY else 'not_configured'
            },
            'configuration': {
                'model': Config.GEMINI_MODEL,
                'max_requests_per_minute': Config.MAX_REQUESTS_PER_MINUTE,
                'circuit_breaker_enabled': True
            }
        }
        
        # Determine overall health
        if not Config.GEMINI_API_KEY:
            health_status['status'] = 'degraded'
            health_status['issues'] = ['Gemini API key not configured']
        
        return create_response(health_status)
        
    except Exception as e:
        return create_response({
            'status': 'unhealthy',
            'error': f'Health check failed: {str(e)}',
            'timestamp': rate_limiter.get_current_time()
        }, 500)

def handle_test(event, context):
    """Handle configuration test."""
    try:
        test_results = {
            'status': 'success',
            'timestamp': rate_limiter.get_current_time(),
            'config': {
                'gemini_model': Config.GEMINI_MODEL,
                'api_key_present': bool(Config.GEMINI_API_KEY),
                'api_key_length': len(Config.GEMINI_API_KEY) if Config.GEMINI_API_KEY else 0,
                'elevenlabs_configured': bool(Config.ELEVEN_API_KEY),
                'voice_id_configured': bool(Config.VOICE_ID),
                'debug_mode': Config.DEBUG
            },
            'rate_limiting': {
                'max_requests_per_minute': Config.MAX_REQUESTS_PER_MINUTE,
                'sleep_between_requests': Config.SLEEP_BETWEEN_REQUESTS,
                'circuit_breaker_failures': Config.CIRCUIT_BREAKER_FAILURES,
                'circuit_breaker_timeout': Config.CIRCUIT_BREAKER_TIMEOUT
            },
            'netlify_functions': [
                'analyze',
                'chat',
                'admin', 
                'languages'
            ]
        }
        
        # Add warnings for missing configuration
        warnings = []
        if not Config.GEMINI_API_KEY:
            warnings.append('Gemini API key not configured')
        if not Config.ELEVEN_API_KEY:
            warnings.append('ElevenLabs API key not configured (voice features disabled)')
        
        if warnings:
            test_results['warnings'] = warnings
        
        return create_response(test_results)
        
    except Exception as e:
        return create_response({
            'status': 'failed',
            'error': f'Configuration test failed: {str(e)}',
            'timestamp': rate_limiter.get_current_time()
        }, 500)

# Netlify Functions entry point
handler = main
