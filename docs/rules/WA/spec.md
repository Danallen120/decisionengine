# Washington rule spec (DRAFT, not attorney-reviewed)

**Status:** Draft v0.2, updated 2026-10-09. **Attorney review:** not started.
Nothing here is encoded in the engine until an attorney approves it. Statute text was read from the **official** Revised Code of Washington at app.leg.wa.gov (see [sources](sources.md)). Numbered questions (W1, W2, …) are in [open-questions.md](open-questions.md); each is tagged **Law** (attorney), **Terms** (account facts), **Policy** (institution choice), or **Owner**. Supporting research, with quotes and sources for each point, is in [legal-review.md](legal-review.md). "#45" points to its claim-audit rows, "Gap 1" to its gaps, and "Risk R3" to the cross-cutting risk review (`docs/rules/legal-risk-review.md`).

## Changes since v0.1

v0.2 applies the findings of the legal research review (2026-10-09). Findings that need a legal judgment were added to the open questions instead of being decided here.

| Change | Basis |
|---|---|
| **Earliest Path B payment moved one day later:** death + 41 and notice + 11. No weekend or holiday extension. The claim that RCW 1.12.040 governs is withdrawn. | *Troxell v. Rainier Sch. Dist.*, 154 Wn.2d 345 (2005) (full days must pass); *Christensen v. Ellsworth*, 162 Wn.2d 365 (2007) (RCW 1.12.040 "by its terms does not apply"); #45, #57, #58, W4 |
| **Path B is mandatory: the institution "shall pay".** Stricter institution policy on Path B risks a suit to compel payment. | RCW 11.62.010(1), 11.62.020; W12; Risk R3 |
| **Partial claims are contemplated by the statute.** The not-determinable default is kept only until the attorney confirms. | RCW 11.62.010(1), (2)(g), (i); #42, W5 |
| **Proof of death for joint survivorship accounts is a policy choice**, not a statutory requirement. | RCW 30A.22.140; #23, #63 |
| **Protection depends on a signed written contract of deposit.** | RCW 30A.22.060; *Estate of Brownfield v. Bank of America*, 170 Wn. App. 553 (2012); #26, Gap 2 |
| **Added rules the review found missing:** the 120-hour survival rule, slayer and abuser notices, agent authority ending at death, vulnerable-adult holds, the institution's setoff limits, and escheat. | RCW 11.05A; 11.84; 30A.22.170; 11.125.100; 74.34.215; *Kalk v. Security Pacific Bank*, 126 Wn.2d 346 (1995); 63.30; Gaps 1–10 |
| **W3 correction:** an informal written dispute letter can also remove the chapter 30A.22 discharge, not only an RCW 11.11.050 notice. | RCW 30A.22.120, .210, .040(2); #12, W3 |
| **Citation corrections:** the nonprobate-asset definition is RCW 11.02.005(**13**) for most of the coverage period (renumbered (14) by 2026 c 204 § 15); the tax-release bar covers Washington **state or local** taxing authorities; the California limit depends on the date of death. | #11, #43, #2 |

## What the engine decides

For one deposit account of a Washington decedent, the engine answers four questions:

1. Who may the institution pay, and in what shares?
2. What documents must the institution receive first?
3. What is the earliest date it may pay?
4. Does a statute protect the institution from liability if it pays as decided?

Anything outside the paths below is **not determinable** and goes to a person. **Coverage begins with deaths on April 1, 2022** (owner decision W1, 2026-10-07). Earlier deaths are not determinable.

**What a decision does not check:** the engine relies on the facts entered. Statutory protection applies only if the documents actually received match those facts and meet the statute (Risk R23). Every decision will list the institution's pre-payment checks it does not perform, such as sanctions screening, levies and Treasury reclamation (Risk R2, R8, R11).

## How Washington differs from California

