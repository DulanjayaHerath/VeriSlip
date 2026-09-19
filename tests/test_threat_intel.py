"""Tests for the STIX 2.1 and TAXII 2.1 threat-intelligence feed."""

from fastapi.testclient import TestClient

from api.main import app
from core.threat_intel.stix_exporter import build_stix_bundle

try:  # pragma: no cover - optional library for validation
    from stix2.validator import validate_instance
except Exception:  # pragma: no cover - library may not be installed in all environments
    validate_instance = None

client = TestClient(app)


def test_stix_bundle_is_valid_stix_21():
    bundle = build_stix_bundle()
    assert bundle["type"] == "bundle"
    assert bundle["spec_version"] == "2.1"
    assert bundle["objects"]
    if validate_instance is not None:
        assert validate_instance(bundle) is None


def test_taxii_collection_endpoint_exposes_feed():
    response = client.get("/taxii2/collections/verislip-fraud-indicators/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "Collection"
    assert payload["spec_version"] == "2.1"
    assert payload["name"] == "VeriSlip Fraud Indicators"
    assert payload["objects"]


def test_taxii_objects_endpoint_returns_stix_bundle():
    response = client.get("/taxii2/collections/verislip-fraud-indicators/objects/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["type"] == "bundle"
    assert payload["spec_version"] == "2.1"
    if validate_instance is not None:
        assert validate_instance(payload) is None
