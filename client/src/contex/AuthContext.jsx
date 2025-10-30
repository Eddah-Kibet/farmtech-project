import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const value = {
    currentUser,
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
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      const user = JSON.parse(savedUser);
      setCurrentUser(user);
    }
    setLoading(false);
  }, []);

  const value = {
    currentUser,
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
const register = async (userData) => {
  try {
    const response = await axios.post('/register', userData);
    const user = response.data.user;
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
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
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
  setCurrentUser(null);
};
const updateUser = (updatedUser) => {
  setCurrentUser(updatedUser);
  localStorage.setItem('user', JSON.stringify(updatedUser));
};
import axios from 'axios'; 

// Add to AuthProvider component:
useEffect(() => {
  axios.defaults.baseURL = 'http://localhost:5000';
}, []);

useEffect(() => {
  const token = localStorage.getItem('token');
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }
}, []);
// Add this inside the existing useEffect for loading user
useEffect(() => {
  const token = localStorage.getItem('token');
  const savedUser = localStorage.getItem('user');
  if (savedUser) {
    const user = JSON.parse(savedUser);
    // Standardize profile picture field
    if (user.profile_picture && !user.profilePicture) {
      user.profilePicture = user.profile_picture;
    }
    setCurrentUser(user);
  }
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }
  setLoading(false);
}, []);
const register = async (userData) => {
  try {
    const response = await axios.post('/register', userData);
    const user = response.data.user;
    // Standardize profile picture field
    if (user.profile_picture && !user.profilePicture) {
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
    // Standardize profile picture field
    if (user.profile_picture && !user.profilePicture) {
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

const updateUser = (updatedUser) => {
  // Standardize profile picture field
  const user = { ...updatedUser };
  if (user.profile_picture && !user.profilePicture) {
    user.profilePicture = user.profile_picture;
  }
  setCurrentUser(user);
  localStorage.setItem('user', JSON.stringify(user));
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