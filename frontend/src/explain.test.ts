import { describeShare, explainReason, humanizeCode, REASONS, stepForError } from "./explain";

test("every known reason has a meaning and a next step", () => {
  for (const reason of Object.values(REASONS)) {
    expect(reason.meaning).not.toBe("");
    expect(reason.nextStep).not.toBe("");
  }
});

test("unknown reason codes still get a safe explanation", () => {
  expect(explainReason("something_new").nextStep).toMatch(/manual review/);
});

test("codes and shares read as plain English", () => {
  expect(humanizeCode("DEATH_CERTIFICATE")).toBe("Death certificate");
  expect(describeShare("1/3")).toBe("1/3 (33.33%)");
  expect(describeShare("bad")).toBe("bad");
});

test("validation errors map to the step that owns the field", () => {
  expect(stepForError(["facts", "date_of_death"])).toBe(0);
  expect(stepForError(["facts", "parties", 0, "party_id"])).toBe(1);
  expect(stepForError(["facts", "account", "balance"])).toBe(2);
  expect(stepForError(["facts", "estate", "affiants"])).toBe(3);
  expect(stepForError(["policy"])).toBe(0);
  expect(stepForError([0])).toBe(0);
});
