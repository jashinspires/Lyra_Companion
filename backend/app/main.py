"""Application entrypoint for the Lyra backend."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add logging middleware
    @app.middleware("http")
    async def log_requests(request, call_next):
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"📥 Incoming request: {request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"📤 Response status: {response.status_code}")
        return response

    register_events(app)

    app.include_router(health.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")
    app.include_router(journaling.router, prefix="/api")
    app.include_router(mood.router, prefix="/api")
    app.include_router(safety.router, prefix="/api")

    return app


app = create_app()
