from app.tools.order_tool import get_order_status


def main():

    test_orders = [
        "ORD1001",
        "ORD1010",
        "ORD1020",
        "ORD9999"
    ]

    for order_id in test_orders:

        print("\n" + "=" * 50)
        print(f"ORDER: {order_id}")
        print("=" * 50)

        result = get_order_status(order_id)

        print(result)


if __name__ == "__main__":
    main()