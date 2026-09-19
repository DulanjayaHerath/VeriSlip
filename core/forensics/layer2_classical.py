"""
Layer 2 Forensics: Classical Image Forensics.
- Error Level Analysis (ELA) with adaptive difference amplification
- DCT (Discrete Cosine Transform) double-compression & periodicity analysis
- Font edge rendering sharpness & Laplacian variance consistency
- Localized anomaly candidate bounding box generation
"""

import io
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import cv2
from scipy.fftpack import dct

from core.forensics.utils import pil_to_cv2, cv2_to_base64, cv2_to_pil
from core.forensics.layer2_copymove import (
    detect_copymove_orb,
    detect_copymove_block_dct,
    analyze_copymove_forensics,
)

class Layer2ClassicalForensics:
    """Classical forensic analyzer combining ELA, DCT compression signatures, copy-move detection, and edge variance."""

    def __init__(self, ela_quality: int = 90, ela_scale: float = 18.0):
        self.ela_quality = ela_quality
        self.ela_scale = ela_scale

    def detect_copymove_keypoints(self, cv2_bgr: np.ndarray, **kwargs) -> Dict[str, Any]:
        """Detect copy-move forgery using ORB/SIFT keypoints."""
        return detect_copymove_orb(cv2_bgr, **kwargs)

    def detect_copymove_dct_blocks(self, cv2_bgr: np.ndarray, **kwargs) -> Dict[str, Any]:
        """Detect dense copy-move forgery using block-based DCT correlation."""
        return detect_copymove_block_dct(cv2_bgr, **kwargs)

    def compute_ela(self, pil_image: Image.Image) -> Tuple[Image.Image, np.ndarray, float]:
        """
        Compute Error Level Analysis (ELA).
        Returns:
            - Enhanced ELA visual PIL Image
            - Raw difference array (grayscale float)
            - ELA variance metric
        """
        # Save original to memory at calibrated JPEG quality
        rgb_image = pil_image.convert("RGB")
        buffer = io.BytesIO()
        rgb_image.save(buffer, 'JPEG', quality=self.ela_quality)
        buffer.seek(0)
        resaved_img = Image.open(buffer)

        # Compute absolute difference
        diff = ImageChops.difference(rgb_image, resaved_img)

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

    def decompose_ela_channels(self, pil_image: Image.Image) -> Dict[str, Any]:
        """
        Decompose ELA difference into Luminance (Y) and Chrominance (Cb, Cr) channels.
        In digital receipt tampering (splicing or text alterations), tampered characters typically
        exhibit elevated high-frequency noise in the luminance channel (Y) while chrominance channels
        remain subdued due to chroma subsampling (4:2:0 or 4:2:2 JPEG compression).
        """
        rgb_image = pil_image.convert("RGB")
        buffer = io.BytesIO()
        rgb_image.save(buffer, 'JPEG', quality=self.ela_quality)
        buffer.seek(0)
        resaved_img = Image.open(buffer)

        diff = ImageChops.difference(rgb_image, resaved_img)
        diff_arr = np.array(diff, dtype=np.uint8)

        ycrcb = cv2.cvtColor(diff_arr, cv2.COLOR_RGB2YCrCb).astype(np.float32)
        y_channel = ycrcb[:, :, 0]
        cr_channel = ycrcb[:, :, 1]
        cb_channel = ycrcb[:, :, 2]

        luma_variance = float(np.var(y_channel))
        cr_variance = float(np.var(cr_channel))
        cb_variance = float(np.var(cb_channel))
        chroma_variance = float((cr_variance + cb_variance) / 2.0)

        luma_chroma_disparity = float(luma_variance / (chroma_variance + 1e-4))

        return {
            "luminance_variance": round(luma_variance, 4),
            "chrominance_variance": round(chroma_variance, 4),
            "cr_variance": round(cr_variance, 4),
            "cb_variance": round(cb_variance, 4),
            "luma_chroma_disparity": round(luma_chroma_disparity, 4),
            "luminance_diff": y_channel,
            "chrominance_diff": (cb_channel + cr_channel) / 2.0,
        }

    def detect_jpeg_grid_shift(self, gray: np.ndarray) -> Dict[str, Any]:
        """
        Detect double-JPEG compression grid misalignment and spatial shift (0 to 7 px).
        When a tampered receipt snippet (e.g. amount or reference digits) is cropped and
        pasted into another document, the original 8x8 block DCT boundary is shifted by
        (shift_x, shift_y) != (0, 0), introducing dual periodic boundary traces.
        """
        h, w = gray.shape
        if h < 64 or w < 64 or float(np.std(gray)) < 5.0:
            return {
                "detected_shift": (0, 0),
                "grid_periodicity_strength": 1.0,
                "is_aligned": True,
                "horizontal_grid_profile": [0.0] * 8,
                "vertical_grid_profile": [0.0] * 8,
                "notes": []
            }

        diff_h = np.abs(gray[:, 1:] - gray[:, :-1])
        diff_v = np.abs(gray[1:, :] - gray[:-1, :])

        h_scores = []
        for shift_x in range(8):
            cols = [c for c in range(diff_h.shape[1]) if (c + 1 - shift_x) % 8 == 0]
            h_scores.append(float(np.mean(diff_h[:, cols])) if cols else 0.0)

        v_scores = []
        for shift_y in range(8):
            rows = [r for r in range(diff_v.shape[0]) if (r + 1 - shift_y) % 8 == 0]
            v_scores.append(float(np.mean(diff_v[rows, :])) if rows else 0.0)

        best_shift_x = int(np.argmax(h_scores))
        best_shift_y = int(np.argmax(v_scores))

        mean_h = float(np.mean(h_scores)) + 1e-6
        mean_v = float(np.mean(v_scores)) + 1e-6
        peak_ratio_h = max(h_scores) / mean_h
        peak_ratio_v = max(v_scores) / mean_v
        grid_strength = max(peak_ratio_h, peak_ratio_v)

        is_misaligned = (best_shift_x not in (0, 1) or best_shift_y not in (0, 1)) and grid_strength > 1.18

        notes = []
        if is_misaligned:
            notes.append(
                f"Non-aligned JPEG 8x8 block grid shift detected at offset ({best_shift_x}, {best_shift_y})."
            )

        return {
            "detected_shift": (best_shift_x, best_shift_y),
            "grid_periodicity_strength": round(float(grid_strength), 3),
            "horizontal_grid_profile": [round(s, 3) for s in h_scores],
            "vertical_grid_profile": [round(s, 3) for s in v_scores],
            "is_aligned": not is_misaligned,
            "notes": notes
        }

    @staticmethod
    def _normalize_candidate_box(candidate: Any) -> Optional[Tuple[int, int, int, int]]:
        """Normalize candidate ROI boxes across common project formats."""
        if candidate is None:
            return None

        if isinstance(candidate, dict):
            if all(k in candidate for k in ("x", "y", "w", "h")):
                return (int(candidate["x"]), int(candidate["y"]), int(candidate["w"]), int(candidate["h"]))
            if all(k in candidate for k in ("x1", "y1", "x2", "y2")):
                x1, y1, x2, y2 = (int(candidate[k]) for k in ("x1", "y1", "x2", "y2"))
                return (x1, y1, max(0, x2 - x1), max(0, y2 - y1))
            for key in ("bbox", "box"):
                if key in candidate:
                    box = candidate[key]
                    if isinstance(box, (list, tuple, np.ndarray)) and len(box) == 4:
                        if key == "bbox":
                            x1, y1, x2, y2 = (int(v) for v in box)
                            return (x1, y1, max(0, x2 - x1), max(0, y2 - y1))
                        return (int(box[0]), int(box[1]), int(box[2]), int(box[3]))
            return None

        if isinstance(candidate, (list, tuple, np.ndarray)) and len(candidate) == 4:
            coords = [int(v) for v in candidate]
            return (coords[0], coords[1], coords[2], coords[3])

        return None

    def detect_block_artifact_grid(
        self,
        gray: np.ndarray,
        candidate_boxes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Block Artifact Grid (BAG) Analysis (#115).
        Extracts 8x8 block boundary discontinuity signal across luminance channels,
        detects grid phase displacement between text regions and background canvas,
        and outputs a binary grid-discrepancy mask.
        """
        gray = np.asarray(gray)
        if gray.ndim == 3:
            if gray.shape[-1] in (1, 3, 4):
                gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY) if gray.shape[-1] == 3 else gray[:, :, 0]
        h, w = gray.shape
        bag_mask = np.zeros((h, w), dtype=np.uint8)
        if h < 64 or w < 64:
            return {
                "has_bag_anomaly": False,
                "discrepant_regions": [],
                "bag_mask": bag_mask,
                "notes": []
            }

        # Step 1: Compute global background grid phase
        # If candidate boxes are given, mask them with background median so high-contrast
        # spliced patches cannot bias the background grid phase detection.
        bg_gray = gray.copy()
        if candidate_boxes:
            bg_median = int(np.median(gray))
            for candidate in candidate_boxes:
                box = self._normalize_candidate_box(candidate)
                if box is None:
                    continue
                bx, by, bw, bh = box
                if bw > 0 and bh > 0 and by + bh <= h and bx + bw <= w:
                    bg_gray[by:by+bh, bx:bx+bw] = bg_median

        global_grid = self.detect_jpeg_grid_shift(bg_gray)
        gx, gy = global_grid["detected_shift"]

        # Step 2: Compute 8x8 block boundary discontinuity signals
        diff_h = np.abs(gray[:, 1:] - gray[:, :-1])
        diff_v = np.abs(gray[1:, :] - gray[:-1, :])

        # Step 3: Analyze candidate boxes (or split image into regional tiles if none provided)
        regions_to_test = []
        if candidate_boxes:
            for candidate in candidate_boxes:
                box = self._normalize_candidate_box(candidate)
                if box is None:
                    continue
                regions_to_test.append(box)
        else:
            # Regional 64x64 tiles
            for ty in range(0, h - 64, 48):
                for tx in range(0, w - 64, 48):
                    regions_to_test.append((tx, ty, 64, 64))

        discrepant_regions = []
        is_targeted = bool(candidate_boxes)
        # Targeted candidate boxes use a sensitive threshold (1.12),
        # while blind background tile scans require higher strength (1.35)
        # to avoid false positives from isolated text strokes.
        required_strength = 1.12 if is_targeted else 1.35

        for (rx, ry, rw, rh) in regions_to_test:
            if rw < 32 or rh < 32 or ry + rh > h or rx + rw > w:
                continue

            roi_gray = gray[ry:ry+rh, rx:rx+rw]
            local_grid = self.detect_jpeg_grid_shift(roi_gray)
            lx, ly = local_grid["detected_shift"]
            l_strength = local_grid["grid_periodicity_strength"]

            # Convert local ROI grid phase to absolute image coordinate space
            abs_lx = (lx + rx) % 8
            abs_ly = (ly + ry) % 8

            # Circular distance modulo 8 between local grid and global background grid
            dx = min(abs(abs_lx - gx) % 8, 8 - (abs(abs_lx - gx) % 8))
            dy = min(abs(abs_ly - gy) % 8, 8 - (abs(abs_ly - gy) % 8))

            # True phase displacement (>= 2 pixels offset from global grid)
            if (dx >= 2 or dy >= 2) and l_strength >= required_strength:
                discrepant_regions.append({
                    "box": [int(rx), int(ry), int(rw), int(rh)],
                    "local_shift": (int(abs_lx), int(abs_ly)),
                    "global_shift": (int(gx), int(gy)),
                    "phase_disparity": (int(dx), int(dy)),
                    "strength": round(float(l_strength), 3),
                    "label": "Block Artifact Grid (BAG) Phase Shift"
                })
                # Highlight in binary discrepancy mask
                bag_mask[ry:ry+rh, rx:rx+rw] = 255

        has_bag_anomaly = len(discrepant_regions) > 0
        notes = []
        if has_bag_anomaly:
            notes.append(
                f"Block Artifact Grid (BAG) phase shift detected across {len(discrepant_regions)} regional blocks."
            )

        return {
            "has_bag_anomaly": has_bag_anomaly,
            "discrepant_regions": discrepant_regions[:10],
            "global_grid_phase": (gx, gy),
            "bag_mask": bag_mask,
            "notes": notes
        }

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

        # Decompose ELA differences into chromatic vs luminance channels
        ela_channels = self.decompose_ela_channels(pil_image)

        # Detect 8x8 block grid shift & misalignment
        gray_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY).astype(np.float32)
        grid_shift_res = self.detect_jpeg_grid_shift(gray_img)
        dct_res["grid_alignment"] = grid_shift_res

        # Detect Block Artifact Grid (BAG) localized phase shifts
        bag_res = self.detect_block_artifact_grid(gray_img, boxes)

        # Detect copy-move forgery (ORB keypoints & block DCT)
        copymove_res = analyze_copymove_forensics(cv2_img)

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
        notes.extend(grid_shift_res["notes"])
        notes.extend(bag_res["notes"])
        notes.extend(copymove_res.get("findings", []))

        return {
            "layer_name": "Layer 2: Classical Image Forensics (ELA & DCT)",
            "anomaly_score": layer2_score,
            "is_anomalous": layer2_score >= 0.40,
            "ela_variance": round(ela_var, 2),
            "detected_regions": boxes,
            "double_compression_analysis": dct_res,
            "channel_decomposition": ela_channels,
            "grid_alignment": grid_shift_res,
            "block_artifact_grid": bag_res,
            "copy_move_analysis": copymove_res,
            "heatmap_base64": cv2_to_base64(heatmap),
            "diff_gray": diff_gray,
            "findings": notes
        }
