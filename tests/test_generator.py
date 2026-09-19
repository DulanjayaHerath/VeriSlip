"""
Unit tests for Synthetic Slip & Tampering Engine.
"""

import pytest

from core.internal.synthetic_slip_generator import SyntheticSlipGenerator


def test_generator_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("VERISLIP_ENABLE_SYNTHETIC_GENERATOR", raising=False)

    with pytest.raises(RuntimeError, match="Synthetic slip generation is disabled"):
        SyntheticSlipGenerator()


@pytest.mark.parametrize("value", ["0", "true", "TRUE", "yes"])
def test_generator_requires_explicit_enable_value(monkeypatch, value):
    monkeypatch.setenv("VERISLIP_ENABLE_SYNTHETIC_GENERATOR", value)

    with pytest.raises(RuntimeError, match="Synthetic slip generation is disabled"):
        SyntheticSlipGenerator()

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


def test_tampered_beneficiary_and_account_swapping():
    generator = SyntheticSlipGenerator(width=400, height=700)
    auth_img, auth_meta = generator.generate_authentic_slip(bank_code="BOC")

    tamp_ben_img, tamp_ben_meta = generator.generate_tampered_slip(
        authentic_slip=auth_img,
        metadata=auth_meta,
        tamper_type="SWAP_BENEFICIARY",
        new_beneficiary_name="Sunil Perera",
    )
    assert tamp_ben_img is not None
    assert tamp_ben_meta["is_tampered"] is True
    assert tamp_ben_meta["tampered_beneficiary"] == "Sunil Perera"
    assert any(b["label"] == "Swapped Beneficiary Name" for b in tamp_ben_meta["ground_truth_boxes"])

    tamp_acc_img, tamp_acc_meta = generator.generate_tampered_slip(
        authentic_slip=auth_img,
        metadata=auth_meta,
        tamper_type="SWAP_ACCOUNT",
        new_account="XXXX-XXXX-1122",
    )
    assert tamp_acc_img is not None
    assert tamp_acc_meta["is_tampered"] is True
    assert tamp_acc_meta["tampered_account"] == "XXXX-XXXX-1122"
    assert any(b["label"] == "Swapped Beneficiary Account" for b in tamp_acc_meta["ground_truth_boxes"])


def test_tampered_date_spoofing():
    generator = SyntheticSlipGenerator(width=400, height=700)
    auth_img, auth_meta = generator.generate_authentic_slip(bank_code="HNB")

    tamp_date_img, tamp_date_meta = generator.generate_tampered_slip(
        authentic_slip=auth_img,
        metadata=auth_meta,
        tamper_type="ALTER_DATE",
        new_date="2026-09-18 15:45:00",
    )
    assert tamp_date_img is not None
    assert tamp_date_meta["is_tampered"] is True
    assert tamp_date_meta["tampered_date_time"] == "2026-09-18 15:45:00"
    assert any(b["label"] == "Spoofed Transaction Timestamp" for b in tamp_date_meta["ground_truth_boxes"])


def test_multitier_tampering_skill_levels():
    """Verify multi-tier adversary skill levels (#32): naive, intermediate, expert."""
    generator = SyntheticSlipGenerator(width=400, height=700)
    auth_img, auth_meta = generator.generate_authentic_slip(bank_code="COMBANK", amount_lkr=20000.0)

    # 1. Naive tampering: has Photoshop EXIF metadata tag
    naive_img, naive_meta = generator.generate_tampered_slip(
        authentic_slip=auth_img,
        metadata=auth_meta,
        tamper_type="ALTER_AMOUNT",
        new_amount=80000.0,
        skill_level="naive"
    )
    assert naive_meta["skill_level"] == "naive"
    exif = naive_img.getexif()
    assert exif.get(0x0131) == "Adobe Photoshop Express"

    # 2. Intermediate tampering: strips editing software metadata
    inter_img, inter_meta = generator.generate_tampered_slip(
        authentic_slip=auth_img,
        metadata=auth_meta,
        tamper_type="ALTER_AMOUNT",
        new_amount=95000.0,
        skill_level="intermediate"
    )
    assert inter_meta["skill_level"] == "intermediate"
    inter_exif = inter_img.getexif()
    assert inter_exif.get(0x0131) is None

    # 3. Expert tampering: strips EXIF, aligns coordinates to 8x8 DCT grid boundary
    expert_img, expert_meta = generator.generate_tampered_slip(
        authentic_slip=auth_img,
        metadata=auth_meta,
        tamper_type="ALTER_AMOUNT",
        new_amount=150000.0,
        skill_level="expert"
    )
    assert expert_meta["skill_level"] == "expert"
    expert_exif = expert_img.getexif()
    assert expert_exif.get(0x0131) is None
    # Check 8x8 grid alignment on box x and y
    box = expert_meta["ground_truth_boxes"][0]["box"]
    assert box[0] % 8 == 0
    assert box[1] % 8 == 0


