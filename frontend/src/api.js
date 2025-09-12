import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export const analyzeContract = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    // Don't set Content-Type header - let axios handle it for FormData
    const response = await axios.post(`${API_BASE_URL}/analyze`, formData);
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error.response?.data || { error: 'Network error' };
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