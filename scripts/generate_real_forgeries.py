#!/usr/bin/env python3
"""
VeriSlip Semi-Synthetic Real Forgery Generator (Internal Forensics Benchmark Tool)
Generates high-fidelity tampered variants from real authentic slips:
1. Spliced amounts with subtle baseline & kerning mismatch
2. Localized copy-paste / clone-stamp patches
3. Multi-pass JPEG & WhatsApp re-compression (Q=60..92)
4. Canva/markup metadata injection
Strictly internal: never exposed on public API endpoints (Policy PR #101).
"""

import os
import sys
import argparse
import random
import io
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.calibrate_real_slips import find_images_in_dir, load_slip_as_pil


FAKE_AMOUNTS = [
    "LKR 850,000.00",
    "LKR 1,250,000.00",
    "Rs. 450,000.00",
    "LKR 95,000.00",
    "LKR 3,500,000.00",
    "Rs. 185,000.00",
    "LKR 620,000.00",
    "LKR 2,100,000.00",
]


def splice_amount_with_baseline_offset(img: Image.Image) -> Image.Image:
    """Simulate Canva/markup amount splice with subtle baseline & font discrepancy."""
    w, h = img.size
    img_np = np.array(img.convert("RGB"))

    # Financial transaction body typically between 25% and 60% height
    bx = int(w * random.uniform(0.20, 0.35))
    by = int(h * random.uniform(0.28, 0.52))
    bw = int(w * random.uniform(0.40, 0.55))
    bh = int(h * random.uniform(0.04, 0.07))

    # Create localized inpainting patch (solid or subtle background clone)
    bg_color = np.median(img_np[by:by+bh, bx:bx+bw], axis=(0, 1)).astype(np.uint8)
    patch = np.full((bh, bw, 3), bg_color, dtype=np.uint8)

    # Add Gaussian sensor noise to match background
    noise = np.random.normal(0, random.uniform(1.5, 4.0), patch.shape).astype(np.int16)
    patch = np.clip(patch.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Splice fake amount text with baseline jump
    text = random.choice(FAKE_AMOUNTS)
    font_scale = random.uniform(0.55, 0.75)
    thickness = random.choice([1, 2])
    text_color = (random.randint(15, 40), random.randint(15, 40), random.randint(15, 40))
    baseline_y = int(bh * random.uniform(0.60, 0.85))

    cv2.putText(
        patch,
        text,
        (int(bw * 0.05), baseline_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        text_color,
        thickness,
        cv2.LINE_AA,
    )

    # Blend patch into original image
    img_np[by:by+bh, bx:bx+bw] = patch
    res_pil = Image.fromarray(img_np)

    # Apply WhatsApp / social media re-compression
    q = random.randint(65, 88)
    buf = io.BytesIO()
    res_pil.save(buf, format="JPEG", quality=q)
    buf.seek(0)
    return Image.open(buf)


def splice_clone_stamp_patch(img: Image.Image) -> Image.Image:
    """Simulate clone-stamp removal of reference number or timestamp."""
    w, h = img.size
    img_np = np.array(img.convert("RGB"))

    # Source clean background block
    src_x = int(w * 0.10)
    src_y = int(h * 0.70)
    pw = int(w * 0.25)
    ph = int(h * 0.05)

    source_patch = img_np[src_y:src_y+ph, src_x:src_x+pw].copy()

    # Destination target area to obscure
    dst_x = int(w * 0.35)
    dst_y = int(h * random.uniform(0.35, 0.55))

    # Apply subtle feathering at patch borders
    feathered = cv2.GaussianBlur(source_patch, (5, 5), 0)
    img_np[dst_y:dst_y+ph, dst_x:dst_x+pw] = feathered

    res_pil = Image.fromarray(img_np)
    buf = io.BytesIO()
    res_pil.save(buf, format="JPEG", quality=random.randint(70, 85))
    buf.seek(0)
    return Image.open(buf)


def inject_canva_markup_metadata(img: Image.Image) -> Image.Image:
    """Simulate Canva or Adobe mobile markup software fingerprint."""
    spliced = splice_amount_with_baseline_offset(img)
    info_dict = spliced.info.copy()
    info_dict["Software"] = random.choice(["Canva Mobile Editor v2.4", "Adobe Photoshop Express 2026", "PicsArt Photo Studio"])
    spliced.info = info_dict
    return spliced


def generate_forgeries(
    authentic_dir: str = "datasets/real_calibration/authentic",
    output_dir: str = "datasets/real_calibration/forgeries_augmented",
    variants_per_slip: int = 2,
):
    os.makedirs(output_dir, exist_ok=True)
    auth_files = find_images_in_dir(authentic_dir)

    print("=" * 70)
    print(" 🛠️  VeriSlip Semi-Synthetic Real Forgery Generator")
    print(f" Source Authentic Directory: {authentic_dir} ({len(auth_files)} slips)")
    print(f" Target Output Directory:   {output_dir}")
    print(f" Variants per slip:         {variants_per_slip}")
    print("=" * 70)

    total_created = 0
    for idx, path in enumerate(auth_files, 1):
        base = os.path.splitext(os.path.basename(path))[0]
        # Clean double extensions if present
        base = base.replace(".pdf", "")
        img = load_slip_as_pil(path)

        for v in range(variants_per_slip):
            forge_type = v % 3
            if forge_type == 0:
                forged = splice_amount_with_baseline_offset(img)
                suffix = "spliced_amount"
            elif forge_type == 1:
                forged = splice_clone_stamp_patch(img)
                suffix = "clone_stamp"
            else:
                forged = inject_canva_markup_metadata(img)
                suffix = "canva_markup"

            out_name = f"{base}_forge_{v+1}_{suffix}.png"
            out_path = os.path.join(output_dir, out_name)
            forged.save(out_path, format="PNG")
            total_created += 1

    print(f"\n✓ Successfully synthesized {total_created} high-fidelity tampered slips!")
    print(f"📁 Saved to: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate realistic semi-synthetic slip forgeries")
    parser.add_argument("--authentic-dir", default="datasets/real_calibration/authentic")
    parser.add_argument("--output-dir", default="datasets/real_calibration/forgeries_augmented")
    parser.add_argument("--variants", type=int, default=2)
    args = parser.parse_args()

    generate_forgeries(args.authentic_dir, args.output_dir, args.variants)
