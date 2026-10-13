# Chift × Horus: Part 1 (mapping), internal working notes

> **Internal only. Not for Chift.** These are my study and prep notes. The external deliverable is `chift_horus_mapping_report.html`.
>
> **Status:** Part 1 is complete and has been revised after a senior BA review (63 issues: 3 critical, 39 major, 21 minor). The review was applied to the mapping data, the report and these notes. Every route is mapped to Horus and checked against the Horus API reference, the guides and the tax-combination files. Open points are listed explicitly; nothing in these notes fills a gap with guesswork. This is a **desk analysis**: no request was sent to a Horus license or a Chift environment.

**Labels used throughout**

| Label | Meaning |
|---|---|
| **[F]** | Fact, stated in a source (source given) |
| **[D]** | Deduction, my conclusion from facts (reasoning shown). Includes conclusions from the *absence* of something in the docs |
| **[A]** | Assumption, plausible but unconfirmed; must be validated. A connector **proposal** (a rule we chose) is labelled [A] too, with the decision or question that owns it |
| **[?]** | Missing or ambiguous in the documentation |
| **[BG]** | General accounting background, to explain a concept. Not a claim about Chift or Horus |

**Source tags:** `[Case]` · `[Chift <operationId or schema>]` (Chift OpenAPI) · `[Horus <endpoint>]` (Horus API reference) · `[Guide: <title>]` (Horus guide pages) · `[Tax files]` (Horus tax-combination spreadsheets, `appendix_horus_tax_combinations.md`)

---

## What changed after the senior review

The ten corrections that matter most, one line each. Full list with evidence and "if Chift raises it" notes: **`03_critical_review_register.md`** (issue register). How to present and defend the result: **`02_meeting_prep_guide.md`** (meeting guide).

1. **Verdicts and ratings:** the scale is applied strictly, with no exceptions: **1 Supported (folders) / 10 Supported with workaround / 0 Not supported**; analytic plans moved to workaround (Low complexity), and every route now carries a complexity, a client impact and the tier-1 questions it waits on (§5).
2. **Headline and recommendation:** "No route is blocked by a missing Horus capability *in the documentation reviewed*", and the recommendation is a **conditional go**: Gate 0, three phases, descoping triggers (§8, §9).
3. **VAT:** the two tax-combination spreadsheets are now read (`[Tax files]`, report appendix C); the catalogue is one list per folder legislation (BE/LU) and direction, the LU codes disagree with the reference enums, and H1 now asks Horus to *confirm* the files, not to send them (§0, §5.3).
4. **Posting status:** "posted" is no longer mapped to `Confirmed=true` by default; proposal: a per-connection posting mode, **review (default)** or direct, and the response always reports the status actually stored (D12, C1, H21) (§5.3, §5.11).
5. **Numbering:** no connector-invented numbers by default; an invoice without a number is pushed for review and returned as a draft, max+1 only as an opt-in, non-numeric numbers rejected (D12, C7) (§5.3).
6. **Foreign currency:** miscellaneous operations in another currency are **converted at the supplied rate, never rejected** ("EUR-only" is gone, C15), and the switch of a paid foreign-currency sales invoice to EUR is disclosed (C16) (§5.2, §5.8).
7. **Credit notes on read:** the daybook type decides; the partner-line sign only in folders without a credit-note daybook; TransactionType is a check, not an override (D1 revised) (§5.2).
8. **Supplier outstanding items:** open amount = amount of the unmatched line; netting per matching group only if Horus returns partial matches (H8), with a documented fallback, control totals and double-count guards (§5.11).
9. **Reliability:** duplicate protection is best effort (no automatic retry without a business key, a lock on identical calls), a failed read-back never returns an error, partner_info reuses only an exact code + name match, and every route rejects an unselected folder (D7, D10, D12, D13) (§5.1, §5.3, §9).
10. **Sources and structure:** sources disclosed (current Horus docs vs the apiary link in the case, SDK-bundled Chift spec, no live calls); questions tiered with stable ids (new H19–H25, C14–C20); the report gained section 6 "Impact on client applications" and appendix C, so sections 6–10 are renumbered (§0, §8, §10).

---

## 0. Sources: what I used, and how much to trust it

| Source | How I got it | Status | Trust |
|---|---|---|---|
| Case page "Case Product / Tech" | Notion connector (public chift.notion.site page) | ✅ Read in full | Primary |
| Chift API reference | `docs.chift.eu` could not be reached from this environment. I used the **OpenAPI spec bundled in Chift's official Python SDK** (`chift` v0.6.16 on PyPI) | ✅ Read | High. All 11 case URLs match operations in this spec one for one. It's a snapshot, so **spot-check the live docs before presenting** (start with tax_code, invoice_number, the outstanding-items parameters and folder_id) |
| Horus API reference (72 endpoints) | Your Notion export (`horus.zip` on Drive: welcome page + every API Reference page, each embedding an OpenAPI 3.0.3 fragment; docs dated 24 Sep 2026), plus the `book-entries.info` page you supplied separately. These are the **current docs at docs.horus-software.be**; the case links the former apiary docs (`horussoftwareapi.docs.apiary.io`). The two versions were not compared (H20 asks which is authoritative) | ✅ Merged and rendered (`appendix_horus_api_reference.md`) | High |
| Horus guides (15 pages) | Your PDF prints (Drive folder "Horus guides"), printed from docs.horus-software.be on 13 Oct 2026 | ✅ Text-extracted (`appendix_horus_guides.md`) | High. Extraction noise in some tables |
| Horus tax-combination spreadsheets | Downloaded 13 Oct 2026 from the links on `invoices.sales.new/update` and `invoices.purchases.new/update` | ✅ Converted (`appendix_horus_tax_combinations.md`); summarised in report appendix C | High; codes and labels disagree with the reference for LU (H1) |
| Not available | Horus Quickstart, Register your integration, Support & FAQ, Changelog; the Postman collection; any webhook documentation | ⛔ | The questions these pages would answer are in the report: registration (H19), doc version (H20), limits (H5), deletion signals (H10) |
| Live calls | None: desk analysis, no request to a Horus license or a Chift environment | n/a | Every claim rests on documents; volumes and behaviour are verified in Gate 0 / phase 1 |

**Discrepancies between Horus sources (worth knowing, and worth mentioning to Chift):**
- [F] The guide *Reading accounting data* says "Use `book-entries.info` to get the full detail of one entry". That page was missing from the first export; you supplied it separately. It returns the entry **header only** (lines as references), so "full detail" in the guide overstates it a little. Worth asking Horus whether more detail is planned.
- [F] Line-type codes differ by endpoint: miscellaneous/bank operation lines use `Type` **1** Customer / **2** Supplier / **3** General [Guide: Bank, financial & miscellaneous operations], while matching and account histories use **100** / **200** / **300** [Guide: Outstanding items & matching]. These are easy to mix up in a connector.
- [F] The page text of `customers.outstanding` says "Get **a customer's** outstanding debts", but its `CompanyIds` filter is an optional array. Whether an empty filter returns **all** customers needs confirming (H8).
- [F] The LU tax-combination sheets use TaxOrigin codes outside the reference enums (sales up to 35 vs 0–20 in `invoices.sales.new`; purchases 40–56 vs 0–39 in `invoices.purchases.new`), and labels differ for sales 15/16/18/19/20 and purchases 12/16/22/23/27 (e.g. purchases 12: "Hors CEE sans facture" in the reference, "Achat TVA Marge" in the file). OSS for LU uses origins 24/26/29, while the reference says TaxCountryCode is "Only used for OSS Vat lines (TaxOrigin = 13)". The PCT condition is 35/50/75/85 in the combinations but 0.35/0.5/0.75/0.85 in "Available values". Typo "Nationam" in one BE purchase row. All asked in H1 [Tax files; Horus invoices.*.new].
- [F] The guide *Making requests* says "Many lists also offer ModifiedAfter / ModifiedBefore"; the reference shows them on three lists only (companies, book-entries, account-histories).

---

## 1. The case in my own words

**What the case asks** [Case]:
- *Task A (route level):* for 10 Chift endpoints, which Horus endpoint(s) to use, and "any particular considerations or specificities".
- *Task B (attribute level):* for **Create client**, **Create sale/purchase entry (multiple plans)** and **Get outstanding items**, a mapping "at the level of each attribute and the different query parameters". Outstanding items is an 11th endpoint that appears only in Task B.
- *Hint:* "it can happen that we need to pull data from multiple endpoints when implementing 1 endpoint in Chift."
- *What they assess:* "how you approach an unfamiliar API, how you structure your thinking, and how you'd explain it to a client."

