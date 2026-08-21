import apiClient from '../api/client';

export const getDestinations = async (params = {}) => {
  const response = await apiClient.get('/destinations/', { params });
  return response.data;
};

export const getDestinationDetail = async (slug) => {
  const response = await apiClient.get(`/destinations/${slug}/`);
  return response.data;
};
