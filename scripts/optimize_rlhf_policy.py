#!/usr/bin/env python3
"""
RLHF & Policy Optimization Script for VeriSlip.
Optimizes the fraud decision boundary threshold and layer fusion weights
by maximizing cumulative expected human preference reward under a KL divergence constraint.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.rlhf.feedback_store import compute_asymmetric_reward, feedback_store


def evaluate_policy(
    records: List[Dict[str, Any]],
    threshold: float,
    beta_kl: float = 2.0,
    baseline_threshold: float = 0.40,
) -> Dict[str, float]:
    """
    Evaluate candidate decision threshold on historical feedback records.
    Objective: Expected Reward - beta * KL_divergence(candidate || baseline)
    """
    if not records:
        return {
            "total_records": 0,
            "cumulative_reward": 0.0,
            "average_reward": 0.0,
            "kl_divergence": 0.0,
            "regularized_objective": 0.0,
        }

    total_reward = 0.0
    for r in records:
        score = r["model_score"]
        action = r["human_action"]
        amount = r.get("amount")
        reward = compute_asymmetric_reward(
            model_score=score,
            human_action=action,
            amount=amount,
            threshold=threshold,
        )
        total_reward += reward

    n = len(records)
    avg_reward = total_reward / n

    # Proxy KL divergence for 1D decision threshold distribution
    # D_KL ~ (theta - theta_0)^2 / (2 * sigma^2)
    kl_penalty = ((threshold - baseline_threshold) ** 2) * 5.0
    regularized_objective = avg_reward - (beta_kl * kl_penalty)

    return {
        "total_records": n,
        "cumulative_reward": round(total_reward, 2),
        "average_reward": round(avg_reward, 4),
        "kl_divergence": round(kl_penalty, 4),
        "regularized_objective": round(regularized_objective, 4),
    }


def optimize_threshold(
    records: List[Dict[str, Any]],
    beta_kl: float = 2.0,
    baseline_threshold: float = 0.40,
    min_thresh: float = 0.20,
    max_thresh: float = 0.70,
    step: float = 0.01,
) -> Tuple[float, Dict[str, float]]:
    """Grid search over threshold space to find optimal business-aligned policy."""
    best_thresh = baseline_threshold
    best_metrics: Dict[str, float] = {}
    best_obj = -float("inf")

    curr = min_thresh
    while curr <= max_thresh + 1e-6:
        metrics = evaluate_policy(
            records=records,
            threshold=curr,
            beta_kl=beta_kl,
            baseline_threshold=baseline_threshold,
        )
        if metrics["regularized_objective"] > best_obj:
            best_obj = metrics["regularized_objective"]
            best_thresh = round(curr, 3)
            best_metrics = metrics
        curr += step

    return best_thresh, best_metrics


def main():
    parser = argparse.ArgumentParser(description="VeriSlip RLHF Policy Optimizer")
    parser.add_argument(
        "--feedback-file",
        type=str,
        default="datasets/rlhf_feedback/triage_feedback.jsonl",
        help="Path to triage feedback JSONL file",
    )
    parser.add_argument(
        "--beta-kl",
        type=float,
        default=1.5,
        help="KL divergence regularization factor against baseline",
    )
    parser.add_argument(
        "--baseline",
        type=float,
        default=0.40,
        help="Baseline calibrated forensic threshold",
    )
    parser.add_argument(
        "--output-profile",
        type=str,
        default=None,
        help="Path to save updated calibration profile JSON",
    )
    args = parser.parse_args()

    feedback_path = Path(args.feedback_file)
    records = []
    if feedback_path.exists():
        with open(feedback_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line.strip()))
    else:
        # Fall back to in-memory store records
        records = [r.to_dict() for r in feedback_store.list_records(limit=1000)]

    print("=" * 65)
    print(" 🤖 VeriSlip RLHF Policy Optimization Report")
    print("=" * 65)
    print(f"Feedback Records Analyzed: {len(records)}")
    print(f"Baseline Threshold:        {args.baseline:.2f}")
    print(f"KL Regularization (Beta):  {args.beta_kl:.2f}")
    print("-" * 65)

    if not records:
        print("ℹ No feedback records collected yet. Using baseline forensic profile.")
        return

    baseline_metrics = evaluate_policy(
        records=records,
        threshold=args.baseline,
        beta_kl=args.beta_kl,
        baseline_threshold=args.baseline,
    )
    print(f"Baseline Average Reward:   {baseline_metrics['average_reward']:.4f}")
    print(f"Baseline Cumulative:       {baseline_metrics['cumulative_reward']:.2f}")

    opt_thresh, opt_metrics = optimize_threshold(
        records=records,
        beta_kl=args.beta_kl,
        baseline_threshold=args.baseline,
    )
    print("-" * 65)
    print(f"🎯 Optimal Policy Threshold: {opt_thresh:.3f}")
    print(f"🚀 Optimized Average Reward: {opt_metrics['average_reward']:.4f}")
    print(f"💰 Optimized Cumulative:     {opt_metrics['cumulative_reward']:.2f}")
    print(f"🛡 KL Divergence Penalty:    {opt_metrics['kl_divergence']:.4f}")
    print("=" * 65)

    if args.output_profile:
        out_p = Path(args.output_profile)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "baseline_threshold": args.baseline,
            "optimized_threshold": opt_thresh,
            "beta_kl": args.beta_kl,
            "records_evaluated": len(records),
            "optimized_metrics": opt_metrics,
        }
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"✓ Saved updated policy profile to {args.output_profile}")


if __name__ == "__main__":
    main()
