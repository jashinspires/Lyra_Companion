"""Service for coping strategy suggestions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from ..schemas.chat import CopingSuggestion, EmotionEstimate


@dataclass(slots=True)
class SuggestionTemplate:
    """Represents a coping suggestion template."""

    emotion: str
    title: str
    description: str
    resource_url: str | None = None


TEMPLATES: Sequence[SuggestionTemplate] = (
    SuggestionTemplate(
        emotion="sad",
        title="Compassionate journaling",
        description="Write a short letter to yourself acknowledging what hurts and what you need right now.",
    ),
    SuggestionTemplate(
        emotion="anxious",
        title="5-4-3-2-1 grounding",
        description="Pause and notice 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.",
    ),
    SuggestionTemplate(
        emotion="angry",
        title="Controlled breathing",
        description="Inhale for 4 counts, hold for 4, exhale for 6. Repeat 5 times to release tension.",
    ),
    SuggestionTemplate(
        emotion="negative",
        title="Reach out",
        description="Send a message to someone you trust describing how you're feeling. Connection matters.",
    ),
)


class SuggestionService:
    """Return coping suggestions tailored to detected emotions."""

    def suggest(self, emotions: Iterable[EmotionEstimate]) -> list[CopingSuggestion]:
        emotion_labels = {emotion.label for emotion in emotions}
        suggestions: list[CopingSuggestion] = []
        for template in TEMPLATES:
            if template.emotion in emotion_labels:
                suggestions.append(
                    CopingSuggestion(
                        title=template.title,
                        description=template.description,
                        resource_url=template.resource_url,
                    )
                )

        if not suggestions:
            suggestions.append(
                CopingSuggestion(
                    title="Check-in",
                    description="Take a deep breath and share anything more you'd like me to know so I can support you better.",
                )
            )

        return suggestions


suggestion_service = SuggestionService()
