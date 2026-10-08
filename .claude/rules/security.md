# Security Rules

Owns: security controls that code must enforce. System shape and contracts are in `ARCHITECTURE.md`, and workflow is in `CLAUDE.md`. The repo is early-stage, so all rules are provisional.

## Required Security Inputs

Stack, auth model, data store, and PII posture come from `ARCHITECTURE.md`. Security-specific inputs that are still open:

| Input | Status |
|---|---|
| Human authentication | UNKNOWN (see ARCHITECTURE.md open questions) |
| Secrets manager | UNKNOWN (depends on deployment) |
| Rate limits, payload-size and batch-size caps | TO BE DECIDED |

## Provisional Security Rules

### Decision path
- No LLM or other model calls, network calls, or randomness anywhere in the decision path.
- No `eval`/`exec`, dynamic imports, `pickle`, or unsafe `yaml.load` on any input, rule file, or fixture. Use `json` or `yaml.safe_load` only.
- Facts outside the rules fail closed. Never fall back to a default rule set. (Whether "fail closed" is an error or an explicit "undecidable" result is an open question in ARCHITECTURE.md.)

### Rule integrity
- Rule changes go to `main` only through reviewed PRs. Enable branch protection (PR + review required, no force-push) before rules land.
- A decision without a rule version and rule-set hash is invalid, and tests assert that both are present.

### No PII by design
- Fact schemas have no fields for names, SSNs/TINs, account numbers, addresses, or DOB. Parties are identified by role (for example, `surviving_spouse`, `child_1`).
- No free-text fields in fact schemas. If one is ever unavoidable, it gets a bounded length, an allowlist pattern, and tests that SSN-like and account-number-like values are rejected.
- Never log request bodies, facts, decisions, or API keys. Log the facts hash, rule version, request ID, outcome code, and latency only. Always redact the `Authorization` header.

### Input validation (Pydantic is the trust boundary)
- Every model that parses external input uses `extra="forbid"`, so unknown fields are rejected with 422, not dropped. Decision-relevant numbers, booleans, and dates also use `strict=True`.
- No `Any`, bare `dict`, or bare `list` at the boundary. Every string has a length bound, every number has range bounds, and constrained values are `Enum`s. Regexes are anchored and linear-time.
- Request and response models are separate. Batch item count and total payload size are capped server-side.

### HTTP boundary
- Auth is applied with a router-level `Depends()`, so new routes are denied by default.
- `/docs`, `/redoc`, and `/openapi.json` are off outside local dev.
- CORS is off until a UI exists. After that, allow exact origins only, and never `*` with credentials.
- Errors return a typed code plus a request ID. Never return stack traces, `str(e)`, rule internals, or SQL.
- Set these headers on every response: HSTS (on TLS), `X-Content-Type-Options: nosniff`, and `Referrer-Policy: no-referrer`. Decision responses also get `Cache-Control: no-store`.
- Apply per-key rate limits, body-size caps, and request timeouts.

### API keys
- Generate with `secrets.token_urlsafe(32)` or stronger and show the key once. Store only an HMAC-SHA256 hash keyed with a server-side secret.
- Accept keys only in the `Authorization` header. Compare with `secrets.compare_digest`.
- Revocation takes effect on the next request. Auth failures return 401, fail closed, and count as a security signal.
- Hold keys in config models as `SecretStr`.

### Persistence
- Parameterized queries or ORM builders only. Never build SQL from strings.
- The decision log is enforced append-only by grants: the runtime DB role has `INSERT` + `SELECT` only. Corrections are new rows.
- Run migrations with a separate privileged role. The runtime role has no DDL rights.

### Secrets and supply chain
- No secrets in source, fixtures, or committed config. Gitignore `.env*`.
- Pin dependencies with hashes. CI runs `pip-audit` and fails the build on known CVEs.
- CI never gets production DB or secret access.

## Prompt Placeholders To Resolve

| Placeholder | Resolution | Driven by |
|---|---|---|
| `{{CODE_QUALITY_PROMPT}}` | `~/Claude_Setup/Code_Security/Code Quality/00 General Code Quality Prompts.md` | Architecture (pure core, I/O at edges) |
| `{{API_SECURITY_PROMPT}}` | `~/Claude_Setup/Code_Security/Web and API Security/06 Secure API Developer.md` | Architecture (REST `/v1`) |
| `{{BACKEND_FRAMEWORK_PROMPT}}` | `~/Claude_Setup/Code_Security/Backend Frameworks/Python/` → `00 Secure Python Developer.md`, `03 Secure Fast API Developer.md`, `09 Secure Pydantic Developeer.md`. Add a persistence prompt (e.g. `05 Secure SQLAlchemy Developer.md`) once the library is chosen. | Backend: Python, FastAPI, Pydantic |
| `{{FRONTEND_FRAMEWORK_PROMPT}}` | `~/Claude_Setup/Code_Security/Client Side Frameworks/ReactJS/00 React19 Secure Generator (JS).md`. Deferred (no UI in v1); JS vs. TS is TO BE DECIDED. | Frontend: React (deferred) |
| `{{AUTH_PROMPT}}` | No dedicated prompt. v1 is API keys only (rules above). The OAuth/JWT guidance in the API and FastAPI prompts does not apply. | Auth: API keys |
| `{{DEPLOYMENT_PROMPT}}` | TO BE DECIDED. The library has no infrastructure prompt yet. | Deployment: TO BE DECIDED |
