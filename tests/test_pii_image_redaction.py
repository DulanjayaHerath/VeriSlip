"""Tests for privacy-preserving receipt image PII redaction."""

import io
import logging

import pytest
from PIL import Image

from core.privacy.pii_redaction import (
    PIIRedactionError,
    PIIRedactionPipeline,
    detect_pii_regions,
    redact_regions,
)
from scripts import redact_receipts


def _tokens(*values):
    return [
        {"text": text, "x": x, "y": y, "w": width, "h": 10, "confidence": 0.99}
        for text, x, y, width in values
    ]


def _types(regions):
    return [region.pii_type for region in regions]


def test_phone_number_detection_and_redaction():
    tokens = _tokens(
        ("Phone", 5, 10, 35),
        ("+94", 45, 10, 25),
        ("77", 75, 10, 18),
        ("123", 98, 10, 24),
        ("4567", 127, 10, 32),
    )
    regions = detect_pii_regions(tokens)
    assert _types(regions) == ["phone"]
    result = redact_regions(Image.new("RGB", (180, 40), "white"), regions, padding=0)
    assert result.image.getpixel((50, 15)) == (0, 0, 0)


def test_account_number_requires_context_and_is_redacted():
    tokens = _tokens(
        ("Account", 5, 10, 45), ("No", 55, 10, 15), ("8012-3456-7890", 75, 10, 90)
    )
    regions = detect_pii_regions(tokens)
    assert _types(regions) == ["account_number"]
    assert regions[0].box == (75, 10, 165, 20)


def test_multiple_pii_regions_are_detected_without_retaining_values():
    tokens = _tokens(
        ("Name", 5, 5, 30),
        ("Sample", 40, 5, 42),
        ("Person", 87, 5, 42),
        ("Phone", 5, 25, 35),
        ("0771234567", 45, 25, 75),
        ("A/C", 5, 45, 25),
        ("12345678901", 35, 45, 85),
    )
    regions = detect_pii_regions(tokens)
    assert set(_types(regions)) == {"person_name", "phone", "account_number"}
    assert "Sample" not in repr(regions)
    assert "0771234567" not in repr(regions)


def test_sri_lankan_nic_is_treated_as_sensitive_identifier():
    regions = detect_pii_regions(
        _tokens(("NIC", 5, 10, 25), ("200012345678", 35, 10, 90))
    )
    assert _types(regions) == ["national_id"]


@pytest.mark.parametrize(
    "values",
    [
        (("Amount", 5, 10, 45), ("12,500.00", 55, 10, 70)),
        (("Date", 5, 10, 30), ("2026-09-29", 40, 10, 75)),
        (("Time", 5, 10, 30), ("14:35:20", 40, 10, 55)),
        (("Reference", 5, 10, 60), ("123456789012", 70, 10, 85)),
    ],
)
def test_non_pii_financial_values_remain_unmasked(values):
    assert detect_pii_regions(_tokens(*values)) == ()


def test_only_pixels_inside_redaction_region_change():
    image = Image.new("RGB", (100, 60), (240, 240, 240))
    regions = detect_pii_regions(
        _tokens(("Phone", 10, 20, 30), ("0712345678", 45, 20, 45))
    )
    result = redact_regions(image, regions, padding=0)
    assert result.image.getpixel((50, 25)) != image.getpixel((50, 25))
    assert result.image.getpixel((5, 5)) == image.getpixel((5, 5))
    assert result.image.getpixel((95, 55)) == image.getpixel((95, 55))


def test_grayscale_input_is_detached_rgb_and_metadata_is_removed():
    image = Image.new("L", (100, 40), 255)
    image.info["comment"] = "private metadata"
    regions = detect_pii_regions(
        _tokens(("Phone", 5, 10, 30), ("0712345678", 40, 10, 55))
    )
    result = redact_regions(image, regions)
    assert result.image.mode == "RGB"
    assert result.image.info == {}
    assert image.info["comment"] == "private metadata"


def test_empty_ocr_fails_closed_without_exporting_unredacted_pixels():
    pipeline = PIIRedactionPipeline(ocr=lambda _image: [])
    with pytest.raises(PIIRedactionError, match="no text"):
        pipeline.redact(Image.new("RGB", (20, 20), "white"))


@pytest.mark.parametrize(
    "tokens",
    [None, [{"text": "Phone", "x": 0, "y": 0, "w": -1, "h": 10}], ["not-a-token"]],
)
def test_malformed_ocr_is_rejected_with_safe_error(tokens):
    if tokens is None:
        with pytest.raises(PIIRedactionError, match="unavailable"):
            detect_pii_regions(tokens)
    else:
        with pytest.raises(PIIRedactionError, match="malformed"):
            detect_pii_regions(tokens)


def test_ocr_failure_does_not_leak_sensitive_value_to_exception_or_logs(caplog):
    sensitive = "0712345678"

    def failing_ocr(_image):
        raise RuntimeError(f"engine rejected {sensitive}")

    pipeline = PIIRedactionPipeline(ocr=failing_ocr)
    with caplog.at_level(logging.DEBUG), pytest.raises(PIIRedactionError) as exc_info:
        pipeline.redact(Image.new("RGB", (20, 20), "white"))
    assert sensitive not in str(exc_info.value)
    assert sensitive not in caplog.text


def test_blur_changes_sensitive_pixels_and_keeps_distant_pixels():
    image = Image.new("RGB", (120, 50), "white")
    for x in range(45, 100, 2):
        image.putpixel((x, 25), (0, 0, 0))
    regions = detect_pii_regions(
        _tokens(("Phone", 5, 20, 30), ("0712345678", 45, 20, 55))
    )
    result = redact_regions(image, regions, method="blur", padding=0)
    assert (
        result.image.crop(regions[0].box).tobytes()
        != image.crop(regions[0].box).tobytes()
    )
    assert result.image.getpixel((5, 5)) == image.getpixel((5, 5))


def test_dataset_cli_uses_sanitizer_and_never_overwrites_existing_output(
    tmp_path, monkeypatch
):
    source_dir = tmp_path / "incoming"
    output_dir = tmp_path / "redacted"
    source_dir.mkdir()
    image = Image.new("RGB", (100, 40), "white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", pnginfo=None)
    (source_dir / "sample.png").write_bytes(buffer.getvalue())

    fake_pipeline = PIIRedactionPipeline(
        ocr=lambda _image: _tokens(("Phone", 5, 10, 30), ("0712345678", 40, 10, 55))
    )
    monkeypatch.setattr(redact_receipts, "PIIRedactionPipeline", lambda: fake_pipeline)

    assert redact_receipts.redact_path(source_dir, output_dir) == (1, 0)
    output = output_dir / "sample.redacted.png"
    first_bytes = output.read_bytes()
    assert Image.open(output).info == {}
    assert redact_receipts.redact_path(source_dir, output_dir) == (0, 1)
    assert output.read_bytes() == first_bytes


def test_dataset_cli_rejects_same_directory_and_invalid_image(tmp_path):
    source = tmp_path / "receipt.png"
    source.write_bytes(b"not an image")
    with pytest.raises(PIIRedactionError, match="separate"):
        redact_receipts.redact_path(source, tmp_path)
    assert redact_receipts.redact_path(source, tmp_path / "safe-output") == (0, 1)
