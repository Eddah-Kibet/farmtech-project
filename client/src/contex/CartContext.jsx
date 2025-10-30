import React, { createContext, useState, useContext } from 'react';

const CartContext = createContext();

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);

  return (
    <CartContext.Provider value={{ cart }}>
      {children}
    </CartContext.Provider>
  );
};
export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(() => {
    try {
      const saved = localStorage.getItem('cart');
      return saved ? JSON.parse(saved) : [];
    } catch (error) {
      console.error('Error loading cart from localStorage:', error);
      return [];
    }
  });

  return (
    <CartContext.Provider value={{ cart }}>
      {children}
    </CartContext.Provider>
  );
};
export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(() => {
    try {
      const saved = localStorage.getItem('cart');
      return saved ? JSON.parse(saved) : [];
    } catch (error) {
      console.error('Error loading cart from localStorage:', error);
      return [];
    }
  });

  const addToCart = (product) => {
    if (!product || !product.id) {
      console.error('Invalid product provided to addToCart');
      return;
    }
    
    const newCart = cart.slice();
    const existing = newCart.find(item => item.id === product.id);
    const price = typeof product.price === 'string' ? parseFloat(product.price) : product.price;
    
    if (existing) {
      existing.quantity += 1;
    } else {
      newCart.push({ ...product, price, quantity: 1 });
    }
    
    setCart(newCart);
    localStorage.setItem('cart', JSON.stringify(newCart));
  };

  return (
    <CartContext.Provider value={{ cart, addToCart }}>
      {children}
    </CartContext.Provider>
  );
};