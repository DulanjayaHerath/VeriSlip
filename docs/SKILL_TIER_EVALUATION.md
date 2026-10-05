# Layer 4 skill-tier evaluation

This evaluator consumes predictions that were produced elsewhere. It does not
train, modify, load, or benchmark a neural-network architecture by itself.
VeriSlip currently includes no validated real Layer 4 prediction file, so this
change publishes no performance result. Automated tests use synthetic fixtures
only.

## Input

Provide a CSV with exactly these columns:

```csv
sample_id,skill_tier,label,score
```

`sample_id` must be unique. `skill_tier` accepts Novice, Intermediate, or
Expert. `label` is 0 or 1, and `score` is a finite probability from 0 to 1.
Tier labels must come from the benchmark protocol, not from model confidence.
Before interpreting results, verify dataset integrity, provenance, permission,
label quality, split isolation, and that every score came from the same frozen
Layer 4 checkpoint and preprocessing configuration.

## Output and interpretation

The command writes deterministic JSON, CSV, and Markdown tables. Each tier
contains sample/class counts, confusion counts, precision, recall, F1, and
ROC-AUC. The classification threshold defaults to 0.5 and appears in JSON.
ROC-AUC uses continuous scores with half credit for ties. If a tier contains
only one class, ROC-AUC is `null` in JSON, blank in CSV, and clearly marked
`N/A (single class)` in Markdown; the tool never substitutes a misleading zero.

Small tier counts produce unstable estimates. This tool does not calculate
confidence intervals, calibrate thresholds, establish statistical significance,
or prove generalization to real receipts.

## Windows CMD

```cmd
python scripts\evaluate_skill_tiers.py C:\benchmarks\layer4_predictions.csv C:\benchmarks\tier_report --threshold 0.5
type C:\benchmarks\tier_report\skill_tier_metrics.md
python -m pytest tests\test_skill_tier_evaluation.py -v
```
