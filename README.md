# DeepRead RAG Service

---

Async RAG (Retrieval-Augmented Generation) service built with FastAPI, PostgreSQL, Qdrant and Ollama.

---

## Info
The service allows users to:

- upload text documents
- split documents into semantic chunks
- generate embeddings
- store vectors in Qdrant
- retrieve relevant context
- ask questions about uploaded documents using LLM

With default settings, the service works fully locally using Ollama models.

This can be useful for:
- private data processing
- offline usage
- local document storage

The behavior can also be changed to work with external API-based models.

---

## Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy Async
- Alembic
- Qdrant
- Ollama
- LangChain
- Docker Compose
- Ruff
- MyPy

---

## Run Project

To run project:

1. Clone repository

```bash
git clone https://github.com/AlexandrSmolyachkovGH/deep_read_rag.git
```

2. Create .env file

```bash
cp .env_example .env
```

3. Run docker compose build and up
4.
```bash
docker compose up --build
```

---
