"""Application entrypoint for the Lyra backend."""

from __future__ import annotations

from fastapi import FastAPI

from .api.routes import chat, health, journaling, mood, safety
from .core.config import settings
from .core.events import register_events


def create_app() -> FastAPI:
    """Instantiate the FastAPI application."""
    app = FastAPI(
        title=settings.project_name,
        description=settings.project_description,
        version=settings.version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    register_events(app)

    app.include_router(health.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")
    app.include_router(journaling.router, prefix="/api")
    app.include_router(mood.router, prefix="/api")
    app.include_router(safety.router, prefix="/api")

    return app


app = create_app()
