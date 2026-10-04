"""Validate and summarise pseudonymous closed-beta observations.

The input deliberately excludes phone numbers, names, receipt images, OCR text,
transaction references, and free-form comments.  It is suitable for aggregate
pilot analysis, not for storing operational WhatsApp payloads.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping


class PilotDataError(ValueError):
    """Raised for invalid pilot data without echoing row contents."""


FIELDS = (
    "participant_id",
    "pilot_day",
    "event_type",
    "model_verdict",
    "confirmed_outcome",
    "feedback_code",
)
PARTICIPANT_RE = re.compile(r"^seller-[a-f0-9]{8}$")
EVENT_TYPES = frozenset({"verification", "feedback", "escalation"})
VERDICTS = frozenset({"", "authentic", "suspicious", "high_risk"})
OUTCOMES = frozenset({"", "genuine", "fraud", "unconfirmed"})
FEEDBACK_CODES = frozenset(
    {"", "useful", "unclear", "too_slow", "false_alarm", "missed_fraud", "other"}
)


def validate_rows(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, str]]:
    """Return normalized safe rows or fail without exposing supplied values."""
    normalized: list[dict[str, str]] = []
    for index, row in enumerate(rows, 2):
        if set(row) != set(FIELDS):
            raise PilotDataError(f"Pilot row {index} has an invalid schema.")
        clean = {field: str(row.get(field, "")).strip().casefold() for field in FIELDS}
        if not PARTICIPANT_RE.fullmatch(clean["participant_id"]):
            raise PilotDataError(f"Pilot row {index} has an invalid participant ID.")
        try:
            day = int(clean["pilot_day"])
        except ValueError:
            raise PilotDataError(f"Pilot row {index} has an invalid pilot day.") from None
        if not 1 <= day <= 14:
            raise PilotDataError(f"Pilot row {index} has an invalid pilot day.")
        if clean["event_type"] not in EVENT_TYPES:
            raise PilotDataError(f"Pilot row {index} has an invalid event type.")
        if clean["model_verdict"] not in VERDICTS:
            raise PilotDataError(f"Pilot row {index} has an invalid verdict.")
        if clean["confirmed_outcome"] not in OUTCOMES:
            raise PilotDataError(f"Pilot row {index} has an invalid confirmed outcome.")
        if clean["feedback_code"] not in FEEDBACK_CODES:
            raise PilotDataError(f"Pilot row {index} has an invalid feedback code.")
        if clean["event_type"] == "verification" and not clean["model_verdict"]:
            raise PilotDataError(f"Pilot row {index} is missing a verification verdict.")
        clean["pilot_day"] = str(day)
        normalized.append(clean)
    return normalized


def summarise(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Calculate descriptive counts; never infer outcomes from unconfirmed rows."""
    safe_rows = validate_rows(rows)
    verification_rows = [r for r in safe_rows if r["event_type"] == "verification"]
    confirmed = [r for r in verification_rows if r["confirmed_outcome"] in {"genuine", "fraud"}]
    false_positives = sum(
        r["confirmed_outcome"] == "genuine" and r["model_verdict"] != "authentic"
        for r in confirmed
    )
    false_negatives = sum(
        r["confirmed_outcome"] == "fraud" and r["model_verdict"] == "authentic"
        for r in confirmed
    )
    return {
        "participants": len({r["participant_id"] for r in safe_rows}),
        "events": len(safe_rows),
        "verifications": len(verification_rows),
        "confirmed_verifications": len(confirmed),
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "verdict_counts": dict(sorted(Counter(r["model_verdict"] for r in verification_rows).items())),
        "feedback_counts": dict(
            sorted(Counter(r["feedback_code"] for r in safe_rows if r["feedback_code"]).items())
        ),
    }


def analyse_pilot_csv(path: str | Path) -> dict[str, Any]:
    """Read a local CSV and return privacy-safe aggregate pilot counts."""
    try:
        with Path(path).open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != FIELDS:
                raise PilotDataError("Pilot CSV has an invalid header.")
            return summarise(reader)
    except OSError:
        raise PilotDataError("Pilot CSV could not be read.") from None
