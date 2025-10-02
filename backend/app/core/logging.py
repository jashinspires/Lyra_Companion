"""Logging configuration utilities."""

from __future__ import annotations

import logging
import sys

from .config import settings


def configure_logging() -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logging.info(
        "Logging configured for environment '%s'", settings.environment
    )
