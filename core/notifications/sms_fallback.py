"""Provider-neutral SMS fallback alerts for unreachable WhatsApp merchants."""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import re
import secrets
import threading
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Protocol
from urllib.parse import urlsplit

import httpx


logger = logging.getLogger("verislip.sms")
_HIGH_RISK_VERDICT = "HIGH_RISK_TAMPERED"
_SUCCESS_STATUS_CODES = frozenset({"S1000"})
_AUTH_STATUS_CODES = frozenset({"E1301", "E1302", "E1303", "E1312"})


class SmsErrorCode(str, Enum):
    AUTHENTICATION = "authentication"
    TIMEOUT = "timeout"
    NETWORK = "network"
    MALFORMED_RESPONSE = "malformed_response"
    REJECTED = "rejected"
    INVALID_RECIPIENT = "invalid_recipient"


class SmsProviderError(RuntimeError):
    """A stable, non-sensitive SMS provider failure."""

    def __init__(self, code: SmsErrorCode, detail: str):
        super().__init__(detail)
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class SmsGatewayConfig:
    """Dialog/Mobitel-compatible hSenid-style gateway configuration."""

    enabled: bool
    gateway_url: Optional[str]
    application_id: Optional[str]
    password: Optional[str]
    sender_id: Optional[str]
    connect_timeout_seconds: float = 5.0
    read_timeout_seconds: float = 10.0

    @classmethod
    def from_environment(cls) -> "SmsGatewayConfig":
        enabled_value = os.getenv("VERISLIP_SMS_ENABLED", "0").strip()
        if enabled_value not in {"0", "1"}:
            raise RuntimeError("SMS enabled configuration must be 0 or 1.")
        enabled = enabled_value == "1"
        gateway_url = os.getenv("VERISLIP_SMS_GATEWAY_URL", "").strip() or None
        application_id = os.getenv("VERISLIP_SMS_APPLICATION_ID", "").strip() or None
        password = os.getenv("VERISLIP_SMS_PASSWORD", "").strip() or None
        sender_id = os.getenv("VERISLIP_SMS_SENDER_ID", "").strip() or None
        try:
            connect_timeout = float(
                os.getenv("VERISLIP_SMS_CONNECT_TIMEOUT_SECONDS", "5")
            )
            read_timeout = float(
                os.getenv("VERISLIP_SMS_READ_TIMEOUT_SECONDS", "10")
            )
        except ValueError as exc:
            raise RuntimeError("SMS gateway timeout configuration is invalid.") from exc
        if connect_timeout <= 0 or read_timeout <= 0:
            raise RuntimeError("SMS gateway timeouts must be positive.")

        if enabled:
            if not all((gateway_url, application_id, password, sender_id)):
                raise RuntimeError("SMS gateway configuration is incomplete.")
            parsed = urlsplit(gateway_url)
            if (
                parsed.scheme != "https"
                or not parsed.hostname
                or parsed.username is not None
                or parsed.password is not None
                or len(gateway_url) > 500
            ):
                raise RuntimeError("SMS gateway URL configuration is invalid.")
            if len(application_id) > 128 or len(password) > 512:
                raise RuntimeError("SMS gateway credential configuration is invalid.")
            if not re.fullmatch(r"[A-Za-z0-9_.-]{1,32}", sender_id):
                raise RuntimeError("SMS sender ID configuration is invalid.")

        return cls(
            enabled=enabled,
            gateway_url=gateway_url,
            application_id=application_id,
            password=password,
            sender_id=sender_id,
            connect_timeout_seconds=connect_timeout,
            read_timeout_seconds=read_timeout,
        )


@dataclass(frozen=True)
class SmsDelivery:
    provider_reference: str


class SmsProvider(Protocol):
    """Provider boundary used by the fraud-alert fallback coordinator."""

    async def send(
        self,
        recipient: str,
        message: str,
        *,
        client: Optional[httpx.AsyncClient] = None,
    ) -> SmsDelivery: ...


