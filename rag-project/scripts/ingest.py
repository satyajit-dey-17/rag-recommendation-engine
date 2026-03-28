import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from dotenv import load_dotenv
from backend.rag import get_collection
from backend.embeddings import embed_text

load_dotenv()

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "architecture_docs")


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 30) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def ingest_docs():
    collection = get_collection()

    # Wipe existing documents before re-ingesting
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])
        print(f"Cleared {len(existing['ids'])} existing chunks from ChromaDB.")

    docs = []
    for filename in os.listdir(DOCS_DIR):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(DOCS_DIR, filename)
        with open(filepath, "r") as f:
            text = f.read()

        provider = filename.replace(".md", "")
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"{provider}_chunk_{i}",
                "text": chunk,
                "metadata": {
                    "provider": provider,
                    "source": filename,
                    "chunk_index": i,
                },
            })

        print(f"Loaded {len(chunks)} chunks from {filename}")

    # Add all documents in one batch
    collection.add(
        ids=[d["id"] for d in docs],
        embeddings=[embed_text(d["text"]) for d in docs],
        documents=[d["text"] for d in docs],
        metadatas=[d.get("metadata", {}) for d in docs],
    )

    print(f"\nSuccessfully ingested {len(docs)} total chunks into ChromaDB.")


if __name__ == "__main__":
    ingest_docs()