"""OCR crop handling must tolerate small images and empty regions."""

import warnings

import numpy as np
import pytest
from PIL import Image

from core.forensics.ocr_extractor import ReceiptFieldExtractor


@pytest.fixture
def extractor():
    instance = ReceiptFieldExtractor()
    instance.has_native_ocr = False
    return instance


@pytest.mark.parametrize("size", [(1, 1), (2, 2), (3, 4), (1, 80), (80, 1)])
def test_tiny_images_have_no_empty_crop_errors_or_warnings(extractor, size):
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        result = extractor.extract_fields(Image.new("RGB", size, "white"))
    assert result["field_regions"]["amount_box"] is None
    assert result["field_regions"]["field_rows_count"] == 0
    assert np.isfinite(result["bank_confidence"])


@pytest.mark.parametrize("start,end", [(0, 0), (10, 5), (20, 40), (-10, -1)])
def test_empty_or_outside_regions_have_no_detections(extractor, start, end):
    assert extractor.detect_text_lines(np.zeros((20, 80), np.uint8), start, end) == []


def test_clipped_region_boxes_keep_image_coordinates(extractor):
    gray = np.full((80, 100), 255, np.uint8)
    gray[20:35, 30:70] = 0
    expected = extractor.detect_text_lines(gray, 0, 80)
    assert expected
    assert extractor.detect_text_lines(gray, -10, 100) == expected
    assert extractor.detect_text_lines(gray, 10, 80) == expected
