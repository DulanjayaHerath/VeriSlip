"""Security and contract tests for the Courier Rider API."""

import base64
import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from api.main import app
from api.routes import courier


client = TestClient(app)
HEADERS = {"X-API-Key": "test-courier-pro-key"}


def _image_bytes(image_format="JPEG"):
    output = io.BytesIO()
    Image.new("RGB", (40, 60), "white").save(output, format=image_format)
    return output.getvalue()


def _payload(image_bytes=None):
    return {
        "waybill_id": "WB-882910",
        "expected_cod_amount": 12_500.0,
        "slip_base64": base64.b64encode(image_bytes or _image_bytes()).decode("ascii"),
        "target_bank": "COMBANK",
    }


def _forensic_result(verdict="AUTHENTIC", risk=8.5, amount=12_500.0):
    metadata = {"detected_bank_code": "COMBANK", "bank_name": "Commercial Bank"}
    if amount is not None:
        metadata["amount"] = amount
    return {
        "verdict": verdict,
        "tamper_risk_percentage": risk,
        "extracted_metadata": metadata,
    }


def test_successful_low_risk_courier_verification(monkeypatch):
    monkeypatch.setattr(courier, "_analyze_image", lambda *args, **kwargs: _forensic_result())
    response = client.post("/api/v1/courier/verify", headers=HEADERS, json=_payload())
    assert response.status_code == 200
    data = response.json()
    assert data["waybill_id"] == "WB-882910"
    assert data["can_handover_package"] is True
    assert data["rider_action"] == "HANDOVER_PACKAGE_CONFIRMED"
    assert data["risk_level"] == "SAFE"
    assert data["amount_mismatch"] is False
    assert data["cashier_alert"] is None


@pytest.mark.parametrize(
    "verdict,risk", [("SUSPICIOUS", 30.0), ("HIGH_RISK_TAMPERED", 91.0)]
)
def test_suspicious_and_high_risk_results_block_handover(
    monkeypatch, verdict, risk
):
    monkeypatch.setattr(
        courier, "_analyze_image", lambda *args, **kwargs: _forensic_result(verdict, risk)
    )
    response = client.post("/api/v1/courier/verify", headers=HEADERS, json=_payload())
    assert response.status_code == 200
    assert response.json()["can_handover_package"] is False
    assert response.json()["rider_action"] == "DO_NOT_HANDOVER_SUSPECTED_FORGERY"
    assert response.json()["cashier_alert"]


def test_amount_mismatch_blocks_handover(monkeypatch):
    monkeypatch.setattr(
        courier, "_analyze_image", lambda *args, **kwargs: _forensic_result(amount=10_000.0)
    )
    response = client.post("/api/v1/courier/verify", headers=HEADERS, json=_payload())
    assert response.status_code == 200
    assert response.json()["amount_mismatch"] is True
    assert response.json()["can_handover_package"] is False
    assert response.json()["rider_action"] == "DO_NOT_HANDOVER_AMOUNT_MISMATCH"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"waybill_id": "", "expected_cod_amount": -1, "slip_base64": ""},
        {"waybill_id": "WB-1", "expected_cod_amount": "not-a-number", "slip_base64": "abc"},
    ],
)
def test_malformed_or_missing_request_is_rejected(payload):
    response = client.post("/api/v1/courier/verify", headers=HEADERS, json=payload)
    assert response.status_code == 422


def test_invalid_image_is_rejected_without_internal_details():
    payload = _payload()
    payload["slip_base64"] = "not-valid-base64%%%"
    response = client.post("/api/v1/courier/verify", headers=HEADERS, json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Image payload is not valid base64."
    assert "traceback" not in response.text.lower()


def test_unsupported_image_is_rejected_by_shared_sanitizer():
    response = client.post(
        "/api/v1/courier/verify", headers=HEADERS, json=_payload(_image_bytes("GIF"))
    )
    assert response.status_code == 415
    assert response.json()["detail"] == "Unsupported image format. Only JPEG and PNG are accepted."


def test_oversized_image_is_rejected_before_decode(monkeypatch):
    monkeypatch.setattr(courier, "MAX_ENCODED_IMAGE_CHARS", 8)
    response = client.post("/api/v1/courier/verify", headers=HEADERS, json=_payload())
    assert response.status_code == 413
    assert response.json()["detail"] == "Image upload exceeds the permitted size."


def test_courier_endpoint_requires_api_key():
    response = client.post("/api/v1/courier/verify", json=_payload())
    assert response.status_code == 401


def test_courier_endpoint_preserves_rate_and_correlation_headers(monkeypatch):
    monkeypatch.setattr(courier, "_analyze_image", lambda *args, **kwargs: _forensic_result())
    response = client.post(
        "/api/v1/courier/verify",
        headers={**HEADERS, "X-Request-ID": "courier-request-78"},
        json=_payload(),
    )
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "courier-request-78"
    assert response.headers["X-RateLimit-Limit"] == "100"
    assert "X-RateLimit-Remaining" in response.headers


def test_forensic_failure_returns_safe_error(monkeypatch):
    def fail(*args, **kwargs):
        raise courier.ForensicAnalysisError

    monkeypatch.setattr(courier, "_analyze_image", fail)
    response = client.post("/api/v1/courier/verify", headers=HEADERS, json=_payload())
    assert response.status_code == 500
    assert response.json()["detail"] == "Forensic analysis could not be completed."
    assert "traceback" not in response.text.lower()
