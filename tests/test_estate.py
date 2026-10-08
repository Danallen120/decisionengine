"""REQ-CORE-005: small-estate facts (affiants, estate value, real property, administration)."""

import json
from decimal import Decimal

import pytest
from pydantic import ValidationError

from decision_engine.core import AdministrationStatus, AffiantCapacity, Facts

from .conftest import estate_payload, facts_payload

PARTIES = [
    {"party_id": "P1", "relationship": "child"},
    {"party_id": "P2", "relationship": "child"},
    {"party_id": "P3", "relationship": "representative"},
    {"party_id": "P4", "relationship": "trust"},
]


def _parse(affiants=(), parties=PARTIES, **estate):
    payload = facts_payload(
        parties=parties,
        estate=estate_payload(affiants=list(affiants), **estate),
    )
    return Facts.model_validate_json(json.dumps(payload))


def _successor(party_id):
    return {"party_id": party_id, "capacity": "successor"}


def _representative(party_id, on_behalf_of, capacity="guardian_or_conservator"):
    return {"party_id": party_id, "capacity": capacity, "on_behalf_of": on_behalf_of}


def test_successors_and_representatives_parse():
    facts = _parse([_successor("P1"), _representative("P3", "P2")])
    capacities = [a.capacity for a in facts.estate.affiants]
    assert capacities == [AffiantCapacity.SUCCESSOR, AffiantCapacity.GUARDIAN_OR_CONSERVATOR]


def test_trustee_signs_for_a_trust():
    facts = _parse([_representative("P3", "P4", capacity="trustee")])
    assert facts.estate.affiants[0].on_behalf_of == "P4"


@pytest.mark.parametrize(
    ("affiants", "message"),
    [
        ([_successor("P9")], "must be listed in parties"),
        ([_successor("P1"), _successor("P1")], "only once"),
        ([_successor("P4")], "trust signs only through a trustee"),
        ([_successor("P3")], "representative party must sign in a representative capacity"),
        ([{"party_id": "P3", "capacity": "attorney_in_fact"}], "on_behalf_of is required"),
        ([{**_successor("P1"), "on_behalf_of": "P2"}], "not allowed for a successor"),
        ([_representative("P3", "P3")], "act for another listed party"),
        ([_representative("P3", "P9")], "act for another listed party"),
    ],
)
def test_invalid_affiants_are_rejected(affiants, message):
    with pytest.raises(ValidationError, match=message):
        _parse(affiants)


def test_unknown_values_stay_null_and_are_not_defaulted():
    facts = _parse(declared_value=None, has_real_property_in_jurisdiction=None)
    assert facts.estate.declared_value is None
    assert facts.estate.has_real_property_in_jurisdiction is None


def test_declared_value_is_money():
    assert _parse(declared_value="184500").estate.declared_value == Decimal("184500.00")
    with pytest.raises(ValidationError):
        _parse(declared_value=184500.0)


@pytest.mark.parametrize(
    "missing", ["administration", "declared_value", "has_real_property_in_jurisdiction"]
)
def test_estate_facts_must_be_stated_even_when_unknown(missing):
    estate = estate_payload()
    del estate[missing]
    with pytest.raises(ValidationError):
        Facts.model_validate_json(json.dumps(facts_payload(estate=estate)))


def test_administration_status_has_three_states():
    assert {s.value for s in AdministrationStatus} == {
        "none",
        "opened_with_representative_consent",
        "opened_without_consent",
    }
    with pytest.raises(ValidationError):
        _parse(administration="opened")


def test_old_probate_flag_is_rejected():
    with pytest.raises(ValidationError):
        Facts.model_validate_json(json.dumps(facts_payload(probate_opened=False)))
