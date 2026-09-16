"""
Integration tests for FastAPI endpoints.
"""

from fastapi.testclient import TestClient
from api.main import app
import io
from PIL import Image

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "COMBANK" in data["supported_banks"]

def test_synthetic_sample_endpoint():
    res = client.get("/api/v1/forensics/synthetic-sample?bank_code=COMBANK&tampered=false")
    assert res.status_code == 200
    data = res.json()
    assert data["bank_code"] == "COMBANK"
    assert data["is_tampered"] is False
    assert data["image_base64"].startswith("data:image/png;base64,")

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

def test_whatsapp_webhook():
    img = Image.new("RGB", (200, 400), color=(250, 250, 250))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    import base64
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
