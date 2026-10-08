// Plain-English text for engine codes. Every ReasonCode in the engine must appear here;
// tests/test_ui_sync.py fails the build if one is missing.

export interface ReasonExplanation {
  meaning: string;
  nextStep: string;
}

export const REASONS: Record<string, ReasonExplanation> = {
  unsupported_jurisdiction: {
    meaning: "There are no approved rules for this state yet.",
    nextStep:
      "Send the case to a specialist for manual review. California and Washington rules are awaiting attorney approval.",
  },
  no_rule_set_for_date_of_death: {
    meaning: "No approved rules cover a death on this date.",
    nextStep: "Check the date of death. If it is correct, send the case for manual review.",
  },
  fact_pattern_not_covered: {
    meaning: "The approved rules do not cover this combination of facts.",
    nextStep:
      "Check the facts you entered. If they are correct, send the case for manual review.",
  },
  policy_declined: {
    meaning: "Your institution's policy sends cases like this to manual review.",
    nextStep: "Follow your institution's manual review procedure.",
  },
};

export function explainReason(code: string): ReasonExplanation {
  return (
    REASONS[code] ?? {
      meaning: `The engine could not decide (${code}).`,
      nextStep: "Send the case for manual review.",
    }
  );
}

/** "DEATH_CERTIFICATE" → "Death certificate". */
export function humanizeCode(code: string): string {
  const words = code.toLowerCase().replaceAll("_", " ");
  return words.charAt(0).toUpperCase() + words.slice(1);
}

/** "1/3" → "1/3 (33.33%)". */
export function describeShare(share: string): string {
  const [numerator, denominator] = share.split("/").map(Number);
  if (!numerator || !denominator) return share;
  const percent = Math.round((numerator / denominator) * 10000) / 100;
  return `${share} (${percent}%)`;
}

export const STEP_FOR_FIELD: Record<string, number> = {
  jurisdiction: 0,
  date_of_death: 0,
  as_of_date: 0,
  decedent_resident_of_jurisdiction: 0,
  parties: 1,
  account: 2,
  estate: 3,
};

export function stepForError(loc: (string | number)[]): number {
  const field = loc[0] === "facts" ? loc[1] : loc[0];
  return typeof field === "string" ? (STEP_FOR_FIELD[field] ?? 0) : 0;
}
