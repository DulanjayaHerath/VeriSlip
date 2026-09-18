"""
Layer 2.5 Forensics: Flat Occlusion, Redaction & Pasted Patch Detector.
Identifies solid white/color boxes, markup stickers, and redaction overlays
pasted over banking slip backgrounds, logos, or account information.
"""

from typing import Dict, Any, List, Tuple
from PIL import Image
import numpy as np
import cv2

class Layer2OcclusionDetector:
    """Detector for visual redactions, flat masking patches, and pasted rectangular overlays."""

    def __init__(self):
        pass

    def detect_occlusion_patches(self, cv2_img: np.ndarray) -> List[Dict[str, Any]]:
        """
        Scan image for anomalous uniform rectangular patches placed on contrasting backgrounds.
        """
        h, w, c = cv2_img.shape
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        total_area = h * w

        # Edge detection to identify sharp rectangular boundaries
        edges = cv2.Canny(gray, 40, 140)
        
        # Dilate slightly to connect broken border edges
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(edges, kernel, iterations=1)

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        detected_patches = []

        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            area = bw * bh

            # Filter size: Must be noticeable patch, but not the entire background or full card
            if area < 350 or area > total_area * 0.18:
                continue

            # Skip header zone where bank logos legitimately sit (top 18%)
            if y < h * 0.18:
                continue

            # Aspect ratio sanity
            aspect = bw / max(bh, 1)
            if aspect < 0.25 or aspect > 6.0:
                continue

            # Rectangularity check
            cnt_area = cv2.contourArea(cnt)
            rectangularity = cnt_area / max(area, 1)
            if rectangularity < 0.85:
                continue

            # Extract ROI
            roi = cv2_img[y:y+bh, x:x+bw]
            if roi.size == 0:
                continue

            # Check internal uniformity (standard deviation across color channels)
            std_dev = np.mean([np.std(roi[:, :, ch]) for ch in range(3)])

            # An authentic background in mobile slips is either textured or contains content.
            # A pasted digital whiteout patch has extremely low variance (std_dev < 4.0)
            is_flat_patch = std_dev < 4.5

            # Sample immediate perimeter (5 pixels around the box) to measure contrast with surroundings
            pad = 6
            y1_pad = max(0, y - pad)
            y2_pad = min(h, y + bh + pad)
            x1_pad = max(0, x - pad)
            x2_pad = min(w, x + bw + pad)

            outer_roi = cv2_img[y1_pad:y2_pad, x1_pad:x2_pad]
            if outer_roi.size == 0:
                continue

            mean_patch_color = np.mean(roi, axis=(0, 1))
            mean_outer_color = np.mean(outer_roi, axis=(0, 1))
            border_contrast = np.linalg.norm(mean_patch_color - mean_outer_color)

            # Check 1: Solid flat patch on contrasting background (e.g. White patch on blue/colored background)
            if is_flat_patch and border_contrast > 28.0 and (bw > 25 and bh > 15):
                conf = min(0.95, 0.70 + (border_contrast / 180.0))
                detected_patches.append({
                    "box": [int(x), int(y), int(bw), int(bh)],
                    "confidence": round(conf, 2),
                    "label": "Visual Redaction Patch",
                    "std_dev": round(float(std_dev), 2),
                    "contrast": round(float(border_contrast), 2)
                })

            # Check 2: Unfilled geometric wireframe box pasted on content (e.g. BOC empty account box)
            # Center of the box is empty, but perimeter has thin sharp lines
            if 20 < bw < 120 and 15 < bh < 90:
                inner_pad_y = int(bh * 0.20)
                inner_pad_x = int(bw * 0.20)
                if inner_pad_y > 1 and inner_pad_x > 1:
                    inner_core = gray[y+inner_pad_y:y+bh-inner_pad_y, x+inner_pad_x:x+bw-inner_pad_x]
                    border_ring = np.concatenate([
                        gray[y:y+inner_pad_y, x:x+bw].flatten(),
                        gray[y+bh-inner_pad_y:y+bh, x:x+bw].flatten()
                    ]) if bh > 4 else np.array([])

                    if inner_core.size > 0 and border_ring.size > 0:
                        inner_std = np.std(inner_core)
                        border_darkness = np.mean(inner_core) - np.mean(border_ring)
                        if inner_std < 5.0 and border_darkness > 30.0:
                            detected_patches.append({
                                "box": [int(x), int(y), int(bw), int(bh)],
                                "confidence": 0.88,
                                "label": "Pasted Wireframe Box Overlay",
                                "std_dev": round(float(inner_std), 2),
                                "contrast": round(float(border_darkness), 2)
                            })

        # Remove duplicate or enclosing boxes
        return self._filter_duplicate_patches(detected_patches)

    def _filter_duplicate_patches(self, patches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate nested or identical candidate boxes."""
        if not patches:
            return []
        
        # Sort by confidence descending
        patches = sorted(patches, key=lambda p: p["confidence"], reverse=True)
        kept = []

        def iou(b1, b2):
            x1, y1, w1, h1 = b1
            x2, y2, w2, h2 = b2
            xi1 = max(x1, x2)
            yi1 = max(y1, y2)
            xi2 = min(x1 + w1, x2 + w2)
            yi2 = min(y1 + h1, y2 + h2)
            inter = max(0, xi2 - xi1) * max(0, yi2 - yi1)
            union = (w1 * h1) + (w2 * h2) - inter
            return inter / max(union, 1e-5)

        for p in patches:
            if not any(iou(p["box"], k["box"]) > 0.35 for k in kept):
                kept.append(p)

        return kept

    def evaluate(self, pil_image: Image.Image) -> Dict[str, Any]:
        """Evaluate image for redactions and visual occlusions."""
        cv2_img = cv2.cvtColor(np.array(pil_image.convert("RGB")), cv2.COLOR_RGB2BGR)
        patches = self.detect_occlusion_patches(cv2_img)

        anomaly_score = max([p["confidence"] for p in patches], default=0.0)
        findings = []
        for p in patches:
            findings.append(
                f"{p['label']} detected at [{p['box'][0]}, {p['box'][1]}, {p['box'][2]}x{p['box'][3]}] "
                f"with high contrast ({p['contrast']}) against background."
            )

        return {
            "layer_name": "Layer 2.5: Flat Occlusion & Visual Patch Detector",
            "anomaly_score": round(anomaly_score, 3),
            "is_anomalous": anomaly_score >= 0.70,
            "detected_regions": patches,
            "findings": findings
        }
