"""Static integration checks for merchant triage keyboard controls."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_triage_buttons_remain_accessible_and_show_shortcuts():
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert 'id="btn-triage-approve" aria-keyshortcuts="Space"' in html
    assert 'id="btn-triage-flag" aria-keyshortcuts="X"' in html
    assert "✓ Accept" in html and "✕ Flag" in html
    assert '/static/js/triage_shortcuts.js' in html


def test_app_uses_one_cleanup_capable_shortcut_controller():
    javascript = (ROOT / "web" / "js" / "app.js").read_text(encoding="utf-8")
    assert javascript.count("VeriSlipTriageShortcuts.install") == 1
    assert 'window.addEventListener("pagehide", cleanupTriageShortcuts' in javascript
    assert "btnTriageApprove.addEventListener(\"click\"" in javascript
    assert "btnTriageFlag.addEventListener(\"click\"" in javascript
