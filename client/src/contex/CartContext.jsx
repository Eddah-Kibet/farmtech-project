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

  const removeFromCart = (id) => {
    if (!id) {
      console.error('Invalid id provided to removeFromCart');
      return;
    }
    const newCart = cart.filter(item => item.id !== id);
    setCart(newCart);
    localStorage.setItem('cart', JSON.stringify(newCart));
  };

  const updateQuantity = (id, quantity) => {
    if (!id) {
      console.error('Invalid id provided to updateQuantity');
      return;
    }
    if (quantity <= 0) {
      removeFromCart(id);
      return;
    }
    const newCart = cart.map(item =>
      item.id === id ? { ...item, quantity: Math.max(0, quantity) } : item
    );
    setCart(newCart);
    localStorage.setItem('cart', JSON.stringify(newCart));
  };

  const clearCart = () => {
    setCart([]);
    localStorage.removeItem('cart');
  };

  const getTotalPrice = () => {
    return cart.reduce((sum, item) => {
      const price = item.price || 0;
      const quantity = item.quantity || 0;
      return sum + (price * quantity);
    }, 0);
  };

  return (
    <CartContext.Provider value={{
      cart,
      addToCart,
      removeFromCart,
      updateQuantity,
      clearCart,
      getTotalPrice
    }}>
      {children}
    </CartContext.Provider>
  );
};