from app.tools.order_tool import get_order_status


def main():
    for order_id in ["ORD1001", "ORD1002"]:
        result = get_order_status(order_id)

        print("=" * 40)
        print("Order:", order_id)
        print(result)


if __name__ == "__main__":
    main()