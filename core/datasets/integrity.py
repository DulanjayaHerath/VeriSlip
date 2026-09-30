"""Read-only SHA-256 and image-integrity checks for VeriSlip datasets."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import warnings
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Iterable, Mapping

from PIL import Image, UnidentifiedImageError

from core.security.image_sanitizer import (
    MAX_IMAGE_HEIGHT,
    MAX_IMAGE_PIXELS,
    MAX_IMAGE_WIDTH,
    SUPPORTED_IMAGE_FORMATS,
)

MANIFEST_SCHEMA_VERSION = 1
HASH_ALGORITHM = "sha256"
HASH_CHUNK_SIZE = 1024 * 1024
SUPPORTED_IMAGE_SUFFIXES = frozenset({".jpg", ".jpeg", ".png"})
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class IntegrityIssue:
    """A safe, relative-path dataset integrity finding."""

    code: str
    path: str
    message: str


@dataclass(frozen=True)
class VerificationResult:
    """Aggregate result returned without modifying the dataset or manifest."""

    files_checked: int
    issues: tuple[IntegrityIssue, ...]
    duplicates: tuple[tuple[str, ...], ...]

    @property
    def ok(self) -> bool:
        return not self.issues


class DatasetIntegrityError(ValueError):
    """A safe manifest-generation or parsing failure."""

    def __init__(
        self, message: str, issues: Iterable[IntegrityIssue] = ()
    ):  # noqa: D107
        super().__init__(message)
        self.issues = tuple(issues)


def compute_sha256(source: Path | BinaryIO, chunk_size: int = HASH_CHUNK_SIZE) -> str:
    """Return a SHA-256 hex digest using bounded streaming reads."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    digest = hashlib.sha256()
    if hasattr(source, "read"):
        stream = source
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
        return digest.hexdigest()

    with Path(source).open("rb") as stream:
        return compute_sha256(stream, chunk_size)


def _relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _discover_images(root: Path) -> tuple[list[Path], list[IntegrityIssue]]:
    """Discover supported files without following symlinked dataset content."""
    paths: list[Path] = []
    issues: list[IntegrityIssue] = []
    try:
        entries = sorted(root.rglob("*"), key=lambda item: item.as_posix().casefold())
    except OSError:
        raise DatasetIntegrityError("Dataset directory could not be read.") from None

    for path in entries:
        if path.suffix.casefold() not in SUPPORTED_IMAGE_SUFFIXES:
            continue
        relative = _relative_path(root, path)
        try:
            if path.is_symlink() or any(
                parent.is_symlink() for parent in path.parents if parent != root
            ):
                issues.append(
                    IntegrityIssue(
                        "unsafe_path",
                        relative,
                        "Symbolic links are not accepted as dataset images.",
                    )
                )
            elif path.is_file():
                paths.append(path)
        except OSError:
            issues.append(
                IntegrityIssue(
                    "filesystem_error",
                    relative,
                    "Dataset entry could not be inspected.",
                )
            )
    paths.sort(key=lambda item: _relative_path(root, item))
    return paths, issues


def _bomb_warning_type():
    return getattr(Image, "DecompressionBombWarning", RuntimeWarning)


def _bomb_error_type():
    return getattr(Image, "DecompressionBombError", Exception)


