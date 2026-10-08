"""REQ-RULES-001 (selection, fail closed) and REQ-RULES-002 (integrity, hashing)."""

import json
from datetime import date

import pytest
from pydantic import ValidationError

from decision_engine.core import (
    Jurisdiction,
    ReasonCode,
    RuleRegistry,
    RuleRegistryError,
    RuleSet,
    RuleSetData,
)

from .conftest import TEST_CITATION, rule_data, split_evenly

PARAMETER = {
    "name": "test_threshold",
    "description": "A test-only dollar threshold with no legal meaning.",
    "citations": [TEST_CITATION],
    "kind": "money",
    "value": "1000.00",
}


def _data_payload(**overrides):
    payload = {
        "jurisdiction": "CA",
        "version": "1.2.3",
        "effective_from": "2026-01-01",
        "effective_through": None,
        "parameters": [PARAMETER],
    }
    payload.update(overrides)
    return payload


def _data(**overrides):
    return RuleSetData.model_validate_json(json.dumps(_data_payload(**overrides)))


def _registry(*data):
    return RuleRegistry([RuleSet(data=d, logic=split_evenly) for d in data])


# ── Selection ───────────────────────────────────────────


@pytest.mark.parametrize(
    ("date_of_death", "expected_version"),
    [
        (date(2025, 1, 1), "0.0.1"),
        (date(2025, 12, 31), "0.0.1"),
        (date(2026, 1, 1), "0.0.2"),
        (date(2030, 6, 1), "0.0.2"),
    ],
)
def test_selects_the_one_covering_rule_set_at_boundaries(date_of_death, expected_version):
    registry = _registry(
        rule_data(
            version="0.0.1", effective_from=date(2025, 1, 1), effective_through=date(2025, 12, 31)
        ),
        rule_data(version="0.0.2", effective_from=date(2026, 1, 1)),
    )
    selected = registry.select(Jurisdiction.CA, date_of_death)
    assert isinstance(selected, RuleSet)
    assert selected.data.version == expected_version


def test_jurisdiction_without_rule_sets_is_unsupported():
    registry = _registry(rule_data())
    assert registry.select(Jurisdiction.TX, date(2026, 6, 1)) is ReasonCode.UNSUPPORTED_JURISDICTION


def test_date_outside_every_range_has_no_rule_set():
    registry = _registry(
        rule_data(effective_from=date(2025, 1, 1), effective_through=date(2025, 12, 31)),
    )
    for date_of_death in (date(2024, 12, 31), date(2026, 1, 1)):
        assert (
            registry.select(Jurisdiction.CA, date_of_death)
            is ReasonCode.NO_RULE_SET_FOR_DATE_OF_DEATH
        )


def test_empty_registry_supports_nothing():
    assert (
        RuleRegistry([]).select(Jurisdiction.CA, date(2026, 1, 1))
        is ReasonCode.UNSUPPORTED_JURISDICTION
    )


def test_overlapping_ranges_fail_at_load():
    with pytest.raises(RuleRegistryError, match="overlapping"):
        _registry(
            rule_data(
                version="0.0.1", effective_from=date(2025, 1, 1), effective_through=date(2026, 1, 1)
            ),
            rule_data(version="0.0.2", effective_from=date(2026, 1, 1)),
        )


def test_open_ended_range_followed_by_another_overlaps():
    with pytest.raises(RuleRegistryError, match="overlapping"):
        _registry(
            rule_data(version="0.0.1", effective_from=date(2025, 1, 1)),
            rule_data(version="0.0.2", effective_from=date(2026, 1, 1)),
        )


def test_duplicate_versions_fail_at_load():
    with pytest.raises(RuleRegistryError, match="duplicate"):
        _registry(
            rule_data(
                version="0.0.1",
                effective_from=date(2025, 1, 1),
                effective_through=date(2025, 6, 30),
            ),
            rule_data(version="0.0.1", effective_from=date(2026, 1, 1)),
        )


def test_same_dates_in_different_jurisdictions_do_not_overlap():
    registry = _registry(rule_data(Jurisdiction.CA), rule_data(Jurisdiction.WA))
    assert isinstance(registry.select(Jurisdiction.WA, date(2026, 2, 1)), RuleSet)


# ── Rule data validation ────────────────────────────────


def test_effective_through_before_from_is_rejected():
    with pytest.raises(ValidationError, match="effective_through"):
        _data(effective_through="2025-12-31")


def test_parameter_without_citation_is_rejected():
    with pytest.raises(ValidationError):
        _data(parameters=[{**PARAMETER, "citations": []}])


def test_parameter_with_unknown_key_is_rejected():
    with pytest.raises(ValidationError):
        _data(parameters=[{**PARAMETER, "note": "x"}])


def test_duplicate_parameter_names_are_rejected():
    with pytest.raises(ValidationError, match="unique"):
        _data(parameters=[PARAMETER, PARAMETER])


@pytest.mark.parametrize(
    "parameter",
    [
        {**PARAMETER, "value": 1000.0},
        {**PARAMETER, "kind": "days", "value": -1},
        {**PARAMETER, "kind": "date", "value": "not-a-date"},
        {**PARAMETER, "kind": "percent"},
    ],
)
def test_parameter_values_are_strictly_typed(parameter):
    with pytest.raises(ValidationError):
        _data(parameters=[parameter])


def test_all_parameter_kinds_are_accepted():
    data = _data(
        parameters=[
            PARAMETER,
            {**PARAMETER, "name": "test_wait", "kind": "days", "value": 40},
            {**PARAMETER, "name": "test_cutover", "kind": "date", "value": "2026-04-01"},
        ],
    )
    assert [p.kind for p in data.parameters] == ["money", "days", "date"]


# ── Hashing ─────────────────────────────────────────────


def test_hash_ignores_key_order_and_formatting():
    payload = _data_payload()
    reordered = dict(reversed(list(payload.items())))
    a = RuleSetData.model_validate_json(json.dumps(payload))
    b = RuleSetData.model_validate_json(json.dumps(reordered, indent=4))
    assert a.content_hash() == b.content_hash()


def test_equal_money_written_differently_hashes_the_same():
    a = _data(parameters=[{**PARAMETER, "value": "1000"}])
    b = _data(parameters=[{**PARAMETER, "value": "1000.00"}])
    assert a.content_hash() == b.content_hash()


@pytest.mark.parametrize(
    "change",
    [
        {"version": "1.2.4"},
        {"effective_from": "2026-01-02"},
        {"parameters": [{**PARAMETER, "value": "1000.01"}]},
        {"parameters": [{**PARAMETER, "citations": ["Test Code § 2"]}]},
    ],
)
def test_any_semantic_change_changes_the_hash(change):
    assert _data(**change).content_hash() != _data().content_hash()


def test_registry_hash_is_stable_and_sensitive():
    first = _registry(rule_data(Jurisdiction.CA), rule_data(Jurisdiction.WA))
    same = _registry(rule_data(Jurisdiction.WA), rule_data(Jurisdiction.CA))
    different = _registry(rule_data(Jurisdiction.CA))
    assert first.registry_hash == same.registry_hash
    assert first.registry_hash != different.registry_hash
