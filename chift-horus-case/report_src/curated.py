"""Curated narrative for the external report (filled from the harmonised mapping data)."""

TASK_B = ['create_client', 'create_invoice', 'outstandings']

CARD_META = {
    'create_client': {'brief': 'A Chift client becomes a Horus company (third party) flagged as customer, created with <code>companies.new</code>. The connector generates the required search key (from the name, a proposal for Chift, D10 and C8) and fills the Horus-required flags, language and country from Chift data or folder defaults. Creation returns only an id, so the company is read back (two to three calls) to build the Chift response. <code>force_merge</code> flags an existing supplier as customer instead of creating a duplicate. Main risks: undocumented search-key rules, duplicate VAT numbers refused by default, no idempotency key, and one address per company.', 'one_line': 'Native creation with companies.new. The connector generates the Horus search key, derives required flags, and reads the company back to build the Chift response.', 'title': 'Client creation', 'paths': 'POST /consumers/{consumer_id}/accounting/clients'},
    'get_invoices': {'brief': 'Horus has no general invoice list (only open sales invoices are listed): posted invoices become book entries. The connector reads the entry headers per daybook (sales or purchases, invoices and credit notes), then all lines with VAT, analytics and matching in one ledger call, plus open sales items for payment status, invoice-currency amounts and a document-type check, and assembles Chift invoices. Pagination, day-level date filters and payment status are emulated. Main risks: invoice/credit-note classification (the document type is not readable for closed or purchase entries, question H2), ids that change when the accountant edits an entry, and no line quantities.', 'one_line': 'Horus has no general invoice list. Invoices are rebuilt from book entries, account history lines and open-item data, with pagination and day-level filters emulated.', 'title': 'Invoice retrieval (multiple analytic plans)', 'paths': 'GET /consumers/{consumer_id}/accounting/invoices/multi-analytic-plans/type/{invoice_type}'},
    'create_invoice': {'brief': 'Customer invoices and credit notes go to <code>invoices.sales.new</code>, supplier ones to <code>invoices.purchases.new</code>, with the PDF in the same call. Before posting, the connector resolves the daybook, partner, accounts and cost sections from cached reference data, translates <code>tax_code</code> into Horus VAT fields using the folder’s list of accepted combinations (appendix C), converts analytic percentages into amounts and checks the document number. After posting it reads the entry back by default. Main risks: keeping the VAT catalogue aligned with the Horus files, numeric numbering without automatic numbers, and the posting mode (review or direct, question C1).', 'one_line': 'Native creation with invoices.sales.new or invoices.purchases.new, PDF included. VAT codes, analytics and numbering need connector logic; the entry is read back by default.', 'title': 'Invoice creation (multiple analytic plans)', 'paths': 'POST /consumers/{consumer_id}/accounting/invoices/multi-analytic-plans'},
    'journals_folders': {'brief': "Folders map almost one to one onto <code>folders.list</code>; the folder country would need one extra call per folder and is not returned by default (C4). Journals come from <code>daybooks.list</code>: the daybook type maps cleanly to Chift's journal type, the counterpart account needs a lookup in the cached chart of accounts, and Chift fields that Horus does not hold (blocked, unallocated account, next document numbers) are derived or emulated.", 'title': 'Journal retrieval and accounting folders retrieval', 'paths': 'GET …/accounting/journals · GET …/accounting/folders',
                         'one_line': 'Folders map almost one to one onto folders.list (country not returned by default). Journals come from daybooks.list, with the counterpart account looked up in the chart of accounts and next document numbers only emulated.'},
    'ledger_accounts': {'brief': 'Accounts are created with <code>accounts.new</code> (number and name only) after a duplicate check, and read back with one <code>accounts.info</code> call. The chart of accounts comes from <code>accounts.list</code>, cached per folder. Horus has no writable account type, so the Chift type cannot be set on creation and is computed on read from daybooks, categories and, as a last resort, the account number. Type filtering and pagination are emulated; the filter is reliable for income and expense accounts and a best effort for VAT and cash accounts.', 'title': 'Ledger account creation and chart of accounts retrieval', 'paths': 'POST …/accounting/accounts · GET …/accounting/chart-of-accounts',
                        'one_line': 'accounts.new and accounts.list are native, but the Chift account type cannot be written and must be computed on read; type filtering and pagination are emulated.'},
    'misc_operation': {'brief': "Horus has a dedicated endpoint that posts a balanced debit/credit operation in a miscellaneous daybook. The connector splits Chift's signed amounts into debit and credit, maps line types (customer, supplier, general) and resolves accounts, partners and cost sections. It is a workaround because Horus operations have no currency field, so amounts are stored in EUR (a foreign-currency operation is converted at the supplied rate and the original currency is not kept; who converts is question C15), numbers must be numeric, and a read-back is needed when Horus generates the number. The duplicate check on a supplied number is a connector safeguard.", 'one_line': 'Native creation of a balanced debit/credit operation, stored in EUR (foreign-currency operations are converted at the supplied rate), with numeric or Horus-generated numbers; the entry is read back only when Horus generates the number.', 'title': 'Miscellaneous operation creation', 'paths': 'POST /consumers/{consumer_id}/accounting/miscellaneous-operation'},
    'analytics': {'brief': 'A Horus cost schema is an analytic plan and a cost section is an analytic account. Plans come from one call (at most eight rows, paginated by the connector; Free-type dimensions are not returned in v1, question C9). Accounts need one call per list-type schema (at most eight), merged and paginated by the connector. Horus stores no balance per analytic account, so balance, debit and credit can only be computed over a period, which the Chift route does not carry.', 'title': 'Analytic plans retrieval and analytic accounts retrieval (multiple plans)', 'paths': 'GET …/accounting/analytic-plans · GET …/accounting/analytic-accounts/multi-analytic-plans',
                  'one_line': 'Cost schemas are analytic plans (one call, Free-type dimensions hidden in v1). Cost sections are analytic accounts, listed with one call per schema; balances are not stored and can only be computed over a period.'},
    'outstandings': {'brief': 'Horus has open-item lists for both sides, but the two sides differ. Client items come from the open sales invoices list, which returns the folder’s open sales invoices and credit notes with a native open amount (documented), joined with customer ledger lines for account and matching details. Supplier items come from supplier ledger lines: the open amount is the amount of each unmatched line, netted per matching group only if Horus also returns partially matched lines (assumption), and checked against the totals Horus returns (to verify, H23). Whether the ledger lists return every partner of the folder when no company filter is sent is to be confirmed (question H8). Journal ids and types come from cached daybooks, and pagination is emulated. Call budget: two calls for clients and one for suppliers, plus a rare per-item fallback and optional per-entry enrichment (off by default, proposal).', 'one_line': 'Client open items come with a native open amount; supplier open amounts are computed by the connector from unmatched ledger lines (partial matches and folder-wide scope to confirm, H8).', 'title': 'Outstanding items (customers and suppliers)', 'paths': 'GET /consumers/{consumer_id}/accounting/outstandings'},
}

