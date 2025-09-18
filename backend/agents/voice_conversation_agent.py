import os
import tempfile
import time
from typing import Dict, Any, Optional
import google.generativeai as genai

from .voice_utils import (
    recognize_speech_from_file,
    synthesize_speech,
    convert_raw_audio_to_wav,
    validate_audio_file
)
from .conversation_moderator import ConversationModeratorAgent
from config import Config

class VoiceConversationAgent:
    """
    Handles voice conversation pipeline: audio -> text -> AI response -> audio
    Integrates with ElevenLabs for STT/TTS and Gemini for AI responses
    """
    
    def __init__(self, gemini_api_key=None, elevenlabs_api_key=None):
        self.gemini_api_key = gemini_api_key or Config.GEMINI_API_KEY
        self.elevenlabs_api_key = elevenlabs_api_key or Config.ELEVEN_API_KEY
        
        # Initialize Gemini
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        # Initialize moderator
        self.moderator = ConversationModeratorAgent()
        
    def transcribe_audio(self, audio_path, use_elevenlabs=True):
        """
        Transcribe audio file to text using local Google Speech Recognition only.
        """
        try:
            validate_audio_file(audio_path)
            return recognize_speech_from_file(audio_path)
        except Exception as e:
            print(f"[VoiceConversationAgent] Transcription error: {e}")
            raise
    
    def generate_ai_response(self, text, context=None):
        """
        Generate AI response using Gemini
        """
        try:
            # Filter message through moderator
            moderation = self.moderator.filter_message(text)
            if not moderation["allowed"]:
                return {"error": moderation["reason"], "blocked": True}
            
            # Build prompt with context
            system_prompt = """You are NyayMitra AI, a helpful legal assistant specializing in contract analysis and legal guidance.
You provide clear, accurate, and practical legal information in a conversational manner.
Keep responses concise but informative, suitable for voice interaction.
Always remind users that for binding legal advice, they should consult a qualified lawyer."""

            if context:
                prompt = f"{system_prompt}\n\nContext: {context}\n\nUser: {text}\n\nAssistant:"
            else:
                prompt = f"{system_prompt}\n\nUser: {text}\n\nAssistant:"
            
            # Generate response with retries
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(prompt)
                    return {"response": response.text, "success": True}
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        print(f"[VoiceConversationAgent] Gemini error (attempt {attempt + 1}): {e}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise e
            
        except Exception as e:
            print(f"[VoiceConversationAgent] AI response error: {e}")
            return {"error": f"Failed to generate response: {str(e)}", "success": False}
    
    def text_to_speech(self, text):
        """
        Convert text to speech audio file
        """
        try:
            return synthesize_speech(text)
        except Exception as e:
            print(f"[VoiceConversationAgent] TTS error: {e}")
            raise
    
    def process_voice_message(self, audio_path, context=None, use_elevenlabs=True):
        """
        Complete voice processing pipeline: audio -> text -> AI -> audio
        """
        try:
            print(f"[VoiceConversationAgent] Processing voice message from: {audio_path}")
            
            # Step 1: Transcribe audio
            print("[VoiceConversationAgent] Step 1: Transcribing audio...")
            transcribed_text = self.transcribe_audio(audio_path, use_elevenlabs)
            
            if not transcribed_text:
                return {
                    "status": "error",
                    "error": "No speech recognized in audio",
                    "recognized_text": "",
                    "answer": "",
                    "audio_path": None
                }
            
            print(f"[VoiceConversationAgent] Transcribed: {transcribed_text}")
            
            # Step 2: Generate AI response
            print("[VoiceConversationAgent] Step 2: Generating AI response...")
            ai_result = self.generate_ai_response(transcribed_text, context)
            
            if "error" in ai_result:
                return {
                    "status": "error",
                    "error": ai_result["error"],
                    "recognized_text": transcribed_text,
                    "answer": "",
                    "audio_path": None,
                    "blocked": ai_result.get("blocked", False)
                }
            
            answer_text = ai_result["response"]
            print(f"[VoiceConversationAgent] AI response: {answer_text[:100]}...")
            
            # Step 3: Convert response to speech
            print("[VoiceConversationAgent] Step 3: Converting to speech...")
            audio_path = self.text_to_speech(answer_text)
            
            return {
                "status": "success",
                "recognized_text": transcribed_text,
                "answer": answer_text,
                "audio_path": audio_path
            }
            
        except Exception as e:
            print(f"[VoiceConversationAgent] Pipeline error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "recognized_text": "",
                "answer": "",
                "audio_path": None
            }
    
    def process_raw_audio(self, audio_data, samplerate=16000, sample_width=2, context=None):
        """
        Process raw audio data through the voice pipeline
        """
        try:
            # Convert raw audio to WAV file
            wav_path = convert_raw_audio_to_wav(audio_data, samplerate, sample_width)
            
            try:
                # Process the WAV file
                result = self.process_voice_message(wav_path, context)
                return result
            finally:
                # Clean up temporary WAV file
                if os.path.exists(wav_path):
                    os.remove(wav_path)
                    
        except Exception as e:
            print(f"[VoiceConversationAgent] Raw audio processing error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "recognized_text": "",
                "answer": "",
                "audio_path": None
            }

# Convenience function for the pipeline
def voice_conversation_pipeline(audio_path, context=None, use_elevenlabs=True):
    """
    Standalone function for voice conversation pipeline
    """
    agent = VoiceConversationAgent()
    return agent.process_voice_message(audio_path, context, use_elevenlabs)

def voice_conversation_elevenlabs_pipeline(audio_path, context=None):
    """
    ElevenLabs-specific pipeline function
    """
    return voice_conversation_pipeline(audio_path, context, use_elevenlabs=True)