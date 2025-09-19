import time
import threading
from typing import Dict, Any, Callable, Optional
from datetime import datetime, timedelta
import random
from config import Config

class ServerlessRateLimiter:
    """
    Serverless-compatible rate limiter with circuit breaker pattern.
    Uses in-memory storage suitable for serverless functions.
    """
    
    def __init__(self):
        self.minute_requests = []
        self.daily_requests = []
        self.circuit_breaker_open = False
        self.circuit_breaker_open_time = None
        self.consecutive_failures = 0
        self.lock = threading.Lock()
        
        # Configuration from environment
        self.max_requests_per_minute = Config.MAX_REQUESTS_PER_MINUTE
        self.max_requests_per_day = 1200  # Conservative daily limit
        self.circuit_breaker_failures = Config.CIRCUIT_BREAKER_FAILURES
        self.circuit_breaker_timeout = Config.CIRCUIT_BREAKER_TIMEOUT
        self.sleep_between_requests = Config.SLEEP_BETWEEN_REQUESTS
    
    def _cleanup_old_requests(self):
        """Remove old request timestamps."""
        now = time.time()
        
        # Clean minute requests (older than 60 seconds)
        self.minute_requests = [req_time for req_time in self.minute_requests 
                               if now - req_time < 60]
        
        # Clean daily requests (older than 24 hours)
        self.daily_requests = [req_time for req_time in self.daily_requests 
                              if now - req_time < 86400]
    
    def _check_circuit_breaker(self) -> bool:
        """Check if circuit breaker should be closed."""
        if not self.circuit_breaker_open:
            return False
        
        if (time.time() - self.circuit_breaker_open_time) > self.circuit_breaker_timeout:
            self.circuit_breaker_open = False
            self.circuit_breaker_open_time = None
            self.consecutive_failures = 0
            return False
        
        return True
    
    def _wait_for_rate_limit(self):
        """Wait if we're approaching rate limits."""
        with self.lock:
            self._cleanup_old_requests()
            
            # Check if we need to wait for minute limit
            if len(self.minute_requests) >= self.max_requests_per_minute - 1:
                oldest_request = min(self.minute_requests)
                wait_time = 60 - (time.time() - oldest_request) + 1
                if wait_time > 0:
                    time.sleep(wait_time)
                    self._cleanup_old_requests()
            
            # Check daily limit
            if len(self.daily_requests) >= self.max_requests_per_day - 1:
                raise Exception("Daily rate limit exceeded")
    
    def execute_with_rate_limit(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with rate limiting and circuit breaker."""
        
        # Check circuit breaker
        if self._check_circuit_breaker():
            raise Exception("Circuit breaker is open - too many failures")
        
        # Wait for rate limits
        self._wait_for_rate_limit()
        
        # Add request timestamp
        now = time.time()
        with self.lock:
            self.minute_requests.append(now)
            self.daily_requests.append(now)
        
        # Add sleep between requests
        if self.sleep_between_requests > 0:
            time.sleep(self.sleep_between_requests)
        
        try:
            result = func(*args, **kwargs)
            
            # Reset failure count on success
            with self.lock:
                self.consecutive_failures = 0
            
            return result
            
        except Exception as e:
            with self.lock:
                self.consecutive_failures += 1
                
                # Open circuit breaker if too many failures
                if self.consecutive_failures >= self.circuit_breaker_failures:
                    self.circuit_breaker_open = True
                    self.circuit_breaker_open_time = time.time()
            
            raise e
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current rate limiting statistics."""
        with self.lock:
            self._cleanup_old_requests()
            
            return {
                "current_minute_requests": len(self.minute_requests),
                "current_daily_requests": len(self.daily_requests),
                "minute_limit": self.max_requests_per_minute,
                "daily_limit": self.max_requests_per_day,
                "circuit_breaker_open": self.circuit_breaker_open,
                "consecutive_failures": self.consecutive_failures,
                "remaining_minute_requests": max(0, self.max_requests_per_minute - len(self.minute_requests)),
                "remaining_daily_requests": max(0, self.max_requests_per_day - len(self.daily_requests))
            }
    
    def reset_statistics(self):
        """Reset all statistics (for testing)."""
        with self.lock:
            self.minute_requests = []
            self.daily_requests = []
            self.circuit_breaker_open = False
            self.circuit_breaker_open_time = None
            self.consecutive_failures = 0

# Global rate limiter instance
rate_limiter = ServerlessRateLimiter()
