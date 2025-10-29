import React, { useState } from "react";
import CartItem from "../components/CartItem";
import CartSummary from "../components/CartSummary";

function Cart() {
  // Example cart data (you’ll replace this with fetched data later)
  const [cartItems, setCartItems] = useState([
    { id: 1, name: "Fresh Tomatoes", price: 3.5, quantity: 2 },
    { id: 2, name: "Organic Avocados", price: 2.0, quantity: 4 },
  ]);

  // Update quantity handler
  const updateQuantity = (id, newQuantity) => {
    setCartItems((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, quantity: newQuantity } : item
      )
    );
  }}