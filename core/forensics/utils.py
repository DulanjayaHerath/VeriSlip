"""
Image utilities for VeriSlip forensics pipeline.
Handles format conversions, base64 encoding/decoding, and OpenCV/PIL adapters.
"""

import io
import base64
from typing import Tuple, Optional, Union
import numpy as np
from PIL import Image
import cv2

def bytes_to_pil(image_bytes: bytes) -> Image.Image:
    """Convert raw image bytes to PIL Image in RGB format."""
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image

def pil_to_bytes(image: Image.Image, format: str = "PNG", quality: int = 95) -> bytes:
    """Convert PIL Image to bytes."""
    buf = io.BytesIO()
    if format.upper() == "JPEG":
        image.save(buf, format=format, quality=quality)
    else:
        image.save(buf, format=format)
    return buf.getvalue()

def pil_to_cv2(image: Image.Image) -> np.ndarray:
    """Convert PIL Image (RGB) to OpenCV numpy array (BGR)."""
    rgb_arr = np.array(image)
    return cv2.cvtColor(rgb_arr, cv2.COLOR_RGB2BGR)

def cv2_to_pil(cv2_img: np.ndarray) -> Image.Image:
    """Convert OpenCV image (BGR) to PIL Image (RGB)."""
    rgb_arr = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb_arr)

def cv2_to_base64(cv2_img: np.ndarray, format: str = ".png") -> str:
    """Encode OpenCV image directly to base64 data URI."""
    success, encoded = cv2.imencode(format, cv2_img)
    if not success:
        raise ValueError("Failed to encode image to base64")
    b64_str = base64.b64encode(encoded).decode("utf-8")
    mime = "image/png" if format == ".png" else "image/jpeg"
    return f"data:{mime};base64,{b64_str}"

def pil_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Encode PIL image to base64 data URI."""
    buf = io.BytesIO()
    image.save(buf, format=format)
    b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    mime = f"image/{format.lower()}"
    return f"data:{mime};base64,{b64_str}"

def normalize_dimensions(image: Image.Image, max_dim: int = 1600) -> Image.Image:
    """Ensure image is within reasonable bounds for fast forensic analysis without losing fidelity."""
    w, h = image.size
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        return image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return image
