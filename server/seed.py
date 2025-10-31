# seed.py
from app import app, db
from models import User, Product, Order, Rating, order_product
from werkzeug.security import generate_password_hash
from datetime import datetime


def seed_database():
    with app.app_context():
        # -------------------------------------------------
        # 1. Reset DB
        # -------------------------------------------------
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()

        # -------------------------------------------------
        # 2. Users (real profile pictures)
        # -------------------------------------------------
        print("Creating users...")
        users = [
            User(
                name="Jesse Matara",
                email="jesse@example.com",
                password=generate_password_hash("password123"),
                role="farmer",
                phone_number="+254712345678",
                profile_picture="https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=300&h=300&dpr=1"
            ),
            User(
                name="Sarah Buyer",
                email="buyer@example.com",
                password=generate_password_hash("password123"),
                role="buyer",
                phone_number="+254798765432",
                profile_picture="https://images.pexels.com/photos/3763188/pexels-photo-3763188.jpeg?auto=compress&cs=tinysrgb&w=300&h=300&dpr=1"
            ),
            User(
                name="Green Valley Farm",
                email="greenvalley@example.com",
                password=generate_password_hash("password123"),
                role="farmer",
                phone_number="+254723456789",
                profile_picture="https://images.pexels.com/photos/264636/pexels-photo-264636.jpeg?auto=compress&cs=tinysrgb&w=300&h=300&dpr=1"
            ),
            User(
                name="Organic Harvest Co.",
                email="organicharvest@example.com",
                password=generate_password_hash("password123"),
                role="farmer",
                phone_number="+254734567890",
                profile_picture="https://images.pexels.com/photos/2097090/pexels-photo-2097090.jpeg?auto=compress&cs=tinysrgb&w=300&h=300&dpr=1"
            )
        ]
        for u in users:
            db.session.add(u)
        db.session.commit()

        # -------------------------------------------------
        # 3. Products – **real matching images**
        # -------------------------------------------------
        print("Creating products...")
        products = [
            # 1. Tomatoes
            Product(
                name="Organic Tomatoes",
                price=150.00,
                category="Vegetables",
                stock=50,
                description="Fresh, vine-ripened organic tomatoes grown without pesticides",
                image="https://images.pexels.com/photos/1327838/pexels-photo-1327838.jpeg?auto=compress&cs=tinysrgb&w=600",
                farmer_id=1
            ),
            # 2. Free-Range Eggs
            Product(
                name="Free-Range Eggs",
                price=450.00,
                category="Dairy",
                stock=24,
                description="Farm-fresh eggs from free-range chickens raised naturally",
                image="https://images.pexels.com/photos/1622913/pexels-photo-1622913.jpeg?auto=compress&cs=tinysrgb&w=600",
                farmer_id=1
            ),
            # 3. Pure Honey
            Product(
                name="Pure Honey",
                price=1200.00,
                category="Other",
                stock=15,
                description="Raw, unfiltered honey from local bee colonies",
                image="https://images.pexels.com/photos/4041392/pexels-photo-4041392.jpeg?auto=compress&cs=tinysrgb&w=600",
                farmer_id=3
            ),
            # 4. Fresh Apples
            Product(
                name="Fresh Apples",
                price=80.00,
                category="Fruits",
                stock=100,
                description="Crisp, juicy apples picked fresh from our orchard",
                image="https://images.pexels.com/photos/102104/pexels-photo-102104.jpeg?auto=compress&cs=tinysrgb&w=600",
                farmer_id=3
            ),
            # 5. Organic Carrots
            Product(
                name="Organic Carrots",
                price=60.00,
                category="Vegetables",
                stock=75,
                description="Sweet, crunchy carrots grown in rich organic soil",
                image="https://images.pexels.com/photos/365050/pexels-photo-365050.jpeg?auto=compress&cs=tinysrgb&w=600",
                farmer_id=4
            ),
            # 6. Fresh Strawberries
            Product(
                name="Fresh Strawberries",
                price=300.00,
                category="Fruits",
                stock=30,
                description="Sweet, seasonal strawberries perfect for desserts",
                image="https://images.pexels.com/photos/46174/strawberries-fruits-strawberry-red-46174.jpeg?auto=compress&cs=tinysrgb&w=600",
                farmer_id=4
            ),
            # 7. Organic Potatoes
            Product(
                name="Organic Potatoes",
                price=120.00,
                category="Vegetables",
                stock=60,
                description="Hearty potatoes grown using sustainable farming methods",
                image="https://images.pexels.com/photos/144248/potatoes-vegetables-erdfrucht-bio-144248.jpeg?auto=compress&cs=tinysrgb&w=600",
                farmer_id=1
            ),
            # 8. Fresh Milk
            Product(
                name="Fresh Milk",
                price=180.00,
                category="Dairy",
                stock=20,
                description="Fresh milk from grass-fed cows, pasteurized daily",
                image="https://images.pexels.com/photos/248412/pexels-photo-248412.jpeg?auto=compress&cs=tinysrgb&w=600",
                farmer_id=3
            )
        ]

        for p in products:
            db.session.add(p)
        db.session.commit()

        # -------------------------------------------------
        # 4. Orders + order-product links
        # -------------------------------------------------
        print("Creating orders...")
        orders = [
            Order(buyer_id=2, total_amount=600.00, status="delivered"),
            Order(buyer_id=2, total_amount=450.00, status="confirmed"),
            Order(buyer_id=2, total_amount=300.00, status="pending")
        ]
        for o in orders:
            db.session.add(o)
        db.session.flush()   # gives us the auto-generated order IDs

        order_products_data = [
            (1, 1, 2),   # Order 1: 2 × Tomatoes
            (1, 2, 1),   # Order 1: 1 × Eggs
            (2, 3, 1),   # Order 2: 1 × Honey
            (3, 6, 1),   # Order 3: 1 × Strawberries
        ]

        for order_id, product_id, qty in order_products_data:
            stmt = order_product.insert().values(
                order_id=order_id,
                product_id=product_id,
                quantity=qty
            )
            db.session.execute(stmt)

        # -------------------------------------------------
        # 5. Ratings
        # -------------------------------------------------
        print("Creating ratings...")
        ratings = [
            Rating(buyer_id=2, farmer_id=1, product_id=1, score=9,
                   comment="Excellent tomatoes! Very fresh and flavorful."),
            Rating(buyer_id=2, farmer_id=1, product_id=2, score=8,
                   comment="Good quality eggs, will order again."),
            Rating(buyer_id=2, farmer_id=3, product_id=3, score=10,
                   comment="Amazing honey! So pure and delicious.")
        ]
        for r in ratings:
            db.session.add(r)

        db.session.commit()

        # -------------------------------------------------
        # 6. Summary
        # -------------------------------------------------
        print("Database seeded successfully!")
        print("\nSample Data Created:")
        print(f"   Users: {len(users)} (3 farmers, 1 buyer)")
        print(f"   Products: {len(products)}")
        print(f"   Orders: {len(orders)}")
        print(f"   Ratings: {len(ratings)}")
        print("\nTest Credentials:")
        print("   Farmer: jesse@example.com / password123")
        print("   Buyer : buyer@example.com / password123")


if __name__ == '__main__':
    seed_database()