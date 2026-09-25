import os
from typing import TypedDict

import chromadb
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, START, END

from support_assistant.models import AskResponse


MOCK_LLM = os.getenv("MOCK_LLM", "1")


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="support_assistant/chroma_db"
)

collection = client.get_collection(
    name="zepto_policies"
)


class State(TypedDict):
    query: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float


def validate_response(answer, sources, confidence):
    for attempt in range(3):
        try:
            response = AskResponse(
                answer=answer,
                sources=sources,
                confidence=confidence
            )

            return response

        except Exception as error:
            if attempt == 2:
                raise error


def classify_intent(state: State):
    query = state["query"].lower()

    policy_words = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours"
    ]

    is_policy_question = any(
        word in query for word in policy_words
    )

    if is_policy_question:
        intent = "policy_question"
    else:
        intent = "general_question"

    return {
        "intent": intent
    }


def retrieve_and_answer(state: State):
    query = state["query"]

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    documents = results["documents"][0]
    sources = results["ids"][0]

    top_chunk = documents[0]

    if MOCK_LLM == "1":

        answer = (
            "Based on the retrieved context: "
            + top_chunk[:200]
        )

        confidence = 1.0

    else:

        answer = (
            "Real LLM mode will be added later."
        )

        confidence = 1.0

    response = validate_response(
        answer,
        sources,
        confidence
    )

    return {
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence
    }


def direct_answer(state: State):

    if MOCK_LLM == "1":

        answer = (
            "I can only answer questions about "
            "Zepto policies right now."
        )

        confidence = 1.0

    else:

        answer = (
            "Real LLM mode will be added later."
        )

        confidence = 1.0

    response = validate_response(
        answer,
        [],
        confidence
    )

    return {
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence
    }


def route_question(state: State):

    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


graph = StateGraph(State)

graph.add_node(
    "classify_intent",
    classify_intent
)

graph.add_node(
    "retrieve_and_answer",
    retrieve_and_answer
)

graph.add_node(
    "direct_answer",
    direct_answer
)

graph.add_edge(
    START,
    "classify_intent"
)

graph.add_conditional_edges(
    "classify_intent",
    route_question,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)

graph.add_edge(
    "retrieve_and_answer",
    END
)

graph.add_edge(
    "direct_answer",
    END
)

app = graph.compile()


if __name__ == "__main__":

    print("MOCK_LLM:", MOCK_LLM)

    state1 = {
        "query": "What is the delivery charge?",
        "intent": "",
        "answer": "",
        "sources": [],
        "confidence": 0.0
    }

    result1 = app.invoke(state1)

    response1 = AskResponse(
        answer=result1["answer"],
        sources=result1["sources"],
        confidence=result1["confidence"]
    )

    print("\nPolicy question:")
    print(response1)

    state2 = {
        "query": "What is Python?",
        "intent": "",
        "answer": "",
        "sources": [],
        "confidence": 0.0
    }

    result2 = app.invoke(state2)

    response2 = AskResponse(
        answer=result2["answer"],
        sources=result2["sources"],
        confidence=result2["confidence"]
    )

    print("\nGeneral question:")
    print(response2)