"""Tests for sub-pixel glyph rasterization analysis."""

import cv2
import numpy as np
from PIL import Image

from core.forensics.font_anti_aliasing import FontAntiAliasingAnalyzer
from core.forensics.font_kerning import CharacterAlignmentValidator


def _receipt(alien: bool = False, seed: int = 0) -> Image.Image:
    rng = np.random.default_rng(seed)
    canvas = np.full((220, 720, 3), 248, dtype=np.uint8)
    cv2.putText(
        canvas,
        "LKR 123456789012",
        (30, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.4,
        (35, 35, 35),
        2,
        cv2.LINE_AA,
    )
    if alien:
        x = 480 + int(rng.integers(-2, 3))
        cv2.rectangle(canvas, (x - 4, 78), (685, 135), (248, 248, 248), -1)
        cv2.putText(
            canvas,
            "90",
            (x, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.4,
            (220, 55, 15),
            2,
            cv2.LINE_8,
        )
    return Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))


def test_genuine_glyphs_share_gradient_profile():
    result = FontAntiAliasingAnalyzer().analyze(_receipt())
    assert result["glyphs_analyzed"] >= 10
    assert result["is_anomalous"] is False
    assert result["outlier_count"] == 0


def test_pasted_characters_have_psf_or_color_fringe_divergence():
    genuine = FontAntiAliasingAnalyzer().analyze(_receipt())
    pasted = FontAntiAliasingAnalyzer().analyze(_receipt(alien=True))
    assert pasted["is_anomalous"] is True
    assert pasted["anomaly_score"] > genuine["anomaly_score"]
    assert any(region["fringe_z_score"] > 3.0 for region in pasted["detected_regions"])


def test_fixture_precision_exceeds_issue_target():
    labels = [False] * 16 + [True] * 16
    predictions = [
        FontAntiAliasingAnalyzer().analyze(_receipt(alien=label, seed=index))[
            "is_anomalous"
        ]
        for index, label in enumerate(labels)
    ]
    true_positives = sum(
        prediction and label for prediction, label in zip(predictions, labels)
    )
    false_positives = sum(
        prediction and not label for prediction, label in zip(predictions, labels)
    )
    precision = true_positives / max(true_positives + false_positives, 1)
    assert precision >= 0.88


def test_existing_font_validator_exposes_subpixel_breakdown():
    result = CharacterAlignmentValidator().evaluate(_receipt(alien=True))
    assert result["subpixel_rasterization"]["is_anomalous"] is True


def test_insufficient_glyphs_are_inconclusive_not_anomalous():
    image = Image.new("RGB", (80, 80), "white")
    result = FontAntiAliasingAnalyzer().analyze(image)
    assert result["status"] == "insufficient_glyphs"
    assert result["is_anomalous"] is False
