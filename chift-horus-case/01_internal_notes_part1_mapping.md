# Chift × Horus: Part 1 (mapping), internal working notes

> **Internal only. Not for Chift.** These are my study and prep notes. The external report comes later as a separate HTML file.
>
> **Status (13 Oct 2026):** the Chift side is fully analysed. The Horus side is **blocked** because its documentation can't be reached from this environment (see §0). Every Horus-related item below is a question to answer, not a finding.

**Labels used throughout**

| Label | Meaning |
|---|---|
| **[F]** | Fact, stated directly in a source (source given next to it) |
| **[D]** | Deduction, my conclusion from one or more facts (reasoning shown) |
| **[A]** | Assumption, plausible but unconfirmed; must be validated |
| **[?]** | Missing or ambiguous information |
| **[BG]** | General accounting background, included to explain a concept. Not a claim about Chift or Horus |

**Source tags:** `[Case]` = the Notion case page. `[OAS:<operationId>]` = Chift OpenAPI spec (see §0). `[Horus]` = Horus API docs (**not accessed**).

---

## 0. Source status (read this first)

| Source | Status | How it is used |
|---|---|---|
| Case page "Case Product / Tech" (chift.notion.site) | ✅ Read in full through the Notion connector | Defines the scope and the deliverable |
| Chift API reference (`docs.chift.eu`) | ⛔ Denied by this environment's network policy | Not read directly |
| **Chift OpenAPI spec**: the `openapi.json` bundled in Chift's official Python SDK (PyPI package `chift`, v0.6.16), titled "Chift API" | ✅ Read | Chift-side source of truth for these notes. The raw extract is in `appendix_chift_spec_extract.md` |
| Chift Developer Guides (idempotency, multiple folders, …) | ⛔ Not accessible. The spec refers to them but doesn't include them | Flagged where relevant |
| Horus API docs (`horussoftwareapi.docs.apiary.io`; Apiary serves the content from `jsapi.apiary.io`) | ⛔ Denied by network policy | **Nothing about Horus in these notes is factual** |
| Copies of either doc set in Notion or Google Drive | ❌ None found (searched for "Horus" and "Chift" and listed recent, private and shared pages) | n/a |

**Why the SDK spec can stand in for the Chift reference (trust it, but verify):**
- [F] All 11 Chift URLs in the case are slugs of operation summaries in this spec, one for one. For example, `get-invoices-by-type-salepurchase-entries--multiple-analytic-plans` matches the summary "Get invoices by type (sale/purchase entries - Multiple Analytic Plans)" `[OAS:accounting_get_invoices_by_type_multi_analytic_plans]`.
- [D] So the reference pages the case links to are very likely rendered from this spec.
- [A] It's a snapshot (SDK v0.6.16), so fields may have changed since. **Before presenting, re-check the spec against the live docs.chift.eu pages** (10 minutes on a normal laptop).

---

## 1. The case in my own words

**What the case says** `[Case]`:
- "We want to develop a new accounting connector. We need to do an analysis of the **feasibility** and the **match with our existing routes**."
- **Task A (route level):** for each of 10 listed Chift endpoints, say which Horus endpoint(s) to use, plus "any particular considerations or specificities".
- **Task B (attribute level):** for 3 endpoints, give a granular mapping "at the level of each attribute and the different query parameters". The 3 are: Create client, Create sale/purchase entry (multiple plans), and Get clients/suppliers outstanding items.
  - Note: **Outstanding items is not one of the 10 in Task A.** It is an 11th endpoint that appears only in Task B. Don't miss it.
- **Hint:** "it can happen that we need to pull data from multiple endpoints when implementing 1 endpoint in Chift."
- **What they evaluate:** "We're not looking for a perfect answer. We want to see how you approach an unfamiliar API, how you structure your thinking, and how you'd explain it to a client." It is presented in person, in any format.

**Plain-language restatement**
- [F] Chift offers "a universal API giving you access to financial data from the software of your clients… you connect once" (spec `info.description`).
- [D] So a software vendor integrates with Chift once. For each accounting package, Chift maintains a **connector** that translates every standard Chift route into calls on that package's own API.
- [D] Horus is a candidate new package. Before building, Chift wants to know, route by route: *can this be built on Horus's API? With which calls? What gets lost or needs a workaround?*

```text
Software vendor ──(1 standard call)──► Chift unified route ──► Horus connector ──(1..n calls)──► Horus API ──► data of one company/dossier
   (Chift's client)                    e.g. POST /accounting/   (translate params, map fields,
                                       clients                   resolve IDs, combine responses)
```

---

## 2. Business objective and expected outcome

- **Objective [D]:** make a **go/no-go and scoping decision** for a Horus connector. That means: how much of Chift's standard accounting surface Horus can support, at what effort, and what limitations Chift will have to communicate to its own clients.
- **Expected outcome [D, from Case]:**
  1. A route-level mapping table with a coverage verdict per route.
  2. Field-level and query-parameter-level mappings for the 3 detailed routes.
  3. Limitations, dependencies and open questions.
  4. An explanation a client can follow. The case says explicitly "how you'd explain it to a client", so the deliverable must work for non-developers too.

---

## 3. How to break the problem down (the method to show in the presentation)

For **every** Chift route, ask the same 7 questions:

1. **Business meaning:** what business object or action is this? (create a customer, read invoices, …)
2. **Chift contract:** what does Chift *require* as input and *promise* as output (required fields, filters, pagination)?
3. **Capability:** does Horus have this object, and can it be *read* and/or *written* via the API?
4. **Endpoint(s):** which Horus endpoint(s), in what order? Is it one call, or a combination?
5. **Fields:** for each field, is it a direct 1:1 match, a transformation, a lookup, composite, a constant, or unavailable?
6. **Behaviour:** are filters, pagination, incremental sync (`updated_after`), posting status and numbering native in Horus, or must the connector emulate them?
7. **Risk:** limitations, edge cases, error handling.

**Coverage verdict scale** (use the same scale for every route):

