# VeriSlip Comprehensive Manual Testing & Audit Guide

This guide provides a step-by-step procedure to manually test and inspect every component of the **VeriSlip Digital Bank Slip Forensic Verification Engine**.

---

## 📋 Table of Contents
1. [Starting the VeriSlip Server](#1-starting-the-verislip-server)
2. [Testing Datasets & Assets](#2-testing-datasets--assets)
3. [Frontend Web Cockpit Walkthrough](#3-frontend-web-cockpit-walkthrough)
   - [Single Slip Forensic Analysis](#31-single-slip-forensic-analysis)
   - [Forensic PDF Report Export](#32-forensic-pdf-report-export)
   - [Batch Slip Auditor](#33-batch-slip-auditor)
   - [Verification History & PII Scrubbing](#34-verification-history--pii-scrubbing)
   - [Triage Review Cockpit & Keyboard Shortcuts](#35-triage-review-cockpit--keyboard-shortcuts)
4. [Backend API Manual Verification (cURL Examples)](#4-backend-api-manual-verification-curl-examples)
   - [Core Slip Verification (`/api/v1/verify`)](#41-core-slip-verification)
   - [Courier Rider Instant API (`/api/v1/courier/verify`)](#42-courier-rider-instant-api)
   - [Shopify Webhook Gateway (`/api/v1/webhooks/shopify`)](#43-shopify-webhook-gateway)
   - [WhatsApp Webhook Gateway (`/api/v1/webhooks/whatsapp`)](#44-whatsapp-webhook-gateway)
   - [Rate Limiting & Merchant Credits](#45-rate-limiting--merchant-credits)
5. [Algorithmic Forensics Verification](#5-algorithmic-forensics-verification)
   - [Layer 1: Bank Template Matching](#layer-1-bank-template-matching)
   - [Layer 2: Chromatic ELA & JPEG Grid Shift](#layer-2-chromatic-ela--jpeg-grid-shift)
   - [Layer 3: SRM High-Pass Filtering & Noise Inconsistency](#layer-3-srm-high-pass-filtering--noise-inconsistency)
   - [Layer 4: Dual-Stream Deep Learning Fusion](#layer-4-dual-stream-deep-learning-fusion)
6. [Automated Verification Commands](#6-automated-verification-commands)
7. [Shutting Down & Port Management](#7-shutting-down--port-management)

---

## 1. Starting the VeriSlip Server

To launch the FastAPI server and Web Cockpit:

```bash
cd /Users/chirana/IdeaProjects/VeriSlip
python3 -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

- **Web Cockpit UI:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **OpenAPI JSON Schema:** [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 2. Testing Datasets & Assets

All real-world curated testing slips are stored in the repo:
- **Authentic Sri Lankan Bank Slips (30 samples):**
  `datasets/real_calibration/authentic/`
  *(Includes ComBank, Sampath, BOC, HNB, FriMi, Seylan, DFCC, Pan Asia in PDF & PNG)*
- **Tampered / Fraudulent Slips (9 samples):**
  `datasets/real_calibration/tampered/`
  *(Includes forged amounts like 4,200 vs 42,000, spliced transaction IDs, altered dates, Photoshop font overlays)*

---

## 3. Frontend Web Cockpit Walkthrough

Open **`http://127.0.0.1:8000/`** in your browser.

### 3.1 Single Slip Forensic Analysis
1. Navigate to the **"Analyze Slip"** tab.
2. **Test Authentic Slip:**
   - Drag & drop `datasets/real_calibration/authentic/Fund Transfer Receipt.pdf` (or any authentic PNG/PDF).
   - Click **"Run Forensic Audit"**.
   - **Expected Outcome:**
     - Status Badge: **`AUTHENTIC`** (Green).
     - Tamper Risk: `< 15%`.
     - Bank Recognized: e.g. Commercial Bank / BOC / Sampath.
     - Confidence: High.
     - 0 Tamper Bounding Boxes.
3. **Test Tampered Slip:**
   - Drag & drop `datasets/real_calibration/tampered/4,200.png` or `Receipt484674420260721120449252000.pdf`.
   - Click **"Run Forensic Audit"**.
   - **Expected Outcome:**
     - Status Badge: **`HIGH_RISK_TAMPERED`** (Red) or **`SUSPICIOUS`** (Amber).
     - Tamper Risk: `> 75%`.
     - Interactive Image Canvas overlays **red bounding boxes** exactly around spliced numbers.
     - Hover over bounding boxes to inspect confidence scores and splice classifications.
     - ELA and Noise Heatmap tabs display localized spectral anomalies.

### 3.2 Forensic PDF Report Export
1. On any completed analysis screen, click the **"Export Forensic PDF Report"** button.
2. Verify that a court-ready, multi-page forensic audit dossier (`VeriSlip_Forensic_Report_*.pdf`) is generated and downloaded.
3. Open the PDF:
   - Check the header with Verification ID, Timestamp, and Tamper Risk Gauge.
   - Verify that Layer 1 through Layer 4 breakdown tables are rendered.
   - Verify the embedded ELA heatmap and highlighted anomaly bounding boxes.

### 3.3 Batch Slip Auditor
1. Click the **"Batch Auditor"** tab in the top navigation bar.
2. Drag & drop 5 to 10 files from `datasets/real_calibration/authentic/` and `datasets/real_calibration/tampered/`.
3. Click **"Start Batch Audit"**.
4. **Expected Outcome:**
   - Real-time progress bar advances smoothly.
   - Table populates with filename, identified bank, extracted amount, risk score, and verdict badges.
   - Filter dropdowns allow filtering by `Authentic`, `Suspicious`, or `Tampered`.
   - Click **"Export CSV"** to verify audit log export.

### 3.4 Verification History & PII Scrubbing
1. Click the **"History"** tab.
2. **Expected Outcome:**
   - Past verifications appear sorted by newest first.
   - Search box filters by reference number.
   - Date range pickers filter records.
   - **PII Scrubbing Verification:** Verify that raw bank account numbers and customer names never appear in the history records (they are replaced by HMAC-SHA256 hashes like `[ACCOUNT:sha256:860adf3cf821417a]` or sanitized metadata).

### 3.5 Triage Review Cockpit & Keyboard Shortcuts
1. Open the Triage Cockpit view (or triage review modal).
2. Test keyboard navigation:
   - Press **`Space`**: Confirms and accepts the slip as authentic (without scrolling the browser page).
   - Press **`X`** or **`x`**: Rejects / flags the slip as fraudulent.
3. Test that shortcuts are disabled when typing inside search/input fields to prevent accidental triggers.

---

## 4. Backend API Manual Verification (cURL Examples)

Execute these cURL commands in your terminal while the server is running:

### 4.1 Core Slip Verification
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/verify" \
  -H "X-API-Key: test-pro-key" \
  -F "file=@datasets/real_calibration/authentic/Fund Transfer Receipt.pdf"
```
**Expected JSON:**
```json
{
  "verification_id": "...",
  "verdict": "AUTHENTIC",
  "tamper_risk_percentage": 0.7,
  "bank_name": "Commercial Bank of Ceylon",
  "bank_code": "COMBANK",
  "layer_breakdowns": { ... }
}
```

Now test against a tampered slip:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/verify" \
  -H "X-API-Key: test-pro-key" \
  -F "file=@datasets/real_calibration/tampered/4,200.png"
```
**Expected JSON:**
- `"verdict": "HIGH_RISK_TAMPERED"`
- `"tamper_risk_percentage": 98.0`
- `"bounding_boxes"` contains 2 localized splice regions.

### 4.2 Courier Rider Instant API
Riders on delivery can verify slips instantly with low payload overhead:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/courier/verify" \
  -H "X-API-Key: test-pro-key" \
  -F "file=@datasets/real_calibration/authentic/Fund Transfer Receipt.pdf" \
  -F "expected_amount=5000.00"
```
**Expected JSON:**
```json
{
  "status": "APPROVED",
  "is_valid": true,
  "reason": "Authentic slip and amount match",
  "rider_instructions": "Proceed with parcel handover"
}
```

### 4.3 Shopify Webhook Gateway
Simulate an automated Shopify order creation webhook requiring payment verification:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/webhooks/shopify" \
  -H "Content-Type: application/json" \
  -H "X-Shopify-Hmac-Sha256: test-hmac" \
  -d '{
    "id": 1009281,
    "order_number": 1059,
    "total_price": "15000.00",
    "currency": "LKR",
    "note_attributes": [
      {"name": "payment_receipt_url", "value": "https://example.com/receipt.jpg"}
    ]
  }'
```

### 4.4 WhatsApp Webhook Gateway
Verify incoming WhatsApp webhook verification challenge:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/webhooks/whatsapp?hub.mode=subscribe&hub.challenge=test_challenge_123&hub.verify_token=verislip_webhook_secret"
```
**Expected Output:** `test_challenge_123`

### 4.5 Rate Limiting & Merchant Credits
1. Check current API credit balance:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/credits/balance" \
  -H "X-API-Key: test-pro-key"
```
2. Rapidly fire 35 requests in a bash loop to test token bucket rate limiting:
```bash
for i in {1..35}; do
  curl -s -o /dev/null -w "%{http_code}\n" -X GET "http://127.0.0.1:8000/health" -H "X-API-Key: test-free-key"
done
```
**Expected Output:** The first requests return `200`, followed by HTTP `429 Too Many Requests` once tier tokens are exhausted.

---

## 5. Algorithmic Forensics Verification

### Layer 1: Bank Template Matching
- Verifies exact coordinates, aspect ratios, and reference number checksum regexes for all 8 supported Sri Lankan banks:
  - Commercial Bank (`COMBANK`)
  - Sampath Bank (`SAMPATH`)
  - Bank of Ceylon (`BOC`)
  - Hatton National Bank (`HNB`)
  - Seylan Bank (`SEYLAN`)
  - Nations Trust Bank / FriMi (`NTB`)
  - DFCC Bank (`DFCC`)
  - Pan Asia Bank (`PAN_ASIA`)

### Layer 2: Chromatic ELA & JPEG Grid Shift
- **Chromatic vs Luminance ELA (`decompose_ela_channels`):**
  Decomposes recompression error into Y (luminance) and CbCr (chrominance). Spliced digital text tampering generates significant spikes in $Y$ while chrominance channels remain flat.
- **JPEG Grid Shift (`detect_jpeg_grid_shift`):**
  Measures block boundary discontinuities across horizontal and vertical shifts $(dx, dy) \in [0..7]$. Spliced elements pasted from different JPEG documents expose non-aligned 8x8 block grid shifts.

### Layer 3: SRM High-Pass Filtering & Noise Inconsistency
- **Spatial Rich Models (SRM):**
  Applies $3\times 3$ and $5\times 5$ linear high-pass filter kernels (`srm_1st_horizontal`, `srm_2nd_vertical`, `srm_edge_3x3`, `srm_edge_5x5`) to reveal noise variance discontinuities where clone-stamping or brush marks were applied.

### Layer 4: Dual-Stream Deep Learning Fusion
- Runs CNN feature extraction across two complementary streams:
  1. Spatial RGB Stream (visual layout and text features)
  2. Frequency / ELA Error Stream (high-pass artifacts)
- Pretrained weights loaded from `weights/verislip_dualstream_best.pt`.

---

## 6. Automated Verification Commands

Run these automated verification commands at any time:

```bash
# 1. Run all 195 Python unit and integration tests
python3 -m pytest

# 2. Run frontend Node.js triage tests
node --test tests/frontend/triage_shortcuts.test.cjs

# 3. Run real-world empirical calibration accuracy benchmark
python3 scripts/benchmark_accuracy.py
```

**Expected Accuracy Benchmark Output:**
- Overall Accuracy: **100.00%**
- False Positive Rate (FPR): **0.00%**
- False Negative Rate (FNR): **0.00%**
- Mean Latency: ~400–450 ms/slip

---

## 7. Shutting Down & Port Management

To ensure all background processes and ports are closed when you finish:

```bash
# Check if port 8000 is running
lsof -i :8000

# Kill process on port 8000 if active
kill -9 $(lsof -ti :8000) 2>/dev/null || true
```
