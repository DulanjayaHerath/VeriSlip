"""
Courier Rider Fast-Triage Endpoint (VeriSlip Layer 5 Integration)
Optimized for mobile courier delivery apps (PromptX, Koombiyo, Domex, PickMe Flash)
Provides instant binary decision: can_handover_package (True/False)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import io
import base64
import time
from PIL import Image

from core.forensics.unified_scorer import VeriSlipForensicEngine

router = APIRouter(prefix="/courier", tags=["Courier Rider Mobile API"])
engine = VeriSlipForensicEngine()


class CourierVerifyRequest(BaseModel):
    waybill_id: str = Field(..., description="Courier delivery tracking / waybill number (e.g. WB-894102)")
    expected_cod_amount: float = Field(..., description="Expected Cash-On-Delivery total in LKR")
    slip_base64: str = Field(..., description="Base64 encoded photo taken by delivery rider")
    target_bank: Optional[str] = Field("COMBANK", description="Bank code")


class CourierVerifyResponse(BaseModel):
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


@router.post("/verify", response_model=CourierVerifyResponse)
async def verify_courier_delivery(payload: CourierVerifyRequest):
    """
    Ultra-fast mobile triage endpoint for courier delivery agents.
    Evaluates slip authenticity and ensures transferred amount matches expected COD value.
    """
    try:
        # Decode image
        raw_b64 = payload.slip_base64
        if "," in raw_b64:
            raw_b64 = raw_b64.split(",", 1)[1]
        img_bytes = base64.b64decode(raw_b64)
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

    # Run forensic pipeline
    result = engine.analyze(pil_image=image, bank_code=payload.target_bank, include_heatmaps=False)
    risk_pct = result["tamper_risk_percentage"]
    verdict = result["verdict"]

    # Check extracted financial amount
    detected_amt = None
    amount_mismatch = False
    metadata = result.get("extracted_metadata") or {}
    if metadata.get("amount") is not None:
        try:
            detected_amt = float(metadata["amount"])
            if abs(detected_amt - payload.expected_cod_amount) > 1.0:
                amount_mismatch = True
        except (ValueError, TypeError):
            pass

    # Rider decision logic
    if risk_pct > 45.0 or amount_mismatch:
        can_handover = False
        if amount_mismatch:
            action = "DO_NOT_HANDOVER_AMOUNT_MISMATCH"
            alert = f"Slip shows LKR {detected_amt:,.2f} but package COD is LKR {payload.expected_cod_amount:,.2f}."
        else:
            action = "DO_NOT_HANDOVER_SUSPECTED_FORGERY"
            alert = f"High forgery risk ({risk_pct:.1f}%). Tampered slip detected."
    else:
        can_handover = True
        action = "HANDOVER_PACKAGE_CONFIRMED"
        alert = None

    risk_level = "SAFE" if risk_pct < 25.0 else "SUSPICIOUS" if risk_pct <= 45.0 else "FRAUDULENT"

    return CourierVerifyResponse(
        waybill_id=payload.waybill_id,
        can_handover_package=can_handover,
        rider_action=action,
        cashier_alert=alert,
        risk_level=risk_level,
        risk_percentage=risk_pct,
        expected_amount=payload.expected_cod_amount,
        detected_amount=detected_amt,
        amount_mismatch=amount_mismatch,
        timestamp=result.get("timestamp", str(time.time()))
    )
