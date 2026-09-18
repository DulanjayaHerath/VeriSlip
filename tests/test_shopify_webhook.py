"""Signed Shopify manual-payment webhook integration tests."""

import base64
import hashlib
import hmac
import io
import json
from types import SimpleNamespace

import httpx
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from api.main import app
from api.routes import shopify
from core.integrations.shopify import (
    ShopifyIntegrationError,
    download_shopify_image,
)


SECRET = "test-shopify-secret-never-log"
client = TestClient(app)


def _image_bytes():
    output = io.BytesIO()
    Image.new("RGB", (24, 32), "white").save(output, format="PNG")
    return output.getvalue()


def _order(*, proof=True, manual=True):
    attributes = []
    if proof:
        attributes.append(
            {"name": "payment_proof_url", "value": "https://cdn.shopify.com/s/files/proof.png"}
        )
    return {
        "id": 123456,
        "payment_gateway_names": ["Bank Deposit"] if manual else ["Shopify Payments"],
        "note_attributes": attributes,
        "email": "customer-private@example.test",
    }


def _signed_request(payload, event_id="shopify-event-80", **headers):
    body = payload if isinstance(payload, bytes) else json.dumps(payload, separators=(",", ":")).encode()
    signature = base64.b64encode(hmac.new(SECRET.encode(), body, hashlib.sha256).digest()).decode()
    request_headers = {
        "Content-Type": "application/json",
        "X-Shopify-Hmac-Sha256": signature,
        "X-Shopify-Topic": "orders/create",
        "X-Shopify-Webhook-Id": event_id,
        **headers,
    }
    return client.post(
        "/api/v1/integrations/shopify/webhooks/orders-create",
        content=body,
        headers=request_headers,
    )


class ImmediateJobManager:
    def __init__(self, execute=True):
        self.tasks = []
        self.execute = execute

    def submit(self, owner_key_id, correlation_id, task):
        self.tasks.append(task)
        if self.execute:
            task()
        return SimpleNamespace(job_id="job-1")


@pytest.fixture(autouse=True)
def configure_shopify(monkeypatch):
    monkeypatch.setenv("VERISLIP_SHOPIFY_WEBHOOK_SECRET", SECRET)
    shopify.event_store.clear()
    yield
    shopify.event_store.clear()


def _patch_success(monkeypatch, *, manager=None):
    calls = {"download": 0, "forensics": 0}

    async def download(url):
        calls["download"] += 1
        return Image.new("RGB", (24, 32), "white")

    def analyze(*args, **kwargs):
        calls["forensics"] += 1
        return {"verdict": "AUTHENTIC", "tamper_risk_percentage": 4.0}

    monkeypatch.setattr(shopify, "download_shopify_image", download)
    monkeypatch.setattr(shopify, "_analyze_image", analyze)
    monkeypatch.setattr(shopify, "job_manager", manager or ImmediateJobManager())
    return calls


def test_valid_manual_payment_webhook_is_accepted_without_api_key(monkeypatch):
    calls = _patch_success(monkeypatch)
    response = _signed_request(_order(), **{"X-Request-ID": "shopify-correlation-80"})
    assert response.status_code == 202
    assert response.json() == {"status": "accepted", "event_id": "shopify-event-80"}
    assert response.headers["X-Request-ID"] == "shopify-correlation-80"
    assert calls == {"download": 1, "forensics": 1}


@pytest.mark.parametrize("signature", [None, "invalid-signature"])
def test_missing_or_invalid_signature_is_rejected(signature):
    body = json.dumps(_order(), separators=(",", ":")).encode()
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Topic": "orders/create",
        "X-Shopify-Webhook-Id": "event-invalid-signature",
    }
    if signature:
        headers["X-Shopify-Hmac-Sha256"] = signature
    response = client.post(
        "/api/v1/integrations/shopify/webhooks/orders-create", content=body, headers=headers
    )
    assert response.status_code == 401


def test_signed_malformed_payload_is_rejected():
    response = _signed_request(b"{malformed-json", event_id="malformed-event")
    assert response.status_code == 400
    assert response.json()["detail"] == "Shopify webhook payload is malformed."


