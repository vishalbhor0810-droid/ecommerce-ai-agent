from app.rag.retriever import RAGRetriever


def main():

    retriever = RAGRetriever()

    queries = [
        "What is the return policy?",
        "How long does a refund take?",
        "How can I track my order?",
        "Can I cancel my order?",
        "What payment methods are supported?",
        "Tell me about the weather today."
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        results = retriever.search(
            query,
            strategy="sentence",
            top_k=3
        )

        for rank, result in enumerate(results, start=1):

            print(f"\nRank {rank}")
            print(f"Source     : {result['source']}")
            print(f"Similarity : {result['similarity']:.4f}")
            print(f"Text       : {result['text'][:200]}...")


if __name__ == "__main__":
    main()