"""Structured logging configuration for Raycast scripts."""

import sys
from typing import Any, Dict

import structlog
from rich.console import Console
from rich.logging import RichHandler

from .config import settings


def configure_logging() -> None:
    """Configure structured logging with Rich console output."""
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.JSONRenderer() if settings.log_level == "DEBUG" else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(structlog.stdlib, settings.log_level.upper(), 20)
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure Rich handler for console output
    console = Console(stderr=True)
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=True,
        markup=True,
        rich_tracebacks=True,
    )

    # Configure root logger
    import logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich_handler],
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


class ScriptLogger:
    """Context manager for script execution logging."""

    def __init__(self, script_name: str, **context: Any) -> None:
        """Initialize script logger with context."""
        self.logger = get_logger(script_name)
        self.context = context
        self.start_time: float = 0.0

    def __enter__(self) -> "ScriptLogger":
        """Enter logging context."""
        import time
        self.start_time = time.time()
        self.logger.info("Script started", **self.context)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit logging context."""
        import time
        duration = time.time() - self.start_time
        
        if exc_type is None:
            self.logger.info("Script completed successfully", duration=duration, **self.context)
        else:
            self.logger.error(
                "Script failed",
                error=str(exc_val),
                error_type=exc_type.__name__,
                duration=duration,
                **self.context
            )

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self.logger.info(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self.logger.error(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self.logger.warning(message, **kwargs)