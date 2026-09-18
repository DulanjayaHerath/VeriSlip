"""API-key authentication and per-key, multi-tier rate limiting."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import threading
import time
from dataclasses import dataclass
from typing import Callable, Dict, Mapping, Optional, Protocol, Tuple

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response


API_KEY_HEADER = "X-API-Key"
API_KEY_HASHES_ENV = "VERISLIP_API_KEY_HASHES"
SIGNED_WEBHOOK_PATHS = frozenset({"/api/v1/integrations/shopify/webhooks/orders-create"})
logger = logging.getLogger("verislip.auth")


@dataclass(frozen=True)
class RateLimitPolicy:
    """A fixed-window request quota."""

    limit: int
    window_seconds: int
    name: str


TIER_POLICIES: Mapping[str, RateLimitPolicy] = {
    "free": RateLimitPolicy(limit=10, window_seconds=86_400, name="free"),
    "pro": RateLimitPolicy(limit=100, window_seconds=60, name="pro"),
}


@dataclass(frozen=True)
class RateLimitResult:
    """Result of atomically consuming one request from a quota."""

    allowed: bool
    limit: int
    remaining: int
    reset_at: int
    retry_after: int


class RateLimitStore(Protocol):
    """Storage contract implemented by local and distributed counters."""

    def consume(
        self, key_id: str, policy: RateLimitPolicy, now: float
    ) -> RateLimitResult: ...


class InMemoryRateLimitStore:
    """Thread-safe fixed-window counters for local development and tests."""

    def __init__(self) -> None:
        self._counts: Dict[Tuple[str, int, int], int] = {}
        self._lock = threading.Lock()

    def consume(
        self, key_id: str, policy: RateLimitPolicy, now: float
    ) -> RateLimitResult:
        bucket = int(now // policy.window_seconds)
        reset_at = (bucket + 1) * policy.window_seconds
        counter_key = (key_id, policy.window_seconds, bucket)
        with self._lock:
            count = self._counts.get(counter_key, 0) + 1
            self._counts[counter_key] = count
            if len(self._counts) > 10_000:
                self._counts = {
                    key: value
                    for key, value in self._counts.items()
                    if (key[2] + 1) * key[1] > now
                }
        return RateLimitResult(
            allowed=count <= policy.limit,
            limit=policy.limit,
            remaining=max(0, policy.limit - count),
            reset_at=reset_at,
            retry_after=max(1, reset_at - int(now)),
        )


class RedisRateLimitStore:
    """Redis-backed atomic counters for multi-process production deployments."""

    _CONSUME_SCRIPT = """
local count = redis.call('INCR', KEYS[1])
if count == 1 then
  redis.call('EXPIRE', KEYS[1], ARGV[1])
