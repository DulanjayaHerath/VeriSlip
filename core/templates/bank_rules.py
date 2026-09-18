"""
Bank rules and template definitions for Sri Lankan financial institutions & payment slips.
Supports Commercial Bank, Sampath Vishwa, Bank of Ceylon (BOC), Hatton National Bank (HNB),
and generic CEFTS/SLIPS transfer slips.
"""

import re
from typing import Dict, Any, Optional, List

BANK_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "COMBANK": {
        "bank_name": "Commercial Bank of Ceylon PLC",
        "app_name": "ComBank Digital",
        "primary_color_rgb": (0, 75, 141),  # Commercial Bank Blue
        "ref_patterns": [
            r"^(?:CB|TXN|REF)?[0-9]{10,14}$",
            r"^[A-Z0-9]{12,16}$"
        ],
        "mandatory_fields": [
            "Reference",
            "Beneficiary",
            "Amount",
            "Date"
        ],
        "currency": "LKR",
        "amount_pattern": r"(?:LKR|Rs\.?)\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
    },
    "SAMPATH": {
        "bank_name": "Sampath Bank PLC",
        "app_name": "Sampath Vishwa",
        "primary_color_rgb": (243, 112, 33),  # Sampath Orange
        "ref_patterns": [
            r"^(?:SV|SAMP)?[0-9]{8,12}$",
            r"^[0-9]{10}$"
        ],
        "mandatory_fields": [
            "Transaction Ref",
            "To Account",
            "Amount",
            "Status"
        ],
        "currency": "LKR",
        "amount_pattern": r"(?:LKR|Rs\.?)\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
    },
    "BOC": {
        "bank_name": "Bank of Ceylon",
        "app_name": "BOC SmartPay / Digi / B-App",
        "primary_color_rgb": (255, 199, 44),  # BOC Gold/Yellow
        "ref_patterns": [
            r"^(?:BOC|DIGI)?[0-9]{9,13}$",
            r"^[0-9]{12}$"
        ],
        "mandatory_fields": [
            "Payment Reference",
            "Account",
            "Amount",
            "Date"
        ],
        "currency": "LKR",
        "amount_pattern": r"(?:LKR|Rs\.?)\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
    },
    "HNB": {
        "bank_name": "Hatton National Bank PLC",
        "app_name": "HNB Digital Banking / SOLO",
        "primary_color_rgb": (18, 53, 91),  # HNB Dark Blue & Gold
        "ref_patterns": [
            r"^(?:HNB|SOLO)?[0-9]{8,12}$",
            r"^[0-9]{10,14}$"
        ],
        "mandatory_fields": [
            "Reference Number",
            "Beneficiary",
            "Amount",
            "Transfer Date"
        ],
        "currency": "LKR",
        "amount_pattern": r"(?:LKR|Rs\.?)\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
    },
    "SEYLAN": {
        "bank_name": "Seylan Bank PLC",
        "app_name": "Seylan Mobile Banking",
        "primary_color_rgb": (166, 25, 46),  # Seylan Crimson Red
        "ref_patterns": [
            r"^(?:SEY|TXN)?[0-9]{8,14}$",
            r"^[0-9]{10,12}$"
        ],
        "mandatory_fields": [
            "Reference",
            "To Account",
            "Amount",
            "Date"
        ],
        "currency": "LKR",
        "amount_pattern": r"(?:LKR|Rs\.?)\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
    },
    "NTB_FRIMI": {
        "bank_name": "Nations Trust Bank / FriMi",
        "app_name": "FriMi / NTB Direct",
        "primary_color_rgb": (230, 0, 126),  # FriMi Magenta
        "ref_patterns": [
            r"^(?:FM|NTB)?[0-9]{8,14}$",
            r"^[A-Z0-9]{10,14}$"
        ],
        "mandatory_fields": [
            "Transaction ID",
            "Sent To",
            "Amount",
            "Date"
        ],
        "currency": "LKR",
        "amount_pattern": r"(?:LKR|Rs\.?)\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
    },
    "PEOPLES": {
        "bank_name": "People's Bank",
        "app_name": "People's Wave / PeoplesPay",
        "primary_color_rgb": (180, 20, 30),  # People's Bank Red
        "ref_patterns": [
            r"^[0-9]{16,22}$",
            r"^(?:PB|TRC)?[0-9]{10,22}$"
        ],
        "mandatory_fields": [
            "Pay from",
            "Pay to",
            "Amount",
            "Total debit amount",
            "Trace No"
        ],
        "currency": "LKR",
        "amount_pattern": r"(?:LKR|Rs\.?)\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
    },
    "GENERIC_CEFTS": {
        "bank_name": "CEFTS / LankaPay Interbank",
        "app_name": "Generic Payment Slip",
        "primary_color_rgb": (50, 50, 50),
        "ref_patterns": [
            r"^[A-Z0-9]{8,20}$"
        ],
        "mandatory_fields": [
            "Reference",
            "Amount"
        ],
        "currency": "LKR",
        "amount_pattern": r"(?:LKR|Rs\.?)\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
    }
}

def identify_bank_from_text(text: str) -> str:
    """Identify the bank template based on extracted text tokens."""
    text_upper = text.upper()
    if "COMMERCIAL BANK" in text_upper or "COMBANK" in text_upper or "CBC" in text_upper:
        return "COMBANK"
    elif "SAMPATH" in text_upper or "VISHWA" in text_upper:
        return "SAMPATH"
    elif "BANK OF CEYLON" in text_upper or "BOC" in text_upper or "SMARTPAY" in text_upper:
        return "BOC"
    elif "PEOPLE'S BANK" in text_upper or "PEOPLES" in text_upper or "PEOPLESPAY" in text_upper:
        return "PEOPLES"
    elif "HATTON NATIONAL" in text_upper or "HNB" in text_upper or "SOLO" in text_upper:
        return "HNB"
    elif "SEYLAN" in text_upper:
        return "SEYLAN"
    elif "FRIMI" in text_upper or "NATIONS TRUST" in text_upper or "NTB" in text_upper:
        return "NTB_FRIMI"
    return "GENERIC_CEFTS"

def validate_reference_number(bank_code: str, ref_number: str) -> Dict[str, Any]:
    """
    Validate reference number syntax and structure according to bank rules.
    """
    template = BANK_TEMPLATES.get(bank_code, BANK_TEMPLATES["GENERIC_CEFTS"])
    clean_ref = ref_number.strip().replace(" ", "").upper()
    
    is_valid = False
    matched_pattern = None
    for pattern in template["ref_patterns"]:
        if re.match(pattern, clean_ref):
            is_valid = True
            matched_pattern = pattern
            break
            
    # Check for obvious synthetic or suspicious dummy patterns (e.g. 111111111, 12345678)
    suspicious_note = None
    if clean_ref in {"123456789", "000000000", "111111111", "999999999", "1234567890"}:
        is_valid = False
        suspicious_note = "Reference number is a trivial sequential/repeated test pattern."
    elif len(clean_ref) < 6:
        is_valid = False
        suspicious_note = "Reference number is abnormally short for financial transaction."

    return {
        "valid": is_valid,
        "clean_reference": clean_ref,
        "bank_code": bank_code,
        "bank_name": template["bank_name"],
        "suspicious_note": suspicious_note,
        "matched_pattern": matched_pattern
    }
