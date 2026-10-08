"""REQ-CORE-002: decision schema invariants."""

import json
from datetime import date

import pytest
from pydantic import ValidationError

from decision_engine.core import (
    Decision,
    Determination,
    DocumentSource,
    LiabilityProtection,
    Outcome,
    ReasonCode,
    ReleaseDate,
    RequiredDocument,
    canonical_json,
)

from .conftest import TEST_CITATION

HASH = "a" * 64
REF = {"jurisdiction": "CA", "version": "0.0.1", "content_hash": HASH}
POLICY = {"institution": "baseline", "version": "1.0.0", "content_hash": HASH}


def _payee(party_id, share, citations=(TEST_CITATION,)):
    return {"party_id": party_id, "share": share, "citations": list(citations)}


def _determination(payment, documents=()):
    return {
        "payment": payment,
        "required_documents": list(documents),
        "release_date": {"earliest": "2026-03-01", "citations": [TEST_CITATION]},
        "liability_protection": {"applies": True, "citations": [TEST_CITATION]},
    }


def _shares(*payees):
    return {"form": "shares", "payees": list(payees)}


def _decide(determination, **extra):
    payload = {
        "outcome": "determined",
        "determination": determination,
        "rule_set": REF,
        "policy": POLICY,
        "registry_hash": HASH,
        **extra,
    }
    return Decision.model_validate_json(json.dumps(payload))


def _determined(*payees):
    return _decide(_determination(_shares(*payees)))


def _not_determinable(**overrides):
    payload = {
        "outcome": "not_determinable",
        "reasons": ["unsupported_jurisdiction"],
        "policy": POLICY,
        "registry_hash": HASH,
        **overrides,
    }
    return Decision.model_validate_json(json.dumps(payload))


# ── Shares payment ──────────────────────────────────────


def test_shares_summing_to_one_are_accepted():
    decision = _determined(_payee("P1", "1/3"), _payee("P2", "2/3"))
    assert decision.outcome is Outcome.DETERMINED


@pytest.mark.parametrize(
    "shares",
    [["1/3", "1/3"], ["1/2", "2/3"], ["1/3", "1/3", "1/3", "1/3"]],
)
def test_shares_not_summing_to_one_are_rejected(shares):
    payees = [_payee(f"P{i}", s) for i, s in enumerate(shares, start=1)]
    with pytest.raises(ValidationError, match="sum to exactly 1"):
        _determined(*payees)


def test_duplicate_payees_are_rejected():
    with pytest.raises(ValidationError, match="only once"):
        _determined(_payee("P1", "1/2"), _payee("P1", "1/2"))


# ── Any-of payment (joint accounts) ─────────────────────


def test_any_of_payment_lists_parties_and_citations():
    payment = {"form": "any_of", "party_ids": ["P1", "P2"], "citations": [TEST_CITATION]}
    decision = _decide(_determination(payment))
    assert decision.determination is not None
    assert decision.determination.payment.form == "any_of"


@pytest.mark.parametrize(
    "payment",
    [
        {"form": "any_of", "party_ids": ["P1"], "citations": [TEST_CITATION]},
        {"form": "any_of", "party_ids": ["P1", "P1"], "citations": [TEST_CITATION]},
        {"form": "any_of", "party_ids": ["P1", "P2"], "citations": []},
        {"form": "split", "party_ids": ["P1", "P2"], "citations": [TEST_CITATION]},
    ],
)
def test_invalid_any_of_payment_is_rejected(payment):
    with pytest.raises(ValidationError):
        _decide(_determination(payment))


# ── Documents, dates, protection ────────────────────────


def test_conclusions_without_citations_are_rejected():
    with pytest.raises(ValidationError):
        _determined(_payee("P1", "1/1", citations=()))
    with pytest.raises(ValidationError):
        ReleaseDate(earliest=date(2026, 1, 1), citations=())
    with pytest.raises(ValidationError):
        LiabilityProtection(applies=False, citations=())


def test_statutory_documents_need_citations():
    with pytest.raises(ValidationError, match="statutory document"):
        RequiredDocument(code="DEATH_CERTIFICATE")


def test_policy_documents_carry_no_citation():
    document = RequiredDocument(code="BANK_FORM", source=DocumentSource.POLICY)
    assert document.citations == ()
    with pytest.raises(ValidationError, match="policy document"):
        RequiredDocument(code="BANK_FORM", source=DocumentSource.POLICY, citations=(TEST_CITATION,))


def test_duplicate_document_codes_are_rejected():
    document = {"code": "DEATH_CERTIFICATE", "citations": [TEST_CITATION]}
    with pytest.raises(ValidationError, match="only once"):
        _decide(_determination(_shares(_payee("P1", "1/1")), documents=[document, document]))


def test_release_date_policy_days_cannot_be_negative():
    with pytest.raises(ValidationError):
        ReleaseDate(earliest=date(2026, 1, 1), citations=(TEST_CITATION,), policy_days_added=-1)


# ── Outcome invariants ──────────────────────────────────


def test_determined_requires_rule_set():
    payload = {
        "outcome": "determined",
        "determination": _determination(_shares(_payee("P1", "1/1"))),
        "policy": POLICY,
        "registry_hash": HASH,
    }
    with pytest.raises(ValidationError, match="rule set"):
        Decision.model_validate_json(json.dumps(payload))


def test_determined_rejects_reasons():
    with pytest.raises(ValidationError):
        _decide(
            _determination(_shares(_payee("P1", "1/1"))),
            reasons=["fact_pattern_not_covered"],
        )


def test_not_determinable_requires_reasons_and_no_determination():
    with pytest.raises(ValidationError):
        _not_determinable(reasons=[])
    with pytest.raises(ValidationError):
        _not_determinable(determination=_determination(_shares(_payee("P1", "1/1"))))


@pytest.mark.parametrize("missing", ["policy", "registry_hash"])
def test_decision_requires_policy_and_registry_hash(missing):
    payload = {
        "outcome": "not_determinable",
        "reasons": ["unsupported_jurisdiction"],
        "policy": POLICY,
        "registry_hash": HASH,
    }
    del payload[missing]
    with pytest.raises(ValidationError):
        Decision.model_validate_json(json.dumps(payload))


@pytest.mark.parametrize("bad_hash", ["A" * 64, "a" * 63, "g" * 64])
def test_hashes_must_be_lowercase_sha256_hex(bad_hash):
    with pytest.raises(ValidationError):
        _not_determinable(registry_hash=bad_hash)
    with pytest.raises(ValidationError):
        _not_determinable(policy={**POLICY, "content_hash": bad_hash})


def test_reason_codes_include_policy_declined():
    decision = _not_determinable(reasons=["policy_declined"])
    assert decision.reasons == (ReasonCode.POLICY_DECLINED,)


def test_canonical_json_round_trips_byte_identically():
    decision = _determined(_payee("P1", "1/3"), _payee("P2", "2/3"))
    text = canonical_json(decision)
    again = Decision.model_validate_json(text)
    assert canonical_json(again) == text
    assert '"share":"1/3"' in text
    assert ": " not in text


def test_determination_is_frozen():
    determination = Determination.model_validate_json(
        json.dumps(_determination(_shares(_payee("P1", "1/1")))),
    )
    with pytest.raises(ValidationError):
        determination.required_documents = ()  # type: ignore[misc]
