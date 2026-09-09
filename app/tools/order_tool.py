import pandas as pd
from pathlib import Path


ORDERS_FILE = Path("data/orders/orders.csv")


def calculate_escalation_score(status, amount):
    """
    Calculate escalation score from order status and amount.

    Formula:
        score = status_score + amount_score

    Status contribution:
        Returned / Refunded  -> 0.4
        Cancelled            -> 0.3
        Out for Delivery     -> 0.2
        Processing / Shipped -> 0.1
        Delivered            -> 0.0

    Amount contribution:
        amount >= 5000 -> 0.4
        amount >= 2000 -> 0.2
        amount < 2000  -> 0.0

    Maximum score = 0.8
    """

    status_scores = {
        "Returned": 0.4,
        "Refunded": 0.4,
        "Cancelled": 0.3,
        "Out for Delivery": 0.2,
        "Processing": 0.1,
        "Shipped": 0.1,
        "Delivered": 0.0,
    }

    status_score = status_scores.get(status, 0.2)

    if amount >= 5000:
        amount_score = 0.4
    elif amount >= 2000:
        amount_score = 0.2
    else:
        amount_score = 0.0

    return round(status_score + amount_score, 2)


def get_order_status(order_id):
    """
    Retrieve order information from the order dataset.
    """

    df = pd.read_csv(ORDERS_FILE)

    order = df[df["order_id"] == order_id]

    if order.empty:
        return {
            "found": False,
            "order_id": order_id,
            "message": "Order not found."
        }

    row = order.iloc[0]

    status = row["status"]
    amount = float(row["amount"])

    escalation_score = calculate_escalation_score(
        status,
        amount
    )

    return {
        "found": True,
        "order_id": order_id,
        "status": status,
        "amount": amount,
        "escalation_score": escalation_score
    }