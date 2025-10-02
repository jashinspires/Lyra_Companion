"""Lifecycle event handlers."""

from __future__ import annotations

from fastapi import FastAPI

from .config import settings
from .logging import configure_logging


async def on_startup() -> None:
    """Execute actions when the application starts."""
    configure_logging()

    # Placeholder for future integrations (e.g., database connection checks)
    if settings.environment != "test":
        # In production we might warm up models or verify external services here.
        pass


async def on_shutdown() -> None:
    """Execute actions when the application shuts down."""
    # Close database connections, flush telemetry buffers, etc.
    pass


def register_events(app: FastAPI) -> None:
    """Register startup and shutdown events on the application."""
    app.add_event_handler("startup", on_startup)
    app.add_event_handler("shutdown", on_shutdown)
