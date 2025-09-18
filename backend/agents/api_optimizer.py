import time
import json
import random
import threading
import queue
from typing import List, Dict, Any, Optional, Callable
import google.generativeai as genai
from functools import wraps
from .usage_monitor import usage_monitor
from .rate_limit_recovery import rate_limit_recovery

from config import Config

class BatchProcessor:
    """Advanced batch processor for handling multiple clauses efficiently"""
    
    def __init__(self, max_batch_size: int = 5, max_tokens_per_batch: int = 25000):
        self.max_batch_size = max_batch_size
        self.max_tokens_per_batch = max_tokens_per_batch
        self.batch_queue = queue.Queue()
        self.processing_lock = threading.Lock()
        
    def add_to_batch_queue(self, clauses: List[str], analysis_type: str = "risk") -> str:
        """Add clauses to batch queue and return batch ID"""
        batch_id = f"batch_{int(time.time())}_{random.randint(1000, 9999)}"
        
        # Split clauses into optimal batch sizes
        batches = self._split_into_batches(clauses, analysis_type)
        
        for i, batch in enumerate(batches):
            batch_data = {
                'batch_id': f"{batch_id}_{i}",
                'clauses': batch,
                'analysis_type': analysis_type,
                'timestamp': time.time()
            }
            self.batch_queue.put(batch_data)
        
        return batch_id
    
    def _split_into_batches(self, clauses: List[str], analysis_type: str) -> List[List[str]]:
        """Split clauses into optimal batch sizes based on token limits"""
        batches = []
        current_batch = []
        current_tokens = 0
        
        for clause in clauses:
            # Estimate tokens for this clause (rough approximation)
            clause_tokens = len(clause) // 4  # ~4 chars per token
            
            # Check if adding this clause would exceed batch limits
            if (len(current_batch) >= self.max_batch_size or 
                current_tokens + clause_tokens > self.max_tokens_per_batch):
                
                if current_batch:  # Save current batch if not empty
                    batches.append(current_batch)
                    current_batch = []
                    current_tokens = 0
            
            current_batch.append(clause)
            current_tokens += clause_tokens
        
        # Add remaining batch
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def process_next_batch(self, api_optimizer) -> Dict[str, Any]:
        """Process the next batch in queue"""
        try:
            batch_data = self.batch_queue.get_nowait()
        except queue.Empty:
            return {}
        
        print(f"[BatchProcessor] Processing batch {batch_data['batch_id']} with {len(batch_data['clauses'])} clauses")
        
        try:
            # Process batch with enhanced error handling
            result = api_optimizer._process_batch_with_sleep(batch_data['clauses'], batch_data['analysis_type'])
            
            # Mark batch as processed
            self.batch_queue.task_done()
            
            return result
            
        except Exception as e:
            print(f"[BatchProcessor] Batch {batch_data['batch_id']} failed: {e}")
            # Re-queue failed batch with backoff
            time.sleep(30)  # Wait 30 seconds before retry
            self.batch_queue.put(batch_data)
            raise e

# Global batch processor instance
_global_batch_processor = BatchProcessor(max_batch_size=5, max_tokens_per_batch=25000)