| Topic | Washington | California |
|---|---|---|
| Small-estate limit | **$100,000**, fixed, with no inflation adjustment (RCW 11.62.010(2)(c)) | $184,500 (deaths 2022-04-01 to 2025-03-31) or $208,850 (from 2025-04-01); adjusted every 3 years |
| What the limit measures | The **entire probate estate wherever located**, **less liens and encumbrances**, excluding the surviving spouse's or domestic partner's community property interest | **Current** gross value of California property, with listed exclusions |
| Existing administration | **Any** pending or granted application for a personal representative, **in any jurisdiction**, bars the affidavit. There is no consent route. | Only a **California** proceeding bars it, and the personal representative's written consent overcomes that |
| Extra conditions | The decedent was a WA resident; all debts are paid or provided for; written notice went to all other successors at least **10 full days** before payment | None comparable |
| Institution's duty | **"Shall pay"** on a valid affidavit and proof of death | The successor is "entitled" to payment; the court awards fees if the holder refuses unreasonably (§ 13105) |
| Joint accounts | With **or without** right of survivorship (RCW 30A.22.050). A contract that is silent means **no** survivorship (RCW 30A.22.040(11)). | Survivorship presumed and rebuttable (Prob. Code § 5302(a)) |
| A will overriding a POD designation | **Possible** for WA residents under RCW 11.11.020. Bank POD and survivorship accounts are nonprobate assets (RCW 11.02.005(13), now (14); *In re Estate of Burks*, 2004). The institution is protected until it has notice (see W3). | A will cannot change the account terms (§ 5302(e)), and the institution is protected paying per the terms. A will can still be evidence redirecting **ownership** between the claimants (*Placencia*, 2019). |

## Path A: accounts with surviving depositors or POD/trust beneficiaries

The account type is set by the contract of deposit, which must be **in writing and signed** by everyone with a current right to payment (RCW 30A.22.050, .060). Washington treats POD and trust accounts together ("trust and P.O.D. accounts", RCW 30A.22.040(18)). Ownership rules have "no bearing on ... the right of a financial institution to make payments" (RCW 30A.22.110).

| Question | Rule | Citation |
|---|---|---|
| Who may be paid | **Joint account with right of survivorship:** the surviving depositors. Their ownership is rebuttable by clear and convincing evidence of contrary intent when the account was created, which matters only between claimants. **POD or trust account:** the designated beneficiaries who survive. If the account is also a joint account with survivorship, it passes to the beneficiaries only after the last depositor dies. **Joint account without survivorship:** the decedent's funds go to the estate (use Path B or probate) unless the decedent designated a POD beneficiary of that interest. The institution may still pay a surviving co-depositor under RCW 30A.22.140. **Survival means surviving by 120 hours**, shown by clear and convincing evidence; otherwise the person is treated as having died first (see "Not determinable"). | RCW 30A.22.100(2)–(4), .110, .140; RCW 11.05A.020, .030, .040 |
| Shares | **Joint with survivorship, several survivors:** the institution may pay any one or more depositors, without regard to actual ownership (`any_of`). As between the survivors, the funds belong equally unless the contract says otherwise. **POD or trust, several surviving beneficiaries:** equal shares unless the contract specifies otherwise. The institution may not pay any one beneficiary more than the balance divided by the number of beneficiaries, unless the contract provides otherwise (see W2). | RCW 30A.22.140; 30A.22.100(3), (4); 30A.22.160 |
| Documents | **POD or trust:** proof of death of every depositor who had to die before the beneficiary. "Proof of death" means a certified or authenticated copy of a death certificate, or an equivalent government record. **Joint with survivorship:** no proof of death is required by statute (RCW 30A.22.140 permits payment "without regard to whether any other depositor ... [is] deceased"). Requiring it is an institution **policy** choice. **All:** staff confirm the account type from the signed contract of deposit. | RCW 30A.22.160, .040(14), .140, .060 |
| Earliest payment | **POD or trust:** once proof of death is received. **Joint with survivorship:** on request. No statutory waiting period; an institution policy may add one. | RCW 30A.22.160, .140 |
| Liability protection | **Yes.** Payments under the chapter are a complete release and discharge, even if inconsistent with actual ownership. This **depends on a contract of deposit that complies with the chapter** (*Brownfield*). **Exception:** the institution has *actual knowledge* of a dispute, meaning written notice to a manager or officer **of the branch holding the account**, in time to act. | RCW 30A.22.120, .040(2), .060; *Brownfield* |