OVERVIEW = [
    {'route': 'Client creation', 'chift': 'POST /accounting/clients', 'group': 'create_client', 'match': 'Create client',
     'endpoints': ['POST /companies.new', 'GET /companies.info, POST /ibans.list (read-back)', 'POST /companies.list (duplicate checks)', 'POST /companies.update, POST /ibans.new (force_merge)'],
     'pattern': 'Check → create → read back',
     'complexity': 'Medium', 'impact': 'Visible: one address, no person fields, every partner a company', 'blocking': []},
    {'route': 'Invoice retrieval (multiple plans)', 'chift': 'GET /accounting/invoices/multi-analytic-plans/type/{invoice_type}', 'group': 'get_invoices', 'match': 'Get invoices',
     'endpoints': ['POST /daybooks.list (cached)', 'POST /book-entries.list (per daybook)', 'POST /account-histories.list (lines, VAT, analytics, matching; +1 for payments when requested)', 'POST /invoices.sales.outstanding.list (sales: payment status, invoice-currency amounts, type check)'],
     'pattern': 'Rebuild invoices from the ledger',
     'complexity': 'High', 'impact': 'Visible: ids change after edits, no line quantities, foreign currency partly in euro', 'blocking': ['H2', 'H4', 'H5']},
    {'route': 'Invoice creation (multiple plans)', 'chift': 'POST /accounting/invoices/multi-analytic-plans', 'group': 'create_invoice', 'match': 'Create sale/purchase',
     'endpoints': ['POST /invoices.sales.new or /invoices.purchases.new', 'Cached lookups: daybooks, accounts, cost schemas/sections', 'POST /fiscal-years.list (closure check, per request)', 'GET /companies.info (partner check)', 'POST /companies.list → /companies.new or /companies.update (partner_info)', 'POST /book-entries.list (duplicate check)', 'GET /book-entries.info (read-back)'],
     'pattern': 'Resolve → check → create → read back',
     'complexity': 'High', 'impact': 'Visible: numeric numbers, accountant review, no delete', 'blocking': ['H1', 'H3', 'C1', 'C7']},
    {'route': 'Journal retrieval', 'chift': 'GET /accounting/journals', 'group': 'journals_folders', 'match': 'Get journals',
     'endpoints': ['POST /daybooks.list', 'POST /accounts.list (counterpart account, cached)'], 'pattern': 'List + lookup',
     'complexity': 'Low', 'impact': 'Minor: next document numbers not provided by default', 'blocking': []},
    {'route': 'Ledger account creation', 'chift': 'POST /accounting/accounts', 'group': 'ledger_accounts', 'match': 'Create ledger account',
     'endpoints': ['POST /accounts.new', 'POST /accounts.list (duplicate check)', 'GET /accounts.info (read-back)'], 'pattern': 'Check → create → read back',
     'complexity': 'Medium', 'impact': 'Visible: account type cannot be written', 'blocking': []},
    {'route': 'Chart of accounts retrieval', 'chift': 'GET /accounting/chart-of-accounts', 'group': 'ledger_accounts', 'match': 'chart of accounts',
     'endpoints': ['POST /accounts.list', 'POST /daybooks.list (account type derivation, cached)', 'POST /account-histories.list (only for a VAT or cash type filter, cached)'], 'pattern': 'List + derive',
     'complexity': 'Medium', 'impact': 'Minor: account type derived on read, VAT and cash filters best effort', 'blocking': []},
    {'route': 'Accounting folders retrieval', 'chift': 'GET /accounting/folders', 'group': 'journals_folders', 'match': 'Get Folders',
     'endpoints': ['POST /folders.list (Mode 0)', 'GET /folders.info (country; only if Chift needs it, not called by default)'], 'pattern': 'List',
     'complexity': 'Low', 'impact': 'Minor: folder country not returned by default', 'blocking': []},
    {'route': 'Miscellaneous operation creation', 'chift': 'POST /accounting/miscellaneous-operation', 'group': 'misc_operation', 'match': 'miscellaneous',
     'endpoints': ['POST /book-entries.miscellaneous-operations.new', 'Cached lookups: daybooks, accounts, cost schemas/sections', 'POST /fiscal-years.list (closure check, per request)', 'POST /book-entries.list (duplicate check when a number is given)', 'GET /book-entries.info (read-back when Horus numbers the entry)'], 'pattern': 'Resolve → check → create → read back (conditional)',
     'complexity': 'Medium', 'impact': 'Visible: numeric numbers, foreign currency converted to euro', 'blocking': ['C1', 'C15']},
    {'route': 'Analytic plans retrieval', 'chift': 'GET /accounting/analytic-plans', 'group': 'analytics', 'match': 'Analytic Plans',
     'endpoints': ['POST /cost-schemas.list'], 'pattern': 'List',
     'complexity': 'Low', 'impact': 'Minor: free dimensions hidden', 'blocking': []},
    {'route': 'Analytic accounts retrieval (multiple plans)', 'chift': 'GET /accounting/analytic-accounts/multi-analytic-plans', 'group': 'analytics', 'match': 'analytic accounts',
     'endpoints': ['POST /cost-schemas.list', 'POST /cost-sections.list (once per list-type schema, max 8)', 'POST /cost-histories.list (balances, optional)'], 'pattern': 'Loop over plans + merge',
     'complexity': 'Low', 'impact': 'Minor: no balances', 'blocking': []},
    {'route': 'Outstanding items (Task B only)', 'chift': 'GET /accounting/outstandings', 'group': 'outstandings', 'match': 'outstanding',
     'endpoints': ['Clients: POST /invoices.sales.outstanding.list + POST /customers.outstanding', 'Suppliers: POST /suppliers.outstanding', 'POST /daybooks.list (journal ids and types, cached)', 'GET /account-histories.info (rare fallback per unmatched item)', 'GET /book-entries.info (enrichment, optional)'],
     'pattern': 'Join + compute open amounts',
     'complexity': 'High', 'impact': 'Visible: supplier items in euro, one due date per item', 'blocking': ['H8', 'H5']},
]

