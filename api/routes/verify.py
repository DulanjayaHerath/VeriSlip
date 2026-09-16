"""
Verification API Route for VeriSlip.
Receives bank slip image uploads, runs multi-layer forensic detection, and returns verdicts.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, List
from PIL import Image
import io

from core.forensics.unified_scorer import VeriSlipForensicEngine
from core.forensics.ocr_extractor import ReceiptFieldExtractor
from api.schemas.detection import VerificationResponse, BatchVerificationResponse, BatchSlipItem, BatchVerificationSummary

router = APIRouter(prefix="/api/v1", tags=["Verification"])
engine = VeriSlipForensicEngine()
field_extractor = ReceiptFieldExtractor()

@router.post("/verify", response_model=VerificationResponse)
async def verify_slip(
    file: UploadFile = File(..., description="Payment slip or screenshot image file"),
    bank_code: Optional[str] = Form(None, description="Optional bank code: COMBANK, SAMPATH, BOC, HNB, SEYLAN, NTB_FRIMI, GENERIC_CEFTS"),
    reference_no: Optional[str] = Form(None, description="Optional transaction reference number for syntax verification")
):
    """
    Run multi-layer forensic analysis on an uploaded payment slip image.
    Automatically detects bank layout and key fields if not provided.
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

    # Run field extraction & bank template detection
    extracted_meta = field_extractor.extract_fields(pil_img, bank_hint=bank_code)
    effective_bank = bank_code or extracted_meta["detected_bank_code"]

    # Run multi-layer forensics
    try:
        results = engine.analyze(
            pil_image=pil_img,
            bank_code=effective_bank,
            reference_no=reference_no
        )
        results["extracted_metadata"] = extracted_meta
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forensic analysis failed: {str(e)}")

@router.post("/batch-verify", response_model=BatchVerificationResponse)
async def batch_verify_slips(
    files: List[UploadFile] = File(..., description="Multiple payment slip images for batch forensic audit")
):
    """
    Execute high-throughput batch forensic audit on multiple slip images.
    Returns aggregate fraud rate, individual verdicts, and localized tamper signals.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded for batch verification.")

    if len(files) > 25:
        raise HTTPException(status_code=400, detail="Batch limit is 25 images per request.")

    items: List[BatchSlipItem] = []
    auth_cnt = 0
    susp_cnt = 0
    risk_cnt = 0
    total_risk = 0.0

    for f in files:
        fname = f.filename or "unknown_slip.jpg"
        try:
            contents = await f.read()
            pil_img = Image.open(io.BytesIO(contents))
            if pil_img.mode != "RGB":
                pil_img = pil_img.convert("RGB")

            # Field extraction
            extracted = field_extractor.extract_fields(pil_img)
            effective_bank = extracted["detected_bank_code"]

            # Forensics (lightweight without heavy heatmaps serialization for batch speed)
            res = engine.analyze(
                pil_image=pil_img,
                bank_code=effective_bank,
                include_heatmaps=False
            )

            v = res["verdict"]
            risk_pct = res["tamper_risk_percentage"]
            total_risk += risk_pct

            if v == "AUTHENTIC":
                auth_cnt += 1
            elif v == "SUSPICIOUS":
                susp_cnt += 1
            else:
                risk_cnt += 1

            top_find = res["findings_summary"][0] if res["findings_summary"] else "Compliant slip signals"

            items.append(BatchSlipItem(
                filename=fname,
                verdict=v,
                verdict_color=res["verdict_color"],
                tamper_risk_percentage=risk_pct,
                detected_bank=effective_bank,
                bank_name=extracted["bank_name"],
                recommendation=res["recommendation"],
                flagged_regions_count=len(res.get("flagged_regions", [])),
                findings_count=len(res.get("findings_summary", [])),
                top_finding=top_find,
                extracted_metadata=extracted
            ))
        except Exception as err:
            items.append(BatchSlipItem(
                filename=fname,
                verdict="ERROR",
                verdict_color="#ef4444",
                tamper_risk_percentage=100.0,
                detected_bank="UNKNOWN",
                bank_name="Unknown Bank",
                recommendation=f"Error parsing file: {str(err)}",
                flagged_regions_count=0,
                findings_count=1,
                top_finding="Unreadable or corrupt image file"
            ))
            risk_cnt += 1

    total_proc = len(items)
    avg_risk = round(total_risk / max(total_proc, 1), 1)
    fraud_rate = round(((susp_cnt + risk_cnt) / max(total_proc, 1)) * 100, 1)

    summary = BatchVerificationSummary(
        total_processed=total_proc,
        authentic_count=auth_cnt,
        suspicious_count=susp_cnt,
        high_risk_count=risk_cnt,
        avg_risk_percentage=avg_risk,
        fraud_rate_percentage=fraud_rate
    )

    return BatchVerificationResponse(summary=summary, items=items)
