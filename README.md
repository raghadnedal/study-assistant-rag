# Study Assistant RAG

A backend-first Study Assistant built with FastAPI, PostgreSQL, pgvector, Sentence Transformers, and Groq.

## Features

- PDF upload
- Text extraction and chunking
- Local embeddings
- Vector search with pgvector
- RAG-based answers
- Source citations
- Chat sessions
- PostgreSQL chat history
- Document-scoped retrieval
- API validation and tests

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- pgvector
- Sentence Transformers
- Groq API
- pytest

## API Endpoints

- `GET /health`
- `POST /sessions`
- `POST /documents/upload`
- `POST /chat`

## Project Structure

```text
src/app/
├── chat/
├── llm/
├── rag/
├── db.py
└── main.py

tests/
└── test_api.py