"""Fact schema: the only input the core engine accepts (REQ-CORE-001).

The schema has no fields for names, SSNs/TINs, account numbers, addresses, or
dates of birth, and no free-text fields. Parties are identified by an opaque
``party_id`` and their relationship to the decedent. Every date the engine uses,
including the evaluation date, arrives here; the engine never reads a clock.

The relationship vocabulary is provisional. State rule
requirements extend them; they do not encode any state's law on their own.
"""

from datetime import date
from enum import StrEnum
from typing import Annotated, Final, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from decision_engine.core.types import Money, Share

FACTS_SCHEMA_VERSION: Final = "2"
MAX_PARTIES: Final = 50
MAX_ACCOUNT_HOLDERS: Final = 20


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
    FORMER_SPOUSE = "former_spouse"
    FORMER_DOMESTIC_PARTNER = "former_domestic_partner"


class AccountType(StrEnum):
    """How the account was set up, per its terms."""

    SOLE = "sole"
    JOINT = "joint"
    PAYABLE_ON_DEATH = "payable_on_death"
    TOTTEN_TRUST = "totten_trust"


class HolderRole(StrEnum):
    """A non-decedent person's role on the account."""

    CO_OWNER = "co_owner"
    """Another party to the account: a joint owner, or a co-trustee of a Totten trust."""
    POD_PAYEE = "pod_payee"
    TOTTEN_BENEFICIARY = "totten_beneficiary"


_ROLE_RULES: Final[dict[AccountType, tuple[frozenset[HolderRole], HolderRole | None]]] = {
    # account type: (roles allowed, role that must be present)
    AccountType.SOLE: (frozenset(), None),
    AccountType.JOINT: (frozenset({HolderRole.CO_OWNER}), HolderRole.CO_OWNER),
    AccountType.PAYABLE_ON_DEATH: (
        frozenset({HolderRole.CO_OWNER, HolderRole.POD_PAYEE}),
        HolderRole.POD_PAYEE,
    ),
    AccountType.TOTTEN_TRUST: (
        frozenset({HolderRole.CO_OWNER, HolderRole.TOTTEN_BENEFICIARY}),
        HolderRole.TOTTEN_BENEFICIARY,
    ),
}

PartyId = Annotated[str, StringConstraints(pattern=r"^P[1-9][0-9]{0,2}$")]
"""Opaque party reference such as ``P1``. Never a name or other identifier."""


class _StrictModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


class Party(_StrictModel):
    """A person with a potential claim, identified only by role."""

    party_id: PartyId
    relationship: Relationship


class AccountHolder(_StrictModel):
    """Someone other than the decedent named on the account, and whether they survived."""

    party_id: PartyId
    role: HolderRole
    survived_decedent: bool
    terms_share: Share | None = Field(
        default=None,
        description="Share set by the account terms. Only for POD payees and Totten beneficiaries.",
    )


class Account(_StrictModel):
    """The decedent's account and its terms, without any account identifier."""

    account_type: AccountType
    balance: Money
    holders: tuple[AccountHolder, ...] = Field(default=(), max_length=MAX_ACCOUNT_HOLDERS)
    requires_multiple_signatures: bool = Field(
        description="The terms require more than one survivor's signature to withdraw.",
    )
    restraining_order_served: bool = Field(
        description="A court order restraining payment has been served on the institution.",
    )
    withdrawal_notice_received: bool = Field(
        description="A party's written notice restricting withdrawals has been received.",
    )

    @model_validator(mode="after")
    def _check_terms(self) -> Self:
        ids = [holder.party_id for holder in self.holders]
        if len(ids) != len(set(ids)):
            msg = "each party may hold only one role on the account"
            raise ValueError(msg)
        _check_roles(self.account_type, self.holders)
        _check_terms_shares(self.holders)
        return self

    def holders_with(self, role: HolderRole) -> tuple[AccountHolder, ...]:
        """Holders in ``role``, in the order given."""
        return tuple(holder for holder in self.holders if holder.role is role)


def _check_roles(account_type: AccountType, holders: tuple[AccountHolder, ...]) -> None:
    allowed, required = _ROLE_RULES[account_type]
    roles = {holder.role for holder in holders}
    if not roles <= allowed:
        msg = (
            f"a {account_type.value} account cannot have holders in roles {sorted(roles - allowed)}"
        )
        raise ValueError(msg)
    if required is not None and required not in roles:
        msg = f"a {account_type.value} account needs at least one {required.value}"
        raise ValueError(msg)


def _check_terms_shares(holders: tuple[AccountHolder, ...]) -> None:
    with_share = [holder for holder in holders if holder.terms_share is not None]
    if not with_share:
        return
    if any(holder.role is HolderRole.CO_OWNER for holder in with_share):
        msg = "terms_share applies only to POD payees and Totten beneficiaries"
        raise ValueError(msg)
    payees = [holder for holder in holders if holder.role is not HolderRole.CO_OWNER]
    if len(with_share) != len(payees):
        msg = "when the terms set shares, every payee needs one"
        raise ValueError(msg)
    if sum(holder.terms_share or 0 for holder in payees) != 1:
        msg = "terms shares must sum to exactly 1"
        raise ValueError(msg)


class Facts(_StrictModel):
    """Everything the engine may consider for one account."""

    schema_version: Literal["2"] = FACTS_SCHEMA_VERSION
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
        unknown = {h.party_id for h in self.account.holders} - set(party_ids)
        if unknown:
            msg = f"account holders must be listed in parties: {sorted(unknown)}"
            raise ValueError(msg)
        return self
