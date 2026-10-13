"""Hand-written narrative for the concise Horus connector assessment (gen_assess.py)."""

TITLE = 'Horus Connector Assessment'
DESCRIPTION = ("Concise answer to Part 1 of Chift's product/tech case: feasibility of a Horus accounting connector, "
               "route-level mapping (Task A), attribute-level mapping (Task B), key limitations and open questions.")
RAIL_LABEL = 'Chift × Horus · Part 1'
REFERENCE_FILE = 'chift_horus_mapping_report.html'

HEADER_HTML = f'''<header class="doc-head">
  <p class="eyebrow">Chift product/tech case · Part 1 · Mapping Chift – Horus</p>
  <h1>Horus connector assessment</h1>
  <p class="lede">Can Chift's accounting routes be served from the Horus Software API, which Horus endpoints would each route use,
  how the requested attributes map, and what must be confirmed before building.</p>
  <div class="meta">
    <span>Prepared by <b>Silas Deblanc</b></span>
    <span>For <b>Chift, Product &amp; Tech</b></span>
    <span>Date <b>13 October 2026</b></span>
    <span>Status <b>For discussion</b></span>
    <span>Basis <b>desk analysis of the documentation, no live API calls</b></span>
    <span>Detailed reference <b><a href="{REFERENCE_FILE}">full technical mapping</a></b> (unchanged; corrections in appendix B)</span>
  </div>
</header>'''

FOOTER_HTML = ('Prepared by Silas Deblanc for the Chift product/tech case. Based only on the case description, the Chift API specification and the Horus '
               'Software API documentation listed in appendix A. Proposals in this report are analysis, not commitments on behalf of Chift or Horus.')

# ---------- 1. Executive summary ----------
SHORT = {  # route display names used in the summary sentence
    'Client creation': 'client creation', 'Journal retrieval': 'journals', 'Ledger account creation': 'ledger account creation',
    'Chart of accounts retrieval': 'chart of accounts', 'Accounting folders retrieval': 'folders', 'Miscellaneous operation creation': 'miscellaneous operations',
    'Analytic plans retrieval': 'analytic plans', 'Analytic accounts retrieval': 'analytic accounts', 'Invoice retrieval': 'invoice retrieval',
    'Invoice creation': 'invoice creation', 'Outstanding items': 'outstanding items',
}


def _names(rs):
    out = []
    for r in rs:
        key = next((k for k in SHORT if r['route'].startswith(k)), r['route'])
        out.append(SHORT.get(key, r['route']))
    return ', '.join(out[:-1]) + ' and ' + out[-1] if len(out) > 1 else ''.join(out)


