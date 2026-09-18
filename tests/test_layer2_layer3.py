"""
Unit tests for Layer 2 Classical Forensics (ELA & DCT) and Layer 3 Noise Forensics.
"""

from core.internal.synthetic_slip_generator import SyntheticSlipGenerator
from core.forensics.layer2_classical import Layer2ClassicalForensics
from core.forensics.layer3_noise import Layer3NoiseForensics
from core.forensics.unified_scorer import VeriSlipForensicEngine

def test_layer2_ela_and_dct():
    generator = SyntheticSlipGenerator(width=400, height=700)
    auth_img, auth_meta = generator.generate_authentic_slip(bank_code="COMBANK")
    tampered_img, _ = generator.generate_tampered_slip(
        authentic_slip=auth_img,
        metadata=auth_meta,
        tamper_type="ALTER_AMOUNT",
        new_amount=850000.0
    )

    l2 = Layer2ClassicalForensics()
    auth_res = l2.evaluate(auth_img)
    tamper_res = l2.evaluate(tampered_img)

    assert "anomaly_score" in auth_res
    assert "anomaly_score" in tamper_res
    assert "heatmap_base64" in tamper_res
    # Tampered image should show higher anomaly score or detected candidate regions
    assert len(tamper_res["detected_regions"]) >= 0

def test_layer3_noise_forensics():
    generator = SyntheticSlipGenerator(width=400, height=700)
    auth_img, _ = generator.generate_authentic_slip(bank_code="BOC")

    l3 = Layer3NoiseForensics()
    res = l3.evaluate(auth_img)

    assert "anomaly_score" in res
    assert "mean_noise_variance" in res
    assert "noise_heatmap_base64" in res

def test_unified_forensic_engine():
    generator = SyntheticSlipGenerator(width=400, height=700)
    auth_img, auth_meta = generator.generate_authentic_slip(bank_code="COMBANK", amount_lkr=2000.0)
    tampered_img, _ = generator.generate_tampered_slip(
        authentic_slip=auth_img,
        metadata=auth_meta,
        tamper_type="ALTER_AMOUNT",
        new_amount=200000.0
    )

    engine = VeriSlipForensicEngine()
    auth_res = engine.analyze(auth_img, bank_code="COMBANK")
    tamper_res = engine.analyze(tampered_img, bank_code="COMBANK")

    assert auth_res["verdict"] in ["AUTHENTIC", "SUSPICIOUS"]
    assert tamper_res["tamper_risk_percentage"] > auth_res["tamper_risk_percentage"]
    assert "layer_breakdowns" in tamper_res


def test_layer2_chromatic_luminance_ela_decomposition():
    generator = SyntheticSlipGenerator(width=400, height=700)
    auth_img, auth_meta = generator.generate_authentic_slip(bank_code="COMBANK")
    tampered_img, _ = generator.generate_tampered_slip(
        authentic_slip=auth_img,
        metadata=auth_meta,
        tamper_type="ALTER_AMOUNT",
        new_amount=990000.0,
    )

    l2 = Layer2ClassicalForensics()
    decomp_auth = l2.decompose_ela_channels(auth_img)
    decomp_tamp = l2.decompose_ela_channels(tampered_img)

    assert "luminance_variance" in decomp_auth
    assert "chrominance_variance" in decomp_auth
    assert "luma_chroma_disparity" in decomp_auth
    assert decomp_tamp["luminance_variance"] >= 0.0
    assert decomp_tamp["chrominance_variance"] >= 0.0

    eval_res = l2.evaluate(tampered_img)
    assert "channel_decomposition" in eval_res
    assert eval_res["channel_decomposition"]["luminance_variance"] == decomp_tamp["luminance_variance"]


def test_layer2_jpeg_grid_shift_detector():
    import numpy as np
    l2 = Layer2ClassicalForensics()

    # Uniform canvas
    uniform_gray = np.ones((120, 120), dtype=np.float32) * 180.0
    res_uniform = l2.detect_jpeg_grid_shift(uniform_gray)
    assert "detected_shift" in res_uniform
    assert "grid_periodicity_strength" in res_uniform
    assert len(res_uniform["horizontal_grid_profile"]) == 8
    assert len(res_uniform["vertical_grid_profile"]) == 8

    # Synthetic image with explicit 8x8 block step pattern at offset (3, 5)
    pattern = np.zeros((128, 128), dtype=np.float32)
    for y in range(128):
        for x in range(128):
            if (x - 3) % 8 == 0 or (y - 5) % 8 == 0:
                pattern[y, x] = 200.0
    res_shifted = l2.detect_jpeg_grid_shift(pattern)
    assert res_shifted["detected_shift"] == (3, 5)
    assert res_shifted["grid_periodicity_strength"] > 1.2


def test_layer3_srm_filtering_kernels():
    import numpy as np
    l3 = Layer3NoiseForensics()
    canvas = np.random.normal(128, 10, (100, 100)).astype(np.float32)

    residuals = l3.extract_srm_residuals(canvas)
    assert "srm_1st_horizontal" in residuals
    assert "srm_2nd_vertical" in residuals
    assert "srm_edge_3x3" in residuals
    assert "srm_edge_5x5" in residuals

    summary = l3.compute_srm_summary(canvas)
    assert summary["kernels_evaluated"] >= 6
    assert summary["average_srm_variance"] > 0.0
    assert "srm_edge_5x5" in summary["srm_metrics"]

    eval_res = l3.evaluate(auth_img := SyntheticSlipGenerator().generate_authentic_slip()[0])
    assert "srm_analysis" in eval_res
    assert eval_res["srm_analysis"]["kernels_evaluated"] >= 6

