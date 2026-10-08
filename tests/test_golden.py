"""REQ-TEST-001: golden scenarios are the test suite."""

from pathlib import Path

import pytest

from decision_engine.golden import Scenario, load_scenarios, render_markdown, run_scenario
from decision_engine.rules_loader import default_policy, default_registry

from .conftest import TEST_CITATION, account_payload, facts_payload

GOLDEN_DIR = Path(__file__).parents[1] / "golden"
SCENARIOS = load_scenarios(GOLDEN_DIR)
REGISTRY = default_registry()
BASELINE = default_policy()


@pytest.mark.parametrize("scenario", SCENARIOS, ids=[s.id for s in SCENARIOS])
def test_golden_scenario(scenario):
    expected, actual = run_scenario(scenario, REGISTRY, BASELINE)
    assert actual == expected


def test_golden_suite_is_not_empty():
    assert SCENARIOS


def _scenario_yaml(
    scenario_id="GS-GEN-901",
    expected="outcome: not_determinable\n    reasons: [unsupported_jurisdiction]",
):
    return f"""\
- id: {scenario_id}
  title: A test scenario used only by the runner's own tests.
  facts:
    jurisdiction: TX
    date_of_death: "2026-01-15"
    as_of_date: "2026-03-01"
    account:
      account_type: sole
      balance: "1.00"
      requires_multiple_signatures: false
      restraining_order_served: false
      withdrawal_notice_received: false
      ownership_instrument_issued: false
    estate:
      administration: none
      declared_value: null
      has_real_property_in_jurisdiction: null
    parties: []
  expected:
    {expected}
"""


def test_duplicate_ids_across_files_are_rejected(tmp_path):
    (tmp_path / "a.yaml").write_text(_scenario_yaml())
    (tmp_path / "b.yaml").write_text(_scenario_yaml())
    with pytest.raises(ValueError, match="duplicate"):
        load_scenarios(tmp_path)


def test_malformed_expected_decision_fails_loudly(tmp_path):
    (tmp_path / "a.yaml").write_text(_scenario_yaml(expected="outcome: determined"))
    (scenario,) = load_scenarios(tmp_path)
    with pytest.raises(ValueError, match="determination"):
        scenario.expected_comparable()


def test_mismatch_is_detected(tmp_path):
    (tmp_path / "a.yaml").write_text(
        _scenario_yaml(
            expected="outcome: not_determinable\n    reasons: [no_rule_set_for_date_of_death]"
        ),
    )
    (scenario,) = load_scenarios(tmp_path)
    expected, actual = run_scenario(scenario, REGISTRY, BASELINE)
    assert expected != actual


def test_render_lists_payees_and_citations():
    determined = Scenario.model_validate(
        {
            "id": "GS-TEST-001",
            "title": "Determined scenario used only to test rendering.",
            "facts": facts_payload() | {"date_of_death": "2026-01-15"},
            "expected": {
                "outcome": "determined",
                "determination": {
                    "payment": {
                        "form": "shares",
                        "payees": [
                            {"party_id": "P1", "share": "1/1", "citations": [TEST_CITATION]}
                        ],
                    },
                    "required_documents": [
                        {"code": "DEATH_CERTIFICATE", "citations": ["Doc Code § 2"]}
                    ],
                    "release_date": {"earliest": "2026-03-01", "citations": [TEST_CITATION]},
                    "liability_protection": {"applies": True, "citations": [TEST_CITATION]},
                },
                "rule_set": {"jurisdiction": "CA", "version": "0.0.1"},
            },
        },
        strict=False,
    )
    table = render_markdown([determined])
    assert "Pay P1 1/1" in table
    assert "Doc Code § 2; Test Code § 1" in table
    assert "P1 surviving_spouse" in table


def test_render_describes_any_of_payment_and_holders():
    facts = facts_payload(
        account=account_payload(
            account_type="joint",
            holders=[
                {"party_id": "P1", "role": "co_owner", "survived_decedent": True},
                {"party_id": "P2", "role": "co_owner", "survived_decedent": False},
            ],
        ),
    )
    scenario = Scenario.model_validate(
        {
            "id": "GS-TEST-002",
            "title": "Any-of scenario used only to test rendering.",
            "facts": facts,
            "expected": {
                "outcome": "determined",
                "determination": {
                    "payment": {
                        "form": "any_of",
                        "party_ids": ["P1", "P2"],
                        "citations": [TEST_CITATION],
                    },
                    "required_documents": [],
                    "release_date": {"earliest": "2026-03-01", "citations": [TEST_CITATION]},
                    "liability_protection": {"applies": True, "citations": [TEST_CITATION]},
                },
                "rule_set": {"jurisdiction": "CA", "version": "0.0.1"},
            },
        },
        strict=False,
    )
    table = render_markdown([scenario])
    assert "Payable to any of P1, P2" in table
    assert "P2 co_owner (predeceased)" in table
    assert "Test Code § 1" in table


def test_render_shows_terms_shares():
    facts = facts_payload(
        account=account_payload(
            account_type="payable_on_death",
            holders=[
                {
                    "party_id": "P1",
                    "role": "pod_payee",
                    "survived_decedent": True,
                    "terms_share": "7/10",
                },
                {
                    "party_id": "P2",
                    "role": "pod_payee",
                    "survived_decedent": True,
                    "terms_share": "3/10",
                },
            ],
        ),
        jurisdiction="TX",
    )
    scenario = Scenario.model_validate(
        {
            "id": "GS-TEST-003",
            "title": "Terms-share scenario used only to test rendering.",
            "facts": facts,
            "expected": {"outcome": "not_determinable", "reasons": ["unsupported_jurisdiction"]},
        },
        strict=False,
    )
    assert "P1 pod_payee 7/10 by terms" in render_markdown([scenario])
