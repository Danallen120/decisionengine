# Washington: open questions

Each question is tagged with what answers it:

- **Law:** needs an attorney.
- **Terms:** answered by the account's own terms, supplied as facts.
- **Policy:** an institution choice. It may be stricter than the statute, never looser.
- **Owner:** a product decision.

Until a question is answered, the affected cases are **not determinable** (or use the stated conservative default). The research notes summarize [legal-review.md](legal-review.md), which has the quotes and sources.

| # | Question | Answered by | Blocks | Proposed default | Research notes (v0.2) |
|---|---|---|---|---|---|
| W2 | A POD beneficiary predeceased. RCW 30A.22.100(4) gives the funds equally to the *surviving* beneficiaries. RCW 30A.22.160 bars paying any one beneficiary more than the balance divided by the *number of beneficiaries*. Does "number" mean all designated beneficiaries or only the survivors? | Law | GS-WA-009 | Not determinable. A safe alternative: pay each survivor 1/N, where N counts all designated beneficiaries, and route the remainder to a person. | The text supports either reading. A beneficiary is a person "designated" (RCW 30A.22.040(17)), which points to the designated count. No case was located. The remaining balance could be paid with all survivors' written consent, by analogy to RCW 30A.22.180(4) and .210(1)(a). The 120-hour rule also decides who counts as a survivor. |
| W3 | Can a will override a POD designation? Does RCW 11.11 (1998) govern over RCW 30A.22.100's "cannot ... be changed by the will" (1981)? Which notices remove the institution's protection? | Law (narrowed) | Path A | Pay per the account form unless a testamentary-disposition notice **or** a written dispute notice was received; with either, not determinable. | **Well supported:** *In re Estate of Burks*, 124 Wn. App. 327 (2004) applied RCW 11.11.020 to bank POD accounts; *Manary v. Anderson*, 176 Wn.2d 342 (2013); *Dahle v. Nadolski*, 127 Wn. App. 783 (2005). No case addresses the 1981 sentence. **Correction:** an informal written notice reaching the branch can be "actual knowledge of the existence of dispute" (RCW 30A.22.120, .210), so the RCW 11.11.050 notice is not the only trigger. A testamentary beneficiary's claim is time-barred under RCW 11.11.070(3). |
| W4 | Path B day counting: is payment allowed on day 40 (and on notice day 10)? Do weekends and holidays extend the wait? | Law (largely answered) | Path B dates | **Death + 41 and notice + 11, with no weekend or holiday extension.** | *Troxell v. Rainier Sch. Dist.*, 154 Wn.2d 345 (2005): "60 calendar days must intercede"; "both the first and last days must be excluded". *Christensen v. Ellsworth*, 162 Wn.2d 365 (2007): RCW 1.12.040 "by its terms does not apply" to waiting periods. Applied to RCW 11.62 by analogy; no case applies it directly. |
| W5 | Partial claims: may the institution pay a claimant who is entitled only to a share and lacks the others' authority? | Law | Path B shares | Not determinable until the attorney confirms. The research supports paying the claimed portion. | The statute contemplates "the portion thereof claimed" (RCW 11.62.010(2)(g)) and requires entitlement to "the property claimed" ((2)(i)). The institution "shall pay ... so much ... as is claimed" ((1)) and need not inquire (RCW 11.62.020). Refusing such claims by policy risks a proceeding to compel (W12). |
| W6 | Who mails the affidavit copy (with the SSN) to DSHS? Is it a payment condition? Must DSHS receive the (2)(h) successor notice for Medicaid recipients aged 55 and over? | Law + Policy | Path B documents | The claimant's duty, recorded as a process note, not a payment condition. | RCW 11.62.010(5) is passive. Parallel statutes assign the duty to the person administering (RCW 11.42.020(2)(d), 11.40.020(1)(d)). The Northwest Justice Project form tells the claimant to mail it. Nothing makes it a payment condition. DSHS is a "successor" to the extent of funds expended (RCW 11.62.005(2)(a)(iii)). |
| W7 | Should the community property agreement payment (RCW 30A.22.190(1)) be in v1? See the [analysis below](#w7-community-property-agreement-payment). | Owner (Law to confirm) | Path C | Out of scope until approved. | See the analysis below. |
| W8 | Should the $2,500 payment (RCW 30A.22.190(2)) be in v1? See the [analysis below](#w8-small-balance-payment-2500). | Owner + Policy | Path C | Out of scope. | See the analysis below. |
| W9 | Do community property interests affect anything the institution decides? | Law | Path A and Path B scope | Rely on the account form; no community property calculation. | **Supported.** Community property rights "shall not be affected by the form of the account" (RCW 30A.22.030(5)); RCW 30A.22.080, .110, .120. They matter only as a dispute notice. On Path B, the spouse's community half is excluded from the $100,000 test. |
| W10 | Confirm every citation and quotation against the official code. | Law | Approval of the whole spec | — | Done in the review. Corrections are applied in v0.2: RCW 11.02.005(13) vs (14), the "state or local" tax release, day counting, the California amount by date, and section histories. The $2,500 history (1989 c 220) and the 2026 c 204 effective date are still unverified. |
| W11 | Should the **credit union** surviving-spouse payment (RCW 11.62.030) be in v1? A credit union **may** pay a surviving spouse or domestic partner up to **$1,000** on their affidavit. A **good-faith** payment is a full acquittance, and the spouse must account to a later personal representative. | Owner (Law to confirm) | Path C | Out of scope. | Largely superseded for credit unions by RCW 30A.22.190(2), which allows $2,500, more payees, and an actual-knowledge standard. It adds little unless W8 is declined. |
| W12 | RCW 11.62.010(1) says the institution "shall pay". May an institution policy add waiting days or documents on Path B without exposure to a suit to compel? | Law | Policy limits; ARCHITECTURE.md | Statutory requirements only on Path B. | The statute is mandatory ("shall pay"; RCW 11.62.020 recovery proceeding), and no tax release may be required (RCW 11.62.010(4)). Chapter 30A.22, by contrast, uses "may" (Risk R3). |
| W13 | May an RCW 11.62.010 "affidavit" be an electronic or unsworn declaration under RCW 5.50? | Law | Path B documents | Accept only what the attorney approves. | RCW 5.50.030: an unsworn declaration "has the same effect as a sworn declaration". RCW 5.50.040 covers medium requirements. E-SIGN, 15 U.S.C. § 7001 (Risk R20). |
| W14 | Does *Kalk* bar an institution from setting off the decedent's debts against a surviving joint holder's funds, given that RCW 30A.22.040(12) counts setoff as a "payment"? | Law | Path A balance | No setoff against survivor funds in the engine's output. | *Kalk v. Security Pacific Bank*, 126 Wn.2d 346 (1995): a security agreement on one joint tenant's interest "is extinguished upon the joint tenant's death". |
| W15 | Which state's law governs when domicile, account office, and deposit-agreement law differ? | Law | All paths | Not determinable whenever they point to different states. | RCW 30A.22.040(8); *Anderson Nat'l Bank v. Luckett*, 321 U.S. 233 (1944) (Risk R1, R37–R39). |
| W16 | How should federal overlays be handled: Treasury reclamation, IRS levies, OFAC, NCUA/OCC preemption? | Law + Policy | Every determined decision | List them as institution pre-payment checks. Post-death federal credits or a reclamation notice make the case not determinable. | 31 CFR § 210.10(a); 26 U.S.C. § 6332; 31 CFR Chapter V (Risk R2, R8, R11, R16, R17). |

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

**From the legal research review (v0.2):**
- **Discharge coverage is ambiguous.** RCW 30A.22.120 lists § 190, but its operative clause covers payments "at the request of any depositor ... and/or the agent", and a surviving spouse who isn't on the account is not a "depositor" (RCW 30A.22.040(5)). The legislature probably intended coverage given the express cross-reference (reviewer inference).
- **Validity at death.** The agreement isn't revoked by a separation petition or a unilateral will (*Johnson v. Bachmeier*, 147 Wn.2d 60 (2002)), but mutual rescission, which may be shown by conduct, can end it (*Higgins v. Stafford*, 123 Wn.2d 160 (1994)). The spouse's affidavit is the institution's main protection. Dissolution ends "surviving spouse" status; a decree of legal separation does not.
- **Reach.** RCW 30A.22.180(3) also covers a *deceased POD beneficiary's* funds, so § 190(1) can reach a beneficiary's estate share.
- **Other limits.** The agreement doesn't defeat creditors, slayer and abuser rules (RCW 26.16.120; 11.84.030), or court cancellation in equity.

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

**From the legal research review (v0.2):**
- **Per account or aggregate.** The text reads "the balance of the funds **in the name of** a deceased depositor", which supports aggregating every account in the decedent's name at the institution. That is also the conservative reading.
- **Next of kin.** Undefined in chapter 30A.22. RCW 11.28.120(1)(b)'s ranking (children, parents, siblings, grandchildren, nephews and nieces) is a reasonable reference for a policy priority, but not binding. RCW 30A.22.902 extends it to registered domestic partners.
- **Credit unions.** They are covered too, so this payment is broader than the credit union rule in W11.

**Trade-off.** It allows fast, cheap handling of small balances with low risk, given the $2,500 cap. The cost is a new opt-in policy concept, two new relationships, and payee choice that depends on policy instead of law.
