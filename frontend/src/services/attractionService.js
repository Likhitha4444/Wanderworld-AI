import apiClient from '../api/client';

export const getAttractions = async (params = {}) => {
  const response = await apiClient.get('/attractions/', { params });
  return response.data;
};

export const getAttractionDetail = async (slug) => {
  const response = await apiClient.get(`/attractions/${slug}/`);
  return response.data;
};

export const getNearbyAttractions = async (params) => {
  const response = await apiClient.get('/attractions/nearby/', { params });
  return response.data;
};
