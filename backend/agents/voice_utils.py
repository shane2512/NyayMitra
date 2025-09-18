import os
import tempfile
import re
import speech_recognition as sr
import soundfile as sf
import numpy as np
import requests
from datetime import datetime
import io
import wave

from config import Config

# Configuration
genai_api_key = Config.GEMINI_API_KEY
eleven_api_key = Config.ELEVEN_API_KEY
VOICE_ID = Config.VOICE_ID

def clean_text_for_speech(text):
    """Clean text by removing markdown and special formatting for better TTS"""
    # Remove bold markdown
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Remove code blocks
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove list markers
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    # Clean up whitespace
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove quotes and special chars
    text = re.sub(r'>\s+', '', text)
    text = re.sub(r'[^\w\s.,!?;:\'"()-]', '', text)
    return text.strip()

def recognize_speech_from_file(audio_path):
    """
    Convert audio file to text using Google Speech Recognition.
    Accepts any audio file format supported by soundfile; auto-converts to WAV if needed.
    """
    recognizer = sr.Recognizer()
    # Convert to WAV if not already
    if not audio_path.lower().endswith('.wav'):
        try:
            import soundfile as sf
            data, samplerate = sf.read(audio_path)
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_wav:
                sf.write(tmp_wav.name, data, samplerate)
                audio_path = tmp_wav.name
        except Exception as e:
            raise ValueError(f"Could not convert audio to WAV: {e}")
    try:
        with sr.AudioFile(audio_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)
    except Exception as e:
        raise ValueError(f"Audio file could not be read as WAV: {e}")
    try:
        text = recognizer.recognize_google(audio_data)
        print(f"[VoiceUtils] Recognized text: {text}")
        return text
    except sr.UnknownValueError:
        print("[VoiceUtils] Could not understand audio")
        return None
    except sr.RequestError as e:
        raise RuntimeError(f"Speech recognition API error: {e}")

def synthesize_speech(text):
    """
    Generate speech audio from text using ElevenLabs TTS.
    Returns a temporary file path (MP3).
    """
    if not eleven_api_key:
        raise ValueError("ElevenLabs API key not configured")
    
    # Clean text for better speech synthesis
    clean_text = clean_text_for_speech(text)
    
    if not clean_text.strip():
        raise ValueError("No text to synthesize after cleaning")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": eleven_api_key,
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
        print(f"[VoiceUtils] Synthesizing speech for: {clean_text[:100]}...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Write to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name
        
        print(f"[VoiceUtils] TTS audio saved to: {tmp_path}")
        return tmp_path
        
    except Exception as e:
        print(f"[VoiceUtils] TTS error: {e}")
        raise RuntimeError(f"Text-to-speech failed: {e}")

def convert_raw_audio_to_wav(audio_data, samplerate=16000, sample_width=2):
    """
    Convert raw audio data to WAV format.
    """
    try:
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            # Convert raw audio data to numpy array
            if sample_width == 2:
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
            elif sample_width == 4:
                audio_array = np.frombuffer(audio_data, dtype=np.int32)
            else:
                raise ValueError(f"Unsupported sample width: {sample_width}")
            
            # Write WAV file
            sf.write(tmp.name, audio_array, samplerate)
            return tmp.name
            
    except Exception as e:
        raise RuntimeError(f"Failed to convert raw audio to WAV: {e}")

def validate_audio_file(audio_path):
    """
    Validate that the audio file exists and is readable.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    if os.path.getsize(audio_path) == 0:
        raise ValueError("Audio file is empty")
    
    # Try to read the audio file
    try:
        if audio_path.lower().endswith('.wav'):
            with wave.open(audio_path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                if frames == 0:
                    raise ValueError("Audio file contains no audio data")
        return True
    except Exception as e:
        raise ValueError(f"Invalid audio file: {e}")