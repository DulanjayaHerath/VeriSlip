"""
E-Commerce & Merchant Integrations API Routes for VeriSlip.
Supports WooCommerce, Shopify, and Direct Bank Transfer (BACS) webhook verifications.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, Dict, Any
from PIL import Image
import io

from core.forensics.unified_scorer import VeriSlipForensicEngine
from core.templates.bank_rules import identify_bank_from_text
from core.forensics.layer1_structural import Layer1StructuralValidator

router = APIRouter(prefix="/api/v1/integrations", tags=["Merchant & E-Commerce Integrations"])

engine = VeriSlipForensicEngine()
field_validator = Layer1StructuralValidator()

@router.post("/woocommerce/verify")
async def verify_woocommerce_order(
    file: UploadFile = File(..., description="Uploaded payment slip (JPEG, PNG, WebP, or PDF)"),
    order_id: str = Form(..., description="WooCommerce Order ID (e.g. #10482)"),
    order_amount_lkr: float = Form(..., description="Expected order total in LKR (e.g. 15000.0)"),
    customer_email: Optional[str] = Form(None, description="Customer contact email"),
    target_bank: Optional[str] = Form(None, description="Merchant receiving bank code")
):
    """
    Automated BACS / Direct Bank Transfer verification webhook for WooCommerce stores.
    Evaluates customer-uploaded transfer slip, matches order amount against expected checkout total,
    and returns automated order transition action (PROCESSING, ON_HOLD, or CANCELLED).
    """
    is_pdf = file.content_type == "application/pdf" or (file.filename and file.filename.lower().endswith(".pdf"))
    if not (file.content_type.startswith("image/") or is_pdf):
        raise HTTPException(status_code=400, detail="Slip must be an image or PDF file.")

    try:
        contents = await file.read()
        if is_pdf:
            import pypdfium2 as pdfium
            pdf = pdfium.PdfDocument(contents)
            page = pdf[0]
            pil_img = page.render(scale=2.0).to_pil().convert("RGB")
            try:
                pil_img.info["pdf_metadata"] = pdf.get_metadata_dict()
            except Exception:
                pass
            page.close()
            pdf.close()
        else:
            raw_img = Image.open(io.BytesIO(contents))
            info_dict = raw_img.info.copy() if hasattr(raw_img, "info") else {}
            pil_img = raw_img.convert("RGB") if raw_img.mode != "RGB" else raw_img
            pil_img.info = info_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to decode payment slip: {str(e)}")

    # 1. Run full multi-layer forensic analysis
    forensic_results = engine.analyze(
        pil_image=pil_img,
        bank_code=target_bank,
        include_heatmaps=False
    )

    verdict = forensic_results["verdict"]
    risk_pct = forensic_results["tamper_risk_percentage"]

    # 2. Decision Logic for E-Commerce Order Status
    # - Low risk (<= 24.1%): Safe to auto-process order
    # - Suspicious (24.2% - 54.1%): Hold for manual merchant review
    # - High Risk (> 54.1%): Flag fraud, hold dispatch
    if verdict == "AUTHENTIC":
        order_action = "UPDATE_TO_PROCESSING"
        status_note = f"[VeriSlip] Transfer slip verified AUTHENTIC ({risk_pct:.1f}% risk). Order marked for fulfillment."
    elif verdict == "SUSPICIOUS":
        order_action = "HOLD_FOR_MANUAL_REVIEW"
        status_note = f"[VeriSlip] Suspicious anomalies detected ({risk_pct:.1f}% risk). Check bank balance before shipping."
    else:
        order_action = "FLAG_FRAUD_HOLD"
        status_note = f"[VeriSlip] WARNING: High probability of slip forgery ({risk_pct:.1f}% risk). Do NOT dispatch goods."

    return {
        "order_id": order_id,
        "expected_amount_lkr": order_amount_lkr,
        "recommended_order_action": order_action,
        "new_order_status": "processing" if order_action == "UPDATE_TO_PROCESSING" else "on-hold",
        "forensic_verdict": verdict,
        "tamper_risk_percentage": risk_pct,
        "merchant_note": status_note,
        "flagged_regions_count": len(forensic_results.get("flagged_regions", [])),
        "primary_signal": forensic_results["findings_summary"][0] if forensic_results["findings_summary"] else "Clean verification",
        "webhook_response": {
            "status": "success",
            "order_id": order_id,
            "set_paid": order_action == "UPDATE_TO_PROCESSING"
        }
    }


from core.notifications.webhook_dispatcher import WebhookDispatcher
from pydantic import BaseModel, Field

dispatcher = WebhookDispatcher()


class WebhookDispatchRequest(BaseModel):
    target_url: str = Field(..., description="Merchant webhook endpoint URL")
    event: str = Field("order.verified", description="Event type, e.g. order.verified, order.fraud_alert")
    payload_data: Dict[str, Any] = Field(default_factory=dict, description="Custom event metadata payload")


@router.post("/webhooks/dispatch")
async def dispatch_merchant_webhook(req: WebhookDispatchRequest):
    """
    Test or trigger an HMAC-SHA256 signed webhook notification to a merchant URL.
    """
    res = await dispatcher.dispatch(
        target_url=req.target_url,
        event_type=req.event,
        data=req.payload_data
    )
    return res

