from app.models.schemas import AgentResponse


def main():
    response = AgentResponse(
        answer="Your order has been shipped.",
        source="order_tool",
        order_id="ORD1001",
        amount=2499.0,
        escalation_score=0.3,
        escalation_required=False
    )

    print("VALID RESPONSE:")
    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    main()