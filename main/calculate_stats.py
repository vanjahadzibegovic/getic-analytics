from main.models import Product
from main.get_products import calculate_current_run_number
from main import db


def calculate_total_items():
    """
    Calculates the total number of products in the database (from the last run).

    Returns:
            total_products(int): Total number of products
    """
    latest_run_number = calculate_current_run_number(db) - 1
    latest_run_products = Product.query.filter(Product.run_number == latest_run_number)
    total_products = len(latest_run_products.all())
    return total_products


def calculate_total_sold():
    """
    Calculates the total number of sold products.

    Returns:
            total_sold (int): Total number of sold products
    """
    latest_run_number = calculate_current_run_number(db) - 1
    latest_run_products = Product.query.filter(Product.run_number == latest_run_number)
    total_sold = 0
    for product in latest_run_products.all():
        total_sold += product.total_sold
    return total_sold
