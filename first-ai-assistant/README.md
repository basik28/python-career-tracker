# BARIS AI — Local AI Document Assistant

A locally running AI document assistant built with Python, Ollama, FastAPI, and ChromaDB.

BARIS AI allows users to upload PDF documents, retrieve relevant information, and ask questions using a local Large Language Model (LLM).

## Features

- **Local AI Chat:** Interact with a locally hosted language model.
- **PDF Analysis:** Extract and analyze text from PDF documents.
- **Retrieval-Augmented Generation (RAG):** Retrieve relevant document chunks before generating answers.
- **Vector Database:** Store and search document embeddings with ChromaDB.
- **REST API:** Access the application through FastAPI.
- **Web Interface:** Upload PDFs and ask questions through a simple browser interface.
- **Persistent Storage:** Keep indexed document embeddings between sessions.

## Technology Stack

- Python
- Ollama
- Qwen 2.5 3B
- EmbeddingGemma
- ChromaDB
- FastAPI
- HTML, CSS, JavaScript

## Project Structure

```text
first-ai-assistant/
├── static/
│   └── index.html
├── api.py
├── baris_rag_chroma.py
├── calculator.py
├── list_models.py
├── main.py
├── pdf_analyzer.py
├── rag_pdf.py
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama

Download Ollama:

https://ollama.com/

### 3. Download the required models

```bash
ollama pull qwen2.5:3b
ollama pull embeddinggemma
```

### 4. Start the application

```bash
python api.py
```

### 5. Open the application

Open your browser and visit:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API status |
| POST | `/documents` | Upload and index PDF documents |
| POST | `/ask` | Ask questions about indexed documents |

## What I Learned

Through this project, I practiced:

- Python application development
- Working with local LLMs
- API integration
- REST API development
- Vector databases and embeddings
- Retrieval-Augmented Generation (RAG)
- Document processing
- Building a simple AI-powered web application

## Future Improvements

- User authentication
- Better document management
- Improved retrieval quality
- Support for additional document formats
- Cloud deployment

## Developer

**BARIS AI** — A personal AI engineering portfolio project.

Built as part of my journey toward becoming an AI Automation Engineer and AI Application Developer.
