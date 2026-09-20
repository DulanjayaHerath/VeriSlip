"""Frequency-domain discrimination of thermal fading and digital erasure.

The detector works on a median-filtered luminance field so ordinary printed
glyph edges do not dominate the signal. ``high_frequency_cutoff`` is the
normalized radial FFT frequency above which energy is treated as a sharp
transition (0.16 by default). ``splice_threshold`` controls the final
classification threshold, while ``min_border_fraction`` rejects tiny dust and
compression artifacts. These defaults target receipt images of at least
128 pixels on their shortest side and are intentionally conservative.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import cv2
import numpy as np
from PIL import Image


@dataclass(frozen=True)
class ThermalFadeConfig:
    """Sensitivity parameters for thermal-paper transition analysis."""

    high_frequency_cutoff: float = 0.16
    splice_threshold: float = 0.46
    min_border_fraction: float = 0.08
    median_kernel: int = 9

    def __post_init__(self) -> None:
        if not 0.05 <= self.high_frequency_cutoff <= 0.45:
            raise ValueError("high_frequency_cutoff must be between 0.05 and 0.45")
        if not 0.0 <= self.splice_threshold <= 1.0:
            raise ValueError("splice_threshold must be between 0 and 1")
        if not 0.01 <= self.min_border_fraction <= 0.5:
            raise ValueError("min_border_fraction must be between 0.01 and 0.5")
        if self.median_kernel < 3 or self.median_kernel % 2 == 0:
            raise ValueError("median_kernel must be an odd integer of at least 3")


class ThermalFadeDiscriminator:
    """Distinguish continuous thermal dye fading from hard digital splices."""

    def __init__(self, config: ThermalFadeConfig | None = None) -> None:
        self.config = config or ThermalFadeConfig()

    @staticmethod
    def _luminance(image: Image.Image | np.ndarray) -> np.ndarray:
        if isinstance(image, Image.Image):
            rgb = np.asarray(image.convert("RGB"), dtype=np.uint8)
            return cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        array = np.asarray(image)
        if array.ndim == 2:
            return np.clip(array, 0, 255).astype(np.uint8)
        if array.ndim == 3 and array.shape[2] in (3, 4):
            code = cv2.COLOR_BGR2GRAY if array.shape[2] == 3 else cv2.COLOR_BGRA2GRAY
            return cv2.cvtColor(array.astype(np.uint8), code)
        raise ValueError(
            "thermal fade analysis requires a grayscale, RGB, or RGBA image"
        )

    def analyze(self, image: Image.Image | np.ndarray) -> Dict[str, Any]:
        """Return FFT, continuity, and localized hard-border evidence.

        Smooth thermal fading concentrates energy near the FFT origin. Digital
        erase/inpaint operations add high-frequency energy and long, abrupt
        borders to the low-frequency paper field. Images below 64x64 are
        reported as inconclusive rather than producing unstable evidence.
        """

        gray = self._luminance(image)
        height, width = gray.shape
        if min(height, width) < 64:
            return self._empty_result(
                "Image too small for reliable thermal fade analysis"
            )

        field = (
            cv2.medianBlur(gray, self.config.median_kernel).astype(np.float32) / 255.0
        )
        field = cv2.GaussianBlur(field, (5, 5), 0)
        centered = field - float(np.mean(field))

        spectrum = np.abs(np.fft.fftshift(np.fft.fft2(centered))) ** 2
        yy, xx = np.ogrid[:height, :width]
        radius = np.sqrt(
            ((yy - height / 2.0) / height) ** 2 + ((xx - width / 2.0) / width) ** 2
        )
        high_mask = radius >= self.config.high_frequency_cutoff
        high_frequency_ratio = float(
            spectrum[high_mask].sum() / (spectrum.sum() + 1e-12)
        )

        grad_x = cv2.Sobel(field, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(field, cv2.CV_32F, 0, 1, ksize=3)
        gradient = cv2.magnitude(grad_x, grad_y)
        median = float(np.median(gradient))
        mad = float(np.median(np.abs(gradient - median)))
        threshold = max(0.035, median + 6.0 * max(mad, 1e-4))
        hard_edges = (gradient >= threshold).astype(np.uint8) * 255
        hard_edges = cv2.morphologyEx(
            hard_edges,
            cv2.MORPH_CLOSE,
            cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)),
        )

        min_border = self.config.min_border_fraction * min(height, width)
        contours, _ = cv2.findContours(
            hard_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        regions: List[Dict[str, Any]] = []
        for contour in contours:
            perimeter = float(cv2.arcLength(contour, True))
            x, y, w, h = cv2.boundingRect(contour)
            if perimeter < min_border or max(w, h) < min_border:
                continue
            if w * h > 0.8 * width * height:
                continue
            regions.append(
                {
                    "box": [int(x), int(y), int(w), int(h)],
                    "confidence": round(
                        min(0.99, perimeter / (2.0 * (width + height))), 3
                    ),
                    "label": "Abrupt thermal-field transition",
                }
            )

        frequency_score = min(1.0, high_frequency_ratio / 0.006)
        # A splice creates one coherent, long border. Summed edge density would
        # incorrectly treat several ordinary text rows as an erase boundary.
        strongest_border = max(
            (region["confidence"] for region in regions), default=0.0
        )
        transition_score = min(1.0, strongest_border / 0.40)
        splice_likelihood = float(
            np.clip(0.25 * frequency_score + 0.75 * transition_score, 0.0, 1.0)
        )
        is_digital_splice = splice_likelihood >= self.config.splice_threshold and bool(
            regions
        )

        return {
            "classification": (
                "digital_splice" if is_digital_splice else "continuous_thermal_fade"
            ),
            "is_digital_splice": is_digital_splice,
            "splice_likelihood": round(splice_likelihood, 4),
            "high_frequency_ratio": round(high_frequency_ratio, 6),
            "transition_border_score": round(transition_score, 4),
            "fade_continuity_score": round(1.0 - transition_score, 4),
            "detected_regions": sorted(
                regions, key=lambda item: item["confidence"], reverse=True
            )[:8],
            "parameters": {
                "high_frequency_cutoff": self.config.high_frequency_cutoff,
                "splice_threshold": self.config.splice_threshold,
                "min_border_fraction": self.config.min_border_fraction,
            },
            "notes": (
                [
                    "Abrupt high-frequency borders are consistent with digital erasure or inpainting."
                ]
                if is_digital_splice
                else [
                    "Low-frequency luminance change is consistent with continuous thermal-paper fading."
                ]
            ),
        }

    @staticmethod
    def _empty_result(note: str) -> Dict[str, Any]:
        return {
            "classification": "inconclusive",
            "is_digital_splice": False,
            "splice_likelihood": 0.0,
            "high_frequency_ratio": 0.0,
            "transition_border_score": 0.0,
            "fade_continuity_score": 0.0,
            "detected_regions": [],
            "parameters": {},
            "notes": [note],
        }


def analyze_thermal_fade(
    image: Image.Image | np.ndarray,
    config: ThermalFadeConfig | None = None,
) -> Dict[str, Any]:
    """Convenience wrapper for thermal-paper fade analysis."""

    return ThermalFadeDiscriminator(config).analyze(image)
