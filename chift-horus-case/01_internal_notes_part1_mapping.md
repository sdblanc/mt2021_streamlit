# Chift × Horus: Part 1 (mapping), internal working notes

> **Internal only. Not for Chift.** These are my study and prep notes. The external deliverable is `chift_horus_mapping_report.html`.
>
> **Status:** Part 1 is complete. Every route is mapped to Horus, checked by independent reviewers against the Horus API reference and guides, and reconciled. Open points are listed explicitly; nothing in these notes fills a gap with guesswork.

**Labels used throughout**

| Label | Meaning |
|---|---|
| **[F]** | Fact, stated in a source (source given) |
| **[D]** | Deduction, my conclusion from facts (reasoning shown) |
| **[A]** | Assumption, plausible but unconfirmed; must be validated |
| **[?]** | Missing or ambiguous in the documentation |
| **[BG]** | General accounting background, to explain a concept. Not a claim about Chift or Horus |

**Source tags:** `[Case]` · `[Chift <operationId>]` (Chift OpenAPI) · `[Horus <endpoint>]` (Horus API reference) · `[Guide: <title>]` (Horus guide pages)

---

## 0. Sources: what I used, and how much to trust it

| Source | How I got it | Status | Trust |
|---|---|---|---|
| Case page "Case Product / Tech" | Notion connector (public chift.notion.site page) | ✅ Read in full | Primary |
| Chift API reference | `docs.chift.eu` is blocked in this environment. I used the **OpenAPI spec bundled in Chift's official Python SDK** (`chift` v0.6.16 on PyPI) | ✅ Read | High. All 11 case URLs match operations in this spec one for one. It's a snapshot, so **spot-check the live docs before presenting** |
| Horus API reference (72 endpoints) | Your Notion export (`horus.zip` on Drive: welcome page + every API Reference page, each embedding an OpenAPI 3.0.3 fragment; docs dated 24 Sep 2026), plus the `book-entries.info` page you supplied separately | ✅ Merged and rendered (`appendix_horus_api_reference.md`) | High |
| Horus guides (15 pages) | Your PDF prints (Drive folder "Horus guides") | ✅ Text-extracted (`appendix_horus_guides.md`) | High. Extraction noise in some tables |
| Not available | Horus Quickstart, Register your integration, Support & FAQ, Changelog; the **tax-combination spreadsheets** linked from the invoice pages; the Postman collection; any webhook documentation | ⛔ | Gaps are flagged where they matter |

**Discrepancies between Horus sources (worth knowing, and worth mentioning to Chift):**
- [F] The guide *Reading accounting data* says "Use `book-entries.info` to get the full detail of one entry". That page was missing from the first export; you supplied it separately. It returns the entry **header only** (lines as references), so "full detail" in the guide overstates it a little. Worth asking Horus whether more detail is planned.
- [F] Line-type codes differ by endpoint: miscellaneous/bank operation lines use `Type` **1** Customer / **2** Supplier / **3** General [Guide: Bank, financial & miscellaneous operations], while matching and account histories use **100** / **200** / **300** [Guide: Outstanding items & matching]. These are easy to mix up in a connector.
- [F] The page text of `customers.outstanding` says "Get **a customer's** outstanding debts", but its `CompanyIds` filter is an optional array. Whether an empty filter returns **all** customers needs confirming.

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
- **Outcome:** a route-level verdict table, field-level mappings for 3 routes, dependencies, limitations, and a separate list of open questions for Horus and for Chift.

## 3. The method (this is what they want to see)
For every Chift route, ask the same 7 questions:
1. **Business meaning:** what object or action is this?
2. **Chift contract:** what is required as input, and what is promised as output?
3. **Capability:** does Horus have the object, and can it be read and/or written?
4. **Endpoint(s):** which Horus calls, and in what order?
5. **Fields:** direct, transformed, looked up, composite, constant, or unavailable?
6. **Behaviour:** filters, pagination, incremental sync, status and numbering: native or emulated?
7. **Risk:** limitations, edge cases, error handling.

**Verdict scale:** ✅ *Supported* (native, 1:1 or a simple transformation) · 🟡 *Supported with workaround* (several calls, emulated filters, or some fields lost) · 🔴 *Not supported* · ⚪ *To confirm*.

