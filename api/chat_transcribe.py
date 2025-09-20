import json
import os
import numpy as np
import speech_recognition as sr
import tempfile
import base64
from io import BytesIO

def handler(request, context):
    """Vercel serverless function handler for audio transcription."""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({})
        }
    
    if request.method == 'POST':
        try:
            # Handle file upload in Vercel
            if hasattr(request, 'files') and 'audio' in request.files:
                audio_file = request.files['audio']
                audio_data = audio_file.read()
            elif hasattr(request, 'json') and request.json and 'audio' in request.json:
                # Handle base64 encoded audio
                audio_data = base64.b64decode(request.json['audio'])
            else:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'No audio file provided', 'status': 'error'})
                }
            
            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                tmp.write(audio_data)
                wav_path = tmp.name
            
            try:
                # Use speech recognition
                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_path) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
                
                try:
                    text = recognizer.recognize_google(audio_data)
                    print(f"Transcribed: {text}")
                except sr.UnknownValueError:
                    text = ''
                    print("Could not understand audio")
                except sr.RequestError as e:
                    return {
                        'statusCode': 500,
                        'headers': headers,
                        'body': json.dumps({'error': f'Speech API error: {e}', 'status': 'error'})
                    }
                
                # Clean up temp file
                os.unlink(wav_path)
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'transcript': text, 'status': 'success'})
                }
                
            except Exception as audio_error:
                # Clean up temp file on error
                if os.path.exists(wav_path):
                    os.unlink(wav_path)
                raise audio_error
                
        except Exception as e:
            print(f"Transcription error: {e}")
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': str(e), 'status': 'error'})
            }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed', 'status': 'error'})
    }
