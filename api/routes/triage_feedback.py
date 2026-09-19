"""API router for Merchant Human-in-the-Loop Triage Feedback & RLHF Ingestion."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Query, Response
from pydantic import BaseModel, Field

from core.rlhf.feedback_store import feedback_store

router = APIRouter(prefix="/api/v1/triage", tags=["RLHF & Triage Feedback"])


class TriageFeedbackRequest(BaseModel):
    """Payload submitted when a human reviewer takes a triage action (Space / X)."""

    verification_id: Optional[str] = Field(None, description="Optional ID of the verification audited")
    model_score: float = Field(..., description="Automated risk score (0-100 percentage or 0.0-1.0 float)")
    model_verdict: str = Field(..., description="Engine verdict (e.g. AUTHENTIC, SUSPICIOUS, HIGH_RISK_TAMPERED)")
    human_action: str = Field(..., description="Action taken by human expert: APPROVE or FLAG_FRAUD")
    slip_hash: Optional[str] = Field(None, description="SHA-256 hash of slip pixels for deduplication")
    amount: Optional[float] = Field(None, description="Transaction amount for asymmetric loss weighting")
    notes: Optional[str] = Field(None, description="Reviewer notes or comments")


class TriageFeedbackResponse(BaseModel):
    status: str
    feedback_id: str
    reward: float
    human_override: bool
    created_at: str


@router.post("/feedback", response_model=TriageFeedbackResponse)
def submit_triage_feedback(payload: TriageFeedbackRequest):
    """
    Ingest human reviewer feedback (Space / X action) into the active learning buffer
    and compute instantaneous asymmetric business reward.
    """
    record = feedback_store.record_feedback(
        verification_id=payload.verification_id,
        model_score=payload.model_score,
        model_verdict=payload.model_verdict,
        human_action=payload.human_action,
        slip_hash=payload.slip_hash,
        amount=payload.amount,
        notes=payload.notes,
    )

    return TriageFeedbackResponse(
        status="recorded",
        feedback_id=record.feedback_id,
        reward=record.reward,
        human_override=record.human_override,
        created_at=record.created_at,
    )


@router.get("/feedback/stats")
def get_triage_stats() -> Dict[str, Any]:
    """Return operational summary stats: agreement rate, overrides, and cumulative reward."""
    return feedback_store.get_stats()


@router.get("/feedback/recent")
def list_recent_feedback(limit: int = Query(20, ge=1, le=200)) -> List[Dict[str, Any]]:
    """Return recent human review records."""
    records = feedback_store.list_records(limit=limit)
    return [r.to_dict() for r in records]


@router.get("/feedback/export")
def export_dpo_preferences(format: str = Query("json", pattern="^(json|jsonl)$")):
    """
    Export human triage decisions formatted as Direct Preference Optimization (DPO) training pairs.
    """
    pairs = feedback_store.export_dpo_preference_pairs()
    if format == "jsonl":
        import json
        lines = [json.dumps(p) for p in pairs]
        content = "\n".join(lines)
        return Response(content=content, media_type="application/x-ndjson")
    return {"preference_pairs": pairs, "total_pairs": len(pairs)}
