"""
Verification API Route for VeriSlip.
Receives bank slip image uploads, runs multi-layer forensic detection, and returns verdicts.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from PIL import Image
import io

from core.forensics.unified_scorer import VeriSlipForensicEngine
from api.schemas.detection import VerificationResponse

router = APIRouter(prefix="/api/v1", tags=["Verification"])
engine = VeriSlipForensicEngine()

@router.post("/verify", response_model=VerificationResponse)
async def verify_slip(
    file: UploadFile = File(..., description="Payment slip or screenshot image file"),
    bank_code: Optional[str] = Form(None, description="Optional bank code: COMBANK, SAMPATH, BOC, HNB, GENERIC_CEFTS"),
    reference_no: Optional[str] = Form(None, description="Optional transaction reference number for syntax verification")
):
    """
    Run multi-layer forensic analysis on an uploaded payment slip image.
    Returns tamper risk percentage, multi-layer scores, localized bounding boxes, and forensic heatmaps.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image (JPEG, PNG, WebP).")

    try:
        contents = await file.read()
        pil_img = Image.open(io.BytesIO(contents))
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to decode image file: {str(e)}")

    # Run forensics
    try:
        results = engine.analyze(
            pil_image=pil_img,
            bank_code=bank_code,
            reference_no=reference_no
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forensic analysis failed: {str(e)}")