def _normalize_sri_lankan_number(recipient: str) -> str:
    compact = re.sub(r"[\s()-]", "", recipient)
    if compact.startswith("+"):
        compact = compact[1:]
    if compact.startswith("0") and len(compact) == 10:
        compact = f"94{compact[1:]}"
    if not re.fullmatch(r"94[0-9]{9}", compact):
        raise SmsProviderError(
            SmsErrorCode.INVALID_RECIPIENT,
            "SMS recipient is not a valid Sri Lankan phone number.",
        )
    return compact


class DialogMobitelSmsProvider:
    """JSON adapter for Dialog IdeaMart/Mobitel hSenid-compatible SMS APIs."""

    def __init__(self, config: SmsGatewayConfig):
        if not config.enabled:
            raise ValueError("SMS provider requires enabled gateway configuration.")
        self.config = config

    async def _send_with_client(
        self, client: httpx.AsyncClient, recipient: str, message: str
    ) -> SmsDelivery:
        number = _normalize_sri_lankan_number(recipient)
        payload = {
            "version": "1.0",
            "applicationId": self.config.application_id,
            "password": self.config.password,
            "message": message,
            "destinationAddresses": [f"tel:{number}"],
            "sourceAddress": self.config.sender_id,
            "deliveryStatusRequest": "1",
            "encoding": "0",
        }
        try:
            response = await client.post(self.config.gateway_url, json=payload)
        except httpx.TimeoutException:
            raise SmsProviderError(
                SmsErrorCode.TIMEOUT, "SMS gateway timed out."
            ) from None
        except httpx.HTTPError:
            raise SmsProviderError(
                SmsErrorCode.NETWORK, "SMS gateway is unavailable."
            ) from None

        if response.status_code in (401, 403):
            raise SmsProviderError(
                SmsErrorCode.AUTHENTICATION, "SMS gateway authentication failed."
            )
        if response.status_code >= 400:
            raise SmsProviderError(
                SmsErrorCode.REJECTED, "SMS gateway rejected the alert."
            )
        try:
            body = response.json()
        except (ValueError, TypeError):
            raise SmsProviderError(
                SmsErrorCode.MALFORMED_RESPONSE,
                "SMS gateway returned an invalid response.",
            ) from None
        if not isinstance(body, dict) or not isinstance(body.get("statusCode"), str):
            raise SmsProviderError(
                SmsErrorCode.MALFORMED_RESPONSE,
                "SMS gateway returned an invalid response.",
            )
        status_code = body["statusCode"]
        if status_code in _AUTH_STATUS_CODES:
            raise SmsProviderError(
                SmsErrorCode.AUTHENTICATION, "SMS gateway authentication failed."
            )
        if status_code not in _SUCCESS_STATUS_CODES:
            raise SmsProviderError(
                SmsErrorCode.REJECTED, "SMS gateway rejected the alert."
            )
        request_id = body.get("requestId")
        if request_id is not None and not isinstance(request_id, str):
            raise SmsProviderError(
                SmsErrorCode.MALFORMED_RESPONSE,
                "SMS gateway returned an invalid response.",
            )
        return SmsDelivery(provider_reference=request_id or "accepted")

    async def send(
        self,
        recipient: str,
        message: str,
        *,
        client: Optional[httpx.AsyncClient] = None,
    ) -> SmsDelivery:
        if client is not None:
            return await self._send_with_client(client, recipient, message)
        timeout = httpx.Timeout(
            connect=self.config.connect_timeout_seconds,
            read=self.config.read_timeout_seconds,
            write=5.0,
            pool=5.0,
        )
        async with httpx.AsyncClient(
            timeout=timeout, follow_redirects=False
        ) as owned_client:
            return await self._send_with_client(owned_client, recipient, message)


