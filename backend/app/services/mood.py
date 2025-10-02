"""Mood logging service."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from datetime import date, datetime, timezone
from statistics import mean
from typing import Dict, List
from uuid import uuid4

from ..schemas.mood import MoodLog, MoodLogCreate, MoodTrendPoint


class MoodService:
    """In-memory mood tracking service."""

    def __init__(self) -> None:
        self._store: Dict[str, list[MoodLog]] = {}
        self._lock = asyncio.Lock()

    async def log_mood(self, user_id: str, payload: MoodLogCreate) -> MoodLog:
        entry = MoodLog(
            id=str(uuid4()),
            mood=payload.mood,
            intensity=payload.intensity,
            notes=payload.notes,
            recorded_at=datetime.now(timezone.utc),
        )
        async with self._lock:
            self._store.setdefault(user_id, []).append(entry)
        return entry

    async def get_logs(self, user_id: str) -> List[MoodLog]:
        async with self._lock:
            return list(self._store.get(user_id, []))

    async def trend(self, user_id: str) -> List[MoodTrendPoint]:
        async with self._lock:
            logs = list(self._store.get(user_id, []))

        grouped: Dict[date, list[MoodLog]] = defaultdict(list)
        for log in logs:
            grouped[log.recorded_at.date()].append(log)

        trend: list[MoodTrendPoint] = []
        for day, day_logs in sorted(grouped.items()):
            trend.append(
                MoodTrendPoint(
                    date=day,
                    average_intensity=mean(log.intensity for log in day_logs),
                    dominant_mood=max(day_logs, key=lambda log: log.intensity).mood,
                )
            )
        return trend

    async def clear(self) -> None:
        """Reset stored mood logs (testing helper)."""
        async with self._lock:
            self._store.clear()


mood_service = MoodService()
