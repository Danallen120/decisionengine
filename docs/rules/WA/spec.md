# Washington rule spec (DRAFT, not attorney-reviewed)

**Status:** Draft v0.1, written 2026-10-07. **Attorney review:** not started.
Nothing here is encoded in the engine until an attorney approves it. Statute text was read from the **official** Revised Code of Washington at app.leg.wa.gov (see [sources](sources.md)). Numbered questions (W1, W2, …) are in [open-questions.md](open-questions.md). Each is tagged **Law** (attorney), **Terms** (account facts), or **Policy** (institution choice; stricter only).

## What the engine decides

For one deposit account of a Washington decedent, the engine answers four questions:

1. Who may the institution pay, and in what shares?
2. What documents must the institution receive first?
3. What is the earliest date it may pay?
4. Does a statute protect the institution from liability if it pays as decided?

Anything outside the paths below is **not determinable** and goes to a person. **Coverage begins with deaths on April 1, 2022** (owner decision W1, 2026-10-07). Earlier deaths are not determinable.

## How Washington differs from California

| Topic | Washington | California |
|---|---|---|
| Small-estate limit | **$100,000**, fixed, with no inflation adjustment (RCW 11.62.010(2)(c)) | $208,850, adjusted every 3 years |
| What the limit measures | The **entire probate estate wherever located**, **less liens and encumbrances**, excluding the surviving spouse's or domestic partner's community property interest | Gross value of California property, with listed exclusions |
| Existing administration | **Any** pending or granted application for a personal representative, **in any jurisdiction**, bars the affidavit. There is no consent route. | Allowed with the personal representative's written consent |
| Extra conditions | The decedent was a WA resident; all debts are paid or provided for; written notice went to all other successors **at least 10 days** before | None comparable |
| Joint accounts | With **or without** right of survivorship (RCW 30A.22.050) | Survivorship presumed (Prob. Code § 5302(a)) |
| A will overriding a POD designation | **Possible** under RCW 11.11.020 (see W3) | Not possible (§ 5302(e)) |

## Path A: accounts with surviving depositors or POD/trust beneficiaries

The account type is set by the contract of deposit (RCW 30A.22.050). Washington treats POD and trust accounts together ("trust and P.O.D. accounts", RCW 30A.22.040(18)).

| Question | Rule | Citation |
|---|---|---|
| Who is paid | **Joint account with right of survivorship:** the decedent's funds belong to the surviving depositors. **POD or trust account:** the funds belong to the designated beneficiaries who survive. If the account is also a joint account with survivorship, it passes to the beneficiaries only after the last depositor dies. **Joint account without survivorship:** the decedent's funds go to the estate (use Path B or probate) unless the decedent designated a POD beneficiary of that interest. | RCW 30A.22.100(2)–(4) |
| Shares | **Joint with survivorship, several survivors:** the institution may pay any one or more depositors, without regard to actual ownership (`any_of`). As between the survivors, the funds belong equally unless the contract says otherwise. **POD or trust, several surviving beneficiaries:** equal shares unless the contract specifies otherwise. The institution may not pay any one beneficiary more than the balance divided by the number of beneficiaries, unless the contract provides otherwise (see W2). | RCW 30A.22.140; 30A.22.100(3), (4); 30A.22.160 |
| Documents | Proof of death of every depositor who had to die before the beneficiary. "Proof of death" means a certified or authenticated copy of a death certificate, or an equivalent government record. | RCW 30A.22.160; 30A.22.040(14) |
| Earliest payment | Once proof of death is received. No statutory waiting period; an institution policy may add one. | RCW 30A.22.160 |
| Liability protection | **Yes.** Payments made under the chapter are a complete release and discharge, even if inconsistent with actual ownership. **Exception:** the institution has *actual knowledge* of a dispute, meaning written notice to a branch manager or officer in time to act on it. | RCW 30A.22.120; 30A.22.040(2) |

