import re
"""Report sections. Data-driven parts read the harmonised mapping JSON; curated text lives in curated.py."""
from render import esc, inline, rich, chip, lbl, cls, field_table, endpoint_list, flow, bullet_list, VERDICT_TEXT, route_card
from content_static import TITLE, DESCRIPTION, RAIL_LABEL, header_html, footer_html, SCOPE_HTML, ARCH_SVG, CONCEPTS, CONVENTIONS
import curated as K

GROUP_ORDER = ['create_client', 'get_invoices', 'create_invoice', 'journals_folders', 'ledger_accounts',
               'misc_operation', 'analytics', 'outstandings']


def _verdict_of(groups, key, name_contains):
    g = groups[key]
    for r in g['chift_routes']:
        if name_contains.lower() in r['chift_name'].lower():
            return r['verdict'], r['one_line']
    return g['verdict'], g['summary']


def overview_rows(groups):
    rows = []
    for row in K.OVERVIEW:
        v, one = _verdict_of(groups, row['group'], row['match'])
        rows.append(dict(row, verdict=v, one_line=one))
    return rows


def summary_section(groups, cross):
    rows = overview_rows(groups)
    counts = {k: sum(1 for r in rows if r['verdict'] == k) for k in VERDICT_TEXT}
    inventory = {r['path'] for r in cross['inventory']}
    used = set()
    for g in groups.values():
        for e in g['horus_endpoints']:
            card = (e.get('cardinality') or '').lower()
            if e['path'] in inventory and not re.match(r'^(not used|not called|0 for this route|0 \(used by|never)', card):
                used.add(e['path'])
    tiles = ''.join(
        f'<div class="tile"><div class="n">{counts[k]}</div><div class="t">{chip(k)}</div></div>'
        for k in ['supported', 'workaround', 'not_supported', 'unknown'])
    tiles += f'<div class="tile"><div class="n">{len(rows)}</div><div class="t">Chift routes analysed</div></div>'
    tiles += f'<div class="tile"><div class="n">{len([p for p in used if p.startswith("/")])}</div><div class="t">of 72 Horus endpoints called, including optional ones</div></div>'
    html = [f'<p class="lede">{K.SUMMARY_LEDE}</p>', f'<div class="overview">{tiles}</div>']
    html.append('<h3>Key findings</h3><ul class="tight">' + ''.join(f'<li>{x}</li>' for x in K.KEY_FINDINGS) + '</ul>')
    html.append(f'<div class="note key"><span class="note-title">Recommendation</span>{K.RECOMMENDATION}</div>')
    return ''.join(html)


