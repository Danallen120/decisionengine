import { nextPartyId, removeParty, US_STATES } from "../facts";
import { CheckField, InputField, Section, SelectField, TriField } from "../fields";
import {
  ACCOUNT_TYPES,
  ADMINISTRATION_STATUSES,
  AFFIANT_CAPACITIES,
  HOLDER_ROLES,
  RELATIONSHIPS,
  type CaseForm,
} from "../types";

export interface StepProps {
  form: CaseForm;
  setForm: (form: CaseForm) => void;
}

const MONEY_PATTERN = "^(0|[1-9][0-9]{0,14})(\\.[0-9]{1,2})?$";
const SHARE_PATTERN = "^[1-9][0-9]{0,8}/[1-9][0-9]{0,8}$";

export function CaseStep({ form, setForm }: StepProps) {
  return (
    <Section title="Case basics">
      <SelectField
        label="State"
        value={form.jurisdiction}
        options={US_STATES}
        describe={(code) => code}
        onChange={(jurisdiction) => setForm({ ...form, jurisdiction })}
        hint="Only states with attorney-approved rules can be decided."
      />
      <InputField
        label="Date of death"
        type="date"
        value={form.dateOfDeath}
        onChange={(dateOfDeath) => setForm({ ...form, dateOfDeath })}
      />
      <InputField
        label="Evaluate as of"
        type="date"
        value={form.asOfDate}
        onChange={(asOfDate) => setForm({ ...form, asOfDate })}
        hint="The date the decision is made for. Defaults to today."
      />
      <TriField
        label="Was the decedent a resident of this state?"
        value={form.resident}
        onChange={(resident) => setForm({ ...form, resident })}
      />
    </Section>
  );
}

export function PeopleStep({ form, setForm }: StepProps) {
  const add = () =>
    setForm({ ...form, parties: [...form.parties, { id: nextPartyId(form), relationship: "child" }] });
  return (
    <Section title="People">
      <p className="hint">
        Add everyone with a possible claim. People are referred to only by ID (P1, P2, …), never
        by name.
      </p>
      {form.parties.map((party, index) => (
        <div className="row" key={party.id}>
          <strong className="tag">{party.id}</strong>
          <SelectField
            label={`Relationship of ${party.id} to the decedent`}
            value={party.relationship}
            options={RELATIONSHIPS}
            onChange={(relationship) => {
              const parties = form.parties.with(index, { ...party, relationship });
              setForm({ ...form, parties });
            }}
          />
          <button type="button" className="link" onClick={() => setForm(removeParty(form, party.id))}>
            Remove {party.id}
          </button>
        </div>
      ))}
      <button type="button" onClick={add}>
        Add person
      </button>
    </Section>
  );
}

export function AccountStep({ form, setForm }: StepProps) {
  const account = form.account;
  const setAccount = (changes: Partial<CaseForm["account"]>) =>
    setForm({ ...form, account: { ...account, ...changes } });
  const partyIds = form.parties.map((party) => party.id);
  const addHolder = () => {
    const partyId = partyIds.find((id) => !account.holders.some((h) => h.partyId === id));
    if (partyId === undefined) return;
    setAccount({
      holders: [...account.holders, { partyId, role: "co_owner", survived: true, termsShare: "" }],
    });
  };
  return (
    <Section title="Account">
      <SelectField
        label="Account type"
        value={account.type}
        options={ACCOUNT_TYPES}
        onChange={(type) => setAccount({ type, holders: type === "sole" ? [] : account.holders })}
      />
      <InputField
        label="Balance (USD)"
        value={account.balance}
        inputMode="decimal"
        pattern={MONEY_PATTERN}
        placeholder="12500.00"
        onChange={(balance) => setAccount({ balance })}
      />
      {account.type === "sole" ? null : (
        <>
          <h3>Other people on the account</h3>
          {account.holders.map((holder, index) => {
            const update = (changes: Partial<typeof holder>) =>
              setAccount({ holders: account.holders.with(index, { ...holder, ...changes }) });
            return (
              <div className="row" key={holder.partyId}>
                <SelectField
                  label="Person"
                  value={holder.partyId}
                  options={partyIds}
                  describe={(id) => id}
                  onChange={(partyId) => update({ partyId })}
                />
                <SelectField
                  label="Role"
                  value={holder.role}
                  options={HOLDER_ROLES}
                  onChange={(role) => update({ role })}
                />
                <CheckField
                  label="Survived the decedent"
                  checked={holder.survived}
                  onChange={(survived) => update({ survived })}
                />
                <InputField
                  label="Share set by the account terms (optional)"
                  value={holder.termsShare}
                  pattern={SHARE_PATTERN}
                  placeholder="1/2"
                  onChange={(termsShare) => update({ termsShare })}
                />
                <button
                  type="button"
                  className="link"
                  onClick={() => setAccount({ holders: account.holders.filter((_, i) => i !== index) })}
                >
                  Remove
                </button>
              </div>
            );
          })}
          <button type="button" onClick={addHolder} disabled={partyIds.length === account.holders.length}>
            Add person to account
          </button>
          {partyIds.length === 0 ? <p className="hint">Add people in the previous step first.</p> : null}
        </>
      )}
      <h3>Account terms and notices</h3>
      <CheckField
        label="Terms require more than one survivor's signature"
        checked={account.requiresMultipleSignatures}
        onChange={(requiresMultipleSignatures) => setAccount({ requiresMultipleSignatures })}
      />
      <CheckField
        label="A court order restraining payment has been served"
        checked={account.restrainingOrderServed}
        onChange={(restrainingOrderServed) => setAccount({ restrainingOrderServed })}
      />
      <CheckField
        label="Written notice restricting withdrawals received"
        checked={account.withdrawalNoticeReceived}
        onChange={(withdrawalNoticeReceived) => setAccount({ withdrawalNoticeReceived })}
      />
      <CheckField
        label="Written notice of a dispute over the funds received"
        checked={account.disputeNoticeReceived}
        onChange={(disputeNoticeReceived) => setAccount({ disputeNoticeReceived })}
      />
      <CheckField
        label="Written notice that a will disposes of this account received"
        checked={account.testamentaryNoticeReceived}
        onChange={(testamentaryNoticeReceived) => setAccount({ testamentaryNoticeReceived })}
      />
      <CheckField
        label="An ownership instrument (passbook or certificate) was issued"
        checked={account.ownershipInstrumentIssued}
        onChange={(ownershipInstrumentIssued) => setAccount({ ownershipInstrumentIssued })}
      />
    </Section>
  );
}

