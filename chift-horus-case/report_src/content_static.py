"""Static narrative blocks of the external report (no dependency on mapping data)."""

TITLE = 'Horus Connector Mapping'
DESCRIPTION = ("Route-by-route mapping of Chift's unified accounting API onto the Horus Software API: "
               "feasibility verdicts, call patterns, attribute-level mappings and open questions.")
RAIL_LABEL = 'Chift × Horus · Part 1'


def header_html():
    return '''<header class="doc-head">
  <p class="eyebrow">Integration analysis · Case part 1</p>
  <h1>Chift × Horus: accounting connector mapping</h1>
  <p class="lede">For each Chift accounting route in scope: which Horus Software API endpoints implement it, what the connector has to transform, combine or emulate, and what still needs confirmation from Horus or Chift.</p>
  <div class="meta">
    <span>Prepared by <b>Silas Deblanc</b></span>
    <span>For <b>Chift, Product &amp; Tech</b></span>
    <span>Date <b>13 October 2026</b></span>
    <span>Status <b>Analysis for discussion</b></span>
  </div>
</header>'''


def footer_html():
    return ('Prepared by Silas Deblanc as part of the Chift product/tech case. Based only on the case description, '
            'the Chift API specification and the Horus Software API documentation listed in section 2. '
            'Proposals in this report are analysis, not commitments on behalf of Chift or Horus.')


SCOPE_HTML = '''
<h3 id="scope-what">What was analysed</h3>
<div class="two-col">
<div>
<h4>Task A: route-level mapping</h4>
<p>For each of the ten Chift endpoints listed in the case: the Horus endpoint(s) to use and the considerations specific to Horus.</p>
<ul class="tight">
<li>Client creation</li><li>Invoice retrieval (multiple analytic plans)</li><li>Invoice creation (multiple analytic plans)</li>
<li>Journal retrieval</li><li>Ledger account creation</li><li>Chart of accounts retrieval</li><li>Accounting folders retrieval</li>
<li>Miscellaneous operation creation</li><li>Analytic plans retrieval</li><li>Analytic accounts retrieval (multiple plans)</li>
</ul>
</div>
<div>
<h4>Task B: attribute-level mapping</h4>
<p>Every request attribute, response attribute and query parameter of three routes:</p>
<ul class="tight">
<li>Client creation</li>
<li>Invoice creation (multiple analytic plans)</li>
<li>Outstanding items (customer and supplier balances). This route appears only in Task B, so it is also given a route-level summary in section 4.</li>
</ul>
</div>
</div>

<h3 id="scope-sources">Sources</h3>
<div class="table-wrap"><table>
<thead><tr><th>Source</th><th>Version used</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>Case description</td><td>Notion page “Case Product / Tech”</td><td>Defines scope and deliverables.</td></tr>
<tr><td>Chift API reference</td><td>OpenAPI specification shipped with the official Chift Python SDK (<code>chift</code> 0.6.16)</td><td>The live documentation site could not be reached from the analysis environment. All eleven endpoint links in the case match operations in this specification one to one. To re-check against docs.chift.eu before build.</td></tr>
<tr><td>Horus API reference</td><td>72 endpoint pages, each with its OpenAPI definition (documentation dated 24 September 2026)</td><td>Includes <code>book-entries.info</code>, supplied separately.</td></tr>
<tr><td>Horus guides</td><td>15 pages: authentication, token lifecycle, requests, responses and errors, sideloading, data model, reading data, customers and suppliers, invoices, operations, documents, outstanding items and matching, testing, versioning</td><td>Used with the same weight as the API reference.</td></tr>
<tr><td>Not available</td><td>Quickstart, integration registration, support/FAQ and changelog pages; the accepted tax-combination spreadsheets; the Postman collection; webhook documentation</td><td>Points that depend on them are marked “To confirm”.</td></tr>
</tbody></table></div>

<h3 id="scope-method">Method</h3>
<p>Every route was analysed with the same seven questions, so the results can be compared and the approach reused for other connectors:</p>
<ol class="tight">
<li><b>Business meaning:</b> which object or action does the Chift route represent?</li>
<li><b>Chift contract:</b> what is required on input and promised on output?</li>
<li><b>Horus capability:</b> does Horus hold this object, and can it be read or written through the API?</li>
<li><b>Endpoints:</b> which Horus calls, in which order, and how many per Chift request?</li>
<li><b>Attributes:</b> direct, transformed, looked up, composite, constant or unavailable?</li>
<li><b>Behaviour:</b> filters, pagination, numbering, status and incremental sync: native or emulated?</li>
<li><b>Risk:</b> limitations, edge cases and error handling.</li>
</ol>
<p>Each mapping was drafted, then challenged by two independent reviews: one tried to refute every cited endpoint, field and value against the documentation, the other looked for missing attributes, endpoints and edge cases. Accepted findings were reconciled, and a final review checked consistency across routes. The cross-route design decisions that came out of that review are listed in appendix B.</p>

<h3 id="scope-legend">How to read this report</h3>
<div class="two-col">
<div>
<h4>Verdicts</h4>
<ul class="tight">
<li><span class="chip v-supported">Supported</span> One native Horus endpoint, plus cached reference data, serves the route with deterministic transformations. Losses are limited to minor optional fields.</li>
<li><span class="chip v-workaround">Supported with workaround</span> Feasible, but needs extra calls per request (read-backs, joins, loops), emulated filters, pagination or numbering, or loses a capability clients typically rely on.</li>
<li><span class="chip v-not_supported">Not supported</span> No Horus capability for the route.</li>
<li><span class="chip v-unknown">To confirm</span> The documentation is insufficient to decide.</li>
</ul>
</div>
<div>
<h4>Basis of each statement</h4>
<ul class="tight">
<li><span class="lbl lbl-F">Documented</span> Stated in the Chift or Horus documentation.</li>
<li><span class="lbl lbl-D">Derived</span> Concluded from documented facts.</li>
<li><span class="lbl lbl-A">Assumption</span> Plausible but not documented; to validate.</li>
<li><span class="lbl lbl-Q">To confirm</span> Missing or ambiguous in the documentation.</li>
</ul>
<p class="sub">In the detailed texts, these labels are abbreviated as (F), (D), (A) and (?), and references such as (D7) point to the cross-route design decisions in appendix B.</p>
<h4>Mapping types (attribute tables)</h4>
<p class="legend"><span><span class="cls cls-DIRECT">Direct</span> same meaning and format</span> <span><span class="cls cls-TRANSFORM">Transform</span> format, code or sign conversion</span> <span><span class="cls cls-LOOKUP">Lookup</span> resolved through another call</span> <span><span class="cls cls-COMPOSITE">Composite</span> built from several fields or calls</span> <span><span class="cls cls-CONSTANT">Constant</span> set by the connector</span> <span><span class="cls cls-NA">Not available</span> no Horus equivalent</span> <span><span class="cls cls-CHIFT_INTERNAL">Chift-side</span> handled inside Chift</span></p>
</div>
</div>
'''

