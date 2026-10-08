# CLAUDE.md

@ARCHITECTURE.md

Owns: how to work in this repo. System design is in `ARCHITECTURE.md` (imported above). Security controls are in `.claude/rules/security.md`, which loads automatically.

## Status

Bootstrap mode: there is no implementation code yet. If a task depends on an undecided item (see the table below or the ARCHITECTURE.md open questions), ask instead of picking.

## Legal-rule guardrails

- **Never invent law.** Every rule must cite a real, verifiable statute. If the law or a citation is uncertain, add an open-questions entry for that state and do not encode a guess.
- **Golden scenarios are the spec.** Every rule change ships with its citation and matching golden-scenario updates in the same PR. Never change an expected decision just to make a test pass. If the test looks wrong, raise it for attorney review.
- **Write for attorneys.** Rule specs, open questions, and golden-scenario tables must be plain English and readable without the code.
- **Don't widen v1 scope.** No new jurisdictions, UI, or deployment work unless a requirement asks for it.

## Workflow

- **Use a branch and PR for every change.** Never commit to `main`. PRs reference the requirement ID(s) they implement.
- **Plan first for high-risk areas.** Before changing the core engine, rule sets, fact/decision schemas, or the decision log, state the plan and wait for confirmation.
- **Every new GitHub issue MUST use the requirement template** (`.github/ISSUE_TEMPLATE/requirement.yml`), so each issue is a structured, testable requirement: a `REQ-<MODULE>-<###>` ID, an RFC 2119 Description, and testable acceptance criteria, plus Legal Rule Context when the requirement encodes law. If `gh` can't render the form, write the body with the template's sections and fields. No free-form issues.

## Undecided workflow items

| Item | Status |
|---|---|
| Directory layout / package name | TO BE DECIDED |
| Python version, dependency manager, lockfile | TO BE DECIDED |
| Build / run / test / lint / format / type-check commands | TO BE DECIDED |
| Test framework; golden-scenario file format and location | TO BE DECIDED |
| Rule data format (code vs. data files); rule-set hash method | TO BE DECIDED |
| Persistence library and migrations tool | TO BE DECIDED |
| CI platform and required checks | UNKNOWN |
| Required reviewers; how attorney sign-off is recorded | TO BE DECIDED |
| Rule and package versioning / release process | TO BE DECIDED |
