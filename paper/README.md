# VeriSlip conference-paper draft

This directory contains an anonymous IEEE conference-format research draft for
issue #97. It intentionally omits empirical numbers because the repository's
default academic benchmark table and curves are deterministic demonstration
data, not measurements from a controlled study.

## Build on Windows CMD

Install a TeX distribution that provides `IEEEtran`, `latexmk`, BibTeX, and the
packages used in `main.tex`, then run:

```cmd
cd /d D:\Project\VeriSlip\paper
latexmk -pdf main.tex
```

Clean generated files with:

```cmd
latexmk -c
```

## Venue status

The draft follows the standard IEEE conference class. The official MERCon 2026
author page required English, the IEEE conference template, double-blind initial
submission, and no more than six A4 pages including references. It also excluded
review-only and project-report submissions. Those rules are recorded in
`SUBMISSION_CHECKLIST.md` with source URLs and an access date.

MERCon 2026 deadlines have passed. Before targeting a future MERCon or ICTer
edition, re-check that edition's official call, dates, page limit, anonymity,
copyright, and PDF-validation rules. Do not infer one venue's rules from another.

## Integration points

The independent issue branches for #93 (related work), #94 (threat model), and
#95 (methodology) are not copied into this branch. After review/merge, authors
should reconcile their verified detail into this compact manuscript and keep it
within the selected venue's page limit.

Before submission, replace every `Pending controlled evaluation` entry only with
results generated from a versioned manifest, locked configuration, and retained
evaluation artifacts. Never use `benchmarks.DEFAULT_MODEL_RESULTS`, generated
demo curves, or dashboard synthetic profiles as paper evidence.

