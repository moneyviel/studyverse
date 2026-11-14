/* ================= 🎮 Play hub (js/playhub.js) =================
   One place for every game and puzzle, in the Practice tab (school and CA). Every game can be played
   🙋 alone or 👫 with friends:
     Live games (js/live.js Game Rooms)   alone = the closest solo game in the Arcade (js/arcade.js), vs the clock / 🐥 Gappu
       🏁 Quiz Race      → 🎯 Quiz Show          🔔 Buzzer Round → ⚡ Lightning Round (CA: 🏰 Boss Battle)
       🐍 Snakes Battle  → 🐍 Snakes vs Gappu    🏃 Team Relay   → 🏰 Boss Battle      ⚡ Speed Duel (CA) → ⚡ Speed drill
     Puzzles (js/puzzles.js)              alone = Puzzles.quick(kind)   friends = 🧩 Puzzle Race room (Live.open({ game: 'puzzle', kind }))
   CA students get the Arcade with their own CA MCQs (scope.pool), so Snakes vs Gappu etc. work for them too.
   Also draws the two Practice tiles: 🎮 Play and 🧮 Calculator Academy (moved here from World / CA home / Me).
   window.PlayHub = { open } */
(function () {
  'use strict';
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const STx = () => { try { return ST; } catch (e) { return null; } };
  const isCA = () => { const s = STx(); return !!(s && s.profile && s.profile.course === 'ca'); };
  const isJEE = () => { try { return !isCA() && !!(window.Jee && Jee.active && Jee.active()); } catch (e) { return false; } };
  const isParent = () => { try { return !!(window.Cloud && Cloud.isParent && Cloud.isParent()); } catch (e) { return false; } };

  const LIVE = [
    { id: 'quiz', e: '🏁', n: 'Quiz Race', d: 'Same question for everyone. Right and fast wins.', solo: 'quizshow', soloN: 'Quiz Show: climb the coin ladder' },
    { id: 'buzzer', e: '🔔', n: 'Buzzer Round', d: 'First to buzz gets to answer.', solo: 'lightning', soloCA: 'boss', soloN: 'Lightning Round: 60 fast facts' },
    { id: 'snakes', e: '🐍', n: 'Snakes & Ladders', d: 'Race to 100. Answer right on a ladder to climb.', solo: 'snakes', soloN: 'Race 🐥 Gappu to 100' },
    { id: 'relay', e: '🏃', n: 'Team Relay', d: 'Teammates take turns. Team total wins.', solo: 'boss', soloN: 'Boss Battle: your streaks hit the boss' },
    { id: 'duel', e: '⚡', n: 'Speed Duel', d: 'CA exam pace: 72 seconds a question.', ca: true, soloN: 'Speed drill on your slow questions' }];
  const MORE = ['memory', 'storm', 'odd', 'chain'];       // solo-only Arcade games (school content)
  const PZ_FALLBACK = [{ id: 'sdk', e: '🔢', n: 'Sudoku', d: 'Fill the grid: every row, column and box once.' }, { id: 'kak', e: '➕', n: 'Kakuro', d: 'Number crossword: make the sums.' },
    { id: 'xw', e: '📝', n: 'Crossword', d: 'Your chapter’s key words.', chapter: true }, { id: 'ws', e: '🔎', n: 'Word search', d: 'Find the chapter’s words.', chapter: true },
    { id: 'ana', e: '🔤', n: 'Anagram', d: 'Unscramble the chapter’s words.', chapter: true }, { id: 'csdk', e: '🧠', n: 'Concept sudoku', d: 'Sudoku with chapter words.', chapter: true }];
  const pzKinds = () => { try { const k = window.Puzzles && Puzzles.kinds && Puzzles.kinds(); if (Array.isArray(k) && k.length) return k; } catch (e) {} return PZ_FALLBACK; };
  const resume = () => { try { if (window.Live && Live.resume) return Live.resume(); } catch (e) {} return null; };

  /* ---------- screen ---------- */
  function screen() {
    let s = D.getElementById('s-play');
    if (!s) { $1('main').insertAdjacentHTML('beforeend', '<section class="screen" id="s-play"></section>'); s = D.getElementById('s-play'); }
    return s;
  }
  const backToPractice = () => { if (isCA() && window.CaTools) CaTools.practiceHub(); else practiceScreen(); };

  function open() {
    style();
    const el = screen(); show('play', 'practice'); window.scrollTo(0, 0);
    const ca = isCA(), back = resume();
    const live = LIVE.filter(g => !g.ca || ca);
    const row = (e, n, d, alone, friends, extra) => `<div class="ph-g"><span class="ph-ge" aria-hidden="true">${e}</span><div class="ph-gt"><b>${E(n)}</b><small>${E(d)}</small>${extra || ''}</div>
      <div class="ph-gb">${alone ? `<button class="ph-b solo" type="button" ${alone} aria-label="${E(n)}: play alone"><span aria-hidden="true">🙋</span> Alone</button>` : ''}${friends ? `<button class="ph-b fr" type="button" ${friends} aria-label="${E(n)}: play with friends"><span aria-hidden="true">👫</span> Friends</button>` : ''}</div></div>`;
    el.innerHTML = `<div class="ph-root${ca ? ' ph-ca' : ''}"><button class="back" id="phBack">← Practice</button>
      <div class="hello ph-hello" role="heading" aria-level="1"><span aria-hidden="true">🎮</span> Play <small>Games and puzzles · alone or with friends</small></div>
      ${window.DesiGames && DesiGames.tileHTML ? DesiGames.tileHTML() : ''}
      ${savedHTML()}${back ? `<button class="card ph-resume" type="button" id="phResume"><span aria-hidden="true">🔁</span> <b>Back to your room ${E(back)}</b><span class="ph-chev" aria-hidden="true">›</span></button>` : ''}
      <div class="card ph-friends"><h3><span aria-hidden="true">👫</span> Play with friends</h3><p class="sub">Make a room and share its code, or type a friend’s code.</p>
        <div class="ph-join"><input id="phCode" inputmode="text" autocomplete="off" maxlength="8" placeholder="Room code" aria-label="Room code"><button class="btn" type="button" id="phJoin">Join</button></div>
        <button class="btn ghost" type="button" id="phMake">➕ Make a room</button></div>
      <button class="card ph-resume ph-fam" type="button" id="phFam"><span aria-hidden="true">👨‍👩‍👧</span> <b>Play with family<small>Mum, Dad, both parents or a guardian · one phone, one laptop or each on your own</small></b><span class="ph-chev" aria-hidden="true">›</span></button>
      <div class="card"><h3><span aria-hidden="true">🎲</span> Games</h3>${live.map(g => row(g.e, g.n, g.d, `data-solo="${g.id}"`, `data-fr="${g.id}"`, `<small class="ph-alone">🙋 Alone: ${E(g.soloN)}</small>`)).join('')}</div>
      <div class="card"><h3><span aria-hidden="true">🧩</span> Puzzles</h3>
        ${row('📅', 'Daily puzzle', 'A new puzzle every day from your chapter. Keep your puzzle streak!', 'data-daily="1"', '')}
        ${pzKinds().map(k => row(k.e, k.n, k.d + (k.chapter ? ' Pick any chapter.' : ''), `data-pz="${E(k.id)}"`, `data-pzf="${E(k.id)}"`)).join('')}
        <button class="btn ghost ph-all" type="button" id="phPzHub">🏅 Puzzle badges & best times</button></div>
      ${ca || isJEE() ? '' : `<div class="card"><h3><span aria-hidden="true">🕹️</span> More solo games</h3><div class="ph-more">${MORE.map(id => { const g = arcGame(id); return g ? `<button class="ph-m" type="button" data-arc="${id}"><span aria-hidden="true">${g.e}</span><b>${E(g.n)}</b><small>${E(g.d)}</small></button>` : ''; }).join('')}</div>
        <button class="btn ghost ph-all" type="button" id="phArc">🕹️ All arcade games</button></div>`}
      <div class="card ph-calc"><h3><span aria-hidden="true">🧮</span> Calculator Academy</h3><p class="sub">Free bonus course: learn every key with real missions.</p><button class="btn ghost" type="button" id="phCalc">Open Calculator Academy ▶</button></div></div>`;
    $1('#phBack').onclick = () => { S('tap'); backToPractice(); };
    { const dg = $1('#dgTile', el); if (dg) dg.onclick = () => { S('open'); DesiGames.open({ back: open }); }; }   // 🪔 owner preview games (js/desi-games.js)
    wireSaved(el);
    if (back) $1('#phResume').onclick = () => { S('open'); Live.join(back); };
    $1('#phMake').onclick = () => { S('open'); liveOpen(); };
    $1('#phFam').onclick = () => { S('open'); family(open); };
    const join = () => { const c = ($1('#phCode').value || '').trim().toUpperCase(); if (!c) { $1('#phCode').focus(); return; } S('open'); if (window.Live) Live.join(c); };
    $1('#phJoin').onclick = join; $1('#phCode').onkeydown = e => { if (e.key === 'Enter') join(); };
    el.querySelectorAll('[data-fr]').forEach(b => b.onclick = () => { S('open'); liveOpen({ game: b.dataset.fr }); });
    el.querySelectorAll('[data-solo]').forEach(b => b.onclick = () => { S('open'); solo(b.dataset.solo); });
    el.querySelectorAll('[data-pz]').forEach(b => b.onclick = () => { S('open'); if (window.Puzzles && Puzzles.quick) Puzzles.quick(b.dataset.pz, { from: 'play' }); else if (window.Puzzles) Puzzles.hub({ from: 'play' }); });
    el.querySelectorAll('[data-pzf]').forEach(b => b.onclick = () => { S('open'); liveOpen({ game: 'puzzle', kind: b.dataset.pzf }); });
    const dl = $1('[data-daily]', el); if (dl) dl.onclick = () => { S('open'); if (window.Puzzles) Puzzles.daily(); };
    $1('#phPzHub').onclick = () => { S('open'); if (window.Puzzles) Puzzles.hub({ from: 'play' }); };
    el.querySelectorAll('[data-arc]').forEach(b => b.onclick = () => { S('open'); arcade(b.dataset.arc); });
    if ($1('#phArc')) $1('#phArc').onclick = () => { S('open'); arcade(null); };
    $1('#phCalc').onclick = () => { S('open'); if (window.CalcAcademy) CalcAcademy.open({ from: 'practice' }); };
  }
  /* 💾 every saved game in one place: saved puzzles (kept on this phone) + saved Arcade games (until the app closes) */
  const savedAll = () => {
    let a = []; try { if (window.Puzzles && Puzzles.saved) a = a.concat(Puzzles.saved()); } catch (e) {}
    try { if (window.Arcade && Arcade.saved) a = a.concat(Arcade.saved()); } catch (e) {}
    return a.sort((x, y) => y.at - x.at);
  };
  const ago = t => { const m = Math.round((Date.now() - t) / 6e4); return m < 1 ? 'just now' : m < 60 ? m + ' min ago' : m < 1440 ? Math.round(m / 60) + ' h ago' : Math.round(m / 1440) + ' days ago'; };
  function savedHTML() {
    const L = savedAll(); if (!L.length) return '';
    return `<div class="card ph-saved" id="phSaved"><h3><span aria-hidden="true">💾</span> Your saved games <small>${L.length}</small></h3><p class="sub">Pick up any game exactly where you left it.</p>
      ${L.map(x => `<div class="ph-svrow"><button type="button" class="ph-svgo" data-sv="${E(x.kind)}|${E(x.id)}"><span class="ph-sve" aria-hidden="true">${x.e}</span><span class="ph-svt"><b>${E(x.n)}</b><small>${E([x.label, 'saved ' + ago(x.at)].filter(Boolean).join(' · '))}</small></span><span class="ph-svp">▶ Continue</span></button><button type="button" class="ph-svx" data-svx="${E(x.kind)}|${E(x.id)}" aria-label="Delete saved ${E(x.n)}">🗑</button></div>`).join('')}
      ${L.some(x => x.kind === 'arcade') ? '<p class="cl-small ph-svnote">Arcade games stay saved until you close the app; puzzles stay saved on this phone.</p>' : ''}</div>`;
  }
  function wireSaved(el) {
    el.querySelectorAll('[data-sv]').forEach(b => b.onclick = () => { S('open'); const k = b.dataset.sv.split('|')[0], id = b.dataset.sv.slice(k.length + 1);
      if (k === 'puzzle') return Puzzles.resumeSaved(id);
      const s = screen(); show('play', 'practice'); window.scrollTo(0, 0);
      s.innerHTML = `<div class="ph-root${isCA() ? ' ph-ca' : ''}"><button class="back" id="phBack2">← Play</button><div id="phArcHost"></div></div>`;
      $1('#phBack2').onclick = () => { S('tap'); open(); };
      if (!Arcade.resumeSaved(id, $1('#phArcHost'))) open(); });
    el.querySelectorAll('[data-svx]').forEach(b => b.onclick = () => { S('tap'); const k = b.dataset.svx.split('|')[0], id = b.dataset.svx.slice(k.length + 1);
      try { (k === 'puzzle' ? Puzzles : Arcade).dropSaved(id); } catch (e) {} const box = $1('#phSaved', el); if (box) { const h = savedHTML(); if (h) { box.outerHTML = h; wireSaved(el); } else box.remove(); } });
  }
  window.PlayHub_saved = savedAll;
  const arcGame = id => { try { return (window.Arcade && Arcade.GAMES || []).find(g => g.id === id) || null; } catch (e) { return null; } };
  function liveOpen(o) {
    if (!window.Live) { try { toast('Game Rooms are loading. Please try again in a moment.'); } catch (e) {} return; }
    try { Live.open(o); } catch (e) { console.error(e); Live.open(); }
  }

  /* ---------- 👨‍👩‍👧 play with family: one device (pass-and-play) or each on their own device (family Game Room) ---------- */
  function family(back) {
    style(); back = typeof back === 'function' ? back : backToPractice;
    const el = screen(); show('play', 'practice'); window.scrollTo(0, 0);
    const W = [['mum', '👩 Mum'], ['dad', '👨 Dad'], ['both', '👪 Both parents'], ['guardian', '🧑 Guardian']];
    let who = 'mum';
    const draw = () => {
      el.innerHTML = `<div class="ph-root${isCA() ? ' ph-ca' : ''}"><button class="back" id="phFBack">← Back</button>
        <div class="hello ph-hello" role="heading" aria-level="1"><span aria-hidden="true">👨‍👩‍👧</span> Play with family <small>Learn and laugh together — you get your syllabus, grown-ups get general knowledge</small></div>
        <div class="card"><h3>Who is playing with you?</h3><div class="ph-who" role="radiogroup" aria-label="Who is playing">${W.map(([k, t]) => `<button type="button" role="radio" class="ph-wb${k === who ? ' on' : ''}" aria-checked="${k === who}" data-who="${k}">${t}</button>`).join('')}</div>
          <p class="sub" style="margin-top:6px">You can change names or add more grown-ups (Nani, Dadu…) on the next screen.</p></div>
        <button class="card ph-resume ph-fam" type="button" id="phF1"><span aria-hidden="true">📱</span> <b>On one phone or one laptop<small>Sit together and pass it around. Works on this device right now — no codes, no second device.</small></b><span class="ph-chev" aria-hidden="true">›</span></button>
        <button class="card ph-resume ph-fam" type="button" id="phF2"><span aria-hidden="true">💻📱</span> <b>Each on our own phone or laptop<small>You start a room and read out its code. Grown-ups open Knowtopia on their device → Parent Hub → 🎮 Play with my child → type the code.</small></b><span class="ph-chev" aria-hidden="true">›</span></button>
        <p class="sub" style="padding:0 6px">Grown-ups join from a <b>parent account linked to you</b> (Me → Link to my parent). On one device nobody needs to sign in again.</p></div>`;
      $1('#phFBack').onclick = () => { S('tap'); back(); };
      el.querySelectorAll('[data-who]').forEach(b => b.onclick = () => { S('tap'); who = b.dataset.who; draw(); });
      $1('#phF1').onclick = () => { S('open'); if (!window.Family || !Family.student) { try { toast('Family games are loading. Please try again.'); } catch (e) {} return; }
        Family.student({ with: who === 'both' ? ['mum', 'dad'] : [who], backLabel: 'Back', onClose: () => family(back) }); };
      $1('#phF2').onclick = () => { S('open'); liveOpen({ game: 'quiz' }); };
    };
    draw();
  }

  /* ---------- 🙋 alone ---------- */
  function solo(id) {
    const g = LIVE.find(x => x.id === id); if (!g) return;
    if (id === 'duel') { if (window.CaSpeed && CaSpeed.drill) return CaSpeed.drill(); return; }
    arcade(isCA() && g.soloCA ? g.soloCA : g.solo);
  }
  function arcade(game) {
    const el = screen(); show('play', 'practice'); window.scrollTo(0, 0);
    el.innerHTML = `<div class="ph-root${isCA() ? ' ph-ca' : ''}"><button class="back" id="phBack2">← Play</button><div id="phArcHost"></div></div>`;
    $1('#phBack2').onclick = () => { S('tap'); open(); };
    if (!window.Arcade) { $1('#phArcHost').innerHTML = '<div class="card"><p class="sub">Games are loading. Please try again in a moment.</p></div>'; return; }
    const scope = isCA() ? { grade: 13, key: 'ca-' + caLevel(), label: `CA ${cap(caLevel())} · your MCQs`, pool: caPool } : isJEE() ? { grade: 13, key: 'jee', label: 'JEE Main · real JEE + practice questions', pool: (prog, sel) => Jee.arcadePool(prog, sel), chapter: 'jee' } : { grade: STx().profile.grade };
    if (game) scope.game = game;
    Arcade.open($1('#phArcHost'), scope);
  }
  const cap = s => String(s || '').charAt(0).toUpperCase() + String(s || '').slice(1);
  const caLevel = () => { const s = STx(); return (s && s.ca && s.ca.level) || 'foundation'; };
  /* CA questions in the Arcade's pool shape: built units of the student's level, all real reviewed MCQs */
  async function caPool(prog, sel) {
    const P = { quiz: [], tf: [], speed: [], match: [], sort: [], order: [], subjects: [{ id: 'ca', name: 'CA ' + cap(caLevel()) }], chapter: null, multi: false };
    const X = window.Ca && Ca._; if (!X || !X.structure) return P;
    let st; try { st = await X.structure(caLevel()); } catch (e) { return P; }
    const units = []; (st.papers || []).forEach(p => (p.chapters || []).forEach(c => (c.units || []).forEach(u => { if (u.status === 'built') units.push({ p, c, u }); })));
    const chosen = Array.isArray(sel) && sel.length ? units.filter(x => sel.some(t => x.u.id === t || x.u.id.startsWith(t + '-'))) : units;   // 🎯 papers / chapters / units chosen
    for (let i = chosen.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [chosen[i], chosen[j]] = [chosen[j], chosen[i]]; }
    const pick = chosen.slice(0, 12); let n = 0; if (prog) prog(0, pick.length);
    await Promise.all(pick.map(async x => {
      let d = null; try { d = await X.unitData(x.u.id); } catch (e) {}
      if (prog) prog(++n, pick.length);
      ((d && d.mcqs) || []).forEach(q => {
        const it = { q: q.q, options: q.options, answer: q.answer, explain: q.explain || '', src: { sid: 'ca', sname: (X.paperLabel ? X.paperLabel(x.p) : (x.p.title || x.p.id)), se: '📘', ci: 0, ch: x.c.title || '', tid: x.u.id, tt: x.u.title || '' } };
        let ok = false; try { ok = Arcade.okQ ? Arcade.okQ(it) : true; } catch (e) {}
        if (ok && typeof q.q === 'string' && Array.isArray(q.options) && q.options.length >= 2 && q.options.length <= 4 && q.answer >= 0 && q.answer < q.options.length) P.quiz.push(it);
      });
    }));
    return P;
  }

  /* ---------- Practice tiles: 🎮 Play + 🧮 Calculator Academy ---------- */
  /* CA look: same structure as the CA practice tiles (.ca-hub) so they line up and use the CA colours */
  const caTile = (id, e, t, sub) => `<button type="button" class="card ca-hub" id="${id}"><b class="ca-hube" aria-hidden="true">${e}</b><span><b>${t}</b><small>${sub}</small></span><span class="ca-chev" aria-hidden="true">›</span></button>`;
  const tileSub = () => { const n = savedAll().length; return resume() ? `Back to your room ${E(resume())}` : n ? `💾 ${n} saved game${n > 1 ? 's' : ''} — tap to continue` : 'Games &amp; puzzles · alone or with friends'; };
  const playTile = dark => dark ? caTile('phTile', '🎮', 'Play', tileSub()) : `<button type="button" class="card ph-tile${dark ? ' dark' : ''}" id="phTile" aria-label="Play: games and puzzles, alone or with friends"><span class="ph-te" aria-hidden="true">🎮</span><span class="ph-tt"><b>Play</b><small>${tileSub()}</small></span><span class="ph-chev" aria-hidden="true">›</span></button>`;
  function place() {
    const s = STx(); if (!s || !s.profile || isParent()) return;
    const p = D.getElementById('s-practice');
    if (p && p.classList.contains('active') && !isCA() && !p.querySelector(':scope > #phTile')) {
      const g = p.querySelector(':scope > .goalcard'); if (g) { (p.querySelector(':scope > #rwBoss') || g).insertAdjacentHTML('afterend', playTile(false)); wire(); calcTile(p, D.getElementById('phTile')); }   /* after 🎁/👾 cards (js/rewards.js) */
    }
    const c = D.getElementById('s-ca');
    if (c && isCA() && c.classList.contains('active')) {
      const hubs = c.querySelector(':scope > .ca-hubs');
      if (hubs && !hubs.querySelector('#phTile')) { const rb = hubs.querySelector(':scope > #rwBoss'); if (rb) rb.insertAdjacentHTML('afterend', playTile(true)); else hubs.insertAdjacentHTML('afterbegin', playTile(true)); wire(); calcTile(hubs, D.getElementById('phTile')); }
    }
  }
  function calcTile(host, after) {
    if (!window.CalcAcademy || !CalcAcademy.tileHTML || host.querySelector('#cxaTile')) return;
    /* Calculator Academy always sits at the END of the practice list */
    if (isCA()) { let p = null; try { p = CalcAcademy.progress(); } catch (e) {} host.insertAdjacentHTML('beforeend', caTile('cxaTile', '🧮', 'Calculator Academy', `Free bonus${p ? ` · ${p.done} of ${p.all} missions` : ''} · press real keys to learn`)); }
    else host.insertAdjacentHTML('beforeend', CalcAcademy.tileHTML());
    const t = D.getElementById('cxaTile'); if (t) { t.classList.add('ph-cxa'); t.onclick = () => { S('open'); CalcAcademy.open({ from: 'practice' }); }; }
  }
  const famTile = dark => dark ? caTile('phFamTile', '👨‍👩‍👧', 'Play with family', 'Mum, Dad, both parents or a guardian · one device or each on your own')
    : `<button type="button" class="card ph-tile ph-famtile" id="phFamTile" aria-label="Play with family"><span class="ph-te" aria-hidden="true">👨‍👩‍👧</span><span class="ph-tt"><b>Play with family</b><small>Mum, Dad, both parents or a guardian · one phone, one laptop or each on your own</small></span><span class="ph-chev" aria-hidden="true">›</span></button>`;
  function wire() {
    const t = D.getElementById('phTile'); if (t) { t.onclick = () => { S('open'); open(); }; if (!D.getElementById('phFamTile')) t.insertAdjacentHTML('afterend', famTile(isCA())); }
    const f = D.getElementById('phFamTile'); if (f) f.onclick = () => { S('open'); family(); };
  }

  let css = false;
  function style() {
    if (css) return; css = true;
    D.head.insertAdjacentHTML('beforeend', `<style id="phCss">
      .ph-tile{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:none;cursor:pointer;background:linear-gradient(135deg,#6d4aff,#9b5cff);color:#fff;font-family:inherit}
      .ph-tile .ph-te{font-size:34px}.ph-tile .ph-tt{flex:1;display:flex;flex-direction:column}.ph-tile b{font-size:19px}.ph-tile small{opacity:.9;font-size:13px}.ph-chev{font-size:24px;opacity:.8}
      .ph-fam b{display:flex;flex-direction:column;gap:2px}.ph-fam b small{font-weight:600;color:#666;font-size:13px;line-height:1.3}.ph-fam>span:first-child{font-size:26px}
      .ph-who{display:flex;flex-wrap:wrap;gap:8px}.ph-wb{border:2px solid #dcd6f5;background:#fff;border-radius:999px;padding:8px 14px;font:800 15px inherit;font-family:inherit;cursor:pointer;color:inherit}.ph-wb.on{background:#6d4aff;border-color:#6d4aff;color:#fff}
      .ph-famtile{background:linear-gradient(135deg,#e05297,#ff9a5a)!important}
      .ph-tile.dark{background:linear-gradient(135deg,#3b2a7a,#5b3fb8)}
      .ca-hubs .ph-tile,.ca-hubs .cxa-tile{margin-bottom:10px}
      .ph-hello small{display:block}
      .ph-resume{display:flex;align-items:center;gap:8px;width:100%;border:none;background:#fff7d6;cursor:pointer;font-family:inherit;font-size:16px;text-align:left}.ph-resume b{flex:1}
      .ph-join{display:flex;gap:8px;margin:6px 0 10px}.ph-join input{flex:1;min-width:0;font-size:18px;letter-spacing:2px;text-transform:uppercase;padding:10px 12px;border-radius:12px;border:2px solid #dcd6f5;font-family:inherit}.ph-join .btn{width:auto;padding:10px 18px}
      .ph-g{display:flex;align-items:center;gap:10px;padding:10px 0;border-top:1px solid #eee}.ph-g:first-of-type{border-top:none}
      .ph-ge{font-size:28px;width:36px;text-align:center;flex:none}.ph-gt{flex:1;min-width:0;display:flex;flex-direction:column}.ph-gt b{font-size:16px}.ph-gt small{color:#666;font-size:12.5px;line-height:1.3}.ph-gt .ph-alone{color:#6d4aff;margin-top:2px}
      .ph-gb{display:flex;flex-direction:column;gap:6px;flex:none}
      .ph-b{border:none;border-radius:12px;padding:8px 10px;font-weight:800;font-size:13.5px;cursor:pointer;font-family:inherit;min-width:92px;min-height:40px}
      .ph-b.solo{background:#eef2ff;color:#3b3b8f}.ph-b.fr{background:#6d4aff;color:#fff}
      .ph-more{display:grid;grid-template-columns:1fr 1fr;gap:8px}.ph-m{border:none;border-radius:14px;background:#f4f1ff;padding:10px;text-align:left;cursor:pointer;font-family:inherit;display:flex;flex-direction:column;gap:2px}.ph-m span{font-size:24px}.ph-m small{color:#666;font-size:12px;line-height:1.25}
      .ph-all{margin-top:10px}
    </style>`);
  }

  function boot() {
    style();
    let t = 0; new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; try { place(); } catch (e) {} }); }).observe(D.body, { childList: true, subtree: true });
    place();
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
  window.PlayHub = { open, solo, arcade, family, _caPool: caPool };
})();
