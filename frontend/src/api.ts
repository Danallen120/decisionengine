import type { EvaluateResponse, FieldError, Meta } from "./types";

export type EvaluateResult =
  | { kind: "ok"; response: EvaluateResponse }
  | { kind: "invalid"; errors: FieldError[] }
  | { kind: "failed"; message: string };

export async function fetchMeta(): Promise<Meta> {
  const response = await fetch("/v1/meta");
  if (!response.ok) throw new Error(`meta request failed (${response.status})`);
  return (await response.json()) as Meta;
}

export async function evaluateCase(
  policy: string,
  facts: Record<string, unknown>,
): Promise<EvaluateResult> {
  let response: Response;
  try {
    response = await fetch("/v1/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ policy, facts }),
    });
  } catch {
    return { kind: "failed", message: "The decision service could not be reached." };
  }
  if (response.ok) {
    return { kind: "ok", response: (await response.json()) as EvaluateResponse };
  }
  if (response.status === 422) {
    const body = (await response.json()) as { errors?: FieldError[] };
    return { kind: "invalid", errors: body.errors ?? [] };
  }
  if (response.status === 404) {
    return { kind: "failed", message: "That institution policy is not available." };
  }
  return { kind: "failed", message: `The decision service returned an error (${response.status}).` };
}
