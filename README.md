# VeriSlip — AI Forensic Slip & Invoice Tamper Detection

[![VeriSlip CI](https://github.com/actions/workflows/ci.yml/badge.svg)](https://github.com)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**VeriSlip** is an AI-powered image forensic detection platform and fraud prevention engine specifically designed to detect doctored bank transfer slips, payment receipts, and invoices in peer-to-peer commerce and delivery logistics (Facebook Marketplace, Instagram sellers, WhatsApp Business, and COD couriers in Sri Lanka and emerging South Asian markets).

---

## 🏛️ Detection Architecture

VeriSlip combines classical multi-scale image forensics with a learned deep learning ensemble:

* **Layer 1 (Structural & Metadata):** Bank template layout grids, logo anchors, reference number checksum/regex (Commercial Bank, Sampath Vishwa, Bank of Ceylon, Hatton National Bank, CEFTS), and EXIF editing software tags (`Photoshop`, `Canva`, `PicsArt`, `GIMP`).
* **Layer 2 (Classical Forensics):** Multi-scale Error Level Analysis (ELA) with amplified difference mapping, 8x8 2D-DCT double-JPEG compression periodicity analysis, and subpixel font edge consistency.
* **Layer 3 (Noise Residuals):** High-pass spatial filtering (`residual = |gray - median_blur(gray)|`) with zero-edge background masking to detect spliced or clone-stamped text patches.
* **Layer 4 (Ensemble Deep Learning):** PyTorch dual-stream fusion model combining raw image patches and forensic feature maps for calibrated tamper probability scoring and bounding box localization.
* **Layer 5 (Enterprise Moat):** Direct programmatic transaction verification gateway with LankaPay/CEFTS and partner bank merchant APIs.

---

## 👥 3-Person Team Division

The project is structured into three clear engineering pillars:

| Founder | Track | Focus Area & Deliverables | Backlog Issues |
| :--- | :--- | :--- | :--- |
| **Person 1** | **Forensic CV Lead** | Layers 1–3: Bank rules, ELA, DCT compression, noise residuals, splicing detection | Issues #1 – #28 |
| **Person 2** | **Data & ML Lead** | Synthetic tampering engine, PII redaction, Layer 4 deep learning ensemble | Issues #29 – #56 |
| **Person 3** | **Full-Stack & Biz Lead** | FastAPI production server, Web Cockpit UI, WhatsApp Bot, Courier API, billing | Issues #57 – #82 |
| **All (Shared)** | **DevOps & Research** | CI/CD, Docker, Security/Ethics, Research Paper (MERCon), Seller Beta Pilot | Issues #83 – #100 |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
* Python 3.10 or higher
* Node.js (optional, for web assets)
* Git

### 2. Installation
```bash
git clone https://github.com/YOUR_USERNAME/VeriSlip.git
cd VeriSlip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Automated Tests
```bash
pytest tests/ -v
```

### 4. Launch Local Server & Web Cockpit
```bash
python3 -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your web browser:
* **Forensic Cockpit:** Test authentic slips vs tampered amount forgeries in one click.
* **Interactive Heatmaps:** Toggle between raw screenshot, ELA heatmap, noise map, and red bounding boxes.
* **WhatsApp Bot Simulator:** Test the merchant chat flow.
* **Monetization Calculator:** Real-time unit economics estimator.

---

## 📋 100 GitHub Issues for Team Collaboration

To make it effortless for you and your friends to collaborate, we have created an exhaustive, prioritized backlog of **100 GitHub issues** across all 4 streams.

### View the Backlog
Browse the complete list in [docs/ISSUES_BACKLOG.md](docs/ISSUES_BACKLOG.md).

### Batch Import All 100 Issues into Your GitHub Repo
1. Authenticate with GitHub:
   ```bash
   gh auth login
   ```
2. Run the automated issue creator script:
   ```bash
   python3 scripts/create_github_issues.py --repo YOUR_GITHUB_USERNAME/VeriSlip
   ```
3. To preview without creating:
   ```bash
   python3 scripts/create_github_issues.py --dry-run
   ```

---

## 💡 Profitability & Commercial Strategy

1. **WhatsApp Bot Micro-SaaS (B2C):**
   * Instant verification for Instagram and WhatsApp sellers directly inside chat (<3s).
   * **Pricing:** 10 free checks/mo, then **LKR 1,490/month Pro pack** or LKR 10/check prepaid credits.
2. **Logistics & Courier Delivery API (B2B):**
   * Mobile SDK/API for courier driver apps (Domex, Koombiyo, PromptX) verifying buyer deposit claims before handing over COD packages.
   * **Pricing:** **LKR 8.00 per API call**.
3. **Shopify & WooCommerce Auto-Verify Plugin:**
   * Automated verification of direct bank transfer slips uploaded by online shoppers ($29/month).
4. **Official Forensic Audit Certificate:**
   * Downloadable cryptographically signed PDF evidence packs for police cybercrime complaints and bank disputes (LKR 1,500 / $5).

---

## 📂 Project Structure

```
VeriSlip/
├── api/                        # FastAPI Backend Service
│   ├── main.py                 # App entrypoint & static mounting
│   ├── routes/                 # Verification, Forensics, WhatsApp webhook
│   └── schemas/                # Pydantic models
├── core/                       # Core Forensics & Detection Engines
│   ├── templates/              # Bank specifications (ComBank, Sampath, BOC, HNB, CEFTS)
│   ├── forensics/              # Layer 1 (Structural), Layer 2 (ELA/DCT), Layer 3 (Noise)
│   └── ml/                     # Synthetic tampering engine & Layer 4 ensemble
├── web/                        # Premium Web Cockpit UI (HTML/CSS/JS)
├── docs/                       # Project Documentation & ISSUES_BACKLOG.md
├── scripts/                    # Issue creator script & dataset utilities
├── tests/                      # Pytest automated test suite (12 tests)
├── .github/                    # CI/CD workflows and issue templates
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview
```

---

## 📄 Research & Ethics Statement
* **Dual-Use Containment:** The synthetic tampering generator is strictly internal for training data creation and unit testing; it is never exposed publicly.
* **PII Redaction:** Real customer account numbers and names are automatically redacted or synthesized.
