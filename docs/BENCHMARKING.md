# Benchmarking and dashboard workflow

The VeriSlip benchmarking dashboard gives an at-a-glance view of model quality across the forensic detection stack. It highlights ROC-AUC, F1 score, latency per slip, threshold sensitivity, and edge-case examples for false positives and false negatives.

## Prerequisites

```bash
python -m pip install -r requirements.txt
```

## Launch the dashboard

```bash
streamlit run scripts/benchmark_dashboard.py --server.port 8501
```

If you want to evaluate against a local benchmark snapshot, pass the data directory explicitly:

```bash
VERISLIP_DATASET_DIR=/path/to/benchmark-data streamlit run scripts/benchmark_dashboard.py
```

The dashboard accepts a `benchmark_manifest.json` file in the dataset directory and falls back to a deterministic synthetic profile when no manifest is present.

## Headless CI mode

For inspection in scripts, CI jobs, or local validation, the dashboard can emit a JSON snapshot instead of opening the Streamlit UI:

```bash
python scripts/benchmark_dashboard.py --headless --threshold 0.5
```

This output includes per-layer metrics, summary statistics, and an alert flag for benchmark regression scenarios.

## Typical benchmark checks

- Review the average ROC-AUC and F1 for the whole stack.
- Inspect the latency trend across the five detection layers.
- Tune the threshold slider to identify the operating point that balances precision and recall.
- Review false-positive / false-negative examples before shipping a model change.
