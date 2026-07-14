from typing import List
from app.rag.embeddings.embedder import embed_text
from app.rag.vector_store.store import query_collection


def retrieve(
    query: str,
    top_k: int = 5,
    persist_dir: str = "./data/chroma",
) -> List[dict]:
    """
    Given a natural language query, find the most relevant chunks.

    Steps:
    1. Embed the query using the same model used during ingestion
    2. Search ChromaDB for the closest vectors
    3. Return ranked results with content and source metadata

    The same embedding model must be used for both ingestion and retrieval.
    If you embed chunks with model A and queries with model B, the vectors
    live in different spaces and similarity scores become meaningless.
    """
    query_vector = embed_text(query)

    results = query_collection(
        query_vector=query_vector,
        top_k=top_k,
        persist_dir=persist_dir,
    )

    return results


def format_context(results: List[dict]) -> str:
    """
    Format retrieved chunks into a single context string for the LLM prompt.

    Each chunk is labelled with its source so the LLM can cite it.
    The format matters — clear separation between chunks helps the LLM
    distinguish where one source ends and another begins.
    """
    context_parts = []

    for i, result in enumerate(results):
        source = result["metadata"]["source"]
        content = result["content"]
        context_parts.append(f"[Source {i + 1}: {source}]\n{content}")

    return "\n\n---\n\n".join(context_parts)