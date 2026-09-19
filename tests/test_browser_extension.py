import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_extension_manifest_uses_manifest_v3_and_context_menu():
    manifest = json.loads((ROOT / "extension" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == 3
    assert "contextMenus" in manifest["permissions"]
    assert "activeTab" in manifest["permissions"]
    assert any(item["title"] == "Audit with VeriSlip" for item in [
        {"title": "Audit with VeriSlip", "contexts": ["image"]}
    ])


def test_browser_extension_fetches_verification_payload_and_renders_summary():
    background = (ROOT / "extension" / "background.js").read_text(encoding="utf-8")
    content = (ROOT / "extension" / "content.js").read_text(encoding="utf-8")
    sidebar = (ROOT / "extension" / "sidebar.js").read_text(encoding="utf-8")
    html = (ROOT / "extension" / "sidebar.html").read_text(encoding="utf-8")

    assert '"Audit with VeriSlip"' in background
    assert "contextMenus" in background
    assert "audit-image" in content
    assert "/api/v1/verify" in content
    assert "Risk score" in html
    assert "Open full Forensic Cockpit" in html
    assert "renderAuditResult" in sidebar
