"""Deterministic COCO and Pascal VOC exports for VeriSlip synthetic data."""

from __future__ import annotations

import csv
import json
import math
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

from PIL import Image, UnidentifiedImageError

REQUIRED_METADATA_FIELDS = frozenset(
    {
        "filename",
        "is_tampered",
        "tamper_type",
        "bbox_x",
        "bbox_y",
        "bbox_w",
        "bbox_h",
    }
)
_WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:/")


class AnnotationExportError(ValueError):
    """A safe validation or export failure for dataset annotations."""


@dataclass(frozen=True)
class BinaryMask:
    """COCO-compatible uncompressed run-length encoding in column-major order."""

    height: int
    width: int
    counts: tuple[int, ...]


@dataclass(frozen=True)
class NormalizedObject:
    """One clipped tamper object using ``(x, y, width, height)`` geometry."""

    category: str
    bbox: tuple[float, float, float, float]
    segmentation: BinaryMask | None = None


@dataclass(frozen=True)
class NormalizedImage:
    """One relative dataset image and its normalized annotations."""

    file_name: str
    width: int
    height: int
    objects: tuple[NormalizedObject, ...]


@dataclass(frozen=True)
class AnnotationDataset:
    """Format-independent, deterministically ordered dataset annotations."""

    images: tuple[NormalizedImage, ...]
    categories: tuple[str, ...]


def _safe_relative_path(value: str, *, field: str) -> str:
    raw = str(value).strip().replace("\\", "/")
    path = PurePosixPath(raw)
    if (
        not raw
        or path.is_absolute()
        or _WINDOWS_ABSOLUTE_RE.match(raw)
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise AnnotationExportError(f"{field} must be a safe relative path.")
    return path.as_posix()


def _dataset_file(root: Path, relative: str, *, field: str) -> Path:
    root_resolved = root.resolve()
    candidate = root.joinpath(*PurePosixPath(relative).parts)
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        raise AnnotationExportError(
            f"{field} does not reference a readable file."
        ) from None
    if not resolved.is_relative_to(root_resolved) or candidate.is_symlink():
        raise AnnotationExportError(
            f"{field} must remain inside the dataset directory."
        )
    return resolved


def _number(value: float) -> int | float:
    return int(value) if value.is_integer() else value


def _parse_float(value: Any, *, field: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise AnnotationExportError(f"{field} must be a finite number.") from None
    if not math.isfinite(result):
        raise AnnotationExportError(f"{field} must be a finite number.")
    return result


def _clip_bbox(
    box: Sequence[Any], width: int, height: int
) -> tuple[float, float, float, float]:
    if isinstance(box, (str, bytes)) or len(box) != 4:
        raise AnnotationExportError("Bounding boxes must contain exactly four values.")
    x, y, box_width, box_height = (
        _parse_float(value, field="Bounding box coordinate") for value in box
    )
    if box_width <= 0 or box_height <= 0:
        raise AnnotationExportError(
            "Bounding boxes must have positive width and height."
        )

    x2 = x + box_width
    y2 = y + box_height
    clipped_x1 = min(float(width), max(0.0, x))
    clipped_y1 = min(float(height), max(0.0, y))
    clipped_x2 = min(float(width), max(0.0, x2))
    clipped_y2 = min(float(height), max(0.0, y2))
    if clipped_x2 <= clipped_x1 or clipped_y2 <= clipped_y1:
        raise AnnotationExportError("Bounding box has no area inside the image.")
    return (
        clipped_x1,
        clipped_y1,
        clipped_x2 - clipped_x1,
        clipped_y2 - clipped_y1,
    )


def _image_size(path: Path) -> tuple[int, int]:
    try:
        with Image.open(path) as image:
            width, height = image.size
            image.verify()
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError):
        raise AnnotationExportError("Dataset image is corrupt or invalid.") from None
    if width <= 0 or height <= 0:
        raise AnnotationExportError("Dataset image dimensions must be positive.")
    return width, height


def encode_binary_mask(mask: Image.Image, expected_size: tuple[int, int]) -> BinaryMask:
    """Encode a genuine binary mask as deterministic uncompressed COCO RLE."""
    converted = mask.convert("L")
    if converted.size != expected_size:
        raise AnnotationExportError("Mask dimensions must match the source image.")
    width, height = expected_size
    pixels = converted.tobytes()
    counts: list[int] = []
    current = 0
    run_length = 0
    has_foreground = False
    for x in range(width):
        for y in range(height):
            foreground = pixels[(y * width) + x] != 0
            has_foreground = has_foreground or foreground
            value = 1 if foreground else 0
            if value == current:
                run_length += 1
            else:
                counts.append(run_length)
                run_length = 1
                current = value
    counts.append(run_length)
    if not has_foreground:
        raise AnnotationExportError("Tampered annotations cannot use an empty mask.")
    return BinaryMask(height=height, width=width, counts=tuple(counts))


def _load_mask(path: Path, expected_size: tuple[int, int]) -> BinaryMask:
    try:
        with Image.open(path) as image:
            image.load()
            return encode_binary_mask(image, expected_size)
    except AnnotationExportError:
        raise
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError):
        raise AnnotationExportError(
            "Segmentation mask is corrupt or invalid."
        ) from None


