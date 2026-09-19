"""
Unit tests for Layer 1: Structural & Bank Template Validation.
"""

import cv2
import numpy as np
from PIL import Image
from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
from core.forensics.layer1_structural import Layer1StructuralValidator


def _make_skewed_receipt(angle_deg: int) -> Image.Image:
    base = np.full((800, 1200, 3), 255, dtype=np.uint8)
    cv2.rectangle(base, (120, 100), (1080, 700), (245, 245, 245), -1)
    cv2.rectangle(base, (180, 150), (1020, 650), (235, 235, 235), -1)
    cv2.rectangle(base, (220, 200), (980, 600), (255, 255, 255), -1)

    src = np.float32([
        [180, 150],
        [1020, 150],
        [1020, 650],
        [180, 650],
    ])

    angle = np.deg2rad(angle_deg)
    cx, cy = 600, 400
    dst = np.float32([
        [180 + 80 * np.sin(angle), 160],
        [1020 + 70 * np.sin(angle), 220],
        [980 - 80 * np.sin(angle), 660],
        [240 - 60 * np.sin(angle), 690],
    ])

    warped = cv2.warpPerspective(base, cv2.getPerspectiveTransform(src, dst), (1200, 800))
    return Image.fromarray(warped)

def test_bank_identification():
    assert identify_bank_from_text("Commercial Bank of Ceylon Transfer") == "COMBANK"
    assert identify_bank_from_text("Sampath Vishwa Internet Banking") == "SAMPATH"
    assert identify_bank_from_text("BOC Digi Payment Receipt") == "BOC"
    assert identify_bank_from_text("Hatton National Bank SOLO") == "HNB"
    assert identify_bank_from_text("DFCC Virtual Wallet Payment") == "DFCC"
    assert identify_bank_from_text("Pan Asia Mobile Banking Transfer") == "PAN_ASIA"
    assert identify_bank_from_text("People's Bank PeoplesPay Transfer") == "PEOPLES"
    assert identify_bank_from_text("Unknown Bank XYZ") == "GENERIC_CEFTS"

def test_reference_number_validation():
    # Valid Commercial bank reference
    com_res = validate_reference_number("COMBANK", "TXN1098234812")
    assert com_res["valid"] is True

    # Valid DFCC reference
    dfcc_res = validate_reference_number("DFCC", "DFCC1029384756")
    assert dfcc_res["valid"] is True

    # Valid Pan Asia reference
    pabc_res = validate_reference_number("PAN_ASIA", "PABC90817263")
    assert pabc_res["valid"] is True

    # Obvious fake sequential reference
    fake_res = validate_reference_number("COMBANK", "123456789")
    assert fake_res["valid"] is False
    assert "trivial sequential" in fake_res["suspicious_note"]

    # Abnormally short reference
    short_res = validate_reference_number("SAMPATH", "123")
    assert short_res["valid"] is False

def test_layer1_evaluator():
    validator = Layer1StructuralValidator()
    # Create test blank image with smartphone dimensions (400x800)
    test_img = Image.new("RGB", (400, 800), color=(255, 255, 255))
    res = validator.evaluate(test_img, bank_code="GENERIC_CEFTS", reference_no="TXN987654321")

    assert "anomaly_score" in res
    assert "layer_name" in res
    assert res["anomaly_score"] >= 0.0


def test_receipt_perspective_rectification_for_skewed_slips():
    validator = Layer1StructuralValidator()

    for angle in [15, 25, 35, 45]:
        skewed = _make_skewed_receipt(angle)
        rectified = validator.rectify_perspective(skewed)

        assert rectified["used_fallback"] is False, f"Expected successful quad detection at {angle}°"
        assert rectified["confidence"] >= 0.6, f"Expected higher confidence at {angle}°"
        assert rectified["warped_image"].size == (827, 1169), f"Unexpected target size at {angle}°"

        eval_res = validator.evaluate(skewed, bank_code="GENERIC_CEFTS")
        assert "perspective_analysis" in eval_res
        assert eval_res["perspective_analysis"]["confidence"] >= 0.6
