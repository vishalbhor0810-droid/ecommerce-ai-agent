import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# Reproducibility
# --------------------------------------------------

SEED = 42
random.seed(SEED)


# --------------------------------------------------
# Dataset configuration
# --------------------------------------------------

NUM_ORDERS = 50
START_ORDER_ID = 1001

OUTPUT_DIR = Path("data/orders")
OUTPUT_FILE = OUTPUT_DIR / "orders.csv"


# --------------------------------------------------
# Sample e-commerce data
# --------------------------------------------------

CUSTOMERS = [
    ("Aarav Sharma", "aarav.sharma@example.com"),
    ("Vivaan Patel", "vivaan.patel@example.com"),
    ("Aditya Singh", "aditya.singh@example.com"),
    ("Arjun Mehta", "arjun.mehta@example.com"),
    ("Rohan Gupta", "rohan.gupta@example.com"),
    ("Kabir Verma", "kabir.verma@example.com"),
    ("Ishaan Kapoor", "ishaan.kapoor@example.com"),
    ("Rahul Joshi", "rahul.joshi@example.com"),
    ("Ananya Rao", "ananya.rao@example.com"),
    ("Diya Shah", "diya.shah@example.com"),
    ("Priya Nair", "priya.nair@example.com"),
    ("Sneha Iyer", "sneha.iyer@example.com"),
]

PRODUCTS = [
    ("Wireless Headphones", "Electronics", 2499),
    ("Smart Watch", "Electronics", 4999),
    ("Laptop Backpack", "Accessories", 1899),
    ("Running Shoes", "Footwear", 3299),
    ("Cotton T-Shirt", "Clothing", 899),
    ("Denim Jeans", "Clothing", 1999),
    ("Bluetooth Speaker", "Electronics", 2799),
    ("Coffee Maker", "Home Appliances", 3499),
    ("Air Fryer", "Home Appliances", 5999),
    ("Desk Lamp", "Home & Office", 1299),
    ("Yoga Mat", "Sports", 999),
    ("Water Bottle", "Sports", 699),
]

STATUSES = [
    "Processing",
    "Shipped",
    "Out for Delivery",
    "Delivered",
    "Cancelled",
    "Returned",
    "Refunded",
]


# --------------------------------------------------
# Generate orders
# --------------------------------------------------

def generate_orders():
    orders = []

    base_date = datetime(2026, 8, 1)

    for i in range(NUM_ORDERS):

        customer_name, contact = random.choice(CUSTOMERS)

        product_name, product_type, base_amount = random.choice(PRODUCTS)

        # Small random variation in product price
        amount = base_amount + random.randint(-100, 300)

        status = random.choice(STATUSES)

        order_date = base_date + timedelta(
            days=random.randint(0, 38)
        )

        order = {
            "order_id": f"ORD{START_ORDER_ID + i}",
            "customer_name": customer_name,
            "product_name": product_name,
            "product_type": product_type,
            "amount": amount,
            "status": status,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "contact": contact,
        }

        orders.append(order)

    return orders


# --------------------------------------------------
# Save dataset
# --------------------------------------------------

def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    orders = generate_orders()

    df = pd.DataFrame(orders)

    df.to_csv(OUTPUT_FILE, index=False)

    print("=" * 50)
    print("E-commerce order dataset generated")
    print("=" * 50)
    print(f"Records : {len(df)}")
    print(f"Columns : {', '.join(df.columns)}")
    print(f"Seed    : {SEED}")
    print(f"Saved   : {OUTPUT_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    main()