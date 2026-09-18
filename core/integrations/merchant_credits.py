"""Atomic merchant verification-credit tracking for WhatsApp submissions."""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import threading
from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Protocol, Tuple
from urllib.parse import urlsplit


@dataclass(frozen=True)
class MerchantCreditPolicy:
    """Configured business quota for the current merchant subscription tier."""

    tier: str
    verification_limit: int
    upgrade_url: Optional[str]

    @classmethod
    def from_environment(cls) -> "MerchantCreditPolicy":
        tier = os.getenv("VERISLIP_WHATSAPP_DEFAULT_TIER", "free").strip().lower()
        if not tier or len(tier) > 32:
            raise RuntimeError("WhatsApp merchant tier configuration is invalid.")
        try:
            limit = int(os.getenv("VERISLIP_WHATSAPP_FREE_VERIFICATIONS", "5"))
        except ValueError as exc:
            raise RuntimeError(
                "WhatsApp merchant credit configuration is invalid."
            ) from exc
        if limit <= 0:
            raise RuntimeError("WhatsApp merchant credit limit must be positive.")

        raw_url = os.getenv("VERISLIP_WHATSAPP_UPGRADE_URL", "").strip()
        upgrade_url = raw_url or None
        if upgrade_url:
            parsed = urlsplit(upgrade_url)
            if (
                parsed.scheme != "https"
                or not parsed.hostname
                or parsed.username is not None
                or parsed.password is not None
                or len(upgrade_url) > 500
            ):
                raise RuntimeError("WhatsApp upgrade URL configuration is invalid.")
        return cls(tier=tier, verification_limit=limit, upgrade_url=upgrade_url)


@dataclass(frozen=True)
class MerchantBalance:
    tier: str
    limit: int
    used: int
    reserved: int
    remaining: int


class ReservationStatus(str, Enum):
    ACCEPTED = "accepted"
    DUPLICATE = "duplicate"
    EXHAUSTED = "exhausted"


@dataclass(frozen=True)
class CreditReservation:
    status: ReservationStatus
    token: Optional[str]
    balance: MerchantBalance


class MerchantCreditStore(Protocol):
    """Persistence boundary for atomic merchant-credit operations."""

    def balance(self, merchant_identifier: str, policy: MerchantCreditPolicy) -> MerchantBalance: ...

    def reserve(
        self,
        merchant_identifier: str,
        message_id: Optional[str],
        policy: MerchantCreditPolicy,
    ) -> CreditReservation: ...

    def complete(self, token: str, policy: MerchantCreditPolicy) -> MerchantBalance: ...

    def release(self, token: str, policy: MerchantCreditPolicy) -> MerchantBalance: ...


@dataclass(frozen=True)
class _PendingReservation:
    merchant_key: str
    message_key: Optional[str]


