"""Structured logging and correlation context for the VeriSlip API."""

from __future__ import annotations

import json
import logging
import re
import sys
import uuid
from contextvars import ContextVar, Token
from datetime import datetime, timezone
from typing import Optional


REQUEST_ID_HEADER = "X-Request-ID"
CORRELATION_ID_HEADER = "X-Correlation-ID"
_VALID_CORRELATION_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_correlation_id: ContextVar[Optional[str]] = ContextVar(
    "verislip_correlation_id", default=None
)
_SAFE_EXTRA_FIELDS = (
    "method",
    "path",
    "status_code",
    "duration_ms",
    "error_type",
)


def normalize_correlation_id(candidate: Optional[str]) -> str:
    """Return a safe caller ID, or generate a new UUID when it is invalid."""
    if candidate and _VALID_CORRELATION_ID.fullmatch(candidate):
        return candidate
    return str(uuid.uuid4())


def set_correlation_id(correlation_id: str) -> Token:
    """Set request-scoped correlation context and return its reset token."""
    return _correlation_id.set(correlation_id)


def reset_correlation_id(token: Token) -> None:
    """Restore correlation context after request processing completes."""
    _correlation_id.reset(token)


def get_correlation_id() -> Optional[str]:
    """Return the correlation ID propagated through the current execution context."""
    return _correlation_id.get()


class JsonLogFormatter(logging.Formatter):
    """Serialize an allowlisted, privacy-conscious log record as one JSON line."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
            "correlation_id": getattr(
                record, "correlation_id", None
            ) or get_correlation_id(),
        }
        for field in _SAFE_EXTRA_FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        return json.dumps(payload, separators=(",", ":"), ensure_ascii=True)


def configure_json_logging() -> None:
    """Configure VeriSlip loggers once without changing third-party loggers."""
    logger = logging.getLogger("verislip")
    if not any(getattr(handler, "_verislip_json", False) for handler in logger.handlers):
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(JsonLogFormatter())
        handler._verislip_json = True  # type: ignore[attr-defined]
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
