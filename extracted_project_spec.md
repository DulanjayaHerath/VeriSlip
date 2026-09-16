Project Title

VeriSlip (working name) — Forensic Detection of Tampered Payment Slips and Invoices for Peer-to-Peer Commerce

One-Line Pitch

An AI system that detects digitally edited bank transfer slips, receipts, and invoices — the specific fraud pattern hitting Sri Lankan online sellers who accept "proof of payment" screenshots before releasing goods.

Problem Statement

Small sellers on Facebook Marketplace, Instagram, WhatsApp Business, and COD delivery in Sri Lanka routinely accept a screenshot of a bank transfer slip as proof of payment before shipping. Fraudsters edit the amount, reference number, or account details on a real or template slip and send the doctored image. Sellers — especially non-technical, small-scale ones — have no reliable way to verify these screenshots, and by the time the fraud is discovered, goods are already gone. This is a high-frequency, low-average-value fraud (individually too small for police to prioritize, collectively large), and there is currently no accessible tool for the ordinary seller.

Why This Is a Genuine Research Gap

Forgery-detection literature is heavily concentrated on face deepfakes and generic natural-photo tampering (splicing, copy-move on photographs). Structured financial-document screenshots — with fixed layouts, rendered text, app-specific compression artifacts — are a distinct forensic domain that's barely covered.