def _is_tampered(value: Any) -> bool:
    normalized = str(value).strip().casefold()
    if normalized in {"1", "true"}:
        return True
    if normalized in {"0", "false"}:
        return False
    raise AnnotationExportError("is_tampered must be 0, 1, true, or false.")


def _object_sort_key(item: NormalizedObject) -> tuple[Any, ...]:
    return (item.category, *item.bbox)


def _build_dataset(images: Iterable[NormalizedImage]) -> AnnotationDataset:
    ordered = tuple(sorted(images, key=lambda item: item.file_name))
    categories = tuple(
        sorted({obj.category for image in ordered for obj in image.objects})
    )
    return AnnotationDataset(images=ordered, categories=categories)


def load_annotation_dataset(
    dataset_root: Path | str, metadata_file: Path | str | None = None
) -> AnnotationDataset:
    """Load the canonical CSV, images, and optional masks produced by VeriSlip."""
    root = Path(dataset_root)
    if not root.is_dir():
        raise AnnotationExportError("Dataset directory does not exist.")
    metadata_path = (
        Path(metadata_file) if metadata_file else root / "dataset_metadata.csv"
    )
    try:
        metadata_resolved = metadata_path.resolve(strict=True)
    except OSError:
        raise AnnotationExportError("Dataset metadata CSV does not exist.") from None
    if not metadata_resolved.is_file():
        raise AnnotationExportError("Dataset metadata CSV is not a file.")

    try:
        with metadata_resolved.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames is None or not REQUIRED_METADATA_FIELDS.issubset(
                reader.fieldnames
            ):
                raise AnnotationExportError(
                    "Dataset metadata CSV is missing required annotation columns."
                )
            rows = list(reader)
    except UnicodeError:
        raise AnnotationExportError("Dataset metadata CSV must be UTF-8.") from None
    except OSError:
        raise AnnotationExportError("Dataset metadata CSV could not be read.") from None

    grouped: dict[str, list[Mapping[str, str]]] = {}
    for row in rows:
        relative = _safe_relative_path(row.get("filename", ""), field="filename")
        grouped.setdefault(relative, []).append(row)

    normalized_images: list[NormalizedImage] = []
    for relative in sorted(grouped):
        image_path = _dataset_file(root, relative, field="filename")
        width, height = _image_size(image_path)
        objects: list[NormalizedObject] = []
        for row in grouped[relative]:
            if not _is_tampered(row.get("is_tampered")):
                continue
            category = str(row.get("tamper_type", "")).strip()
            if not category or category.upper() == "NONE":
                raise AnnotationExportError(
                    "Tampered rows must provide a concrete tamper_type."
                )
            bbox = _clip_bbox(
                [
                    row.get("bbox_x"),
                    row.get("bbox_y"),
                    row.get("bbox_w"),
                    row.get("bbox_h"),
                ],
                width,
                height,
            )
            segmentation = None
            mask_name = str(row.get("mask_filename", "")).strip()
            if mask_name:
                mask_relative = _safe_relative_path(mask_name, field="mask_filename")
                mask_path = _dataset_file(root, mask_relative, field="mask_filename")
                segmentation = _load_mask(mask_path, (width, height))
            objects.append(NormalizedObject(category, bbox, segmentation))
        normalized_images.append(
            NormalizedImage(
                relative,
                width,
                height,
                tuple(sorted(objects, key=_object_sort_key)),
            )
        )
    return _build_dataset(normalized_images)


