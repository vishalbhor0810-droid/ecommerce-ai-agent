from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embeddings(texts):
    """
    Convert text chunks into numerical vectors.
    """
    return model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )