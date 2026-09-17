# VeriSlip: Open-Source Engineering & Research Backlog

This backlog outlines **100 actionable, prioritized issues** structured across 4 open-source domain tracks for collaborative development and research contributions.

---

## 👥 Domain Track Summary

| Domain Track | Key Technologies | Scope & Focus Areas |
| :--- | :--- | :--- |
| **Track 1: Forensic Computer Vision** | OpenCV, NumPy, SciPy | Layers 1–3: Bank Layouts, ELA, DCT, Sensor Noise, Splicing Localization |
| **Track 2: Machine Learning & Datasets** | PyTorch, Kaggle, CUDA | Synthetic Generator, PII Redaction, Layer 4 Deep Dual-Stream Fusion |
| **Track 3: Backend Systems & Client APIs** | FastAPI, WhatsApp Webhooks | Microservices, Web Cockpit, Courier SDK, Batch Auditor, Forensic PDFs |
| **Track 4: Infrastructure & Research** | GitHub Actions, Docker | CI/CD Automation, Security Governance, Empirical Calibration, Research |

---

## 📋 Complete List of 100 Issues

### 🔬 Track 1: Forensic Computer Vision & Signal Processing (Issues #1 to #28)

#### #1: [COMPLETED] [FORENSICS-CV] Implement ComBank Digital template layout grid and logo anchor verification
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-1, priority:medium, layer:layer-1, contributions-welcome`

### Overview
Create exact pixel-grid anchor coordinates, logo aspect ratio, and header layout checks for Commercial Bank mobile banking receipts. Acceptance criteria: tests match genuine ComBank screenshots and detect mismatched header proportions.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #2: [COMPLETED] [FORENSICS-CV] Implement Sampath Vishwa layout and color histogram matching
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-1, priority:medium, layer:layer-1, contributions-welcome`

### Overview
Add template definitions for Sampath Vishwa app including orange branding palette (RGB 243, 112, 33) and field positions. Acceptance criteria: verifies Sampath slip layout fidelity.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #3: [COMPLETED] [FORENSICS-CV] Implement Bank of Ceylon (BOC) Digi & SmartPay layout rules
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-1, priority:medium, layer:layer-1, contributions-welcome`

### Overview
Define layout parameters for BOC Digi and SmartPay receipts. Acceptance criteria: validates header badge, gold color accents, and standard field offsets.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #4: [COMPLETED] [FORENSICS-CV] Implement Hatton National Bank (HNB) SOLO & Digital Banking rules
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-1, priority:medium, layer:layer-1, contributions-welcome`

### Overview
Add support for HNB digital banking receipts including reference regex and dark blue/gold branding validation.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #5: [COMPLETED] [FORENSICS-CV] Add template matching for Seylan Bank (Seylan Mobile Banking)
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:medium, layer:layer-1, contributions-welcome`

### Overview
Implement template definition and field parser for Seylan Bank transfer receipts.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #6: [COMPLETED] [FORENSICS-CV] Add template matching for Nations Trust Bank (NTB / FriMi)
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:medium, layer:layer-1, contributions-welcome`

### Overview
Support FriMi and Nations Trust Bank slip templates with signature magenta/blue accents.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #7: [FORENSICS-CV] Add template matching for DFCC Bank and Pan Asia Bank
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:low, layer:layer-1, contributions-welcome`

### Overview
Add regex rules and color profiles for DFCC and Pan Asia Bank mobile receipts.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #8: [COMPLETED] [FORENSICS-CV] Implement generic CEFTS & SLIPS interbank slip layout validator
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `domain:cv-forensics, milestone:phase-1, priority:low, layer:layer-1, contributions-welcome`

### Overview
Validate generic interbank transfer receipts complying with LankaPay CEFTS standard fields.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #9: [COMPLETED] [FORENSICS-CV] Implement reference number checksum validation for Commercial Bank
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-1, priority:medium, layer:layer-1, contributions-welcome`

### Overview
Research and implement reference number syntax and mod-checksum rules for ComBank transaction IDs.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #10: [COMPLETED] [FORENSICS-CV] Implement reference number regex and length validator for Sampath & BOC
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `domain:cv-forensics, milestone:phase-1, priority:low, layer:layer-1, contributions-welcome`

### Overview
Validate reference number structures for Sampath Vishwa and BOC Digi, flagging synthetic sequential numbers.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #11: [COMPLETED] [FORENSICS-CV] Build EXIF metadata parser with expanded editing software signatures
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-1, priority:medium, layer:layer-1, contributions-welcome`

### Overview
Expand KNOWN_EDITING_SOFTWARE list to include Pixelmator, Photopea, VSCO, InShot, Procreate, and detect stripped EXIF markers.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #12: [COMPLETED] [FORENSICS-CV] Add PNG chunk metadata inspection for software and author signatures
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:low, layer:layer-1, contributions-welcome`

