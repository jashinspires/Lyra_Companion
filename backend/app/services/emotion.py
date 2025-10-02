"""Basic emotion estimation service."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from ..schemas.chat import EmotionEstimate


@dataclass(slots=True)
class EmotionLexicon:
    """Stores lexicon mappings for simple emotion scoring."""

    positive: set[str]
    negative: set[str]
    anxious: set[str]
    sad: set[str]
    angry: set[str]


DEFAULT_LEXICON = EmotionLexicon(
    positive={"grateful", "hopeful", "calm", "relieved"},
    negative={"upset", "bad", "awful", "terrible"},
    anxious={"nervous", "worried", "anxious", "panic"},
    sad={"sad", "down", "depressed", "lonely"},
    angry={"angry", "mad", "frustrated", "furious"},
)


class EmotionService:
    """Naive lexicon-based emotion detection service."""

    def __init__(self, lexicon: EmotionLexicon | None = None) -> None:
        self.lexicon = lexicon or DEFAULT_LEXICON

    def estimate(self, texts: Iterable[str]) -> list[EmotionEstimate]:
        tokens: Counter[str] = Counter()
        for text in texts:
            tokens.update(word.strip(".,!?").lower() for word in text.split())

        scores: dict[str, int] = {
            "positive": sum(tokens[token] for token in self.lexicon.positive),
            "negative": sum(tokens[token] for token in self.lexicon.negative),
            "anxious": sum(tokens[token] for token in self.lexicon.anxious),
            "sad": sum(tokens[token] for token in self.lexicon.sad),
            "angry": sum(tokens[token] for token in self.lexicon.angry),
        }

        total = sum(scores.values())
        if total == 0:
            return [EmotionEstimate(label="neutral", confidence=0.4)]

        return [
            EmotionEstimate(label=label, confidence=score / total)
            for label, score in scores.items()
            if score > 0
        ]


emotion_service = EmotionService()
