import React, { useRef, useState, useEffect } from 'react';
import { Mic, StopCircle, Loader2 } from 'lucide-react';

const VoiceRecorder = ({ onTranscript }) => {
  const [audioUrl, setAudioUrl] = useState(null);
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [playing, setPlaying] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(null);

  const startRecording = async () => {
    setRecording(true);
    setLoading(false);
    audioChunksRef.current = [];
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new window.MediaRecorder(stream);
    mediaRecorderRef.current.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunksRef.current.push(event.data);
      }
    };
    mediaRecorderRef.current.onstop = async () => {
      setLoading(true);
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
      // Send audioBlob to backend for transcription
      const formData = new FormData();
      formData.append('audio', audioBlob);
      try {
        const response = await fetch('/api/chat_transcribe', {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        console.log('VoiceRecorder response:', data); // Debug log
        
        // Handle demo mode messaging
        if (data.demo_mode) {
          console.log('VoiceRecorder: Demo mode active');
        }
        
        // Handle TTS audio response
        if (data.audio_data) {
          console.log('VoiceRecorder: Received audio_data from backend');
          // Create audio URL from base64 data
          const audioData = `data:audio/mpeg;base64,${data.audio_data}`;
          setAudioUrl(audioData);
          
          // Auto-play the audio response
          setTimeout(() => {
            if (audioRef.current) {
              console.log('VoiceRecorder: Starting audio playback');
              setPlaying(true);
              audioRef.current.play().catch(error => {
                console.error('Audio playback failed:', error);
                setPlaying(false);
              });
            }
          }, 100);
        }
        
        // Handle transcript
        if (data.recognized_text) {
          onTranscript(data.recognized_text);
        } else if (data.transcript) {
          onTranscript(data.transcript);
        }
        
        // Display AI response if no audio
        if (data.ai_response && !data.audio_data) {
          console.log('VoiceRecorder: No audio, trying browser TTS fallback');
          // Use browser's built-in text-to-speech as fallback
          if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(data.ai_response);
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            utterance.volume = 0.8;
            
            utterance.onstart = () => {
              console.log('Browser TTS: Speech started');
              setPlaying(true);
            };
            
            utterance.onend = () => {
              console.log('Browser TTS: Speech ended');
              setPlaying(false);
            };
            
            utterance.onerror = (error) => {
              console.error('Browser TTS error:', error);
              setPlaying(false);
            };
            
            // Small delay to allow UI to update
            setTimeout(() => {
              window.speechSynthesis.speak(utterance);
            }, 500);
          }
        }
        
        // Show demo mode message if applicable
        if (data.message) {
          console.log('Voice service message:', data.message);
        }
      } catch (e) {
        // Optionally handle error
      }
      setLoading(false);
    };
    mediaRecorderRef.current.start();
  };

  const stopRecording = () => {
    setRecording(false);
    mediaRecorderRef.current?.stop();
  };

  // Auto-play effect when audioUrl changes
  useEffect(() => {
    console.log('VoiceRecorder audioUrl state changed:', audioUrl);
    if (audioUrl && audioRef.current) {
      console.log('VoiceRecorder: Audio element ready for playback');
    }
  }, [audioUrl]);

  // Handle audio events
  const handleAudioStart = () => {
    console.log('VoiceRecorder: Audio playback started');
    setPlaying(true);
  };

  const handleAudioEnd = () => {
    console.log('VoiceRecorder: Audio playback ended');
    setPlaying(false);
    setAudioUrl(null); // Clear audio URL after playing
  };

  const handleAudioError = (error) => {
    console.error('VoiceRecorder: Audio playback error:', error);
    setPlaying(false);
  };

  useEffect(() => {
    if (audioUrl) {
      setTimeout(() => {
        const audioEl = document.querySelector('audio');
        if (audioEl) {
          console.log('VoiceRecorder actual <audio> src:', audioEl.src);
        }
      }, 500);
    }
  }, [audioUrl]);

  return (
    <div className="flex flex-col items-center">
      {/* Hidden audio element for playback */}
      <audio
        ref={audioRef}
        src={audioUrl}
        onPlay={handleAudioStart}
        onEnded={handleAudioEnd}
        onError={handleAudioError}
        style={{ display: 'none' }}
      />
      
      {!recording && !loading && !playing && (
        <button
          onClick={startRecording}
          className="p-4 bg-blue-500/20 hover:bg-blue-500/40 rounded-full transition-colors"
          title="Start Recording"
        >
          <Mic className="w-8 h-8 text-blue-500" />
        </button>
      )}
      {recording && !loading && (
        <button
          onClick={stopRecording}
          className="p-4 bg-red-500/20 hover:bg-red-500/40 rounded-full transition-colors"
          title="Stop Recording"
        >
          <StopCircle className="w-8 h-8 text-red-500" />
        </button>
      )}
      {loading && (
        <div className="flex items-center space-x-2 mt-2">
          <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
          <span className="text-sm text-blue-400">Transcribing...</span>
        </div>
      )}
      {playing && (
        <div className="flex items-center space-x-2 mt-2">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-green-400">Playing response...</span>
        </div>
      )}
    </div>
  );
};

export default VoiceRecorder;
