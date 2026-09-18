"""Integration tests for WhatsApp seller onboarding and conversation commands."""

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from api.main import app
from core.integrations.whatsapp_conversation import conversation_store
from core.integrations.whatsapp_media import WhatsAppMediaError


@pytest.fixture(autouse=True)
def clear_conversation_state():
    conversation_store.clear()
    yield
    conversation_store.clear()


@pytest.fixture
def client():
    return TestClient(app, headers={"X-API-Key": "test-pro-key"})


def _message(client, phone, text, message_id=None):
    payload = {"from_phone": phone, "text": text}
    if message_id:
        payload["message_id"] = message_id
    return client.post("/api/v1/webhook/whatsapp", json=payload)


def test_new_user_receives_english_onboarding(client):
    response = _message(client, "+94770000001", "hello", "wamid.new-en")

    assert response.status_code == 200
    body = response.json()
    assert "Welcome to VeriSlip" in body["reply_text"]
    assert body["conversation_state"] == "ready"
    assert body["language"] == "en"
    assert body["duplicate"] is False
    assert body["verdict"] is None


def test_returning_user_gets_command_instead_of_onboarding(client):
    phone = "+94770000002"
    assert _message(client, phone, "hello").status_code == 200

    response = _message(client, phone, "help")

    assert response.status_code == 200
    assert response.json()["reply_text"].startswith("VeriSlip help:")


def test_help_command(client):
    phone = "+94770000003"
    _message(client, phone, "start")
    response = _message(client, phone, "/help")

    assert "Send a JPEG/PNG slip" in response.json()["reply_text"]
    assert "balance" in response.json()["reply_text"]


def test_balance_uses_current_authenticated_quota(client):
    phone = "+94770000004"
    _message(client, phone, "start")
    response = _message(client, phone, "balance")

    assert response.status_code == 200
    remaining = response.headers["X-RateLimit-Remaining"]
    assert response.json()["reply_text"] == (
        "Plan: pro. Requests remaining in the current window: "
        f"{remaining}/100."
    )


def test_first_message_balance_includes_onboarding_and_current_quota(client):
    response = _message(client, "+94770000040", "balance")

    assert response.status_code == 200
    assert "Welcome to VeriSlip" in response.json()["reply_text"]
    assert f"{response.headers['X-RateLimit-Remaining']}/100" in response.json()[
        "reply_text"
    ]


def test_unknown_command_is_handled_gracefully(client):
    phone = "+94770000005"
    _message(client, phone, "hello")

    response = _message(client, phone, "launch rockets")

    assert response.status_code == 200
    assert "did not understand" in response.json()["reply_text"]


@pytest.mark.parametrize(
    ("selection", "command", "language", "expected"),
    [
        ("English", "help", "en", "VeriSlip help"),
        ("සිංහල", "උදව්", "si", "VeriSlip උදව්"),
        ("தமிழ்", "உதவி", "ta", "VeriSlip உதவி"),
    ],
)
def test_supported_language_flows(client, selection, command, language, expected):
    phone = f"seller-{language}"
    onboarding = _message(client, phone, selection)
    response = _message(client, phone, command)

    assert onboarding.status_code == 200
    assert onboarding.json()["language"] == language
    assert response.status_code == 200
    assert response.json()["language"] == language
    assert expected in response.json()["reply_text"]


def test_duplicate_message_id_returns_idempotent_reply(client):
    payload = {
        "from_phone": "+94770000006",
        "text": "hello",
        "message_id": "wamid.duplicate-1",
    }
    first = client.post("/api/v1/webhook/whatsapp", json=payload)
    duplicate = client.post("/api/v1/webhook/whatsapp", json=payload)

    assert first.status_code == duplicate.status_code == 200
    assert first.json()["reply_text"] == duplicate.json()["reply_text"]
    assert first.json()["duplicate"] is False
    assert duplicate.json()["duplicate"] is True


@pytest.mark.parametrize(
    "payload",
    [
        {"from_phone": "+94770000007"},
        {"from_phone": "+94770000007", "text": "   "},
        {
            "from_phone": "+94770000007",
            "text": "help",
            "media_id": "12345",
        },
        {"from_phone": "x", "text": "help"},
    ],
)
def test_malformed_payload_is_rejected_without_crashing(client, payload):
    response = client.post("/api/v1/webhook/whatsapp", json=payload)

    assert response.status_code in {400, 422}
    assert "traceback" not in response.text.lower()


def test_selected_language_is_preserved_for_secure_media_flow(client, monkeypatch):
    phone = "+94770000008"
    _message(client, phone, "සිංහල")
    observed = {}

    async def fake_download(media_id):
        observed["media_id"] = media_id
        return Image.new("RGB", (80, 120), "white")

    monkeypatch.setattr("api.routes.webhook_whatsapp.download_whatsapp_image", fake_download)
    response = client.post(
        "/api/v1/webhook/whatsapp",
        json={"from_phone": phone, "media_id": "123456789"},
    )

    assert response.status_code == 200
    assert response.json()["verdict"] is not None
    assert response.json()["language"] == "si"
    assert observed == {"media_id": "123456789"}


def test_media_service_failure_remains_safe(client, monkeypatch):
    async def failed_download(media_id):
        raise WhatsAppMediaError("WhatsApp media service is unavailable.", 502)

    monkeypatch.setattr(
        "api.routes.webhook_whatsapp.download_whatsapp_image", failed_download
    )
    response = client.post(
        "/api/v1/webhook/whatsapp",
        json={"from_phone": "+94770000009", "media_id": "123456789"},
    )

    assert response.status_code == 502
    assert response.json() == {"detail": "WhatsApp media service is unavailable."}
    assert "traceback" not in response.text.lower()