### Overview
Parse PNG textual chunks (tEXt, zTXt, iTXt) to identify software signatures injected by web/desktop image editors.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #13: [COMPLETED] [FORENSICS-CV] Implement timestamp sanity checks against displayed slip dates
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:medium, layer:layer-1, contributions-welcome`

### Overview
Cross-reference file creation/modification timestamps with receipt displayed date/time to flag retroactively altered slips.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #14: [COMPLETED] [FORENSICS-CV] Mobile screenshot aspect ratio and DPI resolution classifier
* **Domain:** `Computer Vision` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `domain:cv-forensics, milestone:phase-1, priority:low, layer:layer-1, contributions-welcome`

### Overview
Detect non-standard smartphone resolutions, upscaling artifacts, and desktop browser inspect-element proportions.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 1`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #15: [COMPLETED] [FORENSICS-CV] Implement multi-scale Error Level Analysis (ELA) with adaptive quality factors
* **Domain:** `Computer Vision` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `High`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:high, layer:layer-2, contributions-welcome`

### Overview
Evaluate image across multiple JPEG compression quality factors (Q75, Q85, Q90, Q95) and select optimal scale based on image base quality.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 2`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #16: [FORENSICS-CV] Implement chromatic vs luminance ELA difference decomposition
* **Domain:** `Computer Vision` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `High`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:high, layer:layer-2, contributions-welcome`

### Overview
Decompose ELA analysis into Y (luminance) and CbCr (chrominance) channels. Spliced text often exhibits anomalies predominantly in luminance.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 2`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #17: [COMPLETED] [FORENSICS-CV] Build 8x8 block-wise 2D-DCT AC frequency coefficient histogram analyzer
* **Domain:** `Computer Vision` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `High`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:high, layer:layer-2, contributions-welcome`

### Overview
Extract DCT coefficients for primary AC frequencies (1,2) and (2,1) across 8x8 blocks to calculate periodicity index.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 2`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #18: [FORENSICS-CV] Implement double-JPEG compression grid alignment and shift detector
* **Domain:** `Computer Vision` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `High`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:high, layer:layer-2, contributions-welcome`

### Overview
Detect non-aligned 8x8 JPEG block grids which occur when a cropped slip or spliced element is saved with different block boundaries.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 2`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #19: [FORENSICS-CV] Implement copy-move forgery detection using ORB/SIFT keypoint matching
* **Domain:** `Computer Vision` | **Layer:** `Layer 2` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `domain:cv-forensics, milestone:phase-3, priority:high, layer:layer-2, contributions-welcome`

### Overview
Detect cloned digits or pasted bank logos by clustering matched feature points between distinct regions of the receipt.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 2`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #20: [FORENSICS-CV] Implement block-based DCT correlation for dense copy-move detection
* **Domain:** `Computer Vision` | **Layer:** `Layer 2` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `domain:cv-forensics, milestone:phase-3, priority:high, layer:layer-2, contributions-welcome`

### Overview
Divide image into overlapping blocks and compute lexicographic sorting of DCT coefficients to identify duplicated image patches.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 2`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #21: [COMPLETED] [FORENSICS-CV] Build font stroke-width and edge anti-aliasing consistency checker
* **Domain:** `Computer Vision` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:medium, layer:layer-2, contributions-welcome`

### Overview
Measure Laplacian edge energy and gradient profile across text characters to detect font sharpness disparities between amount and card labels.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 2`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #22: [FORENSICS-CV] Implement text baseline alignment and spacing disparity detector
* **Domain:** `Computer Vision` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:medium, layer:layer-2, contributions-welcome`

### Overview
Detect vertical jitter, misaligned baseline bounding boxes, and uneven kerning introduced by manual text insertion.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 2`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #23: [FORENSICS-CV] Implement Spatial Rich Models (SRM) high-pass filtering kernels
* **Domain:** `Computer Vision` | **Layer:** `Layer 3` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `domain:cv-forensics, milestone:phase-3, priority:high, layer:layer-3, contributions-welcome`

### Overview
Apply standard 3x3 and 5x5 SRM linear and non-linear filter kernels to extract subtle noise residuals from screenshot canvas.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 3`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #24: [COMPLETED] [FORENSICS-CV] Calibrate noise residual variance estimation for flat UI backgrounds
* **Domain:** `Computer Vision` | **Layer:** `Layer 3` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:medium, layer:layer-3, contributions-welcome`

### Overview
Ensure edge-masked background regions calculate baseline noise variance without interference from typography anti-aliasing.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 3`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #25: [COMPLETED] [FORENSICS-CV] Implement local noise variance discontinuity clustering
* **Domain:** `Computer Vision` | **Layer:** `Layer 3` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:medium, layer:layer-3, contributions-welcome`

