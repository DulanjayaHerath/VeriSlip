"""Gradient-weighted class activation mapping helpers for Layer 4 forensic attribution."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image

from core.forensics.utils import cv2_to_base64

try:  # pragma: no cover - optional dependency
    import torch
    import torch.nn.functional as F
except ImportError:  # pragma: no cover - optional dependency
    torch = None
    F = None


def compute_iou(box_a: List[int], box_b: List[int]) -> float:
    """Compute the intersection-over-union for two [x, y, width, height] boxes."""
    if not box_a or not box_b:
        return 0.0

    x1 = max(box_a[0], box_b[0])
    y1 = max(box_a[1], box_b[1])
    x2 = min(box_a[0] + box_a[2], box_b[0] + box_b[2])
    y2 = min(box_a[1] + box_a[3], box_b[1] + box_b[3])

    inter_w = max(0, x2 - x1)
    inter_h = max(0, y2 - y1)
    inter_area = inter_w * inter_h

    area_a = max(0, box_a[2] * box_a[3])
    area_b = max(0, box_b[2] * box_b[3])
    union_area = area_a + area_b - inter_area
    if union_area <= 0:
        return 0.0
    return inter_area / union_area


class Layer4GradCAM:
    """Generate Grad-CAM saliency and a counterfactual reconstruction for Layer 4 tamper evidence."""

    def __init__(self, model: Optional[Any] = None, target_stream: str = "rgb_stream"):
        self.model = model
        self.target_stream = target_stream
        self._feature_maps: Dict[str, Any] = {}
        self._gradients: Dict[str, Any] = {}
        self._attached = False

    def attach_hooks(self) -> None:
        """Register forward hooks so the last convolution in each Layer 4 stream exposes activations and gradients."""
        if self.model is None or self._attached:
            return

        def _make_hook(stream_name: str):
            def _hook(module, inputs, output):
                self._feature_maps[stream_name] = output

                def _backward_hook(grad_output):
                    self._gradients[stream_name] = grad_output

                output.register_hook(_backward_hook)

            return _hook

        known_streams = ["rgb_stream", "forensic_stream"]
        for stream_name in known_streams:
            stream = getattr(self.model, stream_name, None)
            if stream is not None and hasattr(stream, "__getitem__"):
                final_block = stream[-1]
                if hasattr(final_block, "conv") and hasattr(final_block.conv, "__getitem__"):
                    final_conv = final_block.conv[0]
                    final_conv.register_forward_hook(_make_hook(stream_name))
        self._attached = True

    def _as_rgb_array(self, image: Image.Image) -> np.ndarray:
        if image.mode != "RGB":
            image = image.convert("RGB")
        return np.asarray(image, dtype=np.float32)

    def _coerce_forensic_tensor(self, image: Image.Image, forensic_input: Optional[np.ndarray]) -> np.ndarray:
        height, width = image.height, image.width
        if forensic_input is None:
            gray = np.asarray(image.convert("L"), dtype=np.float32)
            gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_LINEAR)
            gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
            gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
            grad = np.sqrt(gx ** 2 + gy ** 2)
            return np.stack([
                np.clip((gray - gray.mean()) / 255.0 + 0.5, 0, 1),
                np.clip(grad / 255.0, 0, 1),
                np.clip(np.abs(gray - np.median(gray)) / 255.0, 0, 1),
            ], axis=0).astype(np.float32)

        tensor = np.asarray(forensic_input, dtype=np.float32)
        if tensor.ndim == 2:
            tensor = np.stack([tensor, tensor, tensor], axis=0)
        if tensor.shape[0] != 3 and tensor.shape[-1] == 3:
            tensor = np.moveaxis(tensor, -1, 0)
        if tensor.shape[0] != 3:
            tensor = np.concatenate([tensor[:3], np.zeros((3 - min(3, tensor.shape[0]), height, width), dtype=np.float32)], axis=0)[:3]
        if tensor.shape[-2:] != (height, width):
            resized = np.zeros((3, height, width), dtype=np.float32)
            for channel in range(3):
                resized[channel] = cv2.resize(tensor[channel], (width, height), interpolation=cv2.INTER_LINEAR)
            tensor = resized
        return tensor.astype(np.float32)

    def _resolution_fit(self, heatmap: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        if heatmap.shape != target_size:
            return cv2.resize(heatmap, (target_size[1], target_size[0]), interpolation=cv2.INTER_LINEAR)
        return heatmap

    def _smooth_heatmap(self, heatmap: np.ndarray) -> np.ndarray:
        heatmap = heatmap.astype(np.float32)
        heatmap = cv2.GaussianBlur(heatmap, (31, 31), 0)
        heatmap = (heatmap - heatmap.min()) / max(heatmap.max() - heatmap.min(), 1e-6)
        return heatmap

    def _bbox_from_heatmap(self, heatmap: np.ndarray) -> List[int]:
        mask = heatmap > np.percentile(heatmap, 90)
        if not np.any(mask):
            return [0, 0, max(1, heatmap.shape[1]), max(1, heatmap.shape[0])]

        ys, xs = np.where(mask)
        x1, x2 = int(xs.min()), int(xs.max())
        y1, y2 = int(ys.min()), int(ys.max())
        return [x1, y1, max(1, x2 - x1 + 1), max(1, y2 - y1 + 1)]

    def _build_overlay(self, image: np.ndarray, heatmap: np.ndarray) -> np.ndarray:
        heatmap_3 = cv2.applyColorMap(np.uint8(255 * self._smooth_heatmap(heatmap)), cv2.COLORMAP_JET)
        overlay = cv2.addWeighted(image.astype(np.uint8), 0.65, heatmap_3, 0.35, 0)
        return overlay

    def _counterfactual_from_heatmap(self, image: np.ndarray, heatmap: np.ndarray) -> np.ndarray:
        smoothed = self._smooth_heatmap(heatmap)
        mask = smoothed >= np.percentile(smoothed, 85)
        mask = mask.astype(np.uint8)
        if mask.any():
            kernel = np.ones((15, 15), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
        blurred = cv2.GaussianBlur(image.astype(np.uint8), (31, 31), 0)
        counterfactual = image.astype(np.uint8).copy()
        if mask.any():
            counterfactual[mask > 0] = blurred[mask > 0]
        return counterfactual

    def _compute_model_gradcam(self, image: Image.Image, forensic_input: Optional[np.ndarray]) -> np.ndarray:
        if self.model is None or torch is None or F is None:
            return self._fallback_heatmap(self._as_rgb_array(image))

        rgb_img = np.asarray(image.convert("RGB"), dtype=np.float32) / 255.0
        rgb_tensor = torch.from_numpy(rgb_img).permute(2, 0, 1).unsqueeze(0)
        forensic_tensor = torch.from_numpy(self._coerce_forensic_tensor(image, forensic_input)).unsqueeze(0)

        self._feature_maps = {}
        self._gradients = {}
        self.model.zero_grad()
        rgb_tensor = rgb_tensor.requires_grad_(True)
        forensic_tensor = forensic_tensor.requires_grad_(True)

        class_logits, _ = self.model(rgb_tensor, forensic_tensor)
        score = class_logits[:, 0].sum()
        score.backward(retain_graph=True)

        candidates: List[np.ndarray] = []
        for stream_name in ("rgb_stream", "forensic_stream"):
            feature_map = self._feature_maps.get(stream_name)
            gradients = self._gradients.get(stream_name)
            if feature_map is None or gradients is None:
                continue
            weights = gradients.mean(dim=(2, 3), keepdim=True)
            cam = (weights * feature_map).sum(dim=1, keepdim=True)
            cam = F.relu(cam)
            cam = cam[0, 0].detach().cpu().numpy()
            candidates.append(cam)

        if not candidates:
            return self._fallback_heatmap(self._as_rgb_array(image))

        composite = np.maximum.reduce(candidates)
        return self._normalize_heatmap(np.asarray(composite, dtype=np.float32))

    @staticmethod
    def _normalize_heatmap(heatmap: np.ndarray) -> np.ndarray:
        heatmap = np.asarray(heatmap, dtype=np.float32)
        if heatmap.size == 0:
            return heatmap
        heatmap = (heatmap - heatmap.min()) / max(heatmap.max() - heatmap.min(), 1e-6)
        return heatmap

    def _fallback_heatmap(self, rgb: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(np.uint8(np.clip(rgb, 0, 255)), cv2.COLOR_RGB2GRAY).astype(np.float32)
        residual = np.abs(gray - np.median(gray))
        residual = cv2.GaussianBlur(residual, (31, 31), 0)
        heatmap = self._normalize_heatmap(residual)
        return heatmap

    def generate(
        self,
        image: Image.Image,
        forensic_input: Optional[np.ndarray] = None,
        ground_truth_box: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """Produce a smoothed attribution heatmap, overlay, counterfactual reconstruction, and bounding box."""
        rgb = self._as_rgb_array(image)
        heatmap = self._compute_model_gradcam(image, forensic_input)
        resized_heatmap = self._resolution_fit(heatmap, (image.height, image.width))
        smoothed = self._smooth_heatmap(resized_heatmap)
        bbox = self._bbox_from_heatmap(smoothed)
        overlay = self._build_overlay(rgb, smoothed)
        counterfactual = self._counterfactual_from_heatmap(rgb, smoothed)

        iou = 0.0
        if ground_truth_box is not None:
            iou = compute_iou(ground_truth_box, bbox)

        heatmap_base64 = cv2_to_base64(np.uint8(255 * smoothed), format=".png")
        overlay_base64 = cv2_to_base64(overlay, format=".png")
        counterfactual_base64 = cv2_to_base64(counterfactual, format=".png")

        result = {
            "heatmap": smoothed,
            "overlay": overlay,
            "counterfactual": counterfactual,
            "bbox": bbox,
            "iou": iou,
            "heatmap_base64": heatmap_base64,
            "overlay_base64": overlay_base64,
            "counterfactual_base64": counterfactual_base64,
        }
        return result

    def compute_gradcam(self, image: Image.Image, forensic_input: Optional[np.ndarray] = None, ground_truth_box: Optional[List[int]] = None) -> Dict[str, Any]:
        """Backward compatible alias for Grad-CAM generation."""
        return self.generate(image, forensic_input=forensic_input, ground_truth_box=ground_truth_box)


GradCAMForensics = Layer4GradCAM
GradCAMVisualizer = Layer4GradCAM


__all__ = [
    "Layer4GradCAM",
    "GradCAMForensics",
    "GradCAMVisualizer",
    "compute_iou",
]
