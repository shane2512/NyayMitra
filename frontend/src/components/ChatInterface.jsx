import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageSquare, X, Loader2, RotateCcw, Sparkles, User, Bot, Mic, Keyboard } from 'lucide-react';
import { sendChatMessage, sendBatchChatMessage, clearChatSession, sendVoiceMessage } from '../api';
import VoiceRecorder from './VoiceRecorder';
import Button from './ui/Button';

const ChatInterface = ({ isOpen, onClose, contractContext }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [batchMode, setBatchMode] = useState(false);
  const [batchQuestions, setBatchQuestions] = useState([]);
  const [voiceMode, setVoiceMode] = useState(false);
  const [voiceTranscript, setVoiceTranscript] = useState(null);
  const [audioURL, setAudioURL] = useState(null);
  const [audioLoading, setAudioLoading] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [rateLimitWarning, setRateLimitWarning] = useState(false);
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const audioRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Stop audio when chat is closed
  useEffect(() => {
    if (!isOpen) {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
      setAudioURL(null);
      setVoiceMode(false);
      setVoiceTranscript(null);
    }
  }, [isOpen]);

  // Enhanced API call with retry logic and rate limit handling
  const makeAPICallWithRetry = async (apiCall, maxRetries = 3) => {
    let lastError;
    
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const response = await apiCall();
        setRetryCount(0);
        setRateLimitWarning(false);
        return response;
      } catch (error) {
        lastError = error;
        
        // Check for rate limit error
        if (error.response?.status === 429 || error.response?.data?.error?.includes('rate limit')) {
          setRateLimitWarning(true);
          
          // Calculate exponential backoff delay
          const delay = Math.min(1000 * Math.pow(2, attempt) + Math.random() * 1000, 30000);
          
          if (attempt < maxRetries) {
            setRetryCount(attempt + 1);
            await new Promise(resolve => setTimeout(resolve, delay));
            continue;
          }
        }
        
        // For other errors, retry with shorter delay
        if (attempt < maxRetries) {
          await new Promise(resolve => setTimeout(resolve, 1000));
          continue;
        }
        
        throw error;
      }
    }
    
    throw lastError;
  };

  const sendMessage = async (message = inputMessage) => {
    if (!message.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setSuggestions([]);

    try {
      const response = await makeAPICallWithRetry(async () => {
        return await sendChatMessage(message, sessionId, contractContext);
      });

      const { response: aiResponse, session_id, suggestions: newSuggestions } = response;
      
      setSessionId(session_id);
      
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: aiResponse,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, aiMessage]);
      
      if (newSuggestions && newSuggestions.length > 0) {
        setSuggestions(newSuggestions);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: rateLimitWarning 
          ? 'I\'m currently experiencing high demand. Please wait a moment and try again.' 
          : 'I apologize, but I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const sendBatchQuestions = async () => {
    if (batchQuestions.length === 0 || isLoading) return;

    setIsLoading(true);
    setSuggestions([]);

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: `Batch Questions:\n${batchQuestions.map((q, i) => `${i + 1}. ${q}`).join('\n')}`,
      timestamp: new Date().toISOString(),
      isBatch: true
    };

    setMessages(prev => [...prev, userMessage]);
    setBatchQuestions([]);

    try {
      const response = await makeAPICallWithRetry(async () => {
        return await sendBatchChatMessage(batchQuestions, sessionId, contractContext);
      });

      const { responses, session_id } = response;
      
      setSessionId(session_id);
      
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: responses.map((r, i) => `**Answer ${i + 1}:**\n${r}`).join('\n\n'),
        timestamp: new Date().toISOString(),
        isBatch: true
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending batch questions:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: rateLimitWarning 
          ? 'I\'m currently experiencing high demand. Please wait a moment and try again with fewer questions.' 
          : 'I apologize, but I encountered an error processing your questions. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setBatchMode(false);
    }
  };

  const handleVoiceTranscript = async (transcript, aiResponse, addToChat = true) => {
    setVoiceTranscript(transcript);
    
    if (addToChat) {
      // Old behavior - send transcript as message and get AI response
      setAudioLoading(true);
      
      try {
        // Send the transcript as a message
        await sendMessage(transcript);
        
        // Get voice response
        const response = await makeAPICallWithRetry(async () => {
          return await sendVoiceMessage(transcript, sessionId, contractContext);
        });
        
        if (response.audio_url) {
          console.log('Received audio_url from backend:', response.audio_url);
          const fullAudioUrl = response.audio_url.startsWith('http')
            ? response.audio_url
            : `${window.location.origin}${response.audio_url}`;
          console.log('Setting audio URL in <audio>:', fullAudioUrl);
          setAudioURL(fullAudioUrl);
        }
        if (response.answer) {
          const aiMessage = {
            id: Date.now() + 2,
            role: 'assistant',
            content: response.answer,
            timestamp: new Date().toISOString()
          };
          setMessages(prev => [...prev, aiMessage]);
        }
      } catch (error) {
        console.error('Voice response error:', error);
      } finally {
        setAudioLoading(false);
      }
    } else {
      // New behavior - VoiceRecorder already processed everything
      console.log('Voice processing complete - adding to chat');
      
      // Add user message (transcript) to chat
      const userMessage = {
        id: Date.now(),
        role: 'user', 
        content: transcript,
        timestamp: new Date().toISOString(),
        isVoice: true
      };
      
      // Add AI response to chat
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: aiResponse,
        timestamp: new Date().toISOString(),
        isVoiceResponse: true
      };
      
      setMessages(prev => [...prev, userMessage, aiMessage]);
    }
  };

  const clearHistory = async () => {
    try {
      await clearChatSession(sessionId);
      setMessages([]);
      setSessionId(null);
      setSuggestions([]);
    } catch (error) {
      console.error('Error clearing history:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-800 border border-gray-600 rounded-xl w-full max-w-4xl h-[80vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-600">
          <div className="flex items-center space-x-3">
            <MessageSquare className="w-6 h-6 text-blue-500" />
            <h2 className="text-xl font-bold text-gray-100">AI Legal Assistant</h2>
            {contractContext && (
              <span className="px-2 py-1 bg-green-500/20 text-green-400 text-xs font-medium rounded-full">
                Contract Loaded
              </span>
            )}
          </div>
          <div className="flex items-center space-x-2">
            {rateLimitWarning && (
              <span className="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs font-medium rounded-full">
                Rate Limited - Retrying...
              </span>
            )}
            <button
              onClick={clearHistory}
              className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
              title="Clear chat history"
            >
              <RotateCcw className="w-4 h-4 text-gray-400" />
            </button>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-gray-400" />
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <Sparkles className="w-12 h-12 text-blue-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-100 mb-2">
                Ask me anything about contracts and legal matters
              </h3>
              <p className="text-gray-400 text-sm">
                I can help you understand terms, identify risks, and provide legal insights
              </p>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] rounded-lg p-4 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : message.isError
                    ? 'bg-red-500/10 border border-red-500/30 text-red-400'
                    : 'bg-gray-700 text-gray-100'
                }`}
              >
                <div className="flex items-start space-x-2">
                  {message.role === 'assistant' && <Bot className="w-5 h-5 mt-1 flex-shrink-0" />}
                  {message.role === 'user' && <User className="w-5 h-5 mt-1 flex-shrink-0" />}
                  <div className="flex-1">
                    {message.isBatch && (
                      <span className="text-xs opacity-75 block mb-2">Batch Response</span>
                    )}
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
                  <span className="text-gray-300">Thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        {suggestions.length > 0 && (
          <div className="px-6 py-3 border-t border-gray-600">
            <p className="text-xs text-gray-400 mb-2">Suggested questions:</p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => sendMessage(suggestion)}
                  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-gray-300 text-sm rounded-lg transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Voice Mode */}
        {voiceMode ? (
          <div className="border-t border-gray-600 px-6 py-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-gray-300 flex items-center">
                <Mic className="w-4 h-4 mr-2 text-blue-500" />
                Voice Mode
              </h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setVoiceMode(false)}
              >
                <Keyboard className="w-4 h-4 mr-2" />
                Switch to Text
              </Button>
            </div>
            
            <VoiceRecorder onTranscript={handleVoiceTranscript} />
            
            {audioLoading && (
              <div className="flex items-center space-x-2 text-blue-400 mt-2">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-sm">Processing voice...</span>
              </div>
            )}
            
            {voiceTranscript && (
              <div className="text-center text-gray-300 text-sm mt-2">
                "{voiceTranscript}"
              </div>
            )}
            
            {audioURL && !audioLoading && (
              <audio 
                ref={audioRef}
                src={audioURL} 
                controls 
                autoPlay
                className="w-full mt-2 rounded-lg"
                onEnded={() => setAudioURL(null)}
              />
            )}
            
            <div className="text-xs text-gray-500 mt-2">
              Press the mic to record your question, then listen to the AI's voice response.
            </div>
          </div>
        ) : (
          <div className="border-t border-gray-600 px-6 py-4">
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setBatchMode(!batchMode)}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  batchMode
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {batchMode ? 'Batch Mode ON' : 'Batch Mode'}
              </button>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setVoiceMode(true)}
              >
                <Mic className="w-4 h-4 mr-2" />
                Voice
              </Button>

              {batchMode && batchQuestions.length > 0 && (
                <span className="text-xs text-gray-400">
                  {batchQuestions.length} questions queued
                </span>
              )}
            </div>

            {batchMode ? (
              <div className="mt-3 space-y-2">
                {batchQuestions.map((q, i) => (
                  <div key={i} className="text-sm text-gray-300 bg-gray-700 px-3 py-2 rounded">
                    {i + 1}. {q}
                  </div>
                ))}
                <div className="flex space-x-2">
                  <input
                    ref={inputRef}
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        if (inputMessage.trim()) {
                          setBatchQuestions([...batchQuestions, inputMessage]);
                          setInputMessage('');
                        }
                      }
                    }}
                    placeholder="Add a question to batch..."
                    className="flex-1 bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-gray-100 placeholder-gray-400 focus:outline-none focus:border-blue-500"
                  />
                  <Button
                    variant="primary"
                    onClick={sendBatchQuestions}
                    disabled={batchQuestions.length === 0 || isLoading}
                  >
                    Send Batch
                  </Button>
                </div>
              </div>
            ) : (
              <div className="flex space-x-2 mt-3">
                <input
                  ref={inputRef}
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      sendMessage();
                    }
                  }}
                  placeholder="Type your message..."
                  className="flex-1 bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-gray-100 placeholder-gray-400 focus:outline-none focus:border-blue-500"
                  disabled={isLoading}
                />
                <Button
                  variant="primary"
                  onClick={() => sendMessage()}
                  disabled={!inputMessage.trim() || isLoading}
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatInterface;
