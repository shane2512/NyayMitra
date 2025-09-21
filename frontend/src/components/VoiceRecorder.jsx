import React, { useRef, useState, useEffect } from 'react';
import { Mic, StopCircle, Loader2 } from 'lucide-react';

const VoiceRecorder = ({ onTranscript }) => {
  const [audioUrl, setAudioUrl] = useState(null);
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [transcript, setTranscript] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(null);
  const recognitionRef = useRef(null);

  // Initialize browser speech recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';
      
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('Browser Speech Recognition Result:', transcript);
        setTranscript(transcript);
        processTranscript(transcript);
      };
      
      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setLoading(false);
        setRecording(false);
      };
      
      recognitionRef.current.onend = () => {
        console.log('Speech recognition ended');
        setRecording(false);
      };
    }
  }, []);

  const processTranscript = async (transcriptText) => {
    setLoading(true);
    try {
      // Send transcript to backend for AI response and TTS
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: transcriptText,
          voice_mode: true
        })
      });
      
      const data = await response.json();
      console.log('AI Response:', data);
      
      // Handle TTS audio response
      if (data.audio_data) {
        console.log('Received audio response from backend');
        const audioData = `data:audio/mpeg;base64,${data.audio_data}`;
        setAudioUrl(audioData);
        
        // Auto-play the audio response
        setTimeout(() => {
          if (audioRef.current) {
            console.log('Starting audio playback');
            setPlaying(true);
            audioRef.current.play().catch(error => {
              console.error('Audio playback failed:', error);
              setPlaying(false);
            });
          }
        }, 100);
      }
      
      // Send to chat interface
      if (onTranscript) {
        onTranscript(transcriptText, data.response || data.ai_response, false);
      }
      
      // Fallback to browser TTS if no audio
      if (!data.audio_data && data.response) {
        console.log('No audio from backend, using browser TTS');
        speakWithBrowserTTS(data.response);
      }
      
    } catch (error) {
      console.error('Error processing transcript:', error);
    } finally {
      setLoading(false);
    }
  };

  const speakWithBrowserTTS = (text) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      
      const speakText = () => {
        const utterance = new SpeechSynthesisUtterance(text);
        
        const voices = window.speechSynthesis.getVoices();
        const englishVoice = voices.find(voice => 
          voice.lang.startsWith('en') && voice.name.toLowerCase().includes('female')
        ) || voices.find(voice => voice.lang.startsWith('en')) || voices[0];
        
        if (englishVoice) {
          utterance.voice = englishVoice;
        }
        
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        utterance.onstart = () => setPlaying(true);
        utterance.onend = () => setPlaying(false);
        utterance.onerror = (error) => {
          console.error('Browser TTS error:', error);
          setPlaying(false);
        };
        
        window.speechSynthesis.speak(utterance);
      };
      
      if (window.speechSynthesis.getVoices().length === 0) {
        window.speechSynthesis.onvoiceschanged = speakText;
      } else {
        setTimeout(speakText, 100);
      }
    }
  };

  const startRecording = async () => {
    if (!recognitionRef.current) {
      console.error('Speech recognition not supported');
      return;
    }
    
    setRecording(true);
    setLoading(false);
    setTranscript('');
    
    try {
      console.log('Starting browser speech recognition...');
      recognitionRef.current.start();
    } catch (error) {
      console.error('Error starting speech recognition:', error);
      setRecording(false);
    }
  };
  const stopRecording = () => {
    if (recognitionRef.current && recording) {
      console.log('Stopping speech recognition...');
      recognitionRef.current.stop();
    }
    setRecording(false);
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

  // Cleanup audio when component unmounts or chat closes
  useEffect(() => {
    return () => {
      console.log('VoiceRecorder: Cleaning up audio on unmount');
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.src = '';
      }
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      setPlaying(false);
      setAudioUrl(null);
    };
  }, []);

  // Check if speech recognition is supported
  const isSpeechRecognitionSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;

  if (!isSpeechRecognitionSupported) {
    return (
      <div className="flex flex-col items-center p-4">
        <div className="text-sm text-red-400 text-center">
          Speech recognition is not supported in this browser.
          <br />
          Please use Chrome, Edge, or Safari for voice input.
        </div>
      </div>
    );
  }

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
      
      {/* Display current transcript */}
      {transcript && (
        <div className="mb-2 p-2 bg-gray-800 rounded text-sm text-green-400">
          You said: "{transcript}"
        </div>
      )}
      
      {!recording && !loading && !playing && (
        <button
          onClick={startRecording}
          className="p-4 bg-blue-500/20 hover:bg-blue-500/40 rounded-full transition-colors"
          title="Start Voice Recognition"
        >
          <Mic className="w-8 h-8 text-blue-500" />
        </button>
      )}
      {recording && !loading && (
        <button
          onClick={stopRecording}
          className="p-4 bg-red-500/20 hover:bg-red-500/40 rounded-full transition-colors"
          title="Stop Voice Recognition"
        >
          <StopCircle className="w-8 h-8 text-red-500" />
        </button>
      )}
      {loading && (
        <div className="flex items-center space-x-2 mt-2">
          <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
          <span className="text-sm text-blue-400">Processing...</span>
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
