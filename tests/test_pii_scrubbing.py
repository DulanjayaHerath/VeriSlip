"""Unit tests for automated PII scrubbing on request logs and verification records."""

import io
import json
import logging

from core.history.verification_history import InMemoryVerificationHistoryStore
from core.observability.logging import (
    JsonLogFormatter,
    hash_bank_account,
    scrub_pii,
)


def test_hash_bank_account_deterministic_and_irreversible():
    acc1 = "100028472910"
    acc2 = "1000-2847-2910"
    hash1 = hash_bank_account(acc1)
    hash2 = hash_bank_account(acc2)
    assert len(hash1) == 16
    assert hash1 == hash2
    assert "100028472910" not in hash1


def test_scrub_pii_masks_emails_and_phones():
    text = "Alert for customer user.name@domain.com with phone +94 77 123 4567 or 0712345678"
    scrubbed = scrub_pii(text)
    assert "user.name@domain.com" not in scrubbed
    assert "+94 77 123 4567" not in scrubbed
    assert "0712345678" not in scrubbed
    assert "[REDACTED_EMAIL]" in scrubbed
    assert "[REDACTED_PHONE]" in scrubbed


def test_scrub_pii_hashes_bank_accounts():
    raw_acc = "801234567890"
    text = f"Payment transferred from account {raw_acc} successfully"
    scrubbed = scrub_pii(text)
    assert raw_acc not in scrubbed
    assert "[ACCOUNT:sha256:" in scrubbed


def test_scrub_pii_redacts_named_customer_fields():
    text = 'Processing transaction for customer="Ruwan Silva" and beneficiary="Perera Brothers"'
    scrubbed = scrub_pii(text)
    assert "Ruwan Silva" not in scrubbed
    assert "Perera Brothers" not in scrubbed
    assert "[REDACTED_NAME]" in scrubbed


def test_json_log_formatter_scrubs_pii_in_event_and_extras():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonLogFormatter())
    logger = logging.getLogger("verislip.test_pii")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    try:
        logger.info(
            "Deposit to account 123456789012 from john.doe@bank.lk",
            extra={"method": "POST", "path": "/api/v1/verify?acc=987654321098"},
        )
        output = stream.getvalue()
        log_entry = json.loads(output.strip())

        assert "123456789012" not in log_entry["event"]
        assert "john.doe@bank.lk" not in log_entry["event"]
        assert "[ACCOUNT:sha256:" in log_entry["event"]
        assert "[REDACTED_EMAIL]" in log_entry["event"]
        assert "987654321098" not in log_entry["path"]
        assert "[ACCOUNT:sha256:" in log_entry["path"]
    finally:
        logger.removeHandler(handler)


def test_verification_history_scrubs_account_number_in_reference():
    store = InMemoryVerificationHistoryStore()
    record = store.add(
        owner_key_id="merchant_123",
        reference_no="ACC-829102948210-REF",
        verdict="AUTHENTIC",
        tamper_risk_percentage=4.5,
    )
    assert "829102948210" not in (record.reference_no or "")
    assert "[ACCOUNT:sha256:" in (record.reference_no or "")
