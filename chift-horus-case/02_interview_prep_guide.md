# Interview preparation guide: Chift × Horus, Part 1 (internal)

> **For you, not for Chift.** This guide is about understanding, not a script to memorise. If you can explain each "why" below in your own words, you can defend the work.
> Present from `chift_horus_connector_assessment.html` (the concise report). Use `chift_horus_mapping_report.html` (the detailed technical reference) only to look things up: it is kept unchanged, so where it differs from the concise report, the concise report and its appendix B (corrections) are the position you defend. `03_critical_review_register.md` lists every issue found in review.

---

## 1. Your approach, and why it makes sense

**What the case asks.** For 10 Chift routes, name the Horus endpoints and the specificities to watch (Task A). For 3 routes, go down to every attribute and query parameter (Task B). The case also hints that one Chift route may need several Horus calls. Chift says it wants to see *how you approach an unfamiliar API, structure your thinking, and explain it to a client*.

**What you did, in five steps:**
1. **Read both contracts.** Chift's spec gives what each route promises; Horus's reference and guides give what Horus can store and return.
2. **Aligned the vocabulary first.** "Company" in Horus means a third party the folder deals with (customer, supplier or beneficiary), not the folder's own company. A "daybook" is a journal. A "cost schema" is an analytic plan. Most mapping mistakes come from words that look alike but mean different things.
3. **Asked the same questions for every route.** What is the business object? What does Chift require? Can Horus read or write it? Which calls, in which order? Is each field direct, transformed, looked up, generated, or not available? What is lost?
4. **Labelled every claim.** Documented, Derived, Assumption, or To confirm (not documented). You never present a guess as a fact.
5. **Separated feasibility from design.** "Horus can do this" is a fact from the docs. "The connector should do it this way" is a proposal that Chift or Horus must confirm.

**Why it makes sense.** It is repeatable: the same checklist for every route makes the answers comparable. It is honest about evidence. And it turns gaps into concrete questions rather than hiding them. That is the BA's job: make the decision-makers' choices visible.

**How to describe the review.** "After the first version, I challenged my own work as a senior reviewer would. That changed the headline from 'all feasible' to a more careful split, surfaced the Horus VAT spreadsheets I had missed, and turned some of my implementation rules back into open questions." That shows judgment, not weakness.

---

## 2. The mapping decisions that matter, and the reasoning

You should be able to explain each one with a small example.

| Decision | Plain-language reasoning | Example |
|---|---|---|
| **Chift client → Horus company** | Horus keeps one record per third party, with "is customer" and "is supplier" flags. So a Chift client becomes a company flagged as customer. That is also why Chift's `force_merge` (merge a client into an existing supplier) makes sense on Horus. | A client who is also a supplier: one Horus company, both flags on. |
| **Horus needs a search key Chift doesn't send** | `companies.new` requires `SearchKey`, the third-party code accountants see, unique within the folder (length and allowed characters are undocumented, H7). Chift's create request has no such field (the code only comes back in the response as `third_party_account`), so the connector must generate one. **That rule is a proposal** (C8), and the accountant will see it. | "Acme SA" → `ACMESA`, with a numeric suffix if taken (proposal: upper-case, letters and digits only, shortened; Chift should agree the convention). |
| **VAT code → combination of fields** | Horus has no "VAT code" list. Each line carries a rate, an origin and a type (plus kind and condition for purchases). Only combinations listed in two Horus spreadsheets are valid, per country (Belgium, Luxembourg) and per direction (sales or purchases). So Chift's `tax_code` needs a translation table built from those spreadsheets. | Belgian domestic sale at 21 %: rate 21, origin 0 ("Vente nationale"), type 0 (National). |
| **Analytic percentages → amounts** | Chift sends a percentage per analytic plan. Horus wants amounts on combinations of analytic accounts, and the amounts must add up to the line's base amount. The connector converts percentages into amounts and handles rounding. | Line €1,000, Department 60/40 → €600 and €400. |
| **One Chift read → several Horus calls** | Horus has no endpoint that lists all invoices (`invoices.sales.outstanding.list` returns only open sales invoices and credit notes, without lines). To return Chift invoices, the connector reads entry headers (`book-entries.list`, one call per journal), then the ledger lines (`account-histories.list`: VAT, analytics, matching), plus, for sales, the open sales invoices list for payment status and invoice currency (purchase payment status comes only from ledger matching), and assembles them. | This is the case's "one Chift endpoint, several Horus endpoints" hint. |
| **"Posted" vs Horus "Confirmed"** | Horus keeps API entries unconfirmed by default so the accountant can review them, and invoices can't be deleted through the API. Whether to honour Chift's "posted" by confirming directly is a **decision for Chift**, not something you settle. Your proposal is review by default. | A vendor pushes an invoice; it waits in Horus until the accountant confirms it. |
| **Outstanding items: two different paths** | For customers, Horus has a ready-made list of open sales invoices with the open amount. For suppliers there is no equivalent, so open items come from unmatched ledger lines. How partial payments appear there isn't documented, so the supplier side **needs confirmation**. | A supplier invoice paid 50 %: the docs don't show how the remaining 50 % appears. |
| **Pagination emulated** | No Horus list has page parameters, so the connector fetches the full list and slices it into Chift pages. That the lists return complete results is a deduction (no paging parameters), not documented, and Horus documents no limits; behaviour on large folders **cannot yet be concluded** for any list route (H5). | Invoice retrieval over several years in a big accounting firm. |

