import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the NyayMitra backend application."""
    
    # API keys and other sensitive information
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_default_api_key_here")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    SLEEP_BETWEEN_REQUESTS = float(os.getenv("SLEEP_BETWEEN_REQUESTS", 2))
    
    # Other configurations
    DEBUG = os.getenv("DEBUG", "False") == "True"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    
    # Database configuration (if applicable)
    # DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///nyaymitra.db")