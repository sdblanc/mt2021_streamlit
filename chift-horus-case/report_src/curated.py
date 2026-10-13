"""Curated narrative for the external report (filled from the harmonised mapping data)."""

TASK_B = ['create_client', 'create_invoice', 'outstandings']

CARD_META = {
    'create_client': {'one_line': 'Native creation with companies.new. The connector generates the Horus search key, derives required flags, and reads the company back to build the Chift response.', 'title': 'Client creation', 'paths': 'POST /consumers/{consumer_id}/accounting/clients'},
    'get_invoices': {'one_line': 'Horus has no invoice list. Invoices are rebuilt from book entries, account history lines and open-item data, with pagination and day-level filters emulated.', 'title': 'Invoice retrieval (multiple analytic plans)', 'paths': 'GET /consumers/{consumer_id}/accounting/invoices/multi-analytic-plans/type/{invoice_type}'},
    'create_invoice': {'one_line': 'Native creation with invoices.sales.new or invoices.purchases.new, PDF included. VAT codes, analytics and numbering need connector logic; the entry is read back after creation.', 'title': 'Invoice creation (multiple analytic plans)', 'paths': 'POST /consumers/{consumer_id}/accounting/invoices/multi-analytic-plans'},
    'journals_folders': {'title': 'Journal retrieval and accounting folders retrieval', 'paths': 'GET …/accounting/journals · GET …/accounting/folders',
                         'one_line': 'Folders map almost one to one onto folders.list. Journals come from daybooks.list, with the counterpart account looked up in the chart of accounts and next document numbers only emulated.'},
    'ledger_accounts': {'title': 'Ledger account creation and chart of accounts retrieval', 'paths': 'POST …/accounting/accounts · GET …/accounting/chart-of-accounts',
                        'one_line': 'accounts.new and accounts.list are native, but the Chift account type cannot be written and must be computed on read; type filtering and pagination are emulated.'},
    'misc_operation': {'one_line': 'Native creation of a balanced debit/credit operation. EUR only and numeric numbers only; the entry is read back after creation.', 'title': 'Miscellaneous operation creation', 'paths': 'POST /consumers/{consumer_id}/accounting/miscellaneous-operation'},
    'analytics': {'title': 'Analytic plans retrieval and analytic accounts retrieval (multiple plans)', 'paths': 'GET …/accounting/analytic-plans · GET …/accounting/analytic-accounts/multi-analytic-plans',
                  'one_line': 'Cost schemas are analytic plans (one call). Cost sections are analytic accounts, listed with one call per schema; balances are not stored and can only be computed over a period.'},
    'outstandings': {'one_line': 'Folder-level open items exist on both sides, but the client and supplier paths differ; supplier open amounts are computed from matching groups.', 'title': 'Outstanding items (customers and suppliers)', 'paths': 'GET /consumers/{consumer_id}/accounting/outstandings'},
}