No public dataset of tampered bank-slip/receipt images exists (understandably — this data doesn't get shared). Building one, responsibly, is itself a contribution.

Most receipt/invoice ML research (e.g. OCR-based expense processing) assumes the document is genuine and focuses on extraction, not authenticity verification.

South/Southeast Asian markets (Sri Lanka, Bangladesh, Pakistan, Philippines, Nigeria) share this exact fraud pattern via informal digital commerce — the research and the product both generalize well beyond Sri Lanka.

Research Objectives (for the paper)

Characterize the specific tampering signatures present in edited bank-slip screenshots (font/rendering mismatches, recompression artifacts, copy-move regions, noise-pattern breaks) — an empirical forensic study.

Build and release (or responsibly describe) a benchmark dataset of authentic vs. synthetically tampered payment slips across multiple Sri Lankan bank templates.

Design and evaluate a multi-signal ensemble detector that combines classical forensic features with a learned model, and show it outperforms any single classical technique.

Test robustness against "skilled" tampering — edits that specifically try to defeat the easy checks (matched fonts, cleaned compression, added noise) — since a real adversary adapts.

Report false-positive/false-negative trade-offs framed around real deployment cost (a false "fraud" flag on a real payment vs. a missed fraud), not just raw accuracy.

Detection Architecture (5 layers — build incrementally, each is a milestone)

Layer 1 — Structural/metadata validation

Reference number format/checksum validation per bank.

Template matching: logo position, font, spacing, layout grid against known genuine templates per bank.

EXIF/file-metadata sanity checks (though easily stripped — treat as a weak signal only).

Layer 2 — Classical image forensics

Error Level Analysis (ELA) — edited regions compress differently than untouched ones.

Copy-move detection via keypoint/block matching (SIFT/ORB-based or block-DCT correlation).

Double-JPEG compression / DCT coefficient analysis — screenshot → edit → re-export → send leaves a signature.

Font sub-pixel rendering consistency check on numeric fields.

Layer 3 — Sensor/noise-level forensics

Local noise-residual consistency (PRNU-style analysis, adapted for screenshots rather than camera photos).

Layer 4 — Learned ensemble detector

A model (CNN or ViT-based) trained to take the outputs/feature maps of Layers 1–3 plus raw image patches, and produce a calibrated tamper-probability score with localization (which region looks edited).

This is the core ML contribution — an editor might beat one classical check but rarely all simultaneously; the ensemble is what catches skilled edits.

Layer 5 — Verification-first alternative (the real gold standard, positioned as future work / enterprise tier)

Direct integration with LankaPay/CEFTS or bank merchant APIs so a seller gets a programmatic payment confirmation instead of relying on an image at all. Out of scope for MVP (requires bank partnerships) but should be named explicitly in the report as the long-term roadmap and as your competitive moat once you have traction to negotiate access.

Dataset Plan (do this carefully — see risks below)

Collect a set of genuine, permission-cleared slip/receipt screenshots (your own transactions, friends/family who consent, anonymized/redacted of personal identifying info beyond what's needed).

Generate the tampered set synthetically yourselves — edit amounts/references/names on your own genuine slips using common tools (Photoshop, GIMP, Canva, phone editing apps) to simulate real fraud techniques, at varying skill levels (obvious edits, careful edits, expert edits with cleaned artifacts).

Label each sample with: authentic/tampered, tampering type, tampering region (bounding box), and editing tool/skill tier.

Keep the dataset internal or release only a redacted/synthetic-bank-template version if you publish it — never real customer transaction data, never real account numbers/names.

Split by bank template and by tampering-skill tier for evaluation, so you can report performance separately on "easy" vs. "hard" (skilled) fakes.

Startup / Product Plan

Target users: individual online sellers (Facebook/Instagram Marketplace, WhatsApp Business), small COD delivery operators, small e-commerce sites without payment-gateway integration.

MVP: a web app or browser/WhatsApp-bot widget where a seller uploads the slip screenshot and gets an instant tamper-risk score + flagged regions.

Business model: freemium (limited free checks/month) → subscription for high-volume sellers, or pay-per-check for occasional users; later, a B2B API tier for delivery companies and small e-commerce platforms to embed directly at checkout.

Competitive landscape: no direct competitor doing this for South Asian bank-slip fraud specifically; adjacent players are generic document-fraud detection (enterprise-priced, not aimed at small sellers) and the banks' own (nonexistent, for this use case) verification tools.

Go-to-market: Facebook Marketplace seller groups, WhatsApp Business seller communities, partnerships with courier/delivery apps that already sit between buyer and seller.

Roadmap to Layer 5: once you have usage data and traction, that's your leverage to approach banks/LankaPay for real API integration — the actual defensible long-term moat.

Tech Stack Suggestions

Modeling: Python, PyTorch/TensorFlow (you already know both), OpenCV for classical forensics (ELA, copy-move, DCT analysis), a CNN/ViT backbone (e.g. EfficientNet or a small ViT) for the ensemble classifier.

Data/labeling: Label Studio or a simple custom annotation tool for bounding-box tamper regions.

Backend/API: FastAPI or Flask for the detection service.

Frontend/MVP: a simple React or Next.js upload-and-score interface; a WhatsApp Business API bot is a strong alternative given your users' habits.

Infra: start on free/cheap tiers (Render, Railway, or a university GPU if available) — no need for heavy infra at MVP stage.

Suggested Team Roles (6 people)

Classical forensics lead — ELA, copy-move, DCT/compression analysis (Layers 1–3).

ML/ensemble lead — the learned detector, training pipeline, evaluation (Layer 4).

Data lead — dataset collection, synthetic tampering generation, labeling, splits.

Backend/infra lead — API, model serving, data pipeline.

Frontend/product lead — MVP interface, seller-facing UX, eventually the business side.

Research/writing lead — literature review, experiment tracking, paper drafting, evaluation protocol design (can rotate with whoever is strongest at technical writing).All six should contribute to both the paper and the product — the split above is about primary ownership, not silos.

Timeline / Milestones (dual track)

Weeks 1–2: Literature review + finalize detection architecture; start collecting genuine slip samples.

Weeks 3–5: Build synthetic tampering pipeline; produce v1 labeled dataset; implement Layer 1–2 classical checks.

Weeks 6–8: Implement Layer 3; start training Layer 4 ensemble model; first evaluation results.

Weeks 9–10: Robustness testing against skilled/adaptive tampering; ablations (which layer contributes what).

Weeks 11–12: MVP frontend/API wired to the model; internal seller-friend beta test.

Weeks 13–14: Paper writing, results tables, figures; MERCon/other conference deadline check.

Ongoing after: seller outreach, iterate MVP, begin exploring LankaPay/bank conversations.

Risks & Ethical/Legal Considerations (important — don't skip this in the report)

Dual-use concern: a "fake slip generator" module must never be exposed as a public feature or shared as a standalone tool — keep tampering-generation strictly internal to dataset creation for training/evaluation, never distributed.

Bank trademark/branding: using real bank logos/templates in a published dataset or public demo could raise trademark issues — consider blurring/genericizing branding in anything public-facing, and keep real-branded samples internal only.

Personal data: redact real names, account numbers, and phone numbers from any sample used beyond your own internal testing; get explicit consent from anyone whose real slip you use.

False positives matter a lot: flagging a genuine buyer's real payment as "fraud" damages trust and transactions — the report should treat false-positive rate as a first-class metric, not an afterthought.

Regulatory: once this becomes a real product touching payment verification, expect to eventually need conversations with banks/CBSL about compliance — flag this as future-work, not a blocker for the MVP.

Adversarial adaptation: publishing your detection method in detail could help fraudsters adapt — standard responsible-disclosure practice in security research applies here (describe the approach, avoid publishing a literal step-by-step evasion-proofing gap analysis).

Success Metrics

Research: precision/recall/F1 on tampered vs. authentic, broken down by tampering-skill tier; localization accuracy (IoU on flagged regions); ablation showing ensemble beats any single layer.

Startup: number of active sellers, checks run per week, false-positive complaint rate, conversion from free to paid tier.