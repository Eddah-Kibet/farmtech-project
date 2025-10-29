import React, { useState } from "react";
import CartItem from "../components/CartItem";
import CartSummary from "../components/CartSummary";

function Cart() {
  
  const [cartItems, setCartItems] = useState([
    { id: 1, name: "Fresh Tomatoes", price: 3.5, quantity: 2 },
    { id: 2, name: "Organic Avocados", price: 2.0, quantity: 4 },
  ]);

  
  const updateQuantity = (id, newQuantity) => {
    setCartItems((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  return (
    <div className="cart-page">
      <h2>Your Shopping Cart</h2>
      <div className="cart-container">
        <div className="cart-items">
          {cartItems.map((item) => (
            <CartItem key={item.id} item={item} updateQuantity={updateQuantity} />
          ))}
        </div>
        <CartSummary cartItems={cartItems} />
      </div>
    </div>
  );
}

export default Cart;
