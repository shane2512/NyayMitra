import json
from typing import Dict, Any
from utils import create_response, create_error_response, handle_cors_preflight
from agents.rate_limiter import rate_limiter

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Serverless function to get rate limit status.
    """
    try:
        # Handle CORS preflight
        cors_response = handle_cors_preflight(event)
        if cors_response:
            return cors_response
        
        # Check if this is a GET request
        if event.get('httpMethod') != 'GET':
            return create_error_response("Method not allowed", 405)
        
        # Get rate limit statistics
        stats = rate_limiter.get_statistics()
        
        # Add warning levels
        minute_usage_percent = (stats['current_minute_requests'] / stats['minute_limit']) * 100
        daily_usage_percent = (stats['current_daily_requests'] / stats['daily_limit']) * 100
        
        stats['warnings'] = []
        if minute_usage_percent > 80:
            stats['warnings'].append(f"Approaching minute limit: {minute_usage_percent:.0f}% used")
        if daily_usage_percent > 80:
            stats['warnings'].append(f"Approaching daily limit: {daily_usage_percent:.0f}% used")
        if stats['circuit_breaker_open']:
            stats['warnings'].append("Circuit breaker is open - requests are being throttled")
        
        # Add usage percentages
        stats['minute_usage_percent'] = round(minute_usage_percent, 1)
        stats['daily_usage_percent'] = round(daily_usage_percent, 1)
        
        return create_response(stats)
        
    except Exception as e:
        print(f"[Rate Limit Status API] Error: {e}")
        return create_error_response(f"Failed to get rate limit status: {str(e)}", 500)

# For local testing
if __name__ == "__main__":
    test_event = {
        'httpMethod': 'GET'
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
