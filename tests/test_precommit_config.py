"""Test verifying pre-commit, flake8, and formatting configuration."""

import os
from pathlib import Path
import configparser

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore


def test_precommit_config_exists_and_valid():
    repo_root = Path(__file__).resolve().parent.parent
    precommit_path = repo_root / ".pre-commit-config.yaml"
    assert precommit_path.exists(), ".pre-commit-config.yaml should exist in repo root"

    content = precommit_path.read_text(encoding="utf-8")
    assert "repo: https://github.com/psf/black" in content
    assert "repo: https://github.com/pycqa/flake8" in content
    assert "repo: https://github.com/pycqa/isort" in content


def test_flake8_config_matches_style():
    repo_root = Path(__file__).resolve().parent.parent
    flake8_path = repo_root / ".flake8"
    assert flake8_path.exists(), ".flake8 config should exist"

    config = configparser.ConfigParser()
    config.read(flake8_path)
    assert config.has_section("flake8")
    assert config.get("flake8", "max-line-length") == "88"


def test_pyproject_toml_has_black_and_isort():
    repo_root = Path(__file__).resolve().parent.parent
    pyproject_path = repo_root / "pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml should exist"

    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    assert "black" in data.get("tool", {})
    assert "isort" in data.get("tool", {})
    assert data["tool"]["black"]["line-length"] == 88
    assert data["tool"]["isort"]["profile"] == "black"