**Not determinable on this path:**
- **Written notice of a dispute received.** The institution may withhold payment until all parties consent in writing or a court directs, or it may pay against an adverse-claim bond.
- **Notice of testamentary disposition received.** A will may redirect a nonprobate asset, and the institution loses its reliance protection once it receives proper notice under RCW 11.11.050.
- **The POD beneficiary is a former spouse or former registered domestic partner.** The designation is revoked by dissolution, with exceptions, and the institution is protected only until it has actual knowledge.
- **No beneficiary survived.** The funds go to the estate, so Path B or probate applies.
- **The terms require multiple signatures** in a way the claim doesn't satisfy.

Citations for this list, in order: RCW 30A.22.210, 30A.22.220; RCW 11.11.020, 11.11.040, 11.11.050; RCW 11.07.010(2), (3); RCW 30A.22.100(4).

## Path B: small-estate affidavit (RCW 11.62)

Applies to funds that belong to the estate: a single account, the decedent's share of a joint account without survivorship, or an account where no beneficiary survived.

### Eligibility (all required, as stated in the affidavit)

| Condition | Citation |
|---|---|
| At least 40 days have passed since the death. | RCW 11.62.010(1), (2)(d) |
| The decedent was a Washington resident on the date of death. | RCW 11.62.010(2)(b) |
| The decedent's entire probate estate, wherever located, less liens and encumbrances, does not exceed **$100,000**. This excludes the surviving spouse's or domestic partner's community property interest. | RCW 11.62.010(2)(c) |
| No application or petition to appoint a personal representative is pending or has been granted **in any jurisdiction**. | RCW 11.62.010(2)(e) |
| All debts of the decedent, including funeral and burial expenses, have been paid or provided for. | RCW 11.62.010(2)(f) |
| The claimant gave written notice of the claim to **all other successors** by personal service or mail, and at least **10 days** have passed since. | RCW 11.62.010(2)(h) |
| The claimant is a "successor": an heir or beneficiary under the will, a surviving spouse or domestic partner for their half of the community property, DSHS for recovery claims, or the state for escheat. A creditor is not a successor. | RCW 11.62.005(2) |

### Decision

| Question | Rule | Citation |
|---|---|---|
| Who is paid | The claiming successor who presents the affidavit and proof of death. The claimant must be either personally entitled to full payment, or entitled on behalf of, and with the written authority of, all other successors who have an interest. | RCW 11.62.010(1), (2)(i) |
| Shares | The institution pays "so much ... as is claimed". A claimant acting with every other successor's written authority may take the full balance (W5). | RCW 11.62.010(1), (2)(g), (i) |
| Documents | 1. The affidavit with every RCW 11.62.010(2) statement. 2. Proof of death. No tax release may be required. | RCW 11.62.010(1), (2), (4) |
| Earliest payment | The **later** of: 40 days after death, or 10 days after notice was served or mailed to the other successors (W4). | RCW 11.62.010(1), (2)(d), (h) |
| Liability protection | **Yes.** The institution is discharged as if it had dealt with a personal representative, **unless** it had actual knowledge that a required statement was false. An organization has that knowledge only once it reaches the individual making the payment. If several affidavits arrive, it may pay the first one received with proof of death, or interplead. | RCW 11.62.020 |

**Also required by statute:** a copy of the affidavit, including the decedent's Social Security number, must be mailed to DSHS's Office of Financial Recovery. The statute doesn't say who mails it (W6). The engine never handles the SSN; at most this becomes a process step or document.

**Not determinable on this path:**
- An application to appoint a personal representative exists anywhere.
- The decedent was not a WA resident, or residency is unknown.
- The declared value exceeds $100,000 or is unknown.
- Notice to the other successors hasn't been given, or its date is unknown.
- The claimant is neither fully entitled nor authorized by all other successors.

## Path C: other statutory payments (RCW 30A.22.190)

| Case | Rule | Status |
|---|---|---|
| **Community property agreement** | Pay all funds in the deceased spouse's name to the surviving spouse, on a certified copy of the recorded agreement plus the spouse's affidavit that it was valid and in force at death. | Under owner review (W7; analysis in open-questions) |
| **Balance at or below $2,500** | Payment may go to the surviving spouse, next of kin, funeral director, or a creditor who "may appear to be entitled", on proof of death and an affidavit that no personal representative was appointed. The institution may require waivers, indemnity and other proofs (Policy). | Under owner review (W8; analysis in open-questions) |
| **Foreign personal representative** | After 60 days, with the documents listed in RCW 30A.22.200. | Out of scope for v1 |

