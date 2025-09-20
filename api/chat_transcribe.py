import json
import os
import numpy as np
import speech_recognition as sr
import tempfile

def handler(request):
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
            # Vercel passes files as request.files
            audio_file = request.files.get('audio')
            if not audio_file:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'No audio file provided', 'status': 'error'})
                }
            # Save to temp WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                tmp.write(audio_file.read())
                wav_path = tmp.name
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                text = ''
            except sr.RequestError as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'error': f'Speech API error: {e}', 'status': 'error'})
                }
            os.remove(wav_path)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'transcript': text, 'status': 'success'})
            }
        except Exception as e:
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
