"""Pytest fixtures for Lyra backend tests."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.main import create_app
from app.services.journal import journal_service
from app.services.mood import mood_service


@pytest.fixture()
def app() -> FastAPI:
    """Provide a FastAPI application instance for tests."""
    return create_app()


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Return an async HTTP client bound to the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        yield async_client


@pytest.fixture(autouse=True)
async def reset_state() -> AsyncGenerator[None, None]:
    """Clear in-memory services before and after each test."""
    await journal_service.clear()
    await mood_service.clear()
    yield
    await journal_service.clear()
    await mood_service.clear()
