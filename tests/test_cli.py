"""REQ-CLI-001: CLI behavior, including never echoing input values."""

import io
import json
import sys

import pytest

from decision_engine import cli

from .conftest import facts_payload

SSN_LIKE_VALUE = "123-45-6789"


def _run(monkeypatch, capsys, argv, stdin=b""):
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(stdin)))
    code = cli.main(argv)
    out, err = capsys.readouterr()
    return code, out, err


def test_evaluate_file_outputs_canonical_decision(monkeypatch, capsys, tmp_path):
    path = tmp_path / "facts.json"
    path.write_text(json.dumps(facts_payload(jurisdiction="TX")))
    code, out, err = _run(monkeypatch, capsys, ["evaluate", str(path)])
    assert code == cli.EXIT_OK
    assert err == ""
    decision = json.loads(out)
    assert decision["outcome"] == "not_determinable"
    assert out == json.dumps(decision, sort_keys=True, separators=(",", ":")) + "\n"


def test_evaluate_reads_stdin(monkeypatch, capsys):
    stdin = json.dumps(facts_payload()).encode()
    code, out, _ = _run(monkeypatch, capsys, ["evaluate", "-"], stdin)
    assert code == cli.EXIT_OK
    assert json.loads(out)["schema_version"] == "1"


def test_invalid_input_reports_paths_not_values(monkeypatch, capsys):
    stdin = json.dumps(facts_payload(ssn=SSN_LIKE_VALUE, probate_opened="maybe")).encode()
    code, out, err = _run(monkeypatch, capsys, ["evaluate", "-"], stdin)
    assert code == cli.EXIT_INVALID_INPUT
    assert out == ""
    assert SSN_LIKE_VALUE not in err
    assert "maybe" not in err
    errors = json.loads(err)["errors"]
    assert {"loc": ["ssn"], "type": "extra_forbidden"} in errors


def test_batch_reports_each_item(monkeypatch, capsys):
    items = [facts_payload(), {"jurisdiction": "CA", "note": SSN_LIKE_VALUE}]
    code, out, _ = _run(monkeypatch, capsys, ["batch", "-"], json.dumps(items).encode())
    assert code == cli.EXIT_SOME_INVALID
    assert SSN_LIKE_VALUE not in out
    results = json.loads(out)
    assert results[0]["index"] == 0
    assert "decision" in results[0]
    assert results[1]["index"] == 1
    assert "errors" in results[1]


def test_batch_of_valid_items_exits_ok(monkeypatch, capsys):
    code, _, _ = _run(monkeypatch, capsys, ["batch", "-"], json.dumps([facts_payload()]).encode())
    assert code == cli.EXIT_OK


@pytest.mark.parametrize(
    ("stdin", "message"),
    [
        (b"{not json", "not valid JSON"),
        (json.dumps(facts_payload()).encode(), "must be a JSON array"),
        (json.dumps([{}] * (cli.MAX_BATCH_ITEMS + 1)).encode(), "exceeds"),
    ],
)
def test_batch_rejects_bad_envelopes_before_evaluating(monkeypatch, capsys, stdin, message):
    code, out, err = _run(monkeypatch, capsys, ["batch", "-"], stdin)
    assert code == cli.EXIT_INVALID_INPUT
    assert out == ""
    assert message in json.loads(err)["error"]


def test_oversized_input_is_rejected(monkeypatch, capsys):
    monkeypatch.setattr(cli, "MAX_INPUT_BYTES", 10)
    code, _, err = _run(monkeypatch, capsys, ["evaluate", "-"], b"x" * 11)
    assert code == cli.EXIT_INVALID_INPUT
    assert "exceeds" in err


def test_long_field_names_are_truncated_in_errors(monkeypatch, capsys):
    stdin = json.dumps(facts_payload(**{"k" * 500: 1})).encode()
    _, _, err = _run(monkeypatch, capsys, ["evaluate", "-"], stdin)
    loc = json.loads(err)["errors"][0]["loc"]
    assert len(loc[0]) == cli.MAX_LOC_PART_CHARS


def test_golden_renders_markdown(monkeypatch, capsys):
    code, out, _ = _run(monkeypatch, capsys, ["golden", "golden"])
    assert code == cli.EXIT_OK
    assert out.startswith("| ID |")
    assert "GS-GEN-001" in out
