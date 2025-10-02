"""Mood tracking endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Path, status

from ...schemas.mood import MoodLog, MoodLogCreate, MoodTrendPoint
from ...services.mood import mood_service

router = APIRouter(prefix="/mood", tags=["mood"])


@router.post(
    "/{user_id}/logs",
    response_model=MoodLog,
    status_code=status.HTTP_201_CREATED,
    summary="Log a mood entry",
)
async def log_mood(
    payload: MoodLogCreate,
    user_id: str = Path(..., min_length=1),
) -> MoodLog:
    return await mood_service.log_mood(user_id, payload)


@router.get(
    "/{user_id}/logs",
    response_model=list[MoodLog],
    summary="Retrieve mood logs",
)
async def list_logs(user_id: str = Path(..., min_length=1)) -> list[MoodLog]:
    return await mood_service.get_logs(user_id)


@router.get(
    "/{user_id}/trend",
    response_model=list[MoodTrendPoint],
    summary="Get mood trend data",
)
async def mood_trend(user_id: str = Path(..., min_length=1)) -> list[MoodTrendPoint]:
    return await mood_service.trend(user_id)
