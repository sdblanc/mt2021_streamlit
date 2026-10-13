"""Build the concise, interview-ready Horus connector assessment (single self-contained HTML file).

The detailed analysis stays in chift_horus_mapping_report.html (the preserved technical reference).
Inputs: assess_data.json (condensed route, field-mapping, limitation, question and correction content)
        and assess_content.py (hand-written narrative).
Usage: python3 -I gen_assess.py <out_html>
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import esc, inline, lbl
import assess_content as T

HERE = os.path.dirname(os.path.abspath(__file__))
FZ = {  # feasibility levels, weakest last
    'Confirmed': ('ok', 'Confirmed by the documentation'),
    'Feasible with assumptions': ('ass', 'Feasible, depends on assumptions'),
    'Needs confirmation': ('conf', 'Needs confirmation'),
    'Not yet concluded': ('open', 'Not yet concluded'),
}
MAP = {'Direct': 'direct', 'Transform': 'transform', 'Lookup': 'lookup', 'Generated': 'generated',
       'Constant': 'constant', 'Not available': 'na', 'Chift-side': 'chift'}


def fz(level, short=False):
    k, text = FZ.get(level, ('open', level))
    return f'<span class="fz fz-{k}">{esc(level if short else text)}</span>'


def mp(m):
    return f'<span class="mp mp-{MAP.get(m, "constant")}">{esc(m)}</span>'


def section(sid, num, title, body):
    return f'<section class="block" id="{sid}"><h2><span class="sec-num">{num}</span>{esc(title)}</h2>\n{body}\n</section>'


def nav(items):
    out = ['<ol>']
    for sid, label, subs in items:
        out.append(f'<li><a href="#{sid}">{esc(label)}</a>')
        if subs:
            out.append('<ol>' + ''.join(f'<li><a href="#{s}">{esc(l)}</a></li>' for s, l in subs) + '</ol>')
        out.append('</li>')
    out.append('</ol>')
    return ''.join(out)


def ul(items, fmt=lambda x: inline(x)):
    return '<ul class="tight">' + ''.join(f'<li>{fmt(x)}</li>' for x in items) + '</ul>' if items else ''


def with_basis(it):
    return f'{inline(it["text"])} {lbl(it["basis"])}'


# ---------- sections ----------

def summary(D):
    routes = D['routes']
    counts = {k: sum(1 for r in routes if r['feasibility'] == k) for k in FZ}
    h = [f'<p class="lede">{T.answer(routes)}</p>']
    tiles = ''.join(f'<div class="tile"><div class="n">{counts[k]}</div><div class="t">{fz(k)}</div></div>' for k in FZ)
    tiles += f'<div class="tile"><div class="n">{len(routes)}</div><div class="t">Chift routes analysed (10 in Task A, outstanding items in Task B)</div></div>'
    h.append(f'<div class="overview">{tiles}</div>')
    h.append(f'<p class="small">{T.TILE_NOTE}</p>')
    E = D['lq']['feasibility_evidence']
    boxes = [('confirmed', 'What the documentation confirms', 'ok'), ('assumption', 'What depends on an assumption', 'ass'),
             ('confirmation', 'What needs confirmation from Horus or Chift', 'conf'), ('not_concluded', 'What cannot be concluded yet', 'open')]
    h.append('<h3 id="sum-evidence">How sure are we?</h3><div class="quad">')
    for key, title, k in boxes:
        h.append(f'<div class="q q-{k}"><h4>{esc(title)}</h4>' + ul(E[key], with_basis) + '</div>')
    h.append('</div>')
    h.append('<h3 id="sum-messages">Key messages</h3>' + ul(T.KEY_MESSAGES, lambda x: x))
    h.append(f'<div class="note key"><span class="note-title">Recommendation</span>{T.RECOMMENDATION}</div>')
    return ''.join(h)


def differences(D):
    h = [f'<p>{T.DIFF_INTRO}</p>', T.DIAGRAM]
    h.append('<h3 id="diff-table">Differences that shape the mapping</h3>')
    h.append('<div class="table-wrap"><table><thead><tr><th>Chift</th><th>Horus</th><th>Why it matters for the mapping</th><th>Basis</th></tr></thead><tbody>')
    for d in D['lq']['differences']:
        h.append(f'<tr><td>{inline(d["chift"])}</td><td>{inline(d["horus"])}</td><td>{inline(d["why_it_matters"])}</td><td>{lbl(d["basis"])}</td></tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)


def routes(D):
    rs = D['routes']
    h = [f'<p>{T.ROUTES_INTRO}</p>']
    h.append('<div class="table-wrap"><table class="overview-table"><thead><tr><th>Chift route</th><th>Horus endpoint(s)</th><th>How it works</th><th>Feasibility</th></tr></thead><tbody>')
    for i, r in enumerate(rs):
        main = '<br>'.join(f'<b>{esc(e)}</b>' for e in r['horus_main'])
        sup = '<br>'.join(esc(e) for e in r['horus_support'])
        h.append(f'<tr><td><a href="#rt-{i}"><b>{esc(r["route"])}</b></a><span class="sub mono">{esc(r["chift"])}</span></td>'
                 f'<td class="eps">{main}{"<br>" + sup if sup else ""}</td><td>{inline(r["how_it_works"])}</td><td>{fz(r["feasibility"], True)}</td></tr>')
    h.append('</tbody></table></div>')
    h.append(f'<p class="small">{T.FZ_LEGEND}</p>')
    h.append('<h3 id="rt-details">Considerations per route</h3><div class="filters"><button class="btn" data-expand="route-cards">Expand all</button>'
             '<span class="count">Each route: what is confirmed, what rests on assumptions, what needs an answer, and the specificities to be aware of.</span></div><div id="route-cards">')
    for i, r in enumerate(rs):
        body = [f'<p>{inline(r["documented"])} {lbl("F")}</p>']
        if r['considerations']:
            body.append('<h4>Specificities to be aware of</h4>' + ul(r['considerations'], with_basis))
        if r['not_mappable']:
            body.append('<h4>What Horus cannot provide</h4>' + ul(r['not_mappable']))
        cols = [('depends_on_assumption', 'Depends on an assumption'), ('needs_confirmation', 'Needs confirmation'), ('not_concluded', 'Not yet concluded')]
        grid = ''.join(f'<div><h4>{t}</h4>{ul(r[k])}</div>' for k, t in cols if r[k])
        if grid:
            body.append(f'<div class="cols3">{grid}</div>')
        h.append(f'<details class="route" id="rt-{i}"><summary><span class="r-title"><span class="caret" aria-hidden="true"></span>{esc(r["route"])}</span>'
                 f'<span class="r-verdicts">{fz(r["feasibility"], True)}</span><span class="r-line">{inline(r["feasibility_reason"])}</span></summary>'
                 f'<div class="r-body">{"".join(body)}</div></details>')
    h.append('</div>')
    return ''.join(h)


def field_table(tid, rows):
    present = [m for m in MAP if any(r['mapping'] == m for r in rows)]
    opts = ''.join(f'<option value="{esc(m)}">{esc(m)}</option>' for m in present)
    out = [f'<div class="filters" data-table="{tid}"><input type="search" placeholder="Filter fields (e.g. vat, address, tax)" aria-label="Filter fields">'
           f'<select class="btn" aria-label="Filter by mapping type"><option value="">All mapping types</option>{opts}</select><span class="count" aria-live="polite"></span></div>']
    out.append(f'<div class="table-wrap"><table class="fieldmap simple" id="{tid}"><thead><tr><th>Chift attribute</th><th>Horus</th><th>Mapping</th><th>What happens</th><th>Basis</th></tr></thead><tbody>')
    group = None
    for r in rows:
        if r['group'] != group:
            group = r['group']
            out.append(f'<tr class="group-row"><td colspan="5">{esc(group)}</td></tr>')
        req = ' <span class="tag" title="Required by Chift">req.</span>' if r['required'] else ''
        out.append(f'<tr data-cls="{esc(r["mapping"])}"><td><code>{esc(r["chift_field"])}</code>{req}</td><td>{inline(r["horus_field"])}</td>'
                   f'<td>{mp(r["mapping"])}</td><td class="rule">{inline(r["note"])}</td><td>{lbl(r["basis"])}</td></tr>')
    out.append('</tbody></table></div>')
    return ''.join(out)


def flow_h(steps):
    return '<ol class="hflow">' + ''.join(f'<li>{inline(s)}</li>' for s in steps) + '</ol>'


def task_b(D):
    h = [f'<p>{T.TASKB_INTRO}</p>', T.MAPPING_LEGEND]
    for key, title, chift in T.TASKB_ORDER:
        b = D['taskb'][key]
        h.append(f'<h3 id="tb-{key}">{esc(title)}</h3><p class="kicker mono">{esc(chift)}</p>')
        h.append(f'<p>{inline(b["intro"])}</p>')
        h.append('<h4>Horus calls behind one Chift call</h4>' + flow_h(b['call_flow']))
        h.append('<h4>Key points</h4>' + ul(b['key_points'], with_basis))
        if T.TASKB_EXTRA.get(key):
            h.append(T.TASKB_EXTRA[key])
        h.append(f'<h4>Attribute and query-parameter mapping ({len(b["rows"])} rows)</h4>' + field_table(f'fm-{key}', b['rows']))
        if b['horus_required_extra']:
            h.append('<details class="route inner"><summary><span class="r-title"><span class="caret" aria-hidden="true"></span>Horus-required fields that Chift does not send</span>'
                     '<span class="r-line">How the connector would fill them.</span></summary><div class="r-body"><div class="table-wrap"><table><thead><tr><th>Horus field</th><th>How it would be filled</th><th>Basis</th></tr></thead><tbody>'
                     + ''.join(f'<tr><td>{inline(x["horus_field"])}</td><td>{inline(x["how_filled"])}</td><td>{lbl(x["basis"])}</td></tr>' for x in b['horus_required_extra'])
                     + '</tbody></table></div></div></details>')
    return ''.join(h)


def limitations(D):
    h = [f'<p>{T.LIMITS_INTRO}</p>']
    for i, l in enumerate(D['lq']['limitations'], 1):
        h.append(f'<div class="limit"><h3 id="lim-{i}"><span class="num">{i}</span>{esc(l["title"])} {lbl(l["basis"])}</h3>'
                 f'<dl><dt>What Horus does</dt><dd>{inline(l["what"])}</dd><dt>Business implication</dt><dd>{inline(l["implication"])}</dd>'
                 f'<dt>Proposed handling</dt><dd>{inline(l["handling"])}</dd><dt>To be decided by</dt><dd>{esc(l["decision_owner"])}</dd>'
                 f'<dt>Routes</dt><dd>{esc(l["routes"])}</dd></dl></div>')
    return ''.join(h)


def q_rows(qs):
    out = []
    for q in qs:
        tier = int(q['tier'])
        pr = {1: '<span class="tier tier-1">Before build</span>', 2: '<span class="tier tier-2">Route design</span>', 3: '<span class="tier tier-3">Verify in a test folder</span>'}.get(tier, '')
        ref = '' if q['in_reference'] else ' <span class="tag" title="Not in the detailed reference">new</span>'
        extra = f' <span class="sub">({esc(q["merged_or_remark"])})</span>' if q.get('merged_or_remark') else ''
        out.append(f'<tr id="q-{esc(q["id"].lower())}"><td class="num">{esc(q["id"])}{ref}</td><td>{esc(q["who"])}<br>{pr}</td><td>{inline(q["short"])}{extra}</td><td>{inline(q["why"])}</td><td>{esc(q["routes"])}</td></tr>')
    return ''.join(out)


def questions(D):
    qs = sorted(D['questions'], key=lambda q: (int(q['tier']), 0 if q['who'] == 'Horus' else 1, int(q['id'][1:])))
    head = '<div class="table-wrap"><table class="q-table"><thead><tr><th>#</th><th>For</th><th>Question</th><th>What depends on it</th><th>Routes</th></tr></thead><tbody>'
    first = [q for q in qs if int(q['tier']) == 1]
    rest = [q for q in qs if int(q['tier']) != 1]
    h = [f'<p>{T.QUESTIONS_INTRO}</p>', '<h3 id="q-before">Before build</h3>', head + q_rows(first) + '</tbody></table></div>']
    h.append('<details class="route inner" id="q-other"><summary><span class="r-title"><span class="caret" aria-hidden="true"></span>'
             f'Other open questions ({len(rest)})</span><span class="r-line">Questions that shape one route\u2019s design, or that can be checked in a test folder. '
             'They are referred to by id in the tables above.</span></summary><div class="r-body">' + head + q_rows(rest) + '</tbody></table></div></div></details>')
    h.append(f'<p class="small">{T.QUESTIONS_NOTE}</p>')
    h.append('<h3 id="next-steps">Proposed next steps</h3><ol class="tight">' + ''.join(f'<li>{s}</li>' for s in T.NEXT_STEPS) + '</ol>')
    return ''.join(h)


def appendix(D):
    h = ['<details class="route" id="app-sources"><summary><span class="r-title"><span class="caret" aria-hidden="true"></span>A. Sources, method and how to read this report</span>'
         '<span class="r-line">What the analysis is based on, and what the labels mean.</span></summary><div class="r-body">' + T.SOURCES_HTML + '</div></details>']
    h.append('<details class="route" id="app-corrections"><summary><span class="r-title"><span class="caret" aria-hidden="true"></span>B. Corrections and updates relative to the detailed reference</span>'
             f'<span class="r-line">{esc(T.CORR_LINE)}</span></summary><div class="r-body"><p>{T.CORR_INTRO}</p>')
    h.append('<div class="table-wrap"><table><thead><tr><th>Topic</th><th>The detailed reference says</th><th>This report says</th><th>Why</th><th>Type</th></tr></thead><tbody>')
    for c in D['corr']['corrections']:
        h.append(f'<tr><td><b>{esc(c["topic"])}</b></td><td>{inline(c["reference_said"])}</td><td>{inline(c["now"])}</td><td>{inline(c["why"])}</td><td>{esc(c["kind"])}<br><span class="sub">{esc(c["impact"])} impact</span></td></tr>')
    h.append('</tbody></table></div></div></details>')
    return ''.join(h)


def build(out_html):
    D = json.load(open(os.path.join(HERE, 'assess_data.json')))
    css = open(os.path.join(HERE, 'shell.css')).read() + '\n' + open(os.path.join(HERE, 'assess.css')).read()
    js = open(os.path.join(HERE, 'shell.js')).read()
    secs = [
        ('summary', '1', 'Executive summary and feasibility', summary(D), [('sum-evidence', 'How sure are we?'), ('sum-messages', 'Key messages')]),
        ('differences', '2', 'How Horus differs from Chift', differences(D), []),
        ('routes', '3', 'Route mapping (Task A)', routes(D), [('rt-details', 'Considerations per route')]),
        ('fields', '4', 'Field mappings (Task B)', task_b(D), [(f'tb-{k}', t) for k, t, _ in T.TASKB_ORDER]),
        ('limits', '5', 'Key limitations and design considerations', limitations(D), []),
        ('questions', '6', 'Open questions and next steps', questions(D), [('q-before', 'Before build'), ('next-steps', 'Next steps')]),
        ('appendix', 'A–B', 'Appendices', appendix(D), []),
    ]
    rail = [(sid, f'{num} {title}', subs) for sid, num, title, _, subs in secs]
    body = '\n'.join(section(sid, num, title, html) for sid, num, title, html, _ in secs)
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(T.TITLE)}</title>
<meta name="description" content="{esc(T.DESCRIPTION)}">
<style>
{css}
</style>
</head>
<body>
<div class="page" id="top">
  <aside class="rail" aria-label="Contents">
    <p class="brandline">{esc(T.RAIL_LABEL)}</p>
    <button class="btn toc-toggle" id="toc-toggle" aria-expanded="false" aria-controls="toc">Contents</button>
    <nav id="toc">{nav(rail)}</nav>
    <div class="tools">
      <button class="btn" id="theme-toggle">Dark theme</button>
    </div>
  </aside>
  <main>
    {T.HEADER_HTML}
    {body}
    <footer class="doc-foot">{T.FOOTER_HTML}</footer>
  </main>
</div>
<a class="btn to-top" href="#top">↑ Contents</a>
<script>
{js}
</script>
</body>
</html>
'''
    open(out_html, 'w', encoding='utf-8').write(page)
    return out_html


if __name__ == '__main__':
    if os.path.basename(sys.argv[1]) == 'chift_horus_mapping_report.html':
        sys.exit('Refusing to overwrite the preserved detailed reference.')
    print(build(sys.argv[1]))
