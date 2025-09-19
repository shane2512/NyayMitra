import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the NyayMitra serverless backend."""
    
    # API keys and other sensitive information
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDgZrm7d1htahrLH2KMdVmnOEcQAIWzmys")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY", "sk_f3dc6582c9543b932c988a5a1f8702c19220766e06f59992")
    VOICE_ID = os.getenv("VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    
    # Rate limiting configuration
    SLEEP_BETWEEN_REQUESTS = float(os.getenv("SLEEP_BETWEEN_REQUESTS", 10))
    MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", 8))
    BATCH_PROCESSING_SLEEP = int(os.getenv("BATCH_PROCESSING_SLEEP", 15))
    INTER_BATCH_SLEEP = int(os.getenv("INTER_BATCH_SLEEP", 20))
    CIRCUIT_BREAKER_FAILURES = int(os.getenv("CIRCUIT_BREAKER_FAILURES", 2))
    CIRCUIT_BREAKER_TIMEOUT = int(os.getenv("CIRCUIT_BREAKER_TIMEOUT", 300))
    
    # Other configurations
    DEBUG = os.getenv("DEBUG", "False") == "True"
    
    # Serverless specific
    TEMP_DIR = "/tmp"  # Netlify temp directory
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'pdf'}
