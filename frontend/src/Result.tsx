import { describeShare, explainReason, humanizeCode } from "./explain";
import type { Determination, EvaluateResponse } from "./types";

function Citations({ items }: { items: string[] }) {
  return items.length ? <span className="cite">({items.join("; ")})</span> : null;
}

export function buildRecord(
  response: EvaluateResponse,
  facts: Record<string, unknown>,
  generatedAt: Date,
): string {
  const record = {
    record_version: 1,
    generated_at: generatedAt.toISOString(),
    engine_version: response.engine_version,
    facts_hash: response.facts_hash,
    facts,
    decision: response.decision,
  };
  return JSON.stringify(record, null, 2);
}

function downloadRecord(response: EvaluateResponse, facts: Record<string, unknown>) {
  const blob = new Blob([buildRecord(response, facts, new Date())], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `decision-${response.facts_hash.slice(0, 12)}.json`;
  link.click();
  URL.revokeObjectURL(url);
}

function DeterminationView({ determination }: { determination: Determination }) {
  const { payment, required_documents, release_date, liability_protection } = determination;
  return (
    <>
      <h3>Who may be paid</h3>
      {payment.form === "shares" ? (
        <ul>
          {payment.payees.map((payee) => (
            <li key={payee.party_id}>
              Pay <strong>{payee.party_id}</strong> {describeShare(payee.share)} of the balance.{" "}
              <Citations items={payee.citations} />
            </li>
          ))}
        </ul>
      ) : (
        <p>
          Payable to <strong>any one or more of {payment.party_ids.join(", ")}</strong>, as the
          account terms allow. <Citations items={payment.citations} />
        </p>
      )}
      <h3>Documents to collect first</h3>
      {required_documents.length ? (
        <ul>
          {required_documents.map((document) => (
            <li key={document.code}>
              {humanizeCode(document.code)}{" "}
              {document.source === "policy" ? (
                <span className="cite">(institution policy)</span>
              ) : (
                <Citations items={document.citations} />
              )}
            </li>
          ))}
        </ul>
      ) : (
        <p>No documents are required by statute.</p>
      )}
      <h3>Earliest payment date</h3>
      <p>
        <strong>{release_date.earliest}</strong>
        {release_date.policy_days_added
          ? `, including ${release_date.policy_days_added} days added by institution policy`
          : ""}
        . <Citations items={release_date.citations} />
      </p>
      <h3>Liability protection</h3>
      <p>
        {liability_protection.applies
          ? "Statutory protection applies if you pay as decided."
          : "No statutory protection applies to this payment."}{" "}
        <Citations items={liability_protection.citations} />
      </p>
    </>
  );
}

export function Result(props: {
  response: EvaluateResponse;
  facts: Record<string, unknown>;
  onEdit: () => void;
}) {
  const { decision } = props.response;
  const determined = decision.outcome === "determined" && decision.determination !== null;
  return (
    <section className="result" aria-live="polite">
      <h2 className={determined ? "ok" : "warn"}>
        {determined ? "Decision" : "Not determinable: send for manual review"}
      </h2>
      {determined && decision.determination ? (
        <DeterminationView determination={decision.determination} />
      ) : (
        <ul className="reasons">
          {decision.reasons.map((code) => {
            const reason = explainReason(code);
            return (
              <li key={code}>
                <strong>{reason.meaning}</strong>
                <br />
                Next step: {reason.nextStep}
              </li>
            );
          })}
        </ul>
      )}
      <h3>Record</h3>
      <dl className="record">
        <dt>Rules</dt>
        <dd>
          {decision.rule_set
            ? `${decision.rule_set.jurisdiction} ${decision.rule_set.version}`
            : "No rule set applied"}
        </dd>
        <dt>Institution policy</dt>
        <dd>
          {decision.policy.institution} {decision.policy.version}
        </dd>
        <dt>Facts fingerprint</dt>
        <dd>
          <code>{props.response.facts_hash.slice(0, 16)}…</code>
        </dd>
        <dt>Engine</dt>
        <dd>{props.response.engine_version}</dd>
      </dl>
      <div className="actions no-print">
        <button type="button" onClick={() => downloadRecord(props.response, props.facts)}>
          Download record (JSON)
        </button>
        <button type="button" onClick={() => window.print()}>
          Print / save as PDF
        </button>
        <button type="button" className="link" onClick={props.onEdit}>
          Edit facts
        </button>
      </div>
    </section>
  );
}
