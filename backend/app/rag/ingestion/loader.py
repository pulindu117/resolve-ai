import re
from pathlib import Path
from app.rag.ingestion.models import Document


def load_document(file_path: str) -> Document:
    """
    Load a file from disk and extract its text content.
    Supports PDF, Markdown, and plain text.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return _load_pdf(path)
    elif suffix in (".md", ".markdown"):
        return _load_markdown(path)
    elif suffix == ".txt":
        return _load_text(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def _load_pdf(path: Path) -> Document:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text.strip())

    content = "\n\n".join(pages)

    return Document(
        content=content,
        source=path.name,
        doc_type="pdf",
        metadata={"page_count": len(reader.pages)},
    )


def _load_markdown(path: Path) -> Document:
    content = path.read_text(encoding="utf-8")

    # Strip markdown syntax for cleaner embedding
    # Remove code blocks, headers markers, bold/italic
    content = re.sub(r"```[\s\S]*?```", "", content)
    content = re.sub(r"#{1,6}\s", "", content)
    content = re.sub(r"\*\*?(.*?)\*\*?", r"\1", content)
    content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", content)
    content = re.sub(r"\n{3,}", "\n\n", content).strip()

    return Document(
        content=content,
        source=path.name,
        doc_type="markdown",
        metadata={},
    )


def _load_text(path: Path) -> Document:
    content = path.read_text(encoding="utf-8").strip()

    return Document(
        content=content,
        source=path.name,
        doc_type="txt",
        metadata={},
    )