ARCH_SVG = '''<div class="diagram" role="img" aria-label="Integration architecture: a software vendor calls the Chift unified API; the Horus connector authenticates through my-horus.com once per license and then calls the license-specific Horus API URL, scoped to one folder per request.">
<svg viewBox="0 0 880 250" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="arrowhead" d="M0,0 L10,5 L0,10 z"/></marker></defs>
  <rect class="box" x="10" y="80" width="150" height="70" rx="6"/>
  <text x="85" y="108" text-anchor="middle" font-size="14" font-weight="600">Software vendor</text>
  <text class="muted" x="85" y="128" text-anchor="middle" font-size="12">Chift's client</text>
  <rect class="box-accent" x="210" y="80" width="170" height="70" rx="6"/>
  <text x="295" y="108" text-anchor="middle" font-size="14" font-weight="600">Chift unified API</text>
  <text class="muted" x="295" y="128" text-anchor="middle" font-size="12">consumer · folder_id</text>
  <rect class="box-accent" x="430" y="80" width="170" height="70" rx="6"/>
  <text x="515" y="108" text-anchor="middle" font-size="14" font-weight="600">Horus connector</text>
  <text class="muted" x="515" y="128" text-anchor="middle" font-size="12">map · look up · emulate</text>
  <rect class="box" x="660" y="40" width="210" height="150" rx="6"/>
  <text x="765" y="66" text-anchor="middle" font-size="14" font-weight="600">Horus license</text>
  <text class="muted" x="765" y="86" text-anchor="middle" font-size="12">own database, own api_url</text>
  <rect class="box-accent" x="680" y="100" width="170" height="34" rx="5"/>
  <text x="765" y="122" text-anchor="middle" font-size="12">Folder (one per company)</text>
  <rect class="box" x="680" y="142" width="170" height="34" rx="5"/>
  <text class="muted" x="765" y="164" text-anchor="middle" font-size="12">Folder · Folder · …</text>
  <rect class="box" x="430" y="196" width="170" height="44" rx="6"/>
  <text x="515" y="215" text-anchor="middle" font-size="12" font-weight="600">my-horus.com</text>
  <text class="muted" x="515" y="232" text-anchor="middle" font-size="11">OAuth 2, once per license</text>
  <path class="edge" d="M160 115 H206" marker-end="url(#ah)" stroke-width="1.5"/>
  <path class="edge" d="M380 115 H426" marker-end="url(#ah)" stroke-width="1.5"/>
  <path class="edge" d="M600 115 H656" marker-end="url(#ah)" stroke-width="1.5"/>
  <text class="muted" x="628" y="106" text-anchor="middle" font-size="11">1..n calls</text>
  <path class="edge" d="M515 150 V192" marker-end="url(#ah)" stroke-width="1.2" stroke-dasharray="4 3"/>
  <text class="muted" x="526" y="176" font-size="11">api_url + tokens</text>
  <text class="muted" x="183" y="106" text-anchor="middle" font-size="11">1 call</text>
</svg></div>'''

