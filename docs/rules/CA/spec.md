# California rule spec (DRAFT, not attorney-reviewed)

**Status:** Draft v0.2, updated 2026-10-09 for REQ-CA-001. **Attorney review:** not started.
Nothing here is encoded in the engine until an attorney approves it. Statute text was read from a mirror of the official code (see [sources](sources.md)), and every citation must be confirmed against leginfo.legislature.ca.gov before approval. Numbered questions (Q1, Q2, …) are in [open-questions.md](open-questions.md). Supporting research, with quotes and sources for each point, is in [legal-review.md](legal-review.md). References like "R27" or "G4" point to its claim-audit rows and gaps; "Risk R2" points to the cross-cutting risk review (`docs/rules/legal-risk-review.md`).

## Changes since v0.1

v0.2 applies the findings of the legal research review (2026-10-09). Findings that need a legal judgment were added to the open questions instead of being decided here.

| Change | Basis |
|---|---|
| **Path A now says the institution may pay**, not that funds "belong to" the payee. Ownership is rebuttable by clear and convincing evidence, and a will or living trust can be that evidence, but the institution stays protected when it pays according to the account terms. | §§ 5201, 5302(a), (c)(2), 5405(a); *Placencia v. Strazicich* (2019); *Araiza v. Younkin* (2010); review R1, R3, R69, R70 |
| **Protection presupposes a proper party.** The payee's status must come from account terms validly set or changed under § 5303. | § 5405; *Stevens v. Tri Counties Bank* (2009); R10, G14 |
| **Former-spouse rule widened to joint accounts.** § 5302 is "subject to Section 5040". | §§ 5040, 5302; R12 |
| **Removed an incorrect not-determinable item.** § 13106.5 governs debts owed *to* the decedent that are secured by real property, not deposit accounts. | § 13106.5(a); R36 |
| **Added a good-faith limit on Path B protection.** Notice of a superior claim plus a hold request before the affidavit removes protection (under the predecessor statute). Adverse claims and court orders are added. | § 13106(a); *Mautner v. Peralta* (1989); Fin. Code § 1450; R27, G4 |
| **Earliest Path B payment date is now an open question** with a conservative default of death + 41 days. | CCP § 12; R34, Q3 |
| **The value test is the "current" gross fair market value**, compared with the limit for the date of death. A missing § 13050 exclusion (a life or other interest ending at death) is added. | § 13101(a)(5); § 13050(a)(1); R15, R45 |
| **One affiant receives 100% only if that affiant is the sole successor**, or represents all successors. | § 13006; § 13101(a)(9); R28 |
| **Documents:** items 2–4 must be attached to the affidavit; the bond is the institution's option; and the holder must note how identity was established. | § 13101(d)–(f); § 13102(b); § 13104(f); R30, R31, R33 |
| **Added rules the review found missing:** minor payees, survival proof and simultaneous death, slayer notice, sister-state personal representatives, and Path C court orders. Also new facts needed for federal and state holds (Treasury reclamation, escheat, tax withholding). | §§ 5407(b), 220–223, 6403, 21109, 250–256, 12570–12573, 13650–13657; 31 CFR § 210.10; CCP §§ 1532, 1560; Rev. & Tax. Code § 18670; G1–G12 |
| **Institution policy can carry fee risk:** "stricter than the statute" is not risk-free on Path B. | § 13105(b); § 12572; Q8; Risk R3 |

## Where each answer comes from

- **Law:** statutory conditions and protections. These are fixed by the code and confirmed by an attorney.
- **Account terms:** facts about the specific account, such as POD or Totten beneficiary shares, survivorship, and signature requirements. They arrive with the account facts.
- **Institution policy:** choices the statute leaves to the institution, such as an extra waiting period, extra documents, or declining some cases. A policy may be stricter than the statute but never looser, and every decision records which policy version it used. **On Path B, an unreasonable refusal or delay can expose the institution to attorney's fees (§ 13105(b)), so the limits of policy are an attorney question (Q8).**

## What the engine decides

For one deposit account of a California decedent, the engine answers four questions:

1. Who may the institution pay, and in what shares?
2. What documents must the institution receive first?
3. What is the earliest date it may pay?
4. Does a statute protect the institution from liability if it pays as decided?

