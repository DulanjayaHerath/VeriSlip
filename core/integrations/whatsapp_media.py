"""Secure, bounded retrieval of WhatsApp receipt media into memory."""

from __future__ import annotations

import os
import re
from typing import Optional
from urllib.parse import urlsplit

import httpx
from PIL import Image
from starlette.concurrency import run_in_threadpool

from core.security.image_sanitizer import (
    ImageValidationError,
    MAX_IMAGE_UPLOAD_BYTES,
    sanitize_image_bytes,
)

DEFAULT_GRAPH_API_BASE_URL = "https://graph.facebook.com"
DEFAULT_GRAPH_API_VERSION = "v21.0"
SUPPORTED_MEDIA_TYPES = frozenset({"image/jpeg", "image/png"})
_MEDIA_ID_PATTERN = re.compile(r"^[0-9]{1,64}$")
_VERSION_PATTERN = re.compile(r"^v[0-9]{1,3}\.[0-9]{1,3}$")
_ALLOWED_MEDIA_HOST_SUFFIXES = (".facebook.com", ".fbcdn.net", ".fbsbx.com")


class WhatsAppMediaError(ValueError):
    """A safe, client-facing WhatsApp media retrieval failure."""

    def __init__(self, detail: str, status_code: int):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


def _validate_media_url(url: object) -> str:
    if not isinstance(url, str):
        raise WhatsAppMediaError("WhatsApp returned an invalid media response.", 502)
    parsed = urlsplit(url)
    hostname = (parsed.hostname or "").lower()
    allowed_host = hostname in {"facebook.com", "fbcdn.net", "fbsbx.com"} or any(
        hostname.endswith(suffix) for suffix in _ALLOWED_MEDIA_HOST_SUFFIXES
    )
    try:
        port = parsed.port
    except ValueError:
        raise WhatsAppMediaError(
            "WhatsApp returned an invalid media response.", 502
        ) from None
    if (
        parsed.scheme != "https"
        or not allowed_host
        or parsed.username is not None
        or parsed.password is not None
        or port not in (None, 443)
    ):
        raise WhatsAppMediaError("WhatsApp returned an invalid media response.", 502)
    return url


def _raise_for_meta_status(status_code: int) -> None:
    if status_code in (400, 404):
        raise WhatsAppMediaError("WhatsApp media is invalid or unavailable.", 400)
    if status_code in (401, 403):
        raise WhatsAppMediaError("WhatsApp media service authentication failed.", 502)
    if status_code >= 400:
        raise WhatsAppMediaError("WhatsApp media service is unavailable.", 502)


async def _download_with_client(
    client: httpx.AsyncClient, media_id: str, access_token: str
) -> Image.Image:
    version = os.getenv("VERISLIP_WHATSAPP_GRAPH_API_VERSION", DEFAULT_GRAPH_API_VERSION)
    if not _VERSION_PATTERN.fullmatch(version):
        raise WhatsAppMediaError("WhatsApp media service is not configured.", 503)
    base_url = os.getenv("VERISLIP_WHATSAPP_GRAPH_API_BASE_URL", DEFAULT_GRAPH_API_BASE_URL)
    if base_url.rstrip("/") != DEFAULT_GRAPH_API_BASE_URL:
        raise WhatsAppMediaError("WhatsApp media service is not configured.", 503)

    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        metadata_response = await client.get(
            f"{base_url}/{version}/{media_id}", headers=headers
        )
        _raise_for_meta_status(metadata_response.status_code)
        try:
            metadata = metadata_response.json()
        except (ValueError, TypeError):
            raise WhatsAppMediaError(
                "WhatsApp returned an invalid media response.", 502
            ) from None

        if not isinstance(metadata, dict):
            raise WhatsAppMediaError("WhatsApp returned an invalid media response.", 502)
        media_type = (
            str(metadata.get("mime_type", "")).split(";", 1)[0].lower()
        )
        if media_type not in SUPPORTED_MEDIA_TYPES:
            raise WhatsAppMediaError("WhatsApp media must be a JPEG or PNG image.", 415)
        file_size = metadata.get("file_size")
        if isinstance(file_size, bool) or not isinstance(file_size, int):
            if file_size is not None:
                raise WhatsAppMediaError("WhatsApp returned an invalid media response.", 502)
        elif file_size < 0:
            raise WhatsAppMediaError("WhatsApp returned an invalid media response.", 502)
        elif file_size > MAX_IMAGE_UPLOAD_BYTES:
            raise WhatsAppMediaError("WhatsApp media exceeds the permitted size.", 413)

        media_url = _validate_media_url(metadata.get("url"))
        async with client.stream("GET", media_url, headers=headers) as media_response:
            _raise_for_meta_status(media_response.status_code)
            content_type = (
                media_response.headers.get("content-type", "")
                .split(";", 1)[0]
                .lower()
            )
            if content_type not in SUPPORTED_MEDIA_TYPES:
                raise WhatsAppMediaError("WhatsApp media must be a JPEG or PNG image.", 415)
            content_length = media_response.headers.get("content-length")
            if content_length:
                try:
                    parsed_content_length = int(content_length)
                except ValueError:
                    raise WhatsAppMediaError(
                        "WhatsApp returned an invalid media response.", 502
                    ) from None
                if parsed_content_length < 0:
                    raise WhatsAppMediaError(
                        "WhatsApp returned an invalid media response.", 502
                    )
                if parsed_content_length > MAX_IMAGE_UPLOAD_BYTES:
                    raise WhatsAppMediaError(
                        "WhatsApp media exceeds the permitted size.", 413
                    )

            data = bytearray()
            async for chunk in media_response.aiter_bytes():
                data.extend(chunk)
                if len(data) > MAX_IMAGE_UPLOAD_BYTES:
                    raise WhatsAppMediaError(
                        "WhatsApp media exceeds the permitted size.", 413
                    )
    except WhatsAppMediaError:
        raise
    except httpx.TimeoutException:
        raise WhatsAppMediaError("WhatsApp media service timed out.", 504) from None
    except httpx.HTTPError:
        raise WhatsAppMediaError("WhatsApp media service is unavailable.", 502) from None

    try:
        return await run_in_threadpool(sanitize_image_bytes, bytes(data))
    except ImageValidationError as exc:
        raise WhatsAppMediaError(exc.detail, exc.status_code) from None


async def download_whatsapp_image(
    media_id: str,
    *,
    access_token: Optional[str] = None,
    client: Optional[httpx.AsyncClient] = None,
) -> Image.Image:
    """Download and sanitize WhatsApp JPEG/PNG media without writing it to disk."""
    if not isinstance(media_id, str) or not _MEDIA_ID_PATTERN.fullmatch(media_id):
        raise WhatsAppMediaError("WhatsApp media ID is invalid.", 400)
    token = access_token or os.getenv("VERISLIP_WHATSAPP_ACCESS_TOKEN")
    if not token:
        raise WhatsAppMediaError("WhatsApp media service is not configured.", 503)

    if client is not None:
        return await _download_with_client(client, media_id, token)

    timeout = httpx.Timeout(connect=5.0, read=15.0, write=5.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as owned_client:
        return await _download_with_client(owned_client, media_id, token)
