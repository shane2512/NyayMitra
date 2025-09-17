"""
Utility script to set up the environment for the Legal Judgment RAG system.
"""

import os
import argparse
from pathlib import Path
from dotenv import load_dotenv, set_key

def setup_environment(api_token=None):
    """
    Set up the environment variables for the Legal Judgment RAG system.
    
    Args:
        api_token: Hugging Face API token (optional)
    """
    env_file = Path(".env")
    
    # Create .env file if it doesn't exist
    if not env_file.exists():
        env_file.touch()
    
    # Load existing .env file
    load_dotenv()
    
    # If API token provided, save it to .env
    if api_token:
        set_key(".env", "HUGGINGFACE_API_TOKEN", api_token)
        print(f"API token saved to {env_file.absolute()}")
    
    # Check if API token is set
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not token:
        print("Warning: HUGGINGFACE_API_TOKEN is not set")
        print("You can set it by running: python setup_env.py --api_token YOUR_API_TOKEN")
        print("Without an API token, the system will run in simulated mode")

def main():
    parser = argparse.ArgumentParser(
        description="Set up environment for Legal Judgment RAG system"
    )
    
    parser.add_argument(
        "--api_token",
        type=str,
        help="Hugging Face API token"
    )
    
    args = parser.parse_args()
    setup_environment(args.api_token)

if __name__ == "__main__":
    main()