RATING_NOTE = ('Verdict: can the route be built on the documented Horus API. Build complexity: live Horus calls per request, emulated behaviour and business rules the connector must own. '
               'Client impact: what client applications will notice (section 6). Depends on: the priority-1 questions (section 9) that the route’s final design waits for. '
               'Complexity and impact are the analyst’s assessment from the route cards, to calibrate with Chift.')


SUMMARY_LEDE = ('No route is blocked by a missing Horus capability in the documentation reviewed. '
                'Accounting folders maps directly onto Horus; the other ten routes are supported with workarounds: extra Horus calls, emulated paging or filters, '
                'or behaviour that client applications will notice (section 6). '
                'Build complexity is low for folders, analytic plans, journals and analytic accounts, medium for client creation, ledger account creation, '
                'chart of accounts and miscellaneous operations, and high for invoice creation, invoice retrieval and outstanding items. '
                'Invoice creation, invoice retrieval, outstanding items and miscellaneous operations wait on priority-1 answers before their design is final (section 9). '
                'Emulated paging is expected to work for typical folder sizes; behaviour on large folders is unverified (H5).')

KEY_FINDINGS = [
    '<b>Every object in scope exists in Horus and can be read or written where the case needs it</b>, with the field-level losses summarised below and in section 6: third parties (“companies”), sales and purchase invoices, miscellaneous operations, accounts, daybooks, cost schemas and sections, folders and open items.',
    '<b>Creation calls return only an id.</b> Account creation reads the account back with one <code>accounts.info</code> call; client creation needs two to three calls (company details and bank accounts, plus the receivable account when the chart is not cached); invoices are read back by default, and miscellaneous operations only when Horus generates the number. Values Horus does not store (line quantity and unit price, exact analytic percentages) are echoed in the create response, so a later read can differ (section 6). Duplicate checks are needed before creating, because no idempotency key is documented; they are best effort (section 8).',
    '<b>There is no general “list invoices” endpoint.</b> The only invoice list returns open sales invoices and credit notes (header totals, open amount, payment status, no lines), with no purchase equivalent. Invoice retrieval therefore rebuilds every invoice from book entries (headers) and account history lines (lines, VAT, analytics, matching), and uses the open sales list for payment status. This is the clearest case of “one Chift route, several Horus endpoints”.',
    '<b>VAT is modelled differently.</b> Horus has no VAT-code list and accepts no VAT code on write: each invoice line carries a rate, an origin and a type (plus kind and condition for purchases), and only the combinations Horus publishes in two spreadsheets, per legislation (Belgium, Luxembourg) and direction, are valid (appendix C). The connector builds its own VAT-code catalogue from them, per folder, to serve Chift’s <code>tax_code</code> and VAT-code list. On read, ledger lines also return a Horus VAT code and heading whose meaning is undocumented (question H1).',
    '<b>No documented pagination, and month-based periods.</b> No Horus list endpoint has paging parameters, so lists are expected to return the full result for a folder or a month window (deduction). The connector emulates Chift pagination and day-level date filters and caches reference data per folder (C14). This should work for typical folder sizes; behaviour on large folders, rate limits and timeouts are unverified (H5).',
    '<b>What client applications will notice</b> (section 6): invoice ids that change when an entry is modified; numeric-only numbers; no deletion of a pushed invoice through the integration; one address per partner, no mobile or person fields, and every partner returned as a company; no line quantity or unit price; an account type that cannot be written; empty purchase VAT codes on read; entries that may wait for accountant review; foreign-currency invoices read back in euros once paid, and purchase invoices always; miscellaneous operations stored in euros (an operation in another currency is converted at the supplied rate and its original currency is not kept). Analytic balances are not stored per analytic account and can only be computed over a period (question C4).',
]

