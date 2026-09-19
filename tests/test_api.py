"""
Integration tests for FastAPI endpoints.
"""

from fastapi.testclient import TestClient
from api.main import app
import io
from PIL import Image
import base64

client = TestClient(app, headers={"X-API-Key": "test-pro-key"})

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "COMBANK" in data["supported_banks"]

def test_synthetic_sample_is_not_exposed():
    res = client.get("/api/v1/forensics/synthetic-sample")

    assert res.status_code == 404
    assert "/api/v1/forensics/synthetic-sample" not in app.openapi()["paths"]

def test_verify_endpoint():
    # Generate dummy image
    img = Image.new("RGB", (300, 500), color=(240, 240, 240))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    files = {"file": ("slip.jpg", buf, "image/jpeg")}
    data = {"bank_code": "COMBANK", "reference_no": "TXN1098234812"}

    res = client.post("/api/v1/verify", files=files, data=data)
    assert res.status_code == 200
    payload = res.json()
    assert "verdict" in payload
    assert "tamper_risk_percentage" in payload
    assert "layer_breakdowns" in payload

def test_verify_uses_image_content_not_filename_or_mime_type():
    img = Image.new("RGB", (120, 180), color=(240, 240, 240))
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    res = client.post(
        "/api/v1/verify",
        files={"file": ("receipt.txt", buf.getvalue(), "text/plain")},
    )

    assert res.status_code == 200

def test_verify_rejects_malformed_image_without_internal_details():
    res = client.post(
        "/api/v1/verify",
        files={"file": ("receipt.jpg", b"not-an-image", "image/jpeg")},
    )

    assert res.status_code == 400
    assert res.json()["detail"] == "Uploaded file is not a valid, complete JPEG or PNG image."

def test_verify_rejects_unsupported_image_content():
    img = Image.new("RGB", (20, 20), color="white")
    buf = io.BytesIO()
    img.save(buf, format="GIF")

    res = client.post(
        "/api/v1/verify",
        files={"file": ("receipt.png", buf.getvalue(), "image/png")},
    )

    assert res.status_code == 415

def test_verify_rejects_oversized_upload(monkeypatch):
    monkeypatch.setattr("api.routes.verify.MAX_IMAGE_UPLOAD_BYTES", 8)

    res = client.post(
        "/api/v1/verify",
        files={"file": ("receipt.jpg", b"123456789", "image/jpeg")},
    )

    assert res.status_code == 413
    assert res.json()["detail"] == "Upload exceeds the permitted size."

