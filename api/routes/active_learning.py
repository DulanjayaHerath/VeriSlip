"""
Active Learning & Uncertainty Queue API Routes (#131).
Exposes:
- GET /api/v1/active-learning/queue
- POST /api/v1/active-learning/enqueue
- POST /api/v1/active-learning/annotate
- POST /api/v1/active-learning/trigger-adaptation
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from core.ml.active_learning import (
    UncertaintyQueueManager,
    LoRAAdapterManager,
    compute_shannon_entropy,
    compute_margin_sampling,
)

router = APIRouter(prefix="/api/v1/active-learning", tags=["Active Learning"])
queue_manager = UncertaintyQueueManager()
lora_manager = LoRAAdapterManager()


class EnqueueSlipRequest(BaseModel):
    slip_id: str
    probabilities: List[float] = Field(..., description="[p_authentic, p_tampered]")
    metadata: Optional[Dict[str, Any]] = None


class AnnotateRequest(BaseModel):
    slip_id: str
    human_verdict: str = Field(..., description="AUTHENTIC or HIGH_RISK_TAMPERED")


@router.get("/queue")
def get_uncertainty_queue(limit: int = 50):
    """Retrieve top ambiguous slips queued for expert triage."""
    items = queue_manager.get_pending_queue(limit=limit)
    return {
        "status": "success",
        "pending_count": queue_manager.queue_size(),
        "items": [getattr(item, "model_dump", getattr(item, "dict", None))() for item in items]
    }


@router.post("/enqueue")
def enqueue_slip(req: EnqueueSlipRequest):
    """Evaluate uncertainty metrics and enqueue slip if ambiguous."""
    item = queue_manager.evaluate_and_enqueue(
        slip_id=req.slip_id,
        probabilities=req.probabilities,
        metadata=req.metadata
    )
    return {
        "status": "evaluated",
        "slip_id": item.slip_id,
        "is_ambiguous": item.is_ambiguous,
        "entropy": item.entropy,
        "margin": item.margin,
        "queued": item.is_ambiguous
    }


@router.post("/annotate")
def record_annotation(req: AnnotateRequest):
    """Record expert label on queued ambiguous slip."""
    item = queue_manager.record_human_annotation(req.slip_id, req.human_verdict)
    if not item:
        raise HTTPException(status_code=404, detail="Slip not found in uncertainty queue")
    return {
        "status": "annotated",
        "slip_id": item.slip_id,
        "human_verdict": item.human_verdict,
        "remaining_queue_size": queue_manager.queue_size()
    }


@router.post("/trigger-adaptation")
def trigger_adaptation():
    """Trigger LoRA adapter checkpoint update if enough annotations have been verified."""
    # Gather verified samples
    verified = [
        getattr(item, "model_dump", getattr(item, "dict", None))()
        for item in queue_manager.queue.values()
        if item.human_verdict is not None
    ]
    res = lora_manager.check_and_update_adapter(verified)
    return res
