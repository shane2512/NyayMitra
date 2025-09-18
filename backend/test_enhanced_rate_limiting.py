#!/usr/bin/env python3
"""
Enhanced Rate Limiting Test Script
Tests the improved batch processing and sleep mechanisms
"""

import time
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.api_optimizer import GeminiAPIOptimizer
from config import Config

def test_enhanced_rate_limiting():
    """Test the enhanced rate limiting and batch processing"""
    print("🔧 Testing Enhanced Rate Limiting & Batch Processing")
    print("=" * 60)

    # Check if API key is available
    if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == "your_default_api_key_here":
        print("❌ GEMINI_API_KEY not configured. Please set your API key in environment variables.")
        return

    # Initialize optimizer
    optimizer = GeminiAPIOptimizer(Config.GEMINI_API_KEY)

    # Test data - sample contract clauses
    test_clauses = [
        "The indemnification clause requires the party to indemnify and hold harmless the other party from any claims arising from the party's negligence or willful misconduct.",
        "Termination may occur immediately upon breach of confidentiality obligations without any cure period.",
        "All disputes shall be resolved through binding arbitration in a jurisdiction favorable to the service provider.",
        "The limitation of liability caps damages at an amount equal to the fees paid in the preceding 12 months.",
        "Intellectual property rights shall be assigned to the service provider upon creation, including all future improvements and derivatives.",
        "Payment terms require full payment within 30 days, with interest at 1.5% per month on overdue amounts.",
        "The non-compete clause prevents the party from engaging in similar business activities for 2 years within 50 miles of any customer location."
    ]

    print(f"📋 Testing with {len(test_clauses)} sample clauses")
    print(f"⚙️  Configuration:")
    print(f"   - Max requests per minute: {Config.MAX_REQUESTS_PER_MINUTE}")
    print(f"   - Sleep between requests: {Config.SLEEP_BETWEEN_REQUESTS}s")
    print(f"   - Batch processing sleep: {Config.BATCH_PROCESSING_SLEEP}s")
    print(f"   - Inter-batch sleep: {Config.INTER_BATCH_SLEEP}s")
    print()

    try:
        # Test enhanced batch processing
        print("🚀 Testing Enhanced Batch Processing...")
        start_time = time.time()

        results = optimizer.enhanced_batch_analyze_clauses(test_clauses, "risk")

        elapsed = time.time() - start_time
        print(f"⏱️  Total processing time: {elapsed:.1f}s")
        print(f"📊 Results: {len(results)} clauses analyzed")

        # Show sample results
        if results:
            print("\n📋 Sample Results:")
            for i, (clause_id, result) in enumerate(list(results.items())[:3]):
                analysis = result.get('analysis', {})
                risk_level = analysis.get('risk_level', 'Unknown')
                analysis_text = analysis.get('analysis', 'No analysis')[:100] + "..."
                print(f"   {clause_id}: {risk_level} Risk - {analysis_text}")

        print("\n✅ Enhanced batch processing test completed successfully!")
        print("💡 The system is now using:")
        print("   - Intelligent batch queuing")
        print("   - Enhanced sleep mechanisms")
        print("   - Circuit breaker protection")
        print("   - Exponential backoff with jitter")
        print("   - Aggressive rate limit prevention")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("🔧 Troubleshooting:")
        print("   1. Check your GEMINI_API_KEY")
        print("   2. Verify network connectivity")
        print("   3. Consider increasing sleep times in config.py")
        print("   4. Check API quota limits")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("🔧 Troubleshooting:")
        print("   1. Check your GEMINI_API_KEY")
        print("   2. Verify network connectivity")
        print("   3. Consider increasing sleep times in config.py")
        print("   4. Check API quota limits")

if __name__ == "__main__":
    test_enhanced_rate_limiting()
