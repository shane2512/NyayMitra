import time
import random
import threading
from typing import Dict, Optional, Callable, Any
from functools import wraps
from datetime import datetime, timedelta

class RateLimiter:
    """
    Advanced rate limiter with circuit breaker, exponential backoff, and request batching.
    Implements multiple strategies to handle rate limits effectively.
    """
    
    def __init__(self):
        self.lock = threading.Lock()
        
        # Rate limit tracking
        self.request_times = []
        self.minute_requests = []
        self.daily_requests = []
        
        # Limits
        self.max_requests_per_minute = 50  # Conservative limit (actual is 60)
        self.max_requests_per_day = 1200  # Conservative limit (actual is 1500)
        
        # Circuit breaker
        self.circuit_breaker_failures = 0
        self.circuit_breaker_threshold = 5
        self.circuit_breaker_reset_time = None
        self.circuit_breaker_timeout = 60  # 1 minute timeout
        
        # Backoff settings
        self.base_delay = 2.0  # Base delay in seconds
        self.max_delay = 60.0  # Maximum delay in seconds
        self.jitter_range = 0.5  # Jitter range for randomization
        
        # Statistics
        self.total_requests = 0
        self.rate_limited_count = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
    def _clean_request_history(self):
        """Clean up old request timestamps"""
        now = time.time()
        current_date = datetime.now().date()
        
        # Clean minute window (keep last 60 seconds)
        self.minute_requests = [t for t in self.minute_requests if now - t < 60]
        
        # Clean daily window (keep today's requests)
        self.daily_requests = [t for t in self.daily_requests 
                               if datetime.fromtimestamp(t).date() == current_date]
    
    def _is_circuit_open(self) -> bool:
        """Check if circuit breaker is open"""
        if self.circuit_breaker_failures >= self.circuit_breaker_threshold:
            if self.circuit_breaker_reset_time:
                if time.time() < self.circuit_breaker_reset_time:
                    return True
                else:
                    # Reset circuit breaker
                    self.circuit_breaker_failures = 0
                    self.circuit_breaker_reset_time = None
                    print("[RateLimiter] Circuit breaker reset")
            else:
                # Open circuit breaker
                self.circuit_breaker_reset_time = time.time() + self.circuit_breaker_timeout
                print(f"[RateLimiter] Circuit breaker opened for {self.circuit_breaker_timeout}s")
                return True
        return False
    
    def _calculate_backoff_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter"""
        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
        jitter = random.uniform(-self.jitter_range, self.jitter_range)
        return max(0, delay + jitter)
    
    def _wait_if_needed(self) -> bool:
        """Wait if rate limits are approaching, return True if waited"""
        with self.lock:
            self._clean_request_history()
            
            # Check circuit breaker
            if self._is_circuit_open():
                wait_time = self.circuit_breaker_reset_time - time.time()
                print(f"[RateLimiter] Circuit breaker open, waiting {wait_time:.1f}s")
                time.sleep(wait_time)
                return True
            
            # Check minute limit
            if len(self.minute_requests) >= self.max_requests_per_minute:
                oldest_request = min(self.minute_requests)
                wait_time = 61 - (time.time() - oldest_request)
                if wait_time > 0:
                    print(f"[RateLimiter] Minute limit reached ({len(self.minute_requests)}/{self.max_requests_per_minute}), waiting {wait_time:.1f}s")
                    time.sleep(wait_time)
                    return True
            
            # Check daily limit
            if len(self.daily_requests) >= self.max_requests_per_day:
                print(f"[RateLimiter] Daily limit reached ({len(self.daily_requests)}/{self.max_requests_per_day})")
                # Calculate time until midnight
                now = datetime.now()
                midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                wait_time = (midnight - now).total_seconds()
                print(f"[RateLimiter] Waiting until midnight ({wait_time/3600:.1f} hours)")
                raise Exception("Daily rate limit exceeded. Please try again tomorrow.")
            
            # Add small delay between requests to be conservative
            time.sleep(0.5)
            return False
    
    def record_request(self, success: bool = True):
        """Record a request for rate limiting"""
        with self.lock:
            now = time.time()
            self.minute_requests.append(now)
            self.daily_requests.append(now)
            self.total_requests += 1
            
            if success:
                self.successful_requests += 1
                self.circuit_breaker_failures = 0  # Reset on success
            else:
                self.failed_requests += 1
                self.circuit_breaker_failures += 1
    
    def execute_with_rate_limit(self, func: Callable, max_retries: int = 5) -> Any:
        """Execute function with rate limiting and retry logic"""
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                # Wait if rate limited
                self._wait_if_needed()
                
                # Execute function
                result = func()
                
                # Record successful request
                self.record_request(success=True)
                
                return result
                
            except Exception as e:
                error_str = str(e).lower()
                last_exception = e
                
                # Check if it's a rate limit error
                if any(term in error_str for term in ['429', 'rate limit', 'quota', 'too many']):
                    self.rate_limited_count += 1
                    self.record_request(success=False)
                    
                    if attempt < max_retries - 1:
                        delay = self._calculate_backoff_delay(attempt)
                        print(f"[RateLimiter] Rate limit hit, attempt {attempt + 1}/{max_retries}, waiting {delay:.1f}s")
                        time.sleep(delay)
                        continue
                else:
                    # Not a rate limit error, record failure and raise
                    self.record_request(success=False)
                    raise e
        
        # All retries exhausted
        raise Exception(f"Rate limit exceeded after {max_retries} attempts: {last_exception}")
    
    def get_statistics(self) -> Dict:
        """Get rate limiter statistics"""
        with self.lock:
            self._clean_request_history()
            return {
                "total_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "rate_limited_count": self.rate_limited_count,
                "current_minute_requests": len(self.minute_requests),
                "current_daily_requests": len(self.daily_requests),
                "minute_limit": self.max_requests_per_minute,
                "daily_limit": self.max_requests_per_day,
                "circuit_breaker_failures": self.circuit_breaker_failures,
                "circuit_breaker_open": self._is_circuit_open()
            }
    
    def reset_statistics(self):
        """Reset statistics (for testing)"""
        with self.lock:
            self.total_requests = 0
            self.successful_requests = 0
            self.failed_requests = 0
            self.rate_limited_count = 0
            self.circuit_breaker_failures = 0
            self.circuit_breaker_reset_time = None

# Global rate limiter instance
rate_limiter = RateLimiter()

def with_rate_limit(max_retries: int = 5):
    """Decorator for rate limiting functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return rate_limiter.execute_with_rate_limit(
                lambda: func(*args, **kwargs),
                max_retries=max_retries
            )
        return wrapper
    return decorator
