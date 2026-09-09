from app.rag.pipeline import answer_query
from app.rag.retriever import RAGRetriever
from app.guardrails.groundedness import check_groundedness


def evaluate_query(query: str):
    retriever = RAGRetriever()
    results = retriever.search(query, strategy="sentence", top_k=3)

    # Get pipeline answer (returns a dict with {"answer": "...", "source": "...", ...})
    response = answer_query(query)

    # Extract the answer string safely
    if isinstance(response, dict):
        answer_text = response.get("answer", "")
    else:
        answer_text = str(response)

    # Calculate metrics
    context_relevance = (
        sum(r["similarity"] for r in results) / len(results)
        if results else 0.0
    )

    # Pass the string 'answer_text' instead of the dictionary 'response'
    grounded = check_groundedness(answer_text, results)

    answer_relevance = 1.0 if results and results[0]["similarity"] >= 0.3802 else 0.0

    return {
        "query": query,
        "context_relevance": round(context_relevance, 4),
        "groundedness": float(grounded),
        "answer_relevance": answer_relevance
    }