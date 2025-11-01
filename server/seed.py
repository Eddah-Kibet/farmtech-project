# seed.py
from app import app, db
from models import User, Product, Order, Rating, order_product
from werkzeug.security import generate_password_hash
from datetime import datetime


def seed_database():
    with app.app_context():

        print("Clearing existing data...")
        db.drop_all()
        db.create_all()

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
                image="https://images.unsplash.com/photo-1506976785307-8732e854ad03?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1943",
                farmer_id=1
            ),
            # 3. Pure Honey
            Product(
                name="Pure Honey",
                price=1200.00,
                category="Other",
                stock=15,
                description="Raw, unfiltered honey from local bee colonies",
                image="https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8aG9uZXl8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&q=60&w=900",
                farmer_id=3
            ),
            # 4. Fresh Apples
            Product(
                name="Fresh Apples",
                price=80.00,
                category="Fruits",
                stock=100,
                description="Crisp, juicy apples picked fresh from our orchard",
                image="https://plus.unsplash.com/premium_photo-1667049292983-d2524dd0ef08?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YXBwbGVzfGVufDB8fDB8fHww&auto=format&fit=crop&q=60&w=900",
                farmer_id=3
            ),
            # 5. Organic Carrots
            Product(
                name="Organic Carrots",
                price=60.00,
                category="Vegetables",
                stock=75,
                description="Sweet, crunchy carrots grown in rich organic soil",
                image="https://images.unsplash.com/photo-1590868309235-ea34bed7bd7f?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=927",
                farmer_id=4
            ),
            # 6. Fresh Strawberries
            Product(
                name="Fresh Strawberries",
                price=300.00,
                category="Fruits",
                stock=30,
                description="Sweet, seasonal strawberries perfect for desserts",
                image="https://plus.unsplash.com/premium_photo-1675731118661-15dc54c11130?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8c3RyYXdiZXJyaWVzfGVufDB8fDB8fHww&auto=format&fit=crop&q=60&w=900",
                farmer_id=4
            ),
            # 7. Organic Potatoes
            Product(
                name="Organic Potatoes",
                price=120.00,
                category="Vegetables",
                stock=60,
                description="Hearty potatoes grown using sustainable farming methods",
                image="https://plus.unsplash.com/premium_photo-1664372599369-dd9f4ee07254?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8cG90YXRvZXN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&q=60&w=900",
                farmer_id=1
            ),
            # 8. Fresh Milk
            Product(
                name="Fresh Milk",
                price=180.00,
                category="Dairy",
                stock=20,
                description="Fresh milk from grass-fed cows, pasteurized daily",
                image="https://images.unsplash.com/photo-1523473827533-2a64d0d36748?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1760",
                farmer_id=3
            )
        ]

        for p in products:
            db.session.add(p)
        db.session.commit()

        print("Creating orders...")
        orders = [
            Order(buyer_id=2, total_amount=600.00, status="delivered"),
            Order(buyer_id=2, total_amount=450.00, status="confirmed"),
            Order(buyer_id=2, total_amount=300.00, status="pending")
        ]
        for o in orders:
            db.session.add(o)
        db.session.flush()   

        order_products_data = [
            (1, 1, 2),   
            (1, 2, 1),   
            (2, 3, 1),   
            (3, 6, 1),   
        ]

        for order_id, product_id, qty in order_products_data:
            stmt = order_product.insert().values(
                order_id=order_id,
                product_id=product_id,
                quantity=qty
            )
            db.session.execute(stmt)

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

        print("Seeding messages...")


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