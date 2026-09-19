"""
Layer 1 Forensics: Structural and Metadata Validation.
- EXIF / File Metadata analysis (detects editing software signatures like Photoshop, PicsArt, Canva, etc.)
- Bank template color distribution and aspect ratio sanity
- Reference number format & syntax validation against bank rules
"""

from typing import Dict, Any, List, Optional
from PIL import Image, ExifTags
import numpy as np
import cv2

from core.templates.bank_rules import BANK_TEMPLATES, validate_reference_number

KNOWN_EDITING_SOFTWARE = [
    "photoshop", "picsart", "canva", "gimp", "snapseed", 
    "photopea", "lightroom", "pixlr", "vsco", "pixelmator",
    "inshot", "meitu", "procreate"
]

class Layer1StructuralValidator:
    """Validator for structural integrity, reference numbers, and image metadata."""

    def __init__(self):
        pass

    def analyze_metadata(self, pil_image: Image.Image) -> Dict[str, Any]:
        """
        Inspect EXIF metadata for tampering traces or editing software signatures.
        """
        exif_data = {}
        editing_software_detected = []
        is_suspicious = False
        notes = []

        try:
            if hasattr(pil_image, "_getexif"):
                raw_exif = pil_image._getexif()
                if raw_exif:
                    for tag_id, value in raw_exif.items():
                        tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                        exif_data[tag_name] = str(value)

                    # Check Software or ProcessingSoftware tags
                    software_val = exif_data.get("Software", "").lower()
                    artist_val = exif_data.get("Artist", "").lower()
                    image_desc = exif_data.get("ImageDescription", "").lower()

                    combined_str = f"{software_val} {artist_val} {image_desc}"
                    for tool in KNOWN_EDITING_SOFTWARE:
                        if tool in combined_str:
                            editing_software_detected.append(tool)
                            is_suspicious = True
                            notes.append(f"Image contains metadata traces of editing software: {tool.capitalize()}")
                else:
                    notes.append("EXIF metadata stripped or not present (common for transit).")
            else:
                notes.append("Standard digital screenshot (no EXIF metadata).")
        except Exception as e:
            notes.append(f"EXIF read note: {str(e)}")

        # Check image info dictionary (PNG tEXt/iTXt, XMP chunks, PDF document metadata)
        try:
            if hasattr(pil_image, "info") and isinstance(pil_image.info, dict):
                for k, v in pil_image.info.items():
                    val_str = str(v).lower()
                    for tool in KNOWN_EDITING_SOFTWARE:
                        if tool in val_str and tool not in editing_software_detected:
                            editing_software_detected.append(tool)
                            is_suspicious = True
                            notes.append(f"Document metadata traces editing software: {tool.capitalize()}")
        except Exception as e:
            notes.append(f"Metadata info read note: {str(e)}")

        return {
            "has_exif": bool(exif_data),
            "exif_summary": {k: exif_data[k] for k in list(exif_data.keys())[:8]},
            "editing_software_detected": editing_software_detected,
            "is_suspicious": is_suspicious,
            "notes": notes
        }

    def analyze_layout_and_color(self, pil_image: Image.Image, bank_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze layout proportions, aspect ratio, and header color profile matching known bank branding.
        """
        w, h = pil_image.size
        aspect_ratio = h / max(w, 1)
        notes = []
        is_suspicious = False
        color_match_score = 1.0

        # Normal smartphone screenshot aspect ratio ranges between 1.6 and 2.4
        is_standard_phone_aspect = 1.4 <= aspect_ratio <= 2.4
        if not is_standard_phone_aspect:
            notes.append(f"Unusual aspect ratio ({aspect_ratio:.2f}) for a mobile banking slip screenshot.")

        # Check bank header color match if bank_code is specified
        if bank_code and bank_code in BANK_TEMPLATES:
            template = BANK_TEMPLATES[bank_code]
            expected_rgb = np.array(template["primary_color_rgb"], dtype=float)

            # Sample header region (top 20% of image)
            np_img = np.array(pil_image)
            header_region = np_img[:int(h * 0.25), :, :3]
            
            # Find closest matching pixels in header
            color_diffs = np.linalg.norm(header_region - expected_rgb, axis=2)
            matching_pixels = np.sum(color_diffs < 60) # threshold in RGB distance
            total_pixels = header_region.shape[0] * header_region.shape[1]
            match_ratio = matching_pixels / max(total_pixels, 1)

            if match_ratio < 0.005 and bank_code != "GENERIC_CEFTS":
                # Brand color noticeably absent in header
                notes.append(f"Header lacks characteristic {template['bank_name']} brand color profile.")
                color_match_score = 0.5
            else:
                color_match_score = min(1.0, match_ratio * 20.0 + 0.5)

        return {
            "dimensions": {"width": w, "height": h},
            "aspect_ratio": round(aspect_ratio, 2),
            "is_standard_phone_aspect": is_standard_phone_aspect,
            "color_match_score": round(color_match_score, 2),
            "notes": notes
        }

    def validate_reference(self, bank_code: str, reference_no: str) -> Dict[str, Any]:
        """Validate transaction reference number format."""
        return validate_reference_number(bank_code, reference_no)

    def _order_corners(self, points: np.ndarray) -> np.ndarray:
        """Order 4 polygon points into top-left, top-right, bottom-right, bottom-left."""
        points = np.asarray(points, dtype=np.float32)
        if points.shape != (4, 2):
            raise ValueError("Expected exactly four corner points")

        ordered = np.empty((4, 2), dtype=np.float32)
        ordered[0] = points[np.argmin(points[:, 0] + points[:, 1])]  # top-left
        ordered[2] = points[np.argmax(points[:, 0] + points[:, 1])]  # bottom-right
        ordered[1] = points[np.argmax(points[:, 0] - points[:, 1])]  # top-right
        ordered[3] = points[np.argmin(points[:, 0] - points[:, 1])]  # bottom-left

        # Ensure a consistent clockwise winding and eliminate duplicates before warping.
        if np.linalg.norm(ordered[1] - ordered[0]) == 0 or np.linalg.norm(ordered[2] - ordered[3]) == 0:
            center = points.mean(axis=0)
            angles = np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0])
            order = np.argsort(angles)
            ordered = points[order]
            ordered = np.roll(ordered, 1, axis=0)
        return ordered

    def detect_receipt_quad(self, pil_image: Image.Image) -> Dict[str, Any]:
        """Find the receipt boundary quad via contour + Hough-based fallback."""
        rgb = np.array(pil_image.convert("RGB"))
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        h, w = gray.shape

        if h == 0 or w == 0:
            return {
                "corners": [],
                "confidence": 0.0,
                "method": "none",
                "used_fallback": True,
            }

        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        paper_mask = cv2.threshold(blur, 220, 255, cv2.THRESH_BINARY)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        paper_mask = cv2.morphologyEx(paper_mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(paper_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        candidates = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 0.05 * h * w:
                continue
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4:
                approx = approx.reshape(4, 2)
                ordered = self._order_corners(approx)
                rect_w = max(np.linalg.norm(ordered[1] - ordered[0]), np.linalg.norm(ordered[2] - ordered[3]))
                rect_h = max(np.linalg.norm(ordered[3] - ordered[0]), np.linalg.norm(ordered[2] - ordered[1]))
                if rect_w > 0.15 * w and rect_h > 0.15 * h:
                    area_ratio = area / max(w * h, 1)
                    confidence = min(0.99, 0.55 + area_ratio * 1.5)
                    candidates.append((confidence, ordered, "contour"))

        if not candidates:
            edges = cv2.Canny(blur, 50, 150)
            lines = cv2.HoughLinesP(
                edges,
                rho=1,
                theta=np.pi / 180,
                threshold=max(40, min(w, h) // 8),
                minLineLength=max(50, min(w, h) // 4),
                maxLineGap=40,
            )
            if lines is not None:
                intersections = []
                for i in range(len(lines)):
                    for j in range(i + 1, len(lines)):
                        line_a = lines[i][0] if lines[i].ndim > 1 else lines[i]
                        line_b = lines[j][0] if lines[j].ndim > 1 else lines[j]
                        x1, y1, x2, y2 = line_a
                        x3, y3, x4, y4 = line_b
                        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                        if abs(den) < 1e-6:
                            continue
                        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
                        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
                        if 0 <= px <= w and 0 <= py <= h:
                            intersections.append((float(px), float(py)))
                if intersections:
                    hull = cv2.convexHull(np.asarray(intersections, dtype=np.float32).reshape(-1, 1, 2))
                    points = hull.reshape(-1, 2)
                    if len(points) >= 4:
                        ordered = self._order_corners(points[:4])
                        confidence = min(0.85, 0.45 + 0.25 * len(points) / max(len(points), 1))
                        return {
                            "corners": ordered.astype(int).tolist(),
                            "confidence": round(confidence, 3),
                            "method": "hough",
                            "used_fallback": False,
                        }

        if not candidates:
            return {
                "corners": [],
                "confidence": 0.0,
                "method": "none",
                "used_fallback": True,
            }

        confidence, ordered, method = max(candidates, key=lambda item: item[0])
        return {
            "corners": ordered.astype(int).tolist(),
            "confidence": round(confidence, 3),
            "method": method,
            "used_fallback": False,
        }

    def rectify_perspective(self, pil_image: Image.Image, target_size: Optional[tuple] = None, min_confidence: float = 0.6) -> Dict[str, Any]:
        """Normalize skewed receipt imagery into a frontal A4-sized document view."""
        if target_size is None:
            target_size = (827, 1169)

        width, height = pil_image.size
        quad = self.detect_receipt_quad(pil_image)
        corners = quad.get("corners", [])
        confidence = float(quad.get("confidence", 0.0))

        if not corners or confidence < min_confidence:
            return {
                "confidence": round(confidence, 3),
                "corners": corners,
                "used_fallback": True,
                "warped_image": pil_image,
                "target_size": target_size,
                "source_size": {"width": width, "height": height},
            }

        src = np.asarray(corners, dtype=np.float32)
        if len(src) != 4:
            return {
                "confidence": round(confidence, 3),
                "corners": corners,
                "used_fallback": True,
                "warped_image": pil_image,
                "target_size": target_size,
                "source_size": {"width": width, "height": height},
            }

        src = self._order_corners(src)
        dst = np.array([
            [0, 0],
            [target_size[0] - 1, 0],
            [target_size[0] - 1, target_size[1] - 1],
            [0, target_size[1] - 1],
        ], dtype=np.float32)

        matrix = cv2.getPerspectiveTransform(src, dst)
        warped = cv2.warpPerspective(np.array(pil_image.convert("RGB")), matrix, target_size)
        warped_image = Image.fromarray(warped)

        return {
            "confidence": round(confidence, 3),
            "corners": src.astype(int).tolist(),
            "used_fallback": False,
            "warped_image": warped_image,
            "target_size": target_size,
            "source_size": {"width": width, "height": height},
        }

    def evaluate(self, pil_image: Image.Image, bank_code: Optional[str] = None, reference_no: Optional[str] = None) -> Dict[str, Any]:
        """
        Run full Layer 1 validation and compute structural anomaly score (0.0 = clean, 1.0 = highly anomalous).
        """
        perspective_res = self.rectify_perspective(pil_image)
        # Keep structural scoring on the source image. Rectification is exposed in
        # the result for consumers that need a normalized document, but warping
        # before scoring can erase metadata and alter branding/color evidence.
        metadata_res = self.analyze_metadata(pil_image)
        layout_res = self.analyze_layout_and_color(pil_image, bank_code)
        
        ref_res = None
        if reference_no:
            ref_res = self.validate_reference(bank_code or "GENERIC_CEFTS", reference_no)

        # Calculate Layer 1 risk score
        risk_score = 0.0
        if metadata_res["is_suspicious"]:
            risk_score += 0.45
        if not layout_res["is_standard_phone_aspect"]:
            risk_score += 0.15
        if layout_res["color_match_score"] < 0.6:
            risk_score += 0.20
        if ref_res and not ref_res["valid"]:
            risk_score += 0.40

        risk_score = min(1.0, max(0.0, risk_score))

        all_notes = metadata_res["notes"] + layout_res["notes"]
        if ref_res and ref_res.get("suspicious_note"):
            all_notes.append(ref_res["suspicious_note"])

        return {
            "layer_name": "Layer 1: Structural & Metadata Validation",
            "anomaly_score": round(risk_score, 3),
            "is_anomalous": risk_score >= 0.40,
            "metadata_analysis": metadata_res,
            "layout_analysis": layout_res,
            "reference_analysis": ref_res,
            "perspective_analysis": perspective_res,
            "findings": all_notes
        }
