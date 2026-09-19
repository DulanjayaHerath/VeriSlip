"""
Fintech Core: LankaQR EMVCo-Compliant Dynamic QR Code Parser & Cross-Verification Engine (#122).
Adheres to CBSL LankaQR Specification and EMVCo Merchant-Presented QR Standards.
"""

from typing import Dict, Any, List, Optional, Tuple
import cv2
import numpy as np


def compute_crc16_ccitt(data: str) -> str:
    """
    Compute CRC-16/CCITT-FALSE checksum for EMVCo / LankaQR specification.
    Polynomial: 0x1021, Initial: 0xFFFF, No reflection, Final XOR: 0x0000.
    Returns 4-character uppercase hexadecimal string.
    """
    crc = 0xFFFF
    for char in data.encode("utf-8"):
        crc ^= (char << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def parse_tlv_string(payload: str) -> Dict[str, str]:
    """Parse EMVCo Tag-Length-Value (TLV) string into tag -> value map."""
    tags = {}
    idx = 0
    length_payload = len(payload)

    while idx + 4 <= length_payload:
        tag = payload[idx:idx+2]
        try:
            length = int(payload[idx+2:idx+4])
        except ValueError:
            break
        val_start = idx + 4
        val_end = val_start + length
        if val_end > length_payload:
            break
        val = payload[val_start:val_end]
        tags[tag] = val
        idx = val_end

    return tags


def build_lankaqr_string(
    amount: float,
    reference_no: str,
    merchant_name: str = "COMMERCIAL MERCH",
    merchant_city: str = "Colombo",
    merchant_account: str = "7001010101",
    is_dynamic: bool = True
) -> str:
    """Helper to synthesize a standard CBSL-compliant LankaQR EMVCo payload with valid CRC-16."""
    parts = []
    # Tag 00: Format indicator
    parts.append("000201")
    # Tag 01: Initiation method (12 = dynamic, 11 = static)
    parts.append(f"0102{'12' if is_dynamic else '11'}")
    # Tag 26: LankaPay Merchant Identifier
    acc_subtag = f"0008LANKAPAY01{len(merchant_account):02d}{merchant_account}"
    parts.append(f"26{len(acc_subtag):02d}{acc_subtag}")
    # Tag 52: MCC
    parts.append("52045411")
    # Tag 53: Currency (144 = LKR)
    parts.append("5303144")
    # Tag 54: Amount
    amt_str = f"{amount:.2f}"
    parts.append(f"54{len(amt_str):02d}{amt_str}")
    # Tag 58: Country
    parts.append("5802LK")
    # Tag 59: Merchant Name
    parts.append(f"59{len(merchant_name):02d}{merchant_name}")
    # Tag 60: Merchant City
    parts.append(f"60{len(merchant_city):02d}{merchant_city}")
    # Tag 62: Additional Data (Ref No)
    ref_sub = f"05{len(reference_no):02d}{reference_no}"
    parts.append(f"62{len(ref_sub):02d}{ref_sub}")
    # Tag 63: CRC header
    raw_without_crc = "".join(parts) + "6304"
    crc = compute_crc16_ccitt(raw_without_crc)
    return raw_without_crc + crc


def parse_lankaqr(payload: str) -> Dict[str, Any]:
    """
    Parse and cryptographically validate an EMVCo / LankaQR payload string (#122).
    """
    if not payload or len(payload) < 20:
        return {"is_valid": False, "error": "Payload too short or empty"}

    # Validate CRC-16 if Tag 63 is present
    crc_valid = False
    reported_crc = None
    calculated_crc = None

    if "6304" in payload:
        crc_idx = payload.rfind("6304")
        if crc_idx + 8 <= len(payload):
            data_to_hash = payload[:crc_idx + 4]
            reported_crc = payload[crc_idx + 4:crc_idx + 8].upper()
            calculated_crc = compute_crc16_ccitt(data_to_hash)
            crc_valid = (reported_crc == calculated_crc)

    tags = parse_tlv_string(payload)
    if "00" not in tags or tags["00"] != "01":
        return {"is_valid": False, "error": "Invalid EMVCo format indicator"}

    # Extract parsed fields
    is_dynamic = tags.get("01") == "12"
    amount_str = tags.get("54")
    amount = float(amount_str) if amount_str else None
    currency_code = tags.get("53")
    currency = "LKR" if currency_code == "144" else currency_code
    country = tags.get("58", "LK")
    merchant_name = tags.get("59", "")
    merchant_city = tags.get("60", "")

    # Parse sub-tags of 62 (Additional Data)
    reference_no = None
    bill_number = None
    if "62" in tags:
        subtags = parse_tlv_string(tags["62"])
        reference_no = subtags.get("05")
        bill_number = subtags.get("01")

    return {
        "is_valid": True,
        "is_lankaqr": country == "LK" and currency == "LKR",
        "is_dynamic": is_dynamic,
        "crc_valid": crc_valid,
        "reported_crc": reported_crc,
        "calculated_crc": calculated_crc,
        "amount": amount,
        "currency": currency,
        "country": country,
        "merchant_name": merchant_name,
        "merchant_city": merchant_city,
        "reference_no": reference_no,
        "bill_number": bill_number,
        "raw_tags": tags
    }


def detect_and_decode_qr_from_image(cv2_bgr: np.ndarray) -> Optional[str]:
    """Scan and decode QR code from transaction slip image using OpenCV."""
    if cv2_bgr is None or cv2_bgr.size == 0:
        return None

    detector = cv2.QRCodeDetector()
    val, _, _ = detector.detectAndDecode(cv2_bgr)
    if val and len(val.strip()) > 0:
        return val.strip()
    return None


def cross_verify_lankaqr_with_receipt(
    qr_data: Dict[str, Any],
    receipt_amount: Optional[float],
    receipt_reference: Optional[str]
) -> Dict[str, Any]:
    """
    Cross-verify decoded LankaQR parameters against printed OCR receipt parameters.
    Catches fraud where printed receipt amount or reference is altered while QR payload remains unchanged.
    """
    if not qr_data.get("is_valid", False):
        return {
            "cross_verified": False,
            "error": qr_data.get("error", "Invalid QR payload"),
            "discrepancies": ["QR payload invalid or unparseable"]
        }

    discrepancies = []

    # 1. CRC validation
    if not qr_data.get("crc_valid", False):
        discrepancies.append(
            f"Corrupt LankaQR CRC-16 checksum (reported {qr_data.get('reported_crc')} vs calculated {qr_data.get('calculated_crc')})."
        )

    # 2. Amount verification
    amount_matched = True
    qr_amount = qr_data.get("amount")
    if qr_amount is not None and receipt_amount is not None:
        if abs(qr_amount - receipt_amount) > 0.01:
            amount_matched = False
            discrepancies.append(
                f"Amount discrepancy: QR payload specifies LKR {qr_amount:,.2f} but receipt states LKR {receipt_amount:,.2f}."
            )

    # 3. Reference number verification
    ref_matched = True
    qr_ref = qr_data.get("reference_no")
    if qr_ref and receipt_reference:
        clean_qr_ref = qr_ref.replace(" ", "").upper()
        clean_rcpt_ref = receipt_reference.replace(" ", "").upper()
        if clean_qr_ref not in clean_rcpt_ref and clean_rcpt_ref not in clean_qr_ref:
            ref_matched = False
            discrepancies.append(
                f"Reference number mismatch: QR payload contains '{qr_ref}' while receipt states '{receipt_reference}'."
            )

    is_tampered = len(discrepancies) > 0

    return {
        "cross_verified": True,
        "is_tampered": is_tampered,
        "amount_matched": amount_matched,
        "reference_matched": ref_matched,
        "crc_valid": qr_data.get("crc_valid", False),
        "qr_amount": qr_amount,
        "receipt_amount": receipt_amount,
        "qr_reference": qr_ref,
        "receipt_reference": receipt_reference,
        "discrepancies": discrepancies
    }