WORDS = {0: 'No', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven'}


def answer(routes):
    by = {lvl: [r for r in routes if r['feasibility'] == lvl] for lvl in ('Confirmed', 'Feasible with assumptions', 'Needs confirmation', 'Not yet concluded')}
    parts = [f'<b>The Horus Software API has a documented endpoint for the core object of every Chift route in scope, so the documentation rules out none of the {len(routes)} routes.</b> '
             'That is not the same as every route being settled. ']

    def n(rs, one, many):  # count word plus singular or plural wording
        return f'{WORDS[len(rs)]} {one if len(rs) == 1 else many}'
    if by['Confirmed']:
        rs = by['Confirmed']
        parts.append(f'{n(rs, "route is", "routes are")} confirmed by the documentation ({_names(rs)}). ')
    if by['Feasible with assumptions']:
        rs = by['Feasible with assumptions']
        parts.append(f'{n(rs, "is feasible but relies", "are feasible but rely")} on assumptions the documentation does not confirm ({_names(rs)}). ')
    if by['Needs confirmation']:
        rs = by['Needs confirmation']
        parts.append(f'{n(rs, "needs", "need")} answers from Horus or decisions from Chift before {"its" if len(rs) == 1 else "their"} design is final ({_names(rs)}); '
                     'these are likely the highest-value routes for Chift’s clients (to confirm with Chift) and carry most of the build effort. ')
    if by['Not yet concluded']:
        rs = by['Not yet concluded']
        parts.append(f'{WORDS[len(rs)]} cannot be concluded yet ({_names(rs)}). ')
    parts.append('Behaviour on large folders cannot be concluded from the documentation for any list route.')
    return ''.join(parts)
TILE_NOTE = ('Each route is rated on functional feasibility, by the weakest point that materially affects it (levels explained in section 3). '
             '"Confirmed" means the documentation shows Horus can do what the route needs; documented limitations still apply. '
             'Build effort (analyst’s estimate, to calibrate with Chift): low for folders, analytic plans, journals and analytic accounts; medium for '
             'client creation, ledger account creation, chart of accounts and miscellaneous operations; high for invoice creation, invoice retrieval and '
             'outstanding items. Task A is the route-level mapping of the ten routes listed in the case; Task B is the attribute-level mapping of three routes.')
KEY_MESSAGES = [
    '<b>One Chift call often means several Horus calls.</b> Horus needs its own references (journal, partner, account and analytic codes), and a create returns only an id. '
    'The connector therefore looks up reference data, cached per folder, and reads records back. Horus has no endpoint that lists all invoices '
    '(only open sales invoices and credit notes are listed, without lines), so invoice retrieval is rebuilt from ledger data.',
    '<b>VAT is the main mapping gap.</b> Horus accepts no VAT code, only a combination of rate, origin and type (plus kind and condition for purchases), from lists Horus publishes per country and direction. '
    'Chift\u2019s <code>tax_code</code> needs a translation table: a proposal Chift must accept and Horus must confirm.',
    '<b>Some Chift data has no place in Horus.</b> Examples: line quantity and unit price, several addresses, person names, withholding tax, invoice-level payment terms (Horus keeps terms only on the company), and the account type. '
    'Chift must decide whether such inputs are rejected or dropped, and its clients need to know.',
    '<b>Accountant review is built into Horus.</b> Entries pushed through the API are unconfirmed by default, and invoices cannot be deleted through the API. '
    'Whether Chift\u2019s "posted" should bypass that review is a Chift decision. Proposal: review by default.',
    '<b>Two read-side points rest on undocumented behaviour:</b> telling invoices from credit notes when reading entries, and computing supplier open amounts when invoices are partly paid. '
    'Both need confirmation from Horus.',
]
RECOMMENDATION = ('Proceed to a short validation phase rather than a full build. First get a test licence and answers to the "before build" questions in section 6. '
                  'Then build the reference routes and the simple creates, followed by invoice creation and miscellaneous operations. Leave the ledger-based reads '
                  '(invoice retrieval, outstanding items) until Horus has confirmed credit notes, currency, partial matching and volumes. '
                  'This is a proposal for Chift\u2019s decision, not a commitment on behalf of Chift or Horus.')

# ---------- 2. Differences ----------
DIFF_INTRO = ('Chift exposes one standard accounting model; Horus has its own vocabulary and rules. The connector sits in between: it translates each Chift '
              'request into one or more Horus calls, converts fields, looks up Horus references, and assembles the response. Most of the effort and most of '
              'the risk come from the differences below, not from missing objects.')
DIAGRAM = '''<div class="diagram-flow" role="img" aria-label="One Chift request is translated by the connector into several Horus calls">
  <div class="box"><h4>Chift route</h4><p>One standard request, e.g. <code>POST /accounting/invoices/multi-analytic-plans</code></p></div>
  <div class="arrow" aria-hidden="true">→</div>
  <div class="box mid"><h4>Horus connector</h4><ul><li>translate fields and codes (VAT, signs, dates)</li><li>look up Horus references (journal, partner, accounts, analytics)</li><li>call Horus, combine the results</li></ul></div>
  <div class="arrow" aria-hidden="true">→</div>
  <div class="box"><h4>Horus API (one licence, one folder)</h4><ul><li>reference data, cached per folder</li><li>the create or list call itself</li><li>a read-back, because creates return only an id</li></ul></div>
</div>'''
VOCAB = [  # (Chift term, Horus term)
    ('Folder', 'Folder: one entity’s books; most calls take a <code>FolderId</code>'),
    ('Client / supplier', 'Company flagged <code>IsCustomer</code> / <code>IsSupplier</code>; one record can be both'),
    ('Journal', 'Daybook; its type decides which endpoint can post into it'),
    ('Ledger account', 'Account, referenced by its search key (usually the account number)'),
    ('Analytic plan / analytic account', 'Cost schema / cost section (at most 8 schemas per folder)'),
    ('Sale or purchase entry', 'Book entry created by <code>invoices.sales.new</code> / <code>invoices.purchases.new</code> (Type 0 invoice, 1 credit note)'),
    ('Miscellaneous operation', 'Miscellaneous-operation book entry (debits equal credits)'),
    ('Outstanding item', 'Ledger line not matched yet, or open sales invoice'),
    ('VAT code', 'No VAT-code entity: a combination of rate, origin and type (Proposal: a connector-built list, C2)'),
    ('Posted / draft', 'Confirmed true / false (the pairing is a proposal, C1)'),
]
DIAGRAM += ('<details class="route inner"><summary><span class="r-title"><span class="caret" aria-hidden="true"></span>Same object, different name</span>'
            '<span class="r-line">Chift terms and their Horus equivalents.</span></summary><div class="r-body"><div class="table-wrap"><table>'
            '<thead><tr><th>Chift</th><th>Horus</th></tr></thead><tbody>'
            + ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in VOCAB)
            + '</tbody></table></div></div></details>')

