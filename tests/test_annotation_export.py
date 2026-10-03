"""Tests for deterministic COCO and Pascal VOC dataset exports."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

from core.datasets.annotations import (
    AnnotationExportError,
    build_coco,
    build_voc_xml,
    load_annotation_dataset,
    normalize_generator_annotation,
    write_coco,
    write_voc,
)
from core.internal.synthetic_slip_generator import SyntheticSlipGenerator

FIELDS = [
    "image_id",
    "split",
    "filename",
    "mask_filename",
    "bank_code",
    "is_tampered",
    "tamper_type",
    "bbox_x",
    "bbox_y",
    "bbox_w",
    "bbox_h",
]


def _row(
    filename: str,
    *,
    tamper_type: str = "ALTER_AMOUNT",
    bbox: tuple[object, object, object, object] = (10, 12, 30, 20),
    mask_filename: str = "",
    is_tampered: object = 1,
) -> dict[str, object]:
    return {
        "image_id": Path(filename).stem,
        "split": "train",
        "filename": filename,
        "mask_filename": mask_filename,
        "bank_code": "COMBANK",
        "is_tampered": is_tampered,
        "tamper_type": tamper_type,
        "bbox_x": bbox[0],
        "bbox_y": bbox[1],
        "bbox_w": bbox[2],
        "bbox_h": bbox[3],
    }


def _dataset(tmp_path: Path, rows: list[dict[str, object]]) -> Path:
    root = tmp_path / "dataset"
    root.mkdir(parents=True)
    for row in rows:
        image_path = root.joinpath(*str(row["filename"]).replace("\\", "/").split("/"))
        image_path.parent.mkdir(parents=True, exist_ok=True)
        if not image_path.exists():
            Image.new("RGB", (100, 80), "white").save(image_path)
        mask_name = str(row.get("mask_filename", ""))
        if mask_name:
            mask_path = root.joinpath(*mask_name.replace("\\", "/").split("/"))
            mask_path.parent.mkdir(parents=True, exist_ok=True)
            mask = Image.new("L", (100, 80), 0)
            x, y, width, height = (int(float(value)) for value in row_bbox(row))
            ImageDraw.Draw(mask).rectangle(
                (x, y, x + width - 1, y + height - 1), fill=255
            )
            mask.save(mask_path)
    _write_metadata(root, rows)
    return root


def row_bbox(row: dict[str, object]) -> tuple[object, object, object, object]:
    return row["bbox_x"], row["bbox_y"], row["bbox_w"], row["bbox_h"]


def _write_metadata(root: Path, rows: list[dict[str, object]]) -> None:
    with (root / "dataset_metadata.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_basic_coco_export_has_correct_bbox_dimensions_and_stable_ids(tmp_path):
    rows = [
        _row("train/images/b.png", tamper_type="ALTER_REFERENCE", bbox=(2, 3, 8, 9)),
        _row("train/images/a.png", tamper_type="ALTER_AMOUNT", bbox=(10, 12, 30, 20)),
    ]
    dataset = load_annotation_dataset(_dataset(tmp_path, rows))
    coco = build_coco(dataset)

    assert coco["images"] == [
        {"id": 1, "file_name": "train/images/a.png", "width": 100, "height": 80},
        {"id": 2, "file_name": "train/images/b.png", "width": 100, "height": 80},
    ]
    assert coco["categories"] == [
        {"id": 1, "name": "ALTER_AMOUNT", "supercategory": "tampering"},
        {"id": 2, "name": "ALTER_REFERENCE", "supercategory": "tampering"},
    ]
    assert coco["annotations"][0] == {
        "id": 1,
        "image_id": 1,
        "category_id": 1,
        "bbox": [10, 12, 30, 20],
        "area": 600,
        "iscrowd": 0,
    }
    assert [item["id"] for item in coco["annotations"]] == [1, 2]


def test_pascal_voc_export_has_expected_coordinates_and_valid_xml(tmp_path):
    dataset = load_annotation_dataset(
        _dataset(tmp_path, [_row("train/images/slip.png", bbox=(1.2, 2.8, 10.1, 11.1))])
    )
    tree = build_voc_xml(dataset.images[0])
    xml_bytes = ET.tostring(tree.getroot(), encoding="utf-8")
    parsed = ET.fromstring(xml_bytes)

    assert parsed.findtext("filename") == "slip.png"
    assert parsed.findtext("size/width") == "100"
    assert parsed.findtext("size/height") == "80"
    assert parsed.findtext("object/name") == "ALTER_AMOUNT"
    assert [
        parsed.findtext(f"object/bndbox/{name}")
        for name in ("xmin", "ymin", "xmax", "ymax")
    ] == [
        "1",
        "2",
        "12",
        "14",
    ]


def test_multiple_annotations_and_authentic_image(tmp_path):
    rows = [
        _row("a.png", tamper_type="ALTER_REFERENCE", bbox=(1, 2, 3, 4)),
        _row("a.png", tamper_type="ALTER_AMOUNT", bbox=(10, 20, 30, 40)),
        _row("b.png", tamper_type="NONE", bbox=(-1, -1, -1, -1), is_tampered=0),
    ]
    coco = build_coco(load_annotation_dataset(_dataset(tmp_path, rows)))
    assert len(coco["images"]) == 2
    assert len(coco["annotations"]) == 2
    assert [item["category_id"] for item in coco["annotations"]] == [1, 2]


def test_bbox_is_clipped_but_invalid_boxes_fail(tmp_path):
    clipped = load_annotation_dataset(
        _dataset(tmp_path, [_row("clipped.png", bbox=(-5, 70, 20, 20))])
    )
    assert build_coco(clipped)["annotations"][0]["bbox"] == [0, 70, 15, 10]

    for index, bbox in enumerate(((1, 2, 0, 4), (1, 2, -2, 4), (200, 2, 5, 5))):
        root = tmp_path / f"bad_{index}"
        with pytest.raises(AnnotationExportError):
            load_annotation_dataset(_dataset(root, [_row("bad.png", bbox=bbox)]))


@pytest.mark.parametrize(
    "row_update",
    [
        {"bbox_x": "not-a-number"},
        {"bbox_w": "nan"},
        {"is_tampered": "maybe"},
        {"tamper_type": "NONE"},
    ],
)
def test_malformed_annotation_metadata_fails_safely(tmp_path, row_update):
    row = _row("bad.png")
    row.update(row_update)
    with pytest.raises(AnnotationExportError):
        load_annotation_dataset(_dataset(tmp_path, [row]))


def test_empty_dataset_produces_valid_empty_outputs(tmp_path):
    root = tmp_path / "empty"
    root.mkdir()
    _write_metadata(root, [])
    dataset = load_annotation_dataset(root)
    assert build_coco(dataset) == {"images": [], "annotations": [], "categories": []}
    voc_output = tmp_path / "voc"
    assert write_voc(dataset, voc_output) == ()
    assert voc_output.is_dir()


def test_missing_columns_and_mismatched_mask_are_rejected(tmp_path):
    malformed = tmp_path / "malformed"
    malformed.mkdir()
    (malformed / "dataset_metadata.csv").write_text(
        "filename,is_tampered\nslip.png,1\n", encoding="utf-8"
    )
    with pytest.raises(AnnotationExportError, match="missing required"):
        load_annotation_dataset(malformed)

    row = _row("slip.png", mask_filename="mask.png")
    root = _dataset(tmp_path / "mask", [row])
    Image.new("L", (10, 10), 255).save(root / "mask.png")
    with pytest.raises(AnnotationExportError, match="dimensions"):
        load_annotation_dataset(root)


def test_unicode_nested_filename_is_preserved_safely(tmp_path):
    dataset = load_annotation_dataset(
        _dataset(tmp_path, [_row("train/images/සිංහල_ரசீது.png")])
    )
    output = tmp_path / "voc"
    files = write_voc(dataset, output)
    assert files == (output / "train/images/සිංහල_ரசீது.xml",)
    assert ET.parse(files[0]).findtext("filename") == "සිංහල_ரசீது.png"


def test_real_binary_mask_is_exported_as_coco_rle(tmp_path):
    row = _row(
        "train/images/slip.png",
        bbox=(10, 12, 30, 20),
        mask_filename="train/masks/slip.png",
    )
    coco = build_coco(load_annotation_dataset(_dataset(tmp_path, [row])))
    segmentation = coco["annotations"][0]["segmentation"]
    assert segmentation["size"] == [80, 100]
    assert sum(segmentation["counts"]) == 8000
    assert sum(segmentation["counts"][1::2]) == 600
    assert len(segmentation["counts"]) > 1


def test_deterministic_json_independent_of_csv_row_order(tmp_path):
    rows = [_row("b.png", tamper_type="ALTER_REFERENCE"), _row("a.png")]
    first = _dataset(tmp_path / "first", rows)
    second = _dataset(tmp_path / "second", list(reversed(rows)))
    first_output = write_coco(load_annotation_dataset(first), tmp_path / "first.json")
    second_output = write_coco(
        load_annotation_dataset(second), tmp_path / "second.json"
    )
    assert first_output.read_text(encoding="utf-8") == second_output.read_text(
        encoding="utf-8"
    )
    json.loads(first_output.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "filename", ["../outside.png", "C:\\outside.png", "/tmp/outside.png"]
)
def test_unsafe_source_paths_are_rejected(tmp_path, filename):
    root = tmp_path / "dataset"
    root.mkdir()
    _write_metadata(root, [_row(filename)])
    with pytest.raises(AnnotationExportError, match="safe relative path"):
        load_annotation_dataset(root)


def test_generator_native_metadata_integration():
    generator = SyntheticSlipGenerator(width=400, height=700)
    authentic, metadata = generator.generate_authentic_slip(
        bank_code="COMBANK", amount_lkr=5000
    )
    _, tampered = generator.generate_tampered_slip(
        authentic, metadata, tamper_type="ALTER_AMOUNT", new_amount=50000
    )
    mask = Image.new("L", authentic.size, 0)
    draw = ImageDraw.Draw(mask)
    for entry in tampered["ground_truth_boxes"]:
        x, y, width, height = entry["box"]
        draw.rectangle((x, y, x + width - 1, y + height - 1), fill=255)

    coco = build_coco(
        normalize_generator_annotation(
            "train/images/generated.png", authentic.size, tampered, mask
        )
    )
    expected = tampered["ground_truth_boxes"][0]["box"]
    assert coco["annotations"][0]["bbox"] == expected
    assert coco["categories"][0]["name"] == "ALTER_AMOUNT"
    assert "segmentation" in coco["annotations"][0]


def test_cli_success_failure_and_no_overwrite(tmp_path):
    root = _dataset(tmp_path, [_row("train/images/slip.png")])
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "scripts" / "export_annotations.py"
    output = tmp_path / "exports"
    command = [
        sys.executable,
        str(script),
        str(root),
        "--format",
        "both",
        "--output",
        str(output),
    ]
    success = subprocess.run(
        command, cwd=repo_root, capture_output=True, text=True, check=False
    )
    assert success.returncode == 0
    assert "Exported 1 images and 1 annotations" in success.stdout
    assert json.loads((output / "annotations.json").read_text(encoding="utf-8"))
    assert ET.parse(output / "voc/train/images/slip.xml").getroot().tag == "annotation"

    repeated = subprocess.run(
        command, cwd=repo_root, capture_output=True, text=True, check=False
    )
    assert repeated.returncode == 1
    assert "already exists" in repeated.stderr
    missing = subprocess.run(
        [
            sys.executable,
            str(script),
            str(tmp_path / "missing"),
            "--format",
            "coco",
            "--output",
            str(tmp_path / "bad.json"),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert missing.returncode == 1
