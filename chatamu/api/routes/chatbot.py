from fastapi import APIRouter, HTTPException

from chatamu.api.schemas.chatbot_schema import (
    ChatRequest,
    ChatResponse,
)
from chatamu.api.routes import website
from chatamu.core.rag import ask_question

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    if website.active_website_url is None:
        raise HTTPException(
            status_code=400,
            detail="Please index a website before asking questions.",
        )

    try:
        answer = ask_question(
            question=request.question,
            top_k=request.top_k,
        )

        return ChatResponse(
            question=request.question,
            answer=answer,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate answer: {str(exc)}",
        ) from exc