OVERVIEW = [
    {'route': 'Client creation', 'chift': 'POST /accounting/clients', 'group': 'create_client', 'match': 'Create client',
     'endpoints': ['POST /companies.new', 'GET /companies.info, POST /ibans.list (read-back)', 'POST /companies.list (duplicate checks)', 'POST /companies.update, POST /ibans.new (force_merge)'],
     'pattern': 'Check → create → read back'},
    {'route': 'Invoice retrieval (multiple plans)', 'chift': 'GET /accounting/invoices/multi-analytic-plans/type/{invoice_type}', 'group': 'get_invoices', 'match': 'Get invoices',
     'endpoints': ['POST /daybooks.list (cached)', 'POST /book-entries.list (per daybook)', 'POST /account-histories.list (lines, VAT, analytics, matching)', 'POST /invoices.sales.outstanding.list (sales payments)', 'GET /book-entries.info (single invoice)'],
     'pattern': 'Rebuild invoices from the ledger'},
    {'route': 'Invoice creation (multiple plans)', 'chift': 'POST /accounting/invoices/multi-analytic-plans', 'group': 'create_invoice', 'match': 'Create sale/purchase',
     'endpoints': ['POST /invoices.sales.new or /invoices.purchases.new', 'Cached lookups: daybooks, accounts, cost schemas/sections, fiscal years', 'POST /book-entries.list (duplicate check)', 'GET /book-entries.info (read-back)'],
     'pattern': 'Resolve → check → create → read back'},
    {'route': 'Journal retrieval', 'chift': 'GET /accounting/journals', 'group': 'journals_folders', 'match': 'Get journals',
     'endpoints': ['POST /daybooks.list', 'POST /accounts.list (counterpart account, cached)'], 'pattern': 'List + lookup'},
    {'route': 'Ledger account creation', 'chift': 'POST /accounting/accounts', 'group': 'ledger_accounts', 'match': 'Create ledger account',
     'endpoints': ['POST /accounts.new', 'POST /accounts.list (duplicate check)', 'GET /accounts.info (read-back)'], 'pattern': 'Check → create → read back'},
    {'route': 'Chart of accounts retrieval', 'chift': 'GET /accounting/chart-of-accounts', 'group': 'ledger_accounts', 'match': 'chart of accounts',
     'endpoints': ['POST /accounts.list', 'POST /daybooks.list (account type derivation, cached)'], 'pattern': 'List + derive'},
    {'route': 'Accounting folders retrieval', 'chift': 'GET /accounting/folders', 'group': 'journals_folders', 'match': 'Get Folders',
     'endpoints': ['POST /folders.list (Mode 0)', 'GET /folders.info (country, optional)'], 'pattern': 'List'},
    {'route': 'Miscellaneous operation creation', 'chift': 'POST /accounting/miscellaneous-operation', 'group': 'misc_operation', 'match': 'miscellaneous',
     'endpoints': ['POST /book-entries.miscellaneous-operations.new', 'Cached lookups: daybooks, accounts, cost sections', 'GET /book-entries.info (read-back)'], 'pattern': 'Resolve → create → read back'},
    {'route': 'Analytic plans retrieval', 'chift': 'GET /accounting/analytic-plans', 'group': 'analytics', 'match': 'Analytic Plans',
     'endpoints': ['POST /cost-schemas.list'], 'pattern': 'List'},
    {'route': 'Analytic accounts retrieval (multiple plans)', 'chift': 'GET /accounting/analytic-accounts/multi-analytic-plans', 'group': 'analytics', 'match': 'analytic accounts',
     'endpoints': ['POST /cost-schemas.list', 'POST /cost-sections.list (once per schema, max 8)', 'POST /cost-histories.list (balances, optional)'], 'pattern': 'Loop over plans + merge'},
    {'route': 'Outstanding items (Task B only)', 'chift': 'GET /accounting/outstandings', 'group': 'outstandings', 'match': 'outstanding',
     'endpoints': ['Clients: POST /invoices.sales.outstanding.list + POST /customers.outstanding', 'Suppliers: POST /suppliers.outstanding', 'POST /daybooks.list (journal ids and types, cached)', 'GET /book-entries.info (enrichment, optional)'],
     'pattern': 'Join + compute open amounts'},
]

BUILDING_BLOCKS = [
    {'name': 'Connection and token manager', 'what': 'Stores api_url, access token, single-use refresh token and expiry per Horus license. Refreshes proactively, one refresh at a time per connection, and persists the new token pair before use.', 'routes': 'All'},
    {'name': 'Folder resolution', 'what': 'One rule for every route: folder_id is required when the connection has several selected folders; otherwise the single selected folder is used.', 'routes': 'All'},
    {'name': 'Reference-data cache per folder', 'what': 'Daybooks, chart of accounts, cost schemas and sections (including inactive ones), fiscal years and folder settings. Loaded once and refreshed on a miss, as the Horus guide recommends.', 'routes': 'All write routes, invoices, journals, chart of accounts, outstanding items'},
    {'name': 'Pagination and filter emulation', 'what': 'Horus lists return everything. The connector fetches, filters by day, type or status, sorts deterministically and slices Chift pages, with a short-lived cache so consecutive pages do not refetch.', 'routes': 'All list routes'},
    {'name': 'VAT-code catalogue', 'what': 'Connector-owned list of valid Horus tax combinations with one id grammar (<code>S-21-0-0</code>, <code>P-21-2-0-0-1-true</code>). Serves Chift VAT codes, decodes tax_code on write and encodes it on read.', 'routes': 'Invoice creation, invoice retrieval, VAT codes'},
    {'name': 'Analytics converter', 'what': 'Turns Chift per-plan percentages into Horus cost lines (amounts on combinations of cost sections) with largest-remainder rounding, and back.', 'routes': 'Invoice creation and retrieval, miscellaneous operations'},
    {'name': 'Shared partner mapper', 'what': 'One mapping from a Horus company to a Chift client/supplier/partner, reused by every route that returns partner data.', 'routes': 'Client creation, invoices'},
    {'name': 'Duplicate protection', 'what': 'Search before create (VAT number, external reference, document number) and check before retrying after a timeout or server error, because Horus has no idempotency key.', 'routes': 'All write routes'},
    {'name': 'Error translation', 'what': 'Maps Horus status codes and ErrorType/Details to Chift errors; never forwards tokens.', 'routes': 'All'},
]

