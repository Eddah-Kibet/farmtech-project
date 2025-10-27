from flask import Blueprint, jsonify, request, abort
from models import Review, Product, Buyer
from extensions import db
from datetime import datetime

review_bp = Blueprint('review_bp', __name__, url_prefix='/reviews')

@review_bp.route('/', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify({
        "success": True,
        "count": len(reviews),
        "data": [r.to_dict() for r in reviews]
    }), 200


@review_bp.route('/product/<int:product_id>', methods=['GET'])
def get_reviews_by_product(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify({
        "success": True,
        "product_id": product_id,
        "count": len(reviews),
        "data": [r.to_dict() for r in reviews]
    }), 200


@review_bp.route('/', methods=['POST'])
def create_review():
    data = request.get_json()

    # Validation
    required_fields = ['product_id', 'buyer_id', 'rating', 'comment']
    if not all(field in data for field in required_fields):
        return jsonify({
            "success": False,
            "message": f"Missing fields. Required: {', '.join(required_fields)}"
        }), 400

    if not (1 <= data['rating'] <= 5):
        return jsonify({
            "success": False,
            "message": "Rating must be between 1 and 5"
        }), 400

    review = Review(
        product_id=data['product_id'],
        buyer_id=data['buyer_id'],
        rating=data['rating'],
        comment=data['comment'],
        created_at=datetime.utcnow()
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Review created successfully",
        "data": review.to_dict()
    }), 201

@review_bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        abort(404, description="Review not found")

    db.session.delete(review)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Review {review_id} deleted successfully"
    }), 200
