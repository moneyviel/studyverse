/* ================= StudyVerse Parent Hub =================
   Parents follow and guide a child's study; the child's app shows the parent's goal and keeps healthy limits.
   1. Time tracking (child's app): active study minutes per local day in ST.time = { 'YYYY-MM-DD': minutes }.
      Counts in 15-second steps, only while the page is visible and the student touched it in the last 60 s.
      Keeps the last 60 days. Saved with the app's save(), so js/cloud.js syncs it with the rest of the progress.
   2. Me screen card (school #s-me and the CA profile): "I'm a parent — open Parent Hub" and "Link to my parent".
      Also a small card on the first onboarding screen so a parent's own account does not need a grade first.
   3. Parent Hub (full-screen dialog; Back closes it): one tab per linked child, "+ Add child" makes a 2-day code.
      Per child — this week (minutes chart, totals, streak, questions and accuracy vs last week, last active),
      strengths / needs help / scope to improve, dinner-table questions, exam planner, goals & rewards,
      healthy use (daily limit, quiet hours, break reminder, 4-digit PIN), alerts, weekly report (WhatsApp, print/PDF).
      Everything is computed from the child's synced progress (my_children.state.st); nothing is invented.
      All parent settings live in one controls object saved with rpc/set_child_controls:
        { v:1, goal: minutes/day, reward: { text, days }, limit: minutes/day, quiet: { on, from:'HH:MM', to:'HH:MM' },
          brk: minutes, pinHash: SHA-256 hex of 'studyverse-pin:<child id>:<PIN>', exams: [{ id, name, date, subjects }] }
   4. Child side: when linked (rpc/my_controls → parents > 0) the controls are fetched on start and every 3 minutes
      (cached in localStorage sv_pctl). Shows "Today's goal" on World / Me, a break reminder, and a friendly
      "Time to rest" screen when the daily limit is used up or during quiet hours. "My parent is here" + the parent's
      PIN unlocks for 15 minutes (sv_punlock). The owner account (Cloud.admin()) is never blocked.
   Server: rpc/create_link_code, redeem_link_code, my_children, set_child_controls, my_controls, unlink (schema studyverse).
   No ads, no tracking beyond the minutes above; only a linked parent can read the child's progress (server side). */
