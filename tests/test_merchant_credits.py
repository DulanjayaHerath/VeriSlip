"""Merchant verification-credit unit and WhatsApp integration tests."""

import base64
import io
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient
from PIL import Image

import api.routes.webhook_whatsapp as whatsapp_route
from api.main import app
from core.integrations.merchant_credits import (
    InMemoryMerchantCreditStore,
    MerchantCreditPolicy,
    MerchantCreditService,
    ReservationStatus,
)
from core.integrations.whatsapp_conversation import conversation_store


UPGRADE_URL = "https://billing.example.test/verislip/upgrade"


def _image_base64():
    buffer = io.BytesIO()
    Image.new("RGB", (80, 120), "white").save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def _analysis_result():
    return {
        "verdict": "AUTHENTIC",
        "tamper_risk_percentage": 4.0,
        "flagged_regions": [],
        "findings_summary": [],
    }


@pytest.fixture
def credit_service(monkeypatch):
    service = MerchantCreditService(
        InMemoryMerchantCreditStore(),
        MerchantCreditPolicy("free", 2, UPGRADE_URL),
    )
    monkeypatch.setattr(whatsapp_route, "merchant_credit_service", service)
    monkeypatch.setattr(whatsapp_route.engine, "analyze", lambda image: _analysis_result())
    conversation_store.clear()
    yield service
    conversation_store.clear()


@pytest.fixture
def client(credit_service):
    return TestClient(app, headers={"X-API-Key": "test-pro-key"})


def _verify(client, phone, message_id):
    return client.post(
        "/api/v1/webhook/whatsapp",
        json={
            "from_phone": phone,
            "image_base64": _image_base64(),
            "message_id": message_id,
        },
    )


def test_new_merchant_has_full_initial_balance(credit_service):
    balance = credit_service.balance("+94771111111")

    assert balance.tier == "free"
    assert balance.limit == 2
    assert balance.used == 0
    assert balance.remaining == 2


def test_successful_verification_consumes_one_credit(client, credit_service):
    response = _verify(client, "+94771111112", "wamid.success-1")

    assert response.status_code == 200
    assert "Fraud Check: SAFE" in response.json()["reply_text"]
    assert response.json()["credits_remaining"] == 1
    balance = credit_service.balance("+94771111112")
    assert balance.used == 1
    assert balance.remaining == 1


def test_help_and_onboarding_do_not_consume_credit(client, credit_service):
    phone = "+94771111113"
    onboarding = client.post(
        "/api/v1/webhook/whatsapp",
        json={"from_phone": phone, "text": "hello", "message_id": "wamid.hello"},
    )
    help_response = client.post(
        "/api/v1/webhook/whatsapp",
        json={"from_phone": phone, "text": "help", "message_id": "wamid.help"},
    )

    assert onboarding.status_code == help_response.status_code == 200
    assert credit_service.balance(phone).remaining == 2


def test_balance_command_reports_real_remaining_credits(client):
    phone = "+94771111114"
    assert _verify(client, phone, "wamid.balance-check").status_code == 200

    response = client.post(
        "/api/v1/webhook/whatsapp",
        json={"from_phone": phone, "text": "balance"},
    )

    assert response.status_code == 200
    assert "Verification credits remaining: 1/2" in response.json()["reply_text"]
    assert response.json()["credits_remaining"] == 1


def test_final_credit_and_exhausted_attempt_include_upgrade_link(
    client, credit_service
):
    credit_service.policy = MerchantCreditPolicy("free", 1, UPGRADE_URL)
    phone = "+94771111115"

    final_credit = _verify(client, phone, "wamid.final-credit")
    exhausted = _verify(client, phone, "wamid.after-limit")

    assert final_credit.status_code == 200
    assert final_credit.json()["credits_remaining"] == 0
    assert UPGRADE_URL in final_credit.json()["reply_text"]
    assert exhausted.status_code == 200
    assert exhausted.json()["verdict"] is None
    assert exhausted.json()["credits_remaining"] == 0
    assert "exhausted" in exhausted.json()["reply_text"]
    assert UPGRADE_URL in exhausted.json()["reply_text"]


