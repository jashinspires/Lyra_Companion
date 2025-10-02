"""Journaling endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Path, status

from ...schemas.journal import JournalEntry, JournalEntryCreate, JournalSummary
from ...services.journal import journal_service

router = APIRouter(prefix="/journal", tags=["journal"])


@router.post(
    "/{user_id}/entries",
    response_model=JournalEntry,
    status_code=status.HTTP_201_CREATED,
    summary="Create a journal entry",
)
async def create_entry(
    payload: JournalEntryCreate,
    user_id: str = Path(..., min_length=1, description="Identifier for the user"),
) -> JournalEntry:
    return await journal_service.create_entry(user_id, payload)


@router.get(
    "/{user_id}/entries",
    response_model=list[JournalEntry],
    summary="List journal entries",
)
async def list_entries(user_id: str = Path(..., min_length=1)) -> list[JournalEntry]:
    return await journal_service.list_entries(user_id)


@router.get(
    "/{user_id}/summary",
    response_model=JournalSummary,
    summary="Summarize journal activity",
)
async def journal_summary(user_id: str = Path(..., min_length=1)) -> JournalSummary:
    return await journal_service.summary(user_id)
