"""Conversation orchestration service."""

from __future__ import annotations

import logging
from typing import Iterable

import httpx

from ..core.config import settings
from ..schemas.chat import ChatMessage, ChatRequest, ChatResponse
from .emotion import emotion_service
from .safety import safety_service
from .suggestions import suggestion_service

LOGGER = logging.getLogger(__name__)

OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
MODEL_NAME = "gpt-4o-mini"


class ConversationService:
    """Handle chat orchestration across safety and emotion services."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=20.0)

    async def _call_openai(self, messages: Iterable[ChatMessage]) -> str | None:
        if not settings.openai_api_key:
            return None

        payload = {
            "model": MODEL_NAME,
            "messages": [message.model_dump() for message in messages],
            "temperature": 0.7,
        }
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = await self._client.post(
                OPENAI_CHAT_COMPLETIONS_URL, json=payload, headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as exc:  # noqa: BLE001
            LOGGER.warning("OpenAI call failed: %s", exc)
            return None

    async def generate_reply(self, request: ChatRequest) -> ChatResponse:
        user_messages = [message for message in request.messages if message.role == "user"]
        assistant_messages = [
            message for message in request.messages if message.role == "assistant"
        ]

        safety = safety_service.evaluate_messages(
            [message.content for message in user_messages], locale=request.locale
        )

        if safety.crisis_detected:
            crisis_message = (
                "I'm deeply concerned for your safety. "
                "I recommend contacting {hotline} or local emergency services immediately. "
                "Please reach out to someone you trust right away."
            ).format(hotline=safety.hotline or "a crisis hotline")
            reply = ChatMessage(role="assistant", content=crisis_message)
            emotions = emotion_service.estimate(
                [message.content for message in user_messages]
            )
            suggestions = suggestion_service.suggest(emotions)
            return ChatResponse(reply=reply, emotions=emotions, suggestions=suggestions, safety=safety)

        ai_reply = await self._call_openai(request.messages)
        if not ai_reply:
            ai_reply = self._fallback_reply(user_messages, assistant_messages)

        assistant_message = ChatMessage(role="assistant", content=ai_reply)
        emotions = emotion_service.estimate(
            [message.content for message in user_messages]
        )
        suggestions = suggestion_service.suggest(emotions)
        return ChatResponse(
            reply=assistant_message,
            emotions=emotions,
            suggestions=suggestions,
            safety=safety,
        )

    @staticmethod
    def _fallback_reply(
        user_messages: list[ChatMessage], assistant_messages: list[ChatMessage]
    ) -> str:
        latest = user_messages[-1].content if user_messages else ""
        if not latest:
            return "I'm here with you. How are you feeling right now?"

        if any(keyword in latest.lower() for keyword in ("stressed", "overwhelmed")):
            return (
                "That sounds really heavy. Let's take a slow breath together. "
                "What's one small thing that helped even a little before?"
            )

        if "lonely" in latest.lower():
            return (
                "Feeling disconnected can hurt. I'm here to listen. "
                "Would reaching out to someone you trust feel possible today?"
            )

        if "anxious" in latest.lower():
            return (
                "Anxiety can make everything feel urgent. Let's pause for a moment. "
                "Can you notice three things around you that feel steady?"
            )

        return (
            "Thank you for sharing. I'm here with you. "
            "What would feel most supportive for you in this moment?"
        )


conversation_service = ConversationService()
