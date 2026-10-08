# California rule spec (DRAFT, not attorney-reviewed)

**Status:** Draft v0.1, written 2026-10-07 for REQ-CA-001. **Attorney review:** not started.
Nothing here is encoded in the engine until an attorney approves it. Statute text was read from a mirror of the official code (see [sources](sources.md)), and every citation must be confirmed against leginfo.legislature.ca.gov before approval. Numbered questions (Q1, Q2, …) are in [open-questions.md](open-questions.md).

## Where each answer comes from

- **Law:** statutory conditions and protections. These are fixed by the code and confirmed by an attorney.
- **Account terms:** facts about the specific account, such as POD or Totten beneficiary shares, survivorship, and signature requirements. They arrive with the account facts.
- **Institution policy:** choices the statute leaves to the institution, such as an extra waiting period, extra documents, or declining some cases. A policy may be **stricter** than the statute but never looser, and every decision records which policy version it used.

## What the engine decides

For one deposit account of a California decedent, the engine answers four questions:

1. Who may the institution pay, and in what shares?
2. What documents must the institution receive first?
3. What is the earliest date it may pay?
4. Does a statute protect the institution from liability if it pays as decided?

If the facts fall outside the paths below, the result is **not determinable** and the case goes to a person. The engine never guesses.

## Path A: accounts with a survivor or payable-on-death (POD) payee

Applies when the account is a joint account with a surviving party, a POD account with a surviving POD payee, or a Totten trust account with a surviving beneficiary.

| Question | Rule | Citation |
|---|---|---|
| Who is paid | **Joint account:** sums belong to the surviving party or parties. **POD account, sole or last surviving party deceased:** sums belong to the surviving POD payee(s). **Totten trust account, sole or last surviving trustee deceased:** sums belong to the surviving beneficiary or beneficiaries. | Prob. Code § 5302(a), (b)(2), (c)(2) |
| Shares | **POD and Totten:** two or more surviving payees or beneficiaries take **equal shares**, unless the account terms set different shares (account terms). **Joint, two or more survivors:** the institution may pay any one or more surviving parties according to the account terms. It does not have to work out each party's net contribution, and it is protected whether or not the payment matches beneficial ownership. | § 5302(b)(2)(B), (c)(2)(B); §§ 5401(a), (c), 5402, 5405(a) |
| Documents | Proof of death. **POD:** proof that the payee survived every original party. **Totten:** proof that the beneficiary survived every trustee. **Joint:** the claimant must be a surviving party; payment to a deceased party's representative or heirs needs proof that the decedent was the last surviving party. | §§ 5402, 5403, 5404 |
| Earliest payment | On request, once proof of death is presented. No statutory waiting period applies; an institution policy may add one. | §§ 5402, 5403, 5404 |
| Liability protection | **Yes.** Payment under §§ 5401–5404 discharges the institution from all claims for the amounts paid, even if inconsistent with beneficial ownership. **Exception:** no protection for payments made after the institution is served with a court order restraining payment. | § 5405(a), (b) |

**Not determinable on this path:**
- The POD payee or Totten beneficiary is a former spouse whose marriage or domestic partnership ended before the death. The designation may fail under § 5040, and its exceptions need human review.
- No POD payee or Totten beneficiary survived. The account then passes through the estate, so Path B or probate applies; the engine evaluates Path B when the facts support it.
- The account requires more than one survivor's signature (§ 5401(b)), or the institution holds a written § 5405(c) notice.
- The institution has been served with a court order restraining payment (§ 5405(b)).

## Path B: small-estate affidavit (accounts with no survivor or POD payee)

Applies to an account owned solely by the decedent, with no POD payee.

### Eligibility (all required)

| Condition | Citation |
|---|---|
| The gross value of the decedent's real and personal property in California is at or below the limit for the date of death (table below). Excluded from the total: § 13050 property (joint-tenancy property, multiple-party accounts passing to a survivor or POD payee, property passing to a surviving spouse under § 13500, revocable-trust property, registered vehicles, vessels, and mobilehomes) and property in a § 13151 petition. Also excluded: Armed Forces pay, and wages owed up to the § 13050(c) adjusted amount. | §§ 13100, 13050 |
| At least 40 days have elapsed since the death. | §§ 13100, 13101(a)(3) |
| No proceeding to administer the estate is being or has been conducted in California, **or** the personal representative has consented in writing. | § 13101(a)(4) |

**Value limit by date of death.** The limit is set under § 890 and published by the Judicial Council. "Does not exceed" means a value equal to the limit is eligible.

| Date of death | Limit | Citation |
|---|---|---|
| Before April 1, 2022 | $166,250 | § 13101(g)(1); Judicial Council § 890 list |
| April 1, 2022 – March 31, 2025 | $184,500 | § 13101(g)(2); § 890; Judicial Council § 890 list |
| On or after April 1, 2025 | $208,850 | § 13101(g)(2); § 890; Judicial Council § 890 list |

The next adjustment is scheduled for April 1, 2028. An adjustment never applies to a death before its effective date (§ 890(d)). **Coverage begins with deaths on April 1, 2022** (owner decision, 2026-10-07). Earlier deaths are not determinable.

### Decision

