from flask import Blueprint, request, jsonify
from app import db
from models import Product

products_bp = Blueprint('products', __name__)

# GET ALL PRODUCTS
@products_bp.route('', methods=['GET'])
def get_products():
    products = Product.query.all()
    
    product_list = []
    for product in products:
        product_list.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity_available,
            'farm_name': product.farmer.farm_name
        })
    
    return jsonify({'products': product_list})

# GET ONE PRODUCT
@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity_available,
        'description': product.description,
        'farm_name': product.farmer.farm_name,
        'farmer_contact': product.farmer.contact_person
    })

# CREATE PRODUCT
@products_bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    
    new_product = Product(
        name=data['name'],
        price=data['price'],
        quantity_available=data['quantity'],
        description=data.get('description', ''),
        farmer_id=data['farmer_id']
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({'message': 'Product created!', 'id': new_product.id})

# UPDATE PRODUCT
@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    data = request.get_json()
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'quantity' in data:
        product.quantity_available = data['quantity']
    if 'description' in data:
        product.description = data['description']
    
    db.session.commit()
    
    return jsonify({'message': 'Product updated!'})

# DELETE PRODUCT
@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted!'})