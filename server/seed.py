from extensions import db
from models import (
    User, Buyer, Farmer, Category, SubCategory, Product, ProduceDetail,
    Review, Payment, Order, OrderItem
)
from datetime import datetime, date
import random
from app import app


def seed_data():
    print("Clearing old data...")
    db.drop_all()
    db.create_all()

    print("Creating users and profiles...")
    # --- Users ---
    buyers = [
        User(username="alicew", email="alicew@gmail.com", user_type="buyer"),
        User(username="johnm", email="johnm@gmail.com", user_type="buyer"),
        User(username="lucyk", email="lucyk@gmail.com", user_type="buyer"),
        User(username="petero", email="petero@gmail.com", user_type="buyer"),
        User(username="annn", email="annn@gmail.com", user_type="buyer"),
    ]

    farmers = [
        User(username="farmer_james", email="jamesfarm@gmail.com", user_type="farmer"),
        User(username="greenfields", email="greenfieldsfarm@gmail.com", user_type="farmer"),
        User(username="sunnyvale", email="sunnyvale@gmail.com", user_type="farmer"),
        User(username="mwangifarm", email="mwangifarm@gmail.com", user_type="farmer"),
        User(username="karisafarm", email="karisafarm@gmail.com", user_type="farmer"),
    ]

    for u in buyers + farmers:
        u.set_password("password123")
        db.session.add(u)
    db.session.commit()

    # --- Buyer Profiles ---
    buyer_profiles = [
        Buyer(user_id=buyers[0].id, first_name="Alice", last_name="Wanjiku", address="Nakuru, Kenya"),
        Buyer(user_id=buyers[1].id, first_name="John", last_name="Mwangi", address="Eldoret, Kenya"),
        Buyer(user_id=buyers[2].id, first_name="Lucy", last_name="Kamau", address="Kisumu, Kenya"),
        Buyer(user_id=buyers[3].id, first_name="Peter", last_name="Otieno", address="Nairobi, Kenya"),
        Buyer(user_id=buyers[4].id, first_name="Ann", last_name="Njeri", address="Thika, Kenya"),
    ]
    db.session.add_all(buyer_profiles)
    db.session.commit()

    # --- Farmer Profiles ---
    farmer_profiles = [
        Farmer(user_id=farmers[0].id, farm_name="James Organic Farm", contact_person="James Kariuki", phone="+254712345678", address="Kiambu, Kenya"),
        Farmer(user_id=farmers[1].id, farm_name="Greenfields Farm", contact_person="Mary Wambui", phone="+254713223344", address="Nakuru, Kenya"),
        Farmer(user_id=farmers[2].id, farm_name="Sunnyvale Produce", contact_person="Paul Mutua", phone="+254714556677", address="Machakos, Kenya"),
        Farmer(user_id=farmers[3].id, farm_name="Mwangi Farm", contact_person="Mwangi Gathoni", phone="+254715667788", address="Nyeri, Kenya"),
        Farmer(user_id=farmers[4].id, farm_name="Karisa Family Farm", contact_person="Karisa Omondi", phone="+254716778899", address="Mombasa, Kenya"),
    ]
    db.session.add_all(farmer_profiles)
    db.session.commit()

    print("Creating categories and subcategories...")
    categories = [
        Category(name="Vegetables", description="Fresh vegetables from local farms"),
        Category(name="Fruits", description="Locally grown fruits"),
        Category(name="Cereals", description="Grains and pulses"),
    ]
    db.session.add_all(categories)
    db.session.commit()

    subcategories = [
        SubCategory(name="Kales", category_id=categories[0].id),
        SubCategory(name="Tomatoes", category_id=categories[0].id),
        SubCategory(name="Cabbages", category_id=categories[0].id),
        SubCategory(name="Bananas", category_id=categories[1].id),
        SubCategory(name="Avocados", category_id=categories[1].id),
        SubCategory(name="Lemons", category_id=categories[1].id),
        SubCategory(name="Maize", category_id=categories[2].id),
        SubCategory(name="Beans", category_id=categories[2].id),
    ]
    db.session.add_all(subcategories)
    db.session.commit()

    print("Creating products...")
    # Updated product_data with image URLs
    # Format: (name, description, price, qty, unit, organic, sub_id, image_url)
    product_data = [
        (
            "Tomatoes", 
            "Fresh red tomatoes perfect for cooking", 
            90, 100, "kg", True, 1,
            "https://images.unsplash.com/photo-1546470427-227e1b62cf21?w=500&q=80"
        ),
        (
            "Kales", 
            "Fresh sukuma wiki leaves", 
            40, 150, "bunch", True, 0,
            "https://images.unsplash.com/photo-1622205313162-be1d5712a43f?w=500&q=80"
        ),
        (
            "Cabbages", 
            "Large cabbages harvested today", 
            70, 80, "piece", False, 2,
            "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=500&q=80"
        ),
        (
            "Bananas", 
            "Sweet ripe bananas", 
            120, 50, "bunch", True, 3,
            "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=500&q=80"
        ),
        (
            "Avocados", 
            "Creamy Hass avocados", 
            150, 60, "piece", True, 4,
            "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=500&q=80"
        ),
        (
            "Lemons", 
            "Juicy lemons for juice and cooking", 
            80, 100, "kg", False, 5,
            "https://images.unsplash.com/photo-1587486937409-a97d3e3c1e8e?w=500&q=80"
        ),
        (
            "Maize", 
            "Dry maize for flour or boiling", 
            100, 200, "kg", False, 6,
            "https://images.unsplash.com/photo-1603569283847-aa295f0d016a?w=500&q=80"
        ),
        (
            "Beans", 
            "Red kidney beans rich in protein", 
            160, 150, "kg", False, 7,
            "https://images.unsplash.com/photo-1584949602334-204ce7d69f71?w=500&q=80"
        ),
    ]

    products = []
    for i, (name, desc, price, qty, unit, organic, sub_id, image_url) in enumerate(product_data):
        farmer = random.choice(farmer_profiles)
        product = Product(
            name=name,
            description=desc,
            price=price,
            quantity_available=qty,
            unit=unit,
            farmer_id=farmer.id,
            subcategory_id=subcategories[sub_id].id,
            is_organic=organic,
            harvest_date=date.today(),
            image_url=image_url  # Added image URL
        )
        db.session.add(product)
        products.append(product)
    db.session.commit()

    print("Adding produce details...")
    produce_detail_data = {
        "Tomatoes": ("Roma, Cherry", "Conventional", 7, "Store in cool place", "Rich in Vitamin C, potassium, and lycopene"),
        "Kales": ("Collard", "Organic", 5, "Refrigerate below 5°C", "High in Vitamin A, K, and fiber"),
        "Cabbages": ("Gloria F1", "Conventional", 14, "Cool, humid storage", "Rich in Vitamin C and K"),
        "Bananas": ("Cavendish", "Organic", 5, "Room temperature", "Rich in potassium and Vitamin B6"),
        "Avocados": ("Hass", "Organic", 7, "Cool dry place", "High in healthy fats and Vitamin E"),
        "Lemons": ("Eureka", "Conventional", 21, "Refrigerate", "Rich in Vitamin C and antioxidants"),
        "Maize": ("H614", "Conventional", 60, "Dry and sealed", "High in carbs and fiber"),
        "Beans": ("Rosecoco", "Conventional", 90, "Cool dry storage", "Rich in protein and iron"),
    }

    for product in products:
        d = produce_detail_data[product.name]
        detail = ProduceDetail(
            product_id=product.id,
            variety=d[0],
            growing_method=d[1],
            shelf_life=d[2],
            storage_conditions=d[3],
            nutritional_info=d[4]
        )
        db.session.add(detail)
    db.session.commit()

    print("Adding reviews...")
    comments = [
        "Very fresh and tasty!",
        "Good quality and neatly packed.",
        "Would buy again, great service.",
        "Average size but good quality.",
        "Delivered on time and fresh!",
        "Not very fresh, could improve.",
        "Great taste and good price.",
        "Loved it! Highly recommend."
    ]

    for product in products:
        for buyer in buyer_profiles:
            review = Review(
                product_id=product.id,
                buyer_id=buyer.id,
                rating=random.randint(3, 5),
                comment=random.choice(comments)
            )
            db.session.add(review)
    db.session.commit()

    print("Adding payments...")
    methods = ["mpesa", "bank_transfer", "credit_card", "debit_card", "cash"]
    for buyer in buyer_profiles:
        payment = Payment(
            buyer_id=buyer.id,
            amount=random.randint(500, 3000),
            payment_method=random.choice(methods),
            transaction_id=f"TXN{random.randint(10000, 99999)}",
            status=random.choice(["completed", "pending"])
        )
        db.session.add(payment)
    db.session.commit()

    print("Creating orders and order items...")
    orders = []
    for buyer in buyer_profiles:
        payment = Payment.query.filter_by(buyer_id=buyer.id).first()
        selected_products = random.sample(products, k=3)
        total = 0

        order = Order(
            buyer_id=buyer.id,
            payment_id=payment.id if payment else None,
            status=random.choice(["pending", "confirmed", "shipped"]),
            total_amount=1  # temporary value, will update below
        )
        db.session.add(order)
        db.session.flush()  # get order.id

        for product in selected_products:
            quantity = random.randint(1, 5)
            price = product.price * quantity
            total += price
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price_at_purchase=product.price
            )
            db.session.add(order_item)

        order.total_amount = total if total > 0 else 1
        db.session.add(order)
        orders.append(order)

    db.session.commit()
    print("Database seeded successfully!")


if __name__ == "__main__":
    with app.app_context():
        seed_data()
