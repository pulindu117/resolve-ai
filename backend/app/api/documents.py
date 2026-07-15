import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import UploadResponse, DeleteResponse, DocumentInfo
from app.rag.ingestion_pipeline import ingest_file
from app.rag.vector_store.store import list_documents, delete_document

router = APIRouter()

UPLOAD_DIR = "./data/uploads"


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".md", ".markdown", ".txt"}
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {allowed_extensions}",
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = ingest_file(file_path)

    return UploadResponse(
        source=result["source"],
        chunks_created=result["chunks_created"],
        message=f"Successfully ingested {result['source']}",
    )


@router.get("/documents", response_model=list[DocumentInfo])
async def get_documents():
    docs = list_documents()
    return [DocumentInfo(**doc) for doc in docs]


@router.delete("/documents/{source}", response_model=DeleteResponse)
async def remove_document(source: str):
    deleted_count = delete_document(source)

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"No document found: {source}")

    return DeleteResponse(
        source=source,
        chunks_deleted=deleted_count,
        message=f"Deleted {deleted_count} chunks for {source}",
    )