**Field codes:** `DIRECT` · `TRANSFORM` (format, enum or sign) · `LOOKUP` (resolve an ID via another call) · `COMPOSITE` (built from several fields or calls) · `CONSTANT` (the connector sets the value) · `NA` (no Horus equivalent) · `CHIFT_INTERNAL` (handled by Chift itself, e.g. pagination emulation).

**How the analysis was done:** I read both contracts myself and spot-checked the key endpoints. Independent analysts then mapped each route group. For every mapping, a separate reviewer tried to *refute* each claim (an evidence check) and another looked for *gaps* (a completeness check). A reconciler re-checked each challenge against the docs, and a final critic checked consistency across routes. This mirrors how I would review a colleague's mapping.

## 4. Domain primer: Chift concepts ↔ Horus concepts

Before any route mapping, align the vocabulary. **The same word can mean different things in the two systems.**

| Chift concept | Horus concept | Key facts and traps |
|---|---|---|
| Consumer / connection | **License** + OAuth connection | [F] "Each license has its own database and its own API endpoint" (`api_url`, returned at the end of the OAuth flow; never hard-code it) [Guide: Authentication overview] |
| **Folder** (legal entity) | **Folder**: "the accounting record of one company" | [F] "Almost every endpoint requires a FolderId" [Guide: Data model]. `folders.list` takes `Mode` 0 = all folders, 1 = my folders |
| Client / supplier | **Company** with `IsCustomer` / `IsSupplier` flags (also beneficiaries) | ⚠️ In Horus, "company" means a *third party*, not the legal entity. One object serves both roles, so Chift's `force_merge` is meaningful [Horus companies.new] |
| Journal | **Daybook** | [F] "The daybook Type drives which endpoint you use to post entries" (100/150 purchases, 200/250 sales, 500 bank, 590 financial, 600 misc.) [Guide: Data model] |
| Ledger account | **Account**, identified by `SearchKey` (usually the account number) | [F] Postings reference accounts **by search key**, not by Id [Guide: Data model] |
| Analytic plan | **Cost schema** (an analytical dimension; up to 8 per folder) | [F] Requires the folder's `WithAnalytics` module [Guide: Data model] |
| Analytic account | **Cost section** (a value within a schema) | Referenced by search key in postings |
| Analytic distribution (% per plan) | **Cost lines**: *amounts* on a combination of schema values, or a predefined **cost distribution key** | ⚠️ Percentages per plan must be converted to amounts on joint combinations [Guide: Posting sales & purchase invoices] |
| Sale/purchase entry ("invoice") | **Book entry** created by `invoices.sales.new` / `invoices.purchases.new` (`Type` 0 = invoice, 1 = credit note) | [F] Create returns only the book entry `Id` [Guide: Responses & errors] |
| Invoice lines | Invoice lines → stored as **account history lines** | [F] "one line per account movement, with debit/credit amounts, VAT information, matching number" [Guide: Data model] |
| VAT code (`tax_code` = an ID) | **No VAT-code entity.** VAT = `TaxRate` + `TaxOrigin` + `TaxType` (+ `TaxKind`, `TaxCondition` for purchases) | ⚠️ "Only some combinations are valid", per external spreadsheets we don't have [Guide: Posting sales & purchase invoices] |
| Miscellaneous operation | Book entry in a misc. daybook via `book-entries.miscellaneous-operations.new` | [F] Debit/credit lines that must balance [Guide: Bank, financial & miscellaneous operations] |
| Bookyear | **Fiscal year** (with closure dates per daybook type) | [F] "Check closure dates before posting" [Guide: Data model] |
| Posted vs draft | `Confirmed` true/false | [F] "Entries pushed through the API are unconfirmed by default", to let the accountant review [Guide: Data model]. ⚠️ Not identical to "posted": Confirmed means *validated by the accountant* |
| Outstanding item | Unmatched account history line, or open sales invoice | [F] "Lines that are not matched yet make up the outstanding items" [Guide: Outstanding items & matching] |
| Matching number | `MatchNo` | Same account type and company required [Guide: Outstanding items & matching] |
| Attachment (PDF) | **Document** (main document + annexes) | Upload as `multipart/form-data` with `file` + `body` [Guide: Documents & attachments] |

