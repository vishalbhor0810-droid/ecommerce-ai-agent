import json
from app.agent.graph import build_graph

def main():
    agent = build_graph()

    test_query = "My email is test@example.com and my phone is 9876543210. What is your return policy?"

    print("\n" + "=" * 70)
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

if __name__ == "__main__":
    main()