"""
Forensic Utilities & Synthetic Generation API Routes.
"""

from fastapi import APIRouter, Query
from typing import Optional
import random

from core.ml.dataset_generator import SyntheticSlipGenerator
from core.forensics.utils import pil_to_base64
from api.schemas.detection import SyntheticSlipResponse

router = APIRouter(prefix="/api/v1/forensics", tags=["Forensics & Data"])
generator = SyntheticSlipGenerator()

@router.get("/synthetic-sample", response_model=SyntheticSlipResponse)
def get_synthetic_sample(
    bank_code: str = Query("COMBANK", pattern="^(COMBANK|SAMPATH|BOC|HNB|GENERIC_CEFTS)$"),
    tampered: bool = Query(False, description="Whether to generate a doctored/tampered slip"),
    tamper_type: str = Query("ALTER_AMOUNT", pattern="^(ALTER_AMOUNT|ALTER_REFERENCE)$")
):
    """
    Generate an authentic or doctored bank slip on-the-fly.
    Used for instant live demonstration, automated testing, and model dataset generation.
    """
    sample_amounts = [2500.0, 7850.0, 15000.0, 32400.0, 85000.0]
    names = ["N. P. Fernando", "D. M. Jayasinghe", "S. T. Perera", "R. K. Wickramasinghe"]
    
    amount = random.choice(sample_amounts)
    name = random.choice(names)

    auth_img, metadata = generator.generate_authentic_slip(
        bank_code=bank_code,
        amount_lkr=amount,
        beneficiary_name=name
    )

    if tampered:
        forged_amount = amount * 10.0
        final_img, final_meta = generator.generate_tampered_slip(
            authentic_slip=auth_img,
            metadata=metadata,
            tamper_type=tamper_type,
            new_amount=forged_amount
        )
    else:
        final_img = auth_img
        final_meta = metadata

    b64_str = pil_to_base64(final_img, format="PNG")

    return {
        "bank_code": bank_code,
        "is_tampered": tampered,
        "tamper_type": tamper_type if tampered else None,
        "image_base64": b64_str,
        "metadata": final_meta
    }
