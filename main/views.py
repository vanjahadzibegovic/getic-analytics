from flask import render_template, request, redirect, url_for, flash
from main import app, db, bcrypt
from flask_login import (
    login_user,
    login_required,
    current_user,
    logout_user,
)
from main.models import Product, User
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
    calculate_sold_thirty_days,
    calculate_sold_seven_days,
    map_category,
    map_sort,
)
from main.forms import SearchForm, LoginForm


@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("main"))
        else:
            flash("Login unsuccesful. Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/main", methods=["GET", "POST"])
@login_required
def main():
    latest_run_number = calculate_current_run_number(db) - 1
    latest_run_products = Product.query.filter(
        Product.run_number == latest_run_number
    ).order_by(Product.sold_all_time.desc())
    page = request.args.get("page", 1, type=int)
    products_page = latest_run_products.paginate(page=page, per_page=78)
    first_run_date = (
        Product.query.filter(Product.run_number == 1).first().time_created.date()
    )
    total_products = calculate_total_items(latest_run_products)
    total_sold = calculate_total_sold(latest_run_products)
    thirty_days_sold = calculate_sold_thirty_days(latest_run_products)
    seven_days_sold = calculate_sold_seven_days(latest_run_products)
    return render_template(
        "main.html",
        title="Dashboard",
        base="categories",
        product_type=map_category("all-products"),
        sort_type=map_sort("total-highest"),
        filter="all-products",
        sort="total-highest",
        products=products_page,
        first_run_date=first_run_date,
        total_products=total_products,
        total_sold=total_sold,
        thirty_days_sold=thirty_days_sold,
        seven_days_sold=seven_days_sold,
        form=SearchForm(),
    )


@app.route("/categories/<filter>/<sort>/", methods=["GET", "POST"])
@login_required
def categories(filter, sort):
    latest_run_number = calculate_current_run_number(db) - 1
    if sort == "total-lowest":
        if filter != "all-products":
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.category == filter)
                .order_by(Product.sold_all_time.asc())
            )
        else:
            latest_run_products = Product.query.filter(
                Product.run_number == latest_run_number
            ).order_by(Product.sold_all_time.asc())
    elif sort == "seven-days-highest":
        if filter != "all-products":
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.category == filter)
                .order_by(Product.sold_seven_days.desc())
            )
        else:
            latest_run_products = Product.query.filter(
                Product.run_number == latest_run_number
            ).order_by(Product.sold_seven_days.desc())
    elif sort == "seven-days-lowest":
        if filter != "all-products":
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.category == filter)
                .order_by(Product.sold_seven_days.asc())
            )
        else:
            latest_run_products = Product.query.filter(
                Product.run_number == latest_run_number
            ).order_by(Product.sold_seven_days.asc())
    elif sort == "thirty-days-highest":
        if filter != "all-products":
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.category == filter)
                .order_by(Product.sold_thirty_days.desc())
            )
        else:
            latest_run_products = Product.query.filter(
                Product.run_number == latest_run_number
            ).order_by(Product.sold_thirty_days.desc())
    elif sort == "thirty-days-lowest":
        if filter != "all-products":
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.category == filter)
                .order_by(Product.sold_thirty_days.asc())
            )
        else:
            latest_run_products = Product.query.filter(
                Product.run_number == latest_run_number
            ).order_by(Product.sold_thirty_days.asc())
    elif sort == "price-highest":
        if filter != "all-products":
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.category == filter)
                .order_by(Product.price.desc())
            )
        else:
            latest_run_products = Product.query.filter(
                Product.run_number == latest_run_number
            ).order_by(Product.price.desc())
    elif sort == "price-lowest":
        if filter != "all-products":
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.category == filter)
                .order_by(Product.price.asc())
            )
        else:
            latest_run_products = Product.query.filter(
                Product.run_number == latest_run_number
            ).order_by(Product.price.asc())
    else:
        if filter != "all-products":
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.category == filter)
                .order_by(Product.sold_all_time.desc())
            )
        else:
            latest_run_products = Product.query.filter(
                Product.run_number == latest_run_number
            ).order_by(Product.sold_all_time.desc())

    page = request.args.get("page", 1, type=int)
    products_page = latest_run_products.paginate(page=page, per_page=78)
    first_run_date = (
        Product.query.filter(Product.run_number == 1).first().time_created.date()
    )
    total_products = calculate_total_items(latest_run_products)
    total_sold = calculate_total_sold(latest_run_products)
    thirty_days_sold = calculate_sold_thirty_days(latest_run_products)
    seven_days_sold = calculate_sold_seven_days(latest_run_products)
    return render_template(
        "main.html",
        title="Dashboard",
        base="categories",
        product_type=map_category(filter),
        sort_type=map_sort(sort),
        filter=filter,
        sort=sort,
        products=products_page,
        first_run_date=first_run_date,
        total_products=total_products,
        total_sold=total_sold,
        thirty_days_sold=thirty_days_sold,
        seven_days_sold=seven_days_sold,
        form=SearchForm(),
    )


