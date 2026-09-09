from app.rag.retriever import RAGRetriever
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

RAG_THRESHOLD = 0.3802
MODEL_NAME = "openai/gpt-oss-120b"


class RAGPipeline:
    def __init__(self):
        self.retriever = RAGRetriever()
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def answer_query(self, query: str):
        # Step 1: Retrieve context
        results = self.retriever.search(query, strategy="sentence", top_k=3)

        # Step 2: Check threshold
        if not results:
            return {
                "answer": "I could not find relevant information in the knowledge base.",
                "source": None,
                "similarity": 0.0
            }

        best_result = results[0]

        if best_result["similarity"] < RAG_THRESHOLD:
            return {
                "answer": (
                    "I’m sorry, but I don’t have enough information "
                    "in my knowledge base to answer that question."
                ),
                "source": None,
                "similarity": best_result["similarity"]
            }

        # Step 3: Build context
        context = "\n\n".join(
            [
                f"Source: {result['source']}\n"
                f"{result['text']}"
                for result in results
            ]
        )

        # Step 4: Ask Groq using retrieved context
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a ShopEase e-commerce customer "
                        "support assistant.\n\n"
                        "Answer the user's question ONLY using "
                        "the provided knowledge base context.\n"
                        "Do not invent information.\n"
                        "If the context does not contain enough "
                        "information, say that you do not have "
                        "enough information."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Knowledge Base Context:\n\n"
                        f"{context}\n\n"
                        f"User Question:\n{query}"
                    )
                }
            ]
        )

        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "source": best_result["source"],
            "similarity": best_result["similarity"]
        }


# Module-level helper function for direct imports
def answer_query(query: str):
    pipeline = RAGPipeline()
    return pipeline.answer_query(query)