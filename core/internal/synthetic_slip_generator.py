"""Internal-only synthetic slip and tampering engine.

This module is intended exclusively for offline training, calibration, and tests. It
must never be imported by an API route or other user-facing runtime. Construction is
deny-by-default and requires ``VERISLIP_ENABLE_SYNTHETIC_GENERATOR=1``.
"""

import os
import io
import random
from typing import Dict, Any, Tuple, List, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2

from core.templates.bank_rules import BANK_TEMPLATES

# Try loading standard system fonts, fallback to default
def get_font(size: int = 18, bold: bool = False):
    font_paths = [
        # macOS paths
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFPro.ttf",
        "/Library/Fonts/Arial.ttf",
        # Generic / Linux paths
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

class SyntheticSlipGenerator:
    """Generate training-only synthetic slips when explicitly enabled."""

    def __init__(self, width: int = 420, height: int = 740):
        if os.getenv("VERISLIP_ENABLE_SYNTHETIC_GENERATOR") != "1":
            raise RuntimeError(
                "Synthetic slip generation is disabled. Set "
                "VERISLIP_ENABLE_SYNTHETIC_GENERATOR=1 only in an authorized "
                "offline training or test environment."
            )
        self.width = width
        self.height = height

    def generate_authentic_slip(
        self,
        bank_code: str = "COMBANK",
        amount_lkr: float = 12500.00,
        ref_no: Optional[str] = None,
        beneficiary_name: str = "K. A. D. Silva",
        date_str: str = "16/09/2026 14:32:10"
    ) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Render a clean, high-fidelity synthetic mobile banking transfer slip.
        """
        template = BANK_TEMPLATES.get(bank_code, BANK_TEMPLATES["COMBANK"])
        brand_color = template["primary_color_rgb"]

        if not ref_no:
            ref_no = f"TXN{random.randint(1000000000, 9999999999)}"

        img = Image.new("RGB", (self.width, self.height), color=(248, 249, 252))
        draw = ImageDraw.Draw(img)

        # Draw status bar mock
        draw.rectangle([(0, 0), (self.width, 26)], fill=(235, 238, 242))
        font_small = get_font(12)
        font_regular = get_font(14)
        font_bold = get_font(16, bold=True)
        font_title = get_font(20, bold=True)
        font_amount = get_font(28, bold=True)

        draw.text((16, 6), "09:41", fill=(60, 60, 60), font=font_small)
        draw.text((self.width - 70, 6), "LTE  100%", fill=(60, 60, 60), font=font_small)

        # Draw Bank Header
        draw.rectangle([(0, 26), (self.width, 110)], fill=brand_color)
        draw.text((20, 42), template["app_name"], fill=(255, 255, 255), font=font_title)
        draw.text((20, 74), "Payment Confirmation", fill=(220, 235, 255), font=font_regular)

        # Receipt Container Card
        card_x1, card_y1, card_x2, card_y2 = 20, 130, self.width - 20, self.height - 40
        draw.rounded_rectangle([(card_x1, card_y1), (card_x2, card_y2)], radius=12, fill=(255, 255, 255), outline=(225, 230, 238))

        # Checkmark Icon Circle
        circle_cx, circle_cy = self.width // 2, card_y1 + 45
        draw.ellipse([(circle_cx - 24, circle_cy - 24), (circle_cx + 24, circle_cy + 24)], fill=(46, 175, 80))
        draw.text((circle_cx - 8, circle_cy - 12), "✓", fill=(255, 255, 255), font=font_title)

        draw.text((circle_cx - 65, circle_cy + 34), "Transfer Successful", fill=(30, 41, 59), font=font_bold)

        # Transfer Amount Section
        amount_y = circle_cy + 75
        formatted_amount = f"LKR {amount_lkr:,.2f}"
        # Measure text width roughly
        draw.text((card_x1 + 35, amount_y), formatted_amount, fill=brand_color, font=font_amount)
        amount_bbox = [card_x1 + 30, amount_y - 5, card_x2 - 30, amount_y + 38]

        # Horizontal Divider
        draw.line([(card_x1 + 20, amount_y + 55), (card_x2 - 20, amount_y + 55)], fill=(235, 240, 245), width=1)

        # Fields Section
        field_start_y = amount_y + 70
        spacing = 42

        fields = [
            ("Reference No", ref_no),
            ("Beneficiary", beneficiary_name),
            ("To Account", "XXXX-XXXX-8921"),
            ("Transfer Type", "CEFTS Real-Time"),
            ("Date & Time", date_str),
            ("Status", "COMPLETED")
        ]

        field_bboxes = {}
        for idx, (label, val) in enumerate(fields):
            curr_y = field_start_y + (idx * spacing)
            draw.text((card_x1 + 20, curr_y), label, fill=(110, 120, 135), font=font_regular)
            draw.text((card_x1 + 140, curr_y), val, fill=(30, 41, 59), font=font_bold if label == "Status" else font_regular)
            field_bboxes[label] = [card_x1 + 135, curr_y - 2, card_x2 - 15, curr_y + 24]

        field_bboxes["Amount"] = amount_bbox

        # Footer security seal note
        draw.text((circle_cx - 95, card_y2 - 30), "Verified Electronic Transfer Receipt", fill=(160, 170, 185), font=font_small)

        metadata = {
            "bank_code": bank_code,
            "bank_name": template["bank_name"],
            "amount": amount_lkr,
            "reference_no": ref_no,
            "beneficiary_name": beneficiary_name,
            "date_str": date_str,
            "field_bboxes": field_bboxes,
            "is_tampered": False
        }

        # Apply realistic smartphone JPEG compression
        buf = io_buf = np.array(img)
        # Encode as JPEG
        _, enc = cv2.imencode('.jpg', cv2.cvtColor(buf, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), 92])
        dec = cv2.imdecode(enc, cv2.IMREAD_COLOR)
        final_pil = Image.fromarray(cv2.cvtColor(dec, cv2.COLOR_BGR2RGB))

        return final_pil, metadata

    def generate_tampered_slip(
        self,
        authentic_slip: Image.Image,
        metadata: Dict[str, Any],
        tamper_type: str = "ALTER_AMOUNT",
        new_amount: float = 125000.00,
        **kwargs: Any
    ) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Simulate real-world fraud tampering on an authentic slip:
        - Erasing amount and pasting forged amount
        - Altering reference number
        - Introducing compression mismatch & font edge disparity
        """
        tampered = authentic_slip.copy()
        draw = ImageDraw.Draw(tampered)
        tamper_metadata = dict(metadata)
        tamper_metadata["is_tampered"] = True
        tamper_metadata["tamper_type"] = tamper_type

        brand_color = BANK_TEMPLATES.get(metadata["bank_code"], BANK_TEMPLATES["COMBANK"])["primary_color_rgb"]

        flagged_boxes = []

        if tamper_type == "ALTER_AMOUNT":
            bbox = metadata["field_bboxes"]["Amount"]
            x1, y1, x2, y2 = bbox

            # Simulate attacker drawing white rectangle or clone stamping to erase original amount
            draw.rectangle([(x1, y1), (x2, y2)], fill=(255, 255, 255))
            
            # Splicing in altered amount with slightly mismatched font & color
            font_tampered = get_font(28, bold=True)
            new_amount_str = f"LKR {new_amount:,.2f}"
            
            # Attacker often gets color or alignment slightly off
            attacker_color = (brand_color[0] + 15, max(0, brand_color[1] - 10), min(255, brand_color[2] + 20))
            draw.text((x1 + 5, y1 + 5), new_amount_str, fill=attacker_color, font=font_tampered)

            flagged_boxes.append({
                "box": [x1, y1, x2 - x1, y2 - y1],
                "label": "Forged Transaction Amount",
                "original_value": f"LKR {metadata['amount']:,.2f}",
                "tampered_value": new_amount_str
            })
            tamper_metadata["tampered_amount"] = new_amount

        elif tamper_type in ("ALTER_REFERENCE", "SPOOF_REFERENCE"):
            bbox = metadata["field_bboxes"]["Reference No"]
            x1, y1, x2, y2 = bbox

            draw.rectangle([(x1, y1), (x2, y2)], fill=(255, 255, 255))
            font_tampered = get_font(14)
            fake_ref = kwargs.get("new_reference", f"TXN{random.randint(1000000000, 9999999999)}")
            draw.text((x1 + 5, y1 + 2), fake_ref, fill=(20, 20, 20), font=font_tampered)

            flagged_boxes.append({
                "box": [x1, y1, x2 - x1, y2 - y1],
                "label": "Altered Reference Number",
                "original_value": metadata["reference_no"],
                "tampered_value": fake_ref
            })
            tamper_metadata["tampered_reference"] = fake_ref

        elif tamper_type in ("SWAP_BENEFICIARY", "ALTER_BENEFICIARY"):
            bbox = metadata["field_bboxes"].get("Beneficiary")
            if bbox:
                x1, y1, x2, y2 = bbox
                draw.rectangle([(x1, y1), (x2, y2)], fill=(255, 255, 255))
                font_tampered = get_font(14)
                fake_beneficiary = kwargs.get("new_beneficiary_name", "K. M. Wickramasinghe")
                draw.text((x1 + 5, y1 + 2), fake_beneficiary, fill=(20, 20, 20), font=font_tampered)

                flagged_boxes.append({
                    "box": [x1, y1, x2 - x1, y2 - y1],
                    "label": "Swapped Beneficiary Name",
                    "original_value": metadata.get("beneficiary_name", ""),
                    "tampered_value": fake_beneficiary
                })
                tamper_metadata["tampered_beneficiary"] = fake_beneficiary

        elif tamper_type in ("SWAP_ACCOUNT", "ALTER_ACCOUNT"):
            bbox = metadata["field_bboxes"].get("To Account")
            if bbox:
                x1, y1, x2, y2 = bbox
                draw.rectangle([(x1, y1), (x2, y2)], fill=(255, 255, 255))
                font_tampered = get_font(14)
                fake_account = kwargs.get("new_account", "XXXX-XXXX-9901")
                draw.text((x1 + 5, y1 + 2), fake_account, fill=(20, 20, 20), font=font_tampered)

                flagged_boxes.append({
                    "box": [x1, y1, x2 - x1, y2 - y1],
                    "label": "Swapped Beneficiary Account",
                    "original_value": "XXXX-XXXX-8921",
                    "tampered_value": fake_account
                })
                tamper_metadata["tampered_account"] = fake_account

        elif tamper_type in ("ALTER_DATE", "SPOOF_TIMESTAMP", "ALTER_TIMESTAMP"):
            bbox = metadata["field_bboxes"].get("Date & Time")
            if bbox:
                x1, y1, x2, y2 = bbox
                draw.rectangle([(x1, y1), (x2, y2)], fill=(255, 255, 255))
                font_tampered = get_font(14)
                fake_date = kwargs.get("new_date", "2026-09-18 11:20:45")
                draw.text((x1 + 5, y1 + 2), fake_date, fill=(20, 20, 20), font=font_tampered)

                flagged_boxes.append({
                    "box": [x1, y1, x2 - x1, y2 - y1],
                    "label": "Spoofed Transaction Timestamp",
                    "original_value": metadata.get("date_str", ""),
                    "tampered_value": fake_date
                })
                tamper_metadata["tampered_date_time"] = fake_date

        # Re-save with JPEG compression and inject editing software EXIF metadata
        cv2_img = cv2.cvtColor(np.array(tampered), cv2.COLOR_RGB2BGR)
        _, enc = cv2.imencode('.jpg', cv2_img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        dec = cv2.imdecode(enc, cv2.IMREAD_COLOR)
        final_pil = Image.fromarray(cv2.cvtColor(dec, cv2.COLOR_BGR2RGB))

        # Add editing software metadata trace (Photoshop Express / Canva)
        exif = final_pil.getexif()
        exif[0x0131] = "Adobe Photoshop Express"
        buf = io.BytesIO()
        final_pil.save(buf, format="JPEG", quality=82, exif=exif)
        buf.seek(0)
        final_pil = Image.open(buf)

        tamper_metadata["ground_truth_boxes"] = flagged_boxes
        return final_pil, tamper_metadata
