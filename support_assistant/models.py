from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)


if __name__ == "__main__":
    response = AskResponse(
        answer="Test answer",
        sources=["doc_01"],
        confidence=1.0
    )

    print(response)