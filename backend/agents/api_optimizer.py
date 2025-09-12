import time
import json
import random
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from functools import wraps
from .usage_monitor import usage_monitor

from config import Config

class GeminiAPIOptimizer:
    """
    Optimizes Gemini API usage to avoid rate limits and minimize costs.
    Implements batch processing, retry logic, and token optimization.
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        self.request_times = []  # Track request timestamps for rate limiting
        self.max_requests_per_minute = 60  # Conservative limit
        self.max_tokens_per_request = 30000  # Conservative token limit
        self.sleep_between_requests = float(getattr(Config, 'SLEEP_BETWEEN_REQUESTS', 2))
    
    def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limits and add sleep between requests"""
        now = time.time()
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if now - t < 60]
        if len(self.request_times) >= self.max_requests_per_minute:
            wait_time = 60 - (now - self.request_times[0]) + 1
            print(f"[APIOptimizer] Rate limit reached, waiting {wait_time:.1f} seconds...")
            time.sleep(wait_time)
        # Add user-configurable sleep to further reduce risk
        print(f"[APIOptimizer] Sleeping {self.sleep_between_requests:.1f}s between requests...")
        time.sleep(self.sleep_between_requests)

    def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limits"""
        now = time.time()
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if now - t < 60]
        
        if len(self.request_times) >= self.max_requests_per_minute:
            # Wait until we can make another request
            wait_time = 60 - (now - self.request_times[0]) + 1
            print(f"[APIOptimizer] Rate limit reached, waiting {wait_time:.1f} seconds...")
            time.sleep(wait_time)
    
    def _retry_with_backoff(self, func, max_retries: int = 3):
        """Retry function with exponential backoff on rate limit errors"""
        for attempt in range(max_retries):
            try:
                self._wait_for_rate_limit()
                self.request_times.append(time.time())
                return func()
            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "rate limit" in error_str or "quota" in error_str:
                    if attempt < max_retries - 1:
                        # Extract retry delay from error if available, otherwise use exponential backoff
                        delay = (2 ** attempt) + random.uniform(0, 1)
                        print(f"[APIOptimizer] Rate limit hit, retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})")
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
    
    def batch_analyze_clauses(self, clauses: List[str], analysis_type: str = "risk") -> Dict[str, Any]:
        """
        Batch process multiple clauses in a single API call to minimize requests.
        """
        if not clauses:
            return {}
        
        # Compress clauses if needed
        compressed_clauses = []
        for i, clause in enumerate(clauses):
            compressed = self._compress_text(clause, 800)  # Limit per clause
            compressed_clauses.append(f"CLAUSE_{i+1}: {compressed}")
        
        # Create batch prompt
        batch_prompt = self._create_batch_prompt(compressed_clauses, analysis_type)
        
        def make_request():
            response = self.model.generate_content(batch_prompt)
            return response.text
        
        # Execute with retry logic and monitoring
        start_time = time.time()
        response_text = self._retry_with_backoff(make_request)
        
        # Log usage statistics
        tokens_used = len(batch_prompt) + len(response_text)
        tokens_saved = max(0, (len(clauses) - 1) * 1000)  # Estimate tokens saved by batching
        usage_monitor.log_request(
            request_type="batch_analysis",
            tokens_used=tokens_used,
            batch_size=len(clauses),
            tokens_saved=tokens_saved
        )
        
        # Parse batch response back into individual results
        return self._parse_batch_response(response_text, len(clauses))
    
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
    
    def optimized_generate_content(self, prompt: str, max_retries: int = 3) -> str:
        """
        Generate content with optimization and retry logic
        """
        original_length = len(prompt)
        tokens_saved = 0
        
        # Compress prompt if too long
        if len(prompt) > self.max_tokens_per_request:
            print(f"[APIOptimizer] Compressing prompt from {len(prompt)} to {self.max_tokens_per_request} chars")
            prompt = self._compress_text(prompt, self.max_tokens_per_request)
            tokens_saved = original_length - len(prompt)
        
        def make_request():
            response = self.model.generate_content(prompt)
            return response.text
        
        # Execute with monitoring
        rate_limited = False
        try:
            response_text = self._retry_with_backoff(make_request, max_retries)
        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower():
                rate_limited = True
            raise e
        
        # Log usage
        tokens_used = len(prompt) + len(response_text)
        usage_monitor.log_request(
            request_type="individual_request",
            tokens_used=tokens_used,
            batch_size=1,
            tokens_saved=tokens_saved,
            rate_limited=rate_limited
        )
        
        return response_text
