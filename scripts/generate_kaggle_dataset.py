#!/usr/bin/env python3
"""
Automated Synthetic Dataset Generator & Packager for VeriSlip.
Generates balanced, pixel-accurate training pairs (authentic & doctored slips)
with ground-truth binary segmentation masks and metadata CSV.
Outputs a clean zip archive ready to upload to Kaggle Datasets.
"""

import os
import sys
import argparse
import random
import zipfile
from datetime import datetime
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
from tqdm import tqdm

# Ensure core packages can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.internal.synthetic_slip_generator import SyntheticSlipGenerator
from core.templates.bank_rules import BANK_TEMPLATES

BANKS = ["COMBANK", "SAMPATH", "BOC", "HNB", "SEYLAN", "NTB_FRIMI", "GENERIC_CEFTS"]
TAMPER_TYPES = ["ALTER_AMOUNT", "ALTER_REFERENCE"]

BENEFICIARY_NAMES = [
    "K. A. D. Silva", "M. R. Fernando", "Sunil Perera", "Nimalka Jayasinghe",
    "T. M. Wickramasinghe", "Chaminda Vaas", "G. H. Mendis", "Priyantha Kumara",
    "TechZone Colombo", "Daraz Merchant Direct", "Galle Face Foods", "Urban Trends LK"
]

def create_binary_mask(width: int, height: int, boxes: list) -> Image.Image:
    """Create a single-channel 8-bit binary mask (255 for tampered, 0 for authentic)."""
    mask = Image.new("L", (width, height), color=0)
    draw = ImageDraw.Draw(mask)
    for b in boxes:
        x, y, w, h = b["box"]
        draw.rectangle([(x, y), (x + w, y + h)], fill=255)
    return mask

