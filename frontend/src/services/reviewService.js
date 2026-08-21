import apiClient from '../api/client';

export const getReviews = async (params = {}) => {
  const response = await apiClient.get('/reviews/', { params });
  return response.data;
};

export const createReview = async (data) => {
  const response = await apiClient.post('/reviews/', data);
  return response.data;
};

export const getEntityReviews = async (entityType, slug) => {
  const response = await apiClient.get(`/${entityType}s/${slug}/reviews/`);
  return response.data;
};
