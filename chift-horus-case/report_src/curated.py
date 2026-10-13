"""Curated narrative for the external report (filled from the harmonised mapping data)."""

TASK_B = ['create_client', 'create_invoice', 'outstandings']

CARD_META = {
    'create_client': {'brief': 'A Chift client becomes a Horus company (third party) flagged as customer, created with <code>companies.new</code>. The connector generates the required search key and fills the Horus-required flags, language and country from Chift data or folder defaults. Creation returns only an id, so the company is read back (two to three calls) to build the Chift response. <code>force_merge</code> flags an existing supplier as customer instead of creating a duplicate. Main risks: undocumented search-key rules, duplicate VAT numbers refused by default, no idempotency key, and one address per company.', 'one_line': 'Native creation with companies.new. The connector generates the Horus search key, derives required flags, and reads the company back to build the Chift response.', 'title': 'Client creation', 'paths': 'POST /consumers/{consumer_id}/accounting/clients'},
    'get_invoices': {'brief': 'Horus has no endpoint that lists invoices: posted invoices become book entries. The connector reads the entry headers per daybook (sales or purchases, invoices and credit notes), then all lines with VAT, analytics and matching in one ledger call, plus open sales items for payments and document type, and assembles Chift invoices. Pagination, day-level date filters and payment status are emulated. Main risks: invoice/credit-note classification for closed or purchase entries, ids that change when the accountant edits an entry, and no line quantities.', 'one_line': 'Horus has no invoice list. Invoices are rebuilt from book entries, account history lines and open-item data, with pagination and day-level filters emulated.', 'title': 'Invoice retrieval (multiple analytic plans)', 'paths': 'GET /consumers/{consumer_id}/accounting/invoices/multi-analytic-plans/type/{invoice_type}'},
    'create_invoice': {'brief': 'Customer invoices and credit notes go to <code>invoices.sales.new</code>, supplier ones to <code>invoices.purchases.new</code>, with the PDF in the same call. Before posting, the connector resolves the daybook, partner, accounts and cost sections from cached reference data, translates <code>tax_code</code> into Horus VAT fields, converts analytic percentages into amounts and checks the document number. After posting it reads the entry back. Main risks: the VAT combination catalogue, numeric numbering without automatic numbers, and the confirmation default.', 'one_line': 'Native creation with invoices.sales.new or invoices.purchases.new, PDF included. VAT codes, analytics and numbering need connector logic; the entry is read back after creation.', 'title': 'Invoice creation (multiple analytic plans)', 'paths': 'POST /consumers/{consumer_id}/accounting/invoices/multi-analytic-plans'},
    'journals_folders': {'brief': "Folders map almost one to one onto <code>folders.list</code>. Journals come from <code>daybooks.list</code>: the daybook type maps cleanly to Chift's journal type, the counterpart account needs a lookup in the cached chart of accounts, and Chift fields that Horus does not hold (blocked, unallocated account, next document numbers) are derived or emulated.", 'title': 'Journal retrieval and accounting folders retrieval', 'paths': 'GET …/accounting/journals · GET …/accounting/folders',
                         'one_line': 'Folders map almost one to one onto folders.list. Journals come from daybooks.list, with the counterpart account looked up in the chart of accounts and next document numbers only emulated.'},
    'ledger_accounts': {'brief': 'Accounts are created with <code>accounts.new</code> (number and name only) after a duplicate check, and read back. The chart of accounts comes from <code>accounts.list</code>, cached per folder. Horus has no writable account type, so the Chift type cannot be set on creation and is computed on read from daybooks, categories and, as a last resort, the account number. Type filtering and pagination are emulated.', 'title': 'Ledger account creation and chart of accounts retrieval', 'paths': 'POST …/accounting/accounts · GET …/accounting/chart-of-accounts',
                        'one_line': 'accounts.new and accounts.list are native, but the Chift account type cannot be written and must be computed on read; type filtering and pagination are emulated.'},
    'misc_operation': {'brief': "Horus has a dedicated endpoint that posts a balanced debit/credit operation in a miscellaneous daybook. The connector splits Chift's signed amounts into debit and credit, maps line types (customer, supplier, general) and resolves accounts, partners and cost sections. It is a workaround because Horus operations have no currency field (EUR only), numbers must be numeric, and a read-back is needed when Horus generates the number.", 'one_line': 'Native creation of a balanced debit/credit operation. EUR only and numeric numbers only; the entry is read back after creation.', 'title': 'Miscellaneous operation creation', 'paths': 'POST /consumers/{consumer_id}/accounting/miscellaneous-operation'},
    'analytics': {'brief': 'A Horus cost schema is an analytic plan and a cost section is an analytic account. Plans come from one call. Accounts need one call per list-type schema (at most eight), merged and paginated by the connector. Horus stores no balance per analytic account, so balance, debit and credit can only be computed over a period, which the Chift route does not carry.', 'title': 'Analytic plans retrieval and analytic accounts retrieval (multiple plans)', 'paths': 'GET …/accounting/analytic-plans · GET …/accounting/analytic-accounts/multi-analytic-plans',
                  'one_line': 'Cost schemas are analytic plans (one call). Cost sections are analytic accounts, listed with one call per schema; balances are not stored and can only be computed over a period.'},
    'outstandings': {'brief': 'Horus has folder-level open-item lists, but the two sides differ. Client items come from the open sales invoices list (with a native open amount), joined with customer ledger lines for account and matching details. Supplier items come from supplier ledger lines, with the open amount computed from matching groups. Journal ids and types come from cached daybooks, and pagination is emulated.', 'one_line': 'Folder-level open items exist on both sides, but the client and supplier paths differ; supplier open amounts are computed from matching groups.', 'title': 'Outstanding items (customers and suppliers)', 'paths': 'GET /consumers/{consumer_id}/accounting/outstandings'},
}

