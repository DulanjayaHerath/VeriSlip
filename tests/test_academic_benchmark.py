from pathlib import Path

from benchmarks.run_academic_eval import (
    DEFAULT_MODEL_RESULTS,
    calculate_binary_metrics,
    generate_latex_table,
    run_academic_evaluation,
)


def test_calculate_binary_metrics_basic():
    metrics = calculate_binary_metrics([1, 1, 0, 0], [0.99, 0.80, 0.20, 0.10])

    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1"] == 1.0
    assert metrics["accuracy"] == 1.0
    assert metrics["auroc"] > 0.9
    assert metrics["average_precision"] > 0.9


def test_generate_latex_table_contains_components():
    table = generate_latex_table(DEFAULT_MODEL_RESULTS)

    assert "\\begin{tabular}" in table
    assert "VeriSlip" in table
    assert "Pixel F1" in table
    assert "\\bottomrule" in table


def test_run_academic_evaluation_generates_assets(tmp_path):
    results = run_academic_evaluation(output_dir=tmp_path)

    assert set(results) == set(DEFAULT_MODEL_RESULTS)
    assert (tmp_path / "academic_summary.csv").exists()
    assert (tmp_path / "academic_table.tex").exists()
    assert (tmp_path / "roc_curve.svg").exists()
    assert (tmp_path / "pr_curve.svg").exists()

    csv_text = (tmp_path / "academic_summary.csv").read_text(encoding="utf-8")
    assert "VeriSlip" in csv_text
    assert "MantraNet" in csv_text

    tex_text = (tmp_path / "academic_table.tex").read_text(encoding="utf-8")
    assert "VeriSlip" in tex_text
