/* ================= Legal & Privacy =================
   1. "Legal & Privacy" card at the bottom of the Me screen (links to the static pages in legal/).
   2. Small "By continuing you agree…" line at the bottom of each onboarding step.
   3. One short, skippable notice on first launch (remembered on this device in localStorage 'sv_legal').
   Pages open in the same window (works in the installed app); "Back to StudyVerse" on a page
   returns here, and we reopen the Me screen if that is where the person came from. */
(function () {
  const KEY = 'sv_legal', RET = 'sv_legal_ret';
  const read = () => { try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { return {}; } };
  const write = o => { try { localStorage.setItem(KEY, JSON.stringify(Object.assign(read(), o))); } catch (e) {} };
  const seen = () => !!read().seen;
  const markReturn = where => { try { sessionStorage.setItem(RET, where); } catch (e) {} };

  /* ---------- 1. Me screen ---------- */
  const LINKS = [['terms', 'Terms of Use'], ['privacy', 'Privacy Policy'], ['disclaimer', 'Disclaimer'], ['refunds', 'Refunds & cancellation'],
    ['copyright', 'Copyright'], ['community', 'Community rules'], ['accessibility', 'Accessibility'], ['parents', "Parent's guide to privacy"], ['children', 'Privacy for kids'], ['contact', 'Contact & grievance']];
  function meCard() {
    const host = document.getElementById('s-me'); if (!host) return;
    document.getElementById('lgCard')?.remove();
    host.insertAdjacentHTML('beforeend', `<div class="card lg-card" id="lgCard"><h3><span aria-hidden="true">⚖️</span> Legal &amp; Privacy</h3>
      <p class="sub">Your progress is saved to your account. StudyVerse is not linked to CBSE, NCERT or ICAI. Always check your textbook for exams.</p>
      <ul class="lg-links">${LINKS.map(([f, n]) => `<li><a href="legal/${f}.html">${n}</a></li>`).join('')}</ul>
      <a class="lg-all" href="legal/index.html">All legal &amp; privacy pages <span aria-hidden="true">›</span></a></div>`);
    host.querySelectorAll('#lgCard a').forEach(a => a.addEventListener('click', () => markReturn('me')));
  }
  if (typeof meScreen === 'function') {
    const _me = meScreen;
    meScreen = function () { const r = _me.apply(this, arguments); meCard(); setTimeout(() => { const c = document.getElementById('lgCard'), h = document.getElementById('s-me'); if (c && h && h.lastElementChild !== c) h.appendChild(c); }, 0); return r; };
  }

  /* ---------- 2. Onboarding footer ---------- */
  function obFoot() {
    const ob = document.querySelector('#s-onboard .ob'); if (!ob || ob.querySelector('.lg-foot')) return;
    ob.insertAdjacentHTML('beforeend', `<p class="lg-foot">By continuing you agree to the <a href="legal/terms.html">Terms</a> and <a href="legal/privacy.html">Privacy Policy</a>. Under 18? Please read them with a parent or guardian.</p>`);
    ob.querySelectorAll('.lg-foot a').forEach(a => a.addEventListener('click', () => markReturn('onboard')));
  }

  /* ---------- 3. First-launch notice (inline, not a pop-up, so it never blocks the app) ---------- */
  function note(where) {
    if (seen() || document.getElementById('lgNote')) return;
    const html = `<aside class="lg-note" id="lgNote" aria-label="Welcome notice">
      <p><b><span aria-hidden="true">📘</span> Before you start</b></p>
      <p>StudyVerse helps you understand topics. It is not linked to CBSE, NCERT or ICAI, and it can make mistakes, so check your textbook for exams. Your progress is saved to your account.</p>
      <div class="lg-note-btns"><button type="button" class="lg-ok" id="lgOk">Got it</button><a href="legal/index.html" id="lgMore">Read more</a></div></aside>`;
    if (where === 'onboard') { const c = document.querySelector('#s-onboard .ob > .card'); if (!c) return; c.insertAdjacentHTML('beforebegin', html); }
    else { const t = document.getElementById('worldTitle'); if (!t) return; t.insertAdjacentHTML('beforebegin', html); }
    const n = document.getElementById('lgNote'); if (!n) return;
    document.getElementById('lgOk').onclick = () => { write({ seen: new Date().toISOString().slice(0, 10) }); const had = n.contains(document.activeElement); n.remove(); if (typeof sfx === 'function') sfx('tap');
      if (had) { const f = document.querySelector('#s-onboard.active .ob h1, #s-world.active #worldTitle'); if (f) { if (!f.hasAttribute('tabindex')) f.setAttribute('tabindex', '-1'); f.focus({ preventScroll: true }); } } };
    document.getElementById('lgMore').addEventListener('click', () => { write({ seen: new Date().toISOString().slice(0, 10) }); markReturn(where); });
  }

  if (typeof onboard === 'function') {
    const _ob = onboard;
    onboard = function (step) { const r = _ob.apply(this, arguments); if ((step || 1) === 1) note('onboard'); return r; };
  }
  /* every onboarding screen (including the Grade 11–12 stream and subject pickers, which redraw themselves) gets the footer */
  const obHost = document.getElementById('s-onboard');
  if (obHost) new MutationObserver(obFoot).observe(obHost, { childList: true });
  /* coming back with the browser's Back button may restore this page as it was: forget the "return to" note */
  window.addEventListener('pageshow', e => { if (e.persisted) { try { sessionStorage.removeItem(RET); } catch (err) {} } });

  if (typeof worldScreen === 'function') {
    const _w = worldScreen;
    worldScreen = async function () {
      const r = await _w.apply(this, arguments);
      note('world');
      let ret = null; try { ret = sessionStorage.getItem(RET); sessionStorage.removeItem(RET); } catch (e) {}
      if (ret === 'me' && ST.profile && typeof meScreen === 'function') meScreen();
      return r;
    };
  }
  window.Legal = { seen, reset: () => { try { localStorage.removeItem(KEY); } catch (e) {} } };
})();
