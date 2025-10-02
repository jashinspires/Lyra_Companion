"""Schemas for mood tracking."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class MoodLogCreate(BaseModel):
    """Payload to create a mood log."""

    mood: str = Field(..., min_length=1, max_length=32)
    intensity: int = Field(ge=1, le=5)
    notes: Optional[str] = Field(default=None, max_length=500)


class MoodLog(MoodLogCreate):
    """A persisted mood log entry."""

    id: str
    recorded_at: datetime


class MoodTrendPoint(BaseModel):
    """Aggregated mood data point for charting."""

    date: date
    average_intensity: float
    dominant_mood: Optional[str] = None
