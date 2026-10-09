> **Provenance.** Generated 2026-10-09 by the `estate-law-reviewer` AI research agent (`.claude/agents/estate-law-reviewer.md`). It is research for a licensed attorney, not legal advice.
>
> **Independent spot-check** (2026-10-09; five citations re-fetched and compared word for word):
> - *Troxell*, 154 Wn.2d 345: "60 calendar days must intercede" and "both the first and last days must be excluded" confirmed.
> - *Christensen v. Ellsworth*, 162 Wn.2d 365: "RCW 1.12.040 by its terms does not apply" confirmed.
> - *In re Estate of Burks*, 124 Wn. App. 327: confirmed.
> - *Estate of Brownfield*, 170 Wn. App. 553: confirmed.
> - RCW 11.02.005 renumbering: subsection (13) in the 2025 archive and (14) after 2026 c 204 § 15, confirmed.
>
> The remaining citations have not been independently re-checked.

# Washington deposit-account rule spec: legal research review

**I am not the client's attorney.** This is AI-generated research for a licensed Washington attorney to check. It is not legal advice, and it does not replace attorney sign-off.

- **Date:** 2026-10-09
- **Scope:** Washington rules for paying out a deceased customer's deposit account, for deaths on or after 2022-04-01, as drafted in the DecisionEngine WA spec.
- **Documents reviewed (read in full):**
  - `docs/rules/WA/spec.md` (Draft v0.1, 2026-10-07)
  - `docs/rules/WA/open-questions.md`
  - `docs/rules/WA/sources.md`
  - `ARCHITECTURE.md` (for context)

**Method.**
- I retrieved every Washington statute I rely on from the official RCW site, `https://app.leg.wa.gov/RCW/default.aspx?cite=<section>&full=true`, on 2026-10-09, and checked the quoted text against it.
- I confirmed that the text applied across the coverage period by checking the Code Reviser's 2023 and 2025 RCW archive PDFs for RCW 11.62.010 and 11.02.005, and by reading the 2026 session law that amended 11.02.005 (2026 c 204, EHB 2445).
- I read the full text of the cases from the Caselaw Access Project static files (`static.case.law`). I found them through CourtListener search results and web search.
- I checked the WAC on the official site.
- The California comparison rows were checked against the california.public.law mirror and the Judicial Council § 890 list.

**Limitations.**
- **CourtListener.** Its opinion pages and API detail endpoints returned bot-challenge or authentication responses, and its search API stopped answering partway through. I used it only to identify cases.
- **Justia and casetext** were not reachable from this environment.
- **Coverage gaps in case law.** The Caselaw Access Project ends around 2018, so I did not systematically search Washington opinions from after 2018 or unpublished opinions. No Westlaw or Lexis citator check was done.
- **Parallel citations.** Regional-reporter (P.2d/P.3d) citations are given only where they appeared inside an opinion I read. Where they come from CourtListener's index, they are labeled that way. Otherwise only the official Wash. / Wn. App. citation is given.
- **Not researched:**
  - 2026 c 204's effective date, beyond a secondary source;
  - the 1989 amendment to RCW 30A.22.190;
  - Title 31.12 beyond confirming that credit unions are covered by chapter 30A.22;
  - federal overlays (Treasury reclamation, NCUA, levies, OFAC).

## Summary

**Claim audit totals (80 rows):**

| Finding | Count |
|---|---|
| Verified | 54 |
| Verified with correction | 20 |
| Inaccurate | 4 |
| Unsupported | 1 |
| Unverified | 1 |

**The most important findings, ranked:**

1. **The Path B earliest payment date is probably one day early (W4 can largely be answered now). High.**
   - RCW 11.62.010 requires that "forty days have elapsed" and that "at least ten days have elapsed." The Washington Supreme Court reads "until sixty days have elapsed after" as requiring 60 *full* calendar days, excluding both the first and the last day (*Troxell v. Rainier Pub. Sch. Dist. No. 307*, 154 Wn.2d 345, 111 P.3d 1173 (2005)).
   - It also holds that RCW 1.12.040 "by its terms does not apply" to waiting periods, so weekends and holidays are irrelevant (*Christensen v. Ellsworth*, 162 Wn.2d 365 (2007)).
   - Applied by analogy, which is my inference: the earliest payment is death + **41** days and notice + **11** days, with no weekend or holiday extension.
   - GS-WA-001 and -002 are off by one day (2025-07-12 and 2025-07-19, not 07-11 and 07-18). The spec's statement that days are counted under RCW 1.12.040 should be withdrawn.
   - No case applying *Troxell* to RCW 11.62 was found.

2. **The "stricter-only institution policy" design may conflict with RCW 11.62.010. High.**
   - RCW 11.62.010(1) says the holder "**shall** pay." RCW 11.62.020 lets the successor bring a proceeding to compel payment from a holder who refuses. RCW 11.62.010(4) forbids requiring a state or local tax release.
   - Unlike chapter 30A.22, which uses "may" throughout, Path B is mandatory. A policy that adds waiting days or extra documents on Path B may expose the institution to a suit to compel.

3. **RCW 11.02.005 subsection number. Medium (citation accuracy).**
   - For most of the coverage period the "nonprobate asset" definition was **RCW 11.02.005(13)** (2021 c 140, effective 2022-01-01). It became (14) only by 2026 c 204 § 15; a secondary source says that law took effect June 11, 2026.
   - The text did not change. The spec should cite "(13) (renumbered (14) by 2026 c 204)."

4. **W3 is well supported but not fully closed. Medium.**
   - *In re Estate of Burks*, 124 Wn. App. 327, 100 P.3d 328 (2004), applied RCW 11.11.020 to bank POD certificates of deposit and said the statute "allowed Burks to change the death beneficiary of each account."
   - No case addresses the conflict with RCW 30A.22.100's "cannot, under any circumstances, be changed by the will" sentence. RCW 30A.22.030(2) disfavors implied repeal.
   - An RCW 11.11.050 notice is the only trigger that removes the RCW 11.11.040 protection. But a non-conforming letter from a testamentary beneficiary can still be "actual knowledge of the existence of dispute" under RCW 30A.22.120 and .210, which removes the *chapter 30A.22* discharge. So the 11.11.050 notice is not the only event that matters.

5. **The joint-account proof-of-death requirement is not statutory. Medium.**
   - RCW 30A.22.140 lets the institution pay any surviving depositor on a joint account "without regard to whether any other depositor ... [is] deceased." RCW 30A.22.160's proof-of-death condition applies to POD and trust beneficiaries only.
   - For joint accounts with survivorship (GS-WA-007), requiring proof of death is a policy choice, not a statutory one.

6. **Omitted rules that change who gets paid.** Each is detailed under Gaps.
   - 120-hour survival rule (RCW 11.05A.020, .030, .070). High.
   - Signed written contract of deposit (RCW 30A.22.060; *Estate of Brownfield v. Bank of America*, 170 Wn. App. 553 (2012)). Medium.
   - Slayer and abuser statute (RCW 11.84). Medium.
   - Agent authority ending at death (RCW 30A.22.170; RCW 11.125.100). Medium.
   - Vulnerable-adult holds (RCW 30A.22.210(2); RCW 74.34.215). Low to medium.

7. **Partial claims (W5).**
   - The statute expressly contemplates a claim to "the portion" of property claimed (RCW 11.62.010(2)(g)). The claimant must be "personally entitled to full payment ... of the property claimed" ((2)(i)).
   - A share-only claim is therefore within the statute. The proposed default of "not determinable" is stricter than the statute and raises the same "shall pay" risk as finding 2.

8. **The California $208,850 figure needs a date qualifier.**
   - $208,850 applies only to deaths on or after 2025-04-01.
   - Deaths from 2022-04-01 to 2025-03-31 use $184,500.

## Claim audit

