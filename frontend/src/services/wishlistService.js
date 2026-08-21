import apiClient from '../api/client';

export const getWishlist = async () => {
  const response = await apiClient.get('/wishlist/');
  return response.data;
};

export const addToWishlist = async (data) => {
  const response = await apiClient.post('/wishlist/', data);
  return response.data;
};

export const removeFromWishlist = async (id) => {
  const response = await apiClient.delete(`/wishlist/${id}/`);
  return response.data;
};

export const checkWishlistStatus = async (params) => {
  const response = await apiClient.get('/wishlist/check/', { params });
  return response.data;
};
