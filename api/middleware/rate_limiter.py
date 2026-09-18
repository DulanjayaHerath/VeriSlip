"""
VeriSlip Rate Limiting Middleware
Protects forensic analysis endpoints from denial-of-service and brute-force scanning.
Implements in-memory sliding window counter with client IP tracking.
"""

import time
from collections import defaultdict
from typing import Dict, List
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        max_requests: int = 120,
        window_seconds: int = 60,
        exempt_paths: List[str] = None
    ):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.exempt_paths = exempt_paths or [
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/static",
            "/favicon.ico"
        ]
        self.request_records: Dict[str, List[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Check exemptions
        for exempt in self.exempt_paths:
            if path.startswith(exempt):
                return await call_next(request)

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        cutoff = now - self.window_seconds

        # Clean old timestamps
        history = [ts for ts in self.request_records[client_ip] if ts > cutoff]
        self.request_records[client_ip] = history

        # Check limit
        if len(history) >= self.max_requests:
            retry_after = int(self.window_seconds - (now - history[0])) if history else self.window_seconds
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded. Too many requests.",
                    "max_requests": self.max_requests,
                    "window_seconds": self.window_seconds,
                    "retry_after": max(1, retry_after)
                },
                headers={"Retry-After": str(max(1, retry_after))}
            )

        # Record this request
        self.request_records[client_ip].append(now)

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(max(0, self.max_requests - len(self.request_records[client_ip])))
        return response
