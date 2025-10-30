import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Configure axios base URL once
    axios.defaults.baseURL = 'http://localhost:5000';

    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');

    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }

    if (savedUser) {
      try {
        const user = JSON.parse(savedUser);
        // Standardize profile picture field name coming from different backends
        if (user.profile_picture && !user.profilePicture) {
          user.profilePicture = user.profile_picture;
        }
        setCurrentUser(user);
      } catch (e) {
        console.error('Failed to parse saved user from localStorage', e);
        localStorage.removeItem('user');
      }
    }

    setLoading(false);
  }, []);

  const register = async (userData) => {
    try {
      const response = await axios.post('/register', userData);
      const user = response.data.user;
      if (user && user.profile_picture && !user.profilePicture) {
        user.profilePicture = user.profile_picture;
      }
      return { success: true, user };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || 'Registration failed'
      };
    }
  };

  const login = async (credentials) => {
    try {
      const response = await axios.post('/login', credentials);
      const { token, user } = response.data;
      if (user && user.profile_picture && !user.profilePicture) {
        user.profilePicture = user.profile_picture;
      }
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      setCurrentUser(user);
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
    const user = { ...updatedUser };
    if (user.profile_picture && !user.profilePicture) {
      user.profilePicture = user.profile_picture;
    }
    setCurrentUser(user);
    localStorage.setItem('user', JSON.stringify(user));
  };

  const value = {
    currentUser,
    loading,
    register,
    login,
    logout,
    updateUser
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