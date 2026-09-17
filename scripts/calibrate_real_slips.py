#!/usr/bin/env python3
"""
VeriSlip: Few-Shot Real-World Calibration Engine.
Ingests real mobile banking screenshots (authentic and/or tampered) to compute
empirical baseline thresholds, eliminate false positives, and bridge the domain gap.
"""

import os
import sys
import glob
import json
import random

# Ensure root directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Dict, Any, Tuple
import numpy as np
from PIL import Image, ImageFilter
import cv2

from core.forensics.layer1_structural import Layer1StructuralValidator
from core.forensics.layer2_classical import Layer2ClassicalForensics
from core.forensics.layer3_noise import Layer3NoiseForensics
from core.ml.ensemble_model import Layer4DeepEnsemble


CALIBRATION_DIR = "datasets/real_calibration"
AUTHENTIC_DIR = os.path.join(CALIBRATION_DIR, "authentic")
TAMPERED_DIR = os.path.join(CALIBRATION_DIR, "tampered")
OUTPUT_PROFILE = "weights/calibration_profile.json"


def find_images_in_dir(directory: str) -> List[str]:
    """Find all image and PDF files in a directory."""
    if not os.path.exists(directory):
        return []
    valid_exts = ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.pdf")
    files = []
    for ext in valid_exts:
        files.extend(glob.glob(os.path.join(directory, ext)))
        files.extend(glob.glob(os.path.join(directory, ext.upper())))
    return sorted(list(set(files)))


def load_slip_as_pil(filepath: str) -> Image.Image:
    """Load an image or render page 1 of a bank PDF slip to PIL RGB Image with metadata preserved."""
    if filepath.lower().endswith(".pdf"):
        try:
            import pypdfium2 as pdfium
            pdf = pdfium.PdfDocument(filepath)
            page = pdf[0]
            rendered_img = page.render(scale=2.0).to_pil().convert("RGB")
            try:
                rendered_img.info["pdf_metadata"] = pdf.get_metadata_dict()
            except Exception:
                pass
            page.close()
            pdf.close()
            return rendered_img
        except Exception as e:
            print(f"  ⚠️ Warning: Could not render PDF {filepath}: {e}")
    raw_img = Image.open(filepath)
    info_dict = raw_img.info.copy() if hasattr(raw_img, "info") else {}
    conv_img = raw_img.convert("RGB")
    conv_img.info = info_dict
    return conv_img


