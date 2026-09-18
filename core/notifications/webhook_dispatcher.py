"""
VeriSlip Webhook Dispatcher v1.0
Dispatches signed event payloads to merchant / ERP systems upon slip verification.
Uses HMAC-SHA256 signatures in 'X-VeriSlip-Signature' for replay protection & authenticity.
"""

import hmac
import hashlib
import json
import time
import uuid
from typing import Dict, Any, Optional
import httpx


class WebhookDispatcher:
    def __init__(self, secret_key: str = "verislip_default_webhook_secret"):
        self.secret_key = secret_key

    def generate_signature(self, payload_bytes: bytes) -> str:
        """Compute HMAC-SHA256 signature for the given payload."""
        return hmac.new(
            self.secret_key.encode("utf-8"),
            payload_bytes,
            hashlib.sha256
        ).hexdigest()

    def build_event_payload(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Construct standard webhook notification body."""
        return {
            "event_id": f"evt_{uuid.uuid4().hex[:16]}",
            "event": event_type,
            "created_at": int(time.time()),
            "data": data
        }

    async def dispatch(
        self,
        target_url: str,
        event_type: str,
        data: Dict[str, Any],
        client: Optional[httpx.AsyncClient] = None
    ) -> Dict[str, Any]:
        """
        Send signed webhook POST request to the target URL.
        Returns dispatch status and HTTP response details.
        """
        payload = self.build_event_payload(event_type, data)
        payload_json = json.dumps(payload, sort_keys=True)
        payload_bytes = payload_json.encode("utf-8")
        signature = self.generate_signature(payload_bytes)

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "VeriSlip-Webhook-Dispatcher/1.0",
            "X-VeriSlip-Signature": signature,
            "X-VeriSlip-Event": event_type,
        }

        should_close = False
        if client is None:
            client = httpx.AsyncClient(timeout=5.0)
            should_close = True

        try:
            response = await client.post(target_url, content=payload_bytes, headers=headers)
            return {
                "success": response.is_success,
                "status_code": response.status_code,
                "event_id": payload["event_id"],
                "delivered_at": time.time(),
                "error": None if response.is_success else f"HTTP {response.status_code}"
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": None,
                "event_id": payload["event_id"],
                "delivered_at": time.time(),
                "error": str(e)
            }
        finally:
            if should_close:
                await client.aclose()
