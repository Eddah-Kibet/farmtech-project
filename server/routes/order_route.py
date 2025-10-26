from flask import Blueprint, jsonify, request
from models import Order  
from extensions import db


order_bp = Blueprint('order_bp', __name__, url_prefix='/orders')


@order_bp.route('/', methods=['GET'])
def get_orders():
    """Fetch all orders from the database"""
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders]), 200


@order_bp.route('/<int:id>', methods=['GET'])
def get_order(id):
    """Fetch a specific order by its ID"""
    order = Order.query.get_or_404(id)
    return jsonify(order.to_dict()), 200


@order_bp.route('/', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.get_json()
    new_order = Order(
        product_id=data.get('product_id'),
        buyer_id=data.get('buyer_id'),
        quantity=data.get('quantity'),
        status='pending'
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201


@order_bp.route('/<int:id>', methods=['PATCH'])
def update_order(id):
    """Update an order's status or quantity"""
    order = Order.query.get_or_404(id)
    data = request.get_json()

    if 'status' in data:
        order.status = data['status']
    if 'quantity' in data:
        order.quantity = data['quantity']

    db.session.commit()
    return jsonify(order.to_dict()), 200


@order_bp.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    """Delete an order by its ID"""
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 200
