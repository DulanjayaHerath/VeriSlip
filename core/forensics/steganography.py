"""Digital watermark and steganography utilities for banking receipt forensics.

This module provides a compact but practical set of tools for:
- bitplane slicing of RGB images (LSB / micro-pattern inspection),
- DCT-based watermark recovery statistics,
- authentic bank profile summaries for Commercial Bank and FriMi receipts,
- localized disruption detection for tampered image regions.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Union

import cv2
import numpy as np
from PIL import Image


ImageLike = Union[Image.Image, np.ndarray]

BANK_WATERMARK_PROFILES = {
    "COMBANK": {
        "name": "Commercial Bank of Ceylon",
        "bit_index": 1,
        "expected_lsb_strength": 0.35,
        "expected_dct_strength": 0.55,
        "default_boxes": [
            [0.08, 0.08, 0.84, 0.22],
            [0.12, 0.68, 0.80, 0.90],
        ],
    },
    "NTB_FRIMI": {
        "name": "FriMi / NTB Direct",
        "bit_index": 2,
        "expected_lsb_strength": 0.30,
        "expected_dct_strength": 0.50,
        "default_boxes": [
            [0.10, 0.10, 0.82, 0.22],
            [0.18, 0.65, 0.82, 0.90],
        ],
    },
}


def _as_bgr_array(image: ImageLike) -> np.ndarray:
    """Normalize an input image to an OpenCV BGR array."""
    if isinstance(image, Image.Image):
        rgb = np.asarray(image.convert("RGB"))
        return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    arr = np.asarray(image)
    if arr.ndim == 2:
        return cv2.cvtColor(arr.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    if arr.shape[-1] == 4:
        return cv2.cvtColor(arr.astype(np.uint8), cv2.COLOR_BGRA2BGR)
    if arr.shape[-1] == 3:
        return arr.astype(np.uint8)
    raise ValueError(f"Unsupported image shape: {arr.shape}")


def _extract_channel_plane(channel: np.ndarray, bit_index: int) -> np.ndarray:
    return ((channel.astype(np.uint16) >> bit_index) & 1).astype(np.uint8)


def extract_bitplane(image: ImageLike, bit_index: int = 0, channel: str = "gray") -> np.ndarray:
    """Return a single bit-plane derived from the image.

    Args:
        image: PIL image or numpy array.
        bit_index: bit plane index in [0, 7].
        channel: 'gray', 'r', 'g', 'b', or 'all'.
    """
    if not 0 <= bit_index <= 7:
        raise ValueError("bit_index must be between 0 and 7")

    bgr = _as_bgr_array(image)
    if channel == "gray":
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        return _extract_channel_plane(gray, bit_index)
    if channel == "all":
        result = {}
        for name, idx in {"b": 0, "g": 1, "r": 2}.items():
            result[name] = _extract_channel_plane(bgr[:, :, idx], bit_index)
        return result

    channel_map = {"b": 0, "g": 1, "r": 2}
    if channel.lower() not in channel_map:
        raise ValueError("channel must be one of 'gray', 'r', 'g', 'b', or 'all'")
    return _extract_channel_plane(bgr[:, :, channel_map[channel.lower()]], bit_index)


def extract_bitplanes(image: ImageLike, bit_indices: Optional[Sequence[int]] = None) -> Dict[str, Dict[str, np.ndarray]]:
    """Extract multiple bitplanes for each RGB channel.

    Returns a nested dict keyed by bit index and color channel, e.g.
    {'0': {'r': arr, 'g': arr, 'b': arr}, ...}.
    """
    if bit_indices is None:
        bit_indices = (0, 1, 2)
    output: Dict[str, Dict[str, np.ndarray]] = {}
    bgr = _as_bgr_array(image)
    for bit_index in bit_indices:
        if not 0 <= bit_index <= 7:
            raise ValueError(f"Unsupported bit_index {bit_index}; expected 0..7")
        output[str(bit_index)] = {
            "r": _extract_channel_plane(bgr[:, :, 2], bit_index),
            "g": _extract_channel_plane(bgr[:, :, 1], bit_index),
            "b": _extract_channel_plane(bgr[:, :, 0], bit_index),
        }
    return output


def _default_bbox_to_pixels(shape: Tuple[int, int], box: Sequence[float]) -> Tuple[int, int, int, int]:
    h, w = shape[:2]
    x1, y1, x2, y2 = box
    left = max(0, int(x1 * w))
    top = max(0, int(y1 * h))
    right = min(w, int(x2 * w))
    bottom = min(h, int(y2 * h))
    return left, top, right, bottom


def _region_energy(image: np.ndarray, box: Sequence[float]) -> float:
    h, w = image.shape[:2]
    left, top, right, bottom = _default_bbox_to_pixels((h, w), box)
    if right <= left or bottom <= top:
        return 0.0
    patch = image[top:bottom, left:right]
    if patch.size == 0:
        return 0.0
    return float(np.mean(np.abs(patch)))


def recover_dct_watermark(image: ImageLike, block_size: int = 8, threshold: float = 0.15) -> Dict[str, Any]:
    """Recover a periodic DCT watermark signal from the image.

    The method looks for consistently strong mid-band DCT coefficients in evenly
    tiled 8x8 blocks, which is the expected signature of embedded watermarking
    in modern mobile banking receipt rendering.
    """
    bgr = _as_bgr_array(image)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    h, w = gray.shape
    if h < block_size or w < block_size:
        raise ValueError(f"Image too small for {block_size}x{block_size} DCT blocks")

    energies: List[float] = []
    block_map = np.zeros((h, w), dtype=np.float32)

    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = gray[y : y + block_size, x : x + block_size]
            if block.shape[0] != block_size or block.shape[1] != block_size:
                continue
            dct = cv2.dct(block)
            midband = np.abs(dct[1:4, 1:4])
            block_energy = float(np.mean(midband))
            energies.append(block_energy)
            block_map[y : y + block_size, x : x + block_size] = block_energy

    if not energies:
        return {
            "score": 0.0,
            "detected": False,
            "midband_mean": 0.0,
            "midband_std": 0.0,
            "heatmap": np.zeros_like(gray),
            "details": "No valid DCT blocks were evaluated.",
        }

    values = np.asarray(energies, dtype=np.float32)
    mean_energy = float(np.mean(values))
    std_energy = float(np.std(values))
    score = float(mean_energy / (std_energy + 1e-6))
    detected = score >= threshold

    return {
        "score": round(score, 4),
        "detected": bool(detected),
        "midband_mean": round(mean_energy, 4),
        "midband_std": round(std_energy, 4),
        "heatmap": block_map,
        "details": (
            "Periodic mid-frequency watermark pattern detected"
            if detected
            else "No stable periodic DCT watermark signal found"
        ),
    }


def profile_authentic_watermark(bank_code: Optional[str] = None) -> Dict[str, Any]:
    """Return a watermark profile for known bank templates."""
    key = (bank_code or "COMBANK").upper()
    profile = BANK_WATERMARK_PROFILES.get(key)
    if profile is None:
        profile = BANK_WATERMARK_PROFILES["COMBANK"]
    return {**profile}


def detect_watermark_disruption(
    image: ImageLike,
    boxes: Optional[Sequence[Sequence[float]]] = None,
    bank_code: Optional[str] = None,
    expected_score: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """Flag localized disruptions by sampling each box and comparing local DCT / LSB energy.

    Each entry includes the normalized box, a disruption score, and a label.
    """
    bgr = _as_bgr_array(image)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    profile = profile_authentic_watermark(bank_code)
    if boxes is None:
        boxes = profile.get("default_boxes", [])

    if expected_score is None:
        expected_score = profile["expected_dct_strength"]

    results: List[Dict[str, Any]] = []
    for idx, box in enumerate(boxes):
        left, top, right, bottom = _default_bbox_to_pixels(gray.shape, box)
        if right <= left or bottom <= top:
            continue
        roi = gray[top:bottom, left:right]
        if roi.size == 0:
            continue
        dct = recover_dct_watermark(roi, block_size=8)
        lsb_signal = float(np.mean(np.abs((roi.astype(np.uint16) >> profile["bit_index"]) & 1)))
        disruption = max(0.0, min(1.0, 1.0 - (dct["score"] / max(expected_score, 1e-6))))
        disruption = max(disruption, max(0.0, 1.0 - (lsb_signal / max(profile["expected_lsb_strength"], 1e-6))))
        results.append(
            {
                "index": idx,
                "box": [float(left) / gray.shape[1], float(top) / gray.shape[0], float(right) / gray.shape[1], float(bottom) / gray.shape[0]],
                "pixel_box": [left, top, right, bottom],
                "dct_score": dct["score"],
                "lsb_signal": round(lsb_signal, 4),
                "disruption_score": round(disruption, 4),
                "label": "localized watermark disruption" if disruption > 0.35 else "stable watermark region",
            }
        )

    return results


class BankWatermarkProfiler:
    """Profile authentic bank receipt watermark characteristics."""

    def __init__(self, bank_code: Optional[str] = None):
        self.bank_code = (bank_code or "COMBANK").upper()
        self.profile = profile_authentic_watermark(self.bank_code)

    def analyze(self, image: ImageLike, boxes: Optional[Sequence[Sequence[float]]] = None) -> Dict[str, Any]:
        bitplanes = extract_bitplanes(image, bit_indices=(0, 1, 2))
        dct = recover_dct_watermark(image)
        disruption = detect_watermark_disruption(image, boxes=boxes, bank_code=self.bank_code)

        combined_strength = min(1.0, (dct["score"] / max(self.profile["expected_dct_strength"], 1e-6)) * 0.7)
        lsb_strength = 0.0
        if bitplanes:
            plane = bitplanes.get(str(self.profile["bit_index"]), {})
            if plane:
                lsb_strength = float(np.mean(np.concatenate([v.ravel() for v in plane.values()])))
        combined_strength += min(1.0, (lsb_strength / max(self.profile["expected_lsb_strength"], 1e-6)) * 0.3)

        return {
            "bank_code": self.bank_code,
            "profile": self.profile,
            "bitplanes": bitplanes,
            "dct_analysis": dct,
            "localized_disruptions": disruption,
            "watermark_strength": round(combined_strength, 4),
            "is_authentic": bool(dct["detected"] and combined_strength >= 0.55),
        }


class SteganographyForensics:
    """Practical wrapper for watermark extraction and disruption scoring."""

    def __init__(self, bank_code: Optional[str] = None):
        self.bank_code = (bank_code or "COMBANK").upper()
        self.profiler = BankWatermarkProfiler(self.bank_code)

    def evaluate(self, image: ImageLike, boxes: Optional[Sequence[Sequence[float]]] = None) -> Dict[str, Any]:
        return self.profiler.analyze(image, boxes=boxes)


__all__ = [
    "BANK_WATERMARK_PROFILES",
    "extract_bitplane",
    "extract_bitplanes",
    "recover_dct_watermark",
    "profile_authentic_watermark",
    "detect_watermark_disruption",
    "BankWatermarkProfiler",
    "SteganographyForensics",
]
