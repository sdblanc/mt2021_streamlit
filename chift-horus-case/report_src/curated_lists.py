"""Curated lists for the external report: questions, edge cases, error translation, building blocks, dependencies and working assumptions."""

BUILDING_BLOCKS = [
    {'name': 'Connection and token manager', 'what': 'Stores api_url, access token, single-use refresh token and expiry per Horus license. Refreshes proactively, one refresh at a time per connection, and persists the new token pair before use.', 'routes': 'All'},
    {'name': 'Folder resolution', 'what': 'One rule for every route: folder_id is required when the connection has several selected folders; otherwise the single selected folder is used.', 'routes': 'All'},
    {'name': 'Reference-data cache per folder', 'what': 'Daybooks, chart of accounts, cost schemas and sections (including inactive ones), fiscal years and folder settings. Loaded once per folder, as the Horus guide recommends, and refreshed when a lookup misses (connector design).', 'routes': 'All write routes, invoices, journals, chart of accounts, outstanding items'},
    {'name': 'Pagination and filter emulation', 'what': 'Horus lists return everything. The connector fetches, filters by day, type or status, sorts deterministically and slices Chift pages, with a short-lived cache so consecutive pages do not refetch.', 'routes': 'All list routes'},
    {'name': 'VAT-code catalogue', 'what': 'Connector-owned list of valid Horus tax combinations with one id grammar, e.g. <code>S-21-0-0</code> (sales: rate 21 %, tax origin 0, tax type 0) and <code>P-21-2-0-0-1-true</code> (purchases: rate, origin, type, kind, condition, condition value; see D2). Serves Chift VAT codes, decodes tax_code on write and encodes it on read.', 'routes': 'Invoice creation, invoice retrieval, VAT codes'},
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
    ('Duplicate found by the connector’s pre-check (VAT number, external reference or document number)', 'Do not create.', '409 or 400 with the existing id, per question C6'),
    ('500 / timeout on a read', 'Retry with exponential backoff, as Horus advises.', 'Error after retries'),
    ('500 / timeout on a create', 'Never retry blindly. Search for the record first (external reference, VAT number, document number), and re-post only if nothing is found.', 'Created record, or an error'),
]

DECISION_DEPENDS = {'D1': 'H2', 'D2': 'H1, C2', 'D3': 'H9', 'D4': 'H4', 'D5': 'C5', 'D6': 'H14', 'D7': 'C12', 'D8': 'H13, C9', 'D9': 'H11', 'D10': 'C8', 'D11': 'n/a', 'D12': 'C1, C6, H3', 'D13': 'H6, H16'}

DECISIONS = [
    ('D1', 'Credit notes: on write, use the credit-note daybook (Horus daybook type 250 for sales, 150 for purchases), falling back to the sales or purchase daybook (type 200 or 100). On read, always scan both daybook types and classify each entry as invoice or credit note from the sign of the customer/supplier line; for open sales items, the documented TransactionType takes precedence.', 'Credit notes posted in a sales daybook (by the connector or by an accountant) must still come back as refunds.'),
    ('D2', 'One synthetic VAT-code id grammar for writing, reading and the VAT-code list: <code>S-{rate}-{origin}-{type}</code> for sales (plus <code>-{country}</code> for OSS lines, origin 13), <code>P-{rate}-{origin}-{type}-{kind}-{condition}-{condition value}</code> for purchases (<code>x</code> for an unused component). On read, return a code only when exactly one catalogue entry matches.', 'Horus has no VAT-code entity, and the purchase “kind” cannot be read back.'),
    ('D3', 'reference and customer_memo share the Horus invoice comment as <code>{reference} | {customer_memo}</code>, split the same way on read.', 'Horus has a single free-text comment on invoices.'),
    ('D4', 'Ledger amounts are treated as folder currency (EUR). EUR amounts are never returned with a foreign currency code.', 'The currency of ledger amounts is not documented.'),
    ('D5', 'Outstanding amounts are signed by side: debit minus credit for customers, credit minus debit for suppliers (positive means owed).', 'One consistent sign per side across all code paths.'),
    ('D6', 'One daybook-type to journal-type table for all routes. Daybook types without a documented posting endpoint are returned with Chift <code>blocked = true</code>.', 'Journals, invoices, operations and outstanding items must agree.'),
    ('D7', 'folder_id is required when a connection has several selected folders.', 'Accounting-firm licenses hold many folders.'),
    ('D8', 'One analytics cache per folder, largest-remainder rounding, and “free” cost schemas excluded in v1.', 'Free schemas have no listable values.'),
    ('D9', 'One shared mapping from a Horus company to a Chift client/supplier/partner, used by client creation, invoice retrieval and invoice creation: active = NOT CustomerActivitySuspended (assumption; meaning undocumented); one “main” address from Address (+Address2), ZipCode, Locality, CountryCode; phone = ContactPhone, email = ContactEmail; is_company always true (Horus does not store it); language = lowercase Horus language, “XX” → null; on write, a missing or unsupported language falls back to the folder language; account_number = concentration account search key.', 'The same company must look the same in every route.'),
    ('D10', 'partner_info on invoice creation reuses the client-creation rules (search key, role flags).', 'Avoid duplicate or half-configured companies.'),
    ('D11', 'The verdict definitions of section 2 are applied identically to every route.', 'Comparable verdicts across routes.'),
    ('D12', '“draft” → unconfirmed; “posted” → confirmed, with a per-consumer option to always push unconfirmed. Duplicate check on the document number before every create that supplies an invoice or operation number.', 'Accountant review is the Horus default for API entries.'),
    ('D13', 'Every call by id checks that the object belongs to the requested folder.', 'Calls by id take no folder, so an id from another folder of the same license would otherwise be accepted.'),
]

