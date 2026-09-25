

This module implements a small GenAI-style support assistant for Zepto.

The system:

1. Loads Zepto policy documents.
2. Creates local embeddings using `all-MiniLM-L6-v2`.
3. Stores the embeddings in ChromaDB.
4. Uses LangGraph to classify and route user questions.
5. Retrieves relevant policy documents for policy questions.
6. Produces a structured response using Pydantic.
7. Provides a FastAPI `/ask` endpoint.
8. Runs locally in deterministic mock mode without an API key.
9. Can also be run using Docker.

---


The overall data flow is:

```text
Policy Documents
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