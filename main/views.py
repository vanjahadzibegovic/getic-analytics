from flask import render_template, request
from main import app, db
from main.models import Product
from main.get_products import (
    request_products_from_api,
    write_products_to_db,
    request_proxy_list,
    calculate_current_run_number,
    get_product_images,
)


@app.route("/", methods=["GET", "POST"])
def index():
    latest_run_number = calculate_current_run_number(db) - 1
    latest_run_products = Product.query.filter(
        Product.run_number == latest_run_number
    ).order_by(Product.total_sold.desc())
    page = request.args.get("page", 1, type=int)
    products_page = latest_run_products.paginate(page=page, per_page=78)
    return render_template("index.html", title="Dashboard", products=products_page)


@app.route("/get_products", methods=["GET"])
def get_products():
    proxies = request_proxy_list()
    products = request_products_from_api(proxies)
    write_products_to_db(db, products)
    return "Product stats updated..."


@app.route("/get_images", methods=["GET"])
def get_images():
    get_product_images(db)
    return "Images downloaded..."