RECOMMENDATION = ('<b>Go, conditional on a short gate.</b> '
                  '<b>Gate 0, before build:</b> integration registration (H19) and a test license with a test folder (H17); Horus confirms that the published tax-combination spreadsheets are current and complete (H1, appendix C) '
                  'and states volumes, rate limits and timeouts (H5); Chift decides the posting mode (C1) and the rule for invoices sent without a number (C7). '
                  '<b>Phase 1:</b> reference reads (folders, journals, chart of accounts, analytic plans and accounts) and client and ledger-account creation, with a volume test on the largest test folder. '
                  '<b>Phase 2:</b> invoice creation and miscellaneous operations, tested on the VAT catalogue, numbering, duplicate and timeout scenarios. '
                  '<b>Phase 3:</b> the reads rebuilt from the ledger (invoice retrieval, outstanding items), once H2, H4, H5 and H8 are answered. '
                  '<b>Proposed descoping triggers:</b> a reduced VAT-code list if codes clients need cannot be expressed as accepted combinations; '
                  'a mandatory date window or journal filter on invoice retrieval if full-period reads do not scale; no build without a test license. '
                  'This plan is a proposal for Chift’s decision, not a commitment on behalf of Chift or Horus.')

HORUS_INTRO = ('Horus Office is used by accounting firms (fiduciaries) and SMBs. The Horus Software API reads and writes the data of one Horus Office database. '
               'Three structural facts shape the connector: each license has its own database and API URL, almost every call is scoped to one folder, '
               'and accounting entries are created through business-specific endpoints (invoices, bank, financial, miscellaneous operations) that all return a book entry id.')

ROUTES_INTRO = ('The table answers Task A: for each Chift route, the Horus endpoints that implement it, the call pattern, the verdict, the build complexity, '
                'what client applications will notice and the priority-1 questions the final design depends on. '
                'Each route card below gives the endpoints with their role and call count, the call sequence, the considerations specific to Horus and the key attribute mapping.')

TASK_B_INTRO = ('Each table lists every Chift attribute and query parameter of the route: the request side, and what the connector returns. '
                'Error responses follow the same pattern on all three routes: see the error rows of the client creation table and the error translation table in section 8. '
                'Use the filter to find a field or show only one mapping type. The evidence column quotes the Horus documentation and can be hidden with the button in the sidebar.')

TASK_B_SUMMARY = {
    'create_client': 'A Chift client is a Horus <b>company</b> (third party) with IsCustomer = true, created with <code>companies.new</code> in the folder. Horus requires a search key, a VAT-liability flag, a language and a country that Chift does not always send, so the connector derives them (the search key from the name, a proposal for Chift, D10 and C8). Creation returns only an id, so the connector reads the company back in two to three calls (company details, IBANs and, unless cached, the receivable account) to build the Chift response. Because one Horus company can be both customer and supplier, <code>force_merge</code> maps to flagging an existing supplier as customer.',
    'create_invoice': 'Customer invoices and refunds go to <code>invoices.sales.new</code>, supplier invoices and refunds to <code>invoices.purchases.new</code>, with Type 0 for an invoice and 1 for a credit note. The PDF can be sent in the same call (multipart). The connector first resolves the daybook, the partner, account search keys and cost sections from cached reference data, translates each Chift <code>tax_code</code> into the Horus VAT fields using the folder’s list of accepted combinations, converts analytic percentages into amounts, checks for an existing document number, and reads the entry back after creation (by default). Whether a “posted” invoice is confirmed in Horus depends on the posting mode chosen per connection (proposal, D12, C1).',
    'outstandings': 'Horus has open-item lists for both sides, but they differ. For clients, <code>invoices.sales.outstanding.list</code> gives the folder’s open sales invoices and credit notes with their open amount (documented), joined with <code>customers.outstanding</code> for the account and matching details. For suppliers, only ledger lines are available (<code>suppliers.outstanding</code>), so the open amount is computed by the connector: the line amount for an unmatched line; only if Horus also returns partially matched lines are they netted per matching group, with the remainder allocated to invoices oldest due date first (assumption, H8; allocation rule to agree with Chift, C5). Whether both ledger lists return every partner of the folder when no company filter is sent is to be confirmed (H8). Client items can carry their invoice currency; supplier items are always in euro (D4). Pagination is emulated, and amounts are signed per side (positive means owed).',
}

