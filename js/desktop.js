/* ================= Desktop & tablet experience (pairs with css/desktop.css) =================
   Phones (< 768px) are never touched: nothing below runs its DOM changes unless the window is at least 768px wide,
   and everything is undone when the window gets narrow again.
   • Sidebar (#dskSide): the existing <header> (⭐/🔥 chips) and the bottom <nav> are MOVED into it (same elements, same
     handlers), plus quick links (Play, Puzzles, Story, Exam plan) and Collapse / Focus mode / Keyboard keys.
   • Right rail (#dskRail, ≥1280px, CSS decides): "Today" — goal ring, streak + shields, mystery box, boss of the week,
     exam countdown + today's plan, friends, continue, study timer (just a timer; sessions saved locally), notes while
     learning a topic, a rotating tip/fact strip. Every item opens the existing feature.
   • Screen extras (≥768px): subject cards beside the World map, chapter cards beside a subject map; (≥1024px) a topic preview
     beside the chapter's topic list.
   • Keys: 1–5 / Alt+1–5 tabs (plain digits only when the screen has no numbered choices — js/a11y.js uses digits to
     answer), A–D answer, / search, F focus mode, [ collapse sidebar, K key list. js/a11y.js keeps Enter, Esc, R, H, P.
   • Games, puzzles, live rooms, the boss and topics (below 1536px) hide the Today panel so the playing area gets the room
     (html.dsk-play / html.dsk-norail); css/desktop.css sizes boards and grids by the window height so they fit without scrolling.
   • Below 1280px (no right panel) the World screen shows the same Today cards in a grid under the subjects.
   Local settings only (never synced): localStorage sv_dsk = { side ('open'|'closed', ≥1200), sideN (drawer, <1200), focus,
   notes:{topicId:text}, fm:{day:minutes} }. */