ERROR_MAP = [
    ('401 Unauthorized', 'Refresh the token once (serialised per connection) and replay the call. If the refresh fails, mark the connection as disconnected.', 'Re-authorisation needed when the refresh fails'),
    ('400 Bad Request <code>{ErrorType, Details, Message}</code>', 'Do not retry as-is. Use connector pre-checks to return specific errors (for example an existing client); otherwise pass Details through.', '400, or 422 for validation done by the connector'),
    ('403 Forbidden', 'The folder or resource is not accessible with this connection.', '400 “folder not accessible with this connection”'),
    ('404 Not Found', 'Unknown id (for example a force_merge supplier or a replaced book entry).', '400 or 404, depending on the route'),
    ('500 / timeout on a read', 'Retry with exponential backoff, as Horus advises.', 'Error after retries'),
    ('500 / timeout on a create', 'Never retry blindly. Search for the record first (external reference, VAT number, document number), and re-post only if nothing is found.', 'Created record, or an error'),
]

DECISIONS = [
    ('D1', 'Credit notes: on write, use the credit-note daybook (250/150), falling back to the sales/purchase daybook (200/100). On read, always scan both daybook types and classify each entry as invoice or credit note from the customer/supplier line.', 'Credit notes posted in a sales daybook (by the connector or by an accountant) must still come back as refunds.'),
    ('D2', 'One synthetic VAT-code id grammar for writing, reading and the VAT-code list: <code>S-{rate}-{origin}-{type}</code> for sales, <code>P-{rate}-{origin}-{type}-{kind}-{condition}-{value}</code> for purchases. On read, return a code only when exactly one catalogue entry matches.', 'Horus has no VAT-code entity, and the purchase “kind” cannot be read back.'),
    ('D3', 'reference and customer_memo share the Horus invoice comment as <code>{reference} | {customer_memo}</code>, split the same way on read.', 'Horus has a single free-text comment on invoices.'),
    ('D4', 'Ledger amounts are treated as folder currency (EUR). EUR amounts are never returned with a foreign currency code.', 'The currency of ledger amounts is not documented.'),
    ('D5', 'Outstanding amounts are signed by side: debit minus credit for customers, credit minus debit for suppliers (positive means owed).', 'One consistent sign per side across all code paths.'),
    ('D6', 'One daybook-type to journal-type table for all routes. Daybook types without a documented posting endpoint are exposed as blocked.', 'Journals, invoices, operations and outstanding items must agree.'),
    ('D7', 'folder_id is required when a connection has several selected folders.', 'Accounting-firm licenses hold many folders.'),
    ('D8', 'One analytics cache per folder, largest-remainder rounding, and “free” cost schemas excluded in v1.', 'Free schemas have no listable values.'),
    ('D9', 'One shared mapping from a Horus company to a Chift partner.', 'The same company must look the same in every route.'),
    ('D10', 'partner_info on invoice creation reuses the client-creation rules (search key, role flags).', 'Avoid duplicate or half-configured companies.'),
    ('D11', 'Verdict calibration as defined in section 2.', 'Comparable verdicts across routes.'),
    ('D12', '“draft” → unconfirmed; “posted” → confirmed, with a per-consumer option to always push unconfirmed. Duplicate check on the document number before every create.', 'Accountant review is the Horus default for API entries.'),
    ('D13', 'Every call by id checks that the object belongs to the requested folder.', 'Calls by id take no folder, so an id from another folder of the same license would otherwise be accepted.'),
]

SUMMARY_LEDE = ('All eleven Chift routes in scope can be built on the Horus Software API, and none is blocked. '
                'Two map almost directly (folders and analytic plans). Nine need workarounds that the connector can absorb, at the cost of extra calls, '
                'emulated behaviour, or data loss that Chift should disclose to its clients. For most of them the core Horus capability is native; '
                'the workaround sits in the translation around it.')