class RateLimitedQueue:
    """Thread-safe queue for serializing API requests to prevent rate limit issues"""
    
    def __init__(self, max_requests_per_minute: int = 15, min_delay: float = 5.0):
        self.queue = queue.Queue()
        self.request_times = []
        self.max_requests_per_minute = max_requests_per_minute
        self.min_delay = min_delay
        self.lock = threading.Lock()
        self.consecutive_failures = 0
        self.circuit_breaker_open_until = 0
        self.last_request_time = 0
        
    def execute_request(self, func: Callable, *args, **kwargs):
        """Execute a function with strict rate limiting and intelligent recovery"""
        with self.lock:
            now = time.time()
            
            # Check intelligent recovery system
            should_pause, pause_time = rate_limit_recovery.should_pause_requests()
            if should_pause:
                print(f"[RateQueue] Intelligent recovery suggests pausing for {pause_time:.1f}s")
                time.sleep(pause_time)
                now = time.time()
            
            # Use adaptive delay from recovery system
            adaptive_delay = rate_limit_recovery.get_recommended_delay()
            effective_delay = max(self.min_delay, adaptive_delay)
            
            # Circuit breaker check
            if self.circuit_breaker_open_until > now:
                wait_time = self.circuit_breaker_open_until - now
                print(f"[RateQueue] Circuit breaker active, waiting {wait_time:.1f}s")
                time.sleep(wait_time)
            
            # Clean old request times (older than 1 minute)
            self.request_times = [t for t in self.request_times if now - t < 60]
            
            # Enforce minimum delay between requests
            time_since_last = now - self.last_request_time
            if time_since_last < effective_delay:
                sleep_time = effective_delay - time_since_last
                print(f"[RateQueue] Enforcing {sleep_time:.1f}s delay (adaptive: {adaptive_delay:.1f}s)")
                time.sleep(sleep_time)
                now = time.time()
            
            # Check if we need to wait for rate limit window
            if len(self.request_times) >= self.max_requests_per_minute:
                oldest_request = self.request_times[0]
                wait_time = 60 - (now - oldest_request) + 1
                print(f"[RateQueue] Rate limit reached, waiting {wait_time:.1f}s")
                time.sleep(wait_time)
                now = time.time()
                # Clean again after wait
                self.request_times = [t for t in self.request_times if now - t < 60]
            
            # Execute the request
            self.request_times.append(now)
            self.last_request_time = now
            
            try:
                result = func(*args, **kwargs)
                self.consecutive_failures = 0  # Reset on success
                rate_limit_recovery.record_success()  # Record success in recovery system
                return result
            except Exception as e:
                self.consecutive_failures += 1
                
                # Record rate limit in intelligent recovery system
                error_str = str(e).lower()
                if any(term in error_str for term in ["429", "rate limit", "quota", "too many requests"]):
                    rate_limit_recovery.record_rate_limit(str(e))
                
                if self.consecutive_failures >= 3:
                    self.circuit_breaker_open_until = now + 300  # 5 minute circuit breaker
                    print(f"[RateQueue] Circuit breaker opened for 5 minutes after {self.consecutive_failures} failures")
                raise e

# Global rate-limited queue instance
_global_rate_queue = RateLimitedQueue(max_requests_per_minute=10, min_delay=8.0)