### Overview
Cluster neighboring outlier blocks to form coherent bounding boxes around erased or clone-stamped patches.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 3`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #26: [COMPLETED] [FORENSICS-CV] Detect median filter smoothing traces from brush / blur tools
* **Domain:** `Computer Vision` | **Layer:** `Layer 3` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `domain:cv-forensics, milestone:phase-3, priority:high, layer:layer-3, contributions-welcome`

### Overview
Analyze residual difference histograms to detect when an attacker applied a blur tool to blend forged numbers into the receipt.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 3`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #27: [COMPLETED] [FORENSICS-CV] Build visual side-by-side forensic heatmap generator (Jet/Inferno/Viridis)
* **Domain:** `Computer Vision` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:cv-forensics, milestone:phase-2, priority:low, layer:layer-2, contributions-welcome`

### Overview
Generate publication-ready composite images showing original slip side-by-side with ELA heatmap and noise residual map.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 2`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #28: [COMPLETED] [FORENSICS-CV] Optimize OpenCV forensic feature extraction pipeline for <500ms latency
* **Domain:** `Computer Vision` | **Layer:** `Layer 2` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `domain:cv-forensics, milestone:phase-3, priority:medium, layer:layer-2, contributions-welcome`

### Overview
Vectorize numpy loops and optimize image downsamping for high-throughput API execution.

### Domain & Subsystem
* **Technical Domain:** `Forensic Computer Vision & Signal Processing`
* **Detection Layer / Component:** `Layer 2`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.



---

### 🧠 Track 2: Machine Learning & Synthetic Datasets (Issues #29 to #56)

#### #29: [COMPLETED] [ML-DATA] Expand Synthetic Slip Generator to support all 5 top Sri Lankan bank templates
* **Domain:** `Machine Learning` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-1, priority:medium, layer:synthetic-data, contributions-welcome`

### Overview
Add high-fidelity vector rendering for ComBank, Sampath Vishwa, BOC Digi, HNB SOLO, and CEFTS slips.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Synthetic Data`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #30: [COMPLETED] [ML-DATA] Implement multi-tier tampering attack: Novice skill level
* **Domain:** `Machine Learning` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-1, priority:medium, layer:synthetic-data, contributions-welcome`

### Overview
Simulate novice edits: obvious font mismatches, misaligned text, uncompressed PNG text pasted on compressed JPEG.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Synthetic Data`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #31: [COMPLETED] [ML-DATA] Implement multi-tier tampering attack: Intermediate skill level
* **Domain:** `Machine Learning` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-2, priority:medium, layer:synthetic-data, contributions-welcome`

### Overview
Simulate intermediate edits: matched font family, approximate color match, and single recompression step.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Synthetic Data`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #32: [ML-DATA] Implement multi-tier tampering attack: Expert / Skilled level
* **Domain:** `Machine Learning` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `domain:ml-data, milestone:phase-3, priority:high, layer:synthetic-data, contributions-welcome`

### Overview
Simulate skilled adversary: matched font weight, anti-aliasing smoothing, matching local noise floor, and double-JPEG alignment.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Synthetic Data`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #33: [COMPLETED] [ML-DATA] Implement synthetic amount manipulation attack module
* **Domain:** `Machine Learning` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `domain:ml-data, milestone:phase-1, priority:low, layer:synthetic-data, contributions-welcome`

### Overview
Simulate replacing transaction amounts with 10x or 100x inflated values while generating exact ground-truth bounding boxes.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Synthetic Data`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #34: [COMPLETED] [ML-DATA] Implement synthetic reference number tampering module
* **Domain:** `Machine Learning` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `domain:ml-data, milestone:phase-1, priority:low, layer:synthetic-data, contributions-welcome`

### Overview
Simulate forged reference numbers with spliced digits or altered prefixes.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Synthetic Data`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #35: [ML-DATA] Implement synthetic beneficiary name & account swapping module
* **Domain:** `Machine Learning` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:ml-data, milestone:phase-2, priority:low, layer:synthetic-data, contributions-welcome`

### Overview
Simulate swapping beneficiary names and masked account numbers on receipts.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Synthetic Data`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #36: [ML-DATA] Implement date/timestamp modification attack module
* **Domain:** `Machine Learning` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:ml-data, milestone:phase-2, priority:low, layer:synthetic-data, contributions-welcome`

### Overview
Simulate recycling old payment slips by doctoring the transaction timestamp and date.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Synthetic Data`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #37: [ML-DATA] Build COCO & Pascal VOC annotation exporter for synthetic dataset
* **Domain:** `Machine Learning` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-2, priority:medium, layer:synthetic-data, contributions-welcome`

### Overview
Export generated tampered receipts with standard COCO JSON format bounding boxes and segmentation masks for object detection models.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Synthetic Data`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #38: [COMPLETED] [ML-DATA] Implement automated dataset generation CLI script with configurable sample count
* **Domain:** `Machine Learning` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:ml-data, milestone:phase-2, priority:low, layer:synthetic-data, contributions-welcome`

