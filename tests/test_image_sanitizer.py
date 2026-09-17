"""Security tests for untrusted receipt image ingestion."""

import io

import pytest
from PIL import Image

from core.security import image_sanitizer
from core.security.image_sanitizer import ImageValidationError, sanitize_image_bytes


def _encoded_image(format_name: str, size=(120, 80), mode="RGB") -> bytes:
    image = Image.new(mode, size, color="white")
    buffer = io.BytesIO()
    image.save(buffer, format=format_name)
    return buffer.getvalue()


@pytest.mark.parametrize("format_name", ["JPEG", "PNG"])
def test_sanitizes_supported_images_to_detached_rgb_pixels(format_name):
    payload = _encoded_image(format_name)

    sanitized = sanitize_image_bytes(payload)

    assert sanitized.mode == "RGB"
    assert sanitized.size == (120, 80)
    assert sanitized.info == {}
    sanitized.load()


def test_strips_metadata_from_accepted_image():
    image = Image.new("RGB", (40, 40), "white")
    exif = image.getexif()
    exif[0x0131] = "untrusted-editor-value"
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", exif=exif)

    sanitized = sanitize_image_bytes(buffer.getvalue())

    assert sanitized.getexif().get(0x0131) is None
    assert sanitized.info == {}


def test_rejects_unsupported_image_format():
    with pytest.raises(ImageValidationError) as exc_info:
        sanitize_image_bytes(_encoded_image("GIF"))

    assert exc_info.value.status_code == 415
    assert "JPEG and PNG" in exc_info.value.detail


@pytest.mark.parametrize("payload", [b"not an image", b"\x89PNG\r\n\x1a\ntruncated"])
def test_rejects_malformed_or_truncated_image(payload):
    with pytest.raises(ImageValidationError) as exc_info:
        sanitize_image_bytes(payload)

    assert exc_info.value.status_code == 400
    assert "valid, complete" in exc_info.value.detail


def test_rejects_encoded_upload_over_byte_limit(monkeypatch):
    monkeypatch.setattr(image_sanitizer, "MAX_IMAGE_UPLOAD_BYTES", 8)

    with pytest.raises(ImageValidationError) as exc_info:
        sanitize_image_bytes(b"123456789")

    assert exc_info.value.status_code == 413


def test_rejects_image_over_dimension_limit(monkeypatch):
    monkeypatch.setattr(image_sanitizer, "MAX_IMAGE_WIDTH", 50)

    with pytest.raises(ImageValidationError) as exc_info:
        sanitize_image_bytes(_encoded_image("PNG", size=(51, 10)))

    assert exc_info.value.status_code == 413


def test_treats_pillow_decompression_bomb_warning_as_error(monkeypatch):
    monkeypatch.setattr(Image, "MAX_IMAGE_PIXELS", 100)

    with pytest.raises(ImageValidationError) as exc_info:
        sanitize_image_bytes(_encoded_image("PNG", size=(15, 10)))

    assert exc_info.value.status_code == 413
