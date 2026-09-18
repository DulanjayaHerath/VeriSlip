"""Integration tests for structured request tracing and correlation IDs."""

import io
import json
import logging
import uuid

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from api.main import app
from core.observability.logging import JsonLogFormatter, get_correlation_id


client = TestClient(app, headers={"X-API-Key": "test-pro-key"})


@pytest.fixture
def request_log_stream():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonLogFormatter())
    logger = logging.getLogger("verislip.request")
    logger.addHandler(handler)
    try:
        yield stream
    finally:
        logger.removeHandler(handler)


def _json_records(stream: io.StringIO):
    return [json.loads(line) for line in stream.getvalue().splitlines() if line]


def _jpeg_bytes() -> bytes:
    image = Image.new("RGB", (100, 160), "white")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_generates_request_id_and_returns_response_header(request_log_stream):
    response = client.get("/health")

    generated_id = response.headers["X-Request-ID"]
    assert str(uuid.UUID(generated_id)) == generated_id
    records = _json_records(request_log_stream)
    assert records[-1]["event"] == "request.completed"
    assert records[-1]["correlation_id"] == generated_id
    assert get_correlation_id() is None


@pytest.mark.parametrize("header", ["X-Request-ID", "X-Correlation-ID"])
def test_propagates_valid_caller_correlation_id(header, request_log_stream):
    caller_id = "checkout-2026_09.abc-123"

    response = client.get("/health", headers={header: caller_id})

    assert response.headers["X-Request-ID"] == caller_id
    assert all(
        record["correlation_id"] == caller_id
        for record in _json_records(request_log_stream)
    )


def test_replaces_unsafe_caller_request_id(request_log_stream):
    response = client.get("/health", headers={"X-Request-ID": "bad id\nforged"})

    returned_id = response.headers["X-Request-ID"]
    assert returned_id != "bad id\nforged"
    assert str(uuid.UUID(returned_id)) == returned_id


def test_correlation_context_reaches_image_processing(monkeypatch):
    caller_id = "verification-flow-59"
    observed = []
    from api.routes import verify

    original_sanitizer = verify.sanitize_image_bytes

    def observing_sanitizer(payload):
        observed.append(get_correlation_id())
        return original_sanitizer(payload)

    monkeypatch.setattr(verify, "sanitize_image_bytes", observing_sanitizer)

    response = client.post(
        "/api/v1/verify",
        headers={"X-Request-ID": caller_id},
        files={"file": ("receipt.jpg", _jpeg_bytes(), "image/jpeg")},
    )

    assert response.status_code == 200
    assert observed == [caller_id]
    assert response.headers["X-Request-ID"] == caller_id


def test_logs_safe_structured_error_without_sensitive_request_data(
    request_log_stream,
):
    secret_token = "Bearer super-secret-token-59"
    secret_body = b"private-receipt-contents-59"

    response = client.post(
        "/api/v1/verify?api_key=secret-query-key-59",
        headers={"Authorization": secret_token},
        files={"file": ("customer-94770000000.jpg", secret_body, "image/jpeg")},
    )

    assert response.status_code == 400
    assert response.headers["X-Request-ID"]
    raw_logs = request_log_stream.getvalue()
    records = _json_records(request_log_stream)
    completed = records[-1]
    assert completed["event"] == "request.completed"
    assert completed["path"] == "/api/v1/verify"
    assert completed["status_code"] == 400
    assert "secret-token-59" not in raw_logs
    assert "secret-query-key-59" not in raw_logs
    assert "private-receipt-contents-59" not in raw_logs
    assert "94770000000" not in raw_logs


def test_unhandled_exception_is_logged_and_returned_safely(
    monkeypatch, request_log_stream
):
    from api.routes import verify

    def fail_with_secret(*args, **kwargs):
        raise RuntimeError("database-password-should-not-appear")

    monkeypatch.setattr(verify.field_extractor, "extract_fields", fail_with_secret)

    response = client.post(
        "/api/v1/verify",
        headers={"X-Request-ID": "error-flow-59"},
        files={"file": ("receipt.jpg", _jpeg_bytes(), "image/jpeg")},
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error."}
    assert response.headers["X-Request-ID"] == "error-flow-59"
    raw_logs = request_log_stream.getvalue()
    failed = _json_records(request_log_stream)[-1]
    assert failed["event"] == "request.failed"
    assert failed["error_type"] == "RuntimeError"
    assert failed["correlation_id"] == "error-flow-59"
    assert "database-password-should-not-appear" not in raw_logs
