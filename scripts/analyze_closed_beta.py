#!/usr/bin/env python3
"""Print aggregate results for a local, pseudonymous closed-beta CSV."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.research.closed_beta import PilotDataError, analyse_pilot_csv  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(analyse_pilot_csv(args.csv_file), indent=2, sort_keys=True))
    except PilotDataError as exc:
        print(f"Pilot analysis failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
