"""Build the external Chift x Horus mapping report (single self-contained HTML file).

Inputs: reconciled mapping JSON (one file per route group + cross-cutting), curated narrative in content.py.
Usage: python3 -I gen_report.py <data_dir> <out_html>
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import esc
import content as C

HERE = os.path.dirname(os.path.abspath(__file__))


SANITISE = [
    (r'\s*\(D15\)', ''), (r',\s*D15\)', ')'), (r'Correction \(D15\):\s*', ''), (r'\s*\(D14\)', ''),
    (r'not among the admissible sources', 'not available for this analysis'),
    (r'cannot be built from admissible sources', 'cannot be built from the available documentation'),
    (r'admissible sources', 'available documentation'),
    (r'the raw Notion export', 'the documentation pages'), (r'raw Notion export', 'documentation pages'),
    (r'as of the reference export', 'in the current API reference'), (r'reference export', 'API reference'),
    (r'raw export example', 'reference example'), (r'raw export', 'reference'),
    (r'Harmonised conventions', 'Shared conventions'), (r'harmonised conventions', 'shared conventions'),
]


def sanitise(o):
    import re as _re
    if isinstance(o, dict):
        return {k: sanitise(v) for k, v in o.items()}
    if isinstance(o, list):
        return [sanitise(v) for v in o]
    if isinstance(o, str):
        for a, b in SANITISE:
            o = _re.sub(a, b, o)
        return o
    return o


def load(data_dir):
    groups = {}
    for f in os.listdir(data_dir):
        if f.endswith('.json') and f not in ('cross.json',) and not f.endswith('.reports.json'):
            groups[f[:-5]] = sanitise(json.load(open(os.path.join(data_dir, f))))
    cross = sanitise(json.load(open(os.path.join(data_dir, 'cross.json')))) if os.path.exists(os.path.join(data_dir, 'cross.json')) else None
    return groups, cross


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


def build(data_dir, out_html):
    groups, cross = load(data_dir)
    css = open(os.path.join(HERE, 'shell.css')).read()
    js = open(os.path.join(HERE, 'shell.js')).read()
    sections = C.sections(groups, cross)  # list of (id, num, title, html, subnav)
    rail_items = [(sid, f'{num} {title}' if num else title, subs) for sid, num, title, _, subs in sections]
    body_html = '\n'.join(section(sid, num, title, html) for sid, num, title, html, _ in sections)
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(C.TITLE)}</title>
<meta name="description" content="{esc(C.DESCRIPTION)}">
<style>
{css}
</style>
</head>
<body>
<div class="page">
  <aside class="rail" aria-label="Contents">
    <p class="brandline">{esc(C.RAIL_LABEL)}</p>
    <button class="btn toc-toggle" id="toc-toggle" aria-expanded="false" aria-controls="toc">Contents</button>
    <nav id="toc">{nav(rail_items)}</nav>
    <div class="tools">
      <button class="btn" id="evidence-toggle" aria-pressed="true">Hide evidence</button>
      <button class="btn" id="theme-toggle">Dark theme</button>
    </div>
  </aside>
  <main>
    {C.header_html()}
    {body_html}
    <footer class="doc-foot">{C.footer_html()}</footer>
  </main>
</div>
<script>
{js}
</script>
</body>
</html>
'''
    open(out_html, 'w', encoding='utf-8').write(page)
    return out_html


if __name__ == '__main__':
    print(build(sys.argv[1], sys.argv[2]))
