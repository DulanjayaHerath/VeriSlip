"""
Reinforcement Learning from Human Feedback (RLHF) & Triage Feedback Subsystem.
Implements asymmetric fraud cost reward modeling, thread-safe feedback storage,
and DPO preference pair generation for model alignment.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def compute_asymmetric_reward(
    model_score: float,
    human_action: str,
    amount: Optional[float] = None,
    threshold: float = 0.40,
) -> float:
    """
    Calculate an asymmetric business-aligned reward signal based on fraud risk costs:
    - True Positive (Model caught fraud, Human confirmed): +2.0
    - True Negative (Model cleared authentic, Human confirmed): +1.0
    - False Positive (Model flagged false alarm, Human approved): -5.0 (Customer friction)
    - False Negative (Model missed fraud, Human caught it): -10.0 to -25.0 (Monetary loss)
    """
    normalized_score = model_score / 100.0 if model_score > 1.0 else model_score
    normalized_score = max(0.0, min(1.0, float(normalized_score)))

    model_flagged_fraud = normalized_score >= threshold
    human_flagged_fraud = human_action.upper() in ("FLAG", "FLAG_FRAUD", "REJECT", "TAMPERED")

    if model_flagged_fraud and human_flagged_fraud:
        # True Positive: Fraud successfully caught
        return 2.0
    elif (not model_flagged_fraud) and (not human_flagged_fraud):
        # True Negative: Legitimate transaction passed cleanly
        return 1.0
    elif model_flagged_fraud and (not human_flagged_fraud):
        # False Positive: False alarm on authentic customer
        return -5.0
    else:
        # False Negative: Missed fraud slip (severe business cost)
        base_penalty = -10.0
        if amount and amount > 10_000:
            extra_penalty = min(15.0, ((amount - 10_000) / 10_000) * 1.5)
            return round(base_penalty - extra_penalty, 2)
        return base_penalty


@dataclass(frozen=True)
class TriageFeedbackRecord:
    """Immutable audit record representing one human triage decision."""

    feedback_id: str
    created_at: str
    verification_id: Optional[str]
    slip_hash: Optional[str]
    model_score: float
    model_verdict: str
    human_action: str
    human_override: bool
    reward: float
    amount: Optional[float] = None
    merchant_id: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class InMemoryTriageFeedbackStore:
    """Thread-safe store for human triage feedback with optional JSONL append logging."""

    def __init__(self, log_path: Optional[Path] = None) -> None:
        self._lock = threading.Lock()
        self._records: List[TriageFeedbackRecord] = []
        self.log_path = log_path or Path("datasets/rlhf_feedback/triage_feedback.jsonl")

        # Ensure directory exists if path is provided
        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            self._load_existing_records()

    def _load_existing_records(self) -> None:
        if not self.log_path or not self.log_path.exists():
            return
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        self._records.append(TriageFeedbackRecord(**data))
        except Exception:
            # Fall back cleanly if file is unreadable
            pass

    def record_feedback(
        self,
        *,
        verification_id: Optional[str],
        model_score: float,
        model_verdict: str,
        human_action: str,
        slip_hash: Optional[str] = None,
        amount: Optional[float] = None,
        merchant_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> TriageFeedbackRecord:
        """Record a human reviewer action and calculate asymmetric alignment reward."""
        normalized_score = model_score / 100.0 if model_score > 1.0 else model_score
        normalized_score = max(0.0, min(1.0, float(normalized_score)))

        model_flagged_fraud = normalized_score >= 0.40
        human_flagged_fraud = human_action.upper() in ("FLAG", "FLAG_FRAUD", "REJECT", "TAMPERED")
        human_override = model_flagged_fraud != human_flagged_fraud

        reward = compute_asymmetric_reward(
            model_score=normalized_score,
            human_action=human_action,
            amount=amount,
        )

        record = TriageFeedbackRecord(
            feedback_id=str(uuid.uuid4()),
            created_at=datetime.now(timezone.utc).isoformat(),
            verification_id=verification_id,
            slip_hash=slip_hash,
            model_score=round(normalized_score, 4),
            model_verdict=str(model_verdict),
            human_action=human_action.upper(),
            human_override=human_override,
            reward=reward,
            amount=amount,
            merchant_id=merchant_id,
            notes=notes,
        )

        with self._lock:
            self._records.append(record)
            if self.log_path:
                try:
                    with open(self.log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps(record.to_dict()) + "\n")
                except Exception:
                    pass

        return record

    def list_records(self, limit: int = 100) -> List[TriageFeedbackRecord]:
        with self._lock:
            return list(self._records[-limit:])

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            total = len(self._records)
            if total == 0:
                return {
                    "total_reviews": 0,
                    "human_approvals": 0,
                    "human_flags": 0,
                    "human_overrides": 0,
                    "agreement_rate": 1.0,
                    "cumulative_reward": 0.0,
                    "average_reward": 0.0,
                }

            approvals = sum(1 for r in self._records if r.human_action in ("APPROVE", "AUTHENTIC"))
            flags = sum(1 for r in self._records if r.human_action in ("FLAG", "FLAG_FRAUD", "REJECT"))
            overrides = sum(1 for r in self._records if r.human_override)
            cumulative_reward = sum(r.reward for r in self._records)
            agreement_rate = (total - overrides) / total

            return {
                "total_reviews": total,
                "human_approvals": approvals,
                "human_flags": flags,
                "human_overrides": overrides,
                "agreement_rate": round(agreement_rate, 4),
                "cumulative_reward": round(cumulative_reward, 2),
                "average_reward": round(cumulative_reward / total, 2),
            }

    def export_dpo_preference_pairs(self) -> List[Dict[str, Any]]:
        """
        Format triage feedback into Direct Preference Optimization (DPO) pairs:
        (prompt, chosen decision, rejected decision, margin).
        """
        pairs = []
        with self._lock:
            for r in self._records:
                prompt = (
                    f"Evaluate receipt slip [hash: {r.slip_hash or 'unknown'}]. "
                    f"Automated risk estimate: {r.model_score * 100:.1f}%, initial verdict: {r.model_verdict}."
                )
                if r.human_override:
                    chosen = f"Human Expert Action: {r.human_action}"
                    rejected = f"Automated Action: {r.model_verdict}"
                else:
                    chosen = f"Consensus Action: {r.human_action}"
                    rejected = "OPPOSITE_ACTION"

                pairs.append({
                    "feedback_id": r.feedback_id,
                    "prompt": prompt,
                    "chosen": chosen,
                    "rejected": rejected,
                    "reward": r.reward,
                    "margin": abs(r.reward),
                    "human_override": r.human_override,
                })
        return pairs


# Global singleton instance
feedback_store = InMemoryTriageFeedbackStore()