OVERVIEW = [
    {'route': 'Client creation', 'chift': 'POST /accounting/clients', 'group': 'create_client', 'match': 'Create client',
     'endpoints': ['POST /companies.new', 'GET /companies.info, POST /ibans.list (read-back)', 'POST /companies.list (duplicate checks)', 'POST /companies.update, POST /ibans.new (force_merge)'],
     'pattern': 'Check → create → read back'},
    {'route': 'Invoice retrieval (multiple plans)', 'chift': 'GET /accounting/invoices/multi-analytic-plans/type/{invoice_type}', 'group': 'get_invoices', 'match': 'Get invoices',
     'endpoints': ['POST /daybooks.list (cached)', 'POST /book-entries.list (per daybook)', 'POST /account-histories.list (lines, VAT, analytics, matching)', 'POST /invoices.sales.outstanding.list (sales: payments and invoice/credit-note type)', 'GET /book-entries.info (single invoice)'],
     'pattern': 'Rebuild invoices from the ledger'},
    {'route': 'Invoice creation (multiple plans)', 'chift': 'POST /accounting/invoices/multi-analytic-plans', 'group': 'create_invoice', 'match': 'Create sale/purchase',
     'endpoints': ['POST /invoices.sales.new or /invoices.purchases.new', 'Cached lookups: daybooks, accounts, cost schemas/sections, fiscal years', 'GET /companies.info (partner check)', 'POST /companies.list → /companies.new or /companies.update (partner_info)', 'POST /book-entries.list (duplicate check)', 'GET /book-entries.info (read-back)'],
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
     'endpoints': ['POST /book-entries.miscellaneous-operations.new', 'Cached lookups: daybooks, accounts, cost schemas/sections, fiscal years', 'POST /book-entries.list (duplicate check when a number is given)', 'GET /book-entries.info (read-back when Horus numbers the entry)'], 'pattern': 'Resolve → check → create → read back (conditional)'},
    {'route': 'Analytic plans retrieval', 'chift': 'GET /accounting/analytic-plans', 'group': 'analytics', 'match': 'Analytic Plans',
     'endpoints': ['POST /cost-schemas.list'], 'pattern': 'List'},
    {'route': 'Analytic accounts retrieval (multiple plans)', 'chift': 'GET /accounting/analytic-accounts/multi-analytic-plans', 'group': 'analytics', 'match': 'analytic accounts',
     'endpoints': ['POST /cost-schemas.list', 'POST /cost-sections.list (once per list-type schema, max 8)', 'POST /cost-histories.list (balances, optional)'], 'pattern': 'Loop over plans + merge'},
    {'route': 'Outstanding items (Task B only)', 'chift': 'GET /accounting/outstandings', 'group': 'outstandings', 'match': 'outstanding',
     'endpoints': ['Clients: POST /invoices.sales.outstanding.list + POST /customers.outstanding', 'Suppliers: POST /suppliers.outstanding', 'POST /daybooks.list (journal ids and types, cached)', 'GET /book-entries.info (enrichment, optional)'],
     'pattern': 'Join + compute open amounts'},
]


