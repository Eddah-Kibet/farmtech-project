from flask import Flask
from flask_migrate import Migrate
from extensions import db, bcrypt 
# from models import User, Buyer, Farmer, Category, SubCategory, Product, ProduceDetail, Review, Payment

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    Migrate(app, db)

    # Import routes after db setup
    # from routes.auth import auth_bp
    # from routes.login import login_bp

    # app.register_blueprint(auth_bp)
    # app.register_blueprint(login_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
