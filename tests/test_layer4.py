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


def test_calibration_profile_integration():
    from core.forensics.unified_scorer import VeriSlipForensicEngine
    import json
    import os

    engine = VeriSlipForensicEngine()
    assert engine.calibration is not None
    assert "thresholds" in engine.calibration
    assert "authentic_max_risk" in engine.calibration["thresholds"]
    assert "tuned_weights" in engine.calibration

    # Test analysis on synthetic slip with calibration active
    dummy_img = Image.new("RGB", (300, 500), color=(255, 255, 255))
    res = engine.analyze(dummy_img)

    assert "verdict" in res
    assert res["verdict"] in ("AUTHENTIC", "SUSPICIOUS", "HIGH_RISK_TAMPERED")
    assert 0.0 <= res["tamper_risk_percentage"] <= 100.0


def test_vlm_semantic_reasoner_detects_branch_mismatch():
    from core.ml.vlm_semantic_reasoner import LightweightVisionLanguageReasoner

    reasoner = LightweightVisionLanguageReasoner()
    result = reasoner.evaluate(
        image=Image.new("RGB", (320, 480), color=(255, 255, 255)),
        ocr_tokens=[
            {"text": "Bank: HNB", "x": 10, "y": 10, "w": 80, "h": 20},
            {"text": "Branch: 081", "x": 10, "y": 40, "w": 90, "h": 20},
            {"text": "Account: 7654321", "x": 10, "y": 70, "w": 100, "h": 20},
        ],
        bank_code="HNB",
        reference_no="11111111",
        slip_context={"branch_code": "081", "account_prefix": "765"},
    )

    assert "anomaly_score" in result
    assert result["anomaly_score"] >= 0.0
    assert result["is_anomalous"] or result["structured_output"]["overall_consistency"] is False
    assert any("branch" in finding.lower() or "synthetic" in finding.lower() for finding in result["findings"])


def test_unified_scorer_includes_vlm_reasoning_breakdown():
    from core.forensics.unified_scorer import VeriSlipForensicEngine

    engine = VeriSlipForensicEngine()
    dummy_img = Image.new("RGB", (320, 480), color=(255, 255, 255))
    res = engine.analyze(dummy_img, bank_code="HNB", reference_no="11111111")

    assert "layer4_vlm_reasoning" in res["layer_breakdowns"]
    assert "score" in res["layer_breakdowns"]["layer4_vlm_reasoning"]
    assert 0.0 <= res["layer_breakdowns"]["layer4_vlm_reasoning"]["score"] <= 1.0

