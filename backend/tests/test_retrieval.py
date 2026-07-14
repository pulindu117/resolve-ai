import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag.retrieval.retriever import retrieve, format_context


def test_retrieval():
    queries = [
        "What document types does ResolveAI support?",
        "How does ResolveAI prevent hallucination?",
        "What is a vector database?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 60)

        results = retrieve(query, top_k=2)
        context = format_context(results)

        print(context)
        print()


if __name__ == "__main__":
    test_retrieval()