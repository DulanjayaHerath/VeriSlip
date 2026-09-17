# VeriSlip Layer 4 Model Weights Directory

This directory houses the trained PyTorch checkpoint weights for the **Layer 4 Dual-Stream Forensic Attention Network**.

## Recommended Model Artifact
- **File**: `verislip_dualstream_best.pt`
- **Architecture**: `DualStreamForensicNetwork` (Stream A: RGB Visual Patches, Stream B: ELA + Noise + Gradient Forensic Tensor)
- **Loss Function**: Combined Binary Cross-Entropy (Tamper Classification) + Dice Loss (Tamper Localization Mask)

## How to Obtain Model Weights from Kaggle:
1. Generate the synthetic training dataset locally without manual labeling:
   ```bash
   python3 scripts/generate_kaggle_dataset.py --samples 2000
   ```
   This generates `verislip_kaggle_dataset.zip` containing 4,000 paired authentic & tampered Sri Lankan banking slips with pixel-perfect binary ground-truth masks.

2. Upload `verislip_kaggle_dataset.zip` to [Kaggle Datasets](https://www.kaggle.com/datasets).

3. Import [`notebooks/VeriSlip_DualStream_Training.ipynb`](../notebooks/VeriSlip_DualStream_Training.ipynb) into Kaggle Notebooks, attach your dataset, select **GPU P100 / T4 x2**, and run all cells.

4. Once training completes (approx. 10–15 mins for 15 epochs), download the checkpoint `verislip_dualstream_best.pt`.

5. Place `verislip_dualstream_best.pt` in this `weights/` directory:
   ```bash
   mv ~/Downloads/verislip_dualstream_best.pt weights/
   ```

When VeriSlip starts up, `Layer4DeepEnsemble` will automatically detect and load `weights/verislip_dualstream_best.pt`. If absent, it gracefully falls back to the calibrated mathematical prior.
