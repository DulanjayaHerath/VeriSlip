"""Conservative handling of amounts supplied by receipt extraction."""

import math
from typing import Optional


def detected_payment_amount(result) -> Optional[float]:
    """Missing, malformed and non-finite OCR values must never confirm payment."""
    value = (result.get("extracted_metadata") or {}).get("amount")
    if value is None or isinstance(value, bool):
        return None
    try:
        amount = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return amount if math.isfinite(amount) and amount > 0 else None
