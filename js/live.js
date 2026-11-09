/* ================= StudyVerse LIVE Game Rooms (play with friends) =================
   For paid students (and during the 24-hour trial); free plan sees a friendly locked card; parents never;
   owner/admin always (testing). Server: supabase/migrations/20261109_live_games.sql (SECURITY DEFINER RPCs —
   the database is the source of truth for turns, deadlines and scores; answer keys never reach other players).
   Live events go over Supabase Realtime broadcast (js/rt.js): "sync" (state changed → refetch), "emoji", "roll".
   Presence shows who is online. Every client also polls room_state every few seconds, and calls advance() after a
   deadline, so a game never stalls even without the WebSocket.
   Games: snakes (Snakes & Ladders Battle), quiz (Quiz Race), relay (Team Relay), buzzer (Buzzer round),
          duel (CA / professional Speed Duel: 10 MCQs × 72 s),
          puzzle (🧩 Puzzle Race: everyone solves the SAME puzzle — server: 20261110_puzzle_race.sql).
   Puzzle Race: the host picks a kind in the lobby; Puzzles.pick(kind) (js/puzzles.js) returns a self-contained JSON
   spec that rebuilds the identical puzzle on any device. Fairness/simplicity: EVERYONE gets the host's spec — number
   puzzles (Sudoku, Kakuro) and chapter puzzles alike (same chapter, same puzzle; the spec carries grade/subject, so a
   friend in another class can still load it). Start = the Edge Function puzzle-key, which builds the answer key ON
   THE SERVER (no phone supplies it) and then starts the race. Puzzles.race(el, spec, {onSolved, onQuit, onProgress})
   plays it here; progress goes to puzzle_progress (≤ 1 per 2.5 s) + a "pz" broadcast; onSolved's canonical `answer`
   goes to puzzle_solved, which checks it against the key (wrong = "keep going") and times it on the server. There is
   no "I solved it" button anywhere. Feature-detected: without Puzzles.kinds/pick/race the room says so.
   Questions: the host's app picks them per player course (school class pool / CA MCQ banks) and sends them to
   start_game; each player sees questions from their own class or course.
   Child safety: emoji reactions only (no text chat); players show avatar + first name only.
   Entry points: the 🎮 Play hub (js/playhub.js) calls Live.open({ game }) / Live.join(code) / Live.resume();
   links ?room=CODE. (No tiles are placed by this file any more.) */
(function () {
  'use strict';
  const D = document, $ = s => D.querySelector(s), $$ = (s, r) => [...(r || D).querySelectorAll(s)];
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const say = m => { try { toast(m); } catch (e) {} };
  const one = r => Array.isArray(r) ? r[0] : r;
  const lget = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } };
  const lset = (k, v) => { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const SITE = 'https://study.moneyviel.com/';
  const cap = s => String(s || '').charAt(0).toUpperCase() + String(s || '').slice(1);
  const rpc = async (fn, body) => one(await Cloud.rest('rpc/' + fn, { method: 'POST', body: body || {} }));

  const GAMES = {
    quiz: { e: '🏁', n: 'Quiz Race', d: 'Everyone gets a question at the same time. Right and fast wins.' },
    snakes: { e: '🐍', n: 'Snakes & Ladders Battle', d: 'Take turns to roll. Answer right on a ladder to climb, on a snake to escape.' },
    buzzer: { e: '🔔', n: 'Buzzer Round', d: 'First to buzz answers. A wrong answer lets the others buzz.' },
    relay: { e: '🏃', n: 'Team Relay', d: 'Teammates take turns to answer. The team total wins.', teams: true },
    duel: { e: '⚡', n: 'Speed Duel', d: 'CA exam pace: 10 MCQs, 72 seconds each.', pro: true },
    puzzle: { e: '🧩', n: 'Puzzle Race', d: 'Everyone solves the same puzzle. Fastest to finish wins.', puzzle: true } };
  const PZ_MINS = [3, 5, 8, 10];
  const MODES = { duel: ['1-v-1', 2], ffa: ['Free-for-all', 6], teams: ['Teams', 6] };
  const TEAMS = [{ n: 'Team Blue', e: '🔵' }, { n: 'Team Orange', e: '🟠' }];
  const EMOJI = ['👏', '😂', '😮', '🔥', '💪', '🎉'];
  const BADGES = [['lvComeback', '👑', 'Comeback King', 'Win after being last'], ['lvCaptain', '🧢', 'Team Captain', 'Top scorer of the winning team'], ['lvRacer', '🏎️', 'Quiz Racer', 'Win a Quiz Race or Speed Duel']];

  /* ---------- who am I ---------- */
  const STx = () => { try { return ST; } catch (e) { return null; } };      // app.js: top-level let (not on window)
  const isCA = () => { const s = STx(); return !!(s && s.profile && s.profile.course === 'ca'); };
  function myCourse() {
    const s0 = STx(), p = s0 && s0.profile; if (!p) return null;
    if (p.course === 'ca') return 'ca-' + ((ST.ca && ST.ca.level) || 'foundation');
    const g = +p.grade || 1;
    let ids = []; try { ids = (curSubjects(g) || []).map(x => x.id); } catch (e) {}
    return (g >= 11 && p.stream ? `school-g${g}-${p.stream}` : 'school-g' + g) + (ids.length ? '-m' + subjMask(ids) : '');
  }
  /* the player's OWN subjects travel with them as a small mask, so the host only picks questions from subjects
     each player studies (e.g. no Biology for a Maths student). Append new subject ids at the END only. */
  const SUBJ_ORDER = ['english', 'hindi', 'maths', 'evs', 'sanskrit', 'science', 'social', 'history', 'geography', 'civics', 'economics', 'physics', 'chemistry', 'biology', 'accountancy', 'business', 'polsci', 'psychology', 'sociology', 'cs'];
  function subjMask(ids) { let m = 0n; ids.forEach(id => { const i = SUBJ_ORDER.indexOf(id); if (i >= 0) m |= 1n << BigInt(i); }); return m.toString(16); }
  function maskIds(hex) { let m; try { m = BigInt('0x' + hex); } catch (e) { return null; } return SUBJ_ORDER.filter((_, i) => (m >> BigInt(i)) & 1n); }
  function courseName(c) {
    let m = /^school-g(\d+)(?:-(science|commerce|arts))?(?:-m[0-9a-f]+)?$/.exec(c || ''); if (m) return `Class ${m[1]}${m[2] && m[2] !== 'm' ? ' ' + cap(m[2]) : ''}`;
    m = /^ca-([a-z]+)$/.exec(c || ''); if (m) return 'CA ' + ({ foundation: 'Foundation', inter: 'Intermediate', final: 'Final' }[m[1]] || cap(m[1]));
    return cap(String(c || '').replace(/-/g, ' '));
  }
  const firstName = () => String((ST.profile && ST.profile.name) || 'Player').trim().split(/\s+/)[0].slice(0, 20) || 'Player';
  const avatar = () => (ST.profile && ST.profile.avatar) || '🙂';
  const uid = () => { try { const u = Cloud.user(); return u && u.id; } catch (e) { return null; } };
  /* quick local answer (the server decides for real) */
  function elig() {
    const C = window.Cloud; if (!C || !C.signedIn()) return { ok: false, why: 'signin' };
    if (C.isParent && C.isParent()) return { ok: false, why: 'parent' };
    try { if (C.admin() || localStorage.getItem('sv_owner') === '1') return { ok: true, admin: true }; } catch (e) {}
    if (localStorage.getItem('sv_access') == null) return { ok: null };
    return C.courses().length ? { ok: true } : { ok: false, why: 'free' };
  }
  /* Parent Hub: daily limit / quiet hours → the existing "Time to rest" screen, and no joining */
  function restBlocked() { try { if (window.Parent && Parent._enforce) { Parent._enforce(); return !!D.getElementById('pvRest'); } } catch (e) {} return false; }

  /* ---------- screen ---------- */
  function screen() {
    let s = D.getElementById('s-live');
    if (!s) { s = D.createElement('section'); s.className = 'screen'; s.id = 's-live'; D.querySelector('main').appendChild(s); }
    style(); return s;
  }
  function openScreen() { const s = screen(); show('live', 'practice'); return s; }
  const active = () => { const s = D.getElementById('s-live'); return !!(s && s.classList.contains('active')); };

  /* ================= state ================= */
  const L = { code: null, st: null, qs: null, ch: null, pollT: 0, tickT: 0, offset: 0, sig: '', stageSig: '', fetching: false, again: false, presence: {}, rtOn: false,
    advAt: {}, myAns: {}, sb: null, anim: false, lastLog: '', wasLast: false, seenTurn: null, net: true, failN: 0, emoT: 0, view: '',
    pz: null, pzLive: {}, pzMine: 0, pzSeen: -1, picking: false };
  const nowS = () => Date.now() + L.offset;

  async function fetchState() {
    if (!L.code) return;
    if (L.fetching) { L.again = true; return; }
    L.fetching = true;
    try {
      const j = await rpc('room_state', { p_code: L.code, p_q: !L.qs });
      L.failN = 0; setNet(true);
      if (!j || !j.ok) {
        if (j && (j.code === 'not_member' || j.code === 'not_found')) { const msg = j.banned ? 'The host removed you from the room.' : j.code === 'not_found' ? 'This room has closed.' : 'You are not in this room any more.'; exit(); say(msg); home(); }
        return;
      }
      L.offset = j.now - Date.now();
      if (j.questions) L.qs = j.questions;
      const prev = L.st; L.st = j;
      if (prev && prev.room.status === 'playing' && j.room.status === 'lobby') { L.qs = null; L.myAns = {}; }
      if (prev && prev.room.status === 'lobby' && j.room.status === 'playing') { L.qs = j.questions || null; L.myAns = {}; L.wasLast = false; L.sb = null; pzReset(); if (!L.qs) L.again = true; }
      render();
    } catch (e) { if (++L.failN >= 2) setNet(false); }
    finally { L.fetching = false; if (L.again) { L.again = false; setTimeout(fetchState, 60); } }
  }
  const soon = (() => { let t = 0; return () => { clearTimeout(t); t = setTimeout(fetchState, 80); }; })();
  function setNet(on) { L.net = on; const n = D.querySelector('.lv-net'); if (n) { n.classList.toggle('bad', !on || !L.rtOn); n.textContent = !on ? '⚠️ Reconnecting…' : L.rtOn ? '🟢 Live' : '🟡 Connecting…'; } }
  function schedule() {
    clearTimeout(L.pollT);
    if (!L.code) return;
    L.pollT = setTimeout(() => { if (!active()) return suspend(); fetchState().finally(schedule); }, L.rtOn ? 2500 : 1500);
  }
  function startLoops() {
    clearInterval(L.tickT); L.tickT = setInterval(tick, 250); schedule();
    if (window.RT && !L.ch) {
      L.ch = RT.open('room-' + L.code, { key: uid() || '',
        onStatus: s => { L.rtOn = s === 'joined'; setNet(L.net); if (s === 'joined') soon(); },
        onPresence: p => { L.presence = p; paintOnline(); },
        onBroadcast: (ev, pl) => { if (ev === 'sync') soon(); else if (ev === 'emoji') floatEmoji(pl); else if (ev === 'roll') rollFx(pl); else if (ev === 'pz') pzLiveIn(pl); } });
      L.ch.track({ name: firstName(), avatar: avatar() });
    }
  }
  function suspend() {                 // left the screen: stop talking to the server (still a member; turns auto-skip)
    pzStop(); clearInterval(L.tickT); clearTimeout(L.pollT); if (L.ch) { L.ch.close(); L.ch = null; } L.rtOn = false;
  }
  function exit() { suspend(); pzReset(); L.code = null; L.st = null; L.qs = null; L.sb = null; L.sig = ''; L.stageSig = ''; lset('sv_live_room', null); }
  const broadcast = (ev, pl) => { try { if (L.ch) L.ch.send(ev, pl); } catch (e) {} };
  const synced = () => { broadcast('sync', { s: L.st && L.st.room.step }); fetchState(); };

  /* online = in presence when the live channel is up, else seen by the server in the last 45 s */
  const online = p => p.left ? false : p.user_id === uid() ? true : L.rtOn && L.presence[uid()] ? !!L.presence[p.user_id] : p.online;
  function paintOnline() { if (!L.st) return; L.st.players.forEach(p => $$(`[data-on="${p.user_id}"]`).forEach(el => { const on = online(p); el.classList.toggle('off', !on); el.setAttribute('aria-label', on ? 'online' : 'offline'); el.title = on ? 'online' : 'offline'; })); }

  /* ================= entry: home ================= */
  async function home() {
    const s = openScreen(); L.view = 'home';
    if (L.code && L.st && L.st.ok) { enter(L.code); return; }
    const saved = lget('sv_live_room', null), back = saved && Date.now() - saved.at < 2 * 3600e3 ? saved.code : null;
    const e = elig();
    s.innerHTML = `<div class="lv-root lv-home"><button class="back" id="lvBack">← Back</button>
      <div class="card lv-hero"><div class="lv-hero-e" aria-hidden="true">🎮</div><div><h1 class="lv-h1">Game Rooms</h1><p class="sub">Play live with friends. Everyone gets questions from their own class or course.</p></div></div>
      <div id="lvMain">${e.ok === false ? lockedHTML(e.why) : mainHTML(back)}</div></div>`;
    $('#lvBack').onclick = () => (window.PlayHub && PlayHub.open ? PlayHub.open() : isCA() ? (window.Ca && Ca.home ? Ca.home() : worldScreen()) : practiceScreen());
    if (e.ok !== false) wireMain();
    try {                                                  // the server has the final word
      const j = await rpc('live_eligibility');
      if (j && !j.ok && L.view === 'home' && D.getElementById('lvMain')) { D.getElementById('lvMain').innerHTML = lockedHTML(j.reason); wireLocked(); }
      else if (j && j.ok && e.ok === false && D.getElementById('lvMain')) { D.getElementById('lvMain').innerHTML = mainHTML(back); wireMain(); }
    } catch (x) {}
    if (e.ok === false) wireLocked();
  }
  function lockedHTML(why) {
    const play = !!window.SV_PLAY;
    const msg = why === 'parent' ? 'Game Rooms are for students. Your child can play from their own StudyVerse app.'
      : why === 'signin' ? 'Sign in to play with friends.'
      : 'Game Rooms are part of StudyVerse plans. Play live quiz races, buzzer rounds and Snakes &amp; Ladders battles with your friends.';
    return `<div class="card lv-locked"><div class="lv-lock-e" aria-hidden="true">🔒</div><h2>Game Rooms are locked</h2><p class="sub">${msg}</p>
      ${why === 'free' ? (play ? '<p class="sub">Ask your parent about a StudyVerse plan.</p>' : '<button class="btn" id="lvPlans">See plans</button>') : ''}
      ${why === 'signin' ? '<button class="btn" id="lvSignin">Sign in</button>' : ''}
      <p class="lv-mut">You can still play the Arcade games on your own, any time.</p></div>`;
  }
  function wireLocked() {
    const p = D.getElementById('lvPlans'); if (p) p.onclick = () => { try { Plans.open(); } catch (e) {} };
    const si = D.getElementById('lvSignin'); if (si) si.onclick = () => { try { Cloud.open('in'); } catch (e) {} };
  }
  const defGame = () => (isCA() ? 'duel' : 'quiz');
  const draft = { game: null, mode: null, rounds: 10, secs: 20, level: 'mixed' };
  const LEVELS = [['mixed', '🎲 Mixed'], ['easy', '🟢 Easy'], ['moderate', '🟡 Moderate'], ['hard', '🔴 Hard']];
  function pickerHTML(d, id) {
    const g = d.game, gm = GAMES[g];
    const radios = (name, list, cur, lab) => `<div class="lv-chips" role="radiogroup" aria-label="${lab}">${list.map(([v, t]) => `<button type="button" role="radio" class="lv-chip${String(v) === String(cur) ? ' on' : ''}" aria-checked="${String(v) === String(cur)}" data-${name}="${v}">${t}</button>`).join('')}</div>`;
    const gameOrder = isCA() ? ['duel', 'quiz', 'buzzer', 'snakes', 'relay', 'puzzle'] : ['quiz', 'snakes', 'buzzer', 'relay', 'puzzle', 'duel'];
    const modes = Object.entries(MODES).filter(([k]) => !(gm.puzzle && k === 'teams'));
    return `<div class="lv-pick" id="${id}">
      <h3 class="lv-h3">Game</h3><div class="lv-games" role="radiogroup" aria-label="Game">${gameOrder.map(k => `<button type="button" role="radio" class="lv-game${k === g ? ' on' : ''}" aria-checked="${k === g}" data-game="${k}"><span class="lv-ge" aria-hidden="true">${GAMES[k].e}</span><b>${GAMES[k].n}</b><small>${GAMES[k].d}</small></button>`).join('')}</div>
      <h3 class="lv-h3">Mode</h3>${gm.teams ? '<p class="lv-mut">Team Relay is played in 2 teams.</p>' : radios('mode', modes.map(([k, v]) => [k, `${v[0]}${k === 'teams' ? ' (2 teams)' : k === 'ffa' ? ' (up to 6)' : ''}`]), d.mode, 'Mode')}
      ${gm.puzzle ? `<h3 class="lv-h3">Time limit</h3>${radios('rounds', PZ_MINS.map(v => [v, v + ' min']), d.rounds, 'Time limit')}
      <p class="lv-mut">🧩 Everyone gets the same puzzle — you choose it in the room: Sudoku, Kakuro, Crossword, Word search, Anagram or Concept sudoku.</p></div>` : `
      <h3 class="lv-h3">Question level</h3>${radios('level', LEVELS, d.level || 'mixed', 'Question level')}
      ${g === 'duel' ? '<p class="lv-mut">10 questions · 72 seconds each (100 MCQs in 2 hours).</p>' : `
      ${g === 'snakes' ? '<p class="lv-mut">🏁 The game goes on until someone reaches square 100.</p>' : `<h3 class="lv-h3">Questions</h3>${radios('rounds', [5, 10, 15].map(v => [v, String(v)]), d.rounds, 'Questions')}`}
      <h3 class="lv-h3">Time for each ${g === 'snakes' ? 'turn' : 'question'}</h3>${radios('secs', [[10, '10 s'], [20, '20 s'], [30, '30 s']], d.secs, 'Time')}`}</div>`}`;
  }
  function normDraft(d) {
    if (!GAMES[d.game]) d.game = defGame();
    if (GAMES[d.game].teams) d.mode = 'teams';
    if (!MODES[d.mode]) d.mode = d.game === 'duel' ? 'duel' : 'ffa';
    if (d.game === 'snakes') d.rounds = 30;               // no round limit for Snakes: the server ends it only when someone reaches 100
    else if (d.game === 'puzzle') { if (d.mode === 'teams') d.mode = 'ffa'; if (!PZ_MINS.includes(+d.rounds)) d.rounds = 8; }   // rounds = minutes
    else if (d.game !== 'duel' && ![5, 10, 15].includes(+d.rounds)) d.rounds = 10;
    if (!LEVELS.some(([v]) => v === d.level)) d.level = 'mixed';
    if (![10, 20, 30].includes(+d.secs)) d.secs = 20;
    return d;
  }
  function wirePicker(box, d, onChange) {
    box.querySelectorAll('[data-game]').forEach(b => b.onclick = () => { S('tap'); const was = d.game; d.game = b.dataset.game; if (was !== d.game && d.game === 'duel') d.mode = 'duel'; if (was === 'duel' && d.game !== 'duel' && d.mode === 'duel') d.mode = 'ffa'; if (was !== d.game && d.game === 'puzzle') d.rounds = 8; normDraft(d); onChange(); });
    box.querySelectorAll('[data-mode]').forEach(b => b.onclick = () => { S('tap'); d.mode = b.dataset.mode; normDraft(d); onChange(); });
    box.querySelectorAll('[data-rounds]').forEach(b => b.onclick = () => { S('tap'); d.rounds = +b.dataset.rounds; onChange(); });
    box.querySelectorAll('[data-secs]').forEach(b => b.onclick = () => { S('tap'); d.secs = +b.dataset.secs; onChange(); });
    box.querySelectorAll('[data-level]').forEach(b => b.onclick = () => { S('tap'); d.level = b.dataset.level; onChange(); });
  }
  function mainHTML(back) {
    normDraft(Object.assign(draft, { game: draft.game || defGame(), mode: draft.mode || (defGame() === 'duel' ? 'duel' : 'ffa') }));
    return `${back ? `<div class="card lv-rejoin"><p><b>Your room ${E(back)}</b> is still open.</p><button class="btn mint" id="lvRejoin">↩ Back to room ${E(back)}</button></div>` : ''}
      <div class="card"><h2 class="lv-h2">Join a room</h2><label class="lv-lab" for="lvCode">Room code from your friend</label>
        <div class="lv-joinrow"><input id="lvCode" class="lv-in" maxlength="6" autocomplete="off" autocapitalize="characters" spellcheck="false" inputmode="text" placeholder="ABCDEF" aria-describedby="lvErr"><button class="btn mint" id="lvJoin">Join ▶</button></div>
        <p class="lv-err" id="lvErr" role="alert"></p></div>
      <div class="card"><h2 class="lv-h2">Start a room</h2><p class="sub">Pick a game, then share the code with friends.</p><div id="lvPickH">${pickerHTML(draft, 'lvPick')}</div>
        <button class="btn" id="lvCreate">➕ Create room</button><p class="lv-err" id="lvErr2" role="alert"></p></div>
      <div class="card"><h2 class="lv-h2">🏆 This week with friends</h2><div id="lvBoard"><p class="lv-mut">Loading…</p></div></div>
      <div class="card"><h2 class="lv-h2">🏅 Game badges</h2>${badgeGrid()}</div>`;
  }
  function badgeGrid() {
    const have = (STx() && STx().badges) || {};
    return `<div class="lv-badges">${BADGES.map(([id, e, n, d]) => `<div class="lv-bdg${have[id] ? ' on' : ''}"><b aria-hidden="true">${e}</b><span>${n}</span><small>${have[id] ? 'Earned ✓' : d}</small></div>`).join('')}</div>`;
  }
  function wireMain() {
    const rj = D.getElementById('lvRejoin'); if (rj) rj.onclick = () => { const s = lget('sv_live_room', null); if (s) join(s.code); };
    const inp = D.getElementById('lvCode');
    inp.oninput = () => { const v = inp.value.toUpperCase().replace(/[^A-Z]/g, '').slice(0, 6); if (v !== inp.value) inp.value = v; };
    inp.onkeydown = e => { if (e.key === 'Enter') D.getElementById('lvJoin').click(); };
    D.getElementById('lvJoin').onclick = () => { const v = inp.value.trim().toUpperCase(); if (!/^[A-Z]{6}$/.test(v)) { D.getElementById('lvErr').textContent = 'Room codes have 6 letters.'; return; } join(v); };
    const repaint = () => { D.getElementById('lvPickH').innerHTML = pickerHTML(draft, 'lvPick'); wirePicker(D.getElementById('lvPick'), draft, repaint); };
    wirePicker(D.getElementById('lvPick'), draft, repaint);
    D.getElementById('lvCreate').onclick = create;
    board();
  }
  async function board() {
    const el = D.getElementById('lvBoard'); if (!el) return;
    try {
      const rows = await Cloud.rest('rpc/weekly_board', { method: 'POST', body: {} }); const list = Array.isArray(rows) ? rows : [];
      if (!D.getElementById('lvBoard')) return;
      el.innerHTML = list.length ? `<ol class="lv-lb">${list.map((r, i) => `<li class="${r.me ? 'me' : ''}"><span class="lv-rk">${i + 1}</span><span class="lv-av" aria-hidden="true">${E(r.avatar)}</span><span class="lv-nm">${E(r.name)}${r.me ? ' (you)' : ''}</span><span class="lv-wn">${r.wins} win${r.wins === 1 ? '' : 's'} · ${r.games} game${r.games === 1 ? '' : 's'}</span></li>`).join('')}</ol>`
        : '<p class="lv-mut">Play a game with friends and your weekly table appears here.</p>';
    } catch (e) { el.innerHTML = '<p class="lv-mut">Could not load the table right now.</p>'; }
  }
  const errText = j => (j && j.msg) || 'Something went wrong. Please try again.';
  async function create() {
    if (restBlocked()) return;
    const b = D.getElementById('lvCreate'), er = D.getElementById('lvErr2'); if (!b || b.disabled) return;
    const c = myCourse(); if (!c) return;
    b.disabled = true; er.textContent = '';
    try {
      const j = await rpc('create_room', { p_game: draft.game, p_mode: draft.mode, p_rounds: draft.game === 'duel' ? 10 : +draft.rounds, p_turn_secs: draft.game === 'duel' ? 72 : +draft.secs, p_name: firstName(), p_avatar: avatar(), p_course: c, p_level: draft.level || 'mixed' });
      if (!j || !j.ok) { if (j && (j.code === 'free' || j.code === 'parent')) { D.getElementById('lvMain').innerHTML = lockedHTML(j.code); wireLocked(); return; } er.textContent = errText(j); return; }
      S('unlock'); enter(j.code);
    } catch (e) { er.textContent = (window.Cloud && Cloud.errText) ? Cloud.errText(e) : e.message; }
    finally { if (b.isConnected) b.disabled = false; }
  }
  async function join(code) {
    if (restBlocked()) return;
    code = String(code || '').toUpperCase();
    if (!D.getElementById('s-live') || !active()) { await home(); }
    const er = D.getElementById('lvErr'); if (er) er.textContent = '';
    try {
      const j = await rpc('join_room', { p_code: code, p_name: firstName(), p_avatar: avatar(), p_course: myCourse() });
      if (!j || !j.ok) {
        if (j && (j.code === 'free' || j.code === 'parent')) { const m = D.getElementById('lvMain'); if (m) { m.innerHTML = lockedHTML(j.code); wireLocked(); } return; }
        if (er) er.textContent = errText(j); else say(errText(j));
        if (j && j.code === 'not_found' && lget('sv_live_room', {}).code === code) lset('sv_live_room', null);
        return;
      }
      S('open'); enter(j.code);
    } catch (e) { const m = (window.Cloud && Cloud.errText) ? Cloud.errText(e) : e.message; if (er) er.textContent = m; else say(m); }
  }
  function enter(code) {
    if (L.code && L.code !== code) exit();
    const s = openScreen(); L.view = 'room';
    if (L.code !== code) { L.code = code; L.st = null; L.qs = null; L.sb = null; L.sig = ''; L.stageSig = ''; L.myAns = {}; }
    lset('sv_live_room', { code, at: Date.now() });
    if (!L.st) s.innerHTML = `<div class="lv-root"><div class="card"><p class="sub">Opening room ${E(code)}…</p></div></div>`;
    else { L.sig = ''; L.stageSig = ''; L.sb = null; render(); }
    startLoops(); fetchState();
  }

  /* ================= render ================= */
  function render() {
    const st = L.st; if (!st || !active()) return;
    const r = st.room;
    if (r.status !== 'playing' || r.game !== 'puzzle') pzStop();
    if (r.status === 'lobby') return lobby(st);
    if (r.status === 'finished') return results(st);
    return game(st);
  }
  const host = () => L.st && L.st.room.host_id === uid();
  const meP = () => L.st && L.st.players.find(p => p.user_id === uid());
  const actives = () => L.st.players.filter(p => !p.left);
  const nameOf = id => { const p = L.st && L.st.players.find(x => x.user_id === id); return p ? p.name : 'Someone'; };
  function keepFocus(fn) { const a = D.activeElement, id = a && a.id, k = a && a.dataset && (a.dataset.k || a.dataset.kick); fn(); if (id && D.getElementById(id)) D.getElementById(id).focus(); else if (k != null) { const b = D.querySelector(`[data-k="${k}"],[data-kick="${k}"]`); if (b) b.focus(); } }
  const emojiBar = () => `<div class="lv-emo" role="group" aria-label="Send a reaction">${EMOJI.map(e => `<button type="button" class="lv-emob" data-emo="${e}" aria-label="Send ${e}">${e}</button>`).join('')}</div><div class="lv-floats" aria-hidden="true"></div>`;
  function wireEmoji(root) {
    root.querySelectorAll('[data-emo]').forEach(b => b.onclick = () => {
      if (Date.now() - L.emoT < 1200) return; L.emoT = Date.now();
      const pl = { u: uid(), e: b.dataset.emo }; broadcast('emoji', pl); if (!L.rtOn) floatEmoji(pl); S('tap');
    });
  }
  function floatEmoji(pl) {
    if (!pl || !EMOJI.includes(pl.e)) return;                 // only our own emoji set (no free text)
    const box = D.querySelector('#s-live .lv-floats'); if (!box) return;
    const s = D.createElement('span'); s.className = 'lv-float'; s.style.left = (10 + Math.random() * 70) + '%';
    s.innerHTML = `<b>${pl.e}</b><small>${E(nameOf(pl.u))}</small>`; box.appendChild(s); setTimeout(() => s.remove(), 2600);
  }
  function announce(t) { const a = D.querySelector('#s-live .lv-live'); if (a && t) { a.textContent = ''; setTimeout(() => { a.textContent = t; }, 30); } }
  function teamTotals() { const t = [0, 0]; L.st.players.forEach(p => { if (p.team === 0 || p.team === 1) t[p.team] += p.score; }); return t; }

  /* ---------- lobby ---------- */
  function lobby(st) {
    const r = st.room, me = meP(), H = host(), ps = st.players.filter(p => !p.left), max = MODES[r.mode][1];
    const sig = JSON.stringify(['lobby', r.step, r.host_id, ps.map(p => [p.user_id, p.ready, p.team, p.name]), L.rtOn]);
    if (sig === L.sig) { paintOnline(); return; } L.sig = sig; L.stageSig = ''; L.sb = null;
    const why = startProblem(st);
    const link = SITE + '?room=' + r.code, wa = 'https://wa.me/?text=' + encodeURIComponent(`Join my StudyVerse game room! 🎮 ${GAMES[r.game].n}. Code: ${r.code} ${link}`);
    const pRow = p => `<li class="lv-p"><span class="lv-av" aria-hidden="true">${E(p.avatar)}</span><span class="lv-dot" data-on="${p.user_id}"></span>
      <span class="lv-nm">${E(p.name)}${p.user_id === uid() ? ' (you)' : ''}${p.user_id === r.host_id ? ' <span class="lv-host" title="Host">👑 host</span>' : ''}<small>${E(courseName(p.course))}</small></span>
      <span class="lv-rdy ${p.ready || p.user_id === r.host_id ? 'on' : ''}">${p.user_id === r.host_id ? 'Host' : p.ready ? '✓ Ready' : 'Not ready'}</span>
      ${H && p.user_id !== uid() ? `<button type="button" class="lv-kick" data-kick="${p.user_id}" aria-label="Remove ${E(p.name)}">✕</button>` : ''}</li>`;
    const list = r.mode === 'teams'
      ? `<div class="lv-teams">${TEAMS.map((t, i) => `<div class="lv-team t${i}"><h3 class="lv-h3">${t.e} ${t.n}</h3><ul class="lv-plist">${ps.filter(p => p.team === i).map(pRow).join('') || '<li class="lv-mut">No one yet</li>'}</ul></div>`).join('')}</div>
         <button type="button" class="btn ghost" id="lvTeam">⇄ Switch to ${TEAMS[me && me.team === 0 ? 1 : 0].n}</button>`
      : `<ul class="lv-plist">${ps.map(pRow).join('')}</ul>`;
    keepFocus(() => {
      screen().innerHTML = `<div class="lv-root lv-lobby"><div class="lv-top"><b>🎮 Game room</b><span class="lv-net"></span></div>
        <div class="card lv-codecard"><span class="lv-k">Room code</span><div class="lv-code" aria-label="Room code ${r.code.split('').join(' ')}">${r.code}</div>
          <div class="lv-share"><a class="btn lv-wa" id="lvWa" href="${wa}" target="_blank" rel="noopener">📲 Share on WhatsApp</a><button type="button" class="btn ghost" id="lvCopy">📋 Copy link</button></div>
          <p class="lv-mut">Friends can also type the code in Game Rooms.</p></div>
        <div class="card"><h2 class="lv-h2">${GAMES[r.game].e} ${GAMES[r.game].n}</h2><p class="sub">${r.game === 'puzzle' ? `${MODES[r.mode][0]} · ${r.rounds} min time limit · same puzzle for everyone` : `${MODES[r.mode][0]} · ${r.game === 'snakes' ? 'until someone reaches 100' : `${r.rounds} questions`} · ${r.turn_secs} s each · ${(LEVELS.find(([v]) => v === (r.level || 'mixed')) || LEVELS[0])[1]} questions`}</p>
          ${r.game === 'puzzle' ? pzLobbyHTML(r, H) : ''}
          ${H ? `<details class="lv-set"><summary>Change game</summary><div id="lvPickL">${pickerHTML(normDraft({ game: r.game, mode: r.mode, rounds: r.rounds, secs: r.turn_secs, level: r.level }), 'lvPick2')}</div></details>` : `<p class="lv-mut">${E(GAMES[r.game].d)}</p>`}</div>
        <div class="card"><h2 class="lv-h2">Players <small>(${ps.length}/${max})</small></h2>${list}</div>
        <div class="lv-actions">${H ? `<button class="btn" id="lvStart" ${why ? 'aria-disabled="true"' : ''}>▶ Start game</button><p class="lv-hint" id="lvHint" role="status">${E(why || 'Everyone is ready!')}</p>`
          : `<button class="btn mint" id="lvReady" aria-pressed="${!!(me && me.ready)}">${me && me.ready ? '✓ I’m ready (tap to undo)' : '✋ I’m ready'}</button><p class="lv-hint" role="status">${me && me.ready ? 'Waiting for the host to start…' : 'Tap when you are ready to play.'}</p>`}
          <button class="btn ghost" id="lvLeave">Leave room</button></div>
        ${emojiBar()}<div class="lv-live sr-only" aria-live="polite"></div></div>`;
    });
    setNet(L.net); paintOnline();
    const root = screen();
    wireEmoji(root);
    $('#lvCopy').onclick = async () => { try { await navigator.clipboard.writeText(link); say('Link copied ✓'); } catch (e) { say(link); } S('tap'); };
    $('#lvLeave').onclick = leave;
    root.querySelectorAll('[data-kick]').forEach(b => b.onclick = async () => {
      if (!b.dataset.sure) { b.dataset.sure = '1'; b.textContent = 'Remove?'; b.classList.add('sure'); return; }
      try { const j = await rpc('kick_player', { p_code: r.code, p_user: b.dataset.kick }); if (j && !j.ok) say(errText(j)); synced(); } catch (e) { say('No connection.'); }
    });
    const tb = $('#lvTeam'); if (tb) tb.onclick = async () => { try { await rpc('set_team', { p_code: r.code, p_team: me && me.team === 0 ? 1 : 0 }); S('tap'); synced(); } catch (e) {} };
    const rd = $('#lvReady'); if (rd) rd.onclick = async () => { rd.disabled = true; try { await rpc('set_ready', { p_code: r.code, p_ready: !(me && me.ready) }); S('tap'); synced(); } catch (e) { say('No connection.'); } finally { rd.disabled = false; } };
    const sb = $('#lvStart'); if (sb) sb.onclick = start;
    root.querySelectorAll('[data-pzk]').forEach(b => b.onclick = () => { S('tap'); pickPuzzle(b.dataset.pzk); });
    const pk = D.getElementById('lvPick2');
    if (pk) { const d = normDraft({ game: r.game, mode: r.mode, rounds: r.rounds, secs: r.turn_secs, level: r.level });
      wirePicker(pk, d, async () => {
        try { const j = await rpc('update_room', { p_code: r.code, p_game: d.game, p_mode: d.mode, p_rounds: d.game === 'duel' ? 10 : d.rounds, p_turn_secs: d.game === 'duel' ? 72 : d.secs, p_level: d.level || 'mixed' });
          if (j && !j.ok) say(errText(j)); L.sig = ''; synced(); setTimeout(() => { const det = D.querySelector('.lv-set'); if (det) det.open = true; }, 400); } catch (e) { say('No connection.'); }
      }); }
  }
  function startProblem(st) {
    const r = st.room, ps = st.players.filter(p => !p.left);
    if (ps.length < 2) return 'Share the code — you need at least 2 players.';
    if (r.mode === 'duel' && ps.length !== 2) return '1-v-1 needs exactly 2 players.';
    if (r.mode === 'teams' && (!ps.some(p => p.team === 0) || !ps.some(p => p.team === 1))) return 'Both teams need at least one player.';
    if (r.game === 'puzzle' && !(r.state && r.state.puzzle)) return host() ? 'Pick a puzzle first.' : 'The host is choosing a puzzle…';
    const nr = ps.filter(p => !p.ready && p.user_id !== r.host_id).map(p => p.name);
    if (nr.length) return `Waiting for ${nr.join(', ')} to be ready.`;
    return '';
  }
  async function start() {
    const b = $('#lvStart'), hint = $('#lvHint'); if (!b || b.dataset.busy) return;
    const why = startProblem(L.st); if (why) { hint.textContent = why; S('hmm'); return; }
    b.dataset.busy = '1'; b.textContent = L.st.room.game === 'puzzle' ? '⏳ Starting…' : '⏳ Getting questions ready…';
    try {
      if (L.st.room.game === 'puzzle') {                  // Puzzle Race: the server builds the answer key, then starts
        let j = null;
        try { j = await Cloud.call('/functions/v1/puzzle-key', { method: 'POST', body: { code: L.code } }); }
        catch (e) { hint.textContent = e && e.status === 404 ? 'Puzzle races are not switched on yet on the server. Please try another game.' : (e && e.message) || 'Could not start. Check your internet and try again.'; S('hmm'); return; }
        if (!j || !j.ok) { hint.textContent = errText(j); S('hmm'); return; }
        S('unlock'); L.qs = null; synced(); return;
      }
      const qs = await pickQuestions(L.st);
      const j = await rpc('start_game', { p_code: L.code, p_questions: qs });
      if (!j || !j.ok) { hint.textContent = j && j.code === 'need_questions' ? `We could not find enough questions for ${(j.need || []).map(courseName).join(', ')} yet. Try another game, or fewer questions.` : errText(j); S('hmm'); return; }
      S('unlock'); L.qs = null; synced();
    } catch (e) { hint.textContent = 'Could not get the questions. Check your internet and try again.'; }
    finally { if (b.isConnected) { delete b.dataset.busy; b.textContent = '▶ Start game'; } }
  }
  async function leave() {
    const code = L.code; exit();
    try { await rpc('leave_room', { p_code: code }); } catch (e) {}
    broadcast('sync', {}); S('tap'); home();
  }

  /* ---------- questions (host) ---------- */
  function rng(seed) { let a = 2166136261; for (const ch of String(seed)) a = Math.imul(a ^ ch.charCodeAt(0), 16777619) >>> 0; return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const shuffle = (a, r) => { a = a.slice(); r = r || Math.random; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const STREAM_SUBJ = { science: ['physics', 'chemistry', 'maths', 'biology', 'english'], commerce: ['accountancy', 'business', 'economics', 'english', 'maths'], arts: ['history', 'polsci', 'geography', 'psychology', 'sociology', 'economics', 'english'] };
  const okQ = q => window.Arcade && Arcade.okQ ? Arcade.okQ(q) : (q && typeof q.q === 'string' && Array.isArray(q.options) && Number.isInteger(q.answer));
  const fit = q => !q.visual && q.q.length <= 1400 && q.options.every(o => o.length <= 480);
  /* question level. CA questions carry a level (core / moderate / hard). School questions have none, so we score them:
     more solution steps, longer wording, calculations and NOT/EXCEPT questions count as harder; then each subject's
     questions are split into thirds (easy / moderate / hard) so every level has enough questions. */
  const qScore = q => (Array.isArray(q.steps) ? q.steps.length * 3 : 0) + Math.min(40, (q.q || '').length / 12) + (q.check ? 6 : 0) +
    (/\b(not|except|incorrect|false)\b/i.test(q.q || '') ? 4 : 0) + Math.min(10, (q.options || []).join(' ').length / 40) + (/\d/.test(q.q || '') ? 3 : 0);
  function byLevel(list, lvl, score) {
    if (!lvl || lvl === 'mixed' || list.length < 6) return list;
    const s = list.map(q => [score(q), q]).sort((a, b) => a[0] - b[0]), n = s.length, a = Math.floor(n / 3), b = Math.floor(2 * n / 3);
    return (lvl === 'easy' ? s.slice(0, a) : lvl === 'moderate' ? s.slice(a, b) : s.slice(b)).map(x => x[1]);
  }
  async function schoolPool(g, stream, need, only, lvl) {
    let subs = []; try { subs = (CUR && CUR.grades && CUR.grades[g] && CUR.grades[g].subjects) || []; } catch (e) {}
    if (!subs.length) { try { const cu = await loadJSON('content/curriculum.json'); subs = (cu.grades && cu.grades[g] && cu.grades[g].subjects) || []; } catch (e) {} }
    if (only) subs = subs.filter(s => only.includes(s.id));          // exactly the subjects this player studies
    else if (stream && STREAM_SUBJ[stream]) { const f = subs.filter(s => STREAM_SUBJ[stream].includes(s.id)); if (f.length) subs = f; }
    const mine = ST.profile && +ST.profile.grade === g && ST.profile.course !== 'ca';
    const pickN = mine ? 4 : 3;
    const chosen = shuffle(subs).slice(0, pickN);
    const datas = await Promise.all(chosen.map(s => Promise.resolve(subjectData(g, s.id)).catch(() => null)));
    const by = [];
    datas.forEach((d, i) => {
      if (!d || !Array.isArray(d.chapters)) return; const s = chosen[i], st = (window.Worlds && Worlds.SUBJECT_STYLE && Worlds.SUBJECT_STYLE[s.id]) || { e: '📘' }; const L2 = [];
      d.chapters.forEach(c => (c.topics || []).forEach(t => (t.quiz || []).forEach(q => { if (okQ(q) && fit(q)) L2.push({ _d: qScore(q), q: q.q, o: q.options, a: q.answer, s: `${st.e} ${s.name || cap(s.id)} · ${t.title}`, x: String(q.explain || '').slice(0, 580) }); })));
      const L3 = byLevel(L2, lvl, x => x._d).map(x => { delete x._d; return x; }); if (L3.length) by.push(shuffle(L3));
    });
    return spread(by, need);
  }
  function spread(lists, need) { const out = []; while (out.length < need && lists.some(l => l.length)) for (const l of lists) if (l.length && out.length < need) out.push(l.pop()); return out; }
  async function caPool(level, game, need, lvl) {
    const want = { easy: 'core', moderate: 'moderate', hard: 'hard' }[lvl] || null;
    const X = window.Ca && Ca._; if (!X) return [];
    let st; try { st = await X.structure(level); } catch (e) { return []; }
    const units = []; st.papers.forEach(p => p.chapters.forEach(c => c.units.forEach(u => units.push({ p, c, u }))));
    let pool = units.filter(x => x.u.status === 'built');
    if (game === 'duel') { const obj = pool.filter(x => /-p[34]-/.test(x.u.id)); if (obj.length >= 4) pool = obj; }
    const chosen = shuffle(pool).slice(0, 8), by = [];
    const bad = window.Arcade && Arcade.BAD_OPT;
    for (const x of chosen) {
      let d = null; try { d = await X.unitData(x.u.id); } catch (e) {}
      const L2 = ((d && d.mcqs) || []).filter(q => !want || (q.level || 'core') === want).filter(q => q && typeof q.q === 'string' && Array.isArray(q.options) && q.options.length >= 2 && q.options.length <= 4 && q.options.every(o => typeof o === 'string' && o.trim()) && Number.isInteger(q.answer) && q.answer < q.options.length && !(bad && q.options.some(o => bad.test(o))) && fit(q))
        .map(q => ({ q: q.q, o: q.options, a: q.answer, s: `${X.paperLabel ? X.paperLabel(x.p) : (x.p.title || x.p.id)} · ${x.u.title}`.slice(0, 118), x: String(q.explain || '').slice(0, 580) }));
      if (L2.length) by.push(shuffle(L2));
    }
    if (want && by.reduce((t, l) => t + l.length, 0) < Math.min(need, 10)) return caPool(level, game, need, 'mixed');   // too few at this level: mix
    return spread(by, need);
  }
  async function pickQuestions(st) {
    const r = st.room, courses = [...new Set(st.players.filter(p => !p.left).map(p => p.course))];
    const need = r.game === 'snakes' ? 60 : r.rounds, out = {}, lvl = r.level || 'mixed';
    for (const c of courses) {
      let m, list = [];
      try {
        if ((m = /^school-g(\d+)(?:-(science|commerce|arts))?(?:-m([0-9a-f]+))?$/.exec(c))) list = await schoolPool(+m[1], m[2], need, m[3] ? maskIds(m[3]) : null, lvl);
        else if ((m = /^ca-([a-z]+)$/.exec(c))) list = await caPool(m[1], r.game, need, lvl);
      } catch (e) { console.warn('live: questions for', c, e); }
      out[c] = list;
    }
    return out;
  }

  /* ---------- game screen ---------- */
  function game(st) {
    const r = st.room, gm = GAMES[r.game];
    const shellSig = JSON.stringify(['game', r.code, r.game, r.mode, st.room.status, host()]);
    if (L.sig !== shellSig || !D.querySelector('#s-live .lv-play')) {
      L.sig = shellSig; L.stageSig = ''; L.sb = null; pzStop();
      screen().innerHTML = `<div class="lv-root lv-play" data-game="${r.game}"><div class="lv-top"><b>${gm.e} ${gm.n}</b><span class="lv-round"></span><span class="lv-net"></span></div>
        <div class="lv-timer" role="timer" aria-label="Time left"><i></i><span class="lv-secs"></span></div>
        <div class="lv-scores" aria-label="Scores"></div><div class="lv-stage"></div>
        <div class="lv-gfoot">${emojiBar()}<div class="lv-qrow"><button type="button" class="lv-quit" id="lvQuit">Leave game</button>${host() ? '<button type="button" class="lv-quit" id="lvEnd">End game for everyone</button>' : ''}</div></div><div class="lv-live sr-only" aria-live="polite"></div></div>`;
      wireEmoji(screen());
      const en = $('#lvEnd'); if (en) en.onclick = async function () { if (!this.dataset.sure) { this.dataset.sure = 1; this.textContent = 'Tap again to end the game'; return; } try { await rpc('finish_game', { p_code: L.code }); synced(); } catch (e) { say('No connection.'); } };
      $('#lvQuit').onclick = function () { if (!this.dataset.sure) { this.dataset.sure = 1; this.textContent = 'Tap again to leave'; return; } leave(); };
      setNet(L.net);
    }
    if (r.game === 'puzzle') { pzStrip(st); const rd0 = D.querySelector('#s-live .lv-round'), inf = (r.state && r.state.puzzle) || {}; if (rd0) rd0.textContent = `${inf.e || '🧩'} ${inf.n || 'Puzzle'}`; puzzleStage(st); tick(); return; }
    scores(st);
    const rd = D.querySelector('#s-live .lv-round');
    if (rd) rd.textContent = r.game === 'snakes' ? `Round ${(r.state && r.state.round) || 1} · first to 100 wins` : `Question ${Math.min(r.qi + 1, r.rounds)} of ${r.rounds}`;
    // comeback tracking: was I last at some point (after the first question / round)?
    const ps = actives(), mine = ps.find(p => p.user_id === uid());
    if (mine && ps.length >= 2 && (r.qi >= 1 || (r.state && r.state.round > 1))) { const low = Math.min(...ps.map(p => p.score)); if (mine.score === low && ps.some(p => p.score > low)) L.wasLast = true; }
    if (r.game === 'snakes') snakesStage(st); else if (r.game === 'buzzer') buzzerStage(st); else quizStage(st);
    tick();
  }
  function scores(st) {
    const box = D.querySelector('#s-live .lv-scores'); if (!box) return;
    const r = st.room, ps = st.players.slice().sort((a, b) => b.score - a.score || a.seat - b.seat), turn = r.turn_user, ans = new Set(r.answered_ids || []);
    const chip = p => `<span class="lv-sc${p.user_id === uid() ? ' me' : ''}${p.user_id === turn ? ' turn' : ''}${p.left ? ' left' : ''}"><span class="lv-dot" data-on="${p.user_id}"></span><span aria-hidden="true">${E(p.avatar)}</span> ${E(p.name)}${p.left ? ' (left)' : ''} <b>${r.game === 'snakes' ? '📍' + p.pos : p.score}</b>${ans.has(p.user_id) ? '<i aria-label="answered">✓</i>' : ''}</span>`;
    let h;
    if (r.mode === 'teams') { const t = teamTotals(); h = TEAMS.map((tm, i) => `<div class="lv-tsc t${i}"><b>${tm.e} ${tm.n}: ${t[i]}</b><div>${ps.filter(p => p.team === i).map(chip).join('')}</div></div>`).join(''); }
    else h = ps.map(chip).join('');
    if (box.dataset.h !== h) { box.dataset.h = h; box.innerHTML = h; }
    paintOnline();
  }
  function tick() {
    if (!L.st || !L.code) return;
    if (!active()) return suspend();
    const r = L.st.room, bar = D.querySelector('#s-live .lv-timer i'), sec = D.querySelector('#s-live .lv-secs'), tm = D.querySelector('#s-live .lv-timer');
    if (r.status !== 'playing') return;
    if (r.game === 'puzzle') return pzTick(r);
    const now = nowS(), pre = r.game !== 'snakes' && r.round_at && now < r.round_at;
    if (r.deadline) {
      const total = ((r.game === 'snakes' ? r.turn_secs + 2 : r.turn_secs) * 1000), left = Math.max(0, r.deadline - now), frac = pre ? 1 : Math.min(1, left / total);
      if (bar) bar.style.transform = `scaleX(${frac})`;
      const done = r.state && r.state.done;
      if (sec) sec.textContent = pre ? `Get ready… ${Math.ceil((r.round_at - now) / 1000)}` : done ? 'Round over' : `${Math.ceil(left / 1000)} s`;
      if (tm) tm.classList.toggle('hot', !pre && !done && left <= 5000);
      const cd = D.querySelector('#s-live .lv-count'); if (cd) { if (pre) cd.textContent = Math.max(1, Math.ceil((r.round_at - now) / 1000)); else if (cd.dataset.go !== '1') { cd.dataset.go = '1'; L.stageSig = ''; render(); return; } }
    }
    // keep the game moving: after the deadline (or when everyone answered) any member asks the server to advance
    const done = r.state && r.state.done, offTurn = r.game === 'snakes' && r.turn_user && (() => { const p = L.st.players.find(x => x.user_id === r.turn_user); return !p || p.left || !p.online; })();
    const due = (r.game === 'snakes' && offTurn) || (done && r.done_at ? now >= r.done_at + 2100 : r.deadline && now >= r.deadline + (r.game === 'snakes' || (r.game === 'buzzer' && r.turn_user) ? 1600 : 2100));
    if (!due) return;
    const k = r.step, last = L.advAt[k] || 0; if (Date.now() - last < 1800) return; L.advAt[k] = Date.now();
    rpc('advance', { p_code: L.code, p_step: k }).then(j => { if (j && j.changed) synced(); else fetchState(); }).catch(() => {});
  }

  /* question card: same option order for this question on every render (seeded) */
  function qCard(box, q, key, o) {
    const ord = shuffle(q.o.map((_, k) => k), rng(L.code + key));
    const res = o.res;                     // { choice, answer, correct, explain, points }
    box.innerHTML = `<div class="card lv-q${o.dim ? ' dim' : ''}">${q.s ? `<div class="lv-src">${E(q.s)}</div>` : ''}<div class="lv-qt">${E(q.q)}</div>
      <div class="lv-opts">${ord.map((k, j) => { const cls = res ? (k === res.answer ? ' right' : k === res.choice ? ' wrong' : '') : ''; return `<button type="button" class="opt lv-opt${cls}" data-k="${k}" ${o.lock || res ? 'disabled' : ''}><span class="lv-l" aria-hidden="true">${'ABCD'[j]}</span><span>${E(q.o[k])}</span></button>`; }).join('')}</div>
      <div class="lv-x">${res ? `<div class="lv-exp ${res.correct ? 'good' : 'bad'}" role="status"><b>${res.correct ? `🎉 Correct!${res.points ? ` +${res.points}` : ''}` : res.choice == null ? `⏰ The answer is: ${E(q.o[res.answer])}` : `🤔 The answer is: ${E(q.o[res.answer])}`}</b>${res.explain ? `<p>${E(res.explain)}</p>` : ''}</div>` : ''}${o.note ? `<p class="lv-note" role="status">${o.note}</p>` : ''}</div></div>`;
    if (!o.lock && !res && o.pick) box.querySelectorAll('.lv-opt').forEach(b => b.onclick = () => { box.querySelectorAll('.lv-opt').forEach(x => x.disabled = true); b.classList.add('picked'); o.pick(+b.dataset.k); });
  }
  const myQ = i => { const l = L.qs || []; return l.length ? l[i % l.length] : null; };
  function countdownHTML(t) { return `<div class="card lv-cd"><p class="sub">${t}</p><div class="lv-count" aria-live="off">3</div></div>`; }

  /* ---------- Quiz Race / Speed Duel / Team Relay ---------- */
  function quizStage(st) {
    const r = st.room, box = D.querySelector('#s-live .lv-stage'), me = uid(), now = nowS();
    const pre = r.round_at && now < r.round_at, done = !!(r.state && r.state.done), late = r.deadline && now > r.deadline + 1500;
    const runner = r.game !== 'relay' || (r.state.runners || []).includes(me), ans = st.me.answer && st.me.answer.qi === r.qi ? st.me.answer : null, local = L.myAns[r.step];
    const answered = !!(ans || local), ended = done || late;
    const sig = JSON.stringify([r.step, pre, done, late, answered, !!st.me.reveal, (r.answered_ids || []).length, !!L.qs]);
    if (sig === L.stageSig) return; L.stageSig = sig;
    if (pre) { box.innerHTML = countdownHTML(r.qi === 0 ? `${GAMES[r.game].n} starts in…` : 'Next question in…'); return; }
    if (!L.qs) { box.innerHTML = '<div class="card"><p class="sub">Loading questions…</p></div>'; return; }
    const q = myQ(r.qi); if (!q) { box.innerHTML = '<div class="card"><p class="sub">No question for your course.</p></div>'; return; }
    const waiting = actives().filter(p => (r.game !== 'relay' || (r.state.runners || []).includes(p.user_id)) && !(r.answered_ids || []).includes(p.user_id)).map(p => p.name);
    if (!runner) {
      const runners = (r.state.runners || []).map(nameOf);
      const myTeam = (meP() || {}).team, mate = (r.state.runners || []).find(id => (st.players.find(p => p.user_id === id) || {}).team === myTeam);
      box.innerHTML = `<div class="card lv-wait"><div class="lv-big" aria-hidden="true">🏃</div><h2 class="lv-h2">${mate ? `${E(nameOf(mate))} is running for your team!` : 'Your teammate is running'}</h2><p class="sub">Running now: ${E(runners.join(' and '))}. Cheer them on with an emoji! Your turn comes soon.</p>${ended ? '<p class="lv-note">Round over — next runners coming up…</p>' : ''}</div>`;
      return;
    }
    let res = null;
    if (local) res = local; else if (ans) res = { choice: ans.choice, correct: ans.correct, points: ans.points, answer: st.me.reveal ? st.me.reveal.answer : null, explain: st.me.reveal && st.me.reveal.explain };
    if (res && res.answer == null && st.me.reveal) res.answer = st.me.reveal.answer;
    if (!res && ended && st.me.reveal) res = { choice: null, correct: false, answer: st.me.reveal.answer, explain: st.me.reveal.explain };
    const note = res ? (ended ? 'Next question coming up…' : waiting.length ? `Waiting for ${E(waiting.join(', '))}…` : 'Everyone answered!') : '';
    qCard(box, q, r.qi + ':' + (st.me.course || ''), { res: res && res.answer != null ? res : null, lock: ended || (res && res.answer == null), note: res && res.answer == null ? '✓ Answer sent. ' + note : note,
      pick: async k => {
        try {
          const j = await rpc('submit_answer', { p_code: L.code, p_step: r.step, p_choice: k });
          if (!j || !j.ok) { if (j && j.code === 'late') say('⏰ Time is up!'); else if (j && j.code !== 'stale') say(errText(j)); L.stageSig = ''; fetchState(); return; }
          L.myAns[r.step] = { choice: k, correct: j.correct, answer: j.answer, explain: j.explain, points: j.points };
          S(j.correct ? 'correct' : 'wrong'); announce(j.correct ? `Correct! Plus ${j.points}.` : 'Not quite.');
          L.stageSig = ''; synced();
        } catch (e) { say('No connection — trying again…'); L.stageSig = ''; fetchState(); }
      } });
  }

  /* ---------- Buzzer ---------- */
  function buzzerStage(st) {
    const r = st.room, box = D.querySelector('#s-live .lv-stage'), me = uid(), now = nowS();
    const pre = r.round_at && now < r.round_at, done = !!(r.state && r.state.done), late = !r.turn_user && r.deadline && now > r.deadline + 1000;
    const out = (r.state.out || []).includes(me), buzzer = r.turn_user, local = L.myAns[r.qi + ':b'];
    const sig = JSON.stringify([r.step, pre, done, late, out, buzzer, !!st.me.reveal, !!local, !!L.qs]);
    if (sig === L.stageSig) return; L.stageSig = sig;
    if (pre) { box.innerHTML = countdownHTML(r.qi === 0 ? 'Buzzer round starts in…' : 'Next question in…'); return; }
    if (!L.qs) { box.innerHTML = '<div class="card"><p class="sub">Loading questions…</p></div>'; return; }
    const q = myQ(r.qi); if (!q) return;
    if (done || late) {
      const w = r.state.winner, res = st.me.reveal ? { choice: local ? local.choice : null, correct: !!(local && local.correct), answer: st.me.reveal.answer, explain: st.me.reveal.explain } : null;
      qCard(box, q, r.qi + ':' + st.me.course, { res, lock: true, note: w ? (w === me ? '🏆 You got it! +100' : `🔔 ${E(nameOf(w))} got it!`) + ' Next question coming up…' : 'Nobody got this one. Next question coming up…' });
      return;
    }
    if (buzzer === me) {
      qCard(box, q, r.qi + ':' + st.me.course, { note: '🔔 You buzzed first! Pick your answer before time runs out.', pick: async k => {
        try {
          const j = await rpc('submit_answer', { p_code: L.code, p_step: r.step, p_choice: k });
          if (!j || !j.ok) { if (j && j.code === 'late') say('⏰ Too late!'); L.stageSig = ''; fetchState(); return; }
          L.myAns[r.qi + ':b'] = { choice: k, correct: j.correct }; S(j.correct ? 'correct' : 'wrong'); announce(j.correct ? 'Correct! Plus 100.' : 'Not quite. The others can buzz now.');
          L.stageSig = ''; synced();
        } catch (e) { say('No connection.'); L.stageSig = ''; fetchState(); }
      } });
      announce('You buzzed first! Pick your answer.');
      return;
    }
    const msg = buzzer ? `🔔 <b>${E(nameOf(buzzer))}</b> buzzed! Waiting for the answer…` : out ? 'You tried this one. Watch the others!' : (r.state.out || []).length ? `${E((r.state.out || []).map(nameOf).join(', '))} missed — buzz now!` : 'Know it? Buzz first!';
    box.innerHTML = `<div class="card lv-q">${q.s ? `<div class="lv-src">${E(q.s)}</div>` : ''}<div class="lv-qt">${E(q.q)}</div><ol class="lv-olist" type="A">${q.o.map(o => `<li>${E(o)}</li>`).join('')}</ol></div>
      <button type="button" class="lv-buzz" id="lvBuzz" ${buzzer || out ? 'disabled' : ''}>🔔 BUZZ!</button><p class="lv-note lv-bmsg" role="status">${msg}</p>`;
    const bz = $('#lvBuzz');
    if (bz && !bz.disabled) bz.onclick = async () => {
      bz.disabled = true; S('tap');
      try {
        const j = await rpc('buzz', { p_code: L.code, p_step: r.step });
        if (!j || !j.ok) { if (j && j.code === 'taken') say('Someone buzzed first!'); L.stageSig = ''; fetchState(); return; }
        broadcast('sync', { s: j.step }); L.stageSig = ''; fetchState();
      } catch (e) { bz.disabled = false; say('No connection.'); }
    };
    if (buzzer && buzzer !== me) announce(`${nameOf(buzzer)} buzzed!`);
  }

  /* ---------- Snakes & Ladders Battle ---------- */
  function slMsg(st) {
    const l = st.room.state.last; if (!l) return '';
    const n = l.user === uid() ? 'You' : nameOf(l.user), you = l.user === uid();
    if (l.skip) return `⏭️ ${n} missed a turn.`;
    if (l.kind) {
      const t = l.timeout ? ' (time ran out)' : '';
      if (l.kind === 'lad') return l.ok ? `🪜 ${n} climbed to ${l.to}!` : `🪜 ${n} missed the ladder${t} and stayed on ${l.from}.`;
      return l.ok ? `🐍 ${n} escaped the snake!` : `🐍 ${n} slid down to ${l.to}${t}.`;
    }
    if (l.over) return `🎲 ${n} rolled ${l.roll} — too big! ${you ? 'You need' : 'Needs'} exactly ${100 - l.from} to reach 100.`;
    return `🎲 ${n} rolled ${l.roll}${l.to ? ` and moved to ${l.to}` : ''}.`;
  }
  function snakesStage(st) {
    const r = st.room, box = D.querySelector('#s-live .lv-stage'), me = uid(), now = nowS(), A = window.Arcade;
    const order = (r.state.order || st.players.map(p => p.user_id)), players = order.map(id => st.players.find(p => p.user_id === id)).filter(Boolean);
    if (!L.sb || L.sb.key !== r.code + ':' + order.join()) {
      box.innerHTML = `<div class="lv-slhost"></div><div class="lv-sldice"><div class="arc-die lv-die" aria-hidden="true">🎲</div><div class="lv-slact"></div></div>
        <p class="arc-slog lv-slog" aria-live="polite"></p><p class="sl-rule">${E(A ? A.SL_RULE : '')}</p><div class="lv-slq"></div>`;
      const bd = A && A.slBoard ? A.slBoard(box.querySelector('.lv-slhost'), players.map(p => ({ icon: p.avatar })), (f, ms) => setTimeout(f, ms)) : null;
      L.sb = { key: r.code + ':' + order.join(), bd, ids: players.map(p => p.user_id), lastKey: '' };
      players.forEach((p, i) => bd && bd.place(i, p.pos));
      L.stageSig = '';
    }
    const sb = L.sb, bd = sb.bd;
    // move tokens (animate the roll that just happened)
    if (bd && !L.anim) {
      const l = r.state.last, lk = l ? JSON.stringify(l) : '';
      const moves = [];
      sb.ids.forEach((id, i) => { const p = st.players.find(x => x.user_id === id); if (!p) return; bd.gone(i, p.left || !online(p)); if (bd.pos[i] !== p.pos) moves.push([i, p]); });
      if (moves.length) {
        L.anim = true; let n = moves.length;
        const fin = () => { if (--n <= 0) { L.anim = false; L.stageSig = ''; render(); } };
        moves.forEach(([i, p]) => {
          const then = () => { if (bd.pos[i] !== p.pos) bd.slide(i, p.pos, fin); else fin(); };
          if (l && l.user === p.user_id && l.roll && !l.kind && !l.over && bd.pos[i] === l.from && l.to > l.from && lk !== sb.lastKey) bd.hop(i, l.to, then);   // the roll: step by step
          else bd.slide(i, p.pos, fin);                                                                                                                  // ladder / snake / catch-up
        });
        sb.lastKey = lk;
      } else sb.lastKey = lk;
      const ti = sb.ids.indexOf(r.turn_user); if (ti >= 0) bd.active(ti);
    }
    const log = box.querySelector('.lv-slog'), msg = slMsg(st);
    if (log && log.textContent !== msg && !L.anim) log.textContent = msg;
    const die = box.querySelector('.lv-die'); if (die && r.state.last && r.state.last.roll && die.dataset.k !== String(r.step)) { die.dataset.k = r.step; die.textContent = r.state.last.roll; die.classList.remove('roll'); void die.offsetWidth; die.classList.add('roll'); }
    const pre = r.round_at && now < r.round_at && r.qi === 0 && (r.state.round || 1) === 1 && !r.state.last;
    const gate = r.state.gate, mine = r.turn_user === me;
    const sig = JSON.stringify([r.step, mine, !!gate, pre, !!L.qs, L.anim]);
    if (sig === L.stageSig) return; L.stageSig = sig;
    const act = box.querySelector('.lv-slact'), qb = box.querySelector('.lv-slq');
    if (mine && L.seenTurn !== r.step && !gate) { L.seenTurn = r.step; S('open'); announce('Your turn! Roll the dice.'); }
    if (L.anim) { act.innerHTML = '<p class="lv-note">Moving…</p>'; return; }
    if (gate) {
      act.innerHTML = `<p class="lv-note">${gate.user === me ? (gate.kind === 'lad' ? '🪜 Ladder! Answer right to climb.' : '🐍 Snake! Answer right to escape.') : `${E(nameOf(gate.user))} is answering a ${gate.kind === 'lad' ? 'ladder 🪜' : 'snake 🐍'} question…`}</p>`;
      if (gate.user === me) {
        const q = myQ(gate.qi); if (!q) { qb.innerHTML = '<div class="card"><p class="sub">Loading question…</p></div>'; return; }
        qb.innerHTML = `<div class="lv-sltitle">${gate.kind === 'lad' ? `🪜 Answer right to climb from ${gate.at} to ${gate.to}!` : `🐍 Answer right to escape — or slide to ${gate.to}!`}</div><div class="lv-slqb"></div>`;
        qCard(qb.querySelector('.lv-slqb'), q, 'g' + gate.qi + ':' + st.me.course, { pick: async k => {
          try {
            const j = await rpc('submit_answer', { p_code: L.code, p_step: r.step, p_choice: k });
            if (!j || !j.ok) { if (j && j.code === 'late') say('⏰ Time ran out!'); L.stageSig = ''; fetchState(); return; }
            S(j.correct ? 'correct' : 'wrong'); announce(j.correct ? (gate.kind === 'lad' ? 'Correct! Up you go!' : 'Correct! You escaped!') : 'Not quite.');
            const box2 = qb.querySelector('.lv-slqb'); qCard(box2, q, 'g' + gate.qi + ':' + st.me.course, { res: { choice: k, correct: j.correct, answer: j.answer, explain: j.explain }, lock: true });
            setTimeout(() => { L.stageSig = ''; synced(); }, 1400);
          } catch (e) { say('No connection.'); L.stageSig = ''; fetchState(); }
        } });
        setTimeout(() => { try { qb.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); } catch (e) {} }, 100);
      } else qb.innerHTML = '';
      return;
    }
    qb.innerHTML = '';
    if (mine) {
      act.innerHTML = `<button type="button" class="btn lv-roll" id="lvRoll">🎲 Roll the dice</button>`;
      $('#lvRoll').onclick = async function () {
        this.disabled = true; S('tap'); die.classList.remove('roll'); void die.offsetWidth; die.classList.add('roll');
        try {
          const j = await rpc('submit_move', { p_code: L.code, p_step: r.step });
          if (!j || !j.ok) { if (j && j.code === 'late') say('⏰ Your turn is over.'); else if (j && j.code !== 'stale') say(errText(j)); L.stageSig = ''; fetchState(); return; }
          die.textContent = j.roll; broadcast('roll', { u: me, v: j.roll }); synced();
        } catch (e) { this.disabled = false; say('No connection.'); }
      };
    } else act.innerHTML = `<p class="lv-note">${r.turn_user ? `${E(nameOf(r.turn_user))}'s turn…` : ''}</p>`;
  }
  function rollFx(pl) { if (!pl || pl.u === uid()) return; const d = D.querySelector('#s-live .lv-die'); if (d && /^[1-6]$/.test(String(pl.v))) { d.classList.remove('roll'); void d.offsetWidth; d.classList.add('roll'); d.textContent = pl.v; } }

  /* ---------- 🧩 Puzzle Race ----------
     Contract with js/puzzles.js (feature-detected, it may load later or be an older version):
       Puzzles.kinds() → [{ id, e, n, d, chapter }]      Puzzles.pick(id) → Promise<spec | null>
       Puzzles.race(el, spec, { onSolved({ ms, hints, mistakes }), onQuit(), onProgress({ done, total }) }) → { stop() }
       optional Puzzles.describe(spec) → string | { ch, d }  (lobby label; else read from common spec fields)
     Everyone plays the HOST's spec (see the header). The server times the solve; client ms is only a fallback label. */
  const PZ = () => window.Puzzles || null;
  function pzKinds() {
    try { const P = PZ(), k = P && typeof P.kinds === 'function' ? P.kinds() : null; return Array.isArray(k) ? k.filter(x => x && /^[a-z0-9]{2,12}$/.test(String(x.id || ''))) : []; } catch (e) { return []; }
  }
  const pzCanPick = () => !!(pzKinds().length && typeof PZ().pick === 'function');
  const pzCanRace = () => !!(PZ() && typeof PZ().race === 'function');
  const fmtMs = ms => { const t = Math.max(0, Math.round((+ms || 0) / 1000)); return `${Math.floor(t / 60)}:${String(t % 60).padStart(2, '0')}`; };
  const sayMs = ms => { const t = Math.max(0, Math.round((+ms || 0) / 1000)), m = Math.floor(t / 60), s = t % 60; return (m ? `${m} minute${m === 1 ? '' : 's'} ` : '') + `${s} second${s === 1 ? '' : 's'}`; };
  function pzInfo(kind, spec) {
    const k = pzKinds().find(x => x.id === kind) || {}, str = v => (typeof v === 'string' || typeof v === 'number') ? String(v) : '';
    let ch = '', d = '';
    try { const o = PZ().describe ? PZ().describe(spec) : null; if (typeof o === 'string') ch = o; else if (o) { ch = str(o.ch || o.chapter || o.label); d = str(o.d || o.detail); } } catch (e) {}
    if (!ch && k.chapter && spec) {
      const c = spec.chapter && typeof spec.chapter === 'object' ? (spec.chapter.title || spec.chapter.name) : (spec.chapterTitle || spec.title || spec.label || '');
      const sub = spec.subjectName || (spec.subject && typeof spec.subject === 'object' ? spec.subject.name : '');
      ch = [str(sub), str(c)].filter(Boolean).join(' · ');
    }
    if (!d && spec) {
      const sz = spec.n || spec.size, df = spec.diff || spec.difficulty || spec.level;
      d = [typeof sz === 'number' ? `${sz}×${sz}` : /\d/.test(str(sz)) ? str(sz) : '', str(df) && cap(str(df))].filter(Boolean).join(' · ');
    }
    return { e: String(k.e || '🧩').slice(0, 8), n: String(k.n || 'Puzzle').slice(0, 40), ch: ch.slice(0, 120), d: d.slice(0, 60) };
  }
  function pzLobbyHTML(r, H) {
    const cur = r.state && r.state.puzzle, kinds = H ? pzKinds() : [];
    const now = cur ? `<div class="lv-pzcur" role="status"><span class="lv-ge" aria-hidden="true">${E(cur.e)}</span><span><b>${E(cur.n)}</b>${cur.ch ? `<small>${E(cur.ch)}</small>` : ''}${cur.d ? `<small>${E(cur.d)}</small>` : ''}</span></div>`
      : `<p class="lv-mut" role="status">${H ? 'Choose the puzzle everyone will race on.' : '⏳ The host is choosing a puzzle…'}</p>`;
    if (!H) return now;
    const pick = !pzCanPick() ? '<p class="lv-mut">Puzzles are still loading on this phone. Reload the app if this stays.</p>'
      : `<h3 class="lv-h3">${cur ? 'Change the puzzle' : 'Pick a puzzle'}</h3><div class="lv-pzkinds" role="group" aria-label="Puzzle">${kinds.map(k => `<button type="button" class="lv-pzk${cur && cur.kind === k.id ? ' on' : ''}" data-pzk="${E(k.id)}" aria-pressed="${!!(cur && cur.kind === k.id)}"><span class="lv-ge" aria-hidden="true">${E(k.e || '🧩')}</span><b>${E(k.n || k.id)}</b><small>${k.chapter ? 'From a chapter' : E(k.d || 'Numbers')}</small></button>`).join('')}</div>`;
    return now + pick;
  }
  async function pickPuzzle(kind) {
    if (L.picking || !pzCanPick() || !host()) return;
    const code = L.code; L.picking = true; let spec = null;
    try { spec = await PZ().pick(kind); } catch (e) { console.warn('live: puzzle pick', e); }
    finally { L.picking = false; }
    if (!L.code || L.code !== code) return;
    if (!active()) enter(code);                              // the picker may have used its own screen
    if (!spec) return;
    try { spec = JSON.parse(JSON.stringify(spec)); } catch (e) { say('That puzzle could not be shared.'); return; }
    try {
      const inf = pzInfo(kind, spec), j = await rpc('puzzle_set', { p_code: code, p_kind: kind, p_spec: spec, p_info: inf });
      if (!j || !j.ok) { say(errText(j)); return; }
      S('unlock'); L.sig = ''; synced(); setTimeout(() => announce(`Puzzle chosen: ${inf.n}${inf.ch ? ', ' + inf.ch : ''}.`), 300);
    } catch (e) { say('No connection.'); }
  }
  function pzReset() { pzStop(); L.pzLive = {}; L.pzMine = 0; L.pzSeen = -1; }
  function pzStop() {
    const z = L.pz; if (!z) return; L.pz = null; clearTimeout(z.t);
    try { z.h && z.h.stop && z.h.stop(); } catch (e) {}
  }
  function pzLiveIn(pl) {                                    // a friend's progress over the live channel (the server copy follows by polling)
    if (!pl || typeof pl.u !== 'string' || !Number.isFinite(+pl.p)) return;
    L.pzLive[pl.u] = Math.max(0, Math.min(99, Math.round(+pl.p)));
    if (L.st && L.st.room.game === 'puzzle' && L.st.room.status === 'playing') pzStrip(L.st);
  }
  const pzPct = p => p.correct >= 1 ? 100 : Math.max(+p.answered || 0, L.pzLive[p.user_id] || 0, p.user_id === uid() ? L.pzMine : 0);
  function pzStrip(st) {
    const box = D.querySelector('#s-live .lv-scores'); if (!box) return;
    const r = st.room, sv = (r.state && r.state.solved) || [];
    const ms = p => { const x = sv.find(y => y.u === p.user_id); return x ? x.ms : p.total_ms; };
    const ps = st.players.slice().sort((a, b) => (b.correct >= 1) - (a.correct >= 1) || (a.correct >= 1 ? ms(a) - ms(b) : pzPct(b) - pzPct(a)) || a.seat - b.seat);
    const chip = p => { const done = p.correct >= 1, pc = pzPct(p);
      return `<span role="listitem" class="lv-sc lv-pzc${p.user_id === uid() ? ' me' : ''}${done ? ' done' : ''}${p.left ? ' left' : ''}"><span class="lv-dot" data-on="${p.user_id}"></span><span aria-hidden="true">${E(p.avatar)}</span> ${E(p.name)}${p.left ? ' (left)' : ''} <b>${done ? `✓ ${fmtMs(ms(p))}` : pc + '%'}</b><span class="sr-only">${done ? ', solved' : ' done'}</span><i class="lv-pzbar" aria-hidden="true" style="--p:${pc}%"></i></span>`; };
    const h = ps.map(chip).join('');
    box.setAttribute('role', 'list'); box.setAttribute('aria-label', 'Race progress');
    if (box.dataset.h !== h) { box.dataset.h = h; box.innerHTML = h; }
    paintOnline();
    // announce new solvers (not the first paint, not me — I hear my own result)
    if (L.pzSeen < 0) L.pzSeen = sv.length;
    else if (sv.length > L.pzSeen) { sv.slice(L.pzSeen).forEach(x => { if (x.u !== uid()) { announce(`${nameOf(x.u)} solved it in ${sayMs(x.ms)}!`); S('coin'); } }); L.pzSeen = sv.length; }
  }
  function puzzleStage(st) {
    const r = st.room, box = D.querySelector('#s-live .lv-stage'); if (!box) return;
    const now = nowS(), pre = !!(r.round_at && now < r.round_at), me = meP(), solved = !!(me && me.correct >= 1);
    const sig = JSON.stringify(['pz', r.code, r.round_at, pre, solved, !!L.qs]);
    if (sig === L.stageSig && (solved || pre || !L.qs || (L.pz && box.contains(L.pz.el)))) return; L.stageSig = sig;
    if (pre) { pzStop(); box.innerHTML = countdownHTML('🧩 Puzzle Race starts in…'); return; }
    if (solved) {
      pzStop();
      const sv = (r.state && r.state.solved) || [], i = sv.findIndex(x => x.u === uid()), x = sv[i] || { ms: me.total_ms };
      const place = i >= 0 ? ['🥇 You are first!', '🥈 You are second!', '🥉 You are third!'][i] || `You finished number ${i + 1}.` : '';
      box.innerHTML = `<div class="card lv-wait lv-pzdone"><div class="lv-big" aria-hidden="true">🏁</div><h2 class="lv-h2">Solved in ${fmtMs(x.ms)}!</h2><p class="sub">${place} Waiting for the others — the race ends when everyone has solved it or time runs out.</p></div>`;
      return;
    }
    if (!L.qs) { box.innerHTML = '<div class="card"><p class="sub">Loading the puzzle…</p></div>'; return; }
    if (!pzCanRace()) { box.innerHTML = '<div class="card"><p class="sub">This phone cannot show the puzzle yet. Reload the app (or update it) and open the room again — your place is kept.</p></div>'; return; }
    if (L.pz && box.contains(L.pz.el)) return;
    pzStop();
    box.innerHTML = '<div class="lv-pzhost" role="region" aria-label="Your puzzle"></div>';
    const el = box.firstElementChild, z = { el, h: null, last: 0, t: 0, pend: null, solving: false };
    L.pz = z;
    try {
      z.h = PZ().race(el, JSON.parse(JSON.stringify(L.qs)), {
        onProgress: o => pzProg(z, o), onSolved: o => pzSolved(z, o),
        onError: () => pzNote(z, '🙂 This puzzle could not be made on this phone. Reload the app and open the room again.'),
        onQuit: () => { const q = D.getElementById('lvQuit'); if (q) { q.dataset.sure = 1; q.textContent = 'Tap again to leave'; try { q.focus(); } catch (e) {} } say('To leave the race, tap “Tap again to leave”.'); } });
    } catch (e) { console.warn('live: puzzle race', e); el.innerHTML = '<div class="card"><p class="sub">This puzzle could not be opened on this phone.</p></div>'; }
    // a phone with other content / engine files would build a different puzzle, and its answers would not match the key
    try { if (z.h && z.h.ready && z.h.ready.then) z.h.ready.then(x => { if (x && x.ok && x.same === false) pzNote(z, '⚠️ This phone made a different puzzle from your friends’ (old app files). Reload the app to race fairly.'); }).catch(() => {}); } catch (e) {}
  }
  function pzNote(z, msg) {
    if (z !== L.pz || !z.el.isConnected) return;
    let n = z.el.parentNode.querySelector('.lv-pznote'); if (!n) { n = D.createElement('p'); n.className = 'lv-note lv-pznote'; n.setAttribute('role', 'status'); z.el.parentNode.insertBefore(n, z.el); }
    n.textContent = msg;
  }
  function pzProg(z, o) {
    if (z !== L.pz || !o) return;
    const done = Math.max(0, +o.done || 0), total = Math.max(1, +o.total || 1);
    L.pzMine = Math.min(99, Math.floor(100 * Math.min(done, total) / total));
    if (L.st) pzStrip(L.st);
    z.pend = [done, total];
    const send = () => {
      if (z !== L.pz || !z.pend) return; const [d, t] = z.pend; z.pend = null; z.last = Date.now();
      rpc('puzzle_progress', { p_code: L.code, p_done: d, p_total: t }).then(j => { if (j && j.ok && j.pct != null) broadcast('pz', { u: uid(), p: j.pct }); }).catch(() => {});
    };
    clearTimeout(z.t);
    const wait = 2500 - (Date.now() - z.last);
    if (wait <= 0) send(); else z.t = setTimeout(send, wait);
  }
  /* the puzzle reports a finished grid → the SERVER checks the answer (the only way to be marked solved) */
  async function pzSolved(z, o) {
    if (z !== L.pz || z.solving) return; z.solving = true; clearTimeout(z.t); z.pend = null;
    o = o || {};
    const body = { p_code: L.code, p_answer: o.answer == null ? null : o.answer, p_hints: Math.max(0, +o.hints || 0) | 0, p_mistakes: Math.max(0, +o.mistakes || 0) | 0 };
    pzNote(z, '⏳ Checking your answer…');
    for (let n = 0; n < 4; n++) {
      let j;
      try { j = await rpc('puzzle_solved', body); } catch (e) { await new Promise(res => setTimeout(res, 1500)); continue; }
      if (z !== L.pz) return;
      if (j && j.ok) { S('unlock'); announce(`Correct! Solved in ${sayMs(j.ms)}.${j.place ? ` You finished number ${j.place}.` : ''}`); L.stageSig = ''; synced(); return; }
      if (j && j.code === 'slow') { await new Promise(res => setTimeout(res, 3200)); continue; }
      const msg = j && j.code === 'late' ? '⏰ Time is up!' : errText(j);
      pzNote(z, msg); announce(msg); say(msg); S('hmm');
      z.solving = false; L.stageSig = ''; fetchState(); return;
    }
    z.solving = false; pzNote(z, 'No connection — your answer could not be checked yet.'); say('No connection — your answer could not be checked yet.');
  }
  function pzTick(r) {
    const now = nowS(), pre = !!(r.round_at && now < r.round_at), total = ((r.state && r.state.mins) || r.rounds || 8) * 60000, left = r.deadline ? Math.max(0, r.deadline - now) : total;
    const bar = D.querySelector('#s-live .lv-timer i'), sec = D.querySelector('#s-live .lv-secs'), tm = D.querySelector('#s-live .lv-timer');
    if (bar) bar.style.transform = `scaleX(${pre ? 1 : Math.min(1, left / total)})`;
    if (sec) sec.textContent = pre ? `Get ready… ${Math.ceil((r.round_at - now) / 1000)}` : left > 0 ? `${fmtMs(left)} left` : '⏰ Time is up!';
    if (tm) tm.classList.toggle('hot', !pre && left <= 30000);
    const cd = D.querySelector('#s-live .lv-count'); if (cd) { if (pre) cd.textContent = Math.max(1, Math.ceil((r.round_at - now) / 1000)); else if (cd.dataset.go !== '1') { cd.dataset.go = '1'; L.stageSig = ''; render(); return; } }
    // finish the race once it is over: deadline passed, or every active player has solved it (any member may ask)
    const ps = actives(), all = ps.length > 0 && ps.every(p => p.correct >= 1);
    if (!(all || (r.deadline && now >= r.deadline + 1600))) return;
    const last = L.advAt.pz || 0; if (Date.now() - last < 1800) return; L.advAt.pz = Date.now();
    rpc('puzzle_advance', { p_code: L.code }).then(j => { if (j && j.changed) synced(); else fetchState(); }).catch(() => {});
  }

  /* ---------- results ---------- */
  function results(st) {
    const r = st.room, me = uid(), sig = JSON.stringify(['res', r.step, r.host_id]);
    if (sig === L.sig) return; L.sig = sig; L.stageSig = ''; L.sb = null;
    const ps = st.players.slice().sort((a, b) => b.score - a.score || b.correct - a.correct || a.total_ms - b.total_ms);
    const teams = r.mode === 'teams', wt = r.state.win_team, t = r.state.teams || teamTotals();
    const top = ps.filter(p => !p.left), best = top.length ? top[0].score : 0;
    const winners = teams ? (wt == null ? [] : st.players.filter(p => p.team === wt && !p.left)) : top.filter(p => p.score === best);
    const iWon = winners.some(p => p.user_id === me), mine = st.players.find(p => p.user_id === me) || {};
    const title = teams ? (wt == null ? "🤝 It's a draw!" : `${TEAMS[wt].e} ${TEAMS[wt].n} wins!`) : iWon ? (winners.length > 1 ? '🤝 You share the win!' : '🏆 You won!') : `🏆 ${E(winners.map(p => p.name).join(' & ') || '—')} wins!`;
    // badges + XP once per finished game
    const key = r.code + ':' + r.step, done = (ST.liveDone = Array.isArray(ST.liveDone) ? ST.liveDone : []), fresh = !done.includes(key);
    const earned = [];
    if (fresh) {
      done.push(key); if (done.length > 30) done.splice(0, done.length - 30);
      ST.badges = ST.badges || {};
      const give = id => { if (!ST.badges[id]) { ST.badges[id] = (typeof today === 'function' ? today() : new Date().toISOString().slice(0, 10)); earned.push(id); } };
      if (iWon && L.wasLast && top.length >= 2) give('lvComeback');
      if (teams && iWon) { const mates = st.players.filter(p => p.team === wt); if (Math.max(...mates.map(p => p.score)) === mine.score) give('lvCaptain'); }
      if (iWon && (r.game === 'quiz' || r.game === 'duel')) give('lvRacer');
      try { save(); } catch (e) {}
      try { addXP(10 + (iWon ? 15 : 0), iWon ? 'Game room win!' : 'Game room played'); } catch (e) {}
      S(iWon ? 'unlock' : 'coin');
    }
    const medal = i => ['🥇', '🥈', '🥉'][i] || String(i + 1);
    const row = (p, i) => `<li class="${p.user_id === me ? 'me' : ''}${p.left ? ' left' : ''}"><span class="lv-rk">${medal(i)}</span><span class="lv-av" aria-hidden="true">${E(p.avatar)}</span><span class="lv-nm">${E(p.name)}${p.user_id === me ? ' (you)' : ''}${p.left ? ' (left)' : ''}${teams ? ` <small>${TEAMS[p.team || 0].e}</small>` : ''}</span><span class="lv-pts">${r.game === 'puzzle' ? (p.correct >= 1 ? `⏱ ${fmtMs(p.total_ms)}<small>${p.score} pts</small>` : `${p.answered}% done<small>not finished</small>`) : `${r.game === 'snakes' ? '📍 ' + p.pos : p.score + ' pts'}<small>${p.correct} right</small>`}</span></li>`;
    const conf = iWon ? `<div class="lv-conf" aria-hidden="true">${Array.from({ length: 18 }, (_, j) => `<span style="left:${(j * 5.7 + 2) % 100}%;animation-delay:${(j % 6) * .15}s">${['🎉', '⭐', '✨', '🎊'][j % 4]}</span>`).join('')}</div>` : '';
    const newB = earned.map(id => BADGES.find(b => b[0] === id)).filter(Boolean);
    screen().innerHTML = `<div class="lv-root lv-res"><div class="card lv-rescard">${conf}<div class="lv-res-e" aria-hidden="true">${GAMES[r.game].e}</div><h1 class="lv-h1">${title}</h1>
      ${r.game === 'puzzle' && r.state.puzzle ? `<p class="sub">${E(r.state.puzzle.e)} ${E(r.state.puzzle.n)}${r.state.puzzle.ch ? ' · ' + E(r.state.puzzle.ch) : ''}${(r.state.solved || []).length ? '' : ' · nobody finished in time'}</p>` : ''}
      ${teams ? `<div class="lv-tres">${TEAMS.map((tm, i) => `<div class="t${i}${wt === i ? ' win' : ''}"><b>${tm.e} ${tm.n}</b><span>${t[i] || 0}</span></div>`).join('')}</div>` : ''}
      <ol class="lv-rank">${ps.map(row).join('')}</ol>
      ${fresh ? `<div class="arc-xp">+${10 + (iWon ? 15 : 0)} ⭐ XP</div>` : ''}
      ${newB.length ? `<div class="lv-newb" role="status">${newB.map(b => `<div><b aria-hidden="true">${b[1]}</b> New badge: <b>${b[2]}</b></div>`).join('')}</div>` : ''}
      ${host() ? '<button class="btn mint" id="lvAgain">🔁 Play again with this room</button>' : '<p class="lv-note">The host can start another game in this room.</p>'}
      <div style="height:8px"></div><button class="btn ghost" id="lvHome">🎮 Game Rooms</button><div style="height:8px"></div><button class="btn ghost" id="lvLeave2">Leave room</button></div>
      ${emojiBar()}<div class="lv-live sr-only" aria-live="polite"></div></div>`;
    wireEmoji(screen());
    const ag = $('#lvAgain'); if (ag) ag.onclick = async () => { try { const j = await rpc('rematch', { p_code: L.code }); if (j && !j.ok) say(errText(j)); S('tap'); L.sig = ''; synced(); } catch (e) { say('No connection.'); } };
    $('#lvHome').onclick = () => { const c = L.code; suspend(); L.code = null; L.st = null; lset('sv_live_room', { code: c, at: Date.now() }); home(); };
    $('#lvLeave2').onclick = leave;
    announce(title.replace(/<[^>]+>/g, ''));
  }

  /* ================= voice text for Listen mode (js/a11y.js) ================= */
  function speech(root, ch, list) {
    const t = el => (el ? el.textContent.replace(/\s+/g, ' ').trim() : '');
    const st = L.st;
    if (root.querySelector('.lv-home')) return `Game Rooms. ${t(root.querySelector('.lv-locked')) || 'Join a room with a code from your friend, or start a room and share its code.'}`;
    if (!st) return 'Opening the game room.';
    const r = st.room;
    if (r.status === 'lobby') return `Game room ${r.code.split('').join(' ')}. ${GAMES[r.game].n}. ${st.players.filter(p => !p.left).length} players: ${st.players.filter(p => !p.left).map(p => p.name + (p.ready || p.user_id === r.host_id ? ', ready' : ', not ready')).join('; ')}. ${t(root.querySelector('.lv-hint'))}`;
    if (r.status === 'finished') return `${t(root.querySelector('.lv-rescard h1'))}. ${[...root.querySelectorAll('.lv-rank li')].map(li => t(li)).join('. ')}`;
    const qt = t(root.querySelector('.lv-qt')), opts = ch && ch.length && ch[0].matches('.opt') ? list(ch, 'Option') + ' Say an option number.' : '';
    const sec = t(root.querySelector('.lv-secs'));
    if (r.game === 'snakes') { const me = meP(); return `${t(root.querySelector('.lv-slog'))} You are on square ${me ? me.pos : 1} of 100. ${t(root.querySelector('.lv-sltitle'))} ${qt} ${opts} ${root.querySelector('#lvRoll') ? 'Your turn: say roll, or press the roll button.' : t(root.querySelector('.lv-slact'))} ${sec}`; }
    if (r.game === 'puzzle') return `Puzzle Race. ${t(root.querySelector('.lv-round'))}. ${[...root.querySelectorAll('.lv-pzc')].map(li => t(li)).join('; ')}. ${t(root.querySelector('.lv-pzdone')) || t(root.querySelector('.lv-cd'))} ${sec}`;
    if (r.game === 'buzzer') return `${qt} ${opts || t(root.querySelector('.lv-bmsg'))} ${root.querySelector('#lvBuzz:not([disabled])') ? 'Press the buzz button.' : ''} ${sec}`;
    return `${t(root.querySelector('.lv-round'))}. ${t(root.querySelector('.lv-wait'))} ${qt} ${opts} ${t(root.querySelector('.lv-note'))} ${sec}`;
  }

  /* ================= entry: the 🎮 Play hub (js/playhub.js) opens Game Rooms through window.Live ================= */
  const resume = () => { const s = lget('sv_live_room', null); return s && s.code && Date.now() - s.at < 2 * 3600e3 ? s.code : null; };
  /* Live.open({ game }) → Game Rooms home with that game preselected in the "Start a room" picker; Live.open() = as before */
  function open(o) {
    const g = o && o.game;
    if (g && GAMES[g]) {
      const was = draft.game; draft.game = g;
      if (g === 'duel') draft.mode = 'duel'; else if (draft.mode === 'duel' && was !== g) draft.mode = 'ffa';
      if (g === 'puzzle' && was !== 'puzzle') draft.rounds = 8;
      normDraft(draft);
    }
    return home();
  }

  /* ================= links: ?room=CODE ================= */
  (function catchLink() {
    try {
      const u = new URL(location.href), c = (u.searchParams.get('room') || '').toUpperCase().replace(/[^A-Z]/g, '');
      if (!u.searchParams.has('room')) return;
      u.searchParams.delete('room'); history.replaceState(history.state, '', u.pathname + (u.search || '') + u.hash);
      if (/^[A-Z]{6}$/.test(c)) sessionStorage.setItem('sv_room_join', JSON.stringify({ c, at: Date.now() }));
    } catch (e) {}
  })();
  function pendingJoin() {
    let p = null; try { p = JSON.parse(sessionStorage.getItem('sv_room_join') || 'null'); } catch (e) {}
    if (!p) return;
    if (Date.now() - p.at > 30 * 60e3) { sessionStorage.removeItem('sv_room_join'); return; }
    const C = window.Cloud; if (!C || !C.signedIn() || !STx() || !STx().profile) return;
    if (C.isParent && C.isParent()) { sessionStorage.removeItem('sv_room_join'); say('Game Rooms are for students.'); return; }
    if (!uid()) return;
    const a = D.querySelector('.screen.active'); if (!a || a.id === 's-onboard') return;
    if (localStorage.getItem('sv_access') == null && Date.now() - p.at < 8000) return;    // wait briefly for the plan check
    sessionStorage.removeItem('sv_room_join');
    join(p.c);
  }

  /* ================= styles ================= */
  function style() {
    if (D.getElementById('lvCss')) return;
    const c = D.createElement('style'); c.id = 'lvCss';
    c.textContent = `
.lv-root{position:relative}.lv-root .card{color:var(--ink)}
.lv-h1{font-family:'Baloo 2',Nunito,sans-serif;font-size:26px;line-height:1.1;margin:0 0 4px}.lv-h2{font-family:'Baloo 2',Nunito,sans-serif;font-size:21px;margin:0 0 6px}.lv-h2 small{font-size:14px;color:var(--muted)}
.lv-h3{font-size:14px;font-weight:800;margin:12px 0 6px;color:#3b4064}
.lv-mut{color:var(--muted);font-size:13.5px;margin:6px 0 0}.lv-err{color:#b42318;font-weight:700;font-size:14px;min-height:1px;margin:6px 0 0}
.lv-hero{display:flex;gap:12px;align-items:center}.lv-hero-e{font-size:46px;line-height:1}
.lv-lab{display:block;font-weight:800;font-size:14px;margin:4px 0 6px}
.lv-joinrow{display:flex;gap:8px}.lv-joinrow .btn{width:auto;flex:none;min-height:48px}
.lv-in{flex:1;min-width:0;min-height:48px;border:2px solid #d3d7ef;border-radius:14px;padding:8px 12px;font:800 22px 'Baloo 2',monospace;letter-spacing:6px;text-transform:uppercase;color:var(--ink);background:#fff}
.lv-in:focus{outline:3px solid #7646ea;outline-offset:1px}
.lv-games{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.lv-game{display:flex;flex-direction:column;align-items:flex-start;gap:2px;text-align:left;border:2px solid #e3e6f6;background:#fff;border-radius:16px;padding:10px;min-height:44px;cursor:pointer;font-family:inherit;color:var(--ink)}
.lv-game.on{border-color:#7646ea;background:#f3efff;box-shadow:0 0 0 2px #7646ea33}.lv-ge{font-size:26px;line-height:1}.lv-game b{font-size:14.5px}.lv-game small{font-size:12px;color:var(--muted);line-height:1.3}
.lv-chips{display:flex;flex-wrap:wrap;gap:8px}
.lv-chip{min-height:44px;min-width:56px;padding:8px 14px;border-radius:999px;border:2px solid #e3e6f6;background:#fff;font:800 14px Nunito,system-ui,sans-serif;color:var(--ink);cursor:pointer}
.lv-chip.on{border-color:#7646ea;background:#7646ea;color:#fff}
.lv-pick{margin-bottom:12px}
.lv-badges{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.lv-bdg{text-align:center;background:#f6f7fd;border-radius:14px;padding:8px 4px;opacity:.6}.lv-bdg.on{opacity:1;background:#fff8dc}.lv-bdg b{font-size:28px;display:block}.lv-bdg span{font-weight:800;font-size:13px;display:block}.lv-bdg small{font-size:11.5px;color:var(--muted)}
.lv-lb,.lv-rank{list-style:none;margin:0;padding:0}
.lv-lb li,.lv-rank li{display:flex;align-items:center;gap:8px;padding:8px 6px;border-radius:12px}.lv-lb li.me,.lv-rank li.me{background:#f3efff}.lv-rank li.left{opacity:.55}
.lv-rk{width:28px;text-align:center;font-weight:800}.lv-av{font-size:24px;line-height:1}.lv-nm{flex:1;min-width:0;font-weight:800}.lv-nm small{display:block;font-weight:600;color:var(--muted);font-size:12px}
.lv-wn{font-size:12.5px;color:var(--muted);font-weight:700;text-align:right}.lv-pts{font-weight:800;text-align:right}.lv-pts small{display:block;font-size:11.5px;color:var(--muted);font-weight:700}
.lv-top{display:flex;align-items:center;gap:8px;color:#fff;margin:2px 0 10px;flex-wrap:wrap}.lv-top b{font-family:'Baloo 2',Nunito,sans-serif;font-size:19px;flex:1;min-width:0}
.lv-round{font-weight:800;font-size:13px;background:rgba(255,255,255,.16);border-radius:999px;padding:4px 10px}
.lv-net{font-size:12px;font-weight:800;background:rgba(255,255,255,.14);border-radius:999px;padding:4px 9px}.lv-net.bad{background:#fde68a;color:#5b3b00}
.lv-codecard{text-align:center}.lv-k{font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.6px;color:var(--muted)}
.lv-code{font:800 40px/1.1 'Baloo 2',monospace;letter-spacing:8px;margin:2px 0 10px;color:#4c1d95}
.lv-share{display:flex;gap:8px}.lv-share .btn{flex:1;min-height:48px;display:flex;align-items:center;justify-content:center;text-decoration:none;font-size:15px;padding:10px 8px}
.lv-wa{background:#25d366!important;box-shadow:0 4px 0 #128c4a!important;color:#06351b!important}
.lv-plist{list-style:none;margin:0;padding:0}
.lv-p{display:flex;align-items:center;gap:8px;padding:8px 4px;border-bottom:1px solid #eef0fb;position:relative}.lv-p:last-child{border-bottom:0}
.lv-dot{width:10px;height:10px;border-radius:50%;background:#22c55e;flex:none;box-shadow:0 0 0 2px #fff}.lv-dot.off{background:#9ca3af}
.lv-host{font-size:11.5px;background:#fff3c4;color:#6b4b00;border-radius:999px;padding:1px 7px;font-weight:800;white-space:nowrap}
.lv-rdy{font-size:12px;font-weight:800;border-radius:999px;padding:4px 9px;background:#eef0fb;color:#5f6485;white-space:nowrap}.lv-rdy.on{background:#dcfce7;color:#166534}
.lv-kick{min-width:44px;min-height:44px;border-radius:12px;border:2px solid #fecaca;background:#fff;color:#b42318;font-weight:800;cursor:pointer;font-family:inherit}.lv-kick.sure{background:#b42318;color:#fff;border-color:#b42318}
.lv-teams{display:grid;grid-template-columns:1fr;gap:8px;margin-bottom:10px}.lv-team{border-radius:14px;padding:4px 8px;background:#eff6ff}.lv-team.t1{background:#fff7ed}
.lv-actions{display:flex;flex-direction:column;gap:8px;margin-bottom:12px}.lv-actions .btn[aria-disabled=true]{opacity:.6}
.lv-hint,.lv-note{color:#fff;font-weight:700;font-size:14px;text-align:center;margin:0}.card .lv-note{color:#3b4064;margin-top:8px}
.lv-set summary{cursor:pointer;font-weight:800;min-height:44px;display:flex;align-items:center;color:#5b33c9}
.lv-emo{display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin:6px 0}
.lv-emob{min-width:44px;min-height:44px;border-radius:50%;border:0;background:rgba(255,255,255,.16);font-size:22px;cursor:pointer}
.lv-floats{position:fixed;left:0;right:0;bottom:90px;height:0;pointer-events:none;z-index:50}
.lv-float{position:absolute;bottom:0;display:flex;flex-direction:column;align-items:center;animation:lvUp 2.6s ease-out forwards}.lv-float b{font-size:34px}.lv-float small{background:rgba(0,0,0,.6);color:#fff;border-radius:999px;padding:1px 8px;font-size:12px;font-weight:800}
@keyframes lvUp{0%{transform:translateY(0) scale(.6);opacity:0}15%{opacity:1;transform:translateY(-30px) scale(1.1)}100%{transform:translateY(-220px) scale(1);opacity:0}}
.lv-timer{position:relative;height:26px;border-radius:999px;background:rgba(255,255,255,.18);overflow:hidden;margin-bottom:10px}
.lv-timer i{position:absolute;inset:0;background:linear-gradient(90deg,#2ed3a5,#60a5fa);transform-origin:left;transition:transform .25s linear}.lv-timer.hot i{background:linear-gradient(90deg,#f97316,#ef4444)}
.lv-secs{position:relative;display:block;text-align:center;font-weight:800;font-size:13.5px;line-height:26px;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.5)}
.lv-scores{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.lv-sc{display:inline-flex;align-items:center;gap:4px;background:rgba(255,255,255,.92);color:var(--ink);border-radius:999px;padding:5px 10px;font-weight:700;font-size:13px}
.lv-sc.me{box-shadow:0 0 0 2px #2ed3a5}.lv-sc.turn{background:#fff3c4;box-shadow:0 0 0 3px #ffc93c}.lv-sc.left{opacity:.5}.lv-sc i{font-style:normal;color:#16a34a;font-weight:800}
.lv-tsc{flex:1 1 45%;background:rgba(255,255,255,.1);border-radius:14px;padding:6px}.lv-tsc>b{display:block;color:#fff;font-size:14px;margin-bottom:4px}.lv-tsc>div{display:flex;flex-wrap:wrap;gap:4px}
.lv-q .lv-src{font-size:12px;font-weight:800;color:#6d28d9;margin-bottom:4px}.lv-qt{font-size:17px;font-weight:800;line-height:1.35}
.lv-opt{display:flex;gap:10px;align-items:center;min-height:48px}.lv-opt.picked{border-color:#7646ea}.lv-opt.wrong{border-color:var(--coral);background:#ffecec}
.lv-l{flex:none;width:28px;height:28px;border-radius:50%;background:#eef0fb;display:grid;place-items:center;font-weight:800;font-size:13px}
.lv-exp{border-radius:14px;padding:10px 12px;margin-top:10px;font-size:14px}.lv-exp.good{background:#e3fbf3}.lv-exp.bad{background:#fff1f0}.lv-exp p{margin-top:4px;color:#3b4064}
.lv-olist{margin:8px 0 0 22px;font-weight:700;color:#3b4064}.lv-olist li{margin:3px 0}
.lv-buzz{display:block;width:100%;min-height:96px;border:0;border-radius:24px;background:radial-gradient(circle at 50% 35%,#ff7a7a,#dc2626);color:#fff;font-family:'Baloo 2',Nunito,sans-serif;font-size:34px;font-weight:800;box-shadow:0 8px 0 #991b1b;cursor:pointer;margin:6px 0 12px}
.lv-buzz:active{transform:translateY(4px);box-shadow:0 4px 0 #991b1b}.lv-buzz:disabled{opacity:.45;cursor:default}
.lv-cd{text-align:center}.lv-count{font-family:'Baloo 2',Nunito,sans-serif;font-size:72px;line-height:1;font-weight:800;color:#7646ea;animation:pop .5s ease}
.lv-wait{text-align:center}.lv-big{font-size:56px}
.lv-sldice{display:flex;align-items:center;gap:10px;margin:10px 0 4px}.lv-slact{flex:1}.lv-slact .btn{min-height:52px}.lv-slact .lv-note{text-align:left}
.lv-sltitle{font-family:'Baloo 2',Nunito,sans-serif;font-weight:800;font-size:17px;color:#fff;margin:6px 0}
.lv-gfoot{display:flex;flex-direction:column;align-items:center;gap:4px;margin-top:8px}.lv-qrow{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.lv-quit{min-height:44px;border:0;border-radius:12px;background:rgba(255,255,255,.12);color:#fff;font:800 13px Nunito,system-ui,sans-serif;padding:8px 14px;cursor:pointer}
.lv-rescard{text-align:center;overflow:hidden;position:relative}.lv-res-e{font-size:54px;line-height:1.1}
.lv-rank{text-align:left;margin:10px 0}
.lv-tres{display:flex;gap:8px;margin:8px 0}.lv-tres>div{flex:1;border-radius:14px;padding:8px;background:#eff6ff}.lv-tres>div.t1{background:#fff7ed}.lv-tres>div.win{box-shadow:0 0 0 3px #ffc93c}.lv-tres b{display:block;font-size:13px}.lv-tres span{font-family:'Baloo 2',Nunito,sans-serif;font-size:26px;font-weight:800}
.lv-newb{background:#fff8dc;border-radius:14px;padding:8px;margin:8px 0;font-size:14.5px}
.lv-conf{position:absolute;inset:0;pointer-events:none}.lv-conf span{position:absolute;top:-30px;font-size:20px;animation:conf 2.2s ease-in forwards}
html.sv-rm .lv-conf,html.sv-rm .lv-float{display:none}
.lv-locked{text-align:center}.lv-lock-e{font-size:44px}
.lv-rejoin{display:flex;flex-direction:column;gap:8px}
.lv-pzcur{display:flex;gap:10px;align-items:center;background:#f3efff;border-radius:14px;padding:8px 10px;margin:8px 0}.lv-pzcur b{display:block}.lv-pzcur small{display:block;color:var(--muted);font-size:12.5px;font-weight:700}
.lv-pzkinds{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.lv-pzk{display:flex;flex-direction:column;align-items:center;gap:2px;text-align:center;border:2px solid #e3e6f6;background:#fff;border-radius:14px;padding:8px 4px;min-height:44px;cursor:pointer;font-family:inherit;color:var(--ink)}
.lv-pzk.on{border-color:#7646ea;background:#f3efff}.lv-pzk b{font-size:13px}.lv-pzk small{font-size:11px;color:var(--muted)}
.lv-pzc{position:relative;overflow:hidden;padding-bottom:7px}.lv-pzbar{position:absolute;left:0;bottom:0;height:3px;width:var(--p,0%);background:#7646ea;transition:width .4s}.lv-pzc.done{background:#dcfce7}.lv-pzc.done .lv-pzbar{background:#16a34a}
.lv-pzhost{margin-bottom:6px}
html[data-age=pro]:not(.sv-hc) .lv-pzk.on,html[data-age=pro]:not(.sv-hc) .lv-pzcur{border-color:#C9A76A;background:#F4EAD8}
.lv-tile{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:0;cursor:pointer;font-family:inherit;color:var(--ink);background:linear-gradient(135deg,#fff,#f3efff);min-height:64px}
.lv-tile-e{font-size:34px;line-height:1}.lv-tile-t{flex:1;min-width:0}.lv-tile-t b{display:block;font-family:'Baloo 2',Nunito,sans-serif;font-size:18px}.lv-tile-t small{color:var(--muted);font-size:13px}.lv-tile-go{font-size:28px;color:#7646ea;font-weight:800}
.ca-hubs .lv-tile{margin-bottom:10px}
html[data-age=pro]:not(.sv-hc) #s-live .card,html[data-age=pro]:not(.sv-hc) .lv-tile.dark{background:#FFFDF8}
html[data-age=pro]:not(.sv-hc) .lv-game.on,html[data-age=pro]:not(.sv-hc) .lv-chip.on{border-color:#C9A76A}html[data-age=pro]:not(.sv-hc) .lv-chip.on{background:#15161C;color:#F4EAD8}
html[data-age=pro]:not(.sv-hc) .lv-game.on{background:#F4EAD8;box-shadow:none}html[data-age=pro]:not(.sv-hc) .lv-code{color:#5B0F1B}html[data-age=pro]:not(.sv-hc) .lv-tile-go{color:#C9A76A}
html[data-age=pro]:not(.sv-hc) .lv-q .lv-src{color:#74561F}html[data-age=pro]:not(.sv-hc) .lv-count{color:#74561F}
@media (max-width:380px){.lv-games{grid-template-columns:1fr}.lv-code{font-size:34px;letter-spacing:6px}}`;
    (D.head || D.documentElement).appendChild(c);
  }

  /* ================= start ================= */
  function boot() {
    style();
    setInterval(pendingJoin, 1000); setTimeout(pendingJoin, 600);
  }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', boot) : boot();
  if (window.Nav) home = Nav.route('live', home);
  window.Live = { open, join, resume, speech, _L: L, _pick: pickQuestions, _courseName: courseName };
})();
