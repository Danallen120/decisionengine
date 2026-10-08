# CLAUDE.md

@ARCHITECTURE.md

Security rules live in `.claude/rules/security.md` (loaded automatically). Follow them; they are not repeated here. There is no `SECURITY.md`.

## Project status

Bootstrap mode. There is no implementation code yet, only architecture, security rules, and the requirement issue template. Do not assume tooling, layout, or workflows that the sections below don't define. If a task needs an undecided item, ask instead of picking one.

## Guardrails

- **Never invent law.** Every rule must come from a statute citation that is real and verifiable. If the law is unclear or the citation isn't certain, add an open-questions entry for that state and do not encode a guess.
- **Golden scenarios are the spec.** Every rule change ships with its citation and matching golden-scenario updates in the same PR. Never edit an expected decision just to make a test pass. If the test looks wrong, raise it for attorney review.
- **Write for attorneys.** Rule specs, open-questions lists, and golden-scenario tables must be plain English and readable without the code.
- **Stay in scope.** v1 covers California and Washington only. Library, CLI, and API come first; no UI. Don't add jurisdictions, a UI, or deployment infrastructure unless a requirement asks for it.
- **Respect the core boundary.** Changes to the core engine never pull in framework, I/O, or persistence concerns. Those belong in the CLI or API layers.

## Working style

- **One branch and PR per change.** Never commit directly to `main`.
- **Plan first for rules, schemas, and the decision log.** Before editing the core engine, rule sets, fact/decision schemas, or the decision log, state the plan and wait for confirmation.
- **Keep changes small and reviewable.** Don't refactor beyond what the task needs.
- **Report verification honestly.** Say exactly which tests and scenarios ran and what failed. Never claim a check passed if it didn't run.

## Issues

- **New GitHub issues MUST use the requirement template** (`.github/ISSUE_TEMPLATE/requirement.yml`), so every issue is a structured, testable requirement. This means:
  - an ID in the `REQ-<MODULE>-<###>` format;
  - an RFC 2119 Description;
  - independently testable acceptance criteria;
  - for requirements that encode law, the Legal Rule Context section.
- **From the CLI:** `gh` may not render issue forms. If it doesn't, write the issue body with the same section headings and fields as the template. Don't create free-form issues.
- **Link work to requirements.** PRs reference the requirement ID(s) they implement.

## Undecided workflow items

| Item | Status |
|---|---|
| Directory layout / package name | TO BE DECIDED |
| Python version, dependency manager, lockfile | TO BE DECIDED |
| Build / run / test commands | TO BE DECIDED |
| Lint, format, type-check tools | TO BE DECIDED |
| Test framework and golden-scenario file format/location | TO BE DECIDED |
| Rule data format (code vs. data files) and rule-hash method | TO BE DECIDED |
| CI platform and required checks | UNKNOWN |
| Branch protection / required reviewers | TO BE DECIDED |
| Attorney review workflow (how sign-off is recorded) | TO BE DECIDED |
| Rule and package versioning / release process | TO BE DECIDED |
| Deployment | TO BE DECIDED (per ARCHITECTURE.md) |
| Persistence library / migrations tool | TO BE DECIDED |
