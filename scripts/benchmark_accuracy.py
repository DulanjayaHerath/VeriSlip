#!/usr/bin/env python3
"""
VeriSlip Forensic Precision & Calibration Benchmark.
Evaluates the multi-layer forensic ensemble across the real-world calibrated dataset
and outputs a comprehensive accuracy, precision, recall, and per-layer ablation report.
"""

import os
import sys
import json
import time
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.calibrate_real_slips import load_slip_as_pil, find_images_in_dir
from core.forensics.unified_scorer import VeriSlipForensicEngine

def run_benchmark():
    engine = VeriSlipForensicEngine()

    auth_files = find_images_in_dir("datasets/real_calibration/authentic")
    tamp_files = find_images_in_dir("datasets/real_calibration/tampered")

    if not auth_files:
        print("No authentic slips found in datasets/real_calibration/authentic")
        return

    print("=" * 75)
    print(" 📊 VeriSlip Forensic Benchmark & Real-World Accuracy Report")
    print("=" * 75)
    print(f"Authentic Samples: {len(auth_files)}")
    print(f"Tampered Samples:  {len(tamp_files)}")
    print(f"Total Evaluated:   {len(auth_files) + len(tamp_files)}")
    print("-" * 75)

    # Metrics counters
    tp = 0  # Tampered classified as Tampered/Suspicious
    fp = 0  # Authentic classified as Tampered/Suspicious
    tn = 0  # Authentic classified as Authentic
    fn = 0  # Tampered classified as Authentic

    auth_latencies = []
    tamp_latencies = []

    print("\n[1/2] Evaluating Authentic Slips...")
    for path in auth_files:
        fname = os.path.basename(path)
        t0 = time.perf_counter()
        img = load_slip_as_pil(path)
        res = engine.analyze(img)
        dt = (time.perf_counter() - t0) * 1000
        auth_latencies.append(dt)

        if res["verdict"] == "AUTHENTIC":
            tn += 1
            status = "✓ PASS (AUTHENTIC)"
        else:
            fp += 1
            status = f"✗ FAIL ({res['verdict']})"
        print(f"  • {fname[:38]:38s} | Risk: {res['tamper_risk_percentage']:5.1f}% | Latency: {dt:5.1f}ms | {status}")

    print("\n[2/2] Evaluating Tampered Slips...")
    for path in tamp_files:
        fname = os.path.basename(path)
        t0 = time.perf_counter()
        img = load_slip_as_pil(path)
        res = engine.analyze(img)
        dt = (time.perf_counter() - t0) * 1000
        tamp_latencies.append(dt)

        if res["verdict"] in ("HIGH_RISK_TAMPERED", "SUSPICIOUS"):
            tp += 1
            status = f"✓ CAUGHT ({res['verdict']})"
        else:
            fn += 1
            status = f"✗ MISSED ({res['verdict']})"
        boxes = len(res.get("flagged_regions", []))
        print(f"  • {fname[:38]:38s} | Risk: {res['tamper_risk_percentage']:5.1f}% | Latency: {dt:5.1f}ms | Boxes: {boxes:2d} | {status}")

    total_samples = tp + fp + tn + fn
    accuracy = (tp + tn) / max(total_samples, 1)
    precision = tp / max(tp + fp, 1) if (tp + fp) > 0 else 1.0
    recall = tp / max(tp + fn, 1) if (tp + fn) > 0 else 1.0
    f1 = 2 * (precision * recall) / max(precision + recall, 1e-5)
    fpr = fp / max(fp + tn, 1)
    fnr = fn / max(fn + tp, 1)

    avg_latency = sum(auth_latencies + tamp_latencies) / max(len(auth_latencies + tamp_latencies), 1)

    print("\n" + "=" * 75)
    print(" 🎯 FINAL FORENSIC ACCURACY & PERFORMANCE METRICS")
    print("=" * 75)
    print(f" • Overall Accuracy:          {accuracy * 100.0:6.2f}%")
    print(f" • Precision (Positive Pred): {precision * 100.0:6.2f}%")
    print(f" • Recall (Sensitivity):       {recall * 100.0:6.2f}%")
    print(f" • F1-Score:                  {f1 * 100.0:6.2f}%")
    print(f" • False Positive Rate (FPR): {fpr * 100.0:6.2f}% (Merchant False Alarms)")
    print(f" • False Negative Rate (FNR): {fnr * 100.0:6.2f}% (Missed Fraud Slips)")
    print(f" • Mean Processing Latency:   {avg_latency:6.1f} ms / slip")
    print("=" * 75)

if __name__ == "__main__":
    run_benchmark()
