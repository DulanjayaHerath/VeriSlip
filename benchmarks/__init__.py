"""Academic benchmark tooling for VeriSlip model comparison."""

from .run_academic_eval import (
    DEFAULT_MODEL_RESULTS,
    calculate_binary_metrics,
    generate_latex_table,
    run_academic_evaluation,
)

__all__ = [
    "DEFAULT_MODEL_RESULTS",
    "calculate_binary_metrics",
    "generate_latex_table",
    "run_academic_evaluation",
]
