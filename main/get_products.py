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


def request_products_from_api(proxies=None):
    """
    Makes a call to Getic's API for each product category to get the product data.
    If proxies are provided in the function call, requests will be made through them.

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
            if proxies is not None:
                proxy_index = random.randint(0, len(proxies) - 1)
                proxy = {"https": proxies[proxy_index]}
                print(proxy)
            for category in categories:
                url = f"https://www.getic.com/api/preset-subcategory/{category}?limit=10000&inStock=0&variationId=cfbb89b0-7217-11eb-ed9f-fa163e4a2e20"
                requests.packages.urllib3.disable_warnings(
                    category=InsecureRequestWarning
                )
                if proxies is not None:
                    r = requests.get(url, proxies=proxy, verify=False)
                else:
                    r = requests.get(url, verify=False)
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
            sold_all_time = calculate_product_all_time_sold(
                db, product
            )  # Times product has been sold
            sold_thirty_days = calculate_product_timeperiod_sold(
                db, product, 30
            )  # Times product has been sold in 30 days
            sold_seven_days = calculate_product_timeperiod_sold(
                db, product, 7
            )  # Times product has been sold in 7 days
            print(f"SOLD SEVEN DAYS ON WRITE: {sold_seven_days}")
            print()
            product_row = Product(
                product_id=product[0],
                product_name=product[1],
                brand=product[2],
                category=product[3],
                subcategory=product[4],
                subcategory_id=product[5],
                price=product[6],
                stock=product[7],
                sold_all_time=sold_all_time,
                sold_thirty_days=sold_thirty_days,
                sold_seven_days=sold_seven_days,
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


def calculate_product_all_time_sold(db, product):
    """
    Calculates how many times the product has been sold.

        Parameters:
                db (SQLAlchemy object): Database instance
                product (list): Contains product related data (Name, price, stock...)

        Returns:
                sold_all_time (int): Number of times the product has been sold
    """
    product_entries_db = Product.query.filter(Product.product_id == product[0]).all()
    if product_entries_db:
        last_product_entry = product_entries_db[-1]
        if last_product_entry.stock <= int(product[7]):
            return last_product_entry.sold_all_time
        sold_all_time = last_product_entry.sold_all_time + (
            last_product_entry.stock - int(product[7])
        )
        return sold_all_time
    return 0  # If no product entry in the database, return 0


def calculate_product_timeperiod_sold(db, product, days):
    """
    Calculates how many times the product has been sold in the specified time period.

        Parameters:
                db (SQLAlchemy object): Database instance
                product (list): Contains product related data (Name, price, stock...)
                days (int): Specified time period in days

        Returns:
                sold_in_days (int): Number of times the product has been sold
    """
    product_entries_db = Product.query.filter(Product.product_id == product[0]).all()
    if product_entries_db:
        last_product_entry = product_entries_db[-1]
        print(f"PRODUCT NAME: {last_product_entry.product_name}")
        end_date = last_product_entry.time_created.date()
        print(f"END DATE: {end_date}")

        start_date = end_date - timedelta(days)
        print(f"START DATE: {start_date}")
        end_date_sold = last_product_entry.sold_all_time
        print(end_date_sold)
        sold_in_days = 0
        for element in product_entries_db:
            if element.time_created.date() == start_date:
                start_date_sold = element.sold_all_time
                sold_in_days = end_date_sold - start_date_sold
                print(f"SOLD IN DAYS: {sold_in_days}")
                return sold_in_days
    return 0


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
