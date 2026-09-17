"""Shared test configuration for explicitly authorized synthetic fixtures."""

import pytest


@pytest.fixture(autouse=True)
def enable_internal_synthetic_generator(monkeypatch):
    """Enable internal synthetic data only for the lifetime of each test."""
    monkeypatch.setenv("VERISLIP_ENABLE_SYNTHETIC_GENERATOR", "1")
