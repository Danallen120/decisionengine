"""Fact schema: the only input the core engine accepts (REQ-CORE-001).

The schema has no fields for names, SSNs/TINs, account numbers, addresses, or
dates of birth, and no free-text fields. Parties are identified by an opaque
``party_id`` and their relationship to the decedent. Every date the engine uses,
including the evaluation date, arrives here; the engine never reads a clock.

The relationship and ownership vocabularies are provisional. State rule
requirements extend them; they do not encode any state's law on their own.
"""

from datetime import date
from enum import StrEnum
from typing import Annotated, Final, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from decision_engine.core.types import Money

FACTS_SCHEMA_VERSION: Final = "1"
MAX_PARTIES: Final = 50


class Jurisdiction(StrEnum):
    """US state or DC, by USPS code. Only some have rule sets (see the rule registry)."""

    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DC = "DC"
    DE = "DE"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"


class Relationship(StrEnum):
    """A party's relationship to the decedent (provisional vocabulary)."""

    SURVIVING_SPOUSE = "surviving_spouse"
    REGISTERED_DOMESTIC_PARTNER = "registered_domestic_partner"
    CHILD = "child"
    GRANDCHILD = "grandchild"
    PARENT = "parent"
    SIBLING = "sibling"
    NAMED_BENEFICIARY = "named_beneficiary"


class OwnershipType(StrEnum):
    """How the account was titled at death (provisional vocabulary)."""

    SOLE = "sole"
    JOINT_WITH_SURVIVORSHIP = "joint_with_survivorship"
    PAYABLE_ON_DEATH = "payable_on_death"


PartyId = Annotated[str, StringConstraints(pattern=r"^P[1-9][0-9]{0,2}$")]
"""Opaque party reference such as ``P1``. Never a name or other identifier."""


class _StrictModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


class Party(_StrictModel):
    """A person with a potential claim, identified only by role."""

    party_id: PartyId
    relationship: Relationship


class Account(_StrictModel):
    """The decedent's account, without any account identifier."""

    ownership: OwnershipType
    balance: Money


class Facts(_StrictModel):
    """Everything the engine may consider for one account."""

    schema_version: Literal["1"] = FACTS_SCHEMA_VERSION
    jurisdiction: Jurisdiction
    date_of_death: date
    as_of_date: date = Field(description="Date the decision is evaluated for. Never the clock.")
    account: Account
    probate_opened: bool
    parties: tuple[Party, ...] = Field(max_length=MAX_PARTIES)

    @model_validator(mode="after")
    def _check_consistency(self) -> Self:
        if self.as_of_date < self.date_of_death:
            msg = "as_of_date must be on or after date_of_death"
            raise ValueError(msg)
        party_ids = [party.party_id for party in self.parties]
        if len(party_ids) != len(set(party_ids)):
            msg = "party_id values must be unique"
            raise ValueError(msg)
        return self
