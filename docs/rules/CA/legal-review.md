> **Provenance.** Generated 2026-10-09 by the `estate-law-reviewer` AI research agent (`.claude/agents/estate-law-reviewer.md`). It is research for a licensed attorney, not legal advice.
>
> **Independent spot-check** (2026-10-09; five citations re-fetched and compared word for word):
> - Prob. Code § 13106.5(a): confirmed. The spec's description is wrong, as the review says.
> - § 5407(b) (minor POD/Totten payees): confirmed.
> - Fin. Code § 1450(d) (CAMPAL does not limit adverse-claim rules): confirmed.
> - *Mautner v. Peralta*, 215 Cal.App.3d 796 holding: confirmed.
> - *Placencia v. Strazicich* (G055631) slip opinion: both quoted sentences confirmed.
>
> California statute text is from the california.public.law mirror and still needs confirmation on leginfo (Q9). The remaining citations have not been independently re-checked.

# California deceased-account rule spec: legal research review

**This is research for a licensed attorney to verify. I am not the client's attorney, and nothing here is legal advice or attorney sign-off.**

- **Date:** 2026-10-09
- **Scope:** California rules for paying a deceased customer's deposit account, deaths on or after 2022-04-01. Paths A (multiple-party accounts), B (small-estate affidavit) and C (surviving spouse); 16 draft golden scenarios; open questions Q2, Q3, Q5, Q6, Q8 and Q9. I also checked the California column of the "How Washington differs from California" table, which is in `docs/rules/WA/spec.md`.
- **Documents reviewed (read in full):** `docs/rules/CA/spec.md`, `docs/rules/CA/open-questions.md`, `docs/rules/CA/sources.md`, `ARCHITECTURE.md`, and the "How Washington differs from California" section of `docs/rules/WA/spec.md`. I also extracted and skimmed `docs/rules/CA/CA-attorney-review.docx`; its text matches the three Markdown files.
- **Method:** I listed every legal or factual claim and checked each one against statute or case text I retrieved during this session. I then researched gaps, the assigned open questions, and edge cases. Each conclusion is labelled **Statute says**, **Case law holds**, **Regulator/secondary guidance**, or **Reviewer inference**.
- **Limitations:**
  1. **Statute text came from a mirror, not the official site.** leginfo.legislature.ca.gov returned HTTP 403 to automated requests (tested 2026-10-09), so all California code text came from the california.public.law mirror. The mirror cites leginfo and shows each section as "accessed Oct. 5, 2026". Every section must be confirmed on leginfo (Q9).
  2. **Case law was searched, not exhausted.** Full opinion text came from the Caselaw Access Project (static.case.law) and from a Justia slip-opinion PDF. CourtListener's search API was used to find cases until it hit its hourly rate limit, so case coverage is not exhaustive. I had no Westlaw or Lexis access, so I could not Shepardize or KeyCite anything.
  3. **One reporter citation comes from a secondary source.** For *Placencia v. Strazicich*, I read the slip opinion, but the reporter citation (42 Cal.App.5th 730) comes from a vLex listing.
  4. **I did not read Law Revision Commission comments or legislative history.**

---

## Summary

**Counts (72 claims audited):**

| Classification | Count |
|---|---|
| Verified | 46 |
| Verified with correction | 24 |
| Inaccurate | 1 |
| Unsupported | 0 |
| Unverified (open legal question; no controlling authority located) | 1 |

All dollar limits and breakpoint dates match the official Judicial Council § 890 list. The PDF retrieved on 2026-10-09 has SHA-256 `cb30e97d3b4322512bcd3a5cda8eff5eb3de26c66a0473d9a15295e076eedf56`, which matches `sources.md`. All 16 golden-scenario dates are consistent with the statute, except that the exact payment date in GS-CA-001 depends on Q3.

**Most important findings, ranked:**

1. **The engine cannot treat "who may the institution pay" (§ 5405 protection) as "who owns the money" (§ 5302).**
   - Section 5302(a) and (c)(2) let clear and convincing evidence of a different intent override survivorship and Totten designations. *Placencia v. Strazicich* (2019) holds that a will can supply that evidence despite § 5302(e). *Araiza v. Younkin* (2010) holds the same for a living trust.
   - Both courts say, or are consistent with, the rule that the institution is still protected if it pays according to the account terms.
   - So the Washington spec's California entry, "will override: Not possible (§ 5302(e))", is misleading. Path A output should say "payment protected under § 5405", not "funds belong to".
2. **Path B has no rule for adverse claims or holds, and § 13106 protection depends on good faith.**
   - Section 13106(a) protects a holder that relies "in good faith". *Mautner v. Peralta* (1989) held that the predecessor immunity (former § 631) did not apply where the bank had actual notice of a superior claim and a request to hold before the affidavit arrived.
   - Financial Code § 1450 (banks) and § 6661 (savings associations) add adverse-claim and court-order rules that CAMPAL does not limit.
   - Path B needs a "notice of adverse claim / restraining order / levy received" not-determinable condition.
3. **Institution policy that is "stricter than the statute" carries fee risk on Path B.** Under § 13105(b), the court "shall award reasonable attorney's fees" if the holder acted unreasonably in refusing to pay. Section 12572 gives sister-state personal representatives the same right. Extra documents or waiting days are therefore not risk-free. This affects ARCHITECTURE.md's policy model, and it means Q8 is partly a Law question.
4. **The 40-day date (Q3) is unresolved.**
   - CCP § 12, Civil Code § 10 and Government Code § 6800 exclude the first day and include the last. Under that count, the 40th day after a 2025-06-01 death is 2025-07-11.
   - Whether 40 days "have elapsed" on day 40 or only once day 40 has ended (2025-07-12) is not settled by any authority I located.
   - Recommend a conservative default of death date + 41 until an attorney decides.
5. **The § 5040 (former spouse) rule also reaches joint-account survivorship, not only POD/Totten.** Section 5302 is expressly "Subject to Section 5040", and § 5040(e) covers account-agreement provisions. GS-CA-010 and the not-determinable list should be widened.
6. **Payees and successors who are minors, simultaneous deaths, and slayers are not handled.**
   - Statute says § 5407(b) requires that a POD or Totten payee who is a minor be paid under CUTMA or Prob. Code § 3400 et seq.
   - Sections 220–223, 6403 and 21109 impose clear-and-convincing and 120-hour survival rules.
   - Sections 250, 251 and 256 (slayer) protect the institution only until it receives written notice of a claim.
7. **One not-determinable condition is mis-stated.** The § 13106.5 item ("account is secured by a lien on real property") misdescribes the section. Section 13106.5 is about collecting a debt that is owed to the decedent and secured by a recorded real-property lien. A deposit account is not such a debt.
8. **Q5 (spouse collecting without the affidavit):** I found no statutory procedure that lets a surviving spouse collect a deposit account in the decedent's sole name on spousal status alone, with holder protection.
   - Section 13600 covers employer wages only, and § 13545 covers securities registered in the surviving spouse's name.
   - The available routes are the § 13100 affidavit (spouse as successor) or a § 13650 spousal property order (§§ 13656–13657).
   - Path C can therefore stay not determinable, with a new "court order under § 13656" route as an option.
9. **The value test is "current" value.** Section 13101(a)(5) requires the affiant to state the **current** gross fair market value, while the dollar cap is fixed by the date of death. The spec and the facts schema don't say this.
10. **Federal and state overlays are missing.** These include Treasury reclamation of post-death federal benefit deposits (31 CFR 210.10), escheat of dormant deceased-owner accounts (CCP §§ 1513, 1532, 1560), FTB orders to withhold (Rev. & Tax. Code § 18670), and Medi-Cal notice (Prob. Code § 215).