# ---------- 3. Routes ----------
ROUTES_INTRO = ('This table answers Task A: for each Chift route, the main Horus endpoint(s) to use and how the route works. As the case anticipates, most routes '
                'also pull data from other Horus endpoints (reference data cached per folder, checks and read-backs, some used only in specific cases). '
                'The "+ N" figure counts those supporting endpoints, not calls per request; each route\u2019s details list them with the specificities to be aware of. '
                'Horus reads with filters (most <code>.list</code> endpoints) use POST, with the filters in the request body; simple reads by id '
                '(most <code>.info</code> endpoints) use GET. The feasibility column separates what the documentation confirms from what still depends on assumptions or answers.')
FZ_LEGEND = ('<b>Confirmed</b>: the documentation shows Horus can serve the route; remaining work is mapping. '
             '<b>Feasible with assumptions</b>: the route can be built, but part of the Chift contract rests on an interpretation the documentation does not confirm. '
             '<b>Needs confirmation</b>: a point that affects correctness needs an answer from Horus or a decision from Chift before the design is final. '
             '<b>Not yet concluded</b>: the documentation does not allow a conclusion. '
             '"Confirmed" does not mean complete: documented limitations still apply, for example analytic accounts carry no balance in Horus. '
             'A proposal on how to show a value Horus does not hold (such as those empty balances) does not lower a rating; an interpretation of '
             'undocumented Horus data does.')

# ---------- 4. Task B ----------
TASKB_ORDER = [
    ('client', 'Client creation', 'POST /consumers/{consumer_id}/accounting/clients'),
    ('invoice', 'Invoice creation (sale/purchase entry, multiple analytic plans)', 'POST /consumers/{consumer_id}/accounting/invoices/multi-analytic-plans'),
    ('outst', 'Outstanding items (clients and suppliers)', 'GET /consumers/{consumer_id}/accounting/outstandings'),
]
TASKB_INTRO = ('The case asks for these three routes at the level of each attribute and query parameter. Each table lists every Chift query parameter and '
               'attribute, the Horus field it maps to, the type of mapping, and what happens. For the two create routes the response rows are grouped: '
               'Horus returns only the new id, so the response combines a read-back of what Horus stores (the stored record for client creation; number, status and last update for invoice creation) with values echoed from the request, including values Horus cannot return '
               '(for example line quantity, unit price and exact analytic percentages); echoing is a proposal pending C4.')
MAPPING_LEGEND = ('<p class="small"><b>Mapping types.</b> <span class="mp mp-direct">Direct</span> same meaning, possibly renamed · '
                  '<span class="mp mp-transform">Transform</span> format, code, sign or unit changes · '
                  '<span class="mp mp-lookup">Lookup</span> a Horus reference must be found first · '
                  '<span class="mp mp-generated">Generated</span> the connector must create a value (always a proposal) · '
                  '<span class="mp mp-constant">Constant</span> fixed value · <span class="mp mp-na">Not available</span> Horus has no place for it · '
                  '<span class="mp mp-chift">Chift-side</span> handled by Chift’s platform or the connector, not by a Horus field. '
                  '<b>Basis.</b> Documented = stated in the documentation · Derived = deduced from it · Assumption = a proposal or interpretation to confirm · '
                  'To confirm = not documented.</p>')
