# Cross-route harmonisation decisions (binding for all route mappings)

These decisions resolve the inconsistencies found by the final critic. Apply every decision that touches your route. Where a decision depends on undocumented Horus behaviour, label the resulting rows "A" and keep or add the open question listed.

## D1. Credit notes and daybooks (create ↔ read round-trip)
- **Write (create_invoice):** keep the daybook auto-selection fallback. customer_invoice → [200]; customer_refund → [250], falling back to [200] if the folder has no 250 daybook; supplier_invoice → [100]; supplier_refund → [150], falling back to [100]. Refunds are posted with Type=1. Exactly one candidate daybook must remain, otherwise 400 'journal_id required'. The Horus guide does not tie Type to a daybook type, so keep the open question: "Can a credit note (Type 1) be posted into a 200/100 daybook, and an invoice into 250/150?"
- **Read (get_invoices):** ALWAYS scan both sibling daybook types (customer_* → 200 + 250; supplier_* → 100 + 150) and classify each entry by the partner-line sign. Customer side: a net debit on the customer line is an invoice and a net credit is a credit note. Supplier side: a net credit is an invoice and a net debit is a credit note. For open sales items, TransactionType (0 sale invoice / 1 sale credit note) overrides the sign. This classification is mandatory, not a safety net. Label it A until Horus confirms (or exposes the document Type on read). Call count: one book-entries.list per daybook of the two sibling types.
- **Journals (journals_folders):** state that credit notes may sit in 200/100 daybooks, so journal_type describes the daybook, not every entry in it.

## D2. One canonical synthetic VAT-code grammar
Horus has no VAT-code entity, so the connector owns a VAT catalogue built from the Horus accepted-combination files (not provided, so ask Horus for them). One id grammar, used identically by GET vat-codes, create_invoice (decode) and get_invoices (encode):
- Sales: `S-{TaxRate}-{TaxOrigin}-{TaxType}`, plus `-{TaxCountryCode}` only for OSS lines (TaxOrigin = 13). Example: `S-21-0-0`.
- Purchases: `P-{TaxRate}-{TaxOrigin}-{TaxType}-{TaxKind}-{TaxCondition}-{TaxConditionValue}`, with `x` for a component that is not used. Example: `P-21-2-0-0-1-true`.
- **Read rule:** build the id from VatDetail (VatRate, SaleTaxOrigin/PurchaseTaxOrigin, TaxType, TaxCountryCode, TaxCondition, TaxConditionValue) and return it only if exactly one catalogue entry matches. VatDetail has NO TaxKind, so when several purchase entries match (differing only by TaxKind), or none does, return tax_code = null and keep tax_rate/tax_amount. Never guess, and never return Horus VatCode as the Chift tax_code.
- Open questions to Horus: provide the accepted-combination files; can TaxKind be exposed on read (VatDetail)? Note that read-side TaxCondition has an extra value '4 = Article'.

## D3. Invoice header Comment convention (reference + customer_memo)
- **Write:** Horus header Comment = `{reference}` when only reference is set; `{reference} | {customer_memo}` when both are set; `| {customer_memo}` when only customer_memo is set (the leading separator means "no reference"). Separator = space, pipe, space. Label D for the rule. Comment length limits are undocumented (?).
- **Read (get_invoices, outstandings):** take the header comment, split on the first ` | `: left → reference (null if empty), right → customer_memo. Where the header Comment surfaces on read is undocumented. Read it from the partner-line Comment (account history) first, then book-entries RemarkCompany, then (open sales list) Remark, and label it A. Add the open question to Horus: "Where does the invoice header Comment surface on read (partner-line Comment, RemarkCompany, Remark)?"

## D4. Currency of amounts (one assumption everywhere)
- **Assumption (A, everywhere):** account-history Debit/Credit and book-entry CompanyDetail amounts are in the folder currency (EUR). Invoice-currency amounts are known only from (a) the write echo on create, or (b) TotalCurrencyAmount / OpenCurrencyAmount on invoices.sales.outstanding.list.
- **Rule:** never pair EUR amounts with a foreign currency code. For a foreign-currency document where invoice-currency amounts are not available, return the amounts in EUR with currency = 'EUR' and currency_exchange_rate = 1, flag it as a limitation, and keep the open question "Direction and meaning of CurrencyRate; currency of CompanyDetail amounts". accounting_info.main_currency_total = the EUR partner-line amount.
- Applies to get_invoices, outstandings (supplier lines and client fallback lines) and create_invoice (response rebuilding).

## D5. Sign convention for outstanding items
- Customer lines (AccountType 100): amount = Debit − Credit; match-group residual = Σ(Debit − Credit).
- Supplier lines (AccountType 200): amount = Credit − Debit; residual = Σ(Credit − Debit).
- Positive therefore means "owed": receivable for clients, payable for suppliers. Rows taken from invoices.sales.outstanding.list are already in the receivable view (invoice +, payment −). Apply the same side-based formula in every client and supplier path (primary, reconciliation lines, fallbacks). Open question to Chift: the expected sign convention for OutstandingItem.amount/open_amount.

