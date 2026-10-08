"""Institution policy: choices the statutes leave to the institution (REQ-POLICY-001).

A policy can only make a decision stricter: add waiting days, add required
documents, or decline cases outright. It has no field that could relax a
statutory condition, so it cannot weaken a protection the law grants. Every
decision records the policy's institution, version, and content hash.
"""

from datetime import timedelta
from typing import Final, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from decision_engine.core.canonical import sha256_hex
from decision_engine.core.decision import (
    Determination,
    DocumentSource,
    PolicyRef,
    ReleaseDate,
    RequiredDocument,
)
from decision_engine.core.facts import AccountType, Facts
from decision_engine.core.types import Code, InstitutionId, Money, PlainEnglish, SemVer

POLICY_SCHEMA_VERSION: Final = "1"
MAX_ADDITIONAL_WAITING_DAYS: Final = 3650


class _StrictModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


class PolicyDocument(_StrictModel):
    """A document the institution requires beyond the statute."""

    code: Code
    description: PlainEnglish


class InstitutionPolicy(_StrictModel):
    """One version of one institution's policy."""

    schema_version: Literal["1"] = POLICY_SCHEMA_VERSION
    institution: InstitutionId
    version: SemVer
    description: PlainEnglish
    additional_waiting_days: int = Field(default=0, ge=0, le=MAX_ADDITIONAL_WAITING_DAYS)
    additional_documents: tuple[PolicyDocument, ...] = ()
    declined_account_types: tuple[AccountType, ...] = ()
    decline_balance_above: Money | None = None

    @model_validator(mode="after")
    def _check_unique(self) -> Self:
        codes = [document.code for document in self.additional_documents]
        if len(codes) != len(set(codes)):
            msg = "additional document codes must be unique"
            raise ValueError(msg)
        if len(self.declined_account_types) != len(set(self.declined_account_types)):
            msg = "declined account types must be unique"
            raise ValueError(msg)
        return self

    def content_hash(self) -> str:
        """SHA-256 of the canonical JSON form; independent of file formatting."""
        return sha256_hex(self)

    def ref(self) -> PolicyRef:
        """Identify this policy on a decision."""
        return PolicyRef(
            institution=self.institution,
            version=self.version,
            content_hash=self.content_hash(),
        )

    def declines(self, facts: Facts) -> bool:
        """Return whether the institution declines to decide this case automatically."""
        if facts.account.account_type in self.declined_account_types:
            return True
        limit = self.decline_balance_above
        return limit is not None and facts.account.balance > limit

    def apply(self, determination: Determination) -> Determination:
        """Add the policy's waiting days and documents to a statutory determination."""
        statutory_codes = {document.code for document in determination.required_documents}
        extra_documents = tuple(
            RequiredDocument(code=document.code, source=DocumentSource.POLICY)
            for document in self.additional_documents
            if document.code not in statutory_codes
        )
        release = determination.release_date
        # Rebuilt through the constructor (not model_copy) so every invariant is re-validated.
        return Determination(
            payment=determination.payment,
            required_documents=determination.required_documents + extra_documents,
            release_date=ReleaseDate(
                earliest=release.earliest + timedelta(days=self.additional_waiting_days),
                citations=release.citations,
                policy_days_added=release.policy_days_added + self.additional_waiting_days,
            ),
            liability_protection=determination.liability_protection,
        )