Abbreviation: "RCW x" means the official text at `https://app.leg.wa.gov/RCW/default.aspx?cite=x&full=true`, retrieved 2026-10-09.

| # | Location | Claim | Finding | Authority (quote + URL) | Recommended change |
|---|---|---|---|---|---|
| 1 | spec › WA vs CA › small-estate limit | $100,000, fixed, no inflation adjustment; RCW 11.62.010(2)(c) | **Verified** | RCW 11.62.010(2)(c): "...wherever located, less liens and encumbrances, does not exceed one hundred thousand dollars". No indexing language. Same text in the 2023 and 2025 archive PDFs. | None |
| 2 | same row, CA | $208,850, adjusted every 3 years | **Verified with correction** | Judicial Council § 890 list: §§ 13100, 13101 = $166,250 before 2022-04-01; **$184,500** from 2022-04-01 to 2025-03-31; **$208,850** on or after 2025-04-01; next adjustment 2028-04-01 (https://courts.ca.gov/system/files/file/probate-code-890-adjusted-amounts.pdf). Prob. Code § 890(d): adjustments "do not apply when the decedent's death preceded the date of adjustment." | Say "$184,500 or $208,850 depending on date of death" |
| 3 | WA vs CA › what the limit measures, WA | Entire probate estate wherever located, less liens and encumbrances, excluding the surviving spouse's or partner's community property interest | **Verified** | RCW 11.62.010(2)(c): "...not including the surviving spouse's or surviving domestic partner's community property interest in any assets which are subject to probate..." | None |
| 4 | same, CA | Gross value of California property, with listed exclusions | **Verified** | Prob. Code § 13100 (mirror): "...gross value of the decedent's real and personal property in this state does not exceed..." (https://california.public.law/codes/probate_code_section_13100; confirm at leginfo) | None |
| 5 | WA vs CA › existing administration | Any pending or granted application in any jurisdiction bars the affidavit; no consent route | **Verified** | RCW 11.62.010(2)(e): "no application or petition for the appointment of a personal representative is pending or has been granted in any jurisdiction". No consent alternative appears in chapter 11.62. | None |
| 6 | same, CA | Allowed with the personal representative's written consent | **Verified** | § 13101(a)(4)(B): "The decedent's personal representative has consented in writing to the payment..." (mirror) | None |
| 7 | WA vs CA › extra conditions | WA resident; debts paid or provided for; written notice to other successors at least 10 days before | **Verified** | RCW 11.62.010(2)(b), (f), (h) | None |
| 8 | same, CA | "None comparable" | **Verified** (for the three listed items) | § 13101(a) (mirror) contains no residency, debts-paid or notice statement | None |
| 9 | WA vs CA › joint accounts | Joint accounts with or without survivorship (RCW 30A.22.050) | **Verified** | RCW 30A.22.050(2), (3). RCW 30A.22.040(11): a joint account without survivorship is one that "contains no provision that the funds of a deceased depositor become the property of the surviving depositor". | Note that silence in the contract means *no* survivorship |
| 10 | same, CA | Survivorship presumed (§ 5302(a)) | **Verified** | § 5302(a): "...belong to the surviving party or parties ... unless there is clear and convincing evidence of a different intent." (mirror) | None |
| 11 | WA vs CA › will overriding POD | Possible under RCW 11.11.020; bank POD and survivorship accounts are nonprobate assets under RCW 11.02.005(14) | **Verified with correction** | RCW 11.02.005 now (14), but **(13)** in the 2023 and 2025 archives (https://lawfilesext.leg.wa.gov/law/RCWArchive/2025/pdf/RCW%20%2011%20%20TITLE/RCW%20%2011%20.%2002%20%20CHAPTER/RCW%20%2011%20.%2002%20.005.pdf). The reviser's note to RCW 11.07.010 says it was renumbered "(13) to subsection (14)" by 2026 c 204 s 15. Text unchanged. | Cite "(13), renumbered (14) by 2026 c 204 § 15" |
| 12 | same | Institution protected until it receives an RCW 11.11.050 notice | **Verified with correction** | RCW 11.11.040: may rely "unless ... [it] has actual knowledge of the existence of a claim by a testamentary beneficiary". RCW 11.11.010(1)(a)(i): actual knowledge = "receipt of written notice that: (A) Complies with RCW 11.11.050". RCW 11.11.010(1)(b): "notice of less than five business days is presumed not to be a sufficient notice". | Add the 5-business-day and 30-day presumptions. Note that the RCW 30A.22.120 dispute exception works independently (see #31). |
| 13 | same, CA | Not possible (§ 5302(e)) | **Verified** | § 5302(e): "...a P.O.D. payee designation, cannot be changed by will." (mirror) | None |
| 14 | Path A intro | Account type set by the contract of deposit | **Verified** | RCW 30A.22.050: "the type of account shall be determined by the terms of the contract of deposit" | Add RCW 30A.22.060 (written, signed contract): see Gaps |
| 15 | Path A intro | POD and trust accounts treated together | **Verified** | RCW 30A.22.040(18) | None |
| 16 | Path A › who is paid (joint with survivorship) | Decedent's funds belong to the surviving depositors | **Verified with correction** | RCW 30A.22.100(3): "...belong to the surviving depositors unless there is clear and convincing evidence of a contrary intent at the time the account was created." RCW 30A.22.110 confines this to disputes between claimants, with "no bearing on ... the right of a financial institution to make payments". | Add the clear-and-convincing exception, noting it does not affect the institution (see cases) |
| 17 | Path A › who is paid (POD) | Surviving designated beneficiaries; if also joint with survivorship, only after the last depositor dies | **Verified** | RCW 30A.22.100(4) | None |
| 18 | Path A › who is paid (joint without survivorship) | Decedent's funds go to the estate unless a POD beneficiary was designated for that interest | **Verified** | RCW 30A.22.100(2) | Also note RCW 30A.22.140 (#20) |
| 19 | Path A › shares | Joint with survivorship: pay any one or more depositors (`any_of`) | **Verified** | RCW 30A.22.140: "...to or for any one or more of the depositors named on the account without regard to the actual ownership..." | None |
| 20 | Path A › shares | Survivors own equally unless the contract says otherwise | **Verified** | RCW 30A.22.100(3): "the funds belong equally to the surviving depositors unless the contract of deposit otherwise provides" | None |
| 21 | Path A › shares | POD: equal shares unless the contract specifies otherwise | **Verified** | RCW 30A.22.100(4) | None |
| 22 | Path A › shares | Per-beneficiary cap | **Verified** | RCW 30A.22.160: "shall not, unless the contract of deposit otherwise provides, pay to any one such beneficiary more than ... the total ... by the number of trust or P.O.D. account beneficiaries." | See W2 |
| 23 | Path A › documents | Proof of death of every depositor who had to predecease the beneficiary (RCW 30A.22.160) | **Verified** for POD; **Unsupported** as a statutory requirement for joint accounts with survivorship | RCW 30A.22.160 applies to POD and trust beneficiaries. RCW 30A.22.140 allows payment to a joint depositor "without regard to whether any other depositor ... [is] deceased". | Label proof of death for joint survivorship accounts as **Policy** |
| 24 | Path A › documents | Proof-of-death definition | **Verified** | RCW 30A.22.040(14) | None |
| 25 | Path A › earliest payment | Once proof of death is received; no statutory wait | **Verified with correction** | RCW 30A.22.160. But survivorship itself depends on the 120-hour rule: RCW 11.05A.020 and .030, "not established by clear and convincing evidence to have survived ... by one hundred twenty hours is deemed to have predeceased". | Add a 120-hour survivorship check (see Gaps) |
| 26 | Path A › liability protection | Payments are a complete release, even if inconsistent with ownership | **Verified with correction** | RCW 30A.22.120: "all payments ... in accordance with this section and RCW 30A.22.140, ... .160, ... .190 ... shall constitute a complete release and discharge". *Brownfield*, 170 Wn. App. at 553 (¶14): "The bank's authority to transfer to a beneficiary therefore depends on the existence of a contract complying with the Act." | Condition protection on a signed contract of deposit (RCW 30A.22.060) |
| 27 | Path A › liability protection | Actual knowledge = written notice to a branch manager or officer, in time to act | **Verified** | RCW 30A.22.040(2): "written notice to a manager of a branch ... or an officer ... at the branch, pertaining to funds held on deposit in an account maintained by the branch received within a period of time which affords ... a reasonable opportunity to act" | Note that the notice must reach *the branch holding the account* |
| 28 | Path A › not determinable (dispute) | May withhold until written consent or a court directs; or pay against an adverse-claim bond | **Verified with correction** | RCW 30A.22.210(1) also covers the case where the institution "is otherwise uncertain as to who is entitled". RCW 30A.22.220: bond "double either the amount of the deposit or the adverse claim, whichever is the lesser". Fiduciary-misappropriation affidavit allows a hold of "not more than five business days". | Add the "uncertain" trigger and the 5-business-day hold. Ask the attorney who must post the bond (the text says "the adverse claimant shall execute"). |
| 29 | Path A › not determinable (testamentary notice) | Loses reliance protection on a proper RCW 11.11.050 notice | **Verified** | RCW 11.11.040; 11.11.010(1); 11.11.050(1) (personal service or certified mail, proof "filed under the cause number assigned to the owner's estate"; delivered to the branch manager) | Encode the notice-validity facts or leave the case to a person |
| 30 | Path A › not determinable (former spouse) | Designation revoked by dissolution, with exceptions; protected only until actual knowledge | **Verified** | RCW 11.07.010(2)(a), (b); (3)(a): "not liable ... before the payor ... has actual knowledge of the dissolution". (3)(d) defines actual knowledge differently from RCW 30A.22.040(2): written notice that identifies the asset, with the 30-day and 5-business-day presumptions. | Note the separate actual-knowledge test |
| 31 | Path A › not determinable (no beneficiary survived) | Funds go to the estate (Path B or probate) | **Verified with note** | RCW 11.62.010(1) applies to "any person who is indebted to ... the decedent" for "an asset which is subject to probate". Whether RCW 30A.22.180(1) reaches a one-depositor POD account where every beneficiary predeceased is my inference: yes, as a "single account", RCW 30A.22.040(16). | None needed for Path B |
| 32 | Path A › not determinable (multiple signatures) | Terms requiring multiple signatures | **Verified** (design) | RCW 30A.22.040(15): a "request" must comply with "special requirements concerning necessary signatures" | None |
| 33 | Path B scope | Applies to estate funds (single account, decedent's share of a joint account without survivorship, no surviving beneficiary) | **Verified with correction** | RCW 11.62.010(1). The decedent's share of a joint account without survivorship is "in proportion to the net funds owned by each depositor" (RCW 30A.22.090(2)), which the engine cannot compute. | Make the claimed share an input fact (see GS-014) |
| 34 | Path B › eligibility | 40 days have passed (RCW 11.62.010(1), (2)(d)) | **Verified**, but see #45 on counting | (1) "At any time after forty days from the date of a decedent's death"; (2)(d) "That forty days have elapsed since the death" | — |
| 35 | Path B › eligibility | Washington resident at death | **Verified** | RCW 11.62.010(2)(b) | None |
| 36 | Path B › eligibility | Probate estate, wherever located, less liens and encumbrances, not over $100,000, excluding the spouse's community property interest | **Verified** | RCW 11.62.010(2)(c) | None |
| 37 | Path B › eligibility | No PR application pending or granted in any jurisdiction | **Verified** | RCW 11.62.010(2)(e) | None |
| 38 | Path B › eligibility | All debts, including funeral and burial, paid or provided for | **Verified** | RCW 11.62.010(2)(f) | None |
| 39 | Path B › eligibility | Notice to all other successors by personal service or mail; 10 days passed | **Verified** | RCW 11.62.010(2)(h): "at least ten days have elapsed since the service or mailing of such notice" | See W6: DSHS can itself be a "successor" |
| 40 | Path B › eligibility | Successor definition; creditors excluded | **Verified** | RCW 11.62.005(2)(a)(i)–(iv), (b): a claimant "solely by reason of being a creditor ... shall be excluded", except DSHS and the state | None |
| 41 | Path B › who is paid | Personally entitled, or entitled on behalf of and with the written authority of all others | **Verified** | RCW 11.62.010(2)(i) | None |
| 42 | Path B › shares | "So much ... as is claimed"; full balance with authority | **Verified with correction** | RCW 11.62.010(2)(g): "A description of the personal property and the portion thereof claimed". (2)(i) applies to "the property claimed". | Partial claims are contemplated (W5) |
| 43 | Path B › documents | Affidavit and proof of death; no tax release | **Verified with correction** | RCW 11.62.010(4): "No release from any Washington state or local taxing authority may be required" | Say "Washington state or local" |
| 44 | Path B › earliest payment | The later of 40 days after death or 10 days after notice | **Verified** (structure) | RCW 11.62.010(1), (2)(d), (h) | — |
| 45 | Path B › earliest payment | Days counted under RCW 1.12.040; day 40 = date of death + 40 | **Inaccurate** (by analogy to controlling Supreme Court authority) | *Troxell*, 154 Wn.2d 345, ¶1: "60 calendar days must intercede between the dates"; ¶13: "both the first and last days must be excluded". *Christensen*, 162 Wn.2d 365, ¶23: "RCW 1.12.040 by its terms does not apply because there is no 'time within which an act is to be done.'" | Earliest = death + 41 and notice + 11; no weekend or holiday extension. Attorney to confirm. |
| 46 | Path B › liability protection | Discharged as if dealing with a PR unless actual knowledge of falsity | **Verified** | RCW 11.62.020: "discharged and released to the same extent as if such person has dealt with a personal representative ... unless ... actual knowledge of the falsity of any statement" | None |
| 47 | Path B › liability protection | An organization has knowledge only once it reaches the paying individual | **Verified** | RCW 11.62.020 ¶2: "...brought to the personal attention of the individual making the transfer" | None |
| 48 | Path B › liability protection | Several affidavits: pay the first received with proof of death, or interplead | **Verified** | RCW 11.62.020: "may pay ... in response to the first affidavit received, provided that proof of death has also been received, or alternately implead such property into court" | None |
| 49 | Path B › DSHS copy | Copy with SSN mailed to DSHS Office of Financial Recovery; statute silent on who mails | **Verified** | RCW 11.62.010(5): "A copy of the affidavit, including the decedent's social security number, shall be mailed to ... office of financial recovery." Passive voice. | See W6 |
| 50 | Path B › not determinable list | PR application anywhere; residency unknown; value over $100,000 or unknown; notice not given or date unknown; claimant not entitled or authorized | **Verified** (as conservative design) | RCW 11.62.010(2)(b), (c), (e), (h), (i) | None |
| 51 | Path C › community property agreement | Pay all funds in the deceased spouse's name to the surviving spouse on a certified recorded copy plus the spouse's affidavit | **Verified** | RCW 30A.22.190(1): "...certified copy of the community property agreement as recorded in the office of a county auditor ... and an affidavit of the surviving spouse that the community property agreement was validly executed and in full force and effect" | None |
| 52 | Path C › $2,500 | Payees; proof of death plus no-PR affidavit; waivers and indemnity optional | **Verified** | RCW 30A.22.190(2) | See W8 |
| 53 | Path C › foreign PR | After 60 days, with the RCW 30A.22.200 documents | **Verified** | RCW 30A.22.200(1), (2) | None |
| 54 | Path C › credit union $1,000 | Credit union may pay the surviving spouse or partner; full release; spouse accounts to a later PR | **Verified with correction** | RCW 11.62.030: payment "made in good faith ... shall be a full acquittance". Applies to credit unions "organized under chapter 31.12 RCW or federal law". | Note the *good-faith* standard, which differs from "actual knowledge" |
| 55 | Intestate shares | Surviving spouse takes the decedent's community share plus ½, ¾ or all of the separate estate | **Verified** | RCW 11.04.015(1)(a)–(d) | None |
| 56 | Facts schema | RCW 11.62.010(2)(e) covered by two facts | **Verified** | RCW 11.62.010(2)(e) | None |
| 57 | GS-WA-001 | Earliest payment 2025-07-11; notice wait ended 2025-06-30 | **Inaccurate** (see #45) | *Troxell*; *Christensen* | **2025-07-12**; notice wait ends 2025-07-01 |
| 58 | GS-WA-002 | Earliest 2025-07-18 | **Inaccurate** (see #45) | same | **2025-07-19** |
| 59 | GS-WA-003 | $100,000.00 is eligible | **Verified** | "does not exceed" | None |
| 60 | GS-WA-004 | $100,000.01 not determinable | **Verified** | same | None |
| 61 | GS-WA-005 | PR application pending in another state: not determinable | **Verified** | (2)(e) "in any jurisdiction" | None |
| 62 | GS-WA-006 | Non-resident: not determinable | **Verified** | (2)(b) | None |
| 63 | GS-WA-007 | Joint with survivorship, two survivors: `any_of`; proof of death; protected | **Verified with correction** | RCW 30A.22.140 (no proof of death required) | Mark proof of death as Policy |
| 64 | GS-WA-008 | POD, 3 beneficiaries: 1/3 each | **Verified** | RCW 30A.22.100(4); .160 | None |
| 65 | GS-WA-009 | Depends on W2 | **Verified** (correctly flagged) | RCW 30A.22.100(4); .160 | See W2 |
| 66 | GS-WA-010 | 60/40 terms: pay 3/5 and 2/5 | **Verified** | RCW 30A.22.100(4) ("specifically designated a different method"); .160 ("unless the contract of deposit otherwise provides") | None |
| 67 | GS-WA-011 | Dispute notice: not determinable | **Verified** | RCW 30A.22.210 | None |
| 68 | GS-WA-012 | Testamentary notice: not determinable | **Verified** | RCW 11.11.040, .050 | None |
| 69 | GS-WA-013 | Former-spouse beneficiary: not determinable | **Verified** (conservative) | RCW 11.07.010(2), (3) | None |
| 70 | GS-WA-014 | Decedent's share of a joint account without survivorship goes to Path B | **Verified with correction** | RCW 30A.22.090(2) (share by net contribution); 30A.22.180(2) | Add a fact for the decedent's claimed share. Note that RCW 30A.22.140 separately lets the institution pay the surviving co-depositor. |
| 71 | GS-WA-015 | Death 2022-03-31: not determinable | **Verified** (owner decision W1) | — | None |
| 72 | open-questions › W1 | RCW 11.62.010 unchanged since 2008 | **Verified** | Current history "[2008 c 6 s 923; ...]"; same text in the 2023 and 2025 archive PDFs | None |
| 73 | open-questions › W3 | RCW 11.02.005(14) lists bank accounts; 11.11.010(7) exclusions don't remove them; 11.11.901 (deaths on or after 1999-07-01); protection until a .050 notice | **Verified with correction** | Subsection (13) issue (#11). RCW 11.11.901: "applies to any will of an owner who dies while a resident ... on or after July 1, 1999". *Burks* (see W3). | See W3 |
| 74 | open-questions › W4 | RCW 1.12.040 text | **Verified** (text) | RCW 1.12.040: "computed by excluding the first day, and including the last, unless the last day is a holiday, Saturday, or Sunday" | Conclusion superseded by #45 |
| 75 | open-questions › W6 | RCW 43.20B.080 does not assign the mailing duty | **Verified** | RCW 43.20B.080(3) (recovery from nonprobate assets of recipients aged 55 and over); no mailing provision | See W6 |
| 76 | open-questions › W7 table | Never reaches POD or survivorship funds | **Verified with correction** | RCW 30A.22.180(3) also covers funds of a *deceased POD beneficiary*, so § 190(1) can reach a beneficiary's estate share | Add the § 180(3) case |
| 77 | open-questions › W7 › the agreement itself | Signed, witnessed, acknowledged like a deed; amendable; can't defeat creditors; can be set aside for fraud | **Verified with correction** | RCW 26.16.120: also "under their hands and seals"; set aside "for fraud or under some other recognized head of equity jurisdiction"; and "nor prevent the application of laws governing ... slayers or abusers under chapter 11.84 RCW" | Add the equity and slayer/abuser limits |
| 78 | open-questions › W7 | Wills can't override a community property agreement (RCW 11.11.010(7)(a)(iv)) | **Verified** | RCW 11.11.010(7)(a)(iv): "A right or interest passing under a community property agreement" | None |
| 79 | open-questions › W8 | $2,500, not indexed; last amended 2014 c 37 s 198; effect on amount unverified | **Unverified** (history) | RCW 30A.22.190 history: "[2014 c 37 s 198; 1989 c 220 s 3; 1981 c 192 s 19 ...]". 2014 c 37 was the Title 30A recodification. 1989 c 220 s 3 was not retrieved. | Attorney to confirm. Applies to all 2022+ deaths either way. |
| 80 | sources.md | Section histories | **Verified with correction** | RCW 30A.22.200 history is "1988 c 29 s 9; 1981 c 192 s 20" (shown as "—"). RCW 11.02.005 history begins "2026 c 204 s 15; 2021 c 140 s 1012" (shown as "—"). RCW 11.11.010's own history is "2014 c 58 s 20; 2008 c 6 s 909; 1998 c 292 s 104" (merged with other sections in the table). RCW 43.20B.080's last amendment is 2010 c 94 s 12. | Update sources.md |

## Gaps and omissions

1. **120-hour survival rule. High.**
   - **Statute says.** RCW 11.05A.020 and .030 deem a person who is not shown by clear and convincing evidence to have survived by 120 hours to have predeceased. RCW 11.05A.010(1) and (2) cover co-owners "of property or accounts" and an "account with pay on death designation".
   - **Joint accounts.** RCW 11.05A.040 splits co-owned property where survivorship by 120 hours can't be shown.
   - **Exceptions.** The rule doesn't apply if the governing instrument deals explicitly with simultaneous deaths or survival periods (RCW 11.05A.060).
   - **Payor protection.** RCW 11.05A.070(1)(a): the payor is not liable "before the payor or other third party received written notice of a claimed lack of entitlement". Notice goes by certified or registered mail to the "main office", or by service like a summons. Note the different notice locus from RCW 30A.22.040(2).
   - **Proof.** RCW 11.05A.050(6): a death certificate showing death 120 hours or more after the other death establishes survival.
   - **Effect on the engine.** The engine needs both dates of death, ideally times as well, for any beneficiary or co-depositor who has since died. Otherwise the payee set in Path A can be wrong.

2. **Signed written contract of deposit. Medium.**
   - **Statute says.** RCW 30A.22.060: "The contract of deposit shall be in writing and signed by all individuals who have a current right to payment".
   - **Case law holds.** *Estate of Brownfield v. Bank of America, NA*, 170 Wn. App. 553 (2012) (Div. III). A bank that paid a POD beneficiary shown only in its electronic records, without a located signed card, faced trial on breach of contract. A lost writing may be proven by secondary evidence.
   - **Effect on the engine.** `account_type` should be the type shown on the signed contract of deposit, and staff should confirm that.

3. **Slayer and abuser statute (RCW 11.84). Medium.**
   - **Statute says.** RCW 11.84.020: "No slayer or abuser shall in any way acquire any property or receive any benefit as the result of the death of the decedent".
   - **Joint property.** RCW 11.84.050 covers joint tenants and joint owners.
   - **Community property agreements.** RCW 11.84.030 covers rights under a community property agreement (RCW 26.16.120).
   - **Bank protection.** RCW 11.84.110 protects "any bank ... performing an obligation for the slayer or abuser as one of several joint obligees" if it pays "without written notice, at its home office or at an individual's home or business address".
   - **Reviewer inference.** RCW 11.84.110 does not expressly cover POD payments. For those, rely on RCW 30A.22.120 and .210. Add a fact for "written notice of slayer or abuser claim received", leading to not determinable.

4. **Agents and powers of attorney after death. Medium.**
   - **Statute says.** RCW 30A.22.170: "the authority of an agent to receive payments or make withdrawals from an account terminates with the death". The institution is not liable unless it "had actual knowledge of the ... death at the time payment was made".
   - **Powers of attorney.** RCW 11.125.100(1)(a): a power of attorney terminates when "The principal dies". Under (5), a person acting in good faith without actual knowledge is protected.
   - **Effect on the engine.** Agent requests received after the institution knows of the death should be rejected or not determinable. Agency accounts also pass by RCW 30A.22.100(5).

5. **Vulnerable-adult exploitation hold. Low to medium.**
   - **Statute says.** RCW 30A.22.210(2) and RCW 74.34.215(1) let an institution refuse a disbursal from an account "(b) On which the vulnerable adult is a beneficiary" or "(c) Of a person suspected of perpetrating financial exploitation".
   - **Duration.** The hold expires after "Five business days" for non-securities transactions (RCW 74.34.215(5)(b)), unless extended by a court.
   - **Duties and immunity.** The institution must notify the parties and report to Adult Protective Services and law enforcement ((4)). It is immune if acting in good faith ((7)).
   - **Relevance.** A surviving POD beneficiary may be a vulnerable adult, or the claimant may be a suspect. This is a Policy hook (stricter-only) plus a not-determinable fact.

6. **Creditor claims, notice to creditors, and estate recovery (RCW 11.40, 11.42, 11.18.200). Low for the institution.**
   - **Statute says.** Beneficiaries of POD, trust and survivorship accounts take subject to the decedent's liabilities "to the extent of the decedent's beneficial ownership interest" (RCW 11.18.200(1), (2)(b), (c)). Community-property nonprobate assets are reachable as if probate assets ((2)(g)).
   - **Time bar.** Creditor claims are barred 24 months after death if no notice is given (RCW 11.40.051(1)(c)).
   - **Nonprobate notice agent.** RCW 11.42.020(2)(d): the notice agent "shall also mail a copy of the notice, including the decedent's social security number, to the ... office of financial recovery". This is the same structure as RCW 11.62.010(5), but there the actor is named.
   - **Reviewer inference.** Chapters 11.40 and 11.42 impose no duties on the paying institution. Path B relies on the affiant's statement that debts are paid (RCW 11.62.010(2)(f); 11.62.020 "not required ... to inquire").

7. **Institution's own setoff or pledge against survivor funds. Medium.**
   - **Case law holds.** *Kalk v. Security Pacific Bank Washington N.A.*, 126 Wn.2d 346, 894 P.2d 559 (1995): "a security agreement encumbering only the interest of one joint tenant with right of survivorship is extinguished upon the joint tenant's death."
   - **Reviewer inference.** The engine should not let an institution offset the decedent's debts against a surviving joint holder's funds. Whether RCW 30A.22.040(12) ("set-off" is a "payment") changes this was not resolved in *Kalk*. The attorney should confirm.

8. **Clear-and-convincing evidence and other ownership disputes.**
   - **Case law holds.** Each of these involved litigation between claimants; none affects the institution's statutory discharge when it has no knowledge of a dispute (RCW 30A.22.110, .120, .130):
     - *Taufen v. Estate of Kirpes*, 155 Wn. App. 598 (2010): the survivorship presumption failed where a bank employee, not the depositor, added survivorship. "The legislature created a rebuttable presumption ... that can be overcome only by clear and convincing evidence."
     - *Garten v. Daley* (*Estate of Krappes*), 121 Wn. App. 653, 91 P.3d 96 (2004).
     - *Morse v. Williams*, 48 Wn. App. 734, 740 P.2d 884 (1987).
     - *In re Estate of Fox*, 51 Wn. App. 498, 754 P.2d 690 (1988).
     - *Meyer v. Moore*, 60 Wn. App. 39 (1990), which applied chapter 30.22 to a credit union.
     - *Baker v. Leonard*, 120 Wn.2d 538, 843 P.2d 1050 (1993): accounts created after 1982-07-01 carry a rebuttable presumption; earlier accounts fall under former RCW 30.20.015's conclusive presumption.
   - **Relevance.** For the engine these are reasons a dispute notice may arrive. They are not inputs.

9. **Interpleader practice.**
   - **Case law holds.** *Kitsap Bank v. Denley*, 177 Wn. App. 559 (2013); 312 P.3d 711 per CourtListener's index. The bank "initiated the action under RCW 30.22.210 because of the dispute over the legal ownership of the funds of Correll's POD bank account", and RCW 11.96A.150 fees were awarded.
   - **Relevance.** This supports routing to a person when a dispute exists.

10. **Unclaimed property (RCW 63.30). Low.**
    - **Statute says.** A deposit is presumed abandoned "three years after the later of maturity ... or the owner's last indication of interest" (RCW 63.30.040(5)).
    - **Reviewer inference.** Long-dormant decedent accounts may already have been reported to the state. The engine should treat "funds remitted to the state" as not determinable.

11. **Washington estate tax (RCW 83.100). Low; no hold found.**
    - **Statute says.** RCW 83.100.120(3) treats "banks and other depositories of checking and savings accounts" as persons who do not have possession for estate-tax liability purposes. RCW 11.62.010(4) bars requiring a tax release.
    - **Foreign PRs only.** RCW 30A.22.200(2)(d) requires a Department of Revenue estate tax release or a non-taxability affidavit for foreign PRs.
    - **Reviewer inference.** No estate-tax hold applies on Paths A or B.

12. **Credit unions (Title 31.12). Low.**
    - **Statute says.** Credit unions are "financial institutions" under chapter 30A.22 (RCW 30A.22.040(8)). The $2,500 payment in RCW 30A.22.190(2) is therefore also open to credit unions and is broader than RCW 11.62.030 (more payees, higher cap).
    - **Not reviewed.** I did not review other parts of chapter 31.12 or NCUA rules for federal credit unions.

13. **2026 probate amendments (2026 c 204, EHB 2445).**
    - **Statute says.** RCW 11.28.120(2) and (3) now let a contract service provider or guardian ad litem petition for letters after 60 days, and "any suitable person" after 90 days. Before, any suitable person could do so after 40 days.
    - **Effect on the engine.** A PR application can appear after an affidavit is in progress. The `representative_application` facts must be as of the payment date.
    - **Not verified.** The effective date (June 11, 2026) comes from a secondary search result.

14. **Not researched** (flagged for completeness):
    - payment to minor beneficiaries (UTMA, guardianship);
    - federal benefit reclamation (31 C.F.R. part 210);
    - IRS and child-support levies;
    - OFAC;
    - NCUA and OCC preemption.

## Open questions: research notes

**W2: does the RCW 30A.22.160 cap divide by all designated beneficiaries or only survivors?**
- **Statute says.**
  - RCW 30A.22.160 divides "by the number of trust or P.O.D. account beneficiaries."
  - RCW 30A.22.040(17) defines a beneficiary as a person "designated by a depositor ... to receive the depositor's funds remaining". That points to the designated count.
  - RCW 30A.22.040(5): a beneficiary "becomes a depositor only when the account becomes payable to the beneficiary by reason of having survived". A predeceased designee never acquires a right to payment.
  - RCW 30A.22.100(4): the funds "belong equally to the surviving beneficiaries".
- **Case law holds.** Nothing located. The CourtListener search for "30.22.160" returned 0 results.
- **Reviewer inference.** The text supports either reading.
  - The cap is a payment-protection rule, separate from ownership (RCW 30A.22.110, .130). Using the designated count is the conservative reading: no single payment exceeds 1/N.
  - The remaining balance can then be paid with all surviving beneficiaries' written consent (by analogy to RCW 30A.22.180(4) and .210(1)(a)), or by court order.
  - The 120-hour rule (Gap 1) also decides who counts as a survivor.
- **Can it be answered now?** Not definitively. The proposed default ("not determinable") is safe. A safe determinable alternative is to pay each survivor 1/N_designated and route the remainder to a person.

**W3: can a will (the "superwill" statute) redirect bank POD and survivorship accounts?**
- **Statute says.**
  - RCW 11.02.005(13), now (14), lists "joint bank account with right of survivorship" and "payable on death or trust bank account".
  - RCW 11.11.010(7)(a) does not exclude them.
  - RCW 11.11.020(1): "notwithstanding the rights of any beneficiary designated before the date of the will."
  - RCW 11.11.020(4): a beneficiary designation made after the will controls, and "A beneficiary designation with respect to an asset that renews without the signature of the owner is deemed to have been made on the date on which the account was first opened" (relevant to CDs).
  - Against this: RCW 30A.22.100 says the designations "cannot, under any circumstances, be changed by the will of a depositor". RCW 30A.22.030(2) says no part of the chapter "shall be deemed impliedly repealed by subsequent legislation if such construction can be reasonably avoided". RCW 11.11.005(1)(b) has the same clause.
- **Case law holds.**
  - *In re Estate of Burks*, 124 Wn. App. 327, 330, 100 P.3d 328 (2004) (Div. II): "RCW 11.11.020 specifically refers to nonprobate assets and allowed Burks to change the death beneficiary of each account". The will failed only for lack of specificity ("certain bank accounts").
  - *Manary v. Anderson*, 176 Wn.2d 342 (2013); 292 P.3d 96 per CourtListener's index. It approved *Burks*'s specificity analysis. "We hold that an owner complies with the Act when he specifically refers to a nonprobate asset in his will, even if he does not refer to the instrument".
  - *Dahle v. Nadolski*, 127 Wn. App. 783 (2005), a brokerage joint account: "Nothing in the statute limits the written means of designation to any particular form". So a later signed writing outside the bank's form can re-designate.
  - None of these cases discusses the RCW 30A.22.100 sentence.
- **Reviewer inference.** The spec's conclusion is well supported. The later and more specific statute expressly lists bank accounts, and the two schemes fit together through the institution-protection provisions (RCW 30A.22.110; 11.11.003(3), .007, .040).
- **Correction to the spec.** RCW 11.11.050 notice is the only trigger that removes the RCW 11.11.040 protection. But a written notice that does not comply with 11.11.050 and reaches the branch manager can still be "actual knowledge of the existence of dispute" (RCW 30A.22.120, .040(2)), which removes the chapter 30A.22 discharge and allows withholding under .210.
- **Time bar.** RCW 11.11.070(3) bars a testamentary beneficiary's claim after the earlier of six months from admission of the will to probate or one year from death.
- **Can it be answered now?** Mostly yes. The attorney should confirm the precedence point, which is not adjudicated.

**W4: day counting for Path B. Answerable now, subject to attorney confirmation.**
- **Case law holds.**
  - *Troxell v. Rainier Pub. Sch. Dist. No. 307*, 154 Wn.2d 345, 111 P.3d 1173 (2005), on "until sixty days have elapsed after": a full 60 days must pass, and suit is permitted "at the earliest, on February 9" when notice was given December 10. It adopts the rule that "both the first and last days must be excluded."
  - *Christensen v. Ellsworth*, 162 Wn.2d 365 (2007): CR 6(a) "does not control the computation of time where action is prohibited until a period of time has passed", and "RCW 1.12.040 by its terms does not apply". It is therefore "irrelevant whether the notice period includes weekends or holidays."
- **Reviewer inference.** RCW 11.62.010 uses the same "have elapsed" wording ((2)(d), (h)) and "after forty days" ((1)).
  - (a) Payment may be made on death + 41 and notice + 11, not on day 40.
  - (b) No weekend or holiday extension applies, so the engine does not need the RCW 1.16.050 holiday calendar.
  - **Secondary.** The Northwest Justice Project form has the affiant state that the decedent "died more than 40 days ago".
- No case applies *Troxell* to RCW 11.62.

**W5: partial claims.**
- **Statute says.**
  - RCW 11.62.010(1): "shall pay ... or so much of either as is claimed".
  - (2)(g) requires a description of "the portion thereof claimed".
  - (2)(i) requires that the claimant be "personally entitled to full payment ... of the property claimed".
  - RCW 11.62.020: no duty "to inquire into the truth"; the first affidavit received may be paid.
- **Reviewer inference.** A successor may claim only their own share without the others' authority. The institution is discharged in relying on the affidavit.
  - Because the duty is mandatory ("shall pay"), refusing such a claim by policy risks a proceeding to compel under RCW 11.62.020.
  - The default should become: pay the claimed portion (as a stated amount or fraction from the affidavit), protected under RCW 11.62.020.

**W6: who mails the affidavit copy to DSHS?**
- **Statute says.**
  - RCW 11.62.010(5) is in the passive voice and names no one.
  - By contrast, RCW 11.42.020(2)(d) ("The notice agent shall also mail") and RCW 11.40.020(1)(d) ("The personal representative shall also mail") assign the duty to the party administering the estate. That suggests the comparable actor under chapter 11.62 is the claiming successor (reviewer inference).
  - RCW 43.20B.080(3) authorizes recovery from the estate and nonprobate assets of Medicaid recipients aged 55 and over. It does not assign the mailing.
  - DSHS is itself a "successor" "to the extent of funds expended" (RCW 11.62.005(2)(a)(iii)). So for a Medicaid recipient, the (2)(h) notice to "all other successors" arguably includes DSHS (reviewer inference).
- **Regulator guidance.**
  - WAC 182-527-2730 defines "Estate" to include assets passing "by intestate succession under chapter 11.04 or 11.62 RCW". No current WAC assigns the mailing.
  - The former rule WAC 182-527-2870, "Serving notices on the office of financial recovery (OFR)", was repealed by WSR 16-05-054.
- **Secondary guidance.** The Northwest Justice Project small-estate affidavit form (2025-08) tells the claimant: "Mail a copy of this form including the deceased's Social Security number, to ... Office of Financial Recovery, PO Box 9501, Olympia, WA 98507-9501."
- **Payment condition?** Nothing in RCW 11.62.010(1) or 11.62.020 makes the mailing a condition of payment or discharge.
- **Can it be answered now?** The proposed default (the claimant's duty, recorded as a process note) is consistent with every source found. The attorney should confirm.

**W7: community property agreement payment (owner decision; what an attorney would want the owner to know).**
- **Discharge.** RCW 30A.22.120 lists RCW 30A.22.190, and RCW 30A.22.040(12) counts § 190 payments as "payments". But the operative clause covers payments "at the request of any depositor ... and/or the agent". A surviving spouse is not a "depositor" under RCW 30A.22.040(5) unless they are also on the account. The coverage is textually ambiguous. Reviewer inference: the legislature probably intended coverage, given the express cross-reference.
- **Scope of the agreement.** The statute conditions payment on an agreement "which by its terms would include" the funds. Whether a staff reading suffices is untested, and no case was located.
- **Validity at death.**
  - *Johnson v. Bachmeier*, 147 Wn.2d 60 (2002): a community property agreement is not revoked by a separation petition or a unilateral inconsistent will. "the initiation of legal separation proceedings ... does not immediately effect an abandonment of the CPA".
  - It can be rescinded only by mutual assent, which may be shown by conduct such as mutual wills: *Higgins v. Stafford*, 123 Wn.2d 160, 866 P.2d 31 (1994), as summarized in *Bachmeier*; *In re Estate of Wittman* (*Seeley v. Godfrey*), 58 Wn.2d 841, 365 P.2d 17 (1961).
  - A rescission may exist that the institution cannot see. The spouse's affidavit ("in full force and effect") is the institution's main protection.
  - Dissolution ends "surviving spouse" status (RCW 11.02.005(22); RCW 30A.22.902 for domestic partners). A decree of separation does not.
- **Agreements can defeat survivorship accounts between the parties.**
  - *Lyon v. Lyon*, 100 Wn.2d 409, 670 P.2d 272 (1983): the spouse's rights "under the community property agreement prevail over [the] joint tenancy right of survivorship". That case involved real property.
  - *Morse v. Williams*, 48 Wn. App. 734 (1987): a community property agreement plus a separation contract defeated a later survivorship account.
  - Because § 190(1) reaches only funds payable to a PR, this matters for disputes, not for Path C.
- **Other limits.** The statute adds creditors' rights and the slayer and abuser carve-outs (RCW 26.16.120; 11.84.030). The recipient takes subject to the decedent's debts (RCW 11.18.200(2)(a)).

**W8: the $2,500 payment.**
- **Per account or aggregate?** The text reads "the balance of the funds **in the name of** a deceased depositor", not "in the account". A per-institution aggregate reading is plausible (reviewer inference). The conservative policy is to aggregate all accounts in the decedent's name at the institution.
- **Next of kin.** The phrase is undefined in chapter 30A.22. RCW 30A.22.902 extends it to registered domestic partners. RCW 11.28.120(1)(b) ranks next of kin for administration as children, parents, siblings, grandchildren, nephews and nieces. That is a reasonable reference for a policy priority, but it is not binding here.
- **Creditors.** The statute expressly permits a "funeral director, or other creditor". The recipient is "answerable and accountable" to a later PR. Reviewer inference: no conflict with any duty of the institution, which is discharged under RCW 30A.22.120.
- **Amount history.** Whether 1989 c 220 s 3 set the $2,500 is unverified. The amount has been unchanged at least since the 2014 recodification.

**W9: community property interests.**
- **Statute says.**
  - RCW 30A.22.030(5): community and separate property rights "shall not be affected by the form of the account".
  - RCW 30A.22.080: the institution may contract "without regard as to whether the funds on deposit are the community or separate property".
  - RCW 30A.22.110 and .120: ownership rules have "no bearing on ... the right of a financial institution to make payments".
  - RCW 11.11.005(1)(e); 11.11.020(1) ("Subject to community property rights").
- **Reviewer inference.** Community property claims do not change the institution's decision. They become relevant only as a dispute notice (RCW 30A.22.120, .210).
  - On Path B, the spouse's community half is excluded from the $100,000 test and is a separate successor interest (RCW 11.62.005(2)(a)(ii)). The engine properly relies on the affidavit.
- **Can it be answered now?** The default is supported.

**W10: confirm every citation.** Done in the claim audit. Corrections needed:
- #2: California amount by date of death;
- #11 and #73: RCW 11.02.005(13) versus (14);
- #43: tax release limited to state or local taxing authorities;
- #45, #57, #58: day counting;
- #79: $2,500 amendment history;
- #80: sources.md histories.

**W11: credit union $1,000 payment.**
- **Statute says.** RCW 11.62.030: "may pay"; the cap applies where "the amount of deposit does not exceed ... one thousand dollars". The affidavit states death and that no executor or administrator was appointed. Protection is for payment "made in good faith", which is a different standard from the actual-knowledge tests elsewhere. The spouse must account to a later PR.
- **Reviewer inference.** For credit unions this is largely superseded by RCW 30A.22.190(2) ($2,500, more payees, actual-knowledge standard). It adds little in v1 unless W8 is declined.

## Edge cases and risks

| # | Fact pattern or risk | Severity | Likelihood | Authority |
|---|---|---|---|---|
| E1 | Payment on day 40 or notice + 10 is premature; the affiant's (d) or (h) statement is false on its face | High | High (every Path B case) | *Troxell*; *Christensen*; RCW 11.62.020 (discharge lost only on "actual knowledge of the falsity") |
| E2 | A policy-added Path B wait or document leads a successor to sue to compel | High | Medium | RCW 11.62.010(1) "shall pay"; 11.62.020 recovery proceeding |
| E3 | A POD beneficiary dies 2 days after the depositor; the engine pays that beneficiary's estate share instead of treating them as predeceased | High | Low to medium | RCW 11.05A.020, .030, .070 |
| E4 | The signature card is missing or doesn't match the core-system POD flag | Medium | Medium | RCW 30A.22.060; *Brownfield* |
| E5 | An informal letter from a testamentary beneficiary (not RCW 11.11.050-compliant) reaches the branch manager | Medium | Medium | RCW 30A.22.120, .210, .040(2) |
| E6 | A non-conforming testamentary notice arrives less than 5 business days before payment | Medium | Low | RCW 11.11.010(1)(b) presumptions |
| E7 | A beneficiary or survivor is charged with or convicted of killing the decedent, or is an alleged abuser | Medium | Low | RCW 11.84.020, .050, .110 |
| E8 | An agent under a POA or agency account withdraws after the death, before the institution knows | Medium | Medium | RCW 30A.22.170; 11.125.100(5) |
| E9 | The institution offsets the decedent's loan against a surviving joint holder's CD | Medium | Low | *Kalk*, 126 Wn.2d 346 |
| E10 | The spouse's community property agreement payment proceeds, but the spouses had mutually rescinded the agreement (for example, by mutual wills) | Medium | Low | *Higgins*; *Bachmeier*; *Wittman* |
| E11 | Former-spouse POD beneficiary; notice of the decree arrives without identifying the account | Low to medium | Low | RCW 11.07.010(3)(d) (notice must "identify the nonprobate asset with reasonable specificity") |
| E12 | A $2,500-rule payment is applied per account while the decedent has several small accounts | Medium | Medium | RCW 30A.22.190(2) ("funds in the name of a deceased depositor"); reviewer inference |
| E13 | Several partial affidavits whose claimed portions add up to more than 100% | Medium | Low | RCW 11.62.020 (first affidavit received, or implead) |
| E14 | A Medicaid recipient aged 55 or over; DSHS is a successor but received no (2)(h) notice | Medium | Medium | RCW 11.62.005(2)(a)(iii); 43.20B.080(3); reviewer inference |
| E15 | A PR application by a third party after day 60 or 90 (2026 amendments) while a Path B claim is pending | Low | Low | RCW 11.28.120(2), (3) as amended by 2026 c 204 § 2 |
| E16 | A renewing CD's POD designation dates from account opening for superwill comparisons | Low | Low | RCW 11.11.020(4) |
| E17 | The account has been escheated to the state | Low | Low | RCW 63.30.040(5) |

## Sources consulted

All were accessed 2026-10-09.

**Primary: official RCW** (`https://app.leg.wa.gov/RCW/default.aspx?cite=<section>&full=true`):
- **Small estates:** 11.62.005, .010, .020, .030.
- **Chapter 30A.22:** .010, .020, .030, .040, .050, .060, .070, .080, .090, .100, .110, .120, .130, .140, .150, .160, .170, .180, .190, .200, .210, .220, .230, .240, .250, .260, .900, .902.
- **Title 11:**
  - 11.07.010;
  - 11.11.003, .005, .007, .010, .020, .040, .050, .070, .080, .901;
  - 11.02.005; 11.04.015;
  - 11.05A.010, .020, .030, .040, .050, .060, .070;
  - 11.84.010, .020, .030, .040, .050, .100, .110, .120, .130, .140, .150, .160, .170, .180, .900;
  - 11.125.040, .100, .110;
  - 11.42.010, .020, .085; 11.18.200; 11.40.010, .020, .051; 11.28.237.
- **Other titles:**
  - 1.12.040; 1.16.050; 26.16.120; 43.20B.080;
  - 74.34.020, .215;
  - 63.30.010, .040, .050;
  - 83.100.020, .120, .130, .150;
  - 31.12.025.

**Primary: RCW archive and session law:**
- https://lawfilesext.leg.wa.gov/law/RCWArchive/2023/pdf/RCW%20%2011%20%20TITLE/RCW%20%2011%20.%2062%20%20CHAPTER/RCW%20%2011%20.%2062%20.010.pdf (and the 2025 equivalent)
- the RCW 11.02.005 archive PDFs for 2023 and 2025 (same path pattern)
- 2026 c 204 (EHB 2445): https://lawfilesext.leg.wa.gov/biennium/2025-26/Htm/Bills/Session%20Laws/House/2445.SL.htm

**Primary: WAC:** chapter 182-527 WAC, https://app.leg.wa.gov/WAC/default.aspx?cite=182-527&full=true

**Primary: cases** (full text from the Caselaw Access Project, `https://static.case.law/...`):
- *Manary v. Anderson*, 176 Wn.2d 342 (2013): wash-2d/176/cases/0342-01.json
- *Kalk v. Security Pacific Bank Washington N.A.*, 126 Wn.2d 346 (1995): wash-2d/126/cases/0346-01.json. Also the Court of Appeals decision, 73 Wn. App. 13, 866 P.2d 1276 (1994): wash-app/73/cases/0013-01.json
- *Baker v. Leonard*, 120 Wn.2d 538, 843 P.2d 1050 (1993): wash-2d/120/cases/0538-01.json
- *Johnson v. Bachmeier* (*In re Estate of Bachmeier*), 147 Wn.2d 60 (2002): wash-2d/147/cases/0060-01.json
- *Higgins v. Stafford*, 123 Wn.2d 160, 866 P.2d 31 (1994): wash-2d/123/cases/0160-01.json (downloaded; relied on only as summarized in *Bachmeier*)
- *Lyon v. Lyon*, 100 Wn.2d 409, 670 P.2d 272 (1983): wash-2d/100/cases/0409-01.json
- *Seeley v. Godfrey* (*In re Estate of Wittman*), 58 Wn.2d 841, 365 P.2d 17 (1961): wash-2d/58/cases/0841-01.json
- *Christensen v. Ellsworth*, 162 Wn.2d 365 (2007): wash-2d/162/cases/0365-01.json
- *Troxell v. Rainier Pub. Sch. Dist. No. 307*, 154 Wn.2d 345, 111 P.3d 1173 (2005): wash-2d/154/cases/0345-01.json
- *In re Estate of Burks*, 124 Wn. App. 327, 100 P.3d 328 (2004): wash-app/124/cases/0327-01.json
- *Dahle v. Nadolski*, 127 Wn. App. 783 (2005): wash-app/127/cases/0783-01.json
- *Estate of Brownfield v. Bank of America, NA*, 170 Wn. App. 553 (2012): wash-app/170/cases/0553-01.json
- *Taufen v. Estate of Kirpes*, 155 Wn. App. 598 (2010): wash-app/155/cases/0598-01.json
- *Garten v. Daley* (*Estate of Krappes*), 121 Wn. App. 653, 91 P.3d 96 (2004): wash-app/121/cases/0653-01.json
- *Morse v. Williams*, 48 Wn. App. 734, 740 P.2d 884 (1987): wash-app/48/cases/0734-01.json
- *In re Estate of Fox*, 51 Wn. App. 498, 754 P.2d 690 (1988): wash-app/51/cases/0498-01.json
- *Meyer v. Moore*, 60 Wn. App. 39 (1990): wash-app/60/cases/0039-01.json
- *Kitsap Bank v. Denley*, 177 Wn. App. 559 (2013): wash-app/177/cases/0559-01.json
- Read but not relied on: *Willis v. Estate of Tosh*, 83 Wn. App. 158 (1996); *Sunderland v. Whitcomb* (*Estate of Furst*), 113 Wn. App. 839 (2002); *Collister v. Feller*, 195 Wn. App. 371 (2016)

**Primary: California** (via the mirror; confirm at leginfo.legislature.ca.gov):
- https://california.public.law/codes/probate_code_section_5302, _13100, _13101, _890, _13104
- Judicial Council list: https://courts.ca.gov/system/files/file/probate-code-890-adjusted-amounts.pdf

**Secondary:**
- Northwest Justice Project, Small Estate Affidavit form (2025-08): https://assets.washingtonlawhelp.org/sites/default/files/forms/pdf/2026-06/njp-planning-532-small-estate-affidavit-2025_08.pdf
- Web search results giving 2026 c 204's effective date (June 11, 2026) and bill history (HB 2445 bill summary, apps.leg.wa.gov). The date was not independently confirmed.
- CourtListener search API, used only to identify cases and some parallel cites (Manary 292 P.3d 96; Kalk 894 P.2d 559; Taufen 230 P.3d 199; Kitsap Bank 312 P.3d 711; Dahle / Estate of Cordero 113 P.3d 16).

## Items the attorney must confirm

1. **W4.** Does the *Troxell* and *Christensen* waiting-period rule govern RCW 11.62.010? If so, earliest payment is death + 41 and notice + 11, with no weekend or holiday extension. Correct GS-WA-001 and -002 to 2025-07-12 and 2025-07-19.
2. **Mandatory duty.** Whether RCW 11.62.010(1)'s "shall pay" bars institution policies that add waiting days or documents on Path B. This affects the architecture's stricter-only policy model.
3. **W5.** Whether to pay a share-only claim on the affidavit (the statutory reading) rather than mark it not determinable.
4. **W3.** That chapter 11.11 prevails over RCW 30A.22.100's last sentence, and that a non-conforming written notice still counts as "dispute" knowledge under RCW 30A.22.120 and .210.
5. **W2.** Which divisor applies under RCW 30A.22.160, and how to release the remaining balance.
6. **120-hour rule.** Whether to add the RCW 11.05A rule to Path A, and what date and time facts are needed.
7. **Joint accounts.** That proof of death is policy, not statute, for joint accounts with survivorship (RCW 30A.22.140).
8. **Signed contract.** That the engine should require staff confirmation of a signed contract of deposit (RCW 30A.22.060; *Brownfield*).
9. **W6.** That the claimant mails the DSHS copy and that it is not a payment condition. Also whether DSHS must receive (2)(h) successor notice for Medicaid recipients aged 55 and over.
10. **W7.** Whether RCW 30A.22.120's discharge covers § 190(1) payments to a non-depositor spouse, and how much staff review of the agreement's scope is needed.
11. **W8.** Whether the $2,500 is per account or aggregate; which relationships count as "next of kin"; and the 1989 c 220 history of the amount.
12. **Kalk.** The effect on any institution setoff against survivor or POD funds.
13. **Citations.** RCW 11.02.005(13) versus (14) for each date of death, and 2026 c 204's effective date.
14. **California.** The comparison row's dollar amount by date of death ($184,500 versus $208,850).
15. **Not researched.** Federal overlays (Treasury reclamation, levies, OFAC, NCUA and OCC preemption) and payment to minor beneficiaries.
