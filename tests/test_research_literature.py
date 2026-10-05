"""Consistency checks for the issue #93 research bibliography."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "docs" / "research" / "RELATED_WORK.md"
BIBLIOGRAPHY = ROOT / "docs" / "research" / "references.bib"


def test_every_review_citation_resolves_to_one_bibliography_entry():
    review = REVIEW.read_text(encoding="utf-8")
    bibliography = BIBLIOGRAPHY.read_text(encoding="utf-8")
    cited = set(re.findall(r"@([a-zA-Z0-9_-]+)", review))
    entries = re.findall(r"^@[a-zA-Z]+\{([^,]+),", bibliography, re.MULTILINE)

    assert cited
    assert len(entries) == len(set(entries)), "duplicate BibTeX keys"
    assert cited == set(entries), "unused or unresolved bibliography entries"


def test_bibliography_has_unique_persistent_identifiers_and_safe_links():
    bibliography = BIBLIOGRAPHY.read_text(encoding="utf-8")
    dois = [value.lower() for value in re.findall(r"doi\s*=\s*\{([^}]+)\}", bibliography)]
    urls = re.findall(r"url\s*=\s*\{([^}]+)\}", bibliography)

    assert len(dois) == len(set(dois)), "duplicate DOI"
    assert len(dois) >= 10
    assert len(urls) >= 13
    assert all(url.startswith("https://") for url in urls)


def test_review_distinguishes_evidence_from_verislip_claims():
    review = REVIEW.read_text(encoding="utf-8")
    normalized = " ".join(review.split())

    assert "not evidence that VeriSlip has reproduced" in normalized
    assert "not a calibrated detector" in normalized
    assert "does **not** currently claim PRNU" in normalized
    assert "demo values must not be reported as empirical performance" in normalized