If the facts fall outside the paths below, the result is **not determinable** and the case goes to a person. The engine never guesses.

**What a decision does not check:** the engine relies on the facts entered. Statutory protection applies only if the documents actually received match those facts and meet the statute (Risk R23). Every decision will list the institution's pre-payment checks it does not perform, such as sanctions screening, levies and Treasury reclamation (Risk R2, R8, R11).

## Path A: accounts with a survivor or payable-on-death (POD) payee

Applies when the account is a joint account with a surviving party, a POD account with a surviving POD payee, or a Totten trust account with a surviving beneficiary.

**Payment versus ownership.** Chapter 4 (§§ 5401–5405) governs whom the institution may pay. Chapter 3's ownership rules "have no bearing on the power of withdrawal" (§ 5201). Ownership under § 5302 can be rebutted by clear and convincing evidence of a different intent, and a will (*Placencia*) or a living trust (*Araiza*) can supply that evidence. The institution is still protected when it pays according to the account terms (§ 5405(a), (d)); any dispute over ownership is between the claimants.

| Question | Rule | Citation |
|---|---|---|
| Who may be paid | **Joint account:** the surviving party or parties, according to the account terms. **POD account, sole or last surviving party deceased:** the surviving POD payee(s); if a payee died before the party, the surviving payees take. **Totten trust account, sole or last surviving trustee deceased:** the surviving beneficiary or beneficiaries. An account "in trust for" another is paid as a Totten account unless the institution has written notice otherwise. | §§ 5401–5404; § 5302(a), (b)(2)(A), (c)(2)(A); § 5406 |
| Shares | **POD and Totten:** two or more surviving payees or beneficiaries take **equal shares** unless the account terms **expressly** provide otherwise. After the death there is no survivorship among them unless the terms say so. **Joint, two or more survivors:** the institution may pay any one or more surviving parties according to the account terms. It does not have to work out net contributions, and it is protected whether or not the payment matches beneficial ownership. | § 5302(b)(2)(B)–(C), (c)(2)(B)–(C); §§ 5401(a), (c), 5402, 5405(a) |
| Documents | Proof of death: a certified copy of the death certificate or another prima facie record. **POD:** proof that the payee survived every original party. **Totten:** proof that the beneficiary survived every trustee. **Joint:** the claimant must be a surviving party; payment to a deceased party's representative or heirs needs proof that the decedent was the last surviving party. | §§ 5144, 5402, 5403, 5404 |
| Earliest payment | On request, once proof of death is presented. No statutory waiting period applies. An institution policy may add one. | §§ 5402–5404 |
| Liability protection | **Yes.** Payment under §§ 5401–5404 discharges the institution from all claims for the amounts paid, even if inconsistent with beneficial ownership. This presupposes the payee is a proper party under validly set terms (*Stevens*; § 5303). "No other notice or any other information" affects protection, **except** a court order restraining payment that is served before payment. | § 5405(a), (b); § 5303 |

**Not determinable on this path:**
- **Former spouse.** A POD payee, Totten beneficiary, **or surviving joint party** is a former spouse or former registered domestic partner whose marriage or partnership ended before the death. The designation may fail under § 5040 (pre-2002 dissolutions follow § 5048(c)).
- **Minor payee.** A payee or beneficiary is a minor. Payment must be made under CUTMA or §§ 3400 et seq. (§ 5407(b)), and that payment form is not yet encoded.
- **Survival not shown.** Survival of a payee over the decedent is not shown by clear and convincing evidence: deaths close together, or the order of death unknown (§§ 220–223; § 21109 for at-death transfers; Q10).
- **Slayer notice.** Written notice of a § 250–256 slayer claim was received at the home office or principal address before payment (§ 256). How this interacts with § 5405(b) is Q11.
- **No payee survived.** No POD payee or Totten beneficiary survived the last party. The account then passes through the estate, so Path B or probate applies.
- **Signatures or notice.** The terms require more than one survivor's signature (§ 5401(b)), or the institution holds a written § 5405(c) notice. § 5405(c) does not apply to checking and similar accounts; that refinement is deferred.
- **Restraining order.** The institution has been served with a court order restraining payment (§ 5405(b)).
- **Account type.** The account is titled as a "tenancy in common" account (no survivorship unless express, § 5306) or as a spousal "community property" account (§ 5307).

