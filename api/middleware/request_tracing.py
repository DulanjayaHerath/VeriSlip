"""Request tracing middleware with privacy-safe structured lifecycle logs."""

from __future__ import annotations

import logging
import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from core.observability.logging import (
    CORRELATION_ID_HEADER,
    REQUEST_ID_HEADER,
    normalize_correlation_id,
    reset_correlation_id,
    set_correlation_id,
)


logger = logging.getLogger("verislip.request")


def _route_template(request: Request) -> str:
    """Return the route template, avoiding query strings and path parameter values."""
    route = request.scope.get("route")
    return getattr(route, "path", "unmatched")


class RequestTracingMiddleware(BaseHTTPMiddleware):
    """Attach a correlation ID and emit request lifecycle JSON events."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        supplied_id = request.headers.get(REQUEST_ID_HEADER) or request.headers.get(
            CORRELATION_ID_HEADER
        )
        correlation_id = normalize_correlation_id(supplied_id)
        request.state.correlation_id = correlation_id
        token = set_correlation_id(correlation_id)
        started = time.perf_counter()

        logger.info("request.started", extra={"method": request.method})
        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = round((time.perf_counter() - started) * 1000, 2)
            logger.error(
                "request.failed",
                extra={
                    "method": request.method,
                    "path": _route_template(request),
                    "status_code": 500,
                    "duration_ms": duration_ms,
                    "error_type": type(exc).__name__,
                },
            )
            response = JSONResponse(
                status_code=500, content={"detail": "Internal server error."}
            )
        else:
            duration_ms = round((time.perf_counter() - started) * 1000, 2)
            logger.info(
                "request.completed",
                extra={
                    "method": request.method,
                    "path": _route_template(request),
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                },
            )
        finally:
            reset_correlation_id(token)

        response.headers[REQUEST_ID_HEADER] = correlation_id
        return response
