"""
E-Commerce & Merchant Integrations API Routes for VeriSlip.
Supports WooCommerce, Shopify, and Direct Bank Transfer (BACS) webhook verifications.
"""

from decimal import Decimal
from typing import Any, Dict, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from api.routes.verify import _analyze_image, _decode_document, _read_bounded_upload
from core.notifications.webhook_dispatcher import WebhookDispatcher
from core.security.image_sanitizer import ImageValidationError
from core.security.payment_amounts import detected_payment_amount

router = APIRouter(
    prefix="/api/v1/integrations", tags=["Merchant & E-Commerce Integrations"]
)


@router.post("/woocommerce/verify")
async def verify_woocommerce_order(
    file: UploadFile = File(
        ..., description="Uploaded payment slip (JPEG, PNG, or PDF)"
    ),
    order_id: str = Form(..., description="WooCommerce Order ID (e.g. #10482)"),
    order_amount_lkr: float = Form(
        ...,
        gt=0,
        le=1_000_000_000,
        allow_inf_nan=False,
        description="Expected order total in LKR (e.g. 15000.0)",
    ),
    customer_email: Optional[str] = Form(None, description="Customer contact email"),
    target_bank: Optional[str] = Form(None, description="Merchant receiving bank code"),
):
    """
    Automated BACS / Direct Bank Transfer verification webhook for WooCommerce stores.
    Evaluates customer-uploaded transfer slip, matches order amount against expected checkout total,
    and returns automated order transition action (PROCESSING, ON_HOLD, or CANCELLED).
    """
    try:
        contents = await _read_bounded_upload(file)
        pil_img = await run_in_threadpool(_decode_document, contents)
    except ImageValidationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from None
    except Exception:
        raise HTTPException(
            status_code=400, detail="Uploaded document could not be decoded safely."
        ) from None

    try:
        forensic_results = await run_in_threadpool(
            _analyze_image, pil_img, target_bank, None, False
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Forensic analysis could not be completed."
        ) from None
    finally:
        pil_img.close()

    verdict = forensic_results["verdict"]
    risk_pct = forensic_results["tamper_risk_percentage"]

    detected_amount = detected_payment_amount(forensic_results)
    amount_mismatch = detected_amount is not None and (
        Decimal(str(detected_amount)) != Decimal(str(order_amount_lkr))
    )

    if verdict == "AUTHENTIC" and detected_amount is not None and not amount_mismatch:
        order_action = "UPDATE_TO_PROCESSING"
        status_note = (
            f"[VeriSlip] Low-risk slip ({risk_pct:.1f}% risk) matches the order amount."
        )
    elif verdict not in {"AUTHENTIC", "SUSPICIOUS"}:
        order_action = "FLAG_FRAUD_HOLD"
        status_note = (
            "[VeriSlip] Forensic verification did not pass. Do NOT dispatch goods."
        )
    elif detected_amount is None:
        order_action = "HOLD_FOR_MANUAL_REVIEW"
        status_note = "[VeriSlip] Slip amount could not be verified. Confirm payment with the bank before shipping."
    elif amount_mismatch:
        order_action = "HOLD_FOR_MANUAL_REVIEW"
        status_note = f"[VeriSlip] Slip amount LKR {detected_amount:,.2f} does not match order total LKR {order_amount_lkr:,.2f}."
    else:
        order_action = "HOLD_FOR_MANUAL_REVIEW"
        status_note = f"[VeriSlip] Suspicious anomalies detected ({risk_pct:.1f}% risk). Check bank balance before shipping."

    return {
        "order_id": order_id,
        "expected_amount_lkr": order_amount_lkr,
        "detected_amount_lkr": detected_amount,
        "amount_mismatch": amount_mismatch,
        "recommended_order_action": order_action,
        "new_order_status": (
            "processing" if order_action == "UPDATE_TO_PROCESSING" else "on-hold"
        ),
        "forensic_verdict": verdict,
        "tamper_risk_percentage": risk_pct,
        "merchant_note": status_note,
        "flagged_regions_count": len(forensic_results.get("flagged_regions", [])),
        "primary_signal": (
            forensic_results["findings_summary"][0]
            if forensic_results["findings_summary"]
            else "Clean verification"
        ),
        "webhook_response": {
            "status": "success",
            "order_id": order_id,
            "set_paid": order_action == "UPDATE_TO_PROCESSING",
        },
    }


dispatcher = WebhookDispatcher()


class WebhookDispatchRequest(BaseModel):
    target_url: str = Field(..., description="Merchant webhook endpoint URL")
    event: str = Field(
        "order.verified",
        description="Event type, e.g. order.verified, order.fraud_alert",
    )
    payload_data: Dict[str, Any] = Field(
        default_factory=dict, description="Custom event metadata payload"
    )


@router.post("/webhooks/dispatch")
async def dispatch_merchant_webhook(req: WebhookDispatchRequest):
    """
    Test or trigger an HMAC-SHA256 signed webhook notification to a merchant URL.
    """
    res = await dispatcher.dispatch(
        target_url=req.target_url, event_type=req.event, data=req.payload_data
    )
    return res
