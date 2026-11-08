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
    const h = goalHTML(); let b = host.querySelector(':scope > .pv-goal');
    if (!h) { if (b) b.remove(); return; }
    if (!b) { style(); b = D.createElement('div'); b.className = 'card pv-goal'; b.setAttribute('role', 'status'); after ? after.after(b) : host.prepend(b); }
    if (b.dataset.h !== h) { b.dataset.h = h; b.innerHTML = h; }
  }
  function paintGoal() {
    const w = D.getElementById('s-world'); if (w && w.querySelector('#worldTitle')) placeGoal(w, w.querySelector('#worldTitle'));
    const me = D.getElementById('s-me'); if (me && me.firstElementChild) placeGoal(me, me.querySelector(':scope > .card:not(.pv-goal)'));
    const ca = D.getElementById('s-ca'); if (ca && (ca.querySelector('.ca-journey') || ca.querySelector('.ca-prof'))) placeGoal(ca, ca.querySelector(':scope > .card:not(.pv-goal)'));
    else if (ca) { const b = ca.querySelector(':scope > .pv-goal'); if (b) b.remove(); }
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
    const k = kids[sel], A = await analyse(k);
    if (kids[sel] !== k) return;
    body.innerHTML = childHTML(k, A) + invitesHTML() + mailCardHTML() + acctHTML();
    wireChild(body, k, A); wireMail(body); wireAcct(body);
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
      <label for="pvInE">Child's email</label><input class="cl-in" id="pvInE" type="email" maxlength="120" autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="child@gmail.com">
      <div class="cl-err" id="pvInErr" role="alert"></div><button class="btn" type="submit" id="pvInGo">Send invite</button></form><div style="height:8px"></div><button class="btn ghost" type="button" id="pvInX">Cancel</button>`);
    el.querySelector('#pvInX').onclick = C().closeSheet;
    el.querySelector('#pvInF').onsubmit = async ev => {
      ev.preventDefault(); const e = el.querySelector('#pvInErr'), go = el.querySelector('#pvInGo');
      const name = el.querySelector('#pvInN').value.trim(), email = el.querySelector('#pvInE').value.trim().toLowerCase();
      e.textContent = ''; if (!name) { e.textContent = "Please enter your child's name."; return; }
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

  function childHTML(k, A) {
    const c = k.controls || {}, s = A.s;
    const head = profileHTML(k, A);
    if (!A.has) {
      return head + `<div class="pv-card"><h3>No data yet</h3><p>${esc(A.name)}'s progress shows here after they study with the app while signed in. It updates about every 30 seconds while the app is open.</p></div>` + plannerHTML(A, c) + goalsHTML(A, c) + healthHTML(c) + manageHTML(A);
    }
    const alerts = A.alerts.length ? A.alerts.map(([t, m]) => `<li class="pv-al ${t}">${t === 'bad' ? '⚠️' : '🔔'} ${esc(m)}</li>`).join('') : '<li class="pv-al ok">✅ No alerts — all good this week.</li>';
    const sug = suggestions(A), dq = dinnerQs(A);
    const grp = g => `<li><span class="pv-gt"><b>${esc(g.title)}</b>${g.sub ? `<span class="pv-mut">${esc(g.sub)}</span>` : ''}</span><span class="pv-pill">${pctS(g.acc)} <small>· ${g.cnt} answers</small></span></li>`;
    return head + `
      <section class="pv-card" aria-labelledby="pvAl"><h3 id="pvAl">Alerts</h3><ul class="pv-list">${alerts}</ul></section>
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
      <section class="pv-card" aria-labelledby="pvSt"><h3 id="pvSt">Strengths and needs help</h3>
        ${A.totalAns < 4 ? '<p class="pv-empty">No answers yet — strengths show after a few quizzes.</p>' : `
        <h4>💪 Strong</h4>${A.best.length ? `<ul class="pv-list pv-gl1">${A.best.map(grp).join('')}</ul>` : '<p class="pv-mut">Not enough answers in one chapter yet.</p>'}
        <h4>📌 Needs help</h4>${A.weak.length ? `<ul class="pv-list pv-gl1">${A.weak.map(grp).join('')}</ul>` : '<p class="pv-mut">No weak chapter found — well done.</p>'}
        ${A.subjects && A.subjects.length ? `<h4>By subject</h4><ul class="pv-list pv-gl1">${A.subjects.map(x => `<li><b>${esc(x.name)}</b><span class="pv-sbar" aria-hidden="true"><i style="width:${Math.round(x.acc)}%"></i></span><span class="pv-pill">${pctS(x.acc)}</span></li>`).join('')}</ul>` : ''}
        <p class="pv-mut">Mistakes recorded: <b>${A.mistakes}</b>${A.topMist.length ? ` · most common: ${A.topMist.map(x => `“${esc(x[0])}” ×${x[1]}`).join(', ')}` : ''}</p>`}
        <h4>🚀 Scope to improve</h4><ol class="pv-ol">${sug.map(x => `<li>${x}</li>`).join('') || '<li>Keep going — no suggestions yet.</li>'}</ol></section>
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

  function wireChild(body, k, A) {
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

  window.Parent = { open: () => openHub(), home, link: linkSheet, myCode, minutesToday: () => minutesOn(S(), todayK()), _analyse: analyse, _pull: pullControls, _enforce: enforce };
})();
