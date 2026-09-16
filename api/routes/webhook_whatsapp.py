"""
WhatsApp Business Bot Webhook Route for VeriSlip.
Simulates and handles incoming WhatsApp media messages from social media sellers,
delivering instantaneous fraud risk verdicts and highlighted tamper warnings.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import base64
import io
from PIL import Image

from core.forensics.unified_scorer import VeriSlipForensicEngine

router = APIRouter(prefix="/api/v1/webhook", tags=["WhatsApp Bot"])
engine = VeriSlipForensicEngine()

class WhatsAppMessagePayload(BaseModel):
    from_phone: str = Field(..., description="Seller phone number, e.g. +94771234567")
    image_base64: str = Field(..., description="Base64 encoded image forwarded by seller")
    caption: Optional[str] = Field(None, description="Optional caption from buyer/seller")

class WhatsAppResponsePayload(BaseModel):
    recipient: str
    reply_text: str
    verdict: str
    tamper_risk_percentage: float
    flagged_box_count: int

@router.post("/whatsapp", response_model=WhatsAppResponsePayload)
def handle_whatsapp_slip(payload: WhatsAppMessagePayload):
    """
    Handle WhatsApp slip submission from a merchant.
    Returns simulated WhatsApp text response that would be sent back to the seller.
    """
    try:
        # Strip header if present
        raw_b64 = payload.image_base64
        if "," in raw_b64:
            raw_b64 = raw_b64.split(",")[1]

        img_bytes = base64.b64decode(raw_b64)
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image base64: {str(e)}")

    res = engine.analyze(pil_img)
    verdict = res["verdict"]
    risk = res["tamper_risk_percentage"]
    flagged_count = len(res["flagged_regions"])

    if verdict == "AUTHENTIC":
        reply = (
            f"✅ *VeriSlip Fraud Check: SAFE*\n\n"
            f"📊 Tamper Risk: *{risk}%* (Low)\n"
            f"🛡️ Verdict: Payment slip matches genuine bank formatting.\n"
            f"📦 *Recommendation:* Safe to dispatch order.\n\n"
            f"_Powered by VeriSlip Forensic AI_"
        )
    elif verdict == "SUSPICIOUS":
        reply = (
            f"⚠️ *VeriSlip Fraud Check: CAUTION REQUIRED*\n\n"
            f"📊 Tamper Risk: *{risk}%* (Moderate)\n"
            f"🔍 *Anomalies Detected:*\n"
            + "\n".join([f"• {f}" for f in res["findings_summary"][:2]])
            + f"\n\n🛑 *Recommendation:* Do not ship yet. Verify deposit in your bank app first!\n\n"
            f"_Powered by VeriSlip Forensic AI_"
        )
    else:
        reply = (
            f"🚨 *VeriSlip Alert: HIGH FRAUD RISK DETECTED!*\n\n"
            f"📊 Tamper Risk: *{risk}%* (Critical)\n"
            f"❌ *Tampering Detected:*\n"
            + "\n".join([f"• {f}" for f in res["findings_summary"][:3]])
            + f"\n\n⚠️ *{flagged_count} area(s)* exhibit digital compression/splicing forgery!\n"
            f"🚫 *DO NOT DISPATCH GOODS ON THIS SLIP.*\n\n"
            f"_Powered by VeriSlip Forensic AI_"
        )

    return {
        "recipient": payload.from_phone,
        "reply_text": reply,
        "verdict": verdict,
        "tamper_risk_percentage": risk,
        "flagged_box_count": flagged_count
    }