---

## Claim audit

Statute text was read on the mirror `https://california.public.law/codes/<code>_section_<n>`. The official URL for the attorney to confirm is `https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=<n>` (replace PROB with CIV, CCP, GOV, FIN, RTC or WIC for other codes). All mirror pages were retrieved 2026-10-09.

| # | Location | Claim | Finding | Authority (quote + URL) | Recommended change |
|---|---|---|---|---|---|
| 1 | spec › Path A › Who is paid | Joint account: sums belong to the surviving party or parties (§ 5302(a)). | **Verified with correction.** Statute says the rule is "subject to Section 5040" and is rebuttable. Case law holds that it governs beneficial ownership, while the institution may still pay per the account terms. | § 5302(a): "belong to the surviving party or parties as against the estate of the decedent unless there is clear and convincing evidence of a different intent." https://california.public.law/codes/probate_code_section_5302 ; *Placencia* (row 70 sources): "The financial institution may pay the surviving party according to the terms of the account, but the decedent's estate has a claim for the funds against the surviving party." | Reword to "the institution may pay the surviving party(ies) per the account terms (§§ 5401, 5402) and is protected (§ 5405); beneficial ownership is rebuttable (§ 5302(a))." |
| 2 | spec › Path A › Who is paid | POD, sole or last party deceased: sums belong to the surviving POD payee(s) (§ 5302(b)(2)). | **Verified.** Statute says that if a payee predeceases the party, the survivors among the payees take. | § 5302(b)(2)(A): "belong to the P.O.D. payee or payees if surviving, or to the survivor of them if one or more die before the party" (same URL) | Add a scenario: two payees, one predeceased, so the survivor takes 1/1. |
| 3 | spec › Path A › Who is paid | Totten, sole or last trustee deceased: sums belong to the surviving beneficiaries (§ 5302(c)(2)). | **Verified with correction.** Statute says this is rebuttable. Case law holds that a living trust can show a different intent. | § 5302(c)(2)(A): "unless there is clear and convincing evidence of a different intent" (same URL); *Araiza*: "Because the change was made by a living trust rather than by a will, it is not invalidated by section 5302, subdivision (e)." https://static.case.law/cal-app-4th/188/cases/1120-01.json | Same as row 1. Also consider § 5406 (an account "as trustee for" is paid as a Totten account absent written notice). |
| 4 | spec › Path A › Shares | POD/Totten: equal shares unless the account terms set different shares. | **Verified.** Statute requires that the terms "expressly provide". | § 5302(b)(2)(B), (c)(2)(B): "in equal and undivided shares unless the terms of the account or deposit agreement expressly provide for different shares" (same URL) | Require that terms shares be express. Note: there is no survivorship among payees after the death unless the terms say so (§ 5302(b)(2)(C), (c)(2)(C)). |
| 5 | spec › Path A › Shares | Joint, two or more survivors: may pay any one or more per the terms; no net-contribution inquiry; protected. | **Verified.** | § 5401(a): "Any multiple-party account may be paid, on request and according to its terms, to any one or more of the parties or agents." § 5401(c)(2): not required to "Determine any party's net contribution." https://california.public.law/codes/probate_code_section_5401 ; § 5405(a) (row 10) | None. |
| 6 | spec › Path A › Documents | POD: proof the payee survived every original party. | **Verified.** | § 5403: "upon presentation to the financial institution of proof of death showing that the P.O.D. payee survived all persons named as original payees." https://california.public.law/codes/probate_code_section_5403 | Define "proof of death" per § 5144: a certified copy of the death certificate or another prima facie record. https://california.public.law/codes/probate_code_section_5144 |
| 7 | spec › Path A › Documents | Totten: proof the beneficiary survived every trustee. | **Verified.** | § 5404: "if proof of death is presented to the financial institution showing that the beneficiary or beneficiaries survived all persons named as trustees." https://california.public.law/codes/probate_code_section_5404 | None. |
| 8 | spec › Path A › Documents | Joint: claimant must be a surviving party; paying the representative or heirs needs proof the decedent was the last surviving party. | **Verified.** | § 5402: "payment may not be made to the personal representative or heirs of a deceased party unless proof of death is presented ... showing that the decedent was the last surviving party or unless there is no right of survivorship under Section 5302." https://california.public.law/codes/probate_code_section_5402 | None. |
| 9 | spec › Path A › Earliest payment | Payable on request once proof of death is presented; no statutory waiting period. | **Verified.** §§ 5401–5404 contain no waiting period. That no other waiting period applies is a **Reviewer inference** from my reading of §§ 5401–5405. | §§ 5402–5404 (URLs above): "on request" | None. Gaps G9–G11 (levies, reclamation) may still delay payment in practice. |
| 10 | spec › Path A › Liability protection | Payment under §§ 5401–5404 discharges the institution from all claims, even if inconsistent with beneficial ownership. | **Verified with correction.** Case law holds that protection presupposes the payee is a proper party under the account terms (e.g. not added in violation of § 5303). Statute says protection is not affected by other notices (§ 5405(b), second sentence). | § 5405(a): "discharges the financial institution from all claims for amounts so paid whether or not the payment is consistent with the beneficial ownership." https://california.public.law/codes/probate_code_section_5405 ; *Stevens*: "this presupposes the person is a proper party." https://static.case.law/cal-app-4th/177/cases/0236-01.json | Add: protection assumes the payee's status comes from account terms validly set or changed under § 5303. Cite § 5405(b): "No other notice or any other information ... shall affect its right to the protection." |
| 11 | spec › Path A › Liability; Not determinable | No protection after the institution is served with a court order restraining payment. | **Verified.** | § 5405(b): "does not extend to payments made after the financial institution has been served with a court order restraining payment." (same URL) | Also see Fin. Code § 1450(b), § 6661(b) and gap G4. |
| 12 | spec › Path A › Not determinable | Former spouse as POD payee or Totten beneficiary: may fail under § 5040. | **Verified with correction.** Statute says it applies to any "nonprobate transfer", which includes account-agreement provisions (§§ 5040(e), 5000(a)). Section 5302 itself is "Subject to Section 5040", so joint-account survivorship in favor of a former spouse is also covered. Section 5040(a) requires an instrument "executed by the transferor before or during the marriage". Section 5048(c) keeps pre-2002 law where the dissolution was before 2002. | § 5040(a): "a nonprobate transfer to the transferor's former spouse ... fails if, at the time of the transferor's death, the former spouse is not the transferor's surviving spouse." https://california.public.law/codes/probate_code_section_5040 ; § 5048(c) https://california.public.law/codes/probate_code_section_5048 | Extend to a surviving joint party who is a former spouse or former registered domestic partner. Keep it not determinable. |
| 13 | spec › Path A › Not determinable | If no POD payee or Totten beneficiary survived, the account passes through the estate (Path B or probate). | **Verified with correction.** Statute says it goes to the estate only if **no** payee survived (§ 5302(b)(2)(A), "survivor of them"). Sections 5403 and 5404 also allow paying the personal representative or heirs of the last survivor on proof of death. | §§ 5302, 5403, 5404 (URLs above) | Clarify "no payee survived the last party". |
| 14 | spec › Path A › Not determinable | Terms require multiple survivors' signatures (§ 5401(b)), or a § 5405(c) written notice is held. | **Verified.** Statute says § 5405(c) excludes checking, share-draft and similar accounts. Section 5401(b) says such terms "do not limit the right of the sole survivor or of all of the survivors to receive the sums." | § 5405(c) (URL above); § 5401(b) (URL above) | Keep it not determinable (conservative). Note the checking-account carve-out for later refinement. |
| 15 | spec › Path B › Eligibility | Gross value of California real and personal property ≤ the limit, excluding § 13050 property and § 13151-petition property; the listed exclusions. | **Verified with correction.** The spec's list omits § 13050(a)(1) "a life or other interest terminable upon the decedent's death". Vehicles also include those "titled under Division 16.5"; manufactured homes include "commercial coach, truck camper, or floating home". Statute says the affidavit states the **current** gross fair market value (§ 13101(a)(5)). | § 13050(a)(1): "held by the decedent as a joint tenant, or in which the decedent had a life or other interest terminable upon the decedent's death ... shall be excluded." https://california.public.law/codes/probate_code_section_13050 ; § 13101(a)(5): "The current gross fair market value..." https://california.public.law/codes/probate_code_section_13101 | Add the missing exclusion. Define `declared_value` as the current gross fair market value stated in the affidavit. |
| 16 | spec › Path B › Eligibility | Excludes Armed Forces pay and wages up to the § 13050(c) adjusted amount. | **Verified.** The Judicial Council list gives $18,450 (deaths 2022-04-01 to 2025-03-31) and $20,875 (from 2025-04-01). | § 13050(c)(1)–(2) (URL above); JC list: "§ 13050(c) $16,625 $18,450 $20,875" https://courts.ca.gov/system/files/file/probate-code-890-adjusted-amounts.pdf | None. |
| 17 | spec › Path B › Eligibility | At least 40 days have elapsed since the death (§§ 13100, 13101(a)(3)). | **Verified.** | § 13100: "and if 40 days have elapsed since the death of the decedent" https://california.public.law/codes/probate_code_section_13100 | See row 50 (Q3). |
| 18 | spec › Path B › Eligibility | No California administration proceeding, or the personal representative consented in writing. | **Verified.** Statute says the same rule appears in § 13108(a). Only a **California** proceeding bars use. | § 13101(a)(4)(A): "No proceeding is now being or has been conducted in California for administration of the decedent's estate." § 13108(a) https://california.public.law/codes/probate_code_section_13108 | Cite § 13108 too. |
| 19 | spec › Path B › Value limit | Limit set under § 890 and published by the Judicial Council; a value equal to the limit is eligible. | **Verified.** | § 13100: "does not exceed"; § 890(c) https://california.public.law/codes/probate_code_section_890 | None. |
| 20 | spec › Path B › Value limit | Death before 2022-04-01: $166,250. | **Verified.** | § 13101(g)(1): "one hundred sixty-six thousand two hundred fifty dollars ($166,250)"; JC list | None. |
| 21 | spec › Path B › Value limit | Death 2022-04-01 to 2025-03-31: $184,500. | **Verified.** | JC list, row "§§ 13100, 13101 $166,250 $184,500 $208,850" | None. |
| 22 | spec › Path B › Value limit | Death on or after 2025-04-01: $208,850. | **Verified.** | JC list (as above) | None. |
| 23 | spec › Path B › Value limit | Next adjustment scheduled 2028-04-01. | **Verified.** | JC list: "Unless otherwise provided by statute, these amounts will next be adjusted on April 1, 2028." | Keep the "unless otherwise provided by statute" caveat. |
| 24 | spec › Path B › Value limit | An adjustment never applies to a death before its effective date (§ 890(d)). | **Verified.** | § 890(d): "Adjustments ... do not apply when the decedent's death preceded the date of adjustment." (URL above) | None. |
| 25 | spec › Path B › Value limit | Coverage begins with deaths on 2022-04-01. | **Verified** as an owner decision. It is consistent with the statutory breakpoint in § 13101(f), (g). | § 13101(f), (g) (URL above) | None. |
| 26 | spec › Path B › Who is paid | Pay those who sign as successor, or as a § 13051 representative; a successor takes under the will or by intestacy. | **Verified with correction.** Statute says "successor" means the sole beneficiary **or all** of the beneficiaries. A trust can be a beneficiary under the will. Sister-state or foreign succession law may govern. A sister-state personal representative may also use the procedure (§§ 12570, 13051(d)). | § 13006(a): "the sole beneficiary or all of the beneficiaries who succeeded to a particular item of property." https://california.public.law/codes/probate_code_section_13006 ; § 12570: "a sister state personal representative may ... use the affidavit procedure." https://california.public.law/codes/probate_code_section_12570 | Add the sister-state personal representative as an affiant capacity. Engine facts should show whether the affiants are all the successors. |
| 27 | spec › Path B › Who is paid | The institution may rely in good faith on the affidavit and has no duty to check its statements. | **Verified with correction.** Statute says reliance must be "in good faith". Case law holds that, for the predecessor statute, actual notice of a superior claim plus a hold request removed the immunity. | § 13106(a): "The holder may rely in good faith on the statements ... and has no duty to inquire." https://california.public.law/codes/probate_code_section_13106 ; *Mautner*: "renders its grant of immunity inapplicable where the holder has actual notice of a statutory heir's superior claim and a request to 'hold' distribution of decedent's funds prior to receiving a '630' affidavit." https://static.case.law/cal-app-3d/215/cases/0796-01.json | Add a fact "notice of adverse or superior claim received before payment"; if true, the result is not determinable. |
| 28 | spec › Path B › Shares | One affiant receives 100%. | **Verified with correction.** This is a **Reviewer inference** from § 13006: it is correct only if the single affiant is the **sole** successor to the account, or a § 13051 representative of all successors. Statement (9) also requires "No other person has a superior right." | § 13006 (URL above); § 13101(a)(9) (URL above) | Make it a fact that the affiant(s) are all the successors to this item; if not known, not determinable. |
| 29 | spec › Path B › Shares | Several affiants are together entitled; the affidavit is "modified as appropriate". | **Verified.** | § 13105(a)(1): "The person or persons executing the affidavit ... are entitled to have the property ... paid, delivered, or transferred to them." https://california.public.law/codes/probate_code_section_13105 ; § 13101(b) | See Q2. |
| 30 | spec › Path B › Documents 1–4 | Affidavit with every § 13101(a) statement; certified death certificate; the § 890 list for deaths from 2022-04-01; PR consent and letters. | **Verified.** Statute says items 2–4 must be **attached** to the affidavit. | § 13101(d): "A certified copy of the decedent's death certificate shall be attached"; (e); (f): "the list of adjusted dollar amounts ... in effect on the date of the decedent's death, shall be attached" (URL above) | Say "attached to the affidavit". |
| 31 | spec › Path B › Documents 5 | Evidence of ownership, or a bond or indemnity agreement. | **Verified with correction.** Statute says the evidence is required "if available". If it is not presented, the holder **may** require a bond, or may agree to an indemnity instead. A bond is not mandatory. | § 13102(b): "the holder may require, as a condition for the payment ... a bond or undertaking in a reasonable amount." https://california.public.law/codes/probate_code_section_13102 | Model the bond as an institution option, not a statutory requirement. |
| 32 | spec › Path B › Documents 6 | California real property: inventory and appraisal by a probate referee. | **Verified.** | § 13103: "the affidavit or declaration shall be accompanied by an inventory and appraisal of the real property." https://california.public.law/codes/probate_code_section_13103 | None. |
| 33 | spec › Path B › Documents 7 | Reasonable proof of each affiant's identity. | **Verified with correction.** Statute adds a holder duty: unless notarized, the holder must note on the affidavit how identity was established. | § 13104(f): "the holder shall note on the affidavit or declaration either that the person ... is personally known or a description of the identification provided." https://california.public.law/codes/probate_code_section_13104 | Add the notation duty to the documents and checklist output. |
| 34 | spec › Path B › Earliest payment | Earliest payment is the date 40 days have elapsed (death date + 40 assumed). | **Unverified.** No controlling authority located (see Q3). | CCP § 12, Civ. Code § 10, Gov. Code § 6800 (Sources) | Default to death + 41 until an attorney decides. |
| 35 | spec › Path B › Liability protection | If §§ 13100–13104 are satisfied, receipt of the affidavit discharges the holder; no liability for state taxes. | **Verified.** | § 13106(a): "constitutes sufficient acquittance ... and discharges the holder from any further liability"; (b): "is not liable for any taxes due to this state." (URL above) | Add the good-faith caveat (row 27). |
| 36 | spec › Path B › Not determinable | "The account is secured by a lien on real property (§ 13106.5)." | **Inaccurate.** Statute says § 13106.5 governs collecting a **debt owed to the decedent** that is secured by a recorded real-property lien. A deposit account is not such a debt. | § 13106.5(a): "If the particular item of property transferred under this chapter is a debt or other obligation secured by a lien on real property..." https://california.public.law/codes/probate_code_section_13106.5 | Delete, or restate as "item is not a deposit account (e.g. a secured note owed to the decedent): out of scope". |
| 37 | spec › Path B › Not determinable | Over the limit; administration without consent; no declared value. | **Verified.** These follow from §§ 13100, 13101(a)(4) and (a)(5). | URLs above | None. |
| 38 | spec › Path C | Under § 13500, property passing to a surviving spouse needs no administration. | **Verified with correction.** Statute says this is subject to Chapters 2 and 3 (§§ 13540 et seq., 13550 et seq.). Section 13501 lists property that **is** subject to administration (e.g. property left in trust, or qualified ownership). Section 13502 allows an election to administer. | § 13500: "the property passes to the survivor subject to the provisions of Chapter 2 ... and Chapter 3 ... and no administration is necessary." https://california.public.law/codes/probate_code_section_13500 ; § 13501 https://california.public.law/codes/probate_code_section_13501 | Note §§ 13501 and 13502. See Q5. |
| 39 | spec › Path C | § 13540 covers real property only. | **Verified.** Statute says § 13545 covers securities registered in the surviving spouse's name. Neither section covers a deposit account in the decedent's name. | § 13540(a): "full power to sell, convey, lease, mortgage ... the community or quasi-community real property" https://california.public.law/codes/probate_code_section_13540 ; § 13545 https://california.public.law/codes/probate_code_section_13545 | None. |
| 40 | spec › Path C | A spouse who is a POD payee or joint party uses Path A; a spouse who signs an affidavit uses Path B. | **Verified.** Statute says the affidavit procedure is cumulative with other procedures (§ 13116). Property passing to the spouse under § 13500 is excluded from the value (§ 13050(a)(1)). | § 13116: "in addition to and supplemental to any other procedure" https://california.public.law/codes/probate_code_section_13116 | Note that a spouse-successor's § 13500 property doesn't count toward the limit. |
| 41 | spec › Intestate shares | Community property to the spouse; separate property split between the spouse and issue, parents, or siblings. | **Verified with correction.** Also covers quasi-community property (§ 6401(b)), more remote kin (§ 6402(d)–(g)), and § 6402.5. | § 6401(a): "the intestate share of the surviving spouse is the one-half of the community property that belongs to the decedent." https://california.public.law/codes/probate_code_section_6401 ; https://california.public.law/codes/probate_code_section_6402 | Reference only. Acceptable as a summary. |
| 42 | spec › Intestate shares | On Path B the institution relies on the affidavit's statement of who the successor is. | **Verified** (§ 13106(a)), subject to row 27. | URL above | None. |
| 43 | spec › Facts | Joint with survivorship is California's default (§ 5302(a)). | **Verified with correction.** Statute says the default is rebuttable. A "tenancy in common" account has no survivorship unless express (§ 5306). A spousal "community property" account is governed by community-property law (§ 5307). | § 5306 https://california.public.law/codes/probate_code_section_5306 ; § 5307: "governed by the law governing community property generally." https://california.public.law/codes/probate_code_section_5307 | Add account-type flags for "tenancy in common" and "community property account" (not determinable). |
| 44 | spec › Facts | A joint account without survivorship falls under § 5302(d). | **Verified.** | § 5302(d): "has no effect on beneficial ownership ... other than to transfer the rights of the decedent as part of the decedent's estate." (URL above) | None. |
| 45 | spec › Facts | `estate.declared_value` excludes § 13050 property. | **Verified with correction.** It must also exclude § 13151-petition property, and it is the **current** value (row 15). | §§ 13100, 13101(a)(5) | Amend the definition. |
| 46 | spec › Facts | `has_real_property_in_jurisdiction` (§ 13103). | **Verified.** | § 13103 | None. |
| 47 | spec › Facts | `ownership_instrument_issued` (§ 13102). | **Verified.** | § 13102(a) | None. |
| 48 | spec › Golden | GS-CA-001: earliest payment 2025-07-11; documents listed; protected. | **Verified with correction.** 2025-06-01 + 40 = 2025-07-11 (a Friday) under first-day-excluded counting. Whether day 40 itself is eligible is Q3. | CCP § 12 | Hold the date open until Q3 is decided. The § 13104(f) notation may need to be added. |
| 49 | spec › Golden | GS-CA-002 to 004: boundary values at $184,500 / $184,500.01 / $208,850 on 2025-03-31 and 2025-04-01. | **Verified.** | JC list; § 13101(g)(2) | None. |
| 50 | spec › Golden | GS-CA-005, 006: proceeding without consent is not determinable; with consent, add the consent and letters. | **Verified.** | § 13101(a)(4), (e); § 13108 | None. |
| 51 | spec › Golden | GS-CA-007: real property in the estate; eligible; add inventory and appraisal. | **Verified with correction.** The real property counts toward the limit unless it is in a § 13151 petition (for deaths from 2025-04-01, a primary residence up to $750,000). Section 13115 bars using the affidavit to obtain real property. | § 13103; § 13151(a) https://california.public.law/codes/probate_code_section_13151 ; JC list "§§ 13151, 13152, 13154 ... $750,000" | State in the facts that the declared value includes the real property. |
| 52 | spec › Golden | GS-CA-008: POD, two surviving payees, 1/2 each, payable on request, protected. | **Verified with correction.** Correct for adults. If a payee is a minor, § 5407(b) applies. **Reviewer inference:** after the death, the payees are "parties" (§ 5136(b)), so § 5401(a) may also allow payment to any one of them; equal shares is the safer output. | § 5302(b)(2)(B); § 5407(b) https://california.public.law/codes/probate_code_section_5407 | Add a minor-payee fact; if true, not determinable. |
| 53 | spec › Golden | GS-CA-009: joint, one survivor, 1/1, protected. | **Verified.** | §§ 5302(a), 5402, 5405(a) | None. |
| 54 | spec › Golden | GS-CA-010: POD payee is a former spouse, so not determinable. | **Verified with correction.** Add a joint-party former-spouse variant (row 12). | § 5040 | Add GS for a joint former spouse. |
| 55 | spec › Golden | GS-CA-011: restraining order served before payment, so not determinable. | **Verified with correction.** The scenario doesn't name the path. Section 5405(b) is a Path A rule; Path B needs its own rule (G4). | § 5405(b); Fin. Code § 1450(b) | Specify the path; add a Path B variant. |
| 56 | spec › Golden | GS-CA-012: died 2022-03-31, so not determinable. | **Verified** (owner decision). | — | None. |
| 57 | spec › Golden | GS-CA-013: died 2022-04-01, $184,500, eligible. | **Verified.** | § 13101(g)(2); JC list | None. |
| 58 | spec › Golden | GS-CA-014: Totten, sole trustee, two beneficiaries, 1/2 each; proof both survived. | **Verified.** | §§ 5302(c)(2)(B), 5404 | None. |
| 59 | spec › Golden | GS-CA-015: Totten terms 70/30. | **Verified.** The terms must "expressly provide". | § 5302(c)(2)(B) | None. |
| 60 | spec › Golden | GS-CA-016: joint, two survivors, `any_of`, protected. | **Verified.** | §§ 5401(a), 5402, 5405(a) | None. |
| 61 | open-questions › Q6 | The statute lets the institution pay any one or more surviving parties per the terms; protected. | **Verified.** Case law (*Placencia*) applies § 5405 to payment of a joint account to a survivor per the terms. | § 5401(a); § 5402 ("to any party without regard to whether any other party is ... deceased"); *Placencia* | Mark Q6 as answerable (see notes). |
| 62 | sources › JC list | Official JC list; SHA-256 `cb30e97d…edf56`. | **Verified.** The full hash of the copy I downloaded is `cb30e97d3b4322512bcd3a5cda8eff5eb3de26c66a0473d9a15295e076eedf56`. | JC URL above | Record the full hash. |
| 63 | sources › mirror dates | "Updated" dates: § 890 2020; § 13006 1991; § 13050 2020; § 13051 1991; §§ 13100–13101 2025; § 13100.5 2023; §§ 13102–13106 1990; § 13500 2017; § 13540 1995; § 5040 2017; § 5302 2016; § 5401 2013; §§ 5402–5405 1990; §§ 6401–6402 2015. | **Verified.** All match the mirror pages I fetched. | Mirror pages | Add §§ 13108–13117 (2023 transferee-liability amendments), § 13151 (2025, AB 2016) and the sections in the Gaps section. |
| 64 | WA spec › CA column | California limit is $208,850, "adjusted every 3 years". | **Verified with correction.** That amount applies only to deaths from 2025-04-01. | JC list | Say "$184,500 or $208,850 depending on date of death". |
| 65 | WA spec › CA column | Measures gross value of California property, with listed exclusions. | **Verified.** | §§ 13100, 13050 | None. |
| 66 | WA spec › CA column | Existing administration: allowed with the personal representative's written consent. | **Verified with correction.** Only a **California** proceeding is a bar. A proceeding elsewhere does not bar use (§ 13101(a)(4)(A)), and a sister-state personal representative can itself use the affidavit (§ 12570). | §§ 13101(a)(4), 12570 | Add "California proceedings only". |
| 67 | WA spec › CA column | Extra conditions: "None comparable." | **Verified.** I found no residency, debts-paid or notice-to-successors condition in §§ 13100–13101. Section 12570 shows nondomiciliary decedents qualify. | §§ 13100, 13101, 12570 | None. |
| 68 | WA spec › CA column | Joint accounts: "Survivorship presumed (§ 5302(a))". | **Verified with correction.** Rebuttable by clear and convincing evidence; § 5306 and § 5307 exceptions. | § 5302(a); §§ 5306, 5307 | Add "rebuttable". |
| 69 | WA spec › CA column | A will overriding a POD designation: "Not possible (§ 5302(e))". | **Verified with correction (misleading as stated).** Statute says a designation "cannot be changed by will" (§ 5302(e); see also § 5305(c)). Case law holds that a will may still be clear and convincing evidence of a different intent, so the estate can recover from the survivor, while the bank is protected paying per the terms. | § 5302(e): "cannot be changed by will." *Placencia*: "The court may still look to the will as an expression of intent to negate survivorship." | Reword: "A will cannot change the account terms, and the institution is protected paying per the terms. A will can be evidence redirecting beneficial ownership (*Placencia*)." |
| 70 | spec › Path A (implicit) | § 5302 rules govern whom the institution pays. | **Verified with correction.** Statute says ownership rules in Chapter 3 "have no bearing on the power of withdrawal"; Chapter 4 governs institution liability (§ 5201). | § 5201(a), (b) https://california.public.law/codes/probate_code_section_5201 | Cite §§ 5201 and 5401–5405 as the payment authority, and § 5302 only for default shares. |
| 71 | spec › Path B › Documents (implicit) | The statutory document list is complete. | **Verified with correction.** Section 13101(c) and § 13106.5 add recording requirements only for secured debts (not deposits). Section 13114 lets a public administrator or coroner who holds property refuse until costs are paid (not applicable to banks). Otherwise the list is complete. | § 13114 https://california.public.law/codes/probate_code_section_13114 | None for deposit accounts. |
| 72 | spec › Path B (implicit) | After a Path B payment, the matter is closed for the institution. | **Verified with correction.** Statute says a later administration is not precluded (§ 13108(b)). Liability then runs to the **transferee**, not the holder (§§ 13109, 13109.5, 13110, 13111). | § 13108(b): "does not preclude later proceedings for administration." § 13111(a): "the transferee is liable for ... restitution." https://california.public.law/codes/probate_code_section_13111 | Add an explanatory note in the decision output. |

