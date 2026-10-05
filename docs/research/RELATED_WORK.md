# Related work: financial-document image forensics

## Scope and review method

This review separates evidence about **natural photographs** from evidence about
**structured financial documents**. Sources were selected from peer-reviewed
journals and major computer-vision proceedings, and bibliographic metadata was
checked against publisher or proceedings records. The accompanying
[`references.bib`](references.bib) is the canonical bibliography. This is a
technical review, not evidence that VeriSlip has reproduced any cited result.

Bank-transfer slips and receipts differ from natural photographs in ways that
matter to forensic design: they contain repeated glyphs, large nearly uniform
backgrounds, rigid layout, and semantically constrained fields. A small edit to
an amount, account number, date, or reference can change the document's meaning
without creating the broad scene inconsistencies assumed by much photographic
forensics. Conversely, benign screenshotting, messaging-app recompression,
scanning, and print--capture cycles can create strong pixel-level traces.

## Natural-image forensic foundations

Broad surveys organize passive image forensics around acquisition traces,
pixel correlations, geometric inconsistencies, and compression artifacts
[@farid2009survey; @verdoliva2020media]. These families remain useful for
documents, but their assumptions must be revisited.

### JPEG, DCT, and recompression evidence

JPEG quantization operates on 8-by-8 DCT blocks. Local differences in block
alignment or quantization history can therefore provide evidence of pasted or
re-saved regions. Bianchi and Piva localize differing JPEG histories through a
block-grained analysis [@bianchi2012jpeg], while Ferrara et al. examine local
inconsistencies in color-filter-array artifacts [@ferrara2012cfa]. These are
valuable provenance cues, not direct proof of malicious editing: routine export,
cropping, messaging, or screenshot capture may weaken or reproduce similar
signals.

Error-level analysis (ELA) is a visualization obtained by recompressing an image
at a chosen JPEG quality and amplifying the pixel difference. It is widely used
as an exploratory heuristic, but it is not a calibrated detector and has no
single canonical decision rule. VeriSlip should therefore treat ELA as one
feature alongside explicit JPEG/DCT analysis, never as a standalone authenticity
test. The formal JPEG-localization literature is the defensible basis for that
interpretation [@bianchi2012jpeg], rather than claims based on visual brightness
alone.

### Copy--move and splicing

Copy--move edits duplicate content within one image. Keypoint matching can be
robust to scale and rotation; Amerini et al. use SIFT matches and geometric
verification [@amerini2011sift]. Dense block methods complement keypoints in
low-texture areas. Modern learned systems such as BusterNet jointly identify
source and target regions [@wu2018busternet]. Splicing instead imports material
from another source. Learned self-consistency can expose source-model
inconsistencies [@huh2018selfconsistency], and rich-feature approaches learn
manipulation traces rather than semantic object categories [@zhou2018rich].

For receipts, repeated digits, logos, separators, and table rows create many
legitimate self-similar regions. Copy--move evidence therefore needs minimum
displacement, spatial clustering, and semantic context to avoid treating repeated
typography as cloning.

### Sensor and noise evidence

Photo-response non-uniformity (PRNU) can identify a camera when a stable
reference fingerprint is available [@lukas2006prnu]. CFA and local-noise
inconsistency can also reveal compositing [@ferrara2012cfa]. These assumptions
are fragile for screenshots and heavily compressed receipts, which may contain
no usable camera pipeline trace. VeriSlip does **not** currently claim PRNU
camera attribution; it uses local residual/noise consistency as a weaker anomaly
cue. Learned camera-model fingerprints such as Noiseprint demonstrate a related
direction but require trained models and suitable data [@cozzolino2020noiseprint].

## Document-specific evidence

Document tampering is unusually local and semantic. DocTamper directly targets
tampered text in document images and emphasizes compression-robust localization
[@qu2023doctamper]. Its task formulation is closer to slips than generic scene
splicing, although its learned dataset and operating domain cannot be assumed to
transfer to Sri Lankan bank templates.

