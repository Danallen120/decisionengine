"""Rule sets, their content hash, and selection by jurisdiction and date of death.

Rule *data* (thresholds, dates, document codes, each with citations) is
validated against ``RuleSetData`` and hashed in canonical form (REQ-RULES-002).
Rule *logic* is a pure function paired with that data. The ``version`` covers
both; the hash covers the data, so any change to logic must bump the version.

Selection never falls back to a default: facts outside every rule set's
coverage yield a reason code instead (REQ-RULES-001).
"""

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import date
from hashlib import sha256
from typing import Annotated, Final, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from decision_engine.core.canonical import canonical_json
from decision_engine.core.decision import ReasonCode, RuleResult, RuleSetRef
from decision_engine.core.facts import Facts, Jurisdiction
from decision_engine.core.types import Citation, Money, PlainEnglish, SemVer

RULE_DATA_SCHEMA_VERSION: Final = "1"

ParameterName = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_]{2,63}$")]


class _StrictModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


class _ParameterBase(_StrictModel):
    name: ParameterName
    description: PlainEnglish = Field(description="What this value means, for attorney review.")
    citations: tuple[Citation, ...] = Field(min_length=1)


class MoneyParameter(_ParameterBase):
    """A dollar threshold or limit."""

    kind: Literal["money"]
    value: Money


class DaysParameter(_ParameterBase):
    """A waiting period or deadline in days."""

    kind: Literal["days"]
    value: int = Field(ge=0, le=3650)


class DateParameter(_ParameterBase):
    """A specific date, such as a statutory cut-over."""

    kind: Literal["date"]
    value: date


Parameter = Annotated[
    MoneyParameter | DaysParameter | DateParameter,
    Field(discriminator="kind"),
]


class RuleSetData(_StrictModel):
    """The cited, attorney-reviewable data for one version of one state's rules."""

    schema_version: Literal["1"] = RULE_DATA_SCHEMA_VERSION
    jurisdiction: Jurisdiction
    version: SemVer
    effective_from: date = Field(description="First date of death this rule set covers.")
    effective_through: date | None = Field(
        default=None,
        description="Last date of death covered (inclusive). None means open-ended.",
    )
    parameters: tuple[Parameter, ...]

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.effective_through is not None and self.effective_through < self.effective_from:
            msg = "effective_through must be on or after effective_from"
            raise ValueError(msg)
        names = [parameter.name for parameter in self.parameters]
        if len(names) != len(set(names)):
            msg = "parameter names must be unique"
            raise ValueError(msg)
        return self

    def covers(self, date_of_death: date) -> bool:
        """Return whether a death on this date falls within the effective range."""
        if date_of_death < self.effective_from:
            return False
        return self.effective_through is None or date_of_death <= self.effective_through

    def content_hash(self) -> str:
        """SHA-256 of the canonical JSON form; independent of file formatting."""
        return _sha256_hex(canonical_json(self.model_dump(mode="json")))


RuleLogic = Callable[[Facts, RuleSetData], RuleResult]
"""Pure function from facts and rule data to a result. No I/O, clock, or randomness."""


@dataclass(frozen=True, slots=True)
class RuleSet:
    """Rule data paired with the logic that applies it."""

    data: RuleSetData
    logic: RuleLogic = field(compare=False)

    def ref(self) -> RuleSetRef:
        """Identify this rule set on a decision."""
        return RuleSetRef(
            jurisdiction=self.data.jurisdiction,
            version=self.data.version,
            content_hash=self.data.content_hash(),
        )


class RuleRegistryError(ValueError):
    """The set of rule sets is inconsistent, so no decision can be trusted."""


class RuleRegistry:
    """All loaded rule sets, validated so that selection is never ambiguous."""

    def __init__(self, rule_sets: Iterable[RuleSet]) -> None:
        """Validate and index rule sets.

        Raises:
            RuleRegistryError: on duplicate versions or overlapping effective ranges
                within one jurisdiction.
        """
        ordered = sorted(rule_sets, key=lambda rs: (rs.data.jurisdiction, rs.data.effective_from))
        _check_no_duplicates_or_overlaps(ordered)
        self._rule_sets: tuple[RuleSet, ...] = tuple(ordered)
        self._hash = _sha256_hex(
            canonical_json([rule_set.ref().model_dump(mode="json") for rule_set in ordered]),
        )

    @property
    def registry_hash(self) -> str:
        """Hash identifying every loaded rule set."""
        return self._hash

    def select(self, jurisdiction: Jurisdiction, date_of_death: date) -> RuleSet | ReasonCode:
        """Return the one rule set covering these facts, or why there is none."""
        candidates = [rs for rs in self._rule_sets if rs.data.jurisdiction is jurisdiction]
        if not candidates:
            return ReasonCode.UNSUPPORTED_JURISDICTION
        for rule_set in candidates:
            if rule_set.data.covers(date_of_death):
                return rule_set
        return ReasonCode.NO_RULE_SET_FOR_DATE_OF_DEATH


def _check_no_duplicates_or_overlaps(ordered: list[RuleSet]) -> None:
    seen_versions: set[tuple[Jurisdiction, str]] = set()
    for index, rule_set in enumerate(ordered):
        key = (rule_set.data.jurisdiction, rule_set.data.version)
        if key in seen_versions:
            msg = f"duplicate rule set {key[0]} {key[1]}"
            raise RuleRegistryError(msg)
        seen_versions.add(key)
        if index and _overlaps(ordered[index - 1].data, rule_set.data):
            msg = f"overlapping effective ranges for {rule_set.data.jurisdiction}"
            raise RuleRegistryError(msg)


def _overlaps(earlier: RuleSetData, later: RuleSetData) -> bool:
    if earlier.jurisdiction is not later.jurisdiction:
        return False
    return earlier.effective_through is None or earlier.effective_through >= later.effective_from


def _sha256_hex(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()
