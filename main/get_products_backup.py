from main import db
from main.models import Product
import requests
from urllib3.exceptions import InsecureRequestWarning
import json
import random
import os
from datetime import datetime, timedelta


def request_proxy_list():
    """
    Makes a call to ProxyScrape's API to obtain a list of HTTPS proxies (Elite).

        Returns:
                proxies (list): Contains HTTPS proxies
    """
    url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=elite"
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    r = requests.get(url, verify=False)
    proxies = r.text.split("\r\n")[:-1]
    return proxies


def request_products_from_api(proxies):
    """
    Makes a call to Getic's API for each product category to get the product data.
    It makes a request through a random proxy server to prevent being blocked.

        Parameters:
                proxies (list): Contains HTTPS proxies

        Returns:
                products (list): Contains data about each product
    """

    categories = [
        "outdoor-wireless",
        "home-office-networks",
        "lte-products",
        "fiber-networks",
        "security-systems",
        "iot-products",
        "fleet-management",
        "cables-and-cabinets",
        "electrical-equipment",
        "mounts-and-brackets",
        "gadgets",
    ]
    products = []
    while True:
        try:
            proxy_index = random.randint(0, len(proxies) - 1)
            proxy = {"https": proxies[proxy_index]}
            print(proxy)
            for category in categories:
                url = f"https://www.getic.com/api/preset-subcategory/{category}?limit=10000&inStock=0&variationId=cfbb89b0-7217-11eb-ed9f-fa163e4a2e20"
                requests.packages.urllib3.disable_warnings(
                    category=InsecureRequestWarning
                )
                r = requests.get(url, proxies=proxy, verify=False)
                parsed_response = json.loads(r.text)
                for product_group in parsed_response["content"]:
                    subcategory = product_group["title"]
                    subcategory_id = product_group["id"]
                    for product in product_group["products"]:
                        product_name = product["title"]
                        brand = product["brand"]
                        price = str(product["prices"][0]["prices"][0]["price"])
                        stock = str(product["expectedAmount"])
                        image = f'https://www.getic.com{product["images"][0]["variants"][0]["path"]}'
                        product_id = str(product["id"])
                        products.append(
                            [
                                product_id,
                                product_name,
                                brand,
                                category,
                                subcategory,
                                subcategory_id,
                                price,
                                stock,
                                image,
                            ]
                        )
            break
        except:
            print("Error, looking for another proxy")
    return products


def write_products_to_db(db, products):
    """
    Writes data related to each product into a database table.

    Parameters:
            db (SQLAlchemy object): Database instance
            product (list): Contains product related data (Name, price, stock...)
    """
    run_number = calculate_current_run_number(db)  # Current DB writing iteration
    previous_product_ids = []
    for product in products:
        if product[0] not in previous_product_ids:
            total_sold = calculate_product_total_sold(
                db, product
            )  # Times product has been sold
            product_row = Product(
                product_id=product[0],
                product_name=product[1],
                brand=product[2],
                category=product[3],
                subcategory=product[4],
                subcategory_id=product[5],
                price=product[6],
                stock=product[7],
                total_sold=total_sold,
                image=product[8],
                run_number=run_number,
            )
            previous_product_ids.append(product[0])
            db.session.add(product_row)
    db.session.commit()


def calculate_current_run_number(db):
    """
    Calculates the current iteration of writing products to database.

        Parameters:
                db (SQLAlchemy object): Database instance

        Returns:
                current_run_number (int): Current writing iteration
    """
    all_products = Product.query.all()
    if all_products:
        run_numbers = []
        for product in all_products:
            run_numbers.append(product.run_number)
        current_run_number = max(run_numbers) + 1
        return current_run_number
    return 1  # If there are no products in the database, returns 1


def calculate_product_total_sold(db, product):
    """
    Calculates how many times the product has been sold.

        Parameters:
                db (SQLAlchemy object): Database instance
                product (list): Contains product related data (Name, price, stock...)

        Returns:
                total_sold (int): Number of times the product has been sold
    """
    product_entries_db = Product.query.filter(Product.product_id == product[0]).all()
    if product_entries_db:
        last_product_entry = product_entries_db[-1]
        if last_product_entry.stock <= int(product[7]):
            return last_product_entry.total_sold
        total_sold = last_product_entry.total_sold + (
            last_product_entry.stock - int(product[7])
        )
        return total_sold
    return 0  # If no product entry in the database, return 0


def calculate_product_timeperiod_sold(db, product_id, days):
    product_entries_db = Product.query.filter(Product.product_id == product_id).all()
    if product_entries_db:
        last_product_entry = product_entries_db[-1]
        end_date = last_product_entry.time_created.date()
        start_date = end_date - timedelta(days)
        end_date_sold = last_product_entry.total_sold
        sold_in_days = "N/A"
        for element in product_entries_db:
            if element.time_created.date() == start_date:
                start_date_sold = element.total_sold
                sold_in_days = str(end_date_sold - start_date_sold)
                break
    return sold_in_days


def get_product_images(db):
    """
    Downloads images of all products stored in the database.

    Parameters:
            db (SQLAlchemy object): Database instance
    """
    products = Product.query.distinct(Product.product_id).all()
    print("Downloading images...")
    for product in products:
        print(product.image)
        r = requests.get(product.image).content
        with open(
            os.path.join("main/static/img/", f"{product.product_id}.jpg"), "wb+"
        ) as file:
            file.write(r)
            file.close()
    print("Images downloaded...")