class SmsFallbackStatus(str, Enum):
    NOT_NEEDED = "not_needed"
    SENT = "sent"
    DUPLICATE = "duplicate"
    FAILED = "failed"
    NOT_CONFIGURED = "not_configured"


@dataclass(frozen=True)
class SmsFallbackResult:
    status: SmsFallbackStatus
    error_code: Optional[SmsErrorCode] = None


class InMemoryNotificationDeduplicator:
    """Atomic process-local reservation of notification event identifiers."""

    def __init__(self, *, max_completed: int = 50_000) -> None:
        if max_completed <= 0:
            raise ValueError("SMS idempotency capacity must be positive.")
        self._hash_key = secrets.token_bytes(32)
        self._pending: Dict[str, str] = {}
        self._completed: Dict[str, None] = {}
        self._max_completed = max_completed
        self._lock = threading.Lock()

    def _key(self, recipient: str, event_id: str) -> str:
        return hmac.new(
            self._hash_key,
            f"{recipient}\0{event_id}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def reserve(self, recipient: str, event_id: Optional[str]) -> Optional[str]:
        if not event_id:
            return secrets.token_urlsafe(24)
        key = self._key(recipient, event_id)
        with self._lock:
            if key in self._pending or key in self._completed:
                return None
            token = secrets.token_urlsafe(24)
            self._pending[key] = token
            return token

    def complete(self, recipient: str, event_id: Optional[str], token: str) -> None:
        if not event_id:
            return
        key = self._key(recipient, event_id)
        with self._lock:
            if self._pending.get(key) != token:
                return
            self._pending.pop(key, None)
            self._completed[key] = None
            while len(self._completed) > self._max_completed:
                self._completed.pop(next(iter(self._completed)))

    def release(self, recipient: str, event_id: Optional[str], token: str) -> None:
        if not event_id:
            return
        key = self._key(recipient, event_id)
        with self._lock:
            if self._pending.get(key) == token:
                self._pending.pop(key, None)


class SmsFallbackNotifier:
    """Send SMS only for high-risk results whose WhatsApp delivery failed."""

    def __init__(
        self,
        provider: Optional[SmsProvider],
        deduplicator: Optional[InMemoryNotificationDeduplicator] = None,
    ) -> None:
        self.provider = provider
        self.deduplicator = deduplicator or InMemoryNotificationDeduplicator()

    async def notify(
        self,
        *,
        recipient: str,
        verdict: str,
        whatsapp_delivery_failed: bool,
        event_id: Optional[str],
    ) -> SmsFallbackResult:
        if verdict != _HIGH_RISK_VERDICT or not whatsapp_delivery_failed:
            return SmsFallbackResult(SmsFallbackStatus.NOT_NEEDED)
        if self.provider is None:
            logger.warning("sms.fallback.not_configured")
            return SmsFallbackResult(SmsFallbackStatus.NOT_CONFIGURED)

        token = self.deduplicator.reserve(recipient, event_id)
        if token is None:
            return SmsFallbackResult(SmsFallbackStatus.DUPLICATE)
        message = (
            "VeriSlip HIGH FRAUD RISK alert: a submitted payment slip may be "
            "forged. Do not dispatch goods; confirm payment in your bank account."
        )
        try:
            await self.provider.send(recipient, message)
        except SmsProviderError as exc:
            self.deduplicator.release(recipient, event_id, token)
            logger.warning("sms.fallback.failed", extra={"error_code": exc.code.value})
            return SmsFallbackResult(SmsFallbackStatus.FAILED, exc.code)
        self.deduplicator.complete(recipient, event_id, token)
        logger.info("sms.fallback.sent")
        return SmsFallbackResult(SmsFallbackStatus.SENT)


def build_sms_fallback_notifier() -> SmsFallbackNotifier:
    config = SmsGatewayConfig.from_environment()
    provider = DialogMobitelSmsProvider(config) if config.enabled else None
    return SmsFallbackNotifier(provider)


sms_fallback_notifier = build_sms_fallback_notifier()
