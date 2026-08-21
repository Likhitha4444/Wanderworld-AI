import apiClient from './src/api/client.js';

async function testConnection() {
  try {
    const response = await apiClient.get('/health/');
    console.log('Frontend → Backend connection = PASS');
    console.log('Response:', response.data);
  } catch (error) {
    console.error('Frontend → Backend connection = FAIL');
    console.error('Error:', error.message);
  }
}

testConnection();