KEY_FINDINGS = [
    '<b>Every object in scope exists in Horus, readable and writable where the case needs it:</b> third parties (“companies”), sales and purchase invoices, miscellaneous operations, accounts, daybooks, cost schemas and sections, folders and open items.',
    '<b>Creation calls return only an id.</b> Every write route needs a read-back (usually one <code>.info</code> call) to return the full Chift response, and duplicate checks before creating, because Horus has no idempotency key.',
    '<b>There is no “list invoices” endpoint.</b> Invoice retrieval rebuilds each invoice from book entries (headers) and account history lines (lines, VAT, analytics, matching), plus open-item data for payments. This is the clearest case of “one Chift route, several Horus endpoints”.',
    '<b>VAT is modelled differently.</b> Horus has no VAT-code entity: each line carries a rate, an origin and a type (plus kind and condition for purchases), and only listed combinations are valid. The connector needs its own VAT-code catalogue to serve Chift’s <code>tax_code</code> and VAT-code list.',
    '<b>No pagination and month-based periods.</b> Horus lists return everything for a folder or a month window, so the connector emulates Chift pagination and day-level date filters, and should cache reference data per folder.',
    '<b>Disclosed data loss:</b> one address per third party, no mobile, notes or person fields; no line quantity or unit price on invoices; the account type cannot be written; miscellaneous operations are EUR-only; analytic balances are not stored.',
]

RECOMMENDATION = ('Proceed with a Horus connector covering all eleven routes, built on a small set of shared components: '
                  'token and folder handling, a per-folder reference cache, pagination emulation, a VAT-code catalogue and an analytics converter. '
                  'Before building, settle the open questions with Horus that change the design, mainly the tax-combination files, credit-note daybooks, '
                  'document numbering, the currency of ledger amounts and rate limits, and get a test license, since the API works on live data.')

HORUS_INTRO = ('Horus Office is used by accounting firms (fiduciaries) and SMBs. The Horus Software API reads and writes the data of one Horus Office database. '
               'Three structural facts shape the connector: each license has its own database and API URL, almost every call is scoped to one folder, '
               'and accounting entries are created through business-specific endpoints (invoices, bank, financial, miscellaneous operations) that all return a book entry id.')

ROUTES_INTRO = ('The table answers Task A: for each Chift route, the Horus endpoints that implement it, the call pattern and the verdict. '
                'Each route card below gives the endpoints with their role and call count, the call sequence, the considerations specific to Horus and the key attribute mapping.')

TASK_B_INTRO = ('Each table lists every Chift attribute and query parameter of the route: the request side, and what the connector returns. '
                'Use the filter to find a field or show only one mapping type. The evidence column quotes the Horus documentation and can be hidden with the button in the sidebar.')

TASK_B_SUMMARY = {
    'create_client': 'A Chift client is a Horus <b>company</b> (third party) with IsCustomer = true, created with <code>companies.new</code> in the folder. Horus requires a search key, a VAT-liability flag, a language and a country that Chift does not always send, so the connector derives them. Creation returns only an id, so the connector reads the company back (company details, IBANs and the receivable account) to build the Chift response. Because one Horus company can be both customer and supplier, <code>force_merge</code> maps to flagging an existing supplier as customer.',
    'create_invoice': 'Customer invoices and refunds go to <code>invoices.sales.new</code>, supplier invoices and refunds to <code>invoices.purchases.new</code>, with Type 0 for an invoice and 1 for a credit note. The PDF can be sent in the same call (multipart). The connector first resolves the daybook, the partner, account search keys and cost sections from cached reference data, translates each Chift <code>tax_code</code> into the Horus VAT fields, converts analytic percentages into amounts, checks for an existing document number, and reads the entry back after creation.',
    'outstandings': 'Horus has folder-level open-item lists for both sides, but they differ. For clients, <code>invoices.sales.outstanding.list</code> gives open sales invoices with their open amount, joined with <code>customers.outstanding</code> for the account and matching details. For suppliers, only ledger lines are available (<code>suppliers.outstanding</code>), so the open amount is computed from matching groups. Pagination is emulated, and amounts are signed per side (positive means owed).',
}

