from main import app, db, scheduler
from main.get_products import (
    request_proxy_list,
    request_products_from_api,
    write_products_to_db,
)


def update_products():
    """
    Gets the current product data from Getic's API and updates the database.
    """
    print("Updating products...")
    # proxies = request_proxy_list()
    products = request_products_from_api()
    with app.app_context():
        write_products_to_db(db, products)
        print("Products updated...")


"""
# Schedules product data to be updated each day at the specified time
scheduler.add_job(update_products, "cron", timezone="utc", hour="8")
scheduler.start()
"""

if __name__ == "__main__":
    app.run(debug=True)
