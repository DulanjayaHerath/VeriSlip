import hashlib

from core.security.merkle_audit import MerkleAuditLedger


def _slip_hash(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()


def test_append_generates_verifiable_proof_for_odd_tree():
    ledger = MerkleAuditLedger()
    receipts = [
        ledger.append(
            slip_sha256=_slip_hash(str(i)),
            timestamp=f"2026-01-01T00:00:0{i}Z",
            layer_scores={"layer1": i / 10},
            verdict="AUTHENTIC",
            bounding_boxes=[],
        )
        for i in range(3)
    ]

    assert ledger.size == 3
    assert ledger.root == receipts[-1].root
    assert all(MerkleAuditLedger.verify_proof(receipt) for receipt in receipts)


def test_tampering_with_entry_or_proof_is_rejected():
    ledger = MerkleAuditLedger()
    receipt = ledger.append(
        slip_sha256=_slip_hash("slip"),
        timestamp="2026-01-01T00:00:00Z",
        layer_scores={"layer1": 0.2, "layer4": 0.9},
        verdict="HIGH_RISK_TAMPERED",
        bounding_boxes=[{"box": [1, 2, 3, 4]}],
        merchant_signature="merchant-signature",
    )

    tampered_entry = receipt.to_dict()
    tampered_entry["entry"]["verdict"] = "AUTHENTIC"
    assert not MerkleAuditLedger.verify_proof(tampered_entry)

    tampered_proof = receipt.to_dict()
    tampered_proof["root"] = "0" * 64
    assert not MerkleAuditLedger.verify_proof(tampered_proof)


def test_invalid_slip_hash_cannot_be_added():
    ledger = MerkleAuditLedger()

    try:
        ledger.append(
            slip_sha256="not-a-sha256",
            timestamp="2026-01-01T00:00:00Z",
            layer_scores={},
            verdict="AUTHENTIC",
        )
    except ValueError as exc:
        assert "64-character" in str(exc)
    else:
        raise AssertionError("invalid SHA-256 digest was accepted")
