import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading

class APIUsageMonitor:
    """
    Monitors API usage patterns, tracks quotas, and provides insights for optimization.
    """
    
    def __init__(self):
        self.usage_stats = {
            "requests_per_minute": [],
            "requests_per_hour": [],
            "requests_per_day": [],
            "token_usage": [],
            "batch_efficiency": [],
            "rate_limit_hits": 0,
            "total_requests": 0,
            "total_tokens_saved": 0
        }
        self.lock = threading.Lock()
        
    def log_request(self, request_type: str, tokens_used: int, batch_size: int = 1, 
                   tokens_saved: int = 0, rate_limited: bool = False):
        """Log an API request with usage details"""
        with self.lock:
            timestamp = time.time()
            
            request_data = {
                "timestamp": timestamp,
                "type": request_type,
                "tokens_used": tokens_used,
                "batch_size": batch_size,
                "tokens_saved": tokens_saved,
                "rate_limited": rate_limited
            }
            
            # Update counters
            self.usage_stats["total_requests"] += 1
            self.usage_stats["total_tokens_saved"] += tokens_saved
            
            if rate_limited:
                self.usage_stats["rate_limit_hits"] += 1
            
            # Track by time periods
            self.usage_stats["requests_per_minute"].append(request_data)
            self.usage_stats["requests_per_hour"].append(request_data)
            self.usage_stats["requests_per_day"].append(request_data)
            self.usage_stats["token_usage"].append(request_data)
            
            if batch_size > 1:
                efficiency = batch_size / 1  # vs individual requests
                self.usage_stats["batch_efficiency"].append({
                    "timestamp": timestamp,
                    "batch_size": batch_size,
                    "efficiency": efficiency,
                    "tokens_saved": tokens_saved
                })
            
            # Clean old data
            self._cleanup_old_data()
    
    def _cleanup_old_data(self):
        """Remove data older than retention periods"""
        now = time.time()
        
        # Keep only last minute for per-minute tracking
        self.usage_stats["requests_per_minute"] = [
            r for r in self.usage_stats["requests_per_minute"] 
            if now - r["timestamp"] < 60
        ]
        
        # Keep only last hour for per-hour tracking
        self.usage_stats["requests_per_hour"] = [
            r for r in self.usage_stats["requests_per_hour"] 
            if now - r["timestamp"] < 3600
        ]
        
        # Keep only last day for per-day tracking
        self.usage_stats["requests_per_day"] = [
            r for r in self.usage_stats["requests_per_day"] 
            if now - r["timestamp"] < 86400
        ]
    
    def get_current_usage(self) -> Dict:
        """Get current usage statistics"""
        with self.lock:
            now = time.time()
            
            # Count requests in different time windows
            requests_last_minute = len([
                r for r in self.usage_stats["requests_per_minute"]
                if now - r["timestamp"] < 60
            ])
            
            requests_last_hour = len([
                r for r in self.usage_stats["requests_per_hour"]
                if now - r["timestamp"] < 3600
            ])
            
            requests_today = len([
                r for r in self.usage_stats["requests_per_day"]
                if now - r["timestamp"] < 86400
            ])
            
            # Calculate token usage
            tokens_last_hour = sum([
                r["tokens_used"] for r in self.usage_stats["token_usage"]
                if now - r["timestamp"] < 3600
            ])
            
            # Calculate batch efficiency
            avg_batch_efficiency = 0
            if self.usage_stats["batch_efficiency"]:
                recent_batches = [
                    b for b in self.usage_stats["batch_efficiency"]
                    if now - b["timestamp"] < 3600
                ]
                if recent_batches:
                    avg_batch_efficiency = sum(b["efficiency"] for b in recent_batches) / len(recent_batches)
            
            return {
                "requests_per_minute": requests_last_minute,
                "requests_per_hour": requests_last_hour,
                "requests_today": requests_today,
                "tokens_last_hour": tokens_last_hour,
                "rate_limit_hits": self.usage_stats["rate_limit_hits"],
                "total_requests": self.usage_stats["total_requests"],
                "total_tokens_saved": self.usage_stats["total_tokens_saved"],
                "avg_batch_efficiency": avg_batch_efficiency,
                "optimization_score": self._calculate_optimization_score()
            }
    
    def _calculate_optimization_score(self) -> float:
        """Calculate how well we're optimizing API usage (0-100)"""
        score = 100.0
        
        # Penalize rate limit hits
        if self.usage_stats["total_requests"] > 0:
            rate_limit_ratio = self.usage_stats["rate_limit_hits"] / self.usage_stats["total_requests"]
            score -= rate_limit_ratio * 30  # Up to 30 points penalty
        
        # Reward batch processing
        if self.usage_stats["batch_efficiency"]:
            avg_efficiency = sum(b["efficiency"] for b in self.usage_stats["batch_efficiency"]) / len(self.usage_stats["batch_efficiency"])
            score += min(avg_efficiency * 10, 20)  # Up to 20 points bonus
        
        # Reward token savings
        if self.usage_stats["total_tokens_saved"] > 0:
            score += min(self.usage_stats["total_tokens_saved"] / 1000, 10)  # Up to 10 points bonus
        
        return max(0, min(100, score))
    
    def get_recommendations(self) -> List[str]:
        """Get optimization recommendations based on usage patterns"""
        recommendations = []
        current_usage = self.get_current_usage()
        
        # Rate limit recommendations
        if current_usage["rate_limit_hits"] > 0:
            recommendations.append(
                f"⚠️ {current_usage['rate_limit_hits']} rate limit hits detected. "
                "Consider increasing delays between requests or using larger batch sizes."
            )
        
        if current_usage["requests_per_minute"] > 50:
            recommendations.append(
                "🚨 High request frequency detected. Consider batching more requests together."
            )
        
        # Batch processing recommendations
        if current_usage["avg_batch_efficiency"] < 2 and current_usage["requests_today"] > 10:
            recommendations.append(
                "📦 Low batch efficiency. Try combining more operations into single requests."
            )
        
        # Token usage recommendations
        if current_usage["tokens_last_hour"] > 50000:
            recommendations.append(
                "💰 High token usage detected. Consider compressing inputs or using shorter prompts."
            )
        
        # Success recommendations
        if current_usage["optimization_score"] > 80:
            recommendations.append(
                "✅ Excellent API optimization! Current practices are working well."
            )
        elif current_usage["optimization_score"] > 60:
            recommendations.append(
                "👍 Good API optimization. Minor improvements possible."
            )
        else:
            recommendations.append(
                "🔧 API usage needs optimization. Focus on batching and rate limit management."
            )
        
        return recommendations
    
    def export_usage_report(self) -> str:
        """Export detailed usage report"""
        current_usage = self.get_current_usage()
        recommendations = self.get_recommendations()
        
        report = f"""
# Gemini API Usage Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Current Usage Statistics
- Requests per minute: {current_usage['requests_per_minute']}/60
- Requests per hour: {current_usage['requests_per_hour']}/3600
- Requests today: {current_usage['requests_today']}
- Tokens used (last hour): {current_usage['tokens_last_hour']:,}
- Total requests: {current_usage['total_requests']}
- Rate limit hits: {current_usage['rate_limit_hits']}
- Tokens saved through optimization: {current_usage['total_tokens_saved']:,}
- Average batch efficiency: {current_usage['avg_batch_efficiency']:.2f}x
- Optimization score: {current_usage['optimization_score']:.1f}/100

## Recommendations
"""
        
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        return report

# Global monitor instance
usage_monitor = APIUsageMonitor()
