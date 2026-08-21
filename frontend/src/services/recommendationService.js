import apiClient from '../api/client';

export const getRecommendations = async (type = 'attraction') => {
  const response = await apiClient.get('/recommendations/', { params: { type } });
  return response.data;
};