## Path B: small-estate affidavit (accounts with no survivor or POD payee)

Applies to an account owned solely by the decedent with no POD payee, and to funds that pass to the estate because no payee survived.

### Eligibility (all required)

| Condition | Citation |
|---|---|
| The **current** gross fair market value of the decedent's real and personal property in California does not exceed the limit for the date of death (table below), as stated in the affidavit. **Excluded:** § 13050 property (joint-tenancy property; property in which the decedent had a life or other interest ending at death; multiple-party accounts passing to a survivor or payee; property passing to a surviving spouse under § 13500; revocable-trust property; vehicles registered or titled under the Vehicle Code; vessels; manufactured homes, mobilehomes, commercial coaches, truck campers and floating homes) and property in a § 13151 petition. **Also excluded:** Armed Forces pay, and wages owed up to the § 13050(c) adjusted amount ($18,450 for deaths 2022-04-01 to 2025-03-31; $20,875 from 2025-04-01). | §§ 13100, 13101(a)(5), 13050; Judicial Council § 890 list |
| At least 40 days have elapsed since the death. See "Earliest payment" and Q3. | §§ 13100, 13101(a)(3) |
| No proceeding to administer the estate is being or has been conducted **in California**, or the personal representative has consented in writing. A proceeding in another state does not bar this path. | §§ 13101(a)(4), 13108(a) |

**Value limit by date of death.** The limit is set under § 890 and published by the Judicial Council. "Does not exceed" means a value equal to the limit is eligible.

| Date of death | Limit | Citation |
|---|---|---|
| Before April 1, 2022 | $166,250 | § 13101(g)(1); Judicial Council § 890 list |
| April 1, 2022 – March 31, 2025 | $184,500 | § 13101(g)(2); § 890; Judicial Council § 890 list |
| On or after April 1, 2025 | $208,850 | § 13101(g)(2); § 890; Judicial Council § 890 list |

The next adjustment is scheduled for April 1, 2028, "unless otherwise provided by statute". An adjustment never applies to a death before its effective date (§ 890(d)). **Coverage begins with deaths on April 1, 2022** (owner decision, 2026-10-07). Earlier deaths are not determinable.

### Decision