@app.route("/brands/<filter>/<sort>/", methods=["GET", "POST"])
@login_required
def brands(filter, sort):
    latest_run_number = calculate_current_run_number(db) - 1
    if sort == "total-lowest":
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.brand == filter)
            .order_by(Product.sold_all_time.asc())
        )
    elif sort == "seven-days-highest":
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.brand == filter)
            .order_by(Product.sold_seven_days.desc())
        )
    elif sort == "seven-days-lowest":
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.brand == filter)
            .order_by(Product.sold_seven_days.asc())
        )
    elif sort == "thirty-days-highest":
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.brand == filter)
            .order_by(Product.sold_thirty_days.desc())
        )
    elif sort == "thirty-days-lowest":
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.brand == filter)
            .order_by(Product.sold_thirty_days.asc())
        )
    elif sort == "price-highest":
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.brand == filter)
            .order_by(Product.price.desc())
        )
    elif sort == "price-lowest":
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.brand == filter)
            .order_by(Product.price.asc())
        )
    else:
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.brand == filter)
            .order_by(Product.sold_all_time.desc())
        )
    page = request.args.get("page", 1, type=int)
    products_page = latest_run_products.paginate(page=page, per_page=78)
    first_run_date = (
        Product.query.filter(Product.run_number == 1).first().time_created.date()
    )
    total_products = calculate_total_items(latest_run_products)
    total_sold = calculate_total_sold(latest_run_products)
    thirty_days_sold = calculate_sold_thirty_days(latest_run_products)
    seven_days_sold = calculate_sold_seven_days(latest_run_products)
    return render_template(
        "main.html",
        title="Dashboard",
        base="brands",
        product_type=filter,
        sort_type=map_sort(sort),
        filter=filter,
        sort=sort,
        products=products_page,
        first_run_date=first_run_date,
        total_products=total_products,
        total_sold=total_sold,
        thirty_days_sold=thirty_days_sold,
        seven_days_sold=seven_days_sold,
        form=SearchForm(),
    )


@app.route(
    "/search/",
    defaults={"sort": "total-highest", "product_type": None},
    methods=["POST"],
)
@app.route("/search/<product_type>/<sort>/", methods=["GET"])
@login_required
def search(sort, product_type):
    form = SearchForm()
    if form.validate_on_submit():
        latest_run_number = calculate_current_run_number(db) - 1
        latest_run_products = (
            Product.query.filter(Product.run_number == latest_run_number)
            .filter(Product.product_name.ilike(f"%{form.searched.data}%"))
            .order_by(Product.sold_all_time.desc())
        )
        product_type = form.searched.data
    else:
        if sort == "total-highest":
            latest_run_number = calculate_current_run_number(db) - 1
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.product_name.ilike(f"%{product_type}%"))
                .order_by(Product.sold_all_time.desc())
            )
        elif sort == "total-lowest":
            latest_run_number = calculate_current_run_number(db) - 1
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.product_name.ilike(f"%{product_type}%"))
                .order_by(Product.sold_all_time.asc())
            )
        elif sort == "seven-days-highest":
            latest_run_number = calculate_current_run_number(db) - 1
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.product_name.ilike(f"%{product_type}%"))
                .order_by(Product.sold_seven_days.desc())
            )
        elif sort == "seven-days-lowest":
            latest_run_number = calculate_current_run_number(db) - 1
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.product_name.ilike(f"%{product_type}%"))
                .order_by(Product.sold_seven_days.asc())
            )
        elif sort == "thirty-days-highest":
            latest_run_number = calculate_current_run_number(db) - 1
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.product_name.ilike(f"%{product_type}%"))
                .order_by(Product.sold_thirty_days.desc())
            )
        elif sort == "thirty-days-lowest":
            latest_run_number = calculate_current_run_number(db) - 1
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.product_name.ilike(f"%{product_type}%"))
                .order_by(Product.sold_thirty_days.asc())
            )
        elif sort == "price-highest":
            latest_run_number = calculate_current_run_number(db) - 1
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.product_name.ilike(f"%{product_type}%"))
                .order_by(Product.price.desc())
            )
        elif sort == "price-lowest":
            latest_run_number = calculate_current_run_number(db) - 1
            latest_run_products = (
                Product.query.filter(Product.run_number == latest_run_number)
                .filter(Product.product_name.ilike(f"%{product_type}%"))
                .order_by(Product.price.asc())
            )
    page = request.args.get("page", 1, type=int)
    products_page = latest_run_products.paginate(page=page, per_page=78)
    first_run_date = (
        Product.query.filter(Product.run_number == 1).first().time_created.date()
    )
    total_products = calculate_total_items(latest_run_products)
    total_sold = calculate_total_sold(latest_run_products)
    thirty_days_sold = calculate_sold_thirty_days(latest_run_products)
    seven_days_sold = calculate_sold_seven_days(latest_run_products)
    return render_template(
        "search.html",
        title="Dashboard",
        base="search",
        product_type=product_type,
        sort_type=map_sort(sort),
        sort=sort,
        products=products_page,
        first_run_date=first_run_date,
        total_products=total_products,
        total_sold=total_sold,
        thirty_days_sold=thirty_days_sold,
        seven_days_sold=seven_days_sold,
        form=SearchForm(),
    )
