"""Safety check endpoints."""

from __future__ import annotations

from fastapi import APIRouter, status

from ...schemas.safety import SafetyCheckRequest, SafetyCheckResult
from ...services.safety import safety_service

router = APIRouter(prefix="/safety", tags=["safety"])


@router.post(
    "/check",
    response_model=SafetyCheckResult,
    status_code=status.HTTP_200_OK,
    summary="Run a safety assessment on text",
)
async def safety_check(payload: SafetyCheckRequest) -> SafetyCheckResult:
    return safety_service.evaluate_text(payload.text, locale=payload.locale)
