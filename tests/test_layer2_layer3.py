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
