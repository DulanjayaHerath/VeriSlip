"""Fail-closed validation and sanitization for untrusted receipt images."""

from __future__ import annotations

import io
import warnings

from PIL import Image, ImageOps, UnidentifiedImageError

MAX_IMAGE_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_IMAGE_WIDTH = 6_000
MAX_IMAGE_HEIGHT = 6_000
MAX_IMAGE_PIXELS = 20_000_000
SUPPORTED_IMAGE_FORMATS = frozenset({"JPEG", "PNG"})


class ImageValidationError(ValueError):
    """A safe, client-facing rejection of an untrusted image."""

    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


def _check_dimensions(width: int, height: int) -> None:
    if width <= 0 or height <= 0:
        raise ImageValidationError("Image dimensions are invalid.")
    if (
        width > MAX_IMAGE_WIDTH
        or height > MAX_IMAGE_HEIGHT
        or width * height > MAX_IMAGE_PIXELS
    ):
        raise ImageValidationError(
            "Image dimensions exceed the permitted limit.", status_code=413
        )


def _bomb_warning_type():
    return getattr(Image, "DecompressionBombWarning", RuntimeWarning)


def _bomb_error_type():
    return getattr(Image, "DecompressionBombError", Exception)


def sanitize_image_bytes(image_bytes: bytes) -> Image.Image:
    """Validate and detach a JPEG/PNG into a metadata-free RGB pixel image.

    File names and caller-supplied MIME types are deliberately ignored. Pillow
    identifies the encoded format from the file header, verifies the complete
    stream, and fully decodes it while decompression-bomb warnings are fatal.
    The returned image contains decoded pixels only, preventing metadata,
    appended data, or parser state from reaching the forensic pipeline.
    """
    if not image_bytes:
        raise ImageValidationError("Uploaded image is empty.")
    if len(image_bytes) > MAX_IMAGE_UPLOAD_BYTES:
        raise ImageValidationError(
            "Image upload exceeds the permitted size.", status_code=413
        )

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", _bomb_warning_type())
            with Image.open(io.BytesIO(image_bytes)) as probe:
                image_format = (probe.format or "").upper()
                if image_format not in SUPPORTED_IMAGE_FORMATS:
                    raise ImageValidationError(
                        "Unsupported image format. Only JPEG and PNG are accepted.",
                        status_code=415,
                    )
                if getattr(probe, "n_frames", 1) != 1:
                    raise ImageValidationError("Animated images are not accepted.")
                _check_dimensions(*probe.size)
                probe.verify()

            with Image.open(io.BytesIO(image_bytes)) as decoded:
                _check_dimensions(*decoded.size)
                decoded.load()
                oriented = ImageOps.exif_transpose(decoded)

                if oriented.mode in {"RGBA", "LA"} or (
                    oriented.mode == "P" and "transparency" in oriented.info
                ):
                    rgba = oriented.convert("RGBA")
                    background = Image.new("RGBA", rgba.size, "white")
                    background.alpha_composite(rgba)
                    rgb = background.convert("RGB")
                else:
                    rgb = oriented.convert("RGB")

                _check_dimensions(*rgb.size)
                sanitized = Image.frombytes("RGB", rgb.size, rgb.tobytes())
                sanitized.info.clear()
                return sanitized
    except ImageValidationError:
        raise
    except (_bomb_error_type(), _bomb_warning_type()):
        raise ImageValidationError(
            "Image dimensions exceed the permitted limit.", status_code=413
        ) from None
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError):
        raise ImageValidationError(
            "Uploaded file is not a valid, complete JPEG or PNG image."
        ) from None
