# Academic benchmark suite

The academic evaluation harness compares VeriSlip against the primary forensic baselines used in the project literature: MantraNet, BusterNet, TruFor, and CAT-Net.

## Running the benchmark

```bash
python benchmarks/run_academic_eval.py --output-dir benchmarks/output
```

This produces:

- `benchmarks/output/academic_summary.csv`
- `benchmarks/output/academic_table.tex`
- `benchmarks/output/roc_curve.svg`
- `benchmarks/output/pr_curve.svg`

## Metrics reported

- Pixel-level F1-score
- AUC
- mIoU
- TPR at fixed FPR = 0.01
- Average precision
- EER

## Reproducibility notes

1. Use the same bank slip dataset snapshot for every run.
2. Keep the evaluation threshold and preprocessing pipeline constant across all models.
3. Store the generated CSV and LaTeX table alongside the manuscript source to keep the paper and the benchmark outputs synchronized.
4. Version the benchmark config file or script commit so any paper figure can be regenerated deterministically.