(Rows 1–72 make up the counts in the Summary.)

---

## Gaps and omissions

| # | Gap | Authority | Label | Recommendation |
|---|---|---|---|---|
| G1 | **§ 13600 et seq. (spouse collecting compensation)** covers only salary or compensation owed **by an employer**, up to $18,450 (deaths 2022-04-01 to 2025-03-31) or $20,875 (from 2025-04-01). It does **not** apply to deposit accounts. | § 13600(a): "collect salary or other compensation owed by an employer for personal services of the deceased spouse." https://california.public.law/codes/probate_code_section_13600 ; JC list "§§ 13600, 13601 ... $18,450 $20,875" | Statute says | Note in Path C that § 13600 does not apply. |
| G2 | **§ 13650 spousal property petition.** A court order that property passes to the spouse, which can direct delivery, and becomes conclusive when final. | § 13656(a): "may issue any further orders which may be necessary to cause delivery of the property or its proceeds to the surviving spouse"; § 13657: "shall be conclusive on all persons." https://california.public.law/codes/probate_code_section_13656 , https://california.public.law/codes/probate_code_section_13657 | Statute says | Possible Path C route: pay per a certified final § 13656 order. No specific holder-discharge statute was located for this route, so attorney input is needed. |
| G3 | **Sister-state personal representatives** may use the affidavit and may recover attorney fees. | §§ 12570–12573 https://california.public.law/codes/probate_code_section_12572 : "may be awarded attorney's fees, as provided in subdivision (b) of Section 13105." | Statute says | Add an affiant capacity "sister-state PR" with letters. |
| G4 | **Adverse claims and court orders on Path B and for banks generally.** A fiduciary-misappropriation affidavit triggers a hold of up to 3 court days; a court order must be obeyed. CAMPAL does not limit this. | Fin. Code § 1450(a), (b), (d): "Nothing in the California Multiple-Party Accounts Law ... limits the applicability of this section." https://california.public.law/codes/financial_code_section_1450 ; § 6661 (savings associations) https://california.public.law/codes/financial_code_section_6661 ; *Mautner* | Statute says / Case law holds | Add facts for an adverse-claim affidavit, a court order, and notice of a superior claim, each giving not determinable. Attorney to confirm whether § 6661 is still operative and how it applies to federal savings associations. |
| G5 | **Credit unions:** multiple-party share accounts are governed by CAMPAL. | Fin. Code § 14854: "a credit union share account that is a multiple-party account ... is governed by Part 2 ... of the Probate Code." https://california.public.law/codes/financial_code_section_14854 | Statute says | Note that the spec applies to credit unions. I did not locate a credit-union counterpart to § 1450. |
| G6 | **Minor POD or Totten payees** must be paid under CUTMA or Prob. Code § 3400 et seq. | § 5407(b) (URL above) | Statute says | Minor-payee fact; result not determinable. |
| G7 | **Survival proof and simultaneous death.** A beneficiary who cannot be shown by clear and convincing evidence to have survived is deemed not to have survived. There is a 120-hour rule for intestate heirs (this affects § 13006 successors). Section 21109 applies to at-death transfers (POD/Totten), but § 21104 excludes joint accounts. | § 222(a); § 223; § 6403(a): "A person who fails to survive the decedent by 120 hours is deemed to have predeceased the decedent"; § 21109; § 21104. https://california.public.law/codes/probate_code_section_222 etc. | Statute says | When the deaths of a party and a payee are less than 120 hours apart, or the order of death is unknown, the result is not determinable. |
| G8 | **Slayer and elder abuse.** A killer loses Division 5 property, and joint accounts are severed. An institution paying per its terms is protected unless it received written notice before payment. Section 259 covers abusers. | § 250(a)(4); § 251: "applies to ... joint and multiple-party accounts in financial institutions"; § 256: "is not liable by reason of this part, unless prior to payment it has received at its home office or principal address written notice of a claim." https://california.public.law/codes/probate_code_section_256 ; § 259 | Statute says | Fact "written § 250–256 notice received", giving not determinable. |
| G9 | **Federal benefit reclamation.** The receiving bank is liable for federal benefit payments received after death. | 31 CFR 210.10(a): "An RDFI shall be liable to the Federal Government for the total amount of all benefit payments received after the death..." https://www.ecfr.gov/ (versioner API, part 210 § 210.10) | Statute (regulation) says | Policy or operational hold: exclude post-death federal benefit credits from the payable balance. Attorney to confirm the treatment. |
| G10 | **Escheat (unclaimed property).** A deceased owner's deposit can escheat after 3 years without owner activity. If a claimant proves entitlement before delivery to the Controller, the holder pays the claimant instead. After escheat, the holder may pay and seek reimbursement. | CCP § 1513(a)(1); § 1532(b): "the holder shall not pay or deliver the property to the Controller"; § 1560(b). https://california.public.law/codes/code_of_civil_procedure_section_1513 , …_1532, …_1560 | Statute says | Fact "account escheated or reported to Controller", giving not determinable (claim through the Controller). |
| G11 | **FTB orders to withhold and other levies.** The FTB may require a holder of a taxpayer's credits to withhold, and has special rules for depository institutions. Federal levies were not researched. | Rev. & Tax. Code § 18670(a) https://california.public.law/codes/revenue_and_taxation_code_section_18670 | Statute says. Application to a decedent's account is **Reviewer inference.** | Generalize the "restraining order" fact to "legal process served (court order, levy, order to withhold, garnishment)". |
| G12 | **Medi-Cal notice.** The beneficiary, personal representative, "or the person in possession of property of the decedent" must notify DHCS within 90 days if the decedent received Medi-Cal. Recovery is limited to the federally required probate estate, with no claim when there is a surviving spouse or RDP, or a minor or disabled child. | Prob. Code § 215 https://california.public.law/codes/probate_code_section_215 ; W&I § 14009.5(b), (f)(3) https://california.public.law/codes/welfare_and_institutions_code_section_14009.5 | Statute says. Whether a depository bank is a "person in possession" is **Reviewer inference, uncertain.** | Attorney to decide whether the institution has any § 215 duty. If not, consider an informational note to the affiant. Transferees remain liable for unsecured debts (§§ 13109, 13100.5(c)). |
| G13 | **Community-property nonprobate transfers.** A designation made without the spouse's written consent is ineffective as to the nonconsenting spouse's interest, but the holder remains protected. | § 5020; § 5012: "does not affect the obligation of a holder ... or the protection provided the holder by Section 5003"; § 5003(b)(2) (protection lost after service of a written adverse-claim notice). https://california.public.law/codes/probate_code_section_5003 | Statute says | No engine change for Path A, since § 5405 applies. Add an informational note. |
| G14 | **§ 5303 changes to account terms.** Protection presupposes a proper party (*Stevens*). | § 5303(b) https://california.public.law/codes/probate_code_section_5303 ; *Stevens* | Case law holds | Fact "party added or terms changed by a § 5303 method", or rely on the institution's records. |
| G15 | **Transferee-liability rules (2023 amendments)** explain the downstream risk. Note that § 13112 does not exist on the mirror ("Page not found"); the chapter runs §§ 13109–13111, 13113, 13113.5, 13117. | §§ 13109, 13109.5, 13110, 13110.5, 13111, 13113.5, 13117 (mirror, "updated Jan. 1, 2023") | Statute says | Cite §§ 13109–13111 for transferee liability; the holder is unaffected under § 13106. |
| G16 | **Financial Code provisions specific to deceased depositors.** Beyond §§ 1450, 1451, 6661 and 14854, I did not locate any Financial Code section governing payment of a deceased depositor's account. Federal preemption for national banks and federal savings associations was not researched. | — | Not located | Attorney to confirm. |

