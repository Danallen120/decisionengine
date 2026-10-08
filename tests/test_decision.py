"""REQ-CORE-002: decision schema invariants."""

import json
from datetime import date

import pytest
from pydantic import ValidationError

from decision_engine.core import (
    Decision,
    Determination,
    LiabilityProtection,
    Outcome,
    ReasonCode,
    ReleaseDate,
    canonical_json,
)

from .conftest import TEST_CITATION

HASH = "a" * 64
REF = {"jurisdiction": "CA", "version": "0.0.1", "content_hash": HASH}


def _payee(party_id, share, citations=(TEST_CITATION,)):
    return {"party_id": party_id, "share": share, "citations": list(citations)}


def _determination(payees):
    return {
        "payees": payees,
        "required_documents": [],
        "release_date": {"earliest": "2026-03-01", "citations": [TEST_CITATION]},
        "liability_protection": {"applies": True, "citations": [TEST_CITATION]},
    }


def _determined(payees):
    payload = {
        "outcome": "determined",
        "determination": _determination(payees),
        "rule_set": REF,
        "registry_hash": HASH,
    }
    return Decision.model_validate_json(json.dumps(payload))


def test_shares_summing_to_one_are_accepted():
    decision = _determined([_payee("P1", "1/3"), _payee("P2", "2/3")])
    assert decision.outcome is Outcome.DETERMINED


@pytest.mark.parametrize(
    "shares",
    [["1/3", "1/3"], ["1/2", "2/3"], ["1/3", "1/3", "1/3", "1/3"]],
)
def test_shares_not_summing_to_one_are_rejected(shares):
    payees = [_payee(f"P{i}", s) for i, s in enumerate(shares, start=1)]
    with pytest.raises(ValidationError, match="sum to exactly 1"):
        _determined(payees)


def test_duplicate_payees_are_rejected():
    with pytest.raises(ValidationError, match="only once"):
        _determined([_payee("P1", "1/2"), _payee("P1", "1/2")])


def test_conclusions_without_citations_are_rejected():
    with pytest.raises(ValidationError):
        _determined([_payee("P1", "1/1", citations=())])
    with pytest.raises(ValidationError):
        ReleaseDate(earliest=date(2026, 1, 1), citations=())
    with pytest.raises(ValidationError):
        LiabilityProtection(applies=False, citations=())


def test_determined_requires_rule_set():
    payload = {
        "outcome": "determined",
        "determination": _determination([_payee("P1", "1/1")]),
        "registry_hash": HASH,
    }
    with pytest.raises(ValidationError, match="rule set"):
        Decision.model_validate_json(json.dumps(payload))


def test_determined_rejects_reasons():
    determination = Determination.model_validate_json(
        json.dumps(_determination([_payee("P1", "1/1")])),
    )
    with pytest.raises(ValidationError):
        Decision.model_validate(
            {
                "outcome": Outcome.DETERMINED,
                "reasons": (ReasonCode.FACT_PATTERN_NOT_COVERED,),
                "determination": determination,
                "rule_set": REF,
                "registry_hash": HASH,
            },
        )


def test_not_determinable_requires_reasons_and_no_determination():
    with pytest.raises(ValidationError):
        Decision(outcome=Outcome.NOT_DETERMINABLE, registry_hash=HASH)
    determination = Determination.model_validate_json(
        json.dumps(_determination([_payee("P1", "1/1")])),
    )
    with pytest.raises(ValidationError):
        Decision(
            outcome=Outcome.NOT_DETERMINABLE,
            reasons=(ReasonCode.UNSUPPORTED_JURISDICTION,),
            determination=determination,
            registry_hash=HASH,
        )


def test_decision_requires_registry_hash():
    with pytest.raises(ValidationError):
        Decision(outcome=Outcome.NOT_DETERMINABLE, reasons=(ReasonCode.UNSUPPORTED_JURISDICTION,))  # type: ignore[call-arg]


@pytest.mark.parametrize("bad_hash", ["A" * 64, "a" * 63, "g" * 64])
def test_hashes_must_be_lowercase_sha256_hex(bad_hash):
    with pytest.raises(ValidationError):
        Decision(
            outcome=Outcome.NOT_DETERMINABLE,
            reasons=(ReasonCode.UNSUPPORTED_JURISDICTION,),
            registry_hash=bad_hash,
        )


def test_canonical_json_round_trips_byte_identically():
    decision = _determined([_payee("P1", "1/3"), _payee("P2", "2/3")])
    text = canonical_json(decision)
    again = Decision.model_validate_json(text)
    assert canonical_json(again) == text
    assert '"share":"1/3"' in text
    assert ": " not in text
