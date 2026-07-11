from typing import List
from app.rag.ingestion.models import Document, Chunk


def chunk_document(
    document: Document,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[Chunk]:
    """
    Split a document into overlapping chunks.

    chunk_size: target number of characters per chunk
    chunk_overlap: how many characters to repeat between chunks

    Why overlap? If a sentence is split across two chunks, overlap
    ensures neither chunk loses the context from the boundary.
    """
    text = document.content
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size

        # Don't cut mid-word — walk end forward to next whitespace
        if end < len(text):
            while end < len(text) and not text[end].isspace():
                end += 1

        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(
                Chunk(
                    content=chunk_text,
                    source=document.source,
                    chunk_index=chunk_index,
                    start_char=start,
                    end_char=end,
                    doc_type=document.doc_type,
                    metadata=document.metadata.copy(),
                )
            )
            chunk_index += 1

        # Move start forward, but overlap with previous chunk
        start = end - chunk_overlap

    return chunks