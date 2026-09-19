"""
Prometheus Metrics Middleware for FastAPI / Starlette (#88).
Tracks request latency, throughput, error rates, and path labels.
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.observability.metrics import record_request_metrics


class PrometheusMetricsMiddleware(BaseHTTPMiddleware):
    """Measures request duration and increments HTTP metrics counters."""

    async def dispatch(self, request: Request, call_next):
        # Exclude /metrics from recursive metric explosion
        path = request.url.path
        if path == "/metrics":
            return await call_next(request)

        # Normalize high-cardinality paths if needed
        endpoint = path
        if path.startswith("/api/v1/courier/waybills/"):
            endpoint = "/api/v1/courier/waybills/{id}"
        elif path.startswith("/static/"):
            endpoint = "/static"

        start_time = time.perf_counter()
        status_code = 500
        try:
            response: Response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration = time.perf_counter() - start_time
            record_request_metrics(
                method=request.method,
                endpoint=endpoint,
                status_code=status_code,
                duration_seconds=duration
            )