TASK_B_EXTRA = {
    'create_invoice': '''<div class="note"><span class="note-title">Worked example: analytic distribution</span>
<p>Chift line: base amount 1,000.00; plan DEPARTMENT split 50 % SALES / 50 % SUPPORT; plan PROJECT 100 % ALPHA.</p>
<p>Horus cost lines (amounts on combinations of cost sections, summing to the line base amount):</p>
<div class="table-wrap"><table><thead><tr><th>Amount</th><th>DEPARTMENT</th><th>PROJECT</th></tr></thead>
<tbody><tr><td class="num">500.00</td><td>SALES</td><td>ALPHA</td></tr><tr><td class="num">500.00</td><td>SUPPORT</td><td>ALPHA</td></tr></tbody></table></div>
<p>Combinations are the product of the plan percentages. Rounding uses the largest remainder so the cost lines always sum exactly to the base amount. Deriving combinations from independent plan splits is an assumption Chift should validate (question C10).</p></div>
<div class="note"><span class="note-title">VAT: from Chift tax_code to Horus fields</span>
<p>The connector exposes Horus tax combinations as synthetic VAT codes, for example <code>S-21-0-0</code> = sale, 21 %, origin 0 (national sale), type 0 (national). On write the code is decoded into TaxRate, TaxOrigin and TaxType (plus TaxKind, TaxCondition and TaxConditionValue for purchases). The list of valid combinations comes from Horus reference spreadsheets that still need to be obtained (question H1).</p></div>''',
    'outstandings': '''<div class="note"><span class="note-title">Sign convention</span>
<p>Customer lines: amount = debit − credit. Supplier lines: amount = credit − debit. A positive amount is always owed (a receivable for clients, a payable for suppliers). Chift’s expected convention is question C5.</p></div>''',
}

DEPS_INTRO = ('Several requested routes depend on Chift routes outside the case list. Without them, a consumer cannot supply valid ids to the requested routes.')

DEPENDENCIES = [
    {'name': 'VAT codes (GET vat-codes)', 'why': 'Every invoice line requires <code>tax_code</code>, the id of a VAT code in the accounting software.', 'support': 'No VAT-code entity or endpoint. Served from a connector-owned catalogue of valid Horus tax combinations, with one id grammar shared with invoice creation and retrieval.', 'label': 'D'},
    {'name': 'Supplier creation (POST suppliers)', 'why': 'Purchase invoices need the supplier’s <code>partner_id</code>.', 'support': 'Native: <code>companies.new</code> with IsSupplier = true, same rules as client creation (search key, duplicate VAT check, read-back).', 'label': 'F'},
    {'name': 'Clients and suppliers lists (GET clients / suppliers)', 'why': 'Consumers look up existing partners before creating invoices.', 'support': '<code>companies.list</code> filtered on IsCustomer or IsSupplier; <code>updated_after</code> maps to ModifiedAfter. Chift’s free-text search (an OR over several fields) and pagination are emulated.', 'label': 'D'},
    {'name': 'Payment terms (GET payment-terms)', 'why': 'Optional <code>payment_term_id</code> on invoices.', 'support': 'No payment-term entity. Horus stores a compact delay code per company (for example 30E = 30 days end of month) and invoices take an explicit due date. Return a synthetic list or an empty list; <code>payment_term_id</code> is ignored on creation.', 'label': 'D'},
    {'name': 'Payment methods (GET payment-methods)', 'why': 'Optional <code>payment_method_id</code> on invoices.', 'support': 'Fixed PaymentMode list documented by Horus (bank transfer, domiciliation, card, PayPal, Doccle, Digiteal, check, bill draft…), returned as a constant list.', 'label': 'F'},
    {'name': 'Attachments (GET attachments)', 'why': 'Invoices return <code>attachments_info</code>; files are fetched separately.', 'support': '<code>book-entries.info</code> gives the main document reference, then <code>documents.download</code> returns the bytes. Finding annexes needs a date-bounded <code>documents.list</code>.', 'label': 'D'},
    {'name': 'Bookyears (GET bookyears)', 'why': 'Context for periods, closure checks and journal numbering.', 'support': '<code>fiscal-years.list</code>; the closed flag is documented only on <code>fiscal-years.info</code> (one call per year).', 'label': 'F'},
]

RISKS_INTRO = 'Situations the connector must handle explicitly. Most follow from three Horus traits: no idempotency key, entries that get a new id when updated, and lists without pagination.'