TASKB_EXTRA = {
    'invoice': '''<details class="route inner"><summary><span class="r-title"><span class="caret" aria-hidden="true"></span>VAT: from a Chift tax code to a Horus combination</span>
<span class="r-line">Why tax_code is the most important transformation in this route.</span></summary><div class="r-body">
<p>Horus has no VAT-code list and accepts no VAT code on write. Each invoice line carries a <b>combination</b>: rate, origin and type for sales, plus kind and
condition for purchases. Only the combinations published by Horus are accepted. They come in two spreadsheets linked from the invoice endpoints, one
list per legislation (Belgium, Luxembourg) and direction <span class="lbl lbl-F">Documented</span>:</p>
<div class="table-wrap"><table><thead><tr><th>Spreadsheet</th><th>Belgium</th><th>Luxembourg</th><th>Fields of one combination</th></tr></thead><tbody>
<tr><td>Sales</td><td>18 combinations</td><td>58 combinations</td><td>TaxType, TaxRate, TaxOrigin (+ country for EU one-stop-shop sales)</td></tr>
<tr><td>Purchases</td><td>109 combinations</td><td>146 combinations</td><td>TaxType, TaxKind, TaxRate, TaxCondition, TaxConditionValue, TaxOrigin</td></tr>
</tbody></table></div>
<p>Example: a Belgian domestic sale at 21 % is rate 21, origin 0 ("Vente nationale"), type 0 (National). <span class="lbl lbl-F">Documented</span></p>
<p><b>Proposal:</b> the connector keeps a VAT-code catalogue built from these lists for each folder (selected by the folder's legislation). It translates
<code>tax_code</code> into a combination and rejects codes that are not on the list before calling Horus. Chift should agree on the code format, and Horus
should confirm the lists are current. The spreadsheets and the API reference disagree on some Luxembourg codes, which is asked in section 6.
<span class="lbl lbl-A">Assumption</span></p></div></details>''',
}

# ---------- 5. Limitations ----------
CLIENT_IMPACT_INTRO = ('What client applications and their users will notice with the Horus connector, in plain language, and what to do about it. '
                       'Rows marked as proposals depend on the decisions in section 6.')
CLIENT_IMPACT = [  # (area, what the client notices, what to do)
    ('Numbers', 'Invoice and operation numbers must be numeric: a number such as INV-2024/001 cannot be stored as the number, and Horus does not '
     'number invoices through the API.',
     'Send a numeric <code>invoice_number</code> and keep the printed number in <code>reference</code>. Proposal (C7): non-numeric numbers are '
     'rejected, and an invoice without a number is pushed for accountant review and returned as a draft.'),
    ('Accountant review', 'Pushed entries may wait for the accountant’s review in Horus and come back as drafts until confirmed.',
     'Choose the posting mode at activation: review (proposed default) or direct (proposal, C1).'),
    ('Corrections and ids', 'A pushed invoice cannot be deleted through the integration, and an edited invoice or operation comes back with a new id.',
     'Validate before pushing; match entries on journal and number, not on the id alone.'),
    ('Customers', 'One address per customer; no person names, mobile or notes; individuals come back as companies. Without a VAT number or '
     '<code>external_reference</code>, sending the same customer twice creates two customers under the proposed duplicate check (C6, C8).',
     'Send the main address, the full name, and a VAT number or <code>external_reference</code>.'),
    ('Invoice lines', 'Amounts, VAT and analytics are kept, but quantity, unit price and unit are not: a read returns quantity 1 (proposal, C4).',
     'Keep line detail in the client application.'),
    ('VAT codes', 'VAT codes come from a list the connector builds per folder (proposal, C2); some purchase VAT codes come back empty on read.',
     'Use the connector’s VAT-code list; use the rate and amount when the code is empty.'),
    ('Foreign currency', 'Miscellaneous operations in another currency are stored in euro. On read, paid sales invoices and purchase invoices in '
     'another currency come back in euro (proposal until Horus answers H4).',
     'Keep original-currency amounts in the client application (C15, C16, H4).'),
    ('Incremental sync', '<code>updated_after</code> returns new and changed invoices, but not deleted or replaced ones; whether payments and accountant edits count as changes is still open (H10).',
     'Schedule a periodic full re-sync.'),
    ('Unsupported inputs', 'Withholding tax, the Dutch G/N split, and a forced period or delivery date in another month have no place in Horus.',
     'Do not send them. Proposal (C3): requests with withholding tax, a G/N split or a forced period in another month are rejected; for a delivery date in another month, rejecting or accepting is a Chift decision (C3, H10).'),
]
LIMITS_INTRO = ('This section starts with what Chift\u2019s clients will notice, then lists the limitations behind it. "Proposed handling" is a '
                'recommendation for discussion, not an agreed rule.')
LIMITS_LIST_INTRO = 'The limitations and design considerations that materially affect the proposed solution, most important first.'

# ---------- 6. Questions and next steps ----------
QUESTIONS_INTRO = ('The questions whose answers change feasibility, the design of a Task B mapping, or what Chift can promise its clients. '
                   '"Before build" questions should be answered before development starts.')
