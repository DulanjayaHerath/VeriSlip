"""
Unit tests for Layer 2 copy-move forgery detection.
Tests:
- ORB/SIFT keypoint matching copy-move detector (#19)
- Overlapping block DCT lexicographical correlation copy-move detector (#20)
- Integration with Layer2ClassicalForensics
"""

import numpy as np
import cv2
from PIL import Image

from core.forensics.layer2_copymove import (
    detect_copymove_orb,
    detect_copymove_block_dct,
    analyze_copymove_forensics,
)
from core.forensics.layer2_classical import Layer2ClassicalForensics


def _create_synthetic_test_slip(with_copy_move: bool = False) -> np.ndarray:
    """Create a synthetic high-contrast test image with patterned text / symbols."""
    img = np.full((300, 400, 3), 245, dtype=np.uint8)
    
    # Draw some structured background and text
    cv2.putText(img, "COMMERCIAL BANK", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20, 20, 100), 2)
    cv2.putText(img, "Ref: 9847120394", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (40, 40, 40), 1)
    cv2.putText(img, "Amount: LKR 45,000.00", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (10, 10, 10), 2)
    
    # Add a patterned logo box
    cv2.rectangle(img, (320, 20), (370, 70), (0, 120, 0), -1)
    cv2.circle(img, (345, 45), 15, (255, 255, 255), 2)

    if with_copy_move:
        # Clone a complex patch (e.g. amount text + logo) to another region
        patch = img[100:140, 30:200].copy()
        img[200:240, 150:320] = patch

        # Also duplicate the logo
        logo_patch = img[20:70, 320:370].copy()
        img[220:270, 30:80] = logo_patch

    return img


def test_copymove_orb_clean():
    """Clean slip without cloned regions should not trigger copy-move alarm."""
    clean_img = _create_synthetic_test_slip(with_copy_move=False)
    res = detect_copymove_orb(clean_img, min_matches=6)
    assert isinstance(res, dict)
    assert "detected" in res
    assert res["detected"] is False
    assert res["match_count"] < 6


def test_copymove_orb_cloned():
    """Tampered slip with duplicated logo and amount text should detect keypoint pairs."""
    tampered_img = _create_synthetic_test_slip(with_copy_move=True)
    res = detect_copymove_orb(tampered_img, min_matches=3, match_ratio=0.85)
    assert isinstance(res, dict)
    assert res["match_count"] >= 3
    assert res["detected"] is True
    assert res["confidence"] > 0.0
    assert len(res["clone_pairs"]) > 0
    # First clone pair should have spatial distance >= 30
    assert res["clone_pairs"][0]["spatial_distance"] >= 30.0


def test_copymove_block_dct_clean():
    """Clean slip should have low or zero duplicate block correlation."""
    clean_img = _create_synthetic_test_slip(with_copy_move=False)
    res = detect_copymove_block_dct(clean_img, min_matches=10)
    assert isinstance(res, dict)
    assert res["detected"] is False


def test_copymove_block_dct_cloned():
    """Tampered slip with duplicated patch should detect matching 8x8 DCT blocks."""
    tampered_img = _create_synthetic_test_slip(with_copy_move=True)
    res = detect_copymove_block_dct(tampered_img, min_matches=3, step=4, min_shift=15.0)
    assert isinstance(res, dict)
    assert "match_count" in res
    assert res["detected"] is True
    assert len(res["matches"]) >= 3


def test_analyze_copymove_forensics_unified():
    """Unified copy-move analyzer returns both detectors and findings."""
    tampered_img = _create_synthetic_test_slip(with_copy_move=True)
    res = analyze_copymove_forensics(tampered_img)
    assert res["has_copymove"] is True
    assert res["copymove_confidence"] > 0.0
    assert len(res["findings"]) > 0


def test_layer2_classical_integration():
    """Layer2ClassicalForensics.evaluate() properly includes copy-move analysis."""
    analyzer = Layer2ClassicalForensics()
    clean_img = _create_synthetic_test_slip(with_copy_move=False)
    pil_clean = Image.fromarray(cv2.cvtColor(clean_img, cv2.COLOR_BGR2RGB))
    
    result = analyzer.evaluate(pil_clean)
    assert "copy_move_analysis" in result
    assert "has_copymove" in result["copy_move_analysis"]
