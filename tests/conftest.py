"""Shared test configuration for explicit, non-production test capabilities."""

import hashlib
import json
import os
import pytest


TEST_API_KEYS = {
    hashlib.sha256(b"test-free-key").hexdigest(): "free",
    hashlib.sha256(b"test-pro-key").hexdigest(): "pro",
    hashlib.sha256(b"test-courier-pro-key").hexdigest(): "pro",
}
os.environ["VERISLIP_API_KEY_HASHES"] = json.dumps(TEST_API_KEYS)
os.environ.pop("REDIS_URL", None)


@pytest.fixture(autouse=True)
def enable_internal_synthetic_generator(monkeypatch):
    """Enable internal synthetic data only for the lifetime of each test."""
    monkeypatch.setenv("VERISLIP_ENABLE_SYNTHETIC_GENERATOR", "1")
