FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir sentence-transformers chromadb langgraph fastapi uvicorn pydantic

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

CMD ["uvicorn", "support_assistant.main:api", "--host", "0.0.0.0", "--port", "7860"]