TASK_B_EXTRA = {
    'create_invoice': '''<div class="note"><span class="note-title">Worked example: analytic distribution</span>
<p>Chift line: base amount 1,000.00; plan DEPARTMENT split 50 % SALES / 50 % SUPPORT; plan PROJECT 100 % ALPHA.</p>
<p>Horus cost lines (amounts on combinations of cost sections, summing to the line base amount):</p>
<div class="table-wrap"><table><thead><tr><th>Amount</th><th>DEPARTMENT</th><th>PROJECT</th></tr></thead>
<tbody><tr><td class="num">500.00</td><td>SALES</td><td>ALPHA</td></tr><tr><td class="num">500.00</td><td>SUPPORT</td><td>ALPHA</td></tr></tbody></table></div>
<p>Combinations are the product of the plan percentages. Rounding uses the largest remainder so the cost lines always sum exactly to the base amount. Deriving combinations from independent plan splits is an assumption Chift should validate (question C9).</p></div>
<div class="note"><span class="note-title">VAT: from Chift tax_code to Horus fields</span>
<p>The connector exposes Horus tax combinations as synthetic VAT codes, for example <code>S-21-0-0</code> = sale, 21 %, origin 0 (national sale), type 0 (national) in the Belgian list. On write the code is decoded into TaxRate, TaxOrigin and TaxType (plus TaxKind, TaxCondition and TaxConditionValue for purchases). The valid combinations come from the two Horus tax-combination spreadsheets linked from the invoice endpoints (appendix C): 18 Belgian and 58 Luxembourg sales rows, 109 Belgian and 146 Luxembourg purchase rows. Origin codes differ by legislation and direction, so the catalogue holds one list per folder legislation (Belgium or Luxembourg) and direction, and a code outside the folder’s list is rejected before Horus is called. Horus is asked to confirm that the files are current and complete (question H1).</p></div>''',
    'outstandings': '''<div class="note"><span class="note-title">Sign convention</span>
<p>Customer lines: amount = debit − credit. Supplier lines: amount = credit − debit. A positive amount is always owed (a receivable for clients, a payable for suppliers; proposal, D5). Chift’s invoice due dates use a document view (a customer credit note is positive), so the same credit note is positive in invoice retrieval and negative here; question C5 asks which view Chift prefers. Open sales items take their sign from the documented transaction type (invoice positive, credit note negative); payments keep the sign Horus returns. The sign of credit notes is to be confirmed by a round-trip test (questions H2 and C5).</p></div>''',
}


IMPACT_INTRO = ('What client applications and their users will notice when they use the Horus connector, in plain language. '
                'Each row says what to do about it; the technical detail is in the route cards (section 4) and the attribute tables (section 5). '
                'Rows marked as proposals depend on decisions listed in section 9.')

