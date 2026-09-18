"""Merchant verification history API and storage tests."""

from datetime import datetime, timezone
import hashlib
import io
import time

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from api.main import app
from api.routes import verify
from core.history.verification_history import InMemoryVerificationHistoryStore


PRO_KEY = "test-pro-key"
FREE_KEY = "test-free-key"
PRO_OWNER = hashlib.sha256(PRO_KEY.encode()).hexdigest()
FREE_OWNER = hashlib.sha256(FREE_KEY.encode()).hexdigest()
client = TestClient(app)


def _headers(key=PRO_KEY):
    return {"X-API-Key": key}


def _result(verdict="AUTHENTIC", risk=7.5):
    return {
        "verdict": verdict,
        "verdict_color": "#10b981",
        "tamper_risk_percentage": risk,
        "confidence_score": 0.9,
        "recommendation": "Verification complete.",
        "flagged_regions": [],
        "findings_summary": [],
        "layer_breakdowns": {},
        "forensic_maps": None,
        "extracted_metadata": {
            "detected_bank_code": "COMBANK",
            "bank_name": "Commercial Bank",
            "account_number": "must-not-be-stored",
        },
    }


def _jpeg():
    output = io.BytesIO()
    Image.new("RGB", (20, 20), "white").save(output, format="JPEG")
    return output.getvalue()


@pytest.fixture(autouse=True)
def clear_history():
    verify.history_store.clear()
    yield
    verify.history_store.clear()


def _add(owner, reference, *, verdict="AUTHENTIC", risk=7.5):
    return verify.history_store.add(
        owner,
        reference_no=reference,
        verdict=verdict,
        tamper_risk_percentage=risk,
        bank_code="COMBANK",
        bank_name="Commercial Bank",
    )


def test_successful_verification_is_added_to_merchant_history(monkeypatch):
    monkeypatch.setattr(verify, "_analyze_image", lambda *args, **kwargs: _result())
    response = client.post(
        "/api/v1/verify",
        headers=_headers(),
        files={"file": ("receipt.jpg", _jpeg(), "image/jpeg")},
        data={"reference_no": "REF-1001"},
    )
    assert response.status_code == 200

    history = client.get("/api/v1/verifications/history", headers=_headers())
    assert history.status_code == 200
    payload = history.json()
    assert payload["total"] == 1
    assert payload["items"][0]["reference_no"] == "REF-1001"
    assert payload["items"][0]["verdict"] == "AUTHENTIC"
    assert "account_number" not in payload["items"][0]
    assert "forensic_maps" not in payload["items"][0]


def test_reference_search_is_case_insensitive_and_supports_no_results():
    _add(PRO_OWNER, "ORDER-ABC-100")
    _add(PRO_OWNER, "ORDER-XYZ-200")

    match = client.get(
        "/api/v1/verifications/history?reference=abc", headers=_headers()
    ).json()
    assert match["total"] == 1
    assert match["items"][0]["reference_no"] == "ORDER-ABC-100"

    no_match = client.get(
        "/api/v1/verifications/history?reference=missing", headers=_headers()
    ).json()
    assert no_match["total"] == 0
    assert no_match["items"] == []


def test_date_filter_is_inclusive(monkeypatch):
    monkeypatch.setattr(
        verify.history_store,
        "_clock",
        lambda: datetime(2026, 9, 17, 23, 59, tzinfo=timezone.utc),
    )
    _add(PRO_OWNER, "DAY-ONE")
    monkeypatch.setattr(
        verify.history_store,
        "_clock",
        lambda: datetime(2026, 9, 18, 12, 0, tzinfo=timezone.utc),
    )
    _add(PRO_OWNER, "DAY-TWO")

    response = client.get(
        "/api/v1/verifications/history?date_from=2026-09-18&date_to=2026-09-18",
        headers=_headers(),
    )
    assert response.status_code == 200
    assert [item["reference_no"] for item in response.json()["items"]] == ["DAY-TWO"]


def test_history_pagination_and_ordering():
    for index in range(5):
        _add(PRO_OWNER, f"REF-{index}")

    first = client.get(
        "/api/v1/verifications/history?page=1&page_size=2", headers=_headers()
    ).json()
    second = client.get(
        "/api/v1/verifications/history?page=2&page_size=2", headers=_headers()
    ).json()
    assert first["total"] == 5
    assert first["has_more"] is True
    assert len(first["items"]) == 2
    assert {item["verification_id"] for item in first["items"]}.isdisjoint(
        {item["verification_id"] for item in second["items"]}
    )


def test_empty_history_and_merchant_isolation():
    _add(PRO_OWNER, "PRIVATE-PRO-REFERENCE")

    other = client.get(
        "/api/v1/verifications/history", headers=_headers(FREE_KEY)
    )
    assert other.status_code == 200
    assert other.json()["items"] == []
    assert other.json()["total"] == 0


@pytest.mark.parametrize(
    "query,expected_status",
    [
        ("date_from=not-a-date", 422),
        ("page=0", 422),
        ("page_size=101", 422),
        ("date_from=2026-09-19&date_to=2026-09-18", 400),
    ],
)
def test_history_rejects_malformed_queries(query, expected_status):
    response = client.get(
        f"/api/v1/verifications/history?{query}", headers=_headers()
    )
    assert response.status_code == expected_status
    assert "traceback" not in response.text.lower()


def test_history_requires_api_authentication():
    response = client.get("/api/v1/verifications/history")
    assert response.status_code == 401


def test_failed_verification_is_not_recorded(monkeypatch):
    def fail(*args, **kwargs):
        raise verify.ForensicAnalysisError

    monkeypatch.setattr(verify, "_analyze_image", fail)
    response = client.post(
        "/api/v1/verify",
        headers=_headers(),
        files={"file": ("receipt.jpg", _jpeg(), "image/jpeg")},
        data={"reference_no": "FAILED-REF"},
    )
    assert response.status_code == 500
    history = client.get("/api/v1/verifications/history", headers=_headers()).json()
    assert history["total"] == 0


def test_completed_background_verification_is_recorded_once(monkeypatch):
    monkeypatch.setattr(verify, "_analyze_image", lambda *args, **kwargs: _result())
    submitted = client.post(
        "/api/v1/verify/jobs",
        headers=_headers(),
        files={"file": ("receipt.jpg", _jpeg(), "image/jpeg")},
        data={"reference_no": "ASYNC-100"},
    )
    assert submitted.status_code == 202
    status_url = submitted.json()["status_url"]
    for _ in range(100):
        status = client.get(status_url, headers=_headers()).json()
        if status["status"] == "completed":
            break
        time.sleep(0.005)
    assert status["status"] == "completed"

    history = client.get(
        "/api/v1/verifications/history?reference=ASYNC-100", headers=_headers()
    ).json()
    assert history["total"] == 1


def test_local_store_is_bounded_and_keeps_metadata_only():
    store = InMemoryVerificationHistoryStore(max_records=2, retention_days=10)
    for index in range(3):
        store.add(
            PRO_OWNER,
            reference_no=f"REF-{index}",
            verdict="AUTHENTIC",
            tamper_risk_percentage=1.0,
        )
    page = store.search(PRO_OWNER)
    assert page.total == 2
    assert {item.reference_no for item in page.items} == {"REF-1", "REF-2"}
