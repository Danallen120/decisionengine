# Security Rules

Source of truth for system shape: `ARCHITECTURE.md`. The repo is early-stage (no code yet), so the rules below are provisional defaults grounded only in that file and in the selected prompts.

## Required Security Inputs

| Input | Value | Source |
|---|---|---|
| Runtime | Python. Pure core library + CLI + thin FastAPI `/v1` layer | ARCHITECTURE.md |
| Schemas / validation boundary | Pydantic (facts in, decision out) | ARCHITECTURE.md |
| Client | React. Deferred; no UI in v1 | ARCHITECTURE.md |
| Auth (v1) | API keys: hashed at rest, revocable | ARCHITECTURE.md |
| Human auth | UNKNOWN. "human login until a UI exists" is ambiguous (see ARCHITECTURE.md open questions) | ARCHITECTURE.md |
| Data store | PostgreSQL (API layer only): append-only decision log + API keys | ARCHITECTURE.md |
| PII posture | None collected or stored, by design | ARCHITECTURE.md |
| Deployment / hosting | TO BE DECIDED | ARCHITECTURE.md |
| CI/CD platform | UNKNOWN (GitHub repo exists; no pipeline yet) | repo state |
| Secrets manager | UNKNOWN (depends on deployment) | — |
| Rate-limit and payload-size thresholds | TO BE DECIDED (scale expected low) | ARCHITECTURE.md |

## Provisional Security Rules

### Deterministic core (decision path)
- The core engine does no I/O: no network, filesystem, DB, subprocess, or environment reads.
- No randomness, no system clock, and no LLM or other model calls anywhere in the decision path. Any date the engine needs (for example, an as-of date or the date of death) comes in as a fact.
- Same facts + same rule version must give a byte-identical decision. Golden-scenario tests enforce this.
- The core may import Pydantic and the standard library only. Never FastAPI, a DB driver, an HTTP client, or a logging sink.
- No `eval`/`exec`, dynamic imports, `pickle`, or unsafe `yaml.load` on any input, rule file, or fixture. Rule data is loaded with safe parsers only (`json`, `yaml.safe_load`).

### Rule integrity
- Rules change only through reviewed PRs. Never commit rule changes directly to `main`.
- Every decision records the rule version and a content hash of the rule set used.
- Rule-set selection (by jurisdiction + date of death) is explicit and tested. An unsupported jurisdiction or date fails closed with a typed error; it never falls back to a default rule set.
- Each rule change ships with matching golden-scenario updates and citations in the same PR.

### No PII by design
- Fact schemas contain no fields for names, SSNs/TINs, account numbers, addresses, or DOB. Identify parties by role or relationship (for example, `surviving_spouse`, `child_1`), never by name.
- `extra="forbid"` on every input model, so unexpected PII-bearing fields are rejected at the boundary with 422, not silently dropped.
- Free-text fields are not allowed in fact schemas. If one is ever unavoidable, it gets a bounded length, an allowlist pattern, and a test that SSN-like and account-number-like values are rejected.
- Never log raw request bodies, facts, or decisions. Log a facts hash, rule version, request ID, outcome code, and latency only.

### Input validation (Pydantic as the trust boundary)
- Every model that parses external input sets `extra="forbid"`. Decision-relevant numbers, booleans, and dates also use `strict=True`, so `"1"` never becomes `True`.
- No `Any`, bare `dict`, or bare `list` on a trust boundary. Every string has `min_length`/`max_length`, every number has bounds, and constrained values are `Enum`s (jurisdiction, relationship, account type).
- Regex patterns are anchored and linear-time (no nested quantifiers).
- Separate request and response models. Never serialize internal objects directly.
- Batch endpoints cap the item count and total payload size, both enforced server-side.

