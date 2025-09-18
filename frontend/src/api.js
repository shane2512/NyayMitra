import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

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
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Network error' };
  }
};