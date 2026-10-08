import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { emptyCase, toFacts } from "../facts";
import type { CaseForm } from "../types";
import { AccountStep, CaseStep, EstateStep, PeopleStep, type StepProps } from "./Steps";

let latest: CaseForm;

function Harness({ Step, initial }: { Step: (props: StepProps) => React.JSX.Element; initial: CaseForm }) {
  const [form, setForm] = useState(initial);
  latest = form;
  return <Step form={form} setForm={setForm} />;
}

function withPeople(count: number): CaseForm {
  const form = emptyCase("2026-03-01");
  return {
    ...form,
    parties: Array.from({ length: count }, (_, i) => ({ id: `P${i + 1}`, relationship: "child" as const })),
  };
}

test("case step edits state, dates, and residency", async () => {
  const user = userEvent.setup();
  render(<Harness Step={CaseStep} initial={emptyCase("2026-03-01")} />);
  await user.selectOptions(screen.getByLabelText("State"), "WA");
  await user.type(screen.getByLabelText("Date of death"), "2026-01-15");
  await user.clear(screen.getByLabelText("Evaluate as of"));
  await user.type(screen.getByLabelText("Evaluate as of"), "2026-02-20");
  await user.selectOptions(screen.getByLabelText(/resident of this state/), "no");
  expect(toFacts(latest)).toMatchObject({
    jurisdiction: "WA",
    date_of_death: "2026-01-15",
    as_of_date: "2026-02-20",
    decedent_resident_of_jurisdiction: false,
  });
});

test("people step adds, relabels, and removes people", async () => {
  const user = userEvent.setup();
  render(<Harness Step={PeopleStep} initial={emptyCase("2026-03-01")} />);
  await user.click(screen.getByRole("button", { name: "Add person" }));
  await user.click(screen.getByRole("button", { name: "Add person" }));
  await user.selectOptions(screen.getByLabelText("Relationship of P2 to the decedent"), "surviving_spouse");
  await user.click(screen.getByRole("button", { name: "Remove P1" }));
  expect(latest.parties).toEqual([{ id: "P2", relationship: "surviving_spouse" }]);
});

test("account step manages holders, terms shares, and notices", async () => {
  const user = userEvent.setup();
  render(<Harness Step={AccountStep} initial={withPeople(2)} />);
  await user.selectOptions(screen.getByLabelText("Account type"), "payable_on_death");
  await user.type(screen.getByLabelText("Balance (USD)"), "2500.00");
  await user.click(screen.getByRole("button", { name: "Add person to account" }));
  await user.click(screen.getByRole("button", { name: "Add person to account" }));
  expect(screen.getByRole("button", { name: "Add person to account" })).toBeDisabled();

  const rows = screen.getAllByLabelText("Role");
  await user.selectOptions(rows[0] as HTMLElement, "pod_payee");
  await user.selectOptions(rows[1] as HTMLElement, "pod_payee");
  await user.click(screen.getAllByLabelText("Survived the decedent")[1] as HTMLElement);
  await user.type(screen.getAllByLabelText(/Share set by the account terms/)[0] as HTMLElement, "1/1");
  for (const name of [
    /more than one survivor's signature/,
    /restraining payment/,
    /restricting withdrawals/,
    /dispute over the funds/,
    /a will disposes/,
    /ownership instrument/,
  ]) {
    await user.click(screen.getByLabelText(name));
  }
  await user.click(screen.getAllByRole("button", { name: "Remove" })[1] as HTMLElement);

  const facts = toFacts(latest) as { account: Record<string, unknown> };
  expect(facts.account).toMatchObject({
    account_type: "payable_on_death",
    balance: "2500.00",
    holders: [{ party_id: "P1", role: "pod_payee", survived_decedent: true, terms_share: "1/1" }],
    requires_multiple_signatures: true,
    restraining_order_served: true,
    withdrawal_notice_received: true,
    dispute_notice_received: true,
    testamentary_disposition_notice_received: true,
    ownership_instrument_issued: true,
  });

  await user.selectOptions(screen.getAllByLabelText("Person")[0] as HTMLElement, "P2");
  expect(latest.account.holders[0]?.partyId).toBe("P2");
  await user.selectOptions(screen.getByLabelText("Account type"), "sole");
  expect(latest.account.holders).toEqual([]);
});

test("account step explains when no people exist yet", () => {
  render(<Harness Step={AccountStep} initial={{ ...emptyCase("2026-03-01"), account: { ...emptyCase("2026-03-01").account, type: "joint_with_survivorship" } }} />);
  expect(screen.getByText(/Add people in the previous step first/)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Add person to account" })).toBeDisabled();
});

test("estate step captures declarations and affiants", async () => {
  const user = userEvent.setup();
  render(<Harness Step={EstateStep} initial={withPeople(2)} />);
  await user.selectOptions(screen.getByLabelText(/administration in this state/), "opened_with_representative_consent");
  await user.selectOptions(screen.getByLabelText(/another state/), "no");
  await user.type(screen.getByLabelText(/Declared estate value/), "90000.00");
  await user.selectOptions(screen.getByLabelText(/real property/), "yes");
  await user.type(screen.getByLabelText(/other successors were notified/), "2026-02-01");
  await user.selectOptions(screen.getByLabelText(/authorized in writing/), "yes");

  await user.click(screen.getByRole("button", { name: "Add affiant" }));
  await user.click(screen.getByRole("button", { name: "Add affiant" }));
  expect(screen.getByRole("button", { name: "Add affiant" })).toBeDisabled();
  const capacities = screen.getAllByLabelText("Capacity");
  await user.selectOptions(capacities[1] as HTMLElement, "attorney_in_fact");
  const behalf = screen.getByLabelText("On behalf of");
  expect(within(behalf).queryByRole("option", { name: "P2" })).toBeNull();
  await user.selectOptions(behalf, "P1");

  expect(toFacts(latest)).toMatchObject({
    estate: {
      administration: "opened_with_representative_consent",
      declared_value: "90000.00",
      has_real_property_in_jurisdiction: true,
      representative_application_elsewhere: false,
      successor_notice_given_on: "2026-02-01",
      claim_authorized_by_all_successors: true,
      affiants: [
        { party_id: "P1", capacity: "successor" },
        { party_id: "P2", capacity: "attorney_in_fact", on_behalf_of: "P1" },
      ],
    },
  });

  await user.selectOptions(capacities[1] as HTMLElement, "successor");
  expect(latest.estate.affiants[1]).toEqual({ partyId: "P2", capacity: "successor", onBehalfOf: "" });
  await user.selectOptions(screen.getAllByLabelText("Signed by")[0] as HTMLElement, "P2");
  expect(latest.estate.affiants[0]?.partyId).toBe("P2");
  await user.click(screen.getAllByRole("button", { name: "Remove" })[0] as HTMLElement);
  expect(latest.estate.affiants).toHaveLength(1);
});
