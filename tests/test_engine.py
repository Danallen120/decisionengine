"""REQ-CORE-003: pure, deterministic evaluation; REQ-RULES-001 outcomes."""

import ast
import json
import os
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

from decision_engine.core import (
    AccountType,
    AdministrationStatus,
    Decision,
    Facts,
    Jurisdiction,
    Outcome,
    ReasonCode,
    Relationship,
    RuleRegistry,
    RuleSet,
    canonical_json,
    evaluate,
)

from .conftest import BASELINE, estate_payload, make_facts, rule_data, split_evenly

PURE_PACKAGES = [
    Path(__file__).parents[1] / "src" / "decision_engine" / "core",
    Path(__file__).parents[1] / "src" / "decision_engine" / "state_logic",
]
ALLOWED_IMPORTS = {
    "collections",
    "dataclasses",
    "datetime",
    "decimal",
    "decision_engine",
    "enum",
    "fractions",
    "hashlib",
    "json",
    "pydantic",
    "re",
    "typing",
}
FORBIDDEN_CALLS = {"now", "today", "utcnow", "time", "monotonic", "perf_counter", "urandom"}


# ── Outcomes ────────────────────────────────────────────


def test_covered_facts_are_determined(registry):
    decision = evaluate(make_facts(), registry, BASELINE)
    assert decision.outcome is Outcome.DETERMINED
    assert decision.rule_set is not None
    assert decision.rule_set.version == "0.0.1"
    assert decision.registry_hash == registry.registry_hash


def test_unsupported_jurisdiction_is_not_determinable(registry):
    decision = evaluate(make_facts(jurisdiction="TX"), registry, BASELINE)
    assert decision.outcome is Outcome.NOT_DETERMINABLE
    assert decision.reasons == (ReasonCode.UNSUPPORTED_JURISDICTION,)
    assert decision.determination is None
    assert decision.rule_set is None


def test_death_before_any_rule_set_is_not_determinable(registry):
    decision = evaluate(make_facts(date_of_death="2025-12-31"), registry, BASELINE)
    assert decision.reasons == (ReasonCode.NO_RULE_SET_FOR_DATE_OF_DEATH,)


def test_rule_logic_can_decline_and_the_rule_set_is_still_recorded(registry):
    facts = make_facts(parties=[], estate=estate_payload(affiants=[]))
    decision = evaluate(facts, registry, BASELINE)
    assert decision.reasons == (ReasonCode.FACT_PATTERN_NOT_COVERED,)
    assert decision.rule_set is not None


# ── Determinism ─────────────────────────────────────────


def test_repeated_evaluation_is_byte_identical(registry):
    facts = make_facts()
    assert canonical_json(evaluate(facts, registry, BASELINE)) == canonical_json(
        evaluate(facts, registry, BASELINE)
    )


