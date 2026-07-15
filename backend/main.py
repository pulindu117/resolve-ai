from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, documents

app = FastAPI(
    title="ResolveAI",
    description="AI-powered customer support assistant",
    version="0.6.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, tags=["chat"])
app.include_router(documents.router, tags=["documents"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.6.0"}