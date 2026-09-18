"""Signed Shopify order-creation webhook for manual payment screening."""

from __future__ import annotations

import hashlib
import json
import os
import re
from functools import partial
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Request

from api.routes.verify import _analyze_image
from core.integrations.shopify import ShopifyEventStore, ShopifyIntegrationError, download_shopify_image, verify_webhook_signature
from core.jobs.forensic_jobs import ForensicJobManager, JobQueueFullError
from core.observability.logging import get_correlation_id

router = APIRouter(prefix="/api/v1/integrations/shopify", tags=["Shopify"])
job_manager = ForensicJobManager()


def _bounded_env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except ValueError:
        return default
    return max(minimum, min(maximum, value))


event_store = ShopifyEventStore(
    ttl_seconds=_bounded_env_int(
        "VERISLIP_SHOPIFY_IDEMPOTENCY_TTL_SECONDS", 86_400, 60, 604_800
    ),
    max_records=_bounded_env_int(
        "VERISLIP_SHOPIFY_IDEMPOTENCY_MAX_RECORDS", 10_000, 100, 1_000_000
    ),
)
MAX_WEBHOOK_BYTES = 1_000_000
EVENT_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
PROOF_KEYS = frozenset({"payment_proof_url", "payment_receipt_url", "receipt_url", "slip_url", "bank_slip_url"})


def _is_manual_payment(order: Dict[str, Any]) -> bool:
    gateways = order.get("payment_gateway_names") or []
    if isinstance(gateways, str):
        gateways = [gateways]
    gateway = order.get("gateway")
    if isinstance(gateway, str):
        gateways = [*gateways, gateway]
    terms = ("manual", "bank transfer", "bank deposit", "wire transfer")
    return any(isinstance(value, str) and any(term in value.casefold() for term in terms) for value in gateways)


def _proof_url(order: Dict[str, Any]) -> Optional[str]:
    direct = order.get("payment_proof_url")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    for collection_name in ("note_attributes", "metafields"):
        collection = order.get(collection_name) or []
        if not isinstance(collection, list):
            continue
        for item in collection:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or item.get("key") or "").strip().casefold()
            value = item.get("value")
            if name in PROOF_KEYS and isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _process_forensic_job(event_id: str, image, bank_code: Optional[str]):
    try:
        result = _analyze_image(image, bank_code, None, False)
    except Exception:
        event_store.release(event_id)
        raise RuntimeError("Shopify forensic processing failed.") from None
    event_store.complete(event_id)
    return result


@router.post("/webhooks/orders-create", status_code=202)
async def shopify_orders_create(request: Request):
    """Authenticate and queue screening of a manual-payment order proof."""
    secret = os.getenv("VERISLIP_SHOPIFY_WEBHOOK_SECRET")
    if not secret:
        raise HTTPException(status_code=503, detail="Shopify integration is unavailable.")
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_WEBHOOK_BYTES:
                raise HTTPException(status_code=413, detail="Webhook payload is too large.")
        except ValueError:
            raise HTTPException(status_code=400, detail="Webhook request is malformed.") from None
    body = await request.body()
    if len(body) > MAX_WEBHOOK_BYTES:
        raise HTTPException(status_code=413, detail="Webhook payload is too large.")
    if not verify_webhook_signature(body, request.headers.get("X-Shopify-Hmac-Sha256"), secret):
        raise HTTPException(status_code=401, detail="Shopify webhook signature is invalid.")
    if request.headers.get("X-Shopify-Topic") != "orders/create":
        raise HTTPException(status_code=400, detail="Shopify webhook topic is unsupported.")
    event_id = request.headers.get("X-Shopify-Webhook-Id", "")
    if not EVENT_ID_PATTERN.fullmatch(event_id):
        raise HTTPException(status_code=400, detail="Shopify webhook ID is invalid.")
    try:
        order = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=400, detail="Shopify webhook payload is malformed.") from None
    if not isinstance(order, dict):
        raise HTTPException(status_code=400, detail="Shopify webhook payload is malformed.")

    if not event_store.reserve(event_id):
        return {"status": "duplicate", "event_id": event_id}
    if not _is_manual_payment(order):
        event_store.complete(event_id)
        return {"status": "ignored", "reason": "unsupported_payment_method"}
    proof_url = _proof_url(order)
    if proof_url is None:
        event_store.complete(event_id)
        return {"status": "ignored", "reason": "payment_proof_missing"}
    try:
        image = await download_shopify_image(proof_url)
    except ShopifyIntegrationError as exc:
        event_store.release(event_id)
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from None

    bank_code = order.get("payment_bank_code")
    if not isinstance(bank_code, str) or len(bank_code) > 40:
        bank_code = None
    correlation_id = get_correlation_id() or request.state.correlation_id
    owner_id = "shopify:" + hashlib.sha256(event_id.encode("utf-8")).hexdigest()
    task = partial(_process_forensic_job, event_id, image, bank_code)
    try:
        job_manager.submit(owner_id, correlation_id, task)
    except JobQueueFullError:
        event_store.release(event_id)
        raise HTTPException(status_code=503, detail="Verification capacity is temporarily unavailable.") from None
    return {"status": "accepted", "event_id": event_id}