**Not determinable on this path:**
- **Dispute notice.** Written notice of a dispute was received, or the institution is otherwise uncertain who is entitled. The institution may withhold payment until all parties consent in writing or a court directs. It may also pay against an adverse-claim bond, or hold for up to five business days on a fiduciary-misappropriation affidavit (RCW 30A.22.210, .220).
- **Testamentary disposition.** A notice that a will disposes of the account was received. A proper RCW 11.11.050 notice removes the RCW 11.11.040 protection; an informal letter reaching the branch can still be "actual knowledge of the existence of dispute" (RCW 30A.22.120, .210). Notice received less than five business days before payment is presumed insufficient, and more than 30 days is presumed sufficient (RCW 11.11.010(1)(b)).
- **Former spouse.** The POD beneficiary is a former spouse or former registered domestic partner. The designation is revoked by dissolution, with exceptions, and the institution is protected only until it has actual knowledge as RCW 11.07.010(3) defines it.
- **120-hour survival.** A beneficiary or co-depositor died within 120 hours of the decedent, or the order of death is unknown (RCW 11.05A.020–.040). The payor is protected until it receives written notice of a claimed lack of entitlement (RCW 11.05A.070). The rule doesn't apply if the account terms address simultaneous death (RCW 11.05A.060).
- **Slayer or abuser.** Written notice of a slayer or abuser claim was received (RCW 11.84.020, .050, .110).
- **Vulnerable-adult hold.** A financial-exploitation hold is active (RCW 30A.22.210(2); 74.34.215).
- **No signed contract.** The signed contract of deposit can't be located, or it doesn't match the institution's records (RCW 30A.22.060; *Brownfield*).
- **No beneficiary survived.** The funds go to the estate, so Path B or probate applies.
- **Signatures.** The terms require multiple signatures in a way the claim doesn't satisfy (RCW 30A.22.040(15)).

**The institution's own setoff:** a security agreement that encumbers only one joint tenant's interest is extinguished at that tenant's death (*Kalk*). The engine should not let an institution offset the decedent's debts against a surviving joint holder's funds. The attorney should confirm how this interacts with RCW 30A.22.040(12).

## Path B: small-estate affidavit (RCW 11.62)

Applies to funds that belong to the estate: a single account, the decedent's share of a joint account without survivorship, or an account where no beneficiary survived. **On a valid affidavit and proof of death the institution "shall pay"** (RCW 11.62.010(1)), and a successor may bring a proceeding to compel payment (RCW 11.62.020).

### Eligibility (all required, as stated in the affidavit)

| Condition | Citation |
|---|---|
| Forty full days have elapsed since the death. | RCW 11.62.010(1), (2)(d); *Troxell* |
| The decedent was a Washington resident on the date of death. | RCW 11.62.010(2)(b) |
| The decedent's entire probate estate, wherever located, less liens and encumbrances, does not exceed **$100,000**, excluding the surviving spouse's or domestic partner's community property interest. | RCW 11.62.010(2)(c) |
| No application or petition to appoint a personal representative is pending or has been granted **in any jurisdiction**, as of the payment date. Since the 2026 amendments, others may petition after 60 or 90 days (RCW 11.28.120(2), (3); effective date to confirm). | RCW 11.62.010(2)(e) |
| All debts of the decedent, including funeral and burial expenses, have been paid or provided for. | RCW 11.62.010(2)(f) |
| The claimant gave written notice of the claim to **all other successors** by personal service or mail, and at least 10 full days have elapsed since. For a Medicaid recipient, DSHS may itself be a successor (W6). | RCW 11.62.010(2)(h); 11.62.005(2)(a)(iii) |
| The claimant is a "successor": an heir or beneficiary under the will, a surviving spouse or domestic partner for their half of the community property, DSHS for recovery claims, or the state for escheat. A creditor is not a successor. | RCW 11.62.005(2) |

### Decision

