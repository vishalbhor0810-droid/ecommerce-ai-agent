from pathlib import Path

import chromadb

from app.rag.embeddings import create_embeddings


VECTOR_STORE_PATH = Path("data/vector_store")


class RAGRetriever:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(VECTOR_STORE_PATH)
        )

        self.fixed_collection = self.client.get_collection(
            name="ecommerce_fixed"
        )

        self.sentence_collection = self.client.get_collection(
            name="ecommerce_sentence"
        )

    def search(self, query, strategy="sentence", top_k=3):

        query_embedding = create_embeddings([query])[0]

        if strategy == "fixed":
            collection = self.fixed_collection
        else:
            collection = self.sentence_collection

        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        retrieved = []

        for i in range(len(results["documents"][0])):

            retrieved.append({
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "distance": results["distances"][0][i],
                "similarity": 1 - results["distances"][0][i]
            })

        return retrieved