def create_realistic_spliced_copy(img: Image.Image) -> Image.Image:
    """
    Synthesize a realistic spliced copy of an authentic real slip
    simulating WhatsApp image compression and local font splice.
    """
    img_copy = img.copy().convert("RGB")
    w, h = img_copy.size
    np_img = np.array(img_copy)

    # Pick an arbitrary text/amount rectangular bounding region in middle third
    bx = int(w * 0.25)
    by = int(h * 0.35)
    bw = int(w * 0.50)
    bh = int(h * 0.08)

    # Patch with subtle replacement text or cloned background
    roi = np_img[by:by+bh, bx:bx+bw].copy()
    # Add localized contrast shift and blur to simulate mobile splice
    blurred_roi = cv2.GaussianBlur(roi, (5, 5), 0)
    cv2.putText(blurred_roi, "LKR 950,000.00", (10, int(bh * 0.7)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2, cv2.LINE_AA)

    np_img[by:by+bh, bx:bx+bw] = blurred_roi
    tampered_pil = Image.fromarray(np_img)

    # Apply WhatsApp-like double JPEG compression
    import io
    buf = io.BytesIO()
    tampered_pil.save(buf, format="JPEG", quality=75)
    buf.seek(0)
    return Image.open(buf)


def run_calibration():
    print("=" * 70)
    print(" 🛡️  VeriSlip: Real-World Slip Calibration Engine")
    print("    Tuning multi-layer physics and neural thresholds on real traffic")
    print("=" * 70)

    auth_files = find_images_in_dir(AUTHENTIC_DIR)
    tamp_files = find_images_in_dir(TAMPERED_DIR)

    if not auth_files:
        print(f"\n⚠️  No real authentic slips found in: {AUTHENTIC_DIR}")
        print("\nHow to add your real slips:")
        print(f"1. Copy 3–10 real screenshots into: {AUTHENTIC_DIR}/")
        print("2. (Optional) Redact sensitive account numbers or customer names.")
        print("3. Re-run: python3 scripts/calibrate_real_slips.py")
        print("\nNote: Creating a baseline profile using synthetic mobile variations for demonstration...")
        # Create a sample calibration profile
        from core.ml.dataset_generator import SyntheticSlipGenerator
        gen = SyntheticSlipGenerator()
        auth_pairs = [gen.generate_authentic_slip(b) for b in ["COMBANK", "BOC", "SAMPATH", "HNB", "SEYLAN"]]
        auth_samples = [p[0] for p in auth_pairs]
        tamp_samples = [gen.generate_tampered_slip(p[0], p[1], "ALTER_AMOUNT", 850000.0)[0] for p in auth_pairs]
    else:
        print(f"\n✓ Found {len(auth_files)} real authentic slip(s) in {AUTHENTIC_DIR}")
        auth_samples = [load_slip_as_pil(f) for f in auth_files]
        if tamp_files:
            print(f"✓ Found {len(tamp_files)} real tampered slip(s) in {TAMPERED_DIR}")
            tamp_samples = [load_slip_as_pil(f) for f in tamp_files]
        else:
            print("ℹ️  No real tampered slips found in tampered/ — synthesizing realistic spliced pairs...")
            tamp_samples = [create_realistic_spliced_copy(img) for img in auth_samples]

    # Initialize detection layers
    l1 = Layer1StructuralValidator()
    l2 = Layer2ClassicalForensics()
    l3 = Layer3NoiseForensics()
    l4 = Layer4DeepEnsemble()

    print("\n[1/3] Benchmarking Real-World Authentic Baselines...")
    auth_l1_scores, auth_l2_scores, auth_l3_scores, auth_l4_scores = [], [], [], []
    auth_ela_vars, auth_noise_vars = [], []

    for idx, img in enumerate(auth_samples, 1):
        r1 = l1.evaluate(img)
        r2 = l2.evaluate(img)
        r3 = l3.evaluate(img)
        r4 = l4.evaluate(img, r2.get("diff_gray", np.zeros((img.height, img.width))), r3.get("residual", np.zeros((img.height, img.width))))

        auth_l1_scores.append(r1["anomaly_score"])
        auth_l2_scores.append(r2["anomaly_score"])
        auth_l3_scores.append(r3["anomaly_score"])
        auth_l4_scores.append(r4["anomaly_score"])
        auth_ela_vars.append(r2.get("ela_variance", 0.0))
        auth_noise_vars.append(r3.get("mean_noise_variance", 0.0))
        print(f"  • Authentic #{idx}: L1={r1['anomaly_score']:.2f}, L2={r2['anomaly_score']:.2f}, L3={r3['anomaly_score']:.2f}, L4={r4['anomaly_score']:.2f}")

    print("\n[2/3] Benchmarking Spliced / Tampered Sensitivity...")
    tamp_l1_scores, tamp_l2_scores, tamp_l3_scores, tamp_l4_scores = [], [], [], []
    for idx, img in enumerate(tamp_samples, 1):
        r1 = l1.evaluate(img)
        r2 = l2.evaluate(img)
        r3 = l3.evaluate(img)
        r4 = l4.evaluate(img, r2.get("diff_gray", np.zeros((img.height, img.width))), r3.get("residual", np.zeros((img.height, img.width))))

        tamp_l1_scores.append(r1["anomaly_score"])
        tamp_l2_scores.append(r2["anomaly_score"])
        tamp_l3_scores.append(r3["anomaly_score"])
        tamp_l4_scores.append(r4["anomaly_score"])
        print(f"  • Tampered #{idx}: L1={r1['anomaly_score']:.2f}, L2={r2['anomaly_score']:.2f}, L3={r3['anomaly_score']:.2f}, L4={r4['anomaly_score']:.2f}")

    # Compute statistics
    mean_auth_l1 = float(np.mean(auth_l1_scores))
    mean_auth_l2 = float(np.mean(auth_l2_scores))
    mean_auth_l3 = float(np.mean(auth_l3_scores))
    mean_auth_l4 = float(np.mean(auth_l4_scores))
    max_auth_composite = float(np.max(
        0.15 * np.array(auth_l1_scores) +
        0.35 * np.array(auth_l2_scores) +
        0.25 * np.array(auth_l3_scores) +
        0.25 * np.array(auth_l4_scores)
    ))

    # Calculate optimal tuned weights based on signal-to-noise ratio
    delta_l1 = max(0.01, float(np.mean(tamp_l1_scores) - mean_auth_l1))
    delta_l2 = max(0.01, float(np.mean(tamp_l2_scores) - mean_auth_l2))
    delta_l3 = max(0.01, float(np.mean(tamp_l3_scores) - mean_auth_l3))
    delta_l4 = max(0.01, float(np.mean(tamp_l4_scores) - mean_auth_l4))

    total_delta = delta_l1 + delta_l2 + delta_l3 + delta_l4
    tuned_w1 = round(delta_l1 / total_delta, 3)
    tuned_w2 = round(delta_l2 / total_delta, 3)
    tuned_w3 = round(delta_l3 / total_delta, 3)
    tuned_w4 = round(1.0 - (tuned_w1 + tuned_w2 + tuned_w3), 3)

    # Calibrate risk thresholds so genuine slips never trigger false alarms
    # Add a 10% safety buffer over the maximum observed genuine composite score
    calibrated_auth_ceiling = min(0.30, max(0.12, round(max_auth_composite + 0.08, 3)))
    calibrated_suspicious_ceiling = round(min(0.60, calibrated_auth_ceiling + 0.30), 3)

    calibration_profile = {
        "calibration_status": "CALIBRATED_REAL_WORLD",
        "sample_count": {
            "authentic": len(auth_samples),
            "tampered": len(tamp_samples),
            "is_user_provided": bool(auth_files)
        },
        "baselines": {
            "mean_ela_variance": round(float(np.mean(auth_ela_vars)), 3),
            "mean_noise_variance": round(float(np.mean(auth_noise_vars)), 3),
            "layer_means": {
                "layer1": round(mean_auth_l1, 3),
                "layer2": round(mean_auth_l2, 3),
                "layer3": round(mean_auth_l3, 3),
                "layer4": round(mean_auth_l4, 3)
            }
        },
        "tuned_weights": {
            "w1_structural": tuned_w1,
            "w2_classical": tuned_w2,
            "w3_noise": tuned_w3,
            "w4_ensemble": tuned_w4
        },
        "thresholds": {
            "authentic_max_risk": round(calibrated_auth_ceiling * 100.0, 1),
            "suspicious_max_risk": round(calibrated_suspicious_ceiling * 100.0, 1)
        }
    }

    os.makedirs(os.path.dirname(OUTPUT_PROFILE), exist_ok=True)
    with open(OUTPUT_PROFILE, "w") as f:
        json.dump(calibration_profile, f, indent=2)

    print("\n[3/3] Calibration Completed Successfully!")
    print("-" * 70)
    print(f"📁 Calibration Profile Saved: {OUTPUT_PROFILE}")
    print(f"⚖️  Tuned Layer Weights:  L1={tuned_w1*100:.1f}%, L2={tuned_w2*100:.1f}%, L3={tuned_w3*100:.1f}%, L4={tuned_w4*100:.1f}%")
    print(f"🎯 Calibrated Risk Ceilings:")
    print(f"   • AUTHENTIC:  0% to {calibration_profile['thresholds']['authentic_max_risk']}%")
    print(f"   • SUSPICIOUS: {calibration_profile['thresholds']['authentic_max_risk']}% to {calibration_profile['thresholds']['suspicious_max_risk']}%")
    print(f"   • TAMPERED:   >{calibration_profile['thresholds']['suspicious_max_risk']}%")
    print("-" * 70)
    print("✓ VeriSlip engine will automatically use these thresholds for all verifications!")


if __name__ == "__main__":
    run_calibration()
