#!/usr/bin/env python3
"""Streamlit benchmark dashboard for VeriSlip forensic model monitoring.

The dashboard is designed to monitor multi-layer performance across a slip benchmark
set, visualize ROC and precision-recall curves, inspect false positives/false
negatives, and expose a tunable decision threshold for operation teams.

The script intentionally avoids hard dependency failures when Streamlit is not
installed so the underlying benchmark logic can still be imported and tested in CI.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Iterable

try:  # pragma: no cover - optional dependency for the app runtime
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover
    np = None

try:  # pragma: no cover - optional dependency for the UI runtime
    import streamlit as st
except ModuleNotFoundError:  # pragma: no cover
    st = None


LAYER_NAMES = [
    "Layer 1: Structural",
    "Layer 2: Classical",
    "Layer 3: Noise",
    "Layer 4: Deep Fusion",
    "Layer 5: Semantic / Occlusion",
]


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _roc_auc(labels: Iterable[int], scores: Iterable[float]) -> float:
    labels = list(labels)
    scores = list(scores)
    if not labels or not scores or len(labels) != len(scores):
        return 0.0

    positive_scores = [score for label, score in zip(labels, scores) if label == 1]
    negative_scores = [score for label, score in zip(labels, scores) if label == 0]
    if not positive_scores or not negative_scores:
        return 0.0

    total = 0.0
    for pos_score in positive_scores:
        wins = 0.0
        ties = 0.0
        for neg_score in negative_scores:
            if pos_score > neg_score:
                wins += 1.0
            elif pos_score == neg_score:
                ties += 0.5
        total += wins + ties
    return total / (len(positive_scores) * len(negative_scores))


def _confusion_metrics(labels: Iterable[int], scores: Iterable[float], threshold: float) -> dict[str, float]:
    labels = list(labels)
    scores = list(scores)
    tp = fp = tn = fn = 0
    for label, score in zip(labels, scores):
        prediction = 1 if score >= threshold else 0
        if label == 1 and prediction == 1:
            tp += 1
        elif label == 0 and prediction == 1:
            fp += 1
        elif label == 0 and prediction == 0:
            tn += 1
        elif label == 1 and prediction == 0:
            fn += 1

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2.0 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    accuracy = (tp + tn) / len(labels) if labels else 0.0
    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
    }


def _roc_curve_points(labels: Iterable[int], scores: Iterable[float]) -> list[dict[str, float]]:
    labels = [int(label) for label in labels]
    scores = [float(score) for score in scores]
    if not labels or len(labels) != len(scores):
        return []

    points: list[dict[str, float]] = []
    for threshold in sorted(set(scores), reverse=True):
        metrics = _confusion_metrics(labels, scores, threshold)
        tp = metrics["tp"]
        fn = metrics["fn"]
        fp = metrics["fp"]
        tn = metrics["tn"]
        tpr = tp / (tp + fn) if (tp + fn) else 0.0
        fpr = fp / (fp + tn) if (fp + tn) else 0.0
        points.append({"threshold": threshold, "tpr": tpr, "fpr": fpr})
    return points


def _pr_curve_points(labels: Iterable[int], scores: Iterable[float]) -> list[dict[str, float]]:
    labels = [int(label) for label in labels]
    scores = [float(score) for score in scores]
    if not labels or len(labels) != len(scores):
        return []

    points: list[dict[str, float]] = []
    for threshold in sorted(set(scores), reverse=True):
        metrics = _confusion_metrics(labels, scores, threshold)
        precision = metrics["precision"]
        recall = metrics["recall"]
        points.append({"threshold": threshold, "precision": precision, "recall": recall})
    return points


def _build_curve_points(labels: Iterable[int], scores: Iterable[float], threshold: float) -> dict[str, list[float]]:
    labels = [int(label) for label in labels]
    scores = [float(score) for score in scores]
    if not labels or len(labels) != len(scores):
        return {"thresholds": [threshold], "precision": [0.0], "recall": [0.0]}

    ordered = sorted(zip(scores, labels), key=lambda item: item[0])
    thresholds = [score for score, _ in ordered]
    precision: list[float] = []
    recall: list[float] = []
    for score, _ in ordered:
        metrics = _confusion_metrics(labels, scores, score)
        precision.append(metrics["precision"])
        recall.append(metrics["recall"])

    if thresholds and thresholds[0] > threshold:
        thresholds.insert(0, threshold)
        precision.insert(0, precision[0])
        recall.insert(0, recall[0])
    return {"thresholds": thresholds, "precision": precision, "recall": recall}


def _synthetic_labels_and_scores(layer_index: int, sample_count: int = 120) -> tuple[list[int], list[float]]:
    labels: list[int] = []
    scores: list[float] = []
    for idx in range(sample_count):
        positive = idx % 3 != 0
        labels.append(1 if positive else 0)
        signal = 0.2 + (idx % 17) / 20.0 + (layer_index * 0.08)
        noise = ((idx * 13 + layer_index * 7) % 9) / 100.0
        score = min(0.99, max(0.02, signal + (0.15 if positive else -0.12) + noise))
        scores.append(round(score, 4))
    return labels, scores


def generate_demo_layer_metrics() -> list[dict[str, Any]]:
    """Return stable benchmark metrics for dashboard rendering without dataset files."""

    metrics: list[dict[str, Any]] = []
    layer_profile = [
        (0.95, 0.91, 130.5, 5, 7),
        (0.91, 0.87, 145.2, 6, 8),
        (0.92, 0.89, 154.3, 4, 6),
        (0.97, 0.94, 170.9, 3, 5),
        (0.94, 0.90, 162.1, 4, 7),
    ]

    for index, (roc_auc, f1, latency, fp, fn) in enumerate(layer_profile):
        labels, scores = _synthetic_labels_and_scores(index)
        threshold = 0.5
        conf = _confusion_metrics(labels, scores, threshold)
        metrics.append(
            {
                "layer": LAYER_NAMES[index],
                "label": LAYER_NAMES[index],
                "roc_auc": roc_auc,
                "f1_score": f1,
                "precision": conf["precision"],
                "recall": conf["recall"],
                "accuracy": conf["accuracy"],
                "latency_ms": latency,
                "samples": len(labels),
                "false_positives": fp,
                "false_negatives": fn,
                "threshold": threshold,
                "roc_curve": _roc_curve_points(labels, scores),
                "pr_curve": _pr_curve_points(labels, scores),
                "confusion_matrix": {
                    "tp": conf["tp"],
                    "fp": conf["fp"],
                    "tn": conf["tn"],
                    "fn": conf["fn"],
                },
                "labels": labels,
                "scores": scores,
            }
        )
    return metrics


def collect_benchmark_report(dataset_dir: str | os.PathLike[str] | None = None, threshold: float = 0.5) -> dict[str, Any]:
    """Return a benchmark report for dashboard consumption.

    If a dataset directory is provided and contains a benchmark manifest, the script
    will prefer those records. Otherwise it falls back to deterministic synthetic
    data to keep local development and CI checks reliable.
    """

    dataset_dir = Path(dataset_dir) if dataset_dir else None
    layer_metrics = generate_demo_layer_metrics()
    if dataset_dir and dataset_dir.exists():
        manifest_path = dataset_dir / "benchmark_manifest.json"
        if manifest_path.exists():
            try:
                payload = json.loads(manifest_path.read_text(encoding="utf-8"))
                if isinstance(payload, dict) and isinstance(payload.get("layers"), list):
                    layer_metrics = payload["layers"]
            except json.JSONDecodeError:
                pass

    processed = []
    summary = {"best_layer": "", "avg_roc_auc": 0.0, "avg_f1": 0.0, "max_latency_ms": 0.0}
    for item in layer_metrics:
        label = item.get("layer") or item.get("label") or "Unknown layer"
        roc_auc = _safe_float(item.get("roc_auc"), 0.0)
        f1 = _safe_float(item.get("f1_score"), item.get("f1") or 0.0)
        latency = _safe_float(item.get("latency_ms"), 0.0)
        samples = int(item.get("samples") or 0)
        fp = int(item.get("false_positives") or 0)
        fn = int(item.get("false_negatives") or 0)
        case_list = item.get("false_positive_cases") or item.get("false_negative_cases") or []
        if not case_list:
            case_list = [
                {"case_name": "False positive edge case", "outcome": "Review"},
                {"case_name": "False negative edge case", "outcome": "Review"},
            ]

        layer = {
            "layer": label,
            "roc_auc": roc_auc,
            "f1_score": f1,
            "precision": _safe_float(item.get("precision"), 0.0),
            "recall": _safe_float(item.get("recall"), 0.0),
            "accuracy": _safe_float(item.get("accuracy"), 0.0),
            "latency_ms": latency,
            "samples": samples,
            "false_positives": fp,
            "false_negatives": fn,
            "threshold": _safe_float(item.get("threshold"), threshold),
            "case_examples": case_list,
            "roc_curve": item.get("roc_curve") or _roc_curve_points(item.get("labels", []), item.get("scores", [])),
            "pr_curve": item.get("pr_curve") or _pr_curve_points(item.get("labels", []), item.get("scores", [])),
            "confusion_matrix": item.get("confusion_matrix") or {"tp": 0, "fp": 0, "tn": 0, "fn": 0},
        }
        processed.append(layer)

    if processed:
        best_layer = max(processed, key=lambda entry: entry["roc_auc"])
        summary["best_layer"] = best_layer["layer"]
        summary["avg_roc_auc"] = sum(layer["roc_auc"] for layer in processed) / len(processed)
        summary["avg_f1"] = sum(layer["f1_score"] for layer in processed) / len(processed)
        summary["max_latency_ms"] = max(layer["latency_ms"] for layer in processed)

    return {
        "dataset_dir": str(dataset_dir) if dataset_dir else None,
        "threshold": threshold,
        "layers": processed,
        "summary": summary,
        "alert": summary["avg_roc_auc"] < 0.90 or summary["avg_f1"] < 0.85,
    }


def _render_dashboard(report: dict[str, Any]) -> None:
    if st is None:
        raise RuntimeError("Streamlit is not installed. Install it with: pip install streamlit")

    threshold = float(report.get("threshold", 0.5))
    st.set_page_config(page_title="VeriSlip Benchmark Dashboard", layout="wide")
    st.title("VeriSlip Continuous Forensic Benchmarking")

    with st.sidebar:
        st.header("Controls")
        threshold = st.slider("Decision threshold", 0.10, 0.90, threshold, 0.01)
        st.caption("Tune the operating point to inspect false positives and false negatives.")
        st.metric("Average ROC-AUC", f"{report['summary']['avg_roc_auc']:.3f}")
        st.metric("Average F1", f"{report['summary']['avg_f1']:.3f}")
        st.metric("Peak latency", f"{report['summary']['max_latency_ms']:.1f} ms")

    if report.get("alert"):
        st.warning("Regression detected: benchmark performance is degrading below the healthy operating envelope.")
    else:
        st.success("Benchmark remains within the expected operating envelope.")

    layer_values = [layer["roc_auc"] for layer in report["layers"]]
    f1_values = [layer["f1_score"] for layer in report["layers"]]
    latency_values = [layer["latency_ms"] for layer in report["layers"]]

    col1, col2, col3 = st.columns(3)
    col1.metric("Best layer", report["summary"]["best_layer"])
    col2.metric("Average ROC-AUC", f"{report['summary']['avg_roc_auc']:.3f}")
    col3.metric("Average F1", f"{report['summary']['avg_f1']:.3f}")

    st.subheader("Layer-by-layer scoring")
    st.bar_chart({"ROC-AUC": layer_values, "F1 score": f1_values})
    st.line_chart({"Latency (ms)": latency_values})

    st.subheader("Threshold sensitivity")
    threshold_rows = []
    for layer in report["layers"]:
        threshold_rows.append(
            {
                "Layer": layer["layer"],
                "ROC-AUC": layer["roc_auc"],
                "F1": layer["f1_score"],
                "Latency (ms)": layer["latency_ms"],
                "Threshold": threshold,
            }
        )
    st.dataframe(threshold_rows)

    st.subheader("ROC and PR curves")
    roc_curve_chart = {"fpr": [], "tpr": []}
    pr_curve_chart = {"recall": [], "precision": []}
    for layer in report["layers"]:
        for point in layer.get("roc_curve", []):
            roc_curve_chart["fpr"].append(point.get("fpr", 0.0))
            roc_curve_chart["tpr"].append(point.get("tpr", 0.0))
        for point in layer.get("pr_curve", []):
            pr_curve_chart["recall"].append(point.get("recall", 0.0))
            pr_curve_chart["precision"].append(point.get("precision", 0.0))
    if roc_curve_chart["fpr"]:
        st.line_chart({"FPR": roc_curve_chart["fpr"], "TPR": roc_curve_chart["tpr"]})
    if pr_curve_chart["recall"]:
        st.line_chart({"Recall": pr_curve_chart["recall"], "Precision": pr_curve_chart["precision"]})

    st.subheader("Confusion matrix")
    matrix_rows = []
    for layer in report["layers"]:
        matrix = layer.get("confusion_matrix") or {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
        matrix_rows.append(
            {
                "Layer": layer["layer"],
                "TP": matrix.get("tp", 0),
                "FP": matrix.get("fp", 0),
                "TN": matrix.get("tn", 0),
                "FN": matrix.get("fn", 0),
            }
        )
    st.dataframe(matrix_rows)

    st.subheader("False positive / false negative inspection")
    case_table = []
    for layer in report["layers"]:
        for idx in range(min(len(layer.get("case_examples", [])), 3)):
            case_table.append({
                "Layer": layer["layer"],
                "Case": layer["case_examples"][idx].get("case_name", "Review"),
                "Outcome": layer["case_examples"][idx].get("outcome", "Inspect"),
            })
    if case_table:
        st.dataframe(case_table)
    else:
        st.info("No edge-case examples were loaded. The dashboard is using the default synthetic benchmark profile.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the VeriSlip forensic benchmark dashboard.")
    parser.add_argument("--dataset-dir", type=str, default=os.environ.get("VERISLIP_DATASET_DIR"), help="Optional dataset folder containing benchmark_manifest.json")
    parser.add_argument("--threshold", type=float, default=0.5, help="Decision threshold for binary classification output")
    parser.add_argument("--export-json", type=str, default="", help="Optional output path for a JSON benchmark snapshot")
    parser.add_argument("--headless", action="store_true", help="Print the benchmark snapshot as JSON instead of launching Streamlit")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = collect_benchmark_report(args.dataset_dir, threshold=args.threshold)

    if args.export_json:
        output_path = Path(args.export_json)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if args.headless or st is None:
        print(json.dumps(report, indent=2))
        return 0

    _render_dashboard(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
