"""Local, deterministic PII detection and pixel redaction for receipt images.

The module intentionally keeps OCR, classification, geometry, and rendering
separate. Detection returns only PII categories and bounding boxes; recognized
values are never retained in results, logs, or exceptions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping, Sequence

from PIL import Image, ImageDraw, ImageFilter


class PIIRedactionError(ValueError):
    """A privacy-safe failure that does not include recognized OCR text."""


@dataclass(frozen=True)
class PIIRegion:
    """A classified rectangular PII location without the sensitive value."""

    pii_type: str
    box: tuple[int, int, int, int]


@dataclass(frozen=True)
class RedactionResult:
    """A metadata-free redacted image and non-sensitive summary."""

    image: Image.Image
    regions: tuple[PIIRegion, ...]

    @property
    def counts(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for region in self.regions:
            result[region.pii_type] = result.get(region.pii_type, 0) + 1
        return result


_PHONE_RE = re.compile(r"(?<!\d)(?:\+?94|0)[\s().-]*7\d(?:[\s().-]*\d){7}(?!\d)")
_OLD_NIC_RE = re.compile(r"(?<![A-Z0-9])\d{9}[VX](?![A-Z0-9])", re.IGNORECASE)
_NEW_NIC_RE = re.compile(r"(?<!\d)(?:19|20)\d{10}(?!\d)")
_ACCOUNT_VALUE_RE = re.compile(r"^(?=(?:\D*\d){6,18}\D*$)[\d\s-]+$")
_NAME_VALUE_RE = re.compile(
    r"^[^\W\d_][^\W\d_.'’-]*(?:[\s.'’-]+[^\W\d_][^\W\d_.'’-]*){0,4}$", re.UNICODE
)

_ACCOUNT_LABELS = (
    "account number",
    "account no",
    "account #",
    "acct no",
    "a/c no",
    "a/c",
    "account",
)
_NAME_LABELS = (
    "customer name",
    "account holder",
    "beneficiary name",
    "recipient name",
    "sender name",
    "payee name",
    "name",
)
_NIC_LABELS = ("nic number", "nic no", "nic")
_NON_PII_LABELS = (
    "amount",
    "total",
    "date",
    "time",
    "reference",
    "transaction id",
    "receipt no",
)


@dataclass(frozen=True)
class _Token:
    text: str
    box: tuple[int, int, int, int]


def _parse_tokens(ocr_tokens: Iterable[Mapping[str, Any]]) -> list[_Token]:
    parsed: list[_Token] = []
    try:
        for raw in ocr_tokens:
            if not isinstance(raw, Mapping):
                raise PIIRedactionError("OCR output is malformed.")
            text = raw.get("text", "")
            if not isinstance(text, str):
                raise PIIRedactionError("OCR output is malformed.")
            x, y, w, h = (int(raw[key]) for key in ("x", "y", "w", "h"))
            if x < 0 or y < 0 or w <= 0 or h <= 0:
                raise PIIRedactionError("OCR output is malformed.")
            if text.strip():
                parsed.append(_Token(text.strip(), (x, y, x + w, y + h)))
    except (KeyError, TypeError, ValueError, OverflowError):
        raise PIIRedactionError("OCR output is malformed.") from None
    return parsed


def _same_line(first: _Token, second: _Token) -> bool:
    first_mid = (first.box[1] + first.box[3]) / 2
    second_mid = (second.box[1] + second.box[3]) / 2
    return (
        abs(first_mid - second_mid)
        <= max(first.box[3] - first.box[1], second.box[3] - second.box[1]) * 0.65
    )


def _group_lines(tokens: Sequence[_Token]) -> list[list[_Token]]:
    lines: list[list[_Token]] = []
    for token in sorted(tokens, key=lambda item: (item.box[1], item.box[0])):
        for line in lines:
            if _same_line(line[0], token):
                line.append(token)
                break
        else:
            lines.append([token])
    for line in lines:
        line.sort(key=lambda item: item.box[0])
    return lines


def _union_box(tokens: Sequence[_Token]) -> tuple[int, int, int, int]:
    return (
        min(token.box[0] for token in tokens),
        min(token.box[1] for token in tokens),
        max(token.box[2] for token in tokens),
        max(token.box[3] for token in tokens),
    )


def _matching_spans(
    line: Sequence[_Token], pattern: re.Pattern[str]
) -> list[list[_Token]]:
    text = " ".join(token.text for token in line)
    spans: list[tuple[int, int, _Token]] = []
    offset = 0
    for token in line:
        spans.append((offset, offset + len(token.text), token))
        offset += len(token.text) + 1
    matches: list[list[_Token]] = []
    for match in pattern.finditer(text):
        selected = [
            token
            for start, end, token in spans
            if start < match.end() and end > match.start()
        ]
        if selected:
            matches.append(selected)
    return matches


def _label_value_tokens(line: Sequence[_Token], labels: Sequence[str]) -> list[_Token]:
    """Return tokens following a label, handling labels split by OCR."""
    lowered = [token.text.casefold().strip(" :#") for token in line]
    best_end = -1
    best_words = -1
    for end in range(len(line)):
        for start in range(max(0, end - 2), end + 1):
            phrase = " ".join(lowered[start : end + 1])
            word_count = end - start + 1
            if phrase in labels and word_count > best_words:
                best_end = end
                best_words = word_count
    return list(line[best_end + 1 :]) if best_end >= 0 else []


def detect_pii_regions(
    ocr_tokens: Iterable[Mapping[str, Any]],
) -> tuple[PIIRegion, ...]:
    """Classify local OCR tokens and return PII locations without PII values.

    Phone and Sri Lankan NIC formats are strong identifiers and may be detected
    directly. Account numbers and names require an explicit nearby label so
    dates, totals, times, and ordinary transaction values are not blindly
    masked.
    """
    if ocr_tokens is None:
        raise PIIRedactionError("OCR output is unavailable.")
    tokens = _parse_tokens(ocr_tokens)
    regions: list[PIIRegion] = []

    for line in _group_lines(tokens):
        line_text = " ".join(token.text.casefold() for token in line)
        for pii_type, pattern in (("phone", _PHONE_RE), ("national_id", _OLD_NIC_RE)):
            for matched in _matching_spans(line, pattern):
                regions.append(PIIRegion(pii_type, _union_box(matched)))

        nic_values = _label_value_tokens(line, _NIC_LABELS)
        if nic_values and _NEW_NIC_RE.search(
            " ".join(token.text for token in nic_values)
        ):
            regions.append(PIIRegion("national_id", _union_box(nic_values)))

        if any(label in line_text for label in _NON_PII_LABELS):
            continue

        account_values = _label_value_tokens(line, _ACCOUNT_LABELS)
        account_text = " ".join(token.text for token in account_values).strip(" :")
        if account_values and _ACCOUNT_VALUE_RE.fullmatch(account_text):
            regions.append(PIIRegion("account_number", _union_box(account_values)))

        name_values = _label_value_tokens(line, _NAME_LABELS)
        name_text = " ".join(token.text for token in name_values).strip(" :")
        if name_values and _NAME_VALUE_RE.fullmatch(name_text):
            regions.append(PIIRegion("person_name", _union_box(name_values)))

    return _deduplicate_regions(regions)


def _deduplicate_regions(regions: Sequence[PIIRegion]) -> tuple[PIIRegion, ...]:
    unique: dict[tuple[str, tuple[int, int, int, int]], PIIRegion] = {}
    for region in regions:
        unique[(region.pii_type, region.box)] = region
    return tuple(
        sorted(
            unique.values(),
            key=lambda region: (region.box[1], region.box[0], region.pii_type),
        )
    )


def normalize_regions(
    regions: Iterable[PIIRegion], image_size: tuple[int, int], padding: int = 3
) -> tuple[PIIRegion, ...]:
    """Pad and clip detected boxes to the image boundary."""
    width, height = image_size
    if width <= 0 or height <= 0 or padding < 0:
        raise PIIRedactionError("Image or redaction geometry is invalid.")
    normalized: list[PIIRegion] = []
    for region in regions:
        left, top, right, bottom = region.box
        box = (
            max(0, left - padding),
            max(0, top - padding),
            min(width, right + padding),
            min(height, bottom + padding),
        )
        if box[0] >= box[2] or box[1] >= box[3]:
            raise PIIRedactionError("Redaction geometry is invalid.")
        normalized.append(PIIRegion(region.pii_type, box))
    return tuple(normalized)


def redact_regions(
    image: Image.Image,
    regions: Iterable[PIIRegion],
    *,
    method: str = "mask",
    padding: int = 3,
) -> RedactionResult:
    """Redact actual pixels with an opaque mask or strong blur.

    A detached RGB image is always returned and its metadata is cleared.
    """
    if not isinstance(image, Image.Image) or image.width <= 0 or image.height <= 0:
        raise PIIRedactionError("Image input is invalid.")
    if method not in {"mask", "blur"}:
        raise PIIRedactionError("Redaction method must be 'mask' or 'blur'.")
    output = Image.frombytes("RGB", image.size, image.convert("RGB").tobytes())
    safe_regions = normalize_regions(tuple(regions), output.size, padding)
    if method == "mask":
        draw = ImageDraw.Draw(output)
        for region in safe_regions:
            draw.rectangle(region.box, fill=(0, 0, 0))
    else:
        for region in safe_regions:
            crop = output.crop(region.box)
            radius = max(12, min(crop.size) // 2)
            output.paste(
                crop.filter(ImageFilter.GaussianBlur(radius=radius)), region.box
            )
    output.info.clear()
    return RedactionResult(output, safe_regions)


class PIIRedactionPipeline:
    """Run injected/local OCR, deterministic detection, and pixel redaction."""

    def __init__(
        self, ocr: Callable[[Image.Image], Iterable[Mapping[str, Any]]] | None = None
    ):
        if ocr is None:
            from core.forensics.ocr_extractor import ReceiptFieldExtractor

            ocr = ReceiptFieldExtractor().extract_ocr_tokens
        self._ocr = ocr

    def redact(self, image: Image.Image, *, method: str = "mask") -> RedactionResult:
        """Return a safely redacted image or fail closed if OCR is unavailable."""
        try:
            tokens = self._ocr(image)
        except Exception:
            raise PIIRedactionError(
                "Local OCR could not complete PII redaction."
            ) from None
        if tokens is None:
            raise PIIRedactionError("Local OCR could not complete PII redaction.")
        parsed_tokens = list(tokens)
        regions = detect_pii_regions(parsed_tokens)
        if not any(
            str(token.get("text", "")).strip()
            for token in parsed_tokens
            if isinstance(token, Mapping)
        ):
            raise PIIRedactionError("Local OCR found no text; image was not exported.")
        return redact_regions(image, regions, method=method)
