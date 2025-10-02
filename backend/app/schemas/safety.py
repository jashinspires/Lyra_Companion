"""Schemas for safety and crisis management."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SafetyCheckRequest(BaseModel):
    """Request payload for explicit safety assessments."""

    text: str = Field(..., min_length=1)
    locale: str = "en-US"


class SafetyCheckResult(BaseModel):
    """Result of a safety check."""

    crisis_detected: bool
    risk_level: Optional[str] = None
    matched_category: Optional[str] = None
    recommended_actions: list[str] = Field(default_factory=list)
    hotline: Optional[str] = None
    evaluated_at: datetime
