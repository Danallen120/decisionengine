"""Shared fixtures. Rule sets here are test-only and encode no real law."""

import json
from datetime import date
from typing import Any

import pytest

from decision_engine.core import (
    Determination,
    Facts,
    Jurisdiction,
    LiabilityProtection,
    NotDeterminable,
    Payee,
    ReasonCode,
    ReleaseDate,
    RequiredDocument,
    RuleRegistry,
    RuleSet,
    RuleSetData,
)
from decision_engine.core.decision import RuleResult

TEST_CITATION = "Test Code § 1"


def facts_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "jurisdiction": "CA",
        "date_of_death": "2026-01-15",
        "as_of_date": "2026-03-01",
        "account": {"ownership": "sole", "balance": "12500.00"},
        "probate_opened": False,
        "parties": [
            {"party_id": "P1", "relationship": "surviving_spouse"},
            {"party_id": "P2", "relationship": "child"},
        ],
    }
    payload.update(overrides)
    return payload


def make_facts(**overrides: Any) -> Facts:
    return Facts.model_validate_json(json.dumps(facts_payload(**overrides)))


def split_evenly(facts: Facts, data: RuleSetData) -> RuleResult:
    """Test-only logic: split evenly among all parties, or not determinable if none."""
    del data
    if not facts.parties:
        return NotDeterminable(reasons=(ReasonCode.FACT_PATTERN_NOT_COVERED,))
    count = len(facts.parties)
    shares = ["1/1"] if count == 1 else [f"1/{count}"] * count
    payees = tuple(
        Payee.model_validate({"party_id": p.party_id, "share": s, "citations": (TEST_CITATION,)})
        for p, s in zip(facts.parties, shares, strict=True)
    )
    return Determination(
        payees=payees,
        required_documents=(
            RequiredDocument(code="DEATH_CERTIFICATE", citations=(TEST_CITATION,)),
        ),
        release_date=ReleaseDate(earliest=facts.as_of_date, citations=(TEST_CITATION,)),
        liability_protection=LiabilityProtection(applies=True, citations=(TEST_CITATION,)),
    )


def rule_data(
    jurisdiction: Jurisdiction = Jurisdiction.CA,
    version: str = "0.0.1",
    effective_from: date = date(2026, 1, 1),
    effective_through: date | None = None,
) -> RuleSetData:
    return RuleSetData(
        jurisdiction=jurisdiction,
        version=version,
        effective_from=effective_from,
        effective_through=effective_through,
        parameters=(),
    )


@pytest.fixture
def registry() -> RuleRegistry:
    return RuleRegistry([RuleSet(data=rule_data(), logic=split_evenly)])
