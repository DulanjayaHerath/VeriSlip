"""Tests for bounded, in-memory WhatsApp Cloud API media retrieval."""

import io
import logging

import httpx
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from api.main import app
from core.integrations import whatsapp_media
from core.integrations.whatsapp_media import WhatsAppMediaError, download_whatsapp_image


def _image_bytes(fmt="PNG", *, metadata=False):
    buffer = io.BytesIO()
    kwargs = {}
    if metadata:
        info = PngInfo()
        info.add_text("customer", "sensitive receipt metadata")
        kwargs["pnginfo"] = info
    Image.new("RGB", (24, 32), "white").save(buffer, format=fmt, **kwargs)
    return buffer.getvalue()


def _client(handler):
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


def _success_handler(payload, *, mime_type="image/png"):
    def handler(request):
        assert request.headers["authorization"] == "Bearer test-whatsapp-token"
        if request.url.host == "graph.facebook.com":
            return httpx.Response(
                200,
                json={
                    "url": "https://lookaside.fbsbx.com/whatsapp_business/attachment",
                    "mime_type": mime_type,
                    "file_size": len(payload),
                },
            )
        return httpx.Response(
            200,
            content=payload,
            headers={"content-type": mime_type, "content-length": str(len(payload))},
        )

    return handler


@pytest.mark.anyio
async def test_successful_download_is_sanitized_in_memory():
    client = _client(_success_handler(_image_bytes(metadata=True)))
    async with client:
        image = await download_whatsapp_image(
            "123456789", access_token="test-whatsapp-token", client=client
        )

    assert image.mode == "RGB"
    assert image.size == (24, 32)
    assert image.info == {}


@pytest.mark.anyio
async def test_invalid_media_id_is_rejected_before_network_call():
    called = False

    def handler(request):
        nonlocal called
        called = True
        return httpx.Response(500)

    client = _client(handler)
    async with client:
        with pytest.raises(WhatsAppMediaError) as exc:
            await download_whatsapp_image(
                "../not-a-media-id", access_token="test-whatsapp-token", client=client
            )

    assert exc.value.status_code == 400
    assert called is False


@pytest.mark.anyio
async def test_meta_authentication_failure_is_safe(caplog):
    secret = "super-secret-whatsapp-token"
    client = _client(lambda request: httpx.Response(401, json={"error": secret}))
    with caplog.at_level(logging.DEBUG):
        async with client:
            with pytest.raises(WhatsAppMediaError) as exc:
                await download_whatsapp_image("123", access_token=secret, client=client)

    assert exc.value.status_code == 502
    assert str(exc.value) == "WhatsApp media service authentication failed."
    assert secret not in caplog.text
    assert secret not in str(exc.value)


@pytest.mark.anyio
async def test_network_timeout_returns_safe_gateway_timeout():
    def handler(request):
        raise httpx.ReadTimeout("upstream detail", request=request)

    client = _client(handler)
    async with client:
        with pytest.raises(WhatsAppMediaError) as exc:
            await download_whatsapp_image(
                "123", access_token="test-whatsapp-token", client=client
            )

    assert exc.value.status_code == 504
    assert str(exc.value) == "WhatsApp media service timed out."


@pytest.mark.anyio
async def test_network_failure_returns_safe_bad_gateway():
    def handler(request):
        raise httpx.ConnectError("private upstream detail", request=request)

    client = _client(handler)
    async with client:
        with pytest.raises(WhatsAppMediaError) as exc:
            await download_whatsapp_image(
                "123", access_token="test-whatsapp-token", client=client
            )

    assert exc.value.status_code == 502
    assert str(exc.value) == "WhatsApp media service is unavailable."


@pytest.mark.anyio
async def test_oversized_metadata_is_rejected_before_download(monkeypatch):
    monkeypatch.setattr(whatsapp_media, "MAX_IMAGE_UPLOAD_BYTES", 8)
    download_requested = False

    def handler(request):
        nonlocal download_requested
        if request.url.host == "graph.facebook.com":
            return httpx.Response(
                200,
                json={
                    "url": "https://lookaside.fbsbx.com/media",
                    "mime_type": "image/png",
                    "file_size": 9,
                },
            )
        download_requested = True
        return httpx.Response(200, content=b"123456789")

    client = _client(handler)
    async with client:
        with pytest.raises(WhatsAppMediaError) as exc:
            await download_whatsapp_image(
                "123", access_token="test-whatsapp-token", client=client
            )

    assert exc.value.status_code == 413
    assert download_requested is False


