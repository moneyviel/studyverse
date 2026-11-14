/* ================= Knowtopia 🦁 Squad (school) / 👥 Group (CA) — js/squad.js =================
   Replaces the old sample league: squadScreen() is reassigned here (loads after js/ca.js, js/practice.js and js/parent.js),
   and serves both school students (#s-squad) and CA students (#s-ca with the 👥 Group tab).
   Screen, top to bottom (each part is ONE .card):
     1. 💌 Cheers received (only when there are new ones; shown once)
     2. League: 🏫 class vs class (students enrolled by a school / coaching: classes of their institution ranked by average
        weekly ⭐ per active student — fair for any class size) or 👫 Friends league (everyone else). Resets every Monday.
     3. 🔔 Friend news (at most 3): "Riya beat your Sudoku 4×4 time!", "Kabir is 20 ⭐ ahead this week", streaks… each with 👋 Cheer.
     4. 👫 Friends: weekly leaderboard (first name, avatar, weekly ⭐, 🔥), requests to accept, my friend code, add by code.
        Tap a friend → cheer (preset messages only — no free text, for children's safety) or remove.
     5. 👨‍👩‍👧 Parent challenge (only when one is waiting or just finished; a WAITING one moves up to just below Cheers):
        a linked parent starts a 5-question duel in Parent Hub (card added there by Squad.hubCard, called from js/parent.js);
        the child plays here. Scores are computed by the server from the picked options (see play()).
   Weekly stars: rpc squad_sync gets this week's stars per day from ST.xpLog (+ streak, first name, avatar, puzzle best
   times ST.pz.best), at most once a minute and only when something changed. The server caps a day at 1500 stars.
   Server: supabase/migrations/20261110_squad.sql (squad_sync, squad_home, squad_add_friend, squad_answer, squad_remove,
   squad_cancel_requests, squad_new_code, squad_cheer, pc_create, pc_start, pc_submit, pc_list). Friends only see each other after
   a request is accepted; only first name + avatar are ever shared, never an email. */
