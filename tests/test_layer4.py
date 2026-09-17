"""
Unit tests for Layer 4 Deep Learning Ensemble and Dual-Stream Model.
"""

import numpy as np
from PIL import Image
from core.ml.ensemble_model import Layer4DeepEnsemble, DualStreamForensicNetwork, TORCH_AVAILABLE


def test_layer4_deep_ensemble_fallback_and_inference():
    l4 = Layer4DeepEnsemble(target_size=(128, 128))
    
    # Create test synthetic image and forensic matrices
    dummy_img = Image.new("RGB", (200, 300), color=(240, 240, 240))
    dummy_ela = np.zeros((300, 200), dtype=np.uint8)
    dummy_noise = np.zeros((300, 200), dtype=np.float32)

    res = l4.evaluate(dummy_img, dummy_ela, dummy_noise)

    assert "anomaly_score" in res
    assert "is_anomalous" in res
    assert "engine" in res
    assert "detected_regions" in res
    assert 0.0 <= res["anomaly_score"] <= 1.0


def test_layer4_dualstream_architecture():
    if not TORCH_AVAILABLE:
        return

    import torch
    model = DualStreamForensicNetwork()
    model.eval()

    # Batch of 2, 3x128x128
    rgb = torch.randn(2, 3, 128, 128)
    forensic = torch.randn(2, 3, 128, 128)

    with torch.no_grad():
        prob, loc_map = model(rgb, forensic)
        sig_prob = torch.sigmoid(prob)
        sig_loc = torch.sigmoid(loc_map)

    assert prob.shape == (2, 1)
    assert loc_map.shape == (2, 1, 128, 128)
    assert 0.0 <= sig_prob.min().item() <= 1.0
    assert 0.0 <= sig_prob.max().item() <= 1.0
    assert 0.0 <= sig_loc.min().item() <= 1.0
    assert 0.0 <= sig_loc.max().item() <= 1.0