### Overview
Create script  with balanced authentic and tampered distributions.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Synthetic Data`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #39: [ML-DATA] Build automated PII redaction pipeline for collected real receipts
* **Domain:** `Machine Learning` | **Layer:** `Dataset` | **Milestone:** `Phase 1: Foundations` | **Priority:** `High`
* **Labels:** `domain:ml-data, milestone:phase-1, priority:high, layer:dataset, contributions-welcome`

### Overview
Automatically detect, blur, or synthesize real customer names, account numbers, and phone numbers before storing in research datasets.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Dataset`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #40: [ML-DATA] Collect and curate initial benchmark set of 200 permission-cleared genuine slips
* **Domain:** `Machine Learning` | **Layer:** `Dataset` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-2, priority:medium, layer:dataset, contributions-welcome`

### Overview
Gather consent-cleared slips from team transactions and merchant friends across different mobile operating systems (iOS and Android).

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Dataset`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #41: [COMPLETED] [ML-DATA] Create stratified dataset train/validation/test splits by bank and skill tier
* **Domain:** `Machine Learning` | **Layer:** `Dataset` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-2, priority:medium, layer:dataset, contributions-welcome`

### Overview
Establish strict train/val/test splits ensuring no bank template leakage to test zero-shot generalization on unseen bank templates.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Dataset`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #42: [COMPLETED] [ML-DATA] Create adversarial benchmark test set with human-edited slips (Photoshop/Canva)
* **Domain:** `Machine Learning` | **Layer:** `Dataset` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `domain:ml-data, milestone:phase-3, priority:high, layer:dataset, contributions-welcome`

### Overview
Manually tamper 50 genuine slips using real photo editing software to create a golden evaluation benchmark.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Dataset`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #43: [ML-DATA] Implement dataset integrity and checksum verification script
* **Domain:** `Machine Learning` | **Layer:** `Dataset` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:ml-data, milestone:phase-2, priority:low, layer:dataset, contributions-welcome`

### Overview
Verify SHA-256 hashes and image validity for all dataset samples to prevent corrupt training samples.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Dataset`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #44: [COMPLETED] [ML-DATA] Create dataset documentation and data card following ethical research standards
* **Domain:** `Machine Learning` | **Layer:** `Dataset` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Low`
* **Labels:** `domain:ml-data, milestone:phase-4, priority:low, layer:dataset, contributions-welcome`

### Overview
Document dataset provenance, redaction methodology, distribution statistics, and dual-use ethical safeguards.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Dataset`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #45: [COMPLETED] [ML-DATA] Design PyTorch dual-stream fusion model architecture (RGB + Forensic Maps)
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `domain:ml-data, milestone:phase-3, priority:high, layer:layer-4, contributions-welcome`

### Overview
Build a PyTorch model accepting 3-channel RGB image alongside 3-channel forensic tensor (ELA + Noise + DCT).

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #46: [ML-DATA] Implement EfficientNet-B0 backbone feature extractor for RGB stream
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-3, priority:medium, layer:layer-4, contributions-welcome`

### Overview
Use pretrained EfficientNet-B0 or ConvNeXt-Tiny to extract 512-dim visual representation from receipt patches.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #47: [COMPLETED] [ML-DATA] Implement CNN feature extractor for multi-channel forensic map stream
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-3, priority:medium, layer:layer-4, contributions-welcome`

### Overview
Build a lightweight 4-layer convolutional network extracting high-frequency tampering signatures from forensic maps.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #48: [COMPLETED] [ML-DATA] Implement cross-attention fusion layer combining visual and forensic features
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `domain:ml-data, milestone:phase-3, priority:high, layer:layer-4, contributions-welcome`

### Overview
Fuse RGB features with forensic features using cross-attention or gated feature fusion before classification head.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #49: [COMPLETED] [ML-DATA] Implement binary classification head with temperature calibration
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-3, priority:medium, layer:layer-4, contributions-welcome`

### Overview
Train classification head with Platt scaling / temperature scaling to output true calibrated tamper probabilities.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #50: [COMPLETED] [ML-DATA] Implement U-Net / FPN segmentation head for pixel-level tamper localization
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `domain:ml-data, milestone:phase-3, priority:high, layer:layer-4, contributions-welcome`

### Overview
Add segmentation decoder predicting binary tampering mask highlighting exact forged regions.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #51: [COMPLETED] [ML-DATA] Implement combined loss function: Focal Loss + Dice Loss for class imbalance
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-3, priority:medium, layer:layer-4, contributions-welcome`

### Overview
Handle sparse tampered pixels using combined Focal and Dice loss formulation.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #52: [COMPLETED] [ML-DATA] Build PyTorch training and validation pipeline with TensorBoard logging
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-3, priority:medium, layer:layer-4, contributions-welcome`