CLIENT_IMPACT = [
    {'area': 'Invoice and operation ids',
     'notice': 'When an invoice or operation is modified, Horus stores it as a new entry with a new id, so an id kept by the client application stops working. Documented for changes made through the API; edits made by the accountant in Horus are assumed to behave the same (to confirm, H10).',
     'todo': 'Store journal and number with each pushed entry and match on them, not on the id alone. Always send a number: an entry pushed without one cannot be found again after the accountant edits it.',
     'routes': 'Invoice retrieval, invoice creation, miscellaneous operations', 'label': 'D'},
    {'area': 'Invoice and operation numbers',
     'notice': 'Numbers must be numeric: a number such as INV-2024/001 is rejected. Horus does not number invoices automatically through the API.',
     'todo': 'Send a numeric invoice_number and keep the number shown to customers in reference. Without a number, an invoice is pushed for accountant review and returned as a draft, whatever the posting mode (proposal, C7).',
     'routes': 'Invoice creation, miscellaneous operations', 'label': 'D'},
    {'area': 'Accountant review',
     'notice': 'Entries pushed through the integration may wait for the accountant’s review in Horus before they are final. Until then they come back as drafts, and outstanding items include them only when unposted items are requested.',
     'todo': 'Choose the posting mode when the connection is activated: review (proposed default) or direct posting (proposal, C1).',
     'routes': 'Invoice creation, miscellaneous operations, invoice retrieval, outstanding items', 'label': 'D'},
    {'area': 'Corrections',
     'notice': 'A pushed invoice cannot be deleted through the integration.',
     'todo': 'Validate before pushing; a wrong invoice is corrected by the accountant in Horus or offset with a credit note.',
     'routes': 'Invoice creation', 'label': 'D'},
    {'area': 'Duplicates after a timeout',
     'notice': 'If a create request times out, the integration checks whether the record was created before trying again. It can only do so when the request carried a number (invoices, operations) or a VAT number or your own reference (clients). Without one, it reports an unknown outcome instead of retrying.',
     'todo': 'Always send invoice and operation numbers, and a VAT number or your own reference for clients.',
     'routes': 'Client, invoice and operation creation', 'label': 'D'},
    {'area': 'VAT codes on read',
     'notice': 'For some purchase invoices the VAT code comes back empty, because Horus does not return every component of a purchase VAT combination. The VAT rate and amount are still returned.',
     'todo': 'Use the rate and amount when the code is empty.',
     'routes': 'Invoice retrieval', 'label': 'D'},
    {'area': 'Incremental synchronisation',
     'notice': 'Incremental synchronisation (updated_after) returns new and changed invoices. Deleted or replaced invoices are not reported, and a payment recorded by the accountant may only show up after a full re-sync.',
     'todo': 'Schedule a periodic full re-sync.',
     'routes': 'Invoice retrieval', 'label': 'D'},
    {'area': 'Customers and suppliers',
     'notice': 'One address per customer or supplier; delivery and invoicing addresses and mobile numbers are not stored. Every partner comes back as a company, and first and last names are not stored separately.',
     'todo': 'Send the main address and the full name.',
     'routes': 'Client creation, invoice creation, invoice retrieval', 'label': 'D'},
    {'area': 'Customer codes and duplicates',
     'notice': 'The integration creates the customer code that accountants see from the customer name, unless another scheme is agreed (proposal, C8). Without a VAT number or your own reference, sending the same customer twice creates two customers.',
     'todo': 'Send a VAT number or your own reference for every customer.',
     'routes': 'Client creation, invoice creation', 'label': 'A'},
    {'area': 'Invoice lines and terms',
     'notice': 'Lines keep amounts, VAT and analytics, but not quantity, unit price or unit: on read, a line has quantity 1 and a unit price equal to its amount. Delivery date, payment term and payment method are not returned on read.',
     'todo': 'Keep line detail and terms in the client application.',
     'routes': 'Invoice creation, invoice retrieval', 'label': 'D'},
    {'area': 'Foreign-currency invoices',
     'notice': 'Open sales invoices in another currency are returned in their own currency; once paid they come back in euro, and purchase invoices always come back in euro.',
     'todo': 'Keep the original-currency amounts on your side if you need them, and do not compare amounts of foreign-currency invoices across syncs until Chift decides the representation (C16, H4).',
     'routes': 'Invoice retrieval', 'label': 'A'},
    {'area': 'Foreign currency in open items',
     'notice': 'A customer’s open items can come back in two currencies: open sales invoices in their own currency, the other lines in euro. Supplier open items are always in euro.',
     'todo': 'Total open items per currency, not only per customer.',
     'routes': 'Outstanding items', 'label': 'A'},
    {'area': 'Foreign-currency operations',
     'notice': 'Miscellaneous operations are stored in euro: an operation in another currency is converted at the exchange rate supplied with it, and its original currency is not kept.',
     'todo': 'Send the exchange rate with every operation in another currency and keep the original amounts on your side. Who converts, Chift or the connector, is to be agreed (proposal, C15).',
     'routes': 'Miscellaneous operations', 'label': 'A'},
    {'area': 'Ledger accounts',
     'notice': 'A new account cannot be given a type; the type is derived when the chart of accounts is read. Filtering the chart on VAT or cash accounts may miss accounts that have never been used.',
     'todo': 'Do not rely on the type sent at creation; check VAT and cash account mappings with the accountant.',
     'routes': 'Ledger account creation, chart of accounts', 'label': 'D'},
    {'area': 'Analytics',
     'notice': 'Analytic dimensions whose values are typed freely, rather than chosen from a list, are not available in v1 (C9). Analytic accounts come without balances, which could only be computed over a period (C4).',
     'todo': 'Use list-type dimensions.',
     'routes': 'Analytic plans and accounts, invoices, miscellaneous operations', 'label': 'D'},
    {'area': 'Reference and memo',
     'notice': 'The invoice reference and the customer memo share one comment in Horus; both are returned, split on “ | ”.',
     'todo': 'Avoid “ | ” inside the reference.',
     'routes': 'Invoice creation, invoice retrieval', 'label': 'D'},
    {'area': 'Inputs Horus cannot store',
     'notice': 'Withholding tax, the Dutch G/N payment split, and a financial period or delivery date in another month than the invoice date have no equivalent in Horus, which serves Belgian and Luxembourg folders.',
     'todo': 'Do not send them. Requests that use them are rejected (proposal; Chift may prefer to accept them and drop the value, C3).',
     'routes': 'Invoice creation', 'label': 'D'},
]


CONCLUSION = ('A Horus connector is feasible for the full scope of the case. Every object in scope exists in Horus; VAT codes and payment terms, which the routes reference, '
              'have no Horus entity and are emulated by the connector. Horus has dedicated endpoints for pushing sales and purchase invoices with their PDF and for reading open items, '
              'likely high-value flows for Chift’s clients (to confirm with Chift). '
              'The work is in the translation layer: rebuilding invoices from the ledger, a VAT-code catalogue built from the Horus spreadsheets, analytics conversion, pagination emulation and duplicate protection. '
              'No change on the Horus side is required. Optional Horus improvements would remove client-visible limitations: the purchase VAT kind and the invoice type on read (H1, H2), '
              'automatic invoice numbering or an idempotency key (H3), and a purchase-side open-invoice list (H8).')

