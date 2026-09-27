"""Bounded camera buffering and motion-gated forensic analysis.

Preview and inference have separate clocks: camera frames never queue behind an
expensive scan. No camera image is persisted by this module.
"""

import math
import threading
import time
from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image

from core.forensics.utils import normalize_dimensions


class LatestFrameBuffer:
    """One reusable capture slot; snapshots own their pixels independently."""

    def __init__(self):
        self._lock = threading.Lock()
        self._frame = None
        self.sequence = 0
        self.allocations = 0

    def publish(self, frame):
        if frame is None or frame.ndim != 3 or frame.shape[2] != 3:
            raise ValueError("Expected a BGR camera frame")
        with self._lock:
            if (
                self._frame is None
                or self._frame.shape != frame.shape
                or self._frame.dtype != frame.dtype
            ):
                self._frame = np.empty_like(frame)
                self.allocations += 1
            np.copyto(self._frame, frame)
            self.sequence += 1

    def snapshot(self, after_sequence=0):
        with self._lock:
            if self._frame is None or self.sequence <= after_sequence:
                return None
            return self.sequence, self._frame.copy()


@dataclass(frozen=True)
class MotionState:
    moving: bool
    ready: bool
    generation: int
    change_fraction: float


class MotionGate:
    """Compare against a fixed scene anchor so slow drift cannot look stable.

    Thresholds are pixel/intensity based, not millimetres: physical displacement
    requires camera-specific calibration. Only one scan is requested per scene.
    """

    def __init__(
        self, settle_seconds=0.6, intensity_threshold=18, changed_fraction=0.015
    ):
        if not math.isfinite(settle_seconds) or settle_seconds <= 0:
            raise ValueError("settle_seconds must be positive")
        if not 0 < intensity_threshold < 255 or not 0 < changed_fraction <= 1:
            raise ValueError("Invalid motion thresholds")
        self.settle_seconds = settle_seconds
        self.intensity_threshold = intensity_threshold
        self.changed_fraction = changed_fraction
        self.anchor = None
        self.since = 0.0
        self.generation = 0
        self.consumed = False

    def update(self, frame, now=None):
        now = time.monotonic() if now is None else now
        gray = cv2.cvtColor(cv2.resize(frame, (80, 60)), cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        fraction = (
            1.0
            if self.anchor is None
            else float(
                np.mean(cv2.absdiff(gray, self.anchor) > self.intensity_threshold)
            )
        )
        moving = fraction >= self.changed_fraction
        if moving:
            self.anchor = gray
            self.since = now
            self.generation += 1
            self.consumed = False
        ready = (
            not moving and not self.consumed and now - self.since >= self.settle_seconds
        )
        return MotionState(moving, ready, self.generation, fraction)

    def mark_submitted(self):
        self.consumed = True


class OnnxPreScreen:
    """Optional trained CNN: RGB NCHW float32 [0,1], 320x320, one probability.

    A checkpoint must be explicitly supplied; random weights are never used to
    bypass verification. OpenCV DNN access is serialized because nets are mutable.
    """

    def __init__(self, model_path):
        self.net = cv2.dnn.readNetFromONNX(str(model_path))
        self._lock = threading.Lock()

    def score(self, image):
        rgb = np.asarray(image.convert("RGB"))
        blob = cv2.dnn.blobFromImage(rgb, 1 / 255.0, (320, 320), swapRB=False)
        with self._lock:
            self.net.setInput(blob)
            values = np.asarray(self.net.forward()).reshape(-1)
        if values.size != 1 or not np.isfinite(values[0]) or not 0 <= values[0] <= 1:
            raise ValueError("Pre-screen CNN must return one probability in [0,1]")
        return float(values[0])


class LiveFrameAnalyzer:
    def __init__(self, engine, prescreen=None, threshold=0.35):
        if not 0 <= threshold <= 1:
            raise ValueError("Invalid pre-screen threshold")
        self.engine = engine
        self.prescreen = prescreen
        self.threshold = threshold

    def analyze(self, image):
        started = time.perf_counter()
        score = self.prescreen.score(image) if self.prescreen else None
        prescreen_ms = (
            (time.perf_counter() - started) * 1000 if self.prescreen else None
        )
        # Bound geometry once so returned regions share the stated coordinate space.
        normalized = normalize_dimensions(image, max_dim=1400)
        payload = {
            "frame_size": list(normalized.size),
            "prescreen_score": score,
            "prescreen_ms": prescreen_ms,
            "flagged_regions": [],
            "verdict": None,
            "tamper_risk_percentage": None,
        }
        if score is not None and score < self.threshold:
            payload.update(
                status="prescreen_only",
                recommendation=(
                    "No pre-screen trigger. Full verification has not been performed."
                ),
            )
        else:
            result = self.engine.analyze(pil_image=normalized, include_heatmaps=False)
            payload.update(status="verified")
            for key in (
                "verdict",
                "tamper_risk_percentage",
                "flagged_regions",
                "recommendation",
            ):
                payload[key] = result[key]
        payload["analysis_ms"] = (time.perf_counter() - started) * 1000
        return payload

    def analyze_bgr(self, frame):
        return self.analyze(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
