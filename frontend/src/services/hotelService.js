import apiClient from '../api/client';

export const getHotels = async (params = {}) => {
  const response = await apiClient.get('/hotels/', { params });
  return response.data;
};

export const getHotelDetail = async (slug) => {
  const response = await apiClient.get(`/hotels/${slug}/`);
  return response.data;
};
