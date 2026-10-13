"""Consolidated open questions for Horus and Chift (section 9). Ids are stable; each dict carries id, tier, q, why, routes.
Tiers: 1 = before build (go/no-go, architecture, gate 0), 2 = decides one route's design, 3 = can be verified in a test folder."""

QUESTIONS_INTRO = ('Consolidated and grouped by priority: tier 1 must be answered before build (go/no-go, architecture), tier 2 decides one route’s design, '
                   'tier 3 can be verified in a test folder. The route cards in section 4 list further detail-level questions; each one that changes a design decision is consolidated here.')

QUESTIONS_HORUS = [
    {'id': 'H1', 'tier': 1,
     'q': 'The accepted tax-combination spreadsheets linked from invoices.sales.new/update and invoices.purchases.new/update (downloaded 13 October 2026, appendix C) are the basis of the connector’s VAT-code catalogue, one list per folder legislation and direction. '
          '(a) Are they current and complete for Belgian and Luxembourg folders, and how are changes announced? '
          '(b) The TaxOrigin enums of the API reference (sales 0–20, purchases 0–39) do not include several origins used in the Luxembourg files (sales up to 35, purchases 40–56), and some codes carry different labels in the reference and in the files (for example sales 20, purchases 12): which source is authoritative, and does the API accept the Luxembourg codes? '
          '(c) Is TaxCountryCode expected for the Luxembourg OSS origins 24, 26 and 29 (the reference mentions only origin 13)? Is the PCT condition value sent as 35 or 0.35? Which value is sent with the COUNTRY condition on the four Belgian European purchase rows (origins 26, 7, 36 and 21), where the file leaves it empty? Which combination applies in a folder that is not VAT liable? '
          '(d) How is a combination that is not accepted rejected (status and ErrorType)? '
          '(e) What do VatCode and VatHeading on ledger lines represent: are they stable and one-to-one with a combination (kind included)? Could they be listed, could TaxKind be exposed on read, and is an endpoint listing accepted combinations planned?',
     'why': 'Invoice creation translates every tax_code into these fields; the VAT-code list and the VAT codes returned on read depend on the same catalogue.',
     'routes': 'Invoices, VAT codes'},
    {'id': 'H2', 'tier': 1,
     'q': 'Can a credit note (Type 1) be posted in a sales or purchase daybook, and an invoice in a credit-note daybook? Book entries do not expose the invoice type on read (TransactionType exists only on the open sales items, document types only on documents.list and documents.info): can the Type be exposed on book-entries.list or account-histories.list? '
          'Must credit-note amounts be positive, and with which sign do credit notes appear on read (book entries and invoices.sales.outstanding.list)? '
          'Are negative BaseAmount and TaxAmount values accepted on individual lines (discounts, rounding corrections) of an invoice (Type 0) or a credit note (Type 1), and are negative totals accepted with Type 0?',
     'why': 'Decides daybook selection and the sign rules on write, and invoice/refund classification on read.',
     'routes': 'Invoices, journals, outstanding items'},
    {'id': 'H3', 'tier': 1,
     'q': '(a) Is the document number unique per daybook and fiscal year, and is a duplicate number rejected (with which error)? Does Horus flag duplicate purchase invoices posted through the API, as it does for documents (status PossibleDuplicata)? '
          '(b) Is there an idempotency key, an external reference on invoices and operations that could serve as one, or a way to get the next free number? Can a create that timed out on the client side still be committed afterwards, and is a new book entry listed by book-entries.list as soon as the create call returns? '
          '(c) With Confirmed = true, what does invoices.sales.new do with Number 0, and invoices.purchases.new with Number null or 0: reject, or assign the next number? Could invoices get the automatic numbering (AutoGenerateNumber) that miscellaneous, bank and financial operations have? When an unconfirmed entry sent with number 0 is confirmed in Horus Office, is a number assigned automatically? '
          '(d) For miscellaneous operations, how does AutoGenerateNumber choose the next number when manually numbered entries exist, and must a manually supplied number on a confirmed entry follow the daybook’s sequence or format?',
     'why': 'Duplicate protection, safe retries after a timeout, and numbering of invoices and operations, including invoices sent without a number.',
     'routes': 'Invoices, operations, journals'},
    {'id': 'H4', 'tier': 1,
     'q': 'In which currency are ledger amounts (debit/credit, book-entry totals) and invoice totals expressed for foreign-currency documents, and in which direction is CurrencyRate given? Is the folder base currency always EUR? '
          'Can invoice-currency amounts be rebuilt from the line currency and rate for paid and purchase invoices? On invoices.sales.outstanding.list, what do TotalAmount and TotalCurrencyAmount each represent? '
          'On creation, does invoices.*.new read the amounts in the invoice currency or in euros, and is the default “rate of the day” taken at the invoice date or at the posting date?',
     'why': 'Correct amounts on write and on read for any foreign-currency document.',
     'routes': 'Invoices, outstanding items, folders, operations'},
    {'id': 'H5', 'tier': 1,
     'q': 'Are there rate limits, timeouts, maximum result sizes or maximum period spans on list endpoints (for example a multi-year account-histories.list on a collective account)? Could account-histories.list accept several company ids?',
     'why': 'List requests have no paging parameters, and several routes make one call per daybook or per schema; behaviour on large folders is otherwise unverified.',
     'routes': 'All list routes'},
    {'id': 'H6', 'tier': 3,
     'q': 'Which ErrorType values can be returned (duplicate VAT, search key or number, closed period, invalid tax combination, unknown account or cost section)? Do calls by id for an object in another folder return 403, 404 or 400? '
          'Do the invoice and miscellaneous-operation create endpoints themselves refuse a date in a closed period or a closed fiscal year?',
     'why': 'Specific error messages for Chift consumers, safe retry rules, and whether the connector’s closed-period check is the only guard.',
     'routes': 'All'},
    {'id': 'H7', 'tier': 2,
     'q': 'What are the rules for search keys (length, characters, case) for companies and accounts? Is a cost section search key unique per folder or per schema? Is ExternalReference unique within a folder? Does Horus generate a company search key when none is sent?',
     'why': 'The connector must generate company search keys, validate account numbers and look partners up by external reference.',
     'routes': 'Clients, invoices, accounts, analytics'},
    {'id': 'H8', 'tier': 1,
     'q': 'When the CompanyIds filter is omitted, do customers.outstanding and suppliers.outstanding return the open items of all partners, complete and without a cap? '
          'Do they return partially matched lines (MatchStatus 0), and if so every line of the matching group, payments included? Are Debit and Credit the original amounts or the open remainder? Does account-histories.list with NotMatchedOnly exclude partially matched lines? '
          'Can an item appear twice, as its prior-year line and as its carry-forward (IsReport) line, and how is a carry-forward line linked to its original document? Can one sale or purchase entry carry several customer or supplier lines with different due dates? '
          'Is a purchase-side equivalent of invoices.sales.outstanding.list planned?',
     'why': 'Decides whether outstanding items are complete (partially paid supplier invoices, carried-forward items), how supplier open amounts are computed, and the call pattern.',
     'routes': 'Outstanding items, invoice retrieval'},
    {'id': 'H9', 'tier': 3,
     'q': 'Where does the invoice header comment appear on read (partner-line comment, RemarkCompany or Remark)?',
     'why': 'Round-trip of reference and customer memo.',
     'routes': 'Invoices, outstanding items'},
    {'id': 'H10', 'tier': 2,
     'q': '(a) Do ledger period filters use calendar months or accounting periods? Are the accounting period and the VAT declaration month of an invoice posted through the API always derived from its date? '
          '(b) Does ModifiedAfter on book entries track changes to their lines and matching, and does matching or unmatching update the LastModifiedDate of the entry or of its partner line? Is ModifiedAfter strict or inclusive, how precise is LastModifiedDate and which clock sets it? Does ModifiedAfter on account-histories.list return every line of a replaced entry? '
          '(c) Does an edit or confirmation made by the accountant in Horus Office also create a new book entry id, as an API update does? Does confirming an entry keep its Id and Number, and does an entry edited by the accountant keep its DocumentNo? Is there any signal for deleted or replaced entries (for example webhooks)?',
     'why': 'Reliable incremental synchronisation and date filtering.',
     'routes': 'Invoices, operations, outstanding items'},
    {'id': 'H11', 'tier': 2,
     'q': 'What do CustomerActivitySuspended, Name2, Address2, Family and ContactPerson mean? How is an enterprise number written? Which concentration account applies when none is given? Does invoice creation refuse a company whose customer (sales) or supplier (purchases) flag is false?',
     'why': 'Mapping of active status, addresses, company numbers and receivable accounts, and partner checks on invoice creation.',
     'routes': 'Clients, invoices'},
    {'id': 'H12', 'tier': 2,
     'q': 'Can an account’s category be set, or is it derived from the number? What is the full list of IntCategory values (in particular VAT, supplier collective, bank and cash)? Is AccountCategory always filled for balance-sheet accounts? Does accounts.list include inactive and title accounts?',
     'why': 'Chift account type on creation and in the chart of accounts.',
     'routes': 'Accounts'},
    {'id': 'H13', 'tier': 3,
     'q': 'What do the cost endpoints return for a folder without the analytics module? Must a cost line carry one value per cost schema, or can it omit a non-mandatory schema? Is a line refused when a mandatory schema (including a free one) has no value? '
          'Is there a maximum number of cost lines per invoice line, and are cost lines with amount 0 accepted? Does a mandatory schema apply to every line, including a rounding-correction line? '
          'What do Mandatory, IsLocked, IsDefault and MasterCostSchema mean (is “master” a hierarchical parent, and can it be a Free-type schema)? Is the cost-history balance signed?',
     'why': 'Analytics on write and the analytic routes on read.',
     'routes': 'Analytics, invoices, operations'},
    {'id': 'H14', 'tier': 2,
     'q': 'What does IsUsed mean on daybooks? Can cash, temporary, system or cost daybooks receive entries through the API? Does fiscal-years.list return IsClosed? Is a miscellaneous operation refused when its date is on or before the miscellaneous-operations or VAT closure date, and with which error?',
     'why': 'Journal flags and posting rules.',
     'routes': 'Journals, operations'},
    {'id': 'H15', 'tier': 3,
     'q': 'Which relationship paths can be sideloaded with Include on companies.list, book-entries.list and account-histories.list, and with which fields?',
     'why': 'Can cut read-backs and invoice retrieval to fewer calls.',
     'routes': 'Clients, invoices'},
    {'id': 'H16', 'tier': 3,
     'q': 'book-entries.info takes only an id: can it return an entry from another folder of the same license? What does it return for an entry that was replaced or deleted? Is there any link from a replaced entry to its successor?',
     'why': 'Read-backs and single-invoice reads.',
     'routes': 'Invoices, operations, outstanding items'},
    {'id': 'H17', 'tier': 1,
     'q': 'Can Chift get a test license or test folder? Can test data be removed (the API has no delete for companies or invoices)? Are test licenses hosted the same way as production licenses?',
     'why': 'The API works on live data, and the volume test must reflect production conditions.',
     'routes': 'All write routes'},
    {'id': 'H18', 'tier': 3,
     'q': 'What is the maximum attachment size for multipart uploads?',
     'why': 'Validation of PDFs sent with invoices.',
     'routes': 'Invoices, operations'},
    {'id': 'H19', 'tier': 1,
     'q': 'How does Chift register an integration (client id and secret, redirect URIs, approval), and which Horus user should authorise the connection for an accounting firm and for an SMB so that the right folders are visible?',
     'why': 'The registration and Quickstart pages were not among the guide pages reviewed; the reference names registration as the first step, redirect URIs must be registered, and what a user sees through the API depends on their access in Horus.',
     'routes': 'All (connection setup)'},
    {'id': 'H20', 'tier': 1,
     'q': 'The case links horussoftwareapi.docs.apiary.io; this analysis used docs.horus-software.be (API reference dated 24 September 2026). Is docs.horus-software.be the authoritative documentation, and is the apiary version deprecated or for another API version? (Breaking changes are announced in the Changelog and by email, per the Changes &amp; versioning guide.)',
     'why': 'Every mapping in this report rests on the current documentation; the two versions were not compared.',
     'routes': 'All'},
    {'id': 'H21', 'tier': 1,
     'q': 'Confirmation through the API: may every integration, licence and user type (accountant or entrepreneur) set Confirmed = true on invoices and operations, or can the accounting firm restrict it? Does a connection authorised by a non-accountant user receive 403 when confirming? '
          'Which actions are blocked once an entry is confirmed, besides deleting a miscellaneous operation (for example .update and .lines.update)? Is Confirmed the accountant’s final validation, or does Verified follow it where an extra verification step is configured? Are unconfirmed entries included in balances, VAT returns and closings?',
     'why': 'Decides whether the proposed direct posting mode can be offered on every connection, and what “draft” means for clients.',
     'routes': 'Invoices, operations'},
    {'id': 'H22', 'tier': 3,
     'q': 'Amount validation on invoices.*.new: with OverrideTaxAmounts = false, what happens when a line’s TaxAmount differs from base × rate by more than one cent (refused or recalculated)? Is the header/line sum checked before or after the one-cent adaptation? Is a line with BaseAmount 0 and a non-zero TaxAmount accepted with OverrideTaxAmounts = true? '
          'Which decimal precision do BaseAmount, TaxAmount, TotalAmount and CostLines.Amount accept, and are the equality checks exact?',
     'why': 'Defines how the connector books VAT and rounding; can be verified in a test folder.',
     'routes': 'Invoices'},
    {'id': 'H23', 'tier': 3,
     'q': 'Outstanding items, to confirm or to verify in the test folder: which AccountType values can customers.outstanding and suppliers.outstanding return? Do Data.SumDebit and SumCredit cover exactly the returned lines? '
          'Does invoices.sales.outstanding.list return payments that are not linked to any invoice, and can a top-level payment row be partly allocated? With ConfirmedOnly = true, does OpenAmount still net unconfirmed linked elements?',
     'why': 'Control totals, signs and completeness of the outstanding items route.',
     'routes': 'Outstanding items'},
    {'id': 'H24', 'tier': 1,
     'q': 'OAuth connection lifecycle: which host pattern can a license api_url have, and can it be checked before the code exchange? Can the same user authorise the integration several times for one license, and do earlier refresh tokens stay valid? '
          'What happens to the tokens when the authorising user is deactivated or loses access to a folder? If a refresh succeeds but its response is lost, is the previous refresh token still usable, and which status does the token endpoint return for a revoked or already-used token? '
          'Can the integrator revoke a grant, and do refresh tokens have a maximum or idle lifetime?',
     'why': 'Safe activation, the token-store design and offboarding for Chift’s multi-tenant connections.',
     'routes': 'All'},
    {'id': 'H25', 'tier': 3,
     'q': 'Client creation, to confirm or to verify in the test folder: are PhoneNumber, Website and ContactPerson returned by companies.info as ContactPhone, ContactWebsite and ContactName? Is EnterpriseNumber ever returned for a VAT-liable company, and does the duplicate-VAT refusal apply to a number stored with IsVatLiable = false? '
          'Does Horus normalise VAT numbers before storing and comparing them, and is the duplicate check per folder or per license? Does companies.update refuse a VAT number already used by another company? Does companies.new fail entirely when one IBAN is invalid?',
     'why': 'Round-trip of the client response, duplicate checks and error handling on client creation.',
     'routes': 'Clients'},
]