DEPS_INTRO = ('Several requested routes depend on Chift routes outside the case list. Without them, a consumer cannot supply valid ids to the requested routes.')

DEPENDENCIES = [
    {'name': 'VAT codes (GET vat-codes)', 'why': 'Every invoice line requires <code>tax_code</code>, the id of a VAT code in the accounting software.', 'support': 'No VAT-code entity or endpoint. Served from a connector-owned catalogue of valid Horus tax combinations, with one id grammar shared with invoice creation and retrieval.', 'label': 'D'},
    {'name': 'Supplier creation (POST suppliers)', 'why': 'Purchase invoices reference the supplier by <code>partner_id</code> (optional in the specification; <code>partner_info</code> can create a missing supplier instead).', 'support': 'Workaround, same as client creation: <code>companies.new</code> with IsSupplier = true and the same rules (search key, duplicate VAT check, read-back with <code>companies.info</code>).', 'label': 'D'},
    {'name': 'Clients and suppliers lists (GET clients / suppliers)', 'why': 'Consumers look up existing partners before creating invoices.', 'support': '<code>companies.list</code> filtered on IsCustomer or IsSupplier; <code>updated_after</code> maps to ModifiedAfter. Chift’s free-text search (an OR over several fields) and pagination are emulated.', 'label': 'D'},
    {'name': 'Payment terms (GET payment-terms)', 'why': 'Optional <code>payment_term_id</code> on invoices.', 'support': 'No payment-term entity. Horus stores a compact delay code per company (for example 30E = 30 days end of month) and invoices take an explicit due date. Return a synthetic list or an empty list; <code>payment_term_id</code> is ignored on creation.', 'label': 'D'},
    {'name': 'Payment methods (GET payment-methods)', 'why': 'Optional <code>payment_method_id</code> on invoices.', 'support': 'Fixed PaymentMode list documented by Horus (bank transfer, domiciliation, card, PayPal, Doccle, Digiteal, check, bill draft…), returned as a constant list.', 'label': 'D'},
    {'name': 'Attachments (GET attachments)', 'why': 'Invoices return <code>attachments_info</code>; files are fetched separately.', 'support': '<code>book-entries.info</code> gives the main document reference, then <code>documents.download</code> returns the bytes. Finding annexes needs a date-bounded <code>documents.list</code>.', 'label': 'D'},
    {'name': 'Bookyears (GET bookyears)', 'why': 'Context for periods, closure checks and journal numbering.', 'support': '<code>fiscal-years.list</code>; the closed flag is documented only on <code>fiscal-years.info</code> (one call per year).', 'label': 'D'},
]

RISKS_INTRO = 'Situations the connector must handle explicitly. Most follow from three Horus traits: no documented idempotency key, entries that get a new id when updated, and lists without documented pagination.'

