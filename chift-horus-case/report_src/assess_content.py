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
ANSWER = ''  # set after the route assessments are final (see bottom of file)
TILE_NOTE = ('Each route is rated by the weakest point that materially affects it. "Confirmed" means the documentation shows Horus can do what the route needs; '
             'the remaining work is mapping. The other levels are explained in section 3.')
KEY_MESSAGES = []
RECOMMENDATION = ''

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

# ---------- 3. Routes ----------
ROUTES_INTRO = ('This table answers Task A: for each Chift route, the Horus endpoint(s) to use and how the route works. Main endpoints are in bold; '
                'supporting calls follow. The feasibility column separates what the documentation confirms from what still depends on assumptions or answers. '
                'The considerations for each route are listed below the table.')
FZ_LEGEND = ('<b>Confirmed</b>: the documentation shows Horus can serve the route; remaining work is mapping. '
             '<b>Feasible with assumptions</b>: the route can be built, but part of the Chift contract rests on an interpretation the documentation does not confirm. '
             '<b>Needs confirmation</b>: a point that affects correctness needs an answer from Horus or a decision from Chift before the design is final. '
             '<b>Not yet concluded</b>: the documentation does not allow a conclusion.')

# ---------- 4. Task B ----------
TASKB_ORDER = [
    ('client', 'Client creation', 'POST /consumers/{consumer_id}/accounting/clients'),
    ('invoice', 'Invoice creation (sale/purchase entry, multiple analytic plans)', 'POST /consumers/{consumer_id}/accounting/invoices/multi-analytic-plans'),
    ('outst', 'Outstanding items (clients and suppliers)', 'GET /consumers/{consumer_id}/accounting/outstandings'),
]
TASKB_INTRO = ('The case asks for these three routes at the level of each attribute and query parameter. Each table lists every Chift query parameter and '
               'attribute, the Horus field it maps to, the type of mapping, and what happens. For the two create routes, the response is summarised: '
               'it is read back from Horus and mirrors the request mapping.')
MAPPING_LEGEND = ('<p class="small"><b>Mapping types.</b> <span class="mp mp-direct">Direct</span> same meaning, possibly renamed · '
                  '<span class="mp mp-transform">Transform</span> format, code, sign or unit changes · '
                  '<span class="mp mp-lookup">Lookup</span> a Horus reference must be found first · '
                  '<span class="mp mp-generated">Generated</span> the connector must create a value (always a proposal) · '
                  '<span class="mp mp-constant">Constant</span> fixed value · <span class="mp mp-na">Not available</span> Horus has no place for it · '
                  '<span class="mp mp-chift">Chift-side</span> handled by Chift. '
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
LIMITS_INTRO = ('The limitations and design considerations that materially affect the proposed solution, most important first. "Proposed handling" is a '
                'recommendation for discussion, not an agreed rule.')

# ---------- 6. Questions and next steps ----------
QUESTIONS_INTRO = ('The questions whose answers change feasibility, the design of a Task B mapping, or what Chift can promise its clients. '
                   '"Before build" questions should be answered before development starts.')
QUESTIONS_NOTE = ('Ref. points to the question number in the detailed reference where one exists; "New" marks questions added after the review. '
                  'The detailed reference and its route cards hold further detail-level questions.')
NEXT_STEPS = []

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
A row takes the label of its weakest part.</p>
<p>The <a href="{REFERENCE_FILE}">detailed technical reference</a> keeps the full analysis: endpoint inventory (72 endpoints), complete call sequences, every
edge case and error scenario, cross-route working assumptions, and all detail-level questions.</p>'''
CORR_LINE = 'What changed since the detailed reference was written, and why.'
CORR_INTRO = (f'The <a href="{REFERENCE_FILE}">detailed technical reference</a> is kept unchanged as the record of the original analysis. A later critical review '
              'corrected or qualified some of its conclusions. This report follows the corrected position; the table lists every material difference.')
