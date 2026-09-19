"""
Clearing & Settlement API Routes for LankaPay CEFTS (#116).
"""

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from core.integrations.lankapay_cefts import LankaPayCEFTSBridge

router = APIRouter(prefix="/api/v1/clearing", tags=["Clearing & Settlement"])
cefts_bridge = LankaPayCEFTSBridge()


class CEFTSQueryRequest(BaseModel):
    reference_no: str = Field(..., description="Transaction Reference / Retrieval Reference Number (RRN)")
    slip_amount: Optional[float] = Field(None, description="Optional amount on the slip for reconciliation")
    transaction_date: Optional[str] = Field(None, description="Optional ISO timestamp or date")


@router.post("/cefts/query")
def query_cefts_settlement(req: CEFTSQueryRequest):
    """Query national CEFTS switch via ISO 8583 bridge to verify interbank settlement."""
    result = cefts_bridge.reconcile_slip_with_clearing(
        reference_no=req.reference_no,
        slip_amount=req.slip_amount,
        transaction_date=req.transaction_date
    )
    return {
        "status": "success",
        "clearing_gateway": "LankaPay CEFTS",
        **result
    }
