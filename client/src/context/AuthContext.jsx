import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Configure axios base URL for development
    axios.defaults.baseURL = import.meta.env.DEV ? '/api' : 'http://localhost:5000';
  }, []);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');

    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }

    if (savedUser) {
      try {
        const user = JSON.parse(savedUser);
        // NORMALIZE PROFILE PICTURE - Always use profilePicture in frontend
        const normalizedUser = {
          ...user,
          profilePicture: user.profile_picture || user.profilePicture || null
        };
        setCurrentUser(normalizedUser);
      } catch (e) {
        console.error('Failed to parse saved user from localStorage', e);
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  const register = async (userData) => {
    try {
      console.log('Attempting registration with:', userData);
      const response = await axios.post('/register', userData);
      console.log('Registration response:', response.data);

      // Don't automatically log in after registration
      // Just return success and let the user login manually
      return { success: true };
    } catch (error) {
      console.error('Registration error:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Registration failed'
      };
    }
  };

  const login = async ({ email, password }) => {
    try {
      const response = await axios.post('/login', { email, password });
      const { token, user } = response.data;
      
      // NORMALIZE PROFILE PICTURE - Always use profilePicture in frontend
      const normalizedUser = {
        ...user,
        profilePicture: user.profile_picture || user.profilePicture || null
      };
      
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(normalizedUser));
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      setCurrentUser(normalizedUser);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || 'Login failed'
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
    setCurrentUser(null);
  };

  const updateUser = (updatedUser) => {
    // NORMALIZE PROFILE PICTURE - Always use profilePicture in frontend
    const normalizedUser = {
      ...updatedUser,
      profilePicture: updatedUser.profile_picture || updatedUser.profilePicture || null
    };
    setCurrentUser(normalizedUser);
    localStorage.setItem('user', JSON.stringify(normalizedUser));
  };

  const value = {
    currentUser,
    register,
    login,
    logout,
    updateUser,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}