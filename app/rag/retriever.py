from pathlib import Path

import chromadb

from app.rag.chunking import (
    fixed_size_chunking,
    sentence_based_chunking
)
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

    def add_document(self, source, text):
        """
        Chunk, embed and store a new document in both collections.
        Uses the same chunk IDs as scripts/build_vector_store.py.
        Returns the number of sentence chunks added.
        """

        strategies = [
            ("fixed", self.fixed_collection, fixed_size_chunking),
            ("sentence", self.sentence_collection, sentence_based_chunking),
        ]

        sentence_chunk_count = 0

        for strategy, collection, chunker in strategies:

            # Remove old chunks first in case this document is being updated
            collection.delete(where={"source": source})

            text_chunks = chunker(text)

            if not text_chunks:
                continue

            embeddings = create_embeddings(text_chunks)

            collection.upsert(
                ids=[
                    f"{strategy}_{source}_{index}"
                    for index in range(len(text_chunks))
                ],
                documents=text_chunks,
                embeddings=embeddings.tolist(),
                metadatas=[
                    {"source": source}
                    for _ in text_chunks
                ]
            )

            if strategy == "sentence":
                sentence_chunk_count = len(text_chunks)

        return sentence_chunk_count