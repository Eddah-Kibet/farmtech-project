from app import db, bcrypt
from sqlalchemy.orm import validates
from extensions import db, bcrypt
from datetime import datetime
import re

# Association table for many-to-many relationship between products and categories
product_categories = db.Table('product_categories',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'buyer' or 'farmer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    buyer_profile = db.relationship('Buyer', backref='user', uselist=False, cascade='all, delete-orphan')
    farmer_profile = db.relationship('Farmer', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError('Invalid email address')
        return email
    
    @validates('user_type')
    def validate_user_type(self, key, user_type):
        if user_type not in ['buyer', 'farmer']:
            raise ValueError('User type must be either buyer or farmer')
        return user_type

class Buyer(db.Model):
    __tablename__ = 'buyers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', backref='buyer', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='buyer', lazy=True, cascade='all, delete-orphan')
    
    @validates('phone')
    def validate_phone(self, key, phone):
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValueError('Invalid phone number format')
        return phone

class Farmer(db.Model):
    __tablename__ = 'farmers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farm_name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    certification = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='farmer', lazy=True, cascade='all, delete-orphan')
    
    @validates('phone')
    def validate_phone(self, key, phone):
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValueError('Invalid phone number format')
        return phone

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    subcategories = db.relationship('SubCategory', backref='category', lazy=True, cascade='all, delete-orphan')
    products = db.relationship('Product', secondary=product_categories, back_populates='categories')

class SubCategory(db.Model):
    __tablename__ = 'subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # kg, lb, piece, etc.
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'))
    is_organic = db.Column(db.Boolean, default=False)
    harvest_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    categories = db.relationship('Category', secondary=product_categories, back_populates='products')
    produce_details = db.relationship('ProduceDetail', backref='product', uselist=False, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')
    
    @validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError('Price must be greater than 0')
        return price
    
    @validates('quantity_available')
    def validate_quantity(self, key, quantity):
        if quantity < 0:
            raise ValueError('Quantity cannot be negative')
        return quantity

class ProduceDetail(db.Model):
    __tablename__ = 'produce_details'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    variety = db.Column(db.String(50))
    growing_method = db.Column(db.String(50))  # organic, conventional, hydroponic, etc.
    shelf_life = db.Column(db.Integer)  # in days
    storage_conditions = db.Column(db.String(100))
    nutritional_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @validates('rating')
    def validate_rating(self, key, rating):
        if not 1 <= rating <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return rating

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # credit_card, debit_card, mobile_money, etc.
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @validates('amount')
    def validate_amount(self, key, amount):
        if amount <= 0:
            raise ValueError('Amount must be greater than 0')
        return amount
    
    @validates('payment_method')
    def validate_payment_method(self, key, method):
        valid_methods = ["mpesa", "bank_transfer", "credit_card", "debit_card", "cash"]
        if method not in valid_methods:
            raise ValueError('Invalid payment method')
        return method