# ResolveAI Architecture

## System overview
User → React Frontend (5173)
↓
FastAPI Backend (8000)
↓
┌──────────────────┐
│   RAG Pipeline   │
│                  │
│  1. Embed query  │
│  2. Search Chroma│
│  3. Build prompt │
│  4. Call Gemini  │
└──────────────────┘
↓
Answer + citations

## Ingestion pipeline
Raw file (PDF/MD/TXT)
↓
Loader — extracts clean text
↓
Chunker — splits into ~500 char overlapping chunks
↓
Embedder — BAAI/bge-small-en-v1.5 → 384-dim vectors
↓
ChromaDB — persists vectors + metadata

## Query pipeline
User question
↓
Embedder — same model as ingestion
↓
ChromaDB — cosine similarity search, top-k results
↓
Prompt builder — question + retrieved context
↓
Gemini API — generates grounded answer
↓
Response with source citations

## Key design decisions

| Decision | Choice | Reason |
|---|---|---|
| Chunking | Character-based with overlap | Simple, interpretable, no dependencies |
| Embeddings | BAAI/bge-small-en-v1.5 | Free, runs locally, strong performance |
| Vector DB | ChromaDB | Persistent, beginner-friendly, easy migration path |
| LLM | Pluggable (currently Gemini) | Swap providers by changing one file |
| Framework | No LangChain | Built from scratch to understand internals |