/* ================= Knowtopia — Google Play readiness (js/playready.js) =================
   Loads AFTER js/cloud.js, js/parent.js, js/squad.js and js/live.js. Server: supabase/migrations/20261113_play_ready.sql
   and the Edge Function delete-account. Policy pages: legal/*.html, legal/delete-account.html.
   1. 🗑️ Delete my account — two steps (explain → type DELETE). Button in the account card (js/cloud.js, data-cl="del":
      school Me and CA Profile) and in Parent Hub → Your account (added here). Calls /functions/v1/delete-account, then
      clears this phone and reloads.
   2. 🛡️ Parent controls (Families) — Parent Hub child page gets a "Controls" card (PlayReady.hubCard, called by
      js/parent.js next to Squad.hubCard): 👫 Friends & cheers · 🎮 Live game rooms · 🔔 Friend news. Saved with
      rpc set_child_social; the SERVER enforces them (squad / room RPCs refuse). The child's app reads rpc my_social
      (cached in sv_social) and shows a kind "Your parent has turned this off" card instead of Game Rooms; js/squad.js
      uses the flags that squad_home returns.
   3. 🚩 Report / 🚫 Block — PlayReady.report({ id, name, avatar, context, room }) and PlayReady.block(...): preset reasons
      only (a short note only for confirmed adult CA students). Friend sheets (js/squad.js) and players in a Game Room
      lobby (added here, next to each other player).
   4. Consent records — sign-up sends { sv_consent: { v, g } } in the user metadata (PlayReady.signupMeta, used by
      js/cloud.js) and keeps a pending copy; after sign-in rpc accept_terms records it. rpc legal_status decides the
      one-time "We've updated our terms" gate. School students (Class 1–12, not CA) also tick "I am the parent or
      guardian, or my parent or guardian agrees", with an "Invite your parent" button (Parent.myCode). Checked at most
      once a day per account; any error = no gate (never locks anyone out).
   5. Play build (window.SV_PLAY, js/plans.js): a safety net that hides any link to the pricing page or a payment site. */
