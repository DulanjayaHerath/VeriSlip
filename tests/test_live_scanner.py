"""Motion, buffer ownership, pre-screen routing, and authenticated camera API."""

import io
from unittest.mock import Mock

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from api.main import app
from api.routes import live_scanner
from core.forensics.live_stream import (
    LatestFrameBuffer,
    LiveFrameAnalyzer,
    MotionGate,
    OnnxPreScreen,
)
from scripts.live_stream_scanner import CameraCapture


def test_latest_buffer_recycles_storage_and_detaches_snapshots():
    buffer = LatestFrameBuffer()
    assert buffer.snapshot() is None
    source = np.zeros((60, 80, 3), dtype=np.uint8)
    buffer.publish(source)
    first = buffer.snapshot()
    for value in range(1, 100):
        source.fill(value)
        buffer.publish(source)
    sequence, latest = buffer.snapshot()
    assert buffer.allocations == 1
    assert sequence == 100
    assert np.all(latest == 99)
    assert np.all(first[1] == 0)
    latest.fill(200)
    assert np.all(buffer.snapshot()[1] == 99)
    assert buffer.snapshot(sequence) is None
    buffer.publish(np.zeros((30, 40, 3), dtype=np.uint8))
    assert buffer.allocations == 2


def test_motion_settles_once_and_rearms_after_document_moves():
    gate = MotionGate()
    frame = np.zeros((60, 80, 3), dtype=np.uint8)
    assert gate.update(frame, 0).moving
    assert not gate.update(frame, 0.5).ready
    settled = gate.update(frame, 0.7)
    assert settled.ready
    gate.mark_submitted()
    assert not gate.update(frame, 1).ready
    frame[20:40, 20:40] = 255
    moved = gate.update(frame, 1.1)
    assert moved.moving and moved.generation > settled.generation
    assert gate.update(frame, 1.8).ready


def test_motion_ignores_small_noise_but_detects_cumulative_drift():
    gate = MotionGate()
    frame = np.full((60, 80, 3), 100, dtype=np.uint8)
    gate.update(frame, 0)
    assert gate.update(frame + 2, 0.7).ready
    assert not gate.update(frame + 12, 0.8).moving
    assert gate.update(frame + 24, 0.9).moving


@pytest.mark.parametrize(
    "kwargs",
    [
        {"settle_seconds": 0},
        {"settle_seconds": float("nan")},
        {"changed_fraction": 2},
        {"intensity_threshold": 0},
    ],
)
def test_motion_rejects_invalid_configuration(kwargs):
    with pytest.raises(ValueError):
        MotionGate(**kwargs)


def fake_result():
    return {
        "verdict": "SUSPICIOUS",
        "tamper_risk_percentage": 55,
        "flagged_regions": [
            {"box": [10, 20, 30, 40], "confidence": 0.8, "label": "Review"}
        ],
        "recommendation": "Review this document",
    }


def test_no_checkpoint_runs_full_analysis_and_reports_box_coordinate_space():
    engine = Mock()
    engine.analyze.return_value = fake_result()
    result = LiveFrameAnalyzer(engine).analyze(Image.new("RGB", (2800, 1400)))
    assert result["status"] == "verified"
    assert result["frame_size"] == [1400, 700]
    assert engine.analyze.call_args.kwargs["pil_image"].size == (1400, 700)
    assert engine.analyze.call_args.kwargs["include_heatmaps"] is False
    assert result["prescreen_score"] is None


def test_prescreen_below_threshold_is_never_presented_as_verified():
    engine, screen = Mock(), Mock()
    screen.score.return_value = 0.1
    result = LiveFrameAnalyzer(engine, screen).analyze(Image.new("RGB", (320, 320)))
    assert result["status"] == "prescreen_only"
    assert result["verdict"] is None
    assert result["tamper_risk_percentage"] is None
    engine.analyze.assert_not_called()
    screen.score.return_value = 0.35
    engine.analyze.return_value = fake_result()
    assert (
        LiveFrameAnalyzer(engine, screen).analyze(Image.new("RGB", (320, 320)))[
            "status"
        ]
        == "verified"
    )