## Intestate shares (reference only)

RCW 11.04.015 sets intestate shares. The surviving spouse or domestic partner takes all of the decedent's share of the community estate, plus one-half, three-quarters, or all of the separate estate depending on who else survives. On Path B the institution relies on the affidavit (RCW 11.62.020), so v1 does **not** compute intestate shares.

## Facts the engine will need

**In the schema today:** account type and holders with survivorship and terms shares; balance; multiple-signature requirement; restraining order and withdrawal notice; former-spouse and former-partner relationships; administration status; declared value; affiants.

**Schema changes Washington needs** (for owner approval):
1. Distinguish **joint with** and **without** right of survivorship.
2. **Residency:** whether the decedent was a resident of the jurisdiction (yes / no / unknown).
3. **Administration anywhere:** Washington bars the affidavit if any jurisdiction has a pending or granted application, while California looks only at California proceedings.
4. **Date notice was given to the other successors** (for the 10-day wait).
5. **Notices received:** written notice of a dispute (RCW 30A.22.210), and notice of testamentary disposition (RCW 11.11.050).
6. **Claim scope:** whether the claimant claims the full balance with written authority from all other successors.
7. **Community property agreement:** whether a recorded agreement and the surviving spouse's affidavit were presented (if W7 is approved).

## Draft golden scenarios

These assume W4 resolves as "the later of death + 40 days or notice + 10 days" and a policy that adds nothing.

| ID | Facts | Expected |
|---|---|---|
| GS-WA-001 | Sole account; WA resident; died 2025-06-01; declared estate $90,000.00; no PR application anywhere; one claimant with the other successors' written authority; notice mailed 2025-06-20 | Pay claimant 1/1. Documents: affidavit, proof of death. Earliest payment 2025-07-11 (40 days after death; the notice wait ended 2025-06-30). Protected (RCW 11.62.020). |
| GS-WA-002 | As 001, but notice mailed 2025-07-08 | Earliest payment 2025-07-18 (10 days after notice). |
| GS-WA-003 | As 001, but declared estate $100,000.00 | Eligible: equal to the limit. |
| GS-WA-004 | As 001, but declared estate $100,000.01 | Not determinable: over the limit. |
| GS-WA-005 | As 001, but a PR application is pending in another state | Not determinable (RCW 11.62.010(2)(e)). |
| GS-WA-006 | As 001, but the decedent was not a WA resident | Not determinable (RCW 11.62.010(2)(b)). |
| GS-WA-007 | Joint with survivorship; two surviving depositors | Payable to any of the survivors (`any_of`). Proof of death. Protected (RCW 30A.22.120). |
| GS-WA-008 | POD; three designated beneficiaries, all surviving; no share terms | Pay each 1/3. Proof of death. Protected (RCW 30A.22.120). |
| GS-WA-009 | POD; three designated beneficiaries, one predeceased; no share terms | Belong equally to the 2 survivors (RCW 30A.22.100(4)), but no single payment may exceed 1/3 (RCW 30A.22.160). **Expected outcome depends on W2.** |
| GS-WA-010 | POD; terms give 60% / 40% | Pay 3/5 and 2/5 per the contract of deposit. |
| GS-WA-011 | POD; written notice of dispute received | Not determinable (RCW 30A.22.210). |
| GS-WA-012 | POD; notice of testamentary disposition received | Not determinable (RCW 11.11.040, 11.11.050). |
| GS-WA-013 | POD beneficiary is a former spouse | Not determinable (RCW 11.07.010). |
| GS-WA-014 | Joint without survivorship; decedent's share; small-estate facts as in 001 | Path B applies to the decedent's funds. |
| GS-WA-015 | As 001, but died 2022-03-31 | Not determinable: before coverage starts (W1). |
