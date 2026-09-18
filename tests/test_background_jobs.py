"""Integration tests for background forensic verification jobs."""

import io
import logging
import threading
import time

from fastapi.testclient import TestClient
from PIL import Image

from api.main import app


PRO_HEADERS = {"X-API-Key": "test-pro-key"}
client = TestClient(app, headers=PRO_HEADERS)


def _jpeg_bytes() -> bytes:
    image = Image.new("RGB", (120, 180), "white")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def _fake_result():
    return {
        "verdict": "AUTHENTIC",
        "verdict_color": "#22c55e",
        "tamper_risk_percentage": 1.0,
        "confidence_score": 0.99,
        "recommendation": "Safe test result",
        "flagged_regions": [],
        "findings_summary": [],
        "layer_breakdowns": {},
        "forensic_maps": None,
        "extracted_metadata": {"detected_bank_code": "COMBANK"},
    }


def _submit(headers=None):
    return client.post(
        "/api/v1/verify/jobs",
        headers=headers or {},
        files={"file": ("receipt.jpg", _jpeg_bytes(), "image/jpeg")},
    )


def _wait_for_terminal(job_id: str, attempts: int = 50):
    for _ in range(attempts):
        response = client.get(f"/api/v1/verify/jobs/{job_id}")
        assert response.status_code == 200
        if response.json()["status"] in {"completed", "failed"}:
            return response
        time.sleep(0.01)
    raise AssertionError("Background forensic job did not reach a terminal state")


def test_successful_background_forensic_job_preserves_correlation_id():
    response = _submit(headers={"X-Request-ID": "background-success-58"})

    assert response.status_code == 202
    submission = response.json()
    assert submission["status"] == "pending"
    assert submission["correlation_id"] == "background-success-58"
    assert response.headers["X-Request-ID"] == "background-success-58"

    completed = _wait_for_terminal(submission["job_id"]).json()
    assert completed["status"] == "completed"
    assert completed["correlation_id"] == "background-success-58"
    assert completed["result"]["verdict"] in {
        "AUTHENTIC",
        "SUSPICIOUS",
        "HIGH_RISK_TAMPERED",
    }
    assert completed["error"] is None


def test_background_job_failure_is_safe(monkeypatch):
    from api.routes import verify

    def fail_with_secret(*args, **kwargs):
        raise RuntimeError("private-image-data-must-not-leak")

    monkeypatch.setattr(verify, "_analyze_image", fail_with_secret)
    response = _submit(headers={"X-Request-ID": "background-failure-58"})
    assert response.status_code == 202

    failed_response = _wait_for_terminal(response.json()["job_id"])
    failed = failed_response.json()
    assert failed["status"] == "failed"
    assert failed["result"] is None
    assert failed["error"] == "Forensic analysis could not be completed."
    assert "private-image-data" not in failed_response.text


def test_background_submission_still_uses_image_sanitizer(monkeypatch):
    from api.routes import verify

    observed = threading.Event()
    original = verify.sanitize_image_bytes

    def observing_sanitizer(payload):
        observed.set()
        return original(payload)

    monkeypatch.setattr(verify, "sanitize_image_bytes", observing_sanitizer)

    response = _submit()

    assert response.status_code == 202
    assert observed.wait(timeout=1)
    _wait_for_terminal(response.json()["job_id"])


def test_background_job_endpoints_require_api_key():
    unauthenticated_client = TestClient(app)

    response = unauthenticated_client.post(
        "/api/v1/verify/jobs",
        files={"file": ("receipt.jpg", _jpeg_bytes(), "image/jpeg")},
    )

    assert response.status_code == 401
    assert response.headers["X-Request-ID"]


def test_job_status_is_isolated_between_api_keys():
    response = _submit()
    job_id = response.json()["job_id"]

    other_owner = client.get(
        f"/api/v1/verify/jobs/{job_id}",
        headers={"X-API-Key": "test-free-key"},
    )

    assert other_owner.status_code == 404
    _wait_for_terminal(job_id)


def test_concurrent_jobs_have_pending_or_processing_states(monkeypatch):
    from api.routes import verify

    release = threading.Event()
    started = []
    started_lock = threading.Lock()

    def blocking_analysis(*args, **kwargs):
        with started_lock:
            started.append(threading.current_thread().name)
        assert release.wait(timeout=2)
        return _fake_result()

    monkeypatch.setattr(verify, "_analyze_image", blocking_analysis)
    first = _submit()
    second = _submit()
    assert first.status_code == second.status_code == 202

    first_status = client.get(first.json()["status_url"]).json()["status"]
    second_status = client.get(second.json()["status_url"]).json()["status"]
    assert first_status in {"pending", "processing"}
    assert second_status in {"pending", "processing"}

    release.set()
    assert _wait_for_terminal(first.json()["job_id"]).json()["status"] == "completed"
    assert _wait_for_terminal(second.json()["job_id"]).json()["status"] == "completed"
    assert len(started) == 2
    assert all(name.startswith("verislip-forensics") for name in started)


def test_existing_synchronous_endpoint_runs_analysis_off_event_loop(monkeypatch):
    from api.routes import verify

    worker_threads = []

    def observing_analysis(*args, **kwargs):
        worker_threads.append(threading.current_thread())
        return _fake_result()

    monkeypatch.setattr(verify, "_analyze_image", observing_analysis)

    response = client.post(
        "/api/v1/verify",
        files={"file": ("receipt.jpg", _jpeg_bytes(), "image/jpeg")},
    )

    assert response.status_code == 200
    assert worker_threads
    assert worker_threads[0] is not threading.main_thread()


def test_failed_job_log_does_not_include_internal_exception(monkeypatch):
    from api.routes import verify

    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    job_logger = logging.getLogger("verislip.jobs")
    job_logger.addHandler(handler)

    def fail(*args, **kwargs):
        raise RuntimeError("sensitive-customer-reference-58")

    monkeypatch.setattr(verify, "_analyze_image", fail)
    try:
        response = _submit()
        _wait_for_terminal(response.json()["job_id"])
    finally:
        job_logger.removeHandler(handler)

    assert "forensic_job.failed" in stream.getvalue()
    assert "sensitive-customer-reference-58" not in stream.getvalue()
