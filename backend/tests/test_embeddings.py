import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag.ingestion.loader import load_document
from app.rag.ingestion.chunker import chunk_document
from app.rag.embeddings.embedder import embed_text, embed_texts


def test_embeddings():
    # Load and chunk the sample document
    doc = load_document("tests/sample.txt")
    chunks = chunk_document(doc, chunk_size=200, chunk_overlap=30)

    print(f"Chunks to embed: {len(chunks)}")

    # Embed all chunks in one batch
    texts = [chunk.content for chunk in chunks]
    vectors = embed_texts(texts)

    print(f"Vectors produced: {len(vectors)}")
    print(f"Vector dimensions: {len(vectors[0])}")
    print(f"First vector (first 5 values): {vectors[0][:5]}")

    # Embed a query and verify same dimensions
    query = "What document types does ResolveAI support?"
    query_vector = embed_text(query)
    print(f"\nQuery vector dimensions: {len(query_vector)}")
    print(f"Query vector (first 5 values): {query_vector[:5]}")

    # Quick sanity check: similar texts should produce similar vectors
    # We do this by computing dot product (cosine similarity when normalized)
    import numpy as np
    similarity = np.dot(query_vector, vectors[2])  # chunk 2 mentions doc types
    print(f"\nSimilarity between query and chunk 2: {similarity:.4f}")
    print("(Higher = more similar. Should be noticeably above 0.)")


if __name__ == "__main__":
    test_embeddings()