"""In-memory journaling service."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Dict, List
from uuid import uuid4

from ..schemas.journal import JournalEntry, JournalEntryCreate, JournalSummary


class JournalService:
    """Manage journal entries in memory.

    The service is intentionally simple and can later be
    replaced with a persistent data layer (e.g., MongoDB).
    """

    def __init__(self) -> None:
        self._entries: Dict[str, list[JournalEntry]] = {}
        self._lock = asyncio.Lock()

    async def create_entry(self, user_id: str, payload: JournalEntryCreate) -> JournalEntry:
        now = datetime.now(timezone.utc)
        entry = JournalEntry(
            id=str(uuid4()),
            title=payload.title,
            content=payload.content,
            mood=payload.mood,
            tags=payload.tags,
            created_at=now,
            updated_at=now,
        )
        async with self._lock:
            self._entries.setdefault(user_id, []).append(entry)
        return entry

    async def list_entries(self, user_id: str) -> List[JournalEntry]:
        async with self._lock:
            return list(self._entries.get(user_id, []))

    async def summary(self, user_id: str) -> JournalSummary:
        async with self._lock:
            entries = self._entries.get(user_id, [])
        mood_counts: Dict[str, int] = {}
        for entry in entries:
            if entry.mood:
                mood_counts[entry.mood] = mood_counts.get(entry.mood, 0) + 1
        return JournalSummary(total_entries=len(entries), mood_counts=mood_counts)

    async def clear(self) -> None:
        """Reset all stored journal data.

        Intended for tests and local development convenience.
        """
        async with self._lock:
            self._entries.clear()


journal_service = JournalService()
