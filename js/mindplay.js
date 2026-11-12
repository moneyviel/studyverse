/* ================= 🎮 Brain games and Brain Test (js/mindplay.js) =================
   Hands-on IQ-style games inside Brainstorm Arena (Mind Gym). Puzzles come from js/mindplay-gen.js — made fresh
   every time and checked by the app; students never mark themselves.
   Three looks by age:  j (Grades 1–3) 🎪 Brain Carnival – bright, bouncy, emoji
                        m (Grades 4–8) 🗺️ Brain Quest – an adventure trail of islands
                        s / CA          🧪 Brain Lab – clean, timed, professional
   Games: memory code, perception sprint, balance scales, number pyramid, number wheel, cube folding (not Gr 1–3),
   word jumble, magic square. Each has levels 1–5: a level opens when the one before has ⭐⭐ and learning allows
   (1 level + 1 more for every 2 finished topics/units).
   ⏱️ Brain Test: one timed run through every skill → section scorecard (no IQ number, ever).
   Progress: ST.mind.games[g] = {best: {lvl: stars}}, ST.mind.btests = [{at, pct, sec:{skill:%}}] (last 12).
   window.MindPlay = { hub, test } */
(function () {
  'use strict';
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const G = () => window.MindPlayGen;
  const MG = () => window.MindGym;
  const M = () => MG().state();
  const band = () => { const b = MG()._band(); return b === 'p' ? 's' : b; };
  const persist = () => { try { save(); } catch (e) {} };
  const THEME = { j: { name: 'Brain Carnival', e: '🎪', test: 'Carnival Challenge', cls: 'pl-j' }, m: { name: 'Brain Quest', e: '🗺️', test: 'Grand Expedition', cls: 'pl-m' }, s: { name: 'Brain Lab', e: '🧪', test: 'Brain Test', cls: 'pl-s' } };
  const GAMES = [
    { id: 'memory', e: '🧠', skill: 'Memory', n: { j: 'Animal Memory', m: 'Treasure Code', s: 'Memory Matrix' }, d: 'Remember the secret code, then crack it' },
    { id: 'twins', e: '👀', skill: 'Perception', n: { j: 'Missing Number', m: 'Eagle Scan', s: 'Perception Sprint' }, d: 'Spot what is missing or doubled — fast!' },
    { id: 'scale', e: '⚖️', skill: 'Logic', n: { j: 'Fruit Seesaw', m: 'Balance Bridge', s: 'Balance Logic' }, d: 'Work out hidden weights and balance the scale' },
    { id: 'pyramid', e: '🔺', skill: 'Numbers', n: { j: 'Number Tower', m: 'Pyramid Climb', s: 'Number Pyramid' }, d: 'Each brick is the sum of the two below it' },
    { id: 'wheel', e: '🎡', skill: 'Numbers', n: { j: 'Number Wheel', m: 'Mystic Wheel', s: 'Cipher Wheel' }, d: 'Find the rule hidden in the wheel' },
    { id: 'cube', e: '🧊', skill: 'Space', n: { m: 'Cube Workshop', s: 'Spatial Folding' }, d: 'Fold the flat net into a cube in your mind', not: 'j' },
    { id: 'jumble', e: '🔤', skill: 'Words', n: { j: 'Picture Spell', m: 'Word Scramble', s: 'Anagram Lab' }, d: 'Tap the letters into the right order' },
    { id: 'magic', e: '✨', skill: 'Logic', n: { j: 'Magic Box', m: 'Magic Square', s: 'Magic Square' }, d: 'Every row, column and diagonal must add up the same' }];
  /* suites: 'iq' (Brainstorm Arena, defined here) and others added with MindPlay.addSuite (e.g. js/heartplay.js) */
  const SUITES = { iq: { id: 'iq', test: 'iq', theme: THEME, games: GAMES, gen: () => window.MindPlayGen, back: () => MG().open(), backLabel: 'Mind Gym', store: 'btests', kind: g => KIND[g.id] || g.skill } };
  let SU = SUITES.iq;
  const games = () => SU.games.filter(g => g.not !== band() && !(g.pool && window.MindPool && !MindPool.count(SU.test, g).all));
  const pname = () => { const t = (MG().TESTS || []).find(x => x.id === SU.test); return t ? t.n : SU.theme[band()].name; };
  const gname = g => g.n[band()] || g.n.m;
  var KIND = { memory: 'Memory code', twins: 'Perception sprint', scale: 'Balance scales', pyramid: 'Number pyramid', wheel: 'Number wheel', cube: 'Cube folding', jumble: 'Word jumble', magic: 'Magic square' };
  const PER_ROUND = 5;

  /* progress */
  function gst(id) { const m = M(), k = SU.id === 'iq' ? id : SU.id + ':' + id; m.games = m.games || {}; return m.games[k] = m.games[k] || { best: {} }; }
  const learnLv = () => MG()._owner() ? 5 : Math.min(5, 1 + Math.floor(MG()._steps() / 2));
  function openLv(id) { const b = gst(id).best; let L = 1; while (L < 5 && (b[L] || 0) >= 2 && L < learnLv()) L++; return L; }
  const starsTxt = n => '⭐'.repeat(n) + '☆'.repeat(3 - n);

  /* ---------- screen helpers ---------- */
  function screen() { return MG()._screen(); }
  function frame(inner, back, title) {
    const t = SU.theme[band()], el = screen(); MG()._show();
    el.innerHTML = `<div class="mg-root pl-root ${t.cls}"><button class="back" id="plBack">← ${E(back.t)}</button>${title ? `<div class="pl-title">${title}</div>` : ''}${inner}</div>`;
    $1('#plBack').onclick = () => { S('tap'); back.go(); }; window.scrollTo(0, 0);
    return el;
  }
  function keypad(keys, onKey, extra) {
    const w = D.createElement('div'); w.className = 'pl-keys' + (keys.length > 6 ? ' many' : '');
    w.innerHTML = keys.map(k => `<button type="button" class="pl-key" data-k="${E(k)}">${E(k)}</button>`).join('') + (extra || []).map(([k, l]) => `<button type="button" class="pl-key x" data-k="${E(k)}">${l}</button>`).join('');
    w.querySelectorAll('.pl-key').forEach(b => b.onclick = () => { S('tap'); b.classList.remove('hit'); void b.offsetWidth; b.classList.add('hit'); onKey(b.dataset.k); });
    return w;
  }
  function burst(host, n) {
    const c = D.createElement('div'); c.className = 'mg-conf'; c.setAttribute('aria-hidden', 'true');
    c.innerHTML = Array.from({ length: n || 16 }, (_, i) => `<i style="--dx:${Math.round(Math.cos(i / 16 * 6.28) * (70 + Math.random() * 60))}px;--dy:${Math.round(Math.sin(i / 16 * 6.28) * (60 + Math.random() * 50) - 30)}px">${(band() === 's' ? ['✦', '✧', '•', '◆'] : ['⭐', '✨', '🎉', '💫', '🎈'])[i % (band() === 's' ? 4 : 5)]}</i>`).join('');
    host.style.position = host.style.position || 'relative'; host.appendChild(c); setTimeout(() => c.remove(), 1200);
  }
  function timerBar(host, secs, onEnd) {
    const bar = D.createElement('div'); bar.className = 'pl-timer'; bar.innerHTML = `<i style="animation-duration:${secs}s"></i><span>${secs}s</span>`;
    host.prepend(bar); let left = secs; const sp = bar.querySelector('span');
    const t = setInterval(() => { if (!bar.isConnected) return clearInterval(t); left--; sp.textContent = left + 's'; if (left <= 3) bar.classList.add('low'); if (left <= 0) { clearInterval(t); onEnd(); } }, 1000);
    return () => clearInterval(t);
  }

  /* ========== each game: play(host, puzzle, done(ok, why)) ========== */
  const PLAY = {};

  PLAY.memory = (host, p, done) => {
    const b = band();
    host.innerHTML = `<p class="pl-q">${b === 'j' ? 'Look carefully! Each friend has a secret number.' : 'Memorise the code: each symbol has a number.'}</p><div class="pl-memgrid">${p.pairs.map((x, i) => `<div class="pl-mcard" style="animation-delay:${i * .08}s"><b class="pl-sym">${x.s}</b><span>${x.n}</span></div>`).join('')}</div><button type="button" class="btn pl-ready">I’m ready ▶</button>`;
    let stop = timerBar(host, p.study, go);
    $1('.pl-ready', host).onclick = () => { S('open'); stop(); go(); };
    let ans = {}, i = 0, gone = false;
    function go() {
      if (gone) return; gone = true;
      host.innerHTML = `<p class="pl-q">${b === 'j' ? 'What was the number?' : 'Which number went with this symbol?'}</p><div class="pl-dots">${p.ask.map((_, k) => `<i data-d="${k}"></i>`).join('')}</div><div class="pl-bigsym"></div>`;
      const big = $1('.pl-bigsym', host);
      const show = () => { big.innerHTML = `<b class="pl-sym pop">${p.ask[i].s}</b>`; };
      show();
      host.appendChild(keypad(p.pairs.map(x => x.n).sort((a, c) => a - c).map(String), k => {
        const s = p.ask[i].s, ok = +k === p.ask[i].n; ans[s] = +k;
        const d = host.querySelector(`[data-d="${i}"]`); d.className = ok ? 'y' : 'n';
        i++; if (i < p.ask.length) show(); else finish();
      }));
    }
    function finish() {
      const right = p.ask.filter(x => ans[x.s] === x.n).length, ok = right / p.ask.length >= .75;
      host.querySelector('.pl-keys').remove();
      done(ok, `${right} of ${p.ask.length} remembered. Tip: link each symbol to its number with a little story, like “the 🚀 blasts off on 3”.`,
        `<div class="pl-memgrid small">${p.pairs.map(x => `<div class="pl-mcard ${ans[x.s] === x.n ? 'ok' : 'no'}"><b class="pl-sym">${x.s}</b><span>${x.n}</span></div>`).join('')}</div>`, right / p.ask.length);
    }
  };

  PLAY.twins = (host, p, done) => {
    host.innerHTML = `<p class="pl-q">${E(p.q)}</p><div class="pl-chips">${p.shown.map((x, i) => `<span class="pl-chip" style="animation-delay:${i * .05}s">${x}</span>`).join('')}</div>`;
    let over = false;
    const stop = timerBar(host, p.time, () => end(null));
    host.appendChild(keypad(p.keys.map(String), k => end(k)));
    function end(k) {
      if (over) return; over = true; stop();
      const ok = k != null && String(k) === String(p.answer);
      host.querySelectorAll('.pl-key').forEach(b => { b.disabled = true; if (b.dataset.k === String(p.answer)) b.classList.add('ok'); else if (b.dataset.k === k) b.classList.add('no'); });
      if (p.mode === 'letter') host.querySelectorAll('.pl-chip').forEach(c => { if (c.textContent === p.answer) c.classList.add('hl'); });
      done(ok, k == null ? `Time’s up! The answer was ${p.answer}.` : p.mode === 'digit' ? `${p.answer} is the only number not in the list. Tip: count up in order and look for the gap.` : `${p.answer} appears twice. Tip: scan letter by letter and keep a mental tick-list.`);
    }
  };

  const short = t => { const a = Array.from(t), out = []; let i = 0;
    while (i < a.length) { let j = i; while (j < a.length && a[j] === a[i]) j++; out.push(j - i > 4 ? `${j - i}×${a[i]}` : a.slice(i, j).join('')); i = j; } return out.join(' '); };
  PLAY.scale = (host, p, done) => {
    const beam = (L, Rt, tilt, id) => `<svg viewBox="0 0 220 120" class="pl-scale${id ? ' main' : ''}" ${id ? `id="${id}"` : ''} aria-hidden="true">
      <polygon points="110,62 96,112 124,112" class="pl-stand"/><g class="pl-beam" style="transform:rotate(${tilt}deg)"><rect x="18" y="56" width="184" height="7" rx="3" class="pl-bar"/>
      <g class="pl-pan l"><path d="M18 60 L8 86 L58 86 L48 60" class="pl-rope"/><rect x="4" y="84" width="58" height="6" rx="3" class="pl-plate"/><foreignObject x="0" y="40" width="66" height="44"><div class="pl-pile">${L}</div></foreignObject></g>
      <g class="pl-pan r"><path d="M172 60 L162 86 L212 86 L202 60" class="pl-rope"/><rect x="158" y="84" width="58" height="6" rx="3" class="pl-plate"/><foreignObject x="154" y="40" width="66" height="44"><div class="pl-pile">${Rt}</div></foreignObject></g></g></svg>`;
    let n = 0;
    const b = band();
    host.innerHTML = `<p class="pl-q">${b === 'j' ? 'The seesaw is balanced. How many 🍒 make the other side balance?' : 'These scales balance. How many 🍒 balance the big scale?'}</p>
      <div class="pl-clues">${p.clues.map(([L, Rt]) => `<div class="pl-clue">${beam(L, Rt, 0)}<div class="pl-eq">${short(L)} <b>=</b> ${short(Rt)}</div></div>`).join('')}</div>
      <div class="pl-mainwrap">${beam(p.leftTxt, '', 0, 'plMain')}</div>
      <div class="pl-count"><button type="button" class="pl-pm" data-d="-1" aria-label="One cherry less">−</button><b><span id="plN">0</span> 🍒</b><button type="button" class="pl-pm" data-d="1" aria-label="One cherry more">+</button></div>
      <button type="button" class="btn pl-go">⚖️ Weigh it!</button>`;
    const draw = () => { $1('#plN', host).textContent = n; const r = host.querySelector('#plMain .pl-pan.r .pl-pile'); r.textContent = '🍒'.repeat(Math.min(n, 18)) + (n > 18 ? '+' : ''); };
    host.querySelectorAll('.pl-pm').forEach(x => x.onclick = () => { S('tap'); n = Math.max(0, Math.min(p.max, n + +x.dataset.d)); draw(); });
    $1('.pl-go', host).onclick = () => {
      host.querySelectorAll('.pl-pm,.pl-go').forEach(x => x.disabled = true);
      const L = Object.entries(p.left).reduce((t, [x, c]) => t + p.w[x] * c, 0), tilt = Math.max(-16, Math.min(16, (n - L) * 3));
      const bm = host.querySelector('#plMain .pl-beam'); bm.style.transition = 'transform 1.1s cubic-bezier(.3,1.6,.5,1)'; requestAnimationFrame(() => bm.style.transform = `rotate(${tilt}deg)`);
      const ok = n === p.answer;
      const steps = p.items.map(x => `${x} = ${p.w[x]} 🍒`).join(', ');
      setTimeout(() => done(ok, `${ok ? 'Perfectly balanced! ' : `It needs ${p.answer} 🍒. `}Work it out from the small scales: ${steps}. So ${p.leftTxt} = ${p.answer} 🍒.`), 900);
    };
  };

  PLAY.pyramid = (host, p, done) => {
    const n = p.rows.length, ans = {}, hid = new Set(p.hidden.map(x => x.join()));
    let sel = p.hidden[0].join();
    host.innerHTML = `<p class="pl-q">${band() === 'j' ? 'Each block is the two blocks under it added together. Fill the empty blocks!' : 'Each brick = the two bricks below it added together. Fill every empty brick.'}</p><div class="pl-pyr"></div>`;
    const pyr = $1('.pl-pyr', host);
    const draw = (reveal) => {
      pyr.innerHTML = p.rows.slice().reverse().map((row, ri) => { const a = n - 1 - ri; return `<div class="pl-prow">${row.map((v, c) => { const k = a + ',' + c;
        if (!hid.has(k)) return `<span class="pl-brick">${v}</span>`;
        const val = ans[k] == null ? '' : ans[k], cls = reveal ? (ans[k] === v ? ' ok' : ' no') : (k === sel ? ' sel' : '');
        return `<button type="button" class="pl-brick in${cls}" data-b="${k}">${reveal && ans[k] !== v ? `<s>${val || '?'}</s> ${v}` : (val === '' ? '?' : val)}</button>`; }).join('')}</div>`; }).join('');
      if (!reveal) pyr.querySelectorAll('[data-b]').forEach(x => x.onclick = () => { S('tap'); sel = x.dataset.b; draw(); });
    };
    draw();
    host.appendChild(keypad(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], k => {
      if (k === '⌫') { const s = String(ans[sel] == null ? '' : ans[sel]).slice(0, -1); ans[sel] = s === '' ? null : +s; }
      else if (k === '✓') return check();
      else { const s = String(ans[sel] == null ? '' : ans[sel]) + k; if (s.length <= 3) ans[sel] = +s; }
      draw();
    }, [['⌫', '⌫'], ['✓', '✓ Check']]));
    function check() {
      if (p.hidden.some(x => ans[x.join()] == null)) { toast('Fill every empty brick first'); return; }
      host.querySelector('.pl-keys').remove(); draw(true);
      const ok = p.hidden.every(([a, c]) => ans[a + ',' + c] === p.rows[a][c]);
      done(ok, 'Add the two bricks below to get the one above. If you know the top and one bottom brick, take away to find the other.');
    }
  };

  PLAY.wheel = (host, p, done) => {
    const R = 92, cx = 100, cy = 100, cols = ['#ff5a5f', '#ffc43d', '#21b573', '#2b8cff', '#9b5cff', '#ff8a1f', '#00b8c7', '#ff4fa3'];
    const seg = (i, val, cls) => { const a0 = (i * 45 - 112.5) * Math.PI / 180, a1 = ((i + 1) * 45 - 112.5) * Math.PI / 180, am = (a0 + a1) / 2;
      return `<path d="M${cx} ${cy} L${cx + R * Math.cos(a0)} ${cy + R * Math.sin(a0)} A${R} ${R} 0 0 1 ${cx + R * Math.cos(a1)} ${cy + R * Math.sin(a1)} Z" fill="${cols[i]}" class="pl-wseg ${cls || ''}"/><text x="${cx + 60 * Math.cos(am)}" y="${cy + 60 * Math.sin(am) + 8}" text-anchor="middle" class="pl-wtxt">${val}</text>`; };
    let typed = '';
    const svg = v => `<svg viewBox="0 0 200 200" class="pl-wheel" aria-hidden="true">${p.seg.map((x, i) => seg(i, i === p.miss ? (v || '?') : x, i === p.miss ? 'miss' : '')).join('')}<circle cx="100" cy="100" r="22" class="pl-hub"/><text x="100" y="107" text-anchor="middle" class="pl-hubt">${band() === 's' ? '∑' : '★'}</text></svg>`;
    host.innerHTML = `<p class="pl-q">What number belongs in the empty part of the wheel?</p><div class="pl-wwrap spin">${svg()}</div><div class="pl-typed">?</div>`;
    const wrap = $1('.pl-wwrap', host), ty = $1('.pl-typed', host); setTimeout(() => wrap.classList.remove('spin'), 1100);
    host.appendChild(keypad(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], k => {
      if (k === '⌫') typed = typed.slice(0, -1); else if (k === '✓') return check(); else if (typed.length < 4) typed += k;
      ty.textContent = typed || '?'; wrap.innerHTML = svg(typed);
    }, [['⌫', '⌫'], ['✓', '✓ Check']]));
    function check() {
      if (!typed) { toast('Type a number first'); return; }
      host.querySelector('.pl-keys').remove();
      const ok = +typed === p.answer; ty.innerHTML = ok ? `✅ ${p.answer}` : `<s>${typed}</s> → ${p.answer}`;
      done(ok, p.why + ` The missing number is ${p.answer}.`);
    }
  };

  /* cube: flat net + four cube pictures; afterwards a 3D cube to spin */
  const SYM = s => `<span class="pl-csym">${s[1]}</span>`;
  function netHTML(p) {
    const rows = Math.max(...p.net.map(c => c[0])) + 1, cols = Math.max(...p.net.map(c => c[1])) + 1;
    return `<div class="pl-net" style="grid-template-columns:repeat(${cols},44px);grid-template-rows:repeat(${rows},44px)">${p.net.map(([r, c], i) => `<div class="pl-nc" style="grid-row:${r + 1};grid-column:${c + 1};background:${p.syms[i][0]};animation-delay:${i * .07}s">${SYM(p.syms[i])}</div>`).join('')}</div>`;
  }
  function isoCube(p, o) {
    const f = (pts, i) => `<polygon points="${pts}" fill="${p.syms[i][0]}" stroke="#2a2350" stroke-width="1.6" stroke-linejoin="round"/>`;
    const t = (x, y, i) => `<text x="${x}" y="${y}" text-anchor="middle" class="pl-ct">${p.syms[i][1]}</text>`;
    return `<svg viewBox="0 0 100 100" class="pl-iso" aria-hidden="true">${f('50,12 86,30 50,48 14,30', o[0])}${f('14,30 50,48 50,90 14,72', o[1])}${f('50,48 86,30 86,72 50,90', o[2])}${t(50, 36, o[0])}${t(32, 66, o[1])}${t(68, 66, o[2])}</svg>`;
  }
  function cube3D(p) {
    const at = {}; Object.entries(p.fold).forEach(([i, f]) => at[f] = +i);
    const face = (f, tr) => `<div class="pl-f" style="transform:${tr};background:${p.syms[at[f]][0]}">${p.syms[at[f]][1]}</div>`;
    return `<div class="pl-3d" tabindex="0" aria-label="Cube you can spin"><div class="pl-cube" style="transform:rotateX(-24deg) rotateY(-36deg)">${face('S', 'translateZ(45px)')}${face('N', 'rotateY(180deg) translateZ(45px)')}${face('E', 'rotateY(90deg) translateZ(45px)')}${face('W', 'rotateY(-90deg) translateZ(45px)')}${face('T', 'rotateX(90deg) translateZ(45px)')}${face('B', 'rotateX(-90deg) translateZ(45px)')}</div></div><p class="pl-cap">👆 Drag to spin the folded cube</p>`;
  }
  function spin(el) {
    const c = el.querySelector('.pl-cube'); let rx = -24, ry = -36, sx, sy, down = false;
    el.addEventListener('pointerdown', e => { down = true; sx = e.clientX; sy = e.clientY; el.setPointerCapture(e.pointerId); });
    el.addEventListener('pointermove', e => { if (!down) return; ry += (e.clientX - sx) * .6; rx -= (e.clientY - sy) * .6; sx = e.clientX; sy = e.clientY; c.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg)`; });
    el.addEventListener('pointerup', () => { down = false; });
    el.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') ry -= 20; if (e.key === 'ArrowRight') ry += 20; if (e.key === 'ArrowUp') rx += 20; if (e.key === 'ArrowDown') rx -= 20; c.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg)`; });
  }
  PLAY.cube = (host, p, done) => {
    host.innerHTML = `<p class="pl-q">Fold this flat net into a cube. Which cube could it make?</p><div class="pl-netwrap">${netHTML(p)}</div><div class="pl-opts">${p.opts.map((o, i) => `<button type="button" class="pl-opt" data-i="${i}" aria-label="Cube ${'ABCD'[i]}">${isoCube(p, o)}</button>`).join('')}</div>`;
    host.querySelectorAll('.pl-opt').forEach(x => x.onclick = () => {
      const i = +x.dataset.i, ok = i === p.a;
      host.querySelectorAll('.pl-opt').forEach(y => { y.disabled = true; if (+y.dataset.i === p.a) y.classList.add('ok'); });
      if (!ok) x.classList.add('no');
      done(ok, 'Faces that are opposite on the cube can never be seen together, and the three faces round a corner must sit in the same order as on the net. Spin the folded cube to check!', cube3D(p), null, el => { const c = el.querySelector('.pl-3d'); if (c) spin(c); });
    });
  };

  PLAY.jumble = (host, p, done) => {
    const slots = Array(p.word.length).fill(null); let used = new Set();
    host.innerHTML = `<p class="pl-q">${p.emoji ? `<span class="pl-emo">${p.emoji}</span>` : ''}${E(p.clue)}${p.emoji ? '' : ` · ${p.word.length} letters`}</p><div class="pl-slots"></div><div class="pl-tiles"></div><div class="pl-row2"><button type="button" class="btn ghost pl-mix">🔀 Mix</button><button type="button" class="btn pl-chk">✓ Check</button></div>`;
    let order = p.tiles.map((t, i) => i);
    const draw = () => {
      $1('.pl-slots', host).innerHTML = slots.map((s, i) => `<button type="button" class="pl-slot${s != null ? ' full' : ''}" data-s="${i}">${s != null ? p.tiles[s] : ''}</button>`).join('');
      $1('.pl-tiles', host).innerHTML = order.map(i => `<button type="button" class="pl-tile${used.has(i) ? ' used' : ''}" data-t="${i}" ${used.has(i) ? 'disabled' : ''}>${p.tiles[i]}</button>`).join('');
      host.querySelectorAll('[data-t]').forEach(x => x.onclick = () => { S('tap'); const i = +x.dataset.t, k = slots.indexOf(null); if (k < 0) return; slots[k] = i; used.add(i); draw(); });
      host.querySelectorAll('[data-s]').forEach(x => x.onclick = () => { const k = +x.dataset.s; if (slots[k] == null) return; S('tap'); used.delete(slots[k]); slots[k] = null; draw(); });
    };
    draw();
    $1('.pl-mix', host).onclick = () => { S('tap'); order = order.sort(() => Math.random() - .5); draw(); };
    $1('.pl-chk', host).onclick = () => {
      if (slots.includes(null)) { toast('Use every letter first'); return; }
      const w = slots.map(i => p.tiles[i]).join(''), ok = w === p.word;
      host.querySelectorAll('button').forEach(b => b.disabled = true);
      $1('.pl-slots', host).classList.add(ok ? 'win' : 'shake');
      done(ok, ok ? `Yes — ${p.word}!` : `The word was ${p.word}.`);
    };
  };

  PLAY.magic = (host, p, done) => {
    const val = p.sq.map((v, i) => p.hide.includes(i) ? null : v); let sel = p.hide[0];
    const free = p.hide.map(i => p.sq[i]).sort((a, b) => a - b);
    host.innerHTML = `<p class="pl-q">Fill the empty boxes so every row, column and diagonal adds up to <b>${p.total}</b>. Use each number once.</p><div class="pl-msq"></div>`;
    const L = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
    const draw = reveal => {
      const sum = l => l.every(i => val[i] != null) ? l.reduce((t, i) => t + val[i], 0) : null;
      $1('.pl-msq', host).innerHTML = `<div class="pl-mgrid">${val.map((v, i) => p.hide.includes(i) ? `<button type="button" class="pl-mc in${i === sel && !reveal ? ' sel' : ''}${reveal ? (v === p.sq[i] ? ' ok' : ' no') : ''}" data-c="${i}">${reveal && v !== p.sq[i] ? `<s>${v ?? ''}</s>${p.sq[i]}` : v ?? ''}</button>` : `<span class="pl-mc">${v}</span>`).join('')}</div>
        <div class="pl-sums">${L.slice(0, 3).map(l => { const s = sum(l); return `<span class="${s == null ? '' : s === p.total ? 'ok' : 'no'}">${s ?? '·'}</span>`; }).join('')}</div>`;
      if (!reveal) host.querySelectorAll('[data-c]').forEach(x => x.onclick = () => { S('tap'); sel = +x.dataset.c; draw(); });
    };
    draw();
    host.appendChild(keypad(free.map(String), k => {
      if (k === '✓') return check();
      if (k === '⌫') val[sel] = null; else { const n = +k; const was = val.findIndex((v, i) => v === n && p.hide.includes(i)); if (was >= 0) val[was] = null; val[sel] = n; const nx = p.hide.find(i => val[i] == null); if (nx != null) sel = nx; }
      draw();
    }, [['⌫', '⌫'], ['✓', '✓ Check']]));
    function check() {
      if (p.hide.some(i => val[i] == null)) { toast('Fill every box first'); return; }
      host.querySelector('.pl-keys').remove(); draw(true);
      const ok = p.hide.every(i => val[i] === p.sq[i]);
      done(ok, `The middle box is always the key: it is a third of ${p.total}. Opposite boxes around it add up to the same amount.`);
    }
  };

  function round_(sc) { const m = M(), T = SU.test; m.rounds[T] = (m.rounds[T] || 0) + 1; const H = m.hist[T] = (m.hist[T] || []); H.push(Math.round(sc * 100)); if (H.length > 20) H.splice(0, H.length - 20); }

  /* ---------- running a set of puzzles ---------- */
  function runSet(list, opts) {   // list: [{g, lvl}], opts: {title, back, onEnd(results), timed}
    let i = 0; const res = [], snaps = [];
    /* review: a numbered strip + ◀ Previous lets students look again at any answered challenge (its answer and the why) */
    const stripHTML = cur => `<div class="pl-hist" role="group" aria-label="Answered challenges">${list.map((_, j) => j < snaps.length ? `<button type="button" class="pl-hd ${snaps[j].ok ? 'y' : 'n'}${j === cur ? ' cur' : ''}" data-h="${j}" aria-label="Look again at challenge ${j + 1}">${snaps[j].ok ? '✓' : '✗'}</button>` : `<span class="pl-hd${j === cur ? ' cur' : ''}">${j + 1}</span>`).join('')}</div>`;
    function review(el, j) {
      const card = $1('.pl-card', el); let rv = $1('.pl-revw', el);
      if (!rv) { rv = D.createElement('div'); rv.className = 'card pl-card pl-revw'; card.after(rv); }
      card.hidden = true; rv.hidden = false; window.scrollTo(0, 0);
      rv.innerHTML = `${stripHTML(j)}<p class="pl-revtag">👀 Looking again at challenge ${j + 1}</p><div class="pl-revbody">${snaps[j].html}</div>
        <div class="pl-nav">${j > 0 ? '<button type="button" class="btn ghost" data-go="prev">◀ Previous</button>' : '<span></span>'}<button type="button" class="btn" data-go="next">${j + 1 < i ? 'Next ▶' : `Back to challenge ${i + 1} ▶`}</button></div>`;
      rv.querySelectorAll('[data-h]').forEach(b => b.onclick = () => { S('tap'); review(el, +b.dataset.h); });
      rv.querySelector('[data-go="next"]').onclick = () => { S('tap'); if (j + 1 < i) review(el, j + 1); else back(el); };
      const pv = rv.querySelector('[data-go="prev"]'); if (pv) pv.onclick = () => { S('tap'); review(el, j - 1); };
    }
    function back(el) { const rv = $1('.pl-revw', el); if (rv) rv.hidden = true; $1('.pl-card:not(.pl-revw)', el).hidden = false; }
    const next = () => {
      if (i >= list.length) return opts.onEnd(res);
      const it = list[i]; if (it.s) SU = SUITES[it.s];
      const g = SU.games.find(x => x.id === it.g), p = g.pool ? MindPool.next(SU.test, g) : SU.gen().make(it.g, band(), it.lvl);
      const el = frame(`<div class="card pl-card">${snaps.length ? stripHTML(i) : ''}<div class="pl-top"><span>${it.s ? MG().TESTS.find(x => x.id === it.s).e + ' ' : ''}${g.e} ${E(gname(g))}${opts.tag ? ` · ${E(opts.tag(it))}` : ''}</span><span>${i + 1} / ${list.length}</span></div><div class="mg-bar"><i style="width:${Math.round(i / list.length * 100)}%"></i></div><div class="pl-stage"></div><div class="pl-fb" aria-live="polite"></div></div>`, opts.back, opts.title);
      const stage = $1('.pl-stage', el);
      el.querySelectorAll('.pl-card [data-h]').forEach(b => b.onclick = () => { S('tap'); review(el, +b.dataset.h); });
      PLAY[it.g](stage, p, (ok, why, extra, part, after) => {
        S(ok ? 'right' : 'wrong'); if (ok) burst($1('.pl-card', el));
        res.push({ g: it.g, ok, part: part == null ? (ok ? 1 : 0) : part });
        try { if (!g.pool) MG().record(SU.test, SU.kind(g), ok); } catch (e) {}
        const fb = $1('.pl-fb', el);
        fb.innerHTML = `<p class="mg-v ${ok ? 'ok' : 'no'}">${ok ? (band() === 'j' ? '🎉 Yay, correct!' : band() === 'm' ? '✅ Quest step cleared!' : '✅ Correct') : (band() === 'j' ? '🙈 Oops, not this time!' : '❌ Not quite')}</p><p>${E(why)}</p>${extra || ''}<div class="pl-nav">${i > 0 ? '<button class="btn ghost" type="button" id="plPrev">◀ Previous</button>' : ''}<button class="btn" type="button" id="plNext">${i + 1 < list.length ? 'Next ▶' : 'See results'}</button></div>`;
        if (after) after(fb);
        const cardEl = $1('.pl-card', el);
        setTimeout(() => { const c = cardEl.cloneNode(true); c.querySelectorAll('.pl-nav,.pl-hist,.pq-again,.mg-showme,.mg-conf').forEach(x => x.remove()); c.querySelectorAll('button,input').forEach(x => { x.disabled = true; x.tabIndex = -1; }); snaps[i] = { html: c.innerHTML, ok }; }, 1600);
        const pb = $1('#plPrev', el); if (pb) pb.onclick = () => { S('tap'); review(el, i - 1); };
        const nb = $1('#plNext', el); nb.onclick = () => { S('tap'); if (!snaps[i]) { const c = cardEl.cloneNode(true); c.querySelectorAll('.pl-nav,.pl-hist,.pq-again,.mg-showme,.mg-conf').forEach(x => x.remove()); c.querySelectorAll('button,input').forEach(x => { x.disabled = true; x.tabIndex = -1; }); snaps[i] = { html: c.innerHTML, ok }; } i++; next(); };
        nb.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });
    };
    next();
  }

  /* ---------- hub ---------- */
  function hub() {
    style();
    if (window.MindPool && !MindPool.ready(SU.test)) { const want = SU.id; MindPool.load(SU.test).then(() => { if (SU.id === want) hub(); }); return; }
    const b = band(), t = SU.theme[b], L = games();
    const card = g => { const lv = openLv(g.id), best = gst(g.id).best, st = Math.max(0, ...Object.values(best));
      return `<button type="button" class="pl-game" data-g="${g.id}"><span class="pl-ge" aria-hidden="true">${g.e}</span><span class="pl-gt"><b>${E(gname(g))}</b><small>${E(g.d)}</small><small class="pl-lv">Level ${lv} of 5 · ${starsTxt(best[lv] || 0)}</small>${g.pool ? (c => `<small class="pl-cnt">${c.open} of ${c.all} challenges open</small>`)(MindPool.count(SU.test, g)) : ''}</span></button>`; };
    const trail = b === 'm' ? `<div class="pl-trail">${L.map((g, k) => `<div class="pl-isl" style="--k:${k}">${card(g)}</div>`).join('')}</div>` : `<div class="pl-games">${L.map(card).join('')}</div>`;
    const bt = M()[SU.store] || [];
    const el = frame(`<div class="pl-hero"><div class="pl-he" aria-hidden="true">${t.e}</div><h2>${E(pname())}</h2><p>${t.hero || (b === 'j' ? 'Pick a game and play! Every right answer makes your brain stronger.' : b === 'm' ? 'Explore the islands. Clear levels to light up the trail!' : 'Train each thinking skill, then take the timed test.')}</p></div>
      <button type="button" class="card pl-testbtn"><span aria-hidden="true">⏱️</span><span><b>${E(t.test)}</b><small>${b === 'j' ? 'Play all the games in one fun challenge' : 'Every skill in one timed run'}${bt.length ? ` · Best ${Math.max(...bt.map(x => x.pct))}%` : ''}</small></span><span class="mg-chev">›</span></button>
      ${trail}<button type="button" class="btn ghost pl-scbtn" id="plSc">📊 ${E(pname())} scorecard</button><p class="pl-note">🔓 New levels open when you get ⭐⭐ on the level before and keep finishing ${MG()._isCA() ? 'units' : 'topics'}.</p>`, { t: SU.backLabel, go: () => SU.back() });
    el.querySelectorAll('[data-g]').forEach(x => x.onclick = () => { S('open'); levels(x.dataset.g); });
    $1('.pl-testbtn', el).onclick = () => { S('open'); test(); };
    $1('#plSc', el).onclick = () => { S('open'); MG().card(SU.test); };
  }

  function levels(id) {
    const g = SU.games.find(x => x.id === id), best = gst(id).best, open = openLv(id), lmax = learnLv();
    const el = frame(`<div class="pl-hero"><div class="pl-he" aria-hidden="true">${g.e}</div><h2>${E(gname(g))}</h2><p>${E(g.d)}</p></div>
      <div class="pl-levels">${[1, 2, 3, 4, 5].map(l => { const lock = l > open; const why = lock ? (l > lmax ? `Finish more ${MG()._isCA() ? 'units' : 'topics'}` : 'Get ⭐⭐ on the level before') : '';
        return `<button type="button" class="pl-lvl${lock ? ' lock' : ''}" data-l="${l}" ${lock ? 'disabled' : ''}><b>${lock ? '🔒' : l}</b><span>${lock ? E(why) : starsTxt(best[l] || 0)}</span></button>`; }).join('')}</div>`, { t: pname(), go: hub });
    el.querySelectorAll('[data-l]').forEach(x => x.onclick = () => { S('open'); play(id, +x.dataset.l); });
  }

  function play(id, lvl) {
    const g = SU.games.find(x => x.id === id);
    runSet(Array.from({ length: PER_ROUND }, () => ({ g: id, lvl })), { tag: () => `Level ${lvl}`, back: { t: gname(g), go: () => levels(id) }, onEnd: res => {
      const sc = res.reduce((t, r) => t + r.part, 0) / res.length, stars = sc >= .8 ? 3 : sc >= .6 ? 2 : sc >= .4 ? 1 : 0, st = gst(id);
      const before = openLv(id); st.best[lvl] = Math.max(st.best[lvl] || 0, stars); round_(sc); persist();
      try { addXP(Math.round(sc * 10)); } catch (e) {}
      const opened = openLv(id) > before;
      const el = frame(`<div class="card pl-end"><div class="pl-he" aria-hidden="true">${g.e}</div><h2>${stars === 3 ? 'Superb!' : stars === 2 ? 'Great job!' : stars === 1 ? 'Good try!' : 'Keep practising!'}</h2><div class="pl-bigstars">${starsTxt(stars)}</div>
        <p>${Math.round(sc * 100)}% · Level ${lvl}</p>${opened ? `<p class="pl-unlock">🔓 Level ${lvl + 1} unlocked!</p>` : lvl < 5 && stars < 2 ? '<p class="sub">Get ⭐⭐ to open the next level.</p>' : ''}
        <button class="btn" type="button" id="plAgain">${opened ? `Play level ${lvl + 1} ▶` : 'Play again ▶'}</button><div style="height:8px"></div><button class="btn ghost" type="button" id="plLv">← Levels</button></div>`, { t: gname(g), go: () => levels(id) });
      if (stars >= 2) burst($1('.pl-end', el), 22);
      $1('#plAgain').onclick = () => { S('open'); play(id, opened ? lvl + 1 : lvl); };
      $1('#plLv').onclick = () => { S('tap'); levels(id); };
    } });
  }

  /* ---------- ⏱️ Brain Test: one round through every skill ---------- */
  function test() {
    const b = band(), t = SU.theme[b], L = games();
    const lvl = id => Math.max(1, Math.min(openLv(id), learnLv()));
    const plan = L.map(g => ({ g: g.id, lvl: lvl(g.id) }));
    const el = frame(`<div class="card pl-hero"><div class="pl-he" aria-hidden="true">⏱️</div><h2>${E(t.test)}</h2>
      <p>${plan.length} challenges, one from every game: ${L.map(g => g.e).join(' ')}</p><p class="sub">${b === 'j' ? 'Take your time and have fun!' : 'Work fast but carefully. Some challenges have a timer.'}</p>
      <button class="btn" type="button" id="plStart">Start ▶</button></div><div class="card mg-note">ℹ️ This is a practice test for fun. It shows how you did on these challenges today. ${SU.id === 'iq' ? 'It is not an official IQ test and gives no IQ number.' : 'It is not a psychological assessment and gives no score number for you as a person.'}</div>`, { t: pname(), go: hub });
    $1('#plStart').onclick = () => { S('open'); runSet(plan, { title: `<span>⏱️ ${E(t.test)}</span>`, back: { t: pname(), go: hub }, onEnd: res => result(res) }); };
    function result(res) {
      const sec = {}; res.forEach(r => { const g = SU.games.find(x => x.id === r.g); sec[g.skill] = sec[g.skill] || []; sec[g.skill].push(r.part); });
      const pct = Math.round(res.reduce((s, r) => s + r.part, 0) / res.length * 100);
      const secP = Object.fromEntries(Object.entries(sec).map(([k, v]) => [k, Math.round(v.reduce((a, c) => a + c, 0) / v.length * 100)]));
      const m = M(); m[SU.store] = (m[SU.store] || []).concat({ at: Date.now(), pct, sec: secP }).slice(-12); round_(pct / 100); persist();
      try { addXP(Math.round(pct / 5)); } catch (e) {}
      const word = pct >= 85 ? ['🏆', 'Brilliant!'] : pct >= 70 ? ['🌟', 'Sharp thinking!'] : pct >= 50 ? ['⭐', 'Good going!'] : ['🧭', 'Nice start!'];
      const best = Object.entries(secP).sort((a, c) => c[1] - a[1]);
      const hist = m[SU.store].map(x => x.pct);
      const el2 = frame(`<div class="card pl-end"><div class="pl-he" aria-hidden="true">${word[0]}</div><h2>${word[1]}</h2><div class="pl-ring" style="--p:${pct}"><b>${pct}%</b></div>
        <div class="pl-secs">${Object.entries(secP).map(([k, v]) => `<div class="mg-row"><span>${E(k)}</span><div class="mg-bar"><i style="width:${v}%"></i></div><b>${v}%</b></div>`).join('')}</div>
        ${best.length > 1 && best[0][1] > best[best.length - 1][1] ? `<p class="sub">💪 Strongest: ${E(best[0][0])} · 🎯 Practise: ${E(best[best.length - 1][0])}</p>` : ''}
        ${hist.length > 1 ? `<p class="sub">Your last ${hist.length} tests: ${hist.join('% → ')}%</p>` : ''}
        <button class="btn" type="button" id="plHub">Back to ${E(pname())}</button></div>`, { t: pname(), go: hub });
      if (pct >= 70) burst($1('.pl-end', el2), 24);
      $1('#plHub').onclick = () => { S('tap'); hub(); };
    }
  }

  /* ---------- 🔥 Daily Mind Workout: one challenge from every practice ---------- */
  async function workout() {
    const ids = (MG().TESTS || []).map(t => t.id).filter(id => SUITES[id]);
    if (window.MindPool) await Promise.all(ids.map(id => MindPool.load(id)));
    const plan = ids.map(id => { use(id); const L = games(), g = L[Math.floor(Math.random() * L.length)]; return { s: id, g: g.id, lvl: Math.max(1, Math.min(openLv(g.id), learnLv())) }; });
    use(ids[0]);
    const home = { t: 'Mind Gym', go: () => MG().open() };
    runSet(plan, { title: '<span>🔥 Daily Mind Workout</span>', back: home, onEnd: res => {
      const m = M(), d = new Date(), today = d.toISOString().slice(0, 10), y = new Date(d - 864e5).toISOString().slice(0, 10), w = m.workout || {};
      if (w.day !== today) m.workout = { day: today, streak: w.day === y ? (w.streak || 0) + 1 : 1 };
      const right = res.filter(r => r.ok).length; persist(); try { addXP(right * 3); } catch (e) {}
      use(ids[0]);
      const el = frame(`<div class="card pl-end"><div class="pl-he" aria-hidden="true">🔥</div><h2>${right === res.length ? 'Perfect workout!' : right >= 3 ? 'Great workout!' : 'Workout done!'}</h2>
        <p class="pl-bigstars">${m.workout.streak}-day streak</p>
        <div class="pl-secs">${plan.map((p, k) => { const t = MG().TESTS.find(x => x.id === p.s); return `<div class="mg-row"><span>${t.e} ${E(t.n)}</span><b>${res[k] && res[k].ok ? '✅' : '🔁'}</b></div>`; }).join('')}</div>
        <p class="sub">${right} of ${res.length} right · +${right * 3} ⭐ · Come back tomorrow to grow your streak!</p>
        <button class="btn" type="button" id="plHome">Back to Mind Gym</button></div>`, home);
      if (right >= 3) burst($1('.pl-end', el), 24);
      $1('#plHome').onclick = () => { S('tap'); MG().open(); };
    } });
  }

  let css = false;
  function style() {
    if (css) return; css = true;
    D.head.insertAdjacentHTML('beforeend', `<style id="plCss">
      .pl-title{color:#fff;font-weight:900;margin:2px 0 8px}
      .pl-hero{text-align:center;color:inherit}.pl-hero h2{margin:4px 0}.pl-he{font-size:52px;animation:mpPop .5s both}
      .pl-j .pl-hero,.pl-m .pl-hero,.pl-s .pl-hero{background:var(--plh);border-radius:22px;padding:14px;margin-bottom:12px;color:#fff}
      .pl-j{--plh:linear-gradient(135deg,#ff5fa2,#ffb13d);--plc:#ff5fa2}.pl-m{--plh:linear-gradient(135deg,#0f8f8a,#2b6cff);--plc:#0f8f8a}.pl-s{--plh:linear-gradient(135deg,#1d2440,#3a2f7a);--plc:#6d4aff}
      .pl-testbtn{display:flex;gap:12px;align-items:center;width:100%;text-align:left;border:0;cursor:pointer;font:inherit;background:linear-gradient(135deg,#ffe27a,#ffb13d);color:#3a2a00}.pl-testbtn>span:first-child{font-size:32px}.pl-testbtn span:nth-child(2){flex:1;display:flex;flex-direction:column}.pl-testbtn small{opacity:.85}
      .pl-games{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pl-game{display:flex;flex-direction:column;align-items:flex-start;gap:4px;border:0;border-radius:20px;padding:14px;background:#fff;cursor:pointer;font:inherit;color:#1f2d33;text-align:left;box-shadow:0 4px 14px rgba(0,0,0,.12);border-bottom:5px solid var(--plc)}
      .pl-ge{font-size:36px}.pl-gt{display:flex;flex-direction:column;gap:2px}.pl-gt b{font-size:16px}.pl-gt small{color:#667;font-size:12px}.pl-lv{color:var(--plc)!important;font-weight:800}.pl-cnt{font-size:11px!important;opacity:.8}.pl-scbtn{width:100%;margin-top:12px}.pl-s .pl-scbtn{color:#eef;border-color:#3f4a7a}
      .pl-j .pl-game{animation:plBob 3s ease-in-out infinite;animation-delay:calc(var(--k,0) * .2s)}.pl-j .pl-game:nth-child(odd){transform:rotate(-1deg)}
      .pl-s .pl-game{background:#1f2540;color:#eef;border-bottom-color:#6d4aff}.pl-s .pl-gt small{color:#aab}
      .pl-trail{position:relative;display:flex;flex-direction:column;gap:14px;padding:6px 0}.pl-trail:before{content:"";position:absolute;left:50%;top:0;bottom:0;border-left:4px dashed rgba(255,255,255,.5)}
      .pl-isl{position:relative;width:78%;align-self:flex-start}.pl-isl:nth-child(even){align-self:flex-end}.pl-isl .pl-game{width:100%;flex-direction:row;align-items:center;border-radius:40px 20px 40px 20px;background:linear-gradient(135deg,#fffbe8,#e6fff7)}
      .pl-note{color:#fff;opacity:.85;font-size:13px;text-align:center;margin:12px 4px 20px}
      .pl-levels{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}.pl-lvl{display:flex;flex-direction:column;align-items:center;gap:4px;border:0;border-radius:16px;padding:12px 4px;background:#fff;cursor:pointer;font:inherit;box-shadow:0 3px 10px rgba(0,0,0,.12)}
      .pl-lvl b{font-size:24px;color:var(--plc)}.pl-lvl span{font-size:11px;text-align:center}.pl-lvl.lock{opacity:.6;cursor:default}
      .pl-card{position:relative}.pl-top{display:flex;justify-content:space-between;font-weight:800;font-size:14px;color:var(--plc)}.pl-card .mg-bar i{background:var(--plc)}
      .pl-s .pl-card{background:#161b30;color:#e8ebff}.pl-s .pl-card .sub,.pl-s .pl-card p{color:#cfd3ef}
      .pl-q{font-size:18px;font-weight:700;line-height:1.4;margin:8px 0 12px}.pl-j .pl-q{font-size:20px}
      .pl-timer{position:relative;height:10px;border-radius:9px;background:rgba(0,0,0,.08);margin:6px 0 8px;overflow:hidden}.pl-timer i{position:absolute;inset:0;background:linear-gradient(90deg,#21b573,#ffc43d);transform-origin:left;animation:plShrink linear forwards}
      .pl-timer span{position:absolute;right:6px;top:-18px;font-size:12px;font-weight:800}.pl-timer.low i{background:#ff5a5f}
      .pl-memgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:8px;margin-bottom:12px}.pl-mcard{display:flex;flex-direction:column;align-items:center;padding:8px 4px;border-radius:14px;background:#fff7e6;box-shadow:inset 0 0 0 2px #ffd98a;animation:plFlip .5s both}
      .pl-mcard span{font-weight:900;font-size:20px;color:#6d4aff}.pl-sym{font-size:30px;line-height:1.1}.pl-s .pl-mcard{background:#232a48;box-shadow:inset 0 0 0 1px #3f4a7a}.pl-s .pl-sym{color:#ffd166}
      .pl-memgrid.small .pl-mcard.ok{box-shadow:inset 0 0 0 3px #1e9e6a}.pl-memgrid.small .pl-mcard.no{box-shadow:inset 0 0 0 3px #e45}
      .pl-dots{display:flex;gap:6px;justify-content:center;margin-bottom:8px}.pl-dots i{width:12px;height:12px;border-radius:50%;background:rgba(0,0,0,.12)}.pl-dots .y{background:#1e9e6a}.pl-dots .n{background:#e45}
      .pl-bigsym{text-align:center;margin:6px 0 12px}.pl-bigsym .pl-sym{font-size:72px;display:inline-block}.pop{animation:mpPop .35s both}
      .pl-keys{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:10px}.pl-keys:not(.many){grid-template-columns:repeat(auto-fit,minmax(58px,1fr))}
      .pl-key{border:0;border-radius:14px;padding:13px 0;font-size:20px;font-weight:900;background:#fff;box-shadow:0 3px 0 rgba(0,0,0,.15),0 0 0 2px rgba(0,0,0,.06) inset;cursor:pointer;color:#1f2d33;font-family:inherit}
      .pl-key.x{background:#efeaff;font-size:15px;grid-column:span 1}.pl-key[data-k="✓"]{background:var(--plc);color:#fff;grid-column:span 2}.pl-key.hit{animation:plHit .25s}.pl-key.ok{background:#21b573;color:#fff}.pl-key.no{background:#ff5a5f;color:#fff}
      .pl-s .pl-key{background:#232a48;color:#eef;box-shadow:0 3px 0 #0b0f20}
      .pl-chips{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:6px 0}.pl-chip{min-width:34px;padding:8px 6px;border-radius:10px;background:#eef5ff;font-weight:900;font-size:22px;text-align:center;animation:mpPop .3s both;letter-spacing:1px}
      .pl-chip.hl{background:#ffc43d}.pl-s .pl-chip{background:#232a48;color:#fff;font-family:ui-monospace,monospace}
      .pl-clues{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}.pl-clue{display:flex;flex-direction:column;align-items:center;padding:4px 6px;border-radius:14px;background:rgba(255,196,61,.15)}.pl-clue .pl-scale{width:170px}.pl-eq{font-size:20px;letter-spacing:1px}.pl-eq b{color:var(--plc);margin:0 4px}.pl-mainwrap{display:flex;justify-content:center}.pl-scale.main{width:min(320px,100%)}
      .pl-stand{fill:#8a6d4a}.pl-bar{fill:#c98b3c}.pl-rope{fill:none;stroke:#8a6d4a;stroke-width:1.4}.pl-plate{fill:#e3b56b}.pl-beam{transform-origin:110px 60px;transform-box:view-box}
      .pl-pile{display:flex;flex-wrap:wrap-reverse;justify-content:center;align-content:flex-start;height:44px;font-size:15px;line-height:1.05}.pl-scale.main .pl-pile{font-size:15px}
      .pl-count{display:flex;align-items:center;justify-content:center;gap:16px;margin:8px 0}.pl-count b{font-size:24px}.pl-pm{width:48px;height:48px;border-radius:50%;border:0;font-size:26px;font-weight:900;background:var(--plc);color:#fff;cursor:pointer}
      .pl-pyr{display:flex;flex-direction:column;align-items:center;gap:6px;margin:8px 0}.pl-prow{display:flex;gap:6px}.pl-brick{min-width:52px;padding:10px 4px;border-radius:10px;background:#ffe6c2;font-weight:900;font-size:18px;text-align:center;box-shadow:inset 0 -3px 0 rgba(0,0,0,.12)}
      .pl-brick.in{border:2px dashed var(--plc);background:#fff;cursor:pointer;font-family:inherit;color:#1f2d33}.pl-brick.sel{background:#fff6c7;border-style:solid;animation:mpPulse 1.2s infinite}.pl-brick.ok{background:#d6f5e6;border-color:#1e9e6a}.pl-brick.no{background:#fde2e2;border-color:#e45}
      .pl-s .pl-brick{background:#2a3152;color:#fff}.pl-s .pl-brick.in{background:#161b30;color:#fff}
      .pl-wwrap{display:flex;justify-content:center}.pl-wheel{width:min(240px,80vw)}.pl-wwrap.spin .pl-wheel{animation:plSpin 1s cubic-bezier(.2,.9,.3,1.1) both}.pl-wseg{stroke:#fff;stroke-width:2}.pl-wseg.miss{fill:#fff;stroke:#9b5cff;stroke-dasharray:5 4;stroke-width:2.5}
      .pl-wtxt{font-weight:900;font-size:20px;fill:#1f2d33}.pl-hub{fill:#2a2350}.pl-hubt{fill:#ffd166;font-size:20px;font-weight:900}.pl-typed{text-align:center;font-size:28px;font-weight:900;margin:6px 0;color:var(--plc)}
      .pl-netwrap{display:flex;justify-content:center;margin:6px 0 12px}.pl-net{display:grid;gap:2px}.pl-nc{display:grid;place-items:center;border-radius:6px;box-shadow:inset 0 0 0 2px rgba(0,0,0,.2);animation:mpPop .4s both}.pl-csym{color:#fff;font-size:22px;text-shadow:0 1px 2px rgba(0,0,0,.4)}
      .pl-opts{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pl-opt{border:2px solid rgba(0,0,0,.1);border-radius:16px;background:#fff;padding:6px;cursor:pointer}.pl-opt.ok{border-color:#1e9e6a;background:#e6f7ef}.pl-opt.no{border-color:#e45;background:#fdeaea}
      .pl-iso{width:100%;max-width:120px;display:block;margin:0 auto}.pl-ct{fill:#fff;font-size:15px;font-weight:900;paint-order:stroke;stroke:rgba(0,0,0,.35);stroke-width:2px}
      .pl-3d{width:160px;height:150px;margin:10px auto 0;perspective:600px;touch-action:none;cursor:grab;display:grid;place-items:center}.pl-cube{position:relative;width:90px;height:90px;transform-style:preserve-3d;transition:transform .05s}
      .pl-f{position:absolute;inset:0;display:grid;place-items:center;font-size:34px;color:#fff;border:2px solid rgba(0,0,0,.25);border-radius:8px;backface-visibility:hidden}.pl-cap{text-align:center;font-size:12px;margin:4px 0 8px}
      .pl-emo{font-size:46px;display:block;text-align:center}.pl-slots,.pl-tiles{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:8px 0}
      .pl-slot{width:40px;height:46px;border:0;border-bottom:4px solid var(--plc);border-radius:8px;background:rgba(0,0,0,.04);font-size:22px;font-weight:900;cursor:pointer;color:inherit;font-family:inherit}.pl-slot.full{background:#fff6c7}
      .pl-tile{width:44px;height:48px;border:0;border-radius:12px;background:var(--plc);color:#fff;font-size:22px;font-weight:900;cursor:pointer;box-shadow:0 4px 0 rgba(0,0,0,.2);font-family:inherit;animation:mpPop .3s both}.pl-tile.used{visibility:hidden}
      .pl-slots.win .pl-slot{background:#d6f5e6;animation:plHit .4s}.pl-slots.shake{animation:mgShake .4s}.pl-row2{display:flex;gap:8px}.pl-row2 .btn{flex:1}
      .pl-s .pl-slot.full{background:#2a3152}
      .pl-msq{display:flex;gap:8px;justify-content:center;align-items:center}.pl-mgrid{display:grid;grid-template-columns:repeat(3,60px);gap:6px}.pl-mc{height:60px;display:grid;place-items:center;border-radius:12px;background:#eef1ff;font-size:22px;font-weight:900}
      .pl-mc.in{border:2px dashed var(--plc);background:#fff;cursor:pointer;font-family:inherit;color:#1f2d33}.pl-mc.sel{border-style:solid;background:#fff6c7}.pl-mc.ok{background:#d6f5e6}.pl-mc.no{background:#fde2e2;font-size:16px}
      .pl-sums{display:grid;grid-template-rows:repeat(3,60px);gap:6px}.pl-sums span{display:grid;place-items:center;font-weight:900;color:#99a}.pl-sums .ok{color:#1e9e6a}.pl-sums .no{color:#e45}
      .pl-s .pl-mc{background:#2a3152;color:#fff}.pl-s .pl-mc.in{background:#161b30;color:#fff}
      .pl-fb p{line-height:1.45}.pl-nav{display:flex;gap:8px;margin-top:8px}.pl-nav .btn{flex:1}.pl-nav span{flex:1}.pl-hist{display:flex;gap:5px;flex-wrap:wrap;justify-content:center;margin:0 0 8px}.pl-hd{min-width:28px;height:28px;border-radius:50%;border:0;display:grid;place-items:center;font-weight:900;font-size:12px;background:rgba(0,0,0,.07);color:inherit;font-family:inherit}.pl-hd.y{background:#1e9e6a;color:#fff;cursor:pointer}.pl-hd.n{background:#e45;color:#fff;cursor:pointer}.pl-hd.cur{box-shadow:0 0 0 3px var(--plc)}.pl-revtag{text-align:center;font-weight:800;color:var(--plc);margin:0 0 6px}.pl-revbody{pointer-events:none}.pl-revbody .pl-fb,.pl-revbody .pl-fb *{pointer-events:auto}.pl-end{text-align:center;position:relative}.pl-bigstars{font-size:34px;letter-spacing:4px}.pl-unlock{font-weight:900;color:#1e9e6a;font-size:18px}
      .pl-ring{--p:0;width:120px;height:120px;margin:8px auto;border-radius:50%;display:grid;place-items:center;background:conic-gradient(var(--plc) calc(var(--p)*1%),rgba(0,0,0,.08) 0)}.pl-ring b{width:92px;height:92px;border-radius:50%;background:#fff;display:grid;place-items:center;font-size:26px;color:#1f2d33}
      .pl-secs .mg-bar i{background:var(--plc)}.pl-s .pl-end{background:#161b30;color:#e8ebff}.pl-s .pl-ring b{background:#161b30;color:#fff}
      @keyframes mpPulse{50%{transform:scale(1.04)}}@keyframes mgShake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
      @keyframes plBob{50%{transform:translateY(-4px)}}@keyframes plShrink{to{transform:scaleX(0)}}@keyframes plFlip{from{transform:rotateY(90deg);opacity:0}}
      @keyframes plHit{50%{transform:scale(.9)}}@keyframes plSpin{from{transform:rotate(-200deg) scale(.6);opacity:0}}
      @media (prefers-reduced-motion:reduce){.pl-root *{animation-duration:.01s!important;animation-iteration-count:1!important}}
    </style>`);
  }
  const use = id => { SU = SUITES[id || 'iq'] || SUITES.iq; style(); };
  window.MindPlay = { hub: id => { use(id); hub(); try { if (!MG().isParent()) Nav.here('mindplay', [id || 'iq']); } catch (e) {} }, test: id => { use(id); test(); }, workout, has: id => !!SUITES[id], suite: id => SUITES[id], addSuite: def => { SUITES[def.id] = def; }, PLAY, frame, keypad, burst, timerBar, E, S, band, _style: style };
})();
