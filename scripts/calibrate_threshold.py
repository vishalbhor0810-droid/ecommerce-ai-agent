from app.rag.retriever import RAGRetriever


def main():

    retriever = RAGRetriever()

    # Queries that SHOULD be answered using our knowledge base
    in_scope_queries = [
        "What is the return policy?",
        "How long does a refund take?",
        "How can I track my order?",
        "Can I cancel my order?",
        "What payment methods are supported?",
        "Can I exchange a product?",
    ]

    # Queries that SHOULD NOT be answered using our knowledge base
    out_of_scope_queries = [
        "Tell me about the weather today.",
        "Who is the Prime Minister of India?",
        "What is the capital of France?",
        "How do I learn Python?",
    ]

    print("=" * 70)
    print("THRESHOLD CALIBRATION")
    print("=" * 70)

    print("\nIN-SCOPE QUERIES")
    print("-" * 70)

    in_scope_scores = []

    for query in in_scope_queries:

        results = retriever.search(
            query,
            strategy="sentence",
            top_k=1
        )

        score = results[0]["similarity"]
        source = results[0]["source"]

        in_scope_scores.append(score)

        print(f"Query : {query}")
        print(f"Score : {score:.4f}")
        print(f"Source: {source}")
        print()

    print("\nOUT-OF-SCOPE QUERIES")
    print("-" * 70)

    out_scope_scores = []

    for query in out_of_scope_queries:

        results = retriever.search(
            query,
            strategy="sentence",
            top_k=1
        )

        score = results[0]["similarity"]
        source = results[0]["source"]

        out_scope_scores.append(score)

        print(f"Query : {query}")
        print(f"Score : {score:.4f}")
        print(f"Source: {source}")
        print()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"Highest out-of-scope score : {max(out_scope_scores):.4f}")
    print(f"Lowest in-scope score      : {min(in_scope_scores):.4f}")

    # Candidate threshold
    threshold = (
        max(out_scope_scores) +
        min(in_scope_scores)
    ) / 2

    print(f"\nCandidate threshold        : {threshold:.4f}")

    print("=" * 70)


if __name__ == "__main__":
    main()