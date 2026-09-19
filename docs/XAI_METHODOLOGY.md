# XAI Methodology for Layer 4 Attribution

This document explains the legal-grade interpretability layer used to accompany the Layer 4 forensic ensemble.

## Grad-CAM

Grad-CAM attributes a model decision to the final convolutional feature map in the forensic encoder by weighting each channel with its average gradient with respect to the target logit.

For a feature map `A^k` and target score `y^c`, the channel-wise importance is:

`alpha_k^c = (1/Z) sum_i sum_j (dy^c / dA_ij^k)`

The localization heatmap is then:

`L_GradCAM^c = ReLU(sum_k alpha_k^c A^k)`

The implementation in `core/forensics/xai_gradcam.py` smooths and normalizes the heatmap before rendering an overlay and a counterfactual reconstruction.

## Counterfactual Reconstruction

The system creates a synthetic pristine reconstruction by applying a Gaussian blur to the highest-salience region and preserving the original pixels elsewhere. This approximates the authentic appearance that would remain if the tampered pixels were restored.

## Interpretation Guidance

- Use the heatmap to confirm the model is focusing on the suspicious area rather than unrelated document margins.
- Treat the counterfactual as supportive evidence, not a replacement for human review.
- For audit use, preserve the original and attributed images together with the bounding box and risk score.

## Export Format

The engine exports attribution artifacts as PNG overlays and base64 data URIs for API clients and web dashboards.