(function () {
  'use strict';
  const D = document, LS = localStorage;
  const C = () => window.Cloud || null;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const say = m => { try { toast(m); } catch (e) {} };
  const tap = k => { try { sfx(k); } catch (e) {} };
  const one = r => Array.isArray(r) ? r[0] : r;
  const rpc = (n, b) => C().rest('rpc/' + n, { method: 'POST', body: b || {} });
  const jget = (k, d) => { try { const v = JSON.parse(LS.getItem(k)); return v == null ? d : v; } catch (e) { return d; } };
  const jset = (k, v) => { try { v == null ? LS.removeItem(k) : LS.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const demo = () => { try { return !!LS.getItem('sv_demo'); } catch (e) { return false; } };
  const signedIn = () => !!(C() && C().signedIn() && !demo());
  const parentAcct = () => { try { return !!(C() && C().isParent && C().isParent()); } catch (e) { return false; } };
  const myId = () => { const u = C() && C().user(); return u ? u.id : null; };
  const S = () => { try { return ST; } catch (e) { return null; } };
  const isCA = () => { const s = S(); return !!(s && s.profile && s.profile.course === 'ca'); };
  const errT = e => (C() && C().errText ? C().errText(e) : (e && e.message) || 'Something went wrong.');
  const kf = n => { try { return kfmt(n); } catch (e) { return String(Math.round(n || 0)); } };
  const secs = ms => { const s = Math.round((ms || 0) / 1000); return s < 60 ? `${s} s` : `${Math.floor(s / 60)} min ${s % 60} s`; };
  const fmtT = s => { s = Math.round(s || 0); return s < 60 ? `${s} s` : `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; };
  const CK = 'sv_squad';
  const CHEERS = [['clap', '👏', 'Well done!'], ['fire', '🔥', 'Keep your streak going!'], ['star', '⭐', 'You are a star!'],
                  ['strong', '💪', 'You can do it!'], ['wave', '👋', 'Hi! Let’s study today!'], ['rocket', '🚀', 'Great progress!']];
  const cheerOf = k => CHEERS.find(c => c[0] === k) || CHEERS[2];
  const PZ = { xw: 'Crossword', sdk4: 'Sudoku 4×4', sdk6: 'Sudoku 6×6', sdk9: 'Sudoku 9×9', csdk4: 'Concept Sudoku 4×4', csdk6: 'Concept Sudoku 6×6', kak: 'Kakuro', ws: 'Word search', an: 'Anagram' };
  const pzName = k => { const m = /^([a-z]+?)(\d*)(?:-([a-z]+))?$/.exec(k) || []; const n = PZ[(m[1] || '') + (m[2] || '')] || PZ[m[1]] || 'puzzle'; return m[3] ? `${n} (${m[3]})` : n; };

  /* ================= weekly stars → server (debounced) ================= */
  const utcDay = t => new Date(t).toISOString().slice(0, 10);          // the same day key as app.js today()
  function payload() {
    const s = S(), L = s.xpLog && typeof s.xpLog === 'object' ? s.xpLog : {}, days = {};
    for (let i = 0; i < 15; i++) { const k = utcDay(Date.now() - i * 864e5); if (+L[k] > 0) days[k] = Math.round(+L[k]); }
    const b = s.pz && s.pz.best && typeof s.pz.best === 'object' ? s.pz.best : {}, pz = {};
    Object.keys(b).sort().slice(0, 40).forEach(k => { const v = +b[k]; if (v >= 3 && v <= 86400 && /^[a-z0-9-]{1,24}$/.test(k)) pz[k] = Math.round(v); });
    let n = 0; try { n = liveStreak(); } catch (e) {}
    const p = s.profile || {};
    return { p_days: days, p_streak: n, p_streak_day: (s.streak && s.streak.last) || null, p_name: String(p.name || '').trim().split(/\s+/)[0] || 'Friend',
      p_avatar: p.avatar || '🙂', p_pz: pz, p_course: isCA() ? 'ca' : 'school' };
  }
  let sent = '', sentAt = 0, syncing = null;
  function sync(force) {
    const s = S(); if (!signedIn() || parentAcct() || !s || !s.profile) return Promise.resolve(null);
    if (syncing) return syncing;
    const b = payload(), h = JSON.stringify(b) + (myId() || '');
    if (!force && h === sent && Date.now() - sentAt < 6 * 36e5) return Promise.resolve(null);
    syncing = (async () => { try { const r = one(await rpc('squad_sync', b)); if (r && r.ok) { sent = h; sentAt = Date.now(); } return r; } catch (e) { return null; } finally { syncing = null; } })();
    return syncing;
  }
  setInterval(() => sync(false), 60000);
  D.addEventListener('visibilitychange', () => { if (D.visibilityState === 'hidden') sync(false); });
  setTimeout(() => sync(false), 8000);

  /* ================= data ================= */
  let H = null, cheersNow = [], loadErr = '';
  async function load() {
    loadErr = '';
    await Promise.race([sync(false), new Promise(r => setTimeout(r, 2500))]);
    try {
      const r = one(await rpc('squad_home'));
      if (r && r.ok) { H = r; H._at = Date.now(); cheersNow = (r.cheers || []).concat(cheersNow).slice(0, 10); jset(CK, { uid: myId(), d: Object.assign({}, r, { cheers: [] }), at: Date.now() }); }
      else if (r && r.parent) { H = null; loadErr = 'parent'; }
      else loadErr = (r && r.msg) || 'Could not load your squad.';
    } catch (e) {
      loadErr = errT(e);
      const c = jget(CK, null);
      if (H) H._old = H._at || Date.now(); else if (c && c.uid === myId()) { H = c.d; H._old = c.at; }
    }
  }

  /* ================= styles (once) ================= */
  function style() {
    if (D.getElementById('sqCss')) return;
    const s = D.createElement('style'); s.id = 'sqCss'; s.textContent = `
.sq-vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.sq-card h3,.sq-card .ca-h2s{margin:0 0 4px}.sq-card p.sub{margin:0 0 10px}
.sq-card .row{min-height:44px}.sq-card .row .nm small{font-weight:600}
.sq-list{list-style:none;margin:0;padding:0}
.sq-row{display:flex;align-items:center;gap:10px;padding:9px 4px;border-bottom:1px solid #eef0fb;min-height:44px}.sq-row:last-child{border-bottom:0}
.sq-row .sq-t{flex:1;min-width:0;font-weight:700;line-height:1.3}.sq-row .sq-t small{display:block;color:var(--muted);font-weight:600;font-size:12.5px}
.sq-av{width:38px;height:38px;border-radius:50%;display:grid;place-items:center;font-size:20px;flex:none;background:#f1efff}
.sq-btn{flex:none;min-height:40px;min-width:44px;padding:0 12px;border-radius:12px;border:0;background:#eef0fb;color:var(--ink);font:700 14px Nunito,system-ui,sans-serif;cursor:pointer}
.sq-btn.pri{background:var(--violet);color:#fff}
span.sq-btn{display:grid;place-items:center;font-size:18px}
.sq-frow{width:100%;border:0;background:transparent;text-align:left;font:inherit;color:inherit;cursor:pointer;border-radius:12px}
.sq-frow:focus-visible,.sq-btn:focus-visible{outline:3px solid var(--violet);outline-offset:2px}
.sq-wk{font-family:'Baloo 2',system-ui;font-weight:800;white-space:nowrap}.sq-st{font-size:13px;color:var(--muted);font-weight:700;white-space:nowrap;min-width:38px;text-align:right}
.sq-me{background:#fff8e1;border-radius:12px}
.sq-bar{height:8px;border-radius:8px;background:#eef0fb;overflow:hidden;margin-top:4px}.sq-bar i{display:block;height:100%;border-radius:8px;background:linear-gradient(90deg,#8b5cf6,#3b82f6)}
.sq-foot{font-size:12.5px;color:var(--muted);margin:8px 0 0;text-align:center}
.sq-code{display:flex;align-items:center;gap:10px;margin:12px 0 8px;padding:10px 12px;border-radius:14px;background:#f6f4ff;border:2px dashed #c9bdf8}
.sq-code b{font:800 24px ui-monospace,Menlo,Consolas,monospace;letter-spacing:5px;flex:1}
.sq-add{display:flex;gap:8px;margin-top:6px}.sq-add input{flex:1;min-width:0;min-height:46px;border-radius:12px;border:2px solid #d8dcf0;padding:8px 12px;font:800 18px ui-monospace,Menlo,Consolas,monospace;letter-spacing:4px;text-transform:uppercase;background:#fff;color:#1b1f3a}
.sq-add .btn{width:auto;flex:none;padding:10px 18px}
.sq-err{color:#c0392b;font-size:13.5px;font-weight:700;min-height:18px;margin:6px 0 0}
.sq-req{background:#fff8e1;border-radius:12px;padding:6px 8px;margin:8px 0}
.sq-sub2{font:800 12px Nunito,system-ui;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin:12px 0 2px}
.sq-link{border:0;background:none;color:var(--violet);font-weight:800;cursor:pointer;padding:8px 4px;min-height:40px;font-size:13.5px}
.sq-cgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}
.sq-cgrid button{min-height:56px;border-radius:14px;border:2px solid #e3e6f5;background:#fff;color:#1b1f3a;font:700 14px Nunito,system-ui;cursor:pointer;display:flex;align-items:center;gap:8px;padding:8px 10px;text-align:left}
.sq-cgrid button span{font-size:24px}.sq-cgrid button:disabled{opacity:.5}
.sq-q{font-size:17px;font-weight:800;line-height:1.4;margin:6px 0 10px;color:#1b1f3a}
.sq-qh{display:flex;justify-content:space-between;font-size:13px;color:#5d6280;font-weight:700}
.sq-dots{letter-spacing:3px}
.sq-opts{display:grid;gap:8px}
.sq-opt{min-height:50px;border-radius:14px;border:2px solid #e3e6f5;background:#fff;color:#1b1f3a;font:700 15.5px Nunito,system-ui;text-align:left;padding:10px 14px;cursor:pointer}
.sq-opt.sel{border-color:var(--violet,#6c3ff5);background:#f1edff;box-shadow:inset 0 0 0 1px var(--violet,#6c3ff5)}
.sq-rvw{margin:4px 0 12px}.sq-rvw summary{cursor:pointer;font-weight:800;min-height:40px;display:flex;align-items:center;color:#1b1f3a}
.sq-rv{display:flex;flex-direction:column;gap:2px;padding:8px 2px;border-bottom:1px solid #eef0fb;font-size:14px;color:#1b1f3a}.sq-rv span{font-weight:700}.sq-rv small{color:#5d6280}
.sq-fb{min-height:22px;margin:10px 0;font-size:14.5px;line-height:1.4;color:#1b1f3a}
.sq-vs{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;text-align:center;margin:12px 0}
.sq-vs div{background:#f6f4ff;border-radius:14px;padding:10px 6px}.sq-vs b{display:block;font-size:22px;font-family:'Baloo 2',system-ui}.sq-vs span{font-size:12.5px;color:#5d6280;font-weight:700}
.sq-vs .x{background:none;font-weight:800;color:#5d6280}
.sq-big{font-size:46px;text-align:center;line-height:1.1}
.sq-res{font-weight:800}.sq-res.win{color:#1d7a46}
html[data-age=pro] #s-ca .sq-row{border-bottom-color:rgba(127,127,127,.18)}
html[data-age=pro] #s-ca .sq-me{background:rgba(201,167,106,.16)}
html[data-age=pro] #s-ca .sq-code{background:transparent;border-color:#C9A76A}
html[data-age=pro] #s-ca .sq-btn{background:rgba(127,127,127,.14);color:inherit}html[data-age=pro] #s-ca .sq-btn.pri{background:#C9A76A;color:#15161C}
html[data-age=pro] #s-ca .sq-req{background:rgba(201,167,106,.14)}html[data-age=pro] #s-ca .sq-av{background:rgba(201,167,106,.18)}
html[data-age=pro] #s-ca .sq-link{color:#C9A76A}html[data-age=pro] #s-ca .sq-bar{background:rgba(127,127,127,.18)}html[data-age=pro] #s-ca .sq-bar i{background:#C9A76A}
.pv-card .sq-pcl li{display:flex;align-items:center;gap:8px;justify-content:space-between}.pv-card .sq-pcl .pv-btn{width:auto;min-height:40px;padding:6px 14px;flex:none}
`;
    D.head.appendChild(s);
  }

  /* ================= the screen ================= */
  let EL = null;
  function host() {
    style();
    if (isCA() && window.Ca && Ca._ && Ca._.open) return Ca._.open('squad');
    show('squad', 'squad'); return D.getElementById('s-squad');
  }
  const h2 = (t, id) => isCA() ? `<h2 class="ca-h2s" id="${id}">${t}</h2>` : `<h3 id="${id}">${t}</h3>`;
  const top = () => (isCA() ? '<h1 class="ca-h1 ca-onDark">Group</h1>' : '') + (window.League && League.banner ? League.banner() : '');   // 💎 Ratna League entry
  const caExtra = () => isCA() && window.Ca && Ca.group ? `<div class="card sq-card"><p class="sub" style="margin:0 0 8px">Study group without accounts? Send one unit's MCQ set by link — everyone gets the same questions.</p><button class="btn ghost" id="sqCaGroup">📚 Group MCQ set by link</button></div>` : '';
  const wireCaExtra = () => { const b = D.getElementById('sqCaGroup'); if (b) b.onclick = () => Ca.group(); };

  async function screen() {
    const el = EL = host();
    if (!signedIn() || parentAcct()) {
      el.innerHTML = `${top()}<div class="card sq-card">${h2(isCA() ? '👥 Your study group' : '🦁 Your squad', 'sqOffT')}
        <p class="sub">${demo() ? 'Friends, class leagues and cheers are switched off in the demo.' : 'Sign in to join your class league, add friends with a code and cheer each other on.'}</p>
        ${demo() ? '' : '<button class="btn" id="sqIn">Sign in</button>'}</div>${caExtra()}`;
      const b = D.getElementById('sqIn'); if (b) b.onclick = () => C() && C().open('in'); wireCaExtra(); return;
    }
    if (!H) el.innerHTML = `${top()}<div class="card sq-card"><p class="sub" role="status" style="margin:0">Loading your ${isCA() ? 'group' : 'squad'}…</p></div>`;
    else paint();
    await load();
    if (EL !== el || !el.isConnected || !el.classList.contains('active')) return;
    paint();
  }

  function paint() {
    const el = EL; if (!el) return;
    if (!H) {
      el.innerHTML = `${top()}<div class="card sq-card">${h2('Could not load', 'sqErrT')}<p class="sub">${esc(loadErr || 'Please check your internet connection.')}</p><button class="btn" id="sqRetry">Try again</button></div>${caExtra()}`;
      D.getElementById('sqRetry').onclick = screen; wireCaExtra(); return;
    }
    el.innerHTML = top() + (H._old ? `<p class="note" role="status">Offline — showing your squad from ${esc(new Date(H._old).toLocaleString('en-IN', { day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit' }))}.</p>` : '')
      + cheersHTML() + (pendingPC() ? challengeHTML() : '') + leagueHTML() + nudgesHTML() + friendsHTML() + (pendingPC() ? '' : challengeHTML()) + caExtra();
    wire(el); wireCaExtra();
  }

  /* ---------- 1. cheers received ---------- */
  function cheersHTML() {
    if (!cheersNow.length) return '';
    return `<section class="card sq-card" aria-labelledby="sqChT" role="status">${h2('💌 Cheers for you', 'sqChT')}
      <ul class="sq-list">${cheersNow.map(c => { const k = cheerOf(c.kind); return `<li class="sq-row"><span class="sq-av" aria-hidden="true">${esc(c.avatar)}</span><span class="sq-t">${esc(c.name)}: ${k[1]} ${esc(k[2])}</span></li>`; }).join('')}</ul></section>`;
  }

  /* parent controls (js/playready.js, server squad_home → social): friends & cheers / friend news switched off by a linked parent */
  const off = k => !!(H && H.social && H.social[k] === false);
  const offHTML = (t, m) => `<section class="card sq-card" aria-labelledby="sqOffP">${h2(t, 'sqOffP')}<p class="sub" style="margin:0">${m}</p></section>`;

  /* ---------- 2. league ---------- */
  const daysLeft = () => { const ws = new Date((H.week_start || '') + 'T00:00:00+05:30').getTime(); if (!ws) return null; return Math.max(1, Math.ceil((ws + 7 * 864e5 - Date.now()) / 864e5)); };
  const resetTxt = () => { const n = daysLeft(); return n == null ? 'Resets every Monday' : n === 1 ? 'Resets tomorrow (Monday)' : `Resets Monday · ${n} days left`; };
  function board() {         // me + accepted friends, most stars first
    const me = Object.assign({ me: true }, H.me);
    return [me].concat(H.friends || []).sort((a, b) => (b.week - a.week) || (a.me ? -1 : b.me ? 1 : 0) || String(a.name).localeCompare(b.name));
  }
  function leagueHTML() {
    const L = H.league;
    if (L && L.kind === 'class' && (L.classes || []).length) {
      const cl = L.classes, max = Math.max(1, ...cl.map(c => +c.avg || 0)), mine = cl.findIndex(c => c.me), m = cl[mine];
      const lead = mine === 0 ? (cl.length > 1 ? `🎉 ${esc(m.name)} is top this week!` : `${esc(m.name)} — every star counts!`)
        : `${esc(m.name)} needs ${kf(Math.ceil((+cl[mine - 1].avg - +m.avg) * Math.max(1, m.active)) + 1)} more ⭐ to pass ${esc(cl[mine - 1].name)}.`;
      return `<section class="card sq-card" aria-labelledby="sqLgT"><span class="tag">This week · ${esc(resetTxt())}</span>${h2('🏫 Class league', 'sqLgT')}
        <p class="sub">${esc(L.inst)} · average ⭐ per active student, so every class size is fair.</p>
        <ol class="sq-list" aria-label="Classes ranked this week">${cl.map((c, i) => `<li class="sq-row${c.me ? ' sq-me' : ''}"><span class="rank" aria-hidden="true">${i + 1}</span>
          <span class="sq-t">${esc(c.name)}${c.me ? ' (my class)' : ''}<small>${c.active} of ${c.size} active</small><span class="sq-bar" aria-hidden="true"><i style="width:${Math.round((+c.avg || 0) / max * 100)}%"></i></span></span>
          <span class="sq-wk" aria-label="${esc(c.name)}: ${Math.round(+c.avg || 0)} stars per student">${kf(+c.avg || 0)} ⭐</span></li>`).join('')}</ol>
        <p class="sq-foot" aria-live="polite">${lead} You earned ${kf(H.me.week)} ⭐ this week.</p></section>`;
    }
    if (off('friends')) return '';
    const B = board(), mi = B.findIndex(x => x.me), fr = H.friends || [];
    let lead = '';
    if (!fr.length) lead = 'Add a friend below — then you race each other for weekly stars.';
    else if (mi === 0) lead = B[1] ? `🎉 You lead the league${B[0].week > B[1].week ? ` by ${kf(B[0].week - B[1].week)} ⭐` : ''}!` : '';
    else lead = `${kf(B[mi - 1].week - B[mi].week + 1)} more ⭐ to pass ${esc(B[mi - 1].name)}.`;
    const show = B.slice(0, 5); if (mi >= 5) show.push(B[mi]);
    return `<section class="card sq-card" aria-labelledby="sqLgT"><span class="tag">This week · ${esc(resetTxt())}</span>${h2('👫 Friends league', 'sqLgT')}
      <ol class="sq-list" aria-label="Friends league this week">${show.map(x => `<li class="sq-row${x.me ? ' sq-me' : ''}"><span class="rank" aria-hidden="true">${B.indexOf(x) + 1}</span><span class="sq-av" aria-hidden="true">${esc(x.avatar)}</span>
        <span class="sq-t">${esc(x.name)}${x.me ? ' (you)' : ''}</span><span class="sq-wk">${kf(x.week)} ⭐</span><span class="sq-st" aria-label="${x.streak} day streak">${x.streak ? x.streak + '🔥' : ''}</span></li>`).join('')}</ol>
      ${lead ? `<p class="sq-foot" aria-live="polite">${lead}</p>` : ''}</section>`;
  }

  /* ---------- 3. friend news (nudges) ---------- */
  function nudges() {
    if (off('news') || off('friends')) return [];
    const me = H.me, fr = H.friends || [], out = [], used = new Set(), my = (S().pz && S().pz.best) || {};
    const add = (f, t, s) => { if (!f || used.has(f.id) || out.length >= 3) return; used.add(f.id); out.push({ f, t, s }); };
    fr.forEach(f => { const ks = Object.keys(f.pz || {}).filter(k => +my[k] > 0 && +f.pz[k] < +my[k]); if (ks.length) { const k = ks[0];
      add(f, `${f.name} beat your ${pzName(k)} time!`, `${fmtT(f.pz[k])} vs your ${fmtT(my[k])}. Try to win it back!`); } });
    const ahead = fr.filter(f => f.week > me.week).sort((a, b) => a.week - b.week)[0];
    if (ahead) add(ahead, `${ahead.name} is ${kf(ahead.week - me.week)} ⭐ ahead this week`, 'One quick quest could close the gap!');
    fr.filter(f => f.streak >= 3).sort((a, b) => b.streak - a.streak).forEach(f => add(f, `${f.name} is on a 🔥 ${f.streak}-day streak`, 'Send a cheer to keep it going!'));
    if (!ahead && me.week > 0) { const nx = fr.filter(f => f.week <= me.week).sort((a, b) => b.week - a.week)[0]; if (nx) add(nx, `You are ${kf(me.week - nx.week)} ⭐ ahead of ${nx.name}`, 'Keep it up — and cheer your friend on!'); }
    fr.filter(f => f.today > 0).forEach(f => add(f, `${f.name} earned ${kf(f.today)} ⭐ today`, 'Say well done!'));
    return out;
  }
  function nudgesHTML() {
    const N = nudges(); if (!N.length) return '';
    return `<section class="card sq-card" aria-labelledby="sqNwT">${h2('🔔 Friend news', 'sqNwT')}<ul class="sq-list">${N.map(n => `<li class="sq-row"><span class="sq-av" aria-hidden="true">${esc(n.f.avatar)}</span>
      <span class="sq-t">${esc(n.t)}<small>${esc(n.s)}</small></span><button class="sq-btn" type="button" data-cheer="${esc(n.f.id)}" aria-label="Cheer ${esc(n.f.name)}">👋 Cheer</button></li>`).join('')}</ul></section>`;
  }

  /* ---------- 4. friends ---------- */
  function friendsHTML() {
    if (off('friends')) return offHTML('👫 Friends', `Your parent has turned off friends and cheers for now. You can still learn and play games on your own${H.league && H.league.kind === 'class' ? ', and your class league still counts your stars' : ''}.`);
    const fr = H.friends || [], inc = H.incoming || [], cls = H.league && H.league.kind === 'class';
    const B = board();
    const list = !fr.length ? '<p class="sub">No friends yet. Share your code, or type a friend’s code below. They see your request in their Squad and accept it.</p>'
      : cls ? `<ol class="sq-list" aria-label="Friends this week">${B.map((x, i) => x.me ? `<li class="sq-row sq-me"><span class="rank" aria-hidden="true">${i + 1}</span><span class="sq-av" aria-hidden="true">${esc(x.avatar)}</span><span class="sq-t">${esc(x.name)} (you)</span><span class="sq-wk">${kf(x.week)} ⭐</span><span class="sq-st">${x.streak ? x.streak + '🔥' : ''}</span></li>`
          : `<li><button class="sq-row sq-frow" type="button" data-f="${esc(x.id)}" aria-label="${esc(x.name)}: ${x.week} stars this week, ${x.streak} day streak. Open to cheer or remove."><span class="rank" aria-hidden="true">${i + 1}</span><span class="sq-av" aria-hidden="true">${esc(x.avatar)}</span><span class="sq-t">${esc(x.name)}</span><span class="sq-wk">${kf(x.week)} ⭐</span><span class="sq-st">${x.streak ? x.streak + '🔥' : ''}</span></button></li>`).join('')}</ol>`
      : `<ul class="sq-list" aria-label="My friends">${fr.slice().sort((a, b) => String(a.name).localeCompare(b.name)).map(x => `<li><button class="sq-row sq-frow" type="button" data-f="${esc(x.id)}" aria-label="${esc(x.name)}. Open to cheer or remove."><span class="sq-av" aria-hidden="true">${esc(x.avatar)}</span><span class="sq-t">${esc(x.name)}<small>${kf(x.week)} ⭐ this week${x.streak ? ` · ${x.streak}🔥` : ''}</small></span><span class="sq-btn" aria-hidden="true">👋</span></button></li>`).join('')}</ul>`;
    const req = inc.map(r => `<div class="sq-row sq-req"><span class="sq-av" aria-hidden="true">${esc(r.avatar)}</span><span class="sq-t">${esc(r.name)} wants to be friends</span>
      <button class="sq-btn pri" type="button" data-acc="${esc(r.id)}" aria-label="Accept ${esc(r.name)}">Accept</button><button class="sq-btn" type="button" data-dec="${esc(r.id)}" aria-label="Say no to ${esc(r.name)}">No</button>${window.PlayReady ? `<button class="sq-btn" type="button" data-rep="${esc(r.id)}" aria-label="Report ${esc(r.name)}">🚩</button>` : ''}</div>`).join('');
    return `<section class="card sq-card" aria-labelledby="sqFrT">${h2(`👫 Friends${fr.length ? ` <small class="sq-st">${fr.length}</small>` : ''}`, 'sqFrT')}
      ${req ? `<div aria-live="polite">${req}</div>` : ''}${list}
      ${H.outgoing ? `<p class="sq-foot" style="text-align:left">⏳ ${H.outgoing} request${H.outgoing > 1 ? 's' : ''} waiting for a friend to accept. <button class="sq-link" type="button" id="sqCancel">Cancel ${H.outgoing > 1 ? 'them' : 'it'}</button></p>` : ''}
      <div class="sq-sub2">My friend code</div>
      <div class="sq-code"><b aria-label="Your friend code ${esc(String(H.me.code || '').split('').join(' '))}">${esc(H.me.code || '——')}</b><button class="sq-btn pri" type="button" id="sqShare">Share</button></div>
      <form class="sq-add" id="sqAddF" novalidate><label class="sq-vh" for="sqAddC">Friend's code</label>
        <input id="sqAddC" maxlength="6" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="ABC123" inputmode="text" aria-describedby="sqAddE">
        <button class="btn" type="submit" id="sqAddB">Add friend</button></form>
      <p class="sq-err" id="sqAddE" role="alert"></p>
      <p class="sq-foot" style="text-align:left;margin-top:0">Friends see only your first name, avatar, weekly ⭐ and 🔥 — never your email. <button class="sq-link" type="button" id="sqNewCode">New code</button></p></section>`;
  }

  /* ---------- 5. parent challenge (child side) ---------- */
  const won = (a, am, b, bm) => a > b || (a === b && am < bm);
  const pendingPC = () => (H.challenges || []).some(c => c.child_score == null);
  function challengeHTML() {
    const L = (H.challenges || []).slice(0, 3); if (!L.length) return '';
    const rows = L.map(c => {
      const mine = c.child_score != null;
      let st;
      if (!mine) st = `<small>${c.parent_done ? 'Your parent has played — can you beat them?' : 'Your parent plays on their phone too.'}</small>`;
      else if (c.parent_score == null) st = `<small>You: ${c.child_score}/5 · waiting for your parent to play</small>`;
      else { const w = won(c.child_score, c.child_ms, c.parent_score, c.parent_ms), t = c.child_score === c.parent_score && c.child_ms === c.parent_ms;
        st = `<small class="sq-res${w ? ' win' : ''}">You ${c.child_score}/5 · Parent ${c.parent_score}/5 — ${t ? 'a tie!' : w ? '🏆 you won!' : 'your parent won this time'}</small>`; }
      return `<li class="sq-row"><span class="sq-av" aria-hidden="true">${mine ? '✅' : '⚔️'}</span><span class="sq-t">${esc(c.title)} · 5 questions${st}</span>${mine ? '' : `<button class="sq-btn pri" type="button" data-pc="${esc(c.id)}">Play ▶</button>`}</li>`;
    }).join('');
    const any = L.some(c => c.child_score == null);
    return `<section class="card sq-card" aria-labelledby="sqPcT">${h2(any ? '👨‍👩‍👧 Your parent challenged you!' : '👨‍👩‍👧 Parent challenge', 'sqPcT')}
      <p class="sub">Most correct wins. If it's a tie, the faster one wins.</p><ul class="sq-list">${rows}</ul></section>`;
  }

  /* ---------- wiring ---------- */
  function wire(el) {
    el.querySelectorAll('[data-cheer]').forEach(b => b.onclick = () => friendSheet(b.dataset.cheer, true));
    el.querySelectorAll('[data-f]').forEach(b => b.onclick = () => friendSheet(b.dataset.f));
    el.querySelectorAll('[data-acc],[data-dec]').forEach(b => b.onclick = async () => {
      const id = b.dataset.acc || b.dataset.dec, ok = !!b.dataset.acc; b.disabled = true;
      try { const r = one(await rpc('squad_answer', { p_user: id, p_accept: ok })); if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not save.');
        if (ok) { tap('unlock'); say('🎉 You are now friends!'); } await load(); paint(); }
      catch (e) { b.disabled = false; say(errT(e)); }
    });
    el.querySelectorAll('[data-rep]').forEach(b => b.onclick = () => { const r = (H.incoming || []).find(x => x.id === b.dataset.rep); if (r && window.PlayReady) PlayReady.report({ id: r.id, name: r.name, avatar: r.avatar, context: 'request', after: () => { load().then(paint); } }); });
    const cc = D.getElementById('sqCancel'); if (cc) cc.onclick = async () => { cc.disabled = true; try { await rpc('squad_cancel_requests'); await load(); paint(); say('Request cancelled'); } catch (e) { cc.disabled = false; say(errT(e)); } };
    el.querySelectorAll('[data-pc]').forEach(b => b.onclick = () => { const c = (H.challenges || []).find(x => x.id === b.dataset.pc); if (c) play(c, 'child', () => { load().then(paint); }); });
    const f = D.getElementById('sqAddF'), inp = D.getElementById('sqAddC'), er = D.getElementById('sqAddE');
    if (!f) return;                                    // friends switched off by a parent: no code / add box
    D.getElementById('sqShare').onclick = shareCode;
    D.getElementById('sqNewCode').onclick = newCode;
    inp.oninput = () => { const v = inp.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 6); if (v !== inp.value) inp.value = v; er.textContent = ''; };
    f.onsubmit = async ev => {
      ev.preventDefault(); const code = inp.value.trim().toUpperCase();
      if (!/^[A-Z0-9]{6}$/.test(code)) { er.textContent = 'A friend code has 6 letters and numbers.'; inp.focus(); return; }
      const b = D.getElementById('sqAddB'); b.disabled = true; er.textContent = '';
      try { const r = one(await rpc('squad_add_friend', { p_code: code }));
        if (!r || !r.ok) { er.textContent = (r && r.msg) || 'Could not add.'; b.disabled = false; return; }
        tap(r.status === 'friends' ? 'unlock' : 'tap'); say(r.msg || 'Request sent'); await load(); paint();
        const i2 = D.getElementById('sqAddE'); if (i2) i2.textContent = ''; }
      catch (e) { er.textContent = errT(e); b.disabled = false; }
    };
  }
  async function shareCode() {
    const code = H.me.code, text = `Be my study buddy on Knowtopia! Open Squad → Friends and type my code: ${code}`;
    try { if (navigator.share) { await navigator.share({ title: 'Knowtopia', text }); return; } } catch (e) { if (e && e.name === 'AbortError') return; }
    try { await navigator.clipboard.writeText(text); say('Code copied — paste it to your friend'); return; } catch (e) {}
    window.open('https://wa.me/?text=' + encodeURIComponent(text), '_blank', 'noopener');
  }
  async function newCode() {
    const b = D.getElementById('sqNewCode');
    if (!b.dataset.sure) { b.dataset.sure = 1; b.textContent = 'Tap again: old code stops working'; return; }
    b.disabled = true;
    try { const r = one(await rpc('squad_new_code')); if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not change the code.'); H.me.code = r.code; say('New code ready'); paint(); }
    catch (e) { b.disabled = false; say(errT(e)); }
  }

  /* ---------- friend sheet: cheer (preset only) or remove ---------- */
  function friendSheet(id, cheerOnly) {
    const f = (H.friends || []).find(x => x.id === id); if (!f || !C()) return;
    const el = C().sheet(`<h3 id="clT">${esc(f.avatar)} ${esc(f.name)}</h3><p class="sub">${kf(f.week)} ⭐ this week${f.streak ? ` · 🔥 ${f.streak}-day streak` : ''}</p>
      <div class="sq-sub2" id="sqCgL">Send a cheer</div><div class="sq-cgrid" role="group" aria-labelledby="sqCgL">${CHEERS.map(c => `<button type="button" data-k="${c[0]}"><span aria-hidden="true">${c[1]}</span>${esc(c[2])}</button>`).join('')}</div>
      <p class="sq-err" id="sqCgE" role="alert"></p>
      ${cheerOnly ? '' : `<button class="btn ghost" type="button" id="sqRm">Remove ${esc(f.name)} from friends</button><div style="height:8px"></div>`}
      ${cheerOnly || !window.PlayReady ? '' : `<div class="sq-cgrid"><button type="button" id="sqRep"><span aria-hidden="true">🚩</span>Report</button><button type="button" id="sqBlk"><span aria-hidden="true">🚫</span>Block</button></div>`}
      <button class="btn ghost" type="button" data-close id="sqFx">Close</button>`);
    style();
    el.querySelector('#sqFx').onclick = () => C().closeSheet();
    el.querySelectorAll('.sq-cgrid button').forEach(b => b.onclick = async () => {
      el.querySelectorAll('.sq-cgrid button').forEach(x => x.disabled = true); const E = el.querySelector('#sqCgE'); E.textContent = '';
      try { const r = one(await rpc('squad_cheer', { p_to: id, p_kind: b.dataset.k }));
        if (!r || !r.ok) { E.textContent = (r && r.msg) || 'Could not send.'; el.querySelectorAll('.sq-cgrid button').forEach(x => x.disabled = false); return; }
        tap('unlock'); C().closeSheet(); say(`${cheerOf(b.dataset.k)[1]} Cheer sent to ${f.name}!`); }
      catch (e) { E.textContent = errT(e); el.querySelectorAll('.sq-cgrid button').forEach(x => x.disabled = false); }
    });
    const again = () => { load().then(paint); };
    const rp = el.querySelector('#sqRep'); if (rp) rp.onclick = () => PlayReady.report({ id, name: f.name, avatar: f.avatar, context: 'friend', after: again });
    const bk = el.querySelector('#sqBlk'); if (bk) bk.onclick = () => PlayReady.block({ id, name: f.name, after: again });
    const rm = el.querySelector('#sqRm');
    if (rm) rm.onclick = async () => {
      if (!rm.dataset.sure) { rm.dataset.sure = 1; rm.textContent = `Tap again to remove ${f.name}`; return; }
      rm.disabled = true;
      try { await rpc('squad_remove', { p_user: id }); C().closeSheet(); say(`${f.name} removed`); await load(); paint(); }
      catch (e) { rm.disabled = false; say(errT(e)); }
    };
  }

  /* ================= parent challenge: 5-question player (child here, parent in Parent Hub) =================
     SERVER-VERIFIED: the parent's phone picks 5 questions from the content files and sends them with their right option
     (rpc pc_create). Both sides then get the questions WITHOUT answers from rpc pc_start (which also starts the server
     clock), send only the option they picked (rpc pc_submit p_picks), and the server scores and times it. The right
     answers come back only after submitting. No score is ever sent by a phone. */
  function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  const okQ = q => q && typeof q.q === 'string' && q.q.length <= 600 && Array.isArray(q.options) && q.options.length >= 2 && q.options.length <= 6
    && q.options.every(o => typeof o === 'string' && o.length >= 1 && o.length <= 200) && Number.isInteger(+q.answer) && +q.answer >= 0 && +q.answer < q.options.length;
  /* pick 5 questions for a subject: chapters / units the child has already studied first, then the rest */
  async function pickQuestions(src, studied) {
    const pool = [];
    const add = (k, t, q) => { if (okQ(q)) pool.push({ k, t, s: studied.has(t), q }); };
    if (src.startsWith('ca/')) {
      const [, level, paper] = src.split('/'); if (!window.Ca || !Ca._) return null;
      const st = await Ca._.structure(level); const p = st && st.papers.find(x => x.id === paper); if (!p) return null;
      const units = []; p.chapters.forEach(c => c.units.forEach(u => { if (u.status === 'built') units.push(u); }));
      /* studied units first, then a few others: at most 8 unit files are loaded (phones on slow networks) */
      const order = units.filter(u => studied.has(u.id)).concat(shuffle(units.filter(u => !studied.has(u.id))));
      let n = 0;
      for (const u of order) {
        if (n >= 8 || (n >= 3 && pool.length >= 15)) break;
        let d = null; try { d = await Ca._.unitData(u.id); } catch (e) {} n++; if (!d) continue;
        (d.mcqs || []).forEach(q => { if (q && q.id != null && /^[A-Za-z0-9_-]{1,20}$/.test(String(q.id))) add(`${u.id}#${q.id}`, u.id, q); });
      }
    } else {
      const [g, sid] = src.slice(1).split('/'); const d = await subjectData(+g, sid); if (!d) return null;
      d.chapters.forEach(c => c.topics.forEach(t => (t.quiz || []).forEach((q, i) => add(`${t.id}#${i}`, t.id, q))));
    }
    const pref = pool.filter(x => x.s), base = pref.length >= 5 ? pref : pool;
    const out = [], usedT = new Set();
    for (const x of shuffle(base)) { if (out.length >= 5) break; if (!usedT.has(x.t)) { usedT.add(x.t); out.push(x); } }
    for (const x of shuffle(base)) { if (out.length >= 5) break; if (!out.includes(x)) out.push(x); }
    return out.length === 5 ? out.map(x => ({ k: x.k, q: x.q.q, o: x.q.options, a: +x.q.answer, x: String(x.q.explain || '').slice(0, 600) })) : null;
  }

  /* side: 'child' | 'parent'. Plays in the shared sheet; "Stop" after answering at least one question hands in what was answered. */
  async function play(ch, side, after, names) {
    if (!C()) return;
    style();
    const el = C().sheet(`<h3 id="clT">⚔️ ${esc(ch.title)} challenge</h3><p class="sub" role="status">Getting the questions ready…</p><button class="btn ghost" type="button" data-close id="sqPx">Close</button>`, false);
    el.querySelector('#sqPx').onclick = () => C().closeSheet();
    let qs = null, msg0 = '';
    try { const r = one(await rpc('pc_start', { p_id: ch.id })); if (r && r.ok && Array.isArray(r.questions) && r.questions.length === 5) qs = r.questions; else msg0 = (r && r.msg) || ''; }
    catch (e) { msg0 = errT(e); }
    if (!qs) { const p = el.querySelector('p.sub'); if (p) p.textContent = msg0 || 'These questions could not be loaded. Check your internet and try again.'; return; }
    const picks = [-1, -1, -1, -1, -1];
    let i = 0, done = false, saving = false;
    const finish = async () => {
      if (done || saving) return; saving = true;
      let r = null, msg = '';
      try { r = one(await rpc('pc_submit', { p_id: ch.id, p_picks: picks })); if (!r || !r.ok) { msg = (r && r.msg) || 'Could not save.'; r = null; } }
      catch (e) { msg = errT(e); }
      saving = false;
      if (!r) { if (el.classList.contains('show')) { const fb = el.querySelector('#sqFb'); if (fb) fb.innerHTML = `<span class="sq-err" role="alert">${esc(msg)}</span>`; } else say(msg); return; }
      done = true;
      const res = r.challenge, right = r.score, ms = r.ms, ans = r.answers || [], xs = r.explains || [];
      if (!el.classList.contains('show')) { say(`Saved: ${right} of 5`); if (after) after(res); return; }
      const oth = side === 'child' ? 'Parent' : ((names && names.child) || 'Child');
      const os = side === 'child' ? res.parent_score : res.child_score, om = side === 'child' ? res.parent_ms : res.child_ms;
      const w = os != null && won(right, ms, os, om), tie = os != null && right === os && ms === om;
      const review = qs.map((q, j) => { const ok = picks[j] === ans[j]; return `<li class="sq-rv ${ok ? 'ok' : 'no'}"><b>${ok ? '✅' : picks[j] < 0 ? '⏭️' : '❌'} ${esc(q.q)}</b>
        <span>${ok ? 'Your answer' : 'Right answer'}: “${esc((q.o || [])[ans[j]])}”${!ok && picks[j] >= 0 ? ` · you chose “${esc(q.o[picks[j]])}”` : ''}</span>${xs[j] ? `<small>${esc(xs[j])}</small>` : ''}</li>`; }).join('');
      el.querySelector('.sheet-in').innerHTML = `<div class="sheet-grab"></div><div class="sq-big" aria-hidden="true">${os == null ? '✅' : tie ? '🤝' : w ? '🏆' : '💪'}</div>
        <h3 id="clT" style="text-align:center">${os == null ? `You got ${right} of 5!` : tie ? 'It’s a tie!' : w ? 'You won the duel!' : `${esc(oth)} won this time`}</h3>
        <div class="sq-vs"><div><b>${right}/5</b><span>You · ${secs(ms)}</span></div><div class="x">VS</div><div><b>${os == null ? '?' : os + '/5'}</b><span>${esc(oth)}${os == null ? ' · not played yet' : ' · ' + secs(om)}</span></div></div>
        <p class="sub" style="text-align:center">${os == null ? `We’ll show both scores when ${side === 'child' ? 'your parent' : esc(oth)} has played.` : 'Most correct wins; on a tie the faster one wins.'}</p>
        <details class="sq-rvw"><summary>See the answers</summary><ol class="sq-list">${review}</ol></details>
        <button class="btn" type="button" data-close id="sqPx2">Done</button>`;
      el.querySelector('#sqPx2').onclick = () => { C().closeSheet(); if (after) after(res); };
      tap(w || os == null ? 'unlock' : 'tap');
    };
    const draw = () => {
      const q = qs[i];
      el.querySelector('.sheet-in').innerHTML = `<div class="sheet-grab"></div><h3 id="clT">⚔️ ${esc(ch.title)}</h3>
        <div class="sq-qh"><span>Question ${i + 1} of 5</span><span class="sq-dots" aria-hidden="true">${[0, 1, 2, 3, 4].map(j => j < i ? '●' : j === i ? '◉' : '○').join('')}</span></div>
        <p class="sq-q" id="sqQ">${esc(q.q)}</p>
        <div class="sq-opts" role="radiogroup" aria-labelledby="sqQ">${(q.o || []).map((o, k) => `<button class="sq-opt${picks[i] === k ? ' sel' : ''}" type="button" role="radio" aria-checked="${picks[i] === k}" data-k="${k}">${esc(o)}</button>`).join('')}</div>
        <div class="sq-fb" id="sqFb" aria-live="polite">${picks[i] >= 0 ? 'Answer chosen. You can still change it.' : 'Pick one answer. The scores are checked at the end.'}</div>
        <button class="btn" type="button" id="sqNx" ${picks[i] >= 0 ? '' : 'disabled'}>${i < 4 ? 'Next ▶' : 'Hand in ▶'}</button><div style="height:8px"></div>
        <button class="btn ghost" type="button" data-close id="sqPx">Stop</button>`;
      el.querySelector('#sqPx').onclick = () => { C().closeSheet(); if (picks.some(x => x >= 0) && !done) finish(); };
      el.querySelectorAll('.sq-opt').forEach(b => b.onclick = () => {
        picks[i] = +b.dataset.k; tap('tap');
        el.querySelectorAll('.sq-opt').forEach(x => { const on = +x.dataset.k === picks[i]; x.classList.toggle('sel', on); x.setAttribute('aria-checked', on); });
        el.querySelector('#sqFb').textContent = 'Answer chosen. You can still change it.';
        const nx = el.querySelector('#sqNx'); nx.disabled = false;
      });
      el.querySelector('#sqNx').onclick = () => { if (picks[i] < 0) return; if (i < 4) { i++; draw(); } else finish(); };
      const f = el.querySelector('.sq-opt.sel') || el.querySelector('.sq-opt'); if (f) f.focus();
    };
    draw();
  }

  /* ================= Parent Hub card (called by js/parent.js after a child's view is drawn) ================= */
  async function subjectsFor(st) {
    const p = (st && st.profile) || {}, g = +p.grade;
    if (p.course === 'ca') {
      const level = (st.ca && st.ca.level) || 'foundation'; if (!window.Ca || !Ca._) return [];
      let s; try { s = await Ca._.structure(level); } catch (e) { return []; }
      return (s && s.papers || []).filter(x => x.chapters.some(c => c.units.some(u => u.status === 'built'))).map(x => ({ src: `ca/${level}/${x.id}`, name: x.name }));
    }
    if (!g) return [];
    let cur = null; try { cur = CUR; } catch (e) {}
    if (!cur) { try { cur = await loadJSON('content/curriculum.json'); } catch (e) { return []; } }
    let all = (cur.grades && cur.grades[g] && cur.grades[g].subjects) || [];
    try { if (isStateBoard(p.board)) { await loadBoards(); const ok = boardSubjectIds(g, p.board); if (ok) all = all.filter(x => ok.includes(x.id)); } } catch (e) {}
    if (g >= 11 && Array.isArray(p.subjects) && p.subjects.length) all = all.filter(x => p.subjects.includes(x.id));
    return all.map(x => ({ src: `g${g}/${x.id}`, name: x.name }));
  }
  function studiedSet(st) {
    const s = new Set(); if (!st) return s;
    Object.keys(st.topics || {}).forEach(k => s.add(k));
    Object.keys((st.ca && st.ca.units) || {}).forEach(k => s.add(k));
    return s;
  }
  async function hubCard(body, k, A) {
    if (!body || !k || !k.child_id) return;
    style();
    let box = body.querySelector('#sqPc'); if (box) box.remove();
    box = D.createElement('section'); box.className = 'pv-card'; box.id = 'sqPc'; box.setAttribute('aria-labelledby', 'sqPcT');
    const mg = body.querySelector('.pv-manage'); mg ? body.insertBefore(box, mg) : body.appendChild(box);
    const name = (A && A.name) || k.name || 'your child', st = k.state && k.state.st;
    box.innerHTML = `<h3 id="sqPcT">⚔️ Challenge ${esc(name)}</h3><p class="pv-mut">Loading…</p>`;
    const subs = await subjectsFor(st);
    let list = []; try { const r = one(await rpc('pc_list', { p_child: k.child_id })); list = r && r.ok ? r.challenges || [] : []; } catch (e) {}
    if (!box.isConnected) return;
    const row = c => {
      const date = new Date(c.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
      let st2;
      if (!c.parent_done) st2 = `<button class="pv-btn" type="button" data-pplay="${esc(c.id)}">Play my turn</button>`;
      else if (!c.child_done) st2 = `<span class="pv-st warn">Waiting for ${esc(name)}</span>`;
      else { const w = won(c.parent_score, c.parent_ms, c.child_score, c.child_ms), t = c.parent_score === c.child_score && c.parent_ms === c.child_ms;
        st2 = `<span class="pv-st ${w ? 'ok' : 'warn'}">${t ? '🤝 Tie' : w ? '🏆 You won' : `🏆 ${esc(name)} won`}</span>`; }
      return `<li><div><b>${esc(c.title)}</b> <span class="pv-mut">${esc(date)}</span><br><span class="pv-mut">You ${c.parent_done ? (c.parent_score != null ? c.parent_score + '/5' : '✓') : '–'} · ${esc(name)} ${c.child_done ? (c.child_score != null ? c.child_score + '/5' : '✓') : '–'}</span></div>${st2}</li>`;
    };
    box.innerHTML = `<h3 id="sqPcT">⚔️ Challenge ${esc(name)}</h3>
      <p class="pv-mut">A 5-question duel from ${esc(name)}'s own lessons. You answer here; ${esc(name)} answers in the app (Squad tab). Most correct wins; on a tie the faster one wins.</p>
      ${subs.length ? `<form class="pv-form" id="sqPcF"><label for="sqPcS">Subject</label><select class="pv-in" id="sqPcS">${subs.map(s => `<option value="${esc(s.src)}">${esc(s.name)}</option>`).join('')}</select>
        <p class="pv-err" id="sqPcE" role="alert"></p><button class="pv-btn" type="submit" id="sqPcGo">Start the duel ▶</button></form>`
        : `<p class="pv-empty">Available once ${esc(name)} has chosen a class in the app.</p>`}
      ${list.length ? `<h4>Recent duels</h4><ul class="pv-list sq-pcl">${list.map(row).join('')}</ul>` : ''}`;
    const again = () => hubCard(body, k, A);
    box.querySelectorAll('[data-pplay]').forEach(b => b.onclick = () => { const c = list.find(x => x.id === b.dataset.pplay); if (c) play(c, 'parent', again, { child: name }); });
    const f = box.querySelector('#sqPcF'); if (!f) return;
    f.onsubmit = async ev => {
      ev.preventDefault(); const E = box.querySelector('#sqPcE'), go = box.querySelector('#sqPcGo'), sel = box.querySelector('#sqPcS');
      const src = sel.value, title = sel.options[sel.selectedIndex].textContent; E.textContent = ''; go.disabled = true; go.textContent = 'Picking 5 questions…';
      try {
        const qs = await pickQuestions(src, studiedSet(st));
        if (!qs) { E.textContent = 'Not enough questions in this subject yet. Please choose another one.'; return; }
        const r = one(await rpc('pc_create', { p_child: k.child_id, p_src: src, p_title: title, p_questions: qs }));
        if (!r || !r.ok) { E.textContent = (r && r.msg) || 'Could not start the duel.'; return; }
        play(r.challenge, 'parent', again, { child: name });
      } catch (e) { E.textContent = errT(e); }
      finally { go.disabled = false; go.textContent = 'Start the duel ▶'; }
    };
  }

  /* ================= hook the tab ================= */
  squadScreen = function () { return screen(); };   // eslint-disable-line no-global-assign
  window.squadScreen = squadScreen;
  window.Squad = { screen, sync, hubCard, play, _nudges: () => (H ? nudges() : []), _data: () => H };
})();
