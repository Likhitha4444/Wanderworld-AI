import apiClient from '../api/client';

export const getTravelDNA = async () => {
  const response = await apiClient.get('/travel-dna/');
  return response.data;
};

export const recalculateTravelDNA = async () => {
  const response = await apiClient.post('/travel-dna/recalculate/');
  return response.data;
};
