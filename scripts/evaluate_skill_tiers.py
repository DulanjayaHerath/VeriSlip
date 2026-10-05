#!/usr/bin/env python3
"""Evaluate validated Layer 4 prediction scores by skill tier."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmarks.skill_tier_eval import (  # noqa: E402
    SkillTierEvaluationError,
    evaluate_by_skill_tier,
    load_predictions,
    write_reports,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args(argv)
    try:
        metrics = evaluate_by_skill_tier(load_predictions(args.predictions), threshold=args.threshold)
        write_reports(metrics, args.output, threshold=args.threshold)
    except (OSError, SkillTierEvaluationError) as exc:
        print(f"Evaluation failed: {exc}", file=sys.stderr)
        return 2
    print(f"Evaluated {sum(item.samples for item in metrics)} predictions across {len(metrics)} tiers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
