"""Provider-neutral Layer 5 scaffold tests for issue #100."""

from datetime import date
import logging

import pytest

from core.integrations.transaction_verification import (
    DevelopmentMockProvider,
    MalformedProviderResponseError,
    MatchState,
    ProviderTimeoutError,
    ProviderUnavailableError,
    SyntheticTransaction,
    TransactionVerificationRequest,
    TransactionVerificationService,
    VerificationStatus,
    fingerprint_identifier,
)


REFERENCE = "SYNTHETIC-REF-100"
RECIPIENT = "SYNTHETIC-MERCHANT-001"


def _request(**updates):
    values = {
        "reference": REFERENCE,
        "amount_minor": 125_000,
        "recipient_identifier": RECIPIENT,
        "transaction_date": date(2026, 1, 15),
        "bank_code": "TESTBANK",
        "merchant_identifier": "TEST-MERCHANT",
    }
    values.update(updates)
    return TransactionVerificationRequest(**values)


def _service():
    record = SyntheticTransaction(
        reference=REFERENCE,
        amount_minor=125_000,
        recipient_fingerprint=fingerprint_identifier(RECIPIENT),
        transaction_date=date(2026, 1, 15),
        bank_code="TESTBANK",
    )
    provider = DevelopmentMockProvider(
        {REFERENCE: record}, enabled=True, supported_banks=frozenset({"TESTBANK"})
    )
    return TransactionVerificationService(provider)


def test_successful_synthetic_transaction_match():
    outcome = _service().verify(_request())
    assert outcome.direct.status is VerificationStatus.VERIFIED
    assert outcome.direct.reference_match is MatchState.MATCH
    assert outcome.direct.amount_match is MatchState.MATCH
    assert outcome.direct.recipient_match is MatchState.MATCH


@pytest.mark.parametrize(
    ("update", "field"),
    [
        ({"amount_minor": 125_001}, "amount_match"),
        ({"recipient_identifier": "SYNTHETIC-MERCHANT-002"}, "recipient_match"),
    ],
)
def test_attribute_mismatch_is_not_verified(update, field):
    result = _service().verify(_request(**update)).direct
    assert result.status is VerificationStatus.NOT_VERIFIED
    assert getattr(result, field) is MatchState.MISMATCH


def test_reference_mismatch_is_not_verified_without_echoing_reference():
    result = _service().verify(_request(reference="UNKNOWN-SYNTHETIC-REF")).direct
    assert result.status is VerificationStatus.NOT_VERIFIED
    assert result.reference_match is MatchState.MISMATCH
    assert REFERENCE not in repr(result)


def test_unsupported_bank_is_distinct_from_fraud():
    outcome = _service().verify(_request(bank_code="UNSUPPORTEDBANK"))
    assert outcome.direct.status is VerificationStatus.UNSUPPORTED
    assert outcome.continue_image_forensics is True


class _FailureProvider:
    name = "synthetic-failure-provider"

    def __init__(self, failure):
        self.failure = failure

    def supports(self, request):
        return True

    def verify_transaction(self, request):
        if isinstance(self.failure, BaseException):
            raise self.failure
        return self.failure


@pytest.mark.parametrize(
    ("failure", "reason"),
    [
        (ProviderUnavailableError(), "PROVIDER_UNAVAILABLE"),
        (ProviderTimeoutError(), "PROVIDER_TIMEOUT"),
        (MalformedProviderResponseError(), "PROVIDER_RESPONSE_INVALID"),
        ({"status": "VERIFIED"}, "PROVIDER_RESPONSE_INVALID"),
    ],
)
def test_provider_failures_are_unavailable_and_preserve_fallback(failure, reason):
    outcome = TransactionVerificationService(_FailureProvider(failure)).verify(_request())
    assert outcome.direct.status is VerificationStatus.UNAVAILABLE
    assert outcome.direct.reason_code == reason
    assert outcome.continue_image_forensics is True


def test_mock_is_disabled_by_default_and_never_has_a_network_configuration():
    with pytest.raises(RuntimeError, match="disabled"):
        DevelopmentMockProvider({})
    provider = DevelopmentMockProvider({}, enabled=True)
    assert not hasattr(provider, "base_url")
    assert not hasattr(provider, "access_token")


def test_request_validation_rejects_unsafe_or_invalid_values():
    with pytest.raises(ValueError, match="reference"):
        TransactionVerificationRequest(reference="line\nbreak")
    with pytest.raises(ValueError, match="amount"):
        TransactionVerificationRequest(reference=REFERENCE, amount_minor=-1)
    with pytest.raises(ValueError, match="Currency"):
        TransactionVerificationRequest(reference=REFERENCE, currency="lkr")


def test_sensitive_query_values_are_not_logged(caplog):
    caplog.set_level(logging.INFO, logger="verislip.layer5")
    secret_reference = "SECRET-REFERENCE-991"
    secret_recipient = "SECRET-RECIPIENT-882"
    _service().verify(
        _request(reference=secret_reference, recipient_identifier=secret_recipient)
    )
    assert secret_reference not in caplog.text
    assert secret_recipient not in caplog.text
    assert "layer5.verification.completed" in caplog.text


def test_service_does_not_replace_image_forensic_verdict_even_when_verified():
    outcome = _service().verify(_request())
    assert outcome.direct.status is VerificationStatus.VERIFIED
    assert outcome.continue_image_forensics is True
