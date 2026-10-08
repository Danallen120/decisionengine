# California: open questions

Each question is tagged with what answers it:

- **Law:** needs an attorney.
- **Terms:** answered by the account's own terms, supplied as facts.
- **Policy:** an institution choice. It may be stricter than the statute, never looser.

Until a question is answered, the affected cases are **not determinable**.

## Open

| # | Question | Answered by | Blocks | Proposed default |
|---|---|---|---|---|
| Q2 | With several affiants on Path B, how is payment split? The affiants are entitled together (§ 13105(a)(1)); the split follows the affidavit and institution policy. An attorney should confirm that policy cannot conflict with § 13105. | Policy (Law to confirm) | Path B shares | Not determinable when there is more than one affiant, unless policy says otherwise. |
| Q3 | Day counting for "40 days have elapsed since the death" (§ 13100): is the earliest payment date the death date + 40 days? | Law | Path B earliest payment | Death date + 40. |
| Q4 | On Path B, cross-check the declared successor against will or intestacy facts (§§ 6401, 6402), or rely on the affidavit as § 13106(a) permits? The law allows reliance, so a cross-check is an institution choice. | Policy | Facts schema scope | Rely on the affidavit. |
| Q5 | What procedure lets a surviving spouse or registered domestic partner collect a deposit account without the Path B affidavit (§ 13500 and related sections)? | Law | Path C | Not determinable. |
| Q6 | Joint accounts with two or more survivors: the statute lets the institution pay any one or more surviving parties according to the account terms (§§ 5401(a), 5402), protected under § 5405. The engine now expresses this as an `any_of` payment. An attorney should confirm the reading. | Terms (Law to confirm) | GS-CA-016 | `any_of` payment to all surviving parties. |
| Q8 | Does the institution require verification beyond the statutory documents (for example, for personal-representative consent or § 13051 representatives)? | Policy | Path B documents | Statutory documents only. |
| Q9 | Confirm every citation and quotation against the official code at leginfo.legislature.ca.gov. The automated fetch was blocked; text came from a mirror. | Law | Approval of the whole spec | — |

## Resolved

| # | Decision | By | Date |
|---|---|---|---|
| Q1 | Coverage begins with deaths on 2022-04-01. Earlier deaths are not determinable. | Owner | 2026-10-07 |
| Q7 | Totten trust accounts are in v1 (Path A, §§ 5302(c), 5404). | Owner | 2026-10-07 |
