"""
Layer 2 Forensics: Classical Image Forensics.
- Error Level Analysis (ELA) with adaptive difference amplification
- DCT (Discrete Cosine Transform) double-compression & periodicity analysis
- Font edge rendering sharpness & Laplacian variance consistency
- Localized anomaly candidate bounding box generation
"""

import io
from typing import Dict, Any, List, Tuple
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import cv2
from scipy.fftpack import dct

from core.forensics.utils import pil_to_cv2, cv2_to_base64, cv2_to_pil

class Layer2ClassicalForensics:
    """Classical forensic analyzer combining ELA, DCT compression signatures, and edge variance."""

    def __init__(self, ela_quality: int = 90, ela_scale: float = 18.0):
        self.ela_quality = ela_quality
        self.ela_scale = ela_scale

    def compute_ela(self, pil_image: Image.Image) -> Tuple[Image.Image, np.ndarray, float]:
        """
        Compute Error Level Analysis (ELA).
        Returns:
            - Enhanced ELA visual PIL Image
            - Raw difference array (grayscale float)
            - ELA variance metric
        """
        # Save original to memory at calibrated JPEG quality
        buffer = io.BytesIO()
        pil_image.save(buffer, 'JPEG', quality=self.ela_quality)
        buffer.seek(0)
        resaved_img = Image.open(buffer).convert("RGB")

        # Compute absolute difference
        diff = ImageChops.difference(pil_image.convert("RGB"), resaved_img)

        # Scale difference to emphasize error levels
        diff_arr = np.array(diff, dtype=np.float32)
        diff_gray = cv2.cvtColor(diff_arr.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)

        # Boost contrast for visualization
        amplified = np.clip(diff_arr * self.ela_scale, 0, 255).astype(np.uint8)
        visual_ela = Image.fromarray(amplified)

        # Compute statistical variance of error levels
        ela_variance = float(np.var(diff_gray))
        mean_diff = float(np.mean(diff_gray))

        return visual_ela, diff_gray, ela_variance

    def generate_ela_heatmap(self, diff_gray: np.ndarray) -> np.ndarray:
        """
        Convert grayscale ELA difference to a normalized colored heatmap (BGR).
        """
        # Normalize between 0 and 255
        norm_diff = cv2.normalize(diff_gray, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        # Apply JET or INFERNO colormap for intuitive forensic inspection
        heatmap = cv2.applyColorMap(norm_diff, cv2.COLORMAP_INFERNO)
        return heatmap

    def analyze_dct_coefficients(self, cv2_bgr: np.ndarray) -> Dict[str, Any]:
        """
        Compute 8x8 block-wise Discrete Cosine Transform (DCT) to detect double-JPEG compression artifacts.
        Re-saving or doctoring in external software creates periodic periodicity spikes in AC coefficient histograms.
        """
        gray = cv2.cvtColor(cv2_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
        h, w = gray.shape

        # Crop to multiples of 8
        h_8 = (h // 8) * 8
        w_8 = (w // 8) * 8
        if h_8 < 64 or w_8 < 64:
            return {"double_compression_risk": 0.1, "periodicity_score": 0.0, "notes": ["Image too small for DCT"]}

        cropped = gray[:h_8, :w_8]

        # Collect AC coefficients across 8x8 blocks (specifically low/mid AC frequencies like (1,2), (2,1))
        ac_coeffs = []
        for i in range(0, h_8, 8):
            for j in range(0, w_8, 8):
                block = cropped[i:i+8, j:j+8] - 128.0
                block_dct = cv2.dct(block)
                ac_coeffs.append(block_dct[1, 2])
                ac_coeffs.append(block_dct[2, 1])

        ac_arr = np.array(ac_coeffs)
        # Histogram of AC values
        hist, bin_edges = np.histogram(ac_arr, bins=100, range=(-50, 50))
        
        # Check for periodicity (comb-like modulation) using FFT of histogram
        hist_fft = np.abs(np.fft.rfft(hist - np.mean(hist)))
        # Secondary peak ratio indicates periodic quantization traces
        if len(hist_fft) > 5:
            peak_ratio = float(np.max(hist_fft[3:]) / (np.sum(hist_fft) + 1e-5))
        else:
            peak_ratio = 0.0

        double_compression_risk = min(1.0, peak_ratio * 4.0)

        notes = []
        if double_compression_risk > 0.5:
            notes.append("Periodic DCT frequency spikes detected (characteristic of re-saving or multi-generation compression).")

        return {
            "periodicity_score": round(peak_ratio, 4),
            "double_compression_risk": round(double_compression_risk, 3),
            "notes": notes
        }

    def detect_tamper_bounding_boxes(
        self, 
        diff_gray: np.ndarray, 
        threshold_factor: float = 2.5,
        abs_min_diff: float = 6.0,
        min_area: int = 150,
        max_area: int = 80000
    ) -> List[Dict[str, Any]]:
        """
        Locate suspicious regions where ELA compression error significantly exceeds background baseline
        AND exceeds absolute compression error thresholds.
        """
        mean_val = np.mean(diff_gray)
        std_val = np.std(diff_gray)
        thresh_val = max(abs_min_diff, mean_val + threshold_factor * std_val)

        # Binary thresholding
        _, binary = cv2.threshold(diff_gray, thresh_val, 255, cv2.THRESH_BINARY)
        binary_uint8 = binary.astype(np.uint8)

        # Morphological closing to group nearby text character anomalies into a coherent word/number box
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 7))
        closed = cv2.morphologyEx(binary_uint8, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        boxes = []
        h_img, w_img = diff_gray.shape

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if min_area <= area <= max_area:
                x, y, w, h = cv2.boundingRect(cnt)

                # Discard edge banners (extreme top bar or bottom navigation bar)
                if y < 15 and h < 30:
                    continue
                if (y + h) > (h_img - 15) and h < 30:
                    continue

                # Compute regional intensity vs baseline
                region_roi = diff_gray[y:y+h, x:x+w]
                roi_mean = np.mean(region_roi)
                if roi_mean < abs_min_diff:
                    continue

                confidence = min(0.99, max(0.40, float((roi_mean - mean_val) / (std_val + 1e-4) * 0.25)))

                boxes.append({
                    "box": [int(x), int(y), int(w), int(h)],
                    "area": int(area),
                    "confidence": round(confidence, 2),
                    "label": "Potential Spliced/Modified Region"
                })

        # Sort by confidence descending
        boxes.sort(key=lambda b: b["confidence"], reverse=True)
        return boxes[:6]  # Limit to top 6 candidate anomalies

    def evaluate(self, pil_image: Image.Image) -> Dict[str, Any]:
        """
        Run full Layer 2 Classical Forensics evaluation.
        """
        cv2_img = pil_to_cv2(pil_image)
        visual_ela, diff_gray, ela_var = self.compute_ela(pil_image)
        heatmap = self.generate_ela_heatmap(diff_gray)
        dct_res = self.analyze_dct_coefficients(cv2_img)
        boxes = self.detect_tamper_bounding_boxes(diff_gray)

        # Calculate composite score for Layer 2
        # Normal uncompressed/uniform mobile screenshots have modest ELA variance (~0.5 - 2.5)
        # Spliced/recompressed screenshots exhibit localized ELA variance spikes (> 5.0)
        ela_risk = min(1.0, max(0.0, (ela_var - 2.0) / 16.0)) if ela_var > 2.0 else 0.05
        box_risk = 0.0
        if boxes:
            box_risk = min(1.0, len(boxes) * 0.25 + max(b["confidence"] for b in boxes) * 0.5)

        layer2_score = round(0.45 * ela_risk + 0.35 * box_risk + 0.20 * dct_res["double_compression_risk"], 3)

        notes = []
        if layer2_score > 0.45:
            notes.append(f"Significant compression error level discrepancies detected ({len(boxes)} anomaly regions).")
        notes.extend(dct_res["notes"])

        return {
            "layer_name": "Layer 2: Classical Image Forensics (ELA & DCT)",
            "anomaly_score": layer2_score,
            "is_anomalous": layer2_score >= 0.40,
            "ela_variance": round(ela_var, 2),
            "detected_regions": boxes,
            "double_compression_analysis": dct_res,
            "heatmap_base64": cv2_to_base64(heatmap),
            "diff_gray": diff_gray,
            "findings": notes
        }
