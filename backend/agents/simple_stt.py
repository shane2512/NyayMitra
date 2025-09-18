"""
Simple speech-to-text utility using Google Speech Recognition
"""
import speech_recognition as sr
import os
import tempfile

def transcribe_audio_simple(audio_path):
    """
    Simple, reliable audio transcription using Google Speech Recognition
    """
    try:
        recognizer = sr.Recognizer()
        
        print(f"[SimpleTTS] Transcribing: {audio_path}")
        
        # Check if file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Convert to WAV if needed
        if not audio_path.lower().endswith('.wav'):
            audio_path = convert_to_wav(audio_path)
        
        # Transcribe
        with sr.AudioFile(audio_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)
        
        # Use Google's free speech recognition
        text = recognizer.recognize_google(audio_data, language='en-US')
        print(f"[SimpleTTS] Result: {text}")
        return text
        
    except sr.UnknownValueError:
        print("[SimpleTTS] Could not understand the audio")
        return ""
    except sr.RequestError as e:
        print(f"[SimpleTTS] API error: {e}")
        return ""
    except Exception as e:
        print(f"[SimpleTTS] Error: {e}")
        return ""

def convert_to_wav(audio_path):
    """
    Convert audio file to WAV format using pydub
    """
    try:
        from pydub import AudioSegment
        
        # Load the audio file
        audio = AudioSegment.from_file(audio_path)
        
        # Create temporary WAV file
        wav_path = tempfile.mktemp(suffix='.wav')
        audio.export(wav_path, format="wav")
        
        print(f"[SimpleTTS] Converted to WAV: {wav_path}")
        return wav_path
        
    except ImportError:
        print("[SimpleTTS] pydub not available, assuming audio is already in correct format")
        return audio_path
    except Exception as e:
        print(f"[SimpleTTS] Conversion failed: {e}")
        return audio_path

# Test function
if __name__ == "__main__":
    # Test with a sample audio file
    test_file = "test_audio.wav"
    if os.path.exists(test_file):
        result = transcribe_audio_simple(test_file)
        print(f"Transcription result: {result}")
    else:
        print("No test file found")