**Plain restatement.** Chift sells one standard accounting API to software vendors. For each accounting package, Chift maintains a **connector** that translates each standard route into calls on that package's own API. Horus is a candidate package. For each standard route, the question is: *can it be built on Horus, with which calls, and what is lost or needs a workaround?*

```text
Software vendor ──(1 standard call)──► Chift route ──► Horus connector ──(1..n calls)──► Horus API (license-specific URL) ──► one folder
                                                       translate params · map fields · resolve IDs · combine responses
```

## 2. Business objective and expected outcome
- **Objective [D]:** a go/no-go and scoping decision for a Horus connector: coverage of Chift's accounting surface, effort drivers, and limitations Chift must communicate to its clients.
- **Outcome:** a route-level verdict table with complexity, client impact and dependencies per route; field-level mappings for 3 routes; a client-impact section in plain language (report section 6); dependencies, edge cases and limitations; and a tiered list of open questions for Horus and for Chift, feeding a conditional go.

## 3. The method (this is what they want to see)
For every Chift route, ask the same 7 questions:
1. **Business meaning:** what object or action is this?
2. **Chift contract:** what is required as input, and what is promised as output?
3. **Capability:** does Horus have the object, and can it be read and/or written?
4. **Endpoint(s):** which Horus calls, and in what order?
5. **Fields:** direct, transformed, looked up, composite, constant, or unavailable?
6. **Behaviour:** filters, pagination, incremental sync, status and numbering: native or emulated?
7. **Risk:** limitations, edge cases, error handling.

**Verdict scale (D11, applied identically to every route, no exceptions by decree):**
- ✅ *Supported*: Horus endpoint(s) natively serve the route with deterministic mapping and cached reference lookups only; no extra live Horus calls per request beyond those needed to produce the response; no emulated filtering, paging or numbering; no loss of a capability clients typically rely on.
- 🟡 *Supported with workaround*: feasible, but needs extra live calls per request (read-backs, joins, loops), emulated filters/paging/numbering, or loses a capability; the route works for the documented scope.
- 🔴 *Not supported*: the route cannot be served from the documented API.
- ⚪ *To confirm*: feasibility itself depends on an unanswered question.

On top of the verdict, each route gets three ratings (report section 4): **complexity** (Low/Medium/High: live calls, emulation, business rules to own), **client impact** (what client applications notice) and **depends on** (tier-1 questions the final design waits on). Verdict = can it be built; complexity = how hard; impact = what clients notice.

**Field codes:** `DIRECT` · `TRANSFORM` (format, enum or sign) · `LOOKUP` (resolve an ID via another call) · `COMPOSITE` (built from several fields or calls) · `CONSTANT` (the connector sets the value) · `NA` (no Horus equivalent) · `CHIFT_INTERNAL` (handled by Chift itself, e.g. pagination emulation).

**How the analysis was done:** I read both contracts myself and spot-checked the key endpoints. Independent analysts then mapped each route group. For every mapping, a separate reviewer tried to *refute* each claim (an evidence check) and another looked for *gaps* (a completeness check). A reconciler re-checked each challenge against the docs, and a final critic checked consistency across routes. Then a **senior BA review** challenged the whole solution as Chift would (63 issues, all applied; see `03_critical_review_register.md`). This mirrors how I would review a colleague's mapping.

## 4. Domain primer: Chift concepts ↔ Horus concepts

Before any route mapping, align the vocabulary. **The same word can mean different things in the two systems.**

| Chift concept | Horus concept | Key facts and traps |
|---|---|---|
| Consumer / connection | **License** + OAuth connection | [F] "Each license has its own database and its own API endpoint" (`api_url`, returned at the end of the OAuth flow; never hard-code it) [Guide: Authentication overview]. One connection = one grant by one user for one license, and it sees every folder that user can access [D] |
| **Folder** (legal entity) | **Folder**: "the accounting record of one company" | [F] "Almost every endpoint requires a FolderId" [Guide: Data model]. `folders.list` takes `Mode` 0 = all folders, 1 = my folders |
| Client / supplier | **Company** with `IsCustomer` / `IsSupplier` flags (also beneficiaries) | ⚠️ In Horus, "company" means a *third party*, not the legal entity. One object serves both roles, so Chift's `force_merge` is meaningful [Horus companies.new] |
| Journal | **Daybook** | [F] "The daybook Type drives which endpoint you use to post entries" (100/150 purchases, 200/250 sales, 500 bank, 590 financial, 600 misc.) [Guide: Data model] |
| Ledger account | **Account**, identified by `SearchKey` (usually the account number) | [F] Postings reference accounts **by search key**, not by Id [Guide: Data model] |
| Analytic plan | **Cost schema** (an analytical dimension; up to 8 per folder) | [F] Requires the folder's `WithAnalytics` module [Guide: Data model] |
| Analytic account | **Cost section** (a value within a schema) | Referenced by search key in postings |
| Analytic distribution (% per plan) | **Cost lines**: *amounts* on a combination of schema values, or a predefined **cost distribution key** | ⚠️ Percentages per plan must be converted to amounts on joint combinations [Guide: Posting sales & purchase invoices] |
| Sale/purchase entry ("invoice") | **Book entry** created by `invoices.sales.new` / `invoices.purchases.new` (`Type` 0 = invoice, 1 = credit note) | [F] Create returns only the book entry `Id` [Guide: Responses & errors] |
| Invoice lines | Invoice lines → stored as **account history lines** | [F] "one line per account movement, with debit/credit amounts, VAT information, matching number" [Guide: Data model] |
| VAT code (`tax_code` = an ID) | **No VAT-code list and no VAT-code input.** VAT = `TaxRate` + `TaxOrigin` + `TaxType` (+ `TaxKind`, `TaxCondition` for purchases) | ⚠️ "Only some combinations are valid" [Guide: Posting sales & purchase invoices], listed in two Horus spreadsheets (BE/LU, sales/purchases) [Tax files]. On read, ledger lines return `VatCode` / `VatHeading` strings whose meaning is undocumented [?, H1] |
| Miscellaneous operation | Book entry in a misc. daybook via `book-entries.miscellaneous-operations.new` | [F] Debit/credit lines that must balance [Guide: Bank, financial & miscellaneous operations] |
| Bookyear | **Fiscal year** (with closure dates per daybook type) | [F] "Check closure dates before posting" [Guide: Data model] |
| Posted vs draft | `Confirmed` true/false | [F] "Entries pushed through the API are unconfirmed by default", to let the accountant review [Guide: Data model]. ⚠️ Not identical to "posted": Confirmed means *validated by the accountant*. Proposal (D12): per-connection posting mode, review by default; the response always reports what was stored |
| Outstanding item | Unmatched account history line, or open sales invoice | [F] "Lines that are not matched yet make up the outstanding items" [Guide: Outstanding items & matching]. How partially matched lines are returned is H8 |
| Matching number | `MatchNo` | Same account type and company required [Guide: Outstanding items & matching] |
| Attachment (PDF) | **Document** (main document + annexes) | Upload as `multipart/form-data` with `file` + `body` [Guide: Documents & attachments] |

### Horus API conventions that shape every route
- **Style [F]:** JSON-RPC-style methods `{api_url}/{category}.{action}`. `GET` with query string for simple reads (`.info`, `.me`). **`POST` for lists with filters**, creation and updates [Guide: Making requests]. Exception: `cost-schemas.info` and `cost-sections.info` are POST [Horus reference].
- **Envelope [F]:** payload under `Data`. Related entities are references `{Type, Id}`. Create and update return the new Id (a few wrap it in `Data`; `matching` returns `Data.MatchNo`) [Guide: Responses & errors; Horus reference].
- **Sideloading [F]:** an `Include` parameter (dot paths, comma-separated) returns related entities under `Included`, but **only on `book-entries.list`, `account-histories.list`, `companies.list` and `invoices.sales.outstanding.list`** [Guide: Sideloading].
- **Pagination [D]:** no paging parameter exists on any list endpoint in the reference, and the request guide describes none. So Horus lists are *expected* to return the full result (a deduction from absence, never "documented"), and **Chift must emulate `page`/`size`/`total`** (fetch, then slice). [?] Size limits and timeouts on large folders: H5. Keeping a result cache between page calls needs Chift's agreement (C14).
- **Filters [F]:** strings use "contains" unless the reference says otherwise (`VatNumber`/`Iban` use "equals", account `SearchKeys` "starts with"); all filters must match; null filters are ignored [Guide: Making requests; Horus companies.list, accounts.list]. `ModifiedAfter`/`ModifiedBefore` exist on **three lists in the reference** (companies, book-entries, account-histories), although the guide says "many". ⚠️ "contains" means an exact-match lookup (e.g. by search key) must be post-filtered by the connector [D].
  > Coaching: when I cite a convention, I cite the reference, not the guide's summary: the guide says "many lists", the reference shows three.