end
local ttl = redis.call('TTL', KEYS[1])
return {count, ttl}
"""

    def __init__(self, redis_url: str) -> None:
        try:
            import redis
        except ImportError as exc:  # pragma: no cover - deployment dependency guard
            raise RuntimeError("Redis rate limiting requires the redis package.") from exc
        self._client = redis.Redis.from_url(
            redis_url, decode_responses=True, socket_timeout=2
        )

    def consume(
        self, key_id: str, policy: RateLimitPolicy, now: float
    ) -> RateLimitResult:
        bucket = int(now // policy.window_seconds)
        reset_at = (bucket + 1) * policy.window_seconds
        ttl = max(1, reset_at - int(now))
        redis_key = f"verislip:rate:{policy.name}:{key_id}:{bucket}"
        count, stored_ttl = self._client.eval(
            self._CONSUME_SCRIPT, 1, redis_key, ttl
        )
        count = int(count)
        return RateLimitResult(
            allowed=count <= policy.limit,
            limit=policy.limit,
            remaining=max(0, policy.limit - count),
            reset_at=reset_at,
            retry_after=max(1, int(stored_ttl)),
        )


class ApiKeyRegistry:
    """Authenticate raw keys against configured SHA-256 fingerprints."""

    def __init__(self, tiers_by_hash: Mapping[str, str]) -> None:
        normalized: Dict[str, str] = {}
        for key_hash, tier in tiers_by_hash.items():
            normalized_hash = str(key_hash).lower()
            if len(normalized_hash) != 64 or any(
                character not in "0123456789abcdef" for character in normalized_hash
            ):
                raise ValueError("API key configuration contains an invalid SHA-256 hash.")
            if tier not in TIER_POLICIES:
                raise ValueError("API key configuration contains an unsupported tier.")
            normalized[normalized_hash] = tier
        self._tiers_by_hash = normalized

    @classmethod
    def from_environment(cls) -> "ApiKeyRegistry":
        """Load a JSON object of SHA-256 fingerprint to tier mappings."""
        raw_config = os.getenv(API_KEY_HASHES_ENV, "{}")
        try:
            parsed = json.loads(raw_config)
        except json.JSONDecodeError as exc:
            raise RuntimeError("API key configuration is not valid JSON.") from exc
        if not isinstance(parsed, dict):
            raise RuntimeError("API key configuration must be a JSON object.")
        try:
            return cls(parsed)
        except ValueError as exc:
            raise RuntimeError(str(exc)) from exc

    @property
    def is_configured(self) -> bool:
        return bool(self._tiers_by_hash)

    def authenticate(self, raw_key: str) -> Optional[Tuple[str, str]]:
        """Return the non-secret key fingerprint and tier for a valid key."""
        candidate_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
        for configured_hash, tier in self._tiers_by_hash.items():
            if hmac.compare_digest(candidate_hash, configured_hash):
                return configured_hash, tier
        return None


def build_rate_limit_store() -> RateLimitStore:
    """Select Redis when configured, otherwise use the local process store."""
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        return RedisRateLimitStore(redis_url)
    return InMemoryRateLimitStore()


def _rate_headers(result: RateLimitResult) -> Dict[str, str]:
    return {
        "X-RateLimit-Limit": str(result.limit),
        "X-RateLimit-Remaining": str(result.remaining),
        "X-RateLimit-Reset": str(result.reset_at),
    }


class ApiKeyRateLimitMiddleware(BaseHTTPMiddleware):
    """Authenticate and rate-limit protected API routes without exposing keys."""

    @staticmethod
    def _resolve_state(app):
        seen = set()
        current = app
        while current is not None and id(current) not in seen:
            if hasattr(current, "state"):
                return current.state
            seen.add(id(current))
            current = getattr(current, "app", None)
        return None

    def __init__(
        self,
        app,
        registry: Optional[ApiKeyRegistry] = None,
        store: Optional[RateLimitStore] = None,
        clock: Callable[[], float] = time.time,
        protected_prefix: str = "/api/v1",
    ) -> None:
        super().__init__(app)
        self.registry = registry or ApiKeyRegistry.from_environment()
        state = self._resolve_state(app)
        self.store = store or getattr(state, "api_key_rate_limit_store", None)
        if self.store is None:
            self.store = build_rate_limit_store()
        if state is not None:
            state.api_key_rate_limit_store = self.store
        self.clock = clock
        self.protected_prefix = protected_prefix

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path_is_protected = request.url.path == self.protected_prefix or (
            request.url.path.startswith(f"{self.protected_prefix}/")
        )
        is_signed_webhook = (
            request.method == "POST" and request.url.path in SIGNED_WEBHOOK_PATHS
        )
        if request.method == "OPTIONS" or not path_is_protected or is_signed_webhook:
            return await call_next(request)

        if not self.registry.is_configured:
            logger.error("auth.not_configured")
            return JSONResponse(
                status_code=503,
                content={"detail": "API authentication is unavailable."},
            )

        raw_key = request.headers.get(API_KEY_HEADER)
        if not raw_key:
            logger.warning("auth.missing")
            return JSONResponse(
                status_code=401,
                content={"detail": "API key is required."},
                headers={"WWW-Authenticate": "ApiKey"},
            )

        identity = self.registry.authenticate(raw_key)
        if identity is None:
            logger.warning("auth.invalid")
            return JSONResponse(
                status_code=403,
                content={"detail": "API key is invalid."},
            )

        key_id, tier = identity
        policy = TIER_POLICIES[tier]
        state = self._resolve_state(self.app)
        store = getattr(state, "api_key_rate_limit_store", self.store) if state is not None else self.store
        self.store = store
        # Scope quota counters to the protected route being called so a single API
        # key can use different endpoints without exhausting another endpoint's
        # allowance. This keeps per-key quotas predictable in long-lived apps that
        # serve mixed workloads.
        rate_scope = f"{key_id}:{request.url.path}"
        result = await run_in_threadpool(
            self.store.consume, rate_scope, policy, self.clock()
        )
        headers = _rate_headers(result)
        if not result.allowed:
            logger.warning("rate_limit.exceeded")
            headers["Retry-After"] = str(result.retry_after)
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded."},
                headers=headers,
            )

        request.state.api_key_id = key_id
        request.state.api_tier = tier
        request.state.rate_limit_limit = result.limit
        request.state.rate_limit_remaining = result.remaining
        request.state.rate_limit_reset = result.reset_at
        response = await call_next(request)
        response.headers.update(headers)
        return response