(function () {
  'use strict';
  const D = document, LS = localStorage;
  const LEGAL_V = '2.0';                    // last version that needs acceptance — KEEP IN SYNC with studyverse.legal_settings (legal 2.1 of 12 Nov 2026 was a minor update: no re-acceptance)
  const C = () => window.Cloud || null;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const say = m => { try { toast(m); } catch (e) {} };
  const tap = k => { try { sfx(k); } catch (e) {} };
  const one = r => Array.isArray(r) ? r[0] : r;
  const rpc = async (n, b) => one(await C().rest('rpc/' + n, { method: 'POST', body: b || {} }));
  const jget = (k, d) => { try { const v = JSON.parse(LS.getItem(k)); return v == null ? d : v; } catch (e) { return d; } };
  const jset = (k, v) => { try { v == null ? LS.removeItem(k) : LS.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const demo = () => { try { return !!LS.getItem('sv_demo'); } catch (e) { return false; } };
  const signedIn = () => !!(C() && C().signedIn() && !demo());
  const isParent = () => { try { return !!(C() && C().isParent && C().isParent()); } catch (e) { return false; } };
  const myId = () => { const u = C() && C().user(); return u ? u.id : null; };
  const S = () => { try { return ST; } catch (e) { return null; } };
  const isCA = () => { const s = S(); return !!(s && s.profile && s.profile.course === 'ca'); };
  const errT = e => (C() && C().errText ? C().errText(e) : (e && e.message) || 'Something went wrong.');
  const adult = () => { try { return isCA() && LS.getItem('sv_adult') === 'y'; } catch (e) { return false; } };

  function style() {
    if (D.getElementById('prCss')) return;
    const s = D.createElement('style'); s.id = 'prCss'; s.textContent = `
.pr-del{display:block;margin:12px auto 0;background:none;border:0;color:#B71C2C;font:700 14px Nunito,system-ui,sans-serif;text-decoration:underline;cursor:pointer;min-height:44px;padding:8px 6px}
.pr-del:focus-visible,.pr-rep:focus-visible,.pr-sw input:focus-visible+span{outline:3px solid #8A6A2E;outline-offset:2px}
.pr-list{margin:6px 0 12px;padding-left:20px;font-size:14px;line-height:1.5;color:#4a4d57}.pr-list li{margin:2px 0}
.pr-danger{background:#B71C2C!important;color:#fff!important}.pr-danger:disabled{opacity:.45}
.pr-type{font:800 20px ui-monospace,Menlo,Consolas,monospace!important;letter-spacing:4px;text-transform:uppercase}
.pr-sw{display:flex;align-items:center;gap:12px;min-height:56px;padding:8px 2px;border-bottom:1px solid #efe6d3;cursor:pointer}.pr-sw:last-of-type{border-bottom:0}
.pr-sw .pr-e{font-size:24px;flex:none;width:30px;text-align:center}.pr-sw .pr-t{flex:1;min-width:0;line-height:1.3}.pr-sw .pr-t b{display:block;font-size:15px}.pr-sw .pr-t small{color:#5d5a55;font-size:12.5px}
.pr-sw input{position:absolute;opacity:0;width:1px;height:1px}
.pr-sw input+span{flex:none;width:52px;height:30px;border-radius:30px;background:#c9c2b2;position:relative;transition:background .2s}
.pr-sw input+span::after{content:'';position:absolute;top:3px;left:3px;width:24px;height:24px;border-radius:50%;background:#fff;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.pr-sw input:checked+span{background:#1d7a46}.pr-sw input:checked+span::after{transform:translateX(22px)}
.pr-sw input:disabled+span{opacity:.5}
.pr-st{font-size:13px;min-height:18px;margin:6px 0 0;color:#1d5e36;font-weight:700}.pr-st.bad{color:#B71C2C}
.pr-reasons{display:grid;gap:8px;margin:10px 0}
.pr-reasons label{display:flex!important;align-items:center;gap:10px;min-height:52px;margin:0!important;padding:8px 12px;border:2px solid #e3e6f5;border-radius:14px;background:#fff;cursor:pointer;font:700 15px Nunito,system-ui,sans-serif!important;color:#1b1f3a}
.pr-reasons label span{font-size:22px}.pr-reasons input{width:20px;height:20px;flex:none;margin:0}
.pr-reasons label:has(input:checked){border-color:#6c3ff5;background:#f1edff}
.pr-rep{flex:none;min-width:44px;min-height:40px;border-radius:12px;border:2px solid #e3e6f5;background:#fff;color:#b42318;font-size:16px;cursor:pointer}
#prRepF .cl-show{min-height:44px;font-size:14px!important}#prRepF .cl-show input{width:20px;height:20px}
.pr-off{text-align:center}.pr-off .pr-big{font-size:44px;line-height:1.1}
#prGate{position:fixed;inset:0;z-index:975;display:flex;align-items:center;justify-content:center;padding:18px;background:rgba(10,12,24,.72);overflow:auto}
#prGate .pr-gin{width:100%;max-width:440px;background:#FFFDF8;color:#15161C;border-radius:20px;padding:20px 18px;box-shadow:0 20px 50px rgba(0,0,0,.4);max-height:94vh;overflow:auto}
#prGate h2{margin:0 0 4px;font-size:22px}#prGate p{margin:0 0 10px;font-size:14.5px;line-height:1.45;color:#4a4d57}
#prGate .pr-ver{font-size:12.5px;color:#6b6e78;margin:0 0 10px}
#prGate .pr-sum{background:#F4EAD8;border-radius:12px;padding:10px 12px;font-size:14px;color:#15161C}
#prGate .pr-links{display:flex;flex-wrap:wrap;gap:6px 14px;margin:6px 0 12px;font-size:14px}#prGate .pr-links a{color:#8A6A2E;font-weight:700}
#prGate .pr-chk{display:flex;gap:10px;align-items:flex-start;margin:10px 0;font-size:14.5px;line-height:1.4;cursor:pointer;color:#15161C}
#prGate .pr-chk input{width:22px;height:22px;flex:none;margin:1px 0 0}
#prGate .pr-err{color:#B71C2C;font-size:13.5px;min-height:18px;margin:4px 0 8px;font-weight:700}
#prGate .pr-small{font-size:12.5px;color:#6b6e78;text-align:center;margin:10px 0 0}#prGate .pr-small button{background:none;border:0;color:#8A6A2E;text-decoration:underline;font:inherit;cursor:pointer;padding:6px}
#prGate .btn{width:100%}`;
    D.head.appendChild(s);
  }

  /* ================= 1. delete my account ================= */
  function wipeAndReload() {
    const KEEP = ['sv_play', 'sv_ux', 'sv_legal'], keep = {};
    KEEP.forEach(k => { const v = LS.getItem(k); if (v != null) keep[k] = v; });
    const wipe = () => { try { LS.clear(); } catch (e) {} Object.keys(keep).forEach(k => { try { LS.setItem(k, keep[k]); } catch (e) {} }); };
    /* the app keeps saving its progress from memory (save() on changes, when hidden, before unload): from now on this
       page may only write the kept keys, so nothing of the deleted account comes back after the reload */
    try { const set0 = Storage.prototype.setItem; Storage.prototype.setItem = function (k, v) { if (this === LS && !KEEP.includes(k)) return; return set0.call(this, k, v); }; } catch (e) {}
    wipe();
    try { sessionStorage.clear(); } catch (e) {}
    try { indexedDB.deleteDatabase('sv_photos'); } catch (e) {}
    setTimeout(() => { wipe(); location.replace(location.pathname); }, 1800);
  }
  function deleteAccount() {
    if (!signedIn()) { C() && C().open('in'); return; }
    style();
    const par = isParent(), em = C().email();
    const el = C().sheet(`<h3 id="clT">Delete my account?</h3>
      <p>This closes the account <b>${esc(em)}</b> for good. It cannot be undone.</p>
      <ul class="pr-list"><li>Your progress, stars, streaks, friends, cheers and game results are deleted.</li>
        ${par ? '<li>Your children’s accounts are <b>not</b> deleted — they are only unlinked from you.</li>' : '<li>Links with your parent are removed.</li>'}
        <li>Payment records are kept only as the tax law requires, without your name or email.</li>
        <li>Anything saved on this phone is cleared too.</li></ul>
      <p class="cl-small">Only want a break? You can just sign out instead.</p>
      <button class="btn pr-danger" type="button" id="prDel1">Continue</button><div style="height:8px"></div>
      <button class="btn ghost" type="button" id="prDelX">Cancel</button>`);
    el.querySelector('#prDelX').onclick = () => C().closeSheet();
    el.querySelector('#prDel1').onclick = () => step2(el);
  }
  function step2(el) {
    const box = el.querySelector('.sheet-in');
    box.innerHTML = `<div class="sheet-grab"></div><h3 id="clT">Type DELETE to confirm</h3>
      <p>To make sure this is really you, type the word <b>DELETE</b> in the box below.</p>
      <form id="prDelF" novalidate><label for="prDelIn">Type DELETE</label><input class="cl-in pr-type" id="prDelIn" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="10" aria-describedby="prDelE">
      <div class="cl-err" id="prDelE" role="alert"></div>
      <button class="btn pr-danger" type="submit" id="prDelGo" disabled>Delete my account forever</button></form><div style="height:8px"></div>
      <button class="btn ghost" type="button" id="prDelX2">Cancel</button>`;
    const inp = box.querySelector('#prDelIn'), go = box.querySelector('#prDelGo'), er = box.querySelector('#prDelE');
    inp.oninput = () => { go.disabled = inp.value.trim().toUpperCase() !== 'DELETE'; er.textContent = ''; };
    box.querySelector('#prDelX2').onclick = () => C().closeSheet();
    inp.focus();
    box.querySelector('#prDelF').onsubmit = async ev => {
      ev.preventDefault();
      if (inp.value.trim().toUpperCase() !== 'DELETE') { er.textContent = 'Please type DELETE.'; return; }
      go.disabled = true; go.textContent = 'Deleting…';
      try {
        const r = await C().call('/functions/v1/delete-account', { method: 'POST', body: { confirm: 'DELETE' } });
        if (!r || !r.ok) throw new Error((r && r.error) || 'Could not delete your account.');
        box.innerHTML = `<div class="sheet-grab"></div><h3 id="clT">Your account is deleted</h3><p role="status">Thank you for learning with Knowtopia. This phone is being cleared now.</p>`;
        wipeAndReload();
      } catch (e) {
        er.textContent = (e && e.status != null ? errT(e) : (e && e.message)) + ' If it keeps failing, write to support@knowtopia.in from this email.';
        go.disabled = false; go.textContent = 'Delete my account forever';
      }
    };
  }
  /* parent accounts: Parent Hub → Your account (js/parent.js #pvAcct) */
  function parentDelete() {
    const a = D.getElementById('pvAcct'); if (!a || a.querySelector('.pr-del')) return;
    style();
    const b = D.createElement('button'); b.type = 'button'; b.className = 'pr-del'; b.id = 'prDelP'; b.textContent = 'Delete my account';
    b.onclick = deleteAccount; const out = a.querySelector('#pvOut'); out ? out.after(b) : a.appendChild(b);
  }

  /* ================= 2. parent controls ================= */
  const SW = [['friends', '👫', 'Friends & cheers', 'Add friends with a code, the friends league and cheers.'],
              ['rooms', '🎮', 'Live game rooms', 'Play live quiz races and puzzles with friends.'],
              ['news', '🔔', 'Friend news', 'Small updates like “Riya beat your puzzle time”.']];
  async function hubCard(body, k, A) {
    if (!body || !k || !k.child_id || !signedIn()) return;
    style();
    let box = body.querySelector('#prCtl'); if (box) box.remove();
    box = D.createElement('section'); box.className = 'pv-card'; box.id = 'prCtl'; box.setAttribute('aria-labelledby', 'prCtlT');
    const mg = body.querySelector('.pv-manage'); mg ? body.insertBefore(box, mg) : body.appendChild(box);
    const name = (A && A.name) || k.name || 'your child';
    box.innerHTML = `<h3 id="prCtlT">🛡️ Controls</h3><p class="pv-mut">Loading…</p>`;
    let st = null, msg = '';
    try { const r = await rpc('child_social', { p_child: k.child_id }); if (r && r.ok) st = r; else msg = (r && r.msg) || ''; } catch (e) { msg = errT(e); }
    if (!box.isConnected) return;
    if (!st) { box.innerHTML = `<h3 id="prCtlT">🛡️ Controls</h3><p class="pv-mut">${esc(msg || 'Could not load the controls.')}</p><button class="pv-btn ghost" type="button" id="prCtlR">Try again</button>`;
      box.querySelector('#prCtlR').onclick = () => hubCard(body, k, A); return; }
    box.innerHTML = `<h3 id="prCtlT">🛡️ Controls</h3><p class="pv-mut">Choose what ${esc(name)} can use. Our server checks these switches, so they work on every phone. Learning, games on their own and your challenges always stay on.</p>
      ${SW.map(([key, e, t, d]) => `<label class="pr-sw" for="prSw-${key}"><span class="pr-e" aria-hidden="true">${e}</span><span class="pr-t"><b>${t}</b><small>${d}</small></span>
        <input type="checkbox" role="switch" id="prSw-${key}" data-k="${key}" ${st[key] !== false ? 'checked' : ''} aria-describedby="prCtlS"><span aria-hidden="true"></span></label>`).join('')}
      <p class="pr-st" id="prCtlS" role="status" aria-live="polite"></p>`;
    box.querySelectorAll('input[data-k]').forEach(i => i.onchange = async () => {
      const key = i.dataset.k, on = i.checked, s = box.querySelector('#prCtlS'); i.disabled = true; s.className = 'pr-st'; s.textContent = 'Saving…';
      try {
        const r = await rpc('set_child_social', { p_child: k.child_id, ['p_' + key]: on });
        if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not save.');
        const t = SW.find(x => x[0] === key)[2];
        s.textContent = `${t}: ${on ? 'on' : 'off'} ✓`; tap('tap');
      } catch (e) { i.checked = !on; s.className = 'pr-st bad'; s.textContent = errT(e); }
      finally { i.disabled = false; }
    });
  }

  /* child side: what the parent allows (cached; the server enforces it anyway) */
  const SK = 'sv_social';
  function social() { const c = jget(SK, null); return c && c.uid === myId() ? c : { friends: true, rooms: true, news: true }; }
  let pulling = null;
  function pullSocial() {
    if (!signedIn() || isParent()) return Promise.resolve(null);
    if (pulling) return pulling;
    pulling = (async () => { try { const r = await rpc('my_social'); if (r && r.ok) jset(SK, { uid: myId(), friends: r.friends !== false, rooms: r.rooms !== false, news: r.news !== false, at: Date.now() }); return r; }
      catch (e) { return null; } finally { pulling = null; } })();
    return pulling;
  }
  const offCard = (e, t, m) => `<div class="card pr-off" data-pr-off="1"><div class="pr-big" aria-hidden="true">${e}</div><h2 class="lv-h1" style="font-size:22px">${t}</h2><p class="sub">${m}</p></div>`;
  function liveOff() {
    const m = D.getElementById('lvMain'); if (!m || m.querySelector('[data-pr-off]')) return;
    if (social().rooms !== false) return;
    m.innerHTML = offCard('🔒', 'Game Rooms are turned off', 'Your parent has turned off live game rooms for now. You can still play the Arcade games and puzzles on your own, any time.');
  }

  /* ================= 3. report + block ================= */
  const REASONS = [['unkind', '😠', 'Unkind or rude behaviour'], ['cheating', '🎲', 'Cheating'], ['name', '🙈', 'Rude name or picture'], ['other', '❓', 'Something else']];
  function report(o) {
    if (!o || !o.id || !C()) return;
    style();
    const nm = o.name || 'this player', canBlock = o.context !== 'room';
    const el = C().sheet(`<h3 id="clT">🚩 Report ${esc(nm)}</h3>
      <p>What happened? We look at every report. ${esc(nm)} is not told who reported.</p>
      <form id="prRepF" novalidate><fieldset style="border:0;margin:0;padding:0"><legend class="cl-small" style="padding:0">Pick one reason</legend>
      <div class="pr-reasons" role="radiogroup">${REASONS.map(([k, e, t]) => `<label><input type="radio" name="prR" value="${k}"><span aria-hidden="true">${e}</span>${t}</label>`).join('')}</div></fieldset>
      ${adult() ? '<label for="prRepD">Anything else? (optional)</label><textarea class="cl-in" id="prRepD" rows="3" maxlength="300"></textarea>' : ''}
      ${canBlock ? `<label class="cl-show"><input type="checkbox" id="prRepB"> Also block ${esc(nm)}</label>` : ''}
      <div class="cl-err" id="prRepE" role="alert"></div>
      <button class="btn" type="submit" id="prRepGo">Send report</button></form>
      <p class="cl-small" style="margin-top:10px">Feel unsafe or upset? Tell a parent or teacher too. Our email: support@knowtopia.in</p>
      <button class="btn ghost" type="button" id="prRepX">Cancel</button>`);
    el.querySelector('#prRepX').onclick = () => C().closeSheet();
    el.querySelector('#prRepF').onsubmit = async ev => {
      ev.preventDefault();
      const rc = el.querySelector('input[name=prR]:checked'), er = el.querySelector('#prRepE'), go = el.querySelector('#prRepGo');
      if (!rc) { er.textContent = 'Please pick a reason.'; return; }
      go.disabled = true; er.textContent = '';
      try {
        const d = el.querySelector('#prRepD'), bl = el.querySelector('#prRepB');
        const r = await rpc('report_user', { p_user: o.id, p_reason: rc.value, p_context: o.context || 'friend', p_room: o.room || null, p_detail: d ? d.value.trim() || null : null });
        if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not send the report.');
        let blocked = false;
        if (bl && bl.checked) { const b = await rpc('squad_block', { p_user: o.id }); blocked = !!(b && b.ok); }
        C().closeSheet(); say(blocked ? `Thank you. ${nm} is blocked.` : (r.msg || 'Thank you. We will look at it.')); tap('tap');
        if (o.after) o.after({ reported: true, blocked });
      } catch (e) { er.textContent = errT(e); go.disabled = false; }
    };
  }
  function block(o) {
    if (!o || !o.id || !C()) return;
    style();
    const nm = o.name || 'this friend';
    const el = C().sheet(`<h3 id="clT">🚫 Block ${esc(nm)}?</h3><p>${esc(nm)} will be removed from your friends and can't send you friend requests or cheers. ${esc(nm)} is not told.</p>
      <div class="cl-err" id="prBlE" role="alert"></div>
      <button class="btn pr-danger" type="button" id="prBlGo">Block ${esc(nm)}</button><div style="height:8px"></div><button class="btn ghost" type="button" id="prBlX">Cancel</button>`);
    el.querySelector('#prBlX').onclick = () => C().closeSheet();
    el.querySelector('#prBlGo').onclick = async () => {
      const b = el.querySelector('#prBlGo'), er = el.querySelector('#prBlE'); b.disabled = true;
      try { const r = await rpc('squad_block', { p_user: o.id }); if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not block.');
        C().closeSheet(); say(`${nm} is blocked`); tap('tap'); if (o.after) o.after({ blocked: true }); }
      catch (e) { er.textContent = errT(e); b.disabled = false; }
    };
  }
  /* Game Room lobby: a 🚩 next to every other player (js/live.js draws li.lv-p with a [data-on="<user id>"] dot) */
  function lobbyFlags() {
    const sc = D.getElementById('s-live'); if (!sc || !sc.querySelector('.lv-lobby')) return;
    const L = window.Live && Live._L, me = myId(); if (!L || !L.st || !L.code) return;
    sc.querySelectorAll('.lv-lobby li.lv-p').forEach(li => {
      if (li.querySelector('.pr-rep')) return;
      const dot = li.querySelector('[data-on]'), id = dot && dot.dataset.on; if (!id || id === me) return;
      const p = (L.st.players || []).find(x => x.user_id === id); if (!p) return;
      style();
      const b = D.createElement('button'); b.type = 'button'; b.className = 'pr-rep'; b.textContent = '🚩'; b.setAttribute('aria-label', 'Report ' + p.name); b.title = 'Report';
      b.onclick = () => report({ id, name: p.name, avatar: p.avatar, context: 'room', room: L.code });
      const k = li.querySelector('.lv-kick'); k ? k.before(b) : li.appendChild(b);
    });
  }

  /* ================= 4. consent: sign-up metadata + one-time gate ================= */
  const PK = 'sv_consent_pend', OK = 'sv_legal_ok';
  function signupMeta(role) {
    const g = role === 'student', email = (D.getElementById('clE') && D.getElementById('clE').value || '').trim().toLowerCase();
    jset(PK, { email, v: LEGAL_V, g, at: Date.now() });
    return { sv_consent: { v: LEGAL_V, g } };
  }
  let checking = false, checkedFor = null, lastTry = 0;
  const schoolKid = () => { const s = S(); return !isParent() && !!(s && s.profile && s.profile.course !== 'ca' && +s.profile.grade >= 1); };
  async function checkLegal(force) {
    if (!signedIn() || checking) return;
    const uid = myId(); if (!uid) return;
    const c = jget(OK, null);
    if (!force && c && c.uid === uid && Date.now() - c.at < 864e5) { checkedFor = uid; return; }
    checking = true; lastTry = Date.now();
    try {
      const p = jget(PK, null);
      if (p && p.email && p.email === (C().email() || '').toLowerCase()) {
        try { const a = await rpc('accept_terms', { p_version: p.v, p_guardian: !!p.g, p_how: 'signup', p_agent: navigator.userAgent.slice(0, 200) }); if (a && a.ok) jset(PK, null); } catch (e) {}
      }
      const r = await rpc('legal_status');
      if (!r || !r.ok) return;                       // never lock anyone out on an error
      checkedFor = uid;
      const needG = schoolKid() && !r.parental;
      if (r.accepted && !needG) { jset(OK, { uid, v: r.version, at: Date.now() }); hideGate(); return; }
      gate(r, needG);
    } catch (e) { /* offline / older server: no gate */ } finally { checking = false; }
  }
  function hideGate() { const g = D.getElementById('prGate'); if (g) g.remove(); }
  function gate(r, needG) {
    style();
    let g = D.getElementById('prGate');
    if (g && g.dataset.v === String(r.version) && g.dataset.g === String(!!needG)) return;   // already showing: keep the ticks
    if (g) g.remove();
    g = D.createElement('div'); g.id = 'prGate'; g.dataset.v = String(r.version); g.dataset.g = String(!!needG); g.setAttribute('role', 'dialog'); g.setAttribute('aria-modal', 'true'); g.setAttribute('aria-labelledby', 'prGateT');
    const d = r.effective_on ? new Date(r.effective_on + 'T12:00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' }) : '';
    const kid = schoolKid();
    g.innerHTML = `<div class="pr-gin"><h2 id="prGateT" tabindex="-1">${r.accepted ? 'One quick check' : 'We’ve updated our terms'}</h2>
      <p class="pr-ver">Version ${esc(r.version || LEGAL_V)}${d ? ' · from ' + esc(d) : ''}</p>
      ${!r.accepted && r.summary ? `<div class="pr-sum"><b>What changed:</b> ${esc(r.summary)}</div>` : ''}
      <p style="margin-top:10px">${kid ? 'Please read these with your parent or guardian.' : 'Please read them and tick to continue.'}</p>
      <div class="pr-links"><a href="legal/terms.html">Terms</a><a href="legal/privacy.html">Privacy Policy</a>${kid ? '<a href="legal/children.html">Privacy for kids</a>' : ''}<a href="legal/parents.html">For parents</a></div>
      ${r.accepted ? '' : '<label class="pr-chk"><input type="checkbox" id="prGa"> <span>I accept the Terms and the Privacy Policy.</span></label>'}
      ${needG ? `<label class="pr-chk"><input type="checkbox" id="prGg"> <span>I am the parent or guardian, or my parent or guardian agrees.</span></label>
        <button class="btn ghost" type="button" id="prGinv">👨‍👩‍👧 Invite your parent</button>` : ''}
      <div class="pr-err" id="prGe" role="alert"></div>
      <button class="btn" type="button" id="prGgo">Accept &amp; continue</button>
      <p class="pr-small">Questions? <a href="mailto:support@knowtopia.in">support@knowtopia.in</a> · <button type="button" id="prGout">Sign out</button></p></div>`;
    D.body.appendChild(g);
    g.querySelectorAll('.pr-links a').forEach(a => a.addEventListener('click', () => { try { sessionStorage.setItem('sv_legal_ret', 'me'); } catch (e) {} }));
    const inv = g.querySelector('#prGinv'); if (inv) inv.onclick = () => { try { if (window.Parent && Parent.myCode) Parent.myCode(); } catch (e) {} };
    g.querySelector('#prGout').onclick = function () { if (!this.dataset.sure) { this.dataset.sure = 1; this.textContent = 'Tap again to sign out'; return; } C().signOut(); };
    g.querySelector('#prGgo').onclick = async () => {
      const a = g.querySelector('#prGa'), gg = g.querySelector('#prGg'), er = g.querySelector('#prGe'), go = g.querySelector('#prGgo');
      if (a && !a.checked) { er.textContent = 'Please tick the box to accept the Terms and Privacy Policy.'; a.focus(); return; }
      if (gg && !gg.checked) { er.textContent = 'Please tick the box: your parent or guardian needs to agree.'; gg.focus(); return; }
      go.disabled = true; er.textContent = '';
      try {
        const x = await rpc('accept_terms', { p_version: r.version || LEGAL_V, p_guardian: !!(gg && gg.checked), p_how: 'gate', p_agent: navigator.userAgent.slice(0, 200) });
        if (!x || !x.ok) { if (x && x.code === 'version') { checkLegal(true); return; } throw new Error((x && x.msg) || 'Could not save. Please try again.'); }
        jset(OK, { uid: myId(), v: x.version, at: Date.now() }); hideGate(); say('Thank you ✓'); tap('tap');
      } catch (e) { er.textContent = errT(e); go.disabled = false; }
    };
    setTimeout(() => { const h = g.querySelector('#prGateT'); if (h) h.focus(); }, 50);
  }

  /* ================= 5. Play build safety net ================= */
  function playCss() {
    if (!window.SV_PLAY || D.getElementById('prPlayCss')) return;
    const s = D.createElement('style'); s.id = 'prPlayCss';
    s.textContent = 'a[href*="pricing"],a[href*="razorpay"],#lvPlans,#pwPlans,[data-pl],[data-cl="plans"]{display:none!important}';
    (D.head || D.documentElement).appendChild(s);
  }

  /* ================= start ================= */
  function tick() {
    if (!signedIn()) return;
    if (isParent()) parentDelete();
    if (D.getElementById('lvMain')) liveOff();
    lobbyFlags();
    if (checkedFor !== myId() && !checking && Date.now() - lastTry > 60000) checkLegal();
  }
  function start() {
    style(); playCss();
    let t = 0;
    new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; tick(); }); }).observe(D.body, { childList: true, subtree: true });
    setTimeout(() => { pullSocial().then(() => { if (D.getElementById('lvMain')) liveOff(); }); if (checkedFor !== myId()) checkLegal(); }, 2500);
    setInterval(() => { if (D.visibilityState === 'visible') pullSocial(); }, 5 * 6e4);
  }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', start) : start();

  window.PlayReady = { deleteAccount, hubCard, report, block, social, pullSocial, signupMeta, checkLegal, LEGAL_V };
})();
