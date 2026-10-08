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

Owns: system shape, contracts, and open design questions. Security controls live in `.claude/rules/security.md`, and workflow lives in `CLAUDE.md`.

### Layers (dependencies point inward only)

1. **Core engine**: `evaluate(facts, rules, policy) -> Decision`. It is pure and deterministic: no I/O, clock, randomness, network, or DB, and it imports only the standard library and Pydantic. Same facts + same rule set + same policy always give an identical decision. Rules and policy are loaded by an outer layer and passed in.
2. **Rules**: per-state rule sets, versioned in git. Each is cited YAML data plus pure Python logic (`state_logic`). The engine selects exactly one by jurisdiction + date of death; ranges may not overlap.
3. **CLI**: runs single, batch, and golden-suite evaluations. This is the v1 delivery path.
4. **API**: FastAPI `/v1` with single and batch endpoints. This is the only layer with auth or PostgreSQL.
5. **UI**: React, deferred.

### Contracts

- **Facts**: account and decedent facts, including jurisdiction and date of death. Every date the engine uses (including the as-of date) is a fact, never read from the clock. Account terms are facts too: account type (sole, joint, POD, Totten trust), other holders by role with survivorship and any terms shares, signature requirements, payment-blocking events, and whether the institution issued an ownership instrument. Estate facts come from the affidavit: administration status (none / opened with the personal representative's consent / opened without consent), declared estate value, whether there is in-state real property, and the affiants with their capacity. Unknown values are `null`, never defaulted.
- **Decision**: outcome `determined` or `not_determinable`. A determined decision has a payment, either exact fractional shares summing to 1 or "any of" these parties per the account terms. It also has required documents (from statute, with citations, or from policy), the earliest release date (including any policy days), and liability-protection applicability. Every decision records the registry hash and the policy reference, plus the rule set (version + hash) when one was selected.
- **Institution policy**: a versioned, hashed file per institution for choices the statutes leave to the institution. It can only make decisions stricter (extra waiting days, extra documents, declining account types or balances above a limit); no field can relax a statutory condition. A packaged `baseline` policy adds nothing, and golden scenarios run against it.
- **Rule-set hash**: SHA-256 of the canonical JSON of the validated rule data. It covers data only, so any logic change must bump the version.
- **Decision log row** (API layer, append-only): facts hash, rule version, rule-set hash, policy reference, output, timestamp, API key ID. Raw facts are never stored.
- **API key**: stored hashed, revocable.

### Attorney-facing artifacts

For each state: a rule spec, an open-questions list, and a golden-scenario table. The golden-scenario table is the test suite.

### Assumptions (unconfirmed)

- **A1:** The attorney-facing artifacts live in the repo next to the rules, so attorneys review the same versions the code runs.
- **A2:** Batch evaluation is a loop over single evaluations, with no special batching logic.

### Decisions

- **Unsupported cases** (decided 2026-10-07, REQ-RULES-001): malformed input is a validation error. Valid facts outside rule coverage return `not_determinable` with reason codes, so operations routes them to a person. The engine never falls back to a default rule set.

- **Where answers come from** (decided 2026-10-07): each rule question is answered by law (attorney), account terms (facts), or institution policy (stricter-only). See `docs/rules/<state>/open-questions.md`.

### Open questions

- **Human authentication:** "human login until a UI exists" may mean *no* human login until a UI exists.
- **PII in logged output:** decision output (payees) may identify people, which would conflict with "no PII stored".
- **Effective dates:** what is the date-of-death boundary for each rule set version?
