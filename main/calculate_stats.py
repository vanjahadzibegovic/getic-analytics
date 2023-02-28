from main.models import Product
from main.get_products import calculate_current_run_number
from main import db


def calculate_total_items(products):
    """
    Calculates the total number of products in the database
    by using database entries from the last run.

    Returns:
            total_products(int): Total number of products
    """
    total_products = len(products.all())
    return total_products


def calculate_total_sold(products):
    """
    Calculates the total number of sold products
    by using database entries from the last run.

    Returns:
            total_sold (int): Total number of sold products
    """
    total_sold = 0
    for product in products.all():
        total_sold += product.total_sold
    return total_sold


def get_category(filter):
    category_mapping = {
        "outdoor-wireless": "Outdoor Wireless",
        "home-office-networks": "Home and Office Networks",
        "lte-products": "LTE Products",
        "fiber-networks": "Fiber Networks",
        "security-systems": "Security Systems",
        "iot-products": "IoT Solutions",
        "fleet-management": "Fleet Management",
        "cables-and-cabinets": "Cables and Cabinets",
        "electrical-equipment": "Electrical Equipment",
        "mounts-and-brackets": "Mounts and Brackets",
        "gadgets": "Gadgets",
    }
    return category_mapping[filter]
