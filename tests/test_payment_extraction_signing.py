import hashlib
import hmac
import io

import pytest
from PIL import Image
from fastapi.testclient import TestClient
from api.main import app
from api.routes import verify
from core.forensics.ocr_extractor import ReceiptFieldExtractor
from core.notifications.webhook_dispatcher import WebhookDispatcher


@pytest.mark.parametrize("secret", ["", " ", "verislip_default_webhook_secret"])
def test_signing_requires_secret(monkeypatch, secret):
    monkeypatch.setenv("VERISLIP_WEBHOOK_SECRET", secret)
    with pytest.raises(RuntimeError, match="not configured"):
        WebhookDispatcher().generate_signature(b"test")


def test_configured_signature(monkeypatch):
    monkeypatch.setenv("VERISLIP_WEBHOOK_SECRET", "random-test-secret")
    assert (
        WebhookDispatcher().generate_signature(b"test")
        == hmac.new(b"random-test-secret", b"test", hashlib.sha256).hexdigest()
    )


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Amount: LKR 12,500.00", 12500),
        ("Transfer Amount 10000.50 LKR", 10000.5),
        ("Amount Rs. 500.00", 500),
        ("Balance 10000.00", None),
        ("Reference 123456789", None),
        ("Amount USD 100.00", None),
        ("Amount -100.00", None),
        ("Amount 1,00.00", None),
        ("Amount 100.001", None),
        ("Amount 0.00", None),
    ],
)
def test_amount_parser(text, expected):
    assert (
        ReceiptFieldExtractor.extract_amount([{"text": text, "confidence": 0.99}])
        == expected
    )


def test_conflicting_or_uncertain_amounts():
    tokens = [
        {"text": "Amount 100.00", "confidence": 0.99, "y": 0, "h": 10},
        {"text": "Amount 200.00", "confidence": 0.99, "y": 40, "h": 10},
    ]
    assert ReceiptFieldExtractor.extract_amount(tokens) is None
    tokens[0]["confidence"] = 0.3
    assert ReceiptFieldExtractor.extract_amount(tokens[:1]) is None


@pytest.mark.parametrize("amount,paid", [("10,000.00", True), ("100.00", False)])
def test_real_extraction_reaches_merchant_decision(monkeypatch, amount, paid):
    # Stub OCR recognition and forensic scoring, not structured amount extraction.
    monkeypatch.setattr(
        verify.field_extractor,
        "extract_ocr_tokens",
        lambda image: [
            {"text": "Amount", "confidence": 0.99, "x": 0, "y": 20, "h": 10},
            {"text": "LKR", "confidence": 0.99, "x": 60, "y": 20, "h": 10},
            {"text": amount, "confidence": 0.99, "x": 100, "y": 20, "h": 10},
        ],
    )
    monkeypatch.setattr(
        verify.engine,
        "analyze",
        lambda **kwargs: {
            "verdict": "AUTHENTIC",
            "tamper_risk_percentage": 5,
            "findings_summary": [],
            "flagged_regions": [],
        },
    )
    output = io.BytesIO()
    Image.new("RGB", (100, 150), "white").save(output, format="PNG")
    response = TestClient(app).post(
        "/api/v1/integrations/woocommerce/verify",
        headers={"X-API-Key": "test-pro-key"},
        files={"file": ("receipt.png", output.getvalue(), "image/png")},
        data={"order_id": "1", "order_amount_lkr": "10000"},
    )
    assert response.status_code == 200
    assert response.json()["webhook_response"]["set_paid"] is paid


def test_tesseract_tokens_feed_amount_parser(monkeypatch):
    from types import SimpleNamespace
    import core.forensics.ocr_extractor as module

    extractor = ReceiptFieldExtractor()
    extractor.has_native_ocr = False
    monkeypatch.setattr(module.shutil, "which", lambda name: "tesseract")
    tsv = (
        "level\tleft\ttop\twidth\theight\tconf\ttext\n"
        "5\t0\t10\t50\t10\t99\tAmount\n"
        "5\t60\t10\t50\t10\t99\t500.00\n"
    )

    def run(command, **kwargs):
        assert command[1:3] == ["stdin", "stdout"]
        assert kwargs["input"].startswith(b"\x89PNG")
        return SimpleNamespace(returncode=0, stdout=tsv.encode())

    monkeypatch.setattr(module.subprocess, "run", run)
    fields = extractor.extract_fields(Image.new("RGB", (100, 150), "white"))
    assert fields["amount"] == 500
