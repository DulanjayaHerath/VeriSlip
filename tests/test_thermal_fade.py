"""Tests for thermal POS-paper fading versus digital splice detection."""

import cv2
import numpy as np
import pytest
from PIL import Image, ImageDraw

from core.forensics.layer2_classical import Layer2ClassicalForensics
from core.forensics.thermal_fade import ThermalFadeConfig, ThermalFadeDiscriminator


def _pos_receipt() -> Image.Image:
    image = Image.new("L", (480, 640), 232)
    draw = ImageDraw.Draw(image)
    for y, text in enumerate(
        ("CITY MARKET", "TOTAL LKR 4,250.00", "REF 982174", "THANK YOU"), start=1
    ):
        draw.text((55, y * 105), text, fill=45)
    return image.convert("RGB")


def _naturally_faded_receipt() -> Image.Image:
    source = np.asarray(_pos_receipt(), dtype=np.float32)
    x = np.linspace(0.0, 1.0, source.shape[1], dtype=np.float32)
    smooth_fade = 0.08 + 0.58 * (3 * x**2 - 2 * x**3)
    faded = source + (255.0 - source) * smooth_fade[None, :, None]
    faded = cv2.GaussianBlur(faded, (0, 0), sigmaX=1.2)
    return Image.fromarray(np.clip(faded, 0, 255).astype(np.uint8), "RGB")


def _digitally_erased_receipt() -> Image.Image:
    image = _naturally_faded_receipt()
    draw = ImageDraw.Draw(image)
    draw.rectangle((42, 185, 420, 292), fill=(248, 248, 248))
    draw.text((70, 220), "TOTAL LKR 9,950.00", fill=(25, 25, 25))
    return image


def test_continuous_thermal_fade_is_not_reported_as_digital_splice():
    result = ThermalFadeDiscriminator().analyze(_naturally_faded_receipt())

    assert result["classification"] == "continuous_thermal_fade"
    assert result["is_digital_splice"] is False
    assert result["fade_continuity_score"] > result["transition_border_score"]


def test_digital_erase_has_sharper_fft_and_transition_evidence():
    detector = ThermalFadeDiscriminator()
    faded = detector.analyze(_naturally_faded_receipt())
    altered = detector.analyze(_digitally_erased_receipt())

    assert altered["classification"] == "digital_splice"
    assert altered["splice_likelihood"] > faded["splice_likelihood"]
    assert altered["high_frequency_ratio"] > faded["high_frequency_ratio"]
    assert altered["detected_regions"]


def test_layer2_evaluation_exposes_thermal_fade_analysis():
    result = Layer2ClassicalForensics().evaluate(_digitally_erased_receipt())

    assert result["thermal_fade_analysis"]["is_digital_splice"] is True
    assert result["thermal_fade_analysis"]["detected_regions"]


def test_small_image_is_inconclusive_and_invalid_config_is_rejected():
    result = ThermalFadeDiscriminator().analyze(Image.new("RGB", (32, 32), "white"))
    assert result["classification"] == "inconclusive"
    assert result["detected_regions"] == []

    with pytest.raises(ValueError):
        ThermalFadeConfig(high_frequency_cutoff=0.9)
