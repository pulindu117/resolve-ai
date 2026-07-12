from typing import List
from sentence_transformers import SentenceTransformer

# Load once at module level — not on every function call.
# Loading a model is expensive (seconds). Embedding is cheap (milliseconds).
_MODEL_NAME = "BAAI/bge-small-en-v1.5"
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Return the embedding model, loading it on first call."""
    global _model
    if _model is None:
        print(f"Loading embedding model: {_MODEL_NAME}")
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def embed_text(text: str) -> List[float]:
    """
    Embed a single string and return a vector.
    Used for embedding a user's query at retrieval time.
    """
    model = get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Embed a list of strings in one batch and return a list of vectors.
    Used for embedding chunks during ingestion.
    Batching is faster than embedding one at a time.
    """
    model = get_model()
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    return vectors.tolist()