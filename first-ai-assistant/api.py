from pathlib import Path
from uuid import uuid4
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from baris_rag_chroma import (
    answer_question,
    collection,
    index_pdf,
    search_documents,
)

app = FastAPI(
    
    title="BARIS AI API",
    description="Local PDF RAG assistant powered by Ollama and ChromaDB",
    version="1.0.0",
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "BARIS AI",
        "indexed_chunks": collection.count(),
    }
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/documents")
def add_document(file: UploadFile = File(...)):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    saved_path = UPLOAD_DIR / f"{uuid4().hex}.pdf"

    try:
        content = file.file.read()

        if not content:
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")

        # Basic PDF signature check to reject obvious non-PDF uploads.
        if not content.startswith(b"%PDF"):
            raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF.")

        saved_path.write_bytes(content)
        chunk_count, _ = index_pdf(str(saved_path))

        return {
            "message": "PDF indexed successfully.",
            "original_filename": file.filename,
            "chunks_added_or_updated": chunk_count,
            "total_indexed_chunks": collection.count(),
        }

    except HTTPException:
        raise
    except Exception as error:
        if saved_path.exists():
            saved_path.unlink()
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/ask")
def ask_document(request: AskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if collection.count() == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents indexed yet. Upload a PDF first using POST /documents.",
        )

    try:
        matches = search_documents(question)
        answer = answer_question(question, matches)

        sources = [
            {
                "filename": item["source"],
                "page": item["page"],
            }
            for item in matches
        ]

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=False)
