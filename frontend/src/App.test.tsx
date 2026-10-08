import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { App } from "./App";
import { buildRecord } from "./Result";
import type { EvaluateResponse } from "./types";

const META = {
  engine_version: "0.1.0",
  facts_schema_version: "4",
  decision_schema_version: "2",
  registry_hash: "a".repeat(64),
  policies: [
    { id: "baseline", institution: "baseline", version: "1.0.0", description: "Statutory baseline." },
    { id: "test-bank", institution: "test-bank", version: "2.0.0", description: "Adds five days." },
  ],
};

const DETERMINED: EvaluateResponse = {
  engine_version: "0.1.0",
  facts_hash: "f".repeat(64),
  decision: {
    schema_version: "2",
    outcome: "determined",
    reasons: [],
    determination: {
      payment: {
        form: "shares",
        payees: [{ party_id: "P1", share: "1/1", citations: ["Test Code § 1"] }],
      },
      required_documents: [
        { code: "DEATH_CERTIFICATE", source: "statute", citations: ["Test Code § 2"] },
        { code: "BANK_FORM", source: "policy", citations: [] },
      ],
      release_date: { earliest: "2026-03-06", citations: ["Test Code § 3"], policy_days_added: 5 },
      liability_protection: { applies: true, citations: ["Test Code § 4"] },
    },
    rule_set: { jurisdiction: "CA", version: "1.0.0", content_hash: "b".repeat(64) },
    policy: { institution: "test-bank", version: "2.0.0", content_hash: "c".repeat(64) },
    registry_hash: "a".repeat(64),
  },
};

const NOT_DETERMINABLE: EvaluateResponse = {
  ...DETERMINED,
  decision: {
    ...DETERMINED.decision,
    outcome: "not_determinable",
    reasons: ["unsupported_jurisdiction"],
    determination: null,
    rule_set: null,
  },
};

function mockFetch(evaluate: () => Response) {
  const fetchMock = vi.fn((url: string) =>
    Promise.resolve(url === "/v1/meta" ? Response.json(META) : evaluate()),
  );
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

afterEach(() => {
  vi.unstubAllGlobals();
});

async function goToReview(user: ReturnType<typeof userEvent.setup>) {
  await user.click(screen.getByRole("button", { name: /5\. Review/ }));
}

test("a full case can be entered and decided", async () => {
  const fetchMock = mockFetch(() => Response.json(DETERMINED));
  const user = userEvent.setup();
  render(<App />);

  await user.type(screen.getByLabelText("Date of death"), "2026-01-15");
  await user.click(screen.getByRole("button", { name: "Next" }));
  await user.click(screen.getByRole("button", { name: "Add person" }));
  await user.click(screen.getByRole("button", { name: "Next" }));
  await user.type(screen.getByLabelText("Balance (USD)"), "1000.00");
  await user.click(screen.getByRole("button", { name: "Next" }));
  await user.click(screen.getByRole("button", { name: "Add affiant" }));
  await user.click(screen.getByRole("button", { name: "Next" }));

  await user.selectOptions(await screen.findByLabelText("Institution policy"), "test-bank");
  await user.click(screen.getByRole("button", { name: "Get decision" }));

  expect(await screen.findByRole("heading", { name: "Decision" })).toBeInTheDocument();
  expect(screen.getByText(/1\/1 \(100%\)/)).toBeInTheDocument();
  expect(screen.getByText("Bank form")).toBeInTheDocument();
  expect(screen.getByText(/including 5 days added by institution policy/)).toBeInTheDocument();
  expect(screen.getByText("test-bank 2.0.0")).toBeInTheDocument();

  const [, init] = fetchMock.mock.calls.find(([url]) => url === "/v1/evaluate") as unknown as [string, RequestInit];
  const sent = JSON.parse(init.body as string) as { policy: string; facts: { parties: unknown[] } };
  expect(sent.policy).toBe("test-bank");
  expect(sent.facts.parties).toEqual([{ party_id: "P1", relationship: "child" }]);

  await user.click(screen.getByRole("button", { name: "Edit facts" }));
  expect(screen.getByRole("heading", { name: "Review and decide" })).toBeInTheDocument();
});

test("a not-determinable result explains why and what to do next", async () => {
  mockFetch(() => Response.json(NOT_DETERMINABLE));
  const user = userEvent.setup();
  render(<App />);
  await goToReview(user);
  await user.click(screen.getByRole("button", { name: "Get decision" }));
  expect(await screen.findByText(/no approved rules for this state/)).toBeInTheDocument();
  expect(screen.getByText(/Next step: Send the case to a specialist/)).toBeInTheDocument();
  expect(screen.getByText("No rule set applied")).toBeInTheDocument();
});

test("validation errors jump to the step that owns the field", async () => {
  mockFetch(() =>
    Response.json({ errors: [{ loc: ["facts", "account", "balance"], type: "value_error" }] }, { status: 422 }),
  );
  const user = userEvent.setup();
  render(<App />);
  await goToReview(user);
  await user.click(screen.getByRole("button", { name: "Get decision" }));
  const alert = await screen.findByRole("alert");
  expect(within(alert).getByText("account › balance: Value error")).toBeInTheDocument();
  expect(screen.getByRole("group", { name: "Account" })).toBeInTheDocument();
});

test("service failures are reported without crashing", async () => {
  mockFetch(() => new Response("{}", { status: 500 }));
  const user = userEvent.setup();
  render(<App />);
  await goToReview(user);
  await user.click(screen.getByRole("button", { name: "Get decision" }));
  expect(await screen.findByText(/returned an error \(500\)/)).toBeInTheDocument();
});

test("unknown policy and unreachable service are explained", async () => {
  mockFetch(() => new Response("{}", { status: 404 }));
  const user = userEvent.setup();
  render(<App />);
  await goToReview(user);
  await user.click(screen.getByRole("button", { name: "Get decision" }));
  expect(await screen.findByText(/policy is not available/)).toBeInTheDocument();

  vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("offline"))));
  await user.click(screen.getByRole("button", { name: "Get decision" }));
  expect(await screen.findByText(/could not be reached/)).toBeInTheDocument();
});

test("the record contains facts, decision, and versions", () => {
  const record = JSON.parse(buildRecord(DETERMINED, { jurisdiction: "CA" }, new Date("2026-03-01T00:00:00Z")));
  expect(record).toMatchObject({
    record_version: 1,
    generated_at: "2026-03-01T00:00:00.000Z",
    engine_version: "0.1.0",
    facts_hash: "f".repeat(64),
    facts: { jurisdiction: "CA" },
    decision: { outcome: "determined" },
  });
});

test("case data is never written to browser storage", async () => {
  mockFetch(() => Response.json(DETERMINED));
  const setItem = vi.spyOn(Storage.prototype, "setItem");
  const user = userEvent.setup();
  render(<App />);
  await goToReview(user);
  await user.click(screen.getByRole("button", { name: "Get decision" }));
  await screen.findByRole("heading", { name: "Decision" });
  expect(setItem).not.toHaveBeenCalled();
});
