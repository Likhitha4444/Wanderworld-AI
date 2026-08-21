import apiClient from '../api/client';

export const getTrips = async () => {
  const response = await apiClient.get('/trips/');
  return response.data;
};

export const createTrip = async (data) => {
  const response = await apiClient.post('/trips/', data);
  return response.data;
};

export const getTripDetail = async (id) => {
  const response = await apiClient.get(`/trips/${id}/`);
  return response.data;
};

export const generateItinerary = async (id, preferences = {}) => {
  const response = await apiClient.post(`/trips/${id}/generate/`, { preferences });
  return response.data;
};
