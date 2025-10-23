from extensions import db
from models import User, Buyer, Farmer, Category, SubCategory, Product, ProduceDetail, Review, Payment
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
        Buyer(user_id=buyers[0].id, first_name="Alice", last_name="Wanjiku", address="Nakuru, Kenya", created_at=datetime.utcnow()),
        Buyer(user_id=buyers[1].id, first_name="John", last_name="Mwangi", address="Eldoret, Kenya", created_at=datetime.utcnow()),
        Buyer(user_id=buyers[2].id, first_name="Lucy", last_name="Kamau", address="Kisumu, Kenya", created_at=datetime.utcnow()),
        Buyer(user_id=buyers[3].id, first_name="Peter", last_name="Otieno", address="Nairobi, Kenya", created_at=datetime.utcnow()),
        Buyer(user_id=buyers[4].id, first_name="Ann", last_name="Njeri", address="Thika, Kenya", created_at=datetime.utcnow()),
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
    product_data = [
        ("Tomatoes", "Fresh red tomatoes perfect for cooking", 90, 100, "kg", True, 0),
        ("Kales", "Fresh sukuma wiki leaves", 40, 150, "bunch", True, 1),
        ("Cabbages", "Large cabbages harvested today", 70, 80, "piece", False, 2),
        ("Bananas", "Sweet ripe bananas", 120, 50, "bunch", True, 3),
        ("Avocados", "Creamy Hass avocados", 150, 60, "piece", True, 4),
        ("Lemons", "Juicy lemons for juice and cooking", 80, 100, "kg", False, 5),
        ("Maize", "Dry maize for flour or boiling", 100, 200, "kg", False, 6),
        ("Beans", "Red kidney beans rich in protein", 160, 150, "kg", False, 7),
    ]

    products = []
    for i, (name, desc, price, qty, unit, organic, sub_id) in enumerate(product_data):
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
            harvest_date=date.today()
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
        db.session.add(ProduceDetail(
            product_id=product.id,
            variety=d[0],
            growing_method=d[1],
            shelf_life=d[2],
            storage_conditions=d[3],
            nutritional_info=d[4]
        ))
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
                comment=random.choice(comments),
                created_at=datetime.utcnow()
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
            status=random.choice(["completed", "pending"]),
        )
        db.session.add(payment)
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_data()
