import os
import chromadb
from chromadb.config import Settings
from backend.embeddings import embed_text

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)


def get_collection():
    return client.get_or_create_collection(
        name="architecture_patterns",
        metadata={"hnsw:space": "cosine"},
    )


def add_documents(docs: list[dict]):
    """
    docs: list of {"id": str, "text": str, "metadata": dict}
    """
    collection = get_collection()
    collection.add(
        ids=[d["id"] for d in docs],
        embeddings=[embed_text(d["text"]) for d in docs],
        documents=[d["text"] for d in docs],
        metadatas=[d.get("metadata", {}) for d in docs],
    )


def query_similar(query_embedding: list[float], n_results: int = 5) -> list[str]:
    collection = get_collection()
    count = collection.count()
    if count == 0:
        return []
    n_results = min(n_results, count)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    return results["documents"][0] if results["documents"] else []