class GeminiAPIOptimizer:
    """
    Optimizes Gemini API usage to avoid rate limits and minimize costs.
    Implements batch processing, retry logic, token optimization, and strict rate limiting.
    """
    
    def __init__(self, api_key: str, model_name: str = None):
        if model_name is None:
            model_name = Config.GEMINI_MODEL
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        self.request_times = []  # Track request timestamps for rate limiting
        self.max_requests_per_minute = getattr(Config, 'MAX_REQUESTS_PER_MINUTE', 10)  # Very conservative
        self.circuit_breaker_failures = getattr(Config, 'CIRCUIT_BREAKER_FAILURES', 2)  # Reduced threshold
        self.circuit_breaker_timeout = getattr(Config, 'CIRCUIT_BREAKER_TIMEOUT', 300)  # 5 minutes
        self.consecutive_failures = 0
        self.circuit_breaker_open_until = 0
        self.max_tokens_per_request = 25000  # More conservative token limit
        self.sleep_between_requests = float(getattr(Config, 'SLEEP_BETWEEN_REQUESTS', 8))  # Increased default delay
        self.rate_queue = _global_rate_queue  # Use global queue for all instances
    
    def _wait_for_rate_limit(self):
        """Enhanced rate limiting with multiple safety layers"""
        # Delegate to the global rate queue for thread-safe rate limiting
        pass  # All rate limiting now handled by RateLimitedQueue
    
    def _retry_with_backoff(self, func, max_retries: int = 5):
        """Enhanced retry function with exponential backoff and jitter"""
        base_delay = 2.0
        max_delay = 120.0
        
        for attempt in range(max_retries):
            try:
                # Use the global rate queue to execute the function
                return self.rate_queue.execute_request(func)
                
            except Exception as e:
                error_str = str(e).lower()
                is_rate_limit = any(term in error_str for term in [
                    "429", "rate limit", "quota", "too many requests", 
                    "resource exhausted", "rate_limit_exceeded"
                ])
                
                if is_rate_limit or "quota" in error_str:
                    if attempt < max_retries - 1:
                        # Enhanced exponential backoff with jitter
                        exponential_delay = min(base_delay * (2 ** attempt), max_delay)
                        jitter = random.uniform(0.1, 0.5) * exponential_delay
                        total_delay = exponential_delay + jitter
                        
                        print(f"[APIOptimizer] Rate limit hit! Attempt {attempt + 1}/{max_retries}")
                        print(f"[APIOptimizer] Backing off for {total_delay:.1f}s (base: {exponential_delay:.1f}s + jitter: {jitter:.1f}s)")
                        time.sleep(total_delay)
                        continue
                    else:
                        print(f"[APIOptimizer] Max retries exceeded after rate limit errors")
                        raise Exception(f"Persistent rate limiting after {max_retries} attempts. Please wait before retrying.")
                else:
                    # Non-rate-limit error, don't retry as aggressively
                    if attempt < 2:  # Only retry once for non-rate-limit errors
                        delay = 1.0 + random.uniform(0, 1)
                        print(f"[APIOptimizer] Non-rate-limit error, retrying in {delay:.1f}s: {e}")
                        time.sleep(delay)
                        continue
                    raise e
        
        raise Exception(f"Max retries ({max_retries}) exceeded")
    
    def _compress_text(self, text: str, max_length: int = 1000) -> str:
        """Compress long text while preserving key information"""
        if len(text) <= max_length:
            return text
        
        # Split into sentences and keep most important ones
        sentences = text.replace('\n', ' ').split('. ')
        if len(sentences) <= 3:
            return text[:max_length] + "..."
        
        # Keep first sentence, last sentence, and middle content
        compressed = sentences[0] + ". "
        remaining_length = max_length - len(compressed) - len(sentences[-1]) - 10
        
        middle_content = '. '.join(sentences[1:-1])
        if len(middle_content) > remaining_length:
            middle_content = middle_content[:remaining_length] + "..."
        
        compressed += middle_content + ". " + sentences[-1]
        return compressed
    
    def _process_batch_with_sleep(self, clauses: List[str], analysis_type: str = "risk") -> Dict[str, Any]:
        """Process a batch of clauses with enhanced sleep mechanisms"""
        print(f"[APIOptimizer] Processing batch of {len(clauses)} clauses with type: {analysis_type}")
        
        # Compress clauses more aggressively for batch processing
        compressed_clauses = []
        for i, clause in enumerate(clauses):
            compressed = self._compress_text(clause, 600)  # More aggressive compression
            compressed_clauses.append(f"CLAUSE_{i+1}: {compressed}")
        
        # Create optimized batch prompt
        batch_prompt = self._create_optimized_batch_prompt(compressed_clauses, analysis_type)
        
        def make_batch_request():
            print(f"[APIOptimizer] Executing batch request with {len(compressed_clauses)} clauses")
            response = self.model.generate_content(batch_prompt)
            if not response.text:
                raise Exception("Empty response from batch API")
            return response.text
        
        # Execute with enhanced sleep and monitoring
        start_time = time.time()
        
        # Add extra sleep before batch processing to prevent rate limits
        batch_sleep = getattr(Config, 'BATCH_PROCESSING_SLEEP', 10)
        print(f"[APIOptimizer] Sleeping {batch_sleep}s before batch processing")
        time.sleep(batch_sleep)
        
        response_text = self._retry_with_backoff(make_batch_request, max_retries=3)
        
        elapsed = time.time() - start_time
        print(f"[APIOptimizer] Batch completed in {elapsed:.1f}s")
        
        # Log batch usage
        tokens_used = len(batch_prompt) + len(response_text)
        tokens_saved = max(0, (len(clauses) - 1) * 800)  # Estimate savings
        usage_monitor.log_request(
            request_type="enhanced_batch_analysis",
            tokens_used=tokens_used,
            batch_size=len(clauses),
            tokens_saved=tokens_saved
        )
        
        # Parse and return results
        return self._parse_batch_response(response_text, len(clauses))
    
    def _create_optimized_batch_prompt(self, clauses: List[str], analysis_type: str) -> str:
        """Create highly optimized batch prompt with better structure"""
        clauses_text = "\n\n".join(clauses)
        
        if analysis_type == "risk":
            return f"""You are an expert contract risk analyzer. Analyze ALL the following contract clauses in a SINGLE response.

For EACH clause, provide analysis in this EXACT format:
CLAUSE_X_ANALYSIS:
{{
    "risk_level": "High|Medium|Low",
    "analysis": "Brief explanation of risk factors"
}}

Contract Clauses to Analyze:
{clauses_text}

Analyze each clause for: legal liability, financial risk, operational constraints, compliance requirements, termination risks, indemnification, limitation of liability, IP issues, data protection, dispute resolution.

Respond with analysis for ALL clauses in the exact JSON format shown above. Be strict - only mark as Low risk if truly standard and minimal risk."""
        
        elif analysis_type == "summary":
            return f"""You are a legal expert who explains complex contract terms in simple language.

Analyze ALL the following contract clauses and provide a comprehensive summary that:
1. Explains the overall risk level
2. Highlights the most important concerns in everyday language
3. Provides actionable recommendations
4. Uses a conversational, helpful tone
5. Avoids legal jargon

Contract Clauses:
{clauses_text}

Provide a single comprehensive summary covering all clauses that a regular person can understand."""
        
        return f"Analyze the following contract clauses:\n{clauses_text}"
    
    def batch_analyze_clauses(self, clauses: List[str], analysis_type: str = "risk") -> Dict[str, Any]:
        """
        Batch processing with intelligent queuing and sleep mechanisms
        (Alias for enhanced_batch_analyze_clauses for backward compatibility)
        """
        return self.enhanced_batch_analyze_clauses(clauses, analysis_type)
    
    def enhanced_batch_analyze_clauses(self, clauses: List[str], analysis_type: str = "risk") -> Dict[str, Any]:
        """
        Enhanced batch processing with intelligent queuing and sleep mechanisms
        """
        if not clauses:
            return {}
        
        print(f"[APIOptimizer] Starting enhanced batch analysis for {len(clauses)} clauses")
        
        # Use the global batch processor to queue and process
        batch_id = _global_batch_processor.add_to_batch_queue(clauses, analysis_type)
        
        # Process batches sequentially with enhanced sleep
        all_results = {}
        batch_count = 0
        
        while True:
            try:
                batch_result = _global_batch_processor.process_next_batch(self)
                if not batch_result:
                    break  # No more batches to process
                
                all_results.update(batch_result)
                batch_count += 1
                
                # Add sleep between batches to prevent rate limits
                if batch_count > 0:
                    inter_batch_sleep = getattr(Config, 'INTER_BATCH_SLEEP', 15)
                    print(f"[APIOptimizer] Sleeping {inter_batch_sleep}s between batches")
                    time.sleep(inter_batch_sleep)
                    
            except Exception as e:
                print(f"[APIOptimizer] Batch processing failed: {e}")
                # Continue with next batch if possible
                continue
        
        print(f"[APIOptimizer] Enhanced batch analysis completed: {len(all_results)} results from {batch_count} batches")
        return all_results
    
    def _create_batch_prompt(self, clauses: List[str], analysis_type: str) -> str:
        """Create optimized batch prompt for multiple clauses"""
        clauses_text = "\n\n".join(clauses)
        
        if analysis_type == "risk":
            return f"""
You are an expert contract risk analyzer. Analyze ALL the following contract clauses in a SINGLE response.

For EACH clause, provide analysis in this EXACT format:
CLAUSE_X_ANALYSIS:
{{
    "risk_level": "High|Medium|Low",
    "analysis": "Brief explanation of risk factors"
}}

Contract Clauses to Analyze:
{clauses_text}

Analyze each clause for: legal liability, financial risk, operational constraints, compliance requirements, termination risks, indemnification, limitation of liability, IP issues, data protection, dispute resolution.

Respond with analysis for ALL clauses in the exact JSON format shown above. Be strict - only mark as Low risk if truly standard and minimal risk.
"""
        
        elif analysis_type == "summary":
            return f"""
You are a legal expert who explains complex contract terms in simple language.

Analyze ALL the following contract clauses and provide a comprehensive summary that:
1. Explains the overall risk level
2. Highlights the most important concerns in everyday language
3. Provides actionable recommendations
4. Uses a conversational, helpful tone
5. Avoids legal jargon

Contract Clauses:
{clauses_text}

Provide a single comprehensive summary covering all clauses that a regular person can understand.
"""
        
        return f"Analyze the following contract clauses:\n{clauses_text}"
    
    def _parse_batch_response(self, response_text: str, num_clauses: int) -> Dict[str, Any]:
        """Parse batch response back into individual clause results"""
        results = {}
        
        try:
            # Look for CLAUSE_X_ANALYSIS patterns
            for i in range(1, num_clauses + 1):
                clause_key = f"Clause {i}"
                pattern = f"CLAUSE_{i}_ANALYSIS:"
                
                if pattern in response_text:
                    # Extract JSON for this clause
                    start_idx = response_text.find(pattern) + len(pattern)
                    # Find the end of this clause's JSON (look for next CLAUSE_ or end of string)
                    end_patterns = [f"CLAUSE_{i+1}_ANALYSIS:", "```", "\n\n"]
                    end_idx = len(response_text)
                    
                    for end_pattern in end_patterns:
                        temp_idx = response_text.find(end_pattern, start_idx)
                        if temp_idx != -1 and temp_idx < end_idx:
                            end_idx = temp_idx
                    
                    json_text = response_text[start_idx:end_idx].strip()
                    
                    # Clean up JSON
                    if json_text.startswith('```json'):
                        json_text = json_text[7:]
                    if json_text.endswith('```'):
                        json_text = json_text[:-3]
                    
                    try:
                        analysis_data = json.loads(json_text.strip())
                        results[clause_key] = {
                            "text": f"Clause {i} (batch processed)",
                            "analysis": analysis_data
                        }
                    except json.JSONDecodeError:
                        # Fallback parsing
                        results[clause_key] = {
                            "text": f"Clause {i} (batch processed)",
                            "analysis": {
                                "risk_level": "Medium",
                                "analysis": "Batch processing - manual review recommended"
                            }
                        }
                else:
                    # Fallback if pattern not found
                    results[clause_key] = {
                        "text": f"Clause {i} (batch processed)",
                        "analysis": {
                            "risk_level": "Medium", 
                            "analysis": "Batch analysis completed - review recommended"
                        }
                    }
        
        except Exception as e:
            print(f"[APIOptimizer] Error parsing batch response: {e}")
            # Return fallback results
            for i in range(1, num_clauses + 1):
                results[f"Clause {i}"] = {
                    "text": f"Clause {i} (batch processed)",
                    "analysis": {
                        "risk_level": "Medium",
                        "analysis": "Batch processing error - manual review needed"
                    }
                }
        
        return results
    
    def optimized_generate_content(self, prompt: str, max_retries: int = 5) -> str:
        """
        Generate content with enhanced optimization and retry logic
        """
        original_length = len(prompt)
        tokens_saved = 0
        
        # More aggressive compression for rate limit prevention
        if len(prompt) > self.max_tokens_per_request:
            print(f"[APIOptimizer] Compressing prompt from {len(prompt)} to {self.max_tokens_per_request} chars")
            prompt = self._compress_text(prompt, self.max_tokens_per_request)
            tokens_saved = original_length - len(prompt)
        
        def make_request():
            print(f"[APIOptimizer] Making API request (prompt length: {len(prompt)} chars)")
            response = self.model.generate_content(prompt)
            if not response.text:
                raise Exception("Empty response from API")
            return response.text
        
        # Execute with enhanced monitoring and error handling
        rate_limited = False
        try:
            start_time = time.time()
            response_text = self._retry_with_backoff(make_request, max_retries)
            elapsed = time.time() - start_time
            print(f"[APIOptimizer] Request completed in {elapsed:.1f}s")
            
            # Validate response
            if not response_text or len(response_text.strip()) < 10:
                print(f"[APIOptimizer] Warning: Response is too short or empty")
                raise Exception("API returned empty or very short response")
            
        except Exception as e:
            error_str = str(e).lower()
            if any(term in error_str for term in ["429", "rate limit", "quota", "too many requests"]):
                rate_limited = True
                print(f"[APIOptimizer] CRITICAL: Persistent rate limiting detected. Consider:")
                print("  1. Increasing SLEEP_BETWEEN_REQUESTS in config")
                print("  2. Reducing MAX_REQUESTS_PER_MINUTE") 
                print("  3. Using a different API key or project")
                print("  4. Waiting 10-15 minutes before retrying")
            raise e
        
        # Log usage with enhanced tracking
        tokens_used = len(prompt) + len(response_text)
        usage_monitor.log_request(
            request_type="individual_request",
            tokens_used=tokens_used,
            batch_size=1,
            tokens_saved=tokens_saved,
            rate_limited=rate_limited
        )
        
        return response_text