### Overview
Write training loop with learning rate scheduling, early stopping, and metric logging.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #53: [ML-DATA] Evaluate Layer 4 model performance across skill tiers (Novice, Intermediate, Expert)
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-4, priority:medium, layer:layer-4, contributions-welcome`

### Overview
Generate evaluation tables reporting Precision, Recall, F1, and ROC-AUC per difficulty tier.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #54: [COMPLETED] [ML-DATA] Conduct ablation study: Classical layers vs Deep Learning vs Fusion Ensemble
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `High`
* **Labels:** `domain:ml-data, milestone:phase-4, priority:high, layer:layer-4, contributions-welcome`

### Overview
Demonstrate that the ensemble outperforms any single classical or learned detector in isolation.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #55: [ML-DATA] Quantize PyTorch model to INT8 / ONNX format for rapid CPU inference
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-4, priority:medium, layer:layer-4, contributions-welcome`

### Overview
Export model to ONNX runtime with INT8 dynamic quantization for <100ms inference without GPU.

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #56: [COMPLETED] [ML-DATA] Package Layer 4 inference module into unified engine pipeline
* **Domain:** `Machine Learning` | **Layer:** `Layer 4` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Medium`
* **Labels:** `domain:ml-data, milestone:phase-4, priority:medium, layer:layer-4, contributions-welcome`

### Overview
Integrate trained model checkpoint into  and connect with .

### Domain & Subsystem
* **Technical Domain:** `Machine Learning & Dataset Engineering`
* **Detection Layer / Component:** `Layer 4`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.



---

### 🌐 Track 3: Backend Systems, Client APIs & Integrations (Issues #57 to #82)

#### #57: [BACKEND-API] Implement API Key authentication and multi-tier rate limiting
* **Domain:** `Backend & Full-Stack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-2, priority:medium, layer:backend-api, contributions-welcome`

### Overview
Add API key middleware with Redis or in-memory token bucket limiting free tier to 10 requests/day and pro tier to 100/min.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Backend API`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #58: [BACKEND-API] Implement asynchronous background task processing for heavy forensic scans
* **Domain:** `Backend & Full-Stack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-2, priority:medium, layer:backend-api, contributions-welcome`

### Overview
Use FastAPI background tasks or Celery/RQ for processing high-resolution slips without blocking event loop.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Backend API`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #59: [BACKEND-API] Add structured JSON logging with request tracing and correlation IDs
* **Domain:** `Backend & Full-Stack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:backend-api, milestone:phase-2, priority:low, layer:backend-api, contributions-welcome`

### Overview
Implement structured logging with correlation IDs for tracing verification requests across layers.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Backend API`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #60: [BACKEND-API] Implement merchant telemetry and fraud analytics aggregation endpoints
* **Domain:** `Backend & Full-Stack` | **Layer:** `Backend API` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:medium, layer:backend-api, contributions-welcome`

### Overview
Add  returning daily scan volume, fraud detection rate, and common tampered bank templates.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Backend API`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #61: [BACKEND-API] Implement webhook notification dispatcher for asynchronous order verification
* **Domain:** `Backend & Full-Stack` | **Layer:** `Backend API` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:medium, layer:backend-api, contributions-welcome`

### Overview
Enable merchants to register webhook URLs to receive verification callbacks when scans complete.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Backend API`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #62: [BACKEND-API] Add image sanitization and virus/bomb prevention middleware
* **Domain:** `Backend & Full-Stack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-2, priority:medium, layer:backend-api, contributions-welcome`

### Overview
Validate image file headers, maximum dimensions, decompression bomb thresholds, and strip malicious payloads.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Backend API`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #63: [COMPLETED] [BACKEND-API] Implement OpenAPI / Swagger documentation enhancements and interactive examples
* **Domain:** `Backend & Full-Stack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:backend-api, milestone:phase-2, priority:low, layer:backend-api, contributions-welcome`

### Overview
Provide rich example payloads and detailed field descriptions on  and .

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Backend API`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #64: [COMPLETED] [BACKEND-API] Implement CORS policies and production security headers
* **Domain:** `Backend & Full-Stack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:backend-api, milestone:phase-2, priority:low, layer:backend-api, contributions-welcome`

### Overview
Configure secure CORS origins, HSTS, X-Content-Type-Options, and Content-Security-Policy headers.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Backend API`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #65: [COMPLETED] [BACKEND-API] Add health check probe with detailed component readiness diagnostics
* **Domain:** `Backend & Full-Stack` | **Layer:** `Backend API` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `domain:backend-api, milestone:phase-1, priority:low, layer:backend-api, contributions-welcome`

### Overview
Enhance  endpoint to verify model weights loaded, memory status, and disk availability.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Backend API`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #66: [COMPLETED] [BACKEND-API] Implement Meta WhatsApp Cloud API webhook receiver and signature verification
* **Domain:** `Backend & Full-Stack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `High`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:high, layer:whatsapp-bot, contributions-welcome`

