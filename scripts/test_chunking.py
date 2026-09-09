from app.rag.loader import load_documents
from app.rag.chunking import (
    fixed_size_chunking,
    sentence_based_chunking
)


def main():

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")
    print()

    for document in documents:

        text = document["text"]
        source = document["source"]

        fixed_chunks = fixed_size_chunking(text)

        sentence_chunks = sentence_based_chunking(text)

        print(f"Document: {source}")
        print(f"  Fixed-size chunks: {len(fixed_chunks)}")
        print(f"  Sentence chunks:   {len(sentence_chunks)}")
        print()


if __name__ == "__main__":
    main()