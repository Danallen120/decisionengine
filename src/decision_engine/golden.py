"""Golden scenarios: the attorney-readable spec that is also the test suite (REQ-TEST-001).

A scenario file is YAML with a list of scenarios. Each scenario has a stable
``id``, a plain-English ``title``, ``facts``, and an ``expected`` decision
without hash or policy fields. Hashes change whenever any rule data changes, so
rule sets are compared by version instead. Scenarios specify the law, so they
always run against the statutory baseline policy and the policy is not compared.
"""

import json
from pathlib import Path
from typing import Annotated, Any, Final

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, TypeAdapter

from decision_engine.core import Decision, Facts, InstitutionPolicy, RuleRegistry, evaluate
from decision_engine.rules_loader import load_yaml_as_json

SCENARIO_GLOB: Final = "*.yaml"
_PLACEHOLDER_HASH: Final = "0" * 64
_UNCOMPARED_FIELDS: Final = ("registry_hash", "policy")
_PLACEHOLDER_POLICY: Final = {
    "institution": "baseline",
    "version": "0.0.0",
    "content_hash": "0" * 64,
}

ScenarioId = Annotated[str, StringConstraints(pattern=r"^GS-[A-Z]{2,7}-[0-9]{3}$")]


class Scenario(BaseModel):
    """One golden scenario: facts, the expected decision, and why."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: ScenarioId
    title: Annotated[str, StringConstraints(min_length=10, max_length=200)]
    facts: Facts
    expected: dict[str, Any] = Field(
        description="Decision fields without hashes; validated against the Decision schema.",
    )

    def expected_comparable(self) -> dict[str, Any]:
        """Validate ``expected`` as a full decision and return its hash-free form."""
        candidate = dict(self.expected)
        candidate["registry_hash"] = _PLACEHOLDER_HASH
        candidate["policy"] = _PLACEHOLDER_POLICY
        if isinstance(candidate.get("rule_set"), dict):
            candidate["rule_set"] = {**candidate["rule_set"], "content_hash": _PLACEHOLDER_HASH}
        decision = Decision.model_validate_json(json.dumps(candidate))
        return comparable(decision)


_SCENARIO_LIST = TypeAdapter(list[Scenario])


def comparable(decision: Decision) -> dict[str, Any]:
    """Decision as JSON-mode data without hashes or the policy reference."""
    data = decision.model_dump(mode="json")
    for name in _UNCOMPARED_FIELDS:
        data.pop(name)
    if data["rule_set"] is not None:
        data["rule_set"].pop("content_hash")
    return data


def load_scenarios(directory: Path) -> list[Scenario]:
    """Load every scenario file in ``directory``; IDs must be unique across files."""
    scenarios: list[Scenario] = []
    for path in sorted(directory.glob(SCENARIO_GLOB)):
        scenarios.extend(_SCENARIO_LIST.validate_json(load_yaml_as_json(path)))
    ids = [scenario.id for scenario in scenarios]
    duplicates = sorted({scenario_id for scenario_id in ids if ids.count(scenario_id) > 1})
    if duplicates:
        msg = f"duplicate golden scenario IDs: {', '.join(duplicates)}"
        raise ValueError(msg)
    return scenarios


def run_scenario(
    scenario: Scenario,
    rules: RuleRegistry,
    baseline: InstitutionPolicy,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(expected, actual)`` in comparable form, evaluated under ``baseline``."""
    return scenario.expected_comparable(), comparable(evaluate(scenario.facts, rules, baseline))


def render_markdown(scenarios: list[Scenario]) -> str:
    """Render scenarios as a plain-English table for attorney review."""
    lines = [
        "| ID | Scenario | Key facts | Expected outcome | Citations |",
        "|---|---|---|---|---|",
    ]
    lines.extend(
        f"| {s.id} | {s.title} | {_describe_facts(s.facts)} "
        f"| {_describe_outcome(s)} | {_describe_citations(s)} |"
        for s in scenarios
    )
    return "\n".join(lines) + "\n"


def _describe_facts(facts: Facts) -> str:
    parties = ", ".join(f"{p.party_id} {p.relationship.value}" for p in facts.parties) or "none"
    return (
        f"{facts.jurisdiction.value}; died {facts.date_of_death.isoformat()}; "
        f"evaluated {facts.as_of_date.isoformat()}; {facts.account.account_type.value} account "
        f"${facts.account.balance}{_describe_holders(facts)}; {_describe_estate(facts)}; "
        f"parties: {parties}"
    )


def _describe_estate(facts: Facts) -> str:
    estate = facts.estate
    value = "not declared" if estate.declared_value is None else f"${estate.declared_value}"
    real_property = {None: "unknown", True: "yes", False: "no"}[
        estate.has_real_property_in_jurisdiction
    ]
    affiants = ", ".join(
        f"{a.party_id} {a.capacity.value}" + (f" for {a.on_behalf_of}" if a.on_behalf_of else "")
        for a in estate.affiants
    )
    extras = [
        f"{label}: {_yes_no(flag)}"
        for label, flag in (
            ("resident", facts.decedent_resident_of_jurisdiction),
            ("PR application elsewhere", estate.representative_application_elsewhere),
            ("claim authorized by all successors", estate.claim_authorized_by_all_successors),
        )
    ]
    if estate.successor_notice_given_on is not None:
        extras.append(f"successors notified {estate.successor_notice_given_on.isoformat()}")
    return (
        f"administration: {estate.administration.value}; declared estate {value}; "
        f"real property: {real_property}; affiants: {affiants or 'none'}; " + "; ".join(extras)
    )


def _yes_no(flag: bool | None, /) -> str:  # noqa: FBT001 - maps a fact value to text
    return {None: "unknown", True: "yes", False: "no"}[flag]


def _describe_holders(facts: Facts) -> str:
    holders = [
        f"{h.party_id} {h.role.value}{'' if h.survived_decedent else ' (predeceased)'}"
        + (
            f" {h.terms_share.numerator}/{h.terms_share.denominator} by terms"
            if h.terms_share is not None
            else ""
        )
        for h in facts.account.holders
    ]
    return f" ({', '.join(holders)})" if holders else ""


def _describe_outcome(scenario: Scenario) -> str:
    expected = scenario.expected_comparable()
    if expected["determination"] is None:
        return f"Not determinable ({', '.join(expected['reasons'])})"
    payment = expected["determination"]["payment"]
    if payment["form"] == "any_of":
        return f"Payable to any of {', '.join(payment['party_ids'])}"
    payees = ", ".join(f"{p['party_id']} {p['share']}" for p in payment["payees"])
    return f"Pay {payees}"


def _describe_citations(scenario: Scenario) -> str:
    determination = scenario.expected_comparable()["determination"]
    if determination is None:
        return "—"
    payment = determination["payment"]
    found: set[str] = set(payment.get("citations", []))
    for payee in payment.get("payees", []):
        found.update(payee["citations"])
    for document in determination["required_documents"]:
        found.update(document["citations"])
    found.update(determination["release_date"]["citations"])
    found.update(determination["liability_protection"]["citations"])
    return "; ".join(sorted(found))