@pytest.mark.anyio
async def test_streamed_payload_is_bounded_without_content_length(monkeypatch):
    monkeypatch.setattr(whatsapp_media, "MAX_IMAGE_UPLOAD_BYTES", 8)

    def handler(request):
        if request.url.host == "graph.facebook.com":
            return httpx.Response(
                200,
                json={
                    "url": "https://lookaside.fbsbx.com/media",
                    "mime_type": "image/png",
                },
            )
        return httpx.Response(
            200, content=b"123456789", headers={"content-type": "image/png"}
        )

    client = _client(handler)
    async with client:
        with pytest.raises(WhatsAppMediaError) as exc:
            await download_whatsapp_image(
                "123", access_token="test-whatsapp-token", client=client
            )
    assert exc.value.status_code == 413


@pytest.mark.anyio
async def test_non_image_media_is_rejected():
    client = _client(_success_handler(b"document", mime_type="application/pdf"))
    async with client:
        with pytest.raises(WhatsAppMediaError) as exc:
            await download_whatsapp_image(
                "123", access_token="test-whatsapp-token", client=client
            )
    assert exc.value.status_code == 415


@pytest.mark.anyio
async def test_malformed_metadata_is_rejected():
    client = _client(lambda request: httpx.Response(200, json={"mime_type": "image/png"}))
    async with client:
        with pytest.raises(WhatsAppMediaError) as exc:
            await download_whatsapp_image(
                "123", access_token="test-whatsapp-token", client=client
            )
    assert exc.value.status_code == 502
    assert str(exc.value) == "WhatsApp returned an invalid media response."


@pytest.mark.anyio
async def test_untrusted_media_url_is_rejected_without_requesting_it():
    requests = []

    def handler(request):
        requests.append(str(request.url))
        return httpx.Response(
            200,
            json={
                "url": "https://attacker.example/receipt",
                "mime_type": "image/png",
                "file_size": 4,
            },
        )

    client = _client(handler)
    async with client:
        with pytest.raises(WhatsAppMediaError) as exc:
            await download_whatsapp_image(
                "123", access_token="test-whatsapp-token", client=client
            )

    assert exc.value.status_code == 502
    assert len(requests) == 1


@pytest.mark.anyio
async def test_corrupt_download_is_rejected_by_image_sanitizer():
    client = _client(_success_handler(b"not-an-image"))
    async with client:
        with pytest.raises(WhatsAppMediaError) as exc:
            await download_whatsapp_image(
                "123", access_token="test-whatsapp-token", client=client
            )
    assert exc.value.status_code == 400
    assert str(exc.value) == "Uploaded file is not a valid, complete JPEG or PNG image."


def test_webhook_accepts_media_id_and_preserves_api_middleware(monkeypatch):
    observed = {}

    async def fake_download(media_id):
        observed["media_id"] = media_id
        return Image.new("RGB", (20, 30), "white")

    monkeypatch.setattr("api.routes.webhook_whatsapp.download_whatsapp_image", fake_download)
    client = TestClient(app, headers={"X-API-Key": "test-pro-key"})
    response = client.post(
        "/api/v1/webhook/whatsapp",
        json={"from_phone": "+94770000000", "media_id": "987654321"},
        headers={"X-Request-ID": "whatsapp-media-test"},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "whatsapp-media-test"
    assert observed == {"media_id": "987654321"}
    assert response.json()["recipient"] == "+94770000000"


def test_webhook_requires_exactly_one_image_source():
    client = TestClient(app, headers={"X-API-Key": "test-pro-key"})
    response = client.post(
        "/api/v1/webhook/whatsapp", json={"from_phone": "+94770000000"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Provide exactly one of image_base64 or media_id."
