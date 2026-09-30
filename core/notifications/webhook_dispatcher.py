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
import os
import socket
import ipaddress
from typing import Dict, Any, Optional
import httpx
from starlette.concurrency import run_in_threadpool


def _resolve_target(target_url: str):
    """Approve the host and pin delivery to a validated public IP."""
    try:
        url = httpx.URL(target_url)
        allowed = {
            host.strip().lower()
            for host in os.getenv("VERISLIP_WEBHOOK_HOSTS", "").split(",")
            if host.strip()
        }
        if (
            url.scheme != "https"
            or not url.host
            or url.host.lower() not in allowed
            or url.userinfo
            or url.fragment
            or url.port not in (None, 443)
        ):
            raise ValueError
        addresses = socket.getaddrinfo(url.host, 443, type=socket.SOCK_STREAM)
        ips = [ipaddress.ip_address(item[4][0]) for item in addresses]
        if not ips or any(not ip.is_global or ip.is_multicast for ip in ips):
            raise ValueError
        return url, url.copy_with(host=str(ips[0]))
    except (ValueError, httpx.InvalidURL, OSError):
        raise ValueError(
            "Webhook destination is not permitted or unavailable."
        ) from None


class WebhookDispatcher:
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key

    def generate_signature(self, payload_bytes: bytes) -> str:
        """Compute HMAC-SHA256 signature for the given payload."""
        secret = (
            self.secret_key
            if self.secret_key is not None
            else os.getenv("VERISLIP_WEBHOOK_SECRET", "")
        )
        if not secret.strip() or secret == "verislip_default_webhook_secret":
            raise RuntimeError("Webhook signing is not configured.")
        return hmac.new(
            secret.encode("utf-8"), payload_bytes, hashlib.sha256
        ).hexdigest()

    def build_event_payload(
        self, event_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Construct standard webhook notification body."""
        return {
            "event_id": f"evt_{uuid.uuid4().hex[:16]}",
            "event": event_type,
            "created_at": int(time.time()),
            "data": data,
        }

    async def dispatch(
        self,
        target_url: str,
        event_type: str,
        data: Dict[str, Any],
        client: Optional[httpx.AsyncClient] = None,
    ) -> Dict[str, Any]:
        """
        Send signed webhook POST request to the target URL.
        Returns dispatch status and HTTP response details.
        """
        original_url, pinned_url = await run_in_threadpool(_resolve_target, target_url)
        payload = self.build_event_payload(event_type, data)
        payload_json = json.dumps(payload, sort_keys=True)
        payload_bytes = payload_json.encode("utf-8")
        signature = self.generate_signature(payload_bytes)

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "VeriSlip-Webhook-Dispatcher/1.0",
            "X-VeriSlip-Signature": signature,
            "X-VeriSlip-Event": event_type,
            "Host": original_url.host,
        }

        should_close = False
        if client is None:
            client = httpx.AsyncClient(timeout=5.0, trust_env=False)
            should_close = True

        try:
            # Pin the connection IP while preserving TLS certificate verification
            # against the approved hostname. Never follow destination redirects.
            async with client.stream(
                "POST",
                pinned_url,
                content=payload_bytes,
                headers=headers,
                extensions={"sni_hostname": original_url.host},
                follow_redirects=False,
            ) as response:
                status_code = response.status_code
                success = response.is_success
            return {
                "success": success,
                "status_code": status_code,
                "event_id": payload["event_id"],
                "delivered_at": time.time(),
                "error": None if success else f"HTTP {status_code}",
            }
        except Exception:
            return {
                "success": False,
                "status_code": None,
                "event_id": payload["event_id"],
                "delivered_at": time.time(),
                "error": "Webhook delivery failed.",
            }
        finally:
            if should_close:
                await client.aclose()
