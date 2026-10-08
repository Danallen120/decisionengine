"""REQ-CORE-004: account terms in facts."""

import json

import pytest
from pydantic import ValidationError

from decision_engine.core import AccountType, Facts, HolderRole

from .conftest import account_payload, facts_payload

PARTIES = [
    {"party_id": "P1", "relationship": "child"},
    {"party_id": "P2", "relationship": "child"},
    {"party_id": "P3", "relationship": "sibling"},
]


def _holder(party_id, role, *, survived=True, share=None):
    holder = {"party_id": party_id, "role": role, "survived_decedent": survived}
    if share is not None:
        holder["terms_share"] = share
    return holder


def _parse(account_type, holders, parties=PARTIES):
    payload = facts_payload(
        account=account_payload(account_type=account_type, holders=holders),
        parties=parties,
    )
    return Facts.model_validate_json(json.dumps(payload))


@pytest.mark.parametrize(
    ("account_type", "holders"),
    [
        ("sole", []),
        ("joint", [_holder("P1", "co_owner")]),
        ("payable_on_death", [_holder("P1", "pod_payee"), _holder("P2", "pod_payee")]),
        ("payable_on_death", [_holder("P1", "co_owner"), _holder("P2", "pod_payee")]),
        ("totten_trust", [_holder("P1", "totten_beneficiary")]),
        ("totten_trust", [_holder("P3", "co_owner"), _holder("P1", "totten_beneficiary")]),
    ],
)
def test_valid_account_terms_parse(account_type, holders):
    facts = _parse(account_type, holders)
    assert facts.account.account_type is AccountType(account_type)


@pytest.mark.parametrize(
    ("account_type", "holders", "message"),
    [
        ("sole", [_holder("P1", "co_owner")], "cannot have holders"),
        ("joint", [], "needs at least one co_owner"),
        ("joint", [_holder("P1", "pod_payee")], "cannot have holders"),
        ("payable_on_death", [_holder("P1", "co_owner")], "needs at least one pod_payee"),
        ("payable_on_death", [_holder("P1", "totten_beneficiary")], "cannot have holders"),
        ("totten_trust", [_holder("P1", "pod_payee")], "cannot have holders"),
    ],
)
def test_roles_must_fit_the_account_type(account_type, holders, message):
    with pytest.raises(ValidationError, match=message):
        _parse(account_type, holders)


def test_holders_must_be_listed_parties():
    with pytest.raises(ValidationError, match="must be listed in parties"):
        _parse("joint", [_holder("P9", "co_owner")])


def test_a_party_holds_one_role_only():
    holders = [_holder("P1", "co_owner"), _holder("P1", "pod_payee")]
    with pytest.raises(ValidationError, match="only one role"):
        _parse("payable_on_death", holders)


def test_terms_shares_that_sum_to_one_are_accepted():
    holders = [_holder("P1", "pod_payee", share="7/10"), _holder("P2", "pod_payee", share="3/10")]
    facts = _parse("payable_on_death", holders)
    payees = facts.account.holders_with(HolderRole.POD_PAYEE)
    assert [h.party_id for h in payees] == ["P1", "P2"]


@pytest.mark.parametrize(
    ("holders", "message"),
    [
        (
            [_holder("P1", "pod_payee", share="1/2"), _holder("P2", "pod_payee")],
            "every payee needs one",
        ),
        (
            [_holder("P1", "pod_payee", share="1/2"), _holder("P2", "pod_payee", share="1/3")],
            "sum to exactly 1",
        ),
        (
            [_holder("P1", "co_owner", share="1/2"), _holder("P2", "pod_payee", share="1/2")],
            "only to POD payees",
        ),
    ],
)
def test_terms_shares_are_complete_and_exact(holders, message):
    with pytest.raises(ValidationError, match=message):
        _parse("payable_on_death", holders)


def test_payment_blocking_events_are_required_facts():
    account = account_payload()
    del account["restraining_order_served"]
    with pytest.raises(ValidationError):
        Facts.model_validate_json(json.dumps(facts_payload(account=account)))


def test_holder_count_is_capped():
    parties = [{"party_id": f"P{i}", "relationship": "child"} for i in range(1, 23)]
    holders = [_holder(f"P{i}", "co_owner") for i in range(1, 22)]
    with pytest.raises(ValidationError):
        _parse("joint", holders, parties=parties)