| Question | Rule | Citation |
|---|---|---|
| Who is paid | The claiming successor who presents the affidavit and proof of death. The claimant must be personally entitled to full payment of the property claimed, or entitled on behalf of, and with the written authority of, all other successors who have an interest. | RCW 11.62.010(1), (2)(i) |
| Shares | The institution pays "so much ... as is claimed". The affidavit describes "the portion thereof claimed". A claimant with every other successor's written authority may take the full balance. **A share-only claim is within the statute**; until the attorney confirms (W5), it remains not determinable. | RCW 11.62.010(1), (2)(g), (i) |
| Documents | 1. The affidavit with every RCW 11.62.010(2) statement (W13 covers electronic or unsworn declarations). 2. Proof of death. **No release from any Washington state or local taxing authority may be required.** Extra documents added by institution policy risk a suit to compel (W12). | RCW 11.62.010(1), (2), (4) |
| Earliest payment | The **later** of **death + 41 days** and **notice + 11 days**. "Have elapsed" requires full days, excluding both the first and last day, and there is **no weekend or holiday extension**. This applies the Supreme Court's waiting-period rule by analogy; the attorney should confirm (W4). | RCW 11.62.010(1), (2)(d), (h); *Troxell*; *Christensen* |
| Liability protection | **Yes.** The institution is discharged as if it had dealt with a personal representative, **unless** it had actual knowledge that a required statement was false. An organization has that knowledge only once it reaches the individual making the payment. If several affidavits arrive, it may pay the first one received with proof of death, or interplead. | RCW 11.62.020 |

**Also required by statute:** a copy of the affidavit, including the decedent's Social Security number, must be mailed to DSHS's Office of Financial Recovery. The statute doesn't say who mails it. Every source located points to the claimant, and nothing makes it a condition of payment (W6). The engine never handles the SSN; this is recorded as a process note.

**Not determinable on this path:**
- An application to appoint a personal representative exists anywhere.
- The decedent was not a WA resident, or residency is unknown.
- The declared value exceeds $100,000 or is unknown.
- Notice to the other successors hasn't been given, or its date is unknown.
- The claimant is neither fully entitled nor authorized by all other successors (partial claims pending W5).
- The institution has actual knowledge that a required statement is false.
- **Escheat.** The account has been reported or remitted to the state as unclaimed property (RCW 63.30).

## Path C: other statutory payments (RCW 30A.22.190 and 11.62.030)

| Case | Rule | Status |
|---|---|---|
| **Community property agreement** | Pay all funds in the deceased spouse's name to the surviving spouse or domestic partner, on a certified copy of the recorded agreement plus the spouse's affidavit that it was valid and in force at death. The agreement can be rescinded by mutual assent, which the institution can't see. Legal separation proceedings alone do not revoke it (*Johnson v. Bachmeier*, 2002). | Under owner review (W7; analysis in open-questions) |
| **Balance at or below $2,500** | Payment may go to the surviving spouse, next of kin, funeral director, or a creditor who "may appear to be entitled", on proof of death and an affidavit that no personal representative was appointed. The institution may require waivers, indemnity and other proofs (Policy). The text ("funds in the name of a deceased depositor") supports aggregating all of the decedent's accounts. | Under owner review (W8; analysis in open-questions) |
| **Foreign personal representative** | After 60 days, with the documents listed in RCW 30A.22.200, including an estate tax release or a non-taxability affidavit. | Out of scope for v1 |
| **Credit union, balance at or below $1,000** | A credit union may pay the surviving spouse or domestic partner on their affidavit that no executor or administrator was appointed. A **good-faith** payment is a full acquittance, and the spouse must account to a later personal representative. Largely superseded for credit unions by the $2,500 payment. | Under owner review (W11) |

## Intestate shares (reference only)

RCW 11.04.015 sets intestate shares. The surviving spouse or domestic partner takes all of the decedent's share of the community estate, plus one-half, three-quarters, or all of the separate estate, depending on who else survives. On Path B the institution relies on the affidavit (RCW 11.62.020), so v1 does **not** compute intestate shares.

## Facts the engine will need

**In the schema** (REQ-CORE-004, -005, -006):
- `account.account_type`: `sole`, `joint_with_survivorship`, `joint_without_survivorship` (which may also name POD payees), `payable_on_death`, `totten_trust`; holders with survivorship and terms shares.
- `account.dispute_notice_received` (RCW 30A.22.120, .210) and `account.testamentary_disposition_notice_received` (RCW 11.11.040, .050); restraining order and withdrawal notice; multiple-signature terms.
- `decedent_resident_of_jurisdiction` (RCW 11.62.010(2)(b)).
- `estate.administration` (in Washington) and `estate.representative_application_elsewhere` (any other jurisdiction); together these cover RCW 11.62.010(2)(e).
- `estate.declared_value` (as RCW 11.62.010(2)(c) defines it), `estate.successor_notice_given_on`, `estate.claim_authorized_by_all_successors`, and `estate.affiants`.
- Former-spouse and former-partner relationships (RCW 11.07.010).

