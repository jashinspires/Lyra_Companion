"""Schemas related to conversational interactions."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from .safety import SafetyCheckResult

Role = Literal["user", "assistant", "system"]


class ChatMessage(BaseModel):
    """A single chat message."""

    role: Role
    content: str = Field(..., min_length=1)


class EmotionEstimate(BaseModel):
    """Emotion analysis output from the classifier."""

    label: str
    confidence: float = Field(ge=0.0, le=1.0)


class CopingSuggestion(BaseModel):
    """Suggested exercise or resource."""

    title: str
    description: str
    resource_url: Optional[str] = None


class ChatRequest(BaseModel):
    """Incoming chat request payload."""

    messages: list[ChatMessage]
    locale: str = "en-US"
    timezone: Optional[str] = None
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Outgoing chat response payload."""

    reply: ChatMessage
    emotions: list[EmotionEstimate] = Field(default_factory=list)
    suggestions: list[CopingSuggestion] = Field(default_factory=list)
    safety: Optional[SafetyCheckResult] = None
