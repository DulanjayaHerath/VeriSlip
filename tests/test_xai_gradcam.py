"""Focused tests for XAI Grad-CAM attribution and counterfactual evidence."""

import numpy as np
from PIL import Image

from core.forensics.xai_gradcam import Layer4GradCAM, compute_iou


def test_gradcam_heatmap_matches_edited_region_and_counterfactual():
    image = Image.new("RGB", (220, 220), color=(230, 230, 230))
    for y in range(80, 150):
        for x in range(90, 180):
            image.putpixel((x, y), (30, 30, 30))

    gradcam = Layer4GradCAM()
    result = gradcam.generate(image, ground_truth_box=[90, 80, 90, 70])

    assert result["heatmap"].shape == (220, 220)
    assert np.isfinite(result["heatmap"]).all()
    assert result["heatmap"].max() > 0.0
    assert result["bbox"][2] > 0 and result["bbox"][3] > 0
    assert result["overlay"].shape == (220, 220, 3)
    assert result["counterfactual"].shape == (220, 220, 3)
    assert result["heatmap_base64"].startswith("data:image/png;base64,")
    assert result["counterfactual_base64"].startswith("data:image/png;base64,")
    assert compute_iou([90, 80, 90, 70], result["bbox"]) > 0.75


def test_gradcam_can_generate_heatmap_from_forensic_tensor():
    image = Image.new("RGB", (160, 160), color=(250, 250, 250))
    forensic_tensor = np.zeros((3, 160, 160), dtype=np.float32)
    forensic_tensor[0, 50:110, 40:120] = 1.0
    forensic_tensor[1, 50:110, 40:120] = 0.8
    forensic_tensor[2, 50:110, 40:120] = 0.7

    result = Layer4GradCAM().generate(image, forensic_input=forensic_tensor)

    assert result["heatmap"].shape == (160, 160)
    assert result["bbox"][2] > 0
    assert result["bbox"][3] > 0

