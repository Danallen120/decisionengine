"""Decision schema: the engine's only output (REQ-CORE-002).

Invariants are enforced at construction, so an invalid decision cannot exist:
a determined decision has a rule set, citations on every statutory conclusion,
and either payee shares that sum to exactly 1 or an "any of" list of parties;
a non-determinable decision has reason codes and no conclusions. Every decision
records the rule registry and the institution policy it was made under.
"""

from datetime import date
from enum import StrEnum
from typing import Annotated, Final, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from decision_engine.core.facts import Jurisdiction, PartyId
from decision_engine.core.types import Citation, Code, InstitutionId, SemVer, Sha256Hex, Share

DECISION_SCHEMA_VERSION: Final = "2"

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
    POLICY_DECLINED = "policy_declined"


class _StrictModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


class Payee(_StrictModel):
    """A party who may be paid, and their exact share."""

    party_id: PartyId
    share: Share
    citations: Citations = Field(min_length=1)


class SharesPayment(_StrictModel):
    """Pay each listed party their exact share."""

    form: Literal["shares"] = "shares"
    payees: tuple[Payee, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _check_payees(self) -> Self:
        _require_unique([payee.party_id for payee in self.payees], "payee")
        if sum(payee.share for payee in self.payees) != 1:
            msg = "payee shares must sum to exactly 1"
            raise ValueError(msg)
        return self


class AnyOfPayment(_StrictModel):
    """Payable to any one or more of these parties, per the account terms."""

    form: Literal["any_of"] = "any_of"
    party_ids: tuple[PartyId, ...] = Field(min_length=2)
    citations: Citations = Field(min_length=1)

    @model_validator(mode="after")
    def _check_parties(self) -> Self:
        _require_unique(list(self.party_ids), "party")
        return self


Payment = Annotated[SharesPayment | AnyOfPayment, Field(discriminator="form")]


class DocumentSource(StrEnum):
    """Why a document is required."""

    STATUTE = "statute"
    POLICY = "policy"


class RequiredDocument(_StrictModel):
    """A document that must be received before release."""

    code: Code
    source: DocumentSource = DocumentSource.STATUTE
    citations: Citations = ()

    @model_validator(mode="after")
    def _check_basis(self) -> Self:
        if self.source is DocumentSource.STATUTE and not self.citations:
            msg = "a statutory document needs at least one citation"
            raise ValueError(msg)
        if self.source is DocumentSource.POLICY and self.citations:
            msg = "a policy document has no statutory citation"
            raise ValueError(msg)
        return self


class ReleaseDate(_StrictModel):
    """Earliest date funds may be released, including any days the policy adds."""

    earliest: date
    citations: Citations = Field(min_length=1)
    policy_days_added: int = Field(default=0, ge=0)


class LiabilityProtection(_StrictModel):
    """Whether statutory liability protection applies to paying as decided."""

    applies: bool
    citations: Citations = Field(min_length=1)


class RuleSetRef(_StrictModel):
    """Identifies the exact rule set that produced a decision."""

    jurisdiction: Jurisdiction
    version: SemVer
    content_hash: Sha256Hex


class PolicyRef(_StrictModel):
    """Identifies the exact institution policy a decision was made under."""

    institution: InstitutionId
    version: SemVer
    content_hash: Sha256Hex


class Determination(_StrictModel):
    """The conclusions reached for a covered fact pattern."""

    payment: Payment
    required_documents: tuple[RequiredDocument, ...]
    release_date: ReleaseDate
    liability_protection: LiabilityProtection

    @model_validator(mode="after")
    def _check_documents(self) -> Self:
        _require_unique([document.code for document in self.required_documents], "document")
        return self


def _require_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        msg = f"each {label} may appear only once"
        raise ValueError(msg)


class Decision(_StrictModel):
    """A complete, reproducible decision for one fact set."""

    schema_version: Literal["2"] = DECISION_SCHEMA_VERSION
    outcome: Outcome
    reasons: tuple[ReasonCode, ...] = ()
    determination: Determination | None = None
    rule_set: RuleSetRef | None = None
    policy: PolicyRef
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
