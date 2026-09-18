"""Tests for Dialog/Mobitel SMS delivery and high-risk fallback policy."""

import base64
import io
import logging

import httpx
import pytest
from fastapi.testclient import TestClient
from PIL import Image

import api.routes.webhook_whatsapp as whatsapp_route
from api.main import app
from core.notifications.sms_fallback import (
    DialogMobitelSmsProvider,
    InMemoryNotificationDeduplicator,
    SmsDelivery,
    SmsErrorCode,
    SmsFallbackNotifier,
    SmsFallbackStatus,
    SmsGatewayConfig,
    SmsProviderError,
)


SECRET = "test-sms-password-not-real"


def _config(**overrides):
    values = {
        "enabled": True,
        "gateway_url": "https://sms-gateway.example.test/sms/send",
        "application_id": "APP_TEST_ONLY",
        "password": SECRET,
        "sender_id": "VeriSlip",
        "connect_timeout_seconds": 1.0,
        "read_timeout_seconds": 2.0,
    }
    values.update(overrides)
    return SmsGatewayConfig(**values)


def _client(handler):
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


@pytest.mark.anyio
async def test_successful_dialog_mobitel_sms_request():
    def handler(request):
        payload = __import__("json").loads(request.content)
        assert payload["applicationId"] == "APP_TEST_ONLY"
        assert payload["password"] == SECRET
        assert payload["destinationAddresses"] == ["tel:94771234567"]
        assert payload["sourceAddress"] == "VeriSlip"
        assert "receipt" not in payload["message"].lower()
        return httpx.Response(200, json={"statusCode": "S1000", "requestId": "req-1"})

    provider = DialogMobitelSmsProvider(_config())
    client = _client(handler)
    async with client:
        result = await provider.send(
            "+94771234567", "High-risk fraud alert", client=client
        )

    assert result == SmsDelivery("req-1")


@pytest.mark.anyio
async def test_provider_authentication_failure_is_safe():
    provider = DialogMobitelSmsProvider(_config())
    client = _client(
        lambda request: httpx.Response(401, json={"detail": SECRET})
    )
    async with client:
        with pytest.raises(SmsProviderError) as exc:
            await provider.send("0771234567", "alert", client=client)

    assert exc.value.code is SmsErrorCode.AUTHENTICATION
    assert str(exc.value) == "SMS gateway authentication failed."
    assert SECRET not in str(exc.value)


@pytest.mark.anyio
async def test_provider_timeout_is_safe():
    def handler(request):
        raise httpx.ReadTimeout("private timeout detail", request=request)

    provider = DialogMobitelSmsProvider(_config())
    client = _client(handler)
    async with client:
        with pytest.raises(SmsProviderError) as exc:
            await provider.send("+94771234567", "alert", client=client)
    assert exc.value.code is SmsErrorCode.TIMEOUT
    assert str(exc.value) == "SMS gateway timed out."


@pytest.mark.anyio
async def test_provider_network_failure_is_safe():
    def handler(request):
        raise httpx.ConnectError("private network detail", request=request)

    provider = DialogMobitelSmsProvider(_config())
    client = _client(handler)
    async with client:
        with pytest.raises(SmsProviderError) as exc:
            await provider.send("+94771234567", "alert", client=client)
    assert exc.value.code is SmsErrorCode.NETWORK
    assert str(exc.value) == "SMS gateway is unavailable."


@pytest.mark.anyio
async def test_malformed_provider_response_is_rejected():
    provider = DialogMobitelSmsProvider(_config())
    client = _client(lambda request: httpx.Response(200, content=b"not-json"))
    async with client:
        with pytest.raises(SmsProviderError) as exc:
            await provider.send("+94771234567", "alert", client=client)
    assert exc.value.code is SmsErrorCode.MALFORMED_RESPONSE


@pytest.mark.anyio
async def test_provider_rejected_sms_is_safe():
    provider = DialogMobitelSmsProvider(_config())
    client = _client(
        lambda request: httpx.Response(
            200, json={"statusCode": "E1601", "statusDetail": SECRET}
        )
    )
    async with client:
        with pytest.raises(SmsProviderError) as exc:
            await provider.send("+94771234567", "alert", client=client)
    assert exc.value.code is SmsErrorCode.REJECTED
    assert SECRET not in str(exc.value)


class _FakeProvider:
    def __init__(self, error=None):
        self.error = error
        self.calls = []

    async def send(self, recipient, message, *, client=None):
        self.calls.append((recipient, message))
        if self.error:
            raise self.error
        return SmsDelivery("fake-request")


@pytest.mark.anyio
async def test_fallback_triggers_only_for_unreachable_high_risk_seller():
    provider = _FakeProvider()
    notifier = SmsFallbackNotifier(provider)

    result = await notifier.notify(
        recipient="+94771234567",
        verdict="HIGH_RISK_TAMPERED",
        whatsapp_delivery_failed=True,
        event_id="wamid.high-risk",
    )

    assert result.status is SmsFallbackStatus.SENT
    assert len(provider.calls) == 1


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("verdict", "delivery_failed"),
    [("AUTHENTIC", True), ("SUSPICIOUS", True), ("HIGH_RISK_TAMPERED", False)],
)
async def test_no_sms_when_fallback_is_unnecessary(verdict, delivery_failed):
    provider = _FakeProvider()
    notifier = SmsFallbackNotifier(provider)

    result = await notifier.notify(
        recipient="+94771234567",
        verdict=verdict,
        whatsapp_delivery_failed=delivery_failed,
        event_id="wamid.not-needed",
    )

    assert result.status is SmsFallbackStatus.NOT_NEEDED
    assert provider.calls == []


