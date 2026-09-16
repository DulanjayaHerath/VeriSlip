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
            notes.append(f"Metadata read note: {str(e)}")

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

    def evaluate(self, pil_image: Image.Image, bank_code: Optional[str] = None, reference_no: Optional[str] = None) -> Dict[str, Any]:
        """
        Run full Layer 1 validation and compute structural anomaly score (0.0 = clean, 1.0 = highly anomalous).
        """
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
            "findings": all_notes
        }
