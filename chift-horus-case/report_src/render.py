"""Rendering helpers for the external Chift x Horus report (static HTML from the reconciled mapping JSON)."""
import html, re

VERDICT_TEXT = {
    'supported': 'Supported',
    'workaround': 'Supported with workaround',
    'not_supported': 'Not supported',
    'unknown': 'To confirm',
}
LABEL_TEXT = {'F': ('F', 'Documented'), 'D': ('D', 'Derived'), 'A': ('A', 'Assumption'), '?': ('Q', 'To confirm')}
CLS_TEXT = {
    'DIRECT': 'Direct', 'TRANSFORM': 'Transform', 'LOOKUP': 'Lookup', 'COMPOSITE': 'Composite',
    'CONSTANT': 'Constant', 'NA': 'Not available', 'CHIFT_INTERNAL': 'Chift-side',
}
KIND_TEXT = {
    'path_param': 'Path parameters', 'query_param': 'Query parameters',
    'request_field': 'Request body', 'response_field': 'Response (what the connector returns)',
}
KIND_ORDER = ['path_param', 'query_param', 'request_field', 'response_field']
ROLE_TEXT = {'primary': 'Primary', 'follow_up': 'Follow-up', 'lookup': 'Lookup', 'enrichment': 'Enrichment', 'alternative': 'Alternative', 'optional': 'Optional'}


def esc(s):
    return html.escape('' if s is None else str(s), quote=True)


def inline(s):
    """Escape, then render `code` spans and **bold**."""
    t = esc(s)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
    return t


def rich(s):
    """Escape data text, then render paragraphs, '- ' bullet lists, '1. ' numbered lists, **bold** and `code`."""
    if not s:
        return ''
    blocks, out = re.split(r'\n\s*\n', str(s).strip()), []
    for b in blocks:
        lines = [l for l in b.split('\n') if l.strip()]
        para, items, kind = [], [], None
        def flush():
            nonlocal para, items, kind
            if para:
                out.append('<p>' + inline(' '.join(para)) + '</p>'); para = []
            if items:
                tag = 'ol' if kind == 'ol' else 'ul'
                out.append(f'<{tag} class="tight">' + ''.join(f'<li>{inline(i)}</li>' for i in items) + f'</{tag}>'); items = []
        for l in lines:
            t = l.strip()
            m = re.match(r'^(?:[-*•]\s+)(.*)$', t)
            n = re.match(r'^(\d+)[.)]\s+(.*)$', t)
            if m:
                if para or kind == 'ol': flush()
                kind = 'ul'; items.append(m.group(1))
            elif n:
                if para or kind == 'ul': flush()
                kind = 'ol'; items.append(n.group(2))
            else:
                if items: flush()
                para.append(t)
        flush()
    return ''.join(out)


def chip(verdict):
    v = verdict if verdict in VERDICT_TEXT else 'unknown'
    return f'<span class="chip v-{v}">{VERDICT_TEXT[v]}</span>'


def lbl(label):
    code, text = LABEL_TEXT.get(label, ('Q', 'To confirm'))
    return f'<span class="lbl lbl-{code}" title="{text}">{text}</span>'