def test_onnx_prescreen_input_contract_and_invalid_output(monkeypatch):
    net = Mock()
    net.forward.return_value = np.array([[0.7]], dtype=np.float32)
    monkeypatch.setattr("cv2.dnn.readNetFromONNX", lambda path: net)
    screen = OnnxPreScreen("test.onnx")
    assert screen.score(Image.new("RGB", (10, 20), "red")) == pytest.approx(0.7)
    blob = net.setInput.call_args.args[0]
    assert blob.shape == (1, 3, 320, 320)
    assert np.all(blob[:, 0] == 1) and np.all(blob[:, 2] == 0)
    for output in (np.array([np.nan]), np.array([2]), np.array([0.1, 0.9])):
        net.forward.return_value = output
        with pytest.raises(ValueError):
            screen.score(Image.new("RGB", (320, 320)))


def image_upload():
    buf = io.BytesIO()
    Image.new("RGB", (80, 60)).save(buf, format="PNG")
    return {"file": ("camera.png", buf.getvalue(), "image/png")}


def test_live_api_auth_validation_and_worker_capacity(monkeypatch):
    client = TestClient(app)
    assert client.post("/api/v1/live/verify", files=image_upload()).status_code == 401
    client.headers["X-API-Key"] = "test-pro-key"
    response = client.post(
        "/api/v1/live/verify", files={"file": ("bad.png", b"bad", "image/png")}
    )
    assert response.status_code == 400
    analyzer = Mock()
    analyzer.analyze.return_value = {"status": "verified", **fake_result()}
    monkeypatch.setattr(live_scanner, "get_analyzer", lambda: analyzer)
    assert live_scanner._capacity.acquire(blocking=False)
    try:
        response = client.post("/api/v1/live/verify", files=image_upload())
        assert response.status_code == 503
        assert response.headers["Retry-After"] == "2"
    finally:
        live_scanner._capacity.release()
    response = client.post("/api/v1/live/verify", files=image_upload())
    assert response.status_code == 200
    assert response.headers["X-Request-ID"]
    analyzer.analyze.side_effect = RuntimeError("private-model-path")
    response = client.post("/api/v1/live/verify", files=image_upload())
    assert response.status_code == 500
    assert "private-model-path" not in response.text
    assert live_scanner._capacity.acquire(blocking=False)
    live_scanner._capacity.release()


def test_live_api_caps_upload_bytes(monkeypatch):
    monkeypatch.setattr("api.routes.verify.MAX_IMAGE_UPLOAD_BYTES", 8)
    response = TestClient(app, headers={"X-API-Key": "test-pro-key"}).post(
        "/api/v1/live/verify", files=image_upload()
    )
    assert response.status_code == 413


def test_capture_releases_camera_and_keeps_only_latest_frame(monkeypatch):
    camera = Mock()
    camera.isOpened.return_value = True
    camera.read.side_effect = [
        (True, np.full((10, 10, 3), value, np.uint8)) for value in range(5)
    ] + [(False, None)]
    monkeypatch.setattr("cv2.VideoCapture", lambda source: camera)
    capture = CameraCapture(0, fps=1000).start()
    assert capture.done.wait(timeout=2)
    capture.close()
    assert capture.frames.sequence == 5
    assert capture.frames.allocations == 1
    assert np.all(capture.frames.snapshot()[1] == 4)
    camera.release.assert_called_once()


def test_capture_open_failure_releases_device(monkeypatch):
    camera = Mock()
    camera.isOpened.return_value = False
    monkeypatch.setattr("cv2.VideoCapture", lambda source: camera)
    capture = CameraCapture(0).start()
    assert capture.done.wait(timeout=2)
    capture.close()
    assert capture.error
    camera.release.assert_called_once()
