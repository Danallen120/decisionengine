"""Load rule data and institution policies from disk (the I/O edge for rules and policy).

YAML is parsed with a safe loader that keeps dates as strings, then validated in
pydantic's JSON mode, so YAML and JSON inputs follow exactly the same strict rules
(for example, unquoted decimals become floats and are rejected as money).
"""

import json
from collections.abc import Mapping
from importlib.resources import files
from pathlib import Path
from typing import Final

import yaml

from decision_engine.core import (
    InstitutionPolicy,
    Jurisdiction,
    RuleRegistry,
    RuleSet,
    RuleSetData,
)
from decision_engine.core.rules import RuleLogic
from decision_engine.state_logic import LOGIC

MAX_RULE_FILE_BYTES: Final = 1_000_000
RULE_DATA_GLOB: Final = "*.yaml"
BASELINE_POLICY: Final = "baseline.yaml"

LogicTable = Mapping[tuple[Jurisdiction, str], RuleLogic]


class RuleLoadError(ValueError):
    """Rule data on disk is missing, malformed, or has no matching logic."""


class _DatesAsStringsLoader(yaml.SafeLoader):
    """SafeLoader that leaves ISO dates as strings for strict JSON-mode validation."""


_DatesAsStringsLoader.yaml_implicit_resolvers = {
    first: [(tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load_yaml_as_json(path: Path, max_bytes: int = MAX_RULE_FILE_BYTES) -> str:
    """Read a YAML file safely and return the same data as JSON text."""
    raw = path.read_bytes()
    if len(raw) > max_bytes:
        msg = f"{path.name} exceeds {max_bytes} bytes"
        raise RuleLoadError(msg)
    data = yaml.load(raw, Loader=_DatesAsStringsLoader)  # noqa: S506 - SafeLoader subclass
    return json.dumps(data)


def load_rule_data(path: Path) -> RuleSetData:
    """Parse and validate one rule data file."""
    return RuleSetData.model_validate_json(load_yaml_as_json(path))


def load_registry(data_dir: Path, logic: LogicTable) -> RuleRegistry:
    """Load every rule data file in ``data_dir`` and pair each with its logic.

    Raises:
        RuleLoadError: if a data file has no logic, or logic has no data file.
    """
    rule_sets = []
    for path in sorted(data_dir.rglob(RULE_DATA_GLOB)):
        data = load_rule_data(path)
        key = (data.jurisdiction, data.version)
        if key not in logic:
            msg = f"no rule logic registered for {key[0]} {key[1]} ({path.name})"
            raise RuleLoadError(msg)
        rule_sets.append(RuleSet(data=data, logic=logic[key]))
    loaded = {(rs.data.jurisdiction, rs.data.version) for rs in rule_sets}
    orphans = sorted(f"{jurisdiction} {version}" for jurisdiction, version in set(logic) - loaded)
    if orphans:
        msg = f"rule logic without rule data: {', '.join(orphans)}"
        raise RuleLoadError(msg)
    return RuleRegistry(rule_sets)


def default_registry() -> RuleRegistry:
    """Load the rule sets shipped with this package."""
    data_dir = Path(str(files("decision_engine") / "rules_data"))
    return load_registry(data_dir, LOGIC)


def load_policy(path: Path) -> InstitutionPolicy:
    """Parse and validate one institution policy file."""
    return InstitutionPolicy.model_validate_json(load_yaml_as_json(path))


def default_policy() -> InstitutionPolicy:
    """The packaged statutory baseline policy, which adds nothing beyond the law."""
    return load_policy(Path(str(files("decision_engine") / "policies" / BASELINE_POLICY)))


def load_policies(directory: Path | None = None) -> dict[str, InstitutionPolicy]:
    """The baseline policy plus every policy file in ``directory``, keyed by institution.

    Raises:
        RuleLoadError: if two policies name the same institution.
    """
    baseline = default_policy()
    policies = {baseline.institution: baseline}
    if directory is None:
        return policies
    for path in sorted(directory.glob(RULE_DATA_GLOB)):
        policy = load_policy(path)
        if policy.institution in policies:
            msg = f"more than one policy for institution {policy.institution!r}"
            raise RuleLoadError(msg)
        policies[policy.institution] = policy
    return policies