## D6. One daybook Type → Chift journal_type table (shared by all routes)
| Horus daybook Type | Chift journal_type | Label | API posting endpoint documented? |
|---|---|---|---|
| 100 Purchase | supplier_invoice | D | yes (invoices.purchases.new) |
| 150 PurchaseCreditNote | supplier_refund | D | yes (invoices.purchases.new) |
| 200 Sale | customer_invoice | D | yes (invoices.sales.new) |
| 250 SaleCreditNote | customer_refund | D | yes (invoices.sales.new) |
| 500 Bank | financial_operation | D | yes (book-entries.banks.new) |
| 590 Financial | financial_operation | D | yes (book-entries.financials.new) |
| 550 Cash | financial_operation | A | not documented |
| 600 MiscOperation | miscellaneous_operation | D | yes (book-entries.miscellaneous-operations.new) |
| 610 TemporaryMiscOperation, 690 SystemMiscOperation, 700 CostMiscOperation | miscellaneous_operation | A | not documented |
| 900 Budget, 990 External, 0 Undefined, unknown future values | unknown | A | no |
- Get journals: blocked = true for every type without a documented API posting endpoint (550, 610, 690, 700, 900, 990, 0), labelled A.
- create_misc_operation auto-selects and validates only Type 600, which matches the blocked flag.

## D7. One folder_id rule (every route)
folder_id is required whenever the connection has more than one selected folder. If exactly one folder was selected at activation, use it. If no selection is stored, use the single folder returned by POST /folders.list {Mode: 0}. Otherwise return 400 'folder_id required'. Horus 403 → Chift 400 'folder not accessible with this connection'.

## D8. Analytics: one cache, one rounding rule, one Free-schema policy
- One per-folder cache: POST /cost-schemas.list, plus POST /cost-sections.list per List-type schema with Filter.IncludeInactive = true. Write routes (create_invoice, create_misc_operation) reject an inactive section with 422 and resolve schema/section search keys only from this folder-scoped cache (no per-call cost-sections.info / cost-schemas.info).
- Chift ids: analytic_plan = cost schema GUID Id; analytic_account = cost section GUID Id. Posting converts them to SchemaSearchKey / Value (section SearchKey) through the cache.
- Rounding: percentages → amounts use the largest-remainder method on the per-line product allocation, so the cost lines sum exactly to the line BaseAmount (cross-cutting convention aligned to this).
- Free schemas (CostSectionType 900): excluded from Chift analytics in v1. They are not returned by Get analytic plans/accounts, not accepted on write, and omitted on read (flag a warning). Keep the open question.

## D9. One shared Horus company → Chift partner mapper
Used identically by the create_client response, the get_invoices partner and the create_invoice partner:
- active = NOT CustomerActivitySuspended (A; meaning undocumented); otherwise true. Beneficiary flags are ignored (beneficiaries are out of scope).
- addresses = one 'main' address built from Address (+Address2), ZipCode, Locality, CountryCode; address-level phone/email = null (company phone/email are returned at root: phone = ContactPhone, email = ContactEmail).
- is_company = true (Chift default; Horus does not store it, so disclose this as data loss).
- language = lowercase Horus Language for FR/NL/DE/EN/ES/PT; 'XX' → null.
- third_party_account = company SearchKey; account_number = CustomerConcentrationAccount (or SupplierConcentrationAccount for suppliers) resolved to the account SearchKey.
- **Write-side language fallback (everywhere):** a Chift language outside the Horus company enum → the folder language from folders.info (which may be 'XX').

## D10. partner_info in create_invoice
- partner_info.account_number has no description in the Chift spec. Treat it as the Horus company SearchKey (A) and add the [Chift] open question "What does partner_info.account_number mean: a third-party code or a ledger account?"
- Apply create_client's SearchKey rules (sanitise; must be unique within the folder). If a company with that exact SearchKey exists, reuse it only if it is in the same folder. If it lacks the role flag needed for the invoice side (IsCustomer for customer_*, IsSupplier for supplier_*), set the flag with companies.update (force_merge logic, never "" values). Otherwise create it with companies.new using create_client's required-field rules.

## D11. Verdict calibration (stated once in the report)
- **Supported:** one native Horus endpoint (plus cached reference data) serves the route with deterministic field transformations; no Chift behaviour must be emulated; losses are limited to minor optional fields.
- **Supported with workaround:** feasible, but needs extra per-request calls (read-backs, joins, N+1), emulated filters/pagination/numbering, or loses a capability or field that clients typically rely on.
- **Not supported:** no Horus capability. **To confirm:** documentation insufficient.
- Consequence: create_misc_operation becomes **workaround** (non-EUR operations and non-numeric numbers cannot be posted, line_number is dropped, and a read-back is needed when Horus generates the number). Folders and analytic plans stay supported.

## D12. Posting status and duplicate checks (both write routes)
- Chift status 'draft' → Confirmed = false. Chift 'posted' (the Chift default) → Confirmed = true, with a per-consumer setting "always push unconfirmed" (recommended where the accountant must review API entries). Both behaviours are possible in Horus. Which default fits fiduciary clients is a Chift/Horus product decision, so keep the open question.
- Duplicate pre-check: whenever an invoice_number / operation_number is supplied, run POST /book-entries.list (FolderId, DaybookId, fiscal-year period, Filter.DocumentNo) before creating. On a timeout or 500, check before retrying (never blind-retry; Horus has no idempotency key).

## D13. Cross-folder guard on Id-only calls
Every Id-only call must verify the folder: companies.info → Data.Folder.Id, book-entries.info → Data.Folder.Id, daybooks.info → Data.Folder.Id = folder_id. Otherwise return 400. Analytics are resolved only from the folder-scoped cache (D8).

## D14. create_invoice daybook row
Rewrite the daybooks.list endpoint role to the per-invoice_type filter of D1 (no "exactly one of 200/250" wording).

## D15. Endpoint count
The Horus reference has **72** endpoints (including GET /book-entries.info). Replace any "71".