| Question | Rule | Citation |
|---|---|---|
| Who is paid | The person(s) who sign the affidavit or declaration as **successor of the decedent**, or as someone authorized to act for the successor. That means a § 13051 representative (guardian, conservator, trustee, custodian, sister-state personal representative, or attorney-in-fact) or a sister-state personal representative using the affidavit under § 12570. "Successor" means the sole beneficiary **or all** of the beneficiaries who take the item under the will, or the heirs by intestacy (or under another state's law where it governs). The institution may rely **in good faith** on the affidavit and has no duty to check its statements. | §§ 13006, 13051, 12570, 13101(a)(7)–(9), 13105(a), 13106(a) |
| Shares | **One affiant:** 100%, **only if** the affiant is the sole successor to this item, or represents all successors. Otherwise not determinable. **Several affiants:** they are together entitled (§ 13105(a)(1)), and the affidavit is "modified as appropriate" (§ 13101(b)). The proposed default is a single payment to all affiants jointly, or shares only as the affidavit states them (Q2). | §§ 13006, 13101(a)(9), (b), 13105(a)(1) |
| Documents | 1. An affidavit or declaration under penalty of perjury containing every § 13101(a) statement. If signed outside California, it must recite that it is made under the laws of California (CCP § 2015.5). 2. A certified copy of the death certificate, **attached**. 3. For deaths on or after April 1, 2022, the Judicial Council's list of adjusted amounts in effect on the date of death, **attached**. 4. If a personal representative consented: copies of the consent and the letters, **attached**. 5. If the decedent held evidence of ownership the institution could have required: that evidence "if available". If it is not presented, the institution **may** require a bond or agree to an indemnity (institution option). 6. If the estate includes California real property: an inventory and appraisal by a probate referee. 7. Reasonable proof of each affiant's identity. **Institution duty:** unless the affidavit is notarized, note on it how identity was established. | § 13101(a), (d)–(f); §§ 13102, 13103, 13104(f); CCP § 2015.5 |
| Earliest payment | The day on which 40 days have elapsed since death. **Proposed conservative default: death date + 41 days**, until the attorney decides whether day 40 itself qualifies (Q3). The affidavit should be signed on or after that date, because it states that 40 days have elapsed. An institution policy may add days, subject to § 13105(b). | §§ 13100, 13101(a)(3); CCP § 12 |
| Liability protection | **Yes**, if §§ 13100–13104 are satisfied and the institution relies **in good faith**. Receiving the affidavit discharges the institution from further liability for the money paid, and it is not liable for **state** taxes because of the payment. A later administration is not barred; liability then runs to the people paid (the transferees), not to the institution. | § 13106(a), (b); § 13108(b); §§ 13109–13111 |

**Not determinable on this path:**
- The estate value exceeds the limit, or no value was declared.
- A California administration proceeding exists without the personal representative's written consent.
- A single affiant is not shown to be the sole successor, or to represent all successors.
- **Notice of a competing claim.** Before payment, the institution received notice of an adverse or superior claim, a request to hold, an adverse-claim affidavit, or a court order (*Mautner*; Fin. Code § 1450 for banks, § 6661 for savings associations).
- **Legal process.** A levy, order to withhold (Rev. & Tax. Code § 18670), garnishment, or restraining order has been served.
- **Escheat.** The account has been reported or delivered to the State Controller as unclaimed property. The claim then goes through the Controller (CCP §§ 1532, 1560).
- **Not a deposit account.** The item is a debt owed **to** the decedent and secured by real property (§ 13106.5). That is out of scope; deposit accounts are not affected.

## Path C: surviving spouse or registered domestic partner

Property passing to a surviving spouse under § 13500 needs no administration, subject to §§ 13540 and 13550 and the exceptions in §§ 13501–13502. But **no statute located lets a spouse collect a deposit account in the decedent's sole name on spousal status alone, with protection for the institution:**

- § 13540 covers real property only.
- § 13545 covers securities registered in the surviving spouse's name.
- § 13600 covers wages owed by an employer, not accounts.

The routes for a spouse are:

1. **Path A:** the spouse is a POD payee or surviving joint party.
2. **Path B:** the spouse signs the affidavit as successor. Property passing to the spouse under § 13500 is excluded from the value, under § 13050(a)(1).
3. **A court order under § 13650.** A certified final order under § 13656 can direct delivery to the spouse, and under § 13657 it is conclusive. Whether to add this route, and what protection applies, is Q5.

A claim that relies only on spousal status remains **not determinable**.

## Intestate shares (reference only)

Sections 6401 and 6402 set intestate shares:
- the surviving spouse takes the decedent's half of the community and quasi-community property;
- the separate property is split between the spouse and the issue, parents, siblings, or more remote kin, according to who survives.

On Path B the institution relies in good faith on the affidavit's statement of who the successor is (§ 13106(a)), so v1 does **not** compute intestate shares (Q4).

## Facts the engine will need

**In the schema today** (REQ-CORE-004 to 006):
- account type and holders with survivorship and terms shares;
- multiple-signature terms;
- notices: restraining order, withdrawal, dispute, testamentary disposition;
- former-spouse and former-partner relationships;
- `estate.declared_value`, `estate.has_real_property_in_jurisdiction`, `estate.administration`, `estate.affiants`;
- `account.ownership_instrument_issued`.

**Changes the research calls for** (schema changes need owner approval):

- **Value definition.** `estate.declared_value` must be defined as the **current** gross fair market value stated in the affidavit, excluding § 13050 and § 13151-petition property, **including** any California real property counted toward the limit.
- **Successors:**
  - whether the affiant or affiants are **all** the successors to this item;
  - an affiant capacity for a **sister-state personal representative** (§ 12570).
- **Payees:**
  - a **minor** payee or beneficiary (§ 5407(b));
  - **survival evidence:** each payee's date and time of death, or "living" (§§ 220–223, 21109);
  - a payee who survived but has since died (Risk R32).
- **Notices and holds:**
  - a **slayer notice** received (§ 256);
  - **notice of a competing claim or hold request** (*Mautner*);
  - an **adverse-claim affidavit** (Fin. Code § 1450);
  - **legal process** served: a levy, an order to withhold, a garnishment.
- **Account terms:**
  - an account titled **tenancy in common** or **community property** (§§ 5306, 5307);
  - payee status validly set under **§ 5303**.
- **Overlays:**
  - **escheat** status (CCP §§ 1532, 1560);
  - **post-death federal benefit credits** and a **reclamation notice** (31 CFR § 210.10; Risk R2).
- **Jurisdiction.** Separate the decedent's **domicile**, the **account office state**, and the deposit agreement's **governing-law state** (Risk R1).

**Institution policy, not facts** (REQ-POLICY-001): extra waiting days, extra documents, and declined account types or balances, subject to the § 13105(b) fee risk (Q8).

## Draft golden scenarios

These become `golden/ca.yaml` after attorney review. Path B dates use the conservative Q3 default (death + 41 days) and an institution policy that adds nothing.

| ID | Facts | Expected |
|---|---|---|
| GS-CA-001 | Sole account; died 2025-06-01; CA estate $150,000.00; no proceeding; one affiant, who is the sole successor | Pay affiant 1/1. Documents: affidavit, death certificate (attached), 2025 § 890 list (attached), proof of identity, and the institution's identity notation. Earliest payment **2025-07-12** (death + 41; 2025-07-11 if the attorney decides day 40 qualifies, Q3). Protected (§ 13106). |
| GS-CA-002 | As 001, but died 2025-03-31 with estate $184,500.00 | Eligible: equal to the limit for that date. |
| GS-CA-003 | As 001, but died 2025-03-31 with estate $184,500.01 | Not determinable: over the limit. |
| GS-CA-004 | As 001, but died 2025-04-01 with estate $208,850.00 | Eligible: the new limit applies from 2025-04-01. |
| GS-CA-005 | As 001, but a California administration proceeding exists with no PR consent | Not determinable. |
| GS-CA-006 | As 005, but the PR consented in writing | Eligible. Documents add the consent and the letters (attached). |
| GS-CA-007 | As 001, but the estate includes CA real property, counted in the declared value | Eligible. Documents add an inventory and appraisal. |
| GS-CA-008 | POD account; two adult surviving POD payees; no share terms | Pay each 1/2. Document: proof of death. Payable on request. Protected (§ 5405). |
| GS-CA-009 | Joint with survivorship; one surviving party | Payable to the survivor (§§ 5401(a), 5402). Protected (§ 5405). |
| GS-CA-010 | POD payee is the decedent's former spouse | Not determinable (§ 5040). |
| GS-CA-011 | Path A account; a restraining order was served before payment | Not determinable: no § 5405 protection. |
| GS-CA-012 | Died 2022-03-31 | Not determinable: before coverage starts (deaths from 2022-04-01). |
| GS-CA-013 | As 001, but died 2022-04-01 with estate $184,500.00 | Eligible: first day of coverage, at the 2022 limit. |
| GS-CA-014 | Totten trust; the trustee was the sole trustee; two surviving adult beneficiaries; no share terms | Pay each 1/2. Document: proof of death showing both beneficiaries survived the trustee. Payable on request. Protected (§ 5405). |
| GS-CA-015 | Totten trust; account terms expressly give beneficiaries 70% / 30% | Pay 7/10 and 3/10 per the account terms (§ 5302(c)(2)(B)). |
| GS-CA-016 | Joint with survivorship; two surviving parties | Payable to any of the survivors per the account terms (§§ 5401(a), 5402). Protected (§ 5405). Uses the `any_of` payment form. |
| GS-CA-017 | POD account; two designated payees; one died before the decedent | Pay the surviving payee 1/1 (§ 5302(b)(2)(A)). |
| GS-CA-018 | Joint with survivorship; the surviving party is the decedent's former spouse (divorced after the account opened) | Not determinable (§§ 5302, 5040). |
| GS-CA-019 | POD account; the payee is 15 years old | Not determinable: minor payee (§ 5407(b)). |
| GS-CA-020 | Sole account; Path B facts as in 001; before the affidavit arrived, the institution received a would-be heir's written claim and hold request | Not determinable (§ 13106(a) good faith; *Mautner*). |
| GS-CA-021 | As 001, but there is one affiant and the will leaves the account to three children | Not determinable: the affiant is not the sole successor (§ 13006). |
| GS-CA-022 | Path B account; a levy or FTB order to withhold has been served | Not determinable. |
