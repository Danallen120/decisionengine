# CLAUDE.md

@ARCHITECTURE.md

Owns: how to work in this repo. System design is in `ARCHITECTURE.md` (imported above). Security controls are in `.claude/rules/security.md`, which loads automatically.

## Status

Foundation built: schemas, engine, rule loading, golden runner, CLI, and CI. No state rules exist yet, so every decision is `not_determinable`. If a task depends on an undecided item (see the table below or the ARCHITECTURE.md open questions), ask instead of picking.

## Legal-rule guardrails

- **Never invent law.** Every rule must cite a real, verifiable statute. If the law or a citation is uncertain, add an open-questions entry for that state and do not encode a guess.
- **Golden scenarios are the spec.** Every rule change ships with its citation and matching golden-scenario updates in the same PR. Never change an expected decision just to make a test pass. If the test looks wrong, raise it for attorney review.
- **Write for attorneys.** Rule specs, open questions, and golden-scenario tables must be plain English and readable without the code.
- **Don't widen v1 scope.** No new jurisdictions, UI, or deployment work unless a requirement asks for it.

## Workflow

- **Use a branch and PR for every change.** Never commit to `main`. PRs reference the requirement ID(s) they implement.
- **Plan first for high-risk areas.** Before changing the core engine, rule sets, fact/decision schemas, or the decision log, state the plan and wait for confirmation.
- **Every new GitHub issue MUST use the requirement template** (`.github/ISSUE_TEMPLATE/requirement.yml`), so each issue is a structured, testable requirement: a `REQ-<MODULE>-<###>` ID, an RFC 2119 Description, and testable acceptance criteria, plus Legal Rule Context when the requirement encodes law. If `gh` can't render the form, write the body with the template's sections and fields. No free-form issues.

## Commands

```sh
uv sync --locked                       # install pinned dependencies
uv run ruff format . && uv run ruff check .
uv run mypy src                        # strict
uv run lint-imports                    # architecture boundaries
uv run pytest --cov                    # tests + golden scenarios, >= 80% overall
uv run coverage report --fail-under=100 --include='src/decision_engine/core/*,src/decision_engine/state_logic/*'
uv run decision-engine evaluate facts.json   # or: batch, golden golden/
```

CI (`.github/workflows/ci.yml`) runs all of these plus `pip-audit`. Never weaken a gate to make a change pass.

## Decided

| Item | Decision |
|---|---|
| Layout | `src/decision_engine/`: `core/` (pure), `state_logic/` (pure), `rules_loader.py`, `golden.py`, `cli.py`; rule data in `src/decision_engine/rules_data/`; golden scenarios in `golden/*.yaml` |
| Tooling | Python 3.13, uv with hash-pinned `uv.lock`, pytest + hypothesis, ruff (`ALL`), mypy `--strict`, import-linter, pip-audit |
| Coverage | 100% branch for `core/` and `state_logic/`; >= 80% overall |
| Rule format | Hybrid: cited YAML data validated by `RuleSetData` + pure Python logic per (state, version) |
| CI | GitHub Actions, actions pinned by SHA; `checks` and `dependency-audit` are required to merge |

## Undecided workflow items

| Item | Status |
|---|---|
| Persistence library and migrations tool | TO BE DECIDED |
| Required reviewers; how attorney sign-off is recorded | TO BE DECIDED |
| Rule and package versioning / release process | TO BE DECIDED |
