/* ================= 🃏 Question banks as playable games (js/mindpool.js) =================
   Turns the Mind Gym question banks (content/mind/*.json) into game tiles inside each practice grid:
     Brainstorm Arena: 🔍 Picture Detective · 🧩 Pattern Builder · 🔐 Code Breaker · 👢 Odd One Out · 🗂️ Logic Detective
     Heart Compass / Friendship Galaxy / Rise-Again Rocket / Idea Factory: 💬 Story Chat (a guide character asks, you reply)
   Questions stay checked by the app (answer key in the bank). Learning still opens new questions: each game gets its
   fair share of the practice's open questions (at least 5). Unseen questions come first, then missed ones.
   window.MindPool = { load(test), ready(test), next(test, game), count(test, game) } */
(function () {
  'use strict';
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const MG = () => window.MindGym;
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const tst = m => { try { toast(m); } catch (e) {} };
  const band = () => MG()._band();

  /* ---------- banks ---------- */
  const CACHE = {}, LOADING = {}, RECENT = {};
  const load = test => CACHE[test] ? Promise.resolve() : (LOADING[test] = LOADING[test] || MG()._pool(test).then(all => { CACHE[test] = all; }).catch(() => { CACHE[test] = []; }));
  const ready = test => !!CACHE[test];
  function openList(test, g) {
    const all = CACHE[test] || [], L = all.filter(g.pool), tot = all.length || 1;
    const n = MG()._owner() ? L.length : Math.min(L.length, Math.max(5, Math.round(L.length * MG()._open(all.length) / tot)));
    return { L, open: L.slice(0, n) };
  }
  const count = (test, g) => { if (!CACHE[test]) return { all: 1, open: 0 }; const o = openList(test, g); return { all: o.L.length, open: o.open.length }; };
  function next(test, g) {
    const m = MG().state(), { open } = openList(test, g), rec = RECENT[test] = RECENT[test] || [];
    const groups = [open.filter(q => !(q.id in m.seen)), open.filter(q => m.seen[q.id] === 0), open.filter(q => m.seen[q.id] === 1)];
    let q = null;
    for (const G of groups) { const c = shuffle(G.filter(x => !rec.includes(x.id))); if (c.length) { q = c[0]; break; } }
    if (!q) q = open[Math.floor(Math.random() * open.length)];
    rec.push(q.id); if (rec.length > 12) rec.shift();
    return { g: 'pool', q, test, game: g.id };
  }
  function answer(p, ok) {
    const m = MG().state(); m.seen[p.q.id] = ok ? 1 : 0;
    const kind = p.test === 'iq' ? MG()._skillOf(p.q) : p.q.sk || (p.test === 'eq' ? 'Choose wisely' : 'Real-life choices');
    MG().record(p.test, kind, ok);
  }

  /* ---------- shared: choose, then confirm ---------- */
  function chooser(host, p, opts, cfg, done) {   // opts: [{k, html}], cfg: {btn, onPick(el,k), reveal(ok)}
    let sel = null; const q = p.q;
    const chk = $1('.pq-chk', host);
    host.querySelectorAll('[data-k]').forEach(b => b.onclick = () => {
      if (b.disabled) return; S('tap'); sel = +b.dataset.k;
      host.querySelectorAll('[data-k]').forEach(x => x.classList.toggle('on', x === b));
      if (cfg.onPick) cfg.onPick(b, sel); chk.disabled = false; chk.classList.add('ready');
    });
    chk.onclick = () => {
      if (sel == null) { tst('Choose one first'); return; }
      const ok = sel === q.a; chk.remove();
      host.querySelectorAll('[data-k]').forEach(x => { x.disabled = true; if (+x.dataset.k === q.a) x.classList.add('ok'); else if (+x.dataset.k === sel) x.classList.add('no'); });
      answer(p, ok); if (cfg.reveal) cfg.reveal(ok, sel);
      done(ok, q.why, null, null, cfg.after);
    };
  }
  const order = () => shuffle([0, 1, 2, 3]);

  /* 🔍 Picture Detective — picture puzzles with a magnifier, then the answer animates */
  function pdet(host, p, done) {
    const q = p.q, P = window.MindPics, big = !P.textOpts(q);
    host.innerHTML = `<div class="pq-case"><span class="pq-mag" aria-hidden="true">🔍</span><p class="pl-q">${E(q.q)}</p></div>${P.stem(q)}
      <div class="mg-opts${big ? ' picg' : ''} pq-pics">${order().map((k, x) => `<button type="button" class="mg-o pic pq-o" data-k="${k}"${big ? ` aria-label="Option ${'ABCD'[x]}"` : ''}><i class="pq-tag">${'ABCD'[x]}</i>${P.opt(q, k)}</button>`).join('')}</div>
      <button type="button" class="btn pq-chk" disabled>🔍 Check my answer</button>`;
    P.wire(host);
    chooser(host, p, null, { after: fb => { fb.insertAdjacentHTML('afterbegin', '<div class="mg-anim pq-anim"></div><button class="btn ghost pq-again" type="button">↻ Show me again</button>'); const a = $1('.pq-anim', fb); P.show(q, a); $1('.pq-again', fb).onclick = () => { S('open'); P.show(q, a); }; } }, done);
  }

  /* 🧩 Pattern Builder — drop the right tile into the gap of the pattern */
  const GAP = /❓|_{2,}|(?:^|(?<=[\s,(]))\?(?=[\s,)]|$)/g;
  function stemWithSlot(text) {
    let last = null, m; GAP.lastIndex = 0; while ((m = GAP.exec(text))) { last = m; if (!m[0].length) GAP.lastIndex++; }
    if (!last) return `${E(text)}<span class="pq-line"><span class="pq-slot">?</span></span>`;
    return `${E(text.slice(0, last.index))}<span class="pq-slot">?</span>${E(text.slice(last.index + last[0].length))}`;
  }
  function pattern(host, p, done) {
    const q = p.q, emo = q.k === 'picture' || q.k === 'odd-pic';
    host.innerHTML = `<p class="pl-q pq-pat${emo ? ' emo' : ''}">${stemWithSlot(q.q)}</p><p class="sub pq-hint">Tap a tile to drop it into the gap.</p>
      <div class="pq-tiles${emo ? ' emo' : ''}">${order().map(k => `<button type="button" class="pq-tile sx-opt" data-k="${k}">${E(q.o[k])}</button>`).join('')}</div>
      <button type="button" class="btn pq-chk" disabled>✓ Check</button>`;
    const slot = $1('.pq-slot', host);
    chooser(host, p, null, { onPick: (b, k) => { slot.textContent = q.o[k]; slot.classList.add('full'); slot.classList.remove('pop'); void slot.offsetWidth; slot.classList.add('pop'); },
      reveal: ok => { slot.classList.add(ok ? 'ok' : 'no'); if (!ok) slot.insertAdjacentHTML('afterend', `<span class="pq-slot ok fix">${E(q.o[q.a])}</span>`); } }, done);
  }

  /* 🔐 Code Breaker — pick the code, then try the vault */
  function code(host, p, done) {
    const q = p.q;
    host.innerHTML = `<div class="pq-vault"><div class="pq-door" aria-hidden="true">🔒</div><div class="pq-lcd" aria-live="polite">_ _ _ _</div></div><p class="pl-q">${E(q.q)}</p>
      <div class="pq-dial">${order().map(k => `<button type="button" class="pq-key sx-opt" data-k="${k}">${E(q.o[k])}</button>`).join('')}</div>
      <button type="button" class="btn pq-chk" disabled>🔓 Try to unlock</button>`;
    const lcd = $1('.pq-lcd', host), door = $1('.pq-door', host);
    chooser(host, p, null, { onPick: (b, k) => { lcd.textContent = q.o[k]; },
      reveal: ok => { door.textContent = ok ? '🔓' : '🔒'; door.classList.add(ok ? 'open' : 'buzz'); lcd.classList.add(ok ? 'ok' : 'no'); if (!ok) lcd.textContent = `✔ ${q.o[q.a]}`; } }, done);
  }

  /* 👢 Odd One Out — kick the odd one out of the line-up */
  function oddout(host, p, done) {
    const q = p.q, emo = q.k === 'odd-pic';
    host.innerHTML = `<p class="pl-q">${E(q.q)}</p><div class="pq-line-up${emo ? ' emo' : ''}">${order().map(k => `<button type="button" class="pq-mate sx-opt" data-k="${k}">${E(q.o[k])}</button>`).join('')}</div>
      <p class="sub pq-hint">Tap the one that doesn’t belong.</p><button type="button" class="btn pq-chk" disabled>👢 Kick it out!</button>`;
    chooser(host, p, null, { reveal: (ok, sel) => { const b = host.querySelector(`[data-k="${sel}"]`); b.classList.add(ok ? 'gone' : 'bounce'); } }, done);
  }

  /* 🗂️ Logic Detective — a case file: read the clues, pick the answer card, solve the case */
  function logic(host, p, done) {
    const q = p.q, no = (q.id.match(/\d+$/) || ['1'])[0];
    host.innerHTML = `<div class="pq-file"><div class="pq-fh">🗂️ Case #${E(no)}</div><p class="pl-q pq-type">${E(q.q)}</p><span class="pq-stamp" aria-hidden="true"></span></div>
      <div class="pq-clues">${order().map((k, x) => `<button type="button" class="pq-clue sx-opt" data-k="${k}"><i>${'ABCD'[x]}</i>${E(q.o[k])}</button>`).join('')}</div>
      <button type="button" class="btn pq-chk" disabled>🕵️ Solve the case</button>`;
    chooser(host, p, null, { reveal: ok => { const st = $1('.pq-stamp', host); st.textContent = ok ? 'SOLVED' : 'TRY AGAIN'; st.classList.add('on', ok ? 'ok' : 'no'); } }, done);
  }

  /* 💬 Story Chat — a guide character tells the situation, you pick your reply */
  const GUIDE = { eq: ['🦉', 'Ollie the Owl', 'Mentor Asha'], sq: ['👽', 'Zip from the Galaxy', 'Coach Zara'], aq: ['👩‍🚀', 'Captain Rae', 'Coach Rae'], cq: ['🤖', 'Bolt the Robot', 'Inventor Kiran'] };
  const FACE = { happy: '😊', excited: '🤩', proud: '😎', relieved: '😌', grateful: '🙏', sad: '😢', disappointed: '😞', lonely: '🥺', angry: '😠', frustrated: '😤', annoyed: '😒',
    scared: '😨', nervous: '😬', worried: '😟', embarrassed: '😳', guilty: '😔', ashamed: '😣', jealous: '😑', surprised: '😲', bored: '🥱', confused: '😕' };
  const SCENE = [[/birthday|party|cake/i, '🎂'], [/rain|storm|thunder/i, '🌧️'], [/dog|puppy/i, '🐶'], [/cat\b|kitten/i, '🐱'], [/school|class|teacher/i, '🏫'], [/test|exam|marks|paper\b|mock/i, '📝'],
    [/phone|online|chat|instagram|post|video|app\b/i, '📱'], [/cricket|football|match|team|race|sports/i, '🏆'], [/kite/i, '🪁'], [/client|audit|office|firm|senior|partner|article/i, '💼'],
    [/tax|gst|ledger|invoice|ca\b|return/i, '🧾'], [/friend/i, '🧑‍🤝‍🧑'], [/brother|sister|cousin|mum|dad|grand|family|parents/i, '👨‍👩‍👧'], [/park|garden|plant|tree|seed/i, '🌳'],
    [/stage|sing|dance|play\b|show|speech/i, '🎤'], [/draw|paint|colour|poster|art/i, '🎨'], [/money|cash|wallet|coin|price/i, '💰'], [/night|dark|bed/i, '🌙'], [/food|lunch|snack|mango|ice cream|biscuit/i, '🍱'], [/book|read|story/i, '📚']];
  const scene = t => { const e = []; SCENE.forEach(([r, x]) => { if (e.length < 3 && r.test(t) && !e.includes(x)) e.push(x); }); return e.length ? `<div class="pq-scene" aria-hidden="true">${e.map((x, i) => `<span style="--d:${i * .15}s">${x}</span>`).join('')}</div>` : ''; };
  function story(host, p, done) {
    const q = p.q, gd = GUIDE[p.test] || GUIDE.eq, b = band(), who = b === 's' || b === 'p' ? gd[2] : gd[1];
    host.innerHTML = `<div class="pq-chat"><div class="pq-who"><span>${gd[0]}</span><b>${E(who)}</b></div>${scene(q.q)}<div class="pq-msgs"><div class="pq-b them typing"><i></i><i></i><i></i></div></div></div><div class="pq-reps"></div>`;
    const msgs = $1('.pq-msgs', host), reps = $1('.pq-reps', host);
    setTimeout(() => {
      const t = $1('.typing', msgs); t.classList.remove('typing'); t.innerHTML = `<span class="pl-q pq-say">${E(q.q)}</span>`; S('open');
      const faces = q.o.every(o => FACE[o]);
      reps.innerHTML = faces ? `<p class="sub">Tap the face that fits:</p><div class="pq-faces">${order().map(k => `<button type="button" class="pq-face sx-opt" data-k="${k}"><span aria-hidden="true">${FACE[q.o[k]]}</span>${E(q.o[k])}</button>`).join('')}</div>`
        : `<p class="sub">Your reply:</p>` + order().map(k => `<button type="button" class="pq-rep sx-opt" data-k="${k}">${E(q.o[k])}</button>`).join('');
      reps.querySelectorAll('[data-k]').forEach(btn => btn.onclick = () => {
        const k = +btn.dataset.k, ok = k === q.a; S('tap'); reps.innerHTML = '';
        msgs.insertAdjacentHTML('beforeend', `<div class="pq-b me">${FACE[q.o[k]] ? FACE[q.o[k]] + ' ' : ''}${E(q.o[k])}</div><div class="pq-b them typing"><i></i><i></i><i></i></div>`);
        setTimeout(() => { const t2 = msgs.querySelector('.typing'); t2.classList.remove('typing'); t2.innerHTML = ok ? '😊💛 That’s a wise choice!' : `🤔 Hmm… a better reply: <b>${E(q.o[q.a])}</b>`;
          answer(p, ok); done(ok, q.why); }, 700);
      });
    }, 650);
  }

  /* ---------- the game tiles ---------- */
  const IQG = [
    { id: 'pdet', e: '🔍', skill: 'Pictures', n: { j: 'Picture Detective', m: 'Picture Detective', s: 'Visual Reasoning' }, d: 'Mirrors, folds, dice, shapes and more', pool: q => !!q.pic },
    { id: 'pattern', e: '🧩', skill: 'Patterns', n: { j: 'Pattern Builder', m: 'Pattern Builder', s: 'Series & Patterns' }, d: 'Drop the missing piece into the pattern', pool: q => !q.pic && ['series', 'letters', 'machine', 'picture', 'grid'].includes(q.k) },
    { id: 'code', e: '🔐', skill: 'Codes', n: { j: 'Code Breaker', m: 'Code Breaker', s: 'Code Breaker' }, d: 'Crack the secret code and open the vault', pool: q => !q.pic && q.k === 'code' },
    { id: 'oddout', e: '👢', skill: 'Odd one out', n: { j: 'Odd One Out', m: 'Odd One Out', s: 'Odd One Out' }, d: 'Kick out the one that doesn’t belong', pool: q => !q.pic && ['odd', 'odd-word', 'odd-pic'].includes(q.k) },
    { id: 'logic', e: '🗂️', skill: 'Reasoning', n: { j: 'Logic Detective', m: 'Logic Detective', s: 'Logic Cases' }, d: 'Directions, calendars, ages and analogies', pool: q => !q.pic && ['direction', 'calendar', 'clock', 'age', 'rank', 'analogy'].includes(q.k) }];
  const STORY = id => ({ id: 'story', e: '💬', skill: id === 'eq' ? 'Choose wisely' : 'Real-life choices', n: { j: 'Story Chat', m: 'Story Chat', s: 'Real-Life Cases' }, d: 'Chat through real situations and pick the wisest reply', pool: () => true });
  const PLAYS = { pdet, pattern, code, oddout, logic, story };

  function style() {
    if (D.getElementById('pqCss')) return;
    D.head.insertAdjacentHTML('beforeend', `<style id="pqCss">
      .pq-chk{width:100%;margin-top:12px;opacity:.55;transition:opacity .2s,transform .2s}.pq-chk.ready{opacity:1;animation:mpPop .3s}
      .pq-case{display:flex;gap:8px;align-items:flex-start}.pq-mag{font-size:30px;animation:pqWob 2.4s ease-in-out infinite}
      .pq-o{position:relative}.pq-o.on{outline:4px solid var(--plc);transform:translateY(-3px) scale(1.02)}.pq-tag{position:absolute;left:6px;top:4px;font-style:normal;font-weight:900;font-size:12px;opacity:.6}
      .pq-pat{line-height:2;word-spacing:2px}.pq-pat.emo{font-size:26px}.pq-line{display:block;text-align:center}.pq-slot{display:inline-block;min-width:54px;padding:2px 10px;margin:0 2px;border:3px dashed var(--plc);border-radius:12px;text-align:center;font-weight:900;color:var(--plc);background:rgba(255,255,255,.6);line-height:1.5}
      .pq-slot.full{border-style:solid;background:#fff6c7;color:#1f2d33}.pq-slot.pop{animation:mpPop .3s}.pq-slot.ok{background:#d6f5e6;border-color:#1e9e6a;color:#1e7a52}.pq-slot.no{background:#fde2e2;border-color:#e45;text-decoration:line-through;color:#a33}.pq-slot.fix{margin-left:6px}
      .pq-tiles,.pq-dial{display:grid;grid-template-columns:1fr 1fr;gap:8px}.pq-tile,.pq-key{border:0;border-radius:16px;padding:12px 8px;background:var(--plc);color:#fff;font-weight:800;font-size:16px;cursor:pointer;font-family:inherit;box-shadow:0 4px 0 rgba(0,0,0,.22);animation:mpPop .3s both}
      .pq-tiles.emo .pq-tile{font-size:28px;background:#fff;color:#1f2d33}.pq-tile.on,.pq-key.on{visibility:visible;outline:4px solid #ffc43d}.pq-tile.ok,.pq-key.ok,.pq-mate.ok,.pq-clue.ok{background:#1e9e6a!important;color:#fff!important}.pq-tile.no,.pq-key.no,.pq-clue.no{background:#e45!important;color:#fff!important}
      .pq-hint{margin:4px 0 10px;text-align:center}
      .pq-vault{display:flex;align-items:center;gap:12px;justify-content:center;padding:12px;border-radius:18px;background:#2a2f45;margin-bottom:8px}.pq-door{font-size:44px}.pq-door.open{animation:pqOpen .7s}.pq-door.buzz{animation:mgShake .4s}
      .pq-lcd{min-width:130px;padding:10px 14px;border-radius:10px;background:#0e2a1e;color:#5dffa8;font:700 20px ui-monospace,monospace;text-align:center;letter-spacing:2px}.pq-lcd.no{color:#ff8a8a;background:#2a0e0e}
      .pq-key{background:#3a4166;font-family:ui-monospace,monospace;letter-spacing:1px}
      .pq-line-up{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pq-mate{border:0;border-radius:18px;padding:16px 8px;background:#fff;color:#1f2d33;font-weight:800;font-size:17px;cursor:pointer;font-family:inherit;box-shadow:0 4px 12px rgba(0,0,0,.12);animation:mpPop .3s both;transition:transform .5s,opacity .5s}
      .pq-line-up.emo .pq-mate{font-size:36px}.pq-mate.on{outline:4px solid var(--plc);transform:rotate(-3deg)}.pq-mate.gone{transform:translate(120px,-60px) rotate(40deg);opacity:.2}.pq-mate.bounce{animation:mgShake .4s}
      .pq-file{position:relative;padding:12px 14px 14px;border-radius:6px 18px 18px 18px;background:#fff3c4;color:#3a2a00;box-shadow:0 4px 12px rgba(0,0,0,.12);margin-bottom:10px;overflow:hidden}.pq-fh{font-weight:900;font-size:13px;letter-spacing:1px;opacity:.75}.pq-file .pl-q{color:#3a2a00}
      .pq-stamp{position:absolute;right:10px;bottom:8px;font-weight:900;font-size:22px;border:3px solid;border-radius:8px;padding:2px 8px;transform:rotate(-12deg) scale(2);opacity:0;transition:all .35s}.pq-stamp.on{opacity:.9;transform:rotate(-12deg) scale(1)}.pq-stamp.ok{color:#1e9e6a}.pq-stamp.no{color:#d33}
      .pq-clues{display:flex;flex-direction:column;gap:8px}.pq-clue{display:flex;gap:10px;align-items:center;text-align:left;border:0;border-radius:14px;padding:11px 12px;background:#fff;color:#1f2d33;font-weight:700;font-size:15px;cursor:pointer;font-family:inherit;box-shadow:0 3px 10px rgba(0,0,0,.1);animation:mpPop .3s both}
      .pq-clue i{font-style:normal;width:26px;height:26px;border-radius:50%;background:var(--plc);color:#fff;display:grid;place-items:center;flex:none;font-weight:900}.pq-clue.on{outline:3px solid var(--plc)}
      .pq-chat{border-radius:18px;background:rgba(255,255,255,.7);padding:10px}.pq-who{display:flex;align-items:center;gap:8px;margin-bottom:6px}.pq-who span{font-size:30px}.pq-msgs{display:flex;flex-direction:column;gap:8px}
      .pq-b{max-width:88%;padding:10px 12px;border-radius:16px;line-height:1.45;animation:mpPop .3s both}.pq-b.them{align-self:flex-start;background:#fff;color:#1f2d33;border-bottom-left-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,.08)}.pq-b.me{align-self:flex-end;background:var(--plc);color:#fff;border-bottom-right-radius:4px;font-weight:700}
      .pq-say{font-size:16px;margin:0}.pq-b.typing{display:flex;gap:4px}.pq-b.typing i{width:8px;height:8px;border-radius:50%;background:#99a;animation:pqDot 1s infinite}.pq-b.typing i:nth-child(2){animation-delay:.15s}.pq-b.typing i:nth-child(3){animation-delay:.3s}
      .pq-scene{display:flex;gap:10px;justify-content:center;font-size:34px;margin:2px 0 8px}.pq-scene span{animation:pqFloat 2.6s ease-in-out infinite;animation-delay:var(--d)}
      .pq-faces{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pq-face{display:flex;flex-direction:column;align-items:center;gap:4px;border:0;border-radius:18px;padding:12px 6px;background:#fff;color:#1f2d33;font-weight:800;font-size:15px;cursor:pointer;font-family:inherit;box-shadow:0 4px 12px rgba(0,0,0,.12);animation:mpPop .3s both;text-transform:capitalize}
      .pq-face>span:first-child{font-size:44px;transition:transform .2s}.pq-face:active>span:first-child{transform:scale(1.3)}.pl-s .pq-face{background:#232a48;color:#eef}
      @keyframes pqFloat{50%{transform:translateY(-6px)}}
      .pq-reps{display:flex;flex-direction:column;gap:8px;margin-top:10px}.pq-rep{border:2px solid var(--plc);border-radius:18px 18px 4px 18px;padding:10px 12px;background:#fff;color:#1f2d33;font-weight:700;font-size:15px;text-align:left;cursor:pointer;font-family:inherit;align-self:flex-end;max-width:92%;animation:mpPop .3s both}
      .pl-s .pq-tile:not(.ok):not(.no),.pl-s .pq-mate,.pl-s .pq-clue,.pl-s .pq-rep{background:#232a48;color:#eef}.pl-s .pq-tiles.emo .pq-tile{background:#232a48}.pl-s .pq-chat{background:#1b2140}.pl-s .pq-b.them{background:#2a3152;color:#eef}.pl-s .pq-slot{background:#161b30}
      .pl-s .pq-slot.full{background:#2a3152;color:#fff}
      @keyframes pqWob{50%{transform:rotate(-12deg) scale(1.1)}}@keyframes pqDot{50%{transform:translateY(-4px);opacity:.4}}@keyframes pqOpen{40%{transform:scale(1.4) rotate(-15deg)}}
    </style>`);
  }

  function boot() {
    if (!window.MindPlay || !MindPlay.suite || !MindPlay.suite('iq') || !MindPlay.suite('eq') || !MindPlay.suite('sq') || !window.MindGym) return setTimeout(boot, 200);
    style(); Object.assign(MindPlay.PLAY, PLAYS);
    const iq = MindPlay.suite('iq'); if (!iq.games.some(g => g.id === 'pdet')) iq.games.push(...IQG);
    ['eq', 'sq', 'aq', 'cq'].forEach(id => { const s = MindPlay.suite(id); if (s && !s.games.some(g => g.id === 'story')) s.games.push(STORY(id)); });
  }
  boot();
  window.MindPool = { load, ready, next, count };
})();
