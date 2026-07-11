from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Document:
    """A raw document loaded from disk before chunking."""
    content: str                    # full extracted text
    source: str                     # original filename
    doc_type: str                   # "pdf", "markdown", "txt"
    metadata: dict = field(default_factory=dict)


@dataclass
class Chunk:
    """A single piece of a document, ready for embedding."""
    content: str                    # the actual text of this chunk
    source: str                     # which file it came from
    chunk_index: int                # position within the document
    start_char: int                 # character offset in original doc
    end_char: int                   # character offset in original doc
    doc_type: str                   # inherited from parent document
    metadata: dict = field(default_factory=dict)