NEXT_STEPS = [
    'Spot-check the Chift specification used here (OpenAPI bundled with the <code>chift</code> SDK 0.6.16) against the live reference at docs.chift.eu, starting with tax_code, invoice_number, the outstanding-items parameters and folder_id.',
    'Gate 0 with Horus: confirm which documentation is authoritative (the case links the former apiary documentation, H20), register the integration (H19), obtain a test license and test folder (H17), and send the tier-1 questions of section 9, among them the tax-combination files (H1), credit notes (H2), numbering (H3), ledger currency (H4), volumes (H5), open items (H8), confirmation rights (H21) and the connection lifecycle (H24).',
    'Gate 0 with Chift: agree the tier-1 decisions (posting mode C1, numbering C7, caching and timeouts C14, conversion of foreign-currency operations C15), then the route-design conventions (tier 2).',
    'Phase 1: build the shared components (connection and token manager, folder rule, reference cache, pagination emulation, VAT catalogue built from the Horus spreadsheets, analytics converter), the reference reads, and client and ledger-account creation; run a volume test on the largest test folder. If that folder is too small to be representative, measure read-only on a larger real folder with its owner’s consent (proposal): account-histories.list over 12 months, the outstanding-item endpoints and the invoice-retrieval fan-out, against go/no-go thresholds agreed beforehand, repeated on a second license.',
    'Phase 2: invoice creation and miscellaneous operations, tested on the VAT catalogue, numbering, duplicate and timeout scenarios.',
    'Phase 3: invoice retrieval rebuilt from the ledger and outstanding items, once H2, H4, H5 and H8 are answered. Start with supplier outstanding items (open amounts rebuilt from open ledger lines; partial matching to confirm, H8), tested with a partially paid purchase invoice and a partially paid sale invoice. Use the attribute tables in section 5 as acceptance criteria and section 6 as the basis of the client-facing connector documentation.',
]

