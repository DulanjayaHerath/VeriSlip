"""Forensic analysis modules for VeriSlip."""

from core.forensics.anti_spoof import (
    ScreenMoireDetector,
    analyze_moire_pattern,
    analyze_screen_recapture,
    detect_screen_recapture,
    detect_screen_spoofing,
)
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
from core.forensics.thermal_fade import ThermalFadeConfig, ThermalFadeDiscriminator, analyze_thermal_fade

__all__ = [
    "ScreenMoireDetector",
    "analyze_screen_recapture",
    "detect_screen_recapture",
    "detect_screen_spoofing",
    "analyze_moire_pattern",
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
    "ThermalFadeConfig",
    "ThermalFadeDiscriminator",
    "analyze_thermal_fade",
]
