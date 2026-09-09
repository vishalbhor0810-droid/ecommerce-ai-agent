import pandas as pd
from eval.rag_triad import evaluate_query


def main():
    df = pd.read_csv("data/evaluation/rag_queries.csv")

    results = []

    for _, row in df.iterrows():
        result = evaluate_query(row["query"])
        results.append(result)

    output = pd.DataFrame(results)

    output.to_csv(
        "data/evaluation/rag_triad_results.csv",
        index=False
    )

    print("\nRAG TRIAD RESULTS")
    print("=" * 40)

    print(
        "Context Relevance:",
        round(output["context_relevance"].mean(), 4)
    )

    print(
        "Groundedness:",
        round(output["groundedness"].mean(), 4)
    )

    print(
        "Answer Relevance:",
        round(output["answer_relevance"].mean(), 4)
    )

    print("\nSaved to:")
    print("data/evaluation/rag_triad_results.csv")


if __name__ == "__main__":
    main()