- **Updates [F]:** master data uses partial updates (null = keep, "" = erase). **Invoice and operation updates are full replacements and return a *new* book entry Id**, which deletes the original attachment [Guides: Making requests, Posting…].
- **Errors [F]:** `{ErrorType, Details, Message}` with 400/401/403/404/500. Retry advice: 401 → refresh once; 400 → don't retry; 500 → back off [Guide: Responses & errors]. Exception for creates: never retry blindly (see §5.1).
- **Auth [F]:** OAuth 2 authorisation code via `my-horus.com`. The user selects a license; `grant_type=auth_code` (non-standard!); the code is valid for 2 minutes; the access token for 1 hour; **refresh tokens are single-use**, so serialise refreshes per connection [Guides: Authorization flow, Token lifecycle]. Refresh tokens "remain valid until the user revokes them or uninstalls your integration" [F, Guide: Token lifecycle].
  - **Security trap (our reasoning, not in the docs) [D]:** `api_url` comes back via the browser, so validate it (https + Horus host pattern) before POSTing `client_secret` to it. Ask Horus for the pattern (H24). If Chift's security people ask: the state check protects the session, not the host.
- **Versioning [F]:** backwards-compatible changes (new endpoints, optional params, response properties) happen without notice. Breaking changes are announced by email [Guide: Changes & versioning]. So the connector must ignore unknown properties.
- **Testing [F]:** "Requests run against the license's real database. Use a test license or a test folder for write operations" [Guide: Testing the API]. [?] No sandbox is documented (H17, tier 1).

---

## 5. Task A, route by route: the reasoning to understand and defend

