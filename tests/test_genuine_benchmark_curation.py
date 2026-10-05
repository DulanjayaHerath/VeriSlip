import json
from io import BytesIO

from PIL import Image

from core.datasets.curation import (
    CurationError,
    curate_candidate,
    curation_status,
    finalize_integrity,
)
from core.privacy.pii_redaction import PIIRegion, RedactionResult
from scripts import curate_genuine_benchmark


def _png():
    stream = BytesIO()
    Image.new("RGB", (30, 20), "white").save(stream, "PNG")
    return stream.getvalue()


def _metadata(**updates):
    value = {
        "bank_category": "commercial",
        "source_type": "team_transaction",
        "os_family": "android",
        "capture_type": "screenshot",
        "permission_status": "granted",
        "permission_record_id": "consent-00000001",
    }
    value.update(updates)
    return value


class FakeRedactor:
    def redact(self, image, *, method="mask"):
        image = image.copy()
        image.paste("black", (1, 1, 8, 8))
        return RedactionResult(image, (PIIRegion("account_number", (1, 1, 8, 8)),))


def test_candidate_is_sanitized_redacted_and_stored_under_generated_name(tmp_path):
    record = curate_candidate(_png(), _metadata(), tmp_path, redactor=FakeRedactor())
    assert record["sample_id"].startswith("sample-")
    assert record["image_path"] == f"{record['sample_id']}.png"
    with Image.open(tmp_path / record["image_path"]) as image:
        assert image.getpixel((2, 2)) == (0, 0, 0)
        assert not image.info
    saved = json.loads((tmp_path / "curation_metadata.jsonl").read_text())
    assert saved["permission_record_id"] == "consent-00000001"


def test_permission_is_required_and_duplicate_evidence_is_rejected(tmp_path):
    try:
        curate_candidate(_png(), _metadata(permission_status="pending"), tmp_path, redactor=FakeRedactor())
    except CurationError:
        pass
    else:
        raise AssertionError("pending permission must be rejected")
    curate_candidate(_png(), _metadata(), tmp_path, redactor=FakeRedactor())
    try:
        curate_candidate(_png(), _metadata(), tmp_path, redactor=FakeRedactor())
    except CurationError:
        pass
    else:
        raise AssertionError("duplicate permission record must be rejected")


def test_integrity_and_status_are_derived_from_actual_files(tmp_path):
    curate_candidate(_png(), _metadata(os_family="ios"), tmp_path, redactor=FakeRedactor())
    manifest = finalize_integrity(tmp_path)
    assert len(manifest["files"]) == 1
    assert curation_status(tmp_path) == {
        "permission_cleared_samples": 1,
        "target_samples": 200,
        "remaining_to_target": 199,
        "by_os_family": {"android": 0, "ios": 1, "other": 0},
    }


def test_cli_status_empty_dataset_reports_zero_without_fabrication(tmp_path, capsys):
    assert curate_genuine_benchmark.main(["status", str(tmp_path)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["permission_cleared_samples"] == 0
    assert output["remaining_to_target"] == 200


def test_malformed_metadata_fails_without_echoing_sensitive_value(tmp_path):
    secret = "0771234567"
    try:
        curate_candidate(_png(), _metadata(permission_record_id=secret), tmp_path, redactor=FakeRedactor())
    except CurationError as exc:
        assert secret not in str(exc)
    else:
        raise AssertionError("unsafe metadata must be rejected")