### Overview
Build production endpoint for Meta WhatsApp Business Cloud API with HMAC SHA-256 signature verification.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `WhatsApp Bot`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #67: [BACKEND-API] Implement WhatsApp media downloader and temporary image buffer
* **Domain:** `Backend & Full-Stack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:medium, layer:whatsapp-bot, contributions-welcome`

### Overview
Download customer media attachments from WhatsApp media endpoints securely into memory.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `WhatsApp Bot`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #68: [BACKEND-API] Implement WhatsApp conversational state machine and onboarding message flow
* **Domain:** `Backend & Full-Stack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:medium, layer:whatsapp-bot, contributions-welcome`

### Overview
Handle seller onboarding, balance check commands (balance), and help menus in English and Sinhala/Tamil.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `WhatsApp Bot`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #69: [COMPLETED] [BACKEND-API] Build automated WhatsApp image annotation returning red-boxed tamper slips
* **Domain:** `Backend & Full-Stack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:medium, layer:whatsapp-bot, contributions-welcome`

### Overview
When fraud is detected, draw red bounding boxes on the slip image and send it back to the seller via WhatsApp media message.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `WhatsApp Bot`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #70: [BACKEND-API] Implement merchant subscription credit balance tracker for WhatsApp bot
* **Domain:** `Backend & Full-Stack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:medium, layer:whatsapp-bot, contributions-welcome`

### Overview
Track checks used per phone number, notifying user when free quota is reached with payment upgrade link.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `WhatsApp Bot`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #71: [COMPLETED] [BACKEND-API] Add mock WhatsApp interactive test dashboard for local developer testing
* **Domain:** `Backend & Full-Stack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:backend-api, milestone:phase-2, priority:low, layer:whatsapp-bot, contributions-welcome`

### Overview
Refine Web Cockpit WhatsApp simulator tab to allow testing custom phone numbers and arbitrary image uploads.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `WhatsApp Bot`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #72: [BACKEND-API] Integrate Sri Lankan SMS fallback notification via Dialog/Mobitel SMS gateway
* **Domain:** `Backend & Full-Stack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Low`
* **Labels:** `domain:backend-api, milestone:phase-4, priority:low, layer:whatsapp-bot, contributions-welcome`

### Overview
Send SMS alert to seller if a high-risk fraud attempt occurs while seller is offline.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `WhatsApp Bot`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #73: [COMPLETED] [BACKEND-API] Implement interactive zoom and pan controls on inspection canvas
* **Domain:** `Backend & Full-Stack` | **Layer:** `Web Frontend` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:backend-api, milestone:phase-2, priority:low, layer:web-frontend, contributions-welcome`

### Overview
Allow users to zoom in up to 400% on highlighted tamper bounding boxes to inspect subpixel artifacts.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Web Frontend`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #74: [COMPLETED] [BACKEND-API] Add side-by-side split screen view comparing original slip and ELA heatmap
* **Domain:** `Backend & Full-Stack` | **Layer:** `Web Frontend` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-2, priority:medium, layer:web-frontend, contributions-welcome`

### Overview
Add slider handle to swipe between raw screenshot and forensic heatmap view.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Web Frontend`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #75: [BACKEND-API] Build merchant history drawer with past verification search and filter
* **Domain:** `Backend & Full-Stack` | **Layer:** `Web Frontend` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:medium, layer:web-frontend, contributions-welcome`

### Overview
Allow merchants to view previously checked slips with search by reference number or date.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Web Frontend`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #76: [COMPLETED] [BACKEND-API] Add light/dark theme toggle and mobile-responsive viewport tuning
* **Domain:** `Backend & Full-Stack` | **Layer:** `Web Frontend` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `domain:backend-api, milestone:phase-2, priority:low, layer:web-frontend, contributions-welcome`

### Overview
Optimize CSS for mobile browser viewing on seller smartphones.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Web Frontend`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #77: [BACKEND-API] Implement keyboard shortcuts for rapid merchant triage (Space: Accept, X: Flag)
* **Domain:** `Backend & Full-Stack` | **Layer:** `Web Frontend` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Low`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:low, layer:web-frontend, contributions-welcome`

### Overview
Power-seller shortcuts for high-speed review of multiple slips during peak sales.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Web Frontend`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #78: [BACKEND-API] Implement dedicated Courier Rider API endpoint 
* **Domain:** `Backend & Full-Stack` | **Layer:** `Courier B2B` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:medium, layer:courier-b2b, contributions-welcome`

### Overview
Streamlined response payload optimized for mobile courier apps with simple boolean .

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Courier B2B`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #79: [BACKEND-API] Build WooCommerce plugin boilerplate for direct bank transfer auto-verification
* **Domain:** `Backend & Full-Stack` | **Layer:** `E-Commerce` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `High`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:high, layer:e-commerce, contributions-welcome`

### Overview
Create WordPress/WooCommerce plugin that intercepts order checkout receipt uploads and queries VeriSlip API.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `E-Commerce`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #80: [BACKEND-API] Build Shopify Webhook app integration for manual payment screening
* **Domain:** `Backend & Full-Stack` | **Layer:** `E-Commerce` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `High`
* **Labels:** `domain:backend-api, milestone:phase-4, priority:high, layer:e-commerce, contributions-welcome`

### Overview
Develop Shopify app listening to order creation events and screening attached wire deposit proofs.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `E-Commerce`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #81: [COMPLETED] [BACKEND-API] Implement formal PDF Forensic Audit Report generator with cryptographic seal
* **Domain:** `Backend & Full-Stack` | **Layer:** `Audit Report` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:medium, layer:audit-report, contributions-welcome`