(function () {
  const D = document, R = D.documentElement;
  const MQ = matchMedia('(min-width:768px)'), MQW = matchMedia('(min-width:1024px)'), MQR = matchMedia('(min-width:1280px)');
  const MQX = matchMedia('(min-width:1200px)'), MQT = matchMedia('(min-width:1536px)');   // ≥1200: the open menu pushes the page; below it is a drawer
  const wantDsk = () => { const l = R.dataset.layout || 'auto'; return l !== 'mobile' && MQ.matches; };   // phones never; tablets can choose
  const $1 = (s, r) => (r || D).querySelector(s), $$ = (s, r) => [...(r || D).querySelectorAll(s)];
  const E = s => (typeof esc === 'function' ? esc(String(s == null ? '' : s)) : String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])));
  const st = () => (typeof ST !== 'undefined' ? ST : null);
  const prof = () => (st() && st().profile) || null;
  const isCA = () => { try { return !!(window.Ca && Ca.isCA && Ca.isCA()); } catch (e) { return !!(prof() && prof().course === 'ca'); } };
  const isParent = () => { try { return !!(window.Cloud && Cloud.isParent && Cloud.isParent()); } catch (e) { return false; } };
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches || R.classList.contains('sv-rm');
  const tdy = () => (typeof today === 'function' ? today() : new Date().toISOString().slice(0, 10));
  const tap = k => { try { sfx(k || 'tap'); } catch (e) {} };
  const L = (() => { let o = {}; try { o = JSON.parse(localStorage.getItem('sv_dsk') || '{}') || {}; } catch (e) {} o.notes = o.notes || {}; o.fm = o.fm || {}; return o; })();
  if (L.col && !L.side) { L.side = 'closed'; } delete L.col;      // v58 setting → v59
  const saveL = () => { try { localStorage.setItem('sv_dsk', JSON.stringify(L)); } catch (e) {} };
  const act = () => { const s = $1('.screen.active'); return s ? s.id.slice(2) : ''; };

  /* ================= shell: sidebar + rail ================= */
  let built = false, home = null;
  function build() {
    if (built) return;
    const hdr = $1('header'), nav = $1('nav[aria-label="Main"]') || $1('nav'); if (!hdr || !nav) return;
    built = true;
    home = { hdr: [hdr.parentNode, hdr.nextSibling], nav: [nav.parentNode, nav.nextSibling] };
    const side = D.createElement('aside'); side.id = 'dskSide'; side.setAttribute('aria-label', 'Knowtopia menu');
    side.innerHTML = `<div class="dsk-sh" id="dskNavH">Go to</div><div class="dsk-sh" id="dskQlH">Quick start</div><div class="dsk-ql" id="dskQl" role="group" aria-labelledby="dskQlH"></div>
      <div class="dsk-foot"><button type="button" id="dskKeysB" aria-haspopup="dialog"><span aria-hidden="true">⌨️</span><span class="dsk-l">Keyboard keys</span></button>
      <button type="button" id="dskFocusB" aria-pressed="false"><span aria-hidden="true">🎧</span><span class="dsk-l">Focus mode</span></button></div>`;
    side.prepend(hdr); $1('#dskNavH', side).after(nav);
    const tg = D.createElement('button'); tg.type = 'button'; tg.id = 'dskTgl'; tg.setAttribute('aria-controls', 'dskSide'); tg.className = 'dsk-only';
    hdr.prepend(tg); tg.onclick = () => toggleSide();
    D.body.prepend(side);
    const scrim = D.createElement('div'); scrim.id = 'dskScrim'; scrim.setAttribute('aria-hidden', 'true'); scrim.onclick = () => toggleSide(false); D.body.appendChild(scrim);
    const tip = D.createElement('div'); tip.id = 'dskTip'; tip.setAttribute('role', 'tooltip'); tip.hidden = true; D.body.appendChild(tip);
    wireTips(side);
    side.addEventListener('click', e => { const b = e.target.closest('nav button, .dsk-ql button'); if (b && R.classList.contains('dsk-drawer')) setTimeout(() => toggleSide(false, true), 0); });
    const rail = D.createElement('aside'); rail.id = 'dskRail'; rail.setAttribute('aria-label', 'Today');
    D.body.appendChild(rail);
    const fx = D.createElement('button'); fx.type = 'button'; fx.id = 'dskFocusX'; fx.innerHTML = '<span aria-hidden="true">↩</span> Show menus'; fx.onclick = () => setFocus(false);
    D.body.appendChild(fx);
    const brand = $1('.brand', hdr); if (brand) { brand.setAttribute('role', 'link'); brand.tabIndex = 0; brand.title = 'Home'; brand.onclick = goHome; brand.onkeydown = e => { if (e.key === 'Enter') goHome(); }; }
    $1('#dskKeysB').onclick = keysHelp;
    $1('#dskFocusB').onclick = () => setFocus(!R.classList.contains('dsk-focus'));
    R.classList.add('dsk'); applyCol(); setFocus(!!L.focus, true);
    labelNav(); quick(); obState(); refresh(); enhance();
  }
  function unbuild() {
    if (!built) return; built = false;
    const hdr = $1('#dskSide header'), nav = $1('#dskSide nav');
    if (hdr && home) home.hdr[0].insertBefore(hdr, home.hdr[1] && home.hdr[1].parentNode === home.hdr[0] ? home.hdr[1] : home.hdr[0].firstChild);
    if (nav && home) home.nav[0].insertBefore(nav, home.nav[1] && home.nav[1].parentNode === home.nav[0] ? home.nav[1] : null);
    ['#dskSide', '#dskRail', '#dskFocusX', '#dskScrim', '#dskTip', '#dskTgl', '#dskToday'].forEach(s => { const e = $1(s); if (e) e.remove(); });
    unwrapChapter(); $$('.dsk-pzside').forEach(unwrapPz); $$('.dsk-only').forEach(e => e.remove());
    $$('nav button[aria-keyshortcuts]').forEach(e => e.removeAttribute('aria-keyshortcuts'));
    R.classList.remove('dsk', 'dsk-col', 'dsk-focus', 'dsk-ob', 'dsk-drawer', 'dsk-play', 'dsk-norail', 'dsk-wide');
    const b = $1('.brand'); if (b) { b.removeAttribute('role'); b.removeAttribute('tabindex'); b.removeAttribute('title'); b.onclick = null; b.onkeydown = null; }
  }
  /* The menu: ☰ opens it, « closes it, at every width ≥768. Wide (≥1200): the open menu pushes the page (choice remembered, open by
     default). Narrower: the menu is a slim icon bar and opens as a drawer over the page (choice remembered; it closes again after you
     pick a place, with Esc or a tap outside). Collapsed icons show their name in a tooltip. */
  const sideOpen = () => (MQX.matches ? L.side !== 'closed' : L.sideN === 'open');
  function toggleSide(on, quiet) {
    const open = on == null ? !sideOpen() : !!on;
    if (MQX.matches) L.side = open ? 'open' : 'closed'; else L.sideN = open ? 'open' : 'closed';
    saveL(); applyCol(); if (!quiet) tap('tap');
    if (open && !MQX.matches) { const f = $1('#dskSide nav button.on') || $1('#dskSide nav button'); if (f && !quiet) f.focus({ preventScroll: true }); }
    else if (!open && !quiet) { const t = $1('#dskTgl'); if (t) t.focus({ preventScroll: true }); }
  }
  function applyCol() {
    const open = sideOpen(), wide = MQX.matches;
    R.classList.toggle('dsk-wide', wide);
    R.classList.toggle('dsk-col', !(wide && open));          // page layout: slim icon bar
    R.classList.toggle('dsk-drawer', !wide && open);        // drawer over the page
    const side = $1('#dskSide'); if (side) side.classList.toggle('open', open);
    const b = $1('#dskTgl');
    if (b) { b.setAttribute('aria-expanded', String(open)); b.innerHTML = `<span aria-hidden="true">${open ? '«' : '☰'}</span>`;
      b.setAttribute('aria-label', open ? 'Close the menu' : 'Open the menu'); b.dataset.tip = open ? 'Close menu  [' : 'Open menu  ['; }
    hideTip();
  }
  /* tooltips for the icon bar (a real element, so the scrolling menu cannot clip it) */
  let tipT = 0;
  const tipText = x => { if (x.dataset.tip) return x.dataset.tip; const l = x.querySelector('.dsk-l'); if (l) return l.textContent.trim();
    const own = [...x.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();   // nav tab: "<b>🦁</b>Squad"
    return (own || x.getAttribute('aria-label') || x.title || x.textContent).replace(/\s+/g, ' ').trim(); };
  function showTip(x) {
    const tip = $1('#dskTip'); if (!tip || !x) return;
    if ($1('#dskSide').classList.contains('open')) return hideTip();   // labels are showing
    const t = tipText(x); if (!t) return hideTip();
    tip.textContent = t; tip.hidden = false; const r = x.getBoundingClientRect();
    tip.style.left = Math.round(r.right + 10) + 'px'; tip.style.top = Math.round(r.top + r.height / 2) + 'px';
  }
  function hideTip() { clearTimeout(tipT); const t = $1('#dskTip'); if (t) t.hidden = true; }
  function wireTips(side) {
    side.addEventListener('mouseover', e => { const x = e.target.closest('button, .brand'); clearTimeout(tipT); if (x) tipT = setTimeout(() => showTip(x), 250); else hideTip(); });
    side.addEventListener('mouseleave', hideTip);
    side.addEventListener('focusin', e => { const x = e.target.closest('button'); if (x && x.matches(':focus-visible')) showTip(x); });
    side.addEventListener('focusout', hideTip);
    side.addEventListener('scroll', hideTip, { passive: true });
  }
  function setFocus(on, silent) {
    L.focus = !!on; saveL(); R.classList.toggle('dsk-focus', !!on);
    const b = $1('#dskFocusB'); if (b) b.setAttribute('aria-pressed', String(!!on));
    if (!silent) { tap('tap'); try { toast(on ? '🎧 Focus mode: menus hidden. Press F to bring them back' : 'Menus are back'); } catch (e) {} }
    if (!on) { const fb = $1('#dskFocusB'); if (fb && !silent) fb.focus({ preventScroll: true }); }
  }
  /* parents, onboarding, the CA setup: no student sidebar */
  function obState() { R.classList.toggle('dsk-ob', !prof() || act() === 'onboard' || isParent()); }
  function labelNav() {          /* the small key numbers are drawn by CSS counters; here only the shortcut hint for screen readers */
    let n = 0; $$('#dskSide nav button[data-s]').forEach(b => { if (b.hidden) { b.removeAttribute('aria-keyshortcuts'); return; } n++; const v = `Alt+${n}`; if (b.getAttribute('aria-keyshortcuts') !== v) b.setAttribute('aria-keyshortcuts', v); });
  }
  function navButtons() { return $$('nav button[data-s]').filter(b => !b.hidden && b.offsetParent !== null); }
  function goHome() { tap('tap'); try { if (isCA() && window.Ca) Ca.home(); else worldScreen(); } catch (e) {} }

  /* quick links (one row each, existing features only) */
  function quick() {
    const box = $1('#dskQl'); if (!box) return;
    const ca = isCA(), items = [];
    items.push(['🎮', 'Play games', () => window.PlayHub && PlayHub.open()]);
    if (!ca) items.push(['🧩', 'Puzzles', () => window.Puzzles && Puzzles.hub({ from: 'play' })]);
    if (ca && window.CaTools) { items.push(['🎙️', 'Viva practice', () => CaTools.vivaHub && CaTools.vivaHub()]); items.push(['🏆', 'Mock papers', () => CaTools.mocks && CaTools.mocks()]); }
    if (!ca && window.Story) items.push(['📖', 'Story mode', openStory]);
    if (window.ExamPlan) items.push(['📅', 'Exam plan', () => ExamPlan.openPlan()]);
    const sig = items.map(i => i[1]).join('|'); if (box.dataset.sig === sig) return; box.dataset.sig = sig;
    box.innerHTML = items.map((it, i) => `<button type="button" data-i="${i}"><span aria-hidden="true">${it[0]}</span><span class="dsk-l">${E(it[1])}</span></button>`).join('');
    $$('button', box).forEach(b => b.onclick = () => { tap('open'); try { items[+b.dataset.i][2](); } catch (e) {} });
    applyCol();
  }
  async function openStory() {
    const n = typeof NAV !== 'undefined' && NAV || {};
    if (n.subject && n.chapter != null) return Story.open(n.subject, n.chapter);
    const c = await continueInfo(); if (c && c.sid) return Story.open(c.sid, c.ci);
    try { toast('Open a chapter first, then tap 📖 Story'); } catch (e) {} worldScreen();
  }

  /* ================= "continue where you left off" ================= */
  async function continueInfo() {
    const s = st(); if (!s || !prof()) return null;
    if (isCA()) { const u = s.ca && s.ca.last; return u ? { ca: true, uid: u } : null; }
    const g = prof().grade, ts = Object.entries(s.topics || {}).filter(([k]) => k.startsWith(`g${g}-`)).sort((a, b) => String(b[1].last || '').localeCompare(String(a[1].last || '')));
    if (!ts.length) { const sub = (typeof curSubjects === 'function' ? curSubjects(g) : [])[0]; if (!sub) return null; const d = await subjectData(g, sub.id); if (!d || !d.chapters[0]) return null;
      return { sid: sub.id, ci: 0, ti: 0, t: d.chapters[0].topics[0], c: d.chapters[0], sname: sub.name, fresh: true }; }
    const m = /^g\d+-([a-z0-9]+)-/.exec(ts[0][0]); if (!m) return null;
    const sid = m[1], d = await subjectData(g, sid); if (!d) return null;
    for (let ci = 0; ci < d.chapters.length; ci++) { const ti = d.chapters[ci].topics.findIndex(t => t.id === ts[0][0]); if (ti < 0) continue;
      const c = d.chapters[ci]; let nci = ci, nti = ti + 1;
      if (nti >= c.topics.length) { const j = c.topics.findIndex(t => !topicStars(t.id)); if (j >= 0) nti = j; else if (ci + 1 < d.chapters.length) { nci = ci + 1; nti = 0; } else nti = ti; }
      const sub = curSubjects(g).find(x => x.id === sid);
      return { sid, ci: nci, ti: nti, t: d.chapters[nci].topics[nti], c: d.chapters[nci], sname: sub ? sub.name : sid };
    }
    return null;
  }

  /* ================= right rail ================= */
  let rT = 0, railBusy = false, railAgain = false;
  function refresh() { clearTimeout(rT); rT = setTimeout(paintRail, 250); }
  const ring = (p, sz = 64, label = '') => { const r = sz / 2 - 6, c = 2 * Math.PI * r, v = Math.max(0, Math.min(1, p));
    return `<svg class="dsk-ring" width="${sz}" height="${sz}" viewBox="0 0 ${sz} ${sz}" role="img" aria-label="${E(label)}"><circle class="bg" cx="${sz / 2}" cy="${sz / 2}" r="${r}"/><circle class="fg" cx="${sz / 2}" cy="${sz / 2}" r="${r}" stroke-dasharray="${c.toFixed(1)}" stroke-dashoffset="${(c * (1 - v)).toFixed(1)}" transform="rotate(-90 ${sz / 2} ${sz / 2})"/><text x="50%" y="54%" text-anchor="middle" dominant-baseline="middle">${Math.round(v * 100)}%</text></svg>`; };
  function squadData() {
    try { const h = window.Squad && Squad._data && Squad._data(); if (h && h.me) return h; } catch (e) {}
    try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (!/squad/i.test(k)) continue; const v = JSON.parse(localStorage.getItem(k) || 'null'); if (v && v.d && v.d.me) return v.d; } } catch (e) {}
    return null;
  }
  async function paintRail() {
    const rail = $1('#dskRail'); if (!rail || !prof() || isParent()) return;
    const inline = !MQR.matches;
    if (inline && (act() !== 'world' || isCA())) { const t = $1('#dskToday'); if (t) t.remove(); return; }
    if (!inline) { const t = $1('#dskToday'); if (t) t.remove(); }
    if (railBusy) { railAgain = true; return; } railBusy = true;
    try {
      const s = st(), p = prof(), ca = isCA(), out = [];
      const dt = new Date(), h = dt.getHours();
      out.push(`<div class="dsk-rh"><div><b>${h < 12 ? 'Good morning' : h < 17 ? 'Good afternoon' : 'Good evening'}</b><small>${E(dt.toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'short' }))}</small></div><button type="button" class="dsk-rx" id="dskRailX" aria-label="Hide the Today panel (focus mode)" title="Focus mode (F)">🎧</button></div>`);
      /* notes while learning a topic (school) */
      if (!ca && act() === 'topic' && typeof RUN !== 'undefined' && RUN && RUN.t) {
        const tid = RUN.t.id;
        out.push(`<div class="dsk-rc dsk-notes"><h3><span aria-hidden="true">📝</span> My notes <small style="margin-left:auto">saved on this computer</small></h3><label class="sr-only" for="dskNote">My notes for ${E(RUN.t.title)}</label><textarea id="dskNote" data-t="${E(tid)}" placeholder="Write what you learn here, in your own words…">${E(L.notes[tid] || '')}</textarea></div>`);
      }
      /* goal + streak */
      const G = (window.Garden && Garden.GOAL) || 50, xp = window.Garden && Garden.dailyXP ? Garden.dailyXP() : ((s.daily && s.daily.d === tdy() && s.daily.xp) || 0);
      const stk = typeof liveStreak === 'function' ? liveStreak() : 0, sh = (s.rw && +s.rw.sh) || 0;
      out.push(`<button type="button" class="dsk-rc" data-go="goal"><h3><span aria-hidden="true">🎯</span> Today's goal<span class="dsk-go" aria-hidden="true">›</span></h3><div class="dsk-row">${ring(xp / G, 64, `${Math.min(xp, G)} of ${G} stars today`)}
        <div><div class="dsk-big">${Math.min(xp, G)} / ${G} ⭐</div><p>${xp >= G ? 'Goal reached! 🎉 Streak safe.' : `${G - xp} more stars to keep your streak.`}</p><div class="dsk-chipr"><span>🔥 ${stk}-day streak</span>${sh ? `<span>${'🛡️'.repeat(Math.min(sh, 3))} shield${sh > 1 ? 's' : ''}</span>` : ''}</div></div></div></button>`);
      /* mystery box */
      try { if (window.Rewards && Rewards.boxWaiting && Rewards.boxWaiting()) out.push(`<button type="button" class="dsk-rc dsk-box" data-go="box"><div class="dsk-row"><span class="dsk-gift" aria-hidden="true">🎁</span><div><div class="dsk-big">Mystery box waiting!</div><p style="color:#5a4300">You reached today's goal. Open your surprise.</p></div></div></button>`); } catch (e) {}
      /* boss of the week */
      try { if (window.Rewards && Rewards.boss) { const b = Rewards.boss(), need = Rewards._need ? Rewards._need((b.qids && b.qids.length) || 10) : 7, left = Math.max(0, 3 - (b.tries || 0)), hp = b.beaten ? 0 : Math.max(0, need - (b.best || 0));
        out.push(`<button type="button" class="dsk-rc" data-go="boss"><h3><span aria-hidden="true">${ca ? '📒' : '👾'}</span> Boss of the week<span class="dsk-go" aria-hidden="true">›</span></h3>${b.beaten ? '<p>Beaten this week! 🏆 A new boss comes on Monday.</p>' : `<div class="dsk-hp" role="progressbar" aria-label="Boss health" aria-valuemin="0" aria-valuemax="${need}" aria-valuenow="${hp}"><i style="width:${hp / need * 100}%"></i></div><p>Health ${hp} / ${need} · ${left ? `${left} ${left === 1 ? 'try' : 'tries'} left` : 'no tries left this week'}</p>`}</button>`); } } catch (e) {}
      /* exam countdown + today's plan */
      try { if (window.ExamPlan) { const sp = ExamPlan.cur();
        if (sp && sp.date) { const dl = ExamPlan.daysTo(sp.date), items = sp.day && sp.day.d === tdy() ? sp.day.items || [] : [];
          out.push(`<button type="button" class="dsk-rc" data-go="exam"><h3><span aria-hidden="true">📅</span> Exam plan<span class="dsk-go" aria-hidden="true">›</span></h3><div class="dsk-row"><div class="dsk-days">${Math.max(0, dl)}<small>${dl === 1 ? 'day' : 'days'}</small></div><div><p>${dl < 0 ? 'Exam day has passed. Set your next exam.' : dl === 0 ? 'Exam day! You are ready. 💪' : 'until your exam'}</p></div></div>
            ${items.length ? `<ul class="dsk-tasks" aria-label="Today's plan">${items.slice(0, 3).map(t => { const dn = !!(sp.done && sp.done[t.id]) || !!t.done; return `<li class="${dn ? 'done' : ''}"><i aria-hidden="true">${dn ? '✓' : ''}</i><span>${E(t.title)}</span></li>`; }).join('')}</ul>` : `<p style="margin-top:6px">Open the plan to see today's tasks.</p>`}</button>`);
        } else out.push(`<button type="button" class="dsk-rc" data-go="exam"><h3><span aria-hidden="true">📅</span> Exam coming up?<span class="dsk-go" aria-hidden="true">›</span></h3><p>Set the date and get a small plan for every day.</p></button>`);
      } } catch (e) {}
      /* continue */
      const cont = await continueInfo();
      if (cont && cont.ca) out.push(`<button type="button" class="dsk-rc" data-go="cont"><h3><span aria-hidden="true">▶️</span> Continue where you left off</h3><p>Open your last unit and keep going.</p></button>`);
      else if (cont && cont.t) out.push(`<button type="button" class="dsk-rc" data-go="cont"><h3><span aria-hidden="true">▶️</span> ${cont.fresh ? 'Start your first quest' : 'Continue where you left off'}</h3><div class="dsk-big" style="font-size:16px">${E(cont.t.title)}</div><p>${E(cont.sname)} · Ch ${E(cont.c.n)} · ${E(cont.c.title)}</p></button>`);
      /* friends */
      const H = squadData();
      if (H && H.me) {
        const fr = (H.friends || []).slice(), me = Object.assign({}, H.me, { me: true, name: (p.name || 'You') });
        const top = fr.concat([me]).sort((a, b) => (+b.week || 0) - (+a.week || 0)).slice(0, 3);
        let nd = []; try { nd = (Squad._nudges && Squad._nudges()) || []; } catch (e) {}
        out.push(`<button type="button" class="dsk-rc" data-go="squad"><h3><span aria-hidden="true">${ca ? '👥' : '🦁'}</span> ${ca ? 'Group' : 'Friends'} this week<span class="dsk-go" aria-hidden="true">›</span></h3>
          ${fr.length ? `<ol class="dsk-fr">${top.map((f, i) => `<li class="${f.me ? 'me' : ''}"><span class="r">${i + 1}</span><span class="a" aria-hidden="true">${E(f.avatar || '🙂')}</span><span>${E(f.me ? 'You' : f.name)}</span><span class="w">${typeof kfmt === 'function' ? kfmt(f.week || 0) : (f.week || 0)} ⭐</span></li>`).join('')}</ol>` : '<p>Add a friend with their code and race each other every week.</p>'}
          ${nd[0] ? `<div class="dsk-nudge">🔔 ${E(nd[0].t)}</div>` : ''}</button>`);
      } else out.push(`<button type="button" class="dsk-rc" data-go="squad"><h3><span aria-hidden="true">${ca ? '👥' : '🦁'}</span> ${ca ? 'Study group' : 'Squad'}<span class="dsk-go" aria-hidden="true">›</span></h3><p>See your league, friends and cheers.</p></button>`);
      /* study timer */
      out.push(timerHTML());
      /* tip / fact strip */
      out.push(`<div class="dsk-rc dsk-mot" aria-live="off"><span class="dsk-k2" id="dskMotK"></span><p id="dskMotT"></p></div>`);
      const keep = D.activeElement && rail.contains(D.activeElement) ? D.activeElement.id || (D.activeElement.dataset && D.activeElement.dataset.go) : null;
      if (keep === 'dskNote') { /* never re-render while typing notes */ railBusy = false; return; }
      if (inline) { paintToday(out.filter(x => !/class="dsk-rh"|dsk-notes|id="dskTimer"|dsk-mot/.test(x)), dt); return; }
      rail.innerHTML = out.join('');
      if (!rail.dataset.done) { rail.dataset.done = 1; rail.classList.add('dsk-first'); setTimeout(() => rail.classList.remove('dsk-first'), 900); }
      wireRail(rail); mot(true); paintTimer();
      if (keep) { const k = $1('#' + keep, rail) || $1(`[data-go="${keep}"]`, rail); if (k) k.focus({ preventScroll: true }); }
    } catch (e) { /* rail is optional */ }
    finally { railBusy = false; if (railAgain) { railAgain = false; refresh(); } }
  }
  /* below 1280px: the Today cards sit in the World screen, under the subject cards */
  function paintToday(cards, dt) {
    const scr = $1('#s-world'); if (!scr || !scr.classList.contains('active')) return;
    let el = $1('#dskToday');
    if (!el) { el = D.createElement('section'); el.id = 'dskToday'; el.className = 'dsk-today dsk-only'; el.setAttribute('aria-labelledby', 'dskTodayH'); }
    const anchor = $1(':scope > #dskSubj', scr) || $1(':scope > .hud', scr);
    if (anchor && el.previousElementSibling !== anchor) anchor.after(el); else if (!anchor && !el.isConnected) scr.appendChild(el);
    const html = `<h2 id="dskTodayH">Today <small>${E(dt.toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'short' }))}</small></h2><div class="dsk-tgrid">${cards.join('')}</div>`;
    if (el.dataset.h !== html) { el.dataset.h = html; el.innerHTML = html; wireRail(el); }
  }
  function wireRail(rail) {
    const rx = $1('#dskRailX', rail); if (rx) rx.onclick = () => setFocus(true);
    $$('[data-go]', rail).forEach(b => b.onclick = async () => {
      tap('open'); const k = b.dataset.go;
      try {
        if (k === 'goal' || k === 'box') practiceScreen();
        else if (k === 'boss') { await practiceScreen(); setTimeout(() => { const x = $1('#rwBoss'); if (x) { x.scrollIntoView({ block: 'center', behavior: reduced() ? 'auto' : 'smooth' }); const g = $1('#rwBossGo') || x; g.focus({ preventScroll: true }); } }, 400); }
        else if (k === 'exam') ExamPlan.openPlan();
        else if (k === 'squad') squadScreen();
        else if (k === 'cont') { const c = await continueInfo(); if (!c) return; if (c.ca) Ca.unit(c.uid); else playTopic(c.sid, c.ci, c.ti); }
      } catch (e) {}
    });
    const n = $1('#dskNote', rail);
    if (n) { let t; n.oninput = () => { clearTimeout(t); t = setTimeout(() => { const v = n.value; if (v.trim()) L.notes[n.dataset.t] = v.slice(0, 5000); else delete L.notes[n.dataset.t]; saveL(); }, 400); }; }
    wireTimer(rail);
  }

  /* ---------- tips & facts (checked, simple, original wording) ---------- */
  const TIPS = ['Small steps every day beat one huge push on Sunday.', 'Mistakes are how your brain learns. Fix one today!', 'Explain a topic to someone (or to Gappu). Teaching is the best way to remember.',
    'Read a question twice before you answer it.', 'A short break after 25 minutes helps you remember more.', 'Revise yesterday’s topic for 5 minutes before starting a new one.',
    'Drink some water and sit up straight. Your brain will thank you.', 'Stuck? Draw it. A quick picture often makes it clear.'];
  const FACTS = ['An octopus has three hearts.', 'Light from the Sun takes about 8 minutes to reach Earth.', 'A day on Venus is longer than a year on Venus.',
    'Ice floats because water expands when it freezes.', 'Your heart beats about one lakh times every day.', 'The tiger is India’s national animal.',
    'Some kinds of bamboo can grow almost a metre in a single day.', 'Indian mathematicians were among the first to use zero as a number.'];
  const CA_TIPS = ['Write the journal entry before you think about the ledger.', 'Attempt every MCQ you are sure of first, then come back to the rest.', 'Read the question’s last line first: it tells you what is asked.',
    'Work a past paper with the timer once a week.', 'Revise yesterday’s unit for ten minutes before starting a new one.', 'Show working notes neatly. Marks are given for steps too.'];
  let motI = Math.floor(Math.random() * 100), motT = 0;
  function mot(now) {
    const k = $1('#dskMotK'), t = $1('#dskMotT'); if (!k || !t) return;
    const ca = isCA(), list = ca ? CA_TIPS.map(x => ['💡 Study tip', x]) : [].concat(...TIPS.map((x, i) => [['💡 Study tip', x], ['🌍 Did you know?', FACTS[i % FACTS.length]]]));
    const it = list[motI % list.length];
    const put = () => { k.textContent = it[0]; t.textContent = it[1]; t.style.opacity = 1; };
    if (now || reduced()) put(); else { t.style.opacity = 0; setTimeout(put, 400); }
    clearInterval(motT); motT = setInterval(() => { if (D.hidden || !$1('#dskMotT')) return; motI++; mot(false); }, 14000);
  }

  /* ---------- study timer (Pomodoro-style; awards nothing, saves minutes locally) ---------- */
  const TM = { len: 25, left: 25 * 60, run: false, end: 0, brk: false, t: 0 };
  function timerHTML() {
    const mins = Math.round(L.fm[tdy()] || 0);
    return `<div class="dsk-rc" id="dskTimer" role="group" aria-labelledby="dskTmH"><h3 id="dskTmH"><span aria-hidden="true">⏱️</span> Study timer<small style="margin-left:auto" id="dskTmM">${mins ? `${mins} min today` : ''}</small></h3>
      <div class="dsk-tm"><div class="dsk-tt" id="dskTmT" aria-hidden="true">25:00</div><p id="dskTmS">Focus for ${TM.len} minutes, then rest 5.</p></div>
      <div class="dsk-tb"><button type="button" class="pri" id="dskTmGo">Start</button><button type="button" id="dskTmR">Reset</button>${[15, 25, 45].map(m => `<button type="button" data-m="${m}" aria-pressed="${TM.len === m}" aria-label="${m} minutes">${m}′</button>`).join('')}</div>
      <p class="sr-only" id="dskTmLive" aria-live="polite"></p></div>`;
  }
  const fmtT = s => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
  function paintTimer() {
    const t = $1('#dskTmT'), g = $1('#dskTmGo'), sEl = $1('#dskTmS'); if (!t) return;
    const left = TM.run ? Math.max(0, (TM.end - Date.now()) / 1000) : TM.left;
    t.textContent = fmtT(Math.ceil(left)); if (g) g.textContent = TM.run ? 'Pause' : (TM.left < (TM.brk ? 5 : TM.len) * 60 ? 'Resume' : 'Start');
    if (sEl) sEl.textContent = TM.brk ? 'Break time! Stretch, drink water. 🌿' : TM.run ? 'Focusing… you can do it!' : `Focus for ${TM.len} minutes, then rest 5.`;
    $$('#dskTimer [data-m]').forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.m === TM.len)));
  }
  function tick() {
    if (!TM.run) return;
    const left = (TM.end - Date.now()) / 1000;
    if (left <= 0) {
      TM.run = false; clearInterval(TM.t);
      const live = $1('#dskTmLive');
      if (!TM.brk) { L.fm[tdy()] = (L.fm[tdy()] || 0) + TM.len; saveL(); TM.brk = true; TM.left = 5 * 60;
        tap('unlock'); try { toast(`⏱️ ${TM.len} minutes of focus done! Take a 5-minute break 🌿`); } catch (e) {} if (live) live.textContent = `${TM.len} minutes done. Take a 5 minute break.`;
        const m = $1('#dskTmM'); if (m) m.textContent = `${Math.round(L.fm[tdy()])} min today`; }
      else { TM.brk = false; TM.left = TM.len * 60; tap('tap'); try { toast('Break over. Ready for the next round? 💪'); } catch (e) {} if (live) live.textContent = 'Break over.'; }
    }
    paintTimer();
  }
  function wireTimer(r) {
    const g = $1('#dskTmGo', r); if (!g) return;
    g.onclick = () => { tap('tap'); if (TM.run) { TM.left = Math.max(0, (TM.end - Date.now()) / 1000); TM.run = false; clearInterval(TM.t); } else { TM.end = Date.now() + TM.left * 1000; TM.run = true; clearInterval(TM.t); TM.t = setInterval(tick, 500); } paintTimer(); };
    $1('#dskTmR', r).onclick = () => { TM.run = false; clearInterval(TM.t); TM.brk = false; TM.left = TM.len * 60; paintTimer(); };
    $$('[data-m]', r).forEach(b => b.onclick = () => { if (TM.run) return; TM.len = +b.dataset.m; TM.brk = false; TM.left = TM.len * 60; paintTimer(); });
    if (TM.run) { clearInterval(TM.t); TM.t = setInterval(tick, 500); }
  }

  /* ================= screen extras (≥768px; topic preview ≥1024px) ================= */
  let eT = 0, enhancing = false;
  function enhance() { clearTimeout(eT); eT = setTimeout(doEnhance, 60); }
  async function doEnhance() {
    if (!built || !wantDsk() || enhancing || !prof()) return; modes(); gridShape(); enhancing = true;
    try {
      const a = act();
      if (a === 'world' && !isCA()) await worldCards();
      if (a === 'subject') await chapterCards();
      if (a === 'chapter' && MQW.matches) await chapterPreview();
    } catch (e) {} finally { enhancing = false; }
  }
  /* puzzle grids: rows × columns as CSS variables, so css/desktop.css can size the grid by the window height */
  function gridShape() {
    $$('#s-puz #pzGrid, #s-live #pzGrid').forEach(g => { const rows = $$(':scope > .pz-row, :scope > [role=row]', g); if (!rows.length) return;
      const dr = rows.length, dc = rows[0].children.length || 1;
      if (g.style.getPropertyValue('--dr') !== String(dr)) g.style.setProperty('--dr', dr);
      if (g.style.getPropertyValue('--dc') !== String(dc)) g.style.setProperty('--dc', dc); });
    /* ≥1024: the grid sits on the left; the clue bar, tools, keys and clue list go into one column on the right
       (.dsk-pzside), so the page is exactly as tall as the taller of the two */
    $$('#s-puz .pz-root').forEach(root => {
      const gw = $1(':scope > .pz-gridwrap', root); let side = $1(':scope > .dsk-pzside', root);
      if (!gw || !MQW.matches) { if (side) unwrapPz(side); return; }
      if (!side) { side = D.createElement('div'); side.className = 'dsk-pzside dsk-only'; gw.after(side); }
      else if (side.previousElementSibling !== gw) gw.after(side);
      [...root.children].forEach(c => { if (c === gw || c === side || c.matches('.pz-bar, .pz-sub, .pz-live, .note, .back')) return;   // clue bar, tools, keys, clues…
        side.appendChild(c); });
    });
  }
  function unwrapPz(side) { [...side.children].forEach(c => side.before(c)); side.remove(); }
  async function worldCards() {
    const scr = $1('#s-world'), map = $1('#map'); if (!scr || !map || !map.querySelector('svg')) return;
    const g = prof().grade, subs = curSubjects(g); if (!subs.length) return;
    const sig = g + ':' + subs.map(s => s.id).join(',') + ':' + Object.keys(st().topics || {}).length;
    const anchor = $1(':scope > .hud', scr) || map;
    const old = $1('#dskSubj'); if (old && old.dataset.sig === sig && old.previousElementSibling === anchor) return;
    const datas = await Promise.all(subs.map(s => subjectData(g, s.id)));
    let cur = false;
    const cards = subs.map((s, i) => { const d = datas[i], sty = (Worlds.SUBJECT_STYLE || {})[s.id] || { e: '📘', c: '#ffc93c' }, pct = d ? Math.round(subjectPct(d)) : 0;
      let state = !d ? 'soon' : pct >= 100 ? 'done' : 'open'; if (state === 'open' && !cur) { state = 'cur'; cur = true; }
      const nx = d ? d.chapters.find(c => !c.topics.every(t => topicStars(t.id))) : null;
      return `<button type="button" class="dsk-sc ${state === 'cur' ? 'cur' : ''} ${state === 'soon' ? 'soon' : ''}" data-sid="${E(s.id)}" style="--c:${E(sty.c || '#ffc93c')}" aria-label="${E(s.name)}: ${d ? `${pct}% done, ${d.chapters.length} chapters` : 'coming soon'}">
        <span class="dsk-pc" aria-hidden="true">${d ? pct + '%' : ''}</span><span class="dsk-se" aria-hidden="true">${E(sty.e || '📘')}</span>${state === 'cur' ? '<span class="dsk-tagc">Up next</span>' : ''}<b>${E(s.name)}</b>
        <small>${d ? (nx ? `Ch ${E(nx.n)} · ${E(nx.title)}` : 'All chapters done! 🏆') : 'Coming soon'}</small>${d ? `<span class="dsk-bar" aria-hidden="true"><i style="width:${pct}%"></i></span>` : ''}</button>`; });
    const el = old || D.createElement('div'); el.id = 'dskSubj'; el.className = 'dsk-cards dsk-only'; el.dataset.sig = sig;
    el.innerHTML = `<h2>Your subjects <small>${subs.length} worlds to explore</small></h2>` + cards.join('');
    if (el.previousElementSibling !== anchor) anchor.after(el);
    $$('.dsk-sc', el).forEach(b => b.onclick = () => { const s = b.dataset.sid; if (b.classList.contains('soon')) { tap('hmm'); try { toast('This subject is being built — coming soon!'); } catch (e) {} return; } tap('open'); subjectScreen(s); });
  }
  async function chapterCards() {
    const map = $1('#cmap'), n = typeof NAV !== 'undefined' ? NAV : {}; if (!map || !n.subject || !map.querySelector('svg')) return;
    const g = prof().grade, sid = n.subject, d = await subjectData(g, sid); if (!d) return;
    const sig = sid + ':' + Object.keys(st().topics || {}).length;
    const scr = $1('#s-subject'), anchor = $1(':scope > #subTools', scr) || $1(':scope > #viewTgl', scr) || map;
    const old = $1('#dskChap'); if (old && old.dataset.sig === sig && old.previousElementSibling === anchor) return;
    const col = ((Worlds.SUBJECT_STYLE || {})[sid] || {}).c || '#ffc93c'; let cur = false;
    const cards = d.chapters.map((c, i) => { const dn = c.topics.filter(t => topicStars(t.id)).length, all = c.topics.length, pct = all ? Math.round(dn / all * 100) : 0;
      const isCur = !cur && dn < all; if (isCur) cur = true;
      const stars = all ? Math.round(c.topics.reduce((a, t) => a + topicStars(t.id), 0) / all) : 0;
      return `<button type="button" class="dsk-sc ${isCur ? 'cur' : ''}" data-ci="${i}" style="--c:${E(col)}" aria-label="Chapter ${E(c.n)}: ${E(c.title)}. ${dn} of ${all} quests done.">
        <span class="dsk-pc" aria-hidden="true">${pct}%</span><span class="dsk-se" aria-hidden="true">${E(c.emoji || '📘')}</span><span class="dsk-tagc">${isCur ? 'Up next · ' : ''}Chapter ${E(c.n)}</span><b>${E(c.title)}</b>
        <small>${dn}/${all} quests <span class="dsk-st" aria-hidden="true">${'⭐'.repeat(stars)}${'☆'.repeat(3 - stars)}</span></small><span class="dsk-bar" aria-hidden="true"><i style="width:${pct}%"></i></span></button>`; });
    const el = old || D.createElement('div'); el.id = 'dskChap'; el.className = 'dsk-cards dsk-only'; el.dataset.sig = sig;
    el.innerHTML = `<h2>Chapters <small>${d.chapters.length} chapters</small></h2>` + cards.join('');
    if (el.previousElementSibling !== anchor) anchor.after(el);
    $$('.dsk-sc', el).forEach(b => b.onclick = () => { tap('open'); chapterScreen(sid, +b.dataset.ci); });
  }
  function unwrapChapter() { const w = $1('#dskChGrid'); if (!w) return; const l = $1('.dsk-tlist', w); if (l) [...l.children].forEach(c => w.before(c)); w.remove(); }
  async function chapterPreview() {
    const scr = $1('#s-chapter'), n = typeof NAV !== 'undefined' ? NAV : {}; if (!scr || !n.subject || n.chapter == null) return;
    const tc = $$(':scope > .tcard', scr); if (!tc.length || $1('#dskChGrid', scr)) return;
    const g = prof().grade, d = await subjectData(g, n.subject), c = d && d.chapters[n.chapter]; if (!c) return;
    if ($1('#dskChGrid', scr) || !tc[0].isConnected) return;
    const wrap = D.createElement('div'); wrap.id = 'dskChGrid'; wrap.className = 'dsk-only';
    const list = D.createElement('div'); list.className = 'dsk-tlist'; list.setAttribute('role', 'list');
    tc[0].before(wrap); tc.forEach(t => list.appendChild(t)); wrap.appendChild(list);
    const pv = D.createElement('div'); pv.id = 'dskPrev'; pv.className = 'card'; pv.setAttribute('aria-live', 'polite'); wrap.appendChild(pv);
    const col = ((Worlds.SUBJECT_STYLE || {})[n.subject] || {}).c || '#7646ea', sid = n.subject, ci = n.chapter;
    const paint = ti => {
      const t = c.topics[ti]; if (!t) return; const sStar = topicStars(t.id), Lr = t.learn || {};
      tc.forEach((b, i) => b.classList.toggle('dsk-sel', i === ti));
      pv.style.setProperty('--c', col);
      pv.innerHTML = `<div class="dsk-ph" data-e="${E(c.emoji || '📘')}"><span class="tag">Quest ${ti + 1} of ${c.topics.length}</span><h2>${E(t.title)}</h2>${Lr.hook ? `<p>${E(Lr.hook)}</p>` : ''}</div>
        <div class="dsk-pb">${(Lr.points || []).length ? `<h3>💡 What you will learn</h3><ul class="dsk-pts">${Lr.points.slice(0, 3).map(x => `<li>${E(x)}</li>`).join('')}</ul>` : ''}
        <div class="dsk-facts"><span>${sStar ? '⭐'.repeat(sStar) + ' earned' : '☆ not started'}</span>${(t.games || []).length ? `<span>🎮 ${t.games.length} game${t.games.length > 1 ? 's' : ''}</span>` : ''}<span>❓ ${(t.quiz || []).length} quiz questions</span><span>🐥 Teach Gappu</span></div>
        <div class="dsk-pbtn"><button type="button" class="btn ${sStar ? 'ghost' : ''}" id="dskPGo">${sStar ? '🔁 Play again' : 'Start quest ▶'}</button></div></div>`;
      $1('#dskPGo', pv).onclick = () => { tap('open'); playTopic(sid, ci, ti); };
    };
    const first = Math.max(0, c.topics.findIndex(t => !topicStars(t.id)));
    tc.forEach((b, i) => { b.setAttribute('role', 'listitem'); b.addEventListener('mouseenter', () => paint(i)); b.addEventListener('focus', () => paint(i)); });
    paint(first);
  }

  /* ================= keyboard ================= */
  const typing = a => a && ((/^(input|textarea|select)$/i.test(a.tagName) && !/^(range|checkbox|radio|button)$/i.test(a.type || '')) || a.isContentEditable);
  function keysHelp() {
    tap('open'); let sh = $1('#dskKeys');
    if (!sh) { sh = D.createElement('div'); sh.className = 'sheet'; sh.id = 'dskKeys'; sh.setAttribute('role', 'dialog'); sh.setAttribute('aria-modal', 'true'); sh.setAttribute('aria-labelledby', 'dskKeysT'); D.body.appendChild(sh);
      sh.addEventListener('click', e => { if (e.target === sh) sh.classList.remove('show'); }); }
    const nb = navButtons().map((b, i) => `<tr><td><kbd>${i + 1}</kbd></td><td>${E(b.textContent.replace(/\d+$/, '').trim())}</td></tr>`).join('');
    sh.innerHTML = `<div class="sheet-in"><h2 id="dskKeysT"><span aria-hidden="true">⌨️</span> Keyboard keys</h2><p class="sub">Study faster with the keyboard.</p>
      <table class="dsk-keys"><tbody>${nb}<tr><td><kbd>Alt</kbd>+<kbd>1</kbd>…<kbd>5</kbd></td><td>Same, even while answering</td></tr>
      <tr><td><kbd>1</kbd>–<kbd>4</kbd> or <kbd>A</kbd>–<kbd>D</kbd></td><td>Pick an answer</td></tr><tr><td><kbd>Enter</kbd></td><td>Next / continue</td></tr>
      <tr><td><kbd>/</kbd></td><td>Search topics</td></tr><tr><td><kbd>F</kbd></td><td>Focus mode (hide the menus)</td></tr><tr><td><kbd>[</kbd></td><td>Small / big menu</td></tr>
      <tr><td><kbd>R</kbd></td><td>Read the screen aloud</td></tr><tr><td><kbd>H</kbd></td><td>Voice &amp; keys help</td></tr><tr><td><kbd>Esc</kbd></td><td>Close a window</td></tr><tr><td><kbd>K</kbd></td><td>This list</td></tr></tbody></table>
      <button type="button" class="btn ghost" id="dskKeysX">Got it</button></div>`;
    sh.classList.add('show'); const x = $1('#dskKeysX', sh); x.onclick = () => { sh.classList.remove('show'); const b = $1('#dskKeysB'); if (b) b.focus({ preventScroll: true }); }; x.focus();
  }
  function search() {
    const go = () => { const i = $1('.screen.active #gsIn, .screen.active #caHomeQ'); if (i) { i.focus(); i.scrollIntoView({ block: 'center' }); return true; } return false; };
    if (go()) return; goHome(); let n = 0; const t = setInterval(() => { if (go() || ++n > 20) clearInterval(t); }, 150);
  }
  D.addEventListener('keydown', e => {
    if (built && e.key === 'Escape' && R.classList.contains('dsk-drawer')) { e.preventDefault(); toggleSide(false); return; }
    if (!built || e.ctrlKey || e.metaKey) return;
    const a = D.activeElement; if (typing(a)) return;
    if ($1('.sheet.show, .asksheet.show, .pv-hub.show') && !(e.key === 'k' && $1('#dskKeys.show'))) return;
    if (R.classList.contains('dsk-ob')) return;
    const k = e.key;
    if (/^[1-5]$/.test(k) && (e.altKey || !e.defaultPrevented)) {
      const nb = navButtons()[+k - 1]; if (!nb) return;
      if (!e.altKey) { /* digits answer questions (js/a11y.js) — only switch tabs where nothing is numbered */
        if ($$('.screen.active .opt:not([disabled]), .screen.active .tcard, .screen.active .node, .screen.active .choice, .screen.active .arc-opt, .screen.active .lv-opt').some(x => x.offsetParent !== null)) return; }
      e.preventDefault(); nb.click(); nb.focus({ preventScroll: true }); return;
    }
    if (e.altKey || e.defaultPrevented) return;
    if (/^[a-dA-D]$/.test(k) && !e.repeat) {
      const ops = $$('.screen.active .opt, .sheet.show .opt').filter(x => x.offsetParent !== null);
      if (ops.length >= 2) { const o = ops['abcd'.indexOf(k.toLowerCase())]; if (o && !o.disabled) { e.preventDefault(); o.click(); } return; }
    }
    if (k === '/') { e.preventDefault(); search(); }
    else if ((k === 'f' || k === 'F') && !e.repeat) { e.preventDefault(); setFocus(!R.classList.contains('dsk-focus')); }
    else if (k === '[') { e.preventDefault(); toggleSide(); }
    else if ((k === 'k' || k === 'K') && !e.repeat) { e.preventDefault(); const s = $1('#dskKeys.show'); if (s) s.classList.remove('show'); else keysHelp(); }
  });

  /* ================= hooks ================= */
  /* games and puzzles get the whole width: no Today panel (and a compact page top) while playing */
  function modes() {
    const a = act(), s = $1('.screen.active');
    const play = !!s && (a === 'puz' || a === 'live' || a === 'boss' || (a === 'play' && !!$1('#phArcHost', s)) || (a === 'chapter' && !!$1('.sty-scene', s)));
    const norail = play || (a === 'topic' && !MQT.matches);
    if (R.classList.contains('dsk-play') !== play) R.classList.toggle('dsk-play', play);
    if (R.classList.contains('dsk-norail') !== norail) R.classList.toggle('dsk-norail', norail);
  }
  function onShow() { if (!built) return; obState(); modes(); labelNav(); quick(); refresh(); enhance(); hideTip(); }
  if (typeof window.show === 'function') { const _show = window.show; window.show = function () { const r = _show.apply(this, arguments); try { onShow(); } catch (e) {} return r; }; }
  if (typeof window.hud === 'function') { const _hud = window.hud; window.hud = function () { const r = _hud.apply(this, arguments); try { if (built) refresh(); } catch (e) {} return r; }; }
  function boot() {
    const m = $1('main'); if (m) new MutationObserver(() => { if (built) enhance(); }).observe(m, { childList: true, subtree: true });
    const nv = $1('nav'); if (nv) new MutationObserver(() => { if (built) { clearTimeout(nv._dsk); nv._dsk = setTimeout(labelNav, 50); } }).observe(nv, { childList: true, attributes: true, subtree: true, attributeFilter: ['hidden'] });
    sync();
  }
  function sync() { tabletSwitch(); if (wantDsk()) { build(); if (built) { applyCol(); obState(); modes(); refresh(); enhance(); } } else unbuild(); }
  addEventListener('sv-layout', sync);
  /* tablets: a small switch between the phone layout and the desktop layout (shown only when the screen is wide enough for both) */
  function tabletSwitch() {
    let b = D.getElementById('svLayoutSw');
    if (R.dataset.device !== 'tablet' || !MQ.matches) { if (b) b.remove(); return; }
    if (!b) { b = D.createElement('button'); b.type = 'button'; b.id = 'svLayoutSw'; D.body.appendChild(b);
      b.onclick = () => { const desk = R.classList.contains('dsk'); svSetLayout(desk ? 'mobile' : 'desktop'); }; }
    const desk = wantDsk();
    b.textContent = desk ? '📱 Phone view' : '🖥️ Desktop view';
    b.setAttribute('aria-label', desk ? 'Switch to the phone layout' : 'Switch to the desktop layout');
  }
  [MQ, MQW, MQR, MQX, MQT].forEach(q => { try { q.addEventListener('change', sync); } catch (e) { q.addListener(sync); } });
  setInterval(() => { if (built && !D.hidden) { obState(); refresh(); } }, 30000);
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', () => setTimeout(boot, 0)); else setTimeout(boot, 0);
  window.Desktop = { refresh, enhance, focus: setFocus, side: toggleSide, keys: keysHelp, _L: L, _continue: continueInfo };
})();
