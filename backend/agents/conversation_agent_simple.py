import google.generativeai as genai
import json
import time
from typing import Dict, Any, Optional
from config import Config

class ConversationAgent:
    """Simple conversation agent focused on reliability"""
    
    def __init__(self, api_key: str = None):
        """Initialize the conversation agent"""
        self.config = Config()
        self.api_key = api_key or self.config.GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError("Google Gemini API key is required")
            
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.config.GEMINI_MODEL)
        
        print("[ConversationAgent] Initialized successfully")
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio using Google Speech Recognition (most reliable)"""
        try:
            # Use our simple STT implementation
            from .simple_stt import transcribe_audio_simple
            result = transcribe_audio_simple(audio_path)
            
            if result and result.strip():
                print(f"[ConversationAgent] Transcription successful: {result}")
                return result.strip()
            else:
                raise RuntimeError("Transcription returned empty result")
                
        except Exception as e:
            print(f"[ConversationAgent] Transcription failed: {e}")
            raise RuntimeError(f"Could not transcribe audio: {e}")
    
    def generate_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """Generate AI response using Gemini"""
        try:
            # Build context-aware prompt
            prompt = self._build_prompt(message, context)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                return "I apologize, but I couldn't generate a response. Please try again."
            
            # Clean up response
            result = response.text.strip()
            print(f"[ConversationAgent] Generated response length: {len(result)}")
            
            return result
            
        except Exception as e:
            print(f"[ConversationAgent] Response generation error: {e}")
            return "I'm having trouble processing your request right now. Please try again."
    
    def _build_prompt(self, message: str, context: Dict[str, Any] = None) -> str:
        """Build context-aware prompt for the AI"""
        base_prompt = """You are NyayMitra, a helpful AI assistant specializing in legal contract analysis.
        
You provide clear, accurate information about:
- Contract terms and clauses
- Legal risks and implications  
- Plain language explanations of legal concepts
- General legal guidance

Always be helpful, professional, and remind users to consult qualified legal professionals for specific legal advice.

"""
        
        # Add conversation context if available
        if context:
            if context.get('conversation_history'):
                base_prompt += f"\nConversation history: {context['conversation_history']}\n"
            
            if context.get('contract_context'):
                base_prompt += f"\nContract being discussed: {context['contract_context']}\n"
        
        base_prompt += f"\nUser message: {message}\n\nResponse:"
        
        return base_prompt
    
    def synthesize_speech(self, text: str) -> Optional[bytes]:
        """Convert text to speech (placeholder - implement as needed)"""
        print(f"[ConversationAgent] TTS requested for: {text[:50]}...")
        # For now, return None - implement TTS if needed
        return None
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the agent is working properly"""
        try:
            # Test Gemini API
            test_response = self.model.generate_content("Hello, are you working?")
            
            return {
                "status": "healthy",
                "gemini_api": "connected" if test_response else "error",
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }