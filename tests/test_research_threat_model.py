"""Completeness checks for the issue #94 research threat model."""

from pathlib import Path


DOCUMENT = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "research"
    / "THREAT_MODEL.md"
)


def _normalized_document() -> str:
    return " ".join(DOCUMENT.read_text(encoding="utf-8").split())


def test_threat_model_contains_formal_observation_and_decision_model():
    text = _normalized_document()

    for expression in ("X = M_\\theta(G;R)", "Y=T_\\phi(X)+\\epsilon", "s=f(e)"):
        assert expression in text
    for verdict in ("authentic", "suspicious", "high-risk", "inconclusive"):
        assert verdict in text


def test_threat_model_covers_actors_attacks_and_trust_boundaries():
    text = _normalized_document().lower()

    for actor in ("novice", "intermediate", "expert"):
        assert actor in text
    for attack in (
        "amount substitution",
        "account-number substitution",
        "copy--move",
        "inpainting",
        "recompression",
        "screen recapture",
        "print--scan",
        "replay",
    ):
        assert attack in text
    assert "ocr boundary" in text
    assert "external-provider boundary" in text


def test_threat_model_has_explicit_non_guarantees_and_privacy_controls():
    text = _normalized_document()

    assert "does not permit" in text
    assert "does not imply authenticity" in text
    assert "Raw images and full OCR/PII values are not written to routine logs" in text
    assert "does not permit \"authentic\" to mean" not in text
    assert "repository unit tests or demo benchmark values establish field accuracy" in text
