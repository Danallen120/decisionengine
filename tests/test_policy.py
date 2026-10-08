"""REQ-POLICY-001: institution policy can only make decisions stricter."""

import json
from datetime import timedelta

import pytest
from pydantic import ValidationError

from decision_engine.core import (
    DocumentSource,
    InstitutionPolicy,
    Outcome,
    ReasonCode,
    evaluate,
)
from decision_engine.rules_loader import default_policy, load_policy

from .conftest import BASELINE, account_payload, make_facts, make_policy

BANK_FORM = {"code": "BANK_CLAIM_FORM", "description": "The institution's own claim form, signed."}


def test_baseline_policy_adds_nothing(registry):
    decision = evaluate(make_facts(), registry, BASELINE)
    assert decision.determination is not None
    assert decision.determination.release_date.policy_days_added == 0
    sources = {d.source for d in decision.determination.required_documents}
    assert sources == {DocumentSource.STATUTE}


def test_policy_adds_waiting_days(registry):
    base = evaluate(make_facts(), registry, BASELINE).determination
    stricter = evaluate(
        make_facts(), registry, make_policy(additional_waiting_days=10)
    ).determination
    assert base is not None
    assert stricter is not None
    assert stricter.release_date.earliest == base.release_date.earliest + timedelta(days=10)
    assert stricter.release_date.policy_days_added == 10
    assert stricter.release_date.citations == base.release_date.citations


def test_policy_adds_documents_after_statutory_ones(registry):
    policy = make_policy(additional_documents=[BANK_FORM])
    determination = evaluate(make_facts(), registry, policy).determination
    assert determination is not None
    codes = [(d.code, d.source) for d in determination.required_documents]
    assert codes == [
        ("DEATH_CERTIFICATE", DocumentSource.STATUTE),
        ("BANK_CLAIM_FORM", DocumentSource.POLICY),
    ]


def test_policy_document_already_required_by_statute_is_not_duplicated(registry):
    duplicate = {"code": "DEATH_CERTIFICATE", "description": "A death certificate, per policy."}
    determination = evaluate(
        make_facts(), registry, make_policy(additional_documents=[duplicate])
    ).determination
    assert determination is not None
    assert [d.code for d in determination.required_documents] == ["DEATH_CERTIFICATE"]
    assert determination.required_documents[0].source is DocumentSource.STATUTE


def test_policy_can_decline_account_types(registry):
    decision = evaluate(make_facts(), registry, make_policy(declined_account_types=["sole"]))
    assert decision.outcome is Outcome.NOT_DETERMINABLE
    assert decision.reasons == (ReasonCode.POLICY_DECLINED,)
    assert decision.rule_set is not None


@pytest.mark.parametrize(("balance", "declined"), [("12500.00", False), ("12500.01", True)])
def test_policy_can_decline_balances_above_a_limit(registry, balance, declined):
    facts = make_facts(account=account_payload(balance=balance))
    decision = evaluate(facts, registry, make_policy(decline_balance_above="12500.00"))
    assert (decision.reasons == (ReasonCode.POLICY_DECLINED,)) is declined


def test_unsupported_jurisdiction_takes_precedence_over_policy(registry):
    policy = make_policy(declined_account_types=["sole"])
    decision = evaluate(make_facts(jurisdiction="TX"), registry, policy)
    assert decision.reasons == (ReasonCode.UNSUPPORTED_JURISDICTION,)


def test_every_decision_records_the_policy(registry):
    policy = make_policy(additional_waiting_days=3)
    for facts in (make_facts(), make_facts(jurisdiction="TX")):
        decision = evaluate(facts, registry, policy)
        assert decision.policy == policy.ref()


@pytest.mark.parametrize(
    "override",
    [
        {"additional_waiting_days": -1},
        {"additional_waiting_days": 3651},
        {"additional_documents": [BANK_FORM, BANK_FORM]},
        {"declined_account_types": ["sole", "sole"]},
        {"decline_balance_above": 100.0},
        {"institution": "Test Bank"},
        {"waive_waiting_period": True},
        {"description": "short"},
    ],
)
def test_invalid_or_relaxing_policies_are_rejected(override):
    with pytest.raises(ValidationError):
        make_policy(**override)


def test_policy_has_no_field_that_could_relax_the_law():
    """Guards the design: only additive or declining knobs exist."""
    assert set(InstitutionPolicy.model_fields) == {
        "schema_version",
        "institution",
        "version",
        "description",
        "additional_waiting_days",
        "additional_documents",
        "declined_account_types",
        "decline_balance_above",
    }


def test_policy_hash_ignores_formatting_and_tracks_meaning():
    a = make_policy(additional_waiting_days=5)
    reordered = json.dumps(dict(reversed(list(a.model_dump(mode="json").items()))), indent=2)
    assert InstitutionPolicy.model_validate_json(reordered).content_hash() == a.content_hash()
    assert make_policy(additional_waiting_days=6).content_hash() != a.content_hash()


def test_packaged_baseline_policy_adds_nothing():
    policy = default_policy()
    assert policy.institution == "baseline"
    assert policy.additional_waiting_days == 0
    assert policy.additional_documents == ()
    assert policy.declined_account_types == ()
    assert policy.decline_balance_above is None


def test_policy_files_load_from_yaml(tmp_path):
    path = tmp_path / "bank.yaml"
    path.write_text(
        "institution: example-bank\n"
        "version: 2.1.0\n"
        "description: Example institution policy used only in tests.\n"
        "additional_waiting_days: 5\n"
        'decline_balance_above: "50000.00"\n',
    )
    policy = load_policy(path)
    assert policy.ref().institution == "example-bank"
    assert str(policy.decline_balance_above) == "50000.00"
