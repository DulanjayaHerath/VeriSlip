# Sub-pixel glyph rasterization analysis

VeriSlip's Layer 1 font checks compare the rendering profile of each connected
glyph with the receipt's own dominant profile. This is a classical computer
vision signal; it does not add or change a neural model.

## Signals

For each plausible glyph, the analyzer measures the 90/10 luminance transition
band around detected edges. Its normalized width approximates the point spread
function (PSF): hard rasterization has a narrow transition, while gamma-correct
anti-aliasing produces a wider band. It also measures RGB sub-pixel color fringe
as `abs(R - B) / (G + 1)` along the same boundary.

The document median and median absolute deviation form a robust reference.
A glyph is flagged only when its profile exceeds three robust standard
deviations and a minimum absolute transition (`0.35 px`) or fringe (`0.035`)
difference. Requiring both statistical and absolute divergence avoids unstable
scores on nearly monochrome text.

## Output and integration

`FontAntiAliasingAnalyzer.analyze()` returns aggregate medians, counts, anomaly
score, and localized evidence with PSF/fringe values and z-scores. The existing
`CharacterAlignmentValidator` exposes this under `subpixel_rasterization`.
The signal is intentionally not fused into the legacy production verdict until
permission-cleared samples from CoreText, FreeType, DirectWrite, Canvas, camera
capture, and messaging recompression have been calibrated.

## Validation and limitations

Unit fixtures compare uniform anti-aliased receipt numerals with pasted hard-edge
colored glyphs and enforce at least 88% precision on that deterministic set.
This is not a claim of 88% field precision. Resolution, resampling, camera blur,
JPEG chroma subsampling, display capture, and naturally mixed fonts can erase or
imitate the signal. Treat it as explainable corroborating evidence and calibrate
thresholds against the deployment's banks and capture devices.
