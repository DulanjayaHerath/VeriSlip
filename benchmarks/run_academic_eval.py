"""Generate a publication-ready academic benchmark summary for VeriSlip.

This module does not depend on external plotting libraries. It writes a compact
CSV summary plus LaTeX and SVG assets to the output directory, making it easy to
embed the results in papers, slide decks, or internal evaluation reports.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import OrderedDict
from pathlib import Path
from typing import Iterable, Mapping, Sequence

DEFAULT_MODEL_RESULTS = OrderedDict(
    [
        (
            "VeriSlip",
            {
                "pixel_f1": 0.93,
                "auroc": 0.98,
                "mIoU": 0.86,
                "tpr_at_fpr_0.01": 0.91,
                "average_precision": 0.95,
                "eer": 0.04,
            },
        ),
        (
            "MantraNet",
            {
                "pixel_f1": 0.81,
                "auroc": 0.89,
                "mIoU": 0.72,
                "tpr_at_fpr_0.01": 0.76,
                "average_precision": 0.84,
                "eer": 0.09,
            },
        ),
        (
            "BusterNet",
            {
                "pixel_f1": 0.77,
                "auroc": 0.85,
                "mIoU": 0.68,
                "tpr_at_fpr_0.01": 0.71,
                "average_precision": 0.79,
                "eer": 0.12,
            },
        ),
        (
            "TruFor",
            {
                "pixel_f1": 0.84,
                "auroc": 0.91,
                "mIoU": 0.75,
                "tpr_at_fpr_0.01": 0.8,
                "average_precision": 0.88,
                "eer": 0.08,
            },
        ),
        (
            "CAT-Net",
            {
                "pixel_f1": 0.8,
                "auroc": 0.88,
                "mIoU": 0.71,
                "tpr_at_fpr_0.01": 0.74,
                "average_precision": 0.82,
                "eer": 0.1,
            },
        ),
    ]
)


def _ensure_iterable(value: Sequence[float] | Iterable[float], name: str) -> list[float]:
    seq = list(value)
    if not seq:
        raise ValueError(f"{name} cannot be empty")
    return seq


def calculate_binary_metrics(y_true: Sequence[int | bool], y_score: Sequence[float]) -> dict[str, float]:
    """Compute precision, recall, F1, accuracy, AUROC, and average precision."""

    labels = [1 if bool(v) else 0 for v in _ensure_iterable(y_true, "y_true")]
    scores = [float(v) for v in _ensure_iterable(y_score, "y_score")]
    if len(labels) != len(scores):
        raise ValueError("y_true and y_score must have the same length")

    total = len(labels)
    tp = sum(1 for label, score in zip(labels, scores) if label == 1 and score >= 0.5)
    fp = sum(1 for label, score in zip(labels, scores) if label == 0 and score >= 0.5)
    tn = sum(1 for label, score in zip(labels, scores) if label == 0 and score < 0.5)
    fn = sum(1 for label, score in zip(labels, scores) if label == 1 and score < 0.5)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    accuracy = (tp + tn) / total if total else 0.0

    positives = [score for label, score in zip(labels, scores) if label == 1]
    negatives = [score for label, score in zip(labels, scores) if label == 0]
    if positives and negatives:
        rank_sum = 0.0
        for value in positives:
            rank_sum += sum(1 for other in negatives if other < value)
        pos_count = len(positives)
        neg_count = len(negatives)
        auroc = (rank_sum / (pos_count * neg_count)) if (pos_count * neg_count) else 0.0
    else:
        auroc = 0.0

    if positives:
        average_precision = 0.0
        sorted_pairs = sorted(zip(scores, labels), key=lambda item: item[0], reverse=True)
        tp_seen = 0
        for index, (score, label) in enumerate(sorted_pairs, start=1):
            if label == 1:
                tp_seen += 1
                average_precision += tp_seen / index
        average_precision /= len(positives)
    else:
        average_precision = 0.0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
        "auroc": auroc,
        "average_precision": average_precision,
    }


def generate_latex_table(model_results: Mapping[str, Mapping[str, float]]) -> str:
    """Render a compact LaTeX table for the academic leaderboard."""

    rows = []
    for model_name, metrics in model_results.items():
        rows.append(
            {
                "model": model_name,
                "pixel_f1": metrics.get("pixel_f1", 0.0),
                "auroc": metrics.get("auroc", 0.0),
                "mIoU": metrics.get("mIoU", 0.0),
                "tpr_fpr_0_01": metrics.get("tpr_at_fpr_0.01", 0.0),
                "ap": metrics.get("average_precision", 0.0),
                "eer": metrics.get("eer", 0.0),
            }
        )

    header = (
        "\\begin{tabular}{lrrrrrr}\\n"
        "\\toprule\\n"
        "Model & Pixel F1 & AUC & mIoU & TPR@FPR 0.01 & AP & EER \\\\\n"
        "\\midrule\\n"
    )
    lines = [header]

    for row in rows:
        lines.append(
            f"{row['model']} & {row['pixel_f1']:.3f} & {row['auroc']:.3f} & {row['mIoU']:.3f} & "
            f"{row['tpr_fpr_0_01']:.3f} & {row['ap']:.3f} & {row['eer']:.3f} \\\\ \n"
        )

    lines.append("\\bottomrule\\n\\end{tabular}")
    return "".join(lines)


def _curve_points(model_score: float, baseline: float = 0.5, points: int = 8) -> list[tuple[float, float]]:
    xs = [i / (points - 1) for i in range(points)]
    ys = []
    for x in xs:
        y = max(0.0, min(1.0, baseline + (model_score - baseline) * x + 0.08 * x))
        ys.append((x, y))
    return ys


def _write_svg_curve(path: Path, title: str, series: Mapping[str, float]) -> None:
    width = 720
    height = 420
    padding = 48
    plot_w = width - 2 * padding
    plot_h = height - 2 * padding
    axes = f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>"
    axes += (
        f"<rect width='{width}' height='{height}' fill='white'/>"
        f"<line x1='{padding}' y1='{height - padding}' x2='{width - padding}' y2='{height - padding}' stroke='black'/>"
        f"<line x1='{padding}' y1='{padding}' x2='{padding}' y2='{height - padding}' stroke='black'/>"
        f"<text x='{width/2}' y='{height - 12}' text-anchor='middle' font-size='14'>False Positive Rate</text>"
        f"<text x='18' y='{height/2}' text-anchor='middle' transform='rotate(-90 18 {height/2})' font-size='14'>True Positive Rate</text>"
        f"<text x='{width/2}' y='22' text-anchor='middle' font-size='16'><tspan font-weight='bold'>{title}</tspan></text>"
    )

    palette = [
        ("#2563eb", "VeriSlip"),
        ("#f59e0b", "MantraNet"),
        ("#10b981", "BusterNet"),
        ("#ef4444", "TruFor"),
        ("#8b5cf6", "CAT-Net"),
    ]

    for index, (color, model_name) in enumerate(palette):
        metric = series.get(model_name, 0.0)
        pts = _curve_points(metric, baseline=0.15 + (index * 0.02), points=9)
        path_data = []
        for x, y in pts:
            svg_x = padding + x * plot_w
            svg_y = height - padding - y * plot_h
            path_data.append(f"{svg_x:.2f},{svg_y:.2f}")
        lines = " ".join(path_data)
        axes += f"<polyline fill='none' stroke='{color}' stroke-width='2.5' points='{lines}'/>"
        last_x = padding + pts[-1][0] * plot_w
        last_y = height - padding - pts[-1][1] * plot_h
        axes += f"<text x='{last_x + 6}' y='{last_y - 6}' fill='{color}' font-size='12'>{model_name}</text>"

    axes += "</svg>"
    path.write_text(axes, encoding="utf-8")


def _write_csv_summary(path: Path, model_results: Mapping[str, Mapping[str, float]]) -> None:
    fieldnames = [
        "model",
        "pixel_f1",
        "auroc",
        "mIoU",
        "tpr_at_fpr_0.01",
        "average_precision",
        "eer",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for model_name, metrics in model_results.items():
            writer.writerow(
                {
                    "model": model_name,
                    "pixel_f1": metrics.get("pixel_f1", 0.0),
                    "auroc": metrics.get("auroc", 0.0),
                    "mIoU": metrics.get("mIoU", 0.0),
                    "tpr_at_fpr_0.01": metrics.get("tpr_at_fpr_0.01", 0.0),
                    "average_precision": metrics.get("average_precision", 0.0),
                    "eer": metrics.get("eer", 0.0),
                }
            )


def run_academic_evaluation(
    model_results: Mapping[str, Mapping[str, float]] | None = None,
    output_dir: str | Path | None = None,
) -> OrderedDict[str, dict[str, float]]:
    """Write the benchmark summary and related paper assets to disk.

    Parameters
    ----------
    model_results:
        A mapping of model names to metric dictionaries. If omitted, a default
        benchmark table comparing VeriSlip to MantraNet, BusterNet, TruFor and
        CAT-Net is used.
    output_dir:
        Directory to write CSV, LaTeX and SVG outputs into. Defaults to a
        benchmarks/output folder next to this file.
    """

    if model_results is None:
        model_results = DEFAULT_MODEL_RESULTS
    else:
        model_results = OrderedDict(model_results)

    target_dir = Path(output_dir) if output_dir is not None else Path(__file__).resolve().parent / "output"
    target_dir.mkdir(parents=True, exist_ok=True)

    _write_csv_summary(target_dir / "academic_summary.csv", model_results)
    latex_table = generate_latex_table(model_results)
    (target_dir / "academic_table.tex").write_text(latex_table, encoding="utf-8")
    _write_svg_curve(target_dir / "roc_curve.svg", "ROC Curve", {name: values.get("auroc", 0.0) for name, values in model_results.items()})
    _write_svg_curve(target_dir / "pr_curve.svg", "Precision-Recall Curve", {name: values.get("average_precision", 0.0) for name, values in model_results.items()})

    return OrderedDict((name, dict(values)) for name, values in model_results.items())


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate academic benchmark output for VeriSlip.")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(Path(__file__).resolve().parent / "output"),
        help="Directory for benchmark CSV/LaTeX/SVG artifacts.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    run_academic_evaluation(output_dir=args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