| Verdict | Meaning |
|---|---|
| ✅ Supported | Native equivalent; 1:1 or simple transformation |
| 🟡 Supported with workaround | Several calls combined, filters emulated, or some fields missing |
| 🔴 Not supported | No read/write capability in the Horus API |
| ⚪ Unknown | The documentation doesn't say, so it becomes a question for Horus |

**Field classification codes** (for Task B):

| Code | Meaning | Example |
|---|---|---|
| `DIRECT` | Same meaning, same format | `email` → `email` |
| `TRANSFORM` | Same meaning, different format, unit, enum or sign | ISO language code → Horus language enum; +credit/−debit → debit/credit columns |
| `LOOKUP` | Needs an ID or code resolved via another endpoint | VAT rate + code → Horus VAT-code ID |
| `COMPOSITE` | Built from several fields or endpoints | `open_amount` = invoice total − matched payments |
| `CONSTANT` | Connector sets a fixed or default value | `status = posted` |
| `N/A` | Not available in Horus: return null, or reject the request | `scheme_ids` |

> **Why this matters for the presentation:** the case says they want to see *how I approach an unfamiliar API*. A repeatable method with explicit verdict and classification codes shows exactly that, and it scales to the other connectors Chift builds.

---

## 4. Domain primer (concepts needed to read the mapping)