### Horus API conventions that shape every route
- **Style [F]:** JSON-RPC-style methods `{api_url}/{category}.{action}`. `GET` with query string for simple reads (`.info`, `.me`). **`POST` for lists with filters**, creation and updates [Guide: Making requests].
- **Envelope [F]:** payload under `Data`. Related entities are references `{Type, Id}`. Create and update return only `{Id}` [Guide: Responses & errors].
- **Sideloading [F]:** an `Include` parameter (dot paths, comma-separated) returns related entities under `Included`, but **only on `book-entries.list`, `account-histories.list`, `companies.list` and `invoices.sales.outstanding.list`** [Guide: Sideloading].
- **Pagination [D]:** no paging parameter exists on any list endpoint in the reference, and the request guide describes none. So Horus lists return the full result, and **Chift must emulate `page`/`size`/`total`** (fetch, then slice). [?] Confirm with Horus whether there are size limits or timeouts on large folders.
- **Filters [F]:** strings use "contains", all filters must match, null filters are ignored. `ModifiedAfter`/`ModifiedBefore` exist on many lists, "ideal for incremental synchronisation" [Guide: Making requests]. ⚠️ "contains" means an exact-match lookup (e.g. by search key) must be post-filtered by the connector [D].
- **Updates [F]:** master data uses partial updates (null = keep, "" = erase). **Invoice and operation updates are full replacements and return a *new* book entry Id**, which deletes the original attachment [Guides: Making requests, Posting…].
- **Errors [F]:** `{ErrorType, Details, Message}` with 400/401/403/404/500. Retry advice: 401 → refresh once; 400 → don't retry; 500 → back off [Guide: Responses & errors].
- **Auth [F]:** OAuth 2 authorisation code via `my-horus.com`. The user selects a license; `grant_type=auth_code` (non-standard!); the code is valid for 2 minutes; the access token for 1 hour; **refresh tokens are single-use**, so serialise refreshes per connection [Guides: Authorization flow, Token lifecycle].
- **Versioning [F]:** backwards-compatible changes (new endpoints, optional params, response properties) happen without notice. Breaking changes are announced by email [Guide: Changes & versioning]. So the connector must ignore unknown properties.
- **Testing [F]:** "Requests run against the license's real database. Use a test license or a test folder for write operations" [Guide: Testing the API]. [?] No sandbox is documented.

---

## 5. Task A, route by route: the reasoning to understand and defend

