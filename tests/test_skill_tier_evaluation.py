import csv
import json

import pytest

from benchmarks.skill_tier_eval import (
    SkillTierEvaluationError,
    evaluate_by_skill_tier,
    load_predictions,
    write_reports,
)
from scripts import evaluate_skill_tiers


def _rows():
    return [
        {"sample_id": "n1", "skill_tier": "Novice", "label": 1, "score": 0.9},
        {"sample_id": "n2", "skill_tier": "Novice", "label": 0, "score": 0.1},
        {"sample_id": "i1", "skill_tier": "Intermediate", "label": 1, "score": 0.7},
        {"sample_id": "i2", "skill_tier": "Intermediate", "label": 0, "score": 0.8},
        {"sample_id": "e1", "skill_tier": "Expert", "label": 1, "score": 0.5},
        {"sample_id": "e2", "skill_tier": "Expert", "label": 0, "score": 0.5},
    ]


def test_metrics_and_counts_are_reported_in_stable_tier_order():
    metrics = evaluate_by_skill_tier(_rows())
    assert [item.tier for item in metrics] == ["Novice", "Intermediate", "Expert"]
    assert metrics[0].precision == metrics[0].recall == metrics[0].f1 == 1.0
    assert metrics[1].false_positives == 1
    assert metrics[2].roc_auc == 0.5


def test_threshold_changes_classification_but_not_continuous_auc():
    low = evaluate_by_skill_tier(_rows(), threshold=0.5)[1]
    high = evaluate_by_skill_tier(_rows(), threshold=0.75)[1]
    assert low.roc_auc == high.roc_auc
    assert low.recall != high.recall


def test_single_class_auc_is_absent_not_zero():
    metric = evaluate_by_skill_tier([{"sample_id": "n1", "skill_tier": "Novice", "label": 1, "score": 0.9}])[0]
    assert metric.roc_auc is None


@pytest.mark.parametrize("row_update", [
    {"skill_tier": "Unknown"}, {"label": 2}, {"score": -0.1}, {"score": float("nan")}, {"extra": "field"}
])
def test_invalid_tier_label_score_or_schema_is_rejected(row_update):
    row = _rows()[0] | row_update
    with pytest.raises(SkillTierEvaluationError):
        evaluate_by_skill_tier([row])


def test_duplicate_sample_ids_are_rejected():
    with pytest.raises(SkillTierEvaluationError):
        evaluate_by_skill_tier([_rows()[0], _rows()[0]])


def test_empty_input_and_invalid_threshold_are_rejected():
    with pytest.raises(SkillTierEvaluationError):
        evaluate_by_skill_tier([])
    with pytest.raises(SkillTierEvaluationError):
        evaluate_by_skill_tier(_rows(), threshold=1.1)


def test_reports_are_deterministic_valid_and_mark_single_class_auc(tmp_path):
    metrics = evaluate_by_skill_tier([*_rows(), {"sample_id": "e3", "skill_tier": "Expert", "label": 1, "score": 0.7}])
    write_reports(metrics, tmp_path, threshold=0.5)
    first = (tmp_path / "skill_tier_metrics.json").read_bytes()
    write_reports(metrics, tmp_path, threshold=0.5)
    assert (tmp_path / "skill_tier_metrics.json").read_bytes() == first
    assert json.loads(first)["threshold"] == 0.5
    assert "Novice" in (tmp_path / "skill_tier_metrics.md").read_text()


def test_csv_loader_and_cli_success(tmp_path):
    source = tmp_path / "predictions.csv"
    with source.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("sample_id", "skill_tier", "label", "score"))
        writer.writeheader()
        writer.writerows(_rows())
    assert len(load_predictions(source)) == 6
    output = tmp_path / "report"
    assert evaluate_skill_tiers.main([str(source), str(output)]) == 0
    assert (output / "skill_tier_metrics.csv").exists()


def test_cli_failure_does_not_write_reports(tmp_path):
    source = tmp_path / "bad.csv"
    source.write_text("sample_id,skill_tier,label,score\na,Unknown,1,secret\n", encoding="utf-8")
    output = tmp_path / "report"
    assert evaluate_skill_tiers.main([str(source), str(output)]) == 2
    assert not output.exists()
