"""
Unified Forensic Scorer & Multi-Layer Ensemble for VeriSlip.
Aggregates Layer 1 (Structural), Layer 2 (Classical ELA/DCT), and Layer 3 (Noise Forensics)
into a unified tamper risk score, localized bounding boxes, and actionable seller recommendations.
"""

import os
import json
from typing import Dict, Any, List, Optional
from PIL import Image
import numpy as np

from core.forensics.layer1_structural import Layer1StructuralValidator
from core.forensics.layer2_classical import Layer2ClassicalForensics
from core.forensics.layer3_noise import Layer3NoiseForensics
from core.forensics.font_kerning import CharacterAlignmentValidator
from core.ml.ensemble_model import Layer4DeepEnsemble
from core.forensics.utils import normalize_dimensions, pil_to_base64

def merge_bounding_boxes(boxes: List[Dict[str, Any]], iou_thresh: float = 0.3) -> List[Dict[str, Any]]:
    """Merge overlapping bounding boxes from multiple forensic layers using Non-Maximum Suppression (NMS)."""
    if not boxes:
        return []

    # Sort boxes by confidence
    boxes = sorted(boxes, key=lambda b: b.get("confidence", 0.5), reverse=True)
    merged = []

    def iou(b1, b2):
        x1, y1, w1, h1 = b1
        x2, y2, w2, h2 = b2
        xi1 = max(x1, x2)
        yi1 = max(y1, y2)
        xi2 = min(x1 + w1, x2 + w2)
        yi2 = min(y1 + h1, y2 + h2)
        inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
        b1_area = w1 * h1
        b2_area = w2 * h2
        union_area = b1_area + b2_area - inter_area
        return inter_area / max(union_area, 1e-5)

    while boxes:
        current = boxes.pop(0)
        merged.append(current)
        boxes = [b for b in boxes if iou(current["box"], b["box"]) < iou_thresh]

    return merged