### Overview
Generate publication-grade PDF report with timestamp, SHA-256 hash, ELA diagrams, and legal evidence format.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Audit Report`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #82: [BACKEND-API] Implement payment gateway integration (PayHere / Stripe / Genie) for Pro subscriptions
* **Domain:** `Backend & Full-Stack` | **Layer:** `Monetization` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `High`
* **Labels:** `domain:backend-api, milestone:phase-3, priority:high, layer:monetization, contributions-welcome`

### Overview
Integrate local Sri Lankan payment gateways for charging LKR 1,490/mo Pro subscriptions and credit top-ups.

### Domain & Subsystem
* **Technical Domain:** `Backend Systems & Enterprise Integrations`
* **Detection Layer / Component:** `Monetization`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.



---

### ⚙️ Track 4: Cloud Infrastructure, Security & Applied Research (Issues #83 to #100)

#### #83: [COMPLETED] [INFRA-RESEARCH] Setup GitHub Actions CI pipeline running pytest and code coverage
* **Domain:** `Cloud & Security` | **Layer:** `DevOps` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `domain:infra-research, milestone:phase-1, priority:medium, layer:devops, contributions-welcome`

### Overview
Automate unit tests on every pull request with pytest, codecov, and linting checks.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `DevOps`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #84: [INFRA-RESEARCH] Setup Flake8, Black, and isort pre-commit hooks
* **Domain:** `Cloud & Security` | **Layer:** `DevOps` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `domain:infra-research, milestone:phase-1, priority:low, layer:devops, contributions-welcome`

### Overview
Maintain code style and automated formatting across all team contributions.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `DevOps`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #85: [INFRA-RESEARCH] Create multi-stage Dockerfile for FastAPI backend and frontend static assets
* **Domain:** `Cloud & Security` | **Layer:** `DevOps` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:infra-research, milestone:phase-2, priority:medium, layer:devops, contributions-welcome`

### Overview
Build lightweight production Docker container (<400MB) with non-root user.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `DevOps`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #86: [INFRA-RESEARCH] Create Docker Compose configuration with Redis and Nginx reverse proxy
* **Domain:** `Cloud & Security` | **Layer:** `DevOps` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:infra-research, milestone:phase-2, priority:medium, layer:devops, contributions-welcome`

### Overview
Provide single-command local development and production orchestration ().

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `DevOps`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #87: [INFRA-RESEARCH] Configure deployment pipeline to cloud host (Render / Railway / AWS EC2)
* **Domain:** `Cloud & Security` | **Layer:** `DevOps` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:infra-research, milestone:phase-3, priority:medium, layer:devops, contributions-welcome`

