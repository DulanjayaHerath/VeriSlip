"""Physics-based print-and-scan degradation simulator for synthetic receipts.

This model approximates common degradation stages seen when a digitally generated
receipt is printed on thermal paper and then re-scanned: ink bleed, printer
halftone artifacts, light-field shading, and scanner sensor noise.
"""

from __future__ import annotations

import math
from typing import Iterable, Tuple, Union

import cv2
import numpy as np
from PIL import Image


ArrayLike = Union[np.ndarray, Image.Image]


class PrintScanSimulator:
    """Apply a lightweight print/scan degradation model to RGB images."""

    def __init__(
        self,
        blur_sigma: Tuple[float, float] = (0.9, 1.8),
        bleed_strength: float = 0.45,
        halftone_strength: float = 0.18,
        noise_std: float = 6.5,
        gamma: float = 2.2,
        seed: int | None = None,
    ) -> None:
        self.blur_sigma = blur_sigma
        self.bleed_strength = float(np.clip(bleed_strength, 0.0, 1.0))
        self.halftone_strength = float(np.clip(halftone_strength, 0.0, 1.0))
        self.noise_std = float(noise_std)
        self.gamma = float(gamma)
        self.rng = np.random.default_rng(seed)

    def _to_rgb_array(self, image: ArrayLike) -> np.ndarray:
        if isinstance(image, Image.Image):
            arr = np.asarray(image.convert("RGB"))
        else:
            arr = np.asarray(image)
            if arr.ndim == 2:
                arr = np.repeat(arr[:, :, None], 3, axis=2)
            elif arr.shape[-1] == 4:
                arr = arr[:, :, :3]
            elif arr.shape[-1] == 1:
                arr = np.repeat(arr, 3, axis=2)
        return arr.astype(np.float32)

    def _simulate_ink_bleed(self, rgb: np.ndarray) -> np.ndarray:
        gray = np.dot(rgb[..., :3], np.array([0.299, 0.587, 0.114], dtype=np.float32))
        sigma_x, sigma_y = self.blur_sigma
        bleed = cv2.GaussianBlur(gray, (0, 0), sigmaX=sigma_x, sigmaY=sigma_y)
        mixed = np.clip(
            (1.0 - self.bleed_strength) * gray + self.bleed_strength * bleed,
            0.0,
            255.0,
        )
        return np.dstack([np.clip(rgb[:, :, c] * 0.7 + mixed * 0.3, 0, 255) for c in range(3)])

    def _simulate_halftone(self, rgb: np.ndarray) -> np.ndarray:
        height, width = rgb.shape[:2]
        y, x = np.ogrid[:height, :width]
        rh = 1.0 + 0.08 * np.sin((x + y) / 5.0)
        pattern = ((x * 0.37 + y * 0.19 + self.rng.integers(0, 7, size=(height, width))) % 5) / 5.0
        gray = np.dot(rgb, np.array([0.299, 0.587, 0.114], dtype=np.float32))
        halftone = np.clip(gray * rh + (pattern - 0.5) * self.halftone_strength * 255.0, 0.0, 255.0)
        return np.dstack([np.clip(rgb[:, :, c] * 0.8 + halftone * 0.2, 0, 255) for c in range(3)])

    def _simulate_sensor_noise(self, rgb: np.ndarray) -> np.ndarray:
        height, width = rgb.shape[:2]
        y, x = np.ogrid[:height, :width]

        normalized = np.clip(rgb / 255.0, 1e-3, 1.0)
        gamma_corrected = np.power(normalized, 1.0 / max(self.gamma, 1e-6))

        illumination = 1.0 + 0.08 * np.sin((x / max(width - 1, 1)) * math.pi * 2.5)
        illumination = illumination[:, :, None]
        noise = self.rng.normal(0.0, self.noise_std / 255.0, size=rgb.shape)
        corrected = gamma_corrected * illumination + noise

        # Slight chromatic skew approximates scanner lens aberration.
        red_shift = np.roll(corrected[:, :, 0], 1, axis=1)
        blue_shift = np.roll(corrected[:, :, 2], -1, axis=1)
        corrected[:, :, 0] = red_shift
        corrected[:, :, 2] = blue_shift

        corrected = np.clip(corrected, 0.0, 1.0)
        return np.clip(np.power(corrected, self.gamma) * 255.0, 0.0, 255.0)

    def simulate(self, image: ArrayLike) -> Image.Image:
        """Apply a physically-inspired print-and-scan degradation pass."""
        rgb = self._to_rgb_array(image)
        rgb = self._simulate_ink_bleed(rgb)
        rgb = self._simulate_halftone(rgb)
        rgb = self._simulate_sensor_noise(rgb)
        return Image.fromarray(np.uint8(np.clip(rgb, 0, 255)))

    def simulate_print_scan(self, image: ArrayLike) -> Image.Image:
        return self.simulate(image)

    __call__ = simulate


__all__ = ["PrintScanSimulator"]
