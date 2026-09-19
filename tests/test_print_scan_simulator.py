import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from core.internal.print_scan_simulator import PrintScanSimulator


def test_print_scan_simulator_changes_image_statistics():
    base = np.full((140, 180, 3), 230, dtype=np.uint8)
    base[35:95, 45:135] = 20
    base[70:110, 90:120] = 255

    simulated = PrintScanSimulator(seed=7).simulate(Image.fromarray(base))
    simulated_arr = np.asarray(simulated)
    delta = simulated_arr.astype(np.float32) - base.astype(np.float32)

    assert simulated_arr.shape == base.shape
    assert simulated_arr.dtype == np.uint8
    assert np.std(delta) > 5.0


def test_generate_kaggle_dataset_supports_print_scan_flag(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = tmp_path / "print_scan_dataset"
    env = os.environ.copy()
    env["VERISLIP_ENABLE_SYNTHETIC_GENERATOR"] = "1"

    subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "generate_kaggle_dataset.py"),
            "--samples",
            "4",
            "--output-dir",
            str(output_dir),
            "--no-zip",
            "--simulate-print-scan",
        ],
        cwd=str(repo_root),
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )

    images = sorted((output_dir / "train" / "images").glob("*.png"))
    assert len(images) >= 2
    sample = Image.open(images[0])
    assert sample.size == (420, 740)
