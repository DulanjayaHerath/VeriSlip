"""
Unit tests for Block Artifact Grid (BAG) double-JPEG phase shift detection (#115).
"""

import numpy as np
import cv2
from PIL import Image

from core.forensics.layer2_classical import Layer2ClassicalForensics


def _create_jpeg_spliced_test_image(with_bag_splice: bool = False) -> np.ndarray:
    """Create synthetic test image with aligned or misaligned 8x8 JPEG compression grids."""
    # Create textured canvas
    canvas = np.full((320, 320), 230, dtype=np.uint8)
    for i in range(10, 310, 20):
        cv2.putText(canvas, f"Transaction Line {i:03d}", (20, i), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 30, 1)

    # Compress canvas at Quality 75
    _, enc = cv2.imencode('.jpg', canvas, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
    canvas_jpeg = cv2.imdecode(enc, cv2.IMREAD_GRAYSCALE)

    if with_bag_splice:
        # Create a separate patch compressed independently at Quality 85
        patch = np.full((80, 160), 240, dtype=np.uint8)
        cv2.putText(patch, "FORGED 950,000", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 10, 2)
        _, enc_p = cv2.imencode('.jpg', patch, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        patch_jpeg = cv2.imdecode(enc_p, cv2.IMREAD_GRAYSCALE)

        # Paste at non-multiple of 8 (e.g. x=67, y=103 -> offsets (3, 7))
        canvas_jpeg[103:183, 67:227] = patch_jpeg

    return canvas_jpeg


def test_block_artifact_grid_clean():
    """Clean uniformly compressed slip has aligned grid and no BAG anomalies."""
    clean = _create_jpeg_spliced_test_image(with_bag_splice=False)
    analyzer = Layer2ClassicalForensics()
    res = analyzer.detect_block_artifact_grid(clean)

    assert isinstance(res, dict)
    assert "has_bag_anomaly" in res
    assert res["has_bag_anomaly"] is False
    assert len(res["discrepant_regions"]) == 0
    assert np.all(res["bag_mask"] == 0)


def test_block_artifact_grid_spliced():
    """Spliced image with non-aligned patch generates BAG phase discrepancy."""
    spliced = _create_jpeg_spliced_test_image(with_bag_splice=True)
    analyzer = Layer2ClassicalForensics()

    # Pass the known spliced box
    boxes = [{"box": [67, 103, 160, 80]}]
    res = analyzer.detect_block_artifact_grid(spliced, candidate_boxes=boxes)

    assert isinstance(res, dict)
    assert res["has_bag_anomaly"] is True
    assert len(res["discrepant_regions"]) > 0
    assert np.sum(res["bag_mask"]) > 0


def test_block_artifact_grid_layer2_integration():
    """Layer 2 evaluate includes block_artifact_grid in output."""
    clean = _create_jpeg_spliced_test_image(with_bag_splice=False)
    pil_img = Image.fromarray(clean).convert("RGB")
    analyzer = Layer2ClassicalForensics()
    res = analyzer.evaluate(pil_img)

    assert "block_artifact_grid" in res
    assert "has_bag_anomaly" in res["block_artifact_grid"]
    assert "bag_mask" in res["block_artifact_grid"]
