import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class RateLimitEvent:
    """Represents a rate limit event for analysis"""
    timestamp: float
    error_message: str
    retry_after: Optional[int] = None
    quota_type: Optional[str] = None

class IntelligentRateLimitRecovery:
    """
    Intelligent system for detecting rate limit patterns and implementing
    adaptive recovery strategies
    """
    
    def __init__(self):
        self.rate_limit_events: List[RateLimitEvent] = []
        self.lock = threading.Lock()
        self.adaptive_delay = 5.0  # Start with 5 second delay
        self.max_adaptive_delay = 300.0  # Max 5 minutes
        self.min_adaptive_delay = 2.0  # Min 2 seconds
        self.consecutive_successes = 0
        self.consecutive_failures = 0
        self.last_success_time = 0
        self.quota_reset_times = {}  # Track different quota reset times
        
    def record_rate_limit(self, error_message: str, retry_after: Optional[int] = None):
        """Record a rate limit event for pattern analysis"""
        with self.lock:
            event = RateLimitEvent(
                timestamp=time.time(),
                error_message=error_message,
                retry_after=retry_after,
                quota_type=self._detect_quota_type(error_message)
            )
            self.rate_limit_events.append(event)
            self.consecutive_failures += 1
            self.consecutive_successes = 0
            
            # Keep only last 100 events
            if len(self.rate_limit_events) > 100:
                self.rate_limit_events = self.rate_limit_events[-100:]
            
            # Increase adaptive delay
            self._increase_adaptive_delay()
            
            print(f"[RateRecovery] Rate limit recorded. New adaptive delay: {self.adaptive_delay:.1f}s")
    
    def record_success(self):
        """Record a successful API call"""
        with self.lock:
            self.consecutive_successes += 1
            self.consecutive_failures = 0
            self.last_success_time = time.time()
            
            # Gradually decrease delay after sustained success
            if self.consecutive_successes >= 3:
                self._decrease_adaptive_delay()
    
    def _detect_quota_type(self, error_message: str) -> Optional[str]:
        """Detect the type of quota limit from error message"""
        error_lower = error_message.lower()
        
        if "requests per minute" in error_lower or "rpm" in error_lower:
            return "requests_per_minute"
        elif "requests per day" in error_lower or "rpd" in error_lower:
            return "requests_per_day"
        elif "tokens per minute" in error_lower or "tpm" in error_lower:
            return "tokens_per_minute"
        elif "concurrent requests" in error_lower:
            return "concurrent_requests"
        else:
            return "unknown"
    
    def _increase_adaptive_delay(self):
        """Increase the adaptive delay based on failure patterns"""
        # Exponential backoff with jitter
        multiplier = 1.5 + (self.consecutive_failures * 0.2)
        self.adaptive_delay = min(
            self.adaptive_delay * multiplier,
            self.max_adaptive_delay
        )
    
    def _decrease_adaptive_delay(self):
        """Gradually decrease delay after sustained success"""
        if self.adaptive_delay > self.min_adaptive_delay:
            self.adaptive_delay = max(
                self.adaptive_delay * 0.9,  # Gradual decrease
                self.min_adaptive_delay
            )
            print(f"[RateRecovery] Reducing adaptive delay to {self.adaptive_delay:.1f}s after sustained success")
    
    def get_recommended_delay(self) -> float:
        """Get the current recommended delay between requests"""
        with self.lock:
            # If we have recent rate limits, use adaptive delay
            recent_events = [
                e for e in self.rate_limit_events 
                if time.time() - e.timestamp < 300  # Last 5 minutes
            ]
            
            if recent_events:
                # Check if we have retry-after information
                latest_event = recent_events[-1]
                if latest_event.retry_after:
                    return max(latest_event.retry_after, self.adaptive_delay)
                
                return self.adaptive_delay
            
            # No recent rate limits, use minimum delay
            return self.min_adaptive_delay
    
    def should_pause_requests(self) -> tuple[bool, float]:
        """Check if we should completely pause requests and for how long"""
        with self.lock:
            now = time.time()
            
            # Check for rapid consecutive failures
            if self.consecutive_failures >= 5:
                pause_time = min(60 * (2 ** (self.consecutive_failures - 5)), 900)  # Max 15 minutes
                return True, pause_time
            
            # Check for high frequency of rate limits
            recent_events = [
                e for e in self.rate_limit_events 
                if now - e.timestamp < 60  # Last minute
            ]
            
            if len(recent_events) >= 3:
                return True, 120  # Pause for 2 minutes
            
            return False, 0
    
    def get_rate_limit_analysis(self) -> Dict:
        """Get analysis of rate limiting patterns"""
        with self.lock:
            now = time.time()
            
            # Events in different time windows
            events_1min = [e for e in self.rate_limit_events if now - e.timestamp < 60]
            events_5min = [e for e in self.rate_limit_events if now - e.timestamp < 300]
            events_1hour = [e for e in self.rate_limit_events if now - e.timestamp < 3600]
            
            # Quota type distribution
            quota_types = {}
            for event in events_1hour:
                quota_type = event.quota_type or "unknown"
                quota_types[quota_type] = quota_types.get(quota_type, 0) + 1
            
            # Time since last success
            time_since_success = now - self.last_success_time if self.last_success_time else float('inf')
            
            return {
                "current_adaptive_delay": self.adaptive_delay,
                "consecutive_failures": self.consecutive_failures,
                "consecutive_successes": self.consecutive_successes,
                "events_last_minute": len(events_1min),
                "events_last_5minutes": len(events_5min),
                "events_last_hour": len(events_1hour),
                "quota_type_distribution": quota_types,
                "time_since_last_success": time_since_success,
                "recommended_action": self._get_recommended_action(),
                "should_pause": self.should_pause_requests()[0]
            }
    
    def _get_recommended_action(self) -> str:
        """Get recommended action based on current state"""
        if self.consecutive_failures >= 10:
            return "CRITICAL: Stop all requests for 15+ minutes, check API key and quotas"
        elif self.consecutive_failures >= 5:
            return "HIGH: Implement long pauses between requests (5+ minutes)"
        elif self.consecutive_failures >= 3:
            return "MEDIUM: Increase delays and reduce request frequency"
        elif self.adaptive_delay > 30:
            return "LOW: Current rate limiting is working, maintain current settings"
        else:
            return "GOOD: API usage is stable"
    
    def export_analysis_report(self) -> str:
        """Export a detailed analysis report"""
        analysis = self.get_rate_limit_analysis()
        
        report = f"""
# Rate Limit Recovery Analysis
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Current Status
- Adaptive Delay: {analysis['current_adaptive_delay']:.1f} seconds
- Consecutive Failures: {analysis['consecutive_failures']}
- Consecutive Successes: {analysis['consecutive_successes']}
- Should Pause Requests: {analysis['should_pause']}

## Recent Rate Limit Events
- Last Minute: {analysis['events_last_minute']} events
- Last 5 Minutes: {analysis['events_last_5minutes']} events  
- Last Hour: {analysis['events_last_hour']} events

## Quota Type Distribution
"""
        
        for quota_type, count in analysis['quota_type_distribution'].items():
            report += f"- {quota_type}: {count} events\n"
        
        report += f"""
## Recommendation
{analysis['recommended_action']}

## Time Since Last Success
{analysis['time_since_last_success']:.1f} seconds

"""
        return report

# Global recovery system instance
rate_limit_recovery = IntelligentRateLimitRecovery()