SUMMARY_LEDE = ('All eleven Chift routes in scope can be built on the Horus Software API, and none is blocked. '
                'Two map almost directly (folders and analytic plans). Nine need workarounds that the connector can absorb, at the cost of extra calls, '
                'emulated behaviour, or data loss that Chift should disclose to its clients. For most of them the core Horus capability is native; '
                'the workaround sits in the translation around it.')

KEY_FINDINGS = [
    '<b>Every object in scope exists in Horus and can be read or written where the case needs it</b>, with the field-level losses listed below: third parties (“companies”), sales and purchase invoices, miscellaneous operations, accounts, daybooks, cost schemas and sections, folders and open items.',
    '<b>Creation calls return only an id.</b> Client and account creation read the record back (one <code>.info</code> call) to return the full Chift response; invoices are read back by default, and miscellaneous operations only when Horus generates the number. Duplicate checks are needed before creating, because no idempotency key is documented.',
    '<b>There is no “list invoices” endpoint.</b> Invoice retrieval rebuilds each invoice from book entries (headers) and account history lines (lines, VAT, analytics, matching), plus open-item data for payments. This is the clearest case of “one Chift route, several Horus endpoints”.',
    '<b>VAT is modelled differently.</b> Horus has no VAT-code entity: each line carries a rate, an origin and a type (plus kind and condition for purchases), and only listed combinations are valid. The connector needs its own VAT-code catalogue to serve Chift’s <code>tax_code</code> and VAT-code list.',
    '<b>No documented pagination, and month-based periods.</b> Horus lists appear to return everything for a folder or a month window, so the connector emulates Chift pagination and day-level date filters, and should cache reference data per folder.',
    '<b>Data loss Chift should disclose to its clients:</b> one address per third party, no mobile, notes or person fields; no line quantity or unit price on invoices; the account type cannot be written; miscellaneous operations are EUR-only; analytic balances are not stored.',
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
                'Error responses follow the same pattern on all three routes: see the error rows of the client creation table and the error translation table in section 7. '
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
<p>Combinations are the product of the plan percentages. Rounding uses the largest remainder so the cost lines always sum exactly to the base amount. Deriving combinations from independent plan splits is an assumption Chift should validate (question C9).</p></div>
<div class="note"><span class="note-title">VAT: from Chift tax_code to Horus fields</span>
<p>The connector exposes Horus tax combinations as synthetic VAT codes, for example <code>S-21-0-0</code> = sale, 21 %, origin 0 (national sale), type 0 (national). On write the code is decoded into TaxRate, TaxOrigin and TaxType (plus TaxKind, TaxCondition and TaxConditionValue for purchases). The list of valid combinations comes from Horus reference spreadsheets that still need to be obtained (question H1).</p></div>''',
    'outstandings': '''<div class="note"><span class="note-title">Sign convention</span>
<p>Customer lines: amount = debit − credit. Supplier lines: amount = credit − debit. A positive amount is always owed (a receivable for clients, a payable for suppliers). Chift’s expected convention is question C5.</p></div>''',
}


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

IMPACT_INTRO = ''
CLIENT_IMPACT = []
RATING_NOTE = ''
TAX_APPENDIX = ''

from curated_lists import *  # noqa: E402,F401,F403  (questions, edge cases, error map, building blocks, dependencies, working assumptions)
