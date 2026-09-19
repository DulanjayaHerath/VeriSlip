"""
Unit tests for LankaQR EMVCo parser, CRC-16 validator, and cross-verification engine (#122).
"""

from core.templates.lankaqr_parser import (
    compute_crc16_ccitt,
    build_lankaqr_string,
    parse_lankaqr,
    cross_verify_lankaqr_with_receipt,
)


def test_crc16_ccitt_computation():
    """Verify CRC-16 computation on known EMVCo sample."""
    # Standard test: appending CRC check sequence
    sample_header = "0002010102125303144540815000.005802LK5916COMMERCIAL MERCH6007Colombo6304"
    crc = compute_crc16_ccitt(sample_header)
    assert len(crc) == 4
    assert crc.isupper()
    # Self-validation
    full_payload = sample_header + crc
    parsed = parse_lankaqr(full_payload)
    assert parsed["is_valid"] is True
    assert parsed["crc_valid"] is True
    assert parsed["reported_crc"] == crc


def test_lankaqr_builder_and_parser():
    """Build and parse a dynamic LankaQR slip payload."""
    payload = build_lankaqr_string(
        amount=25450.75,
        reference_no="TXN9876543210",
        merchant_name="KEPITIYA STORE",
        merchant_city="Kandy"
    )

    parsed = parse_lankaqr(payload)
    assert parsed["is_valid"] is True
    assert parsed["is_lankaqr"] is True
    assert parsed["is_dynamic"] is True
    assert parsed["crc_valid"] is True
    assert parsed["amount"] == 25450.75
    assert parsed["currency"] == "LKR"
    assert parsed["country"] == "LK"
    assert parsed["merchant_name"] == "KEPITIYA STORE"
    assert parsed["merchant_city"] == "Kandy"
    assert parsed["reference_no"] == "TXN9876543210"


def test_lankaqr_cross_verification_authentic():
    """Cross-verify matching QR and receipt parameters."""
    payload = build_lankaqr_string(amount=12000.0, reference_no="TXN12345678")
    parsed = parse_lankaqr(payload)

    cross = cross_verify_lankaqr_with_receipt(
        qr_data=parsed,
        receipt_amount=12000.0,
        receipt_reference="TXN12345678"
    )

    assert cross["cross_verified"] is True
    assert cross["is_tampered"] is False
    assert cross["amount_matched"] is True
    assert cross["reference_matched"] is True
    assert len(cross["discrepancies"]) == 0


def test_lankaqr_cross_verification_altered_amount():
    """Detect fraud where receipt amount was forged upwards but QR remains original."""
    payload = build_lankaqr_string(amount=5000.0, reference_no="TXN12345678")
    parsed = parse_lankaqr(payload)

    # Attacker edited printed receipt to 50,000.00
    cross = cross_verify_lankaqr_with_receipt(
        qr_data=parsed,
        receipt_amount=50000.0,
        receipt_reference="TXN12345678"
    )

    assert cross["cross_verified"] is True
    assert cross["is_tampered"] is True
    assert cross["amount_matched"] is False
    assert any("Amount discrepancy" in d for d in cross["discrepancies"])


def test_lankaqr_cross_verification_corrupt_crc():
    """Detect corrupted or manually doctored QR payload with invalid CRC."""
    payload = build_lankaqr_string(amount=5000.0, reference_no="TXN12345678")
    # Corrupt last 2 hex chars of CRC
    corrupt_payload = payload[:-2] + "00"
    parsed = parse_lankaqr(corrupt_payload)

    assert parsed["crc_valid"] is False

    cross = cross_verify_lankaqr_with_receipt(
        qr_data=parsed,
        receipt_amount=5000.0,
        receipt_reference="TXN12345678"
    )
    assert cross["is_tampered"] is True
    assert any("Corrupt LankaQR CRC-16" in d for d in cross["discrepancies"])
