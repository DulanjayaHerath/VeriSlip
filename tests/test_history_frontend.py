"""Static checks for the history drawer where no browser test harness exists."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_history_drawer_contains_accessible_states_and_filters():
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert 'id="history-drawer"' in html
    assert 'aria-labelledby="history-title"' in html
    assert 'id="history-reference"' in html
    assert 'id="history-date-from"' in html
    assert 'id="history-date-to"' in html
    assert 'id="history-status" role="status"' in html


def test_history_frontend_uses_authenticated_api_and_safe_rendering():
    javascript = (ROOT / "web" / "js" / "app.js").read_text(encoding="utf-8")
    assert 'headers.set("X-API-Key", apiKey)' in javascript
    assert "/api/v1/verifications/history" in javascript
    assert "No verification history yet." in javascript
    assert "No verification records match these filters." in javascript
    assert "ref.textContent = item.reference_no" in javascript
    assert "historyList.innerHTML" not in javascript