---

## Open questions: research notes

**Q2. Several affiants: how is payment split?**
- **Statute says** that if §§ 13100–13104 are satisfied, the affiants "are entitled to have the property ... paid ... to them" (§ 13105(a)(1)). The statements are "modified as appropriate" (§ 13101(b)). The successor is "all of the beneficiaries" (§ 13006).
- No statute or case I located specifies a split.
- **Reviewer inference:** The most literal compliant form is a single payment to all affiants jointly. A split follows the affidavit only if the affidavit states the shares.
- Requiring more than the statute may risk § 13105(b) fees if it is "unreasonable".
- **Can be answered now?** Partly. Recommend a "joint payment to all affiants" output, or shares only as stated in the affidavit. Attorney to confirm.

**Q3. Day counting for "40 days have elapsed".**
- **Statute says** (general rule): "The time in which any act provided by law is to be done is computed by excluding the first day, and including the last, unless the last day is a holiday, and then it is also excluded." (CCP § 12, https://california.public.law/codes/code_of_civil_procedure_section_12 ; identical text in Civ. Code § 10 and Gov. Code § 6800.) Gov. Code § 6806 says "A day is the period of time between any midnight and the midnight following."
- CCP § 12a extends a period whose **last day for performance** is a holiday. A 40-day waiting period is not a deadline for performing an act, so whether § 12a applies is uncertain (**Reviewer inference**). Extending it would only make the earliest date later, which is conservative.
- **Case law:** I located no California decision construing "40 days have elapsed" in § 13100 or § 13540. The CourtListener search was cut short by rate limits, and Westlaw was not available. A Supreme Court decision on CCP § 12 and tolling (*Shalabi v. City of Fontana*) is believed to exist but was not read.
- **Analysis:**
  - Under § 12, day 1 is the day after death and day 40 is death + 40 (e.g. 2025-06-01 gives 2025-07-11).
  - "Have elapsed" plausibly means that day 40 has ended, which points to death + 41 (2025-07-12). It may instead mean the act can be done on day 40.
  - The 40-day statement is made in the affidavit (§ 13101(a)(3)), so the affidavit's execution date also matters.
- **Can be answered now?** No. Recommend the default **death date + 41**, and the rule "the affidavit is executed on or after that date", until the attorney decides. Either way, GS-CA-001 should show the chosen date.

**Q5. Surviving spouse or RDP collecting a deposit account without the affidavit.**
- **Statute says:**
  - § 13500: property passing to the spouse needs no administration, subject to §§ 13540 and 13550.
  - § 13540: covers real property only (after 40 days).
  - § 13545: covers securities registered in the surviving spouse's name.
  - § 13600: covers employer compensation only.
  - § 13650: lets the spouse petition for an order that property passes to the spouse; under § 13656 the court may order delivery, and under § 13657 a final order is conclusive.
  - § 37(b) and § 78 define surviving domestic partner and surviving spouse.
- I located no statute giving a holder discharge for paying a spouse based on an affidavit of spousal status for a sole-name deposit account.
- Section 13050(a)(1) excludes property passing to the spouse under § 13500 from the small-estate value, so a spouse can often use the § 13100 affidavit as successor.
- Liability of the spouse: §§ 13550–13554 (debts) and §§ 13561–13563 (superior testate claimants).
- **Secondary:** not consulted.
- **Can be answered now?** Mostly. Path C should remain not determinable for spousal status alone. Add an optional route: "certified final § 13656 order directing delivery to the spouse; pay per the order". The attorney should confirm what protection applies when paying under that order.

**Q6. Joint, two or more survivors: `any_of`.**
- **Statute says:** § 5401(a), "may be paid ... to any one or more of the parties"; § 5402, "to any party without regard to whether any other party is incapacitated or deceased"; § 5405(a) gives protection.
- **Case law holds** (*Placencia*) that payment per the terms to a survivor is proper; beneficial disputes are between the parties (§ 5405(d)).
- **Can be answered now?** Yes. The reading is supported. Caveats: § 5401(b) multi-signature terms, the § 5405(c) notice, and § 5303 proper-party status.

**Q8. Verification beyond the statutory documents.**
- **Statute says** the holder may require a bond if evidence of ownership is missing (§ 13102(b)). It "shall award reasonable attorney's fees" if the holder "acted unreasonably in refusing to pay" (§ 13105(b)).
- **Case law:** Besides dictum in a *Mautner* footnote, I located no published decision applying § 13105(b) fees against a holder. *Mautner* says: "The successor will be entitled to attorney fees only if the court finds the holder acted unreasonably."
- **Reviewer inference:** Reasonable verification is likely defensible, for example:
  - letters for a personal representative's consent, which § 13101(e) already requires;
  - proof of appointment for guardians or conservators, by analogy to § 13601(d);
  - a copy of the power of attorney.

  Blanket extra requirements or delays risk fee exposure.
- **Can be answered now?** It needs an attorney. Reclassify Q8 as "Policy (Law to confirm)". ARCHITECTURE.md's statement that policy "can only make decisions stricter" should note this Path B fee risk.

**Q9. Confirm citations on leginfo.** I could not do this: leginfo returned 403 on 2026-10-09, and all text came from the mirror. The attorney must confirm every section cited here, especially those amended recently: §§ 13100, 13101 and 13151 (2025, AB 2016); §§ 13109–13117 (2023); § 9202 (2026); CCP § 1520 (2026).

### Case law requested in task item 2

| Topic | Located and read | Holding (short quote) | Notes |
|---|---|---|---|
| § 13106 reliance and discharge | *Mautner v. Peralta* (1989) 215 Cal.App.3d 796 (1st Dist.) (construes former §§ 630–631, the predecessors of §§ 13100–13106) | The immunity is "inapplicable where the holder has actual notice of a statutory heir's superior claim and a request to 'hold' distribution ... prior to receiving a '630' affidavit." | The predecessor statute lacked "good faith" wording; § 13106(a) now has it. Its application to § 13106 is **Reviewer inference.** |
| §§ 13109–13112 transferee liability | None located. CourtListener searches for "section 13109" returned only an unrelated 1962 case; "section 13111" was cut off by the rate limit. | — | § 13112 does not exist. |
| § 13105(b) refusal and fees | No holding located; only *Mautner* footnote dictum (above) | — | Believed sparse. Search Westlaw. |
| § 5302 clear and convincing evidence | *Placencia v. Strazicich* (2019) 42 Cal.App.5th 730 (4th Dist., Div. 3; No. G055631; filed 11/26/19; a 12/23/19 modification exists and was not read). Citation per vLex (secondary); slip opinion read. *Araiza v. Younkin* (2010) 188 Cal.App.4th 1120 (2d Dist., Div. 6). | *Placencia*: a will may evidence intent; the bank is protected. *Araiza*: a living trust overrode a Totten designation by clear and convincing evidence. | *Estate of O'Connor* (2017) 16 Cal.App.5th 159 (joint account; no clear and convincing evidence shown, so the account went to the survivor). Believed to exist per secondary sources; **not read**. *Lee v. Yang* (2003) 111 Cal.App.4th 481 (1st Dist.): read in part; concerns lifetime withdrawals and §§ 5301, 5405. |
| § 5405 institution protection | *Stevens v. Tri Counties Bank* (2009) 177 Cal.App.4th 236 (3d Dist.); *Placencia* | *Stevens*: protection "presupposes the person is a proper party"; the bank is liable for adding a party in violation of § 5303. | — |

---

## Edge cases and risks

| # | Fact pattern | Severity | Likelihood | Authority |
|---|---|---|---|---|
| E1 | Bank receives a letter from a would-be heir claiming the account and asking for a hold, then a § 13101 affidavit from someone else. | High | Medium | *Mautner*; § 13106(a) "good faith"; Fin. Code § 1450 |
| E2 | Engine sets the earliest date at death + 40 and the affidavit is signed that same day. A court later reads "elapsed" as requiring day 40 to be complete. | Medium | Medium | CCP § 12; § 13101(a)(3). Reviewer inference |
| E3 | Joint account with a survivor; the decedent's will says the survivor should not take. | Low for the bank (protected); High for misleading output | Medium | *Placencia*; § 5405(a), (d) |
| E4 | Surviving joint owner is the decedent's ex-spouse (divorced after the account was opened). | High | Medium | §§ 5302 ("Subject to Section 5040"), 5040 |
| E5 | POD payee is 15 years old. | High | Medium | § 5407(b) |
| E6 | Owner and POD payee die in the same accident, order unknown. | Medium | Low | §§ 220, 222, 21109 |
| E7 | Surviving joint owner is charged with the decedent's murder; the bank later gets written notice. | High | Low | §§ 251, 256 |
| E8 | Single affiant signs as "successor" but the will leaves the account to three children. | High | Medium | § 13006 ("all of the beneficiaries"); § 13101(a)(9); transferee liability § 13110 |
| E9 | Account balance includes Social Security deposited after death. | Medium | High | 31 CFR 210.10 |
| E10 | Dormant deceased-owner account already reported to the Controller. | Medium | Medium | CCP §§ 1532(b), 1560(b) |
| E11 | Institution policy adds 30 extra days or a notarization requirement; the affiant sues under § 13105(b). | Medium | Medium | § 13105(b); § 12572 |
| E12 | Nonresident decedent; Oregon personal representative presents a § 13101 affidavit. | Medium | Medium | §§ 12570–12573; *Smith v. Cimmet* (2011) 199 Cal.App.4th 1381 (read in part; describes the small-estate exception for foreign representatives) |
| E13 | Value of California property was under the limit at death but over it at affidavit date, or the reverse. | Medium | Low | § 13101(a)(5) "current". Reviewer inference |
| E14 | Account titled "A in trust for B" but is actually a formal trust account. | Medium | Low | § 80; § 5406 (pay as Totten absent written notice) |
| E15 | Spouses' joint account expressly titled "community property". | Medium | Low | § 5307 |
| E16 | FTB order to withhold or IRS levy received after death. | Medium | Low | Rev. & Tax. Code § 18670. Federal levy not researched |
| E17 | Decedent received Medi-Cal at age 55 or older; no surviving spouse. | Low (institution) | Medium | Prob. Code § 215; W&I § 14009.5. Reviewer inference on the bank's role |

---

## Sources consulted

All were accessed 2026-10-09.

**Primary sources:**

- **California code (mirror):** Probate, Code of Civil Procedure, Civil, Government, Financial, Revenue and Taxation, and Welfare and Institutions Code sections, read at `https://california.public.law/codes/<code>_section_<n>`.
  - **Prob. Code:** 37, 78, 80, 100, 215, 220, 221, 222, 223, 250, 251, 252, 254, 255, 256, 257, 259, 890, 5000, 5002, 5003, 5010, 5011, 5012, 5013, 5020, 5021, 5022, 5023, 5030, 5031, 5032, 5040, 5042, 5044, 5048, 5100, 5122, 5124, 5126, 5128, 5130, 5132, 5134, 5136, 5139, 5140, 5142, 5144, 5146, 5148, 5150, 5152, 5201, 5205, 5301, 5302, 5303, 5304, 5305, 5306, 5307, 5401, 5402, 5403, 5404, 5405, 5406, 5407, 5600, 5602, 5604, 6401, 6402, 6403, 9202, 12570, 12571, 12572, 12573, 13006, 13050, 13051, 13100, 13100.5, 13101, 13102, 13103, 13104, 13105, 13106, 13106.5, 13107, 13107.5, 13108, 13109, 13109.5, 13110, 13110.5, 13111, 13113, 13113.5, 13114, 13115, 13116, 13117, 13151, 13152, 13500, 13501, 13502, 13503, 13540, 13541, 13542, 13545, 13550, 13551, 13552, 13553, 13554, 13560, 13561, 13562, 13563, 13600, 13601, 13602, 13603, 13604, 13605, 13606, 13650, 13651, 13655, 13656, 13657, 13658, 13659, 13660, 21104, 21109.
  - **CCP:** 12, 12a, 12b, 12c, 1300, 1415, 1513, 1513.5, 1516, 1520, 1530, 1532, 1560.
  - **Civ. Code:** 7, 10, 11.
  - **Gov. Code:** 6800, 6803, 6804, 6806, 6807.
  - **Fin. Code:** 1450, 1451, 1452, 6661, 14854, 14855, 14860, 14861, 14863, 14865, 14866, 14867.
  - **Rev. & Tax. Code:** 18670.
  - **W&I Code:** 14009.5.
  - **Pages not found on the mirror:** Prob. Code §§ 13112, 5101–5105, 5129, 5149, 5156, 5160, 13543, 13544, 5601, 5603; Fin. Code §§ 852, 853, 854, 14862, 14864.
- **Judicial Council:** "Maximum Amounts for Determining Eligibility for Summary Succession Procedures", https://courts.ca.gov/system/files/file/probate-code-890-adjusted-amounts.pdf (SHA-256 `cb30e97d3b4322512bcd3a5cda8eff5eb3de26c66a0473d9a15295e076eedf56`).
- **eCFR:** 31 CFR 210.10, via `https://www.ecfr.gov/api/versioner/v1/full/2026-09-01/title-31.xml?part=210&section=210.10`.
- **Cases (full text):**
  - *Placencia v. Strazicich*, slip opinion G055631 (filed 11/26/19), https://cases.justia.com/california/court-of-appeal/2019-g055631.pdf
  - *Stevens v. Tri Counties Bank* (2009) 177 Cal.App.4th 236, https://static.case.law/cal-app-4th/177/cases/0236-01.json
  - *Araiza v. Younkin* (2010) 188 Cal.App.4th 1120, https://static.case.law/cal-app-4th/188/cases/1120-01.json
  - *Mautner v. Peralta* (1989) 215 Cal.App.3d 796, https://static.case.law/cal-app-3d/215/cases/0796-01.json
  - *Lee v. Yang* (2003) 111 Cal.App.4th 481, https://static.case.law/cal-app-4th/111/cases/0481-01.json
  - *Smith v. Cimmet* (2011) 199 Cal.App.4th 1381, https://static.case.law/cal-app-4th/199/cases/1381-01.json
  - *Evangelho v. Presoto* (1998) 67 Cal.App.4th 615, https://static.case.law/cal-app-4th/67/cases/0615-01.json (not relied on)
  - *Reich v. Reich*, slip opinion B332714 (2024), https://cases.justia.com/california/court-of-appeal/2024-b332714.pdf (omitted-spouse and IRA case; not relied on)
- **Case search:** CourtListener search API, https://www.courtlistener.com/api/rest/v4/search/ (case discovery only; rate-limited).

**Secondary sources (used only to locate citations):**

- vLex listing for the *Placencia* reporter citation: https://case-law.vlex.com/vid/placencia-v-strazicich-g055631-889690038
- Web search result summaries about *Estate of O'Connor* (not read).

**Attempted and not available:** leginfo.legislature.ca.gov (HTTP 403); law.justia.com (HTTP 403 via WebFetch); CourtListener opinion pages (bot challenge) and cluster API (authentication required).

---

## Items the attorney must confirm

1. Every statute quoted above, against leginfo (Q9). Priority: §§ 13100, 13101, 13151 (AB 2016), 5302, 5405, 5040, 13105, 13106.
2. *Placencia v. Strazicich* reporter citation (42 Cal.App.5th 730), the effect of the 12/23/19 modification, and later history. *Araiza*, *Stevens* and *Mautner*: citator check.
3. Q3: whether the earliest Path B date is death + 40 or death + 41, and whether CCP § 12a applies to the 40-day wait.
4. Whether *Mautner* applies to § 13106 good-faith reliance. What notice should make Path B not determinable.
5. § 13105(b) fee exposure for policy-imposed extra requirements or delays (Q8), and the related ARCHITECTURE.md "stricter-only" policy model.
6. Q2: the correct payment form for multiple affiants.
7. Q5: whether to add a § 13656 court-order route for spouses, and what protection applies.
8. Applying § 5040 to joint-account survivorship with a former spouse, and whether the institution is protected under § 5405 if it pays anyway.
9. Whether the institution has any Medi-Cal notice duty under Prob. Code § 215 as a "person in possession of property of the decedent".
10. Whether Fin. Code § 6661 is still operative. Federal preemption for national banks and federal savings associations. Treatment of federal levies (not researched).
11. Handling of minor payees (§ 5407), survival proof (§§ 220–223, 6403, 21109), slayer notice (§ 256), escheated accounts (CCP §§ 1532, 1560), and Treasury reclamation (31 CFR 210.10).
12. Rewording of the § 13106.5 not-determinable item, and of the Washington spec's California entry on will overrides (§ 5302(e)).