class VeriSlipForensicEngine:
    """Master engine orchestrating all detection layers."""

    def __init__(self):
        self.layer1 = Layer1StructuralValidator()
        self.layer2 = Layer2ClassicalForensics()
        self.layer3 = Layer3NoiseForensics()
        self.layer4 = Layer4DeepEnsemble()
        self.font_validator = CharacterAlignmentValidator()
        self.calibration_path = os.environ.get("VERISLIP_CALIBRATION_PATH", "weights/calibration_profile.json")
        self.calibration = None
        self._load_calibration()

    def _load_calibration(self):
        """Load empirical real-world calibration profile if present."""
        if self.calibration_path and os.path.exists(self.calibration_path):
            try:
                with open(self.calibration_path, "r") as f:
                    self.calibration = json.load(f)
                print(f"[VeriSlip Engine] Loaded real-world calibration profile from {self.calibration_path}")
            except Exception as e:
                print(f"[VeriSlip Engine] Warning: Could not load calibration profile: {e}")

    def analyze(
        self,
        pil_image: Image.Image,
        bank_code: Optional[str] = None,
        reference_no: Optional[str] = None,
        include_heatmaps: bool = True
    ) -> Dict[str, Any]:
        """
        Execute multi-layer forensic analysis on payment slip image.
        """
        # Resize if oversized for efficient, responsive inference and guarantee RGB mode
        orig_info = getattr(pil_image, "info", {}).copy()
        normalized_img = normalize_dimensions(pil_image, max_dim=1400).convert("RGB")
        normalized_img.info = orig_info

        # Run layers 1, 2, and 3 + Font Alignment Validator
        l1_res = self.layer1.evaluate(normalized_img, bank_code=bank_code, reference_no=reference_no)
        l2_res = self.layer2.evaluate(normalized_img)
        l3_res = self.layer3.evaluate(normalized_img)
        font_res = self.font_validator.evaluate(normalized_img)

        # Run Layer 4 Deep Learning Ensemble
        diff_gray = l2_res.get("diff_gray", np.zeros((normalized_img.height, normalized_img.width), dtype=np.float32))
        residual = l3_res.get("residual", np.zeros((normalized_img.height, normalized_img.width), dtype=np.float32))
        l4_res = self.layer4.evaluate(normalized_img, diff_gray, residual)

        # Multi-modal fusion weights (dynamically tuned if calibration profile is active)
        if self.calibration and "tuned_weights" in self.calibration:
            tw = self.calibration["tuned_weights"]
            w1 = tw.get("w1_structural", 0.20)
            w2 = tw.get("w2_classical", 0.25)
            w3 = tw.get("w3_noise", 0.25)
            w4 = tw.get("w4_ensemble", 0.30)
        else:
            w1, w2, w3, w4 = 0.20, 0.25, 0.25, 0.30

        weighted_risk = (
            w1 * l1_res["anomaly_score"] +
            w2 * l2_res["anomaly_score"] +
            w3 * l3_res["anomaly_score"] +
            w4 * l4_res["anomaly_score"]
        )

        # Non-Diluting Max-Pooled Fusion:
        # Decisive anomalies override linear dilution, preventing missed tampering
        l4_corroborated = (
            len(l4_res.get("detected_regions", [])) > 0 or
            l1_res["anomaly_score"] > 0.15 or
            l2_res["anomaly_score"] > 0.15 or
            l3_res["anomaly_score"] > 0.20 or
            font_res["anomaly_score"] > 0.40
        )
        peak_signals = [
            weighted_risk,
            l2_res["anomaly_score"] * 0.90 if l2_res["anomaly_score"] > 0.30 else 0.0,
            l3_res["anomaly_score"] * 0.90 if l3_res["anomaly_score"] > 0.35 else 0.0,
            l4_res["anomaly_score"] * 0.92 if (l4_res["anomaly_score"] > 0.70 and l4_corroborated) else 0.0,
            font_res["anomaly_score"] * 0.85 if font_res["anomaly_score"] > 0.65 else 0.0
        ]
        composite_risk = max(peak_signals)

        # Boost risk if editing software was definitively identified in file metadata
        if l1_res["metadata_analysis"]["is_suspicious"]:
            composite_risk = max(composite_risk, 0.75)

        # Collect candidate bounding boxes from all layers
        candidate_boxes = []
        if l2_res.get("is_anomalous", False):
            for box in l2_res.get("detected_regions", []):
                candidate_boxes.append(box)

        if l3_res.get("is_anomalous", False):
            for outlier in l3_res.get("outlier_blocks", []):
                candidate_boxes.append({
                    "box": outlier["box"],
                    "confidence": round(min(0.90, outlier["z_score"] * 0.15) * l3_res["anomaly_score"], 2),
                    "label": "Noise Residual Break"
                })

        for box in l4_res.get("detected_regions", []):
            candidate_boxes.append(box)

        if font_res.get("is_anomalous", False):
            for box in font_res.get("detected_regions", []):
                candidate_boxes.append(box)

        final_boxes = merge_bounding_boxes(candidate_boxes)

        # Corroborated tamper box elevation:
        # Avoid false positives from isolated phantom boxes by requiring multi-layer corroboration
        if final_boxes:
            top_box_conf = max(b.get("confidence", 0.5) for b in final_boxes)
            has_corroborating_evidence = (
                l2_res["anomaly_score"] > 0.15 or
                l3_res["anomaly_score"] > 0.20 or
                l4_res["anomaly_score"] > 0.65 or
                l1_res["metadata_analysis"]["is_suspicious"]
            )
            if top_box_conf > 0.70 and has_corroborating_evidence:
                composite_risk = max(composite_risk, 0.55 + 0.35 * top_box_conf)
            elif top_box_conf > 0.85:
                composite_risk = max(composite_risk, 0.60)

        # Calibrated risk percentage (0 to 100%)
        risk_percentage = round(min(100.0, max(0.0, composite_risk * 100.0)), 1)

        # Determine calibrated thresholds
        auth_ceiling = 25.0
        susp_ceiling = 55.0
        if self.calibration and "thresholds" in self.calibration:
            auth_ceiling = self.calibration["thresholds"].get("authentic_max_risk", 25.0)
            susp_ceiling = self.calibration["thresholds"].get("suspicious_max_risk", 55.0)

        # Determine verdict category
        if risk_percentage <= auth_ceiling:
            verdict = "AUTHENTIC"
            verdict_color = "#10B981"  # Emerald Green
            recommendation = "Low tamper risk. Payment slip appears genuine. Safe to release goods."
        elif risk_percentage <= susp_ceiling:
            verdict = "SUSPICIOUS"
            verdict_color = "#F59E0B"  # Amber Yellow
            recommendation = "Moderate anomalies detected. Recommend checking bank balance before dispatching."
        else:
            verdict = "HIGH_RISK_TAMPERED"
            verdict_color = "#EF4444"  # Red
            recommendation = "High probability of digital tampering. DO NOT ship goods on this slip alone."

        # Collect all findings
        all_findings = []
        all_findings.extend(l1_res.get("findings", []))
        all_findings.extend(l2_res.get("findings", []))
        all_findings.extend(l3_res.get("findings", []))
        all_findings.extend(font_res.get("findings", []))
        all_findings.extend(l4_res.get("findings", []))

        return {
            "verdict": verdict,
            "verdict_color": verdict_color,
            "tamper_risk_percentage": risk_percentage,
            "confidence_score": round(abs(risk_percentage - 50.0) / 50.0, 2),
            "calibration_profile": "Active (Empirical Real-World Profile)" if self.calibration else "Default Calibrated Prior",
            "recommendation": recommendation,
            "flagged_regions": final_boxes[:5],
            "layer_breakdowns": {
                "layer1_structural": {
                    "score": l1_res["anomaly_score"],
                    "is_anomalous": l1_res["is_anomalous"],
                    "findings": l1_res["findings"],
                    "metadata": l1_res["metadata_analysis"],
                    "layout": l1_res["layout_analysis"]
                },
                "layer2_classical": {
                    "score": l2_res["anomaly_score"],
                    "is_anomalous": l2_res["is_anomalous"],
                    "ela_variance": l2_res["ela_variance"],
                    "findings": l2_res["findings"],
                    "double_compression": l2_res["double_compression_analysis"]
                },
                "layer3_noise": {
                    "score": l3_res["anomaly_score"],
                    "is_anomalous": l3_res["is_anomalous"],
                    "mean_noise_variance": l3_res["mean_noise_variance"],
                    "findings": l3_res["findings"]
                },
                "layer4_ensemble": {
                    "score": l4_res["anomaly_score"],
                    "is_anomalous": l4_res["is_anomalous"],
                    "tamper_probability": l4_res.get("tamper_probability", 0.0),
                    "engine": l4_res.get("engine", "Deep Learning"),
                    "findings": l4_res.get("findings", [])
                }
            },
            "forensic_maps": {
                "original_b64": pil_to_base64(normalized_img, format="JPEG"),
                "ela_heatmap_base64": l2_res.get("heatmap_base64"),
                "noise_heatmap_base64": l3_res.get("noise_heatmap_base64")
            } if include_heatmaps else {},
            "findings_summary": all_findings
        }
