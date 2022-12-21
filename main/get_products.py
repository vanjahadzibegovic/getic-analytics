from main.models import Product
import requests
import json
import random
import os


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
            for category in categories:
                url = f"https://www.getic.com/api/preset-subcategory/{category}?limit=10000&inStock=0&variationId=cfbb89b0-7217-11eb-ed9f-fa163e4a2e20"
                r = requests.get(url, proxies=proxy, verify=False)
                parsed_response = json.loads(r.text)
                for product_group in parsed_response["content"]:
                    subcategory = product_group["title"]
                    subcategory_id = product_group["id"]
                    for product in product_group["products"]:
                        product_name = product["title"]
                        price = str(product["prices"][0]["prices"][0]["price"])
                        stock = str(product["expectedAmount"])
                        image = f'https://www.getic.com{product["images"][0]["variants"][0]["path"]}'
                        product_id = str(product["id"])
                        products.append(
                            [
                                product_id,
                                product_name,
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


def request_proxy_list():
    """
    Makes a call to ProxyScrape's API to obtain a list of HTTPS proxies (Elite).

        Returns:
                proxies (list): Contains HTTPS proxies
    """
    url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=elite"
    r = requests.get(url, verify=False)
    proxies = r.text.split("\r\n")[:-1]
    return proxies


def write_products_to_db(db, products):
    """
    Writes data related to each product into a database table.

    Parameters:
            db (SQLAlchemy object): Database instance
            product (list): Contains product related data (Name, price, stock...)
    """
    run_number = calculate_current_run_number(db)  # Current DB writing iteration
    for product in products:
        total_sold = calculate_total_sold(db, product)  # Times product has been sold
        product = Product(
            product_id=product[0],
            product_name=product[1],
            category=product[2],
            subcategory=product[3],
            subcategory_id=product[4],
            price=product[5],
            stock=product[6],
            total_sold=total_sold,
            image=product[7],
            run_number=run_number,
        )
        db.session.add(product)
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


def calculate_total_sold(db, product):
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
        if last_product_entry.stock <= int(product[6]):
            return last_product_entry.total_sold
        total_sold = last_product_entry.total_sold + (
            last_product_entry.stock - int(product[6])
        )
        return total_sold
    return 0  # If no product entry in the database, return 0


def get_product_images(db):
    """
    Downloads images of all products stored in the database.

    Parameters:
            db (SQLAlchemy object): Database instance
    """
    products = Product.query.distinct(Product.product_id).all()
    for product in products:
        r = requests.get(product.image).content
        with open(
            os.path.join("main/static/img/", f"{product.product_id}.jpg"), "wb+"
        ) as file:
            file.write(r)
            file.close()
