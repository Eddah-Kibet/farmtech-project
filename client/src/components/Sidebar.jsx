import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { 
  Home, 
  ShoppingCart, 
  User, 
  LogOut, 
  Sun, 
  Moon,
  BarChart3,
  Package,
  PlusCircle,
  History
} from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ isOpen, onClose }) => {
  const { currentUser, logout } = useAuth();
  const { isDarkMode, toggleTheme } = useTheme();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    onClose();
  };

  if (!isOpen) return null;

  // Get profile picture with proper fallback
  const getProfilePicture = () => {
    const pic = currentUser?.profilePicture || currentUser?.profile_picture;
    
    // Check if it's a valid URL
    if (pic && pic !== 'null' && pic !== 'undefined' && pic.trim() !== '') {
      return pic;
    }
    
    return null;
  };

  const profilePicture = getProfilePicture();

  return (
    <div className={`sidebar-overlay ${isOpen ? 'open' : ''}`} onClick={onClose}>
      <div className={`sidebar ${isDarkMode ? 'dark' : ''}`} onClick={(e) => e.stopPropagation()}>
        {/* User Profile Section */}
        <div className="sidebar-user-section">
          <div className="sidebar-profile-pic">
            {profilePicture ? (
              <img 
                src={profilePicture}
                alt={currentUser?.name}
                style={{ 
                  width: '40px', 
                  height: '40px', 
                  borderRadius: '50%', 
                  objectFit: 'cover',
                  display: 'block'
                }}
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'flex';
                }}
              />
            ) : null}
            <div 
              className="sidebar-profile-placeholder"
              style={{ display: profilePicture ? 'none' : 'flex' }}
            >
              {currentUser?.name?.charAt(0).toUpperCase()}
            </div>
          </div>
          <div className="sidebar-user-info">
            <div className="sidebar-user-name">{currentUser?.name}</div>
            <div className="sidebar-user-role">{currentUser?.role}</div>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="sidebar-nav">
          <Link 
            to="/marketplace" 
            className={`sidebar-link ${location.pathname === '/marketplace' ? 'active' : ''}`}
            onClick={onClose}
          >
            <Home size={18} />
            <span>Marketplace</span>
          </Link>

          <Link 
            to="/dashboard" 
            className={`sidebar-link ${location.pathname === '/dashboard' ? 'active' : ''}`}
            onClick={onClose}
          >
            <BarChart3 size={18} />
            <span>Dashboard</span>
          </Link>

          {/* Farmer-specific links */}
          {currentUser?.role === 'farmer' && (
            <>
              <Link 
                to="/add-product" 
                className={`sidebar-link ${location.pathname === '/add-product' ? 'active' : ''}`}
                onClick={onClose}
              >
                <PlusCircle size={18} />
                <span>Add Product</span>
              </Link>

              <Link 
                to="/my-products" 
                className={`sidebar-link ${location.pathname === '/my-products' ? 'active' : ''}`}
                onClick={onClose}
              >
                <Package size={18} />
                <span>My Products</span>
              </Link>

              <Link 
                to="/messages" 
                className={`sidebar-link ${location.pathname === '/messages' ? 'active' : ''}`}
                onClick={onClose}
              >
                <History size={18} />
                <span>Messages</span>
              </Link>
            </>
          )}

          {/* Buyer-specific links */}
          {currentUser?.role === 'buyer' && (
            <>
              <Link 
                to="/orders" 
                className={`sidebar-link ${location.pathname === '/orders' ? 'active' : ''}`}
                onClick={onClose}
              >
                <ShoppingCart size={18} />
                <span>My Orders</span>
              </Link>

              <Link 
                to="/messages" 
                className={`sidebar-link ${location.pathname === '/messages' ? 'active' : ''}`}
                onClick={onClose}
              >
                <History size={18} />
                <span>Messages</span>
              </Link>

              <Link 
                to="/order-history" 
                className={`sidebar-link ${location.pathname === '/order-history' ? 'active' : ''}`}
                onClick={onClose}
              >
                <History size={18} />
                <span>Order History</span>
              </Link>
            </>
          )}

          <Link 
            to="/profile" 
            className={`sidebar-link ${location.pathname === '/profile' ? 'active' : ''}`}
            onClick={onClose}
          >
            <User size={18} />
            <span>Profile</span>
          </Link>
        </nav>

        {/* Bottom Actions */}
        <div className="sidebar-actions">
          <button 
            className="sidebar-action-btn"
            onClick={toggleTheme}
          >
            {isDarkMode ? <Sun size={18} /> : <Moon size={18} />}
            <span>{isDarkMode ? 'Light Mode' : 'Dark Mode'}</span>
          </button>

          <button 
            className="sidebar-action-btn logout-btn"
            onClick={handleLogout}
          >
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;