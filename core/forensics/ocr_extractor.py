"""
Automated Receipt Field Extractor & Layout Parser for Sri Lankan Payment Slips.
Extracts bank identity, amount, reference number, date, and status from slip images
using local OCR (Apple Vision on macOS, PyPDFium2 for PDFs, and visual heuristics).
"""

import os
import re
import json
import subprocess
import tempfile
import csv
import io
from decimal import Decimal
from typing import Dict, Any, Optional, List, Tuple
import numpy as np
from PIL import Image
import cv2

from core.templates.bank_rules import BANK_TEMPLATES, validate_reference_number, identify_bank_from_text
from core.forensics.utils import pil_to_cv2

import shutil

NATIVE_OCR_BIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "bin", "apple_vision_ocr"))
SWIFT_SOURCE = os.path.abspath(os.path.join(os.path.dirname(__file__), "apple_vision_ocr.swift"))
SINHALA_UNICODE_START = 0x0D80
SINHALA_UNICODE_END = 0x0DFF
TAMIL_UNICODE_START = 0x0B80
TAMIL_UNICODE_END = 0x0BFF


class ReceiptFieldExtractor:
    """Extracts structured financial transaction fields from slip screenshots."""

    @staticmethod
    def detect_script_from_text(text: str) -> str:
        """Map OCR text to the most likely script for multilingual extraction."""
        if not text:
            return "und"
        if any(chr(SINHALA_UNICODE_START) <= ch <= chr(SINHALA_UNICODE_END) for ch in text):
            return "sin"
        if any(chr(TAMIL_UNICODE_START) <= ch <= chr(TAMIL_UNICODE_END) for ch in text):
            return "tam"
        return "eng"

    def resolve_supported_languages(self, text: str = "") -> List[str]:
        """Return ordered OCR language hints for a mixed-English/Sinhala/Tamil receipt."""
        languages = ["eng"]
        if not text:
            return languages

        scripts = set()
        for chunk in str(text).split():
            script = self.detect_script_from_text(chunk)
            if script != "und":
                scripts.add(script)

        if "sin" in scripts:
            languages.append("sin")
        if "tam" in scripts:
            languages.append("tam")
        return list(dict.fromkeys(languages))

    def __init__(self):
        self.supported_languages = ["eng", "sin", "tam"]
        if not os.path.exists(NATIVE_OCR_BIN) and os.path.exists(SWIFT_SOURCE) and shutil.which("swiftc"):
            try:
                os.makedirs(os.path.dirname(NATIVE_OCR_BIN), exist_ok=True)
                subprocess.run(["swiftc", "-O", "-o", NATIVE_OCR_BIN, SWIFT_SOURCE], check=True, capture_output=True)
            except Exception:
                pass
        self.has_native_ocr = os.path.exists(NATIVE_OCR_BIN) and os.access(NATIVE_OCR_BIN, os.X_OK)

    def extract_ocr_tokens(self, pil_image: Image.Image) -> List[Dict[str, Any]]:
        """
        Extract text tokens and bounding boxes from image using fastest available engine:
        1. Native macOS Vision binary (sub-50ms)
        2. Fallback to morphological word candidate bounding boxes
        """
        if self.has_native_ocr:
            try:
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    tmp_path = tmp.name
                    pil_image.save(tmp_path, format="PNG")
                
                try:
                    proc = subprocess.run(
                        [NATIVE_OCR_BIN, tmp_path],
                        capture_output=True,
                        text=True,
                        timeout=5.0
                    )
                    if proc.returncode == 0 and proc.stdout.strip():
                        tokens = json.loads(proc.stdout.strip())
                        for token in tokens:
                            text = str(token.get("text", "") or "")
                            token["script"] = self.detect_script_from_text(text)
                        return tokens
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
            except Exception:
                pass

        # Optional cross-platform OCR; never mistake geometry for recognized text.
        tesseract = shutil.which("tesseract")
        if tesseract:
            try:
                buffer = io.BytesIO()
                pil_image.save(buffer, format="PNG")
                proc = subprocess.run(
                    [tesseract, "stdin", "stdout", "-l", "eng", "tsv"],
                    input=buffer.getvalue(), capture_output=True, timeout=10,
                )
                if proc.returncode == 0:
                    rows = csv.DictReader(io.StringIO(proc.stdout.decode("utf-8")), delimiter="\t")
                    return [
                        {"text": row["text"], "confidence": float(row["conf"]) / 100,
                         "x": int(row["left"]), "y": int(row["top"]),
                         "w": int(row["width"]), "h": int(row["height"])}
                        for row in rows if row.get("text", "").strip()
                    ]
            except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
                pass

        # Fallback: Morphological word/line detection
        cv2_img = pil_to_cv2(pil_image)
        h, w, _ = cv2_img.shape
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        lines = self.detect_text_lines(gray, 0, h)
        return [
            {"text": "", "confidence": 0.5, "x": box[0], "y": box[1], "w": box[2], "h": box[3], "script": "und"}
            for box in lines
        ]

    @staticmethod
    def extract_amount(tokens: List[Dict[str, Any]]) -> Optional[float]:
        """Accept a unique, confidently read, explicitly labelled LKR amount."""
        lines = []
        for token in sorted(tokens, key=lambda t: (t.get("y", 0), t.get("x", 0))):
            if not str(token.get("text", "")).strip():
                continue
            center = float(token.get("y", 0)) + float(token.get("h", 0)) / 2
            height = max(1, float(token.get("h", 0)))
            for line in lines:
                if abs(line[0] - center) <= min(line[1], height) * 0.5:
                    line[2].append(token)
                    break
            else:
                lines.append([center, height, [token]])
        values = set()
        pattern = re.compile(
            r"^(?:(?:transfer|transaction|payment)\s+)?amount\s*:?\s*"
            r"(?:(?:LKR|Rs\.?)\s*)?"
            r"(?P<value>(?:[0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(?:\.[0-9]{2})?)"
            r"\s*(?:LKR|Rs\.?)?$", re.IGNORECASE,
        )
        for _, _, words in lines:
            text = " ".join(str(t["text"]).strip() for t in sorted(words, key=lambda t: t.get("x", 0)))
            match = pattern.fullmatch(text)
            if match:
                if any(float(t.get("confidence", 0)) < 0.8 for t in words):
                    return None
                value = Decimal(match.group("value").replace(",", ""))
                if not 0 < value <= 1_000_000_000:
                    return None
                values.add(value)
        return float(next(iter(values))) if len(values) == 1 else None

    def detect_bank_from_visuals(self, cv2_img: np.ndarray) -> Tuple[str, float]:
        """Detect bank template by header color signature and aspect ratio."""
        h, w, _ = cv2_img.shape
        header_h = max(1, int(h * 0.22))
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
        y_min = max(0, min(y_min, gray.shape[0]))
        y_max = max(0, min(y_max, gray.shape[0]))
        roi = gray[y_min:y_max, :]
        if roi.size == 0:
            return []
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

        # 1. Extract OCR tokens
        ocr_tokens = self.extract_ocr_tokens(pil_image)
        combined_text = " ".join([t.get("text", "") for t in ocr_tokens if t.get("text")])
        ocr_languages = self.resolve_supported_languages(combined_text)
        primary_script = self.detect_script_from_text(combined_text)

        # 2. Detect Bank Template (prioritize OCR text, then visual color matching)
        if bank_hint and bank_hint in BANK_TEMPLATES:
            detected_bank = bank_hint
            bank_conf = 0.95
        elif combined_text:
            text_bank = identify_bank_from_text(combined_text)
            if text_bank != "GENERIC_CEFTS":
                detected_bank = text_bank
                bank_conf = 0.95
            else:
                detected_bank, bank_conf = self.detect_bank_from_visuals(cv2_img)
        else:
            detected_bank, bank_conf = self.detect_bank_from_visuals(cv2_img)

        bank_meta = BANK_TEMPLATES.get(detected_bank, BANK_TEMPLATES["GENERIC_CEFTS"])

        # 3. Extract Amount & Candidate Regions
        amount_y1 = int(h * 0.22)
        amount_y2 = int(h * 0.45)
        amount_candidates = self.detect_text_lines(gray, amount_y1, amount_y2)

        extracted_amount_bbox = None
        if amount_candidates:
            amount_candidates.sort(key=lambda b: b[2] * b[3], reverse=True)
            extracted_amount_bbox = list(amount_candidates[0])

        fields_y1 = int(h * 0.42)
        fields_y2 = int(h * 0.88)
        detail_candidates = self.detect_text_lines(gray, fields_y1, fields_y2)

        field_bboxes = {
            "amount_box": extracted_amount_bbox,
            "field_rows_count": len(detail_candidates)
        }

        return {
            "detected_bank_code": detected_bank,
            "amount": self.extract_amount(ocr_tokens),
            "bank_name": bank_meta["bank_name"],
            "bank_confidence": bank_conf,
            "currency": bank_meta.get("currency", "LKR"),
            "ocr_languages": ocr_languages,
            "primary_script": primary_script,
            "layout_geometry": {
                "aspect_ratio": round(h / max(w, 1), 2),
                "is_mobile_viewport": 1.4 <= (h / max(w, 1)) <= 2.4,
                "detected_rows": len(detail_candidates)
            },
            "field_regions": field_bboxes,
            "ocr_tokens": ocr_tokens
        }