OCR makes the visible text machine-readable, allowing checks that pixel-only
methods cannot express: currency syntax, required fields, arithmetic, temporal
ordering, and bank/reference conventions. OCR is nevertheless an observation,
not ground truth. Recognition errors, Sinhala/Tamil scripts, low resolution, and
stylized fonts can cause false alarms. Layout-aware document models such as
LayoutLM show the value of combining text and spatial position
[@xu2020layoutlm], but they are document-understanding systems rather than
forgery detectors.

Typography supplies further document-specific signals: inconsistent baselines,
kerning, glyph dimensions, antialiasing, or subpixel color fringes may identify
pasted text. Such rules are interpretable and useful when a template is stable,
but font substitution, accessibility settings, renderer differences, and
rescaling are legitimate confounders. These cues should support, not replace,
semantic and image-forensic evidence.

## Recapture and anti-forensics

Screen recapture and print--scan transformations can obscure compression and
sensor traces while adding moiré, resampling, blur, illumination gradients, or
printer/scanner artifacts. An attacker may also resize, blur, denoise, or
recompress an edit specifically to suppress forensic residuals. Constrained
convolutional filters and learned residual features were proposed to reduce
dependence on image content [@bayar2016constrained], but learned detectors can
still be domain-sensitive. Consequently, VeriSlip should report recapture as an
acquisition condition and reduce confidence in unavailable cues rather than
equating recapture with fraud.

## Relationship to the current VeriSlip implementation

| Evidence family | Current repository mechanism | Literature connection | Important caveat |
|---|---|---|---|
| Structural/semantic | metadata, bank layout/color, OCR field and reference checks | document layout and text-position reasoning [@xu2020layoutlm] | OCR/template coverage is incomplete |
| Recompression | ELA visualization, luminance/chrominance residuals, DCT periodicity, JPEG-grid checks | JPEG localization [@bianchi2012jpeg] | recompression is common and benign |
| Copy--move | ORB/keypoint matching and dense block-DCT matching | keypoint and source/target localization [@amerini2011sift; @wu2018busternet] | repeated glyphs create legitimate matches |
| Local noise | patch residual/noise-consistency analysis | sensor/noise forensics [@lukas2006prnu; @cozzolino2020noiseprint] | this is not PRNU camera attribution |
| Typography | baseline, kerning, glyph rasterization, antialiasing checks | document-tamper focus [@qu2023doctamper] | renderer and scaling changes can confound |
| Recapture | frequency-domain screen/moiré analysis | acquisition-trace perspective [@verdoliva2020media] | absence of moiré does not prove originality |
| Learned ensemble | optional RGB/forensic-stream model with heuristic fallback | residual and rich-feature learning [@bayar2016constrained; @zhou2018rich] | no benchmark claim follows from architecture alone |

## Research gaps and evaluation implications

1. **Domain evidence.** Public natural-image benchmarks do not represent mobile
   banking slips, multilingual text, or local bank templates. Evaluation needs a
   consented, privacy-preserving, versioned corpus with device, compression, and
   recapture variation.
2. **Benign transformation controls.** Each attack test should be paired with
   genuine screenshots, messaging-app recompression, resizing, print--scan, and
   camera recapture controls.
3. **Region and document metrics.** Document-level ROC/PR metrics alone conceal
   localization errors. Region IoU or pixel metrics and field-level outcomes
   should be reported with confidence intervals.
4. **Ablation.** ELA, DCT, copy--move, noise, typography, OCR semantics, and any
   learned component require separate ablations. Repository demo values must not
   be reported as empirical performance.
5. **Calibration and abstention.** Scores should be calibrated on held-out banks
   and acquisition channels, with an explicit inconclusive/manual-review state.
6. **Generalization.** Bank-template, language, device, and time-based splits are
   needed to detect leakage and template memorization.

## Conclusions

The literature supports a multi-evidence design, but not a claim that any one
artifact establishes fraud. Natural-image methods contribute compression,
copy--move, and acquisition traces; document analysis contributes layout, OCR,
typography, and semantic constraints. A defensible VeriSlip evaluation must
measure their complementarity under realistic benign transformations and must
state clearly when a cue is absent, confounded, or not implemented.