TAX_APPENDIX = '''<p>Horus publishes the accepted VAT combinations in two spreadsheets linked from the reference pages of <code>invoices.sales.new</code> / <code>invoices.sales.update</code> and <code>invoices.purchases.new</code> / <code>invoices.purchases.update</code> (“The accepted tax combinations … are available here”). Both were downloaded on 13 October 2026. Each file has one sheet of combinations per legislation and an “Available values” sheet with the code lists. <span class="lbl lbl-F" title="Documented">Documented</span></p>
<div class="table-wrap"><table><thead><tr><th>File</th><th>Belgium (BE)</th><th>Luxembourg (LU)</th><th>Fields of one combination</th></tr></thead><tbody>
<tr><td><code>Tax-combinations-sales.xlsx</code></td><td class="num">18 rows</td><td class="num">58 rows</td><td>TaxType, TaxRate, TaxOrigin; TaxCountryCode on OSS rows</td></tr>
<tr><td><code>Tax-combinations-purchases.xlsx</code></td><td class="num">109 rows</td><td class="num">146 rows</td><td>TaxType, TaxKind, TaxRate, TaxCondition, TaxConditionValue, TaxOrigin</td></tr>
</tbody></table></div>
<h4>How the files feed the VAT-code catalogue</h4>
<ul class="tight">
<li><b>One list per folder legislation and direction</b> (documented). Origin codes depend on both: sales origin 2 is “Exemption Art 44”, Belgian purchase origin 2 is “Achat Marchandises”. The folder legislation (BE or LU) is returned by the folder endpoints.</li>
<li><b>One synthetic code per row</b> (proposal, D2): <code>S-{rate}-{origin}-{type}</code> for sales, plus <code>-{country}</code> on OSS rows; <code>P-{rate}-{origin}-{type}-{kind}-{condition}-{condition value}</code> for purchases, with labels taken from the files. GET vat-codes returns the folder’s lists (C2); invoice creation rejects a code that is not in the folder’s list for the invoice direction before calling Horus; invoice retrieval encodes against the same list.</li>
<li><b>Purchase conditions</b> (documented): 1 DEDUC and 2 INVEST take true or false; 3 PCT takes 35, 50, 75 or 85; 0 COUNTRY is in the value list and on some European rows (with the country code as value in Luxembourg, without a value in Belgium).</li>
<li><b>Template rows</b>: the OSS sales rows (Belgian origin 13, Luxembourg origins 24, 26 and 29) and the Luxembourg purchase rows with the COUNTRY condition give rate and country as “XX” (documented). The connector treats them as templates, filled per transaction with the country and its rate (proposal); which concrete codes GET vat-codes lists for them is a Chift decision (C2).</li>
<li><b>On read</b> (documented): ledger lines also return <code>VatCode</code> and <code>VatHeading</code> strings whose meaning is undocumented; whether they are stable enough to map <code>tax_code</code> on read is asked in H1.</li>
</ul>
<h4>Documentation discrepancies (documented; asked in H1)</h4>
<ul class="tight">
<li>The TaxOrigin enums of the API reference do not cover the Luxembourg codes: sales 0–20 in <code>invoices.sales.new</code> versus up to 35 in the Luxembourg sales file, purchases 0–39 in <code>invoices.purchases.new</code> versus 40–56 in the Luxembourg purchase file. Codes 15, 16, 18, 19 and 20 (sales) and 12, 16, 22, 23 and 27 (purchases) carry different labels in the reference and in the files, for example sales 16 “Ventes Art 44” in the reference and “Ventes d’immobilisés” in the file, purchases 12 “Hors CEE sans facture” and “Achat TVA Marge”. The catalogue follows the files; Horus is asked which source is authoritative.</li>
<li><code>invoices.sales.new</code> describes TaxCountryCode as “Only used for OSS Vat lines (TaxOrigin = 13)”, but the Luxembourg sales file marks OSS rows with origins 24, 26 and 29.</li>
<li>The PCT condition value is 35/50/75/85 in the purchase combinations but 0.35/0.5/0.75/0.85 in “Available values”: the format to send is to be confirmed.</li>
<li>The files have no variant for folders that are not VAT liable; the combination such a folder must send is to be confirmed.</li>
<li>Minor source typo: one Belgian purchase row reads “Nationam” for “National”.</li>
</ul>
<h4>Example: Belgian sales combinations (18 rows)</h4>
<div class="table-wrap"><table><thead><tr><th>Connector code (proposal)</th><th>TaxType</th><th>TaxRate</th><th>TaxOrigin</th><th>Label in the file</th></tr></thead><tbody>
<tr><td><code>S-0-0-0</code></td><td>0 National</td><td class="num">0</td><td class="num">0</td><td>Vente nationale / Verkopen</td></tr>
<tr><td><code>S-0-1-0</code></td><td>0 National</td><td class="num">0</td><td class="num">1</td><td>Vente Cocontractant / Verkopen Medekontraktant</td></tr>
<tr><td><code>S-0-2-0</code></td><td>0 National</td><td class="num">0</td><td class="num">2</td><td>Exemption Art 44 / Vrijstellingen Art 44</td></tr>
<tr><td><code>S-0-4-0</code></td><td>0 National</td><td class="num">0</td><td class="num">4</td><td>Vidanges-Emballages / Leeggoed-Verpakking</td></tr>
<tr><td><code>S-0-5-0</code></td><td>0 National</td><td class="num">0</td><td class="num">5</td><td>Escompte / Diskonto</td></tr>
<tr><td><code>S-0-6-0</code></td><td>0 National</td><td class="num">0</td><td class="num">6</td><td>Autre exemption / Andere Vrijstellingen</td></tr>
<tr><td><code>S-0-7-0</code></td><td>0 National</td><td class="num">0</td><td class="num">7</td><td>Autre exemption avec MAJ du C.A. / andere Vrijstell. met UPD v/d Omzet</td></tr>
<tr><td><code>S-6-0-0</code></td><td>0 National</td><td class="num">6</td><td class="num">0</td><td>Vente nationale / Verkopen</td></tr>
<tr><td><code>S-12-0-0</code></td><td>0 National</td><td class="num">12</td><td class="num">0</td><td>Vente nationale / Verkopen</td></tr>
<tr><td><code>S-21-0-0</code></td><td>0 National</td><td class="num">21</td><td class="num">0</td><td>Vente nationale / Verkopen</td></tr>
<tr><td><code>S-21-3-0</code></td><td>0 National</td><td class="num">21</td><td class="num">3</td><td>Vente Taxe d&#x27;égalisation / Verkopen EgalisatieBelasting</td></tr>
<tr><td><code>S-0-8-1</code></td><td>1 European</td><td class="num">0</td><td class="num">8</td><td>Transfert de biens / Overdracht van Goederen</td></tr>
<tr><td><code>S-0-9-1</code></td><td>1 European</td><td class="num">0</td><td class="num">9</td><td>Ventes Marchandises / Verkopen Handelsgoederen</td></tr>
<tr><td><code>S-0-10-1</code></td><td>1 European</td><td class="num">0</td><td class="num">10</td><td>Livraison avec installation / Leveringen met installatie</td></tr>
<tr><td><code>S-0-11-1</code></td><td>1 European</td><td class="num">0</td><td class="num">11</td><td>Prestation hors Belgique / Diensten Buiten België</td></tr>
<tr><td><code>S-0-12-1</code></td><td>1 European</td><td class="num">0</td><td class="num">12</td><td>Travail à façon / Maakloonwerk</td></tr>
<tr><td><code>S-{rate}-13-1-{country}</code></td><td>1 European</td><td class="num">XX</td><td class="num">13</td><td>(OSS) Vente taxe soumis dans le pays européen / Verkoopbelasting ingediend in het Europese land</td></tr>
<tr><td><code>S-0-14-2</code></td><td>2 International</td><td class="num">0</td><td class="num">14</td><td>Exportations / Export</td></tr>
</tbody></table></div>
<p class="sub">Facts (row counts, codes, labels, discrepancies) come from the two files and the API reference; the connector codes, the template treatment and the per-folder lists are proposals.</p>'''

from curated_lists import *  # noqa: E402,F401,F403  (questions, edge cases, error map, building blocks, dependencies, working assumptions)