def test_duplicate_media_message_does_not_double_charge(
    client, credit_service, monkeypatch
):
    calls = 0

    def analyze(image):
        nonlocal calls
        calls += 1
        return _analysis_result()

    monkeypatch.setattr(whatsapp_route.engine, "analyze", analyze)
    phone = "+94771111116"
    first = _verify(client, phone, "wamid.same-message")
    duplicate = _verify(client, phone, "wamid.same-message")

    assert first.status_code == duplicate.status_code == 200
    assert duplicate.json()["duplicate"] is True
    assert duplicate.json()["credits_remaining"] == 1
    assert calls == 1
    assert credit_service.balance(phone).used == 1


def test_merchants_have_isolated_balances(client, credit_service):
    first_phone = "+94771111117"
    second_phone = "+94771111118"
    assert _verify(client, first_phone, "wamid.first-merchant").status_code == 200

    assert credit_service.balance(first_phone).remaining == 1
    assert credit_service.balance(second_phone).remaining == 2


def test_failed_forensic_analysis_releases_reserved_credit(
    client, credit_service, monkeypatch
):
    def fail_analysis(image):
        raise RuntimeError("private forensic failure")

    monkeypatch.setattr(whatsapp_route.engine, "analyze", fail_analysis)
    phone = "+94771111119"
    response = _verify(client, phone, "wamid.failed-analysis")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error."}
    balance = credit_service.balance(phone)
    assert balance.used == 0
    assert balance.reserved == 0
    assert balance.remaining == 2
    assert "private forensic failure" not in response.text


def test_atomic_concurrent_reservations_never_exceed_limit():
    service = MerchantCreditService(
        InMemoryMerchantCreditStore(), MerchantCreditPolicy("free", 5, None)
    )

    def reserve(index):
        return service.reserve("+94771111120", f"wamid.concurrent-{index}")

    with ThreadPoolExecutor(max_workers=20) as executor:
        reservations = list(executor.map(reserve, range(40)))

    accepted = [
        reservation
        for reservation in reservations
        if reservation.status is ReservationStatus.ACCEPTED
    ]
    assert len(accepted) == 5
    assert service.balance("+94771111120").remaining == 0


def test_concurrent_duplicate_reservation_is_accepted_once():
    service = MerchantCreditService(
        InMemoryMerchantCreditStore(), MerchantCreditPolicy("free", 5, None)
    )

    with ThreadPoolExecutor(max_workers=10) as executor:
        reservations = list(
            executor.map(
                lambda _: service.reserve("+94771111121", "wamid.concurrent-same"),
                range(20),
            )
        )

    statuses = [reservation.status for reservation in reservations]
    assert statuses.count(ReservationStatus.ACCEPTED) == 1
    assert statuses.count(ReservationStatus.DUPLICATE) == 19


def test_credit_configuration_reads_safe_environment(monkeypatch):
    monkeypatch.setenv("VERISLIP_WHATSAPP_DEFAULT_TIER", "free")
    monkeypatch.setenv("VERISLIP_WHATSAPP_FREE_VERIFICATIONS", "7")
    monkeypatch.setenv("VERISLIP_WHATSAPP_UPGRADE_URL", UPGRADE_URL)

    policy = MerchantCreditPolicy.from_environment()

    assert policy == MerchantCreditPolicy("free", 7, UPGRADE_URL)


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("VERISLIP_WHATSAPP_FREE_VERIFICATIONS", "0"),
        ("VERISLIP_WHATSAPP_FREE_VERIFICATIONS", "not-a-number"),
        ("VERISLIP_WHATSAPP_UPGRADE_URL", "http://insecure.example.test/pay"),
        ("VERISLIP_WHATSAPP_UPGRADE_URL", "https://user:pass@example.test/pay"),
    ],
)
def test_invalid_credit_configuration_fails_closed(monkeypatch, name, value):
    monkeypatch.setenv("VERISLIP_WHATSAPP_FREE_VERIFICATIONS", "5")
    monkeypatch.setenv("VERISLIP_WHATSAPP_UPGRADE_URL", UPGRADE_URL)
    monkeypatch.setenv(name, value)

    with pytest.raises(RuntimeError):
        MerchantCreditPolicy.from_environment()
