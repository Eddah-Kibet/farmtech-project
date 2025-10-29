import React from "react";

function CartItem({ item, onRemove }) {
  

  return (
    <div className="cart-item">
      <h3>{item.name}</h3>
      <p>Price: Ksh {item.price}</p>
      <p>Quantity: {item.quantity}</p>
      <p>Total: Ksh {item.price * item.quantity}</p>

      <button
        onClick={() => onRemove(item.id)}
        style={{
          backgroundColor: "red",
          color: "white",
          border: "none",
          padding: "6px 10px",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        Remove
      </button>
    </div>
  );
}

export default CartItem;