def _inspect_image(path: Path) -> dict[str, int | str]:
    """Fully decode an image read-only and return deterministic metadata."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", _bomb_warning_type())
            with Image.open(path) as image:
                image_format = (image.format or "").upper()
                width, height = image.size
                if image_format not in SUPPORTED_IMAGE_FORMATS:
                    raise DatasetIntegrityError(
                        "Image content uses an unsupported format."
                    )
                if getattr(image, "n_frames", 1) != 1:
                    raise DatasetIntegrityError("Animated images are not supported.")
                if (
                    width <= 0
                    or height <= 0
                    or width > MAX_IMAGE_WIDTH
                    or height > MAX_IMAGE_HEIGHT
                    or width * height > MAX_IMAGE_PIXELS
                ):
                    raise DatasetIntegrityError(
                        "Image dimensions exceed the permitted limit."
                    )
                image.verify()
            with Image.open(path) as decoded:
                decoded.load()
        return {"width": width, "height": height, "format": image_format}
    except DatasetIntegrityError:
        raise
    except (_bomb_error_type(), _bomb_warning_type()):
        raise DatasetIntegrityError(
            "Image dimensions exceed the permitted limit."
        ) from None
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError):
        raise DatasetIntegrityError(
            "Image is corrupt, truncated, or invalid."
        ) from None


def _duplicates(files: Iterable[Mapping[str, Any]]) -> tuple[tuple[str, ...], ...]:
    groups: dict[str, list[str]] = defaultdict(list)
    for entry in files:
        groups[str(entry["sha256"])].append(str(entry["path"]))
    return tuple(
        tuple(sorted(paths)) for _, paths in sorted(groups.items()) if len(paths) > 1
    )


def build_manifest(dataset_root: str | os.PathLike[str]) -> dict[str, Any]:
    """Build a deterministic manifest or fail if any image cannot be trusted."""
    root = Path(dataset_root)
    if not root.is_dir() or root.is_symlink():
        raise DatasetIntegrityError(
            "Dataset root must be a readable, non-symlink directory."
        )
    root = root.resolve()
    paths, issues = _discover_images(root)
    files: list[dict[str, Any]] = []
    for path in paths:
        relative = _relative_path(root, path)
        try:
            metadata = _inspect_image(path)
            size = path.stat().st_size
            checksum = compute_sha256(path)
        except DatasetIntegrityError as exc:
            issues.append(IntegrityIssue("corrupt_file", relative, str(exc)))
            continue
        except OSError:
            issues.append(
                IntegrityIssue(
                    "filesystem_error", relative, "Image file could not be read."
                )
            )
            continue
        files.append(
            {
                "path": relative,
                "sha256": checksum,
                "size_bytes": size,
                **metadata,
            }
        )

    if issues:
        raise DatasetIntegrityError(
            "Dataset contains invalid or unsafe images.", issues
        )
    files.sort(key=lambda entry: entry["path"])
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "hash_algorithm": HASH_ALGORITHM,
        "files": files,
        "duplicates": [
            {
                "sha256": next(
                    entry["sha256"] for entry in files if entry["path"] == paths[0]
                ),
                "paths": list(paths),
            }
            for paths in _duplicates(files)
        ],
    }


def write_manifest(
    manifest: Mapping[str, Any], manifest_path: str | os.PathLike[str]
) -> None:
    """Atomically write canonical JSON without timestamps or absolute paths."""
    destination = Path(manifest_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=destination.parent, delete=False
        ) as temporary:
            temporary.write(payload)
            temporary_name = temporary.name
        os.replace(temporary_name, destination)
    except OSError:
        if temporary_name:
            try:
                Path(temporary_name).unlink(missing_ok=True)
            except OSError:
                pass
        raise DatasetIntegrityError("Manifest file could not be written.") from None


def _safe_manifest_path(value: Any) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise DatasetIntegrityError("Manifest contains an unsafe file path.")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise DatasetIntegrityError("Manifest contains an unsafe file path.")
    if ":" in path.parts[0] or path.as_posix() != value:
        raise DatasetIntegrityError("Manifest contains an unsafe file path.")
    if Path(value).suffix.casefold() not in SUPPORTED_IMAGE_SUFFIXES:
        raise DatasetIntegrityError("Manifest contains an unsupported image path.")
    return value


def _validate_manifest(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        raise DatasetIntegrityError("Manifest must contain a JSON object.")
    if payload.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise DatasetIntegrityError("Manifest schema version is unsupported.")
    if payload.get("hash_algorithm") != HASH_ALGORITHM:
        raise DatasetIntegrityError("Manifest hash algorithm is unsupported.")
    entries = payload.get("files")
    if not isinstance(entries, list):
        raise DatasetIntegrityError("Manifest files field is malformed.")
    validated: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in entries:
        if not isinstance(raw, dict):
            raise DatasetIntegrityError("Manifest file entry is malformed.")
        path = _safe_manifest_path(raw.get("path"))
        checksum = raw.get("sha256")
        if (
            path in seen
            or not isinstance(checksum, str)
            or not _SHA256_RE.fullmatch(checksum)
        ):
            raise DatasetIntegrityError("Manifest file entry is malformed.")
        numeric = (raw.get("size_bytes"), raw.get("width"), raw.get("height"))
        if any(type(value) is not int or value < 0 for value in numeric):
            raise DatasetIntegrityError("Manifest file entry is malformed.")
        image_format = raw.get("format")
        if image_format not in SUPPORTED_IMAGE_FORMATS:
            raise DatasetIntegrityError("Manifest file entry is malformed.")
        seen.add(path)
        validated.append(raw)
    return validated


def load_manifest(manifest_path: str | os.PathLike[str]) -> dict[str, Any]:
    """Load and structurally validate a UTF-8 JSON manifest."""
    try:
        payload = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise DatasetIntegrityError(
            "Manifest is missing, unreadable, or malformed."
        ) from None
    _validate_manifest(payload)
    return payload


def verify_dataset(
    dataset_root: str | os.PathLike[str],
    manifest: Mapping[str, Any] | str | os.PathLike[str],
) -> VerificationResult:
    """Verify current dataset state against a manifest without changing either."""
    try:
        payload = (
            load_manifest(manifest)
            if isinstance(manifest, (str, os.PathLike))
            else dict(manifest)
        )
        entries = _validate_manifest(payload)
    except DatasetIntegrityError as exc:
        return VerificationResult(
            0, (IntegrityIssue("malformed_manifest", "<manifest>", str(exc)),), ()
        )

    root = Path(dataset_root)
    if not root.is_dir() or root.is_symlink():
        return VerificationResult(
            0,
            (
                IntegrityIssue(
                    "invalid_root", "<dataset>", "Dataset root is not a safe directory."
                ),
            ),
            (),
        )
    root = root.resolve()
    discovered, issues = _discover_images(root)
    actual_paths = {_relative_path(root, path): path for path in discovered}
    expected = {entry["path"]: entry for entry in entries}

    for path in sorted(expected.keys() - actual_paths.keys()):
        issues.append(
            IntegrityIssue("missing_file", path, "Expected image is missing.")
        )
    for path in sorted(actual_paths.keys() - expected.keys()):
        issues.append(
            IntegrityIssue(
                "unexpected_file", path, "Image is not present in the manifest."
            )
        )

    checked_entries: list[dict[str, Any]] = []
    for relative in sorted(expected.keys() & actual_paths.keys()):
        path = actual_paths[relative]
        entry = expected[relative]
        try:
            resolved = path.resolve(strict=True)
            if not resolved.is_relative_to(root) or path.is_symlink():
                issues.append(
                    IntegrityIssue(
                        "unsafe_path",
                        relative,
                        "Image resolves outside the dataset root.",
                    )
                )
                continue
            metadata = _inspect_image(path)
            size = path.stat().st_size
            checksum = compute_sha256(path)
        except DatasetIntegrityError as exc:
            issues.append(IntegrityIssue("corrupt_file", relative, str(exc)))
            continue
        except OSError:
            issues.append(
                IntegrityIssue(
                    "filesystem_error", relative, "Image file could not be read."
                )
            )
            continue

        checked_entries.append({"path": relative, "sha256": checksum})
        if checksum != entry["sha256"]:
            issues.append(
                IntegrityIssue(
                    "checksum_mismatch", relative, "SHA-256 checksum does not match."
                )
            )
        if size != entry["size_bytes"]:
            issues.append(
                IntegrityIssue("size_mismatch", relative, "File size does not match.")
            )
        for field in ("width", "height", "format"):
            if metadata[field] != entry[field]:
                issues.append(
                    IntegrityIssue(
                        "metadata_mismatch", relative, "Image metadata does not match."
                    )
                )
                break

    issues.sort(key=lambda issue: (issue.path, issue.code))
    return VerificationResult(
        len(checked_entries), tuple(issues), _duplicates(checked_entries)
    )
