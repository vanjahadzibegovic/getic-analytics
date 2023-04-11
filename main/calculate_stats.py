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
        total_sold += product.sold_all_time
    return total_sold


def calculate_sold_thirty_days(products):
    """
    Calculates the total number of products sold in the last thirty days
    by using database entries from the last run.

    Returns:
            thirty_days_sold (int): Number of products sold in thirty days
    """
    thirty_days_sold = 0
    for product in products.all():
        thirty_days_sold += product.sold_thirty_days
    return thirty_days_sold


def calculate_sold_seven_days(products):
    """
    Calculates the total number of products sold in the last seven days
    by using database entries from the last run.

    Returns:
            seven_days_sold (int): Number of products sold in seven days
    """
    seven_days_sold = 0
    for product in products.all():
        seven_days_sold += product.sold_seven_days
    return seven_days_sold


def map_category(filter):
    category_mapping = {
        "all-products": "All Products",
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


def map_sort(sort):
    sort_mapping = {
        "total-highest": "Most Sold - All Time",
        "total-lowest": "Least Sold - All Time",
        "thirty-days-highest": "Most Sold - 30 Days",
        "thirty-days-lowest": "Least Sold - 30 Days",
        "seven-days-highest": "Most Sold - 7 Days",
        "seven-days-lowest": "Least Sold - 7 Days",
        "price-highest": "Most Expensive",
        "price-lowest": "Least Expensive",
    }
    return sort_mapping[sort]
