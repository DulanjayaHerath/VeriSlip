"""Permission-gated curation for genuine receipt benchmark candidates.

Only redacted, metadata-stripped pixels and a constrained metadata record enter
the curated directory. Consent evidence and source images remain outside it.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol

from PIL import Image

from core.datasets.integrity import build_manifest, write_manifest
from core.privacy.pii_redaction import PIIRedactionError, PIIRedactionPipeline
from core.security.image_sanitizer import ImageValidationError, sanitize_image_bytes

METADATA_FILENAME = "curation_metadata.jsonl"
INTEGRITY_FILENAME = "integrity_manifest.json"
_SAFE_CODE = re.compile(r"^consent-[a-f0-9]{8,32}$")
_BANK_CATEGORIES = frozenset({"boc", "commercial", "hnb", "peoples", "sampath", "seylan", "other"})
_SOURCE_TYPES = frozenset({"team_transaction", "merchant_contribution"})
_OS_FAMILIES = frozenset({"ios", "android", "other"})
_CAPTURE_TYPES = frozenset({"screenshot", "camera_photo", "digital_export"})


class CurationError(ValueError):
    """Privacy-safe rejection that never includes metadata values or source paths."""


class Redactor(Protocol):
    def redact(self, image: Image.Image, *, method: str = "mask") -> Any: ...


@dataclass(frozen=True)
class CandidateMetadata:
    """Non-identifying provenance fields required for one curated sample."""

    bank_category: str
    source_type: str
    os_family: str
    capture_type: str
    permission_status: str
    permission_record_id: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CandidateMetadata":
        if set(value) != set(cls.__annotations__):
            raise CurationError("Candidate metadata has an invalid schema.")
        if not all(isinstance(value[field], str) for field in cls.__annotations__):
            raise CurationError("Candidate metadata has invalid values.")
        item = cls(**{field: value[field].strip().casefold() for field in cls.__annotations__})
        if (
            item.bank_category not in _BANK_CATEGORIES
            or item.source_type not in _SOURCE_TYPES
            or item.os_family not in _OS_FAMILIES
            or item.capture_type not in _CAPTURE_TYPES
            or item.permission_status != "granted"
            or not _SAFE_CODE.fullmatch(item.permission_record_id)
        ):
            raise CurationError("Candidate metadata has invalid values.")
        return item


def _load_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise CurationError("Curation metadata is unreadable or malformed.") from None
    if not all(isinstance(record, dict) for record in records):
        raise CurationError("Curation metadata is unreadable or malformed.")
    return records


def _atomic_metadata_write(path: Path, records: list[dict[str, Any]]) -> None:
    payload = "".join(json.dumps(row, sort_keys=True) + "\n" for row in records)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            handle.write(payload)
            temporary = handle.name
        os.replace(temporary, path)
    except OSError:
        if temporary:
            Path(temporary).unlink(missing_ok=True)
        raise CurationError("Curated metadata could not be written.") from None


def curate_candidate(
    image_bytes: bytes,
    metadata: Mapping[str, Any],
    output_root: str | Path,
    *,
    redactor: Redactor | None = None,
) -> dict[str, Any]:
    """Sanitize, locally redact, and store one permission-cleared candidate."""
    details = CandidateMetadata.from_mapping(metadata)
    root = Path(output_root)
    if root.exists() and (not root.is_dir() or root.is_symlink()):
        raise CurationError("Curated output must be a non-symlink directory.")
    root.mkdir(parents=True, exist_ok=True)
    try:
        image = sanitize_image_bytes(image_bytes)
        result = (redactor or PIIRedactionPipeline()).redact(image, method="mask")
    except (ImageValidationError, PIIRedactionError):
        raise CurationError("Candidate image failed safety or PII-redaction checks.") from None

    sample_id = f"sample-{secrets.token_hex(8)}"
    filename = f"{sample_id}.png"
    destination = root / filename
    while destination.exists():
        sample_id = f"sample-{secrets.token_hex(8)}"
        filename = f"{sample_id}.png"
        destination = root / filename
    record = {
        "sample_id": sample_id,
        "image_path": filename,
        **asdict(details),
        "redaction_status": "completed",
        "integrity_status": "pending_manifest",
    }
    records = _load_records(root / METADATA_FILENAME)
    if any(row.get("permission_record_id") == details.permission_record_id for row in records):
        raise CurationError("Permission record has already been curated.")
    try:
        result.image.save(destination, format="PNG")
        records.append(record)
        records.sort(key=lambda row: str(row.get("sample_id", "")))
        _atomic_metadata_write(root / METADATA_FILENAME, records)
    except OSError:
        destination.unlink(missing_ok=True)
        raise CurationError("Curated sample could not be written.") from None
    return record


def finalize_integrity(output_root: str | Path) -> dict[str, Any]:
    """Build the existing deterministic SHA-256 manifest for curated images."""
    root = Path(output_root)
    manifest = build_manifest(root)
    write_manifest(manifest, root / INTEGRITY_FILENAME)
    return manifest


def curation_status(output_root: str | Path) -> dict[str, Any]:
    """Return counts derived solely from records currently present on disk."""
    records = _load_records(Path(output_root) / METADATA_FILENAME)
    return {
        "permission_cleared_samples": len(records),
        "target_samples": 200,
        "remaining_to_target": max(0, 200 - len(records)),
        "by_os_family": {name: sum(row.get("os_family") == name for row in records) for name in sorted(_OS_FAMILIES)},
    }
