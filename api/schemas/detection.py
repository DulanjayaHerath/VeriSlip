"""
Pydantic Schemas for VeriSlip API requests and responses.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    box: List[int] = Field(..., description="[x, y, width, height]")
    confidence: float
    label: str

class LayerScore(BaseModel):
    score: float
    is_anomalous: bool
    findings: List[str]

class VerificationResponse(BaseModel):
    verdict: str = Field(..., description="AUTHENTIC, SUSPICIOUS, or HIGH_RISK_TAMPERED")
    verdict_color: str
    tamper_risk_percentage: float
    confidence_score: float
    recommendation: str
    flagged_regions: List[BoundingBox]
    findings_summary: List[str]
    layer_breakdowns: Dict[str, Any]
    forensic_maps: Optional[Dict[str, Optional[str]]] = None

class SyntheticSlipResponse(BaseModel):
    bank_code: str
    is_tampered: bool
    tamper_type: Optional[str]
    image_base64: str
    metadata: Dict[str, Any]
