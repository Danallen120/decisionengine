// Mirrors the engine's Facts (schema v4) and Decision (schema v2). The API's strict
// schema is the enforcement point; these types keep the form honest at compile time.

export type TriState = "yes" | "no" | "unknown";

export const RELATIONSHIPS = [
  "surviving_spouse",
  "registered_domestic_partner",
  "child",
  "grandchild",
  "parent",
  "sibling",
  "named_beneficiary",
  "former_spouse",
  "former_domestic_partner",
  "trust",
  "representative",
] as const;
export type Relationship = (typeof RELATIONSHIPS)[number];

export const ACCOUNT_TYPES = [
  "sole",
  "joint_with_survivorship",
  "joint_without_survivorship",
  "payable_on_death",
  "totten_trust",
] as const;
export type AccountType = (typeof ACCOUNT_TYPES)[number];

export const HOLDER_ROLES = ["co_owner", "pod_payee", "totten_beneficiary"] as const;
export type HolderRole = (typeof HOLDER_ROLES)[number];

export const ADMINISTRATION_STATUSES = [
  "none",
  "opened_with_representative_consent",
  "opened_without_consent",
] as const;
export type AdministrationStatus = (typeof ADMINISTRATION_STATUSES)[number];

export const AFFIANT_CAPACITIES = [
  "successor",
  "guardian_or_conservator",
  "trustee",
  "custodian_for_minor",
  "other_state_personal_representative",
  "attorney_in_fact",
] as const;
export type AffiantCapacity = (typeof AFFIANT_CAPACITIES)[number];

export interface PartyForm {
  id: string;
  relationship: Relationship;
}

export interface HolderForm {
  partyId: string;
  role: HolderRole;
  survived: boolean;
  termsShare: string; // "" when the terms set no share
}

export interface AffiantForm {
  partyId: string;
  capacity: AffiantCapacity;
  onBehalfOf: string; // "" for a successor
}

export interface CaseForm {
  jurisdiction: string;
  dateOfDeath: string;
  asOfDate: string;
  resident: TriState;
  parties: PartyForm[];
  account: {
    type: AccountType;
    balance: string;
    holders: HolderForm[];
    requiresMultipleSignatures: boolean;
    restrainingOrderServed: boolean;
    withdrawalNoticeReceived: boolean;
    disputeNoticeReceived: boolean;
    testamentaryNoticeReceived: boolean;
    ownershipInstrumentIssued: boolean;
  };
  estate: {
    administration: AdministrationStatus;
    declaredValue: string; // "" means not declared
    realProperty: TriState;
    applicationElsewhere: TriState;
    noticeDate: string; // "" means unknown
    claimAuthorized: TriState;
    affiants: AffiantForm[];
  };
}

// ── Decision (as returned by the API) ──────────────────

export interface Payee {
  party_id: string;
  share: string;
  citations: string[];
}

export type Payment =
  | { form: "shares"; payees: Payee[] }
  | { form: "any_of"; party_ids: string[]; citations: string[] };

export interface RequiredDocument {
  code: string;
  source: "statute" | "policy";
  citations: string[];
}

export interface Determination {
  payment: Payment;
  required_documents: RequiredDocument[];
  release_date: { earliest: string; citations: string[]; policy_days_added: number };
  liability_protection: { applies: boolean; citations: string[] };
}

export interface Decision {
  schema_version: string;
  outcome: "determined" | "not_determinable";
  reasons: string[];
  determination: Determination | null;
  rule_set: { jurisdiction: string; version: string; content_hash: string } | null;
  policy: { institution: string; version: string; content_hash: string };
  registry_hash: string;
}

export interface EvaluateResponse {
  decision: Decision;
  facts_hash: string;
  engine_version: string;
}

export interface PolicyOption {
  id: string;
  institution: string;
  version: string;
  description: string;
}

export interface Meta {
  engine_version: string;
  facts_schema_version: string;
  decision_schema_version: string;
  registry_hash: string;
  policies: PolicyOption[];
}

export interface FieldError {
  loc: (string | number)[];
  type: string;
}