def main():
    parser = argparse.ArgumentParser(description="Generate VeriSlip Kaggle Dataset")
    parser.add_argument("--samples", type=int, default=1000, help="Total number of image pairs to generate")
    parser.add_argument("--output-dir", type=str, default="verislip_dataset", help="Output directory")
    parser.add_argument("--train-ratio", type=float, default=0.8, help="Ratio for train split (remainder is validation)")
    parser.add_argument("--zip", action="store_true", default=True, help="Create a verislip_dataset.zip archive")
    args = parser.parse_args()

    total_samples = args.samples
    output_dir = os.path.abspath(args.output_dir)
    train_dir = os.path.join(output_dir, "train")
    val_dir = os.path.join(output_dir, "val")

    for split_dir in [train_dir, val_dir]:
        os.makedirs(os.path.join(split_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(split_dir, "masks"), exist_ok=True)

    print(f"==================================================")
    print(f"🚀 VeriSlip Synthetic Dataset Generator")
    print(f"   Target Samples : {total_samples}")
    print(f"   Train / Val    : {int(args.train_ratio * 100)}% / {int((1 - args.train_ratio) * 100)}%")
    print(f"   Output Folder  : {output_dir}")
    print(f"   Supported Banks: {', '.join(BANKS)}")
    print(f"==================================================")

    generator = SyntheticSlipGenerator(width=420, height=740)
    records = []

    # Generate 50% authentic, 50% tampered
    num_pairs = total_samples // 2
    train_cutoff = int(num_pairs * args.train_ratio)

    print("\n[1/3] Generating synthetic bank transfer slips & ground-truth masks...")
    pair_counter = 0

    for i in tqdm(range(num_pairs), desc="Generating pairs"):
        bank = random.choice(BANKS)
        beneficiary = random.choice(BENEFICIARY_NAMES)
        amount = round(random.uniform(1500, 95000), 2)
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        split = "train" if i < train_cutoff else "val"

        # 1. Generate Authentic Slip
        auth_img, auth_meta = generator.generate_authentic_slip(
            bank_code=bank,
            amount_lkr=amount,
            beneficiary_name=beneficiary,
            date_str=date_str
        )
        auth_fname = f"slip_{i:05d}_auth.png"
        auth_mask_fname = f"mask_{i:05d}_auth.png"

        auth_img_path = os.path.join(output_dir, split, "images", auth_fname)
        auth_mask_path = os.path.join(output_dir, split, "masks", auth_mask_fname)

        auth_img.save(auth_img_path, format="PNG")
        # Empty mask for authentic slip
        auth_mask = create_binary_mask(420, 740, [])
        auth_mask.save(auth_mask_path, format="PNG")

        records.append({
            "image_id": f"slip_{i:05d}_auth",
            "split": split,
            "filename": os.path.join(split, "images", auth_fname),
            "mask_filename": os.path.join(split, "masks", auth_mask_fname),
            "bank_code": bank,
            "is_tampered": 0,
            "tamper_type": "NONE",
            "bbox_x": -1,
            "bbox_y": -1,
            "bbox_w": -1,
            "bbox_h": -1,
            "amount_lkr": amount,
            "reference_no": auth_meta["reference_no"]
        })

        # 2. Generate Doctored / Tampered Variant
        tamper_type = random.choice(TAMPER_TYPES)
        forged_amount = round(amount * random.uniform(2.5, 12.0), 2)

        tampered_img, tampered_meta = generator.generate_tampered_slip(
            authentic_slip=auth_img,
            metadata=auth_meta,
            tamper_type=tamper_type,
            new_amount=forged_amount
        )
        tamp_fname = f"slip_{i:05d}_tamp.png"
        tamp_mask_fname = f"mask_{i:05d}_tamp.png"

        tamp_img_path = os.path.join(output_dir, split, "images", tamp_fname)
        tamp_mask_path = os.path.join(output_dir, split, "masks", tamp_mask_fname)

        tampered_img.save(tamp_img_path, format="PNG")
        
        boxes = tampered_meta.get("ground_truth_boxes", [])
        tamp_mask = create_binary_mask(420, 740, boxes)
        tamp_mask.save(tamp_mask_path, format="PNG")

        primary_box = boxes[0]["box"] if boxes else [-1, -1, -1, -1]

        records.append({
            "image_id": f"slip_{i:05d}_tamp",
            "split": split,
            "filename": os.path.join(split, "images", tamp_fname),
            "mask_filename": os.path.join(split, "masks", tamp_mask_fname),
            "bank_code": bank,
            "is_tampered": 1,
            "tamper_type": tamper_type,
            "bbox_x": primary_box[0],
            "bbox_y": primary_box[1],
            "bbox_w": primary_box[2],
            "bbox_h": primary_box[3],
            "amount_lkr": forged_amount if tamper_type == "ALTER_AMOUNT" else amount,
            "reference_no": tampered_meta.get("tampered_reference", auth_meta["reference_no"])
        })

    # Save CSV metadata
    print("\n[2/3] Exporting structured metadata CSV & dataset documentation...")
    df = pd.DataFrame(records)
    csv_path = os.path.join(output_dir, "dataset_metadata.csv")
    df.to_csv(csv_path, index=False)
    print(f"  ✓ Saved metadata ledger: {csv_path} ({len(df)} total annotated items)")

    # Write Dataset Card
    card_path = os.path.join(output_dir, "DATASET_CARD.md")
    with open(card_path, "w") as f:
        f.write(f"""# VeriSlip South Asian Bank Transfer Forgery Benchmark Dataset

- **Generated On:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Total Samples:** {len(df)} images ({len(df[df['is_tampered']==0])} Authentic, {len(df[df['is_tampered']==1])} Tampered)
- **Image Resolution:** 420 x 740 (Standard Mobile Viewport)
- **Supported Banks:** {', '.join(BANKS)}
- **Ground Truth Format:**
  - `images/`: RGB PNG payment slip screenshots
  - `masks/`: 1-channel binary segmentation masks (255 = Forged pixels, 0 = Clean background)
  - `dataset_metadata.csv`: Full tabular bounding box and class labels

### Class & Bank Distribution:
{df.groupby(['bank_code', 'is_tampered']).size().to_string()}
""")
    print(f"  ✓ Created DATASET_CARD.md")

    # Zip packaging
    if args.zip:
        zip_filename = f"verislip_kaggle_dataset.zip"
        print(f"\n[3/3] Compressing into '{zip_filename}' for Kaggle upload...")
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(output_dir))
                    zipf.write(file_path, arcname)
        zip_size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
        print(f"  ✓ Compression Complete! Archive: {os.path.abspath(zip_filename)} ({zip_size_mb:.1f} MB)")

    print(f"\n✅ All Done! Ready to upload to Kaggle Datasets.")

if __name__ == "__main__":
    main()
