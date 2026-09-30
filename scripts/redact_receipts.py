#!/usr/bin/env python3
"""Redact PII from one receipt image or a directory before dataset ingestion."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.privacy.pii_redaction import (  # noqa: E402
    PIIRedactionError,
    PIIRedactionPipeline,
)
from core.security.image_sanitizer import (  # noqa: E402
    ImageValidationError,
    sanitize_image_bytes,
)

SUPPORTED_SUFFIXES = frozenset({".jpg", ".jpeg", ".png"})


def _input_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(
            candidate
            for candidate in path.iterdir()
            if candidate.is_file() and candidate.suffix.casefold() in SUPPORTED_SUFFIXES
        )
    raise PIIRedactionError("Input path does not exist.")


def redact_path(
    input_path: Path, output_dir: Path, *, method: str = "mask"
) -> tuple[int, int]:
    """Redact eligible files, returning successful and rejected counts.

    Outputs use PNG to discard source metadata. Existing outputs are rejected so
    the command never overwrites originals or previous exports by default.
    """
    source = input_path.resolve()
    destination = output_dir.resolve()
    if source == destination or (source.is_file() and destination == source.parent):
        raise PIIRedactionError("Output directory must be separate from the input.")
    files = _input_files(source)
    destination.mkdir(parents=True, exist_ok=True)
    pipeline = PIIRedactionPipeline()
    completed = rejected = 0
    for source_file in files:
        output_file = destination / f"{source_file.stem}.redacted.png"
        if output_file.exists():
            rejected += 1
            continue
        try:
            image = sanitize_image_bytes(source_file.read_bytes())
            result = pipeline.redact(image, method=method)
            result.image.save(output_file, format="PNG")
            completed += 1
        except (OSError, ImageValidationError, PIIRedactionError):
            rejected += 1
    return completed, rejected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Redact locally detected PII before receipt dataset ingestion."
    )
    parser.add_argument("input", type=Path, help="JPEG/PNG file or directory")
    parser.add_argument("output_dir", type=Path, help="Separate output directory")
    parser.add_argument("--method", choices=("mask", "blur"), default="mask")
    args = parser.parse_args(argv)
    try:
        completed, rejected = redact_path(
            args.input, args.output_dir, method=args.method
        )
    except PIIRedactionError as exc:
        parser.error(str(exc))
    print(f"Redaction complete: {completed} exported, {rejected} rejected.")
    return 0 if rejected == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