export function EstateStep({ form, setForm }: StepProps) {
  const estate = form.estate;
  const setEstate = (changes: Partial<CaseForm["estate"]>) =>
    setForm({ ...form, estate: { ...estate, ...changes } });
  const partyIds = form.parties.map((party) => party.id);
  const addAffiant = () => {
    const partyId = partyIds.find((id) => !estate.affiants.some((a) => a.partyId === id));
    if (partyId === undefined) return;
    setEstate({ affiants: [...estate.affiants, { partyId, capacity: "successor", onBehalfOf: "" }] });
  };
  return (
    <Section title="Estate (small-estate affidavit)">
      <p className="hint">As declared in the affidavit. Leave a value unknown rather than guessing.</p>
      <SelectField
        label="Estate administration in this state"
        value={estate.administration}
        options={ADMINISTRATION_STATUSES}
        onChange={(administration) => setEstate({ administration })}
      />
      <TriField
        label="Personal representative application pending or granted in another state?"
        value={estate.applicationElsewhere}
        onChange={(applicationElsewhere) => setEstate({ applicationElsewhere })}
      />
      <InputField
        label="Declared estate value (USD, leave blank if not declared)"
        value={estate.declaredValue}
        inputMode="decimal"
        pattern={MONEY_PATTERN}
        onChange={(declaredValue) => setEstate({ declaredValue })}
      />
      <TriField
        label="Does the estate include real property in this state?"
        value={estate.realProperty}
        onChange={(realProperty) => setEstate({ realProperty })}
      />
      <InputField
        label="Date other successors were notified (leave blank if unknown)"
        type="date"
        value={estate.noticeDate}
        onChange={(noticeDate) => setEstate({ noticeDate })}
      />
      <TriField
        label="Is the claim authorized in writing by all other successors?"
        value={estate.claimAuthorized}
        onChange={(claimAuthorized) => setEstate({ claimAuthorized })}
      />
      <h3>Affiants</h3>
      {estate.affiants.map((affiant, index) => {
        const update = (changes: Partial<typeof affiant>) =>
          setEstate({ affiants: estate.affiants.with(index, { ...affiant, ...changes }) });
        return (
          <div className="row" key={affiant.partyId}>
            <SelectField
              label="Signed by"
              value={affiant.partyId}
              options={partyIds}
              describe={(id) => id}
              onChange={(partyId) => update({ partyId })}
            />
            <SelectField
              label="Capacity"
              value={affiant.capacity}
              options={AFFIANT_CAPACITIES}
              onChange={(capacity) =>
                update({ capacity, onBehalfOf: capacity === "successor" ? "" : affiant.onBehalfOf })
              }
            />
            {affiant.capacity === "successor" ? null : (
              <SelectField
                label="On behalf of"
                value={affiant.onBehalfOf}
                options={["", ...partyIds.filter((id) => id !== affiant.partyId)]}
                describe={(id) => id || "Choose…"}
                onChange={(onBehalfOf) => update({ onBehalfOf })}
              />
            )}
            <button
              type="button"
              className="link"
              onClick={() => setEstate({ affiants: estate.affiants.filter((_, i) => i !== index) })}
            >
              Remove
            </button>
          </div>
        );
      })}
      <button type="button" onClick={addAffiant} disabled={partyIds.length === estate.affiants.length}>
        Add affiant
      </button>
    </Section>
  );
}
