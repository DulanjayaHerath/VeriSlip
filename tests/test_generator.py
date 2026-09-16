"""
Unit tests for Synthetic Slip & Tampering Engine.
"""

from core.ml.dataset_generator import SyntheticSlipGenerator

def test_authentic_slip_generation():
    generator = SyntheticSlipGenerator(width=400, height=700)
    img, meta = generator.generate_authentic_slip(
        bank_code="COMBANK",
        amount_lkr=15000.0,
        beneficiary_name="A. B. Perera"
    )

    assert img is not None
    assert img.size == (400, 700)
    assert meta["is_tampered"] is False
    assert meta["amount"] == 15000.0
    assert "field_bboxes" in meta
    assert "Amount" in meta["field_bboxes"]

def test_tampered_amount_generation():
    generator = SyntheticSlipGenerator(width=400, height=700)
    auth_img, auth_meta = generator.generate_authentic_slip(
        bank_code="SAMPATH",
        amount_lkr=5000.0
    )

    tampered_img, tamper_meta = generator.generate_tampered_slip(
        authentic_slip=auth_img,
        metadata=auth_meta,
        tamper_type="ALTER_AMOUNT",
        new_amount=50000.0
    )

    assert tampered_img is not None
    assert tamper_meta["is_tampered"] is True
    assert tamper_meta["tamper_type"] == "ALTER_AMOUNT"
    assert len(tamper_meta["ground_truth_boxes"]) > 0
    assert tamper_meta["ground_truth_boxes"][0]["label"] == "Forged Transaction Amount"
