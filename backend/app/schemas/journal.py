"""Schemas for journaling features."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class JournalEntryCreate(BaseModel):
    """Payload for creating a journal entry."""

    title: Optional[str] = Field(default=None, max_length=120)
    content: str = Field(..., min_length=1)
    mood: Optional[str] = Field(default=None, max_length=32)
    tags: list[str] = Field(default_factory=list, max_length=8)


class JournalEntry(JournalEntryCreate):
    """A stored journal entry."""

    id: str
    created_at: datetime
    updated_at: datetime


class JournalSummary(BaseModel):
    """Aggregate view of journal activity."""

    total_entries: int
    mood_counts: dict[str, int]