EDGE_CASES = [
    {'case': 'A create call times out or returns 500 (client, invoice, operation, account).', 'handling': 'Never retry blindly. Search for the record first (external reference, VAT number, document number) and re-post only if it does not exist.', 'routes': 'All write routes', 'label': 'D'},
    {'case': 'The client’s VAT number already exists, as a customer or as a supplier only.', 'handling': 'Pre-check before creating. Return an “already exists” error with the existing id, and suggest <code>force_merge</code> when the match is a supplier.', 'routes': 'Client creation', 'label': 'D'},
    {'case': 'The invoice date falls in a period the accountant has closed.', 'handling': 'Check the fiscal-year closure dates before posting, as Horus recommends, and return a clear error. Horus offers no forced period on invoice creation.', 'routes': 'Invoice and operation creation', 'label': 'F'},
    {'case': 'Header totals and line totals differ by rounding.', 'handling': 'Horus checks totals = base + tax and the sum of lines; tax within one cent is recalculated unless OverrideTaxAmounts is set. Validate in the connector first and use <code>invoice_correction</code> when needed.', 'routes': 'Invoice creation', 'label': 'F'},
    {'case': 'An analytic split such as 33 / 33 / 34 %.', 'handling': 'Largest-remainder rounding so cost lines sum exactly to the line base amount.', 'routes': 'Invoice creation', 'label': 'D'},
    {'case': 'A tax_code that is not a valid Horus combination.', 'handling': 'Reject with 422 before calling Horus.', 'routes': 'Invoice creation', 'label': 'D'},
    {'case': 'A foreign-currency invoice or operation.', 'handling': 'Invoices: allowed when the folder accepts currencies (documented). Miscellaneous operations: the request has no currency field, so non-EUR operations are rejected (derived; proposed default, see C3). On read, ledger amounts are treated as EUR until Horus answers H4, and EUR amounts are never paired with a foreign currency code (assumption, D4).', 'routes': 'Invoices, operations, outstanding items', 'label': 'D'},
    {'case': 'The accountant edits an invoice created through the API.', 'handling': 'Horus generates a new book entry id, so the Chift id changes. Reconcile on daybook and document number; disclose this to consumers.', 'routes': 'Invoice retrieval and creation', 'label': 'F'},
    {'case': 'A credit note stored in a sales or purchase daybook.', 'handling': 'Read both daybook types and classify each entry by the sign of the customer or supplier line; for open sales items, TransactionType overrides the sign.', 'routes': 'Invoice retrieval', 'label': 'A'},
    {'case': 'Several possible journals and no journal_id.', 'handling': 'Auto-select by daybook type when exactly one candidate exists; otherwise 400 “journal_id required”.', 'routes': 'Invoice and operation creation', 'label': 'D'},
    {'case': 'An inactive account or cost section, or analytics sent to a folder without the analytics module.', 'handling': 'Reject with 422 before calling Horus.', 'routes': 'Write routes', 'label': 'D'},
    {'case': 'An id that belongs to another folder of the same license.', 'handling': 'Check the folder on every call by id; return 400.', 'routes': 'All', 'label': 'D'},
    {'case': 'Partial payments and instalments.', 'handling': 'Open amounts come from matching groups. Horus has no instalment structure: an outstanding item has at most one due date, and an invoice has one due date per customer/supplier line (normally one for invoices posted through the API).', 'routes': 'Outstanding items, invoice retrieval', 'label': 'D'},
    {'case': 'An open item carried over from the previous fiscal year.', 'handling': 'Identify the opening entry through its entry type and link the original document where Horus provides it; otherwise leave <code>original_document</code> empty.', 'routes': 'Outstanding items', 'label': 'A'},
    {'case': 'Two Chift calls for the same consumer refresh the token at the same time.', 'handling': 'Serialise refreshes per connection; refresh tokens are single-use.', 'routes': 'All', 'label': 'F'},
    {'case': 'A large folder (an accounting firm’s client with years of entries).', 'handling': 'Full lists with emulated pagination, narrow month windows, per-folder caching and gzip. Horus documents no size or rate limits.', 'routes': 'All list routes', 'label': '?'},
]

from curated_questions import *  # noqa: E402,F401,F403  (questions for Horus and Chift)
