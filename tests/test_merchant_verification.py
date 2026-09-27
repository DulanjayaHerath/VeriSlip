"""Regression coverage for merchant amount checks and safe document ingestion."""

import io
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from PIL import Image, PngImagePlugin

from api.main import app
from api.routes import integrations

client = TestClient(app, headers={"X-API-Key": "test-pro-key"})


def upload(image_format="PNG"):
    buffer = io.BytesIO()
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("private-note", "must-not-reach-analysis")
    Image.new("RGB", (80, 120), "white").save(
        buffer, format=image_format, pnginfo=metadata
    )
    return buffer.getvalue()


def post(contents=None, total="10000", name="receipt.png", mime="image/png"):
    return client.post(
        "/api/v1/integrations/woocommerce/verify",
        files={"file": (name, upload() if contents is None else contents, mime)},
        data={"order_id": "WC-1", "order_amount_lkr": total},
    )


@pytest.fixture
def analyze(monkeypatch):
    result = {
        "verdict": "AUTHENTIC",
        "tamper_risk_percentage": 5.0,
        "findings_summary": [],
        "flagged_regions": [],
        "extracted_metadata": {"amount": 10000},
    }
    stub = Mock(return_value=result)
    monkeypatch.setattr(integrations, "_analyze_image", stub)
    return stub


@pytest.mark.parametrize("amount", [100, 9999.99, 10000.01])
def test_mismatched_amount_cannot_mark_order_paid(analyze, amount):
    analyze.return_value["extracted_metadata"]["amount"] = amount
    response = post()
    assert response.status_code == 200
    result = response.json()
    assert result["amount_mismatch"] is True
    assert result["new_order_status"] == "on-hold"
    assert result["webhook_response"]["set_paid"] is False


@pytest.mark.parametrize("amount", [None, "unreadable", "NaN", "Infinity", -1, 0, True])
def test_missing_or_invalid_amount_requires_review(analyze, amount):
    analyze.return_value["extracted_metadata"]["amount"] = amount
    response = post()
    assert response.status_code == 200
    result = response.json()
    assert result["detected_amount_lkr"] is None
    assert result["recommended_order_action"] == "HOLD_FOR_MANUAL_REVIEW"
    assert result["webhook_response"]["set_paid"] is False


@pytest.mark.parametrize(
    "verdict,paid",
    [("AUTHENTIC", True), ("SUSPICIOUS", False), ("HIGH_RISK_TAMPERED", False)],
)
def test_matching_amount_still_requires_authentic_verdict(analyze, verdict, paid):
    analyze.return_value["verdict"] = verdict
    result = post().json()
    assert result["webhook_response"]["set_paid"] is paid


@pytest.mark.parametrize("total", ["0", "-1", "nan", "inf", "-inf", "1000000001"])
def test_invalid_order_total_is_rejected_before_analysis(analyze, total):
    assert post(total=total).status_code == 422
    analyze.assert_not_called()


def test_upload_byte_limit_is_shared(analyze, monkeypatch):
    monkeypatch.setattr("api.routes.verify.MAX_IMAGE_UPLOAD_BYTES", 8)
    assert post().status_code == 413
    analyze.assert_not_called()


def test_image_dimensions_are_bounded(analyze, monkeypatch):
    monkeypatch.setattr("core.security.image_sanitizer.MAX_IMAGE_WIDTH", 40)
    assert post().status_code == 413
    analyze.assert_not_called()


def test_type_is_detected_from_content_and_metadata_is_removed(analyze):
    def inspect(image, *args):
        assert image.mode == "RGB"
        assert image.info == {}
        return analyze.return_value

    analyze.side_effect = inspect
    assert post(name="receipt.pdf", mime="application/octet-stream").status_code == 200


def test_unsupported_and_malformed_images_are_rejected(analyze):
    assert post(contents=upload("GIF")).status_code == 415
    response = post(contents=b"invalid")
    assert response.status_code == 400
    analyze.assert_not_called()


def test_oversized_pdf_never_reaches_renderer(analyze, monkeypatch):
    import pypdfium2 as pdfium
    from reportlab.pdfgen import canvas

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(4000, 4000))
    pdf.drawString(10, 10, "Test")
    pdf.save()
    render = Mock(side_effect=AssertionError("must reject before render"))
    monkeypatch.setattr(pdfium.PdfPage, "render", render)
    assert (
        post(buffer.getvalue(), name="receipt.txt", mime="text/plain").status_code
        == 413
    )
    render.assert_not_called()
    analyze.assert_not_called()


def test_valid_pdf_uses_shared_decoder(analyze):
    from reportlab.pdfgen import canvas

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(100, 100))
    pdf.drawString(10, 10, "Test")
    pdf.save()
    assert (
        post(buffer.getvalue(), name="receipt.txt", mime="text/plain").status_code
        == 200
    )


def test_internal_decode_and_analysis_errors_are_not_exposed(analyze, monkeypatch):
    analyze.side_effect = RuntimeError("private-server-detail")
    response = post()
    assert response.status_code == 500
    assert "private-server-detail" not in response.text
    monkeypatch.setattr(
        integrations,
        "_decode_document",
        Mock(side_effect=RuntimeError("private-file-path")),
    )
    response = post()
    assert response.status_code == 400
    assert "private-file-path" not in response.text