def test_whatsapp_webhook():
    img = Image.new("RGB", (200, 400), color=(250, 250, 250))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")

    payload = {
        "from_phone": "+94771234567",
        "image_base64": b64_str,
        "caption": "Please verify this payment"
    }

    res = client.post("/api/v1/webhook/whatsapp", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["recipient"] == "+94771234567"
    assert "reply_text" in data

def test_whatsapp_rejects_invalid_base64_without_decoder_details():
    res = client.post(
        "/api/v1/webhook/whatsapp",
        json={"from_phone": "+94771234567", "image_base64": "%%%invalid%%%"},
    )

    assert res.status_code == 400
    assert res.json()["detail"] == "Image payload is not valid base64."

def test_whatsapp_rejects_valid_base64_with_invalid_image():
    res = client.post(
        "/api/v1/webhook/whatsapp",
        json={
            "from_phone": "+94771234567",
            "image_base64": base64.b64encode(b"not-an-image").decode("ascii"),
        },
    )

    assert res.status_code == 400
    assert res.json()["detail"] == "Uploaded file is not a valid, complete JPEG or PNG image."

def test_pdf_report_generation():
    req_data = {
        "verdict": "HIGH_RISK_TAMPERED",
        "tamper_risk_percentage": 94.5,
        "recommendation": "DO NOT DISPATCH GOODS. High likelihood of image doctoring.",
        "findings_summary": ["Localized ELA discrepancy detected", "Spatial noise floor discontinuity"],
        "layer_breakdowns": {
            "layer1_structural": {"score": 0.2, "findings": ["Valid aspect ratio"]},
            "layer2_classical": {"score": 0.88, "findings": ["ELA variance spike"]},
            "layer3_noise": {"score": 0.75, "findings": ["Noise discontinuity"]},
            "layer4_ensemble": {"score": 0.92, "tamper_probability": 0.94}
        },
        "flagged_regions": [{"box": [120, 240, 180, 50], "confidence": 0.92, "label": "Tampered Amount"}],
        "bank_name": "Commercial Bank of Ceylon",
        "reference_no": "TXN99281726"
    }
    res = client.post("/api/v1/report/audit-pdf", json=req_data)
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert len(res.content) > 1000


def test_pdf_report_with_pades_signature_and_tamper_detection():
    from core.security.pdf_signer import generate_self_signed_certificate, sign_pdf_document, verify_pdf_document

    cert_pem, key_pem = generate_self_signed_certificate("VeriSlip Test Authority")
    payload = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
    signed = sign_pdf_document(payload, cert_pem=cert_pem, private_key_pem=key_pem)

    assert b"VERISLIP-PADES-SIGNATURE" in signed
    assert verify_pdf_document(signed, cert_pem)
    assert not verify_pdf_document(signed + b"\nmodified", cert_pem)

    res = client.post(
        "/api/v1/report/audit-pdf",
        json={
            "verdict": "AUTHENTIC",
            "tamper_risk_percentage": 4.2,
            "recommendation": "Proceed with merchant verification.",
            "findings_summary": ["No significant anomaly detected"],
            "layer_breakdowns": {"layer1_structural": {"score": 0.06, "findings": ["Normal"]}},
            "sign_pdf": True,
            "signature_reason": "Test legal certificate",
            "signing_certificate_pem": cert_pem,
            "signing_private_key_pem": key_pem,
        },
    )
    assert res.status_code == 200
    assert b"VERISLIP-PADES-SIGNATURE" in res.content


def test_pdf_report_requires_signing_keys_when_signing_is_requested():
    req_data = {
        "verdict": "AUTHENTIC",
        "tamper_risk_percentage": 0.5,
        "recommendation": "Proceed.",
        "sign_pdf": True,
    }
    res = client.post("/api/v1/report/audit-pdf", json=req_data)
    assert res.status_code == 400
    assert "certificate and private key" in res.json()["detail"]


def test_batch_verify_endpoint():
    img1 = Image.new("RGB", (200, 350), color=(255, 255, 255))
    buf1 = io.BytesIO()
    img1.save(buf1, format="JPEG")
    buf1.seek(0)

    img2 = Image.new("RGB", (200, 350), color=(240, 240, 240))
    buf2 = io.BytesIO()
    img2.save(buf2, format="JPEG")
    buf2.seek(0)

    files = [
        ("files", ("slip1.jpg", buf1, "image/jpeg")),
        ("files", ("slip2.jpg", buf2, "image/jpeg"))
    ]

    res = client.post("/api/v1/batch-verify", files=files)
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    assert data["summary"]["total_processed"] == 2
    assert len(data["items"]) == 2

def test_batch_verify_rejects_invalid_item_without_leaking_details():
    files = [("files", ("bad.jpg", b"not-an-image", "image/jpeg"))]

    res = client.post("/api/v1/batch-verify", files=files)

    assert res.status_code == 200
    item = res.json()["items"][0]
    assert item["verdict"] == "ERROR"
    assert item["recommendation"] == "File was rejected because it is invalid or unsafe."

def test_verify_pdf_slip_endpoint():
    from reportlab.pdfgen import canvas
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    c.drawString(100, 750, "Bank of Ceylon Fund Transfer")
    c.drawString(100, 700, "Amount : LKR 50,000.00")
    c.save()
    buf.seek(0)

    files = {"file": ("bank_slip.pdf", buf, "application/pdf")}
    res = client.post("/api/v1/verify", files=files, data={"bank_code": "BOC"})
    assert res.status_code == 200
    data = res.json()
    assert "verdict" in data
    assert "tamper_risk_percentage" in data


def test_woocommerce_verification():
    img = Image.new("RGB", (200, 400), color=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    files = {"file": ("slip.png", buf, "image/png")}
    data = {"order_id": "#WC-9901", "order_amount_lkr": 25000.0}

    res = client.post("/api/v1/integrations/woocommerce/verify", files=files, data=data)
    assert res.status_code == 200
    res_data = res.json()
    assert res_data["order_id"] == "#WC-9901"
    assert "recommended_order_action" in res_data
    assert "new_order_status" in res_data
    assert "webhook_response" in res_data


def test_analytics_overview():
    res = client.get("/api/v1/analytics/overview")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "operational"
    assert "kpi_metrics" in data
    assert "bank_distribution" in data
    assert "top_tampering_techniques" in data


def test_syndicate_risk_endpoint_detects_ring():
    res = client.get("/api/v1/analytics/syndicate-risk")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "operational"
    assert data["risk_level"] in {"HIGH", "CRITICAL"}
    assert data["cluster_count"] >= 1
    assert data["syndicate_risk_index"] > 0.5
    assert data["graph_summary"]["merchant_count"] >= 5


def test_syndicate_graph_builder_detects_shared_fraud_ring():
    from core.analytics.syndicate_graph import SyndicateGraphBuilder

    graph = SyndicateGraphBuilder().build_synthetic_ring(merchant_count=5)
    clusters = graph.find_clusters(min_cluster_size=2)

    assert len(clusters) >= 1
    assert clusters[0].shared_account_count >= 1
    assert clusters[0].shared_hash_count >= 1
    assert clusters[0].cluster_score > 0.5
    assert graph.compute_syndicate_risk(min_cluster_size=2) > 0.5


def test_courier_verify_endpoint():
    img = Image.new("RGB", (300, 600), color=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    b64_str = base64.b64encode(buf.getvalue()).decode("ascii")

    payload = {
        "waybill_id": "WB-882910",
        "expected_cod_amount": 12500.0,
        "slip_base64": b64_str,
        "target_bank": "COMBANK"
    }

    res = client.post("/api/v1/courier/verify", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["waybill_id"] == "WB-882910"
    assert "can_handover_package" in data
    assert "rider_action" in data
    assert "risk_level" in data
    assert "risk_percentage" in data


def test_webhook_dispatcher_hmac_signature():
    from core.notifications.webhook_dispatcher import WebhookDispatcher
    dispatcher = WebhookDispatcher(secret_key="test_secret_123")
    payload = dispatcher.build_event_payload("order.verified", {"order_id": 101, "risk": 0.05})
    assert payload["event"] == "order.verified"
    assert "event_id" in payload
    assert payload["data"]["order_id"] == 101

    sig = dispatcher.generate_signature(b'{"test": 123}')
    assert len(sig) == 64  # SHA256 hex string


def test_rate_limiter_middleware_headers():
    res = client.get("/api/v1/analytics/overview")
    assert res.status_code == 200
    assert "X-RateLimit-Limit" in res.headers
    assert "X-RateLimit-Remaining" in res.headers

