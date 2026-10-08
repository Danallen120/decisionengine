import { useEffect, useState, type JSX } from "react";
import { evaluateCase, fetchMeta } from "./api";
import { stepForError } from "./explain";
import { emptyCase, localToday, toFacts } from "./facts";
import { SelectField, label } from "./fields";
import { Result } from "./Result";
import { AccountStep, CaseStep, EstateStep, PeopleStep, type StepProps } from "./steps/Steps";
import type { EvaluateResponse, FieldError, Meta } from "./types";

const STEPS: { title: string; Component: (props: StepProps) => JSX.Element }[] = [
  { title: "Case", Component: CaseStep },
  { title: "People", Component: PeopleStep },
  { title: "Account", Component: AccountStep },
  { title: "Estate", Component: EstateStep },
];
const REVIEW_STEP = STEPS.length;

function describeError(error: FieldError): string {
  const path = error.loc.filter((part) => part !== "facts").join(" › ");
  return `${path || "request"}: ${label(error.type)}`;
}

export function App() {
  const [form, setForm] = useState(() => emptyCase(localToday()));
  const [step, setStep] = useState(0);
  const [meta, setMeta] = useState<Meta | null>(null);
  const [metaError, setMetaError] = useState("");
  const [policy, setPolicy] = useState("baseline");
  const [errors, setErrors] = useState<FieldError[]>([]);
  const [failure, setFailure] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<{ response: EvaluateResponse; facts: Record<string, unknown> } | null>(null);

  useEffect(() => {
    fetchMeta()
      .then(setMeta)
      .catch(() => setMetaError("The decision service could not be reached."));
  }, []);

  const submit = async () => {
    setSubmitting(true);
    setErrors([]);
    setFailure("");
    const facts = toFacts(form);
    const outcome = await evaluateCase(policy, facts);
    setSubmitting(false);
    if (outcome.kind === "ok") {
      setResult({ response: outcome.response, facts });
    } else if (outcome.kind === "invalid") {
      setErrors(outcome.errors);
      const first = outcome.errors[0];
      if (first) setStep(stepForError(first.loc));
    } else {
      setFailure(outcome.message);
    }
  };

  if (result) {
    return (
      <main>
        <Header meta={meta} />
        <Result response={result.response} facts={result.facts} onEdit={() => setResult(null)} />
      </main>
    );
  }

  const current = STEPS[step];
  const stepErrors = errors.filter((error) => stepForError(error.loc) === step);
  return (
    <main>
      <Header meta={meta} />
      {metaError ? <p className="error" role="alert">{metaError}</p> : null}
      <nav aria-label="Steps">
        <ol className="steps">
          {[...STEPS.map((s) => s.title), "Review"].map((title, index) => (
            <li key={title}>
              <button
                type="button"
                className={index === step ? "current" : "link"}
                aria-current={index === step ? "step" : undefined}
                onClick={() => setStep(index)}
              >
                {index + 1}. {title}
              </button>
            </li>
          ))}
        </ol>
      </nav>
      {stepErrors.length ? (
        <div className="error" role="alert">
          <p>Please correct these fields:</p>
          <ul>
            {stepErrors.map((error) => (
              <li key={error.loc.join(".")}>{describeError(error)}</li>
            ))}
          </ul>
        </div>
      ) : null}
      {current ? (
        <current.Component form={form} setForm={setForm} />
      ) : (
        <section>
          <h2>Review and decide</h2>
          <SelectField
            label="Institution policy"
            value={policy}
            options={meta ? meta.policies.map((p) => p.id) : ["baseline"]}
            describe={(id) => {
              const option = meta?.policies.find((p) => p.id === id);
              return option ? `${option.institution} ${option.version}: ${option.description}` : id;
            }}
            onChange={setPolicy}
          />
          <pre className="facts" aria-label="Facts to submit">
            {JSON.stringify(toFacts(form), null, 2)}
          </pre>
          {failure ? <p className="error" role="alert">{failure}</p> : null}
          <button type="button" className="primary" onClick={() => void submit()} disabled={submitting}>
            {submitting ? "Deciding…" : "Get decision"}
          </button>
        </section>
      )}
      <div className="actions">
        <button type="button" disabled={step === 0} onClick={() => setStep(step - 1)}>
          Back
        </button>
        <button type="button" disabled={step === REVIEW_STEP} onClick={() => setStep(step + 1)}>
          Next
        </button>
      </div>
    </main>
  );
}

function Header({ meta }: { meta: Meta | null }) {
  return (
    <header>
      <h1>Deceased account decision</h1>
      <p className="hint">
        Local tool. Enter facts only: no names, account numbers, or other personal information.
        {meta ? ` Engine ${meta.engine_version}.` : ""}
      </p>
    </header>
  );
}
