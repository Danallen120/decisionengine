"""Rule data loading at the I/O edge (REQ-RULES-002 AC-03/AC-04)."""

import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from decision_engine.core import Jurisdiction
from decision_engine.rules_loader import (
    RuleLoadError,
    default_registry,
    load_registry,
    load_rule_data,
)

from .conftest import split_evenly

SRC = Path(__file__).parents[1] / "src" / "decision_engine"

RULE_YAML = """\
jurisdiction: CA
version: 0.0.1
effective_from: 2026-01-01
parameters:
  - name: test_threshold
    kind: money
    value: "1000.00"
    description: A test-only dollar threshold with no legal meaning.
    citations: ["Test Code § 1"]
"""


def _write(directory, text=RULE_YAML, name="ca-0.0.1.yaml"):
    path = directory / name
    path.write_text(text)
    return path


def test_loads_valid_rule_data_with_unquoted_dates(tmp_path):
    data = load_rule_data(_write(tmp_path))
    assert data.jurisdiction is Jurisdiction.CA
    assert data.effective_from.isoformat() == "2026-01-01"


def test_unquoted_decimal_money_is_rejected(tmp_path):
    with pytest.raises(ValidationError):
        load_rule_data(_write(tmp_path, RULE_YAML.replace('"1000.00"', "1000.00")))


def test_python_object_tags_are_refused(tmp_path):
    payload = "!!python/object/apply:os.system ['echo pwned']\n"
    with pytest.raises(Exception, match="could not determine a constructor"):
        load_rule_data(_write(tmp_path, payload))


def test_oversized_file_is_rejected(tmp_path):
    path = _write(tmp_path, RULE_YAML + "#" * 1_000_001)
    with pytest.raises(RuleLoadError, match="exceeds"):
        load_rule_data(path)


def test_registry_pairs_data_with_logic(tmp_path):
    _write(tmp_path)
    registry = load_registry(tmp_path, {(Jurisdiction.CA, "0.0.1"): split_evenly})
    assert len(registry.registry_hash) == 64


def test_data_without_logic_is_rejected(tmp_path):
    _write(tmp_path)
    with pytest.raises(RuleLoadError, match="no rule logic"):
        load_registry(tmp_path, {})


def test_logic_without_data_is_rejected(tmp_path):
    with pytest.raises(RuleLoadError, match="without rule data"):
        load_registry(tmp_path, {(Jurisdiction.WA, "0.0.1"): split_evenly})


def test_default_registry_loads_packaged_rules():
    assert len(default_registry().registry_hash) == 64


def test_source_never_uses_unsafe_yaml_loaders():
    for path in SRC.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Attribute) and node.attr in {
                "unsafe_load",
                "full_load",
                "FullLoader",
                "UnsafeLoader",
                "Loader",
            }:
                pytest.fail(f"{path.name}:{node.lineno} uses yaml.{node.attr}")
