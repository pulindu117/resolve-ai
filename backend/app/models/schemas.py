from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    query: str
    chunks_used: int


class DocumentInfo(BaseModel):
    source: str
    doc_type: str
    chunk_count: int


class UploadResponse(BaseModel):
    source: str
    chunks_created: int
    message: str


class DeleteResponse(BaseModel):
    source: str
    chunks_deleted: int
    message: str