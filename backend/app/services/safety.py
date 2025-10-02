"""Safety and crisis detection service."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from ..schemas.safety import SafetyCheckRequest, SafetyCheckResult

CRISIS_KEYWORDS: dict[str, str] = {
    "suicide": "self-harm",
    "kill myself": "self-harm",
    "end it all": "self-harm",
    "hurt myself": "self-harm",
    "overdose": "substance-risk",
    "can't go on": "self-harm",
}

REGIONAL_HOTLINES: dict[str, str] = {
    "en-US": "988 Suicide & Crisis Lifeline",
    "en-IN": "Kiran Helpline: 1800-599-0019",
    "en-GB": "Samaritans: 116 123",
}


class SafetyService:
    """Simple keyword-based crisis detector with extendable interface."""

    def __init__(self, crisis_keywords: dict[str, str] | None = None) -> None:
        self._keywords = crisis_keywords or CRISIS_KEYWORDS

    def evaluate_text(self, text: str, *, locale: str = "en-US") -> SafetyCheckResult:
        """Run safety heuristics on a piece of text."""
        normalized = text.lower()
        matched_categories: set[str] = set()

        for phrase, category in self._keywords.items():
            if phrase in normalized:
                matched_categories.add(category)

        crisis_detected = bool(matched_categories)
        hotline = REGIONAL_HOTLINES.get(locale, REGIONAL_HOTLINES["en-US"])

        recommended_actions: list[str] = []
        if crisis_detected:
            recommended_actions.extend(
                [
                    "Reach out to a trusted friend or family member immediately.",
                    "Contact local emergency services or a crisis hotline for urgent support.",
                    "Avoid any self-harm; you deserve support and care right now.",
                ]
            )

        return SafetyCheckResult(
            crisis_detected=crisis_detected,
            risk_level="high" if crisis_detected else "low",
            matched_category=", ".join(sorted(matched_categories)) if matched_categories else None,
            recommended_actions=recommended_actions,
            hotline=hotline,
            evaluated_at=datetime.now(timezone.utc),
        )

    def evaluate_messages(self, messages: Iterable[str], *, locale: str = "en-US") -> SafetyCheckResult:
        """Evaluate multiple messages and combine results."""
        combined_text = "\n".join(messages)
        return self.evaluate_text(combined_text, locale=locale)


safety_service = SafetyService()
