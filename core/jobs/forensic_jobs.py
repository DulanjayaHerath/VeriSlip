"""Bounded in-process background execution for forensic verification jobs."""

from __future__ import annotations

import logging
import os
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Callable, Dict, Literal, Optional

from core.observability.logging import reset_correlation_id, set_correlation_id


JobState = Literal["pending", "processing", "completed", "failed"]
logger = logging.getLogger("verislip.jobs")


class JobQueueFullError(RuntimeError):
    """Raised when the bounded in-memory job registry has no capacity."""


@dataclass(frozen=True)
class JobSnapshot:
    """Immutable public view of a forensic job."""

    job_id: str
    status: JobState
    correlation_id: str
    created_at: float
    updated_at: float
    result: Optional[Dict[str, Any]]
    error: Optional[str]


@dataclass
class _JobRecord:
    job_id: str
    owner_key_id: str
    correlation_id: str
    status: JobState
    created_at: float
    updated_at: float
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


def _bounded_env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except ValueError:
        return default
    return max(minimum, min(maximum, value))


class ForensicJobManager:
    """Execute jobs on a bounded thread pool and retain safe results temporarily."""

    def __init__(
        self,
        max_workers: Optional[int] = None,
        max_jobs: Optional[int] = None,
        retention_seconds: Optional[int] = None,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.max_workers = max_workers or _bounded_env_int(
            "VERISLIP_JOB_WORKERS", 2, 1, 16
        )
        self.max_jobs = max_jobs or _bounded_env_int(
            "VERISLIP_JOB_MAX_RECORDS", 1_000, 10, 10_000
        )
        self.retention_seconds = retention_seconds or _bounded_env_int(
            "VERISLIP_JOB_RETENTION_SECONDS", 3_600, 60, 86_400
        )
        self._clock = clock
        self._executor = ThreadPoolExecutor(
            max_workers=self.max_workers, thread_name_prefix="verislip-forensics"
        )
        self._records: Dict[str, _JobRecord] = {}
        self._lock = threading.Lock()

    def _cleanup_locked(self, now: float) -> None:
        cutoff = now - self.retention_seconds
        self._records = {
            job_id: record
            for job_id, record in self._records.items()
            if record.status in {"pending", "processing"} or record.updated_at > cutoff
        }

    @staticmethod
    def _snapshot(record: _JobRecord) -> JobSnapshot:
        return JobSnapshot(
            job_id=record.job_id,
            status=record.status,
            correlation_id=record.correlation_id,
            created_at=record.created_at,
            updated_at=record.updated_at,
            result=dict(record.result) if record.result is not None else None,
            error=record.error,
        )

    def submit(
        self,
        owner_key_id: str,
        correlation_id: str,
        task: Callable[[], Dict[str, Any]],
        on_complete: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> JobSnapshot:
        """Register a pending job and schedule it without retaining upload bytes."""
        now = self._clock()
        job_id = str(uuid.uuid4())
        with self._lock:
            self._cleanup_locked(now)
            if len(self._records) >= self.max_jobs:
                raise JobQueueFullError("Forensic job capacity is exhausted.")
            record = _JobRecord(
                job_id=job_id,
                owner_key_id=owner_key_id,
                correlation_id=correlation_id,
                status="pending",
                created_at=now,
                updated_at=now,
            )
            self._records[job_id] = record
            snapshot = self._snapshot(record)
        self._executor.submit(self._run, job_id, task, on_complete)
        return snapshot

    def _run(
        self,
        job_id: str,
        task: Callable[[], Dict[str, Any]],
        on_complete: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> None:
        with self._lock:
            record = self._records.get(job_id)
            if record is None:
                return
            record.status = "processing"
            record.updated_at = self._clock()
            correlation_id = record.correlation_id

        token = set_correlation_id(correlation_id)
        logger.info("forensic_job.started")
        try:
            result = task()
        except Exception as exc:
            with self._lock:
                record = self._records.get(job_id)
                if record is not None:
                    record.status = "failed"
                    record.updated_at = self._clock()
                    record.error = "Forensic analysis could not be completed."
            logger.error(
                "forensic_job.failed", extra={"error_type": type(exc).__name__}
            )
        else:
            if on_complete is not None:
                try:
                    on_complete(result)
                except Exception as exc:
                    logger.warning(
                        "forensic_job.completion_hook_failed",
                        extra={"error_type": type(exc).__name__},
                    )
            with self._lock:
                record = self._records.get(job_id)
                if record is not None:
                    record.status = "completed"
                    record.updated_at = self._clock()
                    record.result = result
            logger.info("forensic_job.completed")
        finally:
            reset_correlation_id(token)

    def get(self, job_id: str, owner_key_id: str) -> Optional[JobSnapshot]:
        """Return a job only to the API key that submitted it."""
        now = self._clock()
        with self._lock:
            self._cleanup_locked(now)
            record = self._records.get(job_id)
            if record is None or not hmac_compare_owner(record.owner_key_id, owner_key_id):
                return None
            return self._snapshot(record)


def hmac_compare_owner(expected: str, supplied: str) -> bool:
    """Compare non-secret key fingerprints without introducing timing variance."""
    import hmac

    return hmac.compare_digest(expected, supplied)
