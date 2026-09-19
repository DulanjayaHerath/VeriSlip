"""
Machine Learning Subsystem: Active Learning & Uncertainty Sampling (#131).
Implements:
1. Shannon Entropy & Margin Sampling for Ambiguity Scoring.
2. In-Memory Thread-Safe Uncertainty Review Queue.
3. LoRA Low-Rank Adapter weight delta accumulation & checkpoint updating mechanism.
"""

import math
import os
import json
import time
from typing import Dict, Any, List, Optional, Tuple
import threading
from pydantic import BaseModel, Field


def compute_shannon_entropy(probabilities: List[float]) -> float:
    """
    Compute Shannon Entropy: H(x) = -sum(p_i * log2(p_i)).
    Normalized between 0.0 (certain) and 1.0 (maximal uncertainty for binary class).
    """
    if not probabilities:
        return 0.0
    
    total = sum(probabilities)
    if total <= 0:
        return 0.0
    
    norm_probs = [p / total for p in probabilities]
    entropy = 0.0
    for p in norm_probs:
        if p > 1e-9:
            entropy -= p * math.log2(p)
            
    # For binary classification (C=2), max entropy is log2(2) = 1.0
    num_classes = max(2, len(norm_probs))
    max_entropy = math.log2(num_classes)
    return round(float(min(1.0, max(0.0, entropy / max_entropy))), 4)


def compute_margin_sampling(probabilities: List[float]) -> float:
    """
    Compute Margin Sampling: M(x) = p_(1) - p_(2).
    A small margin (<0.15) indicates high classifier ambiguity.
    """
    if not probabilities or len(probabilities) < 2:
        return 1.0

    sorted_p = sorted(probabilities, reverse=True)
    margin = sorted_p[0] - sorted_p[1]
    return round(float(max(0.0, min(1.0, margin))), 4)


class AmbiguousSlipItem(BaseModel):
    slip_id: str
    created_at: float = Field(default_factory=time.time)
    probabilities: List[float]
    entropy: float
    margin: float
    is_ambiguous: bool
    metadata: Dict[str, Any] = Field(default_factory=dict)
    human_verdict: Optional[str] = None
    reviewed_at: Optional[float] = None


class UncertaintyQueueManager:
    """Thread-safe queue holding ambiguous slips for human expert active learning triage."""

    def __init__(
        self,
        entropy_threshold: float = 0.85,
        margin_threshold: float = 0.15,
        queue_file: str = "datasets/active_learning/uncertainty_queue.jsonl"
    ):
        self.entropy_threshold = entropy_threshold
        self.margin_threshold = margin_threshold
        self.queue_file = queue_file
        self.queue: Dict[str, AmbiguousSlipItem] = {}
        self.lock = threading.Lock()

        os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
        self._load_from_disk()

    def evaluate_and_enqueue(
        self,
        slip_id: str,
        probabilities: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> AmbiguousSlipItem:
        """Evaluate slip uncertainty. Enqueues if H(x) > threshold or M(x) < margin."""
        entropy = compute_shannon_entropy(probabilities)
        margin = compute_margin_sampling(probabilities)
        is_ambiguous = (entropy >= self.entropy_threshold) or (margin <= self.margin_threshold)

        item = AmbiguousSlipItem(
            slip_id=slip_id,
            probabilities=probabilities,
            entropy=entropy,
            margin=margin,
            is_ambiguous=is_ambiguous,
            metadata=metadata or {}
        )

        if is_ambiguous:
            with self.lock:
                self.queue[slip_id] = item
                self._persist_item(item)

        return item

    def get_pending_queue(self, limit: int = 50) -> List[AmbiguousSlipItem]:
        """Return pending unreviewed items sorted by uncertainty (highest entropy first)."""
        with self.lock:
            pending = [item for item in self.queue.values() if item.human_verdict is None]
            pending.sort(key=lambda x: x.entropy, reverse=True)
            return pending[:limit]

    def record_human_annotation(self, slip_id: str, verdict: str) -> Optional[AmbiguousSlipItem]:
        """Record human expert label on an ambiguous slip."""
        with self.lock:
            if slip_id in self.queue:
                item = self.queue[slip_id]
                item.human_verdict = verdict
                item.reviewed_at = time.time()
                self._rewrite_all()
                return item
        return None

    def queue_size(self) -> int:
        with self.lock:
            return sum(1 for item in self.queue.values() if item.human_verdict is None)

    def _persist_item(self, item: AmbiguousSlipItem):
        try:
            with open(self.queue_file, "a", encoding="utf-8") as f:
                dump_fn = getattr(item, "model_dump", getattr(item, "dict", None))
                f.write(json.dumps(dump_fn()) + "\n")
        except Exception:
            pass

    def _rewrite_all(self):
        try:
            with open(self.queue_file, "w", encoding="utf-8") as f:
                for item in self.queue.values():
                    dump_fn = getattr(item, "model_dump", getattr(item, "dict", None))
                    f.write(json.dumps(dump_fn()) + "\n")
        except Exception:
            pass

    def _load_from_disk(self):
        if os.path.exists(self.queue_file):
            try:
                with open(self.queue_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            data = json.loads(line)
                            item = AmbiguousSlipItem(**data)
                            self.queue[item.slip_id] = item
            except Exception:
                pass


class LoRAAdapterManager:
    """
    Simulates Low-Rank Adaptation (LoRA) checkpoint weight updating mechanism (#131).
    Accumulates verified samples and produces updated adapter checkpoints
    without requiring full backbone model retraining.
    """

    def __init__(
        self,
        checkpoint_dir: str = "weights/lora_adapters",
        batch_trigger_size: int = 5
    ):
        self.checkpoint_dir = checkpoint_dir
        self.batch_trigger_size = batch_trigger_size
        self.current_version = 1
        os.makedirs(self.checkpoint_dir, exist_ok=True)

    def check_and_update_adapter(self, verified_samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check if enough verified annotations have accumulated to trigger LoRA delta update.
        """
        sample_count = len(verified_samples)
        if sample_count < self.batch_trigger_size:
            return {
                "updated": False,
                "reason": f"Accumulated {sample_count}/{self.batch_trigger_size} samples needed for LoRA update.",
                "adapter_version": self.current_version
            }

        self.current_version += 1
        checkpoint_path = os.path.join(self.checkpoint_dir, f"lora_adapter_v{self.current_version}.json")

        adapter_delta = {
            "adapter_version": self.current_version,
            "timestamp": time.time(),
            "samples_trained": sample_count,
            "rank": 8,
            "lora_alpha": 16,
            "target_modules": ["conv_attention", "fc_projection"],
            "delta_norm": round(0.0124 * math.sqrt(sample_count), 4),
            "status": "CHECKPOINT_ACTIVE"
        }

        with open(checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(adapter_delta, f, indent=2)

        return {
            "updated": True,
            "adapter_version": self.current_version,
            "checkpoint_path": checkpoint_path,
            "samples_incorporated": sample_count
        }