---

## 3. Technical concepts at a conceptual level

You need to understand these, not implement them.

- **Endpoint / route.** A URL that does one thing ("create a company"). Chift calls its own endpoints "routes"; the connector translates each one into one or more Horus endpoints.
- **Request and response.** The data sent and the data returned. Horus create calls return only an **id**, so to give Chift the full record the connector reads it back with extra calls (two to three for a client).
- **Query parameter.** A filter or option in the URL (`folder_id`, `date_from`). Task B asks for these explicitly.
- **Lookup.** A Horus reference must be found first, usually in cached reference data. Example: Horus posts analytics by code, so a Chift analytic account id (the Horus cost-section id) is turned into the section's search key from the cached section list; a Chift tax code is turned into a Horus VAT combination. Careful: journal_id and lines[].account_number are *Direct* in the Task B table (the journal id is the Horus daybook id, and the account number is the search key Horus posts with).
- **Pagination.** Returning a long list page by page. Chift does it; Horus doesn't, so it is emulated.
- **Idempotency.** Being able to repeat a request safely without creating a duplicate. Horus documents no idempotency mechanism, so after a timeout the connector must check whether the record exists before retrying. That works only when there is something to search on (an invoice number, a VAT number).
- **OAuth and tokens.** The user logs in to Horus once and grants access; the connector then uses a token. Horus tokens expire after an hour and the refresh token can be used only once. You only need to know that this exists and must be handled carefully.
- **License and folder.** Each Horus customer (a fiduciary or an SMB) has its own database and API address (the license). Inside it, each company's books are a folder. Chift's `folder_id` maps to a Horus folder.
- **Book entry and confirmation.** Every accounting document in Horus becomes a book entry. "Confirmed" is the state after review: API entries are unconfirmed by default so the accountant can review them. Whether every user may confirm through the API, and whether confirmation is the accountant's final validation, is open (H21). Changing an entry through the API creates a new entry with a new id.

---

## 4. Assumptions you must be transparent about

Say these openly before Chift finds them:

1. **Documentation version.** The case links the older Horus docs (apiary). You used the current docs (docs.horus-software.be, reference dated 24 Sept 2026) and did not compare the two.
2. **Chift spec version.** You used the OpenAPI file bundled in Chift's Python SDK (version 0.6.16), because docs.chift.eu wasn't reachable from your environment. Chift should confirm nothing important has changed.
3. **No live testing.** This is a desk analysis. No request was sent to Horus or Chift.
4. **Ledger amounts in euro.** Horus doesn't say in which currency ledger amounts are stored for foreign-currency documents. You assume the folder currency (euro).
5. **Invoice vs credit note on read.** Horus entries and ledger lines don't say invoice or credit note (only open sales items and attached documents carry a type). Your proposed rule: the daybook type decides, and the amount sign only in folders without a credit-note daybook. It is a proposal, not documented behaviour (H2); known failure: a credit note keyed into a sales daybook reads back as an invoice with negative amounts.
6. **Generated values.** The company search key, the VAT-code naming scheme and the rounding of analytic amounts are your proposals, not Horus or Chift rules.
7. **Volumes.** Horus documents no paging and no limits. That its lists return complete results is a deduction from the absence of paging parameters, and nothing was tested, so behaviour on large folders cannot be concluded for any list route (H5).
8. **VAT spreadsheets.** You assume the two Horus tax-combination spreadsheets are current and complete, and that the API accepts the Luxembourg origins missing from the API reference's value lists (H1).
9. **Supplier open items.** You assume `suppliers.outstanding` without a company filter returns every supplier's open lines, partially matched ones included; otherwise a fallback read of supplier ledger lines is needed (H8).

---

## 5. Likely questions, and answers you can defend