QUESTIONS_NOTE = ('Question ids match the detailed reference, where the same topics are covered (wording refined since). "new" marks questions added after the '
                  'critical review. The route cards of the detailed reference hold further detail-level questions. Remark for Chift (C13, no decision '
                  'needed): main_currency cites ISO 3166-1 (a country standard) instead of ISO 4217, and the line tax_amount formula omits the division by 100.')
NEXT_STEPS = [
    'Send the "before build" questions to Horus, and ask for a test licence and the integration registration details.',
    'Settle with Chift the decisions it owns: posting mode, invoice numbering, the VAT-code convention, and how unsupported inputs are handled.',
    'Prototype on a test folder: reference reads, then client and ledger-account creation; measure response times on the largest test folder.',
    'Add invoice creation and miscellaneous operations, testing the VAT translation, numbering, duplicates and timeouts.',
    'Add invoice retrieval and outstanding items once Horus has answered on credit notes, currency, partial matching and limits.',
    'Use the Task B tables as acceptance criteria, and update the detailed reference with every confirmed answer.',
]

# ---------- Appendices ----------
SOURCES_HTML = f'''<h4>Sources</h4>
<div class="table-wrap"><table><thead><tr><th>Source</th><th>What was used</th><th>Note</th></tr></thead><tbody>
<tr><td>The case</td><td>"Case Product / Tech", Part 1 (Mapping Chift – Horus)</td><td>Defines the scope: Task A (10 routes) and Task B (3 routes, attribute level).</td></tr>
<tr><td>Chift API contract</td><td>OpenAPI specification bundled in Chift's Python SDK (package <code>chift</code>, version 0.6.16)</td><td>docs.chift.eu could not be reached from the analysis environment. All 11 routes of the case are present in this specification. To be spot-checked against the live reference.</td></tr>
<tr><td>Horus API reference</td><td>72 endpoint pages from docs.horus-software.be (reference dated 24 September 2026)</td><td>The case links the former documentation (horussoftwareapi.docs.apiary.io). The current documentation was used; the two versions were not compared (question in section 6).</td></tr>
<tr><td>Horus guides</td><td>15 guide pages (authentication, requests, responses, data model, invoices, operations, outstanding items, documents, versioning, testing)</td><td>Printed 13 October 2026.</td></tr>
<tr><td>Horus tax combinations</td><td>The two spreadsheets of accepted VAT combinations linked from the invoice endpoints</td><td>Downloaded 13 October 2026.</td></tr>
<tr><td>Not available</td><td>Horus Quickstart, integration registration, FAQ and changelog pages; Postman collection; webhook documentation</td><td>Gaps are flagged where they matter.</td></tr>
</tbody></table></div>
<h4>Method</h4>
<p>Both contracts were read in full for the routes in scope. For each route the same questions were asked: what is the business object, what does Chift require
and return, can Horus read or write it, which calls in which order, how each field maps, and what is lost or uncertain. Each mapping was then checked
independently against the documentation, and the result was challenged in a critical review. That review led to the corrections in appendix B. No
request was sent to a Horus licence or a Chift environment.</p>
<h4>How to read the labels</h4>
<p><span class="lbl lbl-F">Documented</span> stated in a source · <span class="lbl lbl-D">Derived</span> deduced from the sources (for example from the absence of a field) ·
<span class="lbl lbl-A">Assumption</span> a proposal or interpretation that must be confirmed · <span class="lbl lbl-Q">To confirm</span> not documented.
A label rates the mapping or statement itself: a row whose mapping is a proposal or an interpretation is labelled Assumption, even when it uses
documented Horus fields. Smaller proposals inside a row (validation, defaults, how to reject) are marked "Proposal" in the text. In sections 2 and 5
the label describes the Horus behaviour; proposals there are also marked "Proposal".</p>
<p>The <a href="{REFERENCE_FILE}">detailed technical reference</a> keeps the full analysis: endpoint inventory (72 endpoints), complete call sequences, every
edge case and error scenario, cross-route working assumptions, the dependencies on Chift routes outside the case list (VAT codes, supplier creation,
client and supplier lists, payment terms and methods, attachments, bookyears), the shared connector building blocks, and all detail-level questions.</p>'''
CORR_LINE = 'What changed since the detailed reference was written, and why.'
CORR_INTRO = (f'The <a href="{REFERENCE_FILE}">detailed technical reference</a> is kept unchanged as the record of the original analysis. A later critical review '
              'corrected or qualified some of its conclusions. This report follows the corrected position. The table lists the material differences; '
              'the route details and Task B tables follow the corrected position throughout, also where no row is listed.')
