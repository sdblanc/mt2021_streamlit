# Meeting prep guide: Chift × Horus, Part 1 (internal)

> **Internal only.** A short guide to presenting and defending the Part 1 mapping. Details: `chift_horus_mapping_report.html` (external report), `01_internal_notes_part1_mapping.md` (study notes), `03_critical_review_register.md` (the 63 review issues, each with "if Chift raises it").

## 1. Your opening (60 seconds)

"I mapped the 11 Chift routes onto the current Horus API documentation. **No route is blocked by a missing Horus capability.** Only *Get folders* maps one to one. The other ten are feasible with workarounds of very different weight: low for journals, analytic plans and analytic accounts; medium for client, ledger-account and miscellaneous-operation creation and the chart of accounts; high for invoice creation, invoice retrieval and outstanding items. Four routes wait on priority-1 answers before their design is final. My recommendation is a **conditional go**: a short gate (test license, Horus confirming its VAT files and limits, and two Chift decisions on posting mode and numbering), then three phases. The rest of the deck shows how I got there, what your clients will notice, and what I need from you."

Storyline for the slides or the walk-through: **§1 summary → §4 overview table (the ratings columns) → one deep dive (invoice creation, §5) → §6 client impact → §9 priority-1 questions → §1 recommendation.**

## 2. Concepts you must master

| Concept | What to say | Basis |
|---|---|---|
| License, `api_url`, OAuth | One license = one database = its own API URL, returned at the end of OAuth on my-horus.com. Non-standard `grant_type=auth_code`; code valid 2 min, access token 1 h; refresh tokens are **single-use**, so refreshes are serialised per connection. `folders.list` returns the folders the authorising user can access (all folders for an accountant, Mode 0). | Guides: Authentication, Token lifecycle, Data model; folders.list |
| Folder | Horus folder = Chift folder (one legal entity). Almost every call takes a `FolderId`; calls by id don't, so the connector checks folder ownership (D13). | Guide: Data model |
| Company | A Horus "company" is a **third party**, one record with `IsCustomer` / `IsSupplier` flags. That is why `force_merge` makes sense on Horus. Postings reference it by **search key**, which Horus requires and the connector must generate (proposal, C8). | companies.new; Data model |
| Daybook → endpoint | The daybook type decides the posting endpoint: 100/150 purchases, 200/250 sales, 600 miscellaneous. Entries are created by business endpoints (invoices, operations) that all return a book-entry **id only**. | Guide: Data model |
| Confirmed | API entries are **unconfirmed by default** so the accountant can review them. Updating an invoice or operation creates a **new id**. Invoices cannot be deleted through the API; miscellaneous operations can (`book-entries.miscellaneous-operations.delete`). | Guides: Data model, Posting invoices; reference |
| VAT | No VAT-code list and no VAT code on write. Each line carries a **combination** (rate, origin, type; plus kind and condition for purchases). The valid combinations are in **two Horus spreadsheets, per legislation (BE, LU) and direction**: sales 18 BE / 58 LU rows, purchases 109 BE / 146 LU rows (Appendix C). Reads return `VatCode` / `VatHeading` strings whose meaning is undocumented. | invoices.*.new; tax-combination files |
| Analytics | Cost schema = analytic plan (max 8 per folder); cost section = analytic account. Cost lines carry **amounts** on combinations, so Chift's per-plan percentages must be converted (largest-remainder rounding, D8). | Guide: Posting invoices; cost-schemas.list |
| Reads | No list endpoint has paging parameters (**deduction**: lists return the full result). Text filters use "contains". `ModifiedAfter` exists only on **book-entries.list, account-histories.list and companies.list**. `Include` sideloading works on 4 endpoints only. | Guides: Making requests, Sideloading; reference |
| Open items | Client side: a native open-sales-invoice list with open amount and payment status. Supplier side: **no purchase equivalent**, so open amounts come from unmatched ledger lines and their matching (partial-matching semantics are undocumented, H8). | invoices.sales.outstanding.list; Outstanding items guide |

## 3. Decisions to explain

Each is a **proposal**. Know why, and what would change it.

| Decision | Why | Changes if… |
|---|---|---|
| **Strict verdict scale** (1 supported / 10 workaround) | One definition for every route, with no exceptions. Analytic plans is a workaround only because paging is emulated (≤ 8 rows) and Free dimensions are hidden. Hence the complexity column. | Chift has its own coverage scale (follow it). |
| **Posting mode: review by default** (D12, C1) | Horus is designed for accountant review, invoices can't be deleted through the API, and confirmation rights are undocumented (H21). The response always reports the stored status. | Chift wants "posted" honoured by default → direct mode, with rights confirmed by Horus. |
| **Numbering** (C7) | Horus needs numeric numbers and doesn't auto-number through the API. Without `invoice_number`, push for review with number 0 and return a draft. Never guess max+1 by default. | Horus offers automatic numbering (H3). |
| **VAT catalogue from the Horus files** (D2, C2) | The only documented list of valid combinations. One synthetic code per row (`S-21-0-0`, `P-…`), per folder legislation. On read, return a code only when exactly one row matches. | Horus confirms `VatCode` is a stable code (H1) → use it on read. |
| **Foreign-currency miscellaneous operations: convert, don't reject** (LD6, C15) | Chift's own contract asks for conversion at the supplied rate when the journal allows no other currency. Horus operation lines have no currency field. | Chift core already converts → the connector only checks the balance. |
| **Invoice vs credit note on read** (D1, C5, H2) | The invoice type isn't exposed on read. Options: daybook first (250/150) with the sign as a fallback, or sign first. Each fails differently; that's a decision for Chift. | Horus exposes Type on reads (H2). |
| **Duplicate protection is best effort** (C6) | No idempotency key. Search before create and before any retry, which works only when there is a key (number, VAT number, reference). Otherwise report an unknown outcome. | Horus documents an idempotency mechanism (H3). |
| **Folder rule** (D7, D13, C12) | folder_id required when several folders are selected; folder checked on every id call; an unselected folder is rejected. | Chift's platform already enforces selection. |
| **Pagination and caching** (C14, H5) | Fetch, filter and slice, with a per-folder reference cache and a short-lived page cache. Default window on invoice retrieval: the current fiscal year (C11). | Horus limits or Chift timeouts → mandatory date window (descoping trigger). |
| **Conditional go, three phases** | Reference reads and simple creates first (with a volume test), then invoice and operation creation, then ledger-rebuilt reads once H2, H4, H5 and H8 are answered. | Gate 0 fails (no test license, VAT files unconfirmed). |

