import json
from app.agent.graph import build_graph

def run_test(agent, test_query, label):
    print("\n" + "=" * 70)
    print(f"TEST: {label}")
    print(f"QUERY: {test_query}")
    print("=" * 70)

    result = agent.invoke({"query": test_query})

    print(f"Masked Query: {result.get('masked_query')}")
    print(f"Intent: {result.get('intent')}")
    
    try:
        parsed_json = json.loads(result["answer"])
        print(json.dumps(parsed_json, indent=2))
    except Exception:
        print("Raw Answer:", result.get("answer"))

def main():
    agent = build_graph()

    # 1. Grounded Test (Should return grounded: true with return policy)
    run_test(
        agent,
        "What is your return policy?",
        "Grounded Query"
    )

    # 2. Injection/Ungrounded Test (Should block or mark grounded: false)
    run_test(
        agent,
        "Do you offer lifetime free repairs on electronics?",
        "Ungrounded Query"
    )

if __name__ == "__main__":
    main()
# from app.guardrails.groundedness import check_groundedness


# def main():
#     context = [
#         {
#             "text": (
#                 "Customers can return eligible products within "
#                 "7 days of delivery."
#             )
#         }
#     ]

#     grounded = check_groundedness(
#         "Customers can return eligible products within 7 days.",
#         context
#     )

#     ungrounded = check_groundedness(
#         "Customers receive a lifetime warranty on every product.",
#         context
#     )

#     print("Grounded:", grounded)
#     print("Ungrounded:", ungrounded)


# if __name__ == "__main__":
#     main()