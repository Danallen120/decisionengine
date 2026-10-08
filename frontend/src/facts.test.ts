import { emptyCase, localToday, nextPartyId, removeParty, toFacts, triToJson } from "./facts";
import type { CaseForm } from "./types";

function filled(): CaseForm {
  const form = emptyCase("2026-03-01");
  return {
    ...form,
    dateOfDeath: "2026-01-15",
    resident: "yes",
    parties: [
      { id: "P1", relationship: "child" },
      { id: "P2", relationship: "representative" },
    ],
    account: {
      ...form.account,
      type: "payable_on_death",
      balance: "5000.00",
      holders: [{ partyId: "P1", role: "pod_payee", survived: true, termsShare: "" }],
    },
    estate: {
      ...form.estate,
      declaredValue: "90000",
      noticeDate: "2026-02-01",
      affiants: [
        { partyId: "P1", capacity: "successor", onBehalfOf: "" },
        { partyId: "P2", capacity: "attorney_in_fact", onBehalfOf: "P1" },
      ],
    },
  };
}

test("tri-state maps unknown to null", () => {
  expect(triToJson("yes")).toBe(true);
  expect(triToJson("no")).toBe(false);
  expect(triToJson("unknown")).toBeNull();
});

test("localToday formats the local date", () => {
  expect(localToday(new Date(2026, 0, 5))).toBe("2026-01-05");
});

test("toFacts produces the exact Facts shape", () => {
  const facts = toFacts(filled());
  expect(facts).toEqual({
    jurisdiction: "CA",
    date_of_death: "2026-01-15",
    as_of_date: "2026-03-01",
    decedent_resident_of_jurisdiction: true,
    account: {
      account_type: "payable_on_death",
      balance: "5000.00",
      holders: [{ party_id: "P1", role: "pod_payee", survived_decedent: true }],
      requires_multiple_signatures: false,
      restraining_order_served: false,
      withdrawal_notice_received: false,
      dispute_notice_received: false,
      testamentary_disposition_notice_received: false,
      ownership_instrument_issued: false,
    },
    estate: {
      administration: "none",
      declared_value: "90000",
      has_real_property_in_jurisdiction: null,
      representative_application_elsewhere: null,
      successor_notice_given_on: "2026-02-01",
      claim_authorized_by_all_successors: null,
      affiants: [
        { party_id: "P1", capacity: "successor" },
        { party_id: "P2", capacity: "attorney_in_fact", on_behalf_of: "P1" },
      ],
    },
    parties: [
      { party_id: "P1", relationship: "child" },
      { party_id: "P2", relationship: "representative" },
    ],
  });
});

test("blank optional values become null and terms shares are sent when set", () => {
  const form = filled();
  form.estate.declaredValue = "";
  form.estate.noticeDate = "";
  form.account.holders = [{ partyId: "P1", role: "pod_payee", survived: false, termsShare: "1/1" }];
  const facts = toFacts(form) as { estate: Record<string, unknown>; account: { holders: unknown[] } };
  expect(facts.estate.declared_value).toBeNull();
  expect(facts.estate.successor_notice_given_on).toBeNull();
  expect(facts.account.holders[0]).toEqual({
    party_id: "P1",
    role: "pod_payee",
    survived_decedent: false,
    terms_share: "1/1",
  });
});

test("party IDs are never reused", () => {
  const form = filled();
  expect(nextPartyId(form)).toBe("P3");
  expect(nextPartyId(removeParty(form, "P2"))).toBe("P2");
  expect(nextPartyId({ ...form, parties: [{ id: "P7", relationship: "child" }] })).toBe("P8");
  expect(nextPartyId(emptyCase("2026-01-01"))).toBe("P1");
});

test("removing a party removes every reference to it", () => {
  const form = removeParty(filled(), "P1");
  expect(form.parties.map((p) => p.id)).toEqual(["P2"]);
  expect(form.account.holders).toEqual([]);
  expect(form.estate.affiants).toEqual([{ partyId: "P2", capacity: "attorney_in_fact", onBehalfOf: "" }]);
});