EDGE_CASES = [
    {'case': 'A create call times out or returns 500 (client, invoice, operation, account).', 'handling': 'Never retry blindly. Search for the record first (external reference, VAT number, document number) and re-post only if it does not exist.', 'routes': 'All write routes', 'label': 'D'},
    {'case': 'The client’s VAT number already exists, as a customer or as a supplier only.', 'handling': 'Pre-check before creating. Return an “already exists” error with the existing id, and suggest <code>force_merge</code> when the match is a supplier.', 'routes': 'Client creation', 'label': 'F'},
    {'case': 'The invoice date falls in a period the accountant has closed.', 'handling': 'Check the fiscal-year closure dates before posting, as Horus recommends, and return a clear error. Horus offers no forced period on invoice creation.', 'routes': 'Invoice and operation creation', 'label': 'F'},
    {'case': 'Header totals and line totals differ by rounding.', 'handling': 'Horus checks totals = base + tax and the sum of lines; tax within one cent is recalculated unless OverrideTaxAmounts is set. Validate in the connector first and use <code>invoice_correction</code> when needed.', 'routes': 'Invoice creation', 'label': 'F'},
    {'case': 'An analytic split such as 33 / 33 / 34 %.', 'handling': 'Largest-remainder rounding so cost lines sum exactly to the line base amount.', 'routes': 'Invoice creation', 'label': 'D'},
    {'case': 'A tax_code that is not a valid Horus combination.', 'handling': 'Reject with 422 before calling Horus.', 'routes': 'Invoice creation', 'label': 'D'},
    {'case': 'A foreign-currency invoice or operation.', 'handling': 'Invoices: allowed when the folder accepts currencies. Miscellaneous operations: no currency field, so non-EUR operations are rejected. On read, EUR amounts are never paired with a foreign currency code.', 'routes': 'Invoices, operations, outstanding items', 'label': 'F'},
    {'case': 'The accountant edits an invoice created through the API.', 'handling': 'Horus generates a new book entry id, so the Chift id changes. Reconcile on daybook and document number; disclose this to consumers.', 'routes': 'Invoice retrieval and creation', 'label': 'F'},
    {'case': 'A credit note stored in a sales or purchase daybook.', 'handling': 'Read both daybook types and classify each entry by the sign of the customer or supplier line.', 'routes': 'Invoice retrieval', 'label': 'A'},
    {'case': 'Several possible journals and no journal_id.', 'handling': 'Auto-select by daybook type when exactly one candidate exists; otherwise 400 “journal_id required”.', 'routes': 'Invoice and operation creation', 'label': 'D'},
    {'case': 'An inactive account or cost section, or analytics sent to a folder without the analytics module.', 'handling': 'Reject with 422 before calling Horus.', 'routes': 'Write routes', 'label': 'D'},
    {'case': 'An id that belongs to another folder of the same license.', 'handling': 'Check the folder on every call by id; return 400.', 'routes': 'All', 'label': 'D'},
    {'case': 'Partial payments and instalments.', 'handling': 'Open amounts come from matching groups; Horus has a single due date per entry, so <code>due_dates</code> has at most one element.', 'routes': 'Outstanding items, invoice retrieval', 'label': 'D'},
    {'case': 'An open item carried over from the previous fiscal year.', 'handling': 'Identify the opening entry through its entry type and link the original document where Horus provides it; otherwise leave <code>original_document</code> empty.', 'routes': 'Outstanding items', 'label': 'A'},
    {'case': 'Two Chift calls for the same consumer refresh the token at the same time.', 'handling': 'Serialise refreshes per connection; refresh tokens are single-use.', 'routes': 'All', 'label': 'F'},
    {'case': 'A large folder (an accounting firm’s client with years of entries).', 'handling': 'Full lists with emulated pagination, narrow month windows, per-folder caching and gzip. Horus documents no size or rate limits.', 'routes': 'All list routes', 'label': '?'},
]

QUESTIONS_INTRO = ('Consolidated and ordered by impact on the design. Each route card in section 4 also lists its detailed questions.')

