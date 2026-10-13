(function () {
  var frames = Array.prototype.slice.call(document.querySelectorAll('.frame'));
  var stage = document.querySelector('.stage');
  var viewport = document.querySelector('.viewport');
  var count = document.getElementById('count');
  var progress = document.querySelector('.progress');
  var notesPanel = document.getElementById('notes-panel');
  var notesBtn = document.getElementById('notes-btn');
  var overBtn = document.getElementById('overview-btn');
  var cur = 0;

  function fit() {
    if (document.body.classList.contains('overview')) { fitThumbs(); return; }
    var w = viewport.clientWidth, h = viewport.clientHeight;
    var s = Math.min((w - 24) / 1280, (h - 24) / 720);
    stage.style.transform = 'scale(' + Math.max(s, 0.1) + ')';
  }
  function fitThumbs() {
    frames.forEach(function (f) { f.style.setProperty('--thumb', (f.clientWidth / 1280).toFixed(4)); });
  }
  function fromHash() {
    var m = /^#(\d+)$/.exec(location.hash || '');
    return m ? Math.min(Math.max(parseInt(m[1], 10) - 1, 0), frames.length - 1) : 0;
  }
  function show(i, push) {
    cur = Math.min(Math.max(i, 0), frames.length - 1);
    frames.forEach(function (f, k) { f.classList.toggle('active', k === cur); f.setAttribute('aria-hidden', k === cur ? 'false' : 'true'); });
    count.textContent = (cur + 1) + ' / ' + frames.length;
    progress.style.width = ((cur + 1) / frames.length * 100) + '%';
    var n = frames[cur].querySelector('.notes');
    notesPanel.querySelector('.body-notes').innerHTML = n ? n.innerHTML : '<p>No notes for this slide.</p>';
    if (push !== false) { try { history.replaceState(null, '', '#' + (cur + 1)); } catch (e) {} }
  }
  function toggleNotes(force) {
    var on = typeof force === 'boolean' ? force : notesPanel.hidden;
    notesPanel.hidden = !on;
    notesBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    try { localStorage.setItem('deck-notes', on ? '1' : '0'); } catch (e) {}
  }
  function toggleOverview(force) {
    var on = typeof force === 'boolean' ? force : !document.body.classList.contains('overview');
    document.body.classList.toggle('overview', on);
    overBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    frames.forEach(function (f) { if (on) { f.setAttribute('tabindex', '0'); f.setAttribute('aria-hidden', 'false'); } else { f.removeAttribute('tabindex'); } });
    if (on) { stage.style.transform = 'none'; requestAnimationFrame(function () { fitThumbs(); frames[cur].scrollIntoView({ block: 'center' }); }); }
    else { show(cur, false); fit(); }
  }

  document.getElementById('prev-btn').addEventListener('click', function () { show(cur - 1); });
  document.getElementById('next-btn').addEventListener('click', function () { show(cur + 1); });
  notesBtn.addEventListener('click', function () { toggleNotes(); });
  overBtn.addEventListener('click', function () { toggleOverview(); });
  frames.forEach(function (f, k) {
    f.addEventListener('click', function () { if (document.body.classList.contains('overview')) { show(k); toggleOverview(false); } });
    f.addEventListener('keydown', function (e) { if (document.body.classList.contains('overview') && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); show(k); toggleOverview(false); } });
  });
  document.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    var t = e.target; if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA')) return;
    var overview = document.body.classList.contains('overview');
    switch (e.key) {
      case 'ArrowRight': case 'PageDown': case ' ': if (!overview) { e.preventDefault(); show(cur + 1); } break;
      case 'ArrowLeft': case 'PageUp': if (!overview) { e.preventDefault(); show(cur - 1); } break;
      case 'ArrowDown': if (!overview) { e.preventDefault(); show(cur + 1); } break;
      case 'ArrowUp': if (!overview) { e.preventDefault(); show(cur - 1); } break;
      case 'Home': e.preventDefault(); show(0); break;
      case 'End': e.preventDefault(); show(frames.length - 1); break;
      case 'n': case 'N': toggleNotes(); break;
      case 'o': case 'O': toggleOverview(); break;
      case 'Escape': if (overview) toggleOverview(false); break;
      case 'f': case 'F':
        if (document.fullscreenElement) { document.exitFullscreen && document.exitFullscreen().catch(function () {}); }
        else if (document.documentElement.requestFullscreen) { document.documentElement.requestFullscreen().catch(function () {}); }
        break;
    }
  });
  // swipe on touch screens
  var sx = null, sy = null;
  viewport.addEventListener('touchstart', function (e) { if (e.touches.length === 1) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; } }, { passive: true });
  viewport.addEventListener('touchend', function (e) {
    if (sx === null || document.body.classList.contains('overview')) return;
    var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(cur + (dx < 0 ? 1 : -1));
    sx = sy = null;
  });
  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', function () { show(fromHash(), false); });

  // chart tooltips (hover and keyboard focus)
  var tip = document.querySelector('.tip');
  document.querySelectorAll('[data-tip]').forEach(function (el) {
    function on(e) {
      tip.textContent = el.getAttribute('data-tip'); tip.style.display = 'block';
      var r = el.getBoundingClientRect();
      var x = e && e.clientX ? e.clientX : r.left + r.width / 2, y = e && e.clientY ? e.clientY : r.top;
      tip.style.left = Math.min(x + 12, window.innerWidth - tip.offsetWidth - 8) + 'px';
      tip.style.top = Math.max(y - tip.offsetHeight - 10, 8) + 'px';
    }
    function off() { tip.style.display = 'none'; }
    el.addEventListener('mousemove', on); el.addEventListener('mouseleave', off);
    el.addEventListener('focus', function () { on(null); }); el.addEventListener('blur', off);
  });

  var savedNotes = false;
  try { savedNotes = localStorage.getItem('deck-notes') === '1'; } catch (e) {}
  toggleNotes(savedNotes);
  show(fromHash(), false);
  fit();
})();
