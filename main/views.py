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
from main.calculate_stats import (
    calculate_total_items,
    calculate_total_sold,
    map_category,
    map_sort,
)


@app.route("/", methods=["GET", "POST"])
def index():
    latest_run_number = calculate_current_run_number(db) - 1
    latest_run_products = Product.query.filter(
        Product.run_number == latest_run_number
    ).order_by(Product.total_sold.desc())
    page = request.args.get("page", 1, type=int)
    products_page = latest_run_products.paginate(page=page, per_page=78)
    total_products = calculate_total_items(latest_run_products)
    total_sold = calculate_total_sold(latest_run_products)
    return render_template(
        "index.html",
        title="Dashboard",
        base="categories",
        product_type=map_category("all-products"),
        sort_type=map_sort("total-highest"),
        filter="all-products",
        sort="total-highest",
        products=products_page,
        total_products=total_products,
        total_sold=total_sold,
    )


@app.route("/categories/<filter>/<sort>/", methods=["GET", "POST"])
def categories(filter, sort):
    latest_run_number = calculate_current_run_number(db) - 1
    if sort == "total-lowest":
        if filter != "all-products":
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.category == filter)
                .order_by(Product.total_sold.asc())
            )
        else:
            latest_run_products = Product.query.filter(
                Product.run_number == latest_run_number
            ).order_by(Product.total_sold.asc())
    else:
        if filter != "all-products":
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.category == filter)
                .order_by(Product.total_sold.desc())
            )
        else:
            latest_run_products = Product.query.filter(
                Product.run_number == latest_run_number
            ).order_by(Product.total_sold.desc())
    page = request.args.get("page", 1, type=int)
    products_page = latest_run_products.paginate(page=page, per_page=78)
    total_products = calculate_total_items(latest_run_products)
    total_sold = calculate_total_sold(latest_run_products)
    return render_template(
        "index.html",
        title="Dashboard",
        base="categories",
        product_type=map_category(filter),
        sort_type=map_sort(sort),
        filter=filter,
        sort=sort,
        products=products_page,
        total_products=total_products,
        total_sold=total_sold,
    )


@app.route("/brands/<filter>/<sort>/", methods=["GET", "POST"])
def brands(filter, sort):
    latest_run_number = calculate_current_run_number(db) - 1
    if sort == "total-lowest":
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.brand == filter)
            .order_by(Product.total_sold.asc())
        )
    else:
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.brand == filter)
            .order_by(Product.total_sold.desc())
        )
    page = request.args.get("page", 1, type=int)
    products_page = latest_run_products.paginate(page=page, per_page=78)
    total_products = calculate_total_items(latest_run_products)
    total_sold = calculate_total_sold(latest_run_products)
    return render_template(
        "index.html",
        title="Dashboard",
        base="brands",
        product_type=filter,
        sort_type=map_sort(sort),
        filter=filter,
        sort=sort,
        products=products_page,
        total_products=total_products,
        total_sold=total_sold,
    )