### HTTP boundary (FastAPI layer)
- All routes are under `/v1`. Auth is applied through a router-level `Depends()`, so a new route cannot ship unauthenticated. Deny by default.
- Disable `/docs`, `/redoc`, and `/openapi.json` outside local dev, or put them behind auth.
- CORS stays off until a UI exists. After that, allow exact origins only and never use `*` with credentials.
- Set request body size caps, request timeouts, and per-API-key rate limits (thresholds TO BE DECIDED).
- Error responses are generic: a typed error code plus a request ID. No stack traces, `str(e)`, rule internals, or SQL fragments.
- Set security headers on every response: HSTS (once on TLS), `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, and `Cache-Control: no-store` on decision responses.

### Authentication (API keys)
- Generate keys with `secrets.token_urlsafe(32)` or stronger, show them once, and store only a hash. Keys are high-entropy, so a fast keyed hash (HMAC-SHA256 with a server-side secret) is acceptable.
- Accept keys only in the `Authorization` header, never in query strings, paths, or bodies.
- Compare with `secrets.compare_digest`. Revocation takes effect on the next request.
- Each key is bound to an owning client identity, which is recorded (by key ID, never the key itself) in the decision log.
- Never log, echo, or return a key after creation. Hold keys in config models as `SecretStr`.
- Auth failures fail closed (401) and are counted as a security signal.

### Persistence (API layer only)
- Use parameterized queries or ORM builders only. Never f-string or concatenate SQL.
- The decision log is append-only. The app's DB role has `INSERT` + `SELECT` on it and no `UPDATE`, `DELETE`, or `TRUNCATE`. Corrections are new rows, never edits.
- Each log row holds: facts hash, rule version, rule hash, output, timestamp, key ID. Storing output must stay PII-free (see open question in ARCHITECTURE.md).
- Run migrations with a separate, privileged role. The runtime role has no DDL rights.

### Secrets
- No secrets in source, committed config, fixtures, or logs. `.env*` files are gitignored.
- Load secrets from environment variables now, and from a secrets manager once deployment is decided (UNKNOWN).

### Error handling and logging
- Use specific, domain-typed errors (for example, `UnsupportedJurisdictionError`, `InsufficientFactsError`). No bare `except`, and no swallowed exceptions.
- Use structured (JSON) logs with an explicit field allowlist and a request ID on every line. Redact the `Authorization` header always.

### Supply chain and CI/CD
- Pin dependencies with hashes in a lockfile (tool TO BE DECIDED). Run `pip-audit` in CI and fail the build on known CVEs.
- CI runs the golden-scenario suite on every PR, and a failing scenario blocks merge.
- Protect `main`: PR required, review required for rule and schema changes, no force-push. Pipeline platform UNKNOWN.
- CI never has production DB or secret access. Deployment pipeline rules are TO BE DECIDED.

## Prompt Placeholders To Resolve

| Placeholder | Resolution | Status |
|---|---|---|
| `{{CODE_QUALITY_PROMPT}}` | `~/Claude_Setup/Code_Security/Code Quality/00 General Code Quality Prompts.md` | Resolved |
| `{{API_SECURITY_PROMPT}}` | `~/Claude_Setup/Code_Security/Web and API Security/06 Secure API Developer.md` | Resolved |
| `{{BACKEND_FRAMEWORK_PROMPT}}` | `~/Claude_Setup/Code_Security/Backend Frameworks/Python/00 Secure Python Developer.md`, `.../03 Secure Fast API Developer.md`, `.../09 Secure Pydantic Developeer.md` | Resolved (stack named in ARCHITECTURE.md) |
| `{{FRONTEND_FRAMEWORK_PROMPT}}` | `~/Claude_Setup/Code_Security/Client Side Frameworks/ReactJS/00 React19 Secure Generator (JS).md` | Mapped, but deferred: no UI in v1. JS vs. TS is TO BE DECIDED. |
| `{{AUTH_PROMPT}}` | No dedicated prompt. v1 auth is API keys only (per ARCHITECTURE.md): generate with a CSPRNG, store only a hash, compare in constant time, support revocation, never log keys. Human login deferred until a UI exists. | Resolved inline |
| `{{DEPLOYMENT_PROMPT}}` | TO BE DECIDED | Unresolved: deployment model not chosen |

## Selected Prompt Imports

- **Architecture decisions** (functional core, stateless, deterministic): Code Quality 00. Use its pure core / I/O at the edges, injected clock, and typed errors guidance.
- **Backend framework** (Python + FastAPI + Pydantic): Python 00, FastAPI 03, Pydantic 09, and API Security 06. Persistence library (for example, SQLAlchemy 05) is UNKNOWN until an ORM or driver is chosen.
- **Frontend framework** (React, deferred): React 00 (JS). Not active in v1.
- **Auth model** (API keys): inline rules above plus the API-key and BOLA/BFLA sections of API Security 06. The OAuth/JWT guidance in 06 and 03 does not apply in v1.
- **Deployment model**: UNRESOLVED (TO BE DECIDED). No infrastructure prompt exists in the library yet (`Infrastucture/` is empty).
