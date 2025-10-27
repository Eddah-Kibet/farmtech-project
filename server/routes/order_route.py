from flask import Blueprint, jsonify, request, abort
from models import Order
from extensions import db
from datetime import datetime

order_bp = Blueprint('order_bp', __name__, url_prefix='/orders')


@order_bp.route('/', methods=['GET'])
def get_orders():
    """Fetch all orders"""
    orders = Order.query.all()
    return jsonify({
        "success": True,
        "count": len(orders),
        "data": [order.to_dict() for order in orders]
    }), 200


@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Fetch a specific order by its ID"""
    order = Order.query.get(order_id)
    if not order:
        abort(404, description="Order not found")

    return jsonify({
        "success": True,
        "data": order.to_dict()
    }), 200


@order_bp.route('/', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.get_json()

    # Basic validation
    required_fields = ['product_id', 'buyer_id', 'quantity']
    if not all(field in data for field in required_fields):
        return jsonify({
            "success": False,
            "message": "Missing required fields: product_id, buyer_id, quantity"
        }), 400

    new_order = Order(
        product_id=data['product_id'],
        buyer_id=data['buyer_id'],
        quantity=data['quantity'],
        status=data.get('status', 'pending'),
        created_at=datetime.utcnow()
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Order created successfully",
        "data": new_order.to_dict()
    }), 201


@order_bp.route('/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    """Update an order's status or quantity"""
    order = Order.query.get(order_id)
    if not order:
        abort(404, description="Order not found")

    data = request.get_json()

    # Optional updates
    if 'status' in data:
        order.status = data['status']
    if 'quantity' in data:
        order.quantity = data['quantity']

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Order updated successfully",
        "data": order.to_dict()
    }), 200


@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an order by its ID"""
    order = Order.query.get(order_id)
    if not order:
        abort(404, description="Order not found")

    db.session.delete(order)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Order {order_id} deleted successfully"
    }), 200


# Optional: Custom error handlers
@order_bp.errorhandler(404)
def not_found_error(e):
    return jsonify({"success": False, "error": 404, "message": str(e)}), 404


@order_bp.errorhandler(400)
def bad_request_error(e):
    return jsonify({"success": False, "error": 400, "message": str(e)}), 400