QUESTIONS_HORUS = [
    {'q': 'Can you share the accepted tax-combination files for sales and purchases? Is an endpoint listing VAT codes or combinations available or planned? Can TaxKind be exposed on read?', 'why': 'Invoice creation cannot post valid VAT without them, and Chift’s VAT codes depend on them.', 'routes': 'Invoices, VAT codes'},
    {'q': 'Can a credit note (Type 1) be posted in a sales or purchase daybook, and an invoice in a credit-note daybook? Is the document type exposed on read? Must credit-note amounts be positive?', 'why': 'Decides daybook selection on write and invoice/refund classification on read.', 'routes': 'Invoices, journals'},
    {'q': 'Is the document number unique per daybook and fiscal year? What happens on a duplicate number? Is there an idempotency key, or a way to get the next free number? Could invoices support automatic numbering?', 'why': 'Duplicate protection and numbering for confirmed invoices.', 'routes': 'Invoices, operations, journals'},
    {'q': 'In which currency are ledger amounts (debit/credit, book-entry totals) and invoice totals expressed for foreign-currency documents, and in which direction is CurrencyRate given? Is the folder base currency always EUR?', 'why': 'Correct amounts on read for any foreign-currency document.', 'routes': 'Invoices, outstanding items, folders'},
    {'q': 'Are there rate limits, maximum result sizes or maximum period spans on list endpoints?', 'why': 'Lists are not paginated, and several routes make one call per daybook or per schema.', 'routes': 'All list routes'},
    {'q': 'Which ErrorType values can be returned (duplicate VAT, search key or number, closed period, invalid tax combination, unknown account or cost section)? Do calls by id for an object in another folder return 403, 404 or 400?', 'why': 'Specific error messages for Chift consumers and safe retry rules.', 'routes': 'All'},
    {'q': 'What are the rules for search keys (length, characters, case) for companies and accounts? Is a cost section search key unique per folder or per schema?', 'why': 'The connector must generate company search keys and validate account numbers.', 'routes': 'Clients, accounts, analytics'},
    {'q': 'Does an empty CompanyIds filter on customers.outstanding and suppliers.outstanding return all partners? How are lines carried over from a previous year linked to their original document? Is a purchase-side equivalent of invoices.sales.outstanding.list planned?', 'why': 'Determines the call pattern for outstanding items.', 'routes': 'Outstanding items'},
    {'q': 'Where does the invoice header comment appear on read (partner-line comment, RemarkCompany or Remark)?', 'why': 'Round-trip of reference and customer memo.', 'routes': 'Invoices, outstanding items'},
    {'q': 'Do ledger period filters use calendar months or accounting periods? Does ModifiedAfter on book entries track changes to their lines and matching? Is there any signal for deleted or replaced entries (for example webhooks)?', 'why': 'Reliable incremental synchronisation and date filtering.', 'routes': 'Invoices, outstanding items'},
    {'q': 'What do CustomerActivitySuspended, Name2, Address2, Family and ContactPerson mean? How is an enterprise number written? Which concentration account applies when none is given?', 'why': 'Mapping of active status, addresses, company numbers and receivable accounts.', 'routes': 'Clients'},
    {'q': 'Can an account’s category be set or is it derived from the number? What is the full list of IntCategory values? Does accounts.list include inactive and title accounts?', 'why': 'Chift account type on creation and in the chart of accounts.', 'routes': 'Accounts'},
    {'q': 'What do the cost endpoints return for a folder without the analytics module? Must a cost line carry one value per cost schema? What do Mandatory, IsLocked, IsDefault and MasterCostSchema mean? Is the cost-history balance signed?', 'why': 'Analytics on write and the analytic routes on read.', 'routes': 'Analytics, invoices, operations'},
    {'q': 'What does IsUsed mean on daybooks? Can cash, temporary, system or cost daybooks receive entries through the API? Does fiscal-years.list return IsClosed?', 'why': 'Journal flags and posting rules.', 'routes': 'Journals, operations'},
    {'q': 'Which relationship paths can be sideloaded with Include on companies.list, book-entries.list and account-histories.list, and with which fields?', 'why': 'Can cut read-backs and invoice retrieval to fewer calls.', 'routes': 'Clients, invoices'},
    {'q': 'Does book-entries.info need a FolderId? What does it return for an entry that was replaced or deleted?', 'why': 'Read-backs and single-invoice reads.', 'routes': 'Invoices, operations, outstanding items'},
    {'q': 'Can Chift get a test license or test folder? Can test data be removed (there is no delete for companies or invoices)?', 'why': 'The API works on live data.', 'routes': 'All write routes'},
    {'q': 'What is the maximum attachment size for multipart uploads?', 'why': 'Validation of PDFs sent with invoices.', 'routes': 'Invoices, operations'},
]