def test_non_manual_order_is_ignored(monkeypatch):
    calls = _patch_success(monkeypatch)
    response = _signed_request(_order(manual=False), event_id="card-order")
    assert response.status_code == 202
    assert response.json()["reason"] == "unsupported_payment_method"
    assert calls == {"download": 0, "forensics": 0}


def test_order_without_payment_proof_is_ignored(monkeypatch):
    calls = _patch_success(monkeypatch)
    response = _signed_request(_order(proof=False), event_id="missing-proof")
    assert response.status_code == 202
    assert response.json()["reason"] == "payment_proof_missing"
    assert calls == {"download": 0, "forensics": 0}


def test_duplicate_webhook_does_not_repeat_download_or_processing(monkeypatch):
    calls = _patch_success(monkeypatch)
    first = _signed_request(_order(), event_id="duplicate-event")
    second = _signed_request(_order(), event_id="duplicate-event")
    assert first.status_code == 202
    assert second.status_code == 202
    assert second.json()["status"] == "duplicate"
    assert calls == {"download": 1, "forensics": 1}


@pytest.mark.parametrize(
    "error,status",
    [
        (ShopifyIntegrationError("Shopify payment proof request timed out.", 504), 504),
        (ShopifyIntegrationError("Shopify payment proof service is unavailable.", 502), 502),
        (ShopifyIntegrationError("Uploaded file is not a valid, complete JPEG or PNG image.", 400), 400),
    ],
)
def test_download_failures_are_safe_and_retryable(monkeypatch, error, status):
    calls = 0

    async def fail(url):
        nonlocal calls
        calls += 1
        raise error

    monkeypatch.setattr(shopify, "download_shopify_image", fail)
    first = _signed_request(_order(), event_id="retryable-download")
    second = _signed_request(_order(), event_id="retryable-download")
    assert first.status_code == status
    assert second.status_code == status
    assert calls == 2
    assert "traceback" not in first.text.lower()


def test_forensic_failure_is_safe_and_releases_idempotency(monkeypatch):
    manager = ImmediateJobManager(execute=False)
    _patch_success(monkeypatch, manager=manager)

    def fail(*args, **kwargs):
        raise RuntimeError("private receipt/customer detail")

    monkeypatch.setattr(shopify, "_analyze_image", fail)
    accepted = _signed_request(_order(), event_id="forensic-failure")
    assert accepted.status_code == 202
    with pytest.raises(RuntimeError, match="Shopify forensic processing failed"):
        manager.tasks[0]()

    _patch_success(monkeypatch)
    retry = _signed_request(_order(), event_id="forensic-failure")
    assert retry.status_code == 202
    assert retry.json()["status"] == "accepted"


@pytest.mark.anyio
async def test_receipt_download_is_sanitized_with_mocked_http():
    payload = _image_bytes()

    def handler(request):
        return httpx.Response(200, content=payload, headers={"content-type": "image/png"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        image = await download_shopify_image(
            "https://cdn.shopify.com/s/files/proof.png", client=http_client
        )
    assert image.mode == "RGB"
    assert image.info == {}


@pytest.mark.anyio
async def test_external_timeout_and_network_failure_are_mapped_safely():
    for exception, expected_status in [
        (httpx.ReadTimeout("secret timeout"), 504),
        (httpx.ConnectError("private network detail"), 502),
    ]:
        def handler(request, error=exception):
            error.request = request
            raise error

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
            with pytest.raises(ShopifyIntegrationError) as exc:
                await download_shopify_image(
                    "https://cdn.shopify.com/s/files/proof.png", client=http_client
                )
        assert exc.value.status_code == expected_status
        assert "secret" not in exc.value.detail
        assert "private" not in exc.value.detail


def test_secrets_and_customer_pii_do_not_appear_in_logs(monkeypatch, capsys):
    _patch_success(monkeypatch)
    response = _signed_request(_order(), event_id="privacy-event")
    captured = capsys.readouterr()
    combined = captured.out + captured.err
    assert response.status_code == 202
    assert SECRET not in combined
    assert "customer-private@example.test" not in combined


def test_missing_configuration_fails_closed(monkeypatch):
    monkeypatch.delenv("VERISLIP_SHOPIFY_WEBHOOK_SECRET")
    response = _signed_request(_order(), event_id="missing-config")
    assert response.status_code == 503
    assert response.json()["detail"] == "Shopify integration is unavailable."
