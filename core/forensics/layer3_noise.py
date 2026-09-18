"""
Layer 3 Forensics: Noise Residual and Spatial Inconsistency Analysis.
- High-pass spatial noise extraction (Median Filter Residual)
- Block-wise local noise variance mapping
- Discontinuity detection for spliced text / erased rectangles / clone-stamped patches
"""

from typing import Dict, Any, List, Tuple, Optional
import numpy as np
from PIL import Image
import cv2

from core.forensics.utils import pil_to_cv2, cv2_to_base64

SRM_KERNELS: Dict[str, np.ndarray] = {
    "srm_1st_horizontal": np.array([[0, 0, 0], [-1, 1, 0], [0, 0, 0]], dtype=np.float32),
    "srm_1st_vertical": np.array([[0, -1, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float32),
    "srm_2nd_horizontal": np.array([[0, 0, 0], [-1, 2, -1], [0, 0, 0]], dtype=np.float32),
    "srm_2nd_vertical": np.array([[0, -1, 0], [0, 2, 0], [0, -1, 0]], dtype=np.float32),
    "srm_edge_3x3": np.array([[-1, 2, -1], [2, -4, 2], [-1, 2, -1]], dtype=np.float32) / 4.0,
    "srm_square_3x3": np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32) / 8.0,
    "srm_edge_5x5": np.array([
        [-1,  2,  -2,  2, -1],
        [ 2, -6,   8, -6,  2],
        [-2,  8, -12,  8, -2],
        [ 2, -6,   8, -6,  2],
        [-1,  2,  -2,  2, -1]
    ], dtype=np.float32) / 12.0,
}

class Layer3NoiseForensics:
    """Evaluates noise residual variance and spatial consistency across patches."""

    def __init__(self, block_size: int = 32, median_ksize: int = 3):
        self.block_size = block_size
        self.median_ksize = median_ksize

    def extract_srm_residuals(
        self,
        gray: np.ndarray,
        kernel_names: Optional[List[str]] = None
    ) -> Dict[str, np.ndarray]:
        """
        Apply standard 3x3 and 5x5 Spatial Rich Models (SRM) high-pass filtering kernels
        to extract subtle, directional noise residuals across the canvas.
        """
        selected = kernel_names or list(SRM_KERNELS.keys())
        gray_f = gray.astype(np.float32)
        residuals = {}
        for name in selected:
            if name in SRM_KERNELS:
                kernel = SRM_KERNELS[name]
                filtered = cv2.filter2D(gray_f, cv2.CV_32F, kernel)
                residuals[name] = np.abs(filtered)
        return residuals

    def compute_srm_summary(self, gray: np.ndarray) -> Dict[str, Any]:
        """
        Compute summary statistics (variance, mean energy) across all SRM residual streams.
        """
        residuals = self.extract_srm_residuals(gray)
        metrics = {}
        variances = []
        for name, res in residuals.items():
            var = float(np.var(res))
            mean = float(np.mean(res))
            metrics[name] = {
                "variance": round(var, 4),
                "mean_energy": round(mean, 4),
            }
            variances.append(var)

        avg_srm_var = float(np.mean(variances)) if variances else 0.0
        return {
            "srm_metrics": metrics,
            "average_srm_variance": round(avg_srm_var, 4),
            "kernels_evaluated": len(metrics)
        }

    def extract_noise_residual(self, gray: np.ndarray) -> np.ndarray:
        """
        Extract high-frequency noise residual by subtracting median-filtered estimate.
        residual = |gray - median_blur(gray)|
        """
        denoised = cv2.medianBlur(gray, self.median_ksize)
        residual = cv2.absdiff(gray, denoised).astype(np.float32)
        return residual

    def compute_local_variance_map(self, gray: np.ndarray, residual: np.ndarray) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """
        Divide residual into grid blocks and compute variance for each block,
        weighting flat and text regions to prevent natural typography edges from being flagged.
        """
        h, w = residual.shape
        bs = self.block_size
        grid_h = h // bs
        grid_w = w // bs

        # Edge mask to identify natural text/icon UI components
        edges = cv2.Canny(gray, 60, 160)
        
        var_map = np.zeros((grid_h, grid_w), dtype=np.float32)
        edge_density_map = np.zeros((grid_h, grid_w), dtype=np.float32)

        for gy in range(grid_h):
            for gx in range(grid_w):
                patch_res = residual[gy*bs:(gy+1)*bs, gx*bs:(gx+1)*bs]
                patch_edge = edges[gy*bs:(gy+1)*bs, gx*bs:(gx+1)*bs]
                var_map[gy, gx] = np.var(patch_res)
                edge_density_map[gy, gx] = np.sum(patch_edge > 0)

        # Flat background blocks must have ZERO detected edges
        flat_mask = edge_density_map == 0
        outlier_blocks = []

        if np.sum(flat_mask) > 10:
            flat_variances = var_map[flat_mask]
            mean_flat_var = float(np.mean(flat_variances))
            std_flat_var = float(np.std(flat_variances))

            # Detect flat blocks that have abnormal noise (e.g. brush marks or noisy paste patches)
            if std_flat_var > 0.05:
                flat_z = (var_map - mean_flat_var) / (std_flat_var + 1e-4)
                # Flag flat blocks with high noise
                outlier_indices = np.argwhere((flat_z > 3.5) & flat_mask)
                for gy, gx in outlier_indices:
                    x = int(gx * bs)
                    y = int(gy * bs)
                    outlier_blocks.append({
                        "box": [x, y, bs, bs],
                        "z_score": round(float(flat_z[gy, gx]), 2),
                        "variance": round(float(var_map[gy, gx]), 2)
                    })

        # Filter out 1D UI divider lines or hairline borders:
        # A true tamper patch is a localized 2D cluster; a 1D row spanning >= 40% grid width with low variance is a UI divider rule
        if outlier_blocks:
            row_counts: Dict[int, int] = {}
            col_counts: Dict[int, int] = {}
            for o in outlier_blocks:
                gy = o["box"][1] // bs
                gx = o["box"][0] // bs
                row_counts[gy] = row_counts.get(gy, 0) + 1
                col_counts[gx] = col_counts.get(gx, 0) + 1

            filtered_outliers = []
            for o in outlier_blocks:
                gy = o["box"][1] // bs
                gx = o["box"][0] // bs
                is_divider_row = row_counts.get(gy, 0) >= 6 and (row_counts[gy] / max(grid_w, 1)) >= 0.40 and o["variance"] < 10.0
                is_divider_col = col_counts.get(gx, 0) >= 6 and (col_counts[gx] / max(grid_h, 1)) >= 0.40 and o["variance"] < 10.0
                if not (is_divider_row or is_divider_col):
                    filtered_outliers.append(o)
            outlier_blocks = filtered_outliers

        return var_map, outlier_blocks

    def generate_noise_heatmap(self, residual: np.ndarray) -> np.ndarray:
        """Create colored visual representation of noise residual."""
        # Scale for visibility
        scaled = np.clip(residual * 8.0, 0, 255).astype(np.uint8)
        colored = cv2.applyColorMap(scaled, cv2.COLORMAP_VIRIDIS)
        return colored

    def evaluate(self, pil_image: Image.Image) -> Dict[str, Any]:
        """
        Run full Layer 3 noise consistency evaluation.
        """
        cv2_img = pil_to_cv2(pil_image)
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)

        residual = self.extract_noise_residual(gray)
        var_map, outliers = self.compute_local_variance_map(gray, residual)
        noise_heatmap = self.generate_noise_heatmap(residual)

        mean_var = float(np.mean(var_map))

        # Anomaly scoring:
        # In an untouched digital receipt, flat areas have virtually zero noise residual variance.
        # A tiny statistical tail (1-2 blocks) can randomly hit 3.5 Z-score.
        # Tampered receipts where text was erased or clone-stamped create a cluster of outlier blocks.
        excess_outliers = max(0, len(outliers) - 3)
        outlier_ratio = excess_outliers / max(var_map.size, 1)
        score = min(1.0, outlier_ratio * 50.0)
        score = round(score, 3)

        notes = []
        if len(outliers) > 0:
            notes.append(f"Detected {len(outliers)} localized blocks with noise residual discontinuities in flat regions.")
        if score > 0.4:
            notes.append("High spatial noise inconsistency detected across text/background boundary.")

        srm_summary = self.compute_srm_summary(gray)

        return {
            "layer_name": "Layer 3: Noise Residual & Spatial Consistency",
            "anomaly_score": score,
            "is_anomalous": score >= 0.35,
            "mean_noise_variance": round(mean_var, 3),
            "outlier_blocks": outliers[:8],
            "noise_heatmap_base64": cv2_to_base64(noise_heatmap),
            "srm_analysis": srm_summary,
            "residual": residual,
            "findings": notes
        }
