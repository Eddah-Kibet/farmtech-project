import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ChatBox from '../components/ChatBox';
import axios from 'axios';
import './ChatPage.css';

const ChatPage = () => {
  const { userId } = useParams();
  const navigate = useNavigate();
  const { currentUser } = useAuth();
  const [otherUser, setOtherUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchUserDetails = React.useCallback(async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/products', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      const userProduct = response.data.find(product => product.farmer_id === parseInt(userId));

      if (userProduct) {
        setOtherUser({
          id: parseInt(userId),
          name: userProduct.farmer || 'Unknown Farmer'
        });
      } else {
        setOtherUser({
          id: parseInt(userId),
          name: 'User'
        });
      }
    } catch (error) {
      console.error('Error fetching user details:', error);
      setError('Failed to load user details');
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    if (!currentUser) {
      navigate('/login');
      return;
    }

    if (parseInt(userId) === currentUser.id) {
      setError('You cannot chat with yourself');
      setLoading(false);
      return;
    }}
