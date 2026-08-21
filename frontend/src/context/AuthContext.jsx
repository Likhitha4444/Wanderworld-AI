import { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../api/client';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access');
      if (token) {
        try {
          const response = await apiClient.get('/auth/me/');
          setUser(response.data.data);
        } catch (error) {
          localStorage.removeItem('access');
          localStorage.removeItem('refresh');
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  const login = async (credentials) => {
    const response = await apiClient.post('/auth/login/', credentials);
    const { access, refresh, user } = response.data.data;
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);
    setUser(user);
    return user;
  };

  const register = async (userData) => {
    const response = await apiClient.post('/auth/register/', userData);
    return response.data;
  };

  const logout = async () => {
    try {
        const refresh = localStorage.getItem('refresh');
        await apiClient.post('/auth/logout/', { refresh });
    } catch (error) {
        console.error('Logout failed', error);
    } finally {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, setUser, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
