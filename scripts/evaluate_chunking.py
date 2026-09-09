import csv

from app.rag.retriever import RAGRetriever


TOP_K = 3


def evaluate_strategy(retriever, queries, strategy):

    total_relevant_retrieved = 0
    total_retrieved = 0
    total_relevant_documents = len(queries)

    correct_queries = 0

    print("\n" + "=" * 70)
    print(f"STRATEGY: {strategy}")
    print("=" * 70)

    for item in queries:

        query = item["query"]
        expected_source = item["expected_source"]

        results = retriever.search(
            query,
            strategy=strategy,
            top_k=TOP_K
        )

        # Remove duplicate source documents.
        retrieved_sources = []

        for result in results:
            source = result["source"]

            if source not in retrieved_sources:
                retrieved_sources.append(source)

        relevant_count = sum(
            1
            for source in retrieved_sources
            if source == expected_source
        )

        if expected_source in retrieved_sources:
            correct_queries += 1

        total_relevant_retrieved += relevant_count
        total_retrieved += len(retrieved_sources)

        print(f"\nQuery: {query}")
        print(f"Expected: {expected_source}")
        print(f"Retrieved: {retrieved_sources}")
        print(
            f"Correct: "
            f"{'YES' if expected_source in retrieved_sources else 'NO'}"
        )

    precision = (
        total_relevant_retrieved / total_retrieved
        if total_retrieved
        else 0
    )

    recall = (
        correct_queries / total_relevant_documents
        if total_relevant_documents
        else 0
    )

    print("\n" + "-" * 70)
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")

    return precision, recall


def load_queries():

    queries = []

    with open(
        "data/evaluation/rag_queries.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            queries.append(row)

    return queries


def main():

    retriever = RAGRetriever()
    queries = load_queries()

    fixed_precision, fixed_recall = evaluate_strategy(
        retriever,
        queries,
        "fixed"
    )

    sentence_precision, sentence_recall = evaluate_strategy(
        retriever,
        queries,
        "sentence"
    )

    print("\n" + "=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)

    print(
        f"Fixed-size     → "
        f"Precision: {fixed_precision:.4f}, "
        f"Recall: {fixed_recall:.4f}"
    )

    print(
        f"Sentence-based → "
        f"Precision: {sentence_precision:.4f}, "
        f"Recall: {sentence_recall:.4f}"
    )


if __name__ == "__main__":
    main()