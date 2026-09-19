"""Forensic analysis modules for VeriSlip."""

from core.forensics.steganography import (
    BankWatermarkProfiler,
    SteganographyForensics,
    detect_watermark_disruption,
    extract_bitplane,
    extract_bitplanes,
    profile_authentic_watermark,
    recover_dct_watermark,
)
from core.forensics.xai_gradcam import GradCAMForensics, GradCAMVisualizer, Layer4GradCAM, compute_iou

__all__ = [
    "BankWatermarkProfiler",
    "SteganographyForensics",
    "detect_watermark_disruption",
    "extract_bitplane",
    "extract_bitplanes",
    "profile_authentic_watermark",
    "recover_dct_watermark",
    "Layer4GradCAM",
    "GradCAMForensics",
    "GradCAMVisualizer",
    "compute_iou",
]
