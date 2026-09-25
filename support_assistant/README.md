# Zepto Support Assistant

## Overview

This module implements a small GenAI-style support assistant for Zepto.

The system:

- Loads Zepto policy documents
- Creates local embeddings using `all-MiniLM-L6-v2`
- Stores embeddings in ChromaDB
- Uses LangGraph to classify and route questions
- Retrieves relevant policy context for policy questions
- Produces structured responses using Pydantic
- Provides a FastAPI `/ask` endpoint
- Runs in deterministic mock mode without an API key
- Supports Docker

## Architecture

```text
Zepto Policy Documents
        ↓
Document Loading
        ↓
Sentence Transformer Embeddings
        ↓
ChromaDB
        ↓
User Query
        ↓
LangGraph
        ↓
Intent Classification
        ↓
   ┌───────────────┴───────────────┐
   ↓                               ↓
Policy Question              General Question
   ↓                               ↓
ChromaDB Retrieval            Direct Answer
   ↓                               ↓
Answer Generation             Fixed Mock Answer
   └───────────────┬───────────────┘
                   ↓
            Pydantic Response
                   ↓
              FastAPI /ask
```

## Main Components

- **Embeddings:** Sentence Transformers `all-MiniLM-L6-v2`
- **Vector Database:** ChromaDB
- **Workflow:** LangGraph
- **Validation:** Pydantic
- **API:** FastAPI
- **Deployment:** Docker
- **Default mode:** Deterministic mock mode using `MOCK_LLM=1`

## Files

```text
support_assistant/
├── README.md
├── docs/
├── chroma_db/
├── Dockerfile
├── create_docs.py
├── embed_documents.py
├── graph.py
├── main.py
├── models.py
├── prompt.py
└── test_retrieval.py
```

## How to Run

From the project root:

```bash
python support_assistant/embed_documents.py
python -m uvicorn support_assistant.main:api --reload --port 7860
```

The API endpoint is:

```text
POST /ask
```

Example request:

```json
{
  "query": "What is the return policy?"
}
```

The application can also be run using Docker.

## Design Decisions

Local embeddings and ChromaDB were used so that document retrieval works without an external API key. LangGraph provides the routing between policy retrieval and direct-answer paths.

The default mock mode makes the application deterministic and suitable for offline evaluation. The final response is validated using Pydantic before being returned through the FastAPI endpoint.