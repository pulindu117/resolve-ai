import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag.pipeline import run_rag_pipeline


def test_pipeline():
    queries = [
        "What document types does ResolveAI support?",
        "How does ResolveAI prevent hallucination?",
        "What is the pricing for ResolveAI?",  # not in knowledge base
    ]

    for query in queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)

        result = run_rag_pipeline(query, top_k=3)

        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print(f"Chunks used: {result['chunks_used']}")


if __name__ == "__main__":
    test_pipeline()