| Concept | What it is | Why it matters for the mapping |
|---|---|---|
| **Consumer** | [F] Every route is scoped by a `consumer_id` (uuid) path parameter. [D] It represents the end customer whose software is connected through Chift | Not a Horus concept. The connector must keep, per consumer, the Horus credentials and context |
| **Folder** | [F] "A folder represents a legal entity within the system. Required when the multiple folders feature is enabled." Folders have a `selected` flag set "during the Chift activation process" `[OAS:accounting_get_folders]` | **Key Horus question:** does one Horus API credential give access to one company, or to many (for example, an accountant's portfolio)? This decides whether `folder_id` maps to a Horus company/dossier ID |
| **Chart of accounts / ledger account** | [BG] The list of accounts (number + name) to which every amount is booked. [F] The number "must be unique within the accounting folder… In some countries (e.g., France, Belgium, Spain), the number structure is constrained by local accounting rules" `[OAS:accounting_create_ledger_account]` | Account numbers are the "language" of every posting. The connector must respect Horus's numbering rules |
| **Account classes** | [F] The chart-of-accounts filter `classes` takes e.g. "6,7". [BG] In class-based charts (such as the Belgian/French ones) the first digit is the class: 6 = expenses, 7 = income | If Horus has no class filter, [D] the connector can filter on the first digit of the account number |
| **Journal** | [BG] A "book" grouping entries of one kind. [F] Chift journal types: `customer_invoice`, `customer_refund`, `supplier_invoice`, `supplier_refund`, `financial_operation`, `miscellaneous_operation`, `unknown` | Horus's journal categories must map onto this enum |
| **Sale/purchase entry ("invoice")** | [F] In Chift accounting, "invoice" means the *booking*: `invoice_number` is "an internal reference number… does not necessarily match the number displayed on an invoice". For purchases, `reference` "typically contains the invoice number issued by the supplier" | Don't confuse it with a commercial invoicing module. This is an accounting entry with a header and lines |
| **Miscellaneous operation** | [BG] A manual journal entry not tied to an invoice or bank statement (accruals, corrections, payroll postings…). [F] Lines are signed: "Positive for Credit and negative for Debit" | The sign convention is a typical `TRANSFORM` point |
| **Partner / third party** | [BG] A client or supplier. [F] `force_merge` exists because some "accounting systems using 1 entity to handle clients/customers and suppliers will merge the existing supplier with the new client" | Ask whether Horus has separate client and supplier objects, or one third-party object |
| **`account_number` vs `third_party_account`** (client) | [F] `account_number`: the ledger account "as it will appear in the official accounting export file… In some systems, each customer has a dedicated account; in others, a shared control account is used and customer balances are tracked in a subledger." `third_party_account`: "Third party account number/code representing the client" | Ask which model Horus uses |
| **VAT code (`tax_code`)** | [F] On invoice lines, `tax_code` is "the Id of the Tax Code in the accounting software" | [D] The caller must look the codes up first (Get VAT codes). That endpoint isn't in the case's list, but invoice creation **depends** on it |
| **Analytic plan / account / distribution** | [BG] A plan is an extra analysis axis (department, project…) alongside the general ledger. [F] Plans can have a `parent_id`. An analytic account belongs to one plan. Each invoice line distributes its untaxed amount per plan across accounts, in percentages: "Only whole numbers… must equal 100%" | Does Horus support analytics? How many axes? Percentages or amounts? |
| **Outstanding item** | [F] An item with `amount` and `open_amount`, `due_dates[]`, `matching_numbers[]`, `posted`, `original_document` (when "initially posted in previous bookyear") `[OAS:accounting_get_outstandings]` | Needs payment-matching state from Horus, which is often the hardest data to get |
| **Matching (lettering)** | [BG] Linking an invoice with its payment(s) so that both are cleared | Determines `open_amount` and `matching_numbers` |
| **Posted vs draft** | [F] Input status `draft`/`posted` (default `posted`). Output adds `cancelled`, `paid`, and `matched` (misc. operations) | Does Horus have a draft concept? |
| **Bookyear / financial period** | [F] `force_financial_period` takes the format `mmYYYY`. Bookyears have `name`, `start`, `end` | Does Horus expose periods, and accept a forced period? |
| **Pagination** | [F] List routes return `{items, total, page, size}`, with `page` defaulting to 1 and `size` to 50 | [D] The connector must produce `total`. If Horus doesn't return a total count, the connector must compute it, which may mean fetching everything |
| **Idempotency** | [F] `invoice_number`: "It is recommended to use this number for idempotency to prevent duplicate entries. Refer to the idempotency documentation in the Developer Guides" | [?] The Developer Guide wasn't accessible. How does Chift detect duplicates, and does Horus enforce unique numbers? |

---

## 5. Task A: route-level analysis (Chift side complete, Horus side pending)

For each route: what Chift expects, the **signals that one Chift call will need several Horus calls** (the case's hint), what to look for in the Horus docs, and the specific points to flag.

### 5.1 Client creation: `POST /consumers/{consumer_id}/accounting/clients` `[OAS:accounting_create_client]`
- **Business meaning:** create a customer record in the accounting tool.
- **Chift contract [F]:**
  - Query parameters: `folder_id` and `force_merge` (the ID of an existing supplier to merge with).
  - Body (`ClientItemIn`): only `name` and `addresses[]` are required. Each address requires `address_type` (main/delivery/invoice), `street`, `city`, `postal_code` and `country` (ISO 3166-1).
  - Response (`ClientItemOut`): includes `id`, `last_updated_on`, `third_party_account` and `bank_accounts[]`.
- **Multi-call signals [D]:**
  1. The response must contain the full created client (`id`, `last_updated_on`, `third_party_account`). If Horus's create call returns only an ID → **POST + GET**.
  2. Addresses (up to 3 types) and bank details may be separate sub-resources in Horus → extra calls.
  3. `force_merge` → find the existing supplier and convert or flag it. Only relevant if Horus uses a single third-party entity.
  4. `account_number` → if Horus uses dedicated customer accounts, the account may need to exist first (link to 5.5).
  5. [F] `vat` "can be used as a reliable identifier to match clients between systems" → optional duplicate check (search by VAT) before creating.
- **What to look for in the Horus docs:** a create-customer/third-party endpoint; whether clients and suppliers are one object; required fields; the address model; bank account fields; language and currency formats; whether customer account numbers are auto-assigned; whether POST returns the full object; how the call is scoped to a company.
- **Points to flag [F]:** `first_name`, `last_name`, `function` and `company_id` are used only when `is_company=false` (an individual). `iban`/`bank_account` exist on input, but on output they are "DEPRECATED see bank_accounts" → an input/output asymmetry.

### 5.2 Invoice retrieval: `GET …/accounting/invoices/multi-analytic-plans/type/{invoice_type}` `[OAS:accounting_get_invoices_by_type_multi_analytic_plans]`
- **Business meaning:** list the sale/purchase entries of one type, paginated.
- **Chift contract [F]:**
  - Path: `invoice_type` ∈ {`customer_invoice`, `customer_refund`, `supplier_invoice`, `supplier_refund`}.
  - Query parameters: `page`, `size`, `folder_id`, `date_from`, `date_to`, `journal_ids` (comma-separated), `include_payments` (default false), `payment_status` (all/unpaid/paid; "Cancelled invoices are filtered out when using either paid or unpaid"), `updated_after` (UTC datetime), `include_invoice_lines` (default false), `include_partner_info` (default false), `approval_status` (pending/approved/rejected).
  - Output: header, lines with `analytic_distribution`, `payments[]`, `partner`, `due_dates[]`, `attachments_info`, `accounting_info` (`main_currency`, `main_currency_total`, `account_number`), `approval_status` and `status` (cancelled/draft/posted/paid).
- **Multi-call signals [F, from Chift's own wording]:** lines are left out by default "when this requires extra requests on the target API". The same applies to partner info. Attachments can be `yes_to_request`, meaning a separate `GET /accounting/attachments`. **So Chift's model already expects targets where the list call is lighter than the detail call.**
- **Multi-call signals [D]:**
  - Payments and `payment_status` need matching or open-amount data, probably from another Horus resource.
  - Analytic distribution may come from line detail.
  - `accounting_info.main_currency` may come from company settings.
  - If Horus can't filter by modification date, `updated_after` must be emulated (full fetch + filter), which is expensive. The same goes for `journal_ids`.
- **Transformation points [D]:**
  - Invoice versus credit note: does Horus model refunds as a separate document type, a separate journal, or as negative amounts?
  - If Horus stores analytic **amounts**, the connector must convert them to **whole-number percentages**, which introduces rounding.
- **What to look for in the Horus docs:** sales and purchase document list endpoints; filters (date, journal, modified-since); pagination and total count; whether lines are in the list or only in the detail; payment and matching info; attachment download; the status model (draft/posted/cancelled/paid); any approval workflow.
- **Points to flag [F]:** `invoice_date` is "automatically set to '1970-01-01' if the value is empty". `due_date` falls back to the invoice date when the software doesn't provide one.

### 5.3 Invoice creation: `POST …/accounting/invoices/multi-analytic-plans` `[OAS:accounting_create_invoice_multiple_plans]`
Detailed in §6.2. At route level:
- **Dependencies [D]:** almost every reference in the body is an *ID in the accounting software*, so other routes must be mapped first:

| Field | Depends on | In the case's list of 10? |
|---|---|---|
| `partner_id` | Client exists (5.1) / supplier exists | Client creation yes; **supplier creation and get clients/suppliers no** |
| `journal_id` | Get journals (5.4) | yes |
| `lines[].account_number` | Chart of accounts (5.6) | yes |
| `lines[].tax_code` | **Get VAT codes** | **no, but required** |
| `analytic_distribution[].analytic_plan` / `analytic_account` | 5.9 / 5.10 | yes |
| `payment_term_id`, `payment_method_id` | Get payment terms / payment methods | no (optional fields) |

- **Multi-call signals [D]:**
  - The PDF (`pdf` base64) may need a separate upload call.
  - The response must return the created invoice (`id`) unless `ignore_accounting_id=true`. [F] With that flag, "Chift will not wait for the invoice to be processed to return", which suggests some targets process invoices asynchronously.
  - `partner_info` creates the partner on the fly "In some tools [where] we cannot create a client/supplier by API (… e.g. Tiime)".
- **Query parameters [F]:** `folder_id`, `force_financial_period` (mmYYYY), `regroup_lines` (default true: "Regroup lines by account number, tax code and analytic distribution"), `ignore_accounting_id` (default false), `force_currency_exchange` (default false).

### 5.4 Journal retrieval: `GET …/accounting/journals` `[OAS:accounting_get_journals]`
- **Output [F]:** `id`, `code`, `name`, `journal_type` (enum), `counterpart_account` (bank/cash), `unallocated_account`, `next_document_numbers[]` (per bookyear), `iban`, `currency`, `other_currencies_allowed`, `blocked`.
- **Multi-call and transformation [D]:**
  - `journal_type` must be derived from Horus's journal categories through a mapping table.
  - `next_document_numbers` may need bookyear or sequence data.
  - Bank journals may need bank-account details for `iban`.
- **What to look for in Horus:** a journal list; journal types; whether refund journals are separate from invoice journals (Chift has `customer_refund` and `supplier_refund` types); numbering sequences; blocked/archived flags.

### 5.5 Ledger account creation: `POST …/accounting/accounts` `[OAS:accounting_create_ledger_account]`
- **Body [F]:** `name`\*, `number`\*, and `type` (enum, default `other`). The response returns `AccountItem` (`number`, `name`, `active`, `type`, `scheme_ids`, `accounting_category`).
- **Points [D]:**
  - `type` → Horus classification (`TRANSFORM`).
  - The number must pass local chart rules and be unique.
  - If the create call returns little → a GET afterwards.
- **What to look for in Horus:** whether accounts can be created via the API at all (a common restriction); number format and length; type/category field; per-company scope.

### 5.6 Chart of accounts retrieval: `GET …/accounting/chart-of-accounts` `[OAS:accounting_get_chart_of_accounts]`
- **Filters [F]:** `classes` (e.g. "6,7") and `type`. Note that the filter's `type` enum (`bank`, `cash`, `income`, `expense`, `other_expense`, `vat`) is a **subset** of the output type enum, which also has `receivable`, `payable`, `other_financial` and `other`.
- **Points [D]:**
  - `type` is derived from a Horus category, or else from the number prefix (a heuristic, so risky).
  - The `classes` filter can be emulated by prefix if it isn't native.
  - `scheme_ids` refers to reporting schemes (the spec's examples are RGS and SBR; [BG] these are Dutch reporting standards). Likely `N/A`, but [A] to confirm.
- **[?]** Does Horus return per-partner sub-accounts in the chart? That affects volume and filtering.

### 5.7 Accounting folders retrieval: `GET …/accounting/folders` `[OAS:accounting_get_folders]`
- **[F]** Not paginated: it returns an array of `FolderItem` (`id`, `name`, `selected`, `active`, `vat`, `company_number`, `main_currency`, `addresses[]`).
- **Points [D]:**
  - The company list and the company details (VAT number, address, currency) may be separate Horus endpoints → N+1 calls.
  - `selected` is a Chift-side activation flag, not Horus data.
- **What to look for in Horus:** multi-company access per credential; a list-companies endpoint; company identity fields.
- **Doc inconsistency to mention tactfully [F]:** `FolderItem.main_currency` is described as "Format: ISO 3166-1 codes" (the *country* code standard). `AccountingInfoOut.main_currency` says "ISO-4217" (the *currency* standard), which is the correct one.

### 5.8 Miscellaneous operation creation: `POST …/accounting/miscellaneous-operation` `[OAS:accounting_create_miscellaneous_operation]`
- **Body [F]:**
  - Header: `operation_number`, `currency`\*, `currency_exchange_rate`, `operation_date`\*, `journal_id` (auto-selected only if there's a single journal, otherwise an error), `status` (draft/posted).
  - `lines[]`\*: `amount`\* ("Positive for Credit and negative for Debit"), `type`\* (`customer_account`/`supplier_account`/`general_account`), `account_number`\*, `partner_id` ("Must be filled in if it is a 'customer_account' or 'supplier_account' line type"), `analytic_account` (a single ID: "no distribution possible"), `description`, `line_number`.
- **Points [D]:**
  - Sign → debit/credit columns (`TRANSFORM`).
  - Partner lines → Horus third-party sub-ledger.
  - A journal of type `miscellaneous_operation` is needed.
  - If Horus requires plan + account for analytics, the connector must look up the account's plan (`LOOKUP`).
- **[A] [BG]** In double-entry bookkeeping the lines must balance (sum to 0). **The Chift spec doesn't state this**, so don't claim it as a Chift rule. Check how Horus validates balance.

### 5.9 Analytic plans retrieval: `GET …/accounting/analytic-plans` `[OAS:accounting_get_analytic_plans]`
- **Output [F]:** `id`, `name`, `active`, `parent_id` ("hierarchy… when that is supported").
- **[D]** If Horus has a single analytic axis, expose one plan (and the multi-plan routes then degrade gracefully). If Horus has no analytics, return an empty list and flag it.

### 5.10 Analytic accounts retrieval: `GET …/accounting/analytic-accounts/multi-analytic-plans` `[OAS:accounting_get_analytic_accounts_multi_plans]`
- **[F]** "Returns all analytic accounts of all analytic plans". Output: `id`, `active`, `code`, `name`, `currency`, `balance`, `credit`, `debit` (all three default to 0), `analytic_plan`.
- **Multi-call [D]:**
  - If Horus lists accounts per plan → iterate over the plans (N+1) and merge, then emulate pagination across the merged list.
  - `balance`, `credit` and `debit` may require a separate balance or report endpoint.
- **[?] for Chift:** if the balance isn't available, should it be 0 (the default, but misleading) or null?

### 5.11 Outstanding items (Task B only): `GET …/accounting/outstandings` `[OAS:accounting_get_outstandings]`
Detailed in §6.3. **[D]** This is likely the most complex route, because it depends on payment-matching state, multiple due dates and links across bookyears.

### Route-level summary (Horus columns to fill once the docs are accessible)

| # | Chift route | Method | Likely pattern [D] | Key dependency or risk [D] | Horus endpoint(s) | Verdict |
|---|---|---|---|---|---|---|
| 1 | Create client | POST | Create (+ read back) | Single vs separate third-party model; addresses | ⏳ | ⚪ |
| 2 | Get invoices (multi plans) | GET | List + detail + payments + partner | Lines/payments/analytics may need extra calls; `updated_after` | ⏳ | ⚪ |
| 3 | Create invoice (multi plans) | POST | Lookups → create (+ attach PDF) (+ read back) | VAT-code IDs, journal, partner, analytics | ⏳ | ⚪ |
| 4 | Get journals | GET | List (+ sequences) | Journal-type mapping | ⏳ | ⚪ |
| 5 | Create ledger account | POST | Create | Is write allowed at all? Numbering rules | ⏳ | ⚪ |
| 6 | Get chart of accounts | GET | List (+ type derivation) | Type and class filters | ⏳ | ⚪ |
| 7 | Get folders | GET | List companies (+ details) | Multi-company access model | ⏳ | ⚪ |
| 8 | Create misc. operation | POST | Lookups → create | Sign convention, partner lines, analytics | ⏳ | ⚪ |
| 9 | Get analytic plans | GET | List | Analytics supported? How many axes? | ⏳ | ⚪ |
| 10 | Get analytic accounts (multi plans) | GET | Iterate plans → merge (+ balances) | N+1, balances | ⏳ | ⚪ |
| 11 | Get outstandings (Task B) | GET | Entries + matching + partner (+ prior-year link) | Open amounts and matching | ⏳ | ⚪ |

---

## 6. Task B: attribute-level mapping (Chift side complete, Horus column pending)

The Horus column stays empty (⏳) until the docs are readable. The "Mapping considerations" column says what to check and why.

### 6.1 Client creation: `POST …/accounting/clients`

**Path and query parameters**

| Chift parameter | In | Req | Type | Meaning [F] | Mapping considerations [D] | Horus |
|---|---|---|---|---|---|---|
| `consumer_id` | path | ✔ | uuid | Chift consumer | Chift-internal; selects the stored Horus credentials | n/a |
| `folder_id` | query | | string | Legal entity; required when multi-folder is enabled | → Horus company/dossier identifier (header, path or credential?) | ⏳ |
| `force_merge` | query | | string | ID of an existing supplier to merge with the new client | Relevant only if Horus uses one third-party object. Otherwise ignore, or reject with a clear error | ⏳ |

**Body: `ClientItemIn`**

| Chift field | Req | Type | Meaning [F] | Mapping considerations [D] | Horus |
|---|---|---|---|---|---|
| `name` | ✔ | string | Full or legal name displayed in the software | Max length? For individuals, does Horus build the name from first + last? | ⏳ |
| `is_company` | | bool (default true) | Company vs individual | Horus may have a type enum or separate person/company models (`TRANSFORM`) | ⏳ |
| `first_name`, `last_name`, `function`, `company_id` | | string | Only for individuals | `company_id` = the linked company: does Horus support contact persons under a company? | ⏳ |
| `external_reference` | | string | Caller's own ID | Does Horus have a free "external ID" field? If not, the reference is lost and duplicate detection becomes harder | ⏳ |
| `vat` | | string | VAT number; "reliable identifier to match clients" | Format/validation (country prefix?); use for a duplicate check | ⏳ |
| `company_number` | | string | National company number | Separate field in Horus? | ⏳ |
| `email`, `phone`, `mobile`, `website` | | string | Contact data | Usually `DIRECT`; check whether these sit on the client or on the address | ⏳ |
| `language` | | string | ISO 639-1 | Horus language enum? (`TRANSFORM`) | ⏳ |
| `currency` | | string | e.g. EUR | ISO 4217 vs Horus code (`TRANSFORM`/`LOOKUP`) | ⏳ |
| `iban`, `bank_account` | | string | Bank details (input) | Separate bank sub-resource? (multi-call). The output uses `bank_accounts[]` | ⏳ |
| `active` | | bool (default true) | Active flag | Archive flag in Horus? | ⏳ |
| `internal_notes` | | string | Notes | Free-text field? | ⏳ |
| `account_number` | | string | Receivable ledger account as in official exports | Dedicated vs shared control account; auto-assigned by Horus? | ⏳ |
| `addresses[]` | ✔ | array | List of addresses | One or many addresses in Horus? Typed? | ⏳ |
| ↳ `address_type` | ✔ | main / delivery / invoice | | Map to the Horus address type. If Horus has a single address → use `main`, and drop or flag the others | ⏳ |
| ↳ `street`, `number`, `box` | street ✔ | string | | Does Horus split the house number and box, or use a single line? (`TRANSFORM`: concatenate or split) | ⏳ |
| ↳ `postal_code`, `city` | ✔ | string | | `DIRECT` expected | ⏳ |
| ↳ `country` | ✔ | ISO 3166-1 | | Alpha-2 vs Horus code (`TRANSFORM`/`LOOKUP`) | ⏳ |
| ↳ `name`, `phone`, `mobile`, `email` | | string | Per-address contact data | Supported per address? | ⏳ |

**Response: `ClientItemOut`** (what the connector must return)

| Chift field | Source [D] | Horus |
|---|---|---|
| `id` | Horus client ID (cast to string) | ⏳ |
| `last_updated_on` | Horus modification timestamp. If absent → null | ⏳ |
| `third_party_account` | Horus third-party code/number | ⏳ |
| `bank_accounts[]` (`is_primary`, `currency`, `iban`, `bic_swift`, `account_number`, `routing_code`) | Horus bank details | ⏳ |
| all input fields echoed | from the Horus object (GET after POST if needed) | ⏳ |

### 6.2 Invoice creation: `POST …/accounting/invoices/multi-analytic-plans`

**Why the "multiple plans" variant [F]:** comparing the spec's two request schemas (`InvoiceItemInMonoAnalyticPlan` vs `InvoiceItemInMultiAnalyticPlans`), the header fields are identical. The **only** difference is on the line: single-plan has `analytic_account` ("Analytic account in the default analytic plan"), and multi-plan has `analytic_distribution` (several plans with percentage splits). [D] So the multi-plan route is the superset. If Horus has one analytic axis, it's a special case of it.

**Query parameters**

| Chift parameter | Req | Type / default | Meaning [F] | Mapping considerations [D] | Horus |
|---|---|---|---|---|---|
| `folder_id` | | string | Legal entity | → Horus company scope | ⏳ |
| `force_financial_period` | | `mmYYYY` | Book into this period instead of the current one | Does Horus accept an explicit period or bookyear on creation? If not → unsupported (error) | ⏳ |
| `regroup_lines` | | bool, default **true** | Regroup lines by account number, tax code and analytic distribution | Chift-side preprocessing; reduces line count (useful if Horus limits lines) | n/a (Chift) |
| `ignore_accounting_id` | | bool, default false | Don't wait for processing; the output may differ | Relevant if Horus creates asynchronously or needs a read-back to get the ID | ⏳ |
| `force_currency_exchange` | | bool, default false | Use the provided rate instead of the software's rate | Can a rate be passed to Horus? | ⏳ |

**Header: `InvoiceItemInMultiAnalyticPlans`**

| Chift field | Req | Type | Meaning [F] | Mapping considerations [D] | Horus |
|---|---|---|---|---|---|
| `invoice_type` | ✔ | customer_invoice / customer_refund / supplier_invoice / supplier_refund | Type | Drives the sales vs purchase endpoint/journal and the refund handling (`TRANSFORM`). [?] Refund sign convention on input isn't specified | ⏳ |
| `invoice_number` | | string | Internal number; auto-generated if empty; recommended for idempotency | Can the number be supplied, or is it always auto-numbered? Is uniqueness enforced? | ⏳ |
| `currency` | ✔ | ISO code | Invoice currency | `DIRECT`/`TRANSFORM` | ⏳ |
| `currency_exchange_rate` | | number, default 1 | Required when the currency ≠ the folder currency | Can a rate be set? | ⏳ |
| `untaxed_amount`, `tax_amount`, `total` | ✔ | number | Header totals; total = untaxed + tax | Does Horus take totals or compute them from lines? A mismatch → rounding (see `invoice_correction`) | ⏳ |
| `invoice_date` | ✔ | date | Accounting date | `DIRECT` | ⏳ |
| `due_date` | ✔ | date | Due date | Single due date vs payment-term schedule in Horus | ⏳ |
| `delivery_date` | | date | Tax-point date when it differs | Supported? | ⏳ |
| `start_date`, `end_date` | | date | Accrual/deferral period | Supported? Otherwise drop and flag | ⏳ |
| `partner_id` | | string | Client/supplier ID in the software | `LOOKUP` (must exist). [?] Optional in the schema: what happens if it's empty? | ⏳ |
| `partner_info` (`account_number`\*, `account_name`\*) | | object | Create the partner during invoice creation, for tools that can't create partners by API | Only needed if Horus can't create partners | ⏳ |
| `journal_id` | | string | Auto if there's only one journal, otherwise an error | `LOOKUP` via journals | ⏳ |
| `reference` | | string | Free reference (purchases: the supplier's invoice number) | Free field in Horus? | ⏳ |
| `payment_communication` | | string | Payment reference (e.g. a structured communication) | Format validation in Horus? | ⏳ |
| `customer_memo` | | string | Note | Free field? | ⏳ |
| `payment_term_id` | | string | Payment term ID | `LOOKUP` | ⏳ |
| `payment_method_id` | | string | Expected payment method | `LOOKUP` / N/A | ⏳ |
| `status` | | draft / posted (default posted) | Finalised or not | Does Horus support drafts? | ⏳ |
| `pdf`, `pdf_name` | | base64 / string | Attachment | Separate upload endpoint? Size limits? | ⏳ |
| `withholding_tax` (`tax_rate`\*, `tax_code`\*, `tax_amount`\*) | | object | Negative for normal withholding | Country-specific; likely N/A unless Horus supports it | ⏳ |
| `invoice_correction` (sale/purchase correction tax codes, credit/debit account numbers) | | object | Adds a rounding correction line | The connector adds an extra line if Horus's computed total ≠ the given total | ⏳ |
| `nl_payment_terms_split` (`g_account`, `n_account`) | | object | "NL only": Dutch G/N account split | Relevance depends on Horus's market coverage [?] | ⏳ |
| `shipping_country` | | ISO 3166-1 | Shipping country | Relevant to VAT (EU)? | ⏳ |
| `lines[]` | ✔ | array | Invoice lines | See below | ⏳ |

**Lines: `InvoiceLineItemInMultiAnalyticPlans`**

| Chift field | Req | Type | Meaning [F] | Mapping considerations [D] | Horus |
|---|---|---|---|---|---|
| `line_number` | | int, default 1 | Order | `DIRECT` or ignored | ⏳ |
| `description` | | string | Line text | Length limit? | ⏳ |
| `quantity`, `unit_price` | ✔ | number | Quantity and unit price excl. tax | Does an accounting entry in Horus even carry quantity/price, or only amounts? | ⏳ |
| `unit_of_measure` | | string | Default unit list; custom units must match by name | Likely N/A for an accounting entry [A] | ⏳ |
| `untaxed_amount`, `tax_amount`, `total` | ✔ | number | Line amounts | Which ones does Horus take? Recomputed? | ⏳ |
| `tax_rate` | ✔ | number (e.g. 21.0) | Rate in percent | Redundant with `tax_code`; use it for validation | ⏳ |
| `tax_code` | ✔ | string | **ID** of the VAT code in the software | `LOOKUP` via Get VAT codes (**a dependency outside the case's list**) | ⏳ |
| `account_number` | ✔ | string | General ledger account (e.g. 701000) | Number or internal ID in Horus? (`DIRECT` vs `LOOKUP`) | ⏳ |
| `analytic_distribution[]` | | array | Per plan | Is analytics supported? Multi-axis? | ⏳ |
| ↳ `analytic_plan` | ✔ | string | Plan ID | `LOOKUP` | ⏳ |
| ↳ `analytic_accounts[]` (`analytic_account`\*, `percentage`\*) | ✔ | array | Whole-number % summing to 100 per plan | Horus in % or in amounts? If amounts → compute % × untaxed, then handle rounding | ⏳ |

**Response: `InvoiceItemOutMultiAnalyticPlans`.** The connector must return at least `id`, the echoed fields, `status`, `partner_id` and `lines`, plus ideally `attachments_info` and `last_updated_on`. This is a reason for a read-back after creation.

**Validations to consider [D]:**
- Header and line totals: `total = untaxed_amount + tax_amount`.
- The sum of lines matches the header (± rounding; otherwise `invoice_correction`).
- Analytic percentages are integers and sum to 100 per plan.
- An exchange rate is present when the currency ≠ the folder currency.
- A journal is given when more than one exists.

**Spec wording to note [F]:** the line `tax_amount` is described as "untaxed_amount * tax_rate", but `tax_rate` is a percentage (e.g. 21.0). [D] The intended formula is untaxed × rate / 100. This is a minor doc nit.

### 6.3 Outstanding items: `GET …/accounting/outstandings`

**Query parameters**

| Chift parameter | Req | Type / default | Meaning [F] | Mapping considerations [D] | Horus |
|---|---|---|---|---|---|
| `type` | ✔ | client / supplier | Receivables vs payables | → the Horus customer vs supplier open-items source | ⏳ |
| `unposted_allowed` | ✔ | "true"/"false" | Include unposted (draft) items | Does Horus distinguish posted/draft? If there's no draft concept, the parameter has no effect | ⏳ |
| `folder_id` | | string | Legal entity | Company scope | ⏳ |
| `page`, `size` | | 1 / 50 | Pagination | Native, or emulated after computing open items? | ⏳ |

**Response: `OutstandingItem`**

| Chift field | Req | Meaning [F] | Mapping considerations [D] | Horus |
|---|---|---|---|---|
| `id` | ✔ | ID of the outstanding item | Invoice/entry ID, or an entry-line ID? | ⏳ |
| `number` | | Invoice / journal entry / financial entry number | `DIRECT` | ⏳ |
| `journal_id`, `journal_type` | ✔ | Journal and its type (enum) | `journal_type` via the journal-type mapping (`LOOKUP` + `TRANSFORM`) | ⏳ |
| `date` | ✔ | Accounting date | `DIRECT` | ⏳ |
| `due_date` | | Due date | `DIRECT` | ⏳ |
| `due_dates[]` (`due_date`\*, `amount`\*, `payment_method`, `payment_method_id`) | | All due dates (instalments) | Does Horus support instalment schedules? Otherwise a single element | ⏳ |
| `currency`, `currency_exchange_rate` | ✔ | Currency and rate | Rate needed when the currency ≠ the folder currency; 1 otherwise | ⏳ |
| `amount` | ✔ | Total amount | Sign convention? [?] | ⏳ |
| `open_amount` | ✔ | Remaining open amount | **`COMPOSITE`** if Horus only gives totals + payments: total − matched amounts | ⏳ |
| `partner_id` | ✔ | Customer, supplier or employee | `DIRECT` (Horus third-party ID) | ⏳ |
| `account_number` | ✔ | Ledger account of the item | Receivable/payable account | ⏳ |
| `reference`, `payment_communication` | | Free reference; payment communication | `DIRECT` if available | ⏳ |
| `matching_numbers[]` | | Matching operations applied | Does Horus expose a matching or lettering code? | ⏳ |
| `posted` | ✔ | Finalised? | Draft concept in Horus? | ⏳ |
| `original_document` (`id`, `number`, `journal_id`, `journal_type`, `date`, `due_date`, `reference`) | | Original item when brought forward from a previous bookyear | Does Horus keep a link from the opening entry to the original invoice? If not → null, and flag it | ⏳ |

**Likely implementation patterns, ranked by preference [D]:**
1. Horus has a native "open items / aged balance per partner" endpoint → ✅ (1 call + journal mapping).
2. Horus exposes invoices with an open/paid amount → 🟡 (invoices + filter on open > 0, plus partner and journal lookups).
3. Horus only exposes entries + matching → 🟡/🔴 (rebuild open items from entry lines and matching; heavy and error-prone).
4. No matching data at all → 🔴 for `open_amount` accuracy.

---

## 7. Cross-cutting checklist for the Horus docs ("General principles" section first)

The case links directly to `#introduction/general-principles` `[Case]`. [D] That page probably defines the rules that apply to every route, so read it first.

| Topic | Question | Why it matters |
|---|---|---|
| Authentication | API key or OAuth2? Per user, per accountant, or per company? Token lifetime? | Defines Chift's activation flow and how credentials are stored per consumer |
| Multi-company | Is the company/dossier a path parameter, a header, or bound to the credential? | Folder mapping (5.7) and the `folder_id` parameter on every route |
| Pagination | Style (page/offset/cursor)? Total count returned? Max page size? | Building Chift's `{items,total,page,size}` |
| Filtering | Date range, modified-since, journal, type? | `updated_after`, `date_from/to`, `journal_ids` (native vs emulated) |
| Rate limits | Requests per minute? | Composite routes multiply calls |
| Write capabilities | Which resources accept POST? Partners, accounts, entries? | Decides write-route feasibility (5.1, 5.3, 5.5, 5.8) |
| IDs | Numeric or uuid? Stable? | Chift IDs are strings → cast |
| Formats | Dates, decimals, country/language/currency codes | `TRANSFORM` rules |
| Errors | Error format, validation messages | Translating to Chift's error model (`ChiftError`: `message`, `status`, `detail`, `error_code`) |
| Sync vs async | Are entries created immediately or queued? | `ignore_accounting_id`, read-back |
| Attachments | Upload/download endpoints, size limits | `pdf`, `attachments_info` |
| Environments | Sandbox? Versioning or deprecation policy? | Testing and maintenance cost |

---

## 8. Gaps, ambiguities and edge cases

**Blocking gap**
- **[?] Horus API documentation is not accessible**, so all Horus mappings and verdicts are pending.

**Chift-side ambiguities, worth asking Chift about (shows rigour)**
1. **[?]** Refund amounts on creation: positive values with `invoice_type = *_refund`, or negative? Not stated in the request schema.
2. **[?]** When the target can't provide a field: return `null`, a default (e.g. `balance` = 0), or an `unknown` enum value? [F] Several enums include `unknown` (`JournalType`, `approval_status`, `attachments_info.status`), which suggests a convention.
3. **[?]** When the target doesn't support a parameter (e.g. `force_financial_period`, `force_merge`): ignore it silently, or return an error?
4. **[?]** The idempotency mechanism (the Developer Guide wasn't accessible).
5. **[F]** Doc nits: `FolderItem.main_currency` "ISO 3166-1" vs ISO 4217; line `tax_amount` formula without /100.
6. **[F]** `partner_id` is listed as required but nullable in the invoice *output* schema. Clarify the expectation when the target has no partner on an entry.

**Edge cases to test once Horus is known [D]**

| Area | Edge case | Expected handling (to validate) |
|---|---|---|
| Client | Client already exists as a supplier | `force_merge`, or a duplicate check on VAT |
| Client | Individual (no company) | first/last name mapping |
| Client | Delivery + invoice + main addresses, but Horus allows only one | Keep `main`, flag the loss |
| Invoice | Foreign currency | Rate required; `force_currency_exchange` |
| Invoice | Several VAT rates; reverse-charge or exempt codes | Correct `tax_code` lookup per line |
| Invoice | Analytic split 33/33/34 when Horus stores amounts | Rounding rule; which line absorbs the cent |
| Invoice | Header ≠ sum of lines (rounding) | `invoice_correction` line |
| Invoice | Date in a closed period or bookyear | Error, or `force_financial_period` |
| Invoice | Several journals and no `journal_id` | Error (Chift rule [F]) |
| Invoice | Retry after a timeout | Idempotency via `invoice_number` |
| Invoice | PDF too large / upload fails after the entry was created | Partial success: what to return? |
| Misc. operation | Unbalanced lines | Horus validation error → mapped to `ChiftError` |
| Outstandings | Partial payments; instalments | `open_amount`, `due_dates[]` |
| Outstandings | Item carried over from the previous bookyear | `original_document` |
| Lists | No total count in Horus | Compute it, at a cost |
| All | Expired credentials / rate limit hit | Clear error, retries with backoff |

---

## 9. How to complete the Horus side (step by step, once the docs are readable)

1. Read **General principles** and fill §7 (auth, company scoping, pagination, errors, limits).
2. List every Horus resource and its methods (GET/POST/PUT) in a two-column inventory.
3. For each Chift route in §5: find the Horus resource(s), note the call sequence, and set a verdict.
4. For the 3 routes in §6: fill the Horus column field by field, with a classification code.
5. For each 🟡/🔴: write the limitation in client language ("Horus does not expose X; the connector will return null / reject the request").
6. Re-check §8 edge cases against what Horus actually supports.
7. Only then write the external HTML report.

---

## 10. What to communicate to Chift, and what to clarify

**Communicate**
- The method (the 7 questions, verdict scale, field codes). It is reusable for any new connector.
- The route-level table with verdicts and the call sequence per route.
- The dependencies outside the requested list: **Get VAT codes** (needed for `tax_code`), supplier creation and lookup (needed for `partner_id` on purchase invoices), payment terms and methods (optional).
- Limitations, written in client language.
- Open questions for Horus and for Chift, kept separate.

**Clarify with Chift** (independent of Horus): the six items in §8 (Chift-side ambiguities), plus:
- MVP scope: which routes must be in v1?
- Is there a Horus partner contact or sandbox account, so the mapping can be validated against real responses?
- Are both invoice variants (single and multiple plans) expected from this connector?

---

## 11. Likely follow-up questions from Chift, with prepared answers

| Likely question | Prepared answer (reasoning) |
|---|---|
| "How did you approach an API you'd never seen?" | Contract first (Chift's required inputs and promised outputs), then the target's general principles (auth, scoping, pagination), then resource inventory → mapping → verdict → limitations. Same 7 questions for every route. |
| "Why do some routes need several Horus calls?" | Chift's response models combine data that targets often store separately. Chift's own spec anticipates this: lines and partner info are excluded by default "when this requires extra requests on the target API", and attachments can be `yes_to_request`. |
| "Why the multi-plan invoice route?" | The only schema difference is `analytic_distribution` vs `analytic_account` on the line, so the multi-plan route is the superset. A single-axis target is a special case. |
| "Why mention VAT codes when they weren't in the list?" | `tax_code` is required on every invoice line and is "the Id of the Tax Code in the accounting software". Invoice creation can't be used without a way to look the codes up. |
| "What if Horus doesn't support a field?" | Classify it as N/A, return null (or the agreed `unknown` value), document the limitation, and — for required write fields — reject with a clear error rather than silently dropping data. I would confirm Chift's convention (§8, Q2–3). |
| "What's the biggest risk?" | (Pending the Horus docs.) Based on the Chift contract alone: outstandings (they depend on matching state), analytic distribution (percentages vs amounts, number of axes), and multi-company scoping. |
| "How would you explain this to a client?" | "Chift speaks one standard language. For Horus we checked, for each standard request, whether Horus understands it directly, needs a few extra steps, or can't do it. Here is what works, what works with limits, and what we still need Horus to confirm." |
| "How confident are you?" | Chift side: high (read from Chift's own OpenAPI spec, to be re-checked against the live docs). Horus side: only as good as the Horus docs. I separate facts, deductions and assumptions explicitly. |
| "Performance concerns?" | N+1 patterns (analytic accounts per plan, folder details, invoice detail per row). Mitigate with the `include_*` flags (opt-in), `updated_after` if native, and caching reference data (journals, VAT codes, chart of accounts). |

---

## 12. Status and next steps

- ✅ Case read; Chift contracts for all 11 routes extracted and analysed (§5–§6; raw extract in the appendix).
- ⛔ Horus mapping blocked: `horussoftwareapi.docs.apiary.io` and `jsapi.apiary.io` are denied by the environment's network policy.
- ⏭️ Once the Horus docs are accessible: complete §5's Horus column and verdicts, fill §6's Horus column, update §8 and §11, then build the external HTML report.
