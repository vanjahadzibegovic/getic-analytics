from main import db
from sqlalchemy.sql import func
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    subcategory = db.Column(db.String(200), nullable=False)
    subcategory_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    total_sold = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(400), nullable=False)
    run_number = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"Product('{self.id}', '{self.product_name}', '{self.product_id}', '{self.category}', '{self.subcategory}', '{self.price}', '{self.stock}', '{self.total_sold}', '{self.run_number}')"
