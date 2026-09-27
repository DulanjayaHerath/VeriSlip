"""Regression coverage for default credentials and webhook SSRF."""

import hashlib
import json
import socket

import httpx
import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.middleware.rate_limiter import ApiKeyRegistry
from core.notifications.webhook_dispatcher import WebhookDispatcher


@pytest.mark.parametrize("config", [None, "", "{}", "  {}  "])
@pytest.mark.parametrize("mode", [None, "production", "staging"])
def test_missing_keys_fail_closed(monkeypatch, config, mode):
    for name, value in [("VERISLIP_API_KEY_HASHES", config), ("VERISLIP_ENV", mode)]:
        if value is None:
            monkeypatch.delenv(name, raising=False)
        else:
            monkeypatch.setenv(name, value)
    registry = ApiKeyRegistry.from_environment()
    assert not registry.is_configured
    assert registry.authenticate("verislip-dev-key") is None


def test_development_opt_in_and_configured_keys(monkeypatch):
    monkeypatch.setenv("VERISLIP_ENV", "development")
    monkeypatch.delenv("VERISLIP_API_KEY_HASHES", raising=False)
    assert ApiKeyRegistry.from_environment().authenticate("verislip-dev-key")
    key_hash = hashlib.sha256(b"configured-key").hexdigest()
    monkeypatch.setenv("VERISLIP_API_KEY_HASHES", json.dumps({key_hash: "free"}))
    registry = ApiKeyRegistry.from_environment()
    assert registry.authenticate("verislip-dev-key") is None
    assert registry.authenticate("configured-key")


@pytest.mark.anyio
@pytest.mark.parametrize(
    "url,addresses",
    [
        ("http://merchant.example/hook", ["8.8.8.8"]),
        ("https://other.example/hook", ["8.8.8.8"]),
        ("https://merchant.example:8443/hook", ["8.8.8.8"]),
        ("https://user:pass@merchant.example/hook", ["8.8.8.8"]),
        ("https://merchant.example/hook", ["127.0.0.1"]),
        ("https://merchant.example/hook", ["10.1.2.3"]),
        ("https://merchant.example/hook", ["169.254.169.254"]),
        ("https://merchant.example/hook", ["::1"]),
        ("https://merchant.example/hook", ["fc00::1"]),
        ("https://merchant.example/hook", ["::ffff:127.0.0.1"]),
        ("https://merchant.example/hook", ["8.8.8.8", "192.168.1.1"]),
        ("https://merchant.example/hook", []),
    ],
)
async def test_unsafe_targets_never_connect(monkeypatch, url, addresses):
    monkeypatch.setenv("VERISLIP_WEBHOOK_HOSTS", "merchant.example")
    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *a, **kw: [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 443)) for ip in addresses
        ],
    )

    def unexpected(request):
        pytest.fail("Unsafe destination reached transport")

    async with httpx.AsyncClient(transport=httpx.MockTransport(unexpected)) as client:
        with pytest.raises(ValueError, match="destination"):
            await WebhookDispatcher(secret_key="test-secret").dispatch(
                url, "test", {}, client=client
            )


@pytest.mark.anyio
@pytest.mark.parametrize("status", [200, 302])
async def test_pinned_delivery_preserves_tls_host_and_blocks_redirects(
    monkeypatch, status
):
    monkeypatch.setenv("VERISLIP_WEBHOOK_HOSTS", "merchant.example")
    resolutions = []

    def resolve(*args, **kwargs):
        resolutions.append(args)
        assert len(resolutions) == 1
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 443))]

    monkeypatch.setattr(socket, "getaddrinfo", resolve)
    requests = []

    def capture(request):
        requests.append(request)
        assert request.url.host == "8.8.8.8"
        assert request.headers["host"] == "merchant.example"
        assert request.extensions["sni_hostname"] == "merchant.example"
        assert request.url.path == "/hook"
        return httpx.Response(status, headers={"location": "http://127.0.0.1/admin"})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(capture), follow_redirects=True
    ) as client:
        result = await WebhookDispatcher(secret_key="test-secret").dispatch(
            "https://merchant.example/hook", "test", {}, client=client
        )
    assert len(requests) == 1
    assert result["status_code"] == status
    assert result["success"] is (status == 200)


def test_dispatch_endpoint_without_allowlist_returns_safe_error(monkeypatch):
    monkeypatch.delenv("VERISLIP_WEBHOOK_HOSTS", raising=False)
    response = TestClient(app).post(
        "/api/v1/integrations/webhooks/dispatch",
        headers={"X-API-Key": "test-pro-key"},
        json={"target_url": "http://127.0.0.1/internal"},
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Webhook destination is not permitted or unavailable."
    )
