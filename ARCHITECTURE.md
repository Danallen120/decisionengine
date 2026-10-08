# Architecture

## Required Architecture Inputs

- System purpose: Deterministic, statute-cited entitlement decision engine for deceased customers' financial accounts - given account facts, decides who may legally be paid and in what shares, what documents are required, the earliest release date, and whether statutory liability protection applies. v1 jurisdictions: California and Washington.
- Primary use cases: (1) evaluate a single account's facts and return a cited decision; (2) evaluate a batch of fact sets, including the golden-scenario suite; (3) produce attorney-reviewable documentation: a plain-English rule spec per state with citations, an open-questions list per state, and a golden-scenario table (facts -> expected decision -> citation) that doubles as the test suite
- Target users / actors: operations and compliance staff at financial institutions who submit account facts and receive decisions; API clients (integrating systems); reviewing attorneys, who review the rule specs and golden scenarios, not the code
- Runtime environment: web
- Server framework: python — pure-Python core library (no I/O, no framework dependencies) plus a thin FastAPI wrapper as a separate layer; Pydantic for fact and decision schemas
- Client framework: react - deferred; no UI in v1 (library, CLI, and API first)
- API style and integration model: REST, synchronous, stateless (facts in, decision out); single and batch evaluation endpoints; versioned (/v1); also importable as a Python package
- Authentication and session model: standard — API keys (hashed at rest, revocable) for API clients; human login until a UI exists
- Data model expectations: RDBMS (PostgreSQL) for the API layer only — append-only decision log (input facts hash, rule version, output, timestamp) for audit and reproducibility, plus API keys. The core engine is stateless; rules are versioned code/data in git, selected by the decedent's date of death. No PII collected or stored by design.
- Deployment model: TO BE DECIDED - not needed for v1 (library + CLI run locally)
- Scale expectations: TO BE DECIDED - expected low; stateless design scales horizontally if needed, so do not optimize for scale in v1

## Initial Architecture (Provisional)

Nothing is implemented yet. This section shows the intended design, based only on the inputs above.

### Layers (dependencies point inward only)

1. **Core engine** (pure Python package). `evaluate(facts) -> Decision`. It has no I/O, no clock reads, no randomness, no network or DB access, and no framework imports except Pydantic. The same facts and the same rule version always give the same decision.
2. **Rules** (versioned code/data in git, one rule set per state). The engine selects a rule set by jurisdiction and the decedent's date of death. Every decision output cites a statute.
3. **CLI**. A thin wrapper around the core that evaluates one fact set, evaluates a batch, and runs the golden-scenario suite. It runs locally; this is the v1 delivery path.
4. **API** (FastAPI, `/v1`). A thin wrapper around the core with single and batch evaluation endpoints, synchronous and stateless. This is the only layer that touches PostgreSQL or handles auth.
5. **UI** (React). Deferred, not in v1.

### Core contracts

- **Facts** (Pydantic). Account and decedent facts the engine needs, including jurisdiction and date of death.
- **Decision** (Pydantic). Payees and shares, required documents, earliest release date, liability-protection applicability, rule version, and a statute citation for each conclusion.
- **Rule version**. Every decision records the rule version it used, so decisions can be reproduced.

### Persistence (API layer only)

- **Decision log**, append-only: input facts hash, rule version, output, timestamp.
- **API keys**: stored hashed, revocable.
- The core engine and CLI have no persistence.

### Attorney-facing artifacts (part of the system)

For each state there is a plain-English rule spec with citations, an open-questions list, and a golden-scenario table (facts -> expected decision -> citation). The golden-scenario table is the test suite, so the scenarios and the rules must not drift apart.

### Assumptions (unconfirmed)

- **A1:** The rule spec, open questions, and golden scenarios are files kept in the repo next to the rules, so attorneys review the same versions the code runs.
- **A2:** Only the facts hash goes in the decision log. The raw facts are not logged, which is consistent with "no PII stored".
- **A3:** Batch evaluation is a loop over single evaluations in the core, with no special batching logic.
- **A4:** "Earliest release date" is computed from dates supplied in the facts, never from the system clock, which keeps the engine deterministic.

### Open questions / unknowns

- **Deployment model:** TO BE DECIDED.
- **Scale targets:** TO BE DECIDED (expected low).
- **Human authentication:** the input says "human login until a UI exists". Does this mean *no* human login until a UI exists? It needs clarifying.
- **PII and the output log:** do account facts (for example, heir names) contain PII by nature? If so, logging the decision *output* may conflict with "no PII stored".
- **Unsupported or ambiguous cases:** how does the engine report a jurisdiction, date range, or fact pattern the rules don't cover (an explicit "undecidable" result vs. an error)?
- **Rule set by date of death:** what is the effective-date boundary for each rule set version?
