import google.generativeai as genai
import json
import time
from typing import Dict, Any, Optional
from config import Config

class ConversationAgent:
    """Simple conversation agent focused on reliability"""
    
    def __init__(self, api_key: str = None, model_name: str = None):
        """Initialize the conversation agent"""
        self.config = Config()
        self.api_key = api_key or self.config.GEMINI_API_KEY
        self.model_name = model_name or self.config.GEMINI_MODEL
        if not self.api_key:
            raise ValueError("Google Gemini API key is required")
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        print(f"[ConversationAgent] Initialized successfully with model {self.model_name}")
    
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
Respond in 1-2 sentences. Be as concise and precise as possible.

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
        """Convert text to speech using ElevenLabs API, returns MP3 bytes."""
        import requests
        import tempfile
        import re
        api_key = self.config.ELEVEN_API_KEY
        voice_id = self.config.VOICE_ID
        if not api_key or not voice_id:
            print("[ConversationAgent] ElevenLabs API key or VOICE_ID missing!")
            return None
        # Clean text for better TTS
        def clean_text_for_speech(text):
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            text = re.sub(r'\*(.*?)\*', r'\1', text)
            text = re.sub(r'`(.*?)`', r'\1', text)
            text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
            text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
            text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
            text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
            text = re.sub(r'\n+', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            text = re.sub(r'>\s+', '', text)
            text = re.sub(r'[^\w\s.,!?;:\'\"()-]', '', text)
            return text.strip()
        clean_text = clean_text_for_speech(text)
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": clean_text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        try:
            print(f"[ConversationAgent] Requesting TTS from ElevenLabs for: {clean_text[:100]}...")
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            # Save to temp file and return bytes
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                tmp.write(response.content)
                tmp_path = tmp.name
            with open(tmp_path, 'rb') as f:
                audio_bytes = f.read()
            print(f"[ConversationAgent] TTS audio bytes length: {len(audio_bytes)}")
            return audio_bytes
        except Exception as e:
            print(f"[ConversationAgent] ElevenLabs TTS error: {e}")
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