CONCEPTS = [
    ('Consumer connection', 'License + OAuth connection', 'Each license (an accounting firm or an SMB) has its own database and its own API URL, returned at the end of the OAuth flow.', 'F'),
    ('Folder (legal entity)', 'Folder', 'The accounting record of one company. Almost every endpoint requires a FolderId.', 'F'),
    ('Client / supplier', 'Company, flagged IsCustomer / IsSupplier', 'In Horus, “company” means a third party. One record can be both customer and supplier.', 'F'),
    ('Journal', 'Daybook', 'The daybook type decides which posting endpoint is used (sales, purchases, bank, financial, miscellaneous).', 'F'),
    ('Ledger account', 'Account, identified by its search key', 'Postings reference accounts by search key (usually the account number), not by id.', 'F'),
    ('Analytic plan / analytic account', 'Cost schema / cost section', 'Requires the folder’s analytics module. Up to 8 cost schemas per folder.', 'F'),
    ('Analytic distribution', 'Cost lines (amounts) or a cost distribution key', 'Horus allocates amounts to combinations of cost sections; Chift sends percentages per plan.', 'F'),
    ('Sale/purchase entry', 'Book entry created from a sales or purchase invoice', 'Type 0 = invoice, 1 = credit note. Creation returns only the book entry id.', 'F'),
    ('Entry lines', 'Account history lines', 'One line per account movement, with debit/credit, VAT detail, matching number and cost detail.', 'F'),
    ('VAT code', 'No VAT-code entity: rate + origin + type (+ kind and condition for purchases)', 'Only some combinations are valid; Horus lists them in reference spreadsheets.', 'F'),
    ('Miscellaneous operation', 'Miscellaneous operation (OD) book entry', 'Debit and credit lines that must balance.', 'F'),
    ('Bookyear', 'Fiscal year', 'Carries closure dates per daybook type; Horus recommends checking them before posting.', 'F'),
    ('Posted / draft', 'Confirmed true / false', 'API entries are unconfirmed by default so the accountant can review them before confirming.', 'F'),
    ('Outstanding item', 'Unmatched account history line, or open sales invoice', 'Lines not yet matched make up the outstanding items.', 'F'),
    ('Attachment', 'Document (main document and annexes)', 'Sent as multipart/form-data with the entry, or attached afterwards.', 'F'),
]

CONVENTIONS = [
    ('Authentication', 'OAuth 2 authorisation code flow through my-horus.com. The user picks the license; the code is exchanged with <code>grant_type=auth_code</code> (not the usual <code>authorization_code</code>). Access tokens last one hour; refresh tokens are single-use, so refreshes must be serialised per connection.', 'F'),
    ('Base URL', 'One API URL per license, received during authorisation. It must be stored with the connection and never hard-coded.', 'F'),
    ('Request style', 'JSON-RPC style methods (<code>{api_url}/{category}.{action}</code>). Simple reads use GET with a query string; lists with filters, creations and updates use POST with a JSON body.', 'F'),
    ('Response envelope', 'Payload under <code>Data</code>. Related entities are references <code>{Type, Id}</code>. Creations and updates return only <code>{Id}</code>.', 'F'),
    ('Sideloading', 'An <code>Include</code> parameter returns related entities under <code>Included</code>, on four endpoints only: book-entries.list, account-histories.list, companies.list and invoices.sales.outstanding.list.', 'F'),
    ('Pagination', 'No list endpoint has paging parameters and the guides describe none. Lists return the full result, so the connector must emulate Chift’s page, size and total.', 'D'),
    ('Filters', 'String filters use “contains”; all filters must match. Many lists offer <code>ModifiedAfter</code>/<code>ModifiedBefore</code> for incremental synchronisation. Ledger periods are expressed in months.', 'F'),
    ('Updates', 'Master data uses partial updates (null keeps a value, an empty string erases it). Invoice and operation updates (<code>.update</code>) are full replacements that create a new book entry id and drop the original attachment. Exception: <code>book-entries.miscellaneous-operations.lines.update</code> changes some lines in place (no amount changes).', 'F'),
    ('Errors', 'Errors other than authorisation errors (401) return <code>{ErrorType, Details, Message}</code>. Status codes: 400, 401, 403, 404, 500. Horus advises: refresh once on 401, do not retry 400, back off on 500. The list of ErrorType values is not documented.', 'F'),
    ('Versioning', 'New endpoints, optional parameters and response properties can appear without notice; breaking changes are announced by email. The connector must ignore unknown properties.', 'F'),
    ('Testing', 'Requests run against the license’s real database. Write tests need a test license or test folder; no sandbox is documented.', 'F'),
]
