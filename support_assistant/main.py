from fastapi import FastAPI
from support_assistant.models import AskRequest, AskResponse
from support_assistant.graph import app

api = FastAPI()

@api.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):

    state = {
        "query": request.query,
        "intent": "",
        "answer": "",
        "sources": [],
        "confidence": 0.0
    }

    result = app.invoke(state)

    response = AskResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )

    return response
