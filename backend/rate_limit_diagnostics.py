#!/usr/bin/env python3
"""
Rate Limit Diagnostic Tool
Helps diagnose and monitor API rate limiting issues in NyayMitra
"""

import sys
import os
import time
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agents.usage_monitor import usage_monitor
from agents.rate_limit_recovery import rate_limit_recovery
from agents.api_optimizer import GeminiAPIOptimizer, _global_rate_queue
from config import Config

def print_separator(title=""):
    print("\n" + "="*60)
    if title:
        print(f" {title}")
        print("="*60)

def check_configuration():
    """Check current configuration settings"""
    print_separator("CONFIGURATION CHECK")
    
    print("Current Rate Limiting Settings:")
    print(f"  SLEEP_BETWEEN_REQUESTS: {Config.SLEEP_BETWEEN_REQUESTS}s")
    print(f"  MAX_REQUESTS_PER_MINUTE: {Config.MAX_REQUESTS_PER_MINUTE}")
    print(f"  CIRCUIT_BREAKER_FAILURES: {Config.CIRCUIT_BREAKER_FAILURES}")
    print(f"  CIRCUIT_BREAKER_TIMEOUT: {Config.CIRCUIT_BREAKER_TIMEOUT}s")
    
    if hasattr(Config, 'MIN_DELAY_BETWEEN_REQUESTS'):
        print(f"  MIN_DELAY_BETWEEN_REQUESTS: {Config.MIN_DELAY_BETWEEN_REQUESTS}s")
    if hasattr(Config, 'MAX_RETRIES'):
        print(f"  MAX_RETRIES: {Config.MAX_RETRIES}")
    
    print(f"\nAPI Configuration:")
    print(f"  GEMINI_MODEL: {Config.GEMINI_MODEL}")
    print(f"  API Key Set: {'Yes' if Config.GEMINI_API_KEY != 'your_default_api_key_here' else 'No'}")

def check_usage_statistics():
    """Check current usage statistics"""
    print_separator("USAGE STATISTICS")
    
    current_usage = usage_monitor.get_current_usage()
    
    print("Current API Usage:")
    print(f"  Requests per minute: {current_usage['requests_per_minute']}")
    print(f"  Requests per hour: {current_usage['requests_per_hour']}")
    print(f"  Requests today: {current_usage['requests_today']}")
    print(f"  Tokens last hour: {current_usage['tokens_last_hour']:,}")
    print(f"  Rate limit hits: {current_usage['rate_limit_hits']}")
    print(f"  Total requests: {current_usage['total_requests']}")
    print(f"  Optimization score: {current_usage['optimization_score']:.1f}/100")
    
    print("\nRecommendations:")
    for rec in usage_monitor.get_recommendations():
        print(f"  • {rec}")

def check_rate_limit_recovery():
    """Check intelligent rate limit recovery status"""
    print_separator("RATE LIMIT RECOVERY STATUS")
    
    analysis = rate_limit_recovery.get_rate_limit_analysis()
    
    print("Recovery System Status:")
    print(f"  Current adaptive delay: {analysis['current_adaptive_delay']:.1f}s")
    print(f"  Consecutive failures: {analysis['consecutive_failures']}")
    print(f"  Consecutive successes: {analysis['consecutive_successes']}")
    print(f"  Should pause requests: {analysis['should_pause']}")
    
    print(f"\nRecent Rate Limit Events:")
    print(f"  Last minute: {analysis['events_last_minute']}")
    print(f"  Last 5 minutes: {analysis['events_last_5minutes']}")
    print(f"  Last hour: {analysis['events_last_hour']}")
    
    if analysis['quota_type_distribution']:
        print(f"\nQuota Type Distribution:")
        for quota_type, count in analysis['quota_type_distribution'].items():
            print(f"  {quota_type}: {count} events")
    
    print(f"\nRecommended Action:")
    print(f"  {analysis['recommended_action']}")

def test_api_connection(test_simple=True):
    """Test API connection with simple request"""
    print_separator("API CONNECTION TEST")
    
    if Config.GEMINI_API_KEY == "your_default_api_key_here":
        print("❌ ERROR: API key not configured!")
        print("Please set GEMINI_API_KEY in your environment variables.")
        return False
    
    if not test_simple:
        print("Skipping API test (test_simple=False)")
        return True
    
    try:
        print("Testing API connection with simple request...")
        optimizer = GeminiAPIOptimizer(Config.GEMINI_API_KEY, Config.GEMINI_MODEL)
        
        # Simple test prompt
        test_prompt = "Say 'API connection successful' if you can see this message."
        
        start_time = time.time()
        response = optimizer.optimized_generate_content(test_prompt)
        elapsed = time.time() - start_time
        
        print(f"✅ API Test Successful!")
        print(f"   Response time: {elapsed:.1f}s")
        print(f"   Response length: {len(response)} characters")
        print(f"   Response preview: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        
        # Analyze the error
        error_str = str(e).lower()
        if "api key" in error_str or "authentication" in error_str:
            print("   Issue: API key authentication failed")
            print("   Solution: Check your API key is valid and active")
        elif "429" in error_str or "rate limit" in error_str:
            print("   Issue: Rate limiting detected")
            print("   Solution: Wait before retrying, or check quota limits")
        elif "quota" in error_str:
            print("   Issue: API quota exceeded")
            print("   Solution: Check your quota usage in Google Cloud Console")
        else:
            print(f"   Issue: Unknown error - {e}")
        
        return False

def run_diagnostics(test_api=True):
    """Run complete diagnostic suite"""
    print("NyayMitra Rate Limit Diagnostic Tool")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all checks
    check_configuration()
    check_usage_statistics()
    check_rate_limit_recovery()
    
    if test_api:
        api_success = test_api_connection()
    else:
        api_success = True
        print_separator("API CONNECTION TEST")
        print("Skipped API test (test_api=False)")
    
    # Summary
    print_separator("DIAGNOSTIC SUMMARY")
    
    if api_success:
        print("✅ System appears to be working correctly")
        print("\nNext steps if you're still experiencing rate limits:")
        print("  1. Monitor the system for a few minutes")
        print("  2. Check if rate limits occur during high usage")
        print("  3. Consider increasing delays further if needed")
        print("  4. Verify your API quota limits in Google Cloud Console")
    else:
        print("❌ Issues detected - resolve API connectivity first")
    
    print(f"\nFor detailed analysis, run:")
    print(f"  python -c \"from backend.agents.rate_limit_recovery import rate_limit_recovery; print(rate_limit_recovery.export_analysis_report())\"")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="NyayMitra Rate Limit Diagnostics")
    parser.add_argument("--no-api-test", action="store_true", 
                       help="Skip API connection test")
    
    args = parser.parse_args()
    
    run_diagnostics(test_api=not args.no_api_test)