**Changes the research calls for** (schema changes need owner approval):
- **Survival evidence for every holder:** date and time of death, or "living", so the 120-hour rule can be applied (RCW 11.05A).
- **Notices and holds:** a slayer or abuser notice (RCW 11.84); an active vulnerable-adult hold (RCW 74.34.215); actual knowledge that the affidavit is false, and the count of competing affidavits (RCW 11.62.020).
- **Signed contract:** staff confirmation that the signed contract of deposit was located and matches (RCW 30A.22.060).
- **Claims and accounts:**
  - the portion claimed, as an amount or fraction (RCW 11.62.010(2)(g); W5);
  - the decedent's share of a joint account without survivorship (RCW 30A.22.090(2));
  - escheat status (RCW 63.30).
- **Overlays:**
  - post-death federal benefit credits and a reclamation notice (31 CFR § 210.10; Risk R2);
  - separate domicile, account-office state, and governing-law state (Risk R1).

**Waiting on owner decisions:** community property agreement documents (W7); `funeral_director` and `creditor` relationships plus claimant priority in policy (W8); institution type in policy (W11).

## Draft golden scenarios

These assume W4 resolves as the review recommends (death + 41, notice + 11, no weekend or holiday extension) and an institution policy that adds nothing.

| ID | Facts | Expected |
|---|---|---|
| GS-WA-001 | Sole account; WA resident; died 2025-06-01; declared estate $90,000.00; no PR application anywhere; one claimant with the other successors' written authority; notice mailed 2025-06-20 | Pay claimant 1/1. Documents: affidavit, proof of death. Earliest payment **2025-07-12** (death + 41; the notice wait ended 2025-07-01). Protected (RCW 11.62.020). |
| GS-WA-002 | As 001, but notice mailed 2025-07-08 | Earliest payment **2025-07-19** (notice + 11). |
| GS-WA-003 | As 001, but declared estate $100,000.00 | Eligible: equal to the limit. |
| GS-WA-004 | As 001, but declared estate $100,000.01 | Not determinable: over the limit. |
| GS-WA-005 | As 001, but a PR application is pending in another state | Not determinable (RCW 11.62.010(2)(e)). |
| GS-WA-006 | As 001, but the decedent was not a WA resident | Not determinable (RCW 11.62.010(2)(b)). |
| GS-WA-007 | Joint with survivorship; two surviving depositors | Payable to any of the survivors (`any_of`). No document required by statute; proof of death only if institution policy requires it. Protected (RCW 30A.22.120, .140). |
| GS-WA-008 | POD; three designated beneficiaries, all surviving by more than 120 hours; no share terms | Pay each 1/3. Proof of death. Protected (RCW 30A.22.120). |
| GS-WA-009 | POD; three designated beneficiaries, one predeceased; no share terms | The funds belong equally to the 2 survivors (RCW 30A.22.100(4)), but no single payment may exceed 1/3 (RCW 30A.22.160). **Expected outcome depends on W2.** A safe alternative: pay each survivor 1/3 and route the rest to a person. |
| GS-WA-010 | POD; terms give 60% / 40% | Pay 3/5 and 2/5 per the contract of deposit. |
| GS-WA-011 | POD; written notice of dispute received at the branch | Not determinable (RCW 30A.22.210). |
| GS-WA-012 | POD; notice of testamentary disposition received | Not determinable (RCW 11.11.040, 11.11.050). |
| GS-WA-013 | POD beneficiary is a former spouse | Not determinable (RCW 11.07.010). |
| GS-WA-014 | Joint without survivorship; decedent's share; small-estate facts as in 001 | Path B applies to the decedent's funds, using the claimed share as an input. |
| GS-WA-015 | As 001, but died 2022-03-31 | Not determinable: before coverage starts (W1). |
| GS-WA-016 | POD; the sole beneficiary died 2 days after the depositor; no survival terms | Not determinable: the 120-hour rule treats the beneficiary as having died first (RCW 11.05A.030). |
| GS-WA-017 | As 001, but the affidavit was presented on 2025-07-11 (day 40) | Not yet payable; earliest 2025-07-12. |
| GS-WA-018 | POD; written slayer or abuser notice received | Not determinable (RCW 11.84). |
