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

FACTS_SCHEMA_VERSION: Final = "4"
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
    TRUST = "trust"
    """A trust that takes as a beneficiary. It acts only through a trustee affiant."""
    REPRESENTATIVE = "representative"
    """Acts for another party (e.g. a guardian or attorney-in-fact); no claim of its own."""


class AdministrationStatus(StrEnum):
    """Whether a proceeding to administer the estate exists in the jurisdiction."""

    NONE = "none"
    OPENED_WITH_REPRESENTATIVE_CONSENT = "opened_with_representative_consent"
    """A proceeding exists, and the personal representative consented in writing."""
    OPENED_WITHOUT_CONSENT = "opened_without_consent"


class AffiantCapacity(StrEnum):
    """The capacity in which someone signs a small-estate affidavit (provisional vocabulary)."""

    SUCCESSOR = "successor"
    GUARDIAN_OR_CONSERVATOR = "guardian_or_conservator"
    TRUSTEE = "trustee"
    CUSTODIAN_FOR_MINOR = "custodian_for_minor"
    OTHER_STATE_PERSONAL_REPRESENTATIVE = "other_state_personal_representative"
    ATTORNEY_IN_FACT = "attorney_in_fact"


class AccountType(StrEnum):
    """How the account was set up, per its terms."""

    SOLE = "sole"
    JOINT_WITH_SURVIVORSHIP = "joint_with_survivorship"
    JOINT_WITHOUT_SURVIVORSHIP = "joint_without_survivorship"
    """The decedent's funds pass to the estate unless they named a POD payee for them."""
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
    AccountType.JOINT_WITH_SURVIVORSHIP: (frozenset({HolderRole.CO_OWNER}), HolderRole.CO_OWNER),
    AccountType.JOINT_WITHOUT_SURVIVORSHIP: (
        frozenset({HolderRole.CO_OWNER, HolderRole.POD_PAYEE}),
        HolderRole.CO_OWNER,
    ),
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
    dispute_notice_received: bool = Field(
        description="Written notice of a dispute over the funds has been received.",
    )
    testamentary_disposition_notice_received: bool = Field(
        description="Written notice that a will disposes of this account has been received.",
    )
    ownership_instrument_issued: bool = Field(
        description=(
            "The institution issued an ownership instrument (e.g. a passbook or certificate) "
            "that it could require to be presented before paying."
        ),
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


class Affiant(_StrictModel):
    """Someone who signs a small-estate affidavit, and for whom."""

    party_id: PartyId
    capacity: AffiantCapacity
    on_behalf_of: PartyId | None = Field(
        default=None,
        description="The successor a representative signs for. Empty when signing as successor.",
    )


class Estate(_StrictModel):
    """Estate-level facts, as declared in the affidavit. Unknown values are null, never guessed."""

    administration: AdministrationStatus
    declared_value: Money | None = Field(
        description=(
            "Gross value of the decedent's property in the jurisdiction, excluding property the "
            "statute excludes, as declared by the affiants."
        ),
    )
    has_real_property_in_jurisdiction: bool | None
    representative_application_elsewhere: bool | None = Field(
        description=(
            "An application to appoint a personal representative is pending or has been "
            "granted outside the jurisdiction."
        ),
    )
    successor_notice_given_on: date | None = Field(
        description="Date the claimant served or mailed notice of the claim to other successors.",
    )
    claim_authorized_by_all_successors: bool | None = Field(
        description="The claimant has written authority from every other interested successor.",
    )
    affiants: tuple[Affiant, ...] = Field(default=(), max_length=MAX_PARTIES)


class Facts(_StrictModel):
    """Everything the engine may consider for one account."""

    schema_version: Literal["4"] = FACTS_SCHEMA_VERSION
    jurisdiction: Jurisdiction
    date_of_death: date
    as_of_date: date = Field(description="Date the decision is evaluated for. Never the clock.")
    decedent_resident_of_jurisdiction: bool | None
    account: Account
    estate: Estate
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
        _check_affiants(self.estate.affiants, {p.party_id: p.relationship for p in self.parties})
        notice = self.estate.successor_notice_given_on
        if notice is not None and not self.date_of_death <= notice <= self.as_of_date:
            msg = "successor_notice_given_on must be between date_of_death and as_of_date"
            raise ValueError(msg)
        return self


def _check_affiants(affiants: tuple[Affiant, ...], parties: dict[str, Relationship]) -> None:
    signer_ids = [affiant.party_id for affiant in affiants]
    if len(signer_ids) != len(set(signer_ids)):
        msg = "each party may sign the affidavit only once"
        raise ValueError(msg)
    for affiant in affiants:
        _check_affiant(affiant, parties)


def _check_affiant(affiant: Affiant, parties: dict[str, Relationship]) -> None:
    relationship = parties.get(affiant.party_id)
    if relationship is None:
        msg = f"affiant {affiant.party_id} must be listed in parties"
        raise ValueError(msg)
    if relationship is Relationship.TRUST:
        msg = "a trust signs only through a trustee affiant"
        raise ValueError(msg)
    is_successor = affiant.capacity is AffiantCapacity.SUCCESSOR
    if is_successor and relationship is Relationship.REPRESENTATIVE:
        msg = "a representative party must sign in a representative capacity"
        raise ValueError(msg)
    if is_successor != (affiant.on_behalf_of is None):
        msg = "on_behalf_of is required for a representative and not allowed for a successor"
        raise ValueError(msg)
    if affiant.on_behalf_of is not None and (
        affiant.on_behalf_of == affiant.party_id or affiant.on_behalf_of not in parties
    ):
        msg = "a representative must act for another listed party"
        raise ValueError(msg)
