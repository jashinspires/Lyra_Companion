"""Unit tests for conversation service helpers."""

from __future__ import annotations

from dataclasses import dataclass

from app.services.conversation import ConversationService


@dataclass
class _Part:
    text: str | None


@dataclass
class _Content:
    parts: list[_Part]


@dataclass
class _Candidate:
    content: _Content
    finish_reason: object | None


@dataclass
class _PromptFeedback:
    block_reason: object | None


@dataclass
class _Response:
    candidates: list[_Candidate]
    prompt_feedback: _PromptFeedback | None = None


def test_extract_response_text_returns_joined_text() -> None:
    response = _Response(
        candidates=[
            _Candidate(
                content=_Content(parts=[_Part(text="Hello"), _Part(text=" world")]),
                finish_reason="FinishReason.MAX_TOKENS",
            )
        ]
    )

    text, finish_reason = ConversationService._extract_response_text(response)

    assert text == "Hello world"
    assert finish_reason == "FinishReason.MAX_TOKENS"


def test_extract_response_text_handles_missing_parts_and_feedback() -> None:
    response = _Response(
        candidates=[
            _Candidate(content=_Content(parts=[]), finish_reason="FinishReason.MAX_TOKENS"),
        ],
        prompt_feedback=_PromptFeedback(block_reason="BlockedReason.SAFETY"),
    )

    text, finish_reason = ConversationService._extract_response_text(response)

    assert text is None
    # We should still surface the finish_reason from the candidate even without text parts
    assert finish_reason == "FinishReason.MAX_TOKENS"
