import re
from typing import List


def fixed_size_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> List[str]:
    """
    Split text into fixed-size character chunks
    with a specified overlap.
    """

    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def sentence_based_chunking(
    text: str,
    sentences_per_chunk: int = 3
) -> List[str]:
    """
    Split text into chunks containing a fixed number
    of complete sentences.
    """

    # Split on sentence-ending punctuation.
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    chunks = []

    for i in range(0, len(sentences), sentences_per_chunk):

        chunk_sentences = sentences[
            i:i + sentences_per_chunk
        ]

        chunk = " ".join(chunk_sentences)

        if chunk:
            chunks.append(chunk)

    return chunks