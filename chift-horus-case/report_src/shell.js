(function () {
  var root = document.documentElement;

  // Theme toggle (remembered per viewer when storage is available)
  var themeBtn = document.getElementById('theme-toggle');
  function currentTheme() {
    var t = root.getAttribute('data-theme');
    if (t) return t;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function labelTheme() { if (themeBtn) themeBtn.textContent = currentTheme() === 'dark' ? 'Light theme' : 'Dark theme'; }
  try { var saved = localStorage.getItem('chm-theme'); if (saved === 'dark' || saved === 'light') root.setAttribute('data-theme', saved); } catch (e) {}
  labelTheme();
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('chm-theme', next); } catch (e) {}
    labelTheme();
  });

  // Mobile contents toggle
  var rail = document.querySelector('.rail');
  var tocBtn = document.getElementById('toc-toggle');
  if (tocBtn && rail) tocBtn.addEventListener('click', function () {
    var open = rail.classList.toggle('open');
    tocBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.querySelectorAll('.rail nav a').forEach(function (a) {
    a.addEventListener('click', function () { if (rail && window.innerWidth <= 960) { rail.classList.remove('open'); if (tocBtn) tocBtn.setAttribute('aria-expanded', 'false'); } });
  });

  // Active section highlight
  var links = {};
  document.querySelectorAll('.rail nav a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && links[en.target.id]) {
          Object.keys(links).forEach(function (k) { links[k].classList.remove('active'); });
          links[en.target.id].classList.add('active');
        }
      });
    }, { rootMargin: '-10% 0px -80% 0px' });
    Object.keys(links).forEach(function (id) { var el = document.getElementById(id); if (el) obs.observe(el); });
  }

  // Open a route card when navigated to by anchor
  function openFromHash() {
    var id = location.hash.slice(1); if (!id) return;
    var el = document.getElementById(id);
    if (el && el.tagName === 'DETAILS') el.open = true;
  }
  window.addEventListener('hashchange', openFromHash); openFromHash();

  // Expand / collapse all route cards within a container
  document.querySelectorAll('[data-expand]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var scope = document.getElementById(btn.getAttribute('data-expand'));
      if (!scope) return;
      var cards = scope.querySelectorAll('details');
      var anyClosed = Array.prototype.some.call(cards, function (d) { return !d.open; });
      cards.forEach(function (d) { d.open = anyClosed; });
      btn.textContent = anyClosed ? 'Collapse all' : 'Expand all';
    });
  });

  // Evidence column toggle (all field-mapping tables)
  var evBtn = document.getElementById('evidence-toggle');
  if (evBtn) evBtn.addEventListener('click', function () {
    var hidden = document.body.classList.toggle('hide-evidence');
    evBtn.setAttribute('aria-pressed', hidden ? 'false' : 'true');
    evBtn.textContent = hidden ? 'Show evidence' : 'Hide evidence';
  });

  // Field-mapping filters
  document.querySelectorAll('.filters[data-table]').forEach(function (bar) {
    var table = document.getElementById(bar.getAttribute('data-table'));
    if (!table) return;
    var search = bar.querySelector('input[type="search"]');
    var select = bar.querySelector('select');
    var count = bar.querySelector('.count');
    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr:not(.group-row)'));
    function apply() {
      var q = (search && search.value || '').toLowerCase().trim();
      var c = select ? select.value : '';
      var shown = 0;
      rows.forEach(function (r) {
        var ok = (!q || r.textContent.toLowerCase().indexOf(q) !== -1) && (!c || r.getAttribute('data-cls') === c);
        r.hidden = !ok; if (ok) shown++;
      });
      table.querySelectorAll('tbody tr.group-row').forEach(function (g) {
        var n = g.nextElementSibling, any = false;
        while (n && !n.classList.contains('group-row')) { if (!n.hidden) any = true; n = n.nextElementSibling; }
        g.hidden = !any;
      });
      if (count) count.textContent = shown + ' of ' + rows.length + ' fields';
    }
    if (search) search.addEventListener('input', apply);
    if (select) select.addEventListener('change', apply);
    apply();
  });
})();
