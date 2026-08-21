import apiClient from '../api/client';

export const performSearch = async (query) => {
  const response = await apiClient.get('/search/', { params: { q: query } });
  return response.data;
};
