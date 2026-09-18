"""Tenant-isolated, metadata-only verification history storage."""

from __future__ import annotations

import os
import threading
import uuid
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Callable, List, Optional, Protocol


def _bounded_env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except ValueError:
        return default
    return max(minimum, min(maximum, value))


@dataclass(frozen=True)
class VerificationHistoryRecord:
    """Minimal metadata retained for one successful verification."""

    verification_id: str
    created_at: datetime
    reference_no: Optional[str]
    verdict: str
    tamper_risk_percentage: float
    bank_code: Optional[str]
    bank_name: Optional[str]


@dataclass(frozen=True)
class HistoryPage:
    """One page of a merchant's matching verification metadata."""

    items: List[VerificationHistoryRecord]
    total: int
    page: int
    page_size: int
    has_more: bool


class VerificationHistoryStore(Protocol):
    """Persistence boundary for a production database-backed implementation."""

    def add(
        self,
        owner_key_id: str,
        *,
        reference_no: Optional[str],
        verdict: str,
        tamper_risk_percentage: float,
        bank_code: Optional[str] = None,
        bank_name: Optional[str] = None,
    ) -> VerificationHistoryRecord: ...

    def search(
        self,
        owner_key_id: str,
        *,
        reference_query: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> HistoryPage: ...


@dataclass(frozen=True)
class _OwnedRecord:
    owner_key_id: str
    record: VerificationHistoryRecord


class InMemoryVerificationHistoryStore:
    """Thread-safe bounded local store; replace with shared storage in production."""

    def __init__(
        self,
        max_records: Optional[int] = None,
        retention_days: Optional[int] = None,
        clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self.max_records = max_records or _bounded_env_int(
            "VERISLIP_HISTORY_MAX_RECORDS", 10_000, 100, 1_000_000
        )
        self.retention_days = retention_days or _bounded_env_int(
            "VERISLIP_HISTORY_RETENTION_DAYS", 365, 1, 3_650
        )
        self._clock = clock
        self._records: List[_OwnedRecord] = []
        self._lock = threading.Lock()

    def _cleanup_locked(self, now: datetime) -> None:
        cutoff = now - timedelta(days=self.retention_days)
        self._records = [r for r in self._records if r.record.created_at >= cutoff]
        if len(self._records) > self.max_records:
            self._records = self._records[-self.max_records :]

    def add(
        self,
        owner_key_id: str,
        *,
        reference_no: Optional[str],
        verdict: str,
        tamper_risk_percentage: float,
        bank_code: Optional[str] = None,
        bank_name: Optional[str] = None,
    ) -> VerificationHistoryRecord:
        """Store only display metadata, never receipt bytes or forensic payloads."""
        now = self._clock().astimezone(timezone.utc)
        reference = reference_no.strip()[:128] if reference_no else None
        record = VerificationHistoryRecord(
            verification_id=str(uuid.uuid4()),
            created_at=now,
            reference_no=reference or None,
            verdict=str(verdict)[:40],
            tamper_risk_percentage=max(0.0, min(100.0, float(tamper_risk_percentage))),
            bank_code=str(bank_code)[:40] if bank_code else None,
            bank_name=str(bank_name)[:100] if bank_name else None,
        )
        with self._lock:
            self._cleanup_locked(now)
            self._records.append(_OwnedRecord(owner_key_id=owner_key_id, record=record))
            if len(self._records) > self.max_records:
                self._records = self._records[-self.max_records :]
        return record

    def search(
        self,
        owner_key_id: str,
        *,
        reference_query: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> HistoryPage:
        now = self._clock().astimezone(timezone.utc)
        query = reference_query.strip().casefold() if reference_query else None
        start = datetime.combine(date_from, time.min, tzinfo=timezone.utc) if date_from else None
        end = (
            datetime.combine(date_to + timedelta(days=1), time.min, tzinfo=timezone.utc)
            if date_to
            else None
        )
        with self._lock:
            self._cleanup_locked(now)
            matches = [
                owned.record
                for owned in self._records
                if owned.owner_key_id == owner_key_id
                and (not query or query in (owned.record.reference_no or "").casefold())
                and (start is None or owned.record.created_at >= start)
                and (end is None or owned.record.created_at < end)
            ]
        matches.sort(key=lambda item: item.created_at, reverse=True)
        total = len(matches)
        offset = (page - 1) * page_size
        items = matches[offset : offset + page_size]
        return HistoryPage(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            has_more=offset + len(items) < total,
        )

    def clear(self) -> None:
        """Clear local state; intended for tests and controlled shutdowns."""
        with self._lock:
            self._records.clear()
