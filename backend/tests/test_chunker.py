import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag.ingestion.models import Document
from app.rag.ingestion.chunker import chunk_document


def test_chunk_document_produces_chunks():
    doc = Document(content="A" * 1000, source="test.txt", doc_type="txt")
    chunks = chunk_document(doc, chunk_size=200, chunk_overlap=20)
    assert len(chunks) > 0


def test_chunks_respect_minimum_length():
    doc = Document(content="Short text here.", source="test.txt", doc_type="txt")
    chunks = chunk_document(doc, chunk_size=500, chunk_overlap=50)
    for chunk in chunks:
        assert len(chunk.content) > 0


def test_empty_document_produces_no_chunks():
    doc = Document(content="", source="empty.txt", doc_type="txt")
    chunks = chunk_document(doc, chunk_size=200, chunk_overlap=20)
    assert len(chunks) == 0


def test_chunk_indices_are_sequential():
    doc = Document(content="B" * 1000, source="test.txt", doc_type="txt")
    chunks = chunk_document(doc, chunk_size=200, chunk_overlap=20)
    indices = [c.chunk_index for c in chunks]
    assert indices == sorted(indices)