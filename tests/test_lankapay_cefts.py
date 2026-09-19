"""
Unit tests for LankaPay CEFTS ISO 8583 settlement bridge and reconciliation (#116).
"""

from fastapi.testclient import TestClient
from api.main import app
from core.integrations.lankapay_cefts import (
    ISO8583Packet,
    MockLankaPayCEFTSSwitch,
    LankaPayCEFTSBridge,
)


def test_iso8583_pack_and_unpack():
    """Verify ISO 8583 serialization and deserialization."""
    packet = ISO8583Packet(mti="0200")
    packet.set_field(3, "400000")
    packet.set_field(4, "000002500000")  # 25,000.00
    packet.set_field(37, "TXN1002938475")
    packet.set_field(49, "144")

    raw = packet.pack()
    assert "MTI=0200" in raw
    assert "003=400000" in raw
    assert "037=TXN1002938475" in raw

    unpacked = ISO8583Packet.unpack(raw)
    assert unpacked.mti == "0200"
    assert unpacked.get_field(3) == "400000"
    assert unpacked.get_field(4) == "000002500000"
    assert unpacked.get_field(37) == "TXN1002938475"


def test_cefts_settlement_reconciliation_success():
    """Verify successful settlement lookup for known settled transaction."""
    bridge = LankaPayCEFTSBridge()
    res = bridge.reconcile_slip_with_clearing(
        reference_no="TXN1002938475",
        slip_amount=25000.00
    )
    assert res["is_settled"] is True
    assert res["response_code"] == "00"
    assert res["settled_amount"] == 25000.00
    assert res["approval_code"] == "AP8821"


def test_cefts_settlement_amount_mismatch():
    """Detect when slip amount does not match switch settled amount."""
    bridge = LankaPayCEFTSBridge()
    # Slip claims 80,000 but switch only cleared 25,000
    res = bridge.reconcile_slip_with_clearing(
        reference_no="TXN1002938475",
        slip_amount=80000.00
    )
    assert res["is_settled"] is False
    assert res["is_amount_mismatch"] is True
    assert res["response_code"] == "64"
    assert res["settled_amount"] == 25000.00


def test_cefts_transaction_not_found():
    """Flag fake or completely forged transaction references."""
    bridge = LankaPayCEFTSBridge()
    res = bridge.reconcile_slip_with_clearing(
        reference_no="FAKE_TXN_9999999999",
        slip_amount=50000.00
    )
    assert res["is_settled"] is False
    assert res["response_code"] == "76"


def test_cefts_api_endpoint():
    """Test HTTP POST /api/v1/clearing/cefts/query endpoint."""
    client = TestClient(app, headers={"X-API-Key": "test-pro-key"})
    resp = client.post(
        "/api/v1/clearing/cefts/query",
        json={"reference_no": "TXN1002938475", "slip_amount": 25000.0}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["is_settled"] is True
    assert data["clearing_gateway"] == "LankaPay CEFTS"
