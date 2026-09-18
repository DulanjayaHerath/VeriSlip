import pytest
import numpy as np
import cv2
from PIL import Image

from core.forensics.font_kerning import CharacterAlignmentValidator


def test_character_alignment_validator_clean_image():
    """Verify that a synthetic uniform receipt number strip produces 0.0 anomaly score."""
    val = CharacterAlignmentValidator()
    # Create clean white canvas with aligned numerals
    img = Image.new("RGB", (600, 800), color=(255, 255, 255))
    img_np = np.array(img)
    # Draw aligned bank amount at y=300
    cv2.putText(img_np, "LKR 50,000.00", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20, 20, 20), 2, cv2.LINE_AA)
    test_img = Image.fromarray(img_np)

    result = val.evaluate(test_img)
    assert "anomaly_score" in result
    assert "is_anomalous" in result
    assert "detected_regions" in result
    assert "findings" in result
    assert result["anomaly_score"] < 0.20
    assert result["is_anomalous"] is False


def test_character_alignment_validator_spliced_baseline():
    """Verify that a spliced digit with >= 5px baseline jump is flagged."""
    val = CharacterAlignmentValidator(baseline_jump_threshold=4.5)
    img = Image.new("RGB", (600, 800), color=(255, 255, 255))
    img_np = np.array(img)

    # Draw digits where leading digits have a 6px vertical offset
    cur_x = 100
    baseline = 300
    # First 3 digits shifted
    for ch in "950":
        cv2.putText(img_np, ch, (cur_x, baseline - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20, 20, 20), 2, cv2.LINE_AA)
        cur_x += 18
    # Remaining digits at normal baseline
    for ch in "000":
        cv2.putText(img_np, ch, (cur_x, baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20, 20, 20), 2, cv2.LINE_AA)
        cur_x += 18

    test_img = Image.fromarray(img_np)
    result = val.evaluate(test_img)
    assert result["anomaly_score"] >= 0.50
    assert result["is_anomalous"] is True
    assert len(result["detected_regions"]) > 0
    assert "Numeral alignment anomaly" in result["findings"][0]