def horus_section(groups, cross):
    h = ['<p>' + K.HORUS_INTRO + '</p>', ARCH_SVG]
    h.append('<h3 id="horus-concepts">Concept map: Chift ↔ Horus</h3><p>The same word can mean different things in the two systems. This alignment is the basis of every mapping below.</p>')
    h.append('<div class="table-wrap"><table><thead><tr><th>Chift concept</th><th>Horus concept</th><th>What matters for the connector</th><th>Basis</th></tr></thead><tbody>')
    for a, b, c, l in CONCEPTS:
        h.append(f'<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c)}</td><td>{lbl(l)}</td></tr>')
    h.append('</tbody></table></div>')
    h.append('<h3 id="horus-conventions">Horus conventions that shape every route</h3>')
    h.append('<div class="table-wrap"><table><thead><tr><th>Topic</th><th>Convention</th><th>Basis</th></tr></thead><tbody>')
    for t, c, l in CONVENTIONS:
        h.append(f'<tr><td><b>{esc(t)}</b></td><td>{c}</td><td>{lbl(l)}</td></tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)


def routes_section(groups, cross):
    rows = overview_rows(groups)
    h = [f'<p>{K.ROUTES_INTRO}</p>']
    h.append('<div class="table-wrap"><table class="overview-table"><thead><tr><th>Chift route</th><th>Horus endpoint(s)</th><th>Call pattern</th><th>Verdict</th></tr></thead><tbody>')
    for r in rows:
        eps = '<br>'.join(esc(e) for e in r['endpoints'])
        h.append(f'<tr><td><a href="#card-{r["group"]}"><b>{esc(r["route"])}</b></a><span class="sub mono">{esc(r["chift"])}</span></td>'
                 f'<td class="eps">{eps}</td><td>{esc(r["pattern"])}</td><td>{chip(r["verdict"])}</td></tr>')
    h.append('</tbody></table></div>')
    h.append('<div class="filters"><button class="btn" data-expand="route-cards">Expand all</button><span class="count">Open a route for its endpoints, call sequence, considerations and key attribute mapping.</span></div>')
    h.append('<div id="route-cards">')
    for key in GROUP_ORDER:
        g = groups[key]
        meta = K.CARD_META[key]
        rc = {
            'id': f'card-{key}', 'title': meta['title'], 'paths': meta['paths'],
            'verdicts': [r['verdict'] for r in g['chift_routes'] if 'context' not in r['chift_name'].lower()],
            'one_line': meta['one_line'],
            'summary': g['summary'],
            'brief': meta.get('brief', ''),
            'endpoints': g['horus_endpoints'],
            'sequence': g['call_sequence'],
            'considerations': [{'text': l['description'] + (' Impact: ' + l['impact'] if l.get('impact') else ''), 'label': l['label']} for l in g['limitations']],
            'fields': [] if key in K.TASK_B else g['field_mappings'],
            'questions': g['open_questions'],
        }
        if key in K.TASK_B:
            rc['considerations'].append({'text': f'Full attribute-level mapping in section 5 ({meta["title"]}).', 'label': 'D'})
        h.append(route_card(rc))
    h.append('</div>')
    return ''.join(h)


def task_b_section(groups, cross):
    h = [f'<p>{K.TASK_B_INTRO}</p>']
    for key in K.TASK_B:
        g = groups[key]
        meta = K.CARD_META[key]
        h.append(f'<h3 id="tb-{key}">{esc(meta["title"])} {chip(g["verdict"])}</h3>')
        h.append(f'<p class="kicker mono">{esc(meta["paths"])}</p>')
        h.append(f'<p>{K.TASK_B_SUMMARY[key]}</p>')
        if K.TASK_B_EXTRA.get(key):
            h.append(K.TASK_B_EXTRA[key])
        req = g.get('horus_required_without_chift_source') or []
        if req:
            h.append('<h4>Horus fields with no Chift source, and how the connector fills them</h4>')
            h.append('<div class="table-wrap"><table><thead><tr><th>Horus field</th><th>Fill rule</th><th>Basis</th></tr></thead><tbody>')
            for r in req:
                h.append(f'<tr><td>{inline(r["horus_field"])}</td><td>{inline(r["how_to_fill"])}</td><td>{lbl(r["label"])}</td></tr>')
            h.append('</tbody></table></div>')
        h.append(f'<h4>Attribute mapping ({len(g["field_mappings"])} rows)</h4>')
        h.append(field_table(f'fm-{key}', g['field_mappings']))
        h.append('<h4>Call sequence</h4>' + flow(g['call_sequence']))
    return ''.join(h)


def dependencies_section(groups, cross):
    h = [f'<p>{K.DEPS_INTRO}</p>']
    h.append('<div class="table-wrap"><table><thead><tr><th>Dependency</th><th>Why the requested routes need it</th><th>Horus support</th><th>Basis</th></tr></thead><tbody>')
    for d in K.DEPENDENCIES:
        h.append(f'<tr><td><b>{esc(d["name"])}</b></td><td>{d["why"]}</td><td>{d["support"]}</td><td>{lbl(d["label"])}</td></tr>')
    h.append('</tbody></table></div>')
    h.append('<h3 id="deps-blocks">Connector building blocks</h3><p>These shared components serve several routes and drive most of the effort.</p>')
    h.append('<div class="table-wrap"><table><thead><tr><th>Building block</th><th>What it does</th><th>Routes served</th></tr></thead><tbody>')
    for b in K.BUILDING_BLOCKS:
        h.append(f'<tr><td><b>{esc(b["name"])}</b></td><td>{b["what"]}</td><td>{esc(b["routes"])}</td></tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)


def risks_section(groups, cross):
    h = [f'<p>{K.RISKS_INTRO}</p>']
    h.append('<div class="table-wrap"><table><thead><tr><th>Situation</th><th>Proposed handling</th><th>Routes</th><th>Basis</th></tr></thead><tbody>')
    for e in K.EDGE_CASES:
        h.append(f'<tr><td>{e["case"]}</td><td>{e["handling"]}</td><td>{esc(e["routes"])}</td><td>{lbl(e["label"])}</td></tr>')
    h.append('</tbody></table></div>')
    h.append('<h3 id="risks-errors">Error translation</h3>')
    h.append('<div class="table-wrap"><table><thead><tr><th>Horus response</th><th>Connector behaviour</th><th>Chift response</th></tr></thead><tbody>')
    for e in K.ERROR_MAP:
        h.append(f'<tr><td>{e[0]}</td><td>{e[1]}</td><td>{e[2]}</td></tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)


def questions_section(groups, cross):
    h = [f'<p>{K.QUESTIONS_INTRO}</p>']
    for who, items in (('Horus', K.QUESTIONS_HORUS), ('Chift', K.QUESTIONS_CHIFT)):
        h.append(f'<h3 id="q-{who.lower()}">Questions for {who}</h3>')
        h.append('<div class="table-wrap"><table class="q-table"><thead><tr><th>#</th><th>Question</th><th>Why it matters</th><th>Routes</th></tr></thead><tbody>')
        for i, q in enumerate(items, 1):
            h.append(f'<tr><td class="num">{who[0]}{i}</td><td>{q["q"]}</td><td>{q["why"]}</td><td>{esc(q["routes"])}</td></tr>')
        h.append('</tbody></table></div>')
    return ''.join(h)


def next_section(groups, cross):
    h = [f'<p>{K.CONCLUSION}</p>', '<h3>Proposed next steps</h3><ol class="tight">']
    h += [f'<li>{s}</li>' for s in K.NEXT_STEPS]
    h.append('</ol>')
    return ''.join(h)


def appendix_section(groups, cross):
    inv = sorted(cross['inventory'], key=lambda r: r['path'])
    h = ['<details class="route" id="appendix-inventory"><summary><span class="r-title"><span class="caret">▸</span>A. Horus endpoint inventory (72 endpoints)</span>'
         '<span class="r-line">Every endpoint in the Horus API reference, what it does, and which Chift route in scope uses it.</span></summary><div class="r-body">']
    h.append('<div class="table-wrap"><table><thead><tr><th>Endpoint</th><th>Purpose</th><th>Writes</th><th>Used for (Chift routes in scope)</th></tr></thead><tbody>')
    for r in inv:
        h.append(f'<tr><td class="mono">{esc(r["method"])} {esc(r["path"])}</td><td>{inline(r["purpose"])}</td><td>{"Yes" if r["writes"] else "No"}</td><td>{inline(r["chift_relevance"])}</td></tr>')
    h.append('</tbody></table></div></div></details>')
    h.append('<details class="route" id="appendix-decisions"><summary><span class="r-title"><span class="caret">▸</span>B. Cross-route working assumptions</span>'
             '<span class="r-line">Proposals applied consistently across all route mappings. They are not agreed rules: most depend on an open question in section 8 and will change if the answer differs.</span></summary><div class="r-body">')
    h.append('<div class="table-wrap"><table><thead><tr><th>#</th><th>Working assumption</th><th>Rationale</th><th>Depends on</th></tr></thead><tbody>')
    for d in K.DECISIONS:
        h.append(f'<tr><td class="num">{esc(d[0])}</td><td>{d[1]}</td><td>{d[2]}</td><td>{esc(K.DECISION_DEPENDS.get(d[0], ""))}</td></tr>')
    h.append('</tbody></table></div></div></details>')
    return ''.join(h)


def sections(groups, cross):
    tb_subs = [(f'tb-{k}', K.CARD_META[k]['title']) for k in K.TASK_B]
    return [
        ('summary', '1', 'Executive summary', summary_section(groups, cross), []),
        ('scope', '2', 'Scope, sources and method', SCOPE_HTML, [('scope-sources', 'Sources'), ('scope-method', 'Method'), ('scope-legend', 'How to read')]),
        ('horus', '3', 'How Horus works', horus_section(groups, cross), [('horus-concepts', 'Concept map'), ('horus-conventions', 'Conventions')]),
        ('routes', '4', 'Route mapping (Task A)', routes_section(groups, cross), []),
        ('attributes', '5', 'Attribute-level mapping (Task B)', task_b_section(groups, cross), tb_subs),
        ('dependencies', '6', 'Dependencies and building blocks', dependencies_section(groups, cross), []),
        ('risks', '7', 'Edge cases and error handling', risks_section(groups, cross), []),
        ('questions', '8', 'Open questions', questions_section(groups, cross), [('q-horus', 'For Horus'), ('q-chift', 'For Chift')]),
        ('next', '9', 'Conclusion and next steps', next_section(groups, cross), []),
        ('appendix', 'A–B', 'Appendices', appendix_section(groups, cross), []),
    ]
