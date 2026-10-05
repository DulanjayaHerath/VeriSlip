#!/usr/bin/env python3
"""Curate permission-cleared genuine receipt candidates without retaining originals."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.datasets.curation import (  # noqa: E402
    CurationError,
    curate_candidate,
    curation_status,
    finalize_integrity,
)
from core.datasets.integrity import DatasetIntegrityError  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="sanitize and curate one candidate")
    add.add_argument("image", type=Path)
    add.add_argument("metadata", type=Path)
    add.add_argument("output", type=Path)
    finalize = commands.add_parser("finalize", help="write a SHA-256 integrity manifest")
    finalize.add_argument("output", type=Path)
    status = commands.add_parser("status", help="report actual curated counts")
    status.add_argument("output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "add":
            metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
            record = curate_candidate(args.image.read_bytes(), metadata, args.output)
            print(f"Curated {record['sample_id']}.")
        elif args.command == "finalize":
            manifest = finalize_integrity(args.output)
            print(f"Integrity manifest contains {len(manifest['files'])} images.")
        else:
            print(json.dumps(curation_status(args.output), indent=2, sort_keys=True))
    except (OSError, json.JSONDecodeError, CurationError, DatasetIntegrityError) as exc:
        print(f"Curation failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
