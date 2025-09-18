import React, { useRef, useState, useEffect } from 'react';
import { Mic, StopCircle, Loader2 } from 'lucide-react';

const VoiceRecorder = ({ onTranscript }) => {
  const [audioUrl, setAudioUrl] = useState(null);
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

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
        const response = await fetch('http://localhost:5000/voice/ai', {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        console.log('VoiceRecorder response:', data); // Debug log
        if (data.audio_url) {
          console.log('VoiceRecorder: Received audio_url from backend:', data.audio_url);
          setAudioUrl(data.audio_url);
        }
        if (data.recognized_text) {
          onTranscript(data.recognized_text);
        } else if (data.transcript) {
          onTranscript(data.transcript);
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

  // Debug useEffect hooks
  useEffect(() => {
    console.log('VoiceRecorder audioUrl state changed:', audioUrl);
  }, [audioUrl]);

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
      {!recording && !loading && (
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
    </div>
  );
};

export default VoiceRecorder;
