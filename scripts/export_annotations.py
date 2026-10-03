#!/usr/bin/env python3
"""Export a VeriSlip synthetic dataset as COCO JSON or Pascal VOC XML."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.datasets.annotations import (  # noqa: E402
    AnnotationExportError,
    load_annotation_dataset,
    write_coco,
    write_voc,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export VeriSlip synthetic annotations to COCO or Pascal VOC."
    )
    parser.add_argument("dataset", type=Path, help="Synthetic dataset directory")
    parser.add_argument("--format", choices=("coco", "voc", "both"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--metadata",
        type=Path,
        help="Optional metadata CSV (defaults to dataset_metadata.csv)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace exporter-owned JSON/XML targets that already exist",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        dataset = load_annotation_dataset(args.dataset, args.metadata)
        annotations = sum(len(image.objects) for image in dataset.images)
        if args.format == "coco":
            write_coco(dataset, args.output, overwrite=args.overwrite)
        elif args.format == "voc":
            write_voc(dataset, args.output, overwrite=args.overwrite)
        else:
            args.output.mkdir(parents=True, exist_ok=True)
            write_coco(
                dataset,
                args.output / "annotations.json",
                overwrite=args.overwrite,
            )
            write_voc(dataset, args.output / "voc", overwrite=args.overwrite)
    except (AnnotationExportError, OSError) as exc:
        print(f"Export failed: {exc}", file=sys.stderr)
        return 1

    print(
        f"Exported {len(dataset.images)} images and {annotations} annotations "
        f"as {args.format.upper()}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
