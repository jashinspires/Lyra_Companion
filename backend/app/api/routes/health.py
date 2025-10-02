"""Health check endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Health check")
async def health_check() -> dict[str, str]:
    """Return a simple health status."""
    return {"status": "ok"}
