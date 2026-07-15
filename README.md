# ResolveAI

> AI-powered customer support assistant using Retrieval-Augmented Generation (RAG).

## Status
🚧 Under active development
- v0.7 — Frontend and citations complete.

## Overview
ResolveAI answers customer support questions by retrieving relevant information 
from a company's knowledge base before generating a response — grounding answers 
in real documentation instead of hallucinating.

## Tech Stack
- **Backend:** Python 3.12+, FastAPI
- **AI:** Gemini API
- **Embeddings:** BAAI/bge-small-en-v1.5
- **Vector DB:** ChromaDB
- **Frontend:** React + Vite + Tailwind
- **Database:** SQLite
- **Deployment:** Docker

## Development Roadmap
- [x] v0.1 — Project scaffold
- [x] v0.2 — Document ingestion pipeline
- [x] v0.3 — Embeddings and vector storage
- [x] v0.4 — Retrieval engine
- [x] v0.5 — End-to-end RAG
- [x] v0.6 — FastAPI endpoints
- [x] v0.7 — Frontend and citations
- [ ] v1.0 — Production polish