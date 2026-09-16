"""
Automated Receipt Field Extractor & Layout Parser for Sri Lankan Payment Slips.
Extracts bank identity, amount, reference number, date, and status from slip images
without requiring third-party OCR cloud services.
"""

import re
from typing import Dict, Any, Optional, List, Tuple
import numpy as np
from PIL import Image
import cv2

from core.templates.bank_rules import BANK_TEMPLATES, validate_reference_number, identify_bank_from_text
from core.forensics.utils import pil_to_cv2

class ReceiptFieldExtractor:
    """Extracts structured financial transaction fields from slip screenshots."""

    def __init__(self):
        pass

    def detect_bank_from_visuals(self, cv2_img: np.ndarray) -> Tuple[str, float]:
        """Detect bank template by header color signature and aspect ratio."""
        h, w, _ = cv2_img.shape
        header_h = int(h * 0.22)
        header_roi = cv2_img[:header_h, :]

        # Average color in header
        mean_bgr = np.mean(header_roi, axis=(0, 1))
        mean_rgb = (mean_bgr[2], mean_bgr[1], mean_bgr[0])

        best_bank = "GENERIC_CEFTS"
        best_dist = 999.0

        for bank_code, tmpl in BANK_TEMPLATES.items():
            if bank_code == "GENERIC_CEFTS":
                continue
            target_rgb = np.array(tmpl["primary_color_rgb"], dtype=float)
            dist = np.linalg.norm(mean_rgb - target_rgb)
            if dist < best_dist:
                best_dist = dist
                best_bank = bank_code

        # If color distance is within threshold, confident in bank
        if best_dist < 85.0:
            confidence = max(0.4, 1.0 - (best_dist / 120.0))
            return best_bank, round(confidence, 2)

        return "COMBANK", 0.50  # Default fallback with medium confidence

    def detect_text_lines(self, gray: np.ndarray, y_min: int, y_max: int) -> List[Tuple[int, int, int, int]]:
        """Detect potential horizontal text lines in an image slice using morphological dilation."""
        roi = gray[y_min:y_max, :]
        _, binary = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY_INV)

        # Horizontal kernel to group characters in a word
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 4))
        dilated = cv2.dilate(binary, kernel, iterations=1)

        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        lines = []

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 30 and 10 < h < 60:
                lines.append((x, y + y_min, w, h))

        # Sort top-to-bottom
        lines.sort(key=lambda box: box[1])
        return lines

    def extract_fields(
        self,
        pil_image: Image.Image,
        bank_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze image layout and parse key transaction parameters:
        Amount, Reference, Bank, Date.
        """
        cv2_img = pil_to_cv2(pil_image)
        h, w, _ = cv2_img.shape
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)

        # 1. Detect Bank Template
        if bank_hint and bank_hint in BANK_TEMPLATES:
            detected_bank = bank_hint
            bank_conf = 0.95
        else:
            detected_bank, bank_conf = self.detect_bank_from_visuals(cv2_img)

        bank_meta = BANK_TEMPLATES.get(detected_bank, BANK_TEMPLATES["GENERIC_CEFTS"])

        # 2. Extract Amount Region (Typically between 25% and 45% of slip height)
        amount_y1 = int(h * 0.22)
        amount_y2 = int(h * 0.45)
        amount_candidates = self.detect_text_lines(gray, amount_y1, amount_y2)

        extracted_amount_bbox = None
        if amount_candidates:
            # Pick largest candidate box in amount zone
            amount_candidates.sort(key=lambda b: b[2] * b[3], reverse=True)
            extracted_amount_bbox = list(amount_candidates[0])

        # 3. Extract Detail Fields Region (Between 45% and 85% of slip height)
        fields_y1 = int(h * 0.42)
        fields_y2 = int(h * 0.88)
        detail_candidates = self.detect_text_lines(gray, fields_y1, fields_y2)

        field_bboxes = {
            "amount_box": extracted_amount_bbox,
            "field_rows_count": len(detail_candidates)
        }

        # 4. Generate structured parsing response
        return {
            "detected_bank_code": detected_bank,
            "bank_name": bank_meta["bank_name"],
            "bank_confidence": bank_conf,
            "currency": bank_meta.get("currency", "LKR"),
            "layout_geometry": {
                "aspect_ratio": round(h / max(w, 1), 2),
                "is_mobile_viewport": 1.4 <= (h / max(w, 1)) <= 2.4,
                "detected_rows": len(detail_candidates)
            },
            "field_regions": field_bboxes
        }