def normalize_generator_annotation(
    file_name: str,
    image_size: tuple[int, int],
    metadata: Mapping[str, Any],
    mask: Image.Image | None = None,
) -> AnnotationDataset:
    """Adapt native ``SyntheticSlipGenerator`` metadata without changing it."""
    relative = _safe_relative_path(file_name, field="file_name")
    width, height = image_size
    if width <= 0 or height <= 0:
        raise AnnotationExportError("Image dimensions must be positive.")
    if not bool(metadata.get("is_tampered", False)):
        return _build_dataset([NormalizedImage(relative, width, height, ())])
    category = str(metadata.get("tamper_type", "")).strip()
    boxes = metadata.get("ground_truth_boxes")
    if not category or not isinstance(boxes, list) or not boxes:
        raise AnnotationExportError("Generator tamper metadata is malformed.")
    segmentation = encode_binary_mask(mask, image_size) if mask is not None else None
    objects: list[NormalizedObject] = []
    for entry in boxes:
        if not isinstance(entry, Mapping) or "box" not in entry:
            raise AnnotationExportError("Generator bounding-box metadata is malformed.")
        objects.append(
            NormalizedObject(
                category,
                _clip_bbox(entry["box"], width, height),
                segmentation,
            )
        )
    image = NormalizedImage(
        relative, width, height, tuple(sorted(objects, key=_object_sort_key))
    )
    return _build_dataset([image])


def build_coco(dataset: AnnotationDataset) -> dict[str, Any]:
    """Build a deterministic COCO object-detection document."""
    category_ids = {name: index for index, name in enumerate(dataset.categories, 1)}
    images = []
    annotations = []
    annotation_id = 1
    for image_id, item in enumerate(dataset.images, 1):
        images.append(
            {
                "id": image_id,
                "file_name": item.file_name,
                "width": item.width,
                "height": item.height,
            }
        )
        for obj in item.objects:
            x, y, width, height = obj.bbox
            annotation: dict[str, Any] = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_ids[obj.category],
                "bbox": [_number(value) for value in obj.bbox],
                "area": _number(width * height),
                "iscrowd": 0,
            }
            if obj.segmentation is not None:
                annotation["segmentation"] = {
                    "size": [obj.segmentation.height, obj.segmentation.width],
                    "counts": list(obj.segmentation.counts),
                }
            annotations.append(annotation)
            annotation_id += 1
    return {
        "images": images,
        "annotations": annotations,
        "categories": [
            {"id": category_ids[name], "name": name, "supercategory": "tampering"}
            for name in dataset.categories
        ],
    }


def _indent_xml(root: ET.Element) -> None:
    try:
        ET.indent(root, space="  ")
    except AttributeError:  # pragma: no cover - Python 3.8 compatibility
        pass


def build_voc_xml(image: NormalizedImage) -> ET.ElementTree:
    """Build one Pascal VOC XML tree with outward-rounded bounding boxes."""
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = str(PurePosixPath(image.file_name).parent)
    ET.SubElement(root, "filename").text = PurePosixPath(image.file_name).name
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(image.width)
    ET.SubElement(size, "height").text = str(image.height)
    ET.SubElement(size, "depth").text = "3"
    ET.SubElement(root, "segmented").text = (
        "1" if any(obj.segmentation is not None for obj in image.objects) else "0"
    )
    for item in image.objects:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = item.category
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = "0"
        ET.SubElement(obj, "difficult").text = "0"
        x, y, width, height = item.bbox
        box = ET.SubElement(obj, "bndbox")
        ET.SubElement(box, "xmin").text = str(math.floor(x))
        ET.SubElement(box, "ymin").text = str(math.floor(y))
        ET.SubElement(box, "xmax").text = str(math.ceil(x + width))
        ET.SubElement(box, "ymax").text = str(math.ceil(y + height))
    _indent_xml(root)
    return ET.ElementTree(root)


def write_coco(
    dataset: AnnotationDataset, output_file: Path | str, *, overwrite: bool = False
) -> Path:
    """Write deterministic UTF-8 COCO JSON without overwriting by default."""
    output = Path(output_file)
    if output.exists() and not overwrite:
        raise AnnotationExportError("COCO output already exists.")
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(build_coco(dataset), ensure_ascii=False, indent=2) + "\n"
    output.write_text(payload, encoding="utf-8", newline="\n")
    return output


def write_voc(
    dataset: AnnotationDataset, output_directory: Path | str, *, overwrite: bool = False
) -> tuple[Path, ...]:
    """Write one XML file per image while preserving relative subdirectories."""
    output = Path(output_directory)
    targets = [
        output / PurePosixPath(item.file_name).with_suffix(".xml")
        for item in dataset.images
    ]
    existing = [target for target in targets if target.exists()]
    if existing and not overwrite:
        raise AnnotationExportError("Pascal VOC output already exists.")
    output.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for item, target in zip(dataset.images, targets):
        target.parent.mkdir(parents=True, exist_ok=True)
        build_voc_xml(item).write(
            target, encoding="utf-8", xml_declaration=True, short_empty_elements=True
        )
        written.append(target)
    return tuple(written)
