/* Course switcher — a swipeable strip at the top of every main page for students enrolled in more than one course
   (School · JEE · CA). Tap a course (or swipe the strip) and the same tab reloads for that course: World becomes the
   JEE home or the CA Journey, Practice becomes that course's practice hub, and so on — so no extra filters are needed. */
(function () {
  const D = document;
  const tap = k => { try { sfx(k || 'tap'); } catch (e) {} };
  const parent = () => { try { return !!(window.Cloud && Cloud.isParent && Cloud.isParent()); } catch (e) { return false; } };
  const LV = { foundation: 'Foundation', inter: 'Intermediate', final: 'Final' };
  function list() {
    const p = ST.profile; if (!p || parent()) return [];
    const out = [], j = ST.jee || {};
    if (p.grade) out.push({ k: 'school', e: '🏫', n: 'School', s: '', b: 0 });
    let hasJ = false; try { hasJ = !!(j.track && window.Jee && (Jee.has ? Jee.has() : true)); } catch (e) {}
    if (hasJ) out.push({ k: 'jee', e: '🎯', n: 'JEE', s: '', b: (j.mist || []).length });
    if (ST.ca && ST.ca.level && window.Ca) out.push({ k: 'ca', e: '📊', n: 'CA', s: '', b: Object.keys(ST.ca.revise || {}).length });
    return out;
  }
  function cur() {
    if (ST.profile && ST.profile.course === 'ca') return 'ca';
    try { if (window.Jee && Jee.active && Jee.active()) return 'jee'; } catch (e) {}
    return 'school';
  }
  function go(k) {
    if (k === cur()) return;
    const p = ST.profile; if (!p) return;
    if (k === 'ca') p.course = 'ca';
    else { p.course = null; if (ST.jee) ST.jee.home = k === 'jee'; }
    save(); try { if (window.Look) Look.apply(); } catch (e) {}
    if (k !== 'ca') D.querySelectorAll('nav button[data-s]').forEach(b => { if (b.dataset.caOrig) b.innerHTML = b.dataset.caOrig; });   // CA renames the tabs (Journey, Group…) — undo when leaving CA
    const c = list().find(x => x.k === k); if (c) toast(`${c.e} ${c.n} — everything below is for this course now`);
    tap('open');
    const on = D.querySelector('nav button.on[data-s]');
    if (on && on.dataset.s !== 'world') on.click(); else worldScreen();
  }
  let BAR = null, LASTK = null;
  function paint() {
    let bar = BAR;
    const L = list(), scr = D.querySelector('main > .screen.active');
    const skip = !scr || L.length < 2 || /^s-(topic|onboard)$/.test(scr.id) || scr.querySelector('.jx-q, .ca-opts, .qnav, .tst-nav');
    if (skip) { if (bar && bar.parentElement) bar.remove(); return; }
    const k = cur(), sig = L.map(c => c.k + c.n + c.s + c.b).join('|') + '#' + k;
    if (!bar) { bar = BAR = D.createElement('div'); bar.id = 'cbar'; bar.className = 'cbar'; bar.setAttribute('role', 'tablist'); bar.setAttribute('aria-label', 'Your courses'); wire(bar); }
    if (bar.dataset.sig !== sig) {
      bar.dataset.sig = sig;
      bar.innerHTML = `<div class="cbar-row">${L.map(c => `<button type="button" role="tab" class="cbar-b${c.k === k ? ' on' : ''}" aria-selected="${c.k === k}" data-k="${c.k}"><span class="cbar-e" aria-hidden="true">${c.e}</span><b class="cbar-t">${esc(c.n)}</b>${c.b && c.k !== k ? `<i class="cbar-n" aria-label="${c.b} to fix">${c.b > 99 ? '99+' : c.b}</i>` : ''}</button>`).join('')}<span class="cbar-ind" aria-hidden="true"></span></div>`;
      bar.querySelectorAll('[data-k]').forEach(b => b.onclick = () => go(b.dataset.k));
    }
    const moved = bar.parentElement !== scr || scr.firstElementChild !== bar;
    if (moved) scr.prepend(bar);
    const anim = LASTK !== null && LASTK !== k; LASTK = k;   // glide only when the course really changed — never on ordinary taps
    if (moved || anim || bar.dataset.placed !== k) { bar.dataset.placed = k; slide(bar, anim); }
  }
  function slide(bar, anim) {   // the sliding highlight under the active course
    const on = bar.querySelector('.cbar-b.on'), ind = bar.querySelector('.cbar-ind'); if (!on || !ind) return;
    if (!on.offsetWidth) return requestAnimationFrame(() => slide(bar, anim));
    ind.style.transition = anim ? '' : 'none';
    ind.style.width = on.offsetWidth + 'px'; ind.style.transform = `translateX(${on.offsetLeft}px)`;
    const row = bar.querySelector('.cbar-row'); if (row && (on.offsetLeft < row.scrollLeft || on.offsetLeft + on.offsetWidth > row.scrollLeft + row.clientWidth)) row.scrollTo({ left: on.offsetLeft - 12, behavior: 'smooth' });
    if (!anim) { void ind.offsetWidth; requestAnimationFrame(() => { ind.style.transition = ''; }); }
  }
  function wire(bar) {   // swipe the strip left / right to move to the next / previous course
    let x0 = null, y0 = 0, t0 = 0;
    bar.addEventListener('touchstart', e => { const t = e.touches[0]; x0 = t.clientX; y0 = t.clientY; t0 = Date.now(); }, { passive: true });
    bar.addEventListener('touchend', e => {
      if (x0 === null) return; const t = e.changedTouches[0], dx = t.clientX - x0, dy = t.clientY - y0; x0 = null;
      const row = bar.querySelector('.cbar-row'); if (row && row.scrollWidth > row.clientWidth + 4) return;   // the row itself scrolls — leave it alone
      if (Math.abs(dx) < 50 || Math.abs(dy) > Math.abs(dx) || Date.now() - t0 > 600) return;
      const L = list(), i = L.findIndex(c => c.k === cur()), n = L[(i + (dx < 0 ? 1 : -1) + L.length) % L.length]; if (n) go(n.k);
    }, { passive: true });
  }
  let pend = 0; const kick = () => { if (!pend) pend = requestAnimationFrame(() => { pend = 0; try { paint(); } catch (e) {} }); };
  const start = () => { const m = D.querySelector('main'); if (m) new MutationObserver(kick).observe(m, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] }); kick(); };
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', start); else start();
  window.addEventListener('resize', () => { if (BAR && BAR.isConnected) slide(BAR, false); });
  window.CourseBar = { list, cur, go, paint };
})();
