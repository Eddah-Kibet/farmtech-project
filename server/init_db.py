from app import app, db

def init_database():
    with app.app_context():
        print("🗑️  Dropping existing tables...")
        db.drop_all()
        
        print("🔄 Creating new tables...")
        db.create_all()
        
        print("✅ Database initialized successfully!")
        print("📊 Tables created: users, products, orders, ratings, order_product")

if __name__ == '__main__':
    init_database()