class InMemoryMerchantCreditStore:
    """Thread-safe local credit store for development and automated tests.

    Merchant and message identifiers are stored only as process-keyed HMAC
    fingerprints. Reservations make quota checks atomic and are completed only
    after successful forensic analysis.
    """

    def __init__(self, *, max_idempotency_records: int = 50_000) -> None:
        if max_idempotency_records <= 0:
            raise ValueError("Idempotency capacity must be positive.")
        self._hash_key = secrets.token_bytes(32)
        self._used: Dict[str, int] = {}
        self._pending: Dict[str, _PendingReservation] = {}
        self._pending_messages: Dict[Tuple[str, str], str] = {}
        self._completed_messages: OrderedDict[Tuple[str, str], None] = OrderedDict()
        self._max_idempotency_records = max_idempotency_records
        self._lock = threading.Lock()

    def _fingerprint(self, value: str) -> str:
        return hmac.new(
            self._hash_key, value.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def _balance_locked(
        self, merchant_key: str, policy: MerchantCreditPolicy
    ) -> MerchantBalance:
        used = self._used.get(merchant_key, 0)
        reserved = sum(
            reservation.merchant_key == merchant_key
            for reservation in self._pending.values()
        )
        return MerchantBalance(
            tier=policy.tier,
            limit=policy.verification_limit,
            used=used,
            reserved=reserved,
            remaining=max(0, policy.verification_limit - used - reserved),
        )

    def balance(
        self, merchant_identifier: str, policy: MerchantCreditPolicy
    ) -> MerchantBalance:
        merchant_key = self._fingerprint(merchant_identifier)
        with self._lock:
            return self._balance_locked(merchant_key, policy)

    def reserve(
        self,
        merchant_identifier: str,
        message_id: Optional[str],
        policy: MerchantCreditPolicy,
    ) -> CreditReservation:
        merchant_key = self._fingerprint(merchant_identifier)
        message_key = self._fingerprint(message_id) if message_id else None
        idempotency_key = (
            (merchant_key, message_key) if message_key is not None else None
        )
        with self._lock:
            if idempotency_key is not None and (
                idempotency_key in self._pending_messages
                or idempotency_key in self._completed_messages
            ):
                return CreditReservation(
                    ReservationStatus.DUPLICATE,
                    None,
                    self._balance_locked(merchant_key, policy),
                )

            balance = self._balance_locked(merchant_key, policy)
            if balance.remaining <= 0:
                return CreditReservation(ReservationStatus.EXHAUSTED, None, balance)

            token = secrets.token_urlsafe(24)
            self._pending[token] = _PendingReservation(merchant_key, message_key)
            if idempotency_key is not None:
                self._pending_messages[idempotency_key] = token
            return CreditReservation(
                ReservationStatus.ACCEPTED,
                token,
                self._balance_locked(merchant_key, policy),
            )

    def complete(self, token: str, policy: MerchantCreditPolicy) -> MerchantBalance:
        with self._lock:
            reservation = self._pending.pop(token, None)
            if reservation is None:
                raise ValueError("Credit reservation is invalid or already finalized.")
            self._used[reservation.merchant_key] = (
                self._used.get(reservation.merchant_key, 0) + 1
            )
            if reservation.message_key is not None:
                key = (reservation.merchant_key, reservation.message_key)
                self._pending_messages.pop(key, None)
                self._completed_messages[key] = None
                self._completed_messages.move_to_end(key)
                while len(self._completed_messages) > self._max_idempotency_records:
                    self._completed_messages.popitem(last=False)
            return self._balance_locked(reservation.merchant_key, policy)

    def release(self, token: str, policy: MerchantCreditPolicy) -> MerchantBalance:
        with self._lock:
            reservation = self._pending.pop(token, None)
            if reservation is None:
                raise ValueError("Credit reservation is invalid or already finalized.")
            if reservation.message_key is not None:
                self._pending_messages.pop(
                    (reservation.merchant_key, reservation.message_key), None
                )
            return self._balance_locked(reservation.merchant_key, policy)

    def clear(self) -> None:
        with self._lock:
            self._used.clear()
            self._pending.clear()
            self._pending_messages.clear()
            self._completed_messages.clear()


class MerchantCreditService:
    """Business-level facade independent from API authentication/rate limits."""

    def __init__(
        self, store: MerchantCreditStore, policy: MerchantCreditPolicy
    ) -> None:
        self.store = store
        self.policy = policy

    def balance(self, merchant_identifier: str) -> MerchantBalance:
        return self.store.balance(merchant_identifier, self.policy)

    def reserve(
        self, merchant_identifier: str, message_id: Optional[str]
    ) -> CreditReservation:
        return self.store.reserve(merchant_identifier, message_id, self.policy)

    def complete(self, token: str) -> MerchantBalance:
        return self.store.complete(token, self.policy)

    def release(self, token: str) -> MerchantBalance:
        return self.store.release(token, self.policy)


merchant_credit_service = MerchantCreditService(
    InMemoryMerchantCreditStore(), MerchantCreditPolicy.from_environment()
)
