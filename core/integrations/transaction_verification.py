"""Provider-neutral, read-only Layer 5 transaction-verification contracts.

This module contains no LankaPay or bank network client.  The included mock is
explicitly development-only and operates solely on caller-supplied synthetic
records.  Provider failures are represented separately from transaction
mismatches so an outage can never become an automatic fraud verdict.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
import hashlib
import logging
import re
from typing import Mapping, Optional, Protocol


logger = logging.getLogger("verislip.layer5")
_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9._:/-]{1,128}$")


class VerificationStatus(str, Enum):
    """Provider-neutral outcome; technical failures are not mismatches."""

    VERIFIED = "VERIFIED"
    NOT_VERIFIED = "NOT_VERIFIED"
    UNAVAILABLE = "UNAVAILABLE"
    UNSUPPORTED = "UNSUPPORTED"


class MatchState(str, Enum):
    """Comparison state for an individual supplied attribute."""

    MATCH = "MATCH"
    MISMATCH = "MISMATCH"
    NOT_CHECKED = "NOT_CHECKED"


@dataclass(frozen=True)
class TransactionVerificationRequest:
    """Minimal normalized query passed transiently to an authorized provider."""

    reference: str
    amount_minor: Optional[int] = None
    recipient_identifier: Optional[str] = None
    transaction_date: Optional[date] = None
    bank_code: Optional[str] = None
    merchant_identifier: Optional[str] = None
    currency: str = "LKR"

    def __post_init__(self) -> None:
        if not _SAFE_IDENTIFIER.fullmatch(self.reference):
            raise ValueError("Transaction reference has an invalid format.")
        if self.amount_minor is not None and (
            isinstance(self.amount_minor, bool) or not 0 <= self.amount_minor < 10**15
        ):
            raise ValueError("Transaction amount is outside the supported range.")
        if self.recipient_identifier is not None and not _SAFE_IDENTIFIER.fullmatch(
            self.recipient_identifier
        ):
            raise ValueError("Recipient identifier has an invalid format.")
        if self.merchant_identifier is not None and not _SAFE_IDENTIFIER.fullmatch(
            self.merchant_identifier
        ):
            raise ValueError("Merchant identifier has an invalid format.")
        if self.bank_code is not None and not _SAFE_IDENTIFIER.fullmatch(self.bank_code):
            raise ValueError("Bank code has an invalid format.")
        if not re.fullmatch(r"[A-Z]{3}", self.currency):
            raise ValueError("Currency must use an uppercase ISO-style code.")


@dataclass(frozen=True)
class TransactionVerificationResult:
    """Sanitized result safe for VeriSlip business logic and public APIs."""

    status: VerificationStatus
    provider: str
    reference_match: MatchState = MatchState.NOT_CHECKED
    amount_match: MatchState = MatchState.NOT_CHECKED
    recipient_match: MatchState = MatchState.NOT_CHECKED
    verified_at: Optional[datetime] = None
    provider_reference: Optional[str] = None
    reason_code: Optional[str] = None


@dataclass(frozen=True)
class Layer5Outcome:
    """Direct result plus an explicit image-forensics fallback decision."""

    direct: TransactionVerificationResult
    continue_image_forensics: bool = True


class ProviderUnavailableError(RuntimeError):
    """Authorized provider could not be reached or is not ready."""


class ProviderTimeoutError(ProviderUnavailableError):
    """Authorized provider exceeded its configured deadline."""


class MalformedProviderResponseError(ProviderUnavailableError):
    """Provider returned data that failed the adapter's strict schema."""


class TransactionVerificationProvider(Protocol):
    """Read-only adapter contract; implementations must never move money."""

    @property
    def name(self) -> str: ...

    def supports(self, request: TransactionVerificationRequest) -> bool: ...

    def verify_transaction(
        self, request: TransactionVerificationRequest
    ) -> TransactionVerificationResult: ...


@dataclass(frozen=True)
class SyntheticTransaction:
    """Development fixture; all values must be synthetic."""

    reference: str
    amount_minor: int
    recipient_fingerprint: str
    transaction_date: Optional[date] = None
    bank_code: Optional[str] = None


def fingerprint_identifier(value: str) -> str:
    """Create a one-way comparison token without retaining an account identifier."""
    normalized = value.strip().upper().encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()


