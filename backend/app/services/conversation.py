"""Conversation orchestration service."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Iterable, Sequence

import google.generativeai as genai  # type: ignore[import]

from ..core.config import settings
from ..schemas.chat import ChatMessage, ChatRequest, ChatResponse
from .emotion import emotion_service
from .safety import safety_service
from .suggestions import suggestion_service

LOGGER = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Lyra, a compassionate and empathetic mental health support companion. 
Your role is to:
- Listen actively and validate emotions without judgment
- Offer gentle, supportive responses that prioritize user safety
- Use a warm, conversational tone that feels human and caring
- Ask thoughtful follow-up questions to help users explore their feelings
- Suggest evidence-based coping strategies when appropriate
- Always prioritize user wellbeing and recommend professional help when needed

Remember: You're not a therapist, but a supportive companion. Be genuine, kind, and present."""


class ConversationService:
    """Handle chat orchestration across safety and emotion services."""

    def __init__(self) -> None:
        self._model = None
        self._model_name = "models/gemini-2.5-pro"
        if settings.gemini_api_key:
            try:
                genai.configure(api_key=settings.gemini_api_key)
                self._model = genai.GenerativeModel(
                    self._model_name,
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 1024,
                    },
                )
            except Exception as exc:  # noqa: BLE001
                LOGGER.error("Failed to initialise Gemini model %s: %s", self._model_name, exc)
                self._model = None

    async def _call_gemini(self, messages: Iterable[ChatMessage]) -> str | None:
        """Call Google Gemini API for conversational responses."""
        if not self._model:
            LOGGER.info("No Gemini API key configured, using fallback")
            return None

        try:
            message_list = list(messages)
            attempts: list[Sequence[ChatMessage]] = [message_list]
            if len(message_list) > 4:
                attempts.append(message_list[-4:])

            finish_reasons: list[str | None] = []
            for attempt_index, attempt_messages in enumerate(attempts):
                conversation_text = self._build_conversation_text(attempt_messages)

                LOGGER.info(
                    "Calling Gemini API with %s messages (attempt %s)",
                    len(attempt_messages),
                    attempt_index + 1,
                )

                response = await asyncio.to_thread(self._model.generate_content, conversation_text)

                reply_text, finish_reason = self._extract_response_text(response)
                finish_reasons.append(finish_reason)

                if reply_text:
                    LOGGER.info(
                        "Gemini response received (finish_reason=%s): %s...",
                        finish_reason or "unknown",
                        reply_text[:100],
                    )
                    return reply_text

                if (
                    attempt_index == 0
                    and finish_reason
                    and (
                        "MAX_TOKENS" in finish_reason.upper()
                        or finish_reason.upper() == "2"
                    )
                    and len(attempts) > 1
                ):
                    LOGGER.warning(
                        "Gemini returned finish_reason=%s; retrying with a shorter context",
                        finish_reason,
                    )
                    continue

                if getattr(response, "prompt_feedback", None):
                    LOGGER.warning(
                        "Gemini prompt feedback: %s",
                        getattr(response.prompt_feedback, "block_reason", response.prompt_feedback),
                    )

                LOGGER.warning(
                    "Gemini response was empty or blocked (finish_reason=%s)", finish_reason
                )
                return None

            LOGGER.warning(
                "Gemini response returned no usable text after %s attempts (finish_reasons=%s)",
                len(attempts),
                finish_reasons,
            )
            return None

        except Exception as exc:  # noqa: BLE001
            LOGGER.error("Gemini call failed: %s", exc)
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

        ai_reply = await self._call_gemini(request.messages)
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
    def _build_conversation_text(messages: Sequence[ChatMessage]) -> str:
        conversation_text = SYSTEM_PROMPT + "\n\n"

        for msg in messages:
            if msg.role == "user":
                conversation_text += f"User: {msg.content}\n"
            elif msg.role == "assistant":
                conversation_text += f"Lyra: {msg.content}\n"

        conversation_text += "Lyra:"
        return conversation_text

    @staticmethod
    def _extract_response_text(response: Any) -> tuple[str | None, str | None]:
        if not response:
            return None, None

        candidates = getattr(response, "candidates", None) or []
        finish_reason: str | None = None

        for candidate in candidates:
            raw_finish_reason = getattr(candidate, "finish_reason", None)
            finish_reason = ConversationService._describe_finish_reason(raw_finish_reason)
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None) or []

            texts = [getattr(part, "text", "") for part in parts if getattr(part, "text", None)]
            if texts:
                combined = "".join(texts).strip()
                if combined:
                    return combined, finish_reason

        if finish_reason is None and getattr(response, "prompt_feedback", None):
            finish_reason = ConversationService._describe_finish_reason(
                getattr(response.prompt_feedback, "block_reason", None)
            )

        return None, finish_reason

    @staticmethod
    def _describe_finish_reason(reason: Any) -> str | None:
        if reason is None:
            return None
        if hasattr(reason, "name"):
            return str(reason.name)
        return str(reason)

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
