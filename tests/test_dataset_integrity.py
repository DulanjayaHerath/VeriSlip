"""Tests for deterministic, read-only dataset integrity manifests."""

from __future__ import annotations

import hashlib
import io
import json

import pytest
from PIL import Image

from core.datasets.integrity import (
    DatasetIntegrityError,
    build_manifest,
    compute_sha256,
    verify_dataset,
    write_manifest,
)
from scripts.verify_dataset import main


def _image(path, *, color="white", image_format="PNG", size=(24, 16)):
    Image.new("RGB", size, color).save(path, format=image_format)
    return path


class _BoundedReader(io.BytesIO):
    def __init__(self, value: bytes, maximum: int):
        super().__init__(value)
        self.maximum = maximum

    def read(self, size=-1):
        assert 0 < size <= self.maximum
        return super().read(size)


def test_sha256_is_correct_and_uses_chunked_reads():
    payload = b"VeriSlip integrity" * 100
    stream = _BoundedReader(payload, maximum=13)
    assert compute_sha256(stream, chunk_size=13) == hashlib.sha256(payload).hexdigest()


def test_valid_image_manifest_contains_non_sensitive_metadata(tmp_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    _image(dataset / "sample.png", size=(31, 17))
    manifest = build_manifest(dataset)
    assert manifest["schema_version"] == 1
    assert manifest["hash_algorithm"] == "sha256"
    assert manifest["files"] == [
        {
            "path": "sample.png",
            "sha256": compute_sha256(dataset / "sample.png"),
            "size_bytes": (dataset / "sample.png").stat().st_size,
            "width": 31,
            "height": 17,
            "format": "PNG",
        }
    ]
    assert str(tmp_path) not in json.dumps(manifest)


def test_corrupt_image_is_detected_without_modification(tmp_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    corrupt = dataset / "broken.png"
    corrupt.write_bytes(b"not a real image")
    before = corrupt.read_bytes()
    with pytest.raises(DatasetIntegrityError) as exc_info:
        build_manifest(dataset)
    assert exc_info.value.issues[0].code == "corrupt_file"
    assert exc_info.value.issues[0].path == "broken.png"
    assert corrupt.read_bytes() == before


def test_failed_creation_does_not_write_or_replace_manifest(tmp_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    (dataset / "unsupported.png").write_bytes(b"invalid image content")
    manifest = tmp_path / "manifest.json"
    manifest.write_text("existing manifest", encoding="utf-8")
    assert main(["create", str(dataset), str(manifest)]) == 1
    assert manifest.read_text(encoding="utf-8") == "existing manifest"


def test_manifest_round_trip_verifies_unchanged_nested_dataset(tmp_path):
    dataset = tmp_path / "dataset"
    nested = dataset / "train" / "images"
    nested.mkdir(parents=True)
    _image(nested / "b.png", color="blue")
    _image(dataset / "a.jpg", color="red", image_format="JPEG")
    manifest_path = tmp_path / "integrity.json"
    manifest = build_manifest(dataset)
    write_manifest(manifest, manifest_path)
    result = verify_dataset(dataset, manifest_path)
    assert result.ok
    assert result.files_checked == 2
    assert [entry["path"] for entry in manifest["files"]] == [
        "a.jpg",
        "train/images/b.png",
    ]


def test_manifest_output_is_deterministic(tmp_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    _image(dataset / "z.png", color="black")
    _image(dataset / "A.png", color="green")
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    write_manifest(build_manifest(dataset), first)
    write_manifest(build_manifest(dataset), second)
    assert first.read_bytes() == second.read_bytes()


def test_modified_image_reports_checksum_mismatch(tmp_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    image = _image(dataset / "sample.png", color="white")
    manifest = build_manifest(dataset)
    _image(image, color="black")
    result = verify_dataset(dataset, manifest)
    assert not result.ok
    assert "checksum_mismatch" in {issue.code for issue in result.issues}


def test_missing_and_unexpected_images_are_reported(tmp_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    original = _image(dataset / "expected.png")
    manifest = build_manifest(dataset)
    original.unlink()
    _image(dataset / "new.png")
    result = verify_dataset(dataset, manifest)
    assert {(issue.code, issue.path) for issue in result.issues} == {
        ("missing_file", "expected.png"),
        ("unexpected_file", "new.png"),
    }


def test_file_corrupted_after_manifest_is_reported(tmp_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    image = _image(dataset / "sample.png")
    manifest = build_manifest(dataset)
    image.write_bytes(b"truncated")
    result = verify_dataset(dataset, manifest)
    assert [(issue.code, issue.path) for issue in result.issues] == [
        ("corrupt_file", "sample.png")
    ]


def test_duplicate_content_is_reported_deterministically(tmp_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    first = _image(dataset / "a.png", color="purple")
    (dataset / "nested").mkdir()
    second = dataset / "nested" / "copy.png"
    second.write_bytes(first.read_bytes())
    manifest = build_manifest(dataset)
    assert manifest["duplicates"] == [
        {
            "sha256": compute_sha256(first),
            "paths": ["a.png", "nested/copy.png"],
        }
    ]
    result = verify_dataset(dataset, manifest)
    assert result.ok
    assert result.duplicates == (("a.png", "nested/copy.png"),)


def test_empty_dataset_is_valid(tmp_path):
    dataset = tmp_path / "empty"
    dataset.mkdir()
    manifest = build_manifest(dataset)
    assert manifest["files"] == []
    assert manifest["duplicates"] == []
    assert verify_dataset(dataset, manifest).ok


@pytest.mark.parametrize(
    "manifest",
    [
        "not json",
        json.dumps([]),
        json.dumps({"schema_version": 99, "hash_algorithm": "sha256", "files": []}),
        json.dumps({"schema_version": 1, "hash_algorithm": "md5", "files": []}),
    ],
)
def test_malformed_manifest_is_a_safe_verification_failure(tmp_path, manifest):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(manifest, encoding="utf-8")
    result = verify_dataset(dataset, manifest_path)
    assert not result.ok
    assert result.issues[0].code == "malformed_manifest"
    assert str(tmp_path) not in result.issues[0].message


def test_unsupported_non_image_files_are_ignored(tmp_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    (dataset / "notes.txt").write_text("metadata", encoding="utf-8")
    Image.new("RGB", (10, 10)).save(dataset / "animation.gif", format="GIF")
    assert build_manifest(dataset)["files"] == []


@pytest.mark.parametrize(
    "unsafe_path",
    ["../outside.png", "/tmp/outside.png", "C:/outside.png", "nested\\image.png"],
)
def test_suspicious_manifest_paths_are_rejected(tmp_path, unsafe_path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    manifest = {
        "schema_version": 1,
        "hash_algorithm": "sha256",
        "files": [
            {
                "path": unsafe_path,
                "sha256": "0" * 64,
                "size_bytes": 1,
                "width": 1,
                "height": 1,
                "format": "PNG",
            }
        ],
    }
    result = verify_dataset(dataset, manifest)
    assert result.issues[0].code == "malformed_manifest"


def test_symlinked_image_is_refused_when_supported(tmp_path):
    dataset = tmp_path / "dataset"
    outside = tmp_path / "outside.png"
    dataset.mkdir()
    _image(outside)
    link = dataset / "linked.png"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks are unavailable")
    with pytest.raises(DatasetIntegrityError) as exc_info:
        build_manifest(dataset)
    assert exc_info.value.issues[0].code == "unsafe_path"


def test_cli_create_and_verify_success_exit_codes(tmp_path, capsys):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    _image(dataset / "sample.png")
    manifest = tmp_path / "manifest.json"
    assert main(["create", str(dataset), str(manifest)]) == 0
    assert main(["verify", str(dataset), str(manifest)]) == 0
    output = capsys.readouterr().out
    assert "Manifest created: 1 images" in output
    assert "Verification succeeded: 1 images" in output


def test_cli_failure_exit_code_identifies_relative_path(tmp_path, capsys):
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    image = _image(dataset / "sample.png")
    manifest = tmp_path / "manifest.json"
    assert main(["create", str(dataset), str(manifest)]) == 0
    image.write_bytes(b"corrupt")
    assert main(["verify", str(dataset), str(manifest)]) == 1
    output = capsys.readouterr().out
    assert "[corrupt_file] sample.png" in output
    assert str(tmp_path) not in output
