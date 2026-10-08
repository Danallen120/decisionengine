import type { CaseForm, TriState } from "./types";

export const US_STATES = [
  "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN",
  "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
  "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT",
  "VT", "VA", "WA", "WV", "WI", "WY",
] as const;

export function triToJson(value: TriState): boolean | null {
  if (value === "unknown") return null;
  return value === "yes";
}

/** Today's date in the user's local time zone, as YYYY-MM-DD (a form default only). */
export function localToday(now: Date = new Date()): string {
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${now.getFullYear()}-${month}-${day}`;
}

export function emptyCase(today: string): CaseForm {
  return {
    jurisdiction: "CA",
    dateOfDeath: "",
    asOfDate: today,
    resident: "unknown",
    parties: [],
    account: {
      type: "sole",
      balance: "",
      holders: [],
      requiresMultipleSignatures: false,
      restrainingOrderServed: false,
      withdrawalNoticeReceived: false,
      disputeNoticeReceived: false,
      testamentaryNoticeReceived: false,
      ownershipInstrumentIssued: false,
    },
    estate: {
      administration: "none",
      declaredValue: "",
      realProperty: "unknown",
      applicationElsewhere: "unknown",
      noticeDate: "",
      claimAuthorized: "unknown",
      affiants: [],
    },
  };
}

/** Next unused opaque party ID (P1, P2, …). IDs are never reused after removal. */
export function nextPartyId(form: CaseForm): string {
  const used = form.parties.map((party) => Number(party.id.slice(1)));
  return `P${Math.max(0, ...used) + 1}`;
}

/** Remove a party and every holder or affiant reference to it. */
export function removeParty(form: CaseForm, partyId: string): CaseForm {
  return {
    ...form,
    parties: form.parties.filter((party) => party.id !== partyId),
    account: {
      ...form.account,
      holders: form.account.holders.filter((holder) => holder.partyId !== partyId),
    },
    estate: {
      ...form.estate,
      affiants: form.estate.affiants
        .filter((affiant) => affiant.partyId !== partyId)
        .map((affiant) =>
          affiant.onBehalfOf === partyId ? { ...affiant, onBehalfOf: "" } : affiant,
        ),
    },
  };
}

/** Convert the form into the exact Facts JSON the API expects. */
export function toFacts(form: CaseForm): Record<string, unknown> {
  return {
    jurisdiction: form.jurisdiction,
    date_of_death: form.dateOfDeath,
    as_of_date: form.asOfDate,
    decedent_resident_of_jurisdiction: triToJson(form.resident),
    account: {
      account_type: form.account.type,
      balance: form.account.balance,
      holders: form.account.holders.map((holder) => ({
        party_id: holder.partyId,
        role: holder.role,
        survived_decedent: holder.survived,
        ...(holder.termsShare ? { terms_share: holder.termsShare } : {}),
      })),
      requires_multiple_signatures: form.account.requiresMultipleSignatures,
      restraining_order_served: form.account.restrainingOrderServed,
      withdrawal_notice_received: form.account.withdrawalNoticeReceived,
      dispute_notice_received: form.account.disputeNoticeReceived,
      testamentary_disposition_notice_received: form.account.testamentaryNoticeReceived,
      ownership_instrument_issued: form.account.ownershipInstrumentIssued,
    },
    estate: {
      administration: form.estate.administration,
      declared_value: form.estate.declaredValue === "" ? null : form.estate.declaredValue,
      has_real_property_in_jurisdiction: triToJson(form.estate.realProperty),
      representative_application_elsewhere: triToJson(form.estate.applicationElsewhere),
      successor_notice_given_on: form.estate.noticeDate === "" ? null : form.estate.noticeDate,
      claim_authorized_by_all_successors: triToJson(form.estate.claimAuthorized),
      affiants: form.estate.affiants.map((affiant) => ({
        party_id: affiant.partyId,
        capacity: affiant.capacity,
        ...(affiant.capacity === "successor" ? {} : { on_behalf_of: affiant.onBehalfOf }),
      })),
    },
    parties: form.parties.map((party) => ({
      party_id: party.id,
      relationship: party.relationship,
    })),
  };
}
