"""REQ-CORE-001: fact schema."""

import json
import re

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from decision_engine.core import Facts

from .conftest import facts_payload, make_facts

PII_FIELD_PATTERN = re.compile(
    r"name|ssn|tin|tax|social|account_?(number|no|num)|routing|address|street|zip|postal|"
    r"birth|dob|phone|email",
    re.IGNORECASE,
)


def _parse(payload):
    return Facts.model_validate_json(json.dumps(payload))


def test_valid_facts_parse_and_are_frozen():
    facts = make_facts()
    assert facts.schema_version == "1"
    with pytest.raises(ValidationError):
        facts.probate_opened = True  # type: ignore[misc]


@pytest.mark.parametrize("field", ["name", "ssn", "account_number", "address", "notes"])
def test_unknown_fields_are_rejected(field):
    with pytest.raises(ValidationError) as excinfo:
        _parse(facts_payload(**{field: "x"}))
    assert excinfo.value.errors()[0]["type"] == "extra_forbidden"


def test_unknown_nested_field_is_rejected():
    payload = facts_payload(account={"ownership": "sole", "balance": "1.00", "number": "123"})
    with pytest.raises(ValidationError):
        _parse(payload)


@pytest.mark.parametrize("balance", [12500.0, 12500, "12500.001", "-5.00"])
def test_money_must_be_a_two_place_decimal_string(balance):
    with pytest.raises(ValidationError):
        _parse(facts_payload(account={"ownership": "sole", "balance": balance}))


@pytest.mark.parametrize("value", ["true", 1, "yes"])
def test_booleans_are_not_coerced(value):
    with pytest.raises(ValidationError):
        _parse(facts_payload(probate_opened=value))


def test_as_of_date_before_death_is_rejected():
    with pytest.raises(ValidationError, match="as_of_date"):
        _parse(facts_payload(as_of_date="2026-01-14"))


def test_duplicate_party_ids_are_rejected():
    parties = [
        {"party_id": "P1", "relationship": "child"},
        {"party_id": "P1", "relationship": "child"},
    ]
    with pytest.raises(ValidationError, match="unique"):
        _parse(facts_payload(parties=parties))


@pytest.mark.parametrize("party_id", ["Alice", "P0", "P1000", "p1", ""])
def test_party_ids_are_opaque_references(party_id):
    with pytest.raises(ValidationError):
        _parse(facts_payload(parties=[{"party_id": party_id, "relationship": "child"}]))


def test_party_count_is_capped():
    parties = [{"party_id": f"P{i}", "relationship": "child"} for i in range(1, 52)]
    with pytest.raises(ValidationError):
        _parse(facts_payload(parties=parties))


def test_unknown_jurisdiction_code_is_rejected():
    with pytest.raises(ValidationError):
        _parse(facts_payload(jurisdiction="ZZ"))


def _schema_property_names(schema):
    names = set()
    for node in [schema, *schema.get("$defs", {}).values()]:
        names.update(node.get("properties", {}))
    return names


def test_schema_has_no_pii_fields():
    names = _schema_property_names(Facts.model_json_schema())
    assert names, "schema should expose properties"
    assert not [n for n in names if PII_FIELD_PATTERN.search(n)]


def test_schema_has_no_free_text_fields():
    """Every string field is an enum, a date, a money amount, or a constrained pattern."""
    schema = Facts.model_json_schema()
    for node in [schema, *schema.get("$defs", {}).values()]:
        for name, prop in node.get("properties", {}).items():
            if prop.get("type") == "string":
                assert {"enum", "pattern", "format", "const"} & prop.keys(), name


@given(
    key=st.text(min_size=1, max_size=20).filter(lambda k: k not in facts_payload()),
    value=st.one_of(st.text(max_size=20), st.integers(), st.booleans(), st.none()),
)
def test_any_extra_top_level_key_is_rejected(key, value):
    with pytest.raises(ValidationError):
        _parse(facts_payload(**{key: value}))
