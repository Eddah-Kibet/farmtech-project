import React from "react";

function CartSummary({ cartItems }) {
  
  const subtotal = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  
  const deliveryFee = subtotal > 0 ? 5.99 : 0;

  
  const tax = subtotal * 0.1;

  
  const grandTotal = subtotal + deliveryFee + tax;

  return (
    <div className="cart-summary">
      <h2>Order Summary</h2>

      <div className="summary-row">
        <span>Subtotal:</span>
        <span>${subtotal.toFixed(2)}</span>
      </div>

      <div className="summary-row">
        <span>Delivery Fee:</span>
        <span>${deliveryFee.toFixed(2)}</span>
      </div>

      <div className="summary-row">
        <span>Tax (10%):</span>
        <span>${tax.toFixed(2)}</span>
      </div>

      <hr />

      <div className="summary-row total">
        <strong>Total:</strong>
        <strong>${grandTotal.toFixed(2)}</strong>
      </div>

      <button className="checkout-btn">Proceed to Checkout</button>
    </div>
  );
}

export default CartSummary;
