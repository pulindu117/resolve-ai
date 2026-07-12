import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag.ingestion.loader import load_document
from app.rag.ingestion.chunker import chunk_document
from app.rag.embeddings.embedder import embed_texts, embed_text
from app.rag.vector_store.store import add_chunks, query_collection


def test_vector_store():
    # Full pipeline: load → chunk → embed → store → query
    doc = load_document("tests/sample.txt")
    chunks = chunk_document(doc, chunk_size=200, chunk_overlap=30)

    texts = [chunk.content for chunk in chunks]
    vectors = embed_texts(texts)

    # Store in ChromaDB
    add_chunks(chunks, vectors, persist_dir="./data/chroma")

    # Query with a natural language question
    query = "What document types does ResolveAI support?"
    query_vector = embed_text(query)

    results = query_collection(query_vector, top_k=2, persist_dir="./data/chroma")

    print(f"\nQuery: {query}")
    print(f"Top {len(results)} results:\n")

    for i, result in enumerate(results):
        print(f"--- Result {i + 1} ---")
        print(f"Source: {result['metadata']['source']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Content: {result['content'][:150]}...")
        print()


if __name__ == "__main__":
    test_vector_store()