| Question | Rule | Citation |
|---|---|---|
| Who is paid | The person(s) who sign the affidavit or declaration as **successor of the decedent**, or as someone authorized under § 13051 to act for the successor (for example a guardian, conservator, trustee, or attorney-in-fact). A successor is whoever takes the item under the will, or under intestate succession if there is no will. The institution may rely in good faith on the affidavit and has no duty to check its statements. | §§ 13006, 13051, 13101(a)(7)–(8), 13105(a), 13106(a) |
| Shares | One affiant receives 100%. Several affiants are together entitled to the property (§ 13105(a)(1)), and the affidavit is "modified as appropriate" (§ 13101(b)). How payment is split between them follows the affidavit and institution policy (Q2). | §§ 13101(b), 13105(a)(1) |
| Documents | 1. An affidavit or declaration under penalty of perjury containing every § 13101(a) statement. 2. A certified copy of the death certificate. 3. For deaths on or after April 1, 2022, the Judicial Council's list of adjusted amounts in effect on the date of death. 4. If a personal representative consented: a copy of the consent and of the letters. 5. If the decedent held evidence of ownership that the institution could have required: that evidence, or a bond or indemnity agreement. 6. If the estate includes California real property: an inventory and appraisal by a probate referee. 7. Reasonable proof of each affiant's identity. | § 13101(a), (d), (e), (f); §§ 13102, 13103, 13104 |
| Earliest payment | The date 40 days have elapsed since death. Day counting is a legal question (Q3); an institution policy may add more days. | § 13100 |
| Liability protection | **Yes**, if §§ 13100–13104 are satisfied. Receiving the affidavit discharges the institution from further liability for the money paid, and it is not liable for state taxes because of the payment. | § 13106(a), (b) |

**Not determinable on this path:**
- The estate value exceeds the limit (probate or another procedure is needed).
- A California administration proceeding exists and there is no written consent from the personal representative.
- The account is secured by a lien on real property (§ 13106.5), which is out of scope.
- The facts don't include the declared estate value.

## Path C: surviving spouse or registered domestic partner

Under § 13500, property passing to a surviving spouse (by intestacy under § 6401, or by will) needs no administration. Section 13540 covers real property only. The procedure for a spouse to collect a **deposit account** without the Path B affidavit has not been confirmed yet (Q5). Until it is, a claim that relies only on spousal status is **not determinable**. A spouse who is a POD payee or a surviving joint party uses Path A, and a spouse who signs a small-estate affidavit uses Path B.

## Intestate shares (reference only)

Sections 6401 and 6402 set intestate shares: community property to the spouse, and separate property split between the spouse and issue, parents, or siblings according to who survives. On Path B the institution relies on the affidavit's statement of who the successor is (§ 13106(a)), so v1 does **not** compute intestate shares. Whether it should cross-check them is Q4.

## Facts the engine will need

The current `Facts` schema has no field for these, and adding them is a schema change for owner approval:

- Account type: sole, joint with survivorship, POD, Totten trust. Also whether the account requires multiple signatures, and whether a § 5405(c) notice or a restraining order has been received.
- Surviving joint parties, POD payees, and Totten beneficiaries (by party ID), plus any shares set by the account terms.
- Whether a POD payee or Totten beneficiary is a former spouse or former registered domestic partner.
- The declared gross value of California property, excluding § 13050 property, as stated in the affidavit.
- Whether the estate includes California real property.
- Administration status: none / proceeding exists with personal-representative consent / proceeding exists without consent.
- Affiants (by party ID) and the capacity each signs in (successor, or a § 13051 representative).

## Draft golden scenarios

These become `golden/ca.yaml` after attorney review. Dates assume Q3 is resolved as "death date + 40 days" and an institution policy that adds nothing.

| ID | Facts | Expected |
|---|---|---|
| GS-CA-001 | Sole account; died 2025-06-01; CA estate $150,000.00; no proceeding; one affiant (successor) | Pay affiant 1/1. Documents: affidavit, death certificate, 2025 § 890 list, proof of identity. Earliest payment 2025-07-11. Protected (§ 13106). |
| GS-CA-002 | As 001, but died 2025-03-31 with estate $184,500.00 | Eligible: equal to the limit for that date. |
| GS-CA-003 | As 001, but died 2025-03-31 with estate $184,500.01 | Not determinable: over the limit. |
| GS-CA-004 | As 001, but died 2025-04-01 with estate $208,850.00 | Eligible: new limit applies from 2025-04-01. |
| GS-CA-005 | As 001, but an administration proceeding exists with no PR consent | Not determinable. |
| GS-CA-006 | As 005, but the PR consented in writing | Eligible. Documents add the consent and the letters. |
| GS-CA-007 | As 001, but the estate includes CA real property | Eligible. Documents add an inventory and appraisal. |
| GS-CA-008 | POD account; two surviving POD payees; no share terms | Pay each 1/2. Document: proof of death. Payable on request. Protected (§ 5405). |
| GS-CA-009 | Joint with survivorship; one surviving party | Pay survivor 1/1 (§ 5302(a)). Protected (§ 5405). |
| GS-CA-010 | POD payee is the decedent's former spouse | Not determinable (§ 5040). |
| GS-CA-011 | Restraining order served before payment | Not determinable: no § 5405 protection. |
| GS-CA-012 | Died 2022-03-31 | Not determinable: before coverage starts (deaths from 2022-04-01). |
| GS-CA-013 | As 001, but died 2022-04-01 with estate $184,500.00 | Eligible: first day of coverage, at the 2022 limit. |
| GS-CA-014 | Totten trust; trustee was the sole trustee; two surviving beneficiaries; no share terms | Pay each 1/2. Document: proof of death showing both beneficiaries survived the trustee. Payable on request. Protected (§ 5405). |
| GS-CA-015 | Totten trust; account terms give beneficiaries 70% / 30% | Pay 7/10 and 3/10 per the account terms (§ 5302(c)(2)(B)). |
| GS-CA-016 | Joint with survivorship; two surviving parties | Payable to either or both per the account terms (§§ 5401(a), 5402). Protected (§ 5405). Needs a "joint payee" decision form (see open questions). |
