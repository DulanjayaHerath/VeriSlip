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
    extracted_metadata: Optional[Dict[str, Any]] = None

class SyntheticSlipResponse(BaseModel):
    bank_code: str
    is_tampered: bool
    tamper_type: Optional[str]
    image_base64: str
    metadata: Dict[str, Any]

class BatchSlipItem(BaseModel):
    filename: str
    verdict: str
    verdict_color: str
    tamper_risk_percentage: float
    detected_bank: str
    bank_name: str
    recommendation: str
    flagged_regions_count: int
    findings_count: int
    top_finding: Optional[str] = None
    extracted_metadata: Optional[Dict[str, Any]] = None

class BatchVerificationSummary(BaseModel):
    total_processed: int
    authentic_count: int
    suspicious_count: int
    high_risk_count: int
    avg_risk_percentage: float
    fraud_rate_percentage: float

class BatchVerificationResponse(BaseModel):
    summary: BatchVerificationSummary
    items: List[BatchSlipItem]
