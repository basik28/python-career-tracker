# BARIS AI — Local AI Document Assistant

BARIS AI is a local document-question-answering prototype built with Python, FastAPI, Ollama, Qwen, and ChromaDB.

## Features

- Upload PDF documents through a web interface.
- Extract text and split it into overlapping chunks.
- Generate embeddings locally with Ollama (`embeddinggemma`).
- Store document chunks in a persistent ChromaDB collection.
- Retrieve relevant chunks for a question and generate an answer with Qwen.
- Return source filenames and page numbers with answers.

## Architecture

```text
Browser (HTML/CSS/JavaScript)
          |
          v
      FastAPI
       /   \
      v     v
 ChromaDB  Ollama
 vectors  embeddings + Qwen
```

## Requirements

- Python 3.10+
- Ollama installed and running
- Models downloaded:

```bash
ollama pull qwen2.5:3b
ollama pull embeddinggemma
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Place the application files in the project root:

- `api.py`
- `baris_rag_chroma.py`
- `static/index.html`

Start the API:

```bash
python api.py
```

Open:

- Web app: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Important privacy note

This project is configured for local development. Do not commit private PDFs, `uploads/`, `chroma_db/`, `.env` files, API keys, or personal conversation data to GitHub. The `.gitignore` excludes common local data paths.

## Current limitations

- PDF text extraction does not perform OCR on scanned/image-only PDFs.
- The current prototype does not include authentication or per-user document isolation.
- The local development server is bound to `127.0.0.1`; it is not configured for public production deployment.
- Answers can be incorrect; verify important information against the cited source pages.

## Roadmap

- Authentication and per-user document access
- Better chunking and retrieval evaluation
- Streaming responses and chat history
- Automated tests and deployment
