"""Deterministic Layer 4 prediction evaluation by tampering skill tier."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from benchmarks.run_academic_eval import calculate_binary_metrics

TIERS = ("Novice", "Intermediate", "Expert")


class SkillTierEvaluationError(ValueError):
    """Raised for invalid evaluation input without exposing row values."""


@dataclass(frozen=True)
class TierMetrics:
    tier: str
    samples: int
    positives: int
    negatives: int
    true_positives: int
    false_positives: int
    true_negatives: int
    false_negatives: int
    precision: float
    recall: float
    f1: float
    roc_auc: float | None


def _auc(labels: list[int], scores: list[float]) -> float | None:
    """Calculate pairwise ROC-AUC with half credit for tied scores."""
    positives = [score for label, score in zip(labels, scores) if label == 1]
    negatives = [score for label, score in zip(labels, scores) if label == 0]
    if not positives or not negatives:
        return None
    wins = sum(
        1.0 if positive > negative else 0.5 if positive == negative else 0.0
        for positive in positives
        for negative in negatives
    )
    return wins / (len(positives) * len(negatives))


def validate_predictions(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Normalize the canonical sample_id/skill_tier/label/score schema."""
    validated: list[dict[str, Any]] = []
    seen: set[str] = set()
    required = {"sample_id", "skill_tier", "label", "score"}
    for index, row in enumerate(rows, 2):
        if set(row) != required:
            raise SkillTierEvaluationError(f"Prediction row {index} has an invalid schema.")
        sample_id = row["sample_id"]
        tier_raw = row["skill_tier"]
        if not isinstance(sample_id, str) or not sample_id.strip() or sample_id in seen:
            raise SkillTierEvaluationError(f"Prediction row {index} has an invalid or duplicate sample ID.")
        if not isinstance(tier_raw, str):
            raise SkillTierEvaluationError(f"Prediction row {index} has an invalid skill tier.")
        tier = next((name for name in TIERS if name.casefold() == tier_raw.strip().casefold()), None)
        if tier is None:
            raise SkillTierEvaluationError(f"Prediction row {index} has an invalid skill tier.")
        try:
            label = int(row["label"])
            score = float(row["score"])
        except (TypeError, ValueError, OverflowError):
            raise SkillTierEvaluationError(f"Prediction row {index} has invalid label or score data.") from None
        if isinstance(row["label"], bool) or str(row["label"]).strip() not in {"0", "1"} or not math.isfinite(score) or not 0 <= score <= 1:
            raise SkillTierEvaluationError(f"Prediction row {index} has invalid label or score data.")
        seen.add(sample_id)
        validated.append({"sample_id": sample_id, "skill_tier": tier, "label": label, "score": score})
    if not validated:
        raise SkillTierEvaluationError("Prediction input is empty.")
    return validated


def evaluate_by_skill_tier(rows: Iterable[Mapping[str, Any]], *, threshold: float = 0.5) -> list[TierMetrics]:
    """Report confusion counts, precision, recall, F1, and ROC-AUC per tier."""
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise SkillTierEvaluationError("Threshold must be between 0 and 1.")
    predictions = validate_predictions(rows)
    results: list[TierMetrics] = []
    for tier in TIERS:
        group = [row for row in predictions if row["skill_tier"] == tier]
        if not group:
            continue
        labels = [row["label"] for row in group]
        scores = [row["score"] for row in group]
        binary_scores = [1.0 if score >= threshold else 0.0 for score in scores]
        shared = calculate_binary_metrics(labels, binary_scores)
        tp = sum(label == 1 and score >= threshold for label, score in zip(labels, scores))
        fp = sum(label == 0 and score >= threshold for label, score in zip(labels, scores))
        tn = sum(label == 0 and score < threshold for label, score in zip(labels, scores))
        fn = sum(label == 1 and score < threshold for label, score in zip(labels, scores))
        results.append(TierMetrics(
            tier=tier, samples=len(group), positives=sum(labels), negatives=len(group) - sum(labels),
            true_positives=tp, false_positives=fp, true_negatives=tn, false_negatives=fn,
            precision=shared["precision"], recall=shared["recall"], f1=shared["f1"], roc_auc=_auc(labels, scores),
        ))
    return results


def load_predictions(path: str | Path) -> list[dict[str, Any]]:
    """Load canonical CSV predictions and validate them."""
    try:
        with Path(path).open(newline="", encoding="utf-8-sig") as handle:
            return validate_predictions(csv.DictReader(handle))
    except OSError:
        raise SkillTierEvaluationError("Prediction file could not be read.") from None


def write_reports(metrics: list[TierMetrics], output_dir: str | Path, *, threshold: float) -> None:
    """Write deterministic JSON, CSV, and Markdown reports without timestamps."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    rows = [asdict(item) for item in metrics]
    payload = {"schema_version": 1, "threshold": threshold, "tiers": rows}
    (output / "skill_tier_metrics.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fields = list(TierMetrics.__annotations__)
    with (output / "skill_tier_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "| Tier | Samples | Precision | Recall | F1 | ROC-AUC |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for item in metrics:
        auc = "N/A (single class)" if item.roc_auc is None else f"{item.roc_auc:.4f}"
        lines.append(f"| {item.tier} | {item.samples} | {item.precision:.4f} | {item.recall:.4f} | {item.f1:.4f} | {auc} |")
    (output / "skill_tier_metrics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
