import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { useTheme } from '../context/ThemeContext';
import { Menu, ShoppingCart, Leaf } from 'lucide-react';
import Cart from './Cart';
import Sidebar from './Sidebar';
import './Navigation.css';

const Navigation = () => {
  const { currentUser } = useAuth();
  const { cart } = useCart();
  const { isDarkMode } = useTheme();
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const cartItemCount = cart.reduce((total, item) => total + item.quantity, 0);

  return (
    <nav className={`sticky top-0 z-40 bg-gradient-to-r from-green-600 via-green-500 to-emerald-500 shadow-lg border-b-2 ${isDarkMode ? 'dark:from-gray-800 dark:via-gray-900 dark:to-gray-800 dark:border-gray-600' : 'border-green-400'}`}>
      <div className="max-w-7xl mx-auto flex justify-between items-center px-6 py-4">
        {/* Menu Button for Sidebar */}
        <button 
          className="p-3 rounded-xl text-white hover:bg-white/20 dark:text-gray-200 dark:hover:bg-gray-700/50 transition-all duration-300 hover:scale-110 backdrop-blur-sm"
          onClick={() => setIsSidebarOpen(true)}
          aria-label="Open menu"
        >
          <Menu size={24} />
        </button>

        {/* Logo */}
        <Link to={currentUser ? "/marketplace" : "/"} className="flex items-center gap-3 text-white font-bold text-2xl hover:text-green-100 transition-all duration-300 hover:scale-105">
          <div className="p-2 bg-white/20 rounded-full backdrop-blur-sm">
            <Leaf size={32} className="text-white" />
          </div>
          <span className="hidden sm:block drop-shadow-md">Farm Marketplace</span>
        </Link>
        
        {/* Cart Button (for buyers) */}
        {currentUser?.role === 'buyer' && (
          <button 
            className="relative p-3 rounded-xl text-white hover:bg-white/20 dark:text-gray-200 dark:hover:bg-gray-700/50 transition-all duration-300 hover:scale-110 backdrop-blur-sm" 
            onClick={() => setIsCartOpen(true)}
            title="Shopping Cart"
          >
            <ShoppingCart size={24} />
            {cartItemCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold shadow-lg animate-pulse">{cartItemCount}</span>
            )}
          </button>
        )}
      </div>
      
      {/* Sidebar */}
      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
      
      {/* Cart Modal */}
      <Cart isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
    </nav>
  );
};

export default Navigation;