def test_evaluation_is_identical_across_processes_and_hash_seeds():
    script = (
        "import json, sys\n"
        "sys.path.insert(0, 'tests')\n"
        "from conftest import BASELINE, make_facts, split_evenly, rule_data\n"
        "from decision_engine.core import RuleRegistry, RuleSet, canonical_json, evaluate\n"
        "registry = RuleRegistry([RuleSet(data=rule_data(), logic=split_evenly)])\n"
        "print(canonical_json(evaluate(make_facts(), registry, BASELINE)))\n"
    )
    root = Path(__file__).parents[1]
    outputs = set()
    for seed in ("0", "1", "12345"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        outputs.add(result.stdout)
    assert len(outputs) == 1


def _pure_sources():
    for package in PURE_PACKAGES:
        yield from sorted(package.rglob("*.py"))


def test_pure_packages_import_only_allowed_modules():
    violations = []
    for path in _pure_sources():
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                roots = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots = [node.module.split(".")[0]]
            else:
                continue
            violations += [f"{path.name}: {r}" for r in roots if r not in ALLOWED_IMPORTS]
    assert not violations


def test_pure_packages_never_read_clocks_or_randomness():
    violations = []
    for path in _pure_sources():
        violations.extend(
            f"{path.name}:{node.lineno} .{node.attr}"
            for node in ast.walk(ast.parse(path.read_text()))
            if isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_CALLS
        )
    assert not violations


def test_boundary_scan_detects_a_violation(tmp_path):
    """Guards the guard: the scan must flag a clock read and a forbidden import."""
    bad = tmp_path / "bad.py"
    bad.write_text("import random\nfrom datetime import date\nx = date.today()\n")
    tree = ast.parse(bad.read_text())
    imports = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    calls = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    assert imports - ALLOWED_IMPORTS == {"random"}
    assert calls & FORBIDDEN_CALLS == {"today"}


# ── Properties ──────────────────────────────────────────

_dates = st.dates(min_value=date(1900, 1, 1), max_value=date(2100, 12, 31))
_REGISTRY = RuleRegistry([RuleSet(data=rule_data(), logic=split_evenly)])


_REQUIRED_ROLE = {
    AccountType.JOINT_WITH_SURVIVORSHIP: "co_owner",
    AccountType.JOINT_WITHOUT_SURVIVORSHIP: "co_owner",
    AccountType.PAYABLE_ON_DEATH: "pod_payee",
    AccountType.TOTTEN_TRUST: "totten_beneficiary",
}


@st.composite
def facts_strategy(draw):
    date_of_death = draw(_dates)
    as_of = date_of_death + timedelta(days=draw(st.integers(min_value=0, max_value=3650)))
    account_type = draw(st.sampled_from(list(AccountType)))
    minimum = 0 if account_type is AccountType.SOLE else 1
    count = draw(st.integers(min_value=minimum, max_value=6))
    parties = [
        {"party_id": f"P{i}", "relationship": draw(st.sampled_from(list(Relationship))).value}
        for i in range(1, count + 1)
    ]
    holders = []
    if account_type is not AccountType.SOLE:
        holders = [
            {
                "party_id": party["party_id"],
                "role": _REQUIRED_ROLE[account_type],
                "survived_decedent": draw(st.booleans()),
            }
            for party in parties[: draw(st.integers(min_value=1, max_value=count))]
        ]
    cents = draw(st.integers(min_value=0, max_value=10**12))
    payload = {
        "jurisdiction": draw(st.sampled_from(list(Jurisdiction))).value,
        "date_of_death": date_of_death.isoformat(),
        "as_of_date": as_of.isoformat(),
        "decedent_resident_of_jurisdiction": draw(st.one_of(st.none(), st.booleans())),
        "account": {
            "account_type": account_type.value,
            "balance": f"{cents // 100}.{cents % 100:02d}",
            "holders": holders,
            "requires_multiple_signatures": draw(st.booleans()),
            "restraining_order_served": draw(st.booleans()),
            "withdrawal_notice_received": draw(st.booleans()),
            "dispute_notice_received": draw(st.booleans()),
            "testamentary_disposition_notice_received": draw(st.booleans()),
            "ownership_instrument_issued": draw(st.booleans()),
        },
        "estate": {
            "administration": draw(st.sampled_from(list(AdministrationStatus))).value,
            "declared_value": draw(
                st.one_of(st.none(), st.just(f"{cents // 100}.{cents % 100:02d}"))
            ),
            "has_real_property_in_jurisdiction": draw(st.one_of(st.none(), st.booleans())),
            "representative_application_elsewhere": draw(st.one_of(st.none(), st.booleans())),
            "successor_notice_given_on": draw(
                st.one_of(
                    st.none(), st.just(date_of_death.isoformat()), st.just(as_of.isoformat())
                ),
            ),
            "claim_authorized_by_all_successors": draw(st.one_of(st.none(), st.booleans())),
            "affiants": [
                {"party_id": party["party_id"], "capacity": "successor"}
                for party in parties[: draw(st.integers(min_value=0, max_value=count))]
                if party["relationship"] not in {"trust", "representative"}
            ],
        },
        "parties": parties,
    }
    return Facts.model_validate_json(json.dumps(payload))


@given(facts=facts_strategy())
def test_any_valid_facts_yield_a_valid_decision(facts):
    text = canonical_json(evaluate(facts, _REGISTRY, BASELINE))
    assert canonical_json(Decision.model_validate_json(text)) == text
    assert text == canonical_json(evaluate(facts, _REGISTRY, BASELINE))