## 4. Likely challenges and short answers

1. **"How can you say nothing is blocked?"** "Every object exists and is readable or writable. What's pending is confirmation, not capability: Horus's VAT files and limits, and your posting and numbering decisions."
2. **"Why is analytic plans a workaround?"** "I applied one scale without exceptions. Paging is emulated, even if only over 8 rows, and Free dimensions are hidden pending your choice (C9). The complexity column shows it's trivial."
3. **"Nine 'workarounds' tell me nothing."** "Agreed. That's why each route also has build complexity, client impact and the questions it depends on."
4. **"Will it scale without pagination?"** "For typical folders, yes. For large folders it's unverified: that's H5 plus a volume test in Phase 1, with a date-window descoping trigger."
5. **"Why not just post as confirmed?"** "Horus keeps API entries unconfirmed for review, and a wrong invoice can't be deleted through the API. Review is the safer default; direct mode stays an option per connection."
6. **"Your docs aren't the ones we linked."** "The case links the former apiary docs. I used the current docs.horus-software.be (reference dated 24 Sept 2026) and said so in §2. I've asked Horus which is authoritative (H20)."
7. **"Is your Chift spec current?"** "It's the OpenAPI bundled in your SDK, version 0.6.16; docs.chift.eu was not reachable from my environment. Please confirm the 11 routes haven't changed."
8. **"Isn't the VAT mapping guesswork?"** "No. It's built from Horus's own accepted-combination files. I found three discrepancies with the API reference (Luxembourg OSS origins, Luxembourg origin codes, the PCT value format) and asked Horus (H1)."
9. **"What do our clients lose?"** Walk §6: ids change after edits, numeric numbers, no invoice delete, one address per partner, no line quantities, purchase VAT codes sometimes empty on read, foreign currency partly in euro.
10. **"How long would it take?"** "I didn't estimate effort: the complexity ratings are relative. Phase 1 is the cheapest learning step and de-risks volume and auth."

## 5. Questions to ask Chift

**Ask these five** (all priority 1):
1. **C1 Posting mode.** Review by default, or honour "posted" as confirmed?
2. **C7 Numbering.** Is rejecting non-numeric numbers acceptable, and what happens to an invoice without `invoice_number`?
3. **C14 Caching and timeouts.** Can a connector cache reference data and page results? What is the synchronous timeout, and is there a background pattern?
4. **C15 Foreign-currency operations.** Does Chift core convert before calling the connector, and in which rate direction?
5. **Spec version.** Is the SDK 0.6.16 spec aligned with the live reference for these 11 routes?

**Backup:** C2 (VAT catalogue and null on ambiguity), C12 (folder selection enforcement), C5 (sign conventions and the credit-note choice), C17 (outstanding-item granularity), C8 (meaning of `partner_info.account_number`), and "which flows do your clients need first?" (to order the phases).

**For Horus** (mention only that these are queued; priority 1): H1 VAT files, H2 invoice type on read, H3 numbering and idempotency, H4 currency of ledger amounts, H5 limits, H8 completeness of open items, H17 test license, H19 registration, H20 documentation version, H21 confirmation rights, H24 OAuth lifecycle.

## 6. What changed after the senior review

You should own these changes and present them as rigour, not as rework.

1. The verdict scale is now applied strictly: **1 supported / 10 workaround**, and analytic plans was downgraded.
2. New columns: build complexity, client impact and blocking questions.
3. The headline is qualified, and volumes are flagged as unverified (H5).
4. The recommendation became a **conditional go** with Gate 0, three phases and descoping triggers.
5. Posting mode: **review by default**, with the stored status always reported.
6. Foreign-currency miscellaneous operations are **converted**, no longer rejected.
7. The **Horus tax-combination spreadsheets** were found and added (Appendix C). H1 is now a confirmation question.
8. Sources disclosed: apiary vs current Horus docs, the SDK-bundled Chift spec, and desk analysis only.
9. Questions now have **tiers** and stable ids. There are 14 new questions (H19–H25, C14–C20).
10. A new **§6 Impact on client applications**, in plain language.

## 7. Before the meeting

- [ ] Spot-check docs.chift.eu for the 11 routes (tax_code, invoice_number, the outstanding-items parameters, folder_id). This environment couldn't reach it.
- [ ] Open the two VAT spreadsheets once, so you can show one Belgian sales row and one purchase row.
- [ ] Rehearse the §4 overview table out loud, one sentence per route.
- [ ] Prepare one deep dive: invoice creation (§5), covering VAT, analytics, numbering and posting mode.
- [ ] Decide which five questions you will actually ask. Leave the rest in the report.
