"""
Unit tests for Layer 1: Structural & Bank Template Validation.
"""

from PIL import Image
from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
from core.forensics.layer1_structural import Layer1StructuralValidator

def test_bank_identification():
    assert identify_bank_from_text("Commercial Bank of Ceylon Transfer") == "COMBANK"
    assert identify_bank_from_text("Sampath Vishwa Internet Banking") == "SAMPATH"
    assert identify_bank_from_text("BOC Digi Payment Receipt") == "BOC"
    assert identify_bank_from_text("Hatton National Bank SOLO") == "HNB"
    assert identify_bank_from_text("Unknown Bank XYZ") == "GENERIC_CEFTS"

def test_reference_number_validation():
    # Valid Commercial bank reference
    com_res = validate_reference_number("COMBANK", "TXN1098234812")
    assert com_res["valid"] is True

    # Obvious fake sequential reference
    fake_res = validate_reference_number("COMBANK", "123456789")
    assert fake_res["valid"] is False
    assert "trivial sequential" in fake_res["suspicious_note"]

    # Abnormally short reference
    short_res = validate_reference_number("SAMPATH", "123")
    assert short_res["valid"] is False

def test_layer1_evaluator():
    validator = Layer1StructuralValidator()
    # Create test blank image with smartphone dimensions (400x800)
    test_img = Image.new("RGB", (400, 800), color=(255, 255, 255))
    res = validator.evaluate(test_img, bank_code="GENERIC_CEFTS", reference_no="TXN987654321")

    assert "anomaly_score" in res
    assert "layer_name" in res
    assert res["anomaly_score"] >= 0.0
