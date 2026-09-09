import chromadb

from app.rag.loader import load_documents
from app.rag.chunking import (
    fixed_size_chunking,
    sentence_based_chunking
)
from app.rag.embeddings import create_embeddings


def build_collection(client, name, chunks):
    """
    Create a Chroma collection and store embeddings.
    """

    collection = client.get_or_create_collection(
        name=name,
        configuration={"hnsw": {"space": "cosine"}}
    )

    texts = [chunk["text"] for chunk in chunks]
    embeddings = create_embeddings(texts)

    ids = [chunk["id"] for chunk in chunks]
    metadatas = [
        {"source": chunk["source"]}
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return collection


def prepare_chunks(documents, strategy):
    chunks = []

    for document in documents:

        if strategy == "fixed":
            text_chunks = fixed_size_chunking(document["text"])

        else:
            text_chunks = sentence_based_chunking(document["text"])

        for index, text in enumerate(text_chunks):

            chunks.append({
                "id": f"{strategy}_{document['source']}_{index}",
                "source": document["source"],
                "text": text
            })

    return chunks


def main():

    documents = load_documents()

    client = chromadb.PersistentClient(
        path="data/vector_store"
    )

    fixed_chunks = prepare_chunks(
        documents,
        "fixed"
    )

    sentence_chunks = prepare_chunks(
        documents,
        "sentence"
    )

    fixed_collection = build_collection(
        client,
        "ecommerce_fixed",
        fixed_chunks
    )

    sentence_collection = build_collection(
        client,
        "ecommerce_sentence",
        sentence_chunks
    )

    print("=" * 50)
    print("VECTOR STORE BUILT")
    print("=" * 50)

    print(f"Documents       : {len(documents)}")
    print(f"Fixed chunks    : {len(fixed_chunks)}")
    print(f"Sentence chunks : {len(sentence_chunks)}")

    print()
    print(f"Fixed collection count    : {fixed_collection.count()}")
    print(f"Sentence collection count : {sentence_collection.count()}")

    print("=" * 50)


if __name__ == "__main__":
    main()