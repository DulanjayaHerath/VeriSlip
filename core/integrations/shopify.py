"""Security, idempotency, and media retrieval for Shopify webhooks."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import threading
import time
from typing import Callable, Dict, Optional
from urllib.parse import urlsplit

import httpx
from PIL import Image
from starlette.concurrency import run_in_threadpool

from core.security.image_sanitizer import ImageValidationError, MAX_IMAGE_UPLOAD_BYTES, sanitize_image_bytes

SUPPORTED_MEDIA_TYPES = frozenset({"image/jpeg", "image/png"})
DEFAULT_MEDIA_HOSTS = frozenset({"cdn.shopify.com"})


class ShopifyIntegrationError(ValueError):
    """Safe client-facing Shopify integration failure."""

    def __init__(self, detail: str, status_code: int):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


def verify_webhook_signature(body: bytes, supplied: Optional[str], secret: str) -> bool:
    """Verify Shopify's base64 HMAC-SHA256 signature in constant time."""
    if not supplied or not secret:
        return False
    expected = base64.b64encode(
        hmac.new(secret.encode("utf-8"), body, hashlib.sha256).digest()
    ).decode("ascii")
    return hmac.compare_digest(expected, supplied.strip())


def _bounded_float(name: str, default: float, minimum: float, maximum: float) -> float:
    try:
        value = float(os.getenv(name, str(default)))
    except ValueError:
        return default
    return max(minimum, min(maximum, value))


def _allowed_hosts() -> frozenset[str]:
    configured = os.getenv("VERISLIP_SHOPIFY_MEDIA_HOSTS", "")
    if not configured.strip():
        return DEFAULT_MEDIA_HOSTS
    hosts = {
        host.strip().lower()
        for host in configured.split(",")
        if host.strip() and "/" not in host and ":" not in host and "@" not in host
    }
    if not hosts:
        raise ShopifyIntegrationError("Shopify integration is not configured.", 503)
    return frozenset(hosts)


def validate_media_url(url: object) -> str:
    """Allow only configured HTTPS Shopify media hosts to prevent SSRF."""
    if not isinstance(url, str) or len(url) > 2_048:
        raise ShopifyIntegrationError("Shopify payment proof URL is invalid.", 400)
    parsed = urlsplit(url)
    hostname = (parsed.hostname or "").lower()
    try:
        port = parsed.port
    except ValueError:
        raise ShopifyIntegrationError("Shopify payment proof URL is invalid.", 400) from None
    if (
        parsed.scheme != "https"
        or hostname not in _allowed_hosts()
        or parsed.username is not None
        or parsed.password is not None
        or port not in (None, 443)
    ):
        raise ShopifyIntegrationError("Shopify payment proof URL is invalid.", 400)
    return url


async def _download_with_client(client: httpx.AsyncClient, url: str) -> Image.Image:
    try:
        async with client.stream("GET", validate_media_url(url)) as response:
            if response.status_code in (401, 403):
                raise ShopifyIntegrationError("Shopify payment proof access was rejected.", 502)
            if response.status_code >= 400:
                raise ShopifyIntegrationError("Shopify payment proof is unavailable.", 502)
            content_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
            if content_type not in SUPPORTED_MEDIA_TYPES:
                raise ShopifyIntegrationError("Shopify payment proof must be a JPEG or PNG image.", 415)
            content_length = response.headers.get("content-length")
            if content_length:
                try:
                    length = int(content_length)
                except ValueError:
                    raise ShopifyIntegrationError("Shopify returned an invalid media response.", 502) from None
                if length < 0:
                    raise ShopifyIntegrationError("Shopify returned an invalid media response.", 502)
                if length > MAX_IMAGE_UPLOAD_BYTES:
                    raise ShopifyIntegrationError("Shopify payment proof exceeds the permitted size.", 413)
            data = bytearray()
            async for chunk in response.aiter_bytes():
                data.extend(chunk)
                if len(data) > MAX_IMAGE_UPLOAD_BYTES:
                    raise ShopifyIntegrationError("Shopify payment proof exceeds the permitted size.", 413)
    except ShopifyIntegrationError:
        raise
    except httpx.TimeoutException:
        raise ShopifyIntegrationError("Shopify payment proof request timed out.", 504) from None
    except httpx.HTTPError:
        raise ShopifyIntegrationError("Shopify payment proof service is unavailable.", 502) from None
    try:
        return await run_in_threadpool(sanitize_image_bytes, bytes(data))
    except ImageValidationError as exc:
        raise ShopifyIntegrationError(exc.detail, exc.status_code) from None


async def download_shopify_image(url: str, *, client: Optional[httpx.AsyncClient] = None) -> Image.Image:
    """Download a bounded Shopify proof into sanitized in-memory pixels."""
    if client is not None:
        return await _download_with_client(client, url)
    timeout = httpx.Timeout(
        connect=_bounded_float("VERISLIP_SHOPIFY_CONNECT_TIMEOUT_SECONDS", 5, 1, 30),
        read=_bounded_float("VERISLIP_SHOPIFY_READ_TIMEOUT_SECONDS", 15, 1, 60),
        write=5,
        pool=5,
    )
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as owned:
        return await _download_with_client(owned, url)


class ShopifyEventStore:
    """Bounded local idempotency store using only webhook-ID fingerprints."""

    def __init__(self, ttl_seconds: int = 86_400, max_records: int = 10_000, clock: Callable[[], float] = time.time) -> None:
        self.ttl_seconds = ttl_seconds
        self.max_records = max_records
        self._clock = clock
        self._records: Dict[str, tuple[str, float]] = {}
        self._lock = threading.Lock()

    @staticmethod
    def _key(event_id: str) -> str:
        return hashlib.sha256(event_id.encode("utf-8")).hexdigest()

    def _cleanup_locked(self, now: float) -> None:
        self._records = {key: record for key, record in self._records.items() if record[1] > now}
        if len(self._records) > self.max_records:
            oldest = sorted(self._records, key=lambda key: self._records[key][1])
            for key in oldest[: len(self._records) - self.max_records]:
                self._records.pop(key, None)

    def reserve(self, event_id: str) -> bool:
        now = self._clock()
        key = self._key(event_id)
        with self._lock:
            self._cleanup_locked(now)
            if key in self._records:
                return False
            self._records[key] = ("processing", now + self.ttl_seconds)
            return True

    def complete(self, event_id: str) -> None:
        key = self._key(event_id)
        with self._lock:
            if key in self._records:
                self._records[key] = ("completed", self._clock() + self.ttl_seconds)

    def release(self, event_id: str) -> None:
        with self._lock:
            self._records.pop(self._key(event_id), None)

    def clear(self) -> None:
        with self._lock:
            self._records.clear()
