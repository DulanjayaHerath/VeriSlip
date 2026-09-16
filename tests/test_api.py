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
    assert "VeriSlip" in data["reply_text"]
