from pathlib import Path
from typing import List, Dict


KB_PATH = Path("data/knowledge_base")


def load_documents() -> List[Dict[str, str]]:
    """
    Load all Markdown knowledge-base documents.
    """

    documents = []

    for file_path in sorted(KB_PATH.glob("*.md")):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents