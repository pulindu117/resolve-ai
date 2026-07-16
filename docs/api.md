# API Reference

Base URL: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

---

## POST /chat

Ask a question against the knowledge base.

**Request**
```json
{
  "query": "How do I reset my password?",
  "top_k": 5
}
```

**Response**
```json
{
  "answer": "To reset your password...",
  "sources": ["account-guide.md"],
  "query": "How do I reset my password?",
  "chunks_used": 3
}
```

---

## POST /upload

Upload a document to the knowledge base.

**Body:** `multipart/form-data` with a `file` field.

Accepted types: `.pdf`, `.md`, `.markdown`, `.txt`

**Response**
```json
{
  "source": "faq.md",
  "chunks_created": 12,
  "message": "Successfully ingested faq.md"
}
```

---

## GET /documents

List all indexed documents.

**Response**
```json
[
  {
    "source": "faq.md",
    "doc_type": "markdown",
    "chunk_count": 12
  }
]
```

---

## DELETE /documents/{source}

Remove a document and all its chunks from the knowledge base.

**Response**
```json
{
  "source": "faq.md",
  "chunks_deleted": 12,
  "message": "Deleted 12 chunks for faq.md"
}
```

---

## GET /health

Health check.

**Response**
```json
{
  "status": "ok",
  "version": "0.6.0"
}
```