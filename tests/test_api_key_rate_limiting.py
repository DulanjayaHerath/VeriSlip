"""Authentication and multi-tier rate-limit integration tests."""

import hashlib
import io
import json
import logging

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.middleware.rate_limiter import (
    ApiKeyRateLimitMiddleware,
    ApiKeyRegistry,
    InMemoryRateLimitStore,
)
from api.middleware.request_tracing import RequestTracingMiddleware
from api.main import app as main_app
from core.observability.logging import JsonLogFormatter


FREE_KEY = "free-test-key-57"
SECOND_FREE_KEY = "second-free-test-key-57"
PRO_KEY = "pro-test-key-57"


def _fingerprint(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def _test_app(now=1_700_000_000.0):
    app = FastAPI()
    registry = ApiKeyRegistry(
        {
            _fingerprint(FREE_KEY): "free",
            _fingerprint(SECOND_FREE_KEY): "free",
            _fingerprint(PRO_KEY): "pro",
        }
    )
    app.add_middleware(
        ApiKeyRateLimitMiddleware,
        registry=registry,
        store=InMemoryRateLimitStore(),
        clock=lambda: now,
    )
    app.add_middleware(RequestTracingMiddleware)

    @app.get("/health")
    def health():
        return {"status": "healthy"}

    @app.get("/api/v1/protected")
    def protected():
        return {"status": "ok"}

    return app


def test_valid_api_key_returns_tier_rate_headers():
    client = TestClient(_test_app())

    response = client.get(
        "/api/v1/protected", headers={"X-API-Key": FREE_KEY}
    )

    assert response.status_code == 200
    assert response.headers["X-RateLimit-Limit"] == "10"
    assert response.headers["X-RateLimit-Remaining"] == "9"
    assert response.headers["X-RateLimit-Reset"]
    assert response.headers["X-Request-ID"]


def test_missing_api_key_is_unauthorized_with_correlation_id():
    response = TestClient(_test_app()).get("/api/v1/protected")

    assert response.status_code == 401
    assert response.json() == {"detail": "API key is required."}
    assert response.headers["WWW-Authenticate"] == "ApiKey"
    assert response.headers["X-Request-ID"]


def test_invalid_api_key_is_forbidden_without_echoing_key():
    invalid_key = "invalid-secret-key-57"

    response = TestClient(_test_app()).get(
        "/api/v1/protected", headers={"X-API-Key": invalid_key}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "API key is invalid."}
    assert invalid_key not in response.text


def test_free_tier_allows_ten_requests_per_day_then_limits():
    client = TestClient(_test_app())
    headers = {"X-API-Key": FREE_KEY}

    responses = [client.get("/api/v1/protected", headers=headers) for _ in range(11)]

    assert all(response.status_code == 200 for response in responses[:10])
    limited = responses[10]
    assert limited.status_code == 429
    assert limited.json() == {"detail": "Rate limit exceeded."}
    assert limited.headers["X-RateLimit-Limit"] == "10"
    assert limited.headers["X-RateLimit-Remaining"] == "0"
    assert int(limited.headers["Retry-After"]) > 0


def test_pro_tier_allows_one_hundred_requests_per_minute_then_limits():
    client = TestClient(_test_app())
    headers = {"X-API-Key": PRO_KEY}

    responses = [client.get("/api/v1/protected", headers=headers) for _ in range(101)]

    assert all(response.status_code == 200 for response in responses[:100])
    assert responses[100].status_code == 429
    assert responses[100].headers["X-RateLimit-Limit"] == "100"


def test_rate_limits_are_isolated_between_api_keys():
    client = TestClient(_test_app())
    first = {"X-API-Key": FREE_KEY}
    second = {"X-API-Key": SECOND_FREE_KEY}

    for _ in range(10):
        assert client.get("/api/v1/protected", headers=first).status_code == 200

    assert client.get("/api/v1/protected", headers=first).status_code == 429
    other_key_response = client.get("/api/v1/protected", headers=second)
    assert other_key_response.status_code == 200
    assert other_key_response.headers["X-RateLimit-Remaining"] == "9"


@pytest.mark.parametrize("path", ["/health", "/docs", "/openapi.json"])
def test_intentionally_public_endpoints_do_not_require_api_key(path):
    response = TestClient(_test_app()).get(path)

    assert response.status_code == 200
    assert "X-RateLimit-Limit" not in response.headers
    assert response.headers["X-Request-ID"]


def test_unconfigured_authentication_fails_closed():
    app = FastAPI()
    app.add_middleware(
        ApiKeyRateLimitMiddleware,
        registry=ApiKeyRegistry({}),
        store=InMemoryRateLimitStore(),
    )
    app.add_middleware(RequestTracingMiddleware)

    @app.get("/api/v1/protected")
    def protected():
        return {"status": "ok"}

    response = TestClient(app).get("/api/v1/protected")

    assert response.status_code == 503
    assert response.json() == {"detail": "API authentication is unavailable."}


def test_cors_preflight_remains_public_on_existing_middleware_stack():
    response = TestClient(main_app).options(
        "/api/v1/verify",
        headers={
            "Origin": "https://merchant.example",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "X-API-Key",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://merchant.example"


def test_api_key_is_never_written_to_structured_logs():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonLogFormatter())
    auth_logger = logging.getLogger("verislip.auth")
    request_logger = logging.getLogger("verislip.request")
    auth_logger.addHandler(handler)
    request_logger.addHandler(handler)
    secret = "raw-key-must-never-be-logged-57"
    try:
        response = TestClient(_test_app()).get(
            "/api/v1/protected?token=also-secret",
            headers={"X-API-Key": secret, "Authorization": "Bearer private"},
        )
    finally:
        auth_logger.removeHandler(handler)
        request_logger.removeHandler(handler)

    assert response.status_code == 403
    raw_logs = stream.getvalue()
    records = [json.loads(line) for line in raw_logs.splitlines() if line]
    assert any(record["event"] == "auth.invalid" for record in records)
    assert secret not in raw_logs
    assert "also-secret" not in raw_logs
    assert "Bearer private" not in raw_logs
