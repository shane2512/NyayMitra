import axios from 'axios';

// Netlify Functions API configuration
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/.netlify/functions' 
  : 'http://localhost:8888/.netlify/functions';  // Netlify dev server

// Debug logging
console.log('🔧 API Configuration:');
console.log('NODE_ENV:', process.env.NODE_ENV);
console.log('API_BASE_URL:', API_BASE_URL);
if (typeof window !== 'undefined') {
  console.log('Current origin:', window.location.origin);
}

// Add axios defaults for better debugging
axios.defaults.timeout = 300000; // 5 minutes timeout for long analysis

export const analyzeContract = async (file, language = 'en', interests = []) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('language', language);
  formData.append('interests', JSON.stringify(interests));
  
  try {
    console.log('Making API request to:', `${API_BASE_URL}/analyze`);
    console.log('FormData contents:', {
      file: file.name,
      language: language,
      interests: interests
    });
    
    // Don't set Content-Type header - let axios handle it for FormData
    const response = await axios.post(`${API_BASE_URL}/analyze`, formData);
    console.log('API Response received:', response.status, response.data);
    
    return response.data;
  } catch (error) {
    console.error('API Error details:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      statusText: error.response?.statusText
    });
    
    if (error.response?.data) {
      throw error.response.data;
    } else {
      throw { error: error.message || 'Network error' };
    }
  }
};

export const healthCheck = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/admin?action=health`);
    
    // Handle serverless response format
    if (response.data.body) {
      return JSON.parse(response.data.body);
    }
    return response.data;
    
  } catch (error) {
    if (error.response?.data?.body) {
      const errorData = JSON.parse(error.response.data.body);
      throw errorData;
    }
    throw error.response?.data || { error: 'Network error' };
  }
};

// Chat API functions for serverless
export const sendChatMessage = async (message, sessionId = null, contractContext = null) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat?action=chat`, {
      message,
      session_id: sessionId,
      contract_context: contractContext
    });
    
    if (response.data.body) {
      return JSON.parse(response.data.body);
    }
    return response.data;
    
  } catch (error) {
    console.error('Chat API Error:', error);
    if (error.response?.data?.body) {
      const errorData = JSON.parse(error.response.data.body);
      throw errorData;
    }
    throw error.response?.data || { error: 'Chat request failed' };
  }
};

export const sendBatchChatMessage = async (questions, sessionId = null, contractContext = null) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat?action=batch`, {
      questions,
      session_id: sessionId,
      contract_context: contractContext
    });
    
    if (response.data.body) {
      return JSON.parse(response.data.body);
    }
    return response.data;
    
  } catch (error) {
    console.error('Batch Chat API Error:', error);
    if (error.response?.data?.body) {
      const errorData = JSON.parse(error.response.data.body);
      throw errorData;
    }
    throw error.response?.data || { error: 'Batch chat request failed' };
  }
};

export const getChatHistory = async (sessionId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/chat?action=history&session_id=${sessionId}`);
    
    if (response.data.body) {
      return JSON.parse(response.data.body);
    }
    return response.data;
    
  } catch (error) {
    console.error('Chat History API Error:', error);
    if (error.response?.data?.body) {
      const errorData = JSON.parse(error.response.data.body);
      throw errorData;
    }
    throw error.response?.data || { error: 'Failed to get chat history' };
  }
};

export const clearChatSession = async (sessionId) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat?action=clear`, {
      session_id: sessionId
    });
    
    if (response.data.body) {
      return JSON.parse(response.data.body);
    }
    return response.data;
    
  } catch (error) {
    console.error('Clear Chat API Error:', error);
    if (error.response?.data?.body) {
      const errorData = JSON.parse(error.response.data.body);
      throw errorData;
    }
    throw error.response?.data || { error: 'Failed to clear chat session' };
  }
};

export const getRateLimitStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/admin?action=rate-limit-status`);
    
    if (response.data.body) {
      return JSON.parse(response.data.body);
    }
    return response.data;
    
  } catch (error) {
    console.error('Rate Limit Status API Error:', error);
    if (error.response?.data?.body) {
      const errorData = JSON.parse(error.response.data.body);
      throw errorData;
    }
    throw error.response?.data || { error: 'Failed to get rate limit status' };
  }
};

export const getSupportedLanguages = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/languages`);
    
    if (response.data.body) {
      return JSON.parse(response.data.body);
    }
    return response.data;
    
  } catch (error) {
    console.error('Languages API Error:', error);
    if (error.response?.data?.body) {
      const errorData = JSON.parse(error.response.data.body);
      throw errorData;
    }
    throw error.response?.data || { error: 'Failed to get supported languages' };
  }
};

export const getTranslatorMetrics = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/admin?action=translator-metrics`);
    
    if (response.data.body) {
      return JSON.parse(response.data.body);
    }
    return response.data;
    
  } catch (error) {
    console.error('Translator Metrics API Error:', error);
    if (error.response?.data?.body) {
      const errorData = JSON.parse(error.response.data.body);
      throw errorData;
    }
    throw error.response?.data || { error: 'Failed to get translator metrics' };
  }
};

export const transcribeAudio = async (audioFile) => {
  try {
    const formData = new FormData();
    formData.append('audio', audioFile);
    
    const response = await axios.post(`${API_BASE_URL}/chat?action=transcribe`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    if (response.data.body) {
      return JSON.parse(response.data.body);
    }
    return response.data;
    
  } catch (error) {
    console.error('Transcribe API Error:', error);
    if (error.response?.data?.body) {
      const errorData = JSON.parse(error.response.data.body);
      throw errorData;
    }
    throw error.response?.data || { error: 'Audio transcription failed' };
  }
};

export const sendVoiceMessage = async (message, sessionId = null, contractContext = null) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat?action=voice`, {
      message,
      session_id: sessionId,
      contract_context: contractContext
    });
    
    if (response.data.body) {
      return JSON.parse(response.data.body);
    }
    return response.data;
    
  } catch (error) {
    console.error('Voice Chat API Error:', error);
    if (error.response?.data?.body) {
      const errorData = JSON.parse(error.response.data.body);
      throw errorData;
    }
    throw error.response?.data || { error: 'Voice chat request failed' };
  }
};