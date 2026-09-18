"""
Layer 1.5 Forensics: Semantic Financial, Arithmetic & Temporal Validator.
Validates cross-field mathematical consistency, temporal causality, currency syntax,
and bank template constraints from extracted OCR text and metadata.
"""

import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

class Layer1SemanticValidator:
    """Validates semantic correctness and financial logic of payment slips."""

    def __init__(self):
        # Patterns for currency matching
        self.amount_regex = re.compile(r"(?:LKR|Rs\.?|USD)?\s*([0-9]{1,3}(?:,[0-9]{2,4})*(?:\.[0-9]{2})?)", re.IGNORECASE)
        self.malformed_currency_regex = re.compile(r"\b\d{1,3},\d{4,}(?:\.\d+)?\b")

    def parse_amount(self, text: str) -> Optional[float]:
        """Safely parse currency amount string into float."""
        clean = re.sub(r"[^\d.]", "", text.replace(",", ""))
        try:
            return float(clean)
        except (ValueError, TypeError):
            return None

    def verify_currency_syntax(self, ocr_tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect malformed currency formatting (e.g. 40,0000.00 or 2,2000.00).
        Standard formatting requires exactly 3 digits between thousands separators.
        """
        issues = []
        for item in ocr_tokens:
            text = item.get("text", "")
            matches = self.malformed_currency_regex.findall(text)
            for m in matches:
                # Discard pure numbers that are part of telephone or long reference IDs
                clean_num = m.replace(",", "").replace(".", "")
                # If it looks like a currency amount (has comma and decimal, or preceded by currency symbol)
                is_likely_currency = (
                    ("." in m and len(m.split(".")[-1]) == 2) or
                    any(sym in text for sym in ["LKR", "Rs", "Amount", "debit", "Fee"]) or
                    len(clean_num) <= 10
                )
                if is_likely_currency:
                    box = [item.get("x", 0), item.get("y", 0), item.get("w", 0), item.get("h", 0)]
                    issues.append({
                        "type": "MALFORMED_CURRENCY_GROUPING",
                        "token": m,
                        "box": [round(v) for v in box],
                        "confidence": 0.94,
                        "description": f"Malformed currency grouping '{m}': contains invalid digit grouping instead of standard 3 digits."
                    })
        return issues

    def verify_arithmetic(self, ocr_tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Verify mathematical consistency between Amount, Fees, and Total Debit.
        If Amount + Fee != Total Debit, flags severe tampering.
        """
        amount = None
        amount_box = None
        fee = 0.0
        fee_box = None
        has_fee_stated = False
        total_debit = None
        total_debit_box = None

        # Scan tokens for amount-related fields
        for i, item in enumerate(ocr_tokens):
            t = item.get("text", "").lower()
            
            # Amount field
            if ("amount" in t and "fee" not in t and "total" not in t and "charge" not in t) or "transaction amount" in t:
                # Look in same token or adjacent tokens for the value
                val, box = self._find_value_near(ocr_tokens, i)
                if val is not None and amount is None:
                    amount = val
                    amount_box = box

            # Fee / Charge field
            elif "fee" in t or "charge" in t:
                val, box = self._find_value_near(ocr_tokens, i)
                if val is not None and not has_fee_stated:
                    fee = val
                    fee_box = box
                    has_fee_stated = True

            # Total Debit / Total Amount field
            elif "total debit" in t or "total amount" in t or "net amount" in t:
                val, box = self._find_value_near(ocr_tokens, i)
                if val is not None and total_debit is None:
                    total_debit = val
                    total_debit_box = box

        issues = []
        if amount is not None and total_debit is not None:
            expected_total = round(amount + fee, 2)
            actual_total = round(total_debit, 2)
            diff = round(abs(actual_total - expected_total), 2)

            if diff > 0.05:
                # Definite arithmetic mismatch
                boxes_to_flag = []
                if amount_box:
                    boxes_to_flag.append({"box": amount_box, "confidence": 0.98, "label": "Manipulated Amount"})
                if total_debit_box:
                    boxes_to_flag.append({"box": total_debit_box, "confidence": 0.98, "label": "Arithmetic Contradiction"})

                issues.append({
                    "type": "ARITHMETIC_INCONSISTENCY",
                    "amount": amount,
                    "fee": fee,
                    "total_debit": total_debit,
                    "expected_total": expected_total,
                    "difference": diff,
                    "boxes": boxes_to_flag,
                    "confidence": 0.98,
                    "description": (
                        f"Financial Arithmetic Inconsistency: Stated Amount (LKR {amount:,.2f}) + "
                        f"Fee (LKR {fee:,.2f}) != Total Debit (LKR {total_debit:,.2f}). "
                        f"Discrepancy of LKR {diff:,.2f} indicates selective number tampering."
                    )
                })

        return issues

    def verify_temporal_causality(self, ocr_tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Verify temporal causality between Transaction Time and Print/Generated Time.
        A receipt cannot be generated before the transaction takes place.
        """
        txn_dt = None
        txn_box = None
        gen_dt = None
        gen_box = None

        dt_patterns = [
            r"(\d{2}[/-]\d{2}[/-]\d{4}\s+\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)",
            r"(\d{4}[/-]\d{2}[/-]\d{2}\s+\d{1,2}:\d{2}(?::\d{2})?)",
        ]

        for i, item in enumerate(ocr_tokens):
            text = item.get("text", "")
            lower = text.lower()

            # Transaction Date & Time
            if "date & time" in lower or "transaction date" in lower or "transfer date" in lower:
                dt_obj, box = self._find_datetime_near(ocr_tokens, i)
                if dt_obj and txn_dt is None:
                    txn_dt = dt_obj
                    txn_box = box

            # Generated / Printed Time
            elif "generated:" in lower or "printed on:" in lower or "printed at:" in lower or "printed:" in lower:
                dt_obj, box = self._find_datetime_near(ocr_tokens, i)
                if dt_obj and gen_dt is None:
                    gen_dt = dt_obj
                    gen_box = box

        issues = []
        if txn_dt and gen_dt:
            # If generated/printed is significantly before transaction time (more than 30s)
            delta_sec = (txn_dt - gen_dt).total_seconds()
            if delta_sec > 30:
                boxes = []
                if txn_box:
                    boxes.append({"box": txn_box, "confidence": 0.95, "label": "Time Paradox (Transaction)"})
                if gen_box:
                    boxes.append({"box": gen_box, "confidence": 0.95, "label": "Time Paradox (Generated)"})

                issues.append({
                    "type": "TEMPORAL_CAUSALITY_VIOLATION",
                    "transaction_dt": txn_dt.isoformat(),
                    "generated_dt": gen_dt.isoformat(),
                    "delta_seconds": delta_sec,
                    "boxes": boxes,
                    "confidence": 0.95,
                    "description": (
                        f"Temporal Causality Paradox: Receipt was generated at {gen_dt.strftime('%H:%M:%S')}, "
                        f"which precedes the stated transaction timestamp {txn_dt.strftime('%H:%M:%S')} "
                        f"by {int(delta_sec)} seconds. Impossible in authentic bank processing."
                    )
                })

        return issues

    def verify_mandatory_fields(self, bank_code: str, ocr_tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Verify that required fields are present and not stripped / blank.
        For example: Sampath Vishwa requires 'Source Account :' to contain an account identifier.
        """
        issues = []
        all_text = " \n ".join([t.get("text", "") for t in ocr_tokens])

        # Check Sampath Vishwa Source Account emptiness
        if "sampath" in all_text.lower() or bank_code == "SAMPATH":
            for i, item in enumerate(ocr_tokens):
                t = item.get("text", "").strip()
                if re.match(r"^Source\s*Account\s*:\s*$", t, re.IGNORECASE):
                    # Check if next token is on the same line or within reasonable distance
                    y = item.get("y", 0)
                    h = item.get("h", 0)
                    has_val = False
                    for other in ocr_tokens:
                        if other != item and abs(other.get("y", 0) - y) < h * 0.8 and other.get("x", 0) > item.get("x", 0):
                            val_txt = other.get("text", "").strip()
                            if len(val_txt) > 2:
                                has_val = True
                                break
                    if not has_val:
                        box = [item.get("x", 0), item.get("y", 0), item.get("w", 0) + 150, item.get("h", 0)]
                        issues.append({
                            "type": "MISSING_MANDATORY_FIELD",
                            "field": "Source Account",
                            "box": [round(v) for v in box],
                            "confidence": 0.75,
                            "description": "Mandatory 'Source Account' field is empty / erased on Sampath Vishwa receipt."
                        })

        return issues

    def evaluate(self, ocr_tokens: List[Dict[str, Any]], bank_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Run full semantic financial audit across OCR tokens.
        """
        syntax_issues = self.verify_currency_syntax(ocr_tokens)
        arith_issues = self.verify_arithmetic(ocr_tokens)
        time_issues = self.verify_temporal_causality(ocr_tokens)
        field_issues = self.verify_mandatory_fields(bank_code or "GENERIC_CEFTS", ocr_tokens)

        all_issues = syntax_issues + arith_issues + time_issues + field_issues
        
        # Calculate anomaly score (decisive: max confidence of severe violations)
        anomaly_score = 0.0
        findings = []
        candidate_boxes = []

        for issue in all_issues:
            conf = issue.get("confidence", 0.5)
            anomaly_score = max(anomaly_score, conf)
            findings.append(issue.get("description", ""))

            if "boxes" in issue:
                for b in issue["boxes"]:
                    candidate_boxes.append(b)
            elif "box" in issue:
                candidate_boxes.append({
                    "box": issue["box"],
                    "confidence": conf,
                    "label": issue.get("type", "Semantic Anomaly").replace("_", " ").title()
                })

        return {
            "layer_name": "Layer 1.5: Semantic Financial & Temporal Validation",
            "anomaly_score": round(anomaly_score, 3),
            "is_anomalous": anomaly_score >= 0.70,
            "findings": findings,
            "detected_regions": candidate_boxes,
            "issues": all_issues
        }

    def _find_value_near(self, tokens: List[Dict[str, Any]], idx: int) -> Tuple[Optional[float], Optional[List[int]]]:
        """Look in current token or nearby right/down tokens for numeric amount."""
        curr_text = tokens[idx].get("text", "")
        m = re.search(r"(\d{1,3}(?:,\d{2,4})*(?:\.\d{2}))", curr_text)
        if m:
            val = self.parse_amount(m.group(1))
            box = [tokens[idx].get("x", 0), tokens[idx].get("y", 0), tokens[idx].get("w", 0), tokens[idx].get("h", 0)]
            return val, [round(v) for v in box]

        curr_y = tokens[idx].get("y", 0)
        curr_x = tokens[idx].get("x", 0)
        curr_h = tokens[idx].get("h", 0)

        # Look in other tokens within the same row or row below
        candidates = []
        for other in tokens:
            if other == tokens[idx]:
                continue
            oy = other.get("y", 0)
            ox = other.get("x", 0)
            # Same horizontal line (right side)
            if abs(oy - curr_y) < max(curr_h * 0.9, 15) and ox >= curr_x:
                m = re.search(r"(\d{1,3}(?:,\d{2,4})*(?:\.\d{2}))", other.get("text", ""))
                if m:
                    candidates.append((ox, self.parse_amount(m.group(1)), other))

        if candidates:
            candidates.sort(key=lambda c: c[0])
            winner = candidates[-1]  # rightmost amount on row
            box = [winner[2].get("x", 0), winner[2].get("y", 0), winner[2].get("w", 0), winner[2].get("h", 0)]
            return winner[1], [round(v) for v in box]

        return None, None

    def _find_datetime_near(self, tokens: List[Dict[str, Any]], idx: int) -> Tuple[Optional[datetime], Optional[List[int]]]:
        """Extract datetime object from current or nearby tokens."""
        formats = [
            "%d/%m/%Y %I:%M:%S %p",
            "%d/%m/%Y %I:%M %p",
            "%d-%m-%Y %I:%M:%S %p",
            "%d-%m-%Y %I:%M %p",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M",
        ]

        def try_parse(raw: str) -> Optional[datetime]:
            # Clean common prefixes/suffixes
            cleaned = re.sub(r"^(?:Generated|Printed on|Printed at|Printed|Date & Time|Transaction Date & Time|Date/Time)\s*[:.-]?\s*", "", raw, flags=re.I).strip()
            # Normalize OCR artifacts like 'PN' -> 'PM'
            cleaned = re.sub(r"\bPN\b", "PM", cleaned, flags=re.I)
            # Separate stuck year and time e.g. 202612:38 -> 2026 12:38
            cleaned = re.sub(r"(\d{4})(\d{1,2}:\d{2})", r"\1 \2", cleaned)
            # Normalize multiple spaces
            cleaned = re.sub(r"\s+", " ", cleaned)
            for fmt in formats:
                try:
                    return datetime.strptime(cleaned, fmt)
                except ValueError:
                    pass
            # Try searching with regex
            m = re.search(r"(\d{2}[/-]\d{2}[/-]\d{4}(?:\s+\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)?)", raw, re.I)
            if m:
                s = m.group(1).strip()
                for fmt in formats:
                    try:
                        return datetime.strptime(s, fmt)
                    except ValueError:
                        pass
            return None

        # 1. Check current token
        dt = try_parse(tokens[idx].get("text", ""))
        if dt:
            box = [tokens[idx].get("x", 0), tokens[idx].get("y", 0), tokens[idx].get("w", 0), tokens[idx].get("h", 0)]
            return dt, [round(v) for v in box]

        curr_y = tokens[idx].get("y", 0)
        curr_h = tokens[idx].get("h", 0)

        # 2. Check nearby tokens on same row or right side
        for other in tokens:
            if other == tokens[idx]:
                continue
            if abs(other.get("y", 0) - curr_y) < max(curr_h * 1.2, 18):
                dt = try_parse(other.get("text", ""))
                if dt:
                    box = [other.get("x", 0), other.get("y", 0), other.get("w", 0), other.get("h", 0)]
                    return dt, [round(v) for v in box]

        return None, None