def cls(c):
    return f'<span class="cls cls-{esc(c)}">{esc(CLS_TEXT.get(c, c))}</span>'


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def field_table(table_id, rows, show_kind_groups=True, caption=None):
    """rows: list of field_mapping dicts."""
    out = []
    present = sorted({r.get('classification') for r in rows if r.get('classification')}, key=lambda c: list(CLS_TEXT).index(c) if c in CLS_TEXT else 99)
    opts = ''.join(f'<option value="{esc(c)}">{esc(CLS_TEXT.get(c, c))}</option>' for c in present)
    out.append(f'<div class="filters" data-table="{table_id}">'
               f'<input type="search" id="{table_id}-q" placeholder="Filter fields (e.g. vat, address, tax)" aria-label="Filter fields">'
               f'<select id="{table_id}-c" class="btn" aria-label="Filter by mapping type"><option value="">All mapping types</option>{opts}</select>'
               f'<span class="count" aria-live="polite"></span></div>')
    out.append('<div class="table-wrap"><table class="fieldmap" id="%s">' % table_id)
    if caption:
        out.append(f'<caption class="sr-only">{esc(caption)}</caption>')
    out.append('<thead><tr><th>Chift attribute</th><th>Horus source</th><th>Mapping</th><th>Rule / consideration</th><th>Basis</th><th class="ev">Evidence (Horus docs)</th></tr></thead><tbody>')
    groups = {}
    for r in rows:
        groups.setdefault(r.get('kind', 'request_field'), []).append(r)
    for k in KIND_ORDER + [k for k in groups if k not in KIND_ORDER]:
        if k not in groups:
            continue
        if show_kind_groups:
            out.append(f'<tr class="group-row"><td colspan="6">{esc(KIND_TEXT.get(k, k))}</td></tr>')
        for r in groups[k]:
            name = r.get('chift_field', '')
            if k == 'response_field' and name.startswith('response.'):
                name = name[len('response.'):]
            if name.startswith('query:'):
                name = name[len('query:'):]
            req = ' <span class="tag" title="Required by Chift">req.</span>' if r.get('chift_required') else ''
            out.append(
                f'<tr data-cls="{esc(r.get("classification"))}">'
                f'<td><code>{esc(name)}</code>{req}</td>'
                f'<td>{inline(r.get("horus_source"))}</td>'
                f'<td>{cls(r.get("classification"))}</td>'
                f'<td class="rule">{inline(r.get("rule"))}</td>'
                f'<td>{lbl(r.get("label"))}</td>'
                f'<td class="ev">{inline(r.get("evidence"))}</td></tr>')
    out.append('</tbody></table></div>')
    return '\n'.join(out)


def endpoint_list(eps):
    items = []
    for e in eps:
        items.append(
            f'<li><span class="tag">{esc(ROLE_TEXT.get(e.get("pattern"), e.get("pattern")))}</span>'
            f'<span><span class="ep">{esc(e.get("method"))} {esc(e.get("path"))}</span> '
            f'<span class="sub">{inline(e.get("role"))} <i>({esc(e.get("cardinality"))})</i></span></span></li>')
    return '<ul class="endpoint-list">' + ''.join(items) + '</ul>'


def flow(steps):
    return '<ol class="flow">' + ''.join(f'<li>{inline(re.sub(r"^\\s*\\d+[a-z]?[.)]\\s+", "", s))}</li>' for s in steps) + '</ol>'


def bullet_list(items, fmt):
    if not items:
        return '<p class="sub">None identified.</p>'
    return '<ul class="tight">' + ''.join(f'<li>{fmt(i)}</li>' for i in items) + '</ul>'


def route_card(rc):
    """rc: dict prepared in content.route_cards(groups)."""
    chips = ' '.join(chip(v) for v in rc['verdicts'])
    body = [f'<p>{rc["brief"]}</p>' if rc.get('brief') else '']
    if rc.get('summary'):
        body.append(f'<details class="route inner"><summary><span class="r-title"><span class="caret">▸</span>Detailed analysis</span></summary><div class="r-body">{rich(rc["summary"])}</div></details>')
    body.append('<div class="two-col"><div>')
    body.append('<h4>Horus endpoints</h4>' + endpoint_list(rc['endpoints']))
    body.append('</div><div>')
    body.append('<h4>Call sequence</h4>' + flow(rc['sequence']))
    body.append('</div></div>')
    if rc.get('considerations'):
        body.append('<h4>Considerations and limitations</h4>' + bullet_list(rc['considerations'], lambda x: f'{inline(x["text"])} {lbl(x["label"])}'))
    if rc.get('fields'):
        body.append(f'<details class="route inner"><summary><span class="r-title"><span class="caret">▸</span>Key field mapping ({len(rc["fields"])} rows)</span></summary><div class="r-body">')
        body.append(field_table(rc['id'] + '-fields', rc['fields']))
        body.append('</div></details>')
    if rc.get('questions'):
        body.append(f'<details class="route inner"><summary><span class="r-title"><span class="caret">▸</span>Detailed open questions ({len(rc["questions"])})</span></summary><div class="r-body">')
        body.append(bullet_list(rc['questions'], lambda q: f'<span class="tag">{esc(q["for_whom"])}</span> {inline(q["question"])} <span class="sub">{inline(q.get("why",""))}</span>'))
        body.append('</div></details>')
    return (f'<details class="route" id="{rc["id"]}"><summary>'
            f'<span class="r-title"><span class="caret">▸</span>{esc(rc["title"])}</span><span>{chips}</span>'
            f'<span class="r-path">{esc(rc["paths"])}</span>'
            f'<span class="r-line">{rc["one_line"]}</span></summary>'
            f'<div class="r-body">{"".join(body)}</div></details>')