**"Is the connector feasible?"**
"The documentation rules out none of the 11 routes: Horus has a documented endpoint for each route's core object. But that isn't the same as 'everything is settled'. One route is confirmed by the documentation (analytic accounts). Six are feasible but rest on assumptions the documentation doesn't confirm. Four need answers from Horus or decisions from you before their design is final: invoice retrieval, invoice creation, miscellaneous operations and outstanding items. And behaviour on large folders can't be concluded for any list route. So I'd recommend a short validation phase, with a test licence and answers to the before-build questions, rather than going straight to a full build."

**"Why does creating an invoice need so many Horus calls?"**
"Chift sends most references (journal id, partner id, account numbers), but the connector checks them against the folder before posting, because a wrong invoice can't be deleted through the API. Horus posts analytics by code, so analytic ids must be translated; the folder's legislation selects the VAT list; the fiscal years are checked for closed periods; and there's a best-effort duplicate-number check. Most of that is reference data cached per folder. Then the create call returns only an id, so to return the full invoice we read it back."

**"What will our clients notice?"**
"Mainly five things:
- Invoice numbers must be numeric.
- An invoice changed in Horus gets a new id.
- Pushed invoices may wait for the accountant's review.
- Horus keeps one address per customer and no line quantities.
- Foreign-currency details are partly returned in euro."

**"How do you handle VAT?"**
"Horus publishes the valid VAT combinations in two spreadsheets, per country and direction. My proposal is that the connector keeps a VAT-code list built from them, translates each Chift tax code into one of those combinations and rejects anything that isn't on the list; you'd need to agree that convention (C2). I found inconsistencies between the spreadsheets and the API reference, for example Luxembourg origins missing from the reference's value lists and the partial-deduction value shown as both 35 and 0.35, so asking Horus which is authoritative is the first question on my list (H1)."

**"Why is outstanding items harder for suppliers?"**
"For customers, Horus has a ready list of open sales invoices with the open amount. For suppliers there's no equivalent, so we'd compute open amounts from ledger lines that aren't matched yet. The docs don't say how partial payments show up, so I'd confirm that with Horus before promising supplier balances."

**"What would you ask Horus first?"** Four things:
1. Are the VAT spreadsheets current?
2. What are the limits, and is there a test license?
3. The invoice endpoints have no automatic-numbering option: how are invoices sent without a number numbered, is a number unique per daybook and year, and is there a safe way to retry after a timeout (H3)?
4. How are partial matches returned for suppliers?

**"What do you need from Chift?"** Five things:
1. Should "posted" mean confirmed directly, or go to the accountant's review first?
2. Is rejecting non-numeric invoice numbers acceptable, and should an invoice without a number go to review as a draft (my proposal), be rejected, or get a generated number (C7)?
3. Can connectors cache data, and what are your timeouts?
4. Who converts foreign-currency operations: Chift or the connector?
5. Is the SDK spec current?

**"Why didn't you estimate effort?"**
"I gave a relative build-effort estimate per route in section 1 (low: folders, analytic plans, journals, analytic accounts; medium: client creation, ledger account creation, chart of accounts, miscellaneous operations; high: invoice creation, invoice retrieval, outstanding items). It's my estimate, to calibrate with you. I didn't give days, because that depends on your connector framework and on the answers to the open questions."

**"You changed your conclusion between versions?"**
"Yes. I reviewed my own work against the documentation and tightened the claims: I separated what's documented from what I assumed. The detailed reference is unchanged; the material corrections are listed in appendix B of the assessment report, and the route details and Task B tables follow the corrected position throughout."

---

## 6. Decisions to refer to technical colleagues

Don't claim to have validated these yourself. Say: "That's a design choice I'd make with the engineering team."

- **Caching, timeouts, background processing** for large reads: Chift platform architecture.
- **Retry and duplicate-protection logic** after timeouts: engineering, with Horus's input on idempotency.
- **Token handling** (single-use refresh tokens, concurrency): engineering.
- **Rounding algorithms** for analytic amounts, and VAT plausibility tolerances: engineering and finance, with Chift's conventions.
- **Exact error codes** returned to Chift clients: Chift's connector conventions.
- **Performance at volume**: needs a test license and measurement, not desk analysis.
- **Accounting policy questions** (credit-note conventions, posting periods, VAT treatment for specific cases): the client's accountant or Chift's accounting experts.

What you *do* own: what each field means, why it maps where it does, what is lost and why that matters to a client, and which questions must be answered before building.

---

## 7. Ten-minute checklist before the meeting

- [ ] Walk the route table out loud, one sentence per route.
- [ ] Explain one Task B row of each type: direct, transform, lookup, generated, not available.
- [ ] Explain the "What is confirmed, assumed or still open" box in section 1: confirmed, assumption, needs confirmation, not concluded.
- [ ] Pick the five questions you'll actually ask Chift.
- [ ] If you can, spot-check docs.chift.eu for the create-invoice and outstanding-items routes.
