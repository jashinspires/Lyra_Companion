"""Chat endpoint for conversational support."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ...schemas.chat import ChatRequest, ChatResponse
from ...services.conversation import conversation_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "/session",
    response_model=ChatResponse,
    summary="Generate a supportive reply",
    status_code=status.HTTP_200_OK,
)
async def chat_session(payload: ChatRequest) -> ChatResponse:
    """Orchestrate a conversational turn with safety checks."""
    if not payload.messages:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="messages cannot be empty")

    return await conversation_service.generate_reply(payload)
