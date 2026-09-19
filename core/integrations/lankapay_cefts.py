"""
LankaPay CEFTS ISO 8583 / ISO 20022 Clearing Settlement Bridge (#116).
Enables real-time interbank transaction settlement reconciliation against the national clearing switch.
"""

from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import time


class ISO8583Packet:
    """Standard ISO 8583 Financial Transaction Message packet."""

    def __init__(self, mti: str = "0200"):
        self.mti = mti  # Message Type Identifier (0200=Request, 0210=Response)
        self.fields: Dict[int, str] = {}

    def set_field(self, de_num: int, value: Any):
        self.fields[de_num] = str(value)

    def get_field(self, de_num: int, default: Optional[str] = None) -> Optional[str]:
        return self.fields.get(de_num, default)

    def pack(self) -> str:
        """Serialize packet to a standard string representation."""
        field_strs = [f"{k:03d}={v}" for k, v in sorted(self.fields.items())]
        return f"MTI={self.mti}|" + "|".join(field_strs)

    @classmethod
    def unpack(cls, raw_msg: str) -> "ISO8583Packet":
        """Deserialize packet from string representation."""
        packet = cls()
        tokens = raw_msg.split("|")
        for tok in tokens:
            if tok.startswith("MTI="):
                packet.mti = tok[4:]
            elif "=" in tok:
                k, v = tok.split("=", 1)
                try:
                    packet.fields[int(k)] = v
                except ValueError:
                    pass
        return packet


class MockLankaPayCEFTSSwitch:
    """
    Mock sandbox clearing switch simulating LankaPay CEFTS national switch responses.
    Maintains a simulated ledger of settled interbank transactions.
    """

    def __init__(self):
        # Seed settled transactions (RRN -> details)
        self.ledger: Dict[str, Dict[str, Any]] = {
            "TXN1002938475": {
                "amount": 25000.00,
                "bank_sender": "COMBANK",
                "bank_receiver": "HNB",
                "account_sender": "8001020304",
                "account_receiver": "1002030405",
                "status": "SETTLED",
                "approval_code": "AP8821"
            },
            "TXN5599220011": {
                "amount": 150000.00,
                "bank_sender": "SAMPATH",
                "bank_receiver": "BOC",
                "account_sender": "1020304050",
                "account_receiver": "9080706050",
                "status": "SETTLED",
                "approval_code": "AP4412"
            }
        }

    def register_settled_transaction(self, rrn: str, amount: float, **kwargs):
        """Register a settled interbank transaction in the mock clearing ledger."""
        self.ledger[rrn.strip().upper()] = {
            "amount": amount,
            "status": "SETTLED",
            "approval_code": f"AP{int(time.time()) % 10000:04d}",
            **kwargs
        }

    def process_iso8583_request(self, request_packet: ISO8583Packet) -> ISO8583Packet:
        """Simulate LankaPay switch receiving 0200 and generating 0210 response."""
        response = ISO8583Packet(mti="0210")
        # Echo back key trace identifiers
        rrn = request_packet.get_field(37, "").strip().upper()
        response.set_field(37, rrn)
        response.set_field(11, request_packet.get_field(11, "123456"))  # STAN
        response.set_field(49, "144")  # LKR

        req_amount_str = request_packet.get_field(4)
        req_amount = float(req_amount_str) / 100.0 if req_amount_str else None

        if rrn not in self.ledger:
            # DE 39 = 76: Transaction Not Found on CEFTS Switch
            response.set_field(39, "76")
            response.set_field(44, "TRANSACTION_NOT_FOUND_ON_SWITCH")
            return response

        record = self.ledger[rrn]
        settled_amount = record["amount"]
        response.set_field(4, f"{int(settled_amount * 100):012d}")

        if req_amount is not None and abs(req_amount - settled_amount) > 0.01:
            # DE 39 = 64: Settlement Amount Mismatch
            response.set_field(39, "64")
            response.set_field(44, f"SETTLEMENT_AMOUNT_MISMATCH_SETTLED_{settled_amount:.2f}")
            return response

        # DE 39 = 00: Approved / Settled
        response.set_field(39, "00")
        response.set_field(38, record.get("approval_code", "AP9999"))
        response.set_field(44, "CEFTS_INTERBANK_SETTLED_CONFIRMED")
        response.set_field(102, record.get("account_sender", ""))
        response.set_field(103, record.get("account_receiver", ""))
        return response


class LankaPayCEFTSBridge:
    """Fintech Bridge to LankaPay CEFTS interbank settlement network (#116)."""

    def __init__(self, switch: Optional[MockLankaPayCEFTSSwitch] = None):
        self.switch = switch or MockLankaPayCEFTSSwitch()

    def reconcile_slip_with_clearing(
        self,
        reference_no: str,
        slip_amount: Optional[float] = None,
        transaction_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query national clearing switch to verify whether the slip's reference number
        corresponds to a genuine, settled interbank fund transfer.
        """
        if not reference_no or len(reference_no.strip()) == 0:
            return {
                "settled": False,
                "reconciled": False,
                "error": "No reference number provided for clearing query."
            }

        # Build ISO 8583-0200 Request
        req = ISO8583Packet(mti="0200")
        req.set_field(3, "400000")  # CEFTS Interbank Transfer Inquiry
        req.set_field(37, reference_no.strip().upper())
        req.set_field(11, f"{int(time.time()) % 1000000:06d}")
        req.set_field(49, "144")

        if slip_amount is not None:
            req.set_field(4, f"{int(slip_amount * 100):012d}")

        # Send to switch
        resp = self.switch.process_iso8583_request(req)
        resp_code = resp.get_field(39, "96")
        clearing_note = resp.get_field(44, "")
        approval_code = resp.get_field(38)

        settled_amt_raw = resp.get_field(4)
        settled_amount = float(settled_amt_raw) / 100.0 if settled_amt_raw else None

        is_settled = (resp_code == "00")
        is_amount_mismatch = (resp_code == "64")

        return {
            "reference_no": reference_no,
            "response_code": resp_code,
            "is_settled": is_settled,
            "is_amount_mismatch": is_amount_mismatch,
            "approval_code": approval_code,
            "clearing_note": clearing_note,
            "settled_amount": settled_amount,
            "slip_amount": slip_amount,
            "iso8583_mti": resp.mti
        }