(function () {
  'use strict';
  const D = document, R = D.documentElement, LS = localStorage, DAY = 864e5;
  const SITE = 'https://study.moneyviel.com';
  const CK = 'sv_pctl', UK = 'sv_punlock';
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const say = m => { try { toast(m); } catch (e) {} };
  const C = () => window.Cloud || null;
  const S = () => { try { return ST; } catch (e) { return null; } };
  const persist = () => { try { save(); } catch (e) {} };
  const jget = (k, d) => { try { const v = JSON.parse(LS.getItem(k)); return v == null ? d : v; } catch (e) { return d; } };
  const jset = (k, v) => { try { v == null ? LS.removeItem(k) : LS.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const demo = () => { try { return !!LS.getItem('sv_demo'); } catch (e) { return false; } };
  const signedIn = () => !!(C() && C().signedIn() && !demo());
  const isOwner = () => !!(C() && C().admin());
  const isParentAcct = () => !!(signedIn() && C().isParent && C().isParent());   // account chose "Parent" at sign-up
  const canHub = () => isParentAcct() || isOwner();                              // students never open the hub; the owner can, for testing
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  const pad2 = n => String(n).padStart(2, '0');
  const dk = t => { const d = new Date(t); return `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`; };   // local day key
  const todayK = () => dk(Date.now());
  const noon = () => { const d = new Date(); d.setHours(12, 0, 0, 0); return d.getTime(); };
  const daysBack = n => { const b = noon(), out = []; for (let i = n - 1; i >= 0; i--) out.push(dk(b - i * DAY)); return out; };   // oldest first, ends today
  const dayDate = k => new Date(k + 'T12:00:00');
  const fmtDay = k => dayDate(k).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
  const wkDay = k => dayDate(k).toLocaleDateString('en-IN', { weekday: 'short' });
  const fmtMin = m => { m = Math.round(m || 0); return m < 60 ? `${m} min` : `${Math.floor(m / 60)} h${m % 60 ? ' ' + (m % 60) + ' min' : ''}`; };
  const pctS = v => v == null ? '–' : Math.round(v) + '%';
  const daysTo = date => Math.round((new Date(date + 'T12:00:00') - noon()) / DAY);
  const ago = iso => {
    if (!iso) return 'never synced';
    const t = new Date(iso), ms = Date.now() - t; if (isNaN(ms)) return '–';
    const time = t.toLocaleTimeString('en-IN', { hour: 'numeric', minute: '2-digit' });
    if (dk(t) === todayK()) return ms < 5 * 6e4 ? 'just now' : 'today, ' + time;
    if (dk(t) === dk(noon() - DAY)) return 'yesterday, ' + time;
    const d = Math.round((noon() - new Date(dk(t) + 'T12:00:00')) / DAY);
    return `${d} days ago (${t.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })})`;
  };
  async function sha256(txt) {
    const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(txt));
    return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
  }
  const pinHash = (childId, pin) => sha256(`studyverse-pin:${childId}:${pin}`);
  const rpc = (name, body) => C().rest('rpc/' + name, { method: 'POST', body: body || {} });
  const one = r => Array.isArray(r) ? r[0] : r;

  /* ================= 1. time tracking (child's app) ================= */
  let lastInput = Date.now(), lastActive = 0, cont = 0;
  ['pointerdown', 'keydown', 'touchstart', 'wheel', 'scroll'].forEach(e => addEventListener(e, () => { lastInput = Date.now(); }, { passive: true, capture: true }));
  function timeObj(s) { if (!s.time || typeof s.time !== 'object' || Array.isArray(s.time)) s.time = {}; return s.time; }
  function prune(T) { const cut = daysBack(60)[0]; Object.keys(T).forEach(k => { if (k < cut) delete T[k]; }); }
  function tick() {
    const s = S(); if (!s || !s.profile) return;
    const now = Date.now();
    const active = D.visibilityState === 'visible' && now - lastInput <= 60000 && !hubOpen() && !restOn();
    if (active) {
      const T = timeObj(s), k = todayK(), before = +T[k] || 0;
      T[k] = Math.round((before + 0.25) * 100) / 100;
      if (now - lastActive > 5 * 6e4) cont = 0;
      lastActive = now; cont += 0.25;
      if (Math.floor(T[k]) !== Math.floor(before)) { prune(T); persist(); }
      breakCheck();
    } else if (now - lastActive > 5 * 6e4) cont = 0;          // a 5-minute pause counts as a break
    enforce(); paintGoal();
  }
  setInterval(tick, 15000);
  D.addEventListener('visibilitychange', () => { if (D.visibilityState === 'hidden') persist(); else { pullControls(); enforce(); } });

  /* ================= data helpers (work on any ST object: the child's own or a synced one) ================= */
  const minutesOn = (s, d) => {
    if (!s) return 0;
    if (s.time && s.time[d] != null) return +s.time[d] || 0;
    const a = s.ins && s.ins.day && s.ins.day[d] ? (s.ins.day[d].s || 0) / 60 : 0;        // older saves: time tracked by insights / CA
    const b = s.ca && s.ca.time && s.ca.time[d] ? s.ca.time[d] / 60 : 0;
    return Math.max(a, b);
  };
  function caAnswersByDay(s) {
    const out = {}; const l = s && s.ca && Array.isArray(s.ca.mlog) ? s.ca.mlog : [];
    l.forEach(x => { const d = dk(x[0] * 6e4), o = out[d] || (out[d] = { a: 0, r: 0 }); o.a++; if (x[2]) o.r++; });
    return out;
  }
  function answersOn(s, d, caDays) {
    const i = s && s.ins && s.ins.day && s.ins.day[d] || null, c = caDays[d] || null;
    return { a: (i ? i.a || 0 : 0) + (c ? c.a : 0), r: (i ? i.r || 0 : 0) + (c ? c.r : 0) };
  }
  function goalStreak(s, goal) {           // days in a row with the goal met (today counts once met; an unmet today does not break it)
    if (!goal) return 0; const ds = daysBack(60); let n = 0;
    for (let i = ds.length - 1; i >= 0; i--) { const met = minutesOn(s, ds[i]) >= goal; if (met) n++; else if (i === ds.length - 1) continue; else break; }
    return n;
  }
  const inQuiet = (from, to, now = new Date()) => {
    const m = now.getHours() * 60 + now.getMinutes(), p = t => { const [h, mi] = String(t).split(':').map(Number); return h * 60 + (mi || 0); };
    const a = p(from), b = p(to); if (a === b) return false;
    return a < b ? m >= a && m < b : m >= a || m < b;
  };
  function nextExam(c) { const ex = (c && Array.isArray(c.exams) ? c.exams : []).filter(e => e.date && daysTo(e.date) >= 0).sort((a, b) => a.date < b.date ? -1 : 1); return ex[0] || null; }

  /* ================= 4. child side: controls, goal card, limits ================= */
  const myId = () => { const u = C() && C().user(); return u ? u.id : null; };
  function ctl() {
    if (!signedIn()) return null;
    const j = jget(CK, null); if (!j || !(j.parents > 0)) return null;
    if (j.uid && myId() && j.uid !== myId()) return null;
    return j.controls || {};
  }
  let pulling = false;
  async function pullControls() {
    if (!signedIn() || pulling || isParentAcct()) return; pulling = true;
    try {
      const o = one(await rpc('my_controls'));
      if (o && o.parents > 0) jset(CK, { controls: o.controls || {}, parents: o.parents, at: Date.now(), uid: myId() });
      else jset(CK, null);
      enforce(); paintGoal(); paintMe();
    } catch (e) { /* offline: keep the cached controls */ }
    finally { pulling = false; }
  }

  function goalHTML() {
    const c = ctl(), s = S(); if (!c || !s || !s.profile) return '';
    const goal = +c.goal || 0, rw = c.reward && c.reward.text ? c.reward : null, ex = nextExam(c);
    if (!goal && !rw && !ex) return '';
    const m = Math.floor(minutesOn(s, todayK())), parts = [];
    let bar = '';
    if (goal) {
      const done = m >= goal;
      parts.push(`<b>🎯 Today's goal: ${Math.min(m, goal)}/${goal} min</b>${done ? ' ✅' : ''}`);
      bar = `<div class="pv-gbar" role="progressbar" aria-label="Today's goal" aria-valuemin="0" aria-valuemax="${goal}" aria-valuenow="${Math.min(m, goal)}"><i style="width:${Math.min(100, Math.round(m / goal * 100))}%"></i></div>`;
    }
    if (rw) { const days = +rw.days || 7, gs = goalStreak(s, goal); parts.push(`🎁 Reward: ${esc(rw.text)} after ${days}-day streak${goal ? ` · ${Math.min(gs, days)}/${days} days` : ''}${goal && gs >= days ? ' — earned! 🎉' : ''}`); }
    if (ex) { const n = daysTo(ex.date); parts.push(`📅 ${esc(ex.name)} in ${n} day${n === 1 ? '' : 's'}`); }
    return `<div class="pv-goal-t">${parts[0]}</div>${bar}${parts.slice(1).map(p => `<div class="pv-goal-l">${p}</div>`).join('')}<div class="pv-goal-by">Set by your parent</div>`;
  }
  function placeGoal(host, after) {
    const h = goalHTML(); let b = host.querySelector(':scope > .pv-goal:not(.pv-mission)');
    if (!h) { if (b) b.remove(); return; }
    if (!b) { style(); b = D.createElement('div'); b.className = 'card pv-goal'; b.setAttribute('role', 'status'); after ? after.after(b) : host.prepend(b); }
    if (b.dataset.h !== h) { b.dataset.h = h; b.innerHTML = h; }
  }
  /* parent's focus topic → "Today's mission" card (World for school, CA home for CA) */
  const fMatch = (fid, id) => { if (!id) return false; const m = /^(\d+)-([a-z]+)-(\d+)$/.exec(fid);
    if (m) { const t = /^g(\d+)-([a-z]+)-(\d+)/.exec(id); return !!t && +t[1] === +m[1] && t[2] === m[2] && +t[3] === +m[3]; }
    return id === fid || id.startsWith(fid + '-'); };
  const fDone = (s, f) => { const d = s && s.focusDone && s.focusDone[f.id], sd = f.set_at ? dk(new Date(f.set_at)) : ''; return typeof d === 'string' && d >= sd ? d : null; };
  function myFocus() {
    const c = ctl(), s = S(), f = c && c.focus; if (!f || !f.id || !s || !s.profile) return null;
    const school = /^\d+-[a-z]+-\d+$/.test(f.id); if (school === (s.profile.course === 'ca')) return null;   // a mission for the other course
    return f;
  }
  function focusCheck() {          // done = 3+ answers (or a finished quest) in the mission chapter / unit after the parent set it
    const f = myFocus(), s = S(); if (!f || fDone(s, f)) return;
    const setMin = Math.floor(new Date(f.set_at || 0).getTime() / 6e4) || 0, sd = dk(setMin * 6e4);
    const count = l => { let n = 0; if (Array.isArray(l)) for (let i = l.length - 1; i >= 0; i--) { const x = l[i]; if (!Array.isArray(x) || x[0] < setMin) break; if (fMatch(f.id, String(x[1] || '').split('#')[0])) n++; } return n; };
    const n = Math.max(count(s.ans) + count(s.ca && s.ca.mlog), count(s.ins && s.ins.att));
    const quest = Object.entries(s.topics || {}).some(([tid, t]) => t && t.last && t.last >= sd && fMatch(f.id, tid));
    if (n >= 3 || quest) { if (!s.focusDone || typeof s.focusDone !== 'object') s.focusDone = {}; s.focusDone[f.id] = todayK(); persist(); }
  }
  function missionHTML() {
    const f = myFocus(); if (!f) return '';
    const done = fDone(S(), f);
    return `<div class="pv-goal-t">🎯 <b>Today's mission from your parent:</b> ${esc(f.title)}</div>${f.subject ? `<div class="pv-goal-l">${esc(f.subject)}</div>` : ''}
      ${done ? '<p class="pv-mis-ok">✅ Mission done — well done! Your parent can see it.</p>' : ''}
      <button type="button" class="btn${done ? ' ghost' : ''} pv-mis-go" data-pvmis>${done ? 'Practise again' : 'Practise now ▶'}</button>`;
  }
  async function openMission() {
    const f = myFocus(), s = S(); if (!f) return;
    const m = /^(\d+)-([a-z]+)-(\d+)$/.exec(f.id);
    if (!m) { if (window.Ca && Ca.unit) Ca.unit(f.id, 'mcq'); return; }
    if (+m[1] !== +s.profile.grade) { say(`This chapter is from Grade ${m[1]}. Ask your parent to choose one from Grade ${s.profile.grade}.`); return; }
    try {
      const d = await subjectData(+m[1], m[2]), ci = d ? d.chapters.findIndex(x => +x.n === +m[3]) : -1;
      if (ci < 0) { say('This chapter is coming soon.'); return; }
      (window.chapterScreen || chapterScreen)(m[2], ci);
    } catch (e) { say('Could not open the chapter. Please try again.'); }
  }
  function placeMission(host, after) {
    const h = missionHTML(); let b = host.querySelector(':scope > .pv-mission');
    if (!h) { if (b) b.remove(); return; }
    if (!b) { style(); b = D.createElement('div'); b.className = 'card pv-goal pv-mission'; b.setAttribute('role', 'region'); b.setAttribute('aria-label', "Today's mission from your parent"); }
    if (after && after.nextElementSibling !== b) after.after(b); else if (!after && !b.isConnected) host.prepend(b);
    if (b.dataset.h !== h) { b.dataset.h = h; b.innerHTML = h; b.querySelector('[data-pvmis]').onclick = openMission; }
  }
  function paintGoal() {
    try { focusCheck(); } catch (e) {}
    const w = D.getElementById('s-world');
    if (w && w.querySelector('#worldTitle')) { placeGoal(w, w.querySelector('#worldTitle')); placeMission(w, w.querySelector(':scope > .pv-goal:not(.pv-mission)') || w.querySelector('#worldTitle')); }
    const me = D.getElementById('s-me'); if (me && me.firstElementChild) placeGoal(me, me.querySelector(':scope > .card:not(.pv-goal)'));
    const ca = D.getElementById('s-ca');
    if (ca && (ca.querySelector('.ca-journey') || ca.querySelector('.ca-prof'))) {
      placeGoal(ca, ca.querySelector(':scope > .card:not(.pv-goal)'));
      if (ca.querySelector('.ca-journey')) placeMission(ca, ca.querySelector(':scope > .pv-goal:not(.pv-mission)') || ca.querySelector(':scope > .card:not(.pv-goal)'));
      else { const m = ca.querySelector(':scope > .pv-mission'); if (m) m.remove(); }
    } else if (ca) ca.querySelectorAll(':scope > .pv-goal').forEach(b => b.remove());
  }

  /* break reminder */
  function breakCheck() {
    const c = ctl(); if (!c || isOwner()) return; const n = +c.brk || 0;
    if (n > 0 && cont >= n) { cont = 0; banner(`⏸️ You have studied ${n} minutes. Take a 5-minute break — stretch, drink water, rest your eyes. 💧`); }
  }
  function banner(t) {
    style(); let b = D.getElementById('pvBanner');
    if (!b) { b = D.createElement('div'); b.id = 'pvBanner'; b.setAttribute('role', 'status'); D.body.appendChild(b); }
    b.innerHTML = `<span>${esc(t)}</span><button type="button" aria-label="Close reminder">OK</button>`; b.classList.add('show');
    b.querySelector('button').onclick = () => b.classList.remove('show');
    clearTimeout(banner.t); banner.t = setTimeout(() => b.classList.remove('show'), 12000);
  }

  /* daily limit + quiet hours → rest screen */
  function blockReason() {
    const c = ctl(), s = S(); if (!c || isOwner() || !s || !s.profile) return null;
    if ((+jget(UK, 0) || 0) > Date.now()) return null;
    const q = c.quiet; if (q && q.on && q.from && q.to && inQuiet(q.from, q.to)) return { kind: 'quiet', q };
    const lim = +c.limit || 0; if (lim > 0 && minutesOn(s, todayK()) >= lim) return { kind: 'limit', lim };
    return null;
  }
  const restOn = () => !!D.getElementById('pvRest');
  let fails = 0, waitTill = 0;
  function enforce() {
    const r = blockReason(), el = D.getElementById('pvRest');
    if (!r) { if (el) { el.remove(); const a = D.querySelector('.app'); if (a && a.dataset.pvInert) { a.inert = false; delete a.dataset.pvInert; } } return; }
    const key = r.kind + (r.q ? r.q.from + r.q.to : r.lim);
    if (el && el.dataset.k === key) return;
    showRest(r, key);
  }
  function showRest(r, key) {
    style(); let el = D.getElementById('pvRest');
    if (!el) { el = D.createElement('div'); el.id = 'pvRest'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-labelledby', 'pvRestT'); D.body.appendChild(el); }
    el.dataset.k = key;
    const s = S(), m = Math.floor(minutesOn(s, todayK())), c = ctl() || {};
    const why = r.kind === 'quiet' ? `It's quiet time (${esc(r.q.from)}–${esc(r.q.to)}). Sleep helps your brain remember what you learnt today.` : `You have used today's study time (${r.lim} min). Your brain needs rest to remember what you learnt.`;
    const back = r.kind === 'quiet' ? `See you after ${esc(r.q.to)}!` : 'See you tomorrow!';
    el.innerHTML = `<div class="pv-rest-in"><div class="pv-moon" aria-hidden="true">🌙</div><h1 id="pvRestT">Time to rest — great work today!</h1>
      <p>${why}</p><p class="pv-rest-m">${m ? `You studied <b>${fmtMin(m)}</b> today ⭐` : ''}</p><p>${back}</p>
      <button type="button" class="pv-rest-b" id="pvHere">My parent is here</button>
      <div id="pvPinBox" hidden>${c.pinHash ? `<label for="pvPinIn">Parent's 4-digit PIN</label>
        <input id="pvPinIn" type="password" inputmode="numeric" pattern="[0-9]*" maxlength="4" autocomplete="off">
        <button type="button" class="pv-rest-b gold" id="pvPinGo">Unlock for 15 minutes</button>` : '<p>Your parent has not set a PIN yet. They can set one in Parent Hub → Healthy use.</p>'}
        <p class="pv-rest-e" id="pvPinE" role="alert"></p></div></div>`;
    const a = D.querySelector('.app'); if (a && !a.inert) { a.inert = true; a.dataset.pvInert = '1'; }
    el.querySelector('#pvHere').onclick = () => { const b = el.querySelector('#pvPinBox'); b.hidden = false; const i = el.querySelector('#pvPinIn'); if (i) i.focus(); };
    const go = el.querySelector('#pvPinGo');
    if (go) {
      const tryPin = async () => {
        const e = el.querySelector('#pvPinE'), i = el.querySelector('#pvPinIn'), pin = i.value.trim();
        if (Date.now() < waitTill) { e.textContent = `Too many tries. Wait ${Math.ceil((waitTill - Date.now()) / 1000)} seconds.`; return; }
        if (!/^\d{4}$/.test(pin)) { e.textContent = 'Enter 4 digits.'; return; }
        const ok = (await pinHash(myId(), pin)) === (ctl() || {}).pinHash;
        if (!ok) { fails++; i.value = ''; if (fails >= 5) { fails = 0; waitTill = Date.now() + 60000; e.textContent = 'Too many tries. Wait 60 seconds.'; } else e.textContent = 'That PIN is not right.'; return; }
        fails = 0; jset(UK, Date.now() + 15 * 6e4); say('Unlocked for 15 minutes'); enforce();
      };
      go.onclick = tryPin; el.querySelector('#pvPinIn').onkeydown = ev => { if (ev.key === 'Enter') tryPin(); };
    }
    /* no programmatic focus here: a focus without a tap opens the Listen-mode offer (js/a11y.js); aria-modal + inert app keep screen readers inside */
  }

  /* ================= 2. Me card + onboarding card ================= */
  function meHTML() {
    const j = jget(CK, null), linked = j && j.parents > 0 && (!j.uid || j.uid === myId());
    return `<h3>👨‍👩‍👧 Link with my parent</h3><p class="sub">Your parent can see your study time and progress, set goals and cheer you on.</p>
      ${linked ? `<p class="pv-ok">✓ Linked to ${j.parents} parent${j.parents > 1 ? 's' : ''}. Your parent can see your progress.</p>` : ''}
      <div class="pv-row"><button class="btn" type="button" data-pv="mycode">Show my code for my parent</button><button class="btn ghost" type="button" data-pv="link">Link to my parent (enter code)</button></div>
      ${isOwner() ? '<div class="pv-row" style="margin-top:8px"><button class="btn ghost" type="button" data-pv="hub">Open Parent Hub (owner test)</button></div>' : ''}`;
  }
  function wireMe(c) { c.querySelectorAll('[data-pv]').forEach(b => b.onclick = () => ({ hub: openHub, link: linkSheet, mycode: myCode })[b.dataset.pv]()); }
  function placeMe(host, after) {
    let c = host.querySelector(':scope > .pv-me');
    if (!c) { style(); c = D.createElement('div'); c.className = 'card pv-me'; after ? after.after(c) : host.appendChild(c); }
    const h = meHTML(); if (c.dataset.h !== h) { c.dataset.h = h; c.innerHTML = h; wireMe(c); }
  }
  function paintMe() {
    if (!signedIn() || isParentAcct()) return;
    const me = D.getElementById('s-me');
    if (me && me.firstElementChild) placeMe(me, D.getElementById('svCode') || D.getElementById('svCloud') || me.querySelector(':scope > .statrow'));
    const ca = D.getElementById('s-ca'); if (ca && ca.querySelector('.ca-prof')) placeMe(ca, ca.querySelector(':scope > .statrow'));
  }
  /* student: a 1-day code the parent types in Parent Home → "Enter code from my child's app" (rpc create_child_code) */
  async function myCode() {
    if (!signedIn()) { C() && C().open('in'); return; }
    style();
    const el = C().sheet(`<h3 id="clT">My code for my parent</h3><p class="pv-load">Making your code…</p>`);
    try {
      const r = one(await rpc('create_child_code'));
      if (!r || !r.ok || !r.code) throw new Error((r && r.msg) || 'Could not make a code. Please try again.');
      const till = r.expires_at ? new Date(r.expires_at).toLocaleString('en-IN', { day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit' }) : 'tomorrow';
      const msg = `Please link to my StudyVerse 📚\n1. Open ${SITE} on your phone.\n2. Create an account and choose "Parent".\n3. Tap "Enter code from my child's app" and type this code: ${r.code}\nThe code works till ${till}.`;
      el.querySelector('.sheet-in').innerHTML = `<div class="sheet-grab"></div><h3 id="clT">My code for my parent</h3>
        <p>Ask your parent to open <b>study.moneyviel.com</b> on their phone, create an account as <b>Parent</b>, and tap <b>Enter code from my child's app</b>.</p>
        <div class="pv-bigcode" aria-label="Code ${esc(r.code.split('').join(' '))}">${esc(r.code)}</div><p class="cl-small">Works till ${esc(till)}. Use it once.</p>
        <div class="pv-row"><button class="btn ghost" type="button" id="pvCopy">Copy code</button><a class="btn pv-wa" id="pvWa" href="https://wa.me/?text=${encodeURIComponent(msg)}" target="_blank" rel="noopener">Send on WhatsApp</a></div>
        <div style="height:8px"></div><button class="btn ghost" type="button" id="pvDone">Done</button>`;
      el.querySelector('#pvCopy').onclick = () => { try { navigator.clipboard.writeText(r.code).then(() => say('Code copied'), () => say(r.code)); } catch (x) { say(r.code); } };
      el.querySelector('#pvDone').onclick = () => { C().closeSheet(); pullControls(); };
    } catch (e) {
      el.querySelector('.sheet-in').innerHTML = `<div class="sheet-grab"></div><h3 id="clT">My code for my parent</h3><p class="cl-err" role="alert">${esc(e.status != null ? C().errText(e) : e.message)}</p><button class="btn ghost" type="button" id="pvDone">Close</button>`;
      el.querySelector('#pvDone').onclick = C().closeSheet;
    }
  }
  function linkSheet() {
    if (!signedIn()) { C() && C().open('in'); return; }
    style();
    const el = C().sheet(`<h3 id="clT">Link to my parent</h3><p>Ask your parent to open Parent Hub on their phone and tap <b>+ Add child</b>. Enter the 6-letter code they get.</p>
      <form id="pvLinkF" novalidate><label for="pvLinkC">Code from your parent</label><input class="cl-in pv-code-in" id="pvLinkC" maxlength="6" autocapitalize="characters" autocomplete="off" spellcheck="false" placeholder="ABC123">
      <div class="cl-err" id="pvLinkE" role="alert"></div><button class="btn" type="submit" id="pvLinkGo">Link</button></form><div style="height:8px"></div><button class="btn ghost" type="button" id="pvLinkX">Cancel</button>`);
    el.querySelector('#pvLinkX').onclick = C().closeSheet;
    el.querySelector('#pvLinkF').onsubmit = async ev => {
      ev.preventDefault(); const e = el.querySelector('#pvLinkE'), go = el.querySelector('#pvLinkGo'), code = el.querySelector('#pvLinkC').value.trim().toUpperCase().replace(/\s/g, '');
      e.textContent = ''; if (!/^[A-Z0-9]{6}$/.test(code)) { e.textContent = 'The code has 6 letters or numbers.'; return; }
      go.disabled = true;
      try {
        const r = one(await rpc('redeem_link_code', { p_code: code }));
        if (!r || !r.ok) { e.textContent = (r && r.msg) || 'This code is not valid or has expired.'; return; }
        try { if (C().save) C().save(); } catch (x) {}
        C().closeSheet(); say('Linked to your parent ✓'); await pullControls(); paintMe();
      } catch (err) { e.textContent = C().errText(err); }
      finally { go.disabled = false; }
    };
  }

  /* ================= 3. Parent Hub ================= */
  let hub = null, kids = [], sel = 0, loadErr = '', invites = [], pinned = false;
  const hubOpen = () => !!(hub && hub.classList.contains('show'));
  /* parent accounts: the hub is their whole app ("Parent Home") — full screen, cannot be closed */
  function home() { if (hubOpen() && pinned) return; openHub(true); }
  function openHub(pin) {
    if (!signedIn()) { C() && C().open('in'); return; }
    pin = pin === true || isParentAcct();
    if (!pin && !canHub()) { say('Parent Hub is for parent accounts. Use “Show my code for my parent” instead.'); return; }
    pinned = pin;
    style();
    if (!hub) {
      hub = D.createElement('div'); hub.className = 'sheet pv-hub'; hub.id = 'pvHub';
      hub.setAttribute('role', 'dialog'); hub.setAttribute('aria-modal', 'true'); hub.setAttribute('aria-labelledby', 'pvT');
      D.body.appendChild(hub);
    }
    hub.classList.toggle('pv-pro', !pinned && R.dataset.age === 'pro');
    hub.toggleAttribute('data-pinned', pinned); hub.toggleAttribute('data-nonav', pinned);   // no Back / Escape close; Back history ignores it
    hub.innerHTML = `<div class="pv-wrap"><div class="pv-top">${pinned ? '<span class="pv-logo" aria-hidden="true">Study<b>Verse</b></span>' : '<button class="pv-back" type="button" data-close aria-label="Close Parent Hub">← Back</button>'}<h1 id="pvT">👨‍👩‍👧 Parent Hub</h1><button class="pv-ref" type="button" id="pvRef" aria-label="Refresh">⟳</button></div>
      <div class="pv-tabs" role="tablist" aria-label="Children" id="pvTabs"></div><div id="pvBody" class="pv-body"><p class="pv-load">Loading…</p></div></div>`;
    const bk = hub.querySelector('.pv-back'); if (bk) bk.onclick = closeHub;
    hub.querySelector('#pvRef').onclick = () => load();
    hub.classList.add('show'); hub.scrollTop = 0;
    load();
  }
  function closeHub() { if (hub && !pinned) hub.classList.remove('show'); }
  async function load() {
    loadErr = '';
    const inv = C().rest('parent_invites?select=email,child_name,created_at,accepted_at&order=created_at.desc').then(r => { invites = Array.isArray(r) ? r : []; }, () => {});
    try { const r = await rpc('my_children'); kids = Array.isArray(r) ? r : []; }
    catch (e) { loadErr = C().errText(e); }
    await inv;
    if (sel >= kids.length) sel = 0;
    render();
  }
  function tabs() {
    const t = hub.querySelector('#pvTabs');
    t.innerHTML = kids.map((k, i) => `<button type="button" role="tab" aria-selected="${i === sel}" class="pv-tab${i === sel ? ' on' : ''}" data-i="${i}">${esc(childName(k))}</button>`).join('')
      + (kids.length || loadErr ? '<button type="button" class="pv-tab pv-add" id="pvAdd">+ Add child</button>' : '');
    t.hidden = !kids.length && !loadErr;
    t.querySelectorAll('[data-i]').forEach(b => b.onclick = () => { sel = +b.dataset.i; render(); });
    const a = t.querySelector('#pvAdd'); if (a) a.onclick = addMenu;
  }
  const childName = k => (k && (k.name || (k.state && k.state.st && k.state.st.profile && k.state.st.profile.name))) || 'Child';
  async function render() {
    if (!hub) return; tabs();
    const body = hub.querySelector('#pvBody');
    if (loadErr) { body.innerHTML = `<div class="pv-card"><h2>Could not load</h2><p>${esc(loadErr)}</p><button class="pv-btn" type="button" id="pvRetry">Try again</button></div>` + acctHTML(); body.querySelector('#pvRetry').onclick = load; wireAcct(body); return; }
    if (!kids.length) {
      body.innerHTML = `<div class="pv-card pv-hero"><h2>Welcome! Let's add your child</h2>
        <p>Choose one way below. Your child's study time and progress will then show here.</p>${optsHTML()}
        <p class="pv-note">You will see study time, strong and weak areas, and can set goals and healthy limits. Only you can see your child's data.</p></div>` + invitesHTML() + acctHTML();
      wireOpts(body); wireAcct(body); return;
    }
    const k = kids[sel], A = await analyse(k), X = A.has ? await deep(A) : null;
    if (kids[sel] !== k) return;
    body.innerHTML = childHTML(k, A, X) + invitesHTML() + mailCardHTML() + acctHTML();
    wireChild(body, k, A, X); wireMail(body); wireAcct(body);
    try { if (window.Squad && Squad.hubCard) Squad.hubCard(body, k, A); } catch (e) {}   // ⚔️ parent challenge card (js/squad.js)
    try { if (window.PlayReady && PlayReady.hubCard) PlayReady.hubCard(body, k, A); } catch (e) {}   // 🛡️ friends / rooms / news controls (js/playready.js)
  }

  /* ---------- three ways to add a child ---------- */
  const optsHTML = () => `<div class="pv-opts">
    <button class="pv-opt" type="button" data-add="code"><span aria-hidden="true">📱</span><b>Enter code from my child's app</b><small>On your child's phone: Me → “Show my code for my parent”.</small></button>
    <button class="pv-opt" type="button" data-add="invite"><span aria-hidden="true">📧</span><b>Invite my child by email</b><small>We email your child a link to make their account on their phone.</small></button>
    <button class="pv-opt" type="button" data-add="make"><span aria-hidden="true">🔑</span><b>Make a code for my child to enter</b><small>Your child types it in Me → “Link to my parent”.</small></button></div>`;
  function wireOpts(root) { root.querySelectorAll('[data-add]').forEach(b => b.onclick = () => ({ code: childCodeSheet, invite: inviteSheet, make: addChild })[b.dataset.add]()); }
  function addMenu() {
    style();
    const el = C().sheet(`<h3 id="clT">Add a child</h3><p>Choose one way.</p>${optsHTML()}<div style="height:8px"></div><button class="btn ghost" type="button" id="pvMenuX">Cancel</button>`);
    el.querySelector('#pvMenuX').onclick = C().closeSheet; wireOpts(el);
  }
  function childCodeSheet() {
    style();
    const el = C().sheet(`<h3 id="clT">Enter code from my child's app</h3><p>On your child's phone open StudyVerse → <b>Me</b> → <b>Show my code for my parent</b>. Type that code here.</p>
      <form id="pvCcF" novalidate><label for="pvCcC">Code from your child's app</label><input class="cl-in pv-code-in" id="pvCcC" maxlength="6" autocapitalize="characters" autocomplete="off" spellcheck="false" placeholder="ABC123">
      <label for="pvCcN">Child's name</label><input class="cl-in" id="pvCcN" maxlength="40" autocomplete="off" placeholder="e.g. Riya">
      <div class="cl-err" id="pvCcE" role="alert"></div><button class="btn" type="submit" id="pvCcGo">Link my child</button></form><div style="height:8px"></div><button class="btn ghost" type="button" id="pvCcX">Cancel</button>`);
    el.querySelector('#pvCcX').onclick = C().closeSheet;
    el.querySelector('#pvCcF').onsubmit = async ev => {
      ev.preventDefault(); const e = el.querySelector('#pvCcE'), go = el.querySelector('#pvCcGo');
      const code = el.querySelector('#pvCcC').value.trim().toUpperCase().replace(/\s/g, ''), name = el.querySelector('#pvCcN').value.trim();
      e.textContent = ''; if (!/^[A-Z0-9]{6}$/.test(code)) { e.textContent = 'The code has 6 letters or numbers.'; return; }
      if (!name) { e.textContent = "Please enter your child's name."; return; }
      go.disabled = true;
      try {
        const r = one(await rpc('redeem_child_code', { p_code: code, p_child_name: name }));
        if (!r || !r.ok) { e.textContent = (r && r.msg) || 'This code is not valid or has expired. Ask your child for a new one.'; return; }
        C().closeSheet(); say(`${name} is linked ✓`); load();
      } catch (err) { e.textContent = C().errText(err); }
      finally { go.disabled = false; }
    };
  }
  function inviteSheet() {
    style();
    const el = C().sheet(`<h3 id="clT">Invite my child by email</h3><p>We send your child an email with a link. They open it on their phone and create their own account with that email.</p>
      <form id="pvInF" novalidate><label for="pvInN">Child's name</label><input class="cl-in" id="pvInN" maxlength="40" autocomplete="off" placeholder="e.g. Riya">
      <label for="pvInE">Child's email</label><input class="cl-in" id="pvInE" type="email" data-field="email" maxlength="120" autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="child@gmail.com">
      <div class="cl-err" id="pvInErr" role="alert"></div><button class="btn" type="submit" id="pvInGo">Send invite</button></form><div style="height:8px"></div><button class="btn ghost" type="button" id="pvInX">Cancel</button>`);
    el.querySelector('#pvInX').onclick = C().closeSheet;
    el.querySelector('#pvInF').onsubmit = async ev => {
      ev.preventDefault(); const e = el.querySelector('#pvInErr'), go = el.querySelector('#pvInGo');
      const name = el.querySelector('#pvInN').value.trim(), email = el.querySelector('#pvInE').value.trim().toLowerCase();
      e.textContent = ''; if (!name) { e.textContent = "Please enter your child's name."; return; }
      if (window.Fields && !Fields.valid(ev.target).ok) return;
      if (!EMAIL_RE.test(email)) { e.textContent = "Please enter your child's email address."; return; }
      if (email === (C().email() || '').toLowerCase()) { e.textContent = 'This is your own email. Please enter your child\u2019s email.'; return; }
      go.disabled = true; const label = go.textContent; go.textContent = 'Sending…';
      try {
        const r = await C().call('/functions/v1/parent-invite', { method: 'POST', body: { email, name } });
        if (!r || !r.ok) { e.textContent = (r && (r.msg || r.error)) || 'Could not send the invite. Please try again.'; return; }
        const s = C().sheet(`<h3 id="clT">Invite sent 📧</h3><p>We emailed <b>${esc(email)}</b>. Your child opens it on their phone and creates their account with that email. They'll appear here automatically.</p>
          ${r.exists ? `<p class="cl-small">This email already has a StudyVerse account — ${esc(name)} just needs to sign in once.</p>` : ''}
          <p class="cl-small">Not in the inbox? Ask them to check Spam or Promotions.</p><button class="btn" type="button" id="pvInOk">OK</button>`);
        s.querySelector('#pvInOk').onclick = C().closeSheet; load();
      } catch (err) { e.textContent = C().errText(err); }
      finally { go.disabled = false; go.textContent = label; }
    };
  }
  const invitesHTML = () => !invites.length ? '' : `<section class="pv-card" id="pvInv" aria-labelledby="pvInvT"><h3 id="pvInvT">📧 Email invites</h3><ul class="pv-list">${invites.map(v => `<li class="pv-invr"><div><b>${esc(v.child_name || 'Child')}</b> <span class="pv-mut">${esc(v.email)}</span><br><span class="pv-mut">Sent ${esc(v.created_at ? new Date(v.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }) : '')}</span></div>${v.accepted_at ? '<span class="pv-st ok">✓ Joined</span>' : '<span class="pv-st warn">Waiting for sign-up</span>'}</li>`).join('')}</ul></section>`;
  /* account area (parent accounts only: they have no Me screen) */
  const acctHTML = () => !pinned ? '' : `<section class="pv-card" id="pvAcct" aria-labelledby="pvAcT"><h3 id="pvAcT">👤 Your account</h3><p>${esc(C().email())}</p>
    <button class="pv-btn ghost" type="button" id="pvOut">Sign out</button>
    <p class="pv-note" style="margin-top:10px"><a href="legal/privacy.html">Privacy</a> · <a href="legal/terms.html">Terms</a> · Help: <a href="mailto:support@moneyviel.com">support@moneyviel.com</a></p></section>`;
  function wireAcct(root) {
    const b = root.querySelector('#pvOut'); if (!b) return;
    b.onclick = () => { if (!b.dataset.sure) { b.dataset.sure = 1; b.textContent = 'Tap again to sign out'; return; } b.disabled = true; b.textContent = 'Signing out…'; C().signOut(); };
  }

  /* weekly email: one short summary per week with a button back to this hub (the full report stays in the app) */
  let mailOn = null;
  const mailCardHTML = () => `<div class="pv-card" id="pvMail"><h2>📧 Weekly email</h2>
    <label style="display:flex;gap:10px;align-items:center;min-height:44px;cursor:pointer"><input type="checkbox" id="pvMailOn" style="width:22px;height:22px"${mailOn === false ? '' : ' checked'}>
    <span>Send me a short weekly summary of my children's study time and accuracy, with a link to this full report.</span></label>
    <p class="pv-note" id="pvMailNote">Sent once a week to ${esc(C().email())}. You can switch it off any time.</p></div>`;
  async function wireMail(body) {
    const cb = body.querySelector('#pvMailOn'), note = body.querySelector('#pvMailNote'); if (!cb) return;
    if (mailOn === null) {
      try { const u = C().user(); const r = await C().rest('parent_prefs?select=weekly_email&parent_id=eq.' + encodeURIComponent(u ? u.id : '')); mailOn = Array.isArray(r) && r[0] ? !!r[0].weekly_email : true; cb.checked = mailOn; } catch (e) {}
    }
    cb.onchange = async () => {
      const want = cb.checked; cb.disabled = true;
      try { const r = one(await rpc('set_weekly_email', { p_on: want })); if (!r || !r.ok) throw new Error('x'); mailOn = want; note.textContent = want ? `Weekly email is on (${C().email()}).` : 'Weekly email is off.'; }
      catch (e) { cb.checked = !want; note.textContent = 'Could not save. Please check your internet and try again.'; }
      finally { cb.disabled = false; }
    };
  }

  function addChild() {
    style();
    const el = C().sheet(`<h3 id="clT">Add a child</h3><p>We make a code. Your child enters it on their own StudyVerse account to link to you.</p>
      <form id="pvAddF" novalidate><label for="pvAddN">Child's name</label><input class="cl-in" id="pvAddN" maxlength="40" autocomplete="off" placeholder="e.g. Riya">
      <div class="cl-err" id="pvAddE" role="alert"></div><button class="btn" type="submit" id="pvAddGo">Make code</button></form><div style="height:8px"></div><button class="btn ghost" type="button" id="pvAddX">Cancel</button>`);
    el.querySelector('#pvAddX').onclick = C().closeSheet;
    el.querySelector('#pvAddF').onsubmit = async ev => {
      ev.preventDefault(); const e = el.querySelector('#pvAddE'), go = el.querySelector('#pvAddGo'), name = el.querySelector('#pvAddN').value.trim();
      e.textContent = ''; if (!name) { e.textContent = "Please enter your child's name."; return; }
      go.disabled = true;
      try {
        const r = one(await rpc('create_link_code', { p_child_name: name }));
        if (!r || !r.ok || !r.code) { e.textContent = (r && r.msg) || 'Could not make a code. Please try again.'; return; }
        showCode(name, r.code, r.expires_at);
      } catch (err) { e.textContent = C().errText(err); }
      finally { go.disabled = false; }
    };
  }
  function showCode(name, code, exp) {
    const till = exp ? new Date(exp).toLocaleString('en-IN', { day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit' }) : '2 days';
    const msg = `Let's link StudyVerse 👨‍👩‍👧\n1. On ${name}'s phone open ${SITE} and sign in to ${name}'s account.\n2. Go to Me → "Link to my parent".\n3. Enter this code: ${code}\nThe code works till ${till}.`;
    const el = C().sheet(`<h3 id="clT">Code for ${esc(name)}</h3><p>On ${esc(name)}'s phone: open <b>study.moneyviel.com</b> → <b>Me</b> → <b>Link to my parent</b> → enter this code.</p>
      <div class="pv-bigcode" aria-label="Code ${esc(code.split('').join(' '))}">${esc(code)}</div><p class="cl-small">Works till ${esc(till)}. Use it once.</p>
      <div class="pv-row"><button class="btn ghost" type="button" id="pvCopy">Copy code</button><a class="btn pv-wa" id="pvWa" href="https://wa.me/?text=${encodeURIComponent(msg)}" target="_blank" rel="noopener">Share on WhatsApp</a></div>
      <div style="height:8px"></div><button class="btn ghost" type="button" id="pvDone">Done</button>`);
    el.querySelector('#pvCopy').onclick = () => { try { navigator.clipboard.writeText(code).then(() => say('Code copied'), () => say(code)); } catch (x) { say(code); } };
    el.querySelector('#pvDone').onclick = () => { C().closeSheet(); load(); };
  }

  /* ---------- analysis of one child's synced progress ---------- */
  const STRUCT = {};
  async function caStructure(level) {
    if (!(level in STRUCT)) { try { const r = await fetch(`content/ca/${level}/structure.json`); STRUCT[level] = r.ok ? await r.json() : null; } catch (e) { STRUCT[level] = null; } }
    return STRUCT[level];
  }
  const CUR_ = () => { try { return CUR; } catch (e) { return null; } };
  function subjName(g, sid) { const c = CUR_(), s = c && c.grades && c.grades[g] && (c.grades[g].subjects || []).find(x => x.id === sid); return s ? s.name : sid.charAt(0).toUpperCase() + sid.slice(1); }
  function chapName(g, sid, n) { const c = CUR_(), s = c && c.grades && c.grades[g] && (c.grades[g].subjects || []).find(x => x.id === sid), ch = s && (s.chapters || []).find(x => +x.n === +n); return ch ? ch.title : 'Chapter ' + n; }
  async function topicTitle(tid) {
    const m = /^g(\d+)-([a-z]+)-(\d+)-(\d+)$/.exec(tid); if (!m) return null;
    try { const d = await subjectData(+m[1], m[2]); if (d) for (const c of d.chapters) for (const t of c.topics) if (t.id === tid) return { title: t.title, sub: subjName(+m[1], m[2]) }; } catch (e) {}
    return { title: chapName(+m[1], m[2], +m[3]), sub: subjName(+m[1], m[2]) };
  }
  const LVL = { fnd: 'foundation', int: 'inter', fin: 'final' };

  async function analyse(k) {
    const s = k.state && k.state.st || null, c = k.controls || {};
    const A = { s, has: !!(s && s.profile), ca: !!(s && s.profile && s.profile.course === 'ca'), name: childName(k), c };
    if (!A.has) return A;
    const p = s.profile, caDays = caAnswersByDay(s), d14 = daysBack(14), wk = d14.slice(7), pw = d14.slice(0, 7), d60 = daysBack(60);
    A.label = A.ca ? `CA ${({ foundation: 'Foundation', inter: 'Intermediate', final: 'Final' })[(s.ca && s.ca.level) || 'foundation'] || ''}` : `Grade ${p.grade || '–'}`;
    A.week = wk.map(d => ({ d, m: minutesOn(s, d) }));
    A.weekMin = A.week.reduce((a, x) => a + x.m, 0); A.prevMin = pw.reduce((a, d) => a + minutesOn(s, d), 0);
    const ans = ds => ds.reduce((o, d) => { const x = answersOn(s, d, caDays); o.a += x.a; o.r += x.r; return o; }, { a: 0, r: 0 });
    A.qw = ans(wk); A.qp = ans(pw);
    A.accW = A.qw.a ? A.qw.r / A.qw.a * 100 : null; A.accP = A.qp.a ? A.qp.r / A.qp.a * 100 : null;
    const topicDays = new Set(Object.values(s.topics || {}).map(t => t && t.last).filter(Boolean));
    const active = d => minutesOn(s, d) >= 1 || answersOn(s, d, caDays).a > 0 || topicDays.has(d);
    A.daysActive = wk.filter(active).length;
    let n = 0; for (let i = d60.length - 1; i >= 0; i--) { if (active(d60[i])) n++; else if (i === d60.length - 1) continue; else break; }
    A.streak = n;
    const allDays = new Set(d60.filter(active));
    Object.keys(s.time || {}).forEach(d => { if (+s.time[d] >= 1) allDays.add(d); });
    topicDays.forEach(d => allDays.add(d));
    A.lastDay = [...allDays].sort().pop() || null;
    A.sinceDays = A.lastDay ? Math.round((noon() - dayDate(A.lastDay)) / DAY) : null;
    A.today = minutesOn(s, todayK()); A.yday = minutesOn(s, d14[12]);
    A.goal = +c.goal || 0;
    A.goalDays = A.goal ? A.week.filter(x => x.m >= A.goal).length : 0;
    A.goalStreak = goalStreak(s, A.goal);
    A._active = active; A._caDays = caDays;

    /* strengths and weak areas */
    const groups = {};
    if (A.ca) {
      const level = (s.ca && s.ca.level) || 'foundation', st = await caStructure(level), nm = {};
      if (st) st.papers.forEach(pp => pp.chapters.forEach(ch => { nm[ch.id] = { title: ch.title, sub: (pp.key ? pp.key.toUpperCase().replace('P', 'Paper ') : '') + ' ' + pp.name }; ch.units.forEach(u => { nm[u.id] = { title: u.title }; }); }));
      Object.entries((s.ca && s.ca.mcq) || {}).forEach(([key, v]) => { const uid = key.split('#')[0], ch = uid.split('-').slice(0, 3).join('-'); const g = groups[ch] || (groups[ch] = { id: ch, n: 0, r: 0, wN: 0, wP: 0 }); g.n += v.s || 0; g.r += (v.s || 0) - (v.w || 0); });
      Object.entries((s.ca && s.ca.writes) || {}).forEach(([key, h]) => { const sc = (h || []).filter(a => a && a.score != null && a.max && a.status !== 'waiting'); if (!sc.length) return; const uid = key.split('#')[0], ch = uid.split('-').slice(0, 3).join('-'); const g = groups[ch] || (groups[ch] = { id: ch, n: 0, r: 0, wN: 0, wP: 0 }); const b = Math.max(...sc.map(a => a.score / a.max)); g.wN++; g.wP += b * 100; });
      Object.values(groups).forEach(g => { const x = nm[g.id] || {}; g.title = x.title || g.id; g.sub = (x.sub || '').trim(); g.acc = g.n ? g.r / g.n * 100 : (g.wN ? g.wP / g.wN : null); g.cnt = g.n + g.wN; g.written = g.wN ? Math.round(g.wP / g.wN) : null; });
      A.mistakes = Object.values((s.ca && s.ca.mcq) || {}).reduce((a, v) => a + (v.w || 0), 0); A.topMist = [];
      A.unitNames = nm;
    } else {
      Object.entries(s.qstats || {}).forEach(([qid, v]) => {
        const m = /^g(\d+)-([a-z]+)-(\d+)-\d+#/.exec(qid); if (!m || !v || !v.s) return;
        const id = `${m[1]}-${m[2]}-${+m[3]}`, g = groups[id] || (groups[id] = { id, gr: +m[1], sid: m[2], ch: +m[3], n: 0, r: 0 });
        g.n += v.s; g.r += v.s - (v.w || 0);
      });
      Object.values(groups).forEach(g => { g.title = chapName(g.gr, g.sid, g.ch); g.sub = subjName(g.gr, g.sid); g.acc = g.n ? g.r / g.n * 100 : null; g.cnt = g.n; });
      const mi = Object.entries(s.mistakes || {}).filter(x => x[0] && x[0] !== 'undefined');
      A.mistakes = mi.reduce((a, x) => a + (+x[1] || 0), 0); A.topMist = mi.sort((a, b) => b[1] - a[1]).slice(0, 3);
    }
    const ok = Object.values(groups).filter(g => g.acc != null && g.cnt >= 4);
    const byAcc = ok.slice().sort((a, b) => b.acc - a.acc || b.cnt - a.cnt);
    A.best = byAcc.filter(g => g.acc >= 60).slice(0, 2);
    A.weak = byAcc.slice().reverse().filter(g => g.acc < 75 && !A.best.includes(g)).slice(0, 2);
    A.totalAns = Object.values(groups).reduce((a, g) => a + g.cnt, 0);
    A.groups = groups;
    /* subject totals (school) */
    if (!A.ca) { const sj = {}; Object.values(groups).forEach(g => { const x = sj[g.sub] || (sj[g.sub] = { n: 0, r: 0 }); x.n += g.n; x.r += g.r; }); A.subjects = Object.entries(sj).filter(x => x[1].n >= 6).map(([k2, v]) => ({ name: k2, acc: v.r / v.n * 100, n: v.n })).sort((a, b) => b.acc - a.acc); }

    /* recent topics → dinner-table questions */
    A.recent = [];
    if (A.ca) {
      const u = Object.entries((s.ca && s.ca.units) || {}).map(([id, o]) => [id, Object.values(o || {}).filter(v => typeof v === 'string').sort().pop() || '']).filter(x => x[1]).sort((a, b) => a[1] < b[1] ? 1 : -1);
      u.slice(0, 3).forEach(([id]) => { const x = A.unitNames[id]; if (x) A.recent.push({ title: x.title }); });
    } else {
      const t = Object.entries(s.topics || {}).filter(x => x[1] && x[1].last).sort((a, b) => a[1].last < b[1].last ? 1 : -1).slice(0, 3);
      for (const [id] of t) { const x = await topicTitle(id); if (x) A.recent.push(x); }
    }

    /* alerts */
    A.alerts = [];
    if (A.sinceDays == null) A.alerts.push(['warn', `${A.name} has not studied with the app yet.`]);
    else if (A.sinceDays >= 3) A.alerts.push(['bad', `No study for ${A.sinceDays} days (last on ${fmtDay(A.lastDay)}).`]);
    if (A.accW != null && A.accP != null && A.qw.a >= 10 && A.qp.a >= 10 && A.accP - A.accW > 15) A.alerts.push(['bad', `Accuracy dropped from ${pctS(A.accP)} last week to ${pctS(A.accW)} this week.`]);
    if (A.goal && A.yday < A.goal) A.alerts.push(['warn', `Daily goal missed yesterday (${Math.floor(A.yday)} of ${A.goal} min). Goal met on ${A.goalDays} of the last 7 days.`]);
    return A;
  }

  /* exam target: a simple, explained rule */
  function examPlan(A, ex) {
    const dl = daysTo(ex.date), base = A.goal || 30;
    const target = Math.round((dl <= 14 ? base * 1.5 : dl <= 45 ? base * 1.25 : base) / 5) * 5;
    const avg = A.has ? A.weekMin / 7 : 0;
    const st = !A.has ? ['', 'No data yet'] : avg >= target * 0.8 ? ['ok', '✅ On track'] : avg >= target * 0.5 ? ['warn', '⚠️ A little behind'] : ['bad', '🔴 Behind'];
    return { dl, target, avg, st };
  }
  function suggestions(A) {
    const out = [], w = A.weak;
    if (w[0]) out.push(`<b>Revise “${esc(w[0].title)}”</b>${w[0].sub ? ` (${esc(w[0].sub)})` : ''} — ${pctS(w[0].acc)} correct in ${w[0].cnt} answers. Ask ${esc(A.name)} to redo it and explain it back to you.`);
    if (!A.ca && A.topMist[0]) out.push(`<b>Fix a repeated slip:</b> “${esc(A.topMist[0][0])}” (${A.topMist[0][1]} time${A.topMist[0][1] > 1 ? 's' : ''}). Daily Practice brings such questions back until they are right.`);
    else if (A.ca && w[0] && w[0].written != null && w[0].written < 60) out.push(`<b>Practise written answers</b> in “${esc(w[0].title)}” — best checked score averages ${w[0].written}%. Write one full answer a day.`);
    if (w[1]) out.push(`<b>Then “${esc(w[1].title)}”</b>${w[1].sub ? ` (${esc(w[1].sub)})` : ''} — ${pctS(w[1].acc)} correct in ${w[1].cnt} answers.`);
    if (A.daysActive < 5) out.push(`<b>Study on more days:</b> ${A.daysActive} of 7 days this week. ${A.goal || 20} minutes every day works better than one long session.`);
    else if (A.accW != null && A.accP != null && A.accW < A.accP - 5) out.push(`<b>Slow down a little:</b> accuracy is ${pctS(A.accW)} this week (was ${pctS(A.accP)}). Read each question twice before answering.`);
    if (out.length < 3 && A.totalAns < 20) out.push(`Not enough answers yet to find weak areas (${A.totalAns} so far). This fills in after about 20 questions.`);
    return out.slice(0, 3);
  }
  function dinnerQs(A) {
    const r = A.recent; if (!r.length) return [];
    const t = i => `“${esc((r[i] || r[0]).title)}”`;
    return A.ca
      ? [`Explain ${t(0)} to me as if I were your client. What is the one rule to remember?`, `Which part of ${t(1)} was hardest, and how did you crack it?`, `Where would ${t(2)} be used at a real firm or in our own money matters?`]
      : [`What did you learn about ${t(0)}? Can you teach me in 2 minutes?`, `What was the trickiest question in ${t(1)}, and how did you solve it?`, `Where can we see ${t(2)} in real life — at home or in the market?`];
  }

  function chartSVG(A) {
    const W = 352, PW = 300, H = 150, top = 22, bot = 28, bw = 26, gap = (PW - 7 * bw) / 7;   // bars use 0–300, the goal label sits in the right margin
    const max = Math.max(A.goal || 0, ...A.week.map(x => x.m), 10), y = v => top + (H - top - bot) * (1 - v / max);
    const label = A.week.map(x => `${wkDay(x.d)} ${Math.round(x.m)} min`).join(', ');
    const bars = A.week.map((x, i) => {
      const cx = gap / 2 + i * (bw + gap), h = Math.max(0, H - bot - y(x.m)), today = x.d === todayK(), m = Math.round(x.m);
      return `<g><title>${wkDay(x.d)} ${fmtDay(x.d)}: ${fmtMin(m)}</title>
        ${h > 0 ? `<path d="M${cx},${H - bot} V${H - bot - h + Math.min(4, h)} q0,-4 4,-4 h${bw - 8} q4,0 4,4 V${H - bot} Z" class="pv-bar"/>` : ''}
        <text x="${cx + bw / 2}" y="${H - bot - h - 6}" class="pv-bv">${m || ''}</text>
        <text x="${cx + bw / 2}" y="${H - 10}" class="pv-bx${today ? ' on' : ''}">${today ? 'Today' : wkDay(x.d)}</text></g>`;
    }).join('');
    const gl = A.goal ? `<line x1="0" x2="${PW + 4}" y1="${y(A.goal)}" y2="${y(A.goal)}" class="pv-gl"/><text x="${W}" y="${y(A.goal) + 3.5}" class="pv-glt">goal ${A.goal}</text>` : '';
    return `<svg viewBox="0 0 ${W} ${H}" class="pv-chart" role="img" aria-label="Minutes studied per day, last 7 days: ${esc(label)}"><line x1="0" x2="${W}" y1="${H - bot}" y2="${H - bot}" class="pv-axis"/>${bars}${gl}</svg>`;
  }
  const delta = (a, b, unit) => { if (a == null || b == null) return ''; const d = Math.round(a - b); return d === 0 ? '<span class="pv-d">same</span>' : `<span class="pv-d ${d > 0 ? 'up' : 'dn'}">${d > 0 ? '▲' : '▼'} ${Math.abs(d)}${unit}</span>`; };

  /* ---------- profile & plan (rpc my_children: plans [{course, valid_until, note}], locked_course, email) ---------- */
  const COURSE = { 'school-all': 'All school grades', school: 'School (Grades 1–12)', 'ca-foundation': 'CA Foundation', 'ca-inter': 'CA Intermediate', 'ca-final': 'CA Final' };
  const courseName = c => /^school-g\d+$/.test(c || '') ? 'Grade ' + c.slice(8) : (COURSE[c] || c || '');
  function planLines(k) {
    const now = Date.now(), live = (Array.isArray(k.plans) ? k.plans : []).filter(a => a && a.course && (!a.valid_until || new Date(a.valid_until) > now)), out = [];
    const fmtEnd = iso => { const d = new Date(iso), t = d.toLocaleTimeString('en-IN', { hour: 'numeric', minute: '2-digit' }); return dk(d) === todayK() ? 'today ' + t : dk(d) === dk(noon() + DAY) ? 'tomorrow ' + t : d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }) + ', ' + t; };
    const rank = a => /trial/i.test(a.note || '') ? 1 : !a.valid_until ? 2 : 0;
    live.slice().sort((a, b) => rank(a) - rank(b)).forEach(a => {
      if (/trial/i.test(a.note || '')) out.push(['warn', `⏳ Free trial (${courseName(a.course)}) — ends ${fmtEnd(a.valid_until)}`]);
      else if (!a.valid_until) out.push(['ok', `🎁 Free forever (${courseName(a.course)})`]);
      else out.push(['ok', `✅ ${courseName(a.course)} — till ${new Date(a.valid_until).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}`]);
    });
    if (k.locked_course && !live.some(a => !a.valid_until && a.course === k.locked_course)) out.unshift(['ok', `🎁 Free forever (${courseName(k.locked_course)})`]);
    if (!out.length) out.push(['', `Free plan — ${(window.Plans && Plans.FREE_PER_DAY) || 5} questions a day`]);
    return out;
  }
  function profileHTML(k, A) {
    const s = A.s, p = A.has ? s.profile : null;
    const course = !p ? 'Not set up yet' : A.ca ? A.label : `${p.board ? esc(String(p.board).toUpperCase()) + ' · ' : ''}Grade ${esc(p.grade || '–')}${p.stream ? ' · ' + esc(p.stream) : ''}`;
    return `<section class="pv-card pv-head pv-prof" aria-labelledby="pvPrT"><div class="pv-av" aria-hidden="true">${esc(p && p.avatar && !A.ca ? p.avatar : A.name.trim().charAt(0).toUpperCase())}</div>
      <div class="pv-prof-in"><h2 id="pvPrT">${esc(A.name)}</h2>
        <p class="pv-mut">Profile &amp; plan</p>
        <dl class="pv-dl">${k.email ? `<dt>Email</dt><dd>${esc(k.email)}</dd>` : ''}<dt>Studying</dt><dd>${course}</dd><dt>Last active</dt><dd>${esc(ago(k.updated_at))}</dd>
        <dt>Plan</dt><dd><ul class="pv-plans">${planLines(k).map(([c, t]) => `<li class="pv-plan ${c}">${esc(t)}</li>`).join('')}</ul></dd></dl></div></section>`;
  }

  /* =============== deeper insights for parents ===============
     8-week trend · mastery map · careless vs concept mistakes · best study time · exam readiness · focus topic · wins · CA written answers.
     Everything comes from THIS child's synced ST (k.state.st) — never another child's. The ST-only part is memoised per ST object
     (a reload / new sync gives a new object); the parts that depend on parent controls (readiness, focus) are cheap and run per render.
     Answer log = ST.ans (school answers and CA generated questions, with seconds — logAns in js/app.js)
                + ST.ca.mlog (CA bank MCQs, with seconds) + older ST.ins.att answers (no seconds) from before ST.ans began. */
  const MEMO = new WeakMap();
  let CURP = null;
  async function curriculum() {
    const c = CUR_(); if (c && c.grades && Object.keys(c.grades).length) return c;
    if (!CURP) CURP = fetch('content/curriculum.json').then(r => r.ok ? r.json() : null).catch(() => null);
    return CURP;
  }
  const BUCKETS = [['morning', 'Morning', '5 am–12 noon', h => h >= 5 && h < 12], ['afternoon', 'Afternoon', '12–5 pm', h => h >= 12 && h < 17],
    ['evening', 'Evening', '5–9 pm', h => h >= 17 && h < 21], ['night', 'Night', '9 pm–5 am', h => h >= 21 || h < 5]];
  const MST = [['Not started', 'm0', '○'], ['Learning', 'm1', '½'], ['Good', 'm2', '✓'], ['Mastered', 'm3', '★']];
  /* chapter / unit status: Not started = nothing tried · Learning = under 5 answers or under 60% · Good = 60%+ · Mastered = 85%+ in 8+ answers */
  const mStat = (n, acc, touched) => !n && !touched ? 0 : (n < 5 || acc == null || acc < 60) ? 1 : (acc >= 85 && n >= 8) ? 3 : 2;
  const BADGE = { first: ['🚀', 'First quest'], q10: ['📚', '10 quests'], q50: ['🏆', '50 quests'], q100: ['👑', '100 quests'], star3: ['🌟', 'First 3-star quest'],
    s3: ['🔥', '3-day streak'], s7: ['⚡', '7-day streak'], s30: ['💎', '30-day streak'], w1: ['💧', 'First watering'], w25: ['🌳', 'Gardener: 25 waterings'],
    m1: ['🌻', 'First mastered topic'], goal: ['🎯', 'Daily goal reached'], d1: ['⚔️', 'First duel'], dw: ['🥇', 'Duel winner'], dw10: ['🏅', '10 duel wins'] };   // same list as js/practice.js
  const SKN = { computation: 'Computation', concept: 'Concept', provision: 'Quoting provisions', analysis: 'Analysis', application: 'Application', conclusion: 'Conclusion', presentation: 'Presentation', posting: 'Posting', classification: 'Classification', balancing: 'Balancing', rectification: 'Rectification' };   // as js/ca-check.js
  const SKTIP = { computation: 'Show a working note for every figure — step marks come even when the final answer is wrong.', concept: 'Start with the rule or definition in the exact words of the study material.',
    provision: 'Quote the section / standard number first, then the provision in brief.', analysis: 'Apply the provision to the facts, one fact at a time.', application: 'Use the names, dates and figures given in the question.',
    conclusion: 'End with a clear one-line conclusion that answers exactly what was asked.', presentation: 'Use the proper format: headings, dates, Dr / Cr columns and narrations.',
    posting: 'Post each item to the correct account and side (Dr / Cr).', classification: 'Classify each item correctly (capital / revenue, asset / liability) first.',
    balancing: 'Total both sides and show the balance c/d and b/d with dates.', rectification: 'Show the wrong entry, the correct entry, then the rectifying entry.' };
  const isSchoolId = id => /^\d+-[a-z]+-\d+$/.test(id || '');
  const chapOf = id => { id = String(id || ''); let m = /^g(\d+)-([a-z]+)-(\d+)/.exec(id); if (m) return `${+m[1]}-${m[2]}-${+m[3]}`; m = /^([a-z]+-p\d+-ch\d+)/.exec(id); return m ? m[1] : null; };
  const pctR = (r, n) => n ? r / n * 100 : null;
  const mean = a => a.length ? a.reduce((x, y) => x + y, 0) / a.length : null;
  const median = a => { if (!a.length) return null; const b = a.slice().sort((x, y) => x - y), m = b.length >> 1; return b.length % 2 ? b[m] : (b[m - 1] + b[m]) / 2; };
  const fmtLong = t => new Date(t).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
  const nowMin = () => Math.floor(Date.now() / 6e4);
  const ceil5 = v => Math.ceil(v / 5) * 5;

  function answerLog(s) {
    const out = [], row = x => ({ t: +x[0], id: String(x[1] || '').split('#')[0], ok: !!x[2], secs: x[3] > 0 ? +x[3] : null });
    const ans = Array.isArray(s.ans) ? s.ans.filter(Array.isArray) : [], first = ans.length ? +ans[0][0] : Infinity;
    (s.ins && Array.isArray(s.ins.att) ? s.ins.att : []).forEach(x => { if (Array.isArray(x) && +x[0] < first) out.push(Object.assign(row(x), { secs: null })); });
    ans.forEach(x => out.push(row(x)));
    (s.ca && Array.isArray(s.ca.mlog) ? s.ca.mlog : []).forEach(x => { if (Array.isArray(x)) out.push(row(x)); });
    return out.filter(e => e.t > 0).sort((a, b) => a.t - b.t);
  }
  const nameOf = (A, id) => {
    if (A.ca) { const x = A.unitNames && A.unitNames[id]; return x ? x.title : id; }
    const m = /^(\d+)-([a-z]+)-(\d+)$/.exec(id); return m ? `${chapName(+m[1], m[2], +m[3])} (${subjName(+m[1], m[2])})` : id;
  };

  function trendOf(s, A) {
    const d56 = daysBack(56), weeks = [];
    for (let w = 0; w < 8; w++) {
      const ds = d56.slice(w * 7, w * 7 + 7); let m = 0, a = 0, r = 0, act = 0;
      ds.forEach(d => { m += minutesOn(s, d); const x = answersOn(s, d, A._caDays); a += x.a; r += x.r; if (A._active(d)) act++; });
      weeks.push({ start: ds[0], end: ds[6], m, a, r, acc: pctR(r, a), act, cons: act / 7 * 100 });
    }
    const half = ws => { const a = ws.reduce((x, w) => x + w.a, 0), r = ws.reduce((x, w) => x + w.r, 0), act = ws.reduce((x, w) => x + w.act, 0);
      return { m: ws.reduce((x, w) => x + w.m, 0) / 4, acc: pctR(r, a), cons: act / 28 * 100, any: ws.some(w => w.m >= 1 || w.a > 0 || w.act > 0) }; };
    const P = half(weeks.slice(0, 4)), L = half(weeks.slice(4)), T = { weeks, P, L, verdict: null };
    if (!L.any) return T;
    if (!P.any) { T.verdict = 'New'; return T; }
    const sm = L.m >= P.m * 1.15 && L.m - P.m >= 5 ? 1 : L.m <= P.m * 0.85 && P.m - L.m >= 5 ? -1 : 0;
    const da = L.acc != null && P.acc != null ? L.acc - P.acc : 0, sa = da >= 5 ? 1 : da <= -5 ? -1 : 0;
    const dc = L.cons - P.cons, sc = dc >= 10 ? 1 : dc <= -10 ? -1 : 0;
    T.score = sm + sa + sc; T.verdict = T.score >= 1 ? 'Improving' : T.score <= -1 ? 'Slipping' : 'Steady';
    return T;
  }

  async function masteryOf(s, A, log) {
    const groups = [], first = {};
    if (A.ca) {
      const level = (s.ca && s.ca.level) || 'foundation', st = await caStructure(level); if (!st) return null;
      const mc = {}, wr = {}, units = (s.ca && s.ca.units) || {};
      Object.entries((s.ca && s.ca.mcq) || {}).forEach(([key, v]) => { const u = key.split('#')[0], x = mc[u] || (mc[u] = { n: 0, r: 0 }); x.n += v.s || 0; x.r += (v.s || 0) - (v.w || 0); });
      Object.entries((s.ca && s.ca.writes) || {}).forEach(([key, h]) => { const sc = (h || []).filter(a => a && a.score != null && a.max && a.status !== 'waiting'); if (!sc.length) return; const u = key.split('#')[0], x = wr[u] || (wr[u] = { n: 0, p: 0 }); x.n++; x.p += Math.max(...sc.map(a => a.score / a.max)) * 100; });
      st.papers.forEach(pp => {
        const name = `${pp.key ? pp.key.toUpperCase().replace('P', 'Paper ') + ' · ' : ''}${pp.name}`, items = [];
        pp.chapters.forEach(ch => ch.units.forEach(u => {
          const m = mc[u.id] || { n: 0, r: 0 }, w = wr[u.id], dates = Object.values(units[u.id] || {}).filter(v => typeof v === 'string' && /^\d{4}-\d\d-\d\d/.test(v)).sort();
          const n = m.n + (w ? w.n : 0), acc = m.n ? m.r / m.n * 100 : w ? w.p / w.n : null;
          if (dates.length) first[u.id] = dates[0];
          items.push({ id: u.id, title: u.title, sub: name, ch: ch.title, qn: m.n, qr: m.r, n, acc, st: mStat(n, acc, dates.length > 0) });
        }));
        if (items.length) groups.push({ name, items });
      });
    } else {
      const cur = await curriculum(), g = +s.profile.grade, gr = cur && cur.grades && cur.grades[g]; if (!gr) return null;
      const mine = g >= 11 && Array.isArray(s.profile.subjects) && s.profile.subjects.length ? s.profile.subjects : null, touched = {};
      Object.entries(s.topics || {}).forEach(([tid, t]) => { const c = chapOf(tid); if (!c || !t) return; touched[c] = 1; if (t.last && (!first[c] || t.last < first[c])) first[c] = t.last; });
      (gr.subjects || []).filter(x => !mine || mine.includes(x.id)).forEach(sj => {
        const items = (sj.chapters || []).map(ch => { const id = `${g}-${sj.id}-${+ch.n}`, x = A.groups[id] || { n: 0, r: 0 }, acc = x.n ? x.r / x.n * 100 : null;
          return { id, title: ch.title, sub: sj.name, sid: sj.id, cn: +ch.n, qn: x.n, qr: x.r, n: x.n, acc, st: mStat(x.n, acc, !!touched[id]) }; });
        if (items.length) groups.push({ name: sj.name, sid: sj.id, items });
      });
    }
    log.forEach(e => { const id = A.ca ? e.id : chapOf(e.id); if (!id) return; const d = dk(e.t * 6e4); if (!first[id] || d < first[id]) first[id] = d; });
    groups.forEach(gp => { gp.total = gp.items.length; gp.started = gp.items.filter(x => x.st > 0).length; gp.good = gp.items.filter(x => x.st >= 2).length; gp.cnt = [0, 1, 2, 3].map(k => gp.items.filter(x => x.st === k).length); });
    const all = groups.flatMap(gp => gp.items), total = all.length, started = all.filter(x => x.st > 0).length;
    return { groups, all, first, total, started, good: all.filter(x => x.st >= 2).length, cov: total ? started / total * 100 : 0, cnt: [0, 1, 2, 3].map(k => all.filter(x => x.st === k).length) };
  }

  function mistakesOf(log) {
    const L = log.filter(e => e.t >= nowMin() - 60 * 1440);
    const okT = L.filter(e => e.ok && e.secs != null).map(e => e.secs), med = okT.length >= 5 ? median(okT) : null;
    const fastT = med != null ? Math.max(4, Math.round(med * 0.5)) : 6, wrongBy = {};
    L.forEach(e => { if (!e.ok) wrongBy[e.id] = (wrongBy[e.id] || 0) + 1; });
    let careless = 0, concept = 0, repeat = 0, unknown = 0;
    L.forEach(e => { if (e.ok) return; if (wrongBy[e.id] >= 3) { concept++; repeat++; } else if (e.secs == null) unknown++; else if (e.secs < fastT) careless++; else concept++; });
    return { careless, concept, repeat, unknown, fastT, med, total: careless + concept, timed: L.filter(e => e.secs != null).length,
      reps: Object.entries(wrongBy).filter(x => x[1] >= 3).sort((a, b) => b[1] - a[1]).slice(0, 3) };
  }
  function timeOf(log) {
    const L = log.filter(e => e.t >= nowMin() - 60 * 1440), rows = BUCKETS.map(([key, name, range]) => ({ key, name, range, a: 0, r: 0, secs: 0 }));
    L.forEach(e => { const h = new Date(e.t * 6e4).getHours(), i = BUCKETS.findIndex(b => b[3](h)), x = rows[i]; x.a++; if (e.ok) x.r++; if (e.secs) x.secs += e.secs; });
    rows.forEach(x => { x.acc = pctR(x.r, x.a); x.min = x.secs / 60; });
    const best = rows.filter(x => x.a >= 10).sort((a, b) => b.acc - a.acc || b.a - a.a)[0] || null;
    return { rows, best, total: L.length };
  }

  async function winsOf(s, A, log) {
    const W = {}, f14 = daysBack(14)[0];
    W.badges = Object.entries(s.badges || {}).filter(([id, d]) => BADGE[id] && d).sort((a, b) => a[1] < b[1] ? 1 : -1).map(([id, d]) => ({ e: BADGE[id][0], name: BADGE[id][1], d, fresh: d >= f14 }));
    if (A.ca) W.unitsDone = Object.values((s.ca && s.ca.units) || {}).filter(u => u && ['learn', 'illus', 'job', 'mcq', 'write', 'revise'].every(t => u[t])).length;
    const days = new Set();
    Object.keys(s.time || {}).forEach(d => { if (+s.time[d] >= 1) days.add(d); });
    Object.entries((s.ins && s.ins.day) || {}).forEach(([d, x]) => { if (x && (x.a > 0 || x.s >= 60 || x.q > 0)) days.add(d); });
    Object.entries((s.ca && s.ca.time) || {}).forEach(([d, v]) => { if (+v >= 60) days.add(d); });
    Object.keys(A._caDays).forEach(d => days.add(d));
    Object.values(s.topics || {}).forEach(t => { if (t && t.last) days.add(t.last); });
    let best = 0, run = 0, prev = null, end = null;
    [...days].filter(d => /^\d{4}-\d\d-\d\d$/.test(d)).sort().forEach(d => { run = prev && Math.round((dayDate(d) - dayDate(prev)) / DAY) === 1 ? run + 1 : 1; if (run > best) { best = run; end = d; } prev = d; });
    W.longest = best; W.longestEnd = end; W.current = A.streak;
    const cut = nowMin() - 14 * 1440, by = {};
    log.forEach(e => { const c = A.ca ? chapOf(e.id) : chapOf(e.id); if (!c) return; const x = by[c] || (by[c] = [0, 0, 0, 0]); if (e.t >= cut) { x[2]++; if (e.ok) x[3]++; } else { x[0]++; if (e.ok) x[1]++; } });
    W.improved = Object.entries(by).filter(([, x]) => x[0] >= 4 && x[2] >= 4).map(([id, x]) => ({ id, before: x[1] / x[0] * 100, now: x[3] / x[2] * 100 }))
      .filter(x => x.now - x.before >= 5).sort((a, b) => (b.now - b.before) - (a.now - a.before)).slice(0, 3)
      .map(x => Object.assign(x, { title: A.ca ? ((A.unitNames[x.id] || {}).title || x.id) : nameOf(A, x.id) }));
    const keys = new Set([...Object.keys(s.time || {}), ...Object.keys((s.ins && s.ins.day) || {}), ...Object.keys((s.ca && s.ca.time) || {}), ...Object.keys(A._caDays)].filter(d => /^\d{4}-\d\d-\d\d$/.test(d)));
    let bm = null, bq = null;
    [...keys].sort().forEach(d => { const m = minutesOn(s, d), q = answersOn(s, d, A._caDays).a; if (m >= 1 && (!bm || m > bm.v)) bm = { v: m, d }; if (q > 0 && (!bq || q > bq.v)) bq = { v: q, d }; });
    W.bestDay = bm; W.bestQ = bq;
    const tests = A.ca ? ((s.ca && s.ca.tests) || []).filter(t => t && t.pct != null).map(t => ({ pct: +t.pct, d: t.d, name: t.title || 'Test' }))
      : (s.ins && Array.isArray(s.ins.tl) && s.ins.tl.length ? s.ins.tl : Object.values(s.tests || {})).filter(t => t && t.pct != null).map(t => ({ pct: +t.pct, d: t.d, name: 'Chapter test' }));
    W.bestTest = tests.sort((a, b) => b.pct - a.pct)[0] || null;
    if (A.ca) { let bw = null; Object.values((s.ca && s.ca.writes) || {}).forEach(h => (h || []).forEach(a => { if (a && a.score != null && a.max > 0 && a.status !== 'waiting') { const p = a.score / a.max * 100; if (!bw || p > bw.pct) bw = { pct: p, d: a.d }; } })); W.bestWrite = bw; }
    return W;
  }

  function writesOf(s) {
    const at = [];
    Object.entries((s.ca && s.ca.writes) || {}).forEach(([key, h]) => (h || []).forEach(a => { if (a && a.score != null && a.max > 0 && a.status !== 'waiting') at.push({ key, d: a.d || '', p: a.score / a.max * 100, skills: Array.isArray(a.skills) ? a.skills : [] }); }));
    at.sort((a, b) => a.d < b.d ? -1 : a.d > b.d ? 1 : 0);
    const W = { n: at.length, at, avg: mean(at.map(a => a.p)) };
    if (at.length >= 6) { W.late = mean(at.slice(-5).map(a => a.p)); W.early = mean(at.slice(0, -5).map(a => a.p)); }
    const sk = {};
    at.forEach(a => a.skills.forEach(x => { if (!Array.isArray(x) || !x[0]) return; const o = sk[x[0]] || (sk[x[0]] = { id: x[0], m: 0, got: 0, n: 0 }); o.m += +x[1] || 0; o.got += Math.min(+x[2] || 0, +x[1] || 0); o.n++; }));
    W.skills = Object.values(sk).map(o => Object.assign(o, { lost: Math.round((o.m - o.got) * 100) / 100, keep: o.m ? o.got / o.m * 100 : null })).filter(o => o.lost > 0).sort((a, b) => b.lost - a.lost || a.keep - b.keep).slice(0, 3);
    return W;
  }

  async function deep(A) {
    const hit = MEMO.get(A.s); if (hit) return hit;
    const s = A.s, log = answerLog(s), X = { log };
    X.trend = trendOf(s, A);
    X.mastery = await masteryOf(s, A, log);
    X.first = X.mastery ? X.mastery.first : {};
    X.mist = mistakesOf(log);
    X.reps = [];
    for (const [id, n] of X.mist.reps) { let t = null; if (A.ca) t = (A.unitNames[id] || {}).title || id; else { const x = await topicTitle(id); t = x ? `${x.title} (${x.sub})` : id; } X.reps.push({ id, n, title: t }); }
    X.time = timeOf(log);
    X.wins = await winsOf(s, A, log);
    if (A.ca) X.writes = writesOf(s);
    MEMO.set(A.s, X);
    return X;
  }

  /* readiness 0–100 = 40% syllabus covered + 35% accuracy + 15% consistency (active days of the last 14) + 10% recency */
  function readinessOf(A, X, c) {
    const M = X.mastery; if (!M || !M.total) return null;
    const ex = nextExam(c), caEx = A.ca && A.s.ca && A.s.ca.exam && daysTo(A.s.ca.exam) >= 0 ? { name: 'CA exam', date: A.s.ca.exam } : null, exam = ex || caEx;
    let items = M.all, scope = '';
    if (!A.ca && ex && ex.subjects) {
      const want = String(ex.subjects).toLowerCase().split(/,|&|\/|\band\b/).map(x => x.trim()).filter(x => x.length >= 3);
      const gs = M.groups.filter(g => { const n = g.name.toLowerCase(); return want.some(w => n.startsWith(w) || w.startsWith(n) || (g.sid && (g.sid.startsWith(w) || w.startsWith(g.sid)))); });
      if (gs.length) { items = gs.flatMap(g => g.items); scope = gs.map(g => g.name).join(', '); }
    }
    const total = items.length, started = items.filter(x => x.st > 0).length, C = started / total * 100;
    const qn = items.reduce((a, x) => a + x.qn, 0), qr = items.reduce((a, x) => a + x.qr, 0), accs = items.filter(x => x.acc != null).map(x => x.acc);
    const Acc = qn ? qr / qn * 100 : accs.length ? mean(accs) : 0;
    const K = daysBack(14).filter(A._active).length / 14 * 100;
    const Rc = A.sinceDays == null ? 0 : Math.max(0, 100 - A.sinceDays / 7 * 100);
    const score = Math.round(0.4 * C + 0.35 * Acc + 0.15 * K + 0.1 * Rc);
    const R = { score, C, Acc, K, Rc, total, started, scope, exam, dl: exam ? daysTo(exam.date) : null };
    const from = daysBack(28)[0];
    R.newN = items.filter(x => x.st > 0 && X.first[x.id] && X.first[x.id] >= from).length;
    R.min28 = daysBack(28).reduce((a, d) => a + minutesOn(A.s, d), 0);
    const unit = A.ca ? 'unit' : 'chapter', pl = n => `${n} ${unit}${n === 1 ? '' : 's'}`;
    if (score >= 80) { R.msg = `In the ready zone. Keep revising ${A.ca ? 'units' : 'chapters'} and practising to stay above 80.`; return R; }
    const need = 80 - score, maxGain = 0.4 * (100 - C);
    if (need > maxGain + 1e-9) { R.msg = `Covering every ${unit} adds up to ${Math.floor(maxGain)} points. To reach 80, accuracy must also rise (now ${pctS(Acc)}) — revise the weak ${unit}s.`; return R; }
    R.chNeed = Math.max(1, Math.ceil(need / 0.4 / 100 * total - 1e-9));
    const pace = R.newN / 28;
    if (pace > 0) { R.daysNeed = Math.ceil(R.chNeed / pace - 1e-9); R.reach = noon() + R.daysNeed * DAY; }
    R.msg = pace > 0 ? `At this pace (${pl(R.newN)} started in the last 4 weeks) ${esc(A.name)} will reach 80 by <b>${fmtLong(R.reach)}</b> — about ${pl(R.chNeed)} more to start.`
      : `No new ${unit}s were started in the last 4 weeks. Starting ${pl(R.chNeed)} more lifts the score to 80.`;
    if (exam && R.dl > 0 && (!pace || R.daysNeed > R.dl)) {
      const perCh = R.newN ? R.min28 / R.newN : 60, req = R.chNeed * perCh / R.dl, curDay = R.min28 / 28;
      R.add = Math.max(5, ceil5(req - curDay));
      R.msg += ` To be ready by ${esc(exam.name)} (${R.dl} day${R.dl === 1 ? '' : 's'}), add about <b>${R.add > 240 ? 'more than 4 hours' : R.add + ' min'}/day</b> (now ${Math.round(curDay)} min/day).`;
    } else if (exam && R.reach && R.dl > 0) R.msg += ` That is before ${esc(exam.name)} ✅`;
    return R;
  }

  /* ---------- small SVG charts (one axis each; values also in the aria-label and a table) ---------- */
  function weekBarsSVG(T) {
    const W = 352, H = 150, top = 20, bot = 28, n = T.weeks.length, slot = W / n, bw = Math.min(26, slot - 12);
    const max = Math.max(30, ...T.weeks.map(w => w.m)), y = v => top + (H - top - bot) * (1 - v / max);
    const bars = T.weeks.map((w, i) => { const cx = i * slot + (slot - bw) / 2, m = Math.round(w.m), h = Math.max(0, H - bot - y(w.m)), last = i === n - 1;
      return `<g><title>Week of ${fmtDay(w.start)}: ${fmtMin(m)}</title>${h > 0 ? `<path d="M${cx},${H - bot} V${H - bot - h + Math.min(4, h)} q0,-4 4,-4 h${bw - 8} q4,0 4,4 V${H - bot} Z" class="pv-bar"/>` : ''}
        <text x="${cx + bw / 2}" y="${H - bot - h - 6}" class="pv-bv">${m || ''}</text><text x="${cx + bw / 2}" y="${H - 10}" class="pv-bx${last ? ' on' : ''}">${last ? 'This wk' : fmtDay(w.start)}</text></g>`; }).join('');
    return `<svg viewBox="0 0 ${W} ${H}" class="pv-chart" role="img" aria-label="Minutes studied per week, last 8 weeks: ${esc(T.weeks.map(w => `week of ${fmtDay(w.start)} ${Math.round(w.m)} min`).join(', '))}"><line x1="0" x2="${W}" y1="${H - bot}" y2="${H - bot}" class="pv-axis"/>${bars}</svg>`;
  }
  function lineSVG(series, labels, aria, opt = {}) {      // series: [{ cls, name, vals: [0–100 | null] }]
    const W = 352, H = 150, l = 34, r = 26, top = 12, bot = 26, n = labels.length;
    const x = i => n === 1 ? (l + W - r) / 2 : l + i * (W - l - r) / (n - 1), y = v => top + (H - top - bot) * (1 - v / 100);
    const grid = [0, 50, 100].map(v => `<line x1="${l}" x2="${W - r}" y1="${y(v)}" y2="${y(v)}" class="pv-grid"/><text x="${l - 6}" y="${y(v) + 3.5}" class="pv-yl">${v}%</text>`).join('');
    const xl = labels.map((t, i) => (n <= 8 || i % Math.ceil(n / 6) === 0 || i === n - 1) ? `<text x="${x(i)}" y="${H - 8}" class="pv-bx">${esc(t)}</text>` : '').join('');
    const lines = series.map(sr => {
      let d = '', pen = false; sr.vals.forEach((v, i) => { if (v == null) { pen = false; return; } d += `${pen ? 'L' : 'M'}${x(i).toFixed(1)},${y(v).toFixed(1)} `; pen = true; });
      const dots = sr.vals.map((v, i) => v == null ? '' : `<g><title>${esc(sr.name)} · ${esc(opt.tips ? opt.tips[i] : labels[i])}: ${Math.round(v)}%</title><rect x="${x(i) - 11}" y="${y(v) - 11}" width="22" height="22" class="pv-hit"/>${sr.sq ? `<rect x="${x(i) - 4}" y="${y(v) - 4}" width="8" height="8" class="pv-mk ${sr.cls}"/>` : `<circle cx="${x(i)}" cy="${y(v)}" r="4" class="pv-mk ${sr.cls}"/>`}</g>`).join('');
      return `${sr.noLine ? '' : `<path d="${d}" class="pv-ln ${sr.cls}"/>`}${dots}`;
    }).join('');
    return `<svg viewBox="0 0 ${W} ${H}" class="pv-chart" role="img" aria-label="${esc(aria)}">${grid}${xl}${lines}</svg>`;
  }
  const legend = items => `<ul class="pv-leg" aria-hidden="true">${items.map(([cls, t, sq]) => `<li><i class="pv-sw ${cls}${sq ? ' sq' : ''}"></i>${esc(t)}</li>`).join('')}</ul>`;

  /* ---------- the new cards ---------- */
  function readinessHTML(A, R) {
    if (!R) return '';
    const parts = [['Syllabus covered', R.C, 40, `${R.started} of ${R.total} ${A.ca ? 'units' : 'chapters'}${R.scope ? ' · ' + esc(R.scope) : ''}`], ['Accuracy', R.Acc, 35, 'correct answers'], ['Consistency', R.K, 15, `${Math.round(R.K * 14 / 100)} of the last 14 days`], ['Recency', R.Rc, 10, A.sinceDays == null ? 'not studied yet' : A.sinceDays === 0 ? 'studied today' : `last study ${A.sinceDays} day${A.sinceDays === 1 ? '' : 's'} ago`]];
    const band = R.score >= 80 ? ['ok', 'Ready'] : R.score >= 60 ? ['warn', 'Getting there'] : ['bad', 'Needs work'];
    return `<section class="pv-card" aria-labelledby="pvRd"><h3 id="pvRd">🎓 Exam readiness</h3>
      ${R.exam ? `<p class="pv-mut">For <b>${esc(R.exam.name)}</b> on ${esc(fmtDay(R.exam.date))} · ${R.dl === 0 ? 'today' : R.dl + ' day' + (R.dl === 1 ? '' : 's') + ' left'}</p>` : `<p class="pv-mut">Add an exam in the Exam planner below to get a target date.</p>`}
      <div class="pv-rd"><div class="pv-ring" role="img" aria-label="Readiness ${R.score} out of 100" style="--p:${R.score}"><b>${R.score}</b><small>/100</small></div>
        <div class="pv-rd-in"><span class="pv-st ${band[0]}">${band[1]}</span><p class="pv-rd-msg" id="pvRdMsg">${R.msg}</p></div></div>
      <ul class="pv-list pv-gl1 pv-brk">${parts.map(([n, v, w, sub]) => `<li><span class="pv-gt"><b>${n} <small class="pv-mut">×${w}%</small></b><span class="pv-mut">${sub}</span></span><span class="pv-sbar" aria-hidden="true"><i style="width:${Math.round(v)}%"></i></span><span class="pv-pill">${Math.round(v)}</span></li>`).join('')}</ul>
      <p class="pv-note">Score = 40% syllabus covered + 35% accuracy + 15% consistency + 10% recency. 80+ means ready.</p></section>`;
  }
  function trendHTML(A, T) {
    const any = T.weeks.some(w => w.m >= 1 || w.a > 0);
    if (!any) return `<section class="pv-card" aria-labelledby="pvTr"><h3 id="pvTr">📈 8-week trend</h3><p class="pv-empty">No study recorded in the last 8 weeks yet.</p></section>`;
    const V = { Improving: ['ok', '📈 Improving'], Steady: ['warn', '➡️ Steady'], Slipping: ['bad', '📉 Slipping'], New: ['ok', '🌱 Just started'] }[T.verdict] || ['', 'Not enough weeks yet'];
    const why = T.verdict === 'New' ? `${esc(A.name)} started in the last 4 weeks — the trend shows after a few more weeks.` : T.verdict
      ? `Last 4 weeks vs the 4 before: ${fmtMin(T.L.m)}/week (was ${fmtMin(T.P.m)}), ${pctS(T.L.acc)} correct (was ${pctS(T.P.acc)}), active ${(T.L.cons * 7 / 100).toFixed(1)} days/week (was ${(T.P.cons * 7 / 100).toFixed(1)}).` : '';
    const labels = T.weeks.map((w, i) => i === 7 ? 'This wk' : fmtDay(w.start));
    return `<section class="pv-card" aria-labelledby="pvTr"><h3 id="pvTr">📈 8-week trend</h3>
      <p class="pv-verdict"><span class="pv-st ${V[0]}" id="pvTrV">${V[1]}</span></p>${why ? `<p class="pv-mut">${why}</p>` : ''}
      <h4>Study time per week (minutes)</h4>${weekBarsSVG(T)}
      <h4>Accuracy and consistency</h4>${legend([['acc', 'Accuracy (% correct)'], ['con', 'Consistency (active days ÷ 7)', 1]])}
      ${lineSVG([{ cls: 'acc', name: 'Accuracy', vals: T.weeks.map(w => w.acc) }, { cls: 'con', name: 'Consistency', sq: 1, vals: T.weeks.map(w => w.cons) }], labels,
        `Accuracy and consistency per week: ${T.weeks.map(w => `week of ${fmtDay(w.start)} accuracy ${pctS(w.acc)}, ${w.act} of 7 days active`).join('; ')}`, { tips: T.weeks.map(w => 'week of ' + fmtDay(w.start)) })}
      <details class="pv-tbl"><summary>Show as a table</summary><table><thead><tr><th scope="col">Week of</th><th scope="col">Time</th><th scope="col">Correct</th><th scope="col">Days</th></tr></thead>
        <tbody>${T.weeks.map(w => `<tr><td>${esc(fmtDay(w.start))}</td><td>${fmtMin(w.m)}</td><td>${pctS(w.acc)}${w.a ? ` <small>(${w.a})</small>` : ''}</td><td>${w.act}/7</td></tr>`).join('')}</tbody></table></details></section>`;
  }
  function masteryHTML(A, M) {
    if (!M) return '';
    const u = A.ca ? 'units' : 'chapters', openG = M.groups.slice().sort((a, b) => b.started - a.started)[0];   // open the most-studied subject / paper
    const chip = x => `<li class="pv-chip ${MST[x.st][1]}" title="${esc(x.title)} — ${MST[x.st][0]}${x.acc != null ? `, ${Math.round(x.acc)}% in ${x.n} answers` : ''}"><span class="pv-ci" aria-hidden="true">${MST[x.st][2]}</span><span class="pv-ct">${esc(x.title)}</span><span class="sr-only">: ${MST[x.st][0]}${x.acc != null ? `, ${Math.round(x.acc)}% correct in ${x.n} answers` : ''}</span>${x.acc != null ? `<small aria-hidden="true">${Math.round(x.acc)}%</small>` : ''}</li>`;
    return `<section class="pv-card" aria-labelledby="pvMm"><h3 id="pvMm">🗺️ Mastery map</h3>
      <p><b id="pvMmCov">${Math.round(M.cov)}%</b> of the syllabus started (${M.started} of ${M.total} ${u}) · <b>${M.good}</b> good or mastered.</p>
      <ul class="pv-leg pv-mleg">${MST.map(([n, cls, ic], i) => `<li><span class="pv-chip ${cls} mini" aria-hidden="true">${ic}</span>${n} <b>${M.cnt[i]}</b></li>`).join('')}</ul>
      ${M.groups.map(g => `<details class="pv-mg"${g === openG ? ' open' : ''}><summary><span class="pv-mgn">${esc(g.name)}</span><span class="pv-sbar" aria-hidden="true"><i style="width:${Math.round(g.started / g.total * 100)}%"></i></span><span class="pv-mut">${g.started}/${g.total}</span></summary>
        <ul class="pv-chips">${g.items.map(chip).join('')}</ul></details>`).join('')}
      <p class="pv-note">Learning = fewer than 5 answers or under 60% correct · Good = 60%+ · Mastered = 85%+ in 8 or more answers.</p></section>`;
  }
  function mistakeHTML(A, X) {
    const m = X.mist, enough = m.total >= 5 && (m.timed >= 10 || m.repeat >= 3);
    const body = !enough ? `<p class="pv-empty">No data yet — this fills in after about 10 timed answers with a few mistakes (${m.timed} timed answers so far).</p>` : (() => {
      const pc = v => Math.round(v / m.total * 100), main = m.careless > m.concept ? 'careless' : 'concept';
      return `<div class="pv-split" role="img" aria-label="Careless slips ${m.careless}, concept gaps ${m.concept}"><i class="cs" style="width:${pc(m.careless)}%"></i><i class="cg" style="width:${100 - pc(m.careless)}%"></i></div>
        <div class="pv-kpis two"><div><b id="pvMtC">${m.careless}</b><span><i class="pv-sw sq cs"></i> ⚡ Careless slips · ${pc(m.careless)}%<br><small>fast (under ${m.fastT} s) and wrong</small></span></div>
          <div><b id="pvMtG">${m.concept}</b><span><i class="pv-sw sq cg"></i> 🧩 Concept gaps · ${pc(m.concept)}%<br><small>slow and wrong, or wrong again and again</small></span></div></div>
        <p>${main === 'careless' ? `Most mistakes are <b>slips</b>. Ask ${esc(A.name)} to read each question twice and check before tapping.` : `Most mistakes are <b>concept gaps</b>. Re-learning the lesson helps more than doing more questions.`}</p>
        ${X.reps.length ? `<h4>Wrong again and again</h4><ul class="pv-list pv-gl1">${X.reps.map(r => `<li><span class="pv-gt"><b>${esc(r.title)}</b></span><span class="pv-pill">${r.n}× wrong</span></li>`).join('')}</ul>` : ''}
        <p class="pv-note">Last 60 days. “Fast” = under half of ${esc(A.name)}'s usual time on a correct answer${m.med != null ? ` (${Math.round(m.med)} s)` : ''}. A topic with 3+ wrong answers counts as a concept gap.</p>`; })();
    return `<section class="pv-card" aria-labelledby="pvMt"><h3 id="pvMt">🔍 Careless or concept?</h3>${body}</section>`;
  }
  function timeHTML(A, X) {
    const t = X.time;
    if (t.total < 20) return `<section class="pv-card" aria-labelledby="pvBt"><h3 id="pvBt">⏰ Best study time</h3><p class="pv-empty">No data yet — shows after about 20 answers (${t.total} so far).</p></section>`;
    const max = Math.max(...t.rows.map(x => x.a), 1);
    return `<section class="pv-card" aria-labelledby="pvBt"><h3 id="pvBt">⏰ Best study time</h3>
      ${t.best ? `<p id="pvBtRec">✨ <b>${esc(t.best.name)}</b> (${esc(t.best.range)}) works best: ${pctS(t.best.acc)} correct. Try to keep the main study slot then.</p>` : '<p>Not enough answers in one time slot yet to recommend one.</p>'}
      <ul class="pv-list pv-tod">${t.rows.map(x => `<li${t.best && x.key === t.best.key ? ' class="best"' : ''}><span class="pv-gt"><b>${esc(x.name)}</b><span class="pv-mut">${esc(x.range)}</span></span>
        <span class="pv-sbar" aria-hidden="true"><i style="width:${Math.round(x.a / max * 100)}%"></i></span><span class="pv-todv">${x.a ? `${pctS(x.acc)} correct<br><small>${x.a} answers · ${fmtMin(x.min)}</small>` : '<small>no answers</small>'}</span></li>`).join('')}</ul>
      <p class="pv-note">Last 60 days. Bars = number of answers; time = time spent on questions.</p></section>`;
  }
  function cheerText(A, W) {
    const L = [`🎉 Well done, ${A.name}! I'm proud of you.`];
    if (W.current >= 2) L.push(`🔥 ${W.current}-day study streak!`);
    if (W.badges[0]) L.push(`🏅 New badge: ${W.badges[0].e} ${W.badges[0].name}`);
    if (W.improved[0]) L.push(`📈 ${W.improved[0].title}: ${Math.round(W.improved[0].before)}% → ${Math.round(W.improved[0].now)}%`);
    if (W.bestTest) L.push(`⭐ Best test score: ${Math.round(W.bestTest.pct)}%`);
    L.push('Keep going! 💪');
    return L.join('\n');
  }
  function winsHTML(A, X) {
    const W = X.wins, rows = [];
    if (W.longest) rows.push(['🔥', `Longest streak: <b>${W.longest} day${W.longest === 1 ? '' : 's'}</b>`, W.current ? `now ${W.current} day${W.current === 1 ? '' : 's'}` : '']);
    if (W.bestDay) rows.push(['⏱️', `Most study in a day: <b>${fmtMin(W.bestDay.v)}</b>`, fmtDay(W.bestDay.d)]);
    if (W.bestQ) rows.push(['✅', `Most questions in a day: <b>${W.bestQ.v}</b>`, fmtDay(W.bestQ.d)]);
    if (W.bestTest) rows.push(['⭐', `Best test: <b>${Math.round(W.bestTest.pct)}%</b>`, W.bestTest.d ? fmtDay(W.bestTest.d) : '']);
    if (W.bestWrite) rows.push(['✍️', `Best written answer: <b>${Math.round(W.bestWrite.pct)}%</b>`, W.bestWrite.d ? fmtDay(W.bestWrite.d) : '']);
    if (A.ca && W.unitsDone) rows.push(['📗', `Units fully completed: <b>${W.unitsDone}</b>`, '']);
    const nothing = !rows.length && !W.badges.length && !W.improved.length;
    const txt = cheerText(A, W);
    return `<section class="pv-card" aria-labelledby="pvWn"><h3 id="pvWn">🏆 Wins to celebrate</h3>
      ${nothing ? '<p class="pv-empty">Wins appear here after the first few study days.</p>' : `
      ${W.badges.length ? `<h4>Badges</h4><ul class="pv-badges">${W.badges.slice(0, 8).map(b => `<li${b.fresh ? ' class="new"' : ''}><span aria-hidden="true">${b.e}</span><b>${esc(b.name)}</b><small>${esc(fmtDay(b.d))}${b.fresh ? ' · new' : ''}</small></li>`).join('')}</ul>` : ''}
      ${W.improved.length ? `<h4>Improved most (last 2 weeks vs before)</h4><ul class="pv-list pv-gl1">${W.improved.map(x => `<li><span class="pv-gt"><b>${esc(x.title)}</b></span><span class="pv-pill">${Math.round(x.before)}% → ${Math.round(x.now)}%</span></li>`).join('')}</ul>` : ''}
      ${rows.length ? `<h4>Personal bests</h4><ul class="pv-list pv-pb">${rows.map(([i, t, d]) => `<li><span aria-hidden="true">${i}</span><span>${t}</span>${d ? `<small class="pv-mut">${esc(d)}</small>` : ''}</li>`).join('')}</ul>` : ''}
      <a class="pv-btn pv-wa" id="pvCheer" href="https://wa.me/?text=${encodeURIComponent(txt)}" target="_blank" rel="noopener">Send a cheer on WhatsApp 🎉</a>`}</section>`;
  }
  function writesHTML(A, X) {
    const W = X.writes; if (!A.ca || !W) return '';
    if (!W.n) return `<section class="pv-card" aria-labelledby="pvWr"><h3 id="pvWr">✍️ Written answers</h3><p class="pv-empty">No written answers checked yet. ${esc(A.name)} writes them in each unit's Write tab.</p></section>`;
    const at = W.at.slice(-30), ra = at.map((a, i) => mean(at.slice(Math.max(0, i - 2), i + 1).map(x => x.p)));
    const tr = W.late != null ? (W.late - W.early >= 5 ? ['ok', '📈 Improving'] : W.early - W.late >= 5 ? ['bad', '📉 Slipping'] : ['warn', '➡️ Steady']) : null;
    return `<section class="pv-card" aria-labelledby="pvWr"><h3 id="pvWr">✍️ Written answers</h3>
      <p>Average <b id="pvWrAvg">${pctS(W.avg)}</b> over <b>${W.n}</b> checked answer${W.n === 1 ? '' : 's'}${tr ? ` · last 5: <b>${pctS(W.late)}</b> (before: ${pctS(W.early)}) <span class="pv-st ${tr[0]}">${tr[1]}</span>` : ''}</p>
      ${legend([['wr', 'Each answer', 1], ['acc', 'Average of last 3']])}
      ${lineSVG([{ cls: 'wr', name: 'Answer', sq: 1, noLine: 1, vals: at.map(a => a.p) }, { cls: 'acc', name: 'Average of last 3', vals: ra }], at.map(a => a.d ? fmtDay(a.d) : ''),
        `Written answer marks in order: ${at.map(a => `${a.d ? fmtDay(a.d) : ''} ${Math.round(a.p)}%`).join(', ')}`, { tips: at.map(a => a.d ? fmtDay(a.d) : 'answer') })}
      <h4>Where marks are lost most</h4>${W.skills.length ? `<ul class="pv-list" id="pvWrSk">${W.skills.map(o => `<li><b>${esc(SKN[o.id] || o.id)}</b> — lost ${o.lost} mark${o.lost === 1 ? '' : 's'} (kept ${pctS(o.keep)})<br><span class="pv-mut">Tip: ${esc(SKTIP[o.id] || '')}</span></li>`).join('')}</ul>` : '<p class="pv-mut">No lost marks recorded by skill yet.</p>'}
      <p class="pv-note">Marks from the automatic checker against the ICAI-style marking scheme. Points that need an examiner's judgement are not counted.</p></section>`;
  }
  const focusDoneDate = (s, f) => { const d = s && s.focusDone && s.focusDone[f.id], sd = f.set_at ? dk(new Date(f.set_at)) : ''; return typeof d === 'string' && d >= sd ? d : null; };
  function focusHTML(A, X, c) {
    const M = X.mastery; if (!M) return '';
    const f = c.focus && c.focus.id ? c.focus : null, done = f ? focusDoneDate(A.s, f) : null;
    const weakIds = new Set(A.weak.map(g => g.id));
    const sugg = M.all.filter(x => x.st === 1 || weakIds.has(x.id) || (A.ca && weakIds.has(chapOf(x.id)))).sort((a, b) => (a.acc == null ? 101 : a.acc) - (b.acc == null ? 101 : b.acc)).slice(0, 8);
    const opt = x => `<option value="${esc(x.id)}">${esc(x.title)}${x.acc != null ? ` — ${Math.round(x.acc)}%` : ''} (${MST[x.st][0]})</option>`;
    return `<section class="pv-card" aria-labelledby="pvFo"><h3 id="pvFo">🎯 Focus topic (mission)</h3>
      <p class="pv-mut">Pick one ${A.ca ? 'unit' : 'chapter'}. ${esc(A.name)} sees “Today's mission from your parent” on their home screen with a button to practise it.</p>
      ${f ? `<div class="pv-fnow" id="pvFoNow"><p>Current mission: <b>${esc(f.title)}</b>${f.subject ? ` <span class="pv-mut">(${esc(f.subject)})</span>` : ''}<br><span class="pv-mut">Set on ${esc(fmtDay(dk(new Date(f.set_at || Date.now()))))}</span></p>
        <p>${done ? `<span class="pv-st ok" id="pvFoSt">Done ✓ on ${esc(fmtDay(done))}</span>` : '<span class="pv-st warn" id="pvFoSt">Not practised yet</span>'}</p>
        <button class="pv-btn ghost" type="button" id="pvFoClr">Clear mission</button></div>` : ''}
      <form id="pvFoF" class="pv-form" novalidate><label for="pvFoSel">${f ? 'Change mission' : 'Choose a mission'}</label>
        <select id="pvFoSel" class="pv-in"><option value="">— Choose —</option>${sugg.length ? `<optgroup label="Suggested (needs practice)">${sugg.map(opt).join('')}</optgroup>` : ''}
        ${M.groups.map(g => `<optgroup label="${esc(g.name)}">${g.items.map(opt).join('')}</optgroup>`).join('')}</select>
        <p class="pv-err" id="pvFoE" role="alert"></p><button class="pv-btn" type="submit">Set as mission</button></form></section>`;
  }

  function childHTML(k, A, X) {
    const c = k.controls || {}, s = A.s;
    const head = profileHTML(k, A);
    if (!A.has) {
      return head + `<div class="pv-card"><h3>No data yet</h3><p>${esc(A.name)}'s progress shows here after they study with the app while signed in. It updates about every 30 seconds while the app is open.</p></div>` + plannerHTML(A, c) + goalsHTML(A, c) + healthHTML(c) + manageHTML(A);
    }
    const alerts = A.alerts.length ? A.alerts.map(([t, m]) => `<li class="pv-al ${t}">${t === 'bad' ? '⚠️' : '🔔'} ${esc(m)}</li>`).join('') : '<li class="pv-al ok">✅ No alerts — all good this week.</li>';
    const sug = suggestions(A), dq = dinnerQs(A);
    const grp = g => `<li><span class="pv-gt"><b>${esc(g.title)}</b>${g.sub ? `<span class="pv-mut">${esc(g.sub)}</span>` : ''}</span><span class="pv-pill">${pctS(g.acc)} <small>· ${g.cnt} answers</small></span></li>`;
    const R = readinessOf(A, X, c);
    return head + `
      <section class="pv-card" aria-labelledby="pvAl"><h3 id="pvAl">Alerts</h3><ul class="pv-list">${alerts}</ul></section>
      ${readinessHTML(A, R)}
      <section class="pv-card" aria-labelledby="pvWk"><h3 id="pvWk">This week</h3>
        ${A.weekMin > 0 ? chartSVG(A) : '<p class="pv-empty">No study time recorded in the last 7 days.</p>'}
        <div class="pv-kpis">
          <div><b>${fmtMin(A.weekMin)}</b><span>Total time ${delta(A.weekMin, A.prevMin, ' min')}</span></div>
          <div><b>${A.daysActive}/7</b><span>Days active</span></div>
          <div><b>${A.streak}🔥</b><span>Day streak</span></div>
          <div><b>${A.qw.a}</b><span>Questions ${delta(A.qw.a, A.qp.a, '')}</span></div>
          <div><b>${pctS(A.accW)}</b><span>Correct ${delta(A.accW, A.accP, ' pts')}</span></div>
          <div><b>${fmtMin(A.today)}</b><span>Today</span></div>
        </div>
        <p class="pv-mut">Last week: ${fmtMin(A.prevMin)}, ${A.qp.a} questions, ${pctS(A.accP)} correct.</p></section>
      ${trendHTML(A, X.trend)}${masteryHTML(A, X.mastery)}
      <section class="pv-card" aria-labelledby="pvSt"><h3 id="pvSt">Strengths and needs help</h3>
        ${A.totalAns < 4 ? '<p class="pv-empty">No answers yet — strengths show after a few quizzes.</p>' : `
        <h4>💪 Strong</h4>${A.best.length ? `<ul class="pv-list pv-gl1">${A.best.map(grp).join('')}</ul>` : '<p class="pv-mut">Not enough answers in one chapter yet.</p>'}
        <h4>📌 Needs help</h4>${A.weak.length ? `<ul class="pv-list pv-gl1">${A.weak.map(grp).join('')}</ul>` : '<p class="pv-mut">No weak chapter found — well done.</p>'}
        ${A.subjects && A.subjects.length ? `<h4>By subject</h4><ul class="pv-list pv-gl1">${A.subjects.map(x => `<li><b>${esc(x.name)}</b><span class="pv-sbar" aria-hidden="true"><i style="width:${Math.round(x.acc)}%"></i></span><span class="pv-pill">${pctS(x.acc)}</span></li>`).join('')}</ul>` : ''}
        <p class="pv-mut">Mistakes recorded: <b>${A.mistakes}</b>${A.topMist.length ? ` · most common: ${A.topMist.map(x => `“${esc(x[0])}” ×${x[1]}`).join(', ')}` : ''}</p>`}
        <h4>🚀 Scope to improve</h4><ol class="pv-ol">${sug.map(x => `<li>${x}</li>`).join('') || '<li>Keep going — no suggestions yet.</li>'}</ol></section>
      ${mistakeHTML(A, X)}${timeHTML(A, X)}${winsHTML(A, X)}${writesHTML(A, X)}${focusHTML(A, X, c)}
      <section class="pv-card" aria-labelledby="pvDq"><h3 id="pvDq">🍽️ Dinner-table questions</h3>
        ${dq.length ? `<p class="pv-mut">From what ${esc(A.name)} studied recently. Ask with interest, not as a test.</p><ol class="pv-ol">${dq.map(x => `<li>${x}</li>`).join('')}</ol>` : '<p class="pv-empty">Questions appear after the first finished topic.</p>'}</section>
      ${plannerHTML(A, c)}${goalsHTML(A, c)}${healthHTML(c)}
      <section class="pv-card" aria-labelledby="pvRp"><h3 id="pvRp">📄 Weekly report card</h3><p class="pv-mut">A short summary to share with family or keep.</p>
        <pre class="pv-pre" id="pvRpTxt">${esc(reportText(A, c))}</pre>
        <div class="pv-row"><a class="pv-btn pv-wa" id="pvRpWa" href="https://wa.me/?text=${encodeURIComponent(reportText(A, c))}" target="_blank" rel="noopener">Share on WhatsApp</a><button class="pv-btn ghost" type="button" id="pvRpPr">Print / Save PDF</button></div></section>
      ${manageHTML(A)}`;
  }
  function plannerHTML(A, c) {
    const ex = (Array.isArray(c.exams) ? c.exams : []).slice().sort((a, b) => a.date < b.date ? -1 : 1);
    const caEx = A.has && A.ca && A.s.ca && A.s.ca.exam ? `<p class="pv-mut">${esc(A.name)}'s own CA exam date: <b>${esc(fmtDay(A.s.ca.exam))} ${esc(A.s.ca.exam.slice(0, 4))}</b>.</p>` : '';
    return `<section class="pv-card" aria-labelledby="pvEx"><h3 id="pvEx">📅 Exam planner</h3>${caEx}
      ${ex.length ? `<ul class="pv-list">${ex.map(e => { const P = examPlan(A, e), past = P.dl < 0;
        return `<li class="pv-exam${past ? ' past' : ''}"><div><b>${esc(e.name)}</b> <span class="pv-mut">${esc(fmtDay(e.date))}${e.subjects ? ' · ' + esc(e.subjects) : ''}</span><br>
          ${past ? '<span class="pv-mut">Done</span>' : `<span class="pv-days">${P.dl === 0 ? 'Today!' : P.dl + ' day' + (P.dl === 1 ? '' : 's') + ' left'}</span> <span class="pv-st ${P.st[0]}">${P.st[1]}</span>
          <br><span class="pv-mut">Last 7 days: ${Math.round(P.avg)} min/day · target ${P.target} min/day</span>`}</div>
          <button class="pv-x" type="button" data-exdel="${esc(e.id)}" aria-label="Remove ${esc(e.name)}">✕</button></li>`; }).join('')}</ul>
        <p class="pv-note">Target = daily goal (or 30 min) · ×1.25 when the exam is within 45 days · ×1.5 within 14 days. On track = at least 80% of the target.</p>` : '<p class="pv-empty">No exams added yet.</p>'}
      <form id="pvExF" class="pv-form" novalidate><div class="pv-row"><div class="pv-f"><label for="pvExN">Exam name</label><input id="pvExN" class="pv-in" maxlength="40" placeholder="Half-yearly"></div>
        <div class="pv-f"><label for="pvExD">Date</label><input id="pvExD" class="pv-in" type="date" min="${todayK()}"></div></div>
        <label for="pvExS">Subjects (optional)</label><input id="pvExS" class="pv-in" maxlength="80" placeholder="Maths, Science">
        <p class="pv-err" id="pvExE" role="alert"></p><button class="pv-btn" type="submit">Add exam</button></form></section>`;
  }
  function goalsHTML(A, c) {
    const rw = c.reward || {}, goal = +c.goal || 0, days = +rw.days || 7;
    const prog = goal && A.has ? `<div class="pv-prog"><p>Today: <b>${Math.floor(A.today)}/${goal} min</b>${A.today >= goal ? ' ✅' : ''} · Goal met on <b>${A.goalDays} of 7</b> days</p>
      <div class="pv-gbar"><i style="width:${Math.min(100, Math.round(A.today / goal * 100))}%"></i></div>
      ${rw.text ? `<p>Reward streak: <b>${Math.min(A.goalStreak, days)}/${days} days</b>${A.goalStreak >= days ? ` — 🎉 ${esc(A.name)} earned “${esc(rw.text)}”!` : ''}</p>` : ''}</div>` : '';
    return `<section class="pv-card" aria-labelledby="pvGo"><h3 id="pvGo">🎯 Goals and rewards</h3>${prog}
      <p class="pv-mut">${esc(A.name)} sees the goal and reward on their World and Me screens.</p>
      <form id="pvGoF" class="pv-form" novalidate><div class="pv-row"><div class="pv-f"><label for="pvGoM">Daily goal (minutes)</label><input id="pvGoM" class="pv-in" type="number" min="0" max="300" step="5" inputmode="numeric" value="${goal || ''}" placeholder="20"></div>
        <div class="pv-f"><label for="pvGoD">Days in a row for reward</label><input id="pvGoD" class="pv-in" type="number" min="1" max="60" inputmode="numeric" value="${rw.text ? days : ''}" placeholder="7"></div></div>
        <label for="pvGoR">Reward promise</label><input id="pvGoR" class="pv-in" maxlength="60" value="${esc(rw.text || '')}" placeholder="Pizza night 🍕">
        <p class="pv-err" id="pvGoE" role="alert"></p><button class="pv-btn" type="submit">Save goal</button></form></section>`;
  }
  function healthHTML(c) {
    const q = c.quiet || {};
    return `<section class="pv-card" aria-labelledby="pvHe"><h3 id="pvHe">🌱 Healthy use</h3>
      <p class="pv-mut">When time is up or during quiet hours your child sees a friendly “Time to rest” screen. You can unlock 15 minutes on their phone with your PIN.</p>
      <form id="pvHeF" class="pv-form" novalidate><div class="pv-row"><div class="pv-f"><label for="pvHeL">Daily limit (minutes, 0 = none)</label><input id="pvHeL" class="pv-in" type="number" min="0" max="600" step="5" inputmode="numeric" value="${+c.limit || 0}"></div>
        <div class="pv-f"><label for="pvHeB">Break reminder every (min, 0 = off)</label><input id="pvHeB" class="pv-in" type="number" min="0" max="180" step="5" inputmode="numeric" value="${+c.brk || 0}"></div></div>
        <label class="pv-chk"><input type="checkbox" id="pvHeQ" ${q.on ? 'checked' : ''}> Quiet hours (no study)</label>
        <div class="pv-row"><div class="pv-f"><label for="pvHeF1">From</label><input id="pvHeF1" class="pv-in" type="time" value="${esc(q.from || '21:00')}"></div><div class="pv-f"><label for="pvHeT1">To</label><input id="pvHeT1" class="pv-in" type="time" value="${esc(q.to || '06:00')}"></div></div>
        <label for="pvHeP">Parent PIN (4 digits) ${c.pinHash ? '<span class="pv-okt">— PIN is set ✓ (leave empty to keep)</span>' : ''}</label><input id="pvHeP" class="pv-in" type="password" inputmode="numeric" pattern="[0-9]*" maxlength="4" autocomplete="new-password" placeholder="${c.pinHash ? '••••' : 'e.g. 4826'}">
        <p class="pv-err" id="pvHeE" role="alert"></p><button class="pv-btn" type="submit">Save healthy use</button></form></section>`;
  }
  function manageHTML(A) {
    return `<section class="pv-card pv-manage" aria-labelledby="pvMg"><h3 id="pvMg">Link</h3><p class="pv-mut">Removing the link stops you seeing ${esc(A.name)}'s progress and turns off your goals and limits on their phone.</p><button class="pv-btn ghost danger" type="button" id="pvUnlink">Remove link</button></section>`;
  }

  function reportText(A, c) {
    const wk = daysBack(7), L = [];
    L.push(`📚 StudyVerse weekly report — ${A.name}${A.label ? ' (' + A.label + ')' : ''}`);
    L.push(`Week: ${fmtDay(wk[0])} – ${fmtDay(wk[6])}`);
    if (!A.has) { L.push('No study data yet.'); return L.join('\n'); }
    L.push(`⏱ Study time: ${fmtMin(A.weekMin)} on ${A.daysActive} of 7 days (last week ${fmtMin(A.prevMin)})`);
    L.push(`🔥 Streak: ${A.streak} day${A.streak === 1 ? '' : 's'}`);
    L.push(`✅ Questions: ${A.qw.a} answered${A.accW != null ? `, ${pctS(A.accW)} correct` : ''}${A.accP != null ? ` (last week ${pctS(A.accP)})` : ''}`);
    if (A.best[0]) L.push(`💪 Strong: ${A.best[0].title}${A.best[0].sub ? ' – ' + A.best[0].sub : ''} (${pctS(A.best[0].acc)})`);
    if (A.weak[0]) L.push(`📌 Needs help: ${A.weak[0].title}${A.weak[0].sub ? ' – ' + A.weak[0].sub : ''} (${pctS(A.weak[0].acc)})`);
    if (A.goal) L.push(`🎯 Goal ${A.goal} min/day — met on ${A.goalDays} of 7 days${c.reward && c.reward.text ? ` · reward “${c.reward.text}” streak ${Math.min(A.goalStreak, +c.reward.days || 7)}/${+c.reward.days || 7}` : ''}`);
    const ex = nextExam(c); if (ex) L.push(`📅 ${ex.name} in ${daysTo(ex.date)} days`);
    A.alerts.forEach(a => L.push('⚠️ ' + a[1]));
    return L.join('\n');
  }
  function printReport(A, c) {
    let p = D.getElementById('pvPrint'); if (!p) { p = D.createElement('div'); p.id = 'pvPrint'; D.body.appendChild(p); }
    const sug = A.has ? suggestions(A) : [];
    p.innerHTML = `<h1>StudyVerse — Weekly report card</h1><h2>${esc(A.name)}${A.label ? ' · ' + esc(A.label) : ''}</h2>
      <p class="pp-d">Week ${esc(fmtDay(daysBack(7)[0]))} – ${esc(fmtDay(todayK()))} · printed ${esc(new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' }))}</p>
      ${A.has ? `<div class="pp-chart">${chartSVG(A)}</div>` : ''}
      <pre>${esc(reportText(A, c))}</pre>
      ${sug.length ? `<h3>Scope to improve</h3><ol>${sug.map(x => `<li>${x}</li>`).join('')}</ol>` : ''}
      <p class="pp-f">study.moneyviel.com · Parent Hub</p>`;
    const done = () => { p.remove(); removeEventListener('afterprint', done); };
    addEventListener('afterprint', done);
    try { window.print(); } catch (e) {}
  }

  function wireChild(body, k, A, X) {
    const c = () => Object.assign({ v: 1 }, k.controls || {});
    const saveCtl = async (next, errEl, msg) => {
      errEl.textContent = '';
      try {
        const r = one(await rpc('set_child_controls', { p_child: k.child_id, p_controls: next }));
        if (r && r.ok === false) { errEl.textContent = r.msg || 'Could not save.'; return false; }
        k.controls = next; say(msg || 'Saved ✓'); render(); return true;
      } catch (e) { errEl.textContent = C().errText(e); return false; }
    };
    const ex = body.querySelector('#pvExF');
    ex.onsubmit = ev => { ev.preventDefault(); const e = body.querySelector('#pvExE'), n = body.querySelector('#pvExN').value.trim(), d = body.querySelector('#pvExD').value, sj = body.querySelector('#pvExS').value.trim();
      if (!n) { e.textContent = 'Enter the exam name.'; return; } if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) { e.textContent = 'Choose the exam date.'; return; }
      const next = c(); next.exams = (Array.isArray(next.exams) ? next.exams : []).concat({ id: Date.now().toString(36), name: n, date: d, subjects: sj });
      saveCtl(next, e, 'Exam added ✓'); };
    body.querySelectorAll('[data-exdel]').forEach(b => b.onclick = () => { const next = c(); next.exams = (next.exams || []).filter(x => x.id !== b.dataset.exdel); saveCtl(next, body.querySelector('#pvExE'), 'Exam removed'); });
    body.querySelector('#pvGoF').onsubmit = ev => { ev.preventDefault(); const e = body.querySelector('#pvGoE'), m = +body.querySelector('#pvGoM').value || 0, dd = +body.querySelector('#pvGoD').value || 7, t = body.querySelector('#pvGoR').value.trim();
      if (m < 0 || m > 300) { e.textContent = 'Goal: 0 to 300 minutes.'; return; } if (dd < 1 || dd > 60) { e.textContent = 'Streak: 1 to 60 days.'; return; }
      const next = c(); next.goal = Math.round(m); next.reward = t ? { text: t, days: Math.round(dd) } : null; saveCtl(next, e, 'Goal saved ✓'); };
    body.querySelector('#pvHeF').onsubmit = async ev => { ev.preventDefault(); const e = body.querySelector('#pvHeE');
      const lim = +body.querySelector('#pvHeL').value || 0, brk = +body.querySelector('#pvHeB').value || 0, on = body.querySelector('#pvHeQ').checked, from = body.querySelector('#pvHeF1').value, to = body.querySelector('#pvHeT1').value, pin = body.querySelector('#pvHeP').value.trim();
      if (lim < 0 || lim > 600) { e.textContent = 'Daily limit: 0 to 600 minutes.'; return; }
      if (lim && A.goal && lim < A.goal) { e.textContent = `The daily limit is less than the daily goal (${A.goal} min).`; return; }
      if (brk < 0 || brk > 180) { e.textContent = 'Break reminder: 0 to 180 minutes.'; return; }
      if (on && (!from || !to || from === to)) { e.textContent = 'Choose different From and To times.'; return; }
      if (pin && !/^\d{4}$/.test(pin)) { e.textContent = 'The PIN must be 4 digits.'; return; }
      const next = c(); next.limit = Math.round(lim); next.brk = Math.round(brk); next.quiet = { on, from: from || '21:00', to: to || '06:00' };
      if (pin) next.pinHash = await pinHash(k.child_id, pin);
      if ((lim || on) && !next.pinHash) { e.textContent = 'Please set a 4-digit PIN so you can unlock when needed.'; return; }
      saveCtl(next, e, 'Healthy use saved ✓'); };
    const fo = body.querySelector('#pvFoF');
    if (fo) fo.onsubmit = ev => { ev.preventDefault(); const e = body.querySelector('#pvFoE'), id = body.querySelector('#pvFoSel').value;
      const it = id && X && X.mastery ? X.mastery.all.find(x => x.id === id) : null;
      if (!it) { e.textContent = A.ca ? 'Choose a unit.' : 'Choose a chapter.'; return; }
      const next = c(); next.focus = { id: it.id, title: it.title, subject: it.sub || '', set_at: new Date().toISOString() };
      saveCtl(next, e, `Mission set: ${it.title} ✓`); };
    const fc = body.querySelector('#pvFoClr');
    if (fc) fc.onclick = () => { const next = c(); delete next.focus; saveCtl(next, body.querySelector('#pvFoE'), 'Mission cleared'); };
    const pr = body.querySelector('#pvRpPr'); if (pr) pr.onclick = () => printReport(A, k.controls || {});
    const ul = body.querySelector('#pvUnlink');
    ul.onclick = async () => {
      if (!ul.dataset.sure) { ul.dataset.sure = 1; ul.textContent = 'Tap again to remove the link'; return; }
      ul.disabled = true;
      try { await rpc('unlink', { p_other: k.child_id }); say('Link removed'); kids.splice(sel, 1); sel = 0; render(); }
      catch (e) { ul.disabled = false; say(C().errText(e)); }
    };
  }

  /* ================= styles ================= */
  const css = `
.pv-row{display:flex;gap:8px;flex-wrap:wrap}.pv-row>*{flex:1;min-width:140px}
.pv-me .btn,.pv-goal{min-height:44px}.pv-me .pv-row .btn{flex:1 1 180px}
.pv-ok{color:#1d7a46;font-weight:700;font-size:14px;margin:0 0 10px}
.card.pv-goal{border-left:5px solid #C9A76A;padding:12px 14px;font-size:14.5px;line-height:1.4}
.pv-goal-t{font-size:16px}.pv-goal-l{margin-top:4px;color:var(--ink)}.pv-goal-by{font-size:11.5px;color:var(--muted);margin-top:6px}
.pv-gbar{height:10px;border-radius:9px;background:#efe6d3;overflow:hidden;margin:8px 0 4px}.pv-gbar i{display:block;height:100%;background:linear-gradient(90deg,#C9A76A,#8A6A2E);border-radius:9px}
#pvBanner{position:fixed;left:50%;bottom:calc(86px + env(safe-area-inset-bottom));transform:translate(-50%,30px);opacity:0;pointer-events:none;z-index:970;width:min(92vw,420px);background:#15161C;color:#F4EAD8;border:1.5px solid #C9A76A;border-radius:14px;padding:12px 12px 12px 14px;display:flex;gap:10px;align-items:center;font-size:14.5px;line-height:1.35;transition:.25s;box-shadow:0 10px 30px rgba(0,0,0,.4)}
#pvBanner.show{opacity:1;transform:translate(-50%,0);pointer-events:auto}#pvBanner button{flex:none;min-width:52px;min-height:44px;border:0;border-radius:10px;background:#C9A76A;color:#15161C;font-weight:800;cursor:pointer}
#pvRest{position:fixed;inset:0;z-index:985;display:flex;align-items:center;justify-content:center;padding:24px;background:radial-gradient(120% 90% at 50% 0%,#5B0F1B 0%,#15161C 72%);color:#F4EAD8;text-align:center;overflow:auto}
.pv-rest-in{max-width:400px;width:100%}.pv-moon{font-size:64px;line-height:1;margin-bottom:10px}
#pvRest h1{font-size:26px;line-height:1.2;margin:0 0 12px;color:#F4EAD8;outline:none}#pvRest p{margin:0 0 10px;line-height:1.5;color:#eadcc2}.pv-rest-m b{color:#C9A76A}
.pv-rest-b{display:block;width:100%;min-height:48px;margin-top:12px;border-radius:14px;border:1.5px solid #C9A76A;background:transparent;color:#F4EAD8;font-size:16px;font-weight:700;cursor:pointer}
.pv-rest-b.gold{background:#C9A76A;color:#15161C;border:0}
#pvPinBox{margin-top:14px;text-align:left}#pvPinBox label{display:block;font-weight:700;margin-bottom:6px}
#pvPinIn{width:100%;box-sizing:border-box;font-size:28px;letter-spacing:12px;text-align:center;padding:10px;border-radius:12px;border:1.5px solid #C9A76A;background:#1f2029;color:#F4EAD8}
.pv-rest-e{color:#ffb3b3!important;min-height:20px;margin-top:8px!important}
.pv-code-in{font-size:24px!important;letter-spacing:6px;text-align:center;text-transform:uppercase}
.pv-bigcode{font-size:44px;font-weight:800;letter-spacing:10px;text-align:center;padding:14px 8px;margin:6px 0;border-radius:14px;background:#F4EAD8;color:#5B0F1B;border:2px dashed #C9A76A;font-family:ui-monospace,Menlo,Consolas,monospace}
.btn.pv-wa,.pv-btn.pv-wa{background:#1f8f4e;color:#fff;box-shadow:none;text-align:center;text-decoration:none;display:flex;align-items:center;justify-content:center}
.sheet.pv-hub{z-index:960;background:#F6F0E4;display:none;overflow-y:auto;overscroll-behavior:contain;align-items:stretch}
.sheet.pv-hub.show{display:block}
.pv-wrap{max-width:720px;margin:0 auto;padding:0 14px calc(28px + env(safe-area-inset-bottom));color:#15161C;font-family:Nunito,system-ui,sans-serif}
.pv-top{position:sticky;top:0;z-index:2;display:flex;align-items:center;gap:10px;margin:0 -14px;padding:10px 14px;background:linear-gradient(90deg,#5B0F1B,#7a1626);color:#F4EAD8}
.pv-top h1{flex:1;font-size:20px;margin:0;font-family:'Baloo 2',system-ui,sans-serif;color:#F4EAD8}
.pv-back,.pv-ref{min-height:44px;min-width:44px;border:1.5px solid rgba(244,234,216,.5);background:transparent;color:#F4EAD8;border-radius:12px;font-weight:700;font-size:15px;cursor:pointer;padding:0 12px}
.pv-tabs{display:flex;gap:8px;overflow-x:auto;padding:12px 0 6px}
.pv-tab{flex:none;min-height:44px;padding:0 16px;border-radius:999px;border:1.5px solid #C9A76A;background:#fff;color:#15161C;font-weight:800;font-size:15px;cursor:pointer}
.pv-tab.on{background:#15161C;color:#F4EAD8;border-color:#15161C}.pv-tab.pv-add{border-style:dashed;color:#8A6A2E}
.pv-body{display:grid;grid-template-columns:1fr;gap:12px;padding-top:6px}
.pv-card{background:#fff;border-radius:16px;padding:14px 16px;box-shadow:0 2px 10px rgba(21,22,28,.08);border:1px solid #eadfca}
.pv-card h2{font-size:20px;margin:0 0 2px;font-family:'Baloo 2',system-ui,sans-serif}
.pv-card h3{font-size:17px;margin:0 0 8px;color:#5B0F1B;font-family:'Baloo 2',system-ui,sans-serif}
.pv-card h4{font-size:14.5px;margin:12px 0 6px}
.pv-card p{margin:0 0 8px;font-size:14.5px;line-height:1.45}
.pv-mut{color:#5d5a55;font-size:13.5px}.pv-note{font-size:12.5px;color:#6b665e}.pv-empty{color:#6b665e;font-style:italic}
.pv-head{display:flex;gap:12px;align-items:center;border-left:5px solid #C9A76A}.pv-head p{margin:0}
.pv-av{width:52px;height:52px;flex:none;border-radius:50%;background:#F4EAD8;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;color:#5B0F1B}
.pv-list{list-style:none;margin:0;padding:0}.pv-list li{padding:8px 0;border-top:1px solid #f0e8d8;font-size:14.5px;line-height:1.4}.pv-list li:first-child{border-top:0}
.pv-gl1 li{display:flex;align-items:center;gap:8px}.pv-gl1 li>b{flex:0 0 34%}.pv-gt{flex:1;min-width:0;display:flex;flex-direction:column}.pv-gt .pv-mut{font-size:12.5px}.pv-pill small{font-weight:600;font-size:11.5px}
.pv-pill{flex:none;background:#F4EAD8;color:#5B0F1B;border-radius:999px;padding:3px 10px;font-weight:800;font-size:13px}
.pv-sbar{flex:1 1 80px;height:8px;background:#f1eadc;border-radius:8px;overflow:hidden}.pv-sbar i{display:block;height:100%;background:#8A6A2E;border-radius:8px}
.pv-al{padding:10px 12px!important;border-radius:12px;margin-bottom:6px;border:0!important}.pv-al.bad{background:#fbe9ea;color:#7a0f1a}.pv-al.warn{background:#fff4dc;color:#6b4a06}.pv-al.ok{background:#e8f5ec;color:#1d5e36}
.pv-chart{width:100%;max-width:520px;height:auto;display:block;margin:4px auto 8px}
.pv-bar{fill:#8A6A2E}.pv-axis{stroke:#d8ccb4;stroke-width:1}.pv-bv{font-size:11px;font-weight:800;fill:#15161C;text-anchor:middle}
.pv-bx{font-size:11px;fill:#5d5a55;text-anchor:middle}.pv-bx.on{font-weight:800;fill:#15161C}
.pv-gl{stroke:#B71C2C;stroke-width:1.5;stroke-dasharray:4 4}.pv-glt{font-size:10px;fill:#B71C2C;text-anchor:end;font-weight:700}
.pv-kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:6px 0 8px}
.pv-kpis div{background:#FBF7EF;border-radius:12px;padding:8px;text-align:center;border:1px solid #f0e6d2}
.pv-kpis b{display:block;font-size:18px;color:#15161C}.pv-kpis span{font-size:12px;color:#5d5a55;line-height:1.3;display:block}
.pv-d{display:block;font-weight:800;font-size:11.5px;color:#5d5a55}.pv-d.up{color:#1d7a46}.pv-d.dn{color:#B71C2C}
.pv-ol{margin:0;padding-left:20px}.pv-ol li{margin:6px 0;font-size:14.5px;line-height:1.45}
.pv-exam{display:flex;gap:8px;align-items:flex-start}.pv-exam>div{flex:1}.pv-exam.past{opacity:.6}
.pv-days{font-weight:800;color:#5B0F1B}.pv-st{font-weight:800;font-size:13px;padding:2px 8px;border-radius:999px;margin-left:4px}.pv-st.ok{background:#e8f5ec;color:#1d5e36}.pv-st.warn{background:#fff4dc;color:#6b4a06}.pv-st.bad{background:#fbe9ea;color:#7a0f1a}
.pv-x{flex:none;min-width:44px;min-height:44px;border:0;background:transparent;font-size:18px;cursor:pointer;color:#7a0f1a;border-radius:10px}
.pv-form{margin-top:8px}.pv-form label{display:block;font-weight:700;font-size:13px;margin:8px 0 4px}
.pv-f{flex:1;min-width:140px}.pv-form .pv-row{align-items:flex-end}
.pv-in{width:100%;box-sizing:border-box;min-height:44px;padding:10px 12px;border:1.5px solid #cfc3aa;border-radius:10px;font-size:16px;background:#fff;color:#15161C}
.pv-chk{display:flex!important;align-items:center;gap:10px;min-height:44px;font-size:14.5px!important}.pv-chk input{width:22px;height:22px}
.pv-err{color:#B71C2C!important;min-height:18px;font-size:13px!important;margin:6px 0!important}.pv-okt{color:#1d7a46;font-weight:700}
.pv-btn{min-height:46px;border:0;border-radius:12px;padding:10px 16px;font-weight:800;font-size:15.5px;cursor:pointer;background:#15161C;color:#F4EAD8;width:100%}
.pv-btn.ghost{background:#F4EAD8;color:#15161C}.pv-btn.danger{color:#B71C2C}
.pv-pre{white-space:pre-wrap;font-family:inherit;font-size:13.5px;background:#FBF7EF;border:1px solid #f0e6d2;border-radius:12px;padding:10px 12px;margin:0 0 10px;line-height:1.5}
.pv-steps{margin:6px 0 12px;padding-left:22px;line-height:1.6}.pv-hero{border-top:5px solid #C9A76A}
.pv-load{padding:20px;text-align:center;color:#5d5a55}
.sheet.pv-hub.pv-pro{background:#15161C}.pv-pro .pv-tab{background:#1f2029;color:#F4EAD8;border-color:#8A6A2E}.pv-pro .pv-tab.on{background:#C9A76A;color:#15161C;border-color:#C9A76A}
.pv-pro .pv-top{background:#0e0f13;border-bottom:1px solid #2b2c35}.pv-pro .pv-card{border-color:#2b2c35;box-shadow:none}
@media (min-width:900px){.pv-wrap{max-width:980px}.pv-body{display:block;columns:2;column-gap:12px}.pv-body>.pv-card{break-inside:avoid;margin-bottom:12px;display:block}.pv-body>.pv-head{display:flex}.pv-body>.pv-head,.pv-body>.pv-card:nth-child(2),.pv-body>.pv-hero{column-span:all}}
.pv-opts{display:grid;gap:10px;margin:10px 0}
.pv-opt{display:grid;grid-template-columns:44px 1fr;column-gap:12px;align-items:center;text-align:left;width:100%;min-height:72px;padding:12px 14px;border:1.5px solid #C9A76A;border-radius:14px;background:#FBF7EF;color:#15161C;cursor:pointer;font:inherit}
.pv-opt span{grid-row:span 2;font-size:30px;text-align:center}.pv-opt b{font-size:16px;line-height:1.25}.pv-opt small{font-size:13px;color:#5d5a55;line-height:1.35}
.pv-opt:hover,.pv-opt:focus-visible{background:#F4EAD8;border-color:#8A6A2E}
.pv-logo{font-family:'Baloo 2',system-ui,sans-serif;font-weight:800;font-size:15px;color:#F4EAD8;white-space:nowrap}.pv-logo b{color:#C9A76A}
.pv-invr{display:flex;gap:8px;align-items:center;justify-content:space-between}.pv-invr .pv-st{flex:none}
#pvAcct a{color:#8A6A2E;font-weight:700}
@media (min-width:700px){.pv-opts{grid-template-columns:repeat(3,1fr)}.pv-opt{grid-template-columns:1fr;text-align:center;justify-items:center;row-gap:4px;align-content:start;min-height:150px}.pv-opt span{grid-row:auto}}
.cl-sheet .pv-opts{grid-template-columns:1fr}.cl-sheet .pv-opt{grid-template-columns:44px 1fr;text-align:left;justify-items:start;min-height:72px}.cl-sheet .pv-opt span{grid-row:span 2}
.pv-prof{align-items:flex-start!important}.pv-prof-in{flex:1;min-width:0}.pv-prof-in>.pv-mut{margin:0 0 6px!important}
.pv-dl{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;margin:0;font-size:14px}.pv-dl dt{color:#5d5a55;font-weight:700}.pv-dl dd{margin:0;min-width:0;overflow-wrap:anywhere}
.pv-plans{list-style:none;margin:0;padding:0}.pv-plan{font-weight:800;margin:0 0 3px}.pv-plan.ok{color:#1d5e36}.pv-plan.warn{color:#6b4a06}
.card.pv-mission{border-left-color:#2e9a5c}.pv-mis-go{margin-top:10px;min-height:44px;width:100%}.pv-mis-ok{margin:6px 0 0;font-weight:800;color:#1d7a46}
.pv-verdict{margin:0 0 4px!important}.pv-verdict .pv-st{margin-left:0;font-size:14px;padding:4px 10px}
.pv-grid{stroke:#eee5d3;stroke-width:1}.pv-yl{font-size:10px;fill:#6b665e;text-anchor:end}
.pv-ln{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}.pv-ln.acc{stroke:#2a6fb0}.pv-ln.con{stroke:#b5832a;stroke-dasharray:5 4}
.pv-mk{stroke:#fff;stroke-width:2}.pv-mk.acc{fill:#2a6fb0}.pv-mk.con,.pv-mk.wr{fill:#b5832a}.pv-hit{fill:transparent}
.pv-leg{list-style:none;display:flex;flex-wrap:wrap;gap:6px 14px;margin:2px 0 4px;padding:0;font-size:12.5px;color:#5d5a55}.pv-leg li{display:flex;align-items:center;gap:6px}
.pv-sw{display:inline-block;width:16px;height:3px;border-radius:2px}.pv-sw.acc{background:#2a6fb0}.pv-sw.con{background:repeating-linear-gradient(90deg,#b5832a 0 5px,transparent 5px 8px)}
.pv-sw.sq{width:9px;height:9px;border-radius:2px}.pv-sw.con.sq{background:#b5832a}.pv-sw.wr,.pv-sw.cs{background:#b5832a}.pv-sw.cg{background:#2a6fb0}
.pv-tbl summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font-weight:700;font-size:13.5px;color:#8A6A2E}
.pv-tbl table{width:100%;border-collapse:collapse;font-size:13px}.pv-tbl th,.pv-tbl td{text-align:left;padding:5px 4px;border-top:1px solid #f0e8d8}.pv-tbl th{color:#5d5a55}
.pv-rd{display:flex;gap:14px;align-items:center;margin:6px 0 8px}.pv-rd-in{flex:1;min-width:0}.pv-rd-msg{margin:6px 0 0!important}
.pv-ring{--p:0;flex:none;width:96px;height:96px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(closest-side,#fff 76%,transparent 77% 100%),conic-gradient(#2e9a5c calc(var(--p)*1%),#efe6d3 0)}
.pv-ring b{font-size:28px;line-height:1;color:#15161C}.pv-ring small{font-size:11px;color:#5d5a55}
.pv-brk .pv-sbar{flex:0 0 28%}.pv-brk small{font-weight:600}
.pv-mleg{gap:6px 12px}.pv-mleg b{color:#15161C}
.pv-mg{border-top:1px solid #f0e8d8}.pv-mg summary{display:flex;align-items:center;gap:10px;min-height:44px;cursor:pointer;font-size:14.5px}.pv-mgn{flex:0 0 38%;font-weight:800;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pv-chips{list-style:none;margin:0 0 10px;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.pv-chip{display:inline-flex;align-items:center;gap:5px;max-width:100%;padding:5px 9px;border-radius:10px;font-size:12.5px;line-height:1.25;border:1px solid transparent}
.pv-chip small{font-weight:800;opacity:.85}.pv-ct{min-width:0;overflow-wrap:anywhere}.pv-ci{font-weight:800}
.pv-chip.m0{background:#fff;border-color:#d8ccb4;color:#5d5a55}.pv-chip.m1{background:#e3f1e7;color:#1d4d30}.pv-chip.m2{background:#8fcfa6;color:#0f3a22}.pv-chip.m3{background:#17603a;color:#fff}
.pv-chip.mini{padding:1px 6px;font-size:11px}
.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.pv-split{display:flex;height:12px;border-radius:8px;overflow:hidden;gap:2px;margin:4px 0 8px}.pv-split i{display:block;height:100%}.pv-split .cs{background:#b5832a}.pv-split .cg{background:#2a6fb0}
.pv-kpis.two{grid-template-columns:1fr 1fr}.pv-kpis small{font-size:11px}
.pv-tod li{display:flex;align-items:center;gap:8px}.pv-tod .pv-gt{flex:0 0 34%}.pv-tod .pv-sbar{flex:1}.pv-todv{flex:0 0 36%;text-align:right;font-weight:800;font-size:13px}.pv-todv small{font-weight:600;color:#5d5a55}
.pv-tod li.best{background:#e8f5ec;border-radius:10px;padding-left:8px!important;padding-right:8px!important}
.pv-badges{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(92px,1fr));gap:8px}
.pv-badges li{background:#FBF7EF;border:1px solid #f0e6d2;border-radius:12px;padding:8px 6px;text-align:center;display:flex;flex-direction:column;gap:2px}.pv-badges li span{font-size:24px}
.pv-badges b{font-size:12px;line-height:1.2}.pv-badges small{font-size:11px;color:#5d5a55}.pv-badges li.new{border-color:#C9A76A;background:#fff7e6}
.pv-pb li{display:flex;gap:8px;align-items:baseline}.pv-pb li>span:nth-child(2){flex:1}
#pvCheer{margin-top:12px;min-height:46px}
.pv-fnow{background:#FBF7EF;border:1px solid #f0e6d2;border-radius:12px;padding:10px 12px;margin:6px 0}.pv-fnow .pv-st{margin-left:0}
select.pv-in{appearance:auto;width:100%!important;max-width:none}
#pvPrint{display:none}
@media print{body>*:not(#pvPrint){display:none!important}html,body{background:#fff!important;overflow:visible!important}body{display:block!important}
#pvPrint{display:block!important;color:#000;font-family:Georgia,serif;padding:10mm}#pvPrint h1{font-size:22pt;margin:0 0 4pt;color:#5B0F1B}#pvPrint h2{font-size:15pt;margin:0 0 4pt}
#pvPrint pre{white-space:pre-wrap;font-family:inherit;font-size:12pt;line-height:1.55;border:1px solid #C9A76A;padding:8pt;border-radius:6pt}.pp-d,.pp-f{font-size:10pt;color:#444}.pp-chart svg{max-width:120mm}}`;
  function style() { if (D.getElementById('pvCss')) return; const s = D.createElement('style'); s.id = 'pvCss'; s.textContent = css; D.head.appendChild(s); }

  /* ================= start ================= */
  function start() {
    style();
    let t = 0;
    new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; paintMe(); paintGoal(); }); }).observe(D.body, { childList: true, subtree: true });
    setTimeout(() => { pullControls(); paintMe(); paintGoal(); enforce(); }, 1200);
    try {   // links in the weekly email open the hub: study.moneyviel.com/?hub=1
      const u = new URL(location.href);
      if (u.searchParams.get('hub')) { u.searchParams.delete('hub'); history.replaceState(history.state, '', u.pathname + u.search + u.hash); setTimeout(() => { if (canHub()) openHub(); }, 1500); }
    } catch (e) {}
    setInterval(() => { if (D.visibilityState === 'visible') pullControls(); }, 3 * 6e4);
    setInterval(enforce, 30000);
  }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', start) : start();

  window.Parent = { open: () => openHub(), home, link: linkSheet, myCode, minutesToday: () => minutesOn(S(), todayK()), _analyse: analyse, _pull: pullControls, _enforce: enforce,
    /* read-only toolkit for the teacher dashboard (js/teach.js): the same pure analysis and the same cards as Parent Hub.
       Pass a "k" shaped like a my_children row: { name, state: { st }, controls }. Nothing here changes Parent Hub. */
    lib: { analyse, deep, readinessOf, suggestions, mStat, MST, minutesOn, answersOn, caAnswersByDay, answerLog, mistakesOf, timeOf, trendOf,
      daysBack, dk, todayK, fmtMin, fmtDay, pctS, esc, mean, median, chapOf, curriculum, caStructure, subjName, chapName, BUCKETS,
      chartSVG, lineSVG, legend, weekBarsSVG, readinessHTML, trendHTML, masteryHTML, mistakeHTML, timeHTML, winsHTML, writesHTML, style } };
})();
