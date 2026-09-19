"""
Unit and integration tests for the VeriSlip RLHF and Human-in-the-Loop Active Learning pipeline.
"""

from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from api.main import app
from core.rlhf.feedback_store import (
    InMemoryTriageFeedbackStore,
    compute_asymmetric_reward,
    feedback_store,
)
from scripts.optimize_rlhf_policy import evaluate_policy, optimize_threshold

client = TestClient(app, headers={"X-API-Key": "test-pro-key"})


def test_asymmetric_reward_matrix():
    # 1. True Positive: Caught fraud confirmed
    reward_tp = compute_asymmetric_reward(model_score=0.85, human_action="FLAG_FRAUD")
    assert reward_tp == 2.0

    # 2. True Negative: Clean authentic approved
    reward_tn = compute_asymmetric_reward(model_score=0.08, human_action="APPROVE")
    assert reward_tn == 1.0

    # 3. False Positive: False alarm on authentic customer (merchant friction)
    reward_fp = compute_asymmetric_reward(model_score=0.70, human_action="APPROVE")
    assert reward_fp == -5.0

    # 4. False Negative: Missed fraud slip (direct loss)
    reward_fn_small = compute_asymmetric_reward(model_score=0.12, human_action="FLAG_FRAUD", amount=5000.0)
    assert reward_fn_small == -10.0

    # 5. False Negative on high-value transfer: Scaled financial penalty
    reward_fn_large = compute_asymmetric_reward(model_score=0.12, human_action="FLAG_FRAUD", amount=60000.0)
    assert reward_fn_large < -15.0


def test_feedback_store_recording_and_stats(tmp_path: Path):
    log_file = tmp_path / "triage_feedback.jsonl"
    store = InMemoryTriageFeedbackStore(log_path=log_file)

    r1 = store.record_feedback(
        verification_id="verif-1",
        model_score=0.10,
        model_verdict="AUTHENTIC",
        human_action="APPROVE",
    )
    assert r1.reward == 1.0
    assert r1.human_override is False

    r2 = store.record_feedback(
        verification_id="verif-2",
        model_score=0.85,
        model_verdict="HIGH_RISK_TAMPERED",
        human_action="APPROVE",  # Overrule model!
    )
    assert r2.reward == -5.0
    assert r2.human_override is True

    stats = store.get_stats()
    assert stats["total_reviews"] == 2
    assert stats["human_approvals"] == 2
    assert stats["human_overrides"] == 1
    assert stats["agreement_rate"] == 0.5
    assert stats["cumulative_reward"] == -4.0

    # Verify JSONL disk persistence
    assert log_file.exists()
    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2


def test_dpo_preference_pairs_export(tmp_path: Path):
    store = InMemoryTriageFeedbackStore(log_path=tmp_path / "test.jsonl")
    store.record_feedback(
        verification_id="v-100",
        model_score=0.90,
        model_verdict="HIGH_RISK_TAMPERED",
        human_action="APPROVE",
        slip_hash="sha256_mock_hash_123",
    )

    pairs = store.export_dpo_preference_pairs()
    assert len(pairs) == 1
    pair = pairs[0]
    assert "prompt" in pair
    assert "sha256_mock_hash_123" in pair["prompt"]
    assert "Human Expert Action: APPROVE" in pair["chosen"]
    assert "Automated Action: HIGH_RISK_TAMPERED" in pair["rejected"]
    assert pair["human_override"] is True
    assert pair["margin"] == 5.0


def test_triage_feedback_api_endpoints():
    # 1. Post valid human triage action
    payload = {
        "verification_id": "test-v-001",
        "model_score": 85.5,
        "model_verdict": "HIGH_RISK_TAMPERED",
        "human_action": "FLAG_FRAUD",
        "slip_hash": "a1b2c3d4e5",
        "amount": 25000.0,
        "notes": "Altered amount digit confirmed",
    }
    response = client.post("/api/v1/triage/feedback", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "recorded"
    assert data["feedback_id"]
    assert data["reward"] == 2.0
    assert data["human_override"] is False

    # 2. Query summary statistics
    stats_resp = client.get("/api/v1/triage/feedback/stats")
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert stats["total_reviews"] >= 1
    assert "cumulative_reward" in stats

    # 3. Query recent reviews
    recent_resp = client.get("/api/v1/triage/feedback/recent?limit=5")
    assert recent_resp.status_code == 200
    recent = recent_resp.json()
    assert len(recent) >= 1
    assert recent[-1]["verification_id"] == "test-v-001"

    # 4. Export DPO pairs as JSON
    export_json = client.get("/api/v1/triage/feedback/export?format=json")
    assert export_json.status_code == 200
    assert "preference_pairs" in export_json.json()

    # 5. Export DPO pairs as JSONL
    export_jsonl = client.get("/api/v1/triage/feedback/export?format=jsonl")
    assert export_jsonl.status_code == 200
    assert export_jsonl.headers["content-type"].startswith("application/x-ndjson")


def test_policy_optimization_kl_regularization():
    records = [
        {"model_score": 0.42, "human_action": "FLAG_FRAUD", "amount": 10000.0},
        {"model_score": 0.38, "human_action": "APPROVE", "amount": 5000.0},
        {"model_score": 0.55, "human_action": "FLAG_FRAUD", "amount": 20000.0},
        {"model_score": 0.15, "human_action": "APPROVE", "amount": 1500.0},
    ]

    opt_thresh, metrics = optimize_threshold(
        records=records,
        beta_kl=2.0,
        baseline_threshold=0.40,
    )
    assert 0.20 <= opt_thresh <= 0.70
    assert "regularized_objective" in metrics
    assert metrics["kl_divergence"] >= 0.0
