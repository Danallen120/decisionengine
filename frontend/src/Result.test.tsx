import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Result } from "./Result";
import type { EvaluateResponse } from "./types";

const BASE: EvaluateResponse = {
  engine_version: "0.1.0",
  facts_hash: "f".repeat(64),
  decision: {
    schema_version: "2",
    outcome: "determined",
    reasons: [],
    determination: {
      payment: { form: "any_of", party_ids: ["P1", "P2"], citations: ["RCW 30A.22.140"] },
      required_documents: [],
      release_date: { earliest: "2026-02-01", citations: ["RCW 30A.22.160"], policy_days_added: 0 },
      liability_protection: { applies: false, citations: ["RCW 30A.22.120"] },
    },
    rule_set: { jurisdiction: "WA", version: "1.0.0", content_hash: "b".repeat(64) },
    policy: { institution: "baseline", version: "1.0.0", content_hash: "c".repeat(64) },
    registry_hash: "a".repeat(64),
  },
};

test("any-of payments, no documents, and no protection read clearly", () => {
  render(<Result response={BASE} facts={{}} onEdit={() => undefined} />);
  expect(screen.getByText(/any one or more of P1, P2/)).toBeInTheDocument();
  expect(screen.getByText("No documents are required by statute.")).toBeInTheDocument();
  expect(screen.getByText(/No statutory protection applies/)).toBeInTheDocument();
  expect(screen.getByText("WA 1.0.0")).toBeInTheDocument();
});

test("download and print actions work", async () => {
  const createObjectURL = vi.fn(() => "blob:record");
  const revokeObjectURL = vi.fn();
  vi.stubGlobal("URL", { ...URL, createObjectURL, revokeObjectURL });
  const click = vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => undefined);
  const print = vi.spyOn(window, "print").mockImplementation(() => undefined);
  const user = userEvent.setup();
  render(<Result response={BASE} facts={{ jurisdiction: "WA" }} onEdit={() => undefined} />);

  await user.click(screen.getByRole("button", { name: "Download record (JSON)" }));
  expect(createObjectURL).toHaveBeenCalledOnce();
  expect(click).toHaveBeenCalledOnce();
  expect(revokeObjectURL).toHaveBeenCalledWith("blob:record");

  await user.click(screen.getByRole("button", { name: /Print/ }));
  expect(print).toHaveBeenCalledOnce();
  vi.unstubAllGlobals();
});
