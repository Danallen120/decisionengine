"""Decision schema: the engine's only output (REQ-CORE-002).

Invariants are enforced at construction, so an invalid decision cannot exist:
a determined decision has a rule set, citations on every conclusion, and payee
shares that sum to exactly 1; a non-determinable decision has reason codes and
no conclusions.
"""

from datetime import date
from enum import StrEnum
from typing import Final, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from decision_engine.core.facts import Jurisdiction, PartyId
from decision_engine.core.types import Citation, Code, SemVer, Sha256Hex, Share

DECISION_SCHEMA_VERSION: Final = "1"

Citations = tuple[Citation, ...]


class Outcome(StrEnum):
    """Whether the engine could reach a decision under a covering rule set."""

    DETERMINED = "determined"
    NOT_DETERMINABLE = "not_determinable"


class ReasonCode(StrEnum):
    """Why a decision is not determinable. Operations routes these to a person."""

    UNSUPPORTED_JURISDICTION = "unsupported_jurisdiction"
    NO_RULE_SET_FOR_DATE_OF_DEATH = "no_rule_set_for_date_of_death"
    FACT_PATTERN_NOT_COVERED = "fact_pattern_not_covered"


class _StrictModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


class Payee(_StrictModel):
    """A party who may be paid, and their exact share."""

    party_id: PartyId
    share: Share
    citations: Citations = Field(min_length=1)


class RequiredDocument(_StrictModel):
    """A document that must be received before release."""

    code: Code
    citations: Citations = Field(min_length=1)


class ReleaseDate(_StrictModel):
    """Earliest date funds may be released."""

    earliest: date
    citations: Citations = Field(min_length=1)


class LiabilityProtection(_StrictModel):
    """Whether statutory liability protection applies to paying as decided."""

    applies: bool
    citations: Citations = Field(min_length=1)


class RuleSetRef(_StrictModel):
    """Identifies the exact rule set that produced a decision."""

    jurisdiction: Jurisdiction
    version: SemVer
    content_hash: Sha256Hex


class Determination(_StrictModel):
    """The conclusions a rule set reaches for a covered fact pattern."""

    payees: tuple[Payee, ...] = Field(min_length=1)
    required_documents: tuple[RequiredDocument, ...]
    release_date: ReleaseDate
    liability_protection: LiabilityProtection

    @model_validator(mode="after")
    def _check_payees(self) -> Self:
        party_ids = [payee.party_id for payee in self.payees]
        if len(party_ids) != len(set(party_ids)):
            msg = "each party may appear as a payee only once"
            raise ValueError(msg)
        if sum(payee.share for payee in self.payees) != 1:
            msg = "payee shares must sum to exactly 1"
            raise ValueError(msg)
        return self


class Decision(_StrictModel):
    """A complete, reproducible decision for one fact set."""

    schema_version: Literal["1"] = DECISION_SCHEMA_VERSION
    outcome: Outcome
    reasons: tuple[ReasonCode, ...] = ()
    determination: Determination | None = None
    rule_set: RuleSetRef | None = None
    registry_hash: Sha256Hex = Field(
        description="Hash of all loaded rule sets; makes every result reproducible.",
    )

    @model_validator(mode="after")
    def _check_outcome(self) -> Self:
        if self.outcome is Outcome.DETERMINED:
            if self.determination is None or self.rule_set is None or self.reasons:
                msg = "a determined decision needs a determination and a rule set, and no reasons"
                raise ValueError(msg)
        elif self.determination is not None or not self.reasons:
            msg = "a non-determinable decision needs reasons and no determination"
            raise ValueError(msg)
        return self


class NotDeterminable(_StrictModel):
    """Returned by rule logic when facts fall outside what its rules cover."""

    reasons: tuple[ReasonCode, ...] = Field(min_length=1)


RuleResult = Determination | NotDeterminable
