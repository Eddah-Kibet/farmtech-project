import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import './FarmerProfile.css';

const FarmerProfile = () => {
  const { farmerId } = useParams();
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const [farmerData, setFarmerData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFarmerProfile = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/users/farmer/${farmerId}`);
        setFarmerData(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load farmer profile');
        setLoading(false);
      }
    };

    fetchFarmerProfile();
  }, [farmerId]);

  const handleMessageFarmer = () => {
    if (currentUser && currentUser.role === 'buyer') {
      navigate(`/chat/${farmerId}`);
    }
  };

  if (loading) {
    return (
      <div className="farmer-profile">
        <div className="loading">Loading farmer profile...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="farmer-profile">
        <div className="error">{error}</div>
      </div>
    );
  }
