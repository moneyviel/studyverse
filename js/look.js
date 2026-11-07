/* ================= Look & feel: age bands, quieter 🔊 buttons, a polite Ask button =================
   1. Age bands. <html data-age="kids|junior|teen|senior|pro"> sets the look through CSS custom properties
      (colours, corners, shadows, type, emoji size, motion) in the "Age looks" block of css/app.css.
      Auto picks the band from the grade: 1–3 kids · 4–7 junior · 8–10 teen · 11–12 senior.
      "pro" is reserved for professional courses (CA etc.) and is used when the profile has a course.
      The choice is saved in localStorage sv_ux as look: 'auto' | 'kids' | 'junior' | 'teen' | 'senior'.
   2. Ask Gappu button (#askFab, made by js/ask.js): turns compact once the page is scrolled, and steps
      out of the way (fades out, cannot be tapped) whenever a button, answer or input is underneath it.
      It never hides while it has keyboard focus. */
(function () {
  const D = document, R = D.documentElement;
  const BANDS = [['auto', 'Auto'], ['kids', 'Kids'], ['junior', 'Junior'], ['teen', 'Teen'], ['senior', 'Senior']];
  const BG = { kids: '#0f1b3d', junior: '#13244c', teen: '#0b1022', senior: '#0f1216', pro: '#14171c' };
  const U = () => (window.UX && UX.state) || {};
  const prof = () => (typeof ST !== 'undefined' && ST && ST.profile) || null;

  function autoBand() {
    const p = prof(); if (!p) return 'kids';
    if (p.course) return 'pro';
    const g = +p.grade || 1;
    return g <= 3 ? 'kids' : g <= 7 ? 'junior' : g <= 10 ? 'teen' : 'senior';
  }
  function band() { const l = U().look; return l && l !== 'auto' && BG[l] ? l : autoBand(); }
  function apply() {
    const b = band(); if (R.dataset.age !== b) R.dataset.age = b;
    R.dataset.look = U().look && U().look !== 'auto' ? 'fixed' : 'auto';
    const m = D.querySelector('meta[name=theme-color]'); if (m && BG[b]) m.setAttribute('content', BG[b]);
  }
  function setLook(l) { const u = U(); u.look = l; if (window.UX && UX.save) UX.save(); apply(); paintLook(); }
  apply();

  /* keep the band in step with the grade, whichever path changes it */
  if (typeof window.show === 'function') { const _show = window.show; window.show = function () { const r = _show.apply(this, arguments); apply(); return r; }; }
  if (typeof window.setGrade === 'function') { const _sg = window.setGrade; window.setGrade = function () { const r = _sg.apply(this, arguments); apply(); return r; }; }

  /* ---------- "Look" choice in the Aa settings sheet ---------- */
  function paintLook() {
    const box = D.getElementById('uxLook'); if (!box) return;
    const cur = U().look && U().look !== 'auto' ? U().look : 'auto';
    box.querySelectorAll('button[data-look]').forEach(b => { const on = b.dataset.look === cur; b.classList.toggle('on', on); b.setAttribute('aria-checked', String(on)); b.tabIndex = on ? 0 : -1; });
    const d = D.getElementById('uxLookD'); if (d) d.textContent = cur === 'auto' ? `Auto: the look grows up with you. Now: ${band()[0].toUpperCase() + band().slice(1)}.` : 'Fixed look. Pick Auto to let it change with your grade.';
  }
  function addLook() {
    const s = D.getElementById('uxSheet'); if (!s || D.getElementById('uxLook')) return;
    const prev = s.querySelector('#uxPrev, .ux-prev'); if (!prev) return;
    prev.insertAdjacentHTML('afterend', `<h3 style="margin-top:14px" id="uxLookH">Look</h3><p class="sub" id="uxLookD"></p>
      <div class="ux-sizes ux-look" id="uxLook" role="radiogroup" aria-labelledby="uxLookH" aria-describedby="uxLookD">${BANDS.map(([k, n]) => `<button role="radio" data-look="${k}"><small>${n}</small></button>`).join('')}</div>`);
    s.querySelectorAll('#uxLook button').forEach(b => b.onclick = () => { setLook(b.dataset.look); try { sfx('tap'); } catch (e) {} });
  }
  function hookSettings() {
    if (!window.UX || UX.settings._look) return false;
    const _set = UX.settings;
    UX.settings = function () { const r = _set.apply(this, arguments); addLook(); paintLook(); return r; };
    UX.settings._look = true;
    return true;
  }
  hookSettings();
  /* the header Aa button calls ux.js's own settings() directly, so also catch that tap */
  D.addEventListener('click', e => { if (e.target.closest && e.target.closest('#uxBtn')) setTimeout(() => { addLook(); paintLook(); }, 0); }, true);

  /* ---------- Ask Gappu button ---------- */
  const HIT = 'button,a[href],input,select,textarea,label,[role=button],[role=radio],[role=switch],[role=tab],.opt';
  let raf = 0;
  function fab() { return D.getElementById('askFab'); }
  function covering(f) {
    if (D.activeElement === f) return false;
    const r = f.getBoundingClientRect(); if (!r.width) return false;
    const pad = 6, xs = [r.left - pad, r.left + r.width / 2, r.right + pad], ys = [r.top - pad, r.top + r.height / 2, r.bottom + pad];
    for (const x of xs) for (const y of ys) {
      if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) continue;
      for (const el of D.elementsFromPoint(x, y)) {
        if (el === f || f.contains(el)) continue;
        if (el.closest('svg') || el.closest('.sheet,.asksheet')) break;
        const hit = el.closest(HIT);
        if (hit && !hit.disabled && hit.getAttribute('aria-hidden') !== 'true') return true;
        if (el.matches('main,body,html,.app')) break;
      }
    }
    return false;
  }
  function tick() {
    raf = 0; const f = fab(); if (!f) return;
    const nav = D.querySelector('nav'), nr = nav && nav.style.display !== 'none' ? nav.getBoundingClientRect() : null;
    R.style.setProperty('--fab-b', (nr && nr.height ? Math.round(innerHeight - nr.top + 10) : 16) + 'px');
    const sc = window.scrollY || D.documentElement.scrollTop || 0;
    f.classList.toggle('sv-mini', sc > 40);
    f.classList.toggle('sv-away', covering(f));
  }
  const soon = () => { if (!raf) raf = requestAnimationFrame(tick); };
  addEventListener('scroll', soon, { passive: true, capture: true });
  addEventListener('resize', soon);
  D.addEventListener('touchstart', e => { const f = fab(); if (f && e.target.closest && e.target.closest('#askFab')) { f.classList.add('sv-touch'); clearTimeout(f._t); f._t = setTimeout(() => f.classList.remove('sv-touch'), 1500); } }, { passive: true });
  let mt = 0; const mo = new MutationObserver(() => { clearTimeout(mt); mt = setTimeout(soon, 120); });
  const boot = () => { mo.observe(D.querySelector('main') || D.body, { childList: true, subtree: true }); hookSettings(); apply(); soon(); };
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
  setInterval(soon, 900);          /* catches the button appearing and content that moves without DOM changes */

  /* ---------- header: hide the StudyVerse name whenever the header would not fit (any text size, any width) ---------- */
  function fitHeader() {
    const h = D.querySelector('header'); if (!h) return;
    R.classList.remove('sv-hdr-tight');
    if (h.scrollWidth > h.clientWidth + 1) R.classList.add('sv-hdr-tight');
  }
  new MutationObserver(fitHeader).observe(R, { attributes: true, attributeFilter: ['style', 'data-ts', 'data-age'] });
  addEventListener('resize', fitHeader);
  fitHeader(); setTimeout(fitHeader, 1200);       /* again once web fonts have loaded */
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(fitHeader);

  window.Look = { apply, band, autoBand, set: setLook };
})();
