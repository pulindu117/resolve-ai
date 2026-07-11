import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag.ingestion.loader import load_document
from app.rag.ingestion.chunker import chunk_document


def test_ingestion():
    doc = load_document("tests/sample.txt")
    print(f"\nDocument loaded: {doc.source}")
    print(f"Total characters: {len(doc.content)}")
    print(f"Type: {doc.doc_type}")

    chunks = chunk_document(doc, chunk_size=200, chunk_overlap=30)
    print(f"\nTotal chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i} ---")
        print(f"Characters: {chunk.start_char} → {chunk.end_char}")
        print(f"Content: {chunk.content}")


if __name__ == "__main__":
    test_ingestion()