Each route below gives: the mapping in one sentence, the call pattern, why it needs several calls (the case's hint), the trap to know, and why the verdict is what it is. Full endpoint tables, call sequences and limitations are in the HTML report (section 4, route cards).

**Final verdicts:** ✅ Supported: Get folders, Get analytic plans. 🟡 Supported with workaround: the other 9. 🔴 Not supported: none.

**Verdict calibration (D11), the rule to state when presenting:**
- *Supported* = one native endpoint (plus cached reference data) with deterministic transformations, nothing emulated, and only minor optional fields lost.
- *Workaround* = feasible, but needs extra per-request calls (read-backs, joins, loops), emulated filters/pagination/numbering, or loses a capability clients rely on.

> **The single most important message:** for most routes the core Horus capability *is* native. The "workaround" sits in the translation layer around it: read-backs, ID resolution, VAT codes, analytics conversion and pagination emulation.

### 5.1 Client creation → `POST /companies.new` (🟡)
- **One sentence:** a Chift client = a Horus **company** (third party) with `IsCustomer=true`, created in the folder. [F]
- **Call pattern:** duplicate checks (`companies.list` by VAT / external reference / search key) → `companies.new` → read-back (`companies.info` + `ibans.list` + an account lookup), so about 3–7 calls. [D]
- **Why several calls:** `companies.new` returns only `{Id}` [F, Guide: Responses & errors], but Chift's `ClientItemOut` needs `last_updated_on`, `third_party_account`, `bank_accounts[]` and `account_number`.
- **Traps:**
  - Horus requires `SearchKey`, `IsCustomer`, `IsSupplier`, `IsVatLiable`, `LanguageCode` and `CountryCode`, and Chift doesn't send a search key. The connector generates it (unique *within the folder* [F, Guide: Data model]; length and charset rules undocumented [?]).
  - Duplicate VAT numbers are refused by default (`AllowDuplicateVatNumber`) [F].
  - One flat address only [D]: Chift's delivery and invoice addresses are dropped.
  - Read and write names differ (`PhoneNumber` on write vs `ContactPhone` on read) → always build the response from the read-back.
- **force_merge makes sense here:** one Horus company can be both customer and supplier, so merging = `companies.update {IsCustomer:true}` on the existing supplier (never send `""`, which erases values [F, Guide: Making requests]).
- **Reliability:** no idempotency key → on a 500 or timeout, *search before retrying* (overrides Horus's generic "retry with backoff" advice).
- **Why workaround:** read-back, a generated key, and lost fields (mobile, notes, currency, person fields, extra addresses).

### 5.2 Invoice retrieval (multi plans) → rebuilt from the ledger (🟡)
- **One sentence:** Horus has **no "list invoices" endpoint** [F: no such endpoint among the 72]. Pushed invoices "are converted into book entries" [F, Guide: Posting…], so the connector rebuilds each invoice.
- **Call pattern** for a typical request (customer invoices, one quarter, with lines, partner and payments): `book-entries.list` ×2 (one per daybook of types 200 + 250, partner sideloaded) + `account-histories.list` ×1 (lines, VAT, analytics, matching) + `invoices.sales.outstanding.list` ×1 (document type, open amount) + `account-histories.list` ×1 (payment lines) = **about 5 calls**, plus cached reference data. [D]
- **Why several calls:** each part of a Chift invoice lives in a different Horus resource. This is the clearest example of the case's hint.
- **Traps:**
  - **Credit notes may sit in a sales daybook.** So read both sibling daybook types and classify each entry by the sign of the partner line (customer: net debit = invoice) [A, D1].
  - Periods are months [F], so day-level `date_from/to` is post-filtered.
  - No pagination [D], so the whole window is fetched each time.
  - An accountant's edit creates a **new id** [F]: reconcile on daybook + number.
  - Lines have no quantity or unit price [D].
- **Sideloading:** `Include=CompanyDetail.Company` on `book-entries.list` returns partners in the same call [F, Guide: Sideloading]. This is a good detail to mention.
- **`book-entries.info`** reads one entry by id (header only, no sideloading). It's useful for single-invoice reads and attachments, but not for the list path.

### 5.3 Invoice creation (multi plans) → `invoices.sales.new` / `invoices.purchases.new` (🟡)
- **One sentence:** customer_* → sales endpoint, supplier_* → purchases endpoint; `Type` 0 = invoice, 1 = credit note; the PDF is sent in the same call (multipart). [F]
- **Call pattern:** resolve the folder, daybook, partner, account search keys and cost sections (cached) → duplicate check on the document number → create → read back with `book-entries.info`. [D]
- **Biggest trap, VAT:** Chift's `tax_code` is "the Id of the Tax Code" [F, Chift], but Horus has **no VAT-code entity**. Each line carries `TaxRate + TaxOrigin + TaxType` (+ `TaxKind`, `TaxCondition`, `TaxConditionValue` for purchases), and "only some combinations are valid", listed in spreadsheets we don't have [F, Guide: Posting…]. → The connector owns a **synthetic VAT catalogue** with one id grammar (`S-21-0-0`, `P-21-2-0-0-1-true`, D2).
- **Second trap, analytics:** Chift sends % per plan; Horus wants **amounts on combinations of cost sections** [F]. Convert with a product of the percentages and largest-remainder rounding (D8). Show the worked example in the report (1,000 → 500 SALES/ALPHA + 500 SUPPORT/ALPHA).
- **Other traps:**
  - `Number` is numeric, and there's no auto-numbering on invoices [F].
  - No idempotency key and no invoice delete → duplicate check (D12).
  - Horus checks `Total = Base + Tax` and that the line sums match [F].
  - API entries are **unconfirmed by default** "which lets the accountant review them" [F, Guide: Data model] → mapping "posted" to `Confirmed=true` is a *product decision* (D12).
- **Market scope:** Horus is BE/LU (Legislation enum [F]), so the Dutch G/N split and withholding tax have no counterpart. Present this as market scope, not a connector gap.

### 5.4 Journal retrieval → `daybooks.list` (🟡) and 5.5 Folders → `folders.list` (✅)
- **Journals:** `daybooks.list` gives id, code (`SearchKey`), name (`Heading`), type, IBAN and currency [F].
  - The daybook **type maps cleanly** to Chift `journal_type` (100→supplier_invoice, 150→supplier_refund, 200→customer_invoice, 250→customer_refund, 500/590→financial_operation, 600→miscellaneous_operation) [D, D6].
  - Workaround because `counterpart_account` needs an account lookup, `next_document_numbers` can only be emulated, and `blocked`/`unallocated_account` don't exist [D].
- **The daybook type is the routing key of the whole connector:** "The daybook Type drives which endpoint you use to post entries" [F, Guide: Data model].
- **Folders:** almost 1:1 with `folders.list {Mode: 0}` [F].
  - `Mode` 0 = all folders, 1 = my folders, for an accountant [F].
  - `main_currency` = EUR (a constant; no currency field) [D].
  - Country only via `folders.info` (optional N+1).
- **Trap:** a Horus **company** is not a Chift company/folder. Say this early in the presentation.

### 5.6 Ledger account creation → `accounts.new` (🟡) and 5.7 Chart of accounts → `accounts.list` (🟡)
- **Create:** `accounts.new` takes only `SearchKey` (= number), `Heading` (= name) and optional fields [F]. **The Chift `type` cannot be written** (no category field) [F]. Pattern: duplicate check → create → read back (`accounts.info`).
- **Chart:** `accounts.list`, cached per folder (as Horus recommends [F, Guide: Reading…]).
  - `classes` → a "starts with" search-key prefix [F].
  - The **Chift type is computed** from several sources: bank/financial daybook concentration accounts, `IntCategory` (only `COLLECCUS` documented), `AccountCategory`, then a Belgian number-prefix fallback [A].
  - The type filter and pagination are emulated.
- **Trap:** the number 500 means four different things in Horus enums (daybook Bank, account category, account sub-category, account-history Cash). Always qualify enum values by their field.
- **No delete and no renumbering** of accounts through the API [D], so be careful with writes.

### 5.8 Miscellaneous operation creation → `book-entries.miscellaneous-operations.new` (🟡)
- **One sentence:** a dedicated endpoint posts a balanced debit/credit operation into a type-600 daybook [F].
- **Transformations:**
  - Chift's signed `amount` (positive = credit) → Horus `Debit`/`Credit` columns.
  - Chift line `type` → Horus `Type` 1 customer / 2 supplier / 3 general (CompanyId required for 1/2) [F, Guide: Bank, financial & misc.].
- **Why workaround (and not supported):**
  - **No currency field**, so non-EUR operations are rejected [D].
  - Numbers must be numeric [F].
  - `line_number` isn't stored.
  - A read-back is needed when Horus generates the number (`AutoGenerateNumber` works only with `Confirmed=true` [F]).
- **Balance:** Horus refuses unbalanced operations and has no `AllowUnbalanced` here [F] → validate in the connector and return a clean 422.

### 5.9 Analytic plans → `cost-schemas.list` (✅) and 5.10 analytic accounts → `cost-sections.list` per schema (🟡)
- **Vocabulary:** in Horus, "cost" = analytics. A cost schema = a dimension (max **8** per folder); a cost section = a value [F, Guide: Data model].
- **Plans:** one call, 1:1 → supported.
- **Accounts:**
  - `cost-sections.list` requires `CostSchemaId` [F], so it's one call per schema (≤ 8), then merge and paginate.
  - **Balances are not stored**; they can only be computed from cost histories over a period the Chift route doesn't carry [D].
  - "Free" schemas have no listable values → excluded in v1 (D8).
- **Remember `IncludeInactive=true`**, otherwise inactive sections are hidden by default [F].

### 5.11 Outstanding items → `invoices.sales.outstanding.list` + `customers.outstanding` / `suppliers.outstanding` (🟡)
- **Not N+1:** all three endpoints are folder-level, and omitting the `CompanyIds` filter means "no filter" [D, Guide: Making requests]. Whether the result is then complete and uncapped is to confirm [A].
- **Asymmetric:**
  - Clients have a native `OpenAmount` per open sales invoice (joined with `customers.outstanding` for the account and matching data).
  - Suppliers only have ledger lines, so the open amount is **computed from matching groups** (D5: credit − debit for suppliers, debit − credit for customers; positive = owed).
- **Traps:**
  - A payment appears both inside its invoice (`LinkedElements`) and as its own row, so de-duplicate.
  - Single due date.
  - `original_document` for items carried over from the previous year is uncertain [A].
  - Foreign-currency supplier items are returned in EUR (D4).
- **unposted_allowed** maps to Horus `Confirmed` (validated by the accountant). Invoices pushed via Chift stay invisible with `unposted_allowed=false` until the accountant confirms them. That's a good insight for a client conversation.

---

## 6. Task B: how to read and defend the attribute tables

The full tables are in the HTML report, section 5: 83 rows for client creation, 112 for invoice creation and 39 for outstanding items. Every Chift attribute and query parameter is covered (the final review checked this programmatically against the Chift schemas). Each row has a Horus source, a mapping type, a rule, a basis label and evidence.

**Four things to be able to explain:**
1. **The mapping types** (Direct, Transform, Lookup, Composite, Constant, Not available, Chift-side). They show at a glance where the effort is: Transform/Lookup/Composite rows are connector logic, and Not available rows are disclosed data loss.
2. **"Horus fields with no Chift source"**, a separate table per route. *This is the most overlooked part of a mapping*: the target's required fields that the source doesn't provide. Examples: `SearchKey`, `IsVatLiable` and `LanguageCode` on companies; `TaxOrigin` and `TaxType` on invoice lines; `CostLines[].Amount`.
3. **Request vs response:** for the write routes, the response must be built from a read-back, not echoed, because Horus normalises values and names differ on read.
4. **Query parameters:** e.g. `force_merge`, `regroup_lines` (Chift-side pre-processing), `ignore_accounting_id` (skip the read-back), `force_financial_period` (not supported: Horus has no forced period on creation), `unposted_allowed` (→ `Confirmed`).

**Field-level decisions worth quoting:**

| Chift | Horus | Why it is interesting |
|---|---|---|
| client `account_number` | `CustomerConcentrationAccount` (search key on write, `{Type, Id}` on read) | Horus uses shared control accounts (400000) plus the company as sub-ledger; `third_party_account` = company `SearchKey` |
| client `language` | `LanguageCode` (FR/NL/DE/EN/ES/PT), else the folder language | Required in Horus, optional in Chift |
| invoice `invoice_type` | endpoint (sales/purchases) + `Type` (0/1) + daybook type | One Chift field drives three Horus choices |
| invoice `lines[].tax_code` | `TaxRate` + `TaxOrigin` + `TaxType` (+ purchase fields) | Synthetic VAT catalogue (D2) |
| invoice `analytic_distribution` | `CostLines[{Amount, Costs[{SchemaSearchKey, Value}]}]` | % per plan → amounts on combinations |
| invoice `reference` + `customer_memo` | one `Comment` (`{reference} \| {memo}`) | Single free-text field (D3) |
| invoice `status` | `Confirmed` | Accountant review by default (D12) |
| outstanding `open_amount` | `OpenAmount` (clients) / computed from matching (suppliers) | Asymmetric sources |

---

## 7. How the analysis was checked, and what the review changed

What I did (worth describing, since they assess *how you approach* an unfamiliar API):
1. Read both contracts myself and spot-checked the key endpoints.
2. Each route group was mapped, then **challenged by two independent reviews**: an *evidence* review (try to refute every cited endpoint, field and enum) and a *completeness* review (missing attributes, endpoints, required fields, edge cases).
3. A reconciliation re-checked every challenge against the docs. About 175 corrections were applied; dozens of findings were rejected with reasons.
4. A **final cross-route review** found 5 major inconsistencies *between* routes. Each route was locally correct, but the routes didn't fit together.

**The 5 major cross-route findings (great material for "what would you do differently / what did you learn"):**

| # | Problem | Decision |
|---|---|---|
| D1 | A credit note created in a sales daybook (fallback) would read back as an invoice | Read both daybook types; classify by the partner-line sign |
| D2 | Three different VAT-code id formats across routes; the purchase `TaxKind` can't be read back | One id grammar; return null on ambiguous reads |
| D3 | `reference` written into the comment, read back into different fields | One `{reference} \| {memo}` convention, split on read |
| D4 | Foreign-currency amounts: EUR numbers paired with USD labels | One assumption (ledger in EUR); never mix |
| D5 | Customer open items computed with the supplier sign | Sign by side |

Minor decisions: D6 (one daybook-type table), D7 (one folder rule), D8 (one analytics cache and rounding rule), D9 (one partner mapper), D10 (partner_info), D11 (verdict calibration, which **downgraded miscellaneous operations to workaround**), D12 (posted/confirmed, duplicate checks), D13 (folder check on calls by id).

> **Lesson to say out loud:** a connector is a *system* of routes that must round-trip. What a create route writes must be readable by the get route in the same shape. Reviewing routes in isolation misses this.

---

## 8. What to communicate to Chift, and what to clarify

**Lead with:**
1. Feasible: all 11 routes, none blocked. Two native 1:1, nine with workarounds absorbed by the connector.
2. The shape of the work: a translation layer (read-backs, invoice reconstruction, VAT catalogue, analytics conversion, pagination emulation, duplicate protection), built as shared components.
3. Disclosed limitations, in client language (one address, no line quantities, EUR-only operations, no writable account type, analytic balances not stored).
4. The short list of Horus questions that change the design (report H1–H6) and the Chift conventions to agree (C1–C6).

**The top 6 questions for Horus (why they matter):**
- **H1, tax-combination files:** without them, valid VAT can't be posted.
- **H2, credit notes vs daybooks:** decides write selection and read classification.
- **H3, numbering and idempotency:** duplicate safety.
- **H4, currency of ledger amounts and the `CurrencyRate` direction:** correctness of every foreign-currency read.
- **H5, rate limits and result sizes:** with no pagination, large folders are the performance risk.
- **H6, ErrorType catalogue:** precise errors and safe retries.

**The top Chift-side decisions:** C1 (posted → confirmed by default?), C2 (synthetic VAT catalogue acceptable?), C3 (reject vs ignore unsupported inputs), C5 (sign conventions), C6 (duplicate policy).

---

## 9. Likely follow-up questions, with prepared answers

| Question | Answer (and basis) |
|---|---|
| "How did you approach an API you'd never seen?" | Contract first (Chift's inputs/outputs), then Horus's conventions (auth, folder scoping, envelope, pagination), then a 72-endpoint inventory → mapping → verdict → limitations. The same 7 questions per route, and every claim labelled documented / derived / assumption / to confirm. |
| "Why do some routes need several Horus calls?" | Horus is a ledger with an RPC API. Creates return only an id (so a read-back), invoices exist only as book entries + lines (so a rebuild), and posting references search keys (so lookups). Example: invoice retrieval ≈ 5 calls. [F/D] |
| "What's the hardest part?" | VAT codes (no entity; a combination catalogue we must own) and invoice retrieval (rebuild + credit-note classification). Then outstanding items for suppliers (open amount computed). |
| "Is there a sandbox?" | Not documented: "Requests run against the license's real database. Use a test license or a test folder" [F]. Ask Horus for one (H17). |
| "How does authentication work for Chift's multi-tenant setup?" | OAuth 2 code flow via my-horus.com; the user picks the license; each license has its own `api_url`; non-standard `grant_type=auth_code`; 1-hour access tokens; **single-use refresh tokens**, so serialise refreshes per connection. [F] |
| "Pagination?" | None on any list, so Chift emulates page/size/total. Mitigate with per-folder caching, `ModifiedAfter` incremental sync and gzip. Rate limits undocumented (H5). [D] |
| "What if a field doesn't exist in Horus?" | Classify it as Not available, return null (or Chift's agreed default) on read, and reject or ignore-with-warning on write (decision C3). It's always listed in the attribute table. |
| "Why is miscellaneous operation not 'supported'? It has a dedicated endpoint." | Calibration (D11): no currency field (EUR only), numeric numbers only, and a read-back when Horus numbers the entry. That loses a capability clients rely on. The core endpoint is native. |
| "Can you post a payment matched to its invoice?" | Yes, outside this scope: `book-entries.banks.new` plus `matching` (or `MatchNo` at creation, with `matching.next-number.*`) [F, Guide: Outstanding items & matching]. A good bridge to part 2 (synchronisations). |
| "What happens when the accountant edits an invoice we pushed?" | Horus creates a new book entry id and drops the attachment [F]. The connector reconciles on daybook + number, as Horus advises [F]. |
| "Should entries be confirmed?" | Horus's default is accountant review. Chift's default is "posted". I propose posted → confirmed with a per-consumer "always unconfirmed" option, and I'd validate the default with Chift and Horus (C1). |
| "How confident are you?" | Chift side: high (official spec; re-check against the live docs). Horus side: high on what's documented (API reference + 15 guides). Every assumption is labelled and has a matching question. |
| "Performance?" | The worst cases are invoice retrieval over long periods and large accounting-firm folders (full lists, no paging). Mitigate with caching, narrow windows, gzip and incremental sync, and ask Horus for limits. |
| "What would you do next?" | Answers to H1–H6, a test license, then prototype the two riskiest flows (invoice retrieval, supplier outstanding items) before building the rest on shared components. |
| "Anything wrong in Chift's own docs?" | Two small things: `FolderItem.main_currency` says ISO 3166-1 (country codes; ISO 4217 is meant), and the line `tax_amount` formula omits /100. Mention them tactfully (C13). |

---

## 10. Suggested presentation storyline (15–20 minutes, using the HTML report)

1. **Context (1 min):** what Chift does; what a connector is; what Horus is (BE/LU accounting firms and SMBs; one database and API URL per license). → report header and section 3 diagram.
2. **Method (2 min):** the 7 questions, the verdict scale, the basis labels, the review process. → section 2.
3. **Concept map (2 min):** folder = folder, *company = third party*, daybook = journal, cost schema/section = analytic plan/account, no VAT-code entity. → section 3.
4. **Results (4 min):** the overview table, 2 supported / 9 workaround / 0 not supported, and why "workaround" mostly means translation. → section 4 table.
5. **Deep dive (5 min):** pick **invoice creation** (VAT catalogue + analytics worked example) and **invoice retrieval** (rebuild from the ledger: the "multiple endpoints" hint). Open one route card live and use the attribute-table filter (e.g. type "tax"). → sections 4–5.
6. **Risks and decisions (2 min):** edge cases plus two or three cross-route decisions (credit notes, VAT ids, posted/confirmed). → sections 7 and appendix B.
7. **Open questions and next steps (2 min):** H1–H6, C1–C6, test license, prototype. → sections 8–9.

**Client-friendly phrasing to reuse:** "Chift speaks one standard language. For Horus we checked each standard request: Horus understands it directly, needs a few extra steps, or can't do it. Here's what works, what works with limits, and what we still need Horus to confirm."

---

## 11. Cheat sheet: facts and numbers

| Fact | Value | Source |
|---|---|---|
| Horus endpoints | 72 (incl. `book-entries.info`); 23 GET, 47 POST, 2 DELETE | API reference |
| Endpoints used by the 11 routes | 49 (including optional ones) | analysis |
| Auth | OAuth 2 code; `grant_type=auth_code`; code valid 2 min; access token 1 h; refresh token single-use | Guides: Authorization flow, Token lifecycle |
| Base URL | per license (`api_url` from OAuth) | Guide: Authentication overview |
| Sideloading | `Include` on 4 endpoints | Guide: Sideloading |
| Pagination | none | reference + guides (absence) |
| Ledger periods | month/year | Guide: Reading accounting data |
| Cost schemas per folder | max 8 | Guide: Data model |
| Invoice types | `Type` 0 invoice / 1 credit note | API reference |
| Daybook types | 100 purchase, 150 purchase CN, 200 sale, 250 sale CN, 500 bank, 550 cash, 590 financial, 600 misc., 610/690/700 other misc., 900 budget, 990 external | API reference |
| Operation line types | 1 customer / 2 supplier / 3 general | Guide: Bank, financial & misc. |
| Matching account types | 100 customer / 200 supplier / 300 general | Guide: Outstanding items & matching |
| Legislations | BE, LU | API reference |
| Errors | `{ErrorType, Details, Message}`; 400/401/403/404/500 | Guide: Responses & errors |

---

## 12. Files

| File | What it is |
|---|---|
| `chift_horus_mapping_report.html` | **External deliverable** for Chift (self-contained; open in any browser) |
| `01_internal_notes_part1_mapping.md` | These notes (internal) |
| `data/*.json` | Final harmonised mapping data per route group (what the report is generated from) |
| `decisions.md` | Cross-route decision log D1–D15 (internal wording) |
| `appendix_chift_spec_extract.md` | Chift OpenAPI extract for the case endpoints |
| `appendix_horus_api_reference.md` | Horus API reference (72 endpoints, rendered) |
| `appendix_horus_guides.md` | Horus guides (15 pages, extracted text) |
| `report_src/` | Generator for the HTML report (Python, no dependencies) |
