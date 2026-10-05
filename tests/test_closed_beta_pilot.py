import csv

import pytest

from core.research.closed_beta import FIELDS, PilotDataError, analyse_pilot_csv, summarise
from scripts import analyze_closed_beta


def _row(**updates):
    row = {
        "participant_id": "seller-deadbeef",
        "pilot_day": "1",
        "event_type": "verification",
        "model_verdict": "suspicious",
        "confirmed_outcome": "genuine",
        "feedback_code": "false_alarm",
    }
    row.update(updates)
    return row


def test_summary_counts_only_confirmed_error_outcomes():
    result = summarise([
        _row(),
        _row(participant_id="seller-cafebabe", model_verdict="authentic", confirmed_outcome="fraud", feedback_code="missed_fraud"),
        _row(pilot_day="2", model_verdict="high_risk", confirmed_outcome="unconfirmed", feedback_code=""),
        _row(pilot_day="3", event_type="feedback", model_verdict="", confirmed_outcome="", feedback_code="useful"),
    ])
    assert result["participants"] == 2
    assert result["verifications"] == 3
    assert result["confirmed_verifications"] == 2
    assert result["false_positives"] == 1
    assert result["false_negatives"] == 1


@pytest.mark.parametrize("updates", [
    {"participant_id": "+94770000000"},
    {"pilot_day": "15"},
    {"model_verdict": "definitely_safe"},
    {"feedback_code": "Customer Alice said 123"},
])
def test_validation_rejects_unsafe_or_unstructured_values_without_echo(updates):
    secret = next(iter(updates.values()))
    with pytest.raises(PilotDataError) as error:
        summarise([_row(**updates)])
    assert str(secret) not in str(error.value)


def test_csv_analysis_and_cli_do_not_emit_participant_ids(tmp_path, capsys):
    path = tmp_path / "pilot.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow(_row())
    assert analyse_pilot_csv(path)["events"] == 1
    assert analyze_closed_beta.main([str(path)]) == 0
    output = capsys.readouterr().out
    assert "seller-deadbeef" not in output
    assert '"events": 1' in output


def test_invalid_header_fails_cleanly(tmp_path, capsys):
    path = tmp_path / "pilot.csv"
    path.write_text("name,phone\nAlice,0770000000\n", encoding="utf-8")
    assert analyze_closed_beta.main([str(path)]) == 2
    output = capsys.readouterr()
    assert "Alice" not in output.err
    assert "0770000000" not in output.err
