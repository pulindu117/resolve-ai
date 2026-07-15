import chromadb
from chromadb.config import Settings
from typing import List
from app.rag.ingestion.models import Chunk


def get_client(persist_dir: str = "./data/chroma") -> chromadb.ClientAPI:
    """
    Return a persistent ChromaDB client.
    Data is saved to disk so it survives restarts.
    """
    import os
    os.makedirs(persist_dir, exist_ok=True)

    return chromadb.PersistentClient(
        path=persist_dir,
        settings=Settings(anonymized_telemetry=False),
    )


def get_collection(client: chromadb.ClientAPI, name: str = "resolveai"):
    """
    Get or create a ChromaDB collection.
    A collection is like a table — it holds your vectors and metadata.
    """
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(
    chunks: List[Chunk],
    vectors: List[List[float]],
    persist_dir: str = "./data/chroma",
) -> None:
    """
    Store chunks and their vectors in ChromaDB.
    Each chunk needs a unique ID, its vector, its text, and metadata.
    """
    client = get_client(persist_dir)
    collection = get_collection(client)

    ids = [f"{chunk.source}_{chunk.chunk_index}" for chunk in chunks]
    documents = [chunk.content for chunk in chunks]
    metadatas = [
        {
            "source": chunk.source,
            "chunk_index": chunk.chunk_index,
            "start_char": chunk.start_char,
            "end_char": chunk.end_char,
            "doc_type": chunk.doc_type,
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")


def query_collection(
    query_vector: List[float],
    top_k: int = 5,
    persist_dir: str = "./data/chroma",
) -> List[dict]:
    """
    Find the top_k most similar chunks to a query vector.
    Returns a list of results with content, source, and similarity score.
    """
    client = get_client(persist_dir)
    collection = get_collection(client)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    output = []
    for i in range(len(results["ids"][0])):
        output.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return output


def delete_document(source: str, persist_dir: str = "./data/chroma") -> int:
    """
    Delete all chunks belonging to a specific source document.
    Returns the number of chunks deleted.
    """
    client = get_client(persist_dir)
    collection = get_collection(client)

    results = collection.get(where={"source": source})

    if results["ids"]:
        collection.delete(ids=results["ids"])
        return len(results["ids"])
    return 0



def list_documents(persist_dir: str = "./data/chroma") -> List[dict]:
    """
    Return a summary of all unique documents currently in the store,
    grouped by source with their chunk counts.
    """
    client = get_client(persist_dir)
    collection = get_collection(client)

    all_items = collection.get(include=["metadatas"])

    summary = {}
    for metadata in all_items["metadatas"]:
        source = metadata["source"]
        doc_type = metadata["doc_type"]
        if source not in summary:
            summary[source] = {"source": source, "doc_type": doc_type, "chunk_count": 0}
        summary[source]["chunk_count"] += 1

    return list(summary.values())