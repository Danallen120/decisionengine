# Washington: open questions

Each question is tagged with what answers it:

- **Law:** needs an attorney.
- **Terms:** answered by the account's own terms, supplied as facts.
- **Policy:** an institution choice. It may be stricter than the statute, never looser.
- **Owner:** a product decision.

Until a question is answered, the affected cases are **not determinable**.

| # | Question | Answered by | Blocks | Proposed default |
|---|---|---|---|---|
| W2 | A POD beneficiary predeceased. RCW 30A.22.100(4) gives the funds equally to the *surviving* beneficiaries. RCW 30A.22.160 bars paying any one beneficiary more than the balance divided by the *number of beneficiaries*. Does "number" mean all designated beneficiaries or only the survivors? | Law | GS-WA-009 | Not determinable when any designated beneficiary predeceased. |
| W3 | A will overriding a POD designation. **Research so far:** RCW 11.02.005(14) expressly lists joint bank accounts with survivorship and POD/trust bank accounts as nonprobate assets, and chapter 11.11's exclusions (RCW 11.11.010(7)) don't remove them. So RCW 11.11.020 reaches deposit accounts of WA residents dying on or after 1999-07-01 (RCW 11.11.901), despite RCW 30A.22.100's "cannot ... be changed by the will" sentence (1981). The institution is protected when it pays per the account form until it receives an RCW 11.11.050 notice (RCW 11.11.003(3), .040, .007). **Remaining question:** confirm that the 1998 chapter governs over the 1981 sentence, and that the RCW 11.11.050 notice is the only trigger. | Law (narrowed) | Path A | Pay per the account form unless a testamentary-disposition notice was received; with notice, not determinable. |
| W4 | Earliest payment date for Path B: "at any time after forty days" (RCW 11.62.010(1)), and at least 10 days after notice (RCW 11.62.010(2)(h)). **Research so far:** RCW 1.12.040 counts time by excluding the first day and including the last, and excludes the last day too if it is a Saturday, Sunday, or holiday. So day 40 is the date of death + 40. **Remaining questions:** (a) Is payment allowed *on* day 40 or only from day 41 ("after forty days", "forty days have elapsed")? (b) Does RCW 1.12.040's weekend/holiday extension apply to a waiting period before an act may be done, or only to deadlines? If it applies, the engine needs Washington's legal-holiday calendar (RCW 1.16.050) as cited rule data. | Law (narrowed) | Path B dates | The later of death + 40 days or notice + 10 days, with no weekend/holiday extension. |
| W5 | Partial claims. RCW 11.62.010(1) pays "so much ... as is claimed". If the claimant is entitled only to a share and lacks other successors' authority, can the institution pay a partial amount? | Law + Policy | Path B shares | Pay only a full claim backed by all other successors' written authority; otherwise not determinable. |
| W6 | Who mails the affidavit copy (with the SSN) to DSHS's Office of Financial Recovery (RCW 11.62.010(5)): the claimant or the institution? Must payment wait for it? RCW 43.20B.080 (DSHS estate recovery, including from nonprobate assets of Medicaid recipients 55 and over) does not assign the duty. | Law + Policy | Path B documents | Treat as the claimant's duty; record it as a process note, not a payment condition. |
| W7 | Should the community property agreement payment (RCW 30A.22.190(1)) be in v1? See the [analysis below](#w7-community-property-agreement-payment). | Owner (Law to confirm) | Path C | Out of scope until approved. |
| W8 | Should the $2,500 payment (RCW 30A.22.190(2)) be in v1? See the [analysis below](#w8-small-balance-payment-2500). | Owner + Policy | Path C | Out of scope. |
| W9 | Community property interests. Accounts are "subject to community property rights" (RCW 30A.22.100), but the institution may rely on the account form (RCW 30A.22.120, 11.11.040). Do community property claims affect anything the institution decides? | Law | Path A and Path B scope | Rely on the account form; no CP calculation. |
| W11 | Should the **credit union** surviving-spouse payment (RCW 11.62.030) be in v1? A credit union **may** pay a surviving spouse or domestic partner up to **$1,000** on their affidavit (member died; no executor or administrator appointed; deposit not over $1,000). A good-faith payment is a full release, and the spouse must account to any later personal representative. It only applies to credit unions, so the institution policy would need to record the institution type. | Owner (Law to confirm) | Path C | Out of scope. |
| W10 | Confirm every citation and quotation against the official code. The text was read from app.leg.wa.gov on 2026-10-07; this is a sign-off step. | Law | Approval of the whole spec | — |

## Resolved

| # | Decision | By | Date |
|---|---|---|---|
| W1 | Washington coverage begins with deaths on 2022-04-01, matching California. RCW 11.62.010 is unchanged since 2008, so one rule-set version covers it. | Owner | 2026-10-07 |

## Analysis for owner decisions

### W7: community property agreement payment

**What the statute allows** (RCW 30A.22.190(1)): when a deceased depositor left a surviving spouse, and both had executed a community property agreement that "by its terms would include" the account funds, the institution **may** pay **all** funds in the decedent's name to the surviving spouse.

| Aspect | Finding | Citation |
|---|---|---|
| Which funds | Only funds that would otherwise go to the personal representative: a single account, the decedent's share of a joint account without survivorship, or the last surviving depositor's funds. It never reaches POD or survivorship funds, which go to the named survivors. | RCW 30A.22.190 (opening clause), 30A.22.180 |
| Who | The surviving spouse, or a surviving state registered domestic partner. A former spouse is not a surviving spouse. | RCW 30A.22.190(1), 30A.22.902 |
| Documents | A certified copy of the agreement **as recorded** with a county auditor, plus the surviving spouse's affidavit that the agreement was validly executed and in force at death. | RCW 30A.22.190(1) |
| Limits | No dollar limit, no waiting period, and no residency or notice requirement. | RCW 30A.22.190(1) |
| The agreement itself | Signed by both spouses or partners, and witnessed, acknowledged and certified like a real-estate deed. It can be amended, cannot defeat creditors' rights, and can be set aside by a court for fraud. | RCW 26.16.120 |
| Protection | A payment under § 190 is a "payment" (RCW 30A.22.040(12)), so the complete discharge in RCW 30A.22.120 applies unless the institution has actual knowledge of a dispute. Unlike the § 190(2) and (3) payments, the statute does not make the recipient accountable to a later personal representative. | RCW 30A.22.120, 30A.22.190 (last paragraph) |

**What the engine could and could not decide.** The engine can check every condition except one: whether the agreement "by its terms would include" these funds. That requires someone to read the agreement. It would be a fact the institution's staff confirm, and the engine would rely on it.

**Facts needed:** a surviving spouse or partner among the parties; the recorded certified copy presented; the spouse's affidavit presented; and staff confirmation that the agreement covers the funds.

**Decision if included:** pay the surviving spouse 1/1 on receipt of the documents, protected under RCW 30A.22.120.

**Questions for the attorney:**
1. Does RCW 30A.22.120's discharge clearly cover a § 190(1) payment, given its "at the request of any depositor" wording?
2. Is the spouse's affidavit plus the recorded copy enough, or must the institution independently check the agreement's scope?

**Wills can't override it.** A community property agreement is a nonprobate asset (RCW 11.02.005(14)) but is excluded from chapter 11.11 (RCW 11.11.010(7)(a)(iv)), so a will can't redirect it the way W3 allows for POD accounts.

**Trade-off.** It settles estate funds for surviving spouses with an agreement without probate, with no value limit and no 40-day wait. The cost is one manual step (reading the agreement) plus four new facts.

### W8: small-balance payment ($2,500)

**What the statute allows** (RCW 30A.22.190(2)): when the decedent's funds in the account do not exceed **$2,500**, the institution **may** pay them to "the surviving spouse, next of kin, funeral director, or other creditor who may appear to be entitled thereto".

| Aspect | Finding | Citation |
|---|---|---|
| Which funds | Same as W7: funds that would otherwise go to the personal representative. | RCW 30A.22.190 (opening clause), 30A.22.180 |
| Who | The surviving spouse or partner, next of kin, a funeral director, or another creditor. Unlike the RCW 11.62 affidavit, creditors may be paid here, and the institution chooses among those who "may appear to be entitled". | RCW 30A.22.190(2); compare RCW 11.62.005(2)(b) |
| Documents | Proof of death, plus an affidavit that no personal representative has been appointed. The institution **may** also require waivers, indemnity, receipts, acquittance and other proofs (policy). | RCW 30A.22.190(2) |
| Limits | $2,500, not indexed. No waiting period is stated. The section was last amended by 2014 c 37 s 198; whether that changed the amount is unverified. | RCW 30A.22.190(2) and its history |
| Protection | Discharged under RCW 30A.22.120 unless the institution has actual knowledge of a dispute. The recipient is accountable to any personal representative appointed later. | RCW 30A.22.120, 30A.22.190 (last paragraph) |

**What makes it different.** The statute leaves the choice of payee to the institution's judgment. The engine can decide *eligibility*, but *who* to pay among competing claimants is an institution choice.

**How it could fit the design:** an institution would **opt in** through its policy and set a claimant priority, for example: surviving spouse, then next of kin, then funeral director, then other creditor. Two claimants at the same priority would be not determinable. The baseline policy would not opt in.

This extends today's stricter-only policy rule: a policy could choose among options the statute permits, but still never go past what the statute allows.

**Facts needed:** party relationships `funeral_director` and `creditor` (opaque IDs, no PII); a no-personal-representative affidavit presented; and which parties are claiming.

**Questions for the attorney:**
1. Is "$2,500" measured per account, or across all of the decedent's accounts at the institution?
2. Which relationships count as "next of kin"?
3. Does paying a creditor here conflict with any duty to the estate, given that the recipient is accountable to a later personal representative?

**Trade-off.** It allows fast, cheap handling of small balances with low risk, given the $2,500 cap. The cost is a new opt-in policy concept, two new relationships, and payee choice that depends on policy instead of law.