class DevelopmentMockProvider:
    """Deterministic, opt-in mock that never performs network activity."""

    name = "development-mock"

    def __init__(
        self,
        records: Mapping[str, SyntheticTransaction],
        *,
        enabled: bool = False,
        supported_banks: Optional[frozenset[str]] = None,
    ) -> None:
        if not enabled:
            raise RuntimeError("The development transaction provider is disabled.")
        self._records = {key.upper(): value for key, value in records.items()}
        self._supported_banks = supported_banks

    def supports(self, request: TransactionVerificationRequest) -> bool:
        return self._supported_banks is None or (
            request.bank_code is not None
            and request.bank_code.upper() in self._supported_banks
        )

    def verify_transaction(
        self, request: TransactionVerificationRequest
    ) -> TransactionVerificationResult:
        record = self._records.get(request.reference.upper())
        now = datetime.now(timezone.utc)
        if record is None:
            return TransactionVerificationResult(
                status=VerificationStatus.NOT_VERIFIED,
                provider=self.name,
                reference_match=MatchState.MISMATCH,
                verified_at=now,
                reason_code="REFERENCE_NOT_FOUND",
            )

        amount_match = MatchState.NOT_CHECKED
        if request.amount_minor is not None:
            amount_match = (
                MatchState.MATCH
                if request.amount_minor == record.amount_minor
                else MatchState.MISMATCH
            )
        recipient_match = MatchState.NOT_CHECKED
        if request.recipient_identifier is not None:
            recipient_match = (
                MatchState.MATCH
                if fingerprint_identifier(request.recipient_identifier)
                == record.recipient_fingerprint
                else MatchState.MISMATCH
            )
        date_matches = (
            request.transaction_date is None
            or record.transaction_date is None
            or request.transaction_date == record.transaction_date
        )
        matched = (
            amount_match is not MatchState.MISMATCH
            and recipient_match is not MatchState.MISMATCH
            and date_matches
        )
        return TransactionVerificationResult(
            status=(
                VerificationStatus.VERIFIED
                if matched
                else VerificationStatus.NOT_VERIFIED
            ),
            provider=self.name,
            reference_match=MatchState.MATCH,
            amount_match=amount_match,
            recipient_match=recipient_match,
            verified_at=now,
            reason_code="MATCH" if matched else "ATTRIBUTE_MISMATCH",
        )


class TransactionVerificationService:
    """Contain provider failures and preserve the existing forensic fallback."""

    def __init__(self, provider: TransactionVerificationProvider) -> None:
        self._provider = provider

    def verify(self, request: TransactionVerificationRequest) -> Layer5Outcome:
        if not self._provider.supports(request):
            result = TransactionVerificationResult(
                status=VerificationStatus.UNSUPPORTED,
                provider=self._provider.name,
                reason_code="BANK_OR_PROVIDER_UNSUPPORTED",
            )
        else:
            try:
                result = self._provider.verify_transaction(request)
                if not isinstance(result, TransactionVerificationResult):
                    raise MalformedProviderResponseError
            except ProviderTimeoutError:
                result = TransactionVerificationResult(
                    status=VerificationStatus.UNAVAILABLE,
                    provider=self._provider.name,
                    reason_code="PROVIDER_TIMEOUT",
                )
            except MalformedProviderResponseError:
                result = TransactionVerificationResult(
                    status=VerificationStatus.UNAVAILABLE,
                    provider=self._provider.name,
                    reason_code="PROVIDER_RESPONSE_INVALID",
                )
            except ProviderUnavailableError:
                result = TransactionVerificationResult(
                    status=VerificationStatus.UNAVAILABLE,
                    provider=self._provider.name,
                    reason_code="PROVIDER_UNAVAILABLE",
                )
            except Exception:
                # Adapter defects are unavailable—not evidence of fraud.
                result = TransactionVerificationResult(
                    status=VerificationStatus.UNAVAILABLE,
                    provider=self._provider.name,
                    reason_code="PROVIDER_RESPONSE_INVALID",
                )
        logger.info(
            "layer5.verification.completed",
            extra={"provider": result.provider, "verification_status": result.status.value},
        )
        return Layer5Outcome(direct=result, continue_image_forensics=True)
