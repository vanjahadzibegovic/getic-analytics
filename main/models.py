from main import db, login_manager
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.password}')"


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    subcategory = db.Column(db.String(200), nullable=False)
    subcategory_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    sold_all_time = db.Column(db.Integer, nullable=False)
    sold_thirty_days = db.Column(db.Integer, nullable=False)
    sold_seven_days = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(400), nullable=False)
    run_number = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"Product('{self.id}', '{self.product_name}', '{self.brand}', '{self.product_id}', '{self.category}', '{self.subcategory}', '{self.price}', '{self.stock}', '{self.sold_all_time}', '{self.sold_thirty_days}', '{self.sold_seven_days}', '{self.run_number}', '{self.time_created}')"
