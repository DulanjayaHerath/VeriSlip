"""Repository-to-methodology consistency tests for issue #95."""

from pathlib import Path

from scripts.generate_research_architecture import OUTPUT, build_svg


ROOT = Path(__file__).resolve().parents[1]
METHODOLOGY = ROOT / "docs" / "research" / "METHODOLOGY.md"


def test_architecture_figure_is_reproducible_and_accessible():
    committed = OUTPUT.read_text(encoding="utf-8")

    assert committed == build_svg()
    assert 'role="img"' in committed
    assert "<title" in committed and "<desc" in committed


def test_methodology_documents_implemented_layer_equations():
    text = " ".join(METHODOLOGY.read_text(encoding="utf-8").split())

    for marker in (
        "s_1=\\min(1",
        "s_{1.5}=\\max",
        "v_{ELA}=\\operatorname{Var}",
        "z_b=\\frac",
        "s_3=\\min",
        "s_4=0.55p+0.45m",
        "L=0.18s_1+0.225s_2+0.225s_3+0.27s_4+0.10s_v",
        "\\operatorname{IoU}(A,B)",
    ):
        assert marker in text


def test_methodology_states_critical_implementation_limitations():
    text = " ".join(METHODOLOGY.read_text(encoding="utf-8").split())

    assert "executable third channel is the Sobel gradient magnitude" in text
    assert "it is **not** PRNU camera identification" in text
    assert "has not been established here as an empirically calibrated model" in text
    assert "Repository demonstration tables and synthetic fixtures are not experimental results" in text