@pytest.mark.anyio
async def test_duplicate_fallback_alert_is_sent_once():
    provider = _FakeProvider()
    notifier = SmsFallbackNotifier(
        provider, InMemoryNotificationDeduplicator()
    )
    args = {
        "recipient": "+94771234567",
        "verdict": "HIGH_RISK_TAMPERED",
        "whatsapp_delivery_failed": True,
        "event_id": "wamid.duplicate-alert",
    }

    first = await notifier.notify(**args)
    duplicate = await notifier.notify(**args)

    assert first.status is SmsFallbackStatus.SENT
    assert duplicate.status is SmsFallbackStatus.DUPLICATE
    assert len(provider.calls) == 1


@pytest.mark.anyio
async def test_failed_fallback_can_be_retried_without_secret_leak(caplog):
    provider = _FakeProvider(
        SmsProviderError(SmsErrorCode.AUTHENTICATION, "safe authentication failure")
    )
    notifier = SmsFallbackNotifier(provider)
    args = {
        "recipient": "+94771234567",
        "verdict": "HIGH_RISK_TAMPERED",
        "whatsapp_delivery_failed": True,
        "event_id": "wamid.retry-alert",
    }

    with caplog.at_level(logging.WARNING, logger="verislip.sms"):
        first = await notifier.notify(**args)
        second = await notifier.notify(**args)

    assert first.status is second.status is SmsFallbackStatus.FAILED
    assert len(provider.calls) == 2
    assert SECRET not in caplog.text
    assert "+94771234567" not in caplog.text


def _image_base64():
    buffer = io.BytesIO()
    Image.new("RGB", (80, 120), "white").save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def test_whatsapp_endpoint_triggers_fallback_after_high_risk_result(monkeypatch):
    provider = _FakeProvider()
    notifier = SmsFallbackNotifier(provider)
    monkeypatch.setattr(whatsapp_route, "sms_fallback_notifier", notifier)
    monkeypatch.setattr(
        whatsapp_route.engine,
        "analyze",
        lambda image: {
            "verdict": "HIGH_RISK_TAMPERED",
            "tamper_risk_percentage": 94.0,
            "flagged_regions": [],
            "findings_summary": ["Anomaly detected"],
        },
    )
    response = TestClient(app, headers={"X-API-Key": "test-pro-key"}).post(
        "/api/v1/webhook/whatsapp",
        json={
            "from_phone": "+94771234999",
            "image_base64": _image_base64(),
            "message_id": "wamid.endpoint-sms",
            "whatsapp_delivery_failed": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["sms_fallback_status"] == "sent"
    assert len(provider.calls) == 1


def test_sms_configuration_validation(monkeypatch):
    monkeypatch.setenv("VERISLIP_SMS_ENABLED", "1")
    monkeypatch.setenv("VERISLIP_SMS_GATEWAY_URL", "https://sms.example.test/send")
    monkeypatch.setenv("VERISLIP_SMS_APPLICATION_ID", "APP_TEST")
    monkeypatch.setenv("VERISLIP_SMS_PASSWORD", "placeholder-only")
    monkeypatch.setenv("VERISLIP_SMS_SENDER_ID", "VeriSlip")
    monkeypatch.setenv("VERISLIP_SMS_CONNECT_TIMEOUT_SECONDS", "3")
    monkeypatch.setenv("VERISLIP_SMS_READ_TIMEOUT_SECONDS", "8")

    config = SmsGatewayConfig.from_environment()

    assert config.enabled is True
    assert config.connect_timeout_seconds == 3
    assert config.read_timeout_seconds == 8


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("VERISLIP_SMS_ENABLED", "true"),
        ("VERISLIP_SMS_GATEWAY_URL", "http://sms.example.test/send"),
        ("VERISLIP_SMS_SENDER_ID", "invalid sender id!"),
        ("VERISLIP_SMS_CONNECT_TIMEOUT_SECONDS", "0"),
        ("VERISLIP_SMS_READ_TIMEOUT_SECONDS", "not-a-number"),
    ],
)
def test_invalid_sms_configuration_fails_closed(monkeypatch, name, value):
    monkeypatch.setenv("VERISLIP_SMS_ENABLED", "1")
    monkeypatch.setenv("VERISLIP_SMS_GATEWAY_URL", "https://sms.example.test/send")
    monkeypatch.setenv("VERISLIP_SMS_APPLICATION_ID", "APP_TEST")
    monkeypatch.setenv("VERISLIP_SMS_PASSWORD", "placeholder-only")
    monkeypatch.setenv("VERISLIP_SMS_SENDER_ID", "VeriSlip")
    monkeypatch.setenv(name, value)

    with pytest.raises(RuntimeError):
        SmsGatewayConfig.from_environment()