QUESTIONS_CHIFT = [
    {'q': 'For status “posted”, should the connector confirm entries in Horus, or push them unconfirmed by default so the accountant reviews them?', 'why': 'Horus’s default for API entries is accountant review.', 'routes': 'Invoices, operations'},
    {'q': 'Is a connector-owned VAT-code catalogue acceptable for GET vat-codes, and is returning tax_code = null on read when the code is ambiguous acceptable?', 'why': 'Horus has no VAT-code entity.', 'routes': 'Invoices, VAT codes'},
    {'q': 'For inputs Horus cannot store (withholding tax, Dutch G/N split, accrual dates, forced period, line quantity, extra addresses, non-EUR operations): reject or ignore with a warning? Can the connector return warnings?', 'why': 'Consistent behaviour across Chift connectors.', 'routes': 'Clients, invoices, operations'},
    {'q': 'For values Horus does not hold on read: null or a default (analytic balance 0 or null, approval status “unknown”, empty next document numbers)?', 'why': 'Avoid misleading defaults.', 'routes': 'Invoices, journals, analytics'},
    {'q': 'Which sign convention does Chift expect for refund amounts on input and for outstanding amounts on output?', 'why': 'The case does not specify it.', 'routes': 'Invoices, outstanding items'},
    {'q': 'On a duplicate (VAT number, external reference, document number): return an error (400/409) or the existing record? Which supplier fields may force_merge overwrite?', 'why': 'Duplicate policy must match other connectors.', 'routes': 'Clients, invoices'},
    {'q': 'Is rejecting non-numeric invoice and operation numbers acceptable?', 'why': 'Horus numbers are numeric.', 'routes': 'Invoices, operations'},
    {'q': 'What does partner_info.account_number mean: a third-party code or a ledger account?', 'why': 'The Chift specification does not describe it.', 'routes': 'Invoice creation'},
    {'q': 'Is deriving analytic combinations from independent per-plan percentages acceptable? Can “free” cost schemas stay out of scope in v1?', 'why': 'Horus allocates amounts to combinations of cost sections.', 'routes': 'Invoices, analytics'},
    {'q': 'Should unconfirmed Horus entries be returned as drafts or excluded by default? Is it acceptable that an invoice id changes when the accountant updates it?', 'why': 'Read behaviour for entries under accountant review.', 'routes': 'Invoice retrieval'},
    {'q': 'Which default period should invoice retrieval use when no dates are given?', 'why': 'Horus requires a month window and has no pagination.', 'routes': 'Invoice retrieval'},
    {'q': 'Should the Horus connector always enable the multiple-folders feature?', 'why': 'Accounting-firm licenses hold many folders.', 'routes': 'All'},
    {'q': 'Documentation details: FolderItem.main_currency is described as ISO 3166-1 (a country standard; ISO 4217 is meant), and the line tax_amount formula omits the division by 100.', 'why': 'Small corrections to the Chift API reference.', 'routes': 'Folders, invoices'},
]

CONCLUSION = ('A Horus connector is feasible for the full scope of the case. The Horus API covers every object Chift needs, with dedicated endpoints for the two most valuable flows (pushing sales and purchase invoices with their PDF, and reading open items). '
              'The work is in the translation layer: rebuilding invoices from the ledger, a VAT-code catalogue, analytics conversion, pagination emulation and duplicate protection. '
              'None of these needs changes on the Horus side, but a handful of answers from Horus would remove the main assumptions.')

NEXT_STEPS = [
    'Re-check the Chift specification used here against the live documentation (docs.chift.eu).',
    'Send the questions for Horus (section 8), starting with H1 to H6, and request a test license with a test folder.',
    'Agree the Chift-side conventions in questions C1 to C6 so the connector behaves like the existing ones.',
    'Build the shared components first (connection and token manager, folder rule, reference cache, pagination emulation, VAT catalogue, analytics converter).',
    'Prototype the two riskiest flows against the test folder: invoice retrieval rebuilt from the ledger, and supplier outstanding items computed from matching.',
    'Then implement the remaining routes, using the attribute tables in section 5 as acceptance criteria.',
]