### Overview
Deploy staging environment for live team and merchant beta testing.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `DevOps`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #88: [INFRA-RESEARCH] Setup Prometheus metrics and Grafana dashboard for API latency monitoring
* **Domain:** `Cloud & Security` | **Layer:** `DevOps` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Low`
* **Labels:** `domain:infra-research, milestone:phase-4, priority:low, layer:devops, contributions-welcome`

### Overview
Monitor request latency, layer execution times, and memory utilization.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `DevOps`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #89: [INFRA-RESEARCH] Implement dual-use containment: lock down synthetic tampering generator
* **Domain:** `Cloud & Security` | **Layer:** `Security` | **Milestone:** `Phase 1: Foundations` | **Priority:** `High`
* **Labels:** `domain:infra-research, milestone:phase-1, priority:high, layer:security, contributions-welcome`

### Overview
Ensure synthetic tampering code is strictly internal, isolated from public API endpoints, and protected by environment flags.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `Security`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #90: [INFRA-RESEARCH] Implement automated PII scrubbing on all request logs and stored samples
* **Domain:** `Cloud & Security` | **Layer:** `Security` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `High`
* **Labels:** `domain:infra-research, milestone:phase-2, priority:high, layer:security, contributions-welcome`

### Overview
Hash bank account numbers and redact personal names before persisting any audit records.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `Security`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #91: [INFRA-RESEARCH] Implement rate-limiting and IP reputation against adversarial probing
* **Domain:** `Cloud & Security` | **Layer:** `Security` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `domain:infra-research, milestone:phase-3, priority:medium, layer:security, contributions-welcome`

### Overview
Prevent fraudsters from querying the API repeatedly to reverse-engineer evasion techniques.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `Security`
* **Target Milestone:** `Phase 3: Product & Integrations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #92: [INFRA-RESEARCH] Perform security review on file upload handling and path traversal vulnerabilities
* **Domain:** `Cloud & Security` | **Layer:** `Security` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:infra-research, milestone:phase-2, priority:medium, layer:security, contributions-welcome`

### Overview
Audit file uploads against SVG script injection, path traversal, and decompression attacks.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `Security`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #93: [INFRA-RESEARCH] Conduct literature review on financial document forgery vs natural image forensics
* **Domain:** `Cloud & Security` | **Layer:** `Research Paper` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `domain:infra-research, milestone:phase-1, priority:medium, layer:research-paper, contributions-welcome`

### Overview
Compile comprehensive bibliography and related work section covering ELA, copy-move, and document verification.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `Research Paper`
* **Target Milestone:** `Phase 1: Foundations`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #94: [INFRA-RESEARCH] Draft Research Paper: Problem Formulation & Threat Model section
* **Domain:** `Cloud & Security` | **Layer:** `Research Paper` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `domain:infra-research, milestone:phase-2, priority:medium, layer:research-paper, contributions-welcome`

### Overview
Formulate mathematical threat model characterizing the Sri Lankan P2P payment fraud ecosystem.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `Research Paper`
* **Target Milestone:** `Phase 2: Core Forensics`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #95: [INFRA-RESEARCH] Draft Research Paper: Multi-Layer Architecture & Methodology section
* **Domain:** `Cloud & Security` | **Layer:** `Research Paper` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `domain:infra-research, milestone:phase-3, priority:high, layer:research-paper, contributions-welcome`

### Overview
Document mathematical formulations for Layer 1, Layer 2 (ELA/DCT), Layer 3 (Noise), and Layer 4 (Ensemble).

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `Research Paper`
* **Target Milestone:** `Phase 3: ML & Advanced Forensics`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #96: [COMPLETED] [INFRA-RESEARCH] Generate experimental results tables, ROC curves, and confusion matrices
* **Domain:** `Cloud & Security` | **Layer:** `Research Paper` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `High`
* **Labels:** `domain:infra-research, milestone:phase-4, priority:high, layer:research-paper, contributions-welcome`

### Overview
Produce publication figures comparing single layers against the ensemble across skill tiers.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `Research Paper`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #97: [INFRA-RESEARCH] Finalize conference submission draft for IEEE MERCon / ICTer
* **Domain:** `Cloud & Security` | **Layer:** `Research Paper` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `High`
* **Labels:** `domain:infra-research, milestone:phase-4, priority:high, layer:research-paper, contributions-welcome`

### Overview
Format paper into IEEE two-column template, polish figures, and complete peer-review readiness check.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `Research Paper`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `High`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #98: [INFRA-RESEARCH] Run 2-week closed beta pilot with 10 Sri Lankan social media sellers
* **Domain:** `Cloud & Security` | **Layer:** `GTM & Pilot` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Medium`
* **Labels:** `domain:infra-research, milestone:phase-4, priority:medium, layer:gtm-&-pilot, contributions-welcome`

### Overview
Distribute WhatsApp bot to friendly Instagram/FB Marketplace sellers; collect user feedback and false positive logs.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `GTM & Pilot`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #99: [INFRA-RESEARCH] Draft B2B proposal and pilot deck for Sri Lankan courier logistics operators
* **Domain:** `Cloud & Security` | **Layer:** `GTM & Pilot` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Low`
* **Labels:** `domain:infra-research, milestone:phase-4, priority:low, layer:gtm-&-pilot, contributions-welcome`

### Overview
Create presentation deck highlighting COD rider fraud prevention ROI for Domex, PromptX, and Koombiyo.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `GTM & Pilot`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `Low`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.


#### #100: [INFRA-RESEARCH] Formulate technical roadmap for Layer 5: LankaPay / CEFTS API Direct Verification Gateway
* **Domain:** `Cloud & Security` | **Layer:** `GTM & Pilot` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Medium`
* **Labels:** `domain:infra-research, milestone:phase-4, priority:medium, layer:gtm-&-pilot, contributions-welcome`

### Overview
Document architectural transition from image forensics to an authorized programmatic transaction verification gateway with local banks.

### Domain & Subsystem
* **Technical Domain:** `DevOps, Security & Academic Research`
* **Detection Layer / Component:** `GTM & Pilot`
* **Target Milestone:** `Phase 4: Research & GTM`
* **Difficulty / Priority:** `Medium`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.

