from app.rag.pipeline import RAGPipeline
from dotenv import load_dotenv

load_dotenv()  # Yeh .env file se keys load kar leta hai

def main():

    rag = RAGPipeline()

    queries = [
        "What is the return policy?",
        "How long does a refund take?",
        "How can I track my order?",
        "Can I cancel my order?",
        "What payment methods are supported?",
        "Tell me about the weather today.",
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print(f"QUESTION: {query}")
        print("=" * 70)

        result = rag.answer(query)

        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Source: {result['source']}")

        print("\nANSWER:")
        print(result["answer"])


if __name__ == "__main__":
    main()