QUESTIONS_CHIFT = [
    {'id': 'C1', 'tier': 1,
     'q': 'Posting mode (proposal, D12): should the connector offer a mode chosen per connection at activation, review (every entry pushed unconfirmed, for the accountant to confirm in Horus; proposed default) or direct (status “posted” confirmed in Horus)? Should the mode also be settable per folder for accounting-firm licences? '
          'The response always reports the status actually stored, so a “posted” request in review mode comes back as “draft”: is that acceptable? Across Chift connectors, does “draft” mean “not in the ledger” or “booked but not yet validated”?',
     'why': 'Horus pushes API entries unconfirmed so the accountant can review them, and “confirmed” means validated by the accountant. Confirmation changes numbering, confirmed miscellaneous operations cannot be deleted through the API, and the API has no delete for invoices.',
     'routes': 'Invoices, operations, outstanding items'},
    {'id': 'C2', 'tier': 2,
     'q': 'Is a connector-owned VAT-code catalogue acceptable for GET vat-codes, built per folder from the Horus tax-combination files (Belgian or Luxembourg list, sales and purchases), and is returning tax_code = null on read when the code is ambiguous acceptable? '
          'For OSS rows, whose rate and country vary per sale, should the list contain only the destination countries a consumer asks for? '
          'Should the VAT amounts sent by the consumer be booked exactly as stated (Horus OverrideTaxAmounts = true on every invoice, proposed) rather than recalculated by Horus within its one-cent tolerance, or rejected beyond a tolerance from base × rate (C19)?',
     'why': 'Horus has no VAT-code list and accepts no VAT code on write; the VAT code it returns on read is undocumented.',
     'routes': 'Invoices, VAT codes'},
    {'id': 'C3', 'tier': 2,
     'q': 'For inputs Horus cannot store (withholding tax, Dutch G/N split, accrual dates, a delivery date or forced period in another month than the invoice date, line quantity, extra addresses, the company number of a VAT-liable client, the account type on ledger-account creation, amounts with more than two decimals): reject, or accept and drop them? '
          'When several addresses are sent, which one becomes the single Horus address (proposal: main, then invoice)? The create responses have no warnings field: is logging on the connector side enough?',
     'why': 'Consistent behaviour across Chift connectors.',
     'routes': 'Clients, invoices, operations, accounts'},
    {'id': 'C4', 'tier': 2,
     'q': 'For values Horus does not hold on read: null or a default (analytic balance 0 or null, approval status “unknown”, empty next document numbers)? Should the folder address country be returned, given that it is available only through one extra Horus call per folder? '
          'For fields Horus does not store (line quantity, unit price, exact analytic percentages), should a create response echo the request (current proposal) or return what a later read returns?',
     'why': 'Avoid misleading defaults, and responses that differ from later reads.',
     'routes': 'Invoices, journals, analytics, folders'},
    {'id': 'C5', 'tier': 2,
     'q': 'Sign conventions. (a) Input: do consumers send customer_refund and supplier_refund amounts as positive values, as Chift’s due-date convention describes for output (“A positive amount represents debit on customer invoices and supplier refunds or credit on supplier invoices and customer refunds”) and as invoice retrieval returns them? Do consumers send discount or deposit lines as negative lines on invoices, and can an invoice have a negative total? '
          '(b) Read: when the document type cannot be read, which misclassification is more acceptable: a credit note keyed into a sales daybook returned as an invoice, or a negative invoice returned as a refund? '
          '(c) Outstanding items: should a customer credit note or an unallocated payment be negative (balance view, proposed in D5: positive = owed) or positive (document view, as for invoice due dates)? Is a credit note posted in a sales journal acceptable as journal type customer_invoice with a negative amount, since an outstanding item has no document-type field? '
          '(d) In a partly matched group, may the open amount be allocated to the invoice lines, oldest due date first (proposed), or is pro-rata preferred?',
     'why': 'The request schema does not state the input sign, Horus does not expose the document type on read, and the due-date (document) view and the proposed balance view differ: the same credit note would be positive in invoice retrieval and negative in outstanding items.',
     'routes': 'Invoices, outstanding items'},
    {'id': 'C6', 'tier': 2,
     'q': '(a) On a duplicate (VAT number, external reference, document number): return an error (400/409) or the existing record, and what does Chift’s idempotency guide promise for a repeated invoice_number? For supplier invoices without a number, is a duplicate check on supplier, date and total acceptable? '
          '(b) When a create times out and the outcome cannot be verified (invoice without number, operation numbered by Horus), which error should the connector return, and is “no automatic retry” consistent with other connectors? '
          '(c) force_merge: may client data fill empty supplier fields or overwrite them, and what if both carry a different external_reference? Should an id that is already a customer (proposal: success, nothing changed), or is not a supplier (proposal: 400), be handled otherwise?',
     'why': 'Duplicate and merge policy must match other connectors; Horus keeps one external reference, name, address and VAT number per company, and documents no idempotency key.',
     'routes': 'Clients, invoices, operations'},
    {'id': 'C7', 'tier': 1,
     'q': 'Numbering. (a) Is rejecting non-numeric invoice and operation numbers (and values with leading zeros) acceptable, with the number shown to customers sent in reference? '
          '(b) For an invoice to be confirmed without invoice_number: push it for review with number 0 and return “draft” (proposed default), reject it with 422, or let the connector generate the next number of the journal (max + 1, opt-in only, race risk under concurrent pushes)? '
          '(c) May the connector require invoice_number and operation_number, or assign one, so that every pushed entry keeps a business key after an accountant edit? '
          '(d) Is operation_number meant to become the accounting entry number, or is it the client’s own reference (Horus could then number confirmed operations itself and keep the client value in the line comment)?',
     'why': 'Chift’s contract says a missing number is generated “according to the system’s numbering rules”, but Horus numbers only confirmed bank, financial and miscellaneous operations, not invoices, and stores numbers as numbers; an entry without a number cannot be found again after an accountant edit.',
     'routes': 'Invoices, operations'},
    {'id': 'C8', 'tier': 2,
     'q': '(a) What does partner_info.account_number mean: a third-party code or a ledger account? When it matches an existing partner whose name differs, should the connector refuse (409) or reuse it with a warning? '
          '(b) Is partner_info needed at all for Horus, where partners can be created through the API? If an invoice targets a company without the customer or supplier role, should the connector add the role or reject the invoice? '
          '(c) How should the third-party code (search key) of a new company be generated: from the name (proposed), from external_reference, a per-consumer prefix and sequence, or supplied by the consumer? '
          '(d) When a client has neither VAT number nor external_reference and a company with the same name exists, should the connector create a second record, warn, or refuse?',
     'why': 'The Chift specification does not describe account_number and describes partner_info for tools that cannot create partners by API; the code is visible to accountants, and without a VAT number or external reference there is no reliable duplicate check.',
     'routes': 'Clients, invoice creation'},
    {'id': 'C9', 'tier': 2,
     'q': 'Is deriving analytic combinations from independent per-plan percentages acceptable? Should Get analytic plans list Free-type Horus dimensions (which have no enumerable analytic accounts and are not accepted on write in v1), or hide them (proposed)? '
          'On small amounts, is a read-back distribution that differs from the one sent acceptable (0.10 sent as 33/33/34 reads back as 30/30/40)? For a plan that covers only part of a line, should it be left out (proposed) or returned as a partial distribution?',
     'why': 'Horus allocates amounts to combinations of cost sections.',
     'routes': 'Invoices, analytics'},
    {'id': 'C10', 'tier': 2,
     'q': 'Should unconfirmed Horus entries be returned as drafts or excluded by default? Is it acceptable that an invoice id changes when the accountant updates it? '
          'If a credit note sits in a sales journal (folders without a credit-note journal), is returning it as customer_refund under that journal’s id acceptable when journal_ids is used as a filter? '
          'Do consumers rely on updated_after to detect status changes such as “paid”, and what periodic full re-sync is acceptable, given that deletions and replaced ids are not reported? '
          'For outstanding items with unposted_allowed = false, should an unposted payment reduce the open amount of a posted invoice?',
     'why': 'Read behaviour for entries under accountant review. In review mode (D12), every invoice pushed through Chift stays unconfirmed until the accountant confirms it, so excluding unconfirmed entries by default would hide them.',
     'routes': 'Invoice retrieval, outstanding items'},
    {'id': 'C11', 'tier': 2,
     'q': 'Which default period should invoice retrieval use when no dates are given (proposal: the current fiscal year), and how far back must an updated_after poll look (full history or a bounded look-back)? Are consumers expected to dedupe items re-delivered by a safety overlap?',
     'why': 'Horus requires a month window and its lists have no paging parameters: a bounded default limits the volume of each read, and the look-back drives the cost of every incremental poll.',
     'routes': 'Invoice retrieval'},
    {'id': 'C12', 'tier': 2,
     'q': 'Should the Horus connector always enable the multiple-folders feature? Does the Chift platform reject a folder_id that was not selected at activation before the request reaches the connector, or must the connector enforce it? '
          'Can several Chift consumers share one Horus license (for example several SMB clients of one accounting firm), and who normally activates the connector for an SMB whose books a firm keeps?',
     'why': 'Accounting-firm licenses hold many folders, and one Horus token sees every folder its user can access.',
     'routes': 'All'},
    {'id': 'C13', 'tier': 3,
     'q': 'Documentation remark (no decision needed): FolderItem.main_currency is described as ISO 3166-1 (a country standard; ISO 4217 is meant), and the line tax_amount formula omits the division by 100.',
     'why': 'Small corrections to the Chift API reference.',
     'routes': 'Folders, invoices'},
    {'id': 'C14', 'tier': 1,
     'q': 'Can a connector keep a per-folder reference cache and a short-lived result cache between page calls of the same request? What is the timeout of a synchronous request, and is there a background pattern for heavy reads?',
     'why': 'Horus list requests have no paging parameters: the connector fetches a full list once and slices it. Without a cache between page calls, every page re-reads the whole period.',
     'routes': 'All list routes'},
    {'id': 'C15', 'tier': 1,
     'q': 'Foreign-currency miscellaneous operations: Horus operation lines have no currency or rate field, so amounts are stored in the folder currency (assumed EUR, H4). When an operation arrives in another currency with currency_exchange_rate, does Chift core convert the amounts before calling the connector (as other_currencies_allowed = false suggests), or must the connector convert? '
          'In which direction is the rate expressed, how should a rounding residue on a balanced operation be absorbed, and should the response echo the original currency or EUR with rate 1?',
     'why': 'Chift’s contract requires the rate for operations in another currency and describes conversion for journals that do not allow other currencies.',
     'routes': 'Operations'},
    {'id': 'C16', 'tier': 2,
     'q': 'Foreign-currency documents on read: Horus gives invoice-currency amounts only for open sales invoices, so under the current mapping such an invoice switches to euro once paid, and purchase invoices always come back in euro (never euro amounts with a foreign code, D4). '
          'Until Horus confirms the currency of ledger amounts (H4), keep this behaviour (disclosed), or return one stable euro representation (currency “EUR”, rate 1) for every foreign-currency invoice (the option favoured in this analysis, since a currency change on the same id is harder for consumers)? '
          'In which direction should currency_exchange_rate be expressed? Is it acceptable that one partner’s outstanding items mix currencies (document currency where Horus provides it, euro otherwise)?',
     'why': 'Consumers that sync with updated_after would otherwise see the same invoice change currency and amounts; the Chift contract does not define the rate direction.',
     'routes': 'Invoice retrieval, outstanding items'},
    {'id': 'C17', 'tier': 2,
     'q': 'Outstanding items: (a) should an invoice with several due dates be one item with several due_dates, or one item per instalment (current proposal: one item per customer or supplier line)? (b) Should payments and credit balances not allocated to any invoice appear as items? '
          '(c) Are matching numbers that are unique only per partner acceptable as they are, or should they be prefixed? (d) Should items of employees or other beneficiaries be excluded? (Allocation within a partly matched group and signs: C5.)',
     'why': 'Chift’s due_dates lists all due dates of an outstanding item, while Horus has one due date per ledger line; these choices change what clients see as open items and the totals per item.',
     'routes': 'Outstanding items'},
    {'id': 'C18', 'tier': 2,
     'q': 'When a list filter cannot be honoured exactly on Horus (approval_status on a target without an approval workflow, an unknown or wrong-type journal_id, a chart-of-accounts type such as VAT or cash that can only be estimated), should the connector return 400, ignore the filter, or return a best-effort or empty result? Is Horus “Verified” an acceptable stand-in for “approved”?',
     'why': 'Silent empty or approximate results are hard for consumers to detect; behaviour should match other connectors.',
     'routes': 'Invoice retrieval, chart of accounts'},
    {'id': 'C19', 'tier': 2,
     'q': 'Amount plausibility on invoice creation: what difference between header and lines may invoice_correction absorb (a fixed amount, or one cent per line), with larger differences rejected? Should lines whose tax departs from untaxed amount × rate beyond a tolerance be rejected, given that VAT is booked as sent (C2)?',
     'why': 'Chift defines invoice_correction for rounding and tax_amount as untaxed amount × rate; without limits, real data errors would be booked on the correction account or as VAT.',
     'routes': 'Invoice creation'},
    {'id': 'C20', 'tier': 2,
     'q': 'Error conventions: for validation errors without a predefined error_code (unknown country, invalid IBAN, unknown or inactive account), which status and error_code do other connectors return, 400 or 422? Should a VAT number containing dots or spaces be rejected with ERROR_INVALID_VAT_FORMAT, as its message suggests, or normalised? '
          'Which status and code signal re-authorisation required, a persistent upstream error and an unknown create outcome (C6), and does the platform retry a connector call after a timeout?',
     'why': 'Consumers branch on status and error_code, which must match other connectors.',
     'routes': 'All'},
]
