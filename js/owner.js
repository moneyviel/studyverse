/* ================= StudyVerse “Pulse” (owner dashboard) + 🧠 “Pulse Coach” (follow-ups) — js/owner.js =================
   UI names live in ONE constant, NAME, at the top of the code below (rename there only).
   Who sees it: only owner accounts (studyverse.admins). Me (CA: Profile) → "📈 Pulse — your business at a glance" card, placed right after the
   "🏫 Schools & coaching (owner)" card (same rule as js/inst.js: Cloud.admin()). The server checks again: every
   rpc owner_dash_* returns nothing unless the caller is an owner (supabase/migrations/20261111_owner_dash.sql).

   1. Usage recorder (every student, tiny, no personal content): ST.ou = { v:1,
        d: { 'YYYY-MM-DD': { feature: opens } }   which parts of the app are used (60 days kept)
        x: { 'YYYY-MM-DD': { learn|game|quiz|teach: n } }   the step where a topic quest was left unfinished
        t: { topicId: [starts, finished] }       topic quests started vs finished (drop-off)
        dev: { os, pwa, w: phone|tablet|laptop, app, at } }   device family only (no model, no location)
      Recorded by wrapping show(), playTopic(), doneStep() and the open() of feature modules. Synced with ST by js/cloud.js.
   2. Dashboard (full screen sheet, tabs): Overview · Subscriptions · Students · Usage · Parents & schools · 🧠 Pulse Coach.
      One period (7/30/90 days, 12 months, custom) and one set of filters (class band / class / CA level, status, plan,
      board, school or coaching, state, signup source) apply everywhere. Summary first; tap any number, bar, row or cell
      to go deeper. Every table has a CSV button; every chart has a table view. Charts are plain inline SVG/HTML.
   3. Pulse Coach: today's prioritised follow-ups from fixed rules (server), each with why, a suggested action and
      helpers that only PREPARE things (editable message → copy / email / WhatsApp / call, a one-use 20% renewal code
      after a confirm). Nothing is ever sent automatically. Done / snooze / note are saved for the owner (rpc owner_followup_set).
   Privacy: owner-only; data is used to improve the service; no ad or marketing segmentation of children; messages
   about a child go to the linked parent when there is one.
   Ideas borrowed (read-only) from the owner's other apps: Salonzy SuperAdmin (greeting + one-line summary, search
   anything, tappable KPI tiles that open a filtered list, period picker with auto day/week/month, change vs previous
   period, CSV), Football Club (rule-based "Smart Suggestions — no outside AI", prepared WhatsApp / email reminders),
   Research Workflow (due-in-7-days / overdue tiles that open a drill-down list, refresh button), Takshila ("everything
   that needs you today" home, KPI → drill table, ageing buckets, health tags). */
