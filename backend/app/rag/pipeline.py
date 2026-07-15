from app.rag.retrieval.retriever import retrieve, format_context
from app.rag.llm.gemini_client import generate_response


def run_rag_pipeline(
    query: str,
    top_k: int = 5,
    persist_dir: str = "./data/chroma",
) -> dict:
    """
    End-to-end RAG pipeline.

    1. Retrieve relevant chunks for the query
    2. Format them into a context string
    3. Send query + context to Claude
    4. Return the answer with source citations

    This is the function your API endpoint will call in Phase 6.
    """
    # Step 1: Retrieve
    results = retrieve(query=query, top_k=top_k, persist_dir=persist_dir)

    if not results:
        return {
            "answer": "I don't have enough information in my knowledge base to answer this question.",
            "sources": [],
            "query": query,
        }

    # Step 2: Format context
    context = format_context(results)

    # Step 3: Generate
    answer = generate_response(query=query, context=context)

    # Step 4: Extract sources for citation
    sources = list({result["metadata"]["source"] for result in results})

    return {
        "answer": answer,
        "sources": sources,
        "query": query,
        "chunks_used": len(results),
    }