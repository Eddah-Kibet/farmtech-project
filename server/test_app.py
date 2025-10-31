import pytest
import json
import tempfile
import os
from app import app, db
from models import User, Product, Order, Rating, Message

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

@pytest.fixture
def farmer_token(client):
    """Create a farmer user and return auth token"""
    response = client.post('/register', 
        data=json.dumps({
            'name': 'Test Farmer',
            'email': 'farmer@test.com',
            'password': 'password123',
            'role': 'farmer'
        }),
        content_type='application/json'
    )
    return json.loads(response.data)['token']

@pytest.fixture
def buyer_token(client):
    """Create a buyer user and return auth token"""
    response = client.post('/register',
        data=json.dumps({
            'name': 'Test Buyer',
            'email': 'buyer@test.com',
            'password': 'password123',
            'role': 'buyer'
        }),
        content_type='application/json'
    )
    return json.loads(response.data)['token']

class TestAuth:
    def test_register_success(self, client):
        response = client.post('/register',
            data=json.dumps({
                'name': 'John Doe',
                'email': 'john@test.com',
                'password': 'password123',
                'role': 'farmer'
            }),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'token' in data
        assert data['user']['email'] == 'john@test.com'

    def test_register_duplicate_email(self, client):
        # First registration
        client.post('/register',
            data=json.dumps({
                'name': 'John Doe',
                'email': 'john@test.com',
                'password': 'password123',
                'role': 'farmer'
            }),
            content_type='application/json'
        )
        
        # Duplicate registration
        response = client.post('/register',
            data=json.dumps({
                'name': 'Jane Doe',
                'email': 'john@test.com',
                'password': 'password456',
                'role': 'buyer'
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'Email already exists' in json.loads(response.data)['message']

    def test_login_success(self, client):
        # Register user first
        client.post('/register',
            data=json.dumps({
                'name': 'John Doe',
                'email': 'john@test.com',
                'password': 'password123',
                'role': 'farmer'
            }),
            content_type='application/json'
        )
        
        # Login
        response = client.post('/login',
            data=json.dumps({
                'email': 'john@test.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data

    def test_login_invalid_credentials(self, client):
        response = client.post('/login',
            data=json.dumps({
                'email': 'nonexistent@test.com',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        assert response.status_code == 401

class TestProducts:
    def test_get_products_empty(self, client):
        response = client.get('/products')
        assert response.status_code == 200
        assert json.loads(response.data) == []

    def test_create_product_success(self, client, farmer_token):
        response = client.post('/products',
            data=json.dumps({
                'name': 'Fresh Tomatoes',
                'price': 5.99,
                'category': 'Vegetables',
                'stock': 100,
                'description': 'Fresh organic tomatoes'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Fresh Tomatoes'
        assert data['price'] == 5.99

    def test_create_product_buyer_forbidden(self, client, buyer_token):
        response = client.post('/products',
            data=json.dumps({
                'name': 'Fresh Tomatoes',
                'price': 5.99,
                'category': 'Vegetables',
                'stock': 100
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {buyer_token}'}
        )
        assert response.status_code == 403

    def test_get_product_by_id(self, client, farmer_token):
        # Create product first
        create_response = client.post('/products',
            data=json.dumps({
                'name': 'Fresh Carrots',
                'price': 3.99,
                'category': 'Vegetables',
                'stock': 50
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        product_id = json.loads(create_response.data)['id']
        
        # Get product
        response = client.get(f'/products/{product_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Fresh Carrots'

    def test_update_product(self, client, farmer_token):
        # Create product first
        create_response = client.post('/products',
            data=json.dumps({
                'name': 'Fresh Carrots',
                'price': 3.99,
                'category': 'Vegetables',
                'stock': 50
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        product_id = json.loads(create_response.data)['id']
        
        # Update product
        response = client.put(f'/products/{product_id}',
            data=json.dumps({
                'name': 'Premium Carrots',
                'price': 4.99
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Premium Carrots'
        assert data['price'] == 4.99

    def test_delete_product(self, client, farmer_token):
        # Create product first
        create_response = client.post('/products',
            data=json.dumps({
                'name': 'Fresh Carrots',
                'price': 3.99,
                'category': 'Vegetables',
                'stock': 50
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        product_id = json.loads(create_response.data)['id']
        
        # Delete product
        response = client.delete(f'/products/{product_id}',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        assert response.status_code == 200

class TestOrders:
    def test_create_order_success(self, client, farmer_token, buyer_token):
        # Create product first
        product_response = client.post('/products',
            data=json.dumps({
                'name': 'Fresh Apples',
                'price': 2.99,
                'category': 'Fruits',
                'stock': 100
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        product_id = json.loads(product_response.data)['id']
        
        # Create order
        response = client.post('/orders',
            data=json.dumps({
                'products': [{'id': product_id, 'quantity': 5}]
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {buyer_token}'}
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['total_amount'] == 14.95  # 2.99 * 5

    def test_create_order_insufficient_stock(self, client, farmer_token, buyer_token):
        # Create product with limited stock
        product_response = client.post('/products',
            data=json.dumps({
                'name': 'Limited Apples',
                'price': 2.99,
                'category': 'Fruits',
                'stock': 3
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        product_id = json.loads(product_response.data)['id']
        
        # Try to order more than available
        response = client.post('/orders',
            data=json.dumps({
                'products': [{'id': product_id, 'quantity': 5}]
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {buyer_token}'}
        )
        assert response.status_code == 400
        assert 'Insufficient stock' in json.loads(response.data)['message']

    def test_farmer_cannot_create_order(self, client, farmer_token):
        response = client.post('/orders',
            data=json.dumps({
                'products': [{'id': 1, 'quantity': 1}]
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        assert response.status_code == 403

class TestRatings:
    def test_create_rating_success(self, client, farmer_token, buyer_token):
        # Create product
        product_response = client.post('/products',
            data=json.dumps({
                'name': 'Test Product',
                'price': 5.00,
                'category': 'Fruits',
                'stock': 10
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        product_data = json.loads(product_response.data)
        
        # Create order
        client.post('/orders',
            data=json.dumps({
                'products': [{'id': product_data['id'], 'quantity': 1}]
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {buyer_token}'}
        )
        
        # Create rating
        response = client.post('/ratings',
            data=json.dumps({
                'farmer_id': product_data['farmer_id'],
                'product_id': product_data['id'],
                'score': 8,
                'comment': 'Great product!'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {buyer_token}'}
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['score'] == 8

class TestMessages:
    def test_send_message_success(self, client, farmer_token, buyer_token):
        # Get farmer ID
        farmer_response = client.get('/me',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        farmer_id = json.loads(farmer_response.data)['id']
        
        # Send message from buyer to farmer
        response = client.post('/messages',
            data=json.dumps({
                'receiver_id': farmer_id,
                'content': 'Hello, I am interested in your products!'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {buyer_token}'}
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['content'] == 'Hello, I am interested in your products!'

    def test_get_messages(self, client, farmer_token, buyer_token):
        # Get user IDs
        farmer_response = client.get('/me',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        farmer_id = json.loads(farmer_response.data)['id']
        
        buyer_response = client.get('/me',
            headers={'Authorization': f'Bearer {buyer_token}'}
        )
        buyer_id = json.loads(buyer_response.data)['id']
        
        # Send message
        client.post('/messages',
            data=json.dumps({
                'receiver_id': farmer_id,
                'content': 'Test message'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {buyer_token}'}
        )
        
        # Get messages
        response = client.get(f'/messages/{farmer_id}',
            headers={'Authorization': f'Bearer {buyer_token}'}
        )
        assert response.status_code == 200
        messages = json.loads(response.data)
        assert len(messages) == 1
        assert messages[0]['content'] == 'Test message'

class TestLeaderboard:
    def test_get_leaderboard_empty(self, client):
        response = client.get('/leaderboard')
        assert response.status_code == 200
        assert json.loads(response.data) == []

class TestProfile:
    def test_get_profile(self, client, farmer_token):
        response = client.get('/users/profile',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['email'] == 'farmer@test.com'

    def test_update_profile(self, client, farmer_token):
        response = client.put('/users/profile',
            data=json.dumps({
                'name': 'Updated Farmer Name'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {farmer_token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Updated Farmer Name'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])