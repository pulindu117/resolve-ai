from app.rag.ingestion.loader import load_document
from app.rag.ingestion.chunker import chunk_document
from app.rag.embeddings.embedder import embed_texts
from app.rag.vector_store.store import add_chunks


def ingest_file(file_path: str, chunk_size: int = 500, chunk_overlap: int = 50) -> dict:
    """
    Full ingestion pipeline for a single file: load → chunk → embed → store.
    Returns metadata about what was ingested.
    """
    document = load_document(file_path)
    chunks = chunk_document(document, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    if not chunks:
        return {"source": document.source, "chunks_created": 0}

    texts = [chunk.content for chunk in chunks]
    vectors = embed_texts(texts)

    add_chunks(chunks, vectors)

    return {"source": document.source, "chunks_created": len(chunks)}