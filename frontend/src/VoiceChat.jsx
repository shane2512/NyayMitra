import React, { useState, useRef } from "react";

import { useEffect } from "react";
const VoiceChat = () => {
  const [recording, setRecording] = useState(false);
  const [recognizedText, setRecognizedText] = useState("");
  const [answer, setAnswer] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    setRecognizedText("");
    setAnswer("");
    setAudioUrl(null);
    audioChunksRef.current = [];
    setRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new window.MediaRecorder(stream, { mimeType: 'audio/webm' });
    mediaRecorderRef.current = mediaRecorder;
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) audioChunksRef.current.push(e.data);
    };
    mediaRecorder.onstop = handleStop;
    mediaRecorder.start();
  };

  const stopRecording = () => {
    setRecording(false);
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
  };

  const handleStop = async () => {
    const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
    // Convert WebM to WAV using audio-decode and wav-encoder
    try {
      const arrayBuffer = await audioBlob.arrayBuffer();
      const decode = (await import('audio-decode')).default;
      const encodeWAV = (await import('wav-encoder')).default;
      const audioBuffer = await decode(arrayBuffer);
      const wavArrayBuffer = await encodeWAV(audioBuffer);
      const wavBlob = new Blob([wavArrayBuffer], { type: 'audio/wav' });
      const formData = new FormData();
      formData.append("audio", wavBlob, "recording.wav");
      const response = await fetch("/voice/ai", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        const data = await response.json();
        console.log('Voice AI Response:', data); // Debug log
        setRecognizedText(data.recognized_text || "");
        setAnswer(data.answer || "");
        if (data.audio_url) {
          const fullAudioUrl = data.audio_url.startsWith("http") ? data.audio_url : `${window.location.origin}${data.audio_url}`;
          console.log('Setting audio URL:', fullAudioUrl); // Debug log
          console.log('VoiceChat: Setting audioUrl:', fullAudioUrl);
        console.log('VoiceRecorder: Received audioUrl:', fullAudioUrl);
        setAudioUrl(fullAudioUrl);
        } else {
          console.log('No audio_url in response'); // Debug log
          setAudioUrl(null);
        }
      } else {
        setRecognizedText("Error: Could not process audio");
        setAnswer("");
        setAudioUrl(null);
      }
    } catch (err) {
      setRecognizedText("Error: " + err.message);
      setAnswer("");
      setAudioUrl(null);
    }
  };



  useEffect(() => {
    return () => {
      // Cleanup temp audios when component unmounts
      fetch("/voice/cleanup", { method: "POST" })
        .then((res) => res.json())
        .then((data) => console.log("Audio cleanup:", data))
        .catch((err) => console.log("Audio cleanup error:", err));
    };
  }, []);

  return (
    <div style={{ padding: 20, background: '#222', color: '#fff', borderRadius: 8 }}>
      <h2>🎤 Voice Chat</h2>
      <button onClick={recording ? stopRecording : startRecording} style={{ fontSize: 18, padding: 10, marginBottom: 12 }}>
        {recording ? "Stop Recording" : "Start Recording"}
      </button>
      {recognizedText && <div><b>You said:</b> {recognizedText}</div>}
      {answer && <div><b>AI:</b> {answer}</div>}
      {audioUrl && (
        <div style={{ marginTop: 16 }}>
          <audio 
            ref={(audio) => {
              if (audio) {
                audio.oncanplaythrough = () => {
                  console.log('Audio ready to play');
                  // Try to play automatically (may be blocked by browser)
                  audio.play().catch(e => {
                    console.log('Autoplay blocked, user must click play:', e);
                  });
                };
              }
            }}
            src={audioUrl} 
            controls 
            onError={(e) => console.error('Audio error:', e)}
            onLoadStart={() => console.log('Audio loading started')}
            onCanPlay={() => console.log('Audio can play')}
            onLoadedData={() => console.log('Audio data loaded')}
          />
          <div style={{ fontSize: 12, marginTop: 4, color: '#aaa' }}>
            🔊 AI Response Audio (Click play if it doesn't start automatically)
          </div>
          <div style={{ fontSize: 10, marginTop: 2, color: '#666' }}>
            URL: <a href={audioUrl} target="_blank" rel="noopener noreferrer" style={{color: '#4a9eff'}}>
              {audioUrl}
            </a>
          </div>
          <button 
            onClick={() => {
              const audio = document.querySelector('audio');
              if (audio) {
                audio.play().then(() => {
                  console.log('Manual play successful');
                }).catch(e => {
                  console.error('Manual play failed:', e);
                });
              }
            }}
            style={{ marginTop: 8, padding: '4px 8px', fontSize: 12 }}
          >
            🔊 Force Play Audio
          </button>
        </div>
      )}
    </div>
  );
};

export default VoiceChat;
