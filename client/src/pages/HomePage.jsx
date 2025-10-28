import React from 'react';
import { Link } from 'react-router-dom';
// import { useAuth } from '../context/AuthContext';
import './HomePage.css';

const  HomePage = () => {
//   const { user } = useAuth();
//   const navigate = useNavigate();

//   // Redirect logged-in users to marketplace
//   React.useEffect(() => {
//     if (user) {
//       navigate('/marketplace');
//     }
//   }, [user, navigate]);

//   if (user) {
//     return null; // Will redirect
//   }

  return (
    <div className="homepage">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>Fresh Farm Produce, Direct to You</h1>
          <p>Connect with local farmers and enjoy the freshest produce delivered straight from the farm to your doorstep.</p>
          <div className="hero-buttons">
            <Link to="/register" className="btn btn-primary">Get Started</Link>
            <Link to="/login" className="btn btn-secondary">Sign In</Link>
          </div>
        </div>
        <div className="hero-stats">
          <div className="stat">
            <h3>1,234+</h3>
            <p>Farmers</p>
          </div>
          <div className="stat">
            <h3>5,678+</h3>
            <p>Buyers</p>
          </div>
          <div className="stat">
            <h3>10,000+</h3>
            <p>Products Sold</p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <h2>Why Choose Our Marketplace?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🌱</div>
            <h3>Fresh & Local</h3>
            <p>Get the freshest produce from local farmers in your area.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🤝</div>
            <h3>Support Farmers</h3>
            <p>Directly support local farmers and sustainable agriculture.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🛒</div>
            <h3>Easy Shopping</h3>
            <p>Browse, order, and get delivered with just a few clicks.</p>
          </div>
        </div>
      </section>

      {/* For Farmers Section */}
      <section className="for-farmers">
        <h2>For Farmers</h2>
        <div className="farmers-content">
          <div className="farmers-text">
            <p>Join our platform to reach more customers and sell your produce directly.</p>
            <ul>
              <li>📝 List Your Products Easily</li>
              <li>📊 Manage Orders and Inventory</li>
              <li>💰 Get Paid Directly</li>
              <li>🌍 Reach Local and Regional Buyers</li>
            </ul>
          </div>
          <div className="farmers-image">
            <img src="https://plus.unsplash.com/premium_photo-1678344151150-4a42c45453d5?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1287" 
                alt="Happy farmer" />
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;