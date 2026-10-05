"""Guardrails for the issue #97 IEEE conference draft."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper" / "main.tex"
BIB = ROOT / "paper" / "references.bib"
CHECKLIST = ROOT / "paper" / "SUBMISSION_CHECKLIST.md"


def test_draft_uses_ieee_structure_and_is_anonymous():
    source = PAPER.read_text(encoding="utf-8")

    assert "\\documentclass[conference]{IEEEtran}" in source
    assert "Anonymous Authors" in source
    for section in (
        "Introduction",
        "Related Work",
        "Problem Formulation and Threat Model",
        "Methodology",
        "Evaluation Protocol",
        "Discussion",
        "Conclusion",
    ):
        assert f"\\section{{{section}}}" in source


def test_draft_does_not_present_demo_values_as_results():
    source = " ".join(PAPER.read_text(encoding="utf-8").split())

    assert "\\pending" in source
    assert "Empirical values are deliberately omitted" in source
    assert "deterministic demonstration values" in source
    assert "not experimental observations" in source
    assert re.search(r"(?<![\d.])0\.98(?!\d)", source) is None
    assert re.search(r"(?<![\d.])0\.93(?!\d)", source) is None


def test_citations_resolve_and_bibliography_identifiers_are_unique():
    source = PAPER.read_text(encoding="utf-8")
    bibliography = BIB.read_text(encoding="utf-8")
    cited = set()
    for group in re.findall(r"\\cite\{([^}]+)\}", source):
        cited.update(key.strip() for key in group.split(","))
    entries = re.findall(r"^@[a-zA-Z]+\{([^,]+),", bibliography, re.MULTILINE)
    dois = [value.lower() for value in re.findall(r"doi\s*=\s*\{([^}]+)\}", bibliography)]

    assert cited == set(entries)
    assert len(entries) == len(set(entries))
    assert len(dois) == len(set(dois))


def test_submission_checklist_records_verified_and_unverified_venue_rules():
    checklist = " ".join(CHECKLIST.read_text(encoding="utf-8").split())

    assert "maximum six printed A4 pages including references" in checklist
    assert "double-blind initial manuscript" in checklist
    assert "dates have passed" in checklist
    assert "No current ICTer rule is asserted" in checklist
    assert "not submission-ready" in checklist
