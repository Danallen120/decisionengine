"""Golden scenarios: the attorney-readable spec that is also the test suite (REQ-TEST-001).

A scenario file is YAML with a list of scenarios. Each scenario has a stable
``id``, a plain-English ``title``, ``facts``, and an ``expected`` decision
without hash fields. Hashes change whenever any rule data changes, so they are
compared by the rule-set version instead.
"""

import json
from pathlib import Path
from typing import Annotated, Any, Final

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, TypeAdapter

from decision_engine.core import Decision, Facts, RuleRegistry, evaluate
from decision_engine.rules_loader import load_yaml_as_json

SCENARIO_GLOB: Final = "*.yaml"
_PLACEHOLDER_HASH: Final = "0" * 64
_HASH_FIELDS: Final = ("registry_hash",)

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
        if isinstance(candidate.get("rule_set"), dict):
            candidate["rule_set"] = {**candidate["rule_set"], "content_hash": _PLACEHOLDER_HASH}
        decision = Decision.model_validate_json(json.dumps(candidate))
        return comparable(decision)


_SCENARIO_LIST = TypeAdapter(list[Scenario])


def comparable(decision: Decision) -> dict[str, Any]:
    """Decision as JSON-mode data with hash fields removed."""
    data = decision.model_dump(mode="json")
    for name in _HASH_FIELDS:
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


def run_scenario(scenario: Scenario, rules: RuleRegistry) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(expected, actual)`` in comparable form."""
    return scenario.expected_comparable(), comparable(evaluate(scenario.facts, rules))


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
    probate = "probate opened" if facts.probate_opened else "no probate"
    return (
        f"{facts.jurisdiction.value}; died {facts.date_of_death.isoformat()}; "
        f"evaluated {facts.as_of_date.isoformat()}; {facts.account.ownership.value} account "
        f"${facts.account.balance}; {probate}; parties: {parties}"
    )


def _describe_outcome(scenario: Scenario) -> str:
    expected = scenario.expected_comparable()
    if expected["determination"] is None:
        return f"Not determinable ({', '.join(expected['reasons'])})"
    payees = ", ".join(f"{p['party_id']} {p['share']}" for p in expected["determination"]["payees"])
    return f"Pay {payees}"


def _describe_citations(scenario: Scenario) -> str:
    determination = scenario.expected_comparable()["determination"]
    if determination is None:
        return "—"
    found: set[str] = set()
    for payee in determination["payees"]:
        found.update(payee["citations"])
    for document in determination["required_documents"]:
        found.update(document["citations"])
    found.update(determination["release_date"]["citations"])
    found.update(determination["liability_protection"]["citations"])
    return "; ".join(sorted(found))
