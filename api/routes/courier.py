"""Secure, mobile-oriented courier rider verification endpoint."""

from __future__ import annotations

import base64
import binascii
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from api.routes.verify import ForensicAnalysisError, _analyze_image
from core.security.image_sanitizer import (
    ImageValidationError,
    MAX_IMAGE_UPLOAD_BYTES,
    sanitize_image_bytes,
)


router = APIRouter(prefix="/courier", tags=["Courier Rider Mobile API"])
MAX_ENCODED_IMAGE_CHARS = ((MAX_IMAGE_UPLOAD_BYTES + 2) // 3) * 4


class CourierVerifyRequest(BaseModel):
    """Existing JSON contract used by mobile courier applications."""

    waybill_id: str = Field(
        ..., min_length=1, max_length=128,
        description="Courier delivery tracking / waybill number.",
    )
    expected_cod_amount: float = Field(
        ..., gt=0, le=1_000_000_000,
        description="Expected cash-on-delivery total in LKR.",
    )
    slip_base64: str = Field(
        ..., min_length=1,
        description="Base64-encoded JPEG or PNG captured by the rider.",
    )
    target_bank: Optional[str] = Field(
        "COMBANK", max_length=40, description="Optional supported bank code."
    )


class CourierVerifyResponse(BaseModel):
    """Compact response optimized for an immediate rider handover decision."""

    waybill_id: str
    can_handover_package: bool
    rider_action: str
    cashier_alert: Optional[str] = None
    risk_level: str
    risk_percentage: float
    expected_amount: float
    detected_amount: Optional[float]
    amount_mismatch: bool
    timestamp: str


def _decode_base64_image(encoded: str):
    """Decode and sanitize an untrusted in-memory rider upload."""
    raw = encoded.strip()
    if raw.startswith("data:"):
        prefix, separator, raw = raw.partition(",")
        if (
            not separator
            or not prefix.lower().startswith("data:image/")
            or not prefix.lower().endswith(";base64")
        ):
            raise ImageValidationError("Image payload is not valid base64.")
    if len(raw) > MAX_ENCODED_IMAGE_CHARS:
        raise ImageValidationError(
            "Image upload exceeds the permitted size.", status_code=413
        )
    try:
        image_bytes = base64.b64decode(raw, validate=True)
    except (binascii.Error, ValueError):
        raise ImageValidationError("Image payload is not valid base64.") from None
    return sanitize_image_bytes(image_bytes)


def _detected_amount(result) -> Optional[float]:
    """Return a numeric OCR amount only when the shared extractor supplies one."""
    value = (result.get("extracted_metadata") or {}).get("amount")
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@router.post("/verify", response_model=CourierVerifyResponse)
async def verify_courier_delivery(payload: CourierVerifyRequest):
    """Return a fast binary package-handover decision for a sanitized slip.

    Authentication, tiered rate limiting, request correlation, and structured
    lifecycle logging are applied by the existing ``/api/v1`` middleware.
    """
    try:
        image = await run_in_threadpool(_decode_base64_image, payload.slip_base64)
    except ImageValidationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from None

    try:
        result = await run_in_threadpool(
            _analyze_image, image, payload.target_bank, None, False
        )
    except ForensicAnalysisError:
        raise HTTPException(
            status_code=500, detail="Forensic analysis could not be completed."
        ) from None
    except Exception:
        raise HTTPException(
            status_code=500, detail="Forensic analysis could not be completed."
        ) from None

    risk_pct = float(result["tamper_risk_percentage"])
    verdict = str(result["verdict"])
    detected_amount = _detected_amount(result)
    amount_mismatch = bool(
        detected_amount is not None
        and abs(detected_amount - payload.expected_cod_amount) > 1.0
    )
    unsafe_verdict = verdict in {"SUSPICIOUS", "HIGH_RISK_TAMPERED"}

    if amount_mismatch:
        can_handover = False
        action = "DO_NOT_HANDOVER_AMOUNT_MISMATCH"
        alert = (
            f"Slip shows LKR {detected_amount:,.2f} but package COD is "
            f"LKR {payload.expected_cod_amount:,.2f}."
        )
    elif unsafe_verdict or risk_pct > 45.0:
        can_handover = False
        action = "DO_NOT_HANDOVER_SUSPECTED_FORGERY"
        alert = f"High forgery risk ({risk_pct:.1f}%). Verify with the cashier."
    else:
        can_handover = True
        action = "HANDOVER_PACKAGE_CONFIRMED"
        alert = None

    if verdict == "HIGH_RISK_TAMPERED" or risk_pct > 45.0:
        risk_level = "FRAUDULENT"
    elif verdict == "SUSPICIOUS" or risk_pct >= 25.0:
        risk_level = "SUSPICIOUS"
    else:
        risk_level = "SAFE"

    return CourierVerifyResponse(
        waybill_id=payload.waybill_id,
        can_handover_package=can_handover,
        rider_action=action,
        cashier_alert=alert,
        risk_level=risk_level,
        risk_percentage=risk_pct,
        expected_amount=payload.expected_cod_amount,
        detected_amount=detected_amount,
        amount_mismatch=amount_mismatch,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
