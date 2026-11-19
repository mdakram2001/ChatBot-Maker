from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=2000,
        description="Question about the indexed website"
    )

    top_k: int = Field(default=4, ge=1, le=10)


class ChatResponse(BaseModel):
    question: str
    answer: str