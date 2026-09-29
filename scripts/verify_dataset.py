#!/usr/bin/env python3
"""Create or verify deterministic VeriSlip dataset integrity manifests."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.datasets.integrity import (  # noqa: E402
    DatasetIntegrityError,
    build_manifest,
    verify_dataset,
    write_manifest,
)


def _print_issues(issues) -> None:
    for issue in issues:
        print(f"[{issue.code}] {issue.path}: {issue.message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create or verify a SHA-256 manifest for JPEG/PNG dataset images."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("create", "verify"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("dataset_directory", type=Path)
        subparser.add_argument("manifest_file", type=Path)
    args = parser.parse_args(argv)

    if args.command == "create":
        try:
            manifest = build_manifest(args.dataset_directory)
            write_manifest(manifest, args.manifest_file)
        except DatasetIntegrityError as exc:
            _print_issues(exc.issues)
            print(f"Manifest creation failed: {exc}")
            return 1
        duplicate_groups = len(manifest["duplicates"])
        print(
            f"Manifest created: {len(manifest['files'])} images, "
            f"{duplicate_groups} duplicate groups."
        )
        return 0

    result = verify_dataset(args.dataset_directory, args.manifest_file)
    if result.ok:
        print(
            f"Verification succeeded: {result.files_checked} images, "
            f"{len(result.duplicates)} duplicate groups."
        )
        return 0
    _print_issues(result.issues)
    print(f"Verification failed: {len(result.issues)} integrity issue(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
