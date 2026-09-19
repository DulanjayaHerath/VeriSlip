"""
Layer 2 Forensic Subsystem: Copy-Move Forgery Detection.
Implements:
1. ORB/SIFT keypoint-based clone detection with shift-vector clustering (#19).
2. Block-based DCT lexicographical correlation with 2D translation accumulator (#20).
"""

from collections import Counter
from typing import Dict, Any, List, Tuple
import numpy as np
import cv2


def detect_copymove_orb(
    cv2_bgr: np.ndarray,
    min_spatial_dist: float = 30.0,
    match_ratio: float = 0.75,
    shift_bin_size: float = 18.0,
    min_cluster_matches: int = 6,
    min_matches: int = None,
    max_features: int = 1500
) -> Dict[str, Any]:
    """
    Detect copy-move forgery using ORB/SIFT keypoint matching and shift-vector clustering (#19).
    Cloned regions share a consistent translation vector (dx, dy).
    Inline typographic repetitions (e.g. repeated '0' or 'M' along same horizontal baseline) are filtered out.
    """
    if min_matches is not None:
        min_cluster_matches = min_matches

    if cv2_bgr is None or cv2_bgr.size == 0:
        return {"detected": False, "match_count": 0, "confidence": 0.0, "clone_pairs": [], "method": "orb"}

    gray = cv2.cvtColor(cv2_bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    detector = cv2.ORB_create(nfeatures=max_features)
    method = "orb"
    keypoints, descriptors = detector.detectAndCompute(gray, None)

    if descriptors is None or len(descriptors) < 10:
        return {"detected": False, "match_count": 0, "confidence": 0.0, "clone_pairs": [], "method": method}

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    try:
        knn_matches = matcher.knnMatch(descriptors, descriptors, k=3)
    except Exception:
        return {"detected": False, "match_count": 0, "confidence": 0.0, "clone_pairs": [], "method": method}

    raw_pairs = []
    seen = set()

    for match in knn_matches:
        if len(match) < 2:
            continue
        m1 = match[1] if match[0].trainIdx == match[0].queryIdx else match[0]
        m2 = match[2] if len(match) > 2 else match[1]

        if m1.trainIdx == m1.queryIdx:
            continue

        # Ratio test
        if m1.distance < match_ratio * m2.distance + 1e-4:
            i1, i2 = m1.queryIdx, m1.trainIdx
            pair = tuple(sorted([i1, i2]))
            if pair in seen:
                continue
            seen.add(pair)

            pt1 = np.array(keypoints[pair[0]].pt)
            pt2 = np.array(keypoints[pair[1]].pt)

            spatial_dist = float(np.linalg.norm(pt1 - pt2))
            if spatial_dist >= min_spatial_dist:
                # Canonical ordering
                if (pt1[0] > pt2[0]) or (pt1[0] == pt2[0] and pt1[1] > pt2[1]):
                    pt1, pt2 = pt2, pt1

                dx = pt2[0] - pt1[0]
                dy = pt2[1] - pt1[1]

                # Filter out pure horizontal inline typographic repeats (same line baseline dy < 6 and dx < 80)
                if abs(dy) < 6.0 and abs(dx) < 80.0:
                    continue

                raw_pairs.append({
                    "src_pt": (round(float(pt1[0]), 1), round(float(pt1[1]), 1)),
                    "dst_pt": (round(float(pt2[0]), 1), round(float(pt2[1]), 1)),
                    "dx": dx,
                    "dy": dy,
                    "spatial_distance": round(spatial_dist, 1),
                    "descriptor_distance": float(m1.distance)
                })

    if not raw_pairs:
        return {"detected": False, "match_count": 0, "confidence": 0.0, "clone_pairs": [], "method": method}

    # Shift-vector clustering
    shift_bins = Counter()
    for p in raw_pairs:
        bin_x = int(round(p["dx"] / shift_bin_size))
        bin_y = int(round(p["dy"] / shift_bin_size))
        shift_bins[(bin_x, bin_y)] += 1

    most_common = shift_bins.most_common(1)
    if not most_common:
        return {"detected": False, "match_count": 0, "confidence": 0.0, "clone_pairs": [], "method": method}

    best_bin, max_cluster_size = most_common[0]
    bx, by = best_bin

    clustered_pairs = [
        p for p in raw_pairs
        if abs(int(round(p["dx"] / shift_bin_size)) - bx) <= 1 and
           abs(int(round(p["dy"] / shift_bin_size)) - by) <= 1
    ]

    # Filter out 1D collinear same-baseline typographic repetition (repeated 0s or letters on same line)
    if clustered_pairs:
        src_ys = [p["src_pt"][1] for p in clustered_pairs]
        y_span = max(src_ys) - min(src_ys)
        avg_dy = abs(sum(p["dy"] for p in clustered_pairs) / len(clustered_pairs))
        if avg_dy < 8.0 and y_span < 15.0:
            clustered_pairs = []

    detected = len(clustered_pairs) >= min_cluster_matches
    confidence = min(0.98, max(0.0, (len(clustered_pairs) - min_cluster_matches + 1) / (min_cluster_matches * 2.5))) if detected else 0.0

    return {
        "detected": detected,
        "match_count": len(clustered_pairs),
        "confidence": round(confidence, 3),
        "dominant_shift": (round(bx * shift_bin_size, 1), round(by * shift_bin_size, 1)),
        "clone_pairs": clustered_pairs[:30],
        "method": method
    }


def detect_copymove_block_dct(
    cv2_bgr: np.ndarray,
    block_size: int = 8,
    step: int = 4,
    q_factor: float = 16.0,
    min_shift: float = 25.0,
    shift_bin_size: float = 16.0,
    min_cluster_matches: int = 6,
    min_matches: int = None,
    similarity_thresh: float = 1.0,
    min_texture_std: float = 10.0
) -> Dict[str, Any]:
    """
    Detect dense copy-move forgery via overlapping block DCT lexicographical correlation (#20).
    Uses a 2D shift-vector accumulator to filter out coincidental flat texture matches.
    Inline typographic repeats (dy < 6, dx < 80) are filtered out.
    """
    if min_matches is not None:
        min_cluster_matches = min_matches

    if cv2_bgr is None or cv2_bgr.size == 0:
        return {"detected": False, "match_count": 0, "confidence": 0.0, "matches": []}

    gray = cv2.cvtColor(cv2_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    h, w = gray.shape

    scale = 1.0
    if max(h, w) > 500:
        scale = 500.0 / max(h, w)
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
        h, w = gray.shape

    b = block_size
    if h < b * 2 or w < b * 2:
        return {"detected": False, "match_count": 0, "confidence": 0.0, "matches": []}

    vectors = []
    positions = []

    # 15 AC coefficients
    mask = np.zeros((b, b), dtype=bool)
    mask[:4, :4] = True
    mask[0, 0] = False

    for y in range(0, h - b + 1, step):
        for x in range(0, w - b + 1, step):
            patch = gray[y:y+b, x:x+b]
            if np.std(patch) < min_texture_std:
                continue

            patch_centered = patch - 128.0
            dct_patch = cv2.dct(patch_centered)
            ac_coeffs = dct_patch[mask]

            quantized = np.round(ac_coeffs / q_factor).astype(np.int32)
            vectors.append(quantized)
            positions.append((x, y))

    if len(vectors) < 15:
        return {"detected": False, "match_count": 0, "confidence": 0.0, "matches": []}

    vectors = np.array(vectors)
    positions = np.array(positions)

    sort_idx = np.lexsort([vectors[:, i] for i in reversed(range(vectors.shape[1]))])
    sorted_vectors = vectors[sort_idx]
    sorted_positions = positions[sort_idx]

    num_vecs = len(sorted_vectors)
    candidate_pairs = []
    window = min(6, num_vecs)

    for i in range(num_vecs - 1):
        for j in range(i + 1, min(i + window, num_vecs)):
            diff = np.max(np.abs(sorted_vectors[i] - sorted_vectors[j]))
            if diff <= similarity_thresh:
                pt1 = sorted_positions[i]
                pt2 = sorted_positions[j]

                if (pt1[0] > pt2[0]) or (pt1[0] == pt2[0] and pt1[1] > pt2[1]):
                    pt1, pt2 = pt2, pt1

                dx = (pt2[0] - pt1[0]) / scale
                dy = (pt2[1] - pt1[1]) / scale
                spatial_dist = np.hypot(dx, dy)

                if spatial_dist >= min_shift:
                    # Filter out inline text repetition (same text line dy < 12.0)
                    if abs(dy) < 12.0:
                        continue

                    candidate_pairs.append({
                        "pt1": (int(round(pt1[0] / scale)), int(round(pt1[1] / scale))),
                        "pt2": (int(round(pt2[0] / scale)), int(round(pt2[1] / scale))),
                        "dx": dx,
                        "dy": dy,
                        "spatial_distance": round(float(spatial_dist), 1),
                    })
                    break

    if not candidate_pairs:
        return {"detected": False, "match_count": 0, "confidence": 0.0, "matches": []}

    # 2D shift-vector accumulation
    shift_bins = Counter()
    for p in candidate_pairs:
        bx = int(round(p["dx"] / shift_bin_size))
        by = int(round(p["dy"] / shift_bin_size))
        shift_bins[(bx, by)] += 1

    most_common = shift_bins.most_common(1)
    if not most_common:
        return {"detected": False, "match_count": 0, "confidence": 0.0, "matches": []}

    (best_bx, best_by), cluster_count = most_common[0]

    clustered_matches = [
        p for p in candidate_pairs
        if abs(int(round(p["dx"] / shift_bin_size)) - best_bx) <= 1 and
           abs(int(round(p["dy"] / shift_bin_size)) - best_by) <= 1
    ]

    detected = len(clustered_matches) >= min_cluster_matches
    confidence = min(0.95, max(0.0, (len(clustered_matches) - min_cluster_matches + 1) / (min_cluster_matches * 2.5))) if detected else 0.0

    return {
        "detected": detected,
        "match_count": len(clustered_matches),
        "confidence": round(confidence, 3),
        "dominant_shift": (round(best_bx * shift_bin_size, 1), round(best_by * shift_bin_size, 1)),
        "matches": clustered_matches[:30]
    }


def analyze_copymove_forensics(cv2_bgr: np.ndarray) -> Dict[str, Any]:
    """
    Unified entry point for copy-move forgery analysis combining keypoint and block DCT methods.
    """
    orb_res = detect_copymove_orb(cv2_bgr)
    dct_res = detect_copymove_block_dct(cv2_bgr)

    is_copymove = orb_res["detected"] or dct_res["detected"]
    composite_confidence = max(orb_res["confidence"], dct_res["confidence"])

    findings = []
    if orb_res["detected"]:
        findings.append(
            f"Keypoint-based copy-move cloning detected ({orb_res['match_count']} clustered feature pairs, conf: {orb_res['confidence']})."
        )
    if dct_res["detected"]:
        findings.append(
            f"Dense block-based DCT duplicated patch detected ({dct_res['match_count']} clustered 8x8 blocks, conf: {dct_res['confidence']})."
        )

    return {
        "has_copymove": is_copymove,
        "copymove_confidence": composite_confidence,
        "orb_detection": orb_res,
        "block_dct_detection": dct_res,
        "findings": findings
    }