(function () {
  'use strict';
  /* the names shown in the app — rename here only */
  const NAME = { app: 'Pulse', icon: '📈', card: '📈 Pulse — your business at a glance', coach: 'Pulse Coach', coachIcon: '🧠', sign: '— Mukesh, StudyVerse' };
  const D = document, W = window, SS = sessionStorage;
  const SITE = 'https://study.moneyviel.com/';
  const C = () => W.Cloud || null;
  const S = () => { try { return ST; } catch (e) { return null; } };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const say = m => { try { toast(m); } catch (e) {} };
  const one = r => Array.isArray(r) ? r[0] : r;
  const DAY = 864e5;
  const dkey = t => new Date(t).toISOString().slice(0, 10);
  const todayK = () => dkey(Date.now());
  const addD = (d, n) => dkey(Date.parse(d + 'T00:00:00Z') + n * DAY);

  /* =====================================================================================
     1. usage recorder
     ===================================================================================== */
  const FEAT = [
    ['map', '🗺️', 'World map / CA journey'], ['learn', '📚', 'Topic quests'], ['practice', '🎯', 'Practice'], ['tests', '📝', 'Chapter tests'],
    ['boss', '👾', 'Boss of the week'], ['play', '🎮', 'Play hub'], ['games', '🕹️', 'Arcade games'], ['puzzles', '🧩', 'Puzzles'],
    ['live', '👫', 'Live game rooms'], ['story', '📖', 'Story mode'], ['exam', '📅', 'Exam planner'], ['calc', '🧮', 'Calculator Academy'],
    ['calculator', '🔢', 'Calculator'], ['ask', '🐥', 'Ask Gappu'], ['gk', '🌍', 'GK snacks'], ['dash', '📊', 'My dashboard & analysis'],
    ['squad', '🦁', 'Squad / friends'], ['stars', '⭐', 'Stars sheet'], ['cards', '🃏', 'Card album'], ['me', '😊', 'Me / Profile']];
  const FEATN = Object.fromEntries(FEAT.map(f => [f[0], f]));
  const SCR = { world: 'map', ca: 'map', subject: 'map', chapter: 'map', practice: 'practice', squad: 'squad', me: 'me', insights: 'dash', play: 'play', live: 'live' };
  const STEPN = { learn: 'Learn (reading)', game: 'Play (mini game)', quiz: 'Quiz', teach: 'Teach Gappu' };
  const last = {};
  let saveT = 0, cur = null;
  function ou() {
    const st = S(); if (!st) return null;
    let o = st.ou; if (!o || typeof o !== 'object' || o.v !== 1) o = st.ou = { v: 1, d: {}, x: {}, t: {} };
    o.d = o.d && typeof o.d === 'object' ? o.d : {}; o.x = o.x && typeof o.x === 'object' ? o.x : {}; o.t = o.t && typeof o.t === 'object' ? o.t : {};
    if (!o.dev || o.dev.at !== todayK()) o.dev = device();
    return o;
  }
  function device() {
    const ua = navigator.userAgent || '';
    const os = /Android/i.test(ua) ? 'Android' : /iPhone|iPad|iPod/i.test(ua) ? 'iOS' : /Windows/i.test(ua) ? 'Windows' : /Mac OS/i.test(ua) ? 'Mac' : /CrOS/i.test(ua) ? 'ChromeOS' : /Linux/i.test(ua) ? 'Linux' : 'Other';
    let pwa = false; try { pwa = !!(W.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true; } catch (e) {}
    const w = innerWidth < 600 ? 'phone' : innerWidth < 1024 ? 'tablet' : 'laptop';
    const sc = D.querySelector('script[src*="js/app.js"]'), m = sc && /[?&]v=([\w.-]+)/.exec(sc.getAttribute('src') || '');
    return { os, pwa, w, app: m ? m[1] : '', at: todayK() };
  }
  function dirty() {
    clearTimeout(saveT);
    saveT = setTimeout(() => {
      try {
        const o = ou(); if (!o) return; const lim = addD(todayK(), -60);
        ['d', 'x'].forEach(k => Object.keys(o[k]).forEach(d => { if (!(d >= lim)) delete o[k][d]; }));
        const tk = Object.keys(o.t); if (tk.length > 400) tk.sort((a, b) => (o.t[a][0] || 0) - (o.t[b][0] || 0)).slice(0, tk.length - 400).forEach(k => delete o.t[k]);
        if (typeof save === 'function') save();
      } catch (e) {}
    }, 1200);
  }
  function rec(k) {
    try {
      const st = S(); if (!k || !st || !st.profile || (C() && C().isParent && C().isParent())) return;
      const now = Date.now(); if (last[k] && now - last[k] < 1500) return; last[k] = now;
      const o = ou(), d = todayK(), row = o.d[d] || (o.d[d] = {}); row[k] = (row[k] || 0) + 1; dirty();
    } catch (e) {}
  }
  function leave() {                          // a topic quest was left before the end: remember at which step
    try {
      if (!cur || cur.done) { cur = null; return; }
      const run = typeof RUN !== 'undefined' ? RUN : null, k = (run && run.steps && run.steps[run.at] && run.steps[run.at].k) || 'learn';
      const o = ou(), d = todayK(), row = o.x[d] || (o.x[d] = {}); row[k] = (row[k] || 0) + 1; cur = null; dirty();
    } catch (e) { cur = null; }
  }
  function wrapG(name, fn) { try { const g = W[name]; if (typeof g === 'function' && !g.__od) { const w = fn(g); w.__od = 1; W[name] = w; return true; } } catch (e) {} return false; }
  function hookGlobals() {
    try {
      if (typeof show === 'function' && !show.__od) {
        const _show = show;
        show = function (id) { try { const a = D.querySelector('.screen.active'); if (a && a.id === 's-topic' && id !== 'topic') leave(); rec(SCR[id]); } catch (e) {} return _show.apply(this, arguments); };
        show.__od = 1;
      }
      if (typeof playTopic === 'function' && !playTopic.__od) {
        const _pt = playTopic;
        playTopic = function () {
          const r = _pt.apply(this, arguments);
          Promise.resolve(r).then(() => { try {
            const tid = RUN && RUN.t && RUN.t.id; if (!tid) return;
            const o = ou(), a = Array.isArray(o.t[tid]) ? o.t[tid] : (o.t[tid] = [0, 0]); a[0]++; cur = { tid, done: false }; rec('learn'); dirty();
          } catch (e) {} }).catch(() => {});
          return r;
        };
        playTopic.__od = 1;
      }
      if (typeof doneStep === 'function' && !doneStep.__od) {
        const _ds = doneStep;
        doneStep = function () { try { if (cur && !cur.done && RUN && RUN.t && RUN.t.id === cur.tid) { cur.done = true; const a = ou().t[cur.tid]; if (Array.isArray(a)) a[1] = (a[1] || 0) + 1; dirty(); } } catch (e) {} return _ds.apply(this, arguments); };
        doneStep.__od = 1;
      }
    } catch (e) {}
    const M = [['Story', 'open', 'story'], ['ExamPlan', 'openPlan', 'exam'], ['Rewards', 'startBoss', 'boss'], ['Rewards', 'openAlbum', 'cards'],
      ['PlayHub', 'open', 'play'], ['PlayHub', 'solo', 'games'], ['PlayHub', 'arcade', 'games'], ['Arcade', 'open', 'games'],
      ['Puzzles', 'hub', 'puzzles'], ['Puzzles', 'quick', 'puzzles'], ['Puzzles', 'daily', 'puzzles'], ['Puzzles', 'play', 'puzzles'], ['Puzzles', 'pick', 'puzzles'],
      ['Live', 'open', 'live'], ['Live', 'join', 'live'], ['CalcAcademy', 'open', 'calc'], ['CalcAcademy', 'mission', 'calc'], ['Calc', 'open', 'calculator'],
      ['Ask', 'open', 'ask'], ['GK', 'open', 'gk'], ['Insights', 'open', 'dash'], ['Insights', 'dashboard', 'dash'], ['Tests', 'run', 'tests'], ['Stars', 'open', 'stars'],
      ['CaTools', 'practiceHub', 'practice']];
    M.forEach(([o, m, k]) => { try { const obj = W[o]; if (obj && typeof obj[m] === 'function' && !obj[m].__od) { const f = obj[m]; obj[m] = function () { rec(k); return f.apply(this, arguments); }; obj[m].__od = 1; } } catch (e) {} });
    wrapG('practiceScreen', f => function () { rec('practice'); return f.apply(this, arguments); });
  }

  /* =====================================================================================
     2. Me card (owners only)
     ===================================================================================== */
  const isOwner = () => !!(C() && C().signedIn && C().signedIn() && C().admin && C().admin() && !localStorage.getItem('sv_demo'));
  function placeCard() {
    const meS = D.getElementById('s-me'), ca = D.getElementById('s-ca');
    if (!isOwner()) { D.querySelectorAll('.od-me').forEach(x => x.remove()); return; }
    if (ca && !ca.querySelector('.ca-prof')) ca.querySelectorAll(':scope > .od-me').forEach(x => x.remove());
    [meS && meS.firstElementChild ? meS : null, ca && ca.querySelector('.ca-prof') ? ca : null].filter(Boolean).forEach(h => {
      if (h.querySelector(':scope > .od-me')) return;
      style();
      const c = D.createElement('div'); c.className = 'card od-me';
      c.innerHTML = `<h3>${NAME.card}</h3><p class="sub">Students, subscriptions, usage, parents, schools — and ${NAME.coachIcon} ${NAME.coach}: who to follow up today.</p><button class="btn" type="button">Open ${NAME.app}</button>`;
      c.querySelector('button').onclick = () => open();
      const ref = h.querySelector(':scope > .in-own') || h.querySelector(':scope > #svCodes');
      ref ? ref.after(c) : h.appendChild(c);
    });
  }
  let pq = 0; const placeSoon = () => { cancelAnimationFrame(pq); pq = requestAnimationFrame(() => { try { placeCard(); } catch (e) {} }); };
  function watch() {
    ['s-me', 's-ca'].forEach(id => { const el = D.getElementById(id); if (el && !el.__odw) { el.__odw = 1; new MutationObserver(placeSoon).observe(el, { childList: true }); } });
    placeSoon();
  }

  /* =====================================================================================
     3. dashboard
     ===================================================================================== */
  const rpc = (n, b) => C().rest('rpc/' + n, { method: 'POST', body: b || {} });
  const errT = e => (e && e.status != null && C()) ? C().errText(e) : ((e && e.message) || 'Something went wrong.');
  const nf = n => n == null || isNaN(+n) ? '–' : Math.round(+n).toLocaleString('en-IN');
  const inr = n => n == null || isNaN(+n) ? '–' : '₹' + Math.round(+n).toLocaleString('en-IN');
  const pct = (a, b) => b ? Math.round(100 * a / b) : null;
  const pctS = v => v == null ? '–' : v + '%';
  const fmtD = d => d ? new Date(String(d).length <= 10 ? d + 'T00:00:00Z' : d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', timeZone: String(d).length <= 10 ? 'UTC' : 'Asia/Kolkata' }) : '–';
  const fmtDs = d => d ? new Date(String(d).length <= 10 ? d + 'T00:00:00Z' : d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' }) : '–';
  const fmtM = d => d ? new Date(String(d).slice(0, 10) + 'T00:00:00Z').toLocaleDateString('en-IN', { month: 'short', year: '2-digit', timeZone: 'UTC' }) : '–';
  const ago = d => { if (!d) return 'never'; const n = Math.round((Date.parse(todayK()) - Date.parse(String(d).slice(0, 10))) / DAY); return n <= 0 ? 'today' : n === 1 ? 'yesterday' : n + ' days ago'; };
  const until = d => { if (!d) return '–'; const h = (Date.parse(d) - Date.now()) / 36e5; return h < 0 ? 'ended ' + fmtDs(d) : h < 24 ? 'ends today' : h < 48 ? 'ends tomorrow' : 'ends in ' + Math.ceil(h / 24) + ' days'; };
  const first = n => String(n || '').trim().split(/\s+/)[0] || '';
  const BANDS = [['1-5', 'Class 1–5'], ['6-8', 'Class 6–8'], ['9-10', 'Class 9–10'], ['11-12', 'Class 11–12'], ['ca', 'CA (all levels)'], ['ca-foundation', 'CA Foundation'], ['ca-inter', 'CA Inter'], ['ca-final', 'CA Final']];
  const BANDN = Object.assign(Object.fromEntries(BANDS), { unknown: 'Not chosen yet' });
  const STATUS = [['paid', 'Paying'], ['school', 'School seat'], ['free', 'Free (code / gift)'], ['trial', 'On trial'], ['lapsed', 'Plan ended'], ['trial_ended', 'Trial ended, never paid'], ['none', 'No access yet']];
  const STATN = Object.fromEntries(STATUS);
  const SOURCES = [['self', 'Signed up on their own'], ['school', 'Through a school'], ['parent', 'Invited by a parent'], ['code', 'Free code']];
  const SRCN = Object.fromEntries(SOURCES);
  const TABS = [['overview', '✨ Overview'], ['subs', '💳 Subscriptions'], ['students', '🧒 Students'], ['usage', '🧭 Usage & content'], ['people', '👪 Parents & schools'], ['smart', NAME.coachIcon + ' ' + NAME.coach]];
  const PERIODS = [['7', '7 days'], ['30', '30 days'], ['90', '90 days'], ['365', '12 months'], ['all', 'All time'], ['custom', 'Custom']];
  const COL = { s1: '#2a78d6', s2: '#eb6834', s3: '#1baf7a', good: '#1F7A43', bad: '#B71C2C', ink: '#15161C', mute: '#5d5a52' };
  const RAMP = ['#f1f5fb', '#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b'];

  const V = Object.assign({ tab: 'overview', per: '30', from: '', to: '', f: {}, bucket: 'auto', cohort: 'act', stu: { q: '', sort: 'last_active', desc: true, off: 0 }, show: 'open', who: 'all', pq: '', test: false },
    (() => { try { return JSON.parse(SS.getItem('sv_owner_ui') || '{}'); } catch (e) { return {}; } })());
  const keep = () => { try { SS.setItem('sv_owner_ui', JSON.stringify({ tab: V.tab, per: V.per, from: V.from, to: V.to, f: V.f, bucket: V.bucket, cohort: V.cohort, show: V.show, who: V.who, test: V.test })); } catch (e) {} };
  function range() {
    const t = todayK();
    if (V.per === 'custom' && V.from && V.to) return V.from <= V.to ? [V.from, V.to] : [V.to, V.from];
    if (V.per === 'all') return [addD(t, -3650), t];
    const n = +V.per || 30; return [addD(t, -(n - 1)), t];
  }
  const ALL = () => V.per === 'all';
  /* filters + switches sent to the server: test = show test accounts; cmp = compare the last 30 days with the 30 before (All time) */
  const filt = () => { const o = {}; Object.entries(V.f).forEach(([k, v]) => { if (v !== '' && v != null) o[k] = v; }); if (V.test) o.test = true; if (ALL()) o.cmp = 30; return o; };
  const userF = () => { const o = filt(); delete o.test; delete o.cmp; return o; };
  const plen = () => { const [f, t] = range(); return Math.round((Date.parse(t) - Date.parse(f)) / DAY) + 1; };
  /* what the ▲/▼ arrows compare: this period vs the previous one of the same length; for All time: last 30 days vs the 30 before */
  const cmpText = () => ALL() ? 'last 30 days vs the 30 days before' : `vs the previous ${plen()} days`;
  const pick = (o, a = 'cur', b = 'prev') => ALL() && o.c30 ? [o.c30, o.p30] : [o[a], o[b]];
  const cache = new Map();
  async function get(fn, args) {
    const k = fn + JSON.stringify(args); const c = cache.get(k);
    if (c && Date.now() - c.t < 120000) return c.v;
    const v = one(await rpc(fn, args));
    if (v == null) throw Object.assign(new Error('This is only for the owner account.'), { owner: true });
    if (v && v.ok === false) throw new Error(v.msg || 'Could not load.');
    cache.set(k, { t: Date.now(), v }); return v;
  }

  let hub = null, meta = null, stack = [], loadedAt = 0;
  const REG = {};                // id → { cols, rows, name } for CSV / table views; reset on each render
  let regN = 0;
  function open(tab) {
    if (!isOwner()) { say('Owner only'); return; }
    style(); if (tab) V.tab = tab;
    if (!hub) {
      hub = D.createElement('div'); hub.className = 'sheet pv-hub od-hub'; hub.id = 'odHub'; hub.setAttribute('data-nonav', '');   // Pulse handles Back itself
      hub.setAttribute('role', 'dialog'); hub.setAttribute('aria-modal', 'true'); hub.setAttribute('aria-labelledby', 'odT'); D.body.appendChild(hub);
      hub.addEventListener('click', onClick); hub.addEventListener('pointerover', tipOver); hub.addEventListener('focusin', tipOver);
      hub.addEventListener('pointerout', e => { if (e.pointerType === 'mouse') tipHide(); });
    }
    const was = hub.classList.contains('show'); hub.classList.add('show'); stack = [];
    if (!was) { hpos = 0; baseSt = history.state && !history.state.odv ? history.state : null; hpush(); }
    frame(); paint();
    if (!meta) get('owner_dash_meta', {}).then(m => { meta = m; frame(); paint(); }).catch(() => {});
  }
  /* ---------- Back button: every Pulse view (tab, drill-down) is a browser history entry ----------
     Our popstate listener runs first (capture) and stops the app's own router while Pulse is open. Going back past
     Pulse's first view re-adds it and asks "Leave Pulse?"; Leave goes back to the entry from before Pulse opened. */
  let hpos = 0, leaving = null, baseSt = null;
  const viewNow = () => ({ tab: V.tab, stack: stack.map(x => Object.assign({}, x)) });
  // our entries carry the app router's own state (js/app.js Nav: {sv, pos}) so the router sees "same place" and does nothing
  function hpush() { hpos++; try { history.pushState(Object.assign({}, baseSt || {}, { odv: hpos, view: viewNow() }), ''); } catch (e) {} }
  function restore(v) { if (!v) return; V.tab = v.tab || V.tab; stack = (v.stack || []).map(x => Object.assign({}, x)); keep(); frame(); paint(); }
  function topView() { if (stack.length) { stack = []; hpush(); } }      // filters changed inside a drill-down: back to the tab (as a new view)
  function back() { if (hpos > 0) { try { history.back(); return; } catch (e) {} } askLeave(); }
  function askLeave() {
    if (!hub) return; let c = hub.querySelector('#odLeave'); if (c) { c.querySelector('[data-stay]').focus(); return; }
    c = D.createElement('div'); c.id = 'odLeave'; c.className = 'od-confirm'; c.setAttribute('role', 'alertdialog'); c.setAttribute('aria-modal', 'true'); c.setAttribute('aria-labelledby', 'odLvT');
    c.innerHTML = `<div class="od-cbox"><h2 id="odLvT">Leave ${NAME.app}?</h2><p>You will go back to where you opened it.</p><div class="od-row"><button type="button" class="od-mini od-big" data-stay>Stay</button><button type="button" class="od-mini od-pri od-big" data-leave>Leave</button></div></div>`;
    hub.appendChild(c); c.querySelector('[data-stay]').focus();
    c.querySelector('[data-stay]').onclick = () => c.remove();
    c.querySelector('[data-leave]').onclick = () => leavePulse();
    c.addEventListener('click', e => { if (e.target === c) c.remove(); });
  }
  function leavePulse(then) {
    const c = hub && hub.querySelector('#odLeave'); if (c) c.remove();
    if (hpos <= 0) { close(); if (then) then(); return; }
    leaving = then || true; const n = hpos;
    try { history.go(-n); } catch (e) { close(); }
    setTimeout(() => { if (leaving) { const t = leaving; leaving = null; close(); if (typeof t === 'function') t(); } }, 600);
  }
  W.addEventListener('popstate', e => {
    if (!hub || !hub.classList.contains('show')) return;
    e.stopImmediatePropagation();
    if (leaving) { const t = leaving; leaving = null; close(); if (typeof t === 'function') t(); return; }
    const st = e.state;
    if (st && st.odv) { hpos = st.odv; const c = hub.querySelector('#odLeave'); if (c) c.remove(); restore(st.view); return; }
    hpos = 0; hpush(); askLeave();                 // Back from Pulse's first view: stay on it and ask
  }, true);
  function close() {
    if (!hub) return; hub.classList.remove('show'); tipHide(); hpos = 0;
    const c = hub.querySelector('#odLeave'); if (c) c.remove();
    const b = D.querySelector('.od-me button'); if (b && b.offsetParent) try { b.focus({ preventScroll: true }); } catch (e) {}
  }

  function greeting() { const h = +new Date().toLocaleString('en-GB', { hour: '2-digit', hour12: false, timeZone: 'Asia/Kolkata' }); return h < 12 ? 'Good morning ☀️' : h < 17 ? 'Good afternoon 🌤️' : 'Good evening 🌙'; }
  function frame() {
    const [f, t] = range(), fl = filt(), nF = Object.keys(fl).filter(k => k !== 'q').length;
    const opt = (list, v, all) => `<option value="">${all}</option>` + list.map(([k, n]) => `<option value="${esc(k)}"${String(v) === String(k) ? ' selected' : ''}>${esc(n)}</option>`).join('');
    const plans = (meta && meta.plans || []).map(p => [p.id, p.label + (p.active ? '' : ' (old)')]);
    const insts = (meta && meta.institutions || []).map(i => [i.id, i.name]);
    const boards = (meta && meta.boards || []).map(b => [b, String(b).toUpperCase().replace(/^STATE[-_ ]?/, 'State: ')]);
    const states = (meta && meta.states || []).map(s => [s, s]);
    const chip = (k, label) => `<span class="od-chip">${esc(label)}<button type="button" data-unf="${k}" aria-label="Remove filter ${esc(label)}">✕</button></span>`;
    const chips = [];
    if (fl.band) chips.push(chip('band', BANDN[fl.band] || fl.band)); if (fl.grade) chips.push(chip('grade', 'Class ' + fl.grade));
    if (fl.status) chips.push(chip('status', STATN[fl.status] || fl.status)); if (fl.plan) chips.push(chip('plan', (plans.find(p => p[0] === fl.plan) || [0, fl.plan])[1]));
    if (fl.board) chips.push(chip('board', 'Board ' + String(fl.board).toUpperCase())); if (fl.inst) chips.push(chip('inst', (insts.find(p => p[0] === fl.inst) || [0, 'One school'])[1]));
    if (fl.state) chips.push(chip('state', fl.state)); if (fl.source) chips.push(chip('source', SRCN[fl.source] || fl.source));
    hub.innerHTML = `<div class="pv-wrap od">
      <div class="pv-top"><button class="pv-back" type="button" id="odBk">← Back</button><h1 id="odT"><span>${NAME.icon} ${NAME.app}</span></h1><button class="pv-ref" type="button" id="odRf" aria-label="Refresh data">⟳</button></div>
      <div class="od-hero"><div><div class="od-greet">${greeting()}</div><div class="od-sumline" id="odSum" aria-live="polite">Loading your numbers…</div></div>
        <form class="od-search" id="odSF" role="search"><span aria-hidden="true">🔎</span><input id="odSQ" type="search" placeholder="Find a student: name or email" aria-label="Find a student by name or email" value="${esc(V.f.q || '')}" autocomplete="off"><button type="submit" class="od-sbtn">Find</button></form></div>
      <div class="od-sticky">
      <div class="od-fbar" role="group" aria-label="Period and filters">
        <div class="od-seg" role="radiogroup" aria-label="Period">${PERIODS.map(([k, n]) => `<button type="button" role="radio" aria-checked="${V.per === k}" class="${V.per === k ? 'on' : ''}" data-per="${k}">${n}</button>`).join('')}</div>
        <button type="button" class="od-fbtn${nF ? ' on' : ''}" id="odFB" aria-expanded="false" aria-controls="odFP">⚙️ Filters${nF ? ' (' + nF + ')' : ''}</button>
        <span class="od-range">${ALL() ? 'All time' : `${fmtD(f)} – ${fmtD(t)}`}</span>
      </div>
      ${V.per === 'custom' ? `<div class="od-cust"><label>From <input type="date" id="odFrom" value="${esc(f)}" max="${todayK()}"></label><label>To <input type="date" id="odTo" value="${esc(t)}" max="${todayK()}"></label><button type="button" class="od-mini" id="odCA">Apply</button></div>` : ''}
      <div class="od-fpanel" id="odFP" hidden>
        <div class="od-fgrid">
          <label>Class band / CA level<select data-f="band">${opt(BANDS, V.f.band, 'All classes & courses')}</select></label>
          <label>Class<select data-f="grade">${opt(Array.from({ length: 12 }, (_, i) => [String(i + 1), 'Class ' + (i + 1)]), V.f.grade, 'Any class')}</select></label>
          <label>Status<select data-f="status">${opt(STATUS, V.f.status, 'Any status')}</select></label>
          <label>Plan<select data-f="plan">${opt(plans, V.f.plan, 'Any plan')}</select></label>
          <label>Board<select data-f="board">${opt(boards, V.f.board, 'Any board')}</select></label>
          <label>School / coaching<select data-f="inst">${opt(insts, V.f.inst, 'All (and none)')}</select></label>
          <label>State (of school)<select data-f="state">${opt(states, V.f.state, 'Any state')}</select></label>
          <label>How they joined<select data-f="source">${opt(SOURCES, V.f.source, 'Any way')}</select></label>
        </div>
        <label class="od-check"><input type="checkbox" id="odTest"${V.test ? ' checked' : ''}> Show test accounts <span class="od-mute">(emails at example.com / example.org / .test / .invalid and demo accounts — for checking only)</span></label>
        <div class="od-row"><button type="button" class="od-mini od-pri" id="odFA">Apply filters</button><button type="button" class="od-mini" id="odFC">Clear all</button></div>
      </div>
      ${chips.length || fl.q || V.test ? `<div class="od-chips" aria-label="Active filters">${V.test ? `<span class="od-chip od-chip-t">🧪 Test accounts shown<button type="button" data-untest="1" aria-label="Hide test accounts">✕</button></span>` : ''}${fl.q ? chip('q', '“' + fl.q + '”') : ''}${chips.join('')}${chips.length || fl.q ? '<button type="button" class="od-link" data-unf="*">Clear all</button>' : ''}</div>` : ''}
      <div class="pv-tabs od-tabs" role="tablist" aria-label="Dashboard sections">${TABS.map(([k, n]) => `<button type="button" role="tab" id="odt-${k}" aria-selected="${V.tab === k}" aria-controls="odBody" class="pv-tab${V.tab === k ? ' on' : ''}" data-tab="${k}">${n}</button>`).join('')}</div>
      </div>
      <div id="odBody" class="od-body" role="tabpanel" aria-labelledby="odt-${V.tab}"></div>
      <p class="od-priv">🔒 Owner only. This data is used only to improve StudyVerse for students — never for ads or marketing to children. Messages are prepared for you; nothing is sent automatically.${loadedAt ? ' · Updated ' + new Date(loadedAt).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) : ''}</p>
      <div class="od-tip" id="odTip" role="status" hidden></div></div>`;
    hub.querySelector('#odSF').onsubmit = e => { e.preventDefault(); V.f.q = hub.querySelector('#odSQ').value.trim(); const ch = V.tab !== 'students' || stack.length; V.tab = 'students'; V.stu.off = 0; stack = []; keep(); if (ch) hpush(); frame(); paint(); };
    const fb = hub.querySelector('#odFB'), fp = hub.querySelector('#odFP');
    fb.onclick = () => { fp.hidden = !fp.hidden; fb.setAttribute('aria-expanded', String(!fp.hidden)); if (!fp.hidden) { const s = fp.querySelector('select'); if (s) s.focus(); } };
    hub.querySelector('#odFA').onclick = () => { fp.querySelectorAll('[data-f]').forEach(s => { V.f[s.dataset.f] = s.value; }); V.test = hub.querySelector('#odTest').checked; V.stu.off = 0; topView(); keep(); frame(); paint(); };
    hub.querySelector('#odFC').onclick = () => { V.f = {}; V.stu.off = 0; topView(); keep(); frame(); paint(); };
    const ca = hub.querySelector('#odCA'); if (ca) ca.onclick = () => { V.from = hub.querySelector('#odFrom').value; V.to = hub.querySelector('#odTo').value; if (!V.from || !V.to) { say('Choose both dates'); return; } keep(); frame(); paint(); };
  }
  function onClick(e) {
    const b = e.target.closest('button, [data-go], [data-row], [data-tip]'); if (!b || !hub.contains(b)) { tipHide(); return; }
    const d = b.dataset;
    if (b.id === 'odBk') { if (stack.length) back(); else askLeave(); return; }
    if (b.id === 'odRf') { cache.clear(); meta = null; get('owner_dash_meta', {}).then(m => { meta = m; }).catch(() => {}); paint(); say('Refreshing…'); return; }
    if (d.per) { V.per = d.per; if (V.per === 'custom' && !V.from) { const [f, t] = range(); V.from = addD(t, -29); V.to = t; } keep(); frame(); paint(); return; }
    if (d.tab) { if (V.tab === d.tab && !stack.length) return; V.tab = d.tab; stack = []; keep(); hpush(); hub.querySelectorAll('[data-tab]').forEach(x => { const on = x.dataset.tab === V.tab; x.classList.toggle('on', on); x.setAttribute('aria-selected', String(on)); }); hub.querySelector('#odBody').setAttribute('aria-labelledby', 'odt-' + V.tab); paint(); return; }
    if (d.unf) { if (d.unf === '*') V.f = {}; else delete V.f[d.unf]; V.stu.off = 0; topView(); keep(); frame(); paint(); return; }
    if (d.untest) { V.test = false; topView(); keep(); frame(); paint(); return; }
    if (d.tbl) { const card = b.closest('.od-card'); const v = card.querySelector('.od-viz'), t = card.querySelector('.od-tbl'); const on = t.hidden; t.hidden = !on; if (v) v.hidden = on; b.textContent = on ? 'Chart' : 'Table'; b.setAttribute('aria-pressed', String(on)); return; }
    if (d.more) { const tw = b.previousElementSibling, open = b.getAttribute('aria-expanded') !== 'true'; tw.querySelectorAll('[data-x]').forEach(r => { r.hidden = !open; }); b.setAttribute('aria-expanded', String(open)); b.textContent = open ? 'Show fewer' : 'Show all ' + d.more; return; }
    if (d.csv) { csv(d.csv); return; }
    if (d.go) { go(d.go); return; }
    if (d.tip != null && !d.row) { tipShow(b, true); return; }
    if (d.row) { const r = REG[d.rt]; if (r && r.onRow) r.onRow(r.rows[+d.row], b); return; }
  }
  /* "tab:subs" · "stu:status=paid" (filters then Students) · "f:band=6-8" (filter, stay) · "student:<id>" · "inst:<id>" */
  function go(s) {
    const [k, v] = [s.slice(0, s.indexOf(':')), s.slice(s.indexOf(':') + 1)];
    if (k === 'tab') { V.tab = v; stack = []; }
    else if (k === 'stu' || k === 'f') { v.split('&').forEach(p => { const [a, b] = p.split('='); V.f[a] = decodeURIComponent(b || ''); }); if (k === 'stu') V.tab = 'students'; V.stu.off = 0; stack = []; }
    else if (k === 'student') { stack.push({ kind: 'student', id: v }); }
    else if (k === 'inst') { stack.push({ kind: 'inst', id: v }); }
    else if (k === 'q') { stack.push({ kind: 'question', id: v }); }
    keep(); hpush(); frame(); paint();
  }
  async function paint() {
    if (!hub) return;
    const body = hub.querySelector('#odBody'); if (!body) return;
    Object.keys(REG).forEach(k => delete REG[k]); regN = 0; IDX.length = 0; tipHide();
    const top = stack[stack.length - 1];
    hub.querySelector('#odBk').textContent = top ? '← Back' : '← Close';
    body.innerHTML = '<p class="pv-load" aria-busy="true">Loading…</p>';
    const tok = (paint.n = (paint.n || 0) + 1);
    try {
      let html;
      if (top) html = await ({ student: drillStudent, inst: drillInst, question: drillQuestion })[top.kind](top.id);
      else html = await ({ overview, subs, students, usage, people, smart })[V.tab]();
      if (tok !== paint.n) return;
      body.innerHTML = html; loadedAt = Date.now(); after(body);
      summaryLine();
      if (top) { const h = body.querySelector('h2, h3'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); } hub.scrollTo({ top: 0 }); }
    } catch (e) {
      if (tok !== paint.n) return;
      body.innerHTML = `<div class="pv-card"><p class="od-err" role="alert">${esc(e.owner ? 'This dashboard is only for the owner account. Please sign in as the owner.' : errT(e))}</p><button type="button" class="od-mini" id="odRetry">Try again</button></div>`;
      const r = body.querySelector('#odRetry'); if (r) r.onclick = () => { cache.clear(); paint(); };
    }
  }
  const afterFns = [];
  const later = fn => { afterFns.push(fn); return ''; };
  function after(body) { const l = afterFns.splice(0); l.forEach(fn => { try { fn(body); } catch (e) {} }); }
  async function summaryLine() {
    try {
      const [f, t] = range(), o = await get('owner_dash_overview', { p_from: f, p_to: t, p: filt() }), c = o.cur;
      const el = hub && hub.querySelector('#odSum'); if (el) el.textContent = `${nf(c.students)} student${+c.students === 1 ? '' : 's'} · ${nf(c.paying)} paying · ${nf(c.wau)} active this week`;
    } catch (e) {}
  }

  /* ---------------- small UI parts ---------------- */
  function delta(c, p, good) {
    c = +c || 0; p = +p || 0;
    if (c === p) return `<span class="od-d flat">— same</span>`;
    const up = c > p, ok = good === 'down' ? !up : up, v = p ? Math.round(Math.abs(c - p) / p * 100) + '%' : 'new';
    return `<span class="od-d ${ok ? 'good' : 'bad'}">${up ? '▲' : '▼'} ${v}</span>`;
  }
  /* KPI tile. cur/prev: numbers for the ▲/▼ arrow; prevS: how the earlier value is shown ("was …"). now: note for a snapshot number */
  function kpi(o) {
    const has = o.prev !== undefined && o.prev !== null && !isNaN(+o.prev);
    const prevS = o.prevS != null ? o.prevS : nf(o.prev);
    const cmp = has ? `<span class="od-kc">${delta(o.cur, o.prev, o.good)}<span class="od-was">was ${esc(prevS)}</span></span>` : (o.now ? `<span class="od-kc"><span class="od-was">${esc(o.now)}</span></span>` : '');
    const lbl = `${o.label}: ${strip(String(o.value))}${has ? `. ${cmpText()}: was ${prevS}` : ''}${o.sub ? '. ' + o.sub : ''}`;
    return `<button type="button" class="od-kpi" data-go="${esc(o.go || '')}" aria-label="${esc(lbl)}"><span class="od-kl"><span aria-hidden="true">${o.icon}</span> ${esc(o.label)}</span>
      <b class="od-kv">${o.value}</b>${cmp}${o.sub ? `<span class="od-ks">${esc(o.sub)}</span>` : ''}<span class="od-kgo" aria-hidden="true">›</span></button>`;
  }
  const cmpNote = () => `<p class="od-cmpnote">Arrows compare ${cmpText()}.</p>`;
  function card(title, inner, o = {}) {
    const tools = (o.table ? `<button type="button" class="od-mini" data-tbl="1" aria-pressed="false">Table</button>` : '') + (o.csv ? `<button type="button" class="od-mini" data-csv="${o.csv}">⬇ CSV</button>` : '');
    return `<section class="pv-card od-card${o.cls ? ' ' + o.cls : ''}"${o.id ? ` id="${o.id}"` : ''}><div class="od-ch"><h3>${title}</h3><span class="od-tools">${tools}</span></div>${o.sum ? `<p class="od-sum">${o.sum}</p>` : ''}${o.table ? `<div class="od-viz">${inner}</div><div class="od-tbl" hidden>${o.table}</div>` : inner}${o.foot ? `<p class="od-foot">${o.foot}</p>` : ''}</section>`;
  }
  /* table: cols [{k, l, f(v,row)→html, n:numeric, t(v,row)→csv text}], rows; onRow → rows are buttons-like */
  function table(cols, rows, o = {}) {
    const id = 't' + (++regN); REG[id] = { cols, rows, name: o.name || 'studyverse', onRow: o.onRow };
    if (!rows.length) return `<p class="od-empty">${esc(o.empty || 'Nothing here yet.')}</p>`;
    const head = cols.map(c => {
      const sortable = o.sort && c.s !== false, on = o.sort && o.sort.k === (c.s || c.k);
      return `<th scope="col"${c.n ? ' class="n"' : ''}${on ? ` aria-sort="${o.sort.desc ? 'descending' : 'ascending'}"` : ''}>${sortable ? `<button type="button" class="od-th" data-sortk="${c.s || c.k}">${esc(c.l)}${on ? (o.sort.desc ? ' ▼' : ' ▲') : ''}</button>` : esc(c.l)}</th>`;
    }).join('');
    const lim = o.limit != null ? o.limit : (o.sort ? 0 : 10), cut = lim && rows.length > lim + 2;
    const more = cut ? `<button type="button" class="od-link" data-more="${rows.length}" aria-expanded="false">Show all ${rows.length}</button>` : '';
    if (narrow() && o.cards !== false) {             // phones: one compact card per row instead of a wide table
      const val = (c, r) => c.f ? c.f(r[c.k], r) : esc(r[c.k] == null ? '–' : r[c.k]);
      const generic = r => `<div class="od-ct">${val(cols[0], r)}</div><dl class="od-ckv">${cols.slice(1).map(c => { const v = val(c, r); return v === '–' || v === '' || v === '0' || v === '₹0' ? '' : `<div><dt>${esc(c.l)}</dt><dd>${v}</dd></div>`; }).join('')}</dl>`;
      return `<ul class="od-cards" aria-label="${esc(o.label || 'List')}">${rows.map((r, i) => `<li class="od-ci${o.onRow ? ' od-tr' : ''}"${cut && i >= lim ? ' hidden data-x="1"' : ''}${o.onRow ? ` data-row="${i}" data-rt="${id}" tabindex="0" role="button" aria-label="${esc(o.rowLabel ? o.rowLabel(r) : 'Open details')}"` : ''}>${o.card ? o.card(r) : generic(r)}${o.onRow ? '<span class="od-cgo" aria-hidden="true">›</span>' : ''}</li>`).join('')}</ul>${more}`;
    }
    const body = rows.map((r, i) => `<tr${cut && i >= lim ? ' hidden data-x="1"' : ''}${o.onRow ? ` class="od-tr" data-row="${i}" data-rt="${id}" tabindex="0" role="button" aria-label="${esc(o.rowLabel ? o.rowLabel(r) : 'Open details')}"` : ''}>${cols.map((c, j) => {
      const v = c.f ? c.f(r[c.k], r) : esc(r[c.k] == null ? '–' : r[c.k]);
      return j === 0 ? `<th scope="row"${c.n ? ' class="n"' : ''}>${v}</th>` : `<td${c.n ? ' class="n"' : ''}>${v}</td>`;
    }).join('')}</tr>`).join('');
    return `<div class="od-tw" tabindex="0" role="region" aria-label="${esc(o.label || 'Table')}"><table class="od-t"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>${more}`;
  }
  const narrow = () => innerWidth < 760;
  let wasNarrow = null, rsT = 0;
  W.addEventListener('resize', () => { clearTimeout(rsT); rsT = setTimeout(() => { const n = narrow(); if (wasNarrow !== null && n !== wasNarrow && hub && hub.classList.contains('show')) paint(); wasNarrow = n; }, 250); });
  function csvOf(cols, rows) {
    const q = v => { const s = String(v == null ? '' : v); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
    const txt = (c, r) => c.t ? c.t(r[c.k], r) : (r[c.k] == null ? '' : typeof r[c.k] === 'object' ? JSON.stringify(r[c.k]) : r[c.k]);
    return [cols.map(c => q(c.l)).join(','), ...rows.map(r => cols.map(c => q(txt(c, r))).join(','))].join('\r\n');
  }
  function download(name, text) {
    const a = D.createElement('a'); a.href = URL.createObjectURL(new Blob(['﻿' + text], { type: 'text/csv;charset=utf-8' }));
    a.download = name.replace(/[^\w.-]+/g, '-') + '-' + todayK() + '.csv'; D.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    say('CSV downloaded');
  }
  async function csv(id) {
    if (id === 'students-all') { try { say('Preparing CSV…'); const r = await get('owner_dash_students', { p: filt(), p_sort: V.stu.sort, p_desc: V.stu.desc, p_limit: 5000, p_offset: 0 }); download('studyverse-students', csvOf(STU_COLS, r.rows)); } catch (e) { say(errT(e)); } return; }
    if (id === 'parents-all') { try { const r = await get('owner_dash_parents', { p_from: range()[0], p_to: range()[1], p_q: V.pq || null, p_limit: 5000, p_offset: 0, p: filt() }); download('studyverse-parents', csvOf(PAR_COLS, r.rows)); } catch (e) { say(errT(e)); } return; }
    const r = REG[id]; if (r) download(r.name, csvOf(r.cols.map(c => Object.assign({}, c, { f: null })), r.rows));
  }
  /* tooltip (tap or hover on [data-tip]) */
  function tipShow(el, sticky) {
    const tip = hub && hub.querySelector('#odTip'); if (!tip) return;
    tip.textContent = el.dataset.tip; tip.hidden = false;
    const r = el.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
    tip.style.left = Math.max(8, Math.min(innerWidth - w - 8, r.left + r.width / 2 - w / 2)) + 'px';
    tip.style.top = (r.top - h - 8 < 8 ? r.bottom + 8 : r.top - h - 8) + 'px';
    tip.dataset.sticky = sticky ? '1' : '';
  }
  function tipOver(e) { const el = e.target.closest && e.target.closest('[data-tip]'); if (el && hub.contains(el) && (e.type === 'focusin' || e.pointerType === 'mouse')) tipShow(el); }
  function tipHide() { const tip = hub && hub.querySelector('#odTip'); if (tip) tip.hidden = true; }

  /* ---------------- charts (inline SVG / HTML) ---------------- */
  const nice = m => { if (m <= 5) return Math.max(1, Math.ceil(m)); const p = Math.pow(10, Math.floor(Math.log10(m))), x = m / p; return (x <= 1 ? 1 : x <= 2 ? 2 : x <= 5 ? 5 : 10) * p; };
  const short = n => { n = +n || 0; const a = Math.abs(n); if (a > 0 && a < 10 && n % 1) return n.toFixed(1); return a >= 1e7 ? (n / 1e7).toFixed(1).replace(/\.0$/, '') + 'Cr' : a >= 1e5 ? (n / 1e5).toFixed(1).replace(/\.0$/, '') + 'L' : a >= 1e3 ? (n / 1e3).toFixed(1).replace(/\.0$/, '') + 'k' : String(Math.round(n)); };
  /* line chart: labels[], series [{name, color, values[]}] — one y axis, legend for 2+ series, crosshair hit areas per x */
  function lineChart(labels, series, o = {}) {
    const Wd = innerWidth < 600 ? 380 : 640, H = o.h || (innerWidth < 600 ? 190 : 210), L = 40, R = 12, T = 12, B = 26, n = labels.length;
    const max = nice(Math.max(1, ...series.flatMap(s => s.values.map(v => +v || 0))));
    const x = i => L + (n <= 1 ? (Wd - L - R) / 2 : i * (Wd - L - R) / (n - 1)), y = v => T + (H - T - B) * (1 - (+v || 0) / max);
    const grid = [0, .5, 1].map(f => `<line x1="${L}" x2="${Wd - R}" y1="${y(max * f)}" y2="${y(max * f)}" class="od-grid"/><text x="${L - 6}" y="${y(max * f) + 4}" text-anchor="end" class="od-ax">${o.money ? '₹' : ''}${short(max * f)}</text>`).join('');
    const step = Math.max(1, Math.ceil(n / 6));
    const xl = labels.map((l, i) => (i === n - 1 || (i % step === 0 && n - 1 - i >= step)) ? `<text x="${x(i)}" y="${H - 6}" text-anchor="${i === 0 ? 'start' : i === n - 1 ? 'end' : 'middle'}" class="od-ax">${esc(l)}</text>` : '').join('');
    const lines = series.map(s => `<polyline fill="none" stroke="${s.color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"${s.faded ? ' stroke-dasharray="5 4" opacity=".45"' : ''} points="${s.values.map((v, i) => x(i) + ',' + y(v)).join(' ')}"/>` +
      (n <= 40 && !s.faded ? s.values.map((v, i) => `<circle cx="${x(i)}" cy="${y(v)}" r="${n <= 14 ? 4 : 2.5}" fill="${s.color}" stroke="#fff" stroke-width="1.5"/>`).join('') : '')).join('');
    const hw = n <= 1 ? Wd - L - R : (Wd - L - R) / (n - 1);
    const hits = labels.map((l, i) => `<rect x="${x(i) - hw / 2}" y="${T}" width="${hw}" height="${H - T - B}" fill="transparent" class="od-hit" data-tip="${esc(l + ' · ' + series.map(s => s.name + ' ' + (o.money ? inr(s.values[i]) : nf(s.values[i]))).join(' · '))}"/>`).join('');
    const legend = series.length > 1 ? `<div class="od-leg">${series.map(s => `<span${s.faded ? ' class="od-lf"' : ''}><i style="${s.faded ? `border-top:2px dashed ${s.color};opacity:.6` : `background:${s.color}`}"></i>${esc(s.name)}</span>`).join('')}</div>` : '';
    return `${legend}<svg viewBox="0 0 ${Wd} ${H}" class="od-svg" role="img" aria-label="${esc(o.aria || 'Line chart')}">${grid}${xl}${lines}${hits}</svg>`;
  }
  function colChart(labels, values, o = {}) {
    const pv = o.prev && o.prev.length === values.length ? o.prev.map(v => +v || 0) : null;
    const Wd = innerWidth < 600 ? 380 : 640, H = o.h || 190, L = 40, R = 8, T = 10, B = 26, n = labels.length, max = nice(Math.max(1, ...values.map(v => +v || 0), ...(pv || [])));
    const bw = (Wd - L - R) / Math.max(1, n), y = v => T + (H - T - B) * (1 - (+v || 0) / max), base = H - B;
    const grid = [0, .5, 1].map(f => `<line x1="${L}" x2="${Wd - R}" y1="${y(max * f)}" y2="${y(max * f)}" class="od-grid"/><text x="${L - 6}" y="${y(max * f) + 4}" text-anchor="end" class="od-ax">${o.money ? '₹' : ''}${short(max * f)}</text>`).join('');
    const step = Math.max(1, Math.ceil(n / 6));
    const bars = values.map((v, i) => { const h = Math.max(0, base - y(v)), bx = L + i * bw + Math.min(2, bw * .15), w = Math.max(1, bw - Math.min(4, bw * .3));
      return `<path d="M${bx},${base}V${base - h + Math.min(3, h)}q0,-${Math.min(3, h)} ${Math.min(3, w / 2)},-${Math.min(3, h)}H${bx + w - Math.min(3, w / 2)}q${Math.min(3, w / 2)},0 ${Math.min(3, w / 2)},${Math.min(3, h)}V${base}Z" fill="${o.color || COL.s1}"/>` +
        `<rect x="${L + i * bw}" y="${T}" width="${bw}" height="${H - T - B}" fill="transparent" class="od-hit" data-tip="${esc(labels[i] + ' · ' + (o.money ? inr(v) : nf(v)) + (o.unit ? ' ' + o.unit : '') + (pv ? ' · previous period ' + (o.money ? inr(pv[i]) : nf(pv[i])) : ''))}"/>`; }).join('');
    const pl = pv ? `<polyline fill="none" stroke="${COL.ink}" stroke-width="2" stroke-dasharray="5 4" opacity=".4" points="${pv.map((v, i) => (L + i * bw + bw / 2) + ',' + y(v)).join(' ')}" pointer-events="none"/>` : '';
    const xl = labels.map((l, i) => i % step === 0 && (n - 1 - i >= step || i === 0) ? `<text x="${L + i * bw + bw / 2}" y="${H - 6}" text-anchor="middle" class="od-ax">${esc(l)}</text>` : '').join('');
    const leg = pv ? `<div class="od-leg"><span><i style="background:${o.color || COL.s1}"></i>This period</span><span class="od-lf"><i style="border-top:2px dashed ${COL.ink};opacity:.5"></i>Previous period</span></div>` : '';
    return `${leg}<svg viewBox="0 0 ${Wd} ${H}" class="od-svg" role="img" aria-label="${esc(o.aria || 'Bar chart')}">${grid}${bars}${pl}${xl}</svg>`;
  }
  /* horizontal bars as buttons (each drills): items [{label, value, sub, go, tip}] */
  function hbars(items, o = {}) {
    if (!items.length) return `<p class="od-empty">${esc(o.empty || 'No data yet.')}</p>`;
    const max = Math.max(1, ...items.map(i => +i.value || 0));
    if (o.limit && items.length > o.limit + 2) return hbars(items.slice(0, o.limit), Object.assign({}, o, { limit: 0, max })) +
      `<details class="od-moreb"><summary>Show all ${items.length}</summary>${hbars(items.slice(o.limit), Object.assign({}, o, { limit: 0, max }))}</details>`;
    const mx = o.max || max;
    return `<ul class="od-hb">${items.map(i => { const w = Math.max(i.value ? 2 : 0, Math.round(100 * (+i.value || 0) / mx));
      const inner = `<span class="od-hbl">${i.label}</span><span class="od-hbt"><span class="od-hbf" style="width:${w}%;background:${i.color || o.color || COL.s1}"></span></span><span class="od-hbv">${o.money ? inr(i.value) : nf(i.value)}${i.sub ? `<small>${esc(i.sub)}</small>` : ''}</span>`;
      return `<li>${i.go ? `<button type="button" class="od-hbr" data-go="${esc(i.go)}" aria-label="${esc(i.aria || (strip(i.label) + ': ' + nf(i.value) + (i.sub ? ', ' + i.sub : '') + '. Open'))}">${inner}</button>` : `<div class="od-hbr"${i.tip ? ` data-tip="${esc(i.tip)}" tabindex="0"` : ''}>${inner}</div>`}</li>`; }).join('')}</ul>`;
  }
  const strip = h => String(h).replace(/<[^>]+>/g, '');
  /* small stat tiles: [{i: icon, v: value, l: label, go?}] */
  function tiles(list) {
    return `<div class="od-tiles">${list.map(t => t.go ? `<button type="button" class="od-tile" data-go="${esc(t.go)}"><span aria-hidden="true">${t.i}</span><b>${t.v}</b><small>${esc(t.l)}</small></button>`
      : `<div class="od-tile"><span aria-hidden="true">${t.i}</span><b>${t.v}</b><small>${esc(t.l)}</small></div>`).join('')}</div>`;
  }
  /* ranked list with a % bar: [{i, name, pct, sub}] */
  function rankList(items, lim = 8) {
    if (items.length > lim + 2) return rankList(items.slice(0, lim), 1e9) + `<details class="od-moreb"><summary>Show all ${items.length}</summary>${rankList(items.slice(lim).map((x, k) => Object.assign({}, x, { n0: lim + k })), 1e9)}</details>`;
    return `<ol class="od-rank">${items.map((x, n) => `<li data-tip="${esc(x.name + ': ' + x.sub + (x.tip ? ' · ' + x.tip : ''))}" tabindex="0"><span class="od-rn">${(x.n0 || 0) + n + 1}</span><span class="od-ri" aria-hidden="true">${x.i}</span><span class="od-rname">${esc(x.name)}<small>${esc(x.sub)}</small></span>
      <span class="od-rbar"><span style="width:${Math.max(2, x.pct || 0)}%"></span></span><b class="od-rp">${pctS(x.pct)}</b></li>`).join('')}</ol>`;
  }
  /* heatmap: rows [{label, cells:[{v (0–1 for colour), txt, tip}]}], cols [labels] → a real <table> (screen readers read it as a table) */
  function heat(cols, rows, o = {}) {
    const col = v => v == null ? 'transparent' : RAMP[Math.min(RAMP.length - 1, Math.max(0, Math.round(v * (RAMP.length - 1))))];
    return `<div class="od-tw" tabindex="0" role="region" aria-label="${esc(o.label || 'Heatmap')}"><table class="od-heat"><thead><tr><th scope="col">${esc(o.corner || '')}</th>${cols.map(c => `<th scope="col">${esc(c)}</th>`).join('')}</tr></thead><tbody>${rows.map(r =>
      `<tr><th scope="row">${esc(r.label)}</th>${r.cells.map(c => c == null ? '<td class="od-hx"></td>' : `<td data-tip="${esc(c.tip || '')}" tabindex="-1" style="background:${col(c.v)};color:${c.v > .55 ? '#fff' : COL.ink}">${esc(c.txt)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>
      <div class="od-ramp" aria-hidden="true"><span>${esc(o.lo || 'low')}</span>${RAMP.map(c => `<i style="background:${c}"></i>`).join('')}<span>${esc(o.hi || 'high')}</span></div>`;
  }
  const bLabel = (l, d) => { const b = l.bucket || 'day'; return b === 'month' ? fmtM(d) : fmtDs(d); };

  /* ================= Overview ================= */
  async function overview() {
    const [f, t] = range(), o = await get('owner_dash_overview', { p_from: f, p_to: t, p: filt() }), c = o.cur, p = pick(o)[1];
    const n = Math.round((Date.parse(t) - Date.parse(f)) / DAY) + 1;
    const [C, P] = pick(o);                         // what the arrows compare
    const conv = pct(C.trial_paid, C.trials), convP = pct(P.trial_paid, P.trials);
    const stick = C.mau ? Math.round(100 * C.avg_dau / C.mau) : null, stickP = P.mau ? Math.round(100 * P.avg_dau / P.mau) : null;
    const kp = [
      kpi({ icon: '🧒', label: 'Students', value: nf(c.students), cur: C.signups, prev: P.signups, prevS: '+' + nf(P.signups) + ' sign-ups', sub: `+${nf(C.signups)} sign-ups${ALL() ? ' in 30 days' : ''}`, go: 'tab:students' }),
      kpi({ icon: '💎', label: 'Paying now', value: nf(c.paying), cur: C.paying, prev: P.paying, go: 'stu:status=paid' }),
      kpi({ icon: '🔁', label: 'Monthly revenue (MRR)', value: inr(c.mrr), cur: C.mrr, prev: P.mrr, prevS: inr(P.mrr), sub: 'ex-GST, plans running now', go: 'tab:subs' }),
      kpi({ icon: '💰', label: 'Revenue', value: inr(+c.revenue + (+o.school_revenue || 0)), cur: C.revenue, prev: P.revenue, prevS: inr(P.revenue), sub: `students ${inr(c.revenue)} · schools ${inr(o.school_revenue)}`, go: 'tab:subs' }),
      kpi({ icon: '🌱', label: 'New paying', value: nf(c.new_paid), cur: C.new_paid, prev: P.new_paid, sub: `+ ${nf(c.renewed)} renewed`, go: 'tab:subs' }),
      kpi({ icon: '🍂', label: 'Plans ended (churn)', value: nf(c.churned), cur: C.churned, prev: P.churned, good: 'down', sub: 'not renewed', go: 'stu:status=lapsed' }),
      kpi({ icon: '🎯', label: 'Trial → paid', value: pctS(pct(c.trial_paid, c.trials)), cur: conv || 0, prev: convP || 0, prevS: pctS(convP), sub: `${nf(c.trial_paid)} of ${nf(c.trials)} trials`, go: 'stu:status=trial' }),
      kpi({ icon: '⚡', label: 'Active (day / week / month)', value: `${nf(c.dau)} / ${nf(c.wau)} / ${nf(c.mau)}`, cur: C.wau, prev: P.wau, prevS: nf(P.wau) + ' a week', sub: `${nf(c.active)} active in ${ALL() ? 'all time' : 'period'}`, go: 'tab:usage' }),
      kpi({ icon: '🧲', label: 'Stickiness', value: pctS(c.mau ? Math.round(100 * c.avg_dau / c.mau) : null), cur: stick || 0, prev: stickP || 0, prevS: pctS(stickP), sub: 'avg daily ÷ monthly active', go: 'tab:usage' })];
    const sr = o.series || [], labs = sr.map(r => bLabel(o, r.d));
    const trendT = table([{ k: 'd', l: o.bucket === 'day' ? 'Day' : o.bucket === 'week' ? 'Week of' : 'Month', f: v => esc(bLabel(o, v)), t: v => v }, { k: 'active', l: 'Active students', n: 1 }, { k: 'signups', l: 'Sign-ups', n: 1 }, { k: 'answers', l: 'Answers', n: 1 }], sr, { name: 'activity-trend', label: 'Activity trend table' });
    const tot = Object.values(o.status || {}).reduce((a, b) => a + (+b || 0), 0);
    const st = STATUS.filter(([k]) => o.status && o.status[k]).map(([k, l]) => ({ label: esc(l), value: o.status[k], sub: pctS(pct(o.status[k], tot)), go: 'stu:status=' + k, color: k === 'paid' ? COL.s1 : k === 'school' ? COL.s3 : k === 'lapsed' || k === 'trial_ended' ? '#9a958a' : '#86b6ef' }));
    const bd = BANDS.filter(([k]) => k !== 'ca' && o.bands && o.bands[k]).map(([k, l]) => ({ label: esc(l), value: o.bands[k], go: 'stu:band=' + k }));
    if (o.bands && o.bands.unknown) bd.push({ label: 'Not chosen yet', value: o.bands.unknown, tip: 'Signed up but has not picked a class yet' });
    const src = SOURCES.filter(([k]) => o.sources && o.sources[k]).map(([k, l]) => ({ label: esc(l), value: o.sources[k], go: 'stu:source=' + k }));
    const growth = +c.new_paid - +c.churned;          // renewals keep a student; they do not add one
    const verdict = c.paying > p.paying ? `📈 Subscriptions are <b>growing</b>: ${nf(c.paying)} paying now vs ${nf(p.paying)} ${ALL() ? ' 30 days ago' : ' at the start of this period'}.` : c.paying < p.paying ? `📉 Subscriptions are <b>falling</b>: ${nf(c.paying)} paying now vs ${nf(p.paying)} at the start. Open ${NAME.coachIcon} ${NAME.coach} to win students back.` : `➖ Paying students are <b>steady</b> at ${nf(c.paying)}.`;
    return cmpNote() + `<div class="od-verdict pv-card" role="note">${verdict} <span class="od-mute">New ${nf(c.new_paid)} − ended ${nf(c.churned)} = ${growth >= 0 ? '+' : ''}${nf(growth)} (${nf(c.renewed)} renewed).</span> <button type="button" class="od-link" data-go="tab:smart">Open ${NAME.coach} ›</button></div>
      <div class="od-kpis">${kp.join('')}</div>
      <div class="od-grid2">
        ${card('⚡ Active students & sign-ups', lineChart(labs, [{ name: 'Active students', color: COL.s1, values: sr.map(r => +r.active) }, { name: 'Sign-ups', color: COL.s2, values: sr.map(r => +r.signups) }]
            .concat(!ALL() && (o.pseries || []).length === sr.length ? [{ name: 'Active, previous period', color: COL.s1, faded: true, values: o.pseries.map(r => +r.active) }] : []), { aria: `Active students and sign-ups per ${o.bucket}` }),
          { table: trendT, csv: 't' + regN, sum: `Per ${o.bucket}. Tap a point for numbers.` })}
        ${card('🏷️ Students by status', hbars(st), { sum: 'Tap a bar to see those students.' })}
        ${card('🎒 Students by class / course', hbars(bd), { sum: 'Tap a class band to filter everything by it.' })}
        ${card('🚪 How students joined', hbars(src) + tiles([{ i: '👪', v: nf(o.parents), l: 'parent accounts', go: 'tab:people' }, { i: '🔗', v: nf(o.parents_linked), l: 'linked to a child', go: 'tab:people' }, { i: '🏫', v: nf(o.schools), l: 'schools & coaching', go: 'tab:people' }]))}
      </div>`;
  }

  /* ================= Subscriptions ================= */
  async function subs() {
    const [f, t] = range(), o = await get('owner_dash_subs', { p_from: f, p_to: t, p_bucket: V.bucket === 'auto' ? null : V.bucket, p: filt() });
    const sr = o.series || [], labs = sr.map(r => bLabel(o, r.d)), sum = k => sr.reduce((a, r) => a + (+r[k] || 0), 0);
    const seg = `<div class="od-seg sm" role="radiogroup" aria-label="Group by">${[['auto', 'Auto'], ['day', 'Day'], ['week', 'Week'], ['month', 'Month']].map(([k, n]) => `<button type="button" role="radio" aria-checked="${V.bucket === k}" class="${V.bucket === k ? 'on' : ''}" data-bucket="${k}">${n}</button>`).join('')}</div>`;
    later(b => b.querySelectorAll('[data-bucket]').forEach(x => x.onclick = () => { V.bucket = x.dataset.bucket; keep(); paint(); }));
    later(b => b.querySelectorAll('[data-cohort]').forEach(x => x.onclick = () => { V.cohort = x.dataset.cohort; keep(); paint(); }));
    const trendT = table([{ k: 'd', l: 'Period', f: v => esc(bLabel(o, v)), t: v => v }, { k: 'new', l: 'New', n: 1 }, { k: 'renewed', l: 'Renewed', n: 1 }, { k: 'expired', l: 'Ended', n: 1 }, { k: 'trials', l: 'Trials', n: 1 }, { k: 'failed', l: 'Failed payments', n: 1 }, { k: 'revenue', l: 'Revenue ₹', n: 1, f: v => inr(v) }], sr, { name: 'subscriptions-trend', label: 'Subscriptions per period' });
    const trendId = 't' + regN;
    const revT = table([{ k: 'd', l: 'Period', f: v => esc(bLabel(o, v)), t: v => v }, { k: 'revenue', l: 'Revenue ₹ (ex-GST)', n: 1, f: v => inr(v) }], sr, { name: 'revenue', label: 'Revenue per period' });
    const revId = 't' + regN;
    const planT = table([{ k: 'label', l: 'Plan', f: (v, r) => esc(v || r.plan) }, { k: 'payments', l: 'Payments', n: 1 }, { k: 'revenue', l: 'Revenue', n: 1, f: v => inr(v) }, { k: 'active_now', l: 'Running now', n: 1 }],
      o.by_plan || [], { name: 'plans', label: 'Plans', empty: 'No paid plans in this period.', onRow: r => go('stu:plan=' + encodeURIComponent(r.plan)), rowLabel: r => 'See students on ' + (r.label || r.plan) });
    const planId = 't' + regN;
    const bandRows = (o.by_band || []).map(r => Object.assign({}, r, { name: BANDN[r.band] || r.band, rate: pct(+r.paid + +r.school, r.users) }));
    const bandT = table([{ k: 'name', l: 'Class / course' }, { k: 'users', l: 'Students', n: 1 }, { k: 'paid', l: 'Paying', n: 1 }, { k: 'school', l: 'School seat', n: 1 }, { k: 'trial', l: 'Trial', n: 1 }, { k: 'free', l: 'Free', n: 1 }, { k: 'not_paying', l: 'Not paying', n: 1 },
      { k: 'rate', l: 'Paying %', n: 1, f: v => `<span class="od-pbar"><i style="width:${v || 0}%"></i></span>${pctS(v)}`, t: v => v }],
      bandRows, { name: 'by-class', label: 'Subscriptions by class', onRow: r => r.band !== 'unknown' && go('stu:band=' + r.band), rowLabel: r => 'See students in ' + r.name });
    const bandId = 't' + regN;
    // cohorts
    const coh = (o.cohorts || []).filter(r => +r.n > 0), mx = Math.max(0, ...coh.map(r => (r[V.cohort] || []).length));
    const cohH = coh.length ? heat(Array.from({ length: mx }, (_, k) => k === 0 ? 'Month 0' : '+' + k), coh.map(r => ({ label: `${fmtM(r.m)} (${nf(r.n)})`,
      cells: Array.from({ length: mx }, (_, k) => { const v = (r[V.cohort] || [])[k]; if (v == null) return null; const pc = pct(v, r.n);
        return { v: pc / 100, txt: pctS(pc), tip: `Joined ${fmtM(r.m)}: ${nf(v)} of ${nf(r.n)} (${pc}%) ${V.cohort === 'act' ? 'were active' : 'were paying'} in month ${k}` }; }) })),
      { corner: 'Joined (students)', label: 'Retention by signup month', lo: '0%', hi: '100%' }) : `<p class="od-empty">No sign-ups in the last 12 months for these filters.</p>`;
    const cohSeg = `<div class="od-seg sm" role="radiogroup" aria-label="Retention measure">${[['act', 'Still active'], ['pay', 'Still paying']].map(([k, n]) => `<button type="button" role="radio" aria-checked="${V.cohort === k}" class="${V.cohort === k ? 'on' : ''}" data-cohort="${k}">${n}</button>`).join('')}</div>`;
    const dueT = table([{ k: 'name', l: 'Student', f: (v, r) => `<b>${esc(v || r.email)}</b><small>${esc(r.email)}</small>`, t: (v, r) => v || '' }, { k: 'email', l: 'Email' }, { k: 'band', l: 'Class', f: v => esc(BANDN[v] || '–') },
      { k: 'plan', l: 'Plan' }, { k: 'valid_until', l: 'Ends', f: v => esc(until(v)), t: v => v }, { k: 'last_active', l: 'Last active', f: v => esc(ago(v)), t: v => v || '' }],
      o.due || [], { name: 'renewals-due', label: 'Renewals due', empty: 'No plans end in the next 30 days.', onRow: r => go('student:' + r.user_id), rowLabel: r => 'Open ' + (r.name || r.email) });
    const dueId = 't' + regN;
    const S0 = o.sums || {}, [Cs, Ps] = pick(o, 'sums', 'psums'), netOf = x => (+x.new || 0) - (+x.expired || 0);   // renewals keep a student; they do not add one
    const net = netOf(S0), sg = v => (v >= 0 ? '+' : '') + nf(v);
    return cmpNote() + `<div class="od-kpis">
        ${kpi({ icon: '🌱', label: 'New paying', value: nf(S0.new), cur: Cs.new, prev: Ps.new, go: 'stu:status=paid' })}
        ${kpi({ icon: '🔁', label: 'Renewed', value: nf(S0.renewed), cur: Cs.renewed, prev: Ps.renewed, go: 'stu:status=paid' })}
        ${kpi({ icon: '🍂', label: 'Ended, not renewed', value: nf(S0.expired), cur: Cs.expired, prev: Ps.expired, good: 'down', go: 'stu:status=lapsed' })}
        ${kpi({ icon: net >= 0 ? '📈' : '📉', label: 'Net change', value: sg(net), cur: netOf(Cs), prev: netOf(Ps), prevS: sg(netOf(Ps)), sub: net >= 0 ? 'growing' : 'shrinking', go: 'tab:smart' })}
        ${kpi({ icon: '💰', label: 'Revenue (ex-GST)', value: inr(S0.revenue), cur: Cs.revenue, prev: Ps.revenue, prevS: inr(Ps.revenue), go: 'tab:subs' })}
        ${kpi({ icon: '⚠️', label: 'Failed / unfinished payments', value: nf(S0.failed), cur: Cs.failed, prev: Ps.failed, good: 'down', go: 'tab:smart' })}
        ${kpi({ icon: '⏳', label: 'Trials started', value: nf(S0.trials), cur: Cs.trials, prev: Ps.trials, go: 'stu:status=trial' })}
        ${kpi({ icon: '⏰', label: 'Ending in 7 days', value: nf(o.due7), now: 'right now', sub: `${nf(o.due30)} in 30 days`, go: 'tab:smart' })}</div>
      <div class="od-row od-mt">${seg}</div>
      <div class="od-grid2">
        ${card('📊 Subscriptions over time', lineChart(labs, [{ name: 'New', color: COL.s1, values: sr.map(r => +r.new) }, { name: 'Renewed', color: COL.s3, values: sr.map(r => +r.renewed) }, { name: 'Ended', color: COL.s2, values: sr.map(r => +r.expired) }]
            .concat(!ALL() && (o.pseries || []).length === sr.length ? [{ name: 'New, previous period', color: COL.s1, faded: true, values: o.pseries.map(r => +r.new) }] : []), { aria: 'New, renewed and ended subscriptions' }),
          { table: trendT, csv: trendId, sum: `${nf(sum('trials'))} trials started · ${nf(sum('failed'))} payments failed or left unfinished.` })}
        ${card('💰 Revenue (students, ex-GST)', colChart(labs, sr.map(r => +r.revenue), { money: 1, aria: 'Revenue per period', color: COL.s1, prev: !ALL() && o.pseries ? o.pseries.map(r => +r.revenue) : null }), { table: revT, csv: revId, sum: `${inr(sum('revenue'))} in this period. School invoices are under Parents & schools.` })}
        ${card('🏷️ By plan', planT, { csv: planId, sum: 'Payments in this period. Tap a plan to see its students.' })}
        ${card('🎒 By class / course', bandT, { csv: bandId, sum: 'Everyone matching the filters, right now. Tap a row to see those students.', cls: 'od-span2' })}
      </div>
      ${card('🧊 Do students stay? (retention by signup month)', cohSeg + cohH, { sum: V.cohort === 'act' ? 'Each row = students who joined that month. Each cell = % who still studied in that month after joining. Darker = more stayed.' : 'Each cell = % of that month’s sign-ups who had a running paid plan at the end of that month.' })}
      ${card('⏰ Renewals due in the next 30 days', dueT, { csv: dueId, sum: `${nf(o.due7)} end within 7 days. Tap a student for their profile; reminders are ready in ${NAME.coachIcon} ${NAME.coach}.` })}`;
  }

  /* ================= Students ================= */
  const STU_COLS = [
    { k: 'name', l: 'Student', f: (v, r) => `<b>${esc(v || '—')}</b><small>${esc(r.email)}</small>`, t: v => v || '' },
    { k: 'email', l: 'Email', s: 'email', hide: 1 },
    { k: 'band', l: 'Class / course', s: 'grade', f: (v, r) => esc(r.kind === 'ca' ? 'CA ' + (r.ca_level || 'foundation') : r.grade ? 'Class ' + r.grade : '–'), t: (v, r) => r.kind === 'ca' ? 'CA ' + (r.ca_level || 'foundation') : r.grade || '' },
    { k: 'board', l: 'Board', f: v => esc(v ? String(v).toUpperCase() : '–') },
    { k: 'status', l: 'Plan', f: (v, r) => `<span class="od-st st-${esc(v)}">${esc(STATN[v] || v)}</span><small>${esc(r.plan || '')}</small>`, t: v => STATN[v] || v },
    { k: 'valid_until', l: 'Ends', f: v => esc(v ? fmtDs(v) : '–'), t: v => v || '' },
    { k: 'n_paid', l: 'Past payments', n: 1, s: 'paid_inr', f: (v, r) => `${nf(v)}<small>${inr(r.paid_inr)}</small>`, t: v => v },
    { k: 'parents', l: 'Parents', s: 'n_parents', f: v => esc(v || '–'), t: v => v || '' },
    { k: 'inst_name', l: 'School / class', f: (v, r) => v ? `${esc(v)}<small>${esc(r.class_name || '')}</small>` : '–', t: (v, r) => v ? v + (r.class_name ? ' · ' + r.class_name : '') : '' },
    { k: 'signup', l: 'Joined', f: v => esc(fmtDs(v)), t: v => v ? String(v).slice(0, 10) : '' },
    { k: 'last_active', l: 'Last active', f: v => esc(ago(v)), t: v => v || '' },
    { k: 'streak', l: 'Streak', n: 1, f: v => v ? '🔥 ' + nf(v) : '–', t: v => v },
    { k: 'stars_week', l: 'Stars this week', n: 1, f: v => nf(v), t: v => v },
    { k: 'answered', l: 'Questions', n: 1, f: v => nf(v), t: v => v },
    { k: 'accuracy', l: 'Accuracy', n: 1, f: v => v == null ? '–' : `<span class="${v < 50 ? 'od-bad' : v >= 80 ? 'od-good' : ''}">${v}%</span>`, t: v => v == null ? '' : v },
    { k: 'source', l: 'Joined via', f: v => esc(SRCN[v] || v), t: v => SRCN[v] || v }];
  async function students() {
    const L = 50, r = await get('owner_dash_students', { p: filt(), p_sort: V.stu.sort, p_desc: V.stu.desc, p_limit: L, p_offset: V.stu.off });
    const cols = STU_COLS.filter(c => !c.hide);
    const scard = x => `<div class="od-ct"><b>${esc(x.name || '—')}</b><small>${esc(x.email)}</small></div>
      <div class="od-cline">${esc(x.kind === 'ca' ? 'CA ' + (x.ca_level || 'foundation') : x.grade ? 'Class ' + x.grade : 'Class not chosen')}${x.board ? ' · ' + esc(String(x.board).toUpperCase()) : ''}${x.inst_name ? ' · 🏫 ' + esc(x.inst_name) : ''}</div>
      <div class="od-cfoot"><span class="od-st st-${esc(x.status)}">${esc(STATN[x.status] || x.status)}</span><span>⏱️ ${esc(ago(x.last_active))}</span><span>⭐ ${nf(x.stars_week)} this week</span>${x.streak ? `<span>🔥 ${nf(x.streak)}</span>` : ''}</div>`;
    const SORTS = [['last_active', 'Last active'], ['name', 'Name'], ['signup', 'Joined'], ['stars_week', 'Stars this week'], ['answered', 'Questions'], ['accuracy', 'Accuracy'], ['streak', 'Streak'], ['valid_until', 'Plan ends'], ['paid_inr', 'Paid']];
    const sortSel = narrow() ? `<div class="od-row od-sortrow"><label for="odSort" class="od-mute">Sort by</label><select id="odSort" class="od-sel">${SORTS.map(([k, n]) => `<option value="${k}"${V.stu.sort === k ? ' selected' : ''}>${n}</option>`).join('')}</select><button type="button" class="od-mini" id="odSortDir" aria-label="${V.stu.desc ? 'Highest first' : 'Lowest first'}">${V.stu.desc ? '↓ High first' : '↑ Low first'}</button></div>` : '';
    later(b => { const sel = b.querySelector('#odSort'), dir = b.querySelector('#odSortDir');
      if (sel) sel.onchange = () => { V.stu.sort = sel.value; V.stu.desc = !['name'].includes(sel.value); V.stu.off = 0; paint(); };
      if (dir) dir.onclick = () => { V.stu.desc = !V.stu.desc; V.stu.off = 0; paint(); }; });
    const tb = sortSel + table(cols, r.rows, { name: 'students', label: 'Students', card: scard, sort: { k: V.stu.sort, desc: V.stu.desc }, empty: 'No students match these filters.',
      onRow: x => go('student:' + x.id), rowLabel: x => 'Open ' + (x.name || x.email) });
    later(b => b.querySelectorAll('[data-sortk]').forEach(x => x.onclick = ev => { ev.stopPropagation(); const k = x.dataset.sortk; if (V.stu.sort === k) V.stu.desc = !V.stu.desc; else { V.stu.sort = k; V.stu.desc = !['name', 'email', 'band', 'board', 'status', 'plan', 'inst_name', 'source'].includes(k); } V.stu.off = 0; paint(); }));
    later(b => { const pv = b.querySelector('#odPrev'), nx = b.querySelector('#odNext'); if (pv) pv.onclick = () => { V.stu.off = Math.max(0, V.stu.off - L); paint(); }; if (nx) nx.onclick = () => { V.stu.off += L; paint(); }; });
    const from = r.total ? V.stu.off + 1 : 0, to = Math.min(r.total, V.stu.off + L);
    return card(`🧒 Students <span class="od-count">${nf(r.total)}</span>`, tb + `<div class="od-pager"><span aria-live="polite">${nf(from)}–${nf(to)} of ${nf(r.total)}</span><span><button type="button" class="od-mini" id="odPrev"${V.stu.off ? '' : ' disabled'}>‹ Previous</button> <button type="button" class="od-mini" id="odNext"${to < r.total ? '' : ' disabled'}>Next ›</button></span></div>`,
      { csv: 'students-all', sum: (narrow() ? 'Tap a student to open the full profile.' : 'Tap a column name to sort, a row to open the full profile.') + ' Use 🔎 above to find someone; ⚙️ Filters narrow everything. CSV downloads every matching student (up to 5,000).', cls: 'od-wide' });
  }

  /* --- one student --- */
  const SUBJ = sid => { const st = (W.Worlds && Worlds.SUBJECT_STYLE && Worlds.SUBJECT_STYLE[sid]) || {}; return (st.e ? st.e + ' ' : '') + (st.name || String(sid).replace(/^./, c => c.toUpperCase())); };
  async function topicInfo(id) {           // 'g7-maths-01-01' (+ '#3') → { subject, chapter, topic, q }
    const m = /^g(\d+)-([a-z]+)-(\d+)-(\d+)(?:#(\d+))?$/.exec(id || ''); if (!m) return null;
    try {
      const d = await subjectData(+m[1], m[2]); if (!d || !d.chapters) return null; const tid = `g${m[1]}-${m[2]}-${m[3]}-${m[4]}`;
      for (const c of d.chapters) for (const t of (c.topics || [])) if (t.id === tid) return { g: +m[1], sid: m[2], chapter: c.title, topic: t.title, q: m[5] != null ? (t.quiz || [])[+m[5]] : null };
    } catch (e) {}
    return null;
  }
  async function chapterInfo(ch) {           // 'g7-maths-01'
    const m = /^g(\d+)-([a-z]+)-(\d+)$/.exec(ch || ''); if (!m) return null;
    try { const d = await subjectData(+m[1], m[2]); const c = d && d.chapters && d.chapters.find(c => (c.topics || []).some(t => t.id.startsWith(ch + '-'))); return c ? { g: +m[1], sid: m[2], chapter: c.title } : null; } catch (e) { return null; }
  }
  const nameTopic = async id => { const i = await topicInfo(id); return i ? `${esc(i.topic)}<small class="od-sub">Class ${i.g} · ${esc(SUBJ(i.sid))} · ${esc(i.chapter)}</small>` : `<code>${esc(id)}</code>`; };
  async function drillStudent(id) {
    const r = await get('owner_dash_student', { p_user: id }); const u = r.user || {};
    const nm = u.name || u.email, acc = u.answered ? Math.round(100 * (u.answered - u.wrong) / u.answered) : null;
    const days = []; const map = Object.fromEntries((r.days || []).map(d => [d.d, d]));
    for (let i = 89; i >= 0; i--) { const k = addD(todayK(), -i); days.push({ d: k, a: map[k] ? +map[k].a : 0, s: map[k] ? +map[k].s : 0, x: map[k] ? +map[k].x : 0 }); }
    const activeDays = days.filter(d => d.a || d.s || d.x).length;
    const actT = table([{ k: 'd', l: 'Day', f: v => esc(fmtDs(v)), t: v => v }, { k: 'a', l: 'Answers', n: 1 }, { k: 's', l: 'Minutes', n: 1, f: v => nf(v / 60), t: v => Math.round(v / 60) }, { k: 'x', l: 'Stars', n: 1 }], days.filter(d => d.a || d.s || d.x).reverse(), { name: 'student-activity', label: 'Activity by day' });
    const actId = 't' + regN;
    const subjRows = (r.subjects || []).map(s => { const m = /^g(\d+)-([a-z]+)$/.exec(s.subj) || []; return Object.assign({}, s, { name: (m[1] ? 'Class ' + m[1] + ' · ' : '') + SUBJ(m[2] || s.subj), acc: s.answered ? Math.round(100 * (s.answered - s.wrong) / s.answered) : null, done: (r.topics_done || {})[s.subj] || 0 }); });
    const subjT = table([{ k: 'name', l: 'Subject' }, { k: 'answered', l: 'Questions', n: 1 }, { k: 'acc', l: 'Accuracy', n: 1, f: v => pctS(v), t: v => v }, { k: 'done', l: 'Topics finished', n: 1 }, { k: 'topics', l: 'Topics tried', n: 1 }], subjRows, { name: 'student-subjects', label: 'Subjects', empty: 'No answers recorded yet.' });
    const subjId = 't' + regN;
    const weak = await Promise.all((r.weak || []).map(async w => Object.assign({}, w, { html: await nameTopic(w.topic) })));
    const weakT = table([{ k: 'html', l: 'Topic', f: v => v, t: (v, x) => x.topic }, { k: 'answered', l: 'Answers', n: 1 }, { k: 'acc', l: 'Accuracy', n: 1, f: v => `<span class="od-bad">${v}%</span>`, t: v => v }], weak, { name: 'student-weak', label: 'Weak topics', empty: 'No weak topics — nice!' });
    const payT = table([{ k: 'label', l: 'Plan', f: (v, x) => esc(v || x.plan) }, { k: 'inr', l: 'Amount', n: 1, f: v => inr(v) }, { k: 'status', l: 'Status', f: v => `<span class="od-st st-${v === 'paid' ? 'paid' : v === 'failed' ? 'lapsed' : 'none'}">${esc(v === 'created' ? 'not finished' : v)}</span>`, t: v => v },
      { k: 'code', l: 'Code', f: (v, x) => v ? esc(v) + (x.percent ? ` (${x.percent}%)` : '') : '–' }, { k: 'created_at', l: 'Started', f: v => esc(fmtD(v)), t: v => v }, { k: 'valid_until', l: 'Valid till', f: v => esc(v ? fmtD(v) : '–'), t: v => v || '' }],
      r.payments || [], { name: 'student-payments', label: 'Payments', empty: 'No payments yet.' });
    const payId = 't' + regN;
    const accT = table([{ k: 'course', l: 'Course' }, { k: 'note', l: 'Type', f: v => esc(/^paid/.test(v || '') ? 'Paid plan' : /^inst /.test(v || '') ? 'School seat' : v === 'trial' ? 'Trial' : (v || 'Free / gift')) }, { k: 'valid_until', l: 'Valid till', f: v => esc(v ? until(v) + ' (' + fmtDs(v) + ')' : 'no end date'), t: v => v || '' }, { k: 'granted_at', l: 'Given', f: v => esc(fmtD(v)), t: v => v }],
      r.access || [], { name: 'student-access', label: 'Access', empty: 'No access rows.' });
    const parT = table([{ k: 'email', l: 'Parent email' }, { k: 'linked_at', l: 'Linked', f: v => esc(fmtD(v)), t: v => v }, { k: 'last_sign_in', l: 'Last opened app', f: v => esc(v ? ago(v) : 'never'), t: v => v || '' }, { k: 'weekly_email', l: 'Weekly email', f: v => v ? 'On' : 'Off' }, { k: 'challenges', l: 'Challenges', n: 1 }],
      r.parents || [], { name: 'student-parents', label: 'Parents', empty: 'No parent linked.' });
    const use = Object.entries(r.usage || {}).sort((a, b) => b[1] - a[1]).map(([k, v]) => ({ label: `${(FEATN[k] || [0, '•'])[1]} ${esc((FEATN[k] || [0, 0, k])[2])}`, value: v }));
    const dv = r.device || {};
    const tests = (r.tests || []).slice(0, 8);
    const mail = r.parents && r.parents.length ? r.parents.map(p => p.email).join(',') : u.email;
    return `<div class="pv-card od-prof"><h2>${esc(nm)}</h2><p class="od-mute">${esc(u.email || '')} · ${esc(u.kind === 'ca' ? 'CA ' + (u.ca_level || 'foundation') : u.grade ? 'Class ' + u.grade : 'class not chosen')}${u.board ? ' · ' + esc(String(u.board).toUpperCase()) : ''} · joined ${esc(fmtD(u.signup))} · ${esc(SRCN[u.source] || '')}</p>
        <p><span class="od-st st-${esc(u.status)}">${esc(STATN[u.status] || u.status)}</span> ${esc(u.plan || '')} ${u.valid_until ? '· ' + esc(until(u.valid_until)) : ''}${r.school ? ` · 🏫 ${esc(r.school.name)} ${esc(r.school.class || '')} <button type="button" class="od-link" data-go="inst:${esc(r.school.id)}">open school ›</button>` : ''}</p>
        <div class="od-row"><a class="od-mini" href="mailto:${esc(mail)}">✉️ Email ${r.parents && r.parents.length ? 'parent' : 'student'}</a><button type="button" class="od-mini" data-copy="${esc(u.email)}">📋 Copy email</button></div></div>
      <div class="od-kpis">
        ${kpi({ icon: '⏱️', label: 'Last active', value: esc(ago(u.last_active)), sub: `${activeDays} active days in 90` })}
        ${kpi({ icon: '🔥', label: 'Streak', value: nf(u.streak), sub: r.streak_last ? 'last ' + fmtDs(r.streak_last) : '' })}
        ${kpi({ icon: '⭐', label: 'Stars this week', value: nf(u.stars_week), sub: nf(r.xp) + ' stars in all' })}
        ${kpi({ icon: '✅', label: 'Questions answered', value: nf(u.answered), sub: 'accuracy ' + pctS(acc) })}</div>
      <div class="od-grid2">
        ${card('📅 Activity, last 90 days', !activeDays ? '<p class="od-empty">No activity in the last 90 days.</p>' : colChart(days.map(d => fmtDs(d.d)), days.map(d => d.a), { aria: 'Answers per day, last 90 days', unit: 'answers' }), { table: actT, csv: actId, sum: 'Answers per day. Tap a bar for the day.' })}
        ${card('📚 Subjects', subjT, { csv: subjId })}
        ${card('🩹 Weak topics (accuracy under 70%)', weakT, { sum: 'Good topics to suggest for revision.' })}
        ${card('🧭 What they use (30 days)', hbars(use, { empty: 'No usage recorded yet (needs the latest app version).' }) + (tests.length ? `<h4>Recent tests</h4><ul class="od-list">${tests.map(x => `<li>${esc(x.d || '')} · ${esc(String(x.k || '').replace(/[-_]/g, ' '))} · <b>${x.pct == null ? '–' : esc(x.pct) + '%'}</b></li>`).join('')}</ul>` : ''))}
        ${card('💳 Payments', payT, { csv: payId })}
        ${card('🔑 Access (plans, trial, seats, codes)', accT + ((r.codes || []).length ? `<p class="od-foot">Codes used: ${r.codes.map(c => esc(c.code) + ' (' + esc(c.kind || '') + ')').join(', ')}</p>` : ''))}
        ${card('👪 Parents', parT)}
        ${card('📱 Device & social', `<ul class="od-list"><li>Device: ${esc(dv.os || 'unknown')}${dv.w ? ' · ' + esc(dv.w) : ''}${dv.pwa ? ' · installed app' : dv.os ? ' · in browser' : ''}${dv.app ? ' · app v' + esc(dv.app) : ''}</li><li>Live game rooms joined: ${nf(r.live_games)}</li><li>Squad friends: ${nf(r.friends)}</li></ul>`)}
      </div>`;
  }

  /* ================= Usage & content ================= */
  async function usage() {
    const [f, t] = range(), o = await get('owner_dash_usage', { p_from: f, p_to: t, p: filt() });
    const act = +o.active || 0, tr = +o.tracked_users || 0;
    const fm = Object.fromEntries((o.features || []).map(x => [x.k, x]));
    const feats = FEAT.map(([k, e, n]) => ({ k, label: `${e} ${esc(n)}`, value: fm[k] ? +fm[k].users : 0, opens: fm[k] ? +fm[k].opens : 0 })).sort((a, b) => b.value - a.value);
    const used = feats.filter(x => x.value), unused = feats.filter(x => !x.value);
    const fRank = used.map(x => { const F = FEATN[x.k]; return { i: F[1], name: F[2], pct: pct(x.value, tr), sub: `${nf(x.value)} student${x.value === 1 ? '' : 's'}`, tip: `${nf(x.opens)} opens` }; });
    const featT = table([{ k: 'label', l: 'Feature', f: v => v, t: v => strip(v) }, { k: 'value', l: 'Students', n: 1 }, { k: 'opens', l: 'Opens', n: 1 }], feats, { name: 'feature-usage', label: 'Feature usage' });
    const featId = 't' + regN;
    const dv = o.derived || {};
    const steps = Object.entries(o.drop_steps || {}).sort((a, b) => b[1] - a[1]).map(([k, v]) => ({ label: esc(STEPN[k] || k), value: v, tip: `${nf(v)} topic quests were left during “${STEPN[k] || k}”` }));
    const dt = await Promise.all((o.drop_topics || []).map(async x => Object.assign({}, x, { html: await nameTopic(x.topic), rate: pct(x.left_n, x.starts) })));
    const dropT = table([{ k: 'html', l: 'Topic quest', f: v => v, t: (v, x) => x.topic }, { k: 'starts', l: 'Started', n: 1 }, { k: 'done', l: 'Finished', n: 1 }, { k: 'left_n', l: 'Left', n: 1 }, { k: 'rate', l: 'Left %', n: 1, f: v => `<span class="${v >= 50 ? 'od-bad' : ''}">${pctS(v)}</span>`, t: v => v }],
      dt, { name: 'topic-dropoff', label: 'Topics left unfinished', empty: 'No unfinished quests recorded yet.' });
    const dropId = 't' + regN;
    const hard = await Promise.all((o.hard || []).map(async x => { const i = await topicInfo(x.qid); return Object.assign({}, x, { html: i && i.q ? `${esc(String(i.q.q).slice(0, 110))}<small>Class ${i.g} · ${esc(SUBJ(i.sid))} · ${esc(i.topic)}</small>` : `<code>${esc(x.qid)}</code>` }); }));
    const hardT = table([{ k: 'html', l: 'Question', f: v => v, t: (v, x) => x.qid }, { k: 'tries', l: 'Tries', n: 1 }, { k: 'users', l: 'Students', n: 1 }, { k: 'acc', l: 'Right', n: 1, f: v => `<span class="${v < 40 ? 'od-bad' : ''}">${v}%</span>`, t: v => v }],
      hard, { name: 'hardest-questions', label: 'Hardest questions', empty: 'Not enough answers yet (a question needs 5+ tries).', onRow: x => go('q:' + x.qid), rowLabel: () => 'Open this question' });
    const hardId = 't' + regN;
    const subjI = (o.subjects || []).map(s => ({ label: esc(SUBJ(s.sid)), value: +s.answers, sub: `${nf(s.users)} students · ${pctS(pct(s.right_n, s.answers))} right`, tip: `${SUBJ(s.sid)}: ${nf(s.answers)} answers by ${nf(s.users)} students, ${pctS(pct(s.right_n, s.answers))} right, ${nf(s.secs / 3600)} hours` }));
    const ch = await Promise.all((o.chapters || []).slice(0, 15).map(async x => { const i = await chapterInfo(x.ch); return Object.assign({}, x, { html: i ? `${esc(i.chapter)}<small>Class ${i.g} · ${esc(SUBJ(i.sid))}</small>` : `<code>${esc(x.ch)}</code>` }); }));
    const chT = table([{ k: 'html', l: 'Chapter', f: v => v, t: (v, x) => x.ch }, { k: 'answers', l: 'Answers', n: 1 }, { k: 'users', l: 'Students', n: 1 }, { k: 'acc', l: 'Right', n: 1, f: v => pctS(v), t: v => v }], ch, { name: 'chapters', label: 'Popular chapters', empty: 'No answers in this period.' });
    const chId = 't' + regN;
    const H = {}; (o.hours || []).forEach(([d, h, n]) => { H[d + ':' + h] = +n; });
    const DOW = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], HRS = [[5, 8], [8, 11], [11, 14], [14, 17], [17, 20], [20, 23], [23, 29]];
    const hl = h => { const a = h % 24, f = x => (x % 12 || 12) + (x < 12 || x === 24 ? 'am' : 'pm'); return f(a); };
    const blocks = HRS.map(([a, b]) => `${hl(a)}–${hl(b % 24)}`);
    const hm = Math.max(1, ...DOW.flatMap((_, i) => HRS.map(([a, b]) => { let n = 0; for (let h = a; h < b; h++) n += H[(i + 1) + ':' + (h % 24)] || 0; return n; })));
    const todH = heat(blocks, DOW.map((dn, i) => ({ label: dn, cells: HRS.map(([a, b]) => { let n = 0; for (let h = a; h < b; h++) n += H[(i + 1) + ':' + (h % 24)] || 0; return { v: n / hm, txt: n ? short(n) : '', tip: `${dn} ${hl(a)}–${hl(b % 24)} (India time): ${nf(n)} answers` }; }) })), { corner: 'India time', label: 'Answers by day and time', lo: 'few', hi: 'many' });
    const A0 = o.act || {}, [Ca, Pa] = pick(o, 'act', 'pact'), acc = x => x && +x.answers ? Math.round(100 * x.right / x.answers) : null, hrs = x => Math.round((+(x && x.secs) || 0) / 3600);
    return cmpNote() + `<div class="od-kpis">
        ${kpi({ icon: '⚡', label: 'Active students', value: nf(A0.active), cur: Ca.active, prev: Pa.active, sub: `of ${nf(o.students)} students` })}
        ${kpi({ icon: '✅', label: 'Answers', value: nf(A0.answers), cur: Ca.answers, prev: Pa.answers })}
        ${kpi({ icon: '🎯', label: 'Right answers', value: pctS(acc(A0)), cur: acc(Ca) || 0, prev: acc(Pa) || 0, prevS: pctS(acc(Pa)) })}
        ${kpi({ icon: '⏱️', label: 'Study time', value: nf(hrs(A0)) + ' h', cur: hrs(Ca), prev: hrs(Pa), prevS: nf(hrs(Pa)) + ' h' })}
        ${kpi({ icon: '🧭', label: 'Features used', value: `${used.length} of ${FEAT.length}`, now: 'in this period', sub: unused.length ? unused.length + ' not used yet' : 'all used' })}
        ${kpi({ icon: '🚪', label: 'Quests left midway', value: nf(Object.values(o.drop_steps || {}).reduce((a, b) => a + +b, 0)), now: 'in this period', sub: 'see where below' })}</div>
      <div class="od-grid2">
        ${card('🧭 Most and least used features', (fRank.length ? rankList(fRank) : '<p class="od-empty">No usage recorded yet. Numbers appear as students use the latest app version.</p>')
            + (unused.length ? `<details class="od-moreb"><summary>Not used yet (${unused.length})</summary><div class="od-chiprow">${unused.map(x => `<span class="od-chip2">${x.label}</span>`).join('')}</div></details>` : '')
            + `<h4 class="od-h4">Ever tried (all time)</h4>` + tiles([{ i: '📖', v: nf(dv.story), l: 'Story mode' }, { i: '📅', v: nf(dv.exam), l: 'Exam planner' }, { i: '🧮', v: nf(dv.calc), l: 'Calculator Academy' }, { i: '🌍', v: nf(dv.gk), l: 'GK snacks' }, { i: '🦁', v: nf(dv.friends), l: 'Have squad friends' }, { i: '👫', v: nf(dv.live), l: 'Live rooms (period)' }, { i: '👪', v: nf(dv.challenges), l: 'Parent challenges (period)' }]),
          { table: featT, csv: featId, sum: `% of the ${nf(tr)} students with usage tracking who opened each part in this period.` })}
        ${card('🚪 Where students stop a topic quest', hbars(steps, { color: COL.s2, empty: 'No unfinished quests recorded yet.' }), { sum: 'The step that was on screen when a student left a topic before finishing.' })}
        ${card('📉 Topics most often left unfinished', dropT, { csv: dropId, cls: 'od-span' })}
        ${card('❓ Hardest questions (fix candidates)', hardT, { csv: hardId, sum: 'Lowest share of right answers in this period. Tap one to read it and its answer — maybe the wording or an option needs fixing.', cls: 'od-span' })}
        ${card('📚 Subjects by answers', hbars(subjI, { empty: 'No answers in this period.' }), { sum: 'Tap/hover a bar for students, accuracy and study time.' })}
        ${card('📖 Most practised chapters', chT, { csv: chId })}
        ${card('🕐 When students study', todH, { sum: 'Answers by weekday and time of day (India time). Good times for reminders and new content.', cls: 'od-span' })}
      </div>`;
  }
  async function drillQuestion(qid) {
    const i = await topicInfo(qid); const q = i && i.q;
    if (!q) return `<div class="pv-card"><h2>Question</h2><p>This question id is <code>${esc(qid)}</code>. Its text could not be loaded here (CA questions and removed questions show only the id).</p></div>`;
    const opts = q.options || q.o || [];
    return `<div class="pv-card"><h2>❓ Question to review</h2><p class="od-mute">Class ${i.g} · ${esc(SUBJ(i.sid))} · ${esc(i.chapter)} · ${esc(i.topic)} · <code>${esc(qid)}</code></p>
      <p class="od-q">${esc(q.q)}</p><ol class="od-opts">${opts.map((x, k) => `<li class="${k === q.answer ? 'od-right' : ''}">${esc(x)}${k === q.answer ? ' <b>✓ correct answer</b>' : ''}</li>`).join('')}</ol>
      ${q.explain ? `<p><b>Explanation shown:</b> ${esc(q.explain)}</p>` : ''}${q.mistake ? `<p class="od-mute">Mistake tag: ${esc(q.mistake)}</p>` : ''}
      <p class="od-foot">Ideas: check that only one option can be right, that the wording is simple for Class ${i.g}, and that the explanation shows the steps. Content lives in <code>content/g${i.g}/${esc(i.sid)}.json</code>.</p>
      <button type="button" class="od-mini" data-copy="${esc(qid)}">📋 Copy question id</button></div>`;
  }

  /* ================= Parents & schools ================= */
  const PAR_COLS = [{ k: 'email', l: 'Parent email' }, { k: 'kid_names', l: 'Children', f: v => esc(v || '–') }, { k: 'linked_at', l: 'Linked', f: v => esc(v ? fmtDs(v) : '–'), t: v => v || '' },
    { k: 'last_sign_in_at', l: 'Last opened app', f: v => `<span class="${!v || Date.now() - Date.parse(v) > 14 * DAY ? 'od-bad' : ''}">${esc(v ? ago(v) : 'never')}</span>`, t: v => v || '' },
    { k: 'kid_paid', l: 'Child paying', f: v => v ? '✓' : '–', t: v => v ? 'yes' : 'no' }, { k: 'weekly', l: 'Weekly email', f: v => v ? 'On' : 'Off' },
    { k: 'pending', l: 'Invites waiting', n: 1 }, { k: 'challenges', l: 'Challenges (period)', n: 1 }];
  async function people() {
    const [f, t] = range();
    const [pa, ins, rep] = await Promise.all([get('owner_dash_parents', { p_from: f, p_to: t, p_q: V.pq || null, p_limit: 100, p_offset: 0, p: filt() }), get('owner_dash_institutions', { p: filt() }),
      get('owner_reports', { p_status: 'all', p_limit: 60 }).catch(() => null)]);       // 🚩 reports (migration 20261113_play_ready.sql; empty if not applied yet)
    later(b => { const fm = b.querySelector('#odPF'); if (fm) fm.onsubmit = e => { e.preventDefault(); V.pq = b.querySelector('#odPQ').value.trim(); paint(); }; });
    const parT = table(PAR_COLS, pa.rows || [], { name: 'parents', label: 'Parents', empty: 'No parents match.', onRow: r => { const k = (r.kid_list || [])[0]; if (k) go('student:' + k.id); else say('No child linked yet'); }, rowLabel: r => 'Open child of ' + r.email });
    const instRows = (ins.rows || []).map(r => Object.assign({}, r, { use: r.seats ? pct(r.students, r.seats) : null, act: pct(r.active7, r.students) }));
    const instT = table([{ k: 'name', l: 'School / coaching', f: (v, r) => `<b>${esc(v)}</b><small>${esc([r.type === 'coaching' ? 'Coaching' : 'School', r.city, r.state].filter(Boolean).join(' · '))}</small>`, t: v => v },
      { k: 'status', l: 'Status', f: (v, r) => `<span class="od-st st-${v === 'active' ? 'paid' : v === 'pilot' ? 'trial' : 'lapsed'}">${esc(v === 'pilot' ? 'Pilot' : v === 'active' ? 'Active' : 'Expired')}</span>${v === 'pilot' && r.pilot_until ? `<small>${esc(until(r.pilot_until))}</small>` : ''}`, t: v => v },
      { k: 'seats', l: 'Seats bought', n: 1 }, { k: 'students', l: 'Students joined', n: 1 }, { k: 'use', l: 'Seats used', n: 1, f: v => v == null ? '–' : `<span class="${v < 50 ? 'od-bad' : ''}">${v}%</span>`, t: v => v == null ? '' : v },
      { k: 'act', l: 'Active this week', n: 1, f: (v, r) => r.students ? `<span class="${v < 30 ? 'od-bad' : ''}">${pctS(v)}</span>` : '–', t: v => v == null ? '' : v },
      { k: 'revenue', l: 'Paid (ex-GST)', n: 1, f: v => inr(v), t: v => v }, { k: 'paid_until', l: 'Renewal due', f: v => esc(v ? fmtDs(v) : '–'), t: v => v || '' }, { k: 'unpaid', l: 'Unpaid invoices', n: 1 }],
      instRows, { name: 'institutions', label: 'Schools and coaching', empty: 'No schools or coaching centres yet.', onRow: r => go('inst:' + r.id), rowLabel: r => 'Open ' + r.name });
    const instId = 't' + regN;
    const reqT = table([{ k: 'school', l: 'School', f: (v, r) => `<b>${esc(v || '–')}</b><small>${esc([r.name, r.city].filter(Boolean).join(' · '))}</small>`, t: v => v }, { k: 'students', l: 'Students', n: 1 }, { k: 'phone', l: 'Phone', f: v => v ? `<a href="tel:${esc(v)}">${esc(v)}</a>` : '–', t: v => v || '' }, { k: 'email', l: 'Email', f: v => v ? `<a href="mailto:${esc(v)}">${esc(v)}</a>` : '–', t: v => v || '' }, { k: 'created_at', l: 'Asked', f: v => esc(ago(v)), t: v => v }],
      ins.request_rows || [], { name: 'pilot-requests', label: 'Pilot requests', empty: 'No pilot requests in 90 days.' });
    const reqId = 't' + regN;
    const nC = ALL() ? pa.new_c30 : pa.new, nP = ALL() ? pa.new_p30 : pa.new_prev;
    return cmpNote() + `<h2 class="od-h2">👪 Parents</h2>
      <div class="od-kpis">
        ${kpi({ icon: '👪', label: 'Parents', value: nf(pa.total), cur: nC, prev: nP, prevS: '+' + nf(nP) + ' new', sub: `+${nf(nC)} new · ${nf(pa.linked)} linked` })}
        ${kpi({ icon: '👀', label: 'Opened app this week', value: nf(pa.seen7), cur: pa.seen7, prev: pa.seen7_prev, prevS: nf(pa.seen7_prev) + ' the week before', sub: `${nf(pa.seen30)} this month` })}
        ${kpi({ icon: '😴', label: 'Linked but not seen 14+ days', value: nf(pa.idle), now: 'right now', go: 'tab:smart' })}
        ${kpi({ icon: '✉️', label: 'Weekly email on', value: nf(pa.weekly_on), now: 'right now', sub: `${nf(pa.pending_invites)} child invites waiting` })}
        ${kpi({ icon: '🏆', label: 'Parent challenges', value: nf(pa.challenges), cur: pa.challenges, prev: ALL() ? undefined : pa.challenges_prev, now: ALL() ? 'all time' : undefined })}
        ${kpi({ icon: '💎', label: 'With a paying child', value: nf(pa.kid_paid), now: 'right now' })}</div>
      ${card('👪 Parent list', `<form class="od-search sm" id="odPF" role="search"><span aria-hidden="true">🔎</span><input id="odPQ" type="search" placeholder="Parent email or child name" aria-label="Search parents" value="${esc(V.pq)}"><button type="submit" class="od-sbtn">Find</button></form>` + parT,
        { csv: 'parents-all', sum: 'Most recent first (100 shown; CSV has all). Tap a parent to open their child.', cls: 'od-wide' })}
      <h2 class="od-h2">🏫 Schools & coaching</h2>
      <div class="od-kpis">
        ${kpi({ icon: '🏫', label: 'Institutions', value: nf(ins.total), now: 'right now', sub: `${nf(ins.schools)} school${+ins.schools === 1 ? "" : "s"} · ${nf(ins.coaching)} coaching` })}
        ${kpi({ icon: '🧪', label: 'Pilots running', value: nf(ins.pilots_now), now: 'right now', sub: `pilot → paid ${pctS(pct(ins.pilot_paid, ins.had_pilot))} (${nf(ins.pilot_paid)} of ${nf(ins.had_pilot)})` })}
        ${kpi({ icon: '🪑', label: 'Seats used', value: pctS(pct(ins.students, ins.seats)), now: 'right now', sub: `${nf(ins.students)} joined · ${nf(ins.seats)} bought` })}
        ${kpi({ icon: '⚡', label: 'Active this week', value: pctS(pct(ins.active7, ins.students)), now: 'last 7 days', sub: `${nf(ins.active7)} of ${nf(ins.students)} students` })}
        ${kpi({ icon: '💰', label: 'School revenue', value: inr(ins.revenue), now: 'all time', sub: 'all paid invoices, ex-GST' })}
        ${kpi({ icon: '📞', label: 'Pilot requests (30 days)', value: nf(ins.requests), cur: ins.requests, prev: ins.requests_prev, prevS: nf(ins.requests_prev) + ' the 30 days before', go: 'tab:smart' })}</div>
      ${card('🏫 Schools & coaching centres', instT, { csv: instId, sum: 'Tap one for classes, students, orders and activity.', cls: 'od-wide' })}
      ${card('📞 Pilot requests (last 90 days)', reqT, { csv: reqId })}
      ${reportsHTML(rep)}`;
  }
  /* 🚩 children's-safety reports (friend lists, friend requests, game rooms): preset reasons; a note only from adult students */
  const REPN = { unkind: 'Unkind or rude behaviour', cheating: 'Cheating', name: 'Rude name or picture', other: 'Something else' };
  const REPW = { friend: 'friend list', request: 'friend request', room: 'game room' };
  function reportsHTML(rep) {
    if (!rep || !Array.isArray(rep.rows)) return '';
    const rows = rep.rows.slice().sort((a, b) => (a.status === 'open' ? 0 : 1) - (b.status === 'open' ? 0 : 1));
    later(b => b.querySelectorAll('[data-repst]').forEach(x => x.onclick = async () => {
      x.disabled = true;
      try { const r = one(await rpc('owner_report_set', { p_id: +x.dataset.repid, p_status: x.dataset.repst })); if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not save.');
        say(x.dataset.repst === 'done' ? 'Report marked done ✓' : 'Report reopened'); [...cache.keys()].filter(k => /^owner_(reports|dash_smart)/.test(k)).forEach(k => cache.delete(k)); paint(); }
      catch (e) { x.disabled = false; say(errT(e)); }
    }));
    const li = r => `<li class="od-item p${r.status === 'open' ? 1 : 3}"><div class="od-ih"><span class="od-ii" aria-hidden="true">🚩</span><div><b>${esc(r.reported_name || 'Someone')} — ${esc(REPN[r.reason] || r.reason)}</b>
        <small>${esc(r.reported_email || 'account deleted')} · in a ${esc(REPW[r.context] || r.context)}${r.room_code ? ' ' + esc(r.room_code) : ''} · ${esc(ago(r.created_at))} · by ${esc(r.reporter_name || 'a student')}${+r.n_on_user > 1 ? ` · ${nf(r.n_on_user)} reports in 30 days` : ''}</small></div></div>
        ${r.detail ? `<p class="od-why">“${esc(r.detail)}”</p>` : ''}
        <div class="od-ib">${r.reported_id ? `<button type="button" class="od-mini" data-go="student:${esc(r.reported_id)}">👤 Open profile</button>` : ''}
          ${r.status === 'open' ? `<button type="button" class="od-mini od-pri" data-repst="done" data-repid="${esc(r.id)}">✓ Done</button>` : `<button type="button" class="od-mini" data-repst="open" data-repid="${esc(r.id)}">↩ Reopen</button>`}</div></li>`;
    return `<h2 class="od-h2">🚩 Reports</h2>${card(`🚩 Reports from children <span class="od-count">${nf(rep.open)} open</span>`, rows.length ? `<ul class="od-rep" style="list-style:none;margin:0;padding:0">${rows.map(li).join('')}</ul>` : '<p class="od-empty">No reports. 🎉</p>',
      { sum: 'From friend lists, friend requests and game rooms. Children can only pick a reason (no free text). Look at each one; talk to the parent or remove the account if it is serious.' })}`;
  }
  async function drillInst(id) {
    const r = await get('owner_dash_institution', { p_inst: id }); const i = r.inst || {};
    const t = todayK(), map = Object.fromEntries((r.days || []).map(d => [d.d, d])), days = [];
    for (let k = 29; k >= 0; k--) { const d = addD(t, -k); days.push({ d, users: map[d] ? +map[d].users : 0 }); }
    const clsT = table([{ k: 'name', l: 'Class / batch' }, { k: 'students', l: 'Students', n: 1 }, { k: 'active7', l: 'Active this week', n: 1, f: (v, x) => `${nf(v)} <small>${pctS(pct(v, x.students))}</small>`, t: v => v },
      { k: 'answers30', l: 'Answers (30 days)', n: 1 }, { k: 'right30', l: 'Right', n: 1, f: (v, x) => pctS(pct(v, x.answers30)), t: v => v }, { k: 'homework', l: 'Homework set', n: 1 }],
      r.classes || [], { name: 'classes', label: 'Classes', empty: 'No classes yet.' });
    const clsId = 't' + regN;
    const ordT = table([{ k: 'year', l: 'Year' }, { k: 'students', l: 'Seats', n: 1 }, { k: 'taxable', l: 'Amount (ex-GST)', n: 1, f: v => inr(v), t: v => v }, { k: 'status', l: 'Status' }, { k: 'invoice_no', l: 'Invoice', f: v => esc(v || '–') }, { k: 'valid_until', l: 'Valid till', f: v => esc(fmtD(v)), t: v => v }],
      r.orders || [], { name: 'orders', label: 'Orders', empty: 'No orders yet.' });
    const stT = table([{ k: 'name', l: 'Student', f: (v, x) => `<b>${esc(v || '—')}</b><small>${esc(x.email)}</small>`, t: v => v || '' }, { k: 'class_name', l: 'Class', f: v => esc(v || '–') }, { k: 'last_active', l: 'Last active', f: v => esc(ago(v)), t: v => v || '' },
      { k: 'answered', l: 'Questions', n: 1 }, { k: 'accuracy', l: 'Accuracy', n: 1, f: v => pctS(v), t: v => v == null ? '' : v }, { k: 'streak', l: 'Streak', n: 1 }],
      r.students || [], { name: 'school-students', label: 'Students', empty: 'No students joined yet.', onRow: x => go('student:' + x.id), rowLabel: x => 'Open ' + (x.name || x.email) });
    const stId = 't' + regN;
    const ph = i.contact_phone ? String(i.contact_phone).replace(/[^\d]/g, '') : '';
    return `<div class="pv-card od-prof"><h2>🏫 ${esc(i.name)}</h2><p class="od-mute">${esc([i.type === 'coaching' ? 'Coaching centre' : 'School', i.board, i.city, i.state].filter(Boolean).join(' · '))} · ${esc(i.status === 'pilot' ? 'Pilot ' + (i.pilot_until ? until(i.pilot_until) : '') : i.status)} · ${nf(r.teachers)} teachers</p>
        <p>Coordinator: <b>${esc(i.contact_name || '–')}</b>${i.contact_email ? ` · <a href="mailto:${esc(i.contact_email)}">${esc(i.contact_email)}</a>` : ''}${i.contact_phone ? ` · <a href="tel:${esc(i.contact_phone)}">${esc(i.contact_phone)}</a>` : ''}${(r.admins || []).length ? ' · admins: ' + r.admins.map(esc).join(', ') : ''}</p>
        <div class="od-row">${ph ? `<a class="od-mini" href="https://wa.me/${ph}" target="_blank" rel="noopener">💬 WhatsApp</a><a class="od-mini" href="tel:${esc(i.contact_phone)}">📞 Call</a>` : ''}<button type="button" class="od-mini" data-go="stu:inst=${esc(id)}">🧒 Filter dashboard to this school</button><button type="button" class="od-mini" data-schoolpanel="1">🛠️ Schools panel</button></div></div>
      <div class="od-grid2">
        ${card('⚡ Students active per day (30 days)', colChart(days.map(d => fmtDs(d.d)), days.map(d => d.users), { aria: 'Active students per day', color: COL.s3, unit: 'students' }))}
        ${card('🎒 Classes', clsT, { csv: clsId })}
        ${card('🧒 Students', stT, { csv: stId, cls: 'od-span' })}
        ${card('🧾 Orders', ordT)}
      </div>`;
  }

  /* ================= 🧠 Pulse Coach (follow-ups) ================= */
  const nm = it => first(it.name) || (it.email ? it.email.split('@')[0] : 'your child');
  const sign = '\n\n' + NAME.sign;
  const KIND = {
    trial_end: { i: '⏳', who: 's', t: it => `${nm(it)}'s free trial ends today`, why: it => `The trial ${until(it.due)} and there is no plan yet.`, act: 'Send a friendly note with the plan options.',
      msg: it => `Hello! ${nm(it)}'s free StudyVerse trial ends today.\nIf ${nm(it)} enjoyed the quests and games, you can choose a plan in the app: Me → Plans (prices are + GST as applicable).\nAny question? Just reply to this message.` },
    expiring: { i: '⏰', who: 's', t: it => `${nm(it)}'s plan ${until(it.due)}`, why: it => `${(it.meta && it.meta.plan) || 'The plan'} ends on ${fmtD(it.due)} and has not been renewed.`, act: 'Send a renewal reminder.', code: 1,
      msg: it => `Hello! ${nm(it)}'s StudyVerse plan ends on ${fmtD(it.due)}.\nTo keep the streak, stars and progress going, please renew from Me → Plans.\nThank you for learning with us!` },
    lapsed: { i: '🍂', who: 's', t: it => `${nm(it)}'s plan ended`, why: it => `${(it.meta && it.meta.plan) || 'The plan'} ended on ${fmtD(it.due)} and was not renewed.`, act: 'Win back: ask what would help, offer a one-time renewal discount.', code: 1,
      msg: it => `Hello! We miss ${nm(it)} on StudyVerse. The plan ended on ${fmtD(it.due)}.\nAll progress is saved — ${nm(it)} can continue from where they stopped by renewing from Me → Plans.\nIs there anything we could do better? Your reply helps us a lot.` },
    paid_idle: { i: '😴', who: 's', t: it => `${nm(it)} has a plan but is not studying`, why: it => it.meta && it.meta.last_active ? `Last studied ${ago(it.meta.last_active)} (${it.meta.days} days).` : 'Has not studied yet since getting access.', act: 'Check in gently — maybe they are stuck or forgot.',
      msg: it => `Hello! We noticed ${nm(it)} hasn't opened StudyVerse for a few days.\nJust 10 minutes a day — one topic quest — keeps the streak alive and learning fresh.\nIs anything difficult or not working? Reply and we will help.` },
    falling: { i: '📉', who: 's', t: it => `${nm(it)} is studying less`, why: it => `Active ${it.meta.now7} day(s) this week vs ${it.meta.prev7} the week before.`, act: 'Encourage with a small goal for this week.',
      msg: it => `Hello! ${nm(it)} has been doing well on StudyVerse — a little less this week.\nA small goal can help: 3 short quests this week. The 📅 Exam planner in the Dashboard tab makes a daily plan too.` },
    streak_broken: { i: '🔥', who: 's', t: it => `${nm(it)} just lost a ${it.meta.streak}-day streak`, why: () => 'Missed yesterday — today is the best day to start again.', act: 'Send a cheerful "start again today" note.',
      msg: it => `Hello! ${nm(it)} had a great ${it.meta.streak}-day learning streak on StudyVerse.\nOne quest today starts a new one — it only takes a few minutes! 🔥` },
    frustrated: { i: '😣', who: 's', t: it => `${nm(it)} may be finding questions hard`, why: it => `Only ${it.meta.acc}% right out of ${it.meta.answers} answers this week.`, act: 'Look at their weak topics; suggest revision sheets or easier practice.', profile: 1,
      msg: it => `Hello! ${nm(it)} is working hard on StudyVerse this week. Some topics seem tricky right now.\nThe revision sheets and "Learn" step explain each idea with steps — a quick look before the quiz helps a lot. Reply if you want us to suggest topics.` },
    pay_failed: { i: '💳', who: 's', t: it => `${nm(it)}'s payment did not finish`, why: it => `${(it.meta && it.meta.plan) || 'A plan'} (${inr(it.meta && it.meta.inr)}) was started ${ago(it.due)} but not completed.`, act: 'Offer help to finish the payment.',
      msg: it => `Hello! It looks like the payment for ${(it.meta && it.meta.plan) || 'the StudyVerse plan'} did not complete.\nYou can try again from Me → Plans. If money was deducted, banks usually return it automatically — reply with the payment time and we will check.` },
    parent_idle: { i: '👪', who: 'p', t: it => `Parent of ${(it.meta && it.meta.kids) || 'a student'} hasn't opened the app`, why: it => `Last opened ${it.due ? ago(it.due) : 'never'} — not seeing their child's progress.`, act: 'Remind them about Parent Hub and the weekly report.',
      msg: it => `Hello! You can see ${(it.meta && it.meta.kids) || 'your child'}'s learning progress anytime in StudyVerse Parent Hub: open ${SITE} and sign in with this email.\nYou also get a short weekly report by email.` },
    parent_invite: { i: '📨', who: 'p', t: it => `A parent's invite to ${(it.meta && it.meta.child) || 'their child'} is waiting`, why: it => `Invited ${ago(it.due)}, the child hasn't joined yet.`, act: 'Help the parent: the child must sign in with the invited email.',
      msg: it => `Hello! Your StudyVerse invite for ${(it.meta && it.meta.child) || 'your child'} is still waiting.\nPlease ask them to open ${SITE} and create an account with the same email you entered — it links automatically.` },
    pilot_ending: { i: '🧪', who: 'c', t: it => `${it.name}: pilot ${until(it.due)}`, why: () => 'Free pilot is ending and no order has been placed.', act: 'Call the school coordinator; share results and the next step.',
      msg: it => `Dear ${(it.meta && it.meta.contact) || 'Sir/Madam'},\nYour free StudyVerse pilot at ${it.name} ends on ${fmtD(it.due)}.\nCould we have a 10-minute call to share how your students used it, and the next steps?` },
    pilot_over: { i: '⌛', who: 'c', t: it => `${it.name}: pilot ended, no order`, why: it => `Pilot ended ${ago(it.due)}.`, act: 'Follow up: ask for feedback and offer to continue.',
      msg: it => `Dear ${(it.meta && it.meta.contact) || 'Sir/Madam'},\nThank you for trying StudyVerse at ${it.name}. We would love your feedback on the pilot.\nIf you'd like to continue for your students, we can share the seat options on a short call.` },
    school_renewal: { i: '🏫', who: 'c', t: it => `${it.name}: seats ${until(it.due)}`, why: it => `${nf(it.meta && it.meta.seats)} seats end on ${fmtD(it.due)}.`, act: 'Call the coordinator about renewal for the next year.',
      msg: it => `Dear ${(it.meta && it.meta.contact) || 'Sir/Madam'},\nYour StudyVerse seats at ${it.name} end on ${fmtD(it.due)}. Shall we prepare the renewal for the next academic year?` },
    school_low_use: { i: '🪫', who: 'c', t: it => `${it.name}: low use`, why: it => `${nf(it.meta.students)} of ${nf(it.meta.seats)} seats joined · ${nf(it.meta.active7)} active this week.`, act: 'Offer a short teacher session; share join codes again.',
      msg: it => `Dear ${(it.meta && it.meta.contact) || 'Sir/Madam'},\nOnly a few students at ${it.name} used StudyVerse this week. Can we help? We can run a 15-minute session for teachers, and share the class join codes again.` },
    order_unpaid: { i: '🧾', who: 'c', t: it => `${it.name}: invoice waiting`, why: it => `Invoice ${(it.meta && it.meta.invoice_no) || ''} (${inr(it.meta && it.meta.total)}) sent ${ago(it.due)}, not paid.`, act: 'Send a polite payment reminder.',
      msg: it => `Dear ${(it.meta && it.meta.contact) || 'Sir/Madam'},\nA gentle reminder about StudyVerse invoice ${(it.meta && it.meta.invoice_no) || ''} of ${inr(it.meta && it.meta.total)}. Seats start as soon as it is paid. Thank you!` },
    pilot_request: { i: '📞', who: 'c', t: it => `New pilot request: ${it.name || 'a school'}`, why: it => `${(it.meta && it.meta.contact) || 'Someone'}${it.meta && it.meta.city ? ' from ' + it.meta.city : ''} asked ${ago(it.due)}${it.meta && it.meta.students ? ' (' + it.meta.students + ' students)' : ''}.`, act: 'Call back and set up the pilot (Schools panel → create institution).',
      msg: it => `Dear ${(it.meta && it.meta.contact) || 'Sir/Madam'},\nThank you for asking for a StudyVerse pilot for ${it.name || 'your school'}. When is a good time for a short call to set it up?` },
    report: { i: '🚩', who: 's', t: it => `${it.name || 'A student'} was reported`, why: it => `${({ unkind: 'Unkind or rude behaviour', cheating: 'Cheating', name: 'Rude name or picture', other: 'Something else' })[it.meta && it.meta.reason] || 'A report'} in a ${({ friend: 'friend list', request: 'friend request', room: 'game room' })[it.meta && it.meta.context] || 'friend list'}${it.meta && it.meta.by ? ', reported by ' + it.meta.by : ''}${it.meta && +it.meta.n > 1 ? ` (${it.meta.n} reports in 30 days)` : ''}.${it.meta && it.meta.detail ? ` Note: “${it.meta.detail}”` : ''}`,
      act: 'Read it (Parents & schools → Reports). Talk to the parent, or remove the account if it is serious.' },
    hard_question: { i: '❓', who: 'q', t: () => 'A question most students get wrong', why: it => `Only ${it.meta.acc}% right in ${it.meta.tries} tries (${it.meta.users} students).`, act: 'Read it — fix the wording, options or explanation if needed.' } };
  const PRI = { 1: ['🔴', 'Urgent today'], 2: ['🟠', 'This week'], 3: ['🔵', 'When you can'] };
  const WHO = [['all', 'All'], ['s', 'Students'], ['p', 'Parents'], ['c', 'Schools'], ['q', 'Content']];
  let smartData = null;
  async function smart() {
    const r = smartData = await get('owner_dash_smart', { p: filt() });
    const items = (r.items || []).filter(it => KIND[it.kind]);
    const by = s => items.filter(it => it.state === s);
    const list = by(V.show).filter(it => V.who === 'all' || KIND[it.kind].who === V.who);
    later(b => {
      b.querySelectorAll('[data-show]').forEach(x => x.onclick = () => { V.show = x.dataset.show; keep(); paint(); });
      b.querySelectorAll('[data-who]').forEach(x => x.onclick = () => { V.who = x.dataset.who; keep(); paint(); });
      b.querySelectorAll('[data-all]').forEach(x => x.onclick = () => { V.all = V.all || {}; V.all[x.dataset.all] = !V.all[x.dataset.all]; paint(); });
      b.querySelectorAll('.od-item').forEach(wireItem);
    });
    const im = r.improve || {};
    const hard = await Promise.all((im.hard || []).map(async h => { const i = await topicInfo(h.qid); return `<li><button type="button" class="od-link" data-go="q:${esc(h.qid)}">${i && i.q ? esc(String(i.q.q).slice(0, 90)) : esc(h.qid)}</button> <span class="od-mute">— ${h.acc}% right of ${h.tries}</span></li>`; }));
    const drop = await Promise.all((im.drop || []).map(async d => `<li>${await nameTopic(d.topic)} <span class="od-mute">— left ${d.left_n} of ${d.starts} times</span></li>`));
    const steps = Object.entries(im.steps || {}).sort((a, b) => b[1] - a[1]).slice(0, 3).map(([k, v]) => `${STEPN[k] || k} (${v})`);
    const nobody = +im.tracked ? FEAT.filter(([k]) => !(im.features || {})[k]).map(([k, e, n]) => e + ' ' + n) : [];
    const improve = `<details class="pv-card od-improve" ${V.imp === false ? '' : 'open'}><summary><h3>🛠️ This week: what to improve</h3></summary>
      <div class="od-grid3"><div><h4>Where students stop</h4>${drop.length || steps.length ? `<ol>${drop.join('')}</ol>${steps.length ? `<p class="od-mute">Most often left at: ${esc(steps.join(' · '))}</p>` : ''}` : '<p class="od-mute">Not enough data yet.</p>'}</div>
      <div><h4>Most confusing questions</h4>${hard.length ? `<ol>${hard.join('')}</ol>` : '<p class="od-mute">No question is causing trouble (needs 5+ tries).</p>'}</div>
      <div><h4>Features nobody used (30 days)</h4>${nobody.length ? `<p>${esc(nobody.join(' · '))}</p><p class="od-mute">Make them easier to find, or ask students why.</p>` : `<p class="od-mute">${+im.tracked ? 'Every feature was used. 🎉' : 'Usage tracking starts with the latest app version.'}</p>`}</div></div></details>`;
    const counts = s => by(s).length;
    const head = `<div class="pv-card od-today"><h2>${NAME.coachIcon} ${list.length ? `${nf(by('open').length)} follow-ups today` : V.show === 'open' ? 'All caught up 🎉' : 'Nothing here'}</h2>
      <p class="od-mute">Worked out from your own data with fixed rules — no outside AI. Messages are only prepared; you choose to send them. For children, the message goes to the linked parent when there is one.</p>
      <div class="od-row"><div class="od-seg sm" role="radiogroup" aria-label="Show">${[['open', 'To do'], ['snoozed', 'Snoozed'], ['done', 'Done']].map(([k, n]) => `<button type="button" role="radio" aria-checked="${V.show === k}" class="${V.show === k ? 'on' : ''}" data-show="${k}">${n} (${counts(k)})</button>`).join('')}</div>
      <div class="od-seg sm" role="radiogroup" aria-label="Who">${WHO.map(([k, n]) => `<button type="button" role="radio" aria-checked="${V.who === k}" class="${V.who === k ? 'on' : ''}" data-who="${k}">${n} (${by(V.show).filter(it => k === 'all' || KIND[it.kind].who === k).length})</button>`).join('')}</div></div></div>`;
    const groups = [1, 2, 3].map(p => { const g = list.filter(it => +it.pri === p); if (!g.length) return '';
      const all = V.all && V.all[p], vis = all ? g : g.slice(0, 5);
      return `<section class="od-grp" aria-label="${PRI[p][1]}"><h3 class="od-gh">${PRI[p][0]} ${PRI[p][1]} <span class="od-count">${g.length}</span></h3>${vis.map(itemHTML).join('')}${g.length > 5 ? `<button type="button" class="od-mini od-more-btn" data-all="${p}">${all ? 'Show fewer' : `Show all ${g.length}`}</button>` : ''}</section>`; }).join('');
    return head + (V.show === 'open' ? improve : '') + (groups || `<p class="pv-card od-empty">${V.show === 'open' ? 'Nothing needs you right now. Check again tomorrow.' : 'No items.'}</p>`);
  }
  function itemHTML(it) {
    const K = KIND[it.kind], i = smartIdx(it);
    const to = K.who === 's' ? (it.parents ? 'parent: ' + it.parents.split(',').join(', ') : it.email) : it.email || it.phone || '';
    return `<article class="od-item p${it.pri}" data-i="${i}" aria-label="${esc(K.t(it))}">
      <div class="od-ih"><span class="od-ii" aria-hidden="true">${K.i}</span><div><b>${esc(K.t(it))}</b>${to ? `<small>${esc(to)}${K.who === 's' && it.band ? ' · ' + esc(BANDN[it.band] || '') : ''}</small>` : ''}</div></div>
      <p class="od-why"><b>Why:</b> ${esc(K.why(it))}</p><p class="od-do"><b>Do:</b> ${esc(K.act)}</p>
      ${it.note ? `<p class="od-note">📝 ${esc(it.note)}</p>` : ''}${it.state === 'snoozed' ? `<p class="od-mute">💤 Snoozed till ${esc(fmtD(it.snooze_until))}</p>` : ''}${it.state === 'done' ? `<p class="od-mute">✓ Done ${esc(it.marked_at ? ago(it.marked_at) : '')}</p>` : ''}
      <div class="od-ib">${K.msg ? `<button type="button" class="od-mini od-pri" data-a="prep">✍️ Prepare message</button>` : ''}${K.who === 'q' ? `<button type="button" class="od-mini od-pri" data-go="q:${esc(it.id)}">❓ Open question</button>` : ''}
        ${it.state === 'open' ? `<button type="button" class="od-mini" data-a="done">✓ Done</button>` : `<button type="button" class="od-mini" data-a="open">↩ Back to to-do</button>`}
        <button type="button" class="od-mini" data-a="more" aria-expanded="false">⋯ More</button></div>
      <div class="od-prep" hidden></div>
      <div class="od-more" hidden>
        ${it.state !== 'snoozed' ? `<span class="od-mute">Snooze:</span> <button type="button" class="od-mini" data-a="sn1">1 day</button><button type="button" class="od-mini" data-a="sn3">3 days</button><button type="button" class="od-mini" data-a="sn7">7 days</button>` : ''}
        <button type="button" class="od-mini" data-a="note">📝 Note</button>
        ${K.who === 's' ? `<button type="button" class="od-mini" data-go="student:${esc(it.id)}">👤 Open profile</button>` : ''}${K.who === 'c' && it.kind !== 'pilot_request' ? `<button type="button" class="od-mini" data-go="inst:${esc(it.id)}">🏫 Open school</button>` : ''}
        ${K.code ? `<button type="button" class="od-mini" data-a="code">🎟️ Make a 20% renewal code</button>` : ''}</div></article>`;
  }
  const IDX = []; const smartIdx = it => { IDX.push(it); return IDX.length - 1; };
  function wireItem(el) {
    const it = IDX[+el.dataset.i]; if (!it) return; const K = KIND[it.kind];
    el.querySelectorAll('[data-a]').forEach(b => b.onclick = async () => {
      const a = b.dataset.a;
      if (a === 'more') { const m = el.querySelector('.od-more'); m.hidden = !m.hidden; b.setAttribute('aria-expanded', String(!m.hidden)); return; }
      if (a === 'prep') { prep(el, it, K); return; }
      if (a === 'code') { makeCode(el, it); return; }
      if (a === 'note') { const n = prompt('Note for yourself (only you see it):', it.note || ''); if (n == null) return; await mark(it, it.state === 'open' ? 'open' : it.state, null, n, true); return; }
      if (a === 'done') return mark(it, 'done');
      if (a === 'open') return mark(it, 'open');
      if (/^sn\d$/.test(a)) return mark(it, 'snoozed', +a.slice(2));
    });
  }
  async function mark(it, st, days, note, keepNote) {
    try {
      const r = one(await rpc('owner_followup_set', { p_key: it.key, p_status: st, p_snooze_days: days || null, p_note: keepNote ? (note || '') : (it.note || null) }));
      if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not save.');
      say(st === 'done' ? 'Marked done ✓' : st === 'snoozed' ? `Snoozed for ${days} day${days > 1 ? 's' : ''}` : keepNote ? 'Note saved' : 'Back in to-do');
      [...cache.keys()].filter(k => k.startsWith('owner_dash_smart')).forEach(k => cache.delete(k)); paint();
    } catch (e) { say(errT(e)); }
  }
  function prep(el, it, K) {
    const box = el.querySelector('.od-prep'); if (!box.hidden) { box.hidden = true; return; }
    const to = K.who === 's' ? (it.parents || it.email || '') : (it.email || '');
    const text = K.msg(it) + sign, subj = K.who === 'c' ? 'StudyVerse — ' + (it.name || '') : 'StudyVerse — ' + nm(it);
    const ph = String(it.phone || '').replace(/[^\d]/g, '');
    box.innerHTML = `<label class="od-lbl" for="odM${el.dataset.i}">Message (edit before sending)${K.who === 's' && it.parents ? ' — to the parent' : ''}</label>
      <textarea id="odM${el.dataset.i}" class="pv-in od-ta" rows="6">${esc(text)}</textarea>
      <div class="od-row"><button type="button" class="od-mini od-pri" data-m="copy">📋 Copy</button>${to ? `<a class="od-mini" data-m="mail" href="#">✉️ Email</a>` : ''}<a class="od-mini" data-m="wa" href="#" target="_blank" rel="noopener">💬 WhatsApp</a>${ph ? `<a class="od-mini" href="tel:+${ph}">📞 Call</a>` : ''}</div>
      <p class="od-mute">Opens your own email / WhatsApp with the text ready — you press send. ${ph ? '' : 'WhatsApp: pick the contact yourself.'}</p>`;
    box.hidden = false;
    const ta = box.querySelector('textarea'); ta.focus();
    box.querySelector('[data-m="copy"]').onclick = () => { try { navigator.clipboard.writeText(ta.value); say('Message copied'); } catch (e) { ta.select(); say('Select and copy'); } };
    const ml = box.querySelector('[data-m="mail"]'); if (ml) ml.onclick = e => { e.preventDefault(); location.href = `mailto:${to.split(',').map(encodeURIComponent).join(',')}?subject=${encodeURIComponent(subj)}&body=${encodeURIComponent(ta.value)}`; };
    box.querySelector('[data-m="wa"]').onclick = e => { e.preventDefault(); W.open(`https://wa.me/${ph}?text=${encodeURIComponent(ta.value)}`, '_blank', 'noopener'); };
  }
  async function makeCode(el, it) {
    if (!confirm(`Create a one-time 20% discount code for ${nm(it)}? It works once and ends in 7 days. Nothing is sent — you share it yourself.`)) return;
    const A = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; let code = 'BACK';
    for (let i = 0; i < 6; i++) code += A[Math.floor(Math.random() * A.length)];
    try {
      await C().rest('codes', { method: 'POST', headers: { Prefer: 'return=minimal' }, body: { code, kind: 'discount', percent: 20, max_uses: 1, valid_until: new Date(Date.now() + 7 * DAY).toISOString(), note: (NAME.coach + ' · ' + (it.email || '')).slice(0, 120) } });
      const m = el.querySelector('.od-more'); const p = D.createElement('p'); p.className = 'od-ok'; p.innerHTML = `🎟️ Code <b>${esc(code)}</b> — 20% off, one use, 7 days. <button type="button" class="od-mini" data-copy="${esc(code)}">📋 Copy</button>`; m.appendChild(p);
      say('Code ' + code + ' created');
    } catch (e) { say(errT(e)); }
  }
  D.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-copy]'); if (b && hub && hub.contains(b)) { try { navigator.clipboard.writeText(b.dataset.copy); say('Copied'); } catch (x) {} } });
  D.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-schoolpanel]'); if (b && hub && hub.contains(b) && W.Inst && Inst.owner) leavePulse(() => Inst.owner()); });
  D.addEventListener('keydown', e => {
    if (!hub || !hub.classList.contains('show')) return;
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches && e.target.matches('.od-tr')) { e.preventDefault(); e.target.click(); }
    if (e.key === 'Escape') { e.stopPropagation(); e.preventDefault(); const c = hub.querySelector('#odLeave'); if (c) c.remove(); else if (stack.length) back(); else askLeave(); }
  }, true);

  /* ---------------- styles ---------------- */
  function style() {
    try { if (W.Parent && Parent.lib && Parent.lib.style) Parent.lib.style(); } catch (e) {}
    if (D.getElementById('odCss')) return;
    const s = D.createElement('style'); s.id = 'odCss'; s.textContent = `
.od-hub .od.pv-wrap{max-width:1180px}
.od-hub [hidden]{display:none!important}
.od-sub{display:block;color:#6b675d;font-size:11.5px;font-weight:600}
.od-hero{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;justify-content:space-between;margin:12px 0 4px}
.od-greet{font-family:'Baloo 2',system-ui,sans-serif;font-size:20px;font-weight:800;line-height:1.1}
.od-sumline{font-size:14.5px;color:#4a4740}
.od-search{display:flex;align-items:center;gap:6px;flex:1 1 320px;max-width:460px;background:#fff;border:1.5px solid #cfc3aa;border-radius:12px;padding:0 4px 0 10px;min-height:44px}
.od-search input{flex:1;min-width:0;border:0;outline:0;font-size:16px;background:transparent;min-height:42px;color:#15161C}
.od-search:focus-within{border-color:#5B0F1B;box-shadow:0 0 0 3px rgba(91,15,27,.15)}
.od-search.sm{margin:4px 0 10px;max-width:none}
.od-sbtn{border:0;background:#15161C;color:#F4EAD8;border-radius:9px;font-weight:800;min-height:36px;padding:0 14px;cursor:pointer;font-size:14px}
.od-fbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0 2px}
.od-seg{display:inline-flex;flex-wrap:nowrap;overflow-x:auto;max-width:100%;gap:4px;background:#efe6d4;border-radius:12px;padding:3px}
.od-seg button{min-height:38px;border:0;background:transparent;border-radius:9px;padding:0 11px;font-weight:800;font-size:14px;color:#3c3a35;cursor:pointer}
.od-seg button.on{background:#15161C;color:#F4EAD8}
.od-seg.sm{flex-wrap:wrap}.od-seg button{flex:none}
.od-seg.sm button{min-height:34px;font-size:13.5px;padding:0 9px}
.od-fbtn{min-height:42px;border:1.5px solid #C9A76A;background:#fff;border-radius:12px;padding:0 12px;font-weight:800;font-size:14px;cursor:pointer;color:#15161C}
.od-fbtn.on{border-color:#5B0F1B;color:#5B0F1B;background:#fff6ee}
.od-range{font-size:13px;color:#5d5a52;margin-left:auto}
.od-cust{display:flex;flex-wrap:wrap;gap:8px;align-items:end;margin:8px 0}.od-cust label{display:flex;flex-direction:column;font-size:13px;font-weight:700;gap:2px}
.od-cust input{min-height:40px;border:1.5px solid #cfc3aa;border-radius:10px;padding:0 8px;font-size:15px}
.od-fpanel{background:#fff;border:1px solid #eadfca;border-radius:14px;padding:12px;margin:8px 0}
.od-fgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}
.od-fgrid label{display:flex;flex-direction:column;gap:3px;font-size:13px;font-weight:700;color:#3c3a35}
.od-fgrid select{min-height:42px;border:1.5px solid #cfc3aa;border-radius:10px;padding:0 8px;font-size:15px;background:#fff;color:#15161C}
.od-chips{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:6px 0}
.od-chip{display:inline-flex;align-items:center;gap:2px;background:#15161C;color:#F4EAD8;border-radius:999px;padding:2px 2px 2px 10px;font-size:13px;font-weight:700}
.od-chip button{border:0;background:transparent;color:inherit;min-width:30px;min-height:30px;cursor:pointer;font-size:13px}
.od-tabs{position:sticky;top:64px;z-index:1;background:#F6F0E4;margin:0 -14px;padding:10px 14px 8px}
.od-body{display:grid;gap:12px;padding-top:4px}
.od-body>*{min-width:0}
.od-h2{font-family:'Baloo 2',system-ui,sans-serif;font-size:20px;margin:8px 0 -2px}
.od-kpis{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.od-kpi{position:relative;text-align:left;background:#fff;border:1px solid #eadfca;border-radius:14px;padding:10px 26px 10px 12px;box-shadow:0 2px 8px rgba(21,22,28,.06);cursor:pointer;display:flex;flex-direction:column;gap:2px;min-height:92px;color:#15161C;font:inherit}
.od-kpi:hover,.od-kpi:focus-visible{border-color:#C9A76A;box-shadow:0 4px 14px rgba(21,22,28,.12)}
.od-kpi[data-go=""]{cursor:default}.od-kpi[data-go=""] .od-kgo{display:none}
.od-kl{font-size:12.5px;font-weight:800;color:#5d5a52;line-height:1.2}
.od-kv{font-size:22px;font-family:'Baloo 2',system-ui,sans-serif;line-height:1.15;font-weight:800;word-break:break-word}
.od-ks{font-size:12px;color:#5d5a52;display:flex;flex-wrap:wrap;gap:2px 6px;line-height:1.3}
.od-kgo{position:absolute;right:10px;top:50%;transform:translateY(-50%);color:#b9ad95;font-size:20px}
.od-d{font-weight:800;white-space:nowrap}.od-d.good{color:#1F7A43}.od-d.bad{color:#B71C2C}.od-d.flat{color:#7a766c}
.od-grid2,.od-grid3{display:grid;grid-template-columns:minmax(0,1fr);gap:12px}
.od-card{min-width:0}
.od-ch{display:flex;align-items:flex-start;justify-content:space-between;gap:8px}
.od-ch h3{margin:0 0 4px}
.od-tools{display:flex;gap:6px;flex:none}
.od-sum,.od-foot{font-size:13px!important;color:#5d5a52;margin:2px 0 8px!important;line-height:1.4}
.od-foot{margin:8px 0 0!important}
.od-mini{display:inline-flex;align-items:center;justify-content:center;gap:4px;min-height:36px;border:1.5px solid #cfc3aa;background:#fff;border-radius:10px;padding:0 10px;font-weight:800;font-size:13.5px;cursor:pointer;color:#15161C;text-decoration:none;font-family:inherit}
.od-mini:disabled{opacity:.45;cursor:default}
.od-mini.od-pri{background:#15161C;color:#F4EAD8;border-color:#15161C}
.od-link{text-align:left;border:0;background:none;color:#5B0F1B;font-weight:800;cursor:pointer;text-decoration:underline;font-size:inherit;padding:4px 2px;min-height:32px}
.od-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.od-mt{margin-top:2px}
.od-mute{color:#5d5a52;font-size:13px}
.od-count{display:inline-block;background:#efe6d4;border-radius:999px;padding:0 9px;font-size:13px;font-family:Nunito,system-ui,sans-serif;vertical-align:middle;color:#3c3a35}
.od-verdict{font-size:15px;line-height:1.5;border-left:5px solid #C9A76A}
.od-svg{width:100%;height:auto;display:block;overflow:visible}
.od-svg .od-grid{stroke:#e7dfcf;stroke-width:1}.od-svg .od-ax{font-size:11px;fill:#6b675d;font-family:Nunito,system-ui,sans-serif}
.od-svg .od-hit{cursor:pointer}.od-svg .od-hit:hover{fill:rgba(21,22,28,.05)}
.od-leg{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:13px;font-weight:700;margin:0 0 4px;color:#3c3a35}.od-leg i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.od-hb{list-style:none;margin:0;padding:0;display:grid;gap:4px}
.od-hbr{width:100%;display:grid;grid-template-columns:minmax(90px,38%) 1fr 72px;gap:8px;align-items:center;background:none;border:0;border-radius:10px;padding:5px 6px;text-align:left;font:inherit;color:#15161C;min-height:40px}
button.od-hbr{cursor:pointer}button.od-hbr:hover,button.od-hbr:focus-visible{background:#f6f0e4}
.od-hbl{font-size:13.5px;font-weight:700;line-height:1.25;overflow-wrap:anywhere}
.od-hbt{height:12px;background:#f1ebdf;border-radius:4px;overflow:hidden}.od-hbf{display:block;height:100%;border-radius:0 4px 4px 0}
.od-hbv{font-weight:800;font-size:14px;text-align:right;white-space:nowrap}.od-hbv small{display:block;font-weight:600;font-size:11.5px;color:#5d5a52}
.od-tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:10px;border:1px solid #eee5d4}
.od-t{border-collapse:collapse;width:100%;font-size:13.5px;min-width:100%}
.od-t th,.od-t td{padding:8px 10px;text-align:left;border-bottom:1px solid #f0e9dc;vertical-align:top;white-space:nowrap}
.od-t thead th{background:#faf6ee;font-size:12.5px;color:#4a4740;position:sticky;top:0}
.od-t tbody th{font-weight:600;white-space:normal;min-width:150px;position:sticky;left:0;background:#fff;z-index:0}
.od-t small{display:block;color:#6b675d;font-size:11.5px;font-weight:600;white-space:normal}
.od-t .n{text-align:right}.od-t th.n button{text-align:right}
.od-tr{cursor:pointer}.od-tr:hover td,.od-tr:hover th,.od-tr:focus td,.od-tr:focus th{background:#fbf6ea}.od-tr:focus{outline:2px solid #5B0F1B;outline-offset:-2px}
.od-th{border:0;background:none;font:inherit;font-weight:800;color:inherit;cursor:pointer;padding:0;min-height:28px}
.od-pager{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:8px;font-size:13px;flex-wrap:wrap}
.od-st{display:inline-block;border-radius:999px;padding:1px 8px;font-size:12px;font-weight:800;background:#eee;color:#333}
.od-st.st-paid{background:#e3eefc;color:#184f95}.od-st.st-school{background:#dff5ec;color:#11683f}.od-st.st-trial{background:#fff1d6;color:#7a5200}
.od-st.st-free{background:#efe9fb;color:#4b3aa1}.od-st.st-lapsed,.od-st.st-trial_ended{background:#f6e3e3;color:#8f1d1d}.od-st.st-none{background:#eee;color:#555}
.od-bad{color:#B71C2C;font-weight:800}.od-good{color:#1F7A43;font-weight:800}
.od-pbar{display:inline-block;width:46px;height:8px;background:#f1ebdf;border-radius:4px;margin-right:6px;vertical-align:middle;overflow:hidden}.od-pbar i{display:block;height:100%;background:#2a78d6}
.od-heat{border-collapse:separate;border-spacing:2px;font-size:12px;width:100%}
.od-heat th{font-weight:700;color:#4a4740;padding:4px;white-space:nowrap;text-align:left}.od-heat thead th{text-align:center;font-size:11.5px}
.od-heat td{text-align:center;padding:6px 2px;border-radius:5px;min-width:34px;font-weight:700;cursor:default}.od-heat td.od-hx{background:transparent}
.od-ramp{display:flex;align-items:center;gap:2px;font-size:11.5px;color:#5d5a52;margin-top:6px;justify-content:flex-end}.od-ramp i{width:18px;height:10px;display:inline-block;border-radius:2px}.od-ramp span{margin:0 4px}
.od-empty{color:#5d5a52;font-size:14px;margin:4px 0}
.od-moreb summary{cursor:pointer;font-weight:800;color:#5B0F1B;min-height:40px;display:flex;align-items:center;font-size:14px}
.od-err{color:#B71C2C;font-weight:700}
.od-priv{font-size:12.5px;color:#5d5a52;margin:16px 0 0;line-height:1.45}
.od-tip{position:fixed;z-index:1000;max-width:280px;background:#15161C;color:#F4EAD8;font-size:13px;line-height:1.35;padding:7px 10px;border-radius:9px;pointer-events:none;box-shadow:0 6px 18px rgba(0,0,0,.25)}
.od-prof h2{margin:0}.od-prof p{margin:4px 0 8px}
.od-list{margin:4px 0;padding-left:18px;font-size:14px;line-height:1.6}
.od-q{font-size:17px;font-weight:700}.od-opts li{margin:4px 0}.od-right{color:#1F7A43;font-weight:800}
.od-today h2{margin:0 0 4px}.od-today .od-row{margin-top:8px}
.od-improve summary{cursor:pointer;list-style:none}.od-improve summary::-webkit-details-marker{display:none}.od-improve summary h3{display:inline}.od-improve summary h3::after{content:' ▾';color:#9a958a}
.od-improve ol{margin:4px 0;padding-left:20px;font-size:14px;line-height:1.5}.od-improve h4{margin:10px 0 4px}
.od-grp{display:grid;gap:10px}.od-gh{font-family:'Baloo 2',system-ui,sans-serif;font-size:18px;margin:8px 0 0}
.od-item{background:#fff;border:1px solid #eadfca;border-left:5px solid #9ec5f4;border-radius:14px;padding:12px 14px;box-shadow:0 2px 8px rgba(21,22,28,.05)}
.od-item.p1{border-left-color:#B71C2C}.od-item.p2{border-left-color:#eda100}
.od-ih{display:flex;gap:10px;align-items:flex-start}.od-ii{font-size:24px;line-height:1}.od-ih b{font-size:15.5px;display:block}.od-ih small{display:block;color:#5d5a52;font-size:12.5px;overflow-wrap:anywhere}
.od-why,.od-do{margin:6px 0 0;font-size:14px;line-height:1.4}.od-note{margin:6px 0 0;font-size:13.5px;background:#fff8e6;border-radius:8px;padding:6px 8px}
.od-ib,.od-more{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:10px}
.od-prep{margin-top:10px}.od-ta{font-family:Nunito,system-ui,sans-serif!important;font-size:15px;line-height:1.4;resize:vertical}.od-lbl{display:block;font-size:13px;font-weight:800;margin-bottom:4px}
.od-ok{background:#e9f6ee;border-radius:8px;padding:6px 8px;font-size:14px;width:100%;margin:6px 0 0}
.od-me .btn{margin-top:4px}
.od-kc{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 6px;font-size:12px;line-height:1.3}.od-was{color:#5d5a52}
.od-cmpnote{font-size:12.5px;color:#5d5a52;margin:0 0 -4px}
.od-sticky{display:contents}
.od-check{display:flex;gap:8px;align-items:flex-start;font-size:14px;font-weight:700;margin:10px 0 2px;line-height:1.35}.od-check input{width:20px;height:20px;flex:none;margin:1px 0 0}
.od-chip-t{background:#7a5200}
.od-cards{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.od-ci{position:relative;background:#fff;border:1px solid #eadfca;border-radius:12px;padding:10px 30px 10px 12px;font-size:13.5px;line-height:1.35}
.od-ci.od-tr{cursor:pointer}.od-ci.od-tr:active,.od-ci.od-tr:focus{background:#fbf6ea}
.od-cgo{position:absolute;right:10px;top:50%;transform:translateY(-50%);color:#b9ad95;font-size:20px}
.od-ct b{display:block;font-size:15px}.od-ct small,.od-ct .od-sub{display:block;color:#6b675d;font-size:12px;overflow-wrap:anywhere}
.od-ct{font-weight:700;overflow-wrap:anywhere}
.od-ckv{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 12px;margin:6px 0 0}.od-ckv div{min-width:0}
.od-ckv dt{font-size:11px;color:#6b675d;font-weight:700}.od-ckv dd{margin:0;font-weight:700;overflow-wrap:anywhere}.od-ckv dd small{display:block;font-weight:600;color:#6b675d;font-size:11.5px}
.od-cline{color:#3c3a35;margin-top:4px}
.od-cfoot{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:center;margin-top:6px;font-size:12.5px;color:#3c3a35}
.od-sortrow{margin:0 0 8px}.od-sel{min-height:38px;border:1.5px solid #cfc3aa;border-radius:10px;padding:0 8px;font-size:14px;background:#fff;color:#15161C}
.od-tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:8px;margin-top:8px}
.od-tile{display:flex;flex-direction:column;align-items:flex-start;gap:1px;background:#faf6ee;border:1px solid #eee5d4;border-radius:12px;padding:8px 10px;font:inherit;color:#15161C;text-align:left;min-height:64px}
button.od-tile{cursor:pointer}button.od-tile:hover,button.od-tile:focus-visible{border-color:#C9A76A}
.od-tile b{font-size:18px;font-family:'Baloo 2',system-ui,sans-serif;line-height:1.1}.od-tile small{font-size:11.5px;color:#5d5a52;line-height:1.25}
.od-h4{margin:14px 0 0;font-size:14px}
.od-rank{list-style:none;margin:0;padding:0;display:grid;gap:2px}
.od-rank li{display:grid;grid-template-columns:22px 24px minmax(0,1.6fr) minmax(50px,1fr) 44px;gap:8px;align-items:center;padding:6px 4px;border-radius:10px}
.od-rank li:hover,.od-rank li:focus{background:#f6f0e4;outline:none}
.od-rn{font-size:12px;color:#8a857a;font-weight:800;text-align:right}.od-ri{font-size:18px;text-align:center}
.od-rname{font-weight:700;font-size:13.5px;line-height:1.2;min-width:0}.od-rname small{display:block;font-weight:600;font-size:11.5px;color:#6b675d}
.od-rbar{height:10px;background:#f1ebdf;border-radius:4px;overflow:hidden}.od-rbar span{display:block;height:100%;background:#2a78d6;border-radius:0 4px 4px 0}
.od-rp{text-align:right;font-size:14px}
.od-chiprow{display:flex;flex-wrap:wrap;gap:6px;padding:4px 0}
.od-chip2{display:inline-flex;align-items:center;gap:4px;background:#f1ebdf;border-radius:999px;padding:4px 10px;font-size:12.5px;font-weight:700;color:#3c3a35}
.od-lf{opacity:.8}.od-leg i{width:14px}
.od-confirm{position:fixed;inset:0;z-index:1001;background:rgba(21,22,28,.45);display:flex;align-items:flex-end;justify-content:center;padding:16px}
.od-cbox{background:#fff;border-radius:18px;padding:18px;max-width:420px;width:100%;box-shadow:0 10px 40px rgba(0,0,0,.3)}
.od-cbox h2{margin:0 0 4px;font-family:'Baloo 2',system-ui,sans-serif}.od-cbox p{margin:0 0 14px;color:#4a4740}
.od-cbox .od-row>*{flex:1}.od-big{min-height:48px;font-size:16px}
@media (min-width:700px){.od-confirm{align-items:center}}
@media (min-width:700px){.od-kpis{grid-template-columns:repeat(3,minmax(0,1fr))}.od-grid3{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (min-width:1000px){.od-kpis{grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}.od-grid2{grid-template-columns:repeat(2,minmax(0,1fr))}.od-grid2>.od-span,.od-body>.od-wide{grid-column:1/-1}.od-kv{font-size:24px}}
/* desktop / big screens: use the whole width (Pulse is its own full-screen layer, whatever the app shell does) */
@media (min-width:1024px){
  .od-hub .od.pv-wrap{max-width:none;padding:0 32px 32px}
  .od-hub .od .pv-top{margin:0 -32px;padding:10px 32px}
  .od-sticky{display:block;position:sticky;top:64px;z-index:3;background:#F6F0E4;margin:0 -32px;padding:0 32px;box-shadow:0 6px 10px -10px rgba(21,22,28,.35)}
  .od-sticky .od-tabs{position:static;margin:0;padding:8px 0 10px}
  .od-kpis{grid-template-columns:repeat(4,minmax(0,1fr))}
  .od-tiles{grid-template-columns:repeat(auto-fill,minmax(130px,1fr))}
}
@media (min-width:1400px){.od-kpis{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media (min-width:1024px){.od-grid2>.od-span2{grid-column:1/-1}}
@media (min-width:1700px){.od-grid2>.od-span2{grid-column:span 2}.od-kpis{grid-template-columns:repeat(6,minmax(0,1fr))}.od-grid2{grid-template-columns:repeat(3,minmax(0,1fr))}.od-grid3{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (forced-colors:active){.od-hbf,.od-pbar i{background:CanvasText!important}.od-heat td{border:1px solid CanvasText}}
`;
    D.head.appendChild(s);
  }

  /* ---------------- start ---------------- */
  function start() { hookGlobals(); watch(); W.addEventListener('sv-access', placeSoon); }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', start); else start();
  W.addEventListener('load', hookGlobals);
  W.Owner = { open, close, rec, _features: FEAT, _hook: hookGlobals, _place: placeCard };
})();