Each route below gives: the mapping in one sentence, the call pattern, why it needs several calls (the case's hint), the trap to know, and why the verdict is what it is. Full endpoint tables, call sequences and limitations are in the HTML report (section 4, route cards); what clients notice is in section 6.

**Final verdicts:** ✅ Supported: Get folders. 🟡 Supported with workaround: the other 10 (analytic plans included, Low complexity). 🔴 Not supported: none. (The report computes these counts from the data; never hard-code them in prose.)

**Verdict calibration (D11), the rule to state when presenting:**
- *Supported* = native endpoint(s), deterministic mapping and cached reference lookups only: no extra live calls per request, no emulated filtering, paging or numbering, no lost capability clients rely on.
- *Workaround* = feasible, but needs extra live calls per request (read-backs, joins, loops), emulated filters/paging/numbering, or loses a capability; works for the documented scope.
- Our own safeguards (duplicate pre-checks, an optional read-back for confirmation) are **not** reasons for a verdict; Horus constraints are.

**Ratings per route (as in the report's overview table):**

| Route | Verdict | Complexity | Client impact | Waits on (tier 1) |
|---|---|---|---|---|
| Accounting folders | ✅ | Low | Minor: folder country not returned by default | none |
| Analytic plans | 🟡 | Low | Minor: free dimensions hidden | none |
| Journals | 🟡 | Low | Minor: next document numbers not provided by default | none |
| Analytic accounts | 🟡 | Low | Minor: no balances | none |
| Client creation | 🟡 | Medium | Visible: one address, no person fields, every partner a company | none |
| Ledger account creation | 🟡 | Medium | Visible: account type cannot be written | none |
| Chart of accounts | 🟡 | Medium | Minor: type derived on read, VAT and cash filters best effort | none |
| Miscellaneous operation | 🟡 | Medium | Visible: numeric numbers, foreign currency converted to euro | C1, C15 |
| Invoice creation | 🟡 | **High**: VAT catalogue per legislation and direction, numbering, posting mode | Visible: numeric numbers, accountant review, no delete | H1, H3, C1, C7 |
| Invoice retrieval | 🟡 | **High**: rebuild from the ledger, credit-note classification | Visible: ids change after edits, no line quantities, foreign currency partly in euro | H2, H4, H5 |
| Outstanding items | 🟡 | **High**: supplier open amounts and matching, double-count guards | Visible: supplier items in euro, one due date per item | H8, H5 |

> **The single most important message:** for most routes the core Horus capability *is* native. The "workaround" sits in the translation layer around it: read-backs, ID resolution, VAT codes, analytics conversion and pagination emulation. The complexity column is where the routes really differ.

### 5.1 Client creation → `POST /companies.new` (🟡, Medium)
- **One sentence:** a Chift client = a Horus **company** (third party) with `IsCustomer=true`, created in the folder. [F]
- **Call pattern:** duplicate checks (`companies.list` by VAT / external reference) and a free-key check on the generated search key → `companies.new` → read-back (`companies.info` + `ibans.list` + an account lookup unless the chart is cached), so about 3–7 calls in total, of which the read-back is two to three [D] (LD10).
- **Why several calls:** `companies.new` returns only `{Id}` [F, Guide: Responses & errors], but Chift's `ClientItemOut` needs `last_updated_on`, `third_party_account`, `bank_accounts[]` and `account_number`.
- **Traps:**
  - Horus requires `SearchKey`, `IsCustomer`, `IsSupplier`, `IsVatLiable`, `LanguageCode` and `CountryCode`, and Chift doesn't send a search key. The connector generates it from the name (proposal, D10, C8; unique *within the folder* [F, Guide: Data model]; length and charset rules undocumented [?, H7]).
  - Duplicate VAT numbers are refused by default (`AllowDuplicateVatNumber`) [F].
  - **No vat and no external_reference = no duplicate protection** [D]: a resend creates ACME2. D10 (partner_info) is different on purpose: there the key is the consumer's own code, so a match means reuse. Never sanitise that code before the lookup.
  - One flat address only [D]: Chift's delivery and invoice addresses are dropped (which one is kept: C3).
  - Read and write names differ (`PhoneNumber` on write vs `ContactPhone` on read) → always build the response from the read-back.
- **force_merge makes sense here:** one Horus company can be both customer and supplier, so merging = `companies.update {IsCustomer:true}` on the existing supplier (never send `""`, which erases values [F, Guide: Making requests]).
  - **Single-slot trap [D]:** one ExternalReference, one address, one VAT number per company. Proposal (C6): add IsCustomer + customer-only fields (don't forget `CustomerActivitySuspended` for active=false), fill only empty fields, never overwrite the supplier's ExternalReference (warn; the merged client is found by id), never write VAT on merge until Horus answers (`companies.update` has no `AllowDuplicateVatNumber` [F]).
- **Reliability:** no idempotency key → on a 500 or timeout, *search before retrying* (overrides Horus's generic "retry with backoff" advice). **Best effort only**, with three holes: no key (a client without vat/external_reference: only the generated search key is left), concurrency (two identical calls can both pass the pre-check, hence a connector lock), and undocumented late commits and list visibility (H3). **Exception:** no business key means no automatic retry; return "outcome unknown". Chift's own spec recommends invoice_number for idempotency [F, Chift], so use that in the meeting.
- **Why workaround:** read-back, a generated key, and lost fields (mobile, notes, currency, person fields, extra addresses).

### 5.2 Invoice retrieval (multi plans) → rebuilt from the ledger (🟡, High)
- **One sentence:** Horus has **no general "list invoices" endpoint** [D: no general list among the 72; `invoices.sales.outstanding.list` lists only open sales items]. Pushed invoices "are converted into book entries" [F, Guide: Posting…], so the connector rebuilds each invoice.
- **Call pattern** for a typical request (customer invoices, one quarter, with lines, partner and payments): `book-entries.list` ×2 (one per daybook of types 200 + 250, partner sideloaded) + `account-histories.list` ×1 (lines, VAT, analytics, matching) + `invoices.sales.outstanding.list` ×1 (payment status, invoice-currency amounts, type check) + `account-histories.list` ×1 (payment lines) = **about 5 calls**, plus cached reference data. In general: sales D + 2 (D + 3 with payments), purchases D + 1 (D + 2), with D = number of daybooks of the two sibling types. [D]
- **Why several calls:** each part of a Chift invoice lives in a different Horus resource. This is the clearest example of the case's hint.
- **Traps:**
  - **Credit notes vs invoices on read.** Horus shows the document type only on open sales items. Proposed rule (revised after review): the **daybook type decides** (250/150 = credit note, 200/100 = invoice); the partner-line sign only in folders without a credit-note daybook, which is exactly where our create fallback writes refunds into 200/100 [A, D1]. TransactionType is a **check, not an override** [D]: otherwise a sales invoice would move from customer_invoice to customer_refund once paid. Why not sign first: Chift's own due-date convention allows negative customer invoices [F, Chift InvoiceItemDueDatesOut.amount]. Weak spot to admit: an accountant's credit note keyed into a sales daybook when a credit-note daybook exists comes back as a negative invoice (H2, C5).
  - Periods are months [F], so day-level `date_from/to` is post-filtered.
  - No pagination [D], so the whole window is fetched each time. Default window when no dates are given: proposal, the current fiscal year (C11).
  - **Incremental sync is not cheap [D]:** ModifiedAfter narrows results inside a month window, it does not remove the window. Pass it on headers and lines, complete the few incomplete entries, and plan a periodic full re-sync (deletions and replaced ids are invisible; payments maybe, H10). The payment lookup reads whole collective accounts (`CompanyId` takes one id [F, Horus account-histories.list]), so cache partner-account lines per folder. Coaching: this is the bridge to Part 2; don't call it "native".
  - An edit creates a **new id** [F for API updates; edits in Horus Office: H10]: reconcile on daybook + number, which needs a number (C7).
  - Lines have no quantity or unit price [D]: on read, quantity 1 and unit price = line amount.
  - **Foreign currency on read [A, D4]:** original-currency amounts exist only while a sales invoice is open (from the open-sales list); once paid, the invoice switches to EUR, and purchases always come back in EUR, labelled EUR (never EUR amounts with a foreign code). Offer Chift one stable EUR view until H4 is answered (C16, my preference). Coaching: if asked whether multi-currency works, say posting works when the folder allows it, and that amount and rate semantics and the rate date are H4.
  - **Filters Horus can't honour [D]:** approval_status → "unknown" unless Chift accepts Verified = approved, and never Verified=false = pending; an unknown journal_id → refresh the daybook cache once, then 400. Coaching: the rule is "never return silently narrowed results"; ask Chift what other connectors do (C18).
- **Sideloading:** `Include=CompanyDetail.Company` on `book-entries.list` returns partners in the same call [F, Guide: Sideloading]. This is a good detail to mention.
- **`book-entries.info`** reads one entry by id (header only, no sideloading). It's useful for single-invoice reads and attachments, but not for the list path.

### 5.3 Invoice creation (multi plans) → `invoices.sales.new` / `invoices.purchases.new` (🟡, High)
- **One sentence:** customer_* → sales endpoint, supplier_* → purchases endpoint; `Type` 0 = invoice, 1 = credit note; the PDF is sent in the same call (multipart). [F]
- **Call pattern:** resolve the folder, daybook, partner, account search keys and cost sections (cached) → closure check (`fiscal-years.list`, read fresh) → duplicate check on the document number → create → read back with `book-entries.info` (by default). [D]
- **Biggest trap, VAT:** Chift's `tax_code` is "the Id of the Tax Code" [F, Chift], but Horus has **no VAT-code list and no VAT code on write**. Each line carries `TaxRate + TaxOrigin + TaxType` (+ `TaxKind`, `TaxCondition`, `TaxConditionValue` for purchases), and "only some combinations are valid" [F, Guide: Posting…], listed in two Horus spreadsheets per legislation (BE/LU) and direction [F, Tax files]: sales 18 BE / 58 LU rows, purchases 109 BE / 146 LU rows. So the catalogue is **per folder**. → The connector owns a **synthetic VAT catalogue** with one id grammar (`S-21-0-0`; `P-21-2-0-0-1-true`; OSS rows add the country) built from the files (D2) [A, proposal; C2]. It validates against the folder's list, never against the reference enums (they lack the LU codes). On read, a code is returned only when exactly one row matches (purchase `TaxKind` can't be read back → null).
  > Coaching: if asked whether I opened the spreadsheets: yes, they were fetched on 13 Oct after the first draft. The BE sales list uses the reference codes 0–14 with the same labels; the LU codes do not match the reference, which is H1. That is a real discrepancy found by opening them. Do not call `VatCode` an internal code: its meaning is undocumented.
- **Second trap, analytics:** Chift sends % per plan; Horus wants **amounts on combinations of cost sections** [F]. Convert with a product of the percentages and largest-remainder rounding (D8). Show the worked example in the report (1,000 → 500 SALES/ALPHA + 500 SUPPORT/ALPHA). The independent-plans assumption is question C9.
- **Other traps:**
  - **Numbering.** `Number` is numeric and required on sales (0 allowed only while unconfirmed) [F]; purchases accept null (or 0 while unconfirmed) [F]. Invoices have no AutoGenerateNumber, unlike miscellaneous, bank and financial operations [D: the flag is documented only on those bodies]. Don't defend max(DocumentNo)+1 as the plan: it is a connector-invented number with a race risk. **Proposed default (D12, Chift decides via C7):** an invoice without invoice_number is pushed unconfirmed with Number 0 and returned as `draft`. In review mode that is the Horus default anyway; in direct mode it is a downgrade, and the response reports the real status. Alternatives for C7: reject with 422, or max+1 as an opt-in only after H3 (race, clash with the accountant's numbering). What Horus does with a *confirmed* invoice without a number is unknown [A, H3]. **Non-numeric numbers:** reject, and defend it with Chift's own spec: invoice_number "does not necessarily match the number displayed on an invoice" [F, Chift], and `reference` is free-form. **Supplier invoices without a number:** check supplier + date + total before creating, because `reference` sits in the Comment and cannot be filtered on [D]. Same logic for operations (§5.8): operation_number is *assumed* to be the entry number; say it, and offer the alternative (Horus numbers confirmed ODs, the client value goes in the line comment) (C7).
  - **Duplicates:** no idempotency key and no invoice delete [D] → duplicate check on the document number (D12). **Exception:** no business key (invoice without number, Horus-numbered operation) means no automatic retry; return "outcome unknown". In review mode a duplicate *operation* can still be deleted (unconfirmed, API-injected [F, Horus book-entries.miscellaneous-operations.delete]); an invoice cannot. Chift's own spec recommends invoice_number for idempotency [F, Chift], so use that in the meeting.
  - **Amounts.** Horus checks `Total = Base + Tax` and that the line sums match [F]; that is its only documented consistency check [D]. By default it recalculates line tax (base × rate) and adapts it within 1 cent [F, Horus invoices.sales.new]. Our amount policy (D16) adds three proposals [A, proposal "VAT amounts as issued"; Chift confirms via C2 and C19, Horus via H22]: `OverrideTaxAmounts=true` so the issued invoice's VAT is booked exactly, with an optional check of tax against base × rate (tolerance per C19); invoice_correction only within a rounding tolerance, otherwise 422 for header/line differences; refunds as positive documents. `AllowUnbalanced` stays false.
    > Coaching, if Chift asks "why not let Horus recompute VAT?": the books must equal the invoice the customer received, Horus only adapts within 1 cent, and regroup_lines (on by default [F, Chift]) needs it: 20 lines of 0.15 at 21 % give 0.60 of line VAT against 0.63 recomputed on the regrouped 3.00 [BG arithmetic]. A tolerance check is an option, not the default.
  - **Signs [A, H2/C5]:** the whole document decides (a refund with negative totals is multiplied by −1 as a whole); never abs() a single line; documents with negative discount or deposit lines (mixed signs) and invoices with a negative total are rejected until Horus and Chift confirm otherwise; the rounding-correction line follows the same rule. Coaching: if asked about discounts, say a silent abs() would turn a discount into a charge, so I prefer a clear 422 until H2 is answered.
  - **Posting status.** API entries are **unconfirmed by default** "which lets the accountant review them" [F, Guide: Data model]. Confirmed = validated by the accountant, which is not the same as Chift "posted" (finalised). So we propose a per-connection mode: **review** (push unconfirmed, default) or **direct** (confirm "posted"); mapping "posted" to `Confirmed=true` is offered only in direct mode, and we never claim "posted" for an unconfirmed entry (D12, C1). Whether every user or licence may confirm through the API is H21. In review mode the numbering problem disappears (Number 0 is allowed).
  - **partner_info (D10) [A, proposal; C8]:** Chift's fallback for tools that *cannot* create partners (their example: Tiime [F, Chift]). Horus can, so recommend create-first. If supported: look the code up as sent, by ExternalReference (raw value), then by exact SearchKey; reject codes that need sanitising (422); reuse only if the name matches account_name (else 409 with the existing id); never reuse silently; never flip role flags silently (422 or Chift opt-in); on creation, store the raw value in ExternalReference. Coaching: the risk to name is booking an invoice to the wrong third party, which is the worst outcome for an accountant and cannot be undone through the API.
  - **Period inputs [D]:** force_financial_period and a delivery_date in another month follow one rule: reject, or accept with the limitation that VAT follows the invoice date (C3). Coaching: Chift says delivery_date sets the tax period, so ignoring it silently while rejecting force_financial_period would look inconsistent. That was the review point.
- **Market scope:** Horus is BE/LU (Legislation enum [F]), so the Dutch G/N split and withholding tax have no counterpart. Present this as market scope, not a connector gap.

### 5.4 Journal retrieval → `daybooks.list` (🟡, Low) and 5.5 Folders → `folders.list` (✅, Low)
- **Journals:** `daybooks.list` gives id, code (`SearchKey`), name (`Heading`), type, IBAN and currency [F].
  - The daybook **type maps cleanly** to Chift `journal_type` (100→supplier_invoice, 150→supplier_refund, 200→customer_invoice, 250→customer_refund, 500/590→financial_operation, 600→miscellaneous_operation) [D, D6]. journal_type describes the daybook, not every entry in it: credit notes may sit in 200/100 daybooks (D1).
  - Workaround because `counterpart_account` needs an account lookup, `next_document_numbers` can only be emulated, and `unallocated_account` doesn't exist [D]. `blocked` has no Horus field either, so the connector derives it from the D6 table: blocked=true for daybook types without a documented posting endpoint (550, 610, 690, 700, 900, 990, 0) [A]. The type table also maps 550 Cash → financial_operation and 610/690/700 → miscellaneous_operation [A].
  - `other_currencies_allowed` = false for 500/590/600 [D: their posting bodies have no currency field]. This is why foreign-currency operations are converted, not rejected (§5.8).
- **The daybook type is the routing key of the whole connector:** "The daybook Type drives which endpoint you use to post entries" [F, Guide: Data model].
- **Folders:** almost 1:1 with `folders.list {Mode: 0}` [F].
  - `Mode` 0 = all folders, 1 = my folders, for an accountant [F].
  - `main_currency` = EUR (a constant; no currency field) [A, D4/H4].
  - **Country not fetched by default;** `folders.info` per folder only if Chift needs it (that would make the route a workaround) (C4).
- **Trap:** a Horus **company** is not a Chift company/folder. Say this early in the presentation.

### 5.6 Ledger account creation → `accounts.new` (🟡, Medium) and 5.7 Chart of accounts → `accounts.list` (🟡, Medium)
- **Create:** `accounts.new` takes only `SearchKey` (= number), `Heading` (= name) and optional fields [F]. **The Chift `type` cannot be written** (no category field) [F]. Pattern: duplicate check → create → read back (one `accounts.info` call). The duplicate check and read-back are safeguards; the verdict comes from the unwritable type.
- **Chart:** `accounts.list`, cached per folder (as Horus recommends [F, Guide: Reading…]).
  - `classes` → a "starts with" search-key prefix [F].
  - The **Chift type is computed**: daybook concentration accounts, IntCategory (only COLLECCUS documented), company concentration accounts, line-level AccountType, income/expense categories, then a Belgian number-prefix fallback (BE folders only) [A]. Balance-sheet categories give *no conclusion*, so VAT (411/451), payable (440) and cash (57) can still be reached; for type=vat/cash I also read the line-level AccountType once per folder [D].
  - The type filter and pagination are emulated; type=vat/cash are best effort (how an inexact filter is reported: C18).
  > Coaching: the first version had an ordering bug (balance-sheet → "other" before the prefix step); say it was found in review and fixed, and that unused VAT/cash accounts stay best effort.
- **Trap:** the number 500 means four different things in Horus enums (daybook Bank, account category, account sub-category, account-history Cash). Always qualify enum values by their field.
- **No delete and no renumbering** of accounts through the API [D], so be careful with writes.

### 5.8 Miscellaneous operation creation → `book-entries.miscellaneous-operations.new` (🟡, Medium)
- **One sentence:** a dedicated endpoint posts a balanced debit/credit operation into a type-600 daybook [F].
- **Transformations:**
  - Chift's signed `amount` (positive = credit) → Horus `Debit`/`Credit` columns.
  - Chift line `type` → Horus `Type` 1 customer / 2 supplier / 3 general (CompanyId required for 1/2) [F, Guide: Bank, financial & misc.].
- **Why workaround (and not supported): three Horus constraints, not our own checks:**
  - **No currency field** [F]: amounts are stored in EUR. Non-EUR operations are *converted at the supplied rate*, not rejected; Chift's own contract describes this for journals that don't allow other currencies [F, Chift Journal.other_currencies_allowed: "an exchange rate must be provided for Chift to convert the amounts"; operation currency_exchange_rate "Must be filled in when creating the operation in another currency"]. The original currency is lost [D] (optionally noted in the line comment). Who converts is C15: preferably Chift core before the call; fallback, the connector converts line by line, rounds to 2 decimals and returns 422 if rounding unbalances the entry, unless Chift defines a residue rule. The rate is required when currency ≠ EUR (1, the Chift default, counts as missing).
  - Numbers must be numeric [F] (C7: or let Horus number confirmed ODs).
  - A read-back is needed when Horus generates the number (`AutoGenerateNumber` works only with `Confirmed=true` [F]).
  - Not reasons: the D12 duplicate pre-check (our safeguard) and line_number (Chift uses it only for ordering, and we keep the order).
- **Balance:** Horus refuses unbalanced operations and has no `AllowUnbalanced` here [F] → validate in the connector, on the amounts that will actually be posted (after conversion), and return a clean 422.
- **Unconfirmed operations created through the API can be deleted** [F, Horus book-entries.miscellaneous-operations.delete], confirmed ones cannot: one more reason why review mode is the safer default.

### 5.9 Analytic plans → `cost-schemas.list` (🟡, Low) and 5.10 analytic accounts → `cost-sections.list` per schema (🟡, Low)
- **Vocabulary:** in Horus, "cost" = analytics. A cost schema = a dimension (max **8** per folder); a cost section = a value [F, Guide: Data model].
- **Plans:** one call (8 rows at most), but Chift paging is emulated (Chift's route is paginated [F, Chift], Horus's isn't) and Free schemas are hidden in v1 by choice (C9; `cost-schemas.list` does return them, `900`: Free [F]), so it is supported *with workaround*, Low complexity. parent_id is null if it points to a hidden Free schema.
  > Coaching: if asked why not "supported", say the definitions are applied identically to every route; the effort is trivial.
- **Accounts:**
  - `cost-sections.list` requires `CostSchemaId` [F], so it's one call per schema (≤ 8), then merge and paginate.
  - **Balances are not stored**; they can only be computed from cost histories over a period the Chift route doesn't carry [D] (null or 0: C4).
  - "Free" schemas have no listable values → excluded in v1 (D8).
- **Remember `IncludeInactive=true`**, otherwise inactive sections are hidden by default [F].

### 5.11 Outstanding items → `invoices.sales.outstanding.list` + `customers.outstanding` / `suppliers.outstanding` (🟡, High)
- **Not N+1:** all three endpoints are folder-level, and omitting the `CompanyIds` filter means "no filter" [D, Guide: Making requests: null filters are ignored]. Whether the result then covers every partner, complete and uncapped, is to confirm [A, H8]. Call budget: clients 2 calls, suppliers 1, plus a rare per-item fallback and optional per-entry enrichment (off by default).
- **Asymmetric:**
  - Clients have a native `OpenAmount` per open sales invoice (joined with `customers.outstanding` for the account and matching data).
  - Suppliers only have open ledger lines: open amount = **line amount for unmatched lines** [D, guide definition]; netted per matching group (D5 signs, residual allocated oldest due date first) **only if Horus returns partially matched lines** [A, H8]. Fallback: `account-histories.list` on the supplier concentration accounts, the documented way to read unmatched lines (`NotMatchedOnly`) [F, Guide: Reading accounting data]; if Horus says partially matched lines are left out, the "ALT-R2" variant in the data drops `NotMatchedOnly` and keeps lines with no MatchNo or MatchStatus 0 [A]. Signs per D5 (positive = owed).
  > Coaching: if asked how I know the netting works: I don't yet. The unmatched case is documented, partial matches are H8, and there is a documented fallback. Either answer matters: if partial matches are not returned, partially paid supplier invoices disappear, hence the fallback, the supplier control total (vs Horus SumDebit/SumCredit, H23) and, on the client side, a detector that logs open sales rows with PaymentStatus 10 (partially paid) whose line is missing. Do not call the AccountType filter defensive: we log, never drop.
  > Be ready for "why is our credit note negative here and positive in get invoices?": balance view (positive = owed, additive per partner) vs Chift's document view on due_dates [F, Chift InvoiceItemDueDatesOut.amount]. We propose the balance view and ask (C5). Oldest-first allocation of partial residuals is our proposal; pro-rata is the alternative, and partner totals don't change.
- **Traps:**
  - A payment appears both inside its invoice (`LinkedElements`) and as its own row, so de-duplicate: drop only top-level rows with OpenAmount null whose id appears in another row's LinkedElements.
  - **Client-side double counts:** (1) an entry with several partner lines, (2) a carried-forward line next to its prior-year original. Guard: never re-emit a line whose BookEntry.Id is already on a kept sales-list row, plus the IsReport pairing rule. Chift's `original_document` field shows they expect one item per carried-forward document [D].
  - **Sign trap:** the sales-list examples show an invoice +1210 and a payment −210, never a credit note [F, Horus invoices.sales.outstanding.list]. We now sign from TransactionType (0 +, 1 −) and keep payments raw (a refund to a customer has the opposite sign). If Chift asks why invoice retrieval and outstanding items used to differ: they did, and now they don't.
  - Single due date per line (one item per customer/supplier line; granularity is C17).
  - `original_document` for items carried over from the previous year is uncertain [A, H8].
  - Foreign currency (D4): supplier items are returned in EUR; a customer's items can mix currencies (open sales invoices in their own currency, the other lines in EUR), so clients total per currency (C16).
- **unposted_allowed** maps to Horus `Confirmed` (validated by the accountant). In **review mode** (the proposed default, D12), everything Chift pushes stays invisible with `unposted_allowed=false` until the accountant confirms it; in direct mode, "posted" entries are visible at once. Explain this to clients. Rule to propose: with false, unposted payments do not reduce open amounts, on both sides (C10).

---

## 6. Task B: how to read and defend the attribute tables

The full tables are in the HTML report, section 5: 83 rows for client creation, 112 for invoice creation and 39 for outstanding items. Every Chift attribute and query parameter is covered (the final review checked this programmatically against the Chift schemas). Each row has a Horus source, a mapping type, a rule, a basis label and evidence. Section 6 of the report translates the "Not available" and Assumption rows into plain client language.

**Five things to be able to explain:**
1. **The mapping types** (Direct, Transform, Lookup, Composite, Constant, Not available, Chift-side). They show at a glance where the effort is: Transform/Lookup/Composite rows are connector logic, and Not available rows are disclosed data loss.
2. **"Horus fields with no Chift source"**, a separate table per route. *This is the most overlooked part of a mapping*: the target's required fields that the source doesn't provide. Examples: `SearchKey`, `IsVatLiable` and `LanguageCode` on companies; `TaxOrigin` and `TaxType` on invoice lines; `CostLines[].Amount`.
3. **Request vs response:** the response is built from a read-back for what Horus stores, because Horus normalises values and names differ on read. Values Horus cannot return (invoice-currency amounts under D4, quantity, unit price, exact analytic percentages) are echoed, each with a round-trip note; echo vs later-read is C4. Exception: if the read-back fails after a successful create, return the id plus the request values for the fields Horus stores (mapped as on read, D9), never the raw request echo; never an error (D13).
4. **Query parameters:** e.g. `force_merge`, `regroup_lines` (Chift-side pre-processing), `ignore_accounting_id` (skip the read-back), `force_financial_period` (no forced period on creation in Horus: reject, or accept with the limitation, same rule as delivery_date, C3), `unposted_allowed` (→ `Confirmed`).
5. **The basis label is the weakest part of the rule.** If a row maps to a documented Horus field but our rule contains a proposal (sign, posting mode, VAT override), it is labelled Assumption, with (documented) inline for the factual part. If Chift points to a row and asks "where is that documented?", the answer must be in the row.

**Field-level decisions worth quoting:**

| Chift | Horus | Why it is interesting |
|---|---|---|
| client `account_number` | `CustomerConcentrationAccount` (search key on write, `{Type, Id}` on read) | Horus uses shared control accounts (400000) plus the company as sub-ledger; `third_party_account` = company `SearchKey` |
| client `language` | `LanguageCode` (FR/NL/DE/EN/ES/PT), else the folder language | Required in Horus, optional in Chift |
| invoice `invoice_type` | endpoint (sales/purchases) + `Type` (0/1) + daybook type | One Chift field drives three Horus choices |
| invoice `lines[].tax_code` | `TaxRate` + `TaxOrigin` + `TaxType` (+ purchase fields) | Synthetic VAT catalogue per folder legislation and direction, built from the Horus spreadsheets (D2, C2) |
| invoice `analytic_distribution` | `CostLines[{Amount, Costs[{SchemaSearchKey, Value}]}]` | % per plan → amounts on combinations |
| invoice `reference` + `customer_memo` | one `Comment` (`{reference} \| {memo}`) | Single free-text field (D3) |
| invoice `status` | `Confirmed` | Proposal: per-connection posting mode, review by default (D12, C1) |
| outstanding `open_amount` | `OpenAmount` (clients) / line amount of unmatched lines, group residual only for partial matches (suppliers) | Asymmetric sources (H8) |

---

## 7. How the analysis was checked, and what the review changed

What I did (worth describing, since they assess *how you approach* an unfamiliar API):
1. Read both contracts myself and spot-checked the key endpoints.
2. Each route group was mapped, then **challenged by two independent reviews**: an *evidence* review (try to refute every cited endpoint, field and enum) and a *completeness* review (missing attributes, endpoints, required fields, edge cases).
3. A reconciliation re-checked every challenge against the docs. About 175 corrections were applied; dozens of findings were rejected with reasons.
4. A **final cross-route review** found 5 major inconsistencies *between* routes. Each route was locally correct, but the routes didn't fit together.
5. A **senior BA review** then read the whole solution as Chift would: 63 issues (3 critical: the verdict scale, the VAT files, foreign-currency operations). All were applied; the top ten are at the top of these notes, the full list is in `03_critical_review_register.md`.

**The 5 major cross-route findings (great material for "what would you do differently / what did you learn"):**

| # | Problem | Decision |
|---|---|---|
| D1 | A credit note created in a sales daybook (fallback) would read back as an invoice | Read both daybook types; the daybook type decides, the sign only where no credit-note daybook exists (revised after the final review) |
| D2 | Three different VAT-code id formats across routes; the purchase `TaxKind` can't be read back | One id grammar, built per folder legislation and direction from the Horus tax files; return null on ambiguous reads |
| D3 | `reference` written into the comment, read back into different fields | One `{reference} \| {memo}` convention, split on read |
| D4 | Foreign-currency amounts: EUR numbers paired with USD labels | One assumption (ledger in EUR); never mix; operations converted at the supplied rate |
| D5 | Customer open items computed with the supplier sign | Sign by side |

Minor decisions: D6 (one daybook-type table), D7 (one folder rule, now enforced on every route), D8 (one analytics cache and rounding rule), D9 (one partner mapper), D10 (partner_info: exact code + name match), D11 (verdict calibration, which downgraded miscellaneous operations and, after review, analytic plans), D12 (posting mode, review by default; numbering; best-effort duplicate checks), D13 (folder check on calls by id; a failed read-back never errors), and **D16** (new: invoice amounts, VAT as issued, correction tolerance, refund sign). D14 (invoice daybook selection reworded to the D1 per-type filter) and D15 (endpoint count corrected to 72 once `book-entries.info` was supplied) are internal clean-ups, so the report's appendix B lists D1–D13 and D16, and presents them as *working assumptions* with the open question each depends on.

> **Lesson to say out loud:** a connector is a *system* of routes that must round-trip. What a create route writes must be readable by the get route in the same shape. Reviewing routes in isolation misses this.
>
> **Second lesson (from the senior review):** apply a scale mechanically, with no exceptions, and re-check every "not available" claim: the tax-combination files were linked from the reference pages, and opening them changed the VAT design and raised H1.

---

## 8. What to communicate to Chift, and what to clarify

**Lead with:**
1. No route is blocked by a missing Horus capability in the documentation reviewed. One route is native (folders) and ten need workarounds. Complexity is low, medium or high per route, and four routes wait on priority-1 answers (invoice creation, invoice retrieval, outstanding items, miscellaneous operations). Volumes: fine for typical folders, unverified for large ones (H5).
2. The shape of the work: a translation layer (read-backs, invoice reconstruction, VAT catalogue from the Horus files, analytics conversion, pagination emulation, best-effort duplicate protection), built as shared components.
3. Disclosed limitations, in client language: walk through section 6 of the report (ids change after edits, numeric numbers, no delete, one address and every partner a company, review-pending entries, no line quantities, foreign-currency invoices read back in euro, operations stored in euro and converted at the supplied rate with the original currency lost, no writable account type, analytic balances only computable over a period).
   > Coaching: never say "EUR-only" for operations again. Chift's own `Journal.other_currencies_allowed` text says a rate must be provided "for Chift to convert the amounts". Our Get journals returns false for Type 600, so conversion is the consistent answer. Ask them whether Chift core converts before calling connectors (C15).
   > Coaching: ask Chift how they publish connector limitations, and offer to adapt section 6 to that format.
4. The recommendation: **go, conditional on a short gate** (Gate 0, then three phases; see §9 "What would you do next?"), and the tier-1 questions of section 9, for Horus and for Chift. Always phrase it as a proposal, never as a commitment by Chift or Horus.

**Tier-1 questions for Horus (before build; ids are stable across the report and the data):**
- **H1, confirm the tax-combination files:** current and complete, how changes are announced, LU code discrepancies (which origin list is authoritative), the combination for non-VAT-liable folders, how an invalid combination is rejected, and the meaning of VatCode. They define the VAT catalogue.
  > Coaching: if asked why I didn't open them earlier: they're opened now, and they raised a real discrepancy.
- **H2, credit notes vs daybooks:** decides write selection and read classification; can Type be exposed on read?
- **H3, numbering and idempotency:** uniqueness, late commits after a timeout, what Horus does with a confirmed invoice without a number.
- **H4, currency of ledger amounts and the `CurrencyRate` direction:** correctness of every foreign-currency read.
- **H5, rate limits, result sizes and timeouts:** with no pagination, large folders are the performance risk.
- **H8, outstanding items:** every partner without a filter, and partially matched lines.
- **H17, test license or test folder:** the API works on live data.
- **H19, integration registration** and which Horus user should authorise (firm vs SMB).
- **H20, documentation version:** is docs.horus-software.be authoritative, and is the apiary version the case links deprecated?
- **H21, confirmation rights:** may every licence and user set `Confirmed=true` through the API?
- **H24, OAuth lifecycle:** api_url host pattern, repeated grants, departing users, lost refresh responses.
- (H6, the ErrorType catalogue, is now tier 3: we can verify it in the test folder.)

**Tier-1 decisions for Chift:** **C1** (posting mode: review by default, direct as an option), **C7** (numbering: invoices without a number, non-numeric numbers, operation_number meaning), **C14** (caching between page calls and request timeouts), **C15** (who converts foreign-currency operations, and the rate direction). Then the one tier-2 question to raise in the room: **C17** (outstanding-items scope: one item per instalment or per line, unallocated payments, matching-number prefixes, beneficiaries). Other tier-2 conventions (C2 VAT catalogue, C3 reject vs drop, C5 signs, C6 duplicates, C8 partner_info…) can go in a follow-up.

---

## 9. Likely follow-up questions, with prepared answers

| Question | Answer (and basis) |
|---|---|
| "How did you approach an API you'd never seen?" | Contract first (Chift's inputs/outputs), then Horus's conventions (auth, folder scoping, envelope, pagination), then a 72-endpoint inventory → mapping → verdict → limitations. The same 7 questions per route, every claim labelled documented / derived / assumption / to confirm, and a senior review that challenged the result before the meeting. |
| "Why do some routes need several Horus calls?" | Horus is a ledger with an RPC API. Creates return only an id (so a read-back), invoices exist only as book entries + lines (so a rebuild), and posting references search keys (so lookups). Example: invoice retrieval ≈ 5 calls. [F/D] |
| "What's the hardest part?" | The three High-complexity routes: invoice creation (VAT catalogue per legislation from the Horus files, and numbering), invoice retrieval (rebuild from the ledger and credit-note classification), and outstanding items (supplier open amounts when lines are partially matched, H8). |
| "Why is analytic plans a workaround if it's one call?" | Strict scale: Chift's route is paginated and Horus isn't, so paging is emulated (trivially, 8 rows at most), and Free dimensions are hidden by choice (C9). Low complexity, but not native. |
| "Is there a sandbox?" | Not documented: "Requests run against the license's real database. Use a test license or a test folder" [F]. Ask Horus for one (H17, tier 1; no build without it). |
| "How does authentication work for Chift's multi-tenant setup?" | OAuth 2 code flow via my-horus.com; the user picks the license; each license has its own `api_url`; non-standard `grant_type=auth_code`; 1-hour access tokens; **single-use refresh tokens**, so serialise refreshes per connection. [F] Caveats to know: one connection = one grant by one user for one license (the 1:1 consumer = license rule is our deduction); repeated grants and a departing accountant are undocumented (H24); only a definitive token-endpoint rejection disconnects, transient errors are retried; offboarding = delete tokens, the user uninstalls in Horus (no revoke endpoint among the 72 [D]; tokens stay valid "until the user revokes them or uninstalls your integration" [F, Guide: Token lifecycle]). |
| "Pagination?" | None on any list (a deduction: no paging parameter in the reference), so Chift emulates page/size/total. Mitigate with per-folder caching, `ModifiedAfter` incremental sync (only on companies, book entries and account histories) and gzip. Rate limits undocumented (H5). It depends on Chift letting the connector cache between page calls (C14); a volume test on the largest test folder ends phase 1. Careful with incremental sync: ModifiedAfter filters headers, but lines are period-bound, so a poll costs as much as its look-back window (C11). We pass ModifiedAfter on lines too, complete incomplete entries per id, and add a 5-minute overlap. [D] |
| "What if a field doesn't exist in Horus?" | Classify it as Not available, return null (or Chift's agreed default, C4) on read, and on write either reject it with 422 or drop it and log it: Chift's response has no warnings field (decision C3). It's always listed in the attribute table and, if clients notice it, in section 6. |
| "Why is miscellaneous operation not 'supported'? It has a dedicated endpoint." | Three Horus constraints, not our own checks: no currency field (stored in EUR, foreign currency converted, original currency lost), numeric numbers only, and a read-back to return a Horus-generated number. The core endpoint is native. Coaching: if they say "drop the duplicate check and it's supported", agree that the check is a safeguard and point to the three constraints; never cite line_number as a loss. |
| "What if a client posts an invoice without a number?" | Chift's contract says it is generated "according to the system's numbering rules" [F, Chift]; Horus has no automatic numbering for invoices [D]. In review mode it arrives as a draft without a number, which is the Horus default anyway. In direct mode I'd do the same downgrade and report the real status, and offer max+1 only as an opt-in, because a wrong confirmed number can't be deleted. Chift decides (C7). |
| "Can you post a payment matched to its invoice?" | Yes, outside this scope: `book-entries.banks.new` plus `matching` (or `MatchNo` at creation, with `matching.next-number.*`) [F, Guide: Outstanding items & matching]. A good bridge to part 2 (synchronisations). |
| "What happens when the accountant edits an invoice we pushed?" | Horus generates a new book entry id when an invoice is updated [F, Guide: Reading accounting data]. Documented for updates; whether an edit made in Horus Office also changes the id is asked in H10. The connector reconciles on daybook + number, as Horus advises [F]. For API updates the original attachment is also deleted [F, Guide: Posting…]; whether an edit in Horus Office keeps it is not documented [?]. Caveat: reconciliation on daybook + number needs a number. Drafts pushed without one (number 0), which our review default produces, cannot be found again after an edit, so we ask consumers to always send a number and propose that Chift decide whether to require or assign one (C7). Whether confirmation itself changes the id is unknown (H10). |
| "Should entries be confirmed?" | No by default. Horus leaves API entries unconfirmed so the accountant can review them, invoices can't be deleted through the API, and "confirmed" means accountant-validated, which is not the same as Chift "posted". I propose a per-connection posting mode chosen at activation, review by default and direct as an option, and the response always reports what was stored. Chift decides (C1); who may confirm through the API is a Horus question (H21). Coaching: do not defend "posted → confirmed is semantically correct"; that was the old wording. |
| "Can a consumer read a folder it didn't select?" | Not through our connector: one Horus token sees every folder of the firm, so every route rejects a non-selected folder_id before calling Horus (D7), unless Chift's platform already does it (C12). Before the review only client creation checked this. |
| "What if Horus creates the entry but your read-back fails?" | We return success with the id and the values we sent for the fields Horus stores (mapped as on read, D9), never the raw request echo, and repair the read-back later. Erroring would invite a retry, and Horus can't delete invoices or confirmed operations. Same rule on every write route (D13). |
| "Can you guarantee no duplicate invoices?" | No connector can on Horus: there is no idempotency key. We pre-check on the number, never retry blindly, lock identical calls and refuse to auto-retry keyless creates. Ask consumers to always send invoice_number, as Chift's own contract recommends. |
| "How confident are you?" | Desk analysis, no live calls. Horus side rests on the current docs (Sept 2026), not the apiary pages the case links (H20); Chift side on the SDK-bundled spec, spot-checked before the meeting. Chift side: high (official spec; re-check against the live docs). Horus side: high on what's documented (API reference, 15 guides and the tax-combination files). Every assumption is labelled and has a matching question. |
| "Performance?" | The worst cases are invoice retrieval over long periods and large accounting-firm folders (full lists, no paging). Mitigate with caching, narrow windows, gzip and incremental sync, and ask Horus for limits (H5). It depends on Chift letting the connector cache between page calls (C14); a volume test on the largest test folder ends phase 1. Call budgets: outstanding items 2 calls (clients) / 1 (suppliers) + optional enrichment, off by default; volume test in phase 1, plus read-only on a real folder (with its owner's consent) if the test folder is too small. |
| "What would you do next?" | Gate 0 (registration, test license, Horus confirms the VAT files and its limits, Chift decides posting mode and numbering), then phase 1 reference reads plus client and account creation with a volume test, phase 2 invoice and operation creation, phase 3 the reads rebuilt from the ledger (once H2, H4, H5 and H8 are answered). Descoping triggers: smaller VAT list, mandatory date window, no build without a test license. |
| "Anything wrong in Chift's own docs?" | Two small things: `FolderItem.main_currency` says ISO 3166-1 (country codes; ISO 4217 is meant), and the line `tax_amount` formula omits /100. Mention them tactfully (C13). |

---

## 10. Suggested presentation storyline (15–20 minutes, using the HTML report)

The meeting guide (`02_meeting_prep_guide.md`) has a shorter version; this one follows the report.

1. **Context (1 min):** what Chift does; what a connector is; what Horus is (BE/LU accounting firms and SMBs; one database and API URL per license). → report header and section 3 diagram.
2. **Method and sources (2 min):** the 7 questions, the verdict scale (strict definitions), the basis labels, the review process. Open with the sources: current Horus docs vs the apiary link, SDK spec, no live calls. → section 2.
3. **Concept map (2 min):** folder = folder, *company = third party*, daybook = journal, cost schema/section = analytic plan/account, no VAT-code list or input. → section 3.
4. **Results (4 min):** the overview table, 1 supported / 10 workaround / 0 not supported, plus complexity and client impact per route, and why "workaround" mostly means translation. → section 4 table.
5. **Deep dive (5 min):** pick **invoice creation** (VAT catalogue from the Horus files + analytics worked example) and **invoice retrieval** (rebuild from the ledger: the "multiple endpoints" hint). Open one route card live and use the attribute-table filter (e.g. type "tax"). → sections 4–5 and appendix C.
6. **Risks and decisions (2 min):** edge cases, what clients notice, plus two or three cross-route decisions (credit notes, VAT ids, posting mode). → section 8, section 6 (client impact) and appendix B.
7. **Open questions and next steps (2 min):** the tier-1 questions, the conditional go (Gate 0, three phases, descoping triggers). → sections 9–10.
   > Coaching: if asked which flows matter most, ask Chift rather than asserting it.

**Client-friendly phrasing to reuse:** "Chift speaks one standard language. For Horus we checked each standard request: Horus understands it directly, needs a few extra steps, or can't do it. Here's what works, what works with limits, and what we still need Horus to confirm."

---

## 11. Cheat sheet: facts and numbers

| Fact | Value | Source |
|---|---|---|
| Verdicts | 1 Supported (folders) / 10 workaround / 0 not supported; complexity 4 Low / 4 Medium / 3 High; 4 routes wait on tier-1 answers | analysis (report section 4) |
| Horus endpoints | 72 (incl. `book-entries.info`); 23 GET, 47 POST, 2 DELETE | API reference |
| Horus endpoints called by the 11 routes | 35 (plus 5 used only for connection setup, an optional default-vehicle lookup or a compensation delete; 49 referenced in the mappings) | analysis |
| Task B rows | 83 client creation / 112 invoice creation / 39 outstanding items | analysis (report section 5) |
| Auth | OAuth 2 code; `grant_type=auth_code`; code valid 2 min; access token 1 h; refresh token single-use | Guides: Authorization flow, Token lifecycle |
| Base URL | per license (`api_url` from OAuth); validate the host before sending the secret (proposal, H24) | Guide: Authentication overview |
| Sideloading | `Include` on 4 endpoints | Guide: Sideloading |
| Pagination | none (deduction from absence) | reference + guides (absence) |
| `ModifiedAfter` | 3 lists: companies, book-entries, account-histories (guide says "many") | API reference |
| Ledger periods | month/year | Guide: Reading accounting data |
| Cost schemas per folder | max 8 | Guide: Data model |
| Invoice types | `Type` 0 invoice / 1 credit note | API reference |
| Posting default | API entries unconfirmed by default; no invoice delete endpoint; unconfirmed API-created ODs can be deleted | Guide: Data model; API reference (incl. absence) |
| AutoGenerateNumber | misc, bank and financial operations only, and only with `Confirmed=true` | API reference |
| Tax combinations | sales BE 18 / LU 58 rows; purchases BE 109 / LU 146 rows | Tax files |
| TaxOrigin enums | reference: sales 0–20, purchases 0–39; LU files use up to 35 (sales) and 40–56 (purchases) | API reference; Tax files |
| Daybook types | 100 purchase, 150 purchase CN, 200 sale, 250 sale CN, 500 bank, 550 cash, 590 financial, 600 misc., 610/690/700 other misc., 900 budget, 990 external | API reference |
| Operation line types | 1 customer / 2 supplier / 3 general | Guide: Bank, financial & misc. |
| Matching account types | 100 customer / 200 supplier / 300 general | Guide: Outstanding items & matching |
| Legislations | BE, LU | API reference |
| Errors | `{ErrorType, Details, Message}`; 400/401/403/404/500 | Guide: Responses & errors |
| Call budget, invoice retrieval | sales D + 2 (+1 with payments), purchases D + 1 (+1); ≈ 5 for a typical sales request | analysis |
| Call budget, outstanding items | client 2, supplier 1, + 0–N enrichment (off by default) | analysis |
| Questions | Horus H1–H25, Chift C1–C20; tier 1: H1–H5, H8, H17, H19, H20, H21, H24 and C1, C7, C14, C15 | report section 9 |
| Report structure | 1 summary · 2 scope, sources, method · 3 how Horus works · 4 routes (Task A) · 5 attributes (Task B) · 6 client impact · 7 dependencies · 8 edge cases · 9 questions · 10 conclusion; appendices A endpoints, B working assumptions, C VAT combinations | report |

---

## 12. Files

| File | What it is |
|---|---|
| `chift_horus_mapping_report.html` | **External deliverable** for Chift (self-contained; open in any browser) |
| `01_internal_notes_part1_mapping.md` | These notes (internal) |
| `02_meeting_prep_guide.md` | Meeting guide: opening, concepts, decisions to defend, likely challenges (internal) |
| `03_critical_review_register.md` | Senior-review issue register: 63 issues with evidence, correction and "if Chift raises it" (internal) |
| `data/*.json` | Final harmonised mapping data per route group (what the report is generated from) |
| `decisions.md` | Cross-route decision log D1–D16 (internal wording) |
| `appendix_chift_spec_extract.md` | Chift OpenAPI extract for the case endpoints |
| `appendix_horus_api_reference.md` | Horus API reference (72 endpoints, rendered) |
| `appendix_horus_guides.md` | Horus guides (15 pages, extracted text) |
| `appendix_horus_tax_combinations.md` | Horus tax-combination spreadsheets (sales and purchases, BE and LU), converted to text |
| `report_src/` | Generator for the HTML report (Python, no dependencies) |
