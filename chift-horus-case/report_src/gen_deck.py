"""Build the presentation deck for the Horus connector assessment (single self-contained HTML file).

Content: deck_content.json (slide text and speaker notes, drafted from the concise report)
Data:    assess_data.json (routes, feasibility levels, Task B mappings) and the tax-combination appendix (VAT counts)
Usage:   python3 -I gen_deck.py <out_html>
"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assess_content as T

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TITLE = 'Horus Connector Assessment Deck'
FOOT = 'Horus connector assessment · Chift product/tech case, Part 1'

LAYOUT = {'1': 'title', '2': 'two', '3': 'stat', '4': 'cols4', '5': 'flow', '6': 'table', '7': 'routes', '8': 'two', '9': 'cards',
          '10': 'chart', '11': 'taskb', '12': 'taskb', '13': 'vat', '14': 'two', '15': 'table', '16': 'cards', '17': 'cards',
          '18': 'timeline', '19': 'closing', 'A1': 'table', 'A2': 'two'}
FZ = {'Confirmed': 'ok', 'Feasible with assumptions': 'ass', 'Needs confirmation': 'conf', 'Not yet concluded': 'open'}
GROUPS = [('direct', 'Direct', ['Direct'], 'same meaning, possibly renamed'),
          ('translate', 'Transform or lookup', ['Transform', 'Lookup'], 'format, code or sign changes, or a Horus reference must be found'),
          ('filled', 'Filled by connector or Chift', ['Generated', 'Constant', 'Chift-side'], 'generated, fixed or handled by Chift'),
          ('na', 'Not available in Horus', ['Not available'], 'no place for it in Horus')]
TASKB_KEYS = [('client', 'Client creation'), ('invoice', 'Invoice creation'), ('outst', 'Outstanding items')]
TASKB_SLIDE = {'11': 'client', '12': 'invoice'}


def esc(s):
    return html.escape(str(s or ''), quote=True)


def fmt(s):
    """Escape, then allow `code` spans and **bold**."""
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    return s


def tag(t):
    if not t:
        return ''
    t = str(t).strip()
    if re.fullmatch(r'([HC]\d{1,2})([ ,/]+[HC]\d{1,2})*', t):
        return f'<span class="tag q">{esc(t)}</span>'
    if t.lower().startswith('propos'):
        return f'<span class="tag prop">{esc(t)}</span>'
    if t in FZ:
        return f'<span class="fz fz-{FZ[t]}">{esc(t)}</span>'
    return f'<span class="tag">{esc(t)}</span>'


def items(lst, cls='b'):
    if not lst:
        return ''
    return f'<ul class="{cls}">' + ''.join(f'<li>{fmt(i["text"])}{tag(i.get("tag"))}</li>' for i in lst) + '</ul>'


def table(t, cls='t'):
    if not t or not t.get('headers'):
        return ''
    h = ''.join(f'<th>{esc(x)}</th>' for x in t['headers'])
    rows = ''.join('<tr>' + ''.join(f'<td>{cell(c)}</td>' for c in r) + '</tr>' for r in t['rows'])
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{rows}</tbody></table>'


def cell(c):
    c = str(c)
    if c in ('Direct', 'Transform', 'Lookup', 'Generated', 'Constant', 'Chift-side', 'Not available'):
        return f'<span class="mp mp-{c.lower().replace(" ", "-")}">{esc(c)}</span>'
    return fmt(c)


def head(s):
    k = f'<p class="kicker">{fmt(s["kicker"])}</p>' if s.get('kicker') else ''
    lead = f'<p class="lead">{fmt(s["lead"])}</p>' if s.get('lead') else ''
    return f'{k}<h1>{fmt(s["title"])}</h1>{lead}'


def callout(s, warn=False):
    return f'<div class="callout{" warn" if warn else ""}">{fmt(s["callout"])}</div>' if s.get('callout') else ''


# ---------- data helpers ----------

def effort_map():
    note = T.TILE_NOTE
    m = re.search(r'low for (.+?); medium for (.+?); high for (.+?)\.', note)
    assert m, 'TILE_NOTE effort sentence not found'
    out = {}
    for level, txt in zip(('Low', 'Medium', 'High'), m.groups()):
        for name in re.split(r', | and ', txt):
            out[name.strip().lower()] = level
    return out


def route_effort(route, eff):
    r = route.lower()
    keys = {'client creation': 'client creation', 'invoice retrieval': 'invoice retrieval', 'invoice creation': 'invoice creation',
            'journal': 'journals', 'ledger account': 'ledger account creation', 'chart of accounts': 'chart of accounts',
            'folders': 'folders', 'miscellaneous': 'miscellaneous operations', 'analytic plans': 'analytic plans',
            'analytic accounts': 'analytic accounts', 'outstanding': 'outstanding items'}
    for k, v in keys.items():
        if k in r:
            return eff[v]
    raise KeyError(route)


def eff_html(level):
    n = {'Low': 1, 'Medium': 2, 'High': 3}[level]
    return '<span class="eff">' + ''.join(f'<b class="{"on" if i < n else ""}"></b>' for i in range(3)) + f' {esc(level)}</span>'


def short_route(name):
    return re.sub(r' \((multiple plans|Task B only)\)', '', name)


def vat_counts():
    txt = open(os.path.join(REPO, 'appendix_horus_tax_combinations.md'), encoding='utf-8').read()
    out = {}
    for part in re.split(r'^## ', txt, flags=re.M)[1:]:
        f = 'sales' if 'sales' in part.split('\n')[0] else 'purchases'
        for leg, n in re.findall(r'### Sheet: Combinations \((BE|LU)\) \((\d+) rows\)', part):
            out[(f, leg)] = int(n)
    return out


# ---------- layouts ----------

def L_title(s, D):
    return (f'<p class="kicker">{fmt(s["kicker"])}</p><h1>{fmt(s["title"])}</h1><p class="lead">{fmt(s["lead"])}</p>'
            '<div class="meta"><span>Presented by <b>Silas Deblanc</b></span><span>For <b>Chift, Product &amp; Tech</b></span>'
            '<span>13 October 2026</span><span>Desk analysis of the documentation, no live API calls</span></div>')


def L_two(s, D):
    cols = ''.join(f'<div class="col panel"><h3>{fmt(b["heading"])}{tag(b.get("tag"))}</h3>{items(b["items"])}</div>' for b in s['blocks'][:2])
    extra = ''.join(f'<div class="col panel"><h3>{fmt(b["heading"])}{tag(b.get("tag"))}</h3>{items(b["items"], "b sm")}</div>' for b in s['blocks'][2:3])
    n = min(len(s['blocks']), 3)
    return head(s) + f'<div class="body"><div class="cols c{max(n, 2)}">{cols}{extra}</div>{table(s.get("table"), "t compact")}{callout(s)}</div>'


def L_stat(s, D):
    by = {}
    for r in D['routes']:
        by.setdefault(r['feasibility'], []).append(short_route(r['route']))
    cards = ''
    for lvl in ('Confirmed', 'Feasible with assumptions', 'Needs confirmation', 'Not yet concluded'):
        if lvl not in by:
            continue
        cards += (f'<div class="stat {FZ[lvl]}"><div class="n">{len(by[lvl])}</div><div class="l">{esc(lvl)}</div>'
                  f'<div class="r">{esc(", ".join(by[lvl]))}</div></div>')
    return head(s) + f'<div class="body"><div class="stats">{cards}</div>{callout(s, warn=True)}</div>'


def L_cols4(s, D):
    kinds = ['ok', 'ass', 'conf', 'open']
    cols = ''.join(f'<div class="panel {kinds[i % 4]}"><h3>{fmt(b["heading"])}</h3>{items(b["items"])}</div>' for i, b in enumerate(s['blocks'][:4]))
    return head(s) + f'<div class="body"><div class="cols c4">{cols}</div>{callout(s)}</div>'


def L_flow(s, D):
    steps = ''
    for i, b in enumerate(s['blocks'], 1):
        body = ''.join(f'<p>{fmt(x["text"])}{tag(x.get("tag"))}</p>' for x in b['items'])
        steps += f'<div class="step"><span class="num">{i}</span><h3>{fmt(b["heading"])}</h3>{body}</div>'
    return head(s) + f'<div class="body"><div class="steps">{steps}</div>{table(s.get("table"), "t compact")}{callout(s)}</div>'


def L_table(s, D):
    blocks = ''.join(f'<div class="panel"><h3>{fmt(b["heading"])}</h3>{items(b["items"], "b sm")}</div>' for b in s.get('blocks', []))
    cls = 't compact' if len(s['table']['rows']) > 6 else 't'
    return head(s) + f'<div class="body">{table(s["table"], cls)}{blocks}{callout(s)}</div>'


def L_routes(s, D):
    eff = effort_map()
    rows = ''
    for r in D['routes']:
        main = '<br>'.join(esc(re.sub(r' \(.*\)$', '', e)) for e in r['horus_main'])
        rows += (f'<tr><td title="{esc(r["chift"])}">{esc(short_route(r["route"]))}</td><td class="eps">{main}</td>'
                 f'<td>+{len(r["horus_support"])}</td><td><span class="fz fz-{FZ[r["feasibility"]]}">{esc(r["feasibility"])}</span></td>'
                 f'<td>{eff_html(route_effort(r["route"], eff))}</td></tr>')
    t = ('<table class="t compact routes"><thead><tr><th>Chift route</th><th>Main Horus endpoint(s)</th><th>Supporting endpoints</th><th>Feasibility</th><th>Build effort</th></tr></thead>'
         f'<tbody>{rows}</tbody></table>')
    return head(s) + f'<div class="body">{t}{callout(s)}</div>'


def L_cards(s, D):
    n = len(s['blocks'])
    cls = {3: 'n3', 4: 'n4', 5: 'n5'}.get(n, 'n4' if n < 4 else 'n3')
    cards = ''.join(f'<div class="card"><h3>{fmt(b["heading"])}{tag(b.get("tag"))}</h3>{items(b["items"])}</div>' for b in s['blocks'])
    return head(s) + f'<div class="body"><div class="cards {cls}">{cards}</div>{callout(s)}</div>'


def L_chart(s, D):
    legend = '<div class="legend">' + ''.join(f'<span><i style="background:var(--s-{g})"></i>{esc(label)}</span>' for g, label, _, _ in GROUPS) + '</div>'
    rows, trows = '', ''
    for key, name in TASKB_KEYS:
        b = D['taskb'][key]
        tot = len(b['rows'])
        counts = {g: sum(1 for r in b['rows'] if r['mapping'] in ms) for g, _, ms, _ in GROUPS}
        assert sum(counts.values()) == tot, (key, counts, tot)
        segs = ''
        for g, label, _, desc in GROUPS:
            c = counts[g]
            if not c:
                continue
            show = str(c) if c / tot >= 0.06 else ''
            segs += (f'<span class="seg {g}" style="flex:{c} 1 0" tabindex="0" data-tip="{esc(name)} · {esc(label)}: {c} of {tot} rows ({esc(desc)})" '
                     f'aria-label="{esc(label)}: {c} of {tot}">{show}</span>')
        rows += f'<div class="bar-row"><div class="name">{esc(name)}<span>{tot} attributes and parameters</span></div><div class="bar">{segs}</div><div class="total">{tot}</div></div>'
        trows += f'<tr><td>{esc(name)}</td>' + ''.join(f'<td>{counts[g]}</td>' for g, *_ in GROUPS) + f'<td>{tot}</td></tr>'
    tview = ('<table class="t compact"><thead><tr><th>Route</th>' + ''.join(f'<th>{esc(l)}</th>' for _, l, _, _ in GROUPS) + '<th>Total</th></tr></thead>'
             f'<tbody>{trows}</tbody></table>')
    return head(s) + f'<div class="body"><div class="chart">{legend}{rows}</div>{tview}{callout(s)}</div>'


def L_taskb(s, D):
    steps = [b for b in s['blocks'] if b['heading'].lower() != 'key points']
    kp = next((b for b in s['blocks'] if b['heading'].lower() == 'key points'), None)
    flow = '<ol class="hsteps">' + ''.join(f'<li><b>{fmt(b["heading"])}</b>' + ''.join(f'<span>{fmt(x["text"])}</span>' for x in b['items']) + '</li>' for b in steps) + '</ol>'
    left = f'<div class="panel"><h3>Key points</h3>{items(kp["items"], "b sm")}</div>' if kp else ''
    return head(s) + f'<div class="body">{flow}<div class="tb3">{left}<div>{table(s.get("table"), "t compact")}</div></div>{callout(s)}</div>'


def L_vat(s, D):
    v = vat_counts()
    t = s.get('table') or {}
    txt = json.dumps(t)
    for n in v.values():  # the drafted table must carry the counts from the spreadsheets
        assert str(n) in txt, f'VAT count {n} missing from slide table'
    if not t.get('headers'):
        t = {'headers': ['Horus spreadsheet', 'Belgium', 'Luxembourg'],
             'rows': [['Sales combinations', v[('sales', 'BE')], v[('sales', 'LU')]], ['Purchase combinations', v[('purchases', 'BE')], v[('purchases', 'LU')]]]}
    blocks = ''.join(f'<div class="panel"><h3>{fmt(b["heading"])}{tag(b.get("tag"))}</h3>{items(b["items"], "b sm")}</div>' for b in s['blocks'])
    return head(s) + f'<div class="body">{table(t, "t compact")}<div class="vat-grid">{blocks}</div>{callout(s)}</div>'


def L_timeline(s, D):
    ph = ''.join(f'<div class="phase{" gate" if i == 0 else ""}"><h3>{fmt(b["heading"])}</h3>{items(b["items"])}</div>' for i, b in enumerate(s['blocks'][:4]))
    rest = ''.join(f'<div class="panel"><h3>{fmt(b["heading"])}{tag(b.get("tag"))}</h3>{items(b["items"], "b sm")}</div>' for b in s['blocks'][4:])
    return head(s) + f'<div class="body"><div class="timeline">{ph}</div>{rest}{callout(s)}</div>'


def L_closing(s, D):
    cols = ''.join(f'<div class="panel"><h3>{fmt(b["heading"])}</h3>{items(b["items"], "b sm")}</div>' for b in s['blocks'][:3])
    return head(s) + f'<div class="body"><div class="cols c{max(min(len(s["blocks"]), 3), 2)}">{cols}</div>{callout(s)}</div>'


RENDER = {'title': L_title, 'two': L_two, 'stat': L_stat, 'cols4': L_cols4, 'flow': L_flow, 'table': L_table, 'routes': L_routes,
          'cards': L_cards, 'chart': L_chart, 'taskb': L_taskb, 'vat': L_vat, 'timeline': L_timeline, 'closing': L_closing}


def notes_html(t):
    paras = [p.strip() for p in re.split(r'\n\s*\n', t or '') if p.strip()]
    return ''.join(f'<p>{fmt(p)}</p>' for p in paras)


def build(out):
    D = json.load(open(os.path.join(HERE, 'assess_data.json')))
    S = json.load(open(os.path.join(HERE, 'deck_content.json')))['slides']
    css = open(os.path.join(HERE, 'deck.css')).read()
    js = open(os.path.join(HERE, 'deck.js')).read()
    frames = []
    total = len(S)
    for i, s in enumerate(S, 1):
        lay = LAYOUT[s['id']]
        cls = ['slide', 'lay-' + lay]
        if s['id'].startswith('A'):
            cls.append('appendix')
        body = RENDER[lay](s, D)
        foot = '' if lay == 'title' else f'<div class="foot"><span>{esc(FOOT)}{" · Appendix" if s["id"].startswith("A") else ""}</span><span class="n">{i} / {total}</span></div>'
        frames.append(f'<div class="frame" id="slide-{i}" role="group" aria-roledescription="slide" aria-label="Slide {i} of {total}: {esc(s["title"])}">'
                      f'<section class="{" ".join(cls)}">{body}{foot}</section><aside class="notes">{notes_html(s.get("notes"))}</aside></div>')
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(TITLE)}</title>
<meta name="description" content="Presentation of the Horus connector assessment (Chift product/tech case, Part 1): feasibility, route mapping, field mappings, limitations, questions and recommendation.">
<style>
{css}
</style>
</head>
<body>
<div class="progress" aria-hidden="true"></div>
<main class="viewport" aria-label="Slides"><div class="stage">
{"".join(frames)}
</div></main>
<div class="notes-panel" id="notes-panel" hidden aria-live="polite"><h2>Speaker notes</h2><div class="body-notes"></div></div>
<nav class="toolbar" aria-label="Slide controls">
  <button id="prev-btn" aria-label="Previous slide">←</button>
  <span class="count" id="count" aria-live="polite"></span>
  <button id="next-btn" aria-label="Next slide">→</button>
  <button id="overview-btn" aria-pressed="false">Overview</button>
  <button id="notes-btn" aria-pressed="false">Notes</button>
  <span class="hint">← → to move · O overview · N notes · F full screen</span>
</nav>
<div class="tip" role="tooltip"></div>
<script>
{js}
</script>
</body>
</html>
'''
    open(out, 'w', encoding='utf-8').write(page)
    return out


if __name__ == '__main__':
    if os.path.basename(sys.argv[1]) in ('chift_horus_mapping_report.html', 'chift_horus_connector_assessment.html'):
        sys.exit('Refusing to overwrite a report file; write the deck to its own path.')
    print(build(sys.argv[1]))
