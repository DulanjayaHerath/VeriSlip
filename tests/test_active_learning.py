"""
Unit tests for Active Learning subsystem and uncertainty sampling (#131).
"""

import tempfile
import os
from fastapi.testclient import TestClient
from api.main import app
from core.ml.active_learning import (
    compute_shannon_entropy,
    compute_margin_sampling,
    UncertaintyQueueManager,
    LoRAAdapterManager,
)


def test_entropy_and_margin_computation():
    """Verify Shannon entropy and margin sampling mathematical properties."""
    # Completely certain prediction
    assert compute_shannon_entropy([1.0, 0.0]) == 0.0
    assert compute_margin_sampling([1.0, 0.0]) == 1.0

    # Maximally uncertain prediction (coin flip)
    assert compute_shannon_entropy([0.5, 0.5]) == 1.0
    assert compute_margin_sampling([0.5, 0.5]) == 0.0

    # Edge case near boundary
    ambiguous_entropy = compute_shannon_entropy([0.52, 0.48])
    ambiguous_margin = compute_margin_sampling([0.52, 0.48])
    assert ambiguous_entropy > 0.95
    assert ambiguous_margin < 0.10


def test_uncertainty_queue_lifecycle():
    """Verify queueing, persistence, and human annotation lifecycle."""
    with tempfile.TemporaryDirectory() as tmpdir:
        queue_path = os.path.join(tmpdir, "queue.jsonl")
        manager = UncertaintyQueueManager(
            entropy_threshold=0.85,
            margin_threshold=0.15,
            queue_file=queue_path
        )

        # Non-ambiguous slip
        clear_item = manager.evaluate_and_enqueue("slip-clean-1", [0.98, 0.02])
        assert clear_item.is_ambiguous is False
        assert manager.queue_size() == 0

        # Ambiguous slip
        amb_item = manager.evaluate_and_enqueue("slip-amb-1", [0.53, 0.47])
        assert amb_item.is_ambiguous is True
        assert manager.queue_size() == 1

        pending = manager.get_pending_queue()
        assert len(pending) == 1
        assert pending[0].slip_id == "slip-amb-1"

        # Record human annotation
        annotated = manager.record_human_annotation("slip-amb-1", "HIGH_RISK_TAMPERED")
        assert annotated is not None
        assert annotated.human_verdict == "HIGH_RISK_TAMPERED"
        assert manager.queue_size() == 0


def test_lora_adapter_checkpointing():
    """Verify LoRA low-rank adapter delta accumulation mechanism."""
    with tempfile.TemporaryDirectory() as tmpdir:
        lora = LoRAAdapterManager(checkpoint_dir=tmpdir, batch_trigger_size=3)
        # Below batch threshold
        res_below = lora.check_and_update_adapter([{"id": 1}])
        assert res_below["updated"] is False

        # Meet batch threshold
        res_above = lora.check_and_update_adapter([{"id": 1}, {"id": 2}, {"id": 3}])
        assert res_above["updated"] is True
        assert res_above["adapter_version"] == 2
        assert os.path.exists(res_above["checkpoint_path"])


def test_active_learning_api_endpoints():
    """Test REST API endpoints for active learning queue."""
    client = TestClient(app, headers={"X-API-Key": "test-pro-key"})

    # 1. Enqueue an ambiguous slip
    enqueue_resp = client.post(
        "/api/v1/active-learning/enqueue",
        json={"slip_id": "test-slip-42", "probabilities": [0.51, 0.49]}
    )
    assert enqueue_resp.status_code == 200
    data = enqueue_resp.json()
    assert data["queued"] is True
    assert data["is_ambiguous"] is True

    # 2. Get queue
    queue_resp = client.get("/api/v1/active-learning/queue")
    assert queue_resp.status_code == 200
    queue_data = queue_resp.json()
    assert queue_data["pending_count"] >= 1

    # 3. Annotate
    annotate_resp = client.post(
        "/api/v1/active-learning/annotate",
        json={"slip_id": "test-slip-42", "human_verdict": "AUTHENTIC"}
    )
    assert annotate_resp.status_code == 200
    assert annotate_resp.json()["human_verdict"] == "AUTHENTIC"

    # 4. Trigger adaptation endpoint
    adapt_resp = client.post("/api/v1/active-learning/trigger-adaptation")
    assert adapt_resp.status_code == 200
