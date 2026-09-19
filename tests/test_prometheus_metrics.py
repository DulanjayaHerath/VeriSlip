"""
Unit tests for Prometheus metrics collection and /metrics endpoint (#88).
"""

import json
from fastapi.testclient import TestClient
from api.main import app
from core.observability.metrics import (
    record_request_metrics,
    record_layer_duration,
    record_verification_verdict,
    set_active_learning_queue_gauge,
    get_metrics_payload,
)


def test_metrics_recording_helpers():
    """Verify helper recording functions increment Prometheus metrics."""
    record_request_metrics("POST", "/api/v1/verify", 200, 0.42)
    record_layer_duration("Layer 2: Classical", 0.085)
    record_verification_verdict("AUTHENTIC", "COMBANK")
    set_active_learning_queue_gauge(7)

    payload = get_metrics_payload().decode("utf-8")
    assert "verislip_http_requests_total" in payload
    assert "verislip_http_request_duration_seconds" in payload
    assert "verislip_forensic_layer_duration_seconds" in payload
    assert "verislip_verification_verdicts_total" in payload
    assert "verislip_active_learning_queue_size 7.0" in payload


def test_metrics_endpoint_http():
    """Test HTTP GET /metrics response status and content type."""
    client = TestClient(app)
    # Trigger a request to generate metrics
    health_resp = client.get("/health")
    assert health_resp.status_code == 200

    metrics_resp = client.get("/metrics")
    assert metrics_resp.status_code == 200
    assert "text/plain" in metrics_resp.headers["content-type"]
    text = metrics_resp.text
    assert "verislip_http_requests_total" in text
    assert 'endpoint="/health"' in text
