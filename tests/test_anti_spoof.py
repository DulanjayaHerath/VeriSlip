"""Unit tests for screen spoofing / recapture detection."""

import numpy as np
from PIL import Image

from core.forensics.anti_spoof import ScreenMoireDetector, analyze_screen_recapture


def _make_moire_pattern(width: int = 512, height: int = 512) -> Image.Image:
    img = np.zeros((height, width), dtype=np.float32)
    for y in range(height):
        for x in range(width):
            img[y, x] = (
                180
                + 45 * np.sin(2 * np.pi * (0.08 * x + 0.07 * y))
                + 28 * np.sin(2 * np.pi * (0.12 * (x + y)))
            )
    return Image.fromarray(np.uint8(np.clip(img, 0, 255)))


def test_screen_moire_detector_detects_synthetic_moire():
    detector = ScreenMoireDetector()
    moire = _make_moire_pattern()

    res = detector.evaluate(moire)
    assert res["is_screen_recapture"] is True
    assert res["screen_spoof_confidence"] > 0.7
    assert res["moire_energy_ratio"] > 0.05

    res_module = analyze_screen_recapture(moire)
    assert res_module["is_screen_recapture"] is True
    assert res_module["screen_spoof_confidence"] >= res["screen_spoof_confidence"] * 0.95


def test_screen_moire_detector_rejects_plain_reference_image():
    plain = Image.new("L", (512, 512), 220)

    res = analyze_screen_recapture(plain)
    assert res["is_screen_recapture"] is False
    assert res["screen_spoof_confidence"] < 0.2
    assert res["moire_energy_ratio"] <= 0.01
