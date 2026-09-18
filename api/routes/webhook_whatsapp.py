"""
WhatsApp Business Bot Webhook Route for VeriSlip.
Simulates and handles incoming WhatsApp media messages from social media sellers,
delivering instantaneous fraud risk verdicts and highlighted tamper warnings.
"""

import base64
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from core.forensics.unified_scorer import VeriSlipForensicEngine
from core.integrations.whatsapp_conversation import (
    ConversationState,
    QuotaSnapshot,
    conversation_store,
    duplicate_verification_message,
    quota_exhausted_message,
    quota_reached_message,
)
from core.integrations.merchant_credits import (
    ReservationStatus,
    merchant_credit_service,
)
from core.integrations.whatsapp_media import (
    WhatsAppMediaError,
    download_whatsapp_image,
)
from core.notifications.sms_fallback import sms_fallback_notifier
from core.security.image_sanitizer import (
    ImageValidationError,
    MAX_IMAGE_UPLOAD_BYTES,
    sanitize_image_bytes,
)

router = APIRouter(prefix="/api/v1/webhook", tags=["WhatsApp Bot"])
engine = VeriSlipForensicEngine()


class WhatsAppMessagePayload(BaseModel):
    from_phone: str = Field(
        ..., min_length=3, max_length=32, description="Seller phone number"
    )
    image_base64: Optional[str] = Field(
        None, description="Base64 encoded image forwarded by seller"
    )
    media_id: Optional[str] = Field(None, description="WhatsApp Cloud API media ID")
    text: Optional[str] = Field(
        None, max_length=2_000, description="Seller command or conversation message"
    )
    message_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=128,
        description="Stable WhatsApp message ID used for idempotency",
    )
    caption: Optional[str] = Field(None, description="Optional caption from buyer/seller")
    whatsapp_delivery_failed: bool = Field(
        False,
        description="True only after the normal WhatsApp fraud alert could not be delivered",
    )


class WhatsAppResponsePayload(BaseModel):
    recipient: str
    reply_text: str
    verdict: Optional[str] = None
    tamper_risk_percentage: Optional[float] = None
    flagged_box_count: Optional[int] = None
    conversation_state: ConversationState = ConversationState.READY
    language: str = "en"
    duplicate: bool = False
    merchant_tier: Optional[str] = None
    credits_remaining: Optional[int] = None
    credit_limit: Optional[int] = None
    sms_fallback_status: Optional[str] = None


@router.post("/whatsapp", response_model=WhatsAppResponsePayload)
async def handle_whatsapp_slip(payload: WhatsAppMessagePayload):
    """
    Handle seller commands or securely verify one WhatsApp receipt image.

    Exactly one of ``text``, ``image_base64``, or ``media_id`` is accepted.
    Conversation state stores only pseudonymous hashes, while receipt images
    continue through the bounded downloader and image sanitizer.
    """
    source_count = sum(
        value is not None
        for value in (payload.text, payload.image_base64, payload.media_id)
    )
    if source_count != 1 or (payload.text is not None and not payload.text.strip()):
        raise HTTPException(
            status_code=400,
            detail="Provide exactly one non-empty text, image_base64, or media_id value.",
        )

    if payload.text is not None:
        merchant_balance = merchant_credit_service.balance(payload.from_phone)
        quota = QuotaSnapshot(
            tier=merchant_balance.tier,
            limit=merchant_balance.limit,
            remaining=merchant_balance.remaining,
            used=merchant_balance.used,
        )
        reply = conversation_store.process(
            payload.from_phone,
            payload.text,
            quota,
            message_id=payload.message_id,
        )
        return {
            "recipient": payload.from_phone,
            "reply_text": reply.text,
            "conversation_state": reply.state,
            "language": reply.language.value,
            "duplicate": reply.duplicate,
            "merchant_tier": merchant_balance.tier,
            "credits_remaining": merchant_balance.remaining,
            "credit_limit": merchant_balance.limit,
        }

    language = conversation_store.seller_language(payload.from_phone)
    reservation = merchant_credit_service.reserve(
        payload.from_phone, payload.message_id
    )
    if reservation.status is ReservationStatus.DUPLICATE:
        return {
            "recipient": payload.from_phone,
            "reply_text": duplicate_verification_message(language),
            "conversation_state": ConversationState.READY,
            "language": language.value,
            "duplicate": True,
            "merchant_tier": reservation.balance.tier,
            "credits_remaining": reservation.balance.remaining,
            "credit_limit": reservation.balance.limit,
        }
    if reservation.status is ReservationStatus.EXHAUSTED:
        return {
            "recipient": payload.from_phone,
            "reply_text": quota_exhausted_message(
                language, merchant_credit_service.policy.upgrade_url
            ),
            "conversation_state": ConversationState.READY,
            "language": language.value,
            "merchant_tier": reservation.balance.tier,
            "credits_remaining": 0,
            "credit_limit": reservation.balance.limit,
        }
    assert reservation.token is not None
    credit_token: Optional[str] = reservation.token

    try:
        if payload.media_id:
            pil_img = await download_whatsapp_image(payload.media_id)
        else:
            assert payload.image_base64 is not None
            # Strip a data-URI header if present.
            raw_b64 = payload.image_base64
            if "," in raw_b64:
                raw_b64 = raw_b64.split(",", 1)[1]

            if len(raw_b64) > ((MAX_IMAGE_UPLOAD_BYTES + 2) // 3) * 4:
                raise ImageValidationError(
                    "Image upload exceeds the permitted size.", status_code=413
                )
            try:
                img_bytes = base64.b64decode(raw_b64, validate=True)
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=400, detail="Image payload is not valid base64."
                ) from None
            pil_img = await run_in_threadpool(sanitize_image_bytes, img_bytes)
        res = await run_in_threadpool(engine.analyze, pil_img)
        merchant_balance = merchant_credit_service.complete(credit_token)
        credit_token = None
    except WhatsAppMediaError as exc:
        if credit_token is not None:
            merchant_credit_service.release(credit_token)
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from None
    except ImageValidationError as exc:
        if credit_token is not None:
            merchant_credit_service.release(credit_token)
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from None
    except HTTPException:
        if credit_token is not None:
            merchant_credit_service.release(credit_token)
        raise
    except BaseException:
        if credit_token is not None:
            merchant_credit_service.release(credit_token)
        raise
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

    if merchant_balance.remaining == 0:
        reply = (
            f"{reply}\n\n"
            f"{quota_reached_message(language, merchant_credit_service.policy.upgrade_url)}"
        )

    sms_result = await sms_fallback_notifier.notify(
        recipient=payload.from_phone,
        verdict=verdict,
        whatsapp_delivery_failed=payload.whatsapp_delivery_failed,
        event_id=payload.message_id,
    )

    return {
        "recipient": payload.from_phone,
        "reply_text": reply,
        "verdict": verdict,
        "tamper_risk_percentage": risk,
        "flagged_box_count": flagged_count,
        "conversation_state": ConversationState.READY,
        "language": language.value,
        "duplicate": False,
        "merchant_tier": merchant_balance.tier,
        "credits_remaining": merchant_balance.remaining,
        "credit_limit": merchant_balance.limit,
        "sms_fallback_status": sms_result.status.value,
    }
