/* ================= Arcade: games that mix concepts across topics, chapters and subjects =================
   Every question, answer, pair, bucket and sequence comes straight from the reviewed course files.
   Nothing is generated except UI text. Wrong options are always the content's own options, or (for
   speed items) other answers from the same speed game, or ±n of a checked maths answer. */
(function () {
  'use strict';
  const SH = a => Games.shuffle(a);
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const E = s => esc(s);
  const rnd = n => Math.floor(Math.random() * n);
  const norm = s => String(s).trim().toLowerCase().replace(/\s+/g, ' ');
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const say = t => (typeof spk === 'function' ? spk(t) : '');
  /* timers: A11Y.timeScale() is 1 (normal), 2 (extra time) or 0 (no timer); clocks wait while the app is talking */
  const TS = () => (window.A11Y ? A11Y.timeScale() : 1);
  const HOLD = () => !!(window.A11Y && A11Y.holdClock());
  const CUE = m => { try { if (window.A11Y) A11Y.cue(m); } catch (e) {} };
  const restart = (el, cls) => { if (!el) return; el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); };

  // Options that depend on their position, and questions that depend on a passage shown elsewhere, are left out.
  const BAD_OPT = /of the above|above (all|both)|\b(both|either|neither) \(?[a-d]\)? (and|or|nor) \(?[a-d]\)?\b|\boption [a-d]\b|उपर्युक्त|उपरोक्त/i;
  const CTX_Q = /\b(the|this|above|given) (passage|extract|paragraph|excerpt)\b|अनुच्छेद के अनुसार|गद्यांश के अनुसार|उपर्युक्त|उपरोक्त|ऊपर दि(ए|या)/i;

  const BOSSES = {
    maths: ['🤖', 'Calcu-Bot'], english: ['🐲', 'The Word Dragon'], hindi: ['🐘', 'Gajraj the Grammar Giant'], sanskrit: ['🦁', 'Simha of the Sutras'],
    evs: ['🐊', 'Captain Croc'], science: ['👾', 'The Lab Blob'], social: ['🗿', 'The Stone Giant'], history: ['🦖', 'Rex of the Ages'],
    geography: ['🌋', 'King Volcano'], civics: ['🦉', 'The Rulebook Owl'], economics: ['🐗', 'The Inflation Boar'], physics: ['🛸', 'The Gravity Saucer'],
    chemistry: ['🦠', 'The Molecule Monster'], biology: ['🦕', 'Gene-o-saurus'], accountancy: ['🦈', 'The Debit Shark'], business: ['🦊', 'The Market Fox'],
    polsci: ['🦅', 'The Power Eagle'], psychology: ['🦑', 'The Mind Squid'], sociology: ['🐙', 'The Crowd Kraken'], cs: ['🐛', 'The Bug King'],
    _: ['🐉', 'The Syllabus Dragon'] };
  const SUBJ = sid => (window.Worlds && Worlds.SUBJECT_STYLE && Worlds.SUBJECT_STYLE[sid]) || { e: '📘' };
  const cap = s => String(s).charAt(0).toUpperCase() + String(s).slice(1);

  /* ---------------- timers that die with the game ---------------- */
  function makeCtx(host) {
    const c = { dead: false, ts: new Set(), is: new Set(), rs: new Set() };
    const alive = () => { if (c.dead) return false; if (!host.isConnected) { c.stop(); return false; } return true; };
    c.alive = alive;
    c.t = (f, ms) => { const id = setTimeout(() => { c.ts.delete(id); if (alive()) f(); }, ms); c.ts.add(id); return id; };
    c.iv = (f, ms) => { const id = setInterval(() => { if (alive()) f(); }, ms); c.is.add(id); return id; };
    c.raf = f => { const id = requestAnimationFrame(ts => { c.rs.delete(id); if (alive()) f(ts); }); c.rs.add(id); return id; };
    c.clearIv = id => { clearInterval(id); c.is.delete(id); };
    c.stop = () => { c.dead = true; c.ts.forEach(clearTimeout); c.is.forEach(clearInterval); c.rs.forEach(cancelAnimationFrame); c.ts.clear(); c.is.clear(); c.rs.clear(); };
    return c;
  }

  /* ---------------- pools: only content that exists ---------------- */
  async function gradeSubjects(g) {
    for (let i = 0; i < 60 && (typeof CUR === 'undefined' || !CUR || !CUR.grades); i++) await wait(100);
    let subs = [];
    try { subs = curSubjects(g) || []; } catch (e) { subs = []; }
    if (!subs.length) { try { const cu = await loadJSON('content/curriculum.json'); subs = (cu.grades && cu.grades[g] && cu.grades[g].subjects) || []; } catch (e) {} }
    return subs;
  }
  const okQ = q => q && typeof q.q === 'string' && q.q.trim() && Array.isArray(q.options) && q.options.length >= 2 && q.options.length <= 4 &&
    q.options.every(o => typeof o === 'string' && o.trim()) && new Set(q.options.map(norm)).size === q.options.length &&
    Number.isInteger(q.answer) && q.answer >= 0 && q.answer < q.options.length &&
    !q.options.some(o => BAD_OPT.test(o)) && !(CTX_Q.test(q.q) && q.q.length < 160);

  async function buildPool(scope, prog) {
    const g = +scope.grade, all = await gradeSubjects(g);
    const subs = scope.subject ? [all.find(s => s.id === scope.subject) || { id: scope.subject, name: cap(scope.subject) }] : all;
    let n = 0; prog(0, subs.length);
    const datas = await Promise.all(subs.map(s => Promise.resolve(subjectData(g, s.id)).catch(() => null).then(d => { prog(++n, subs.length); return d; })));
    const P = { quiz: [], tf: [], speed: [], match: [], sort: [], order: [], subjects: [], chapter: null, multi: false };
    datas.forEach((d, si) => {
      if (!d || !Array.isArray(d.chapters)) return;
      const s = subs[si]; let used = false;
      d.chapters.forEach((c, ci) => {
        if (scope.chapter != null && ci !== +scope.chapter) return;
        if (scope.chapter != null) P.chapter = c;
        (c.topics || []).forEach(t => {
          const src = { sid: s.id, sname: s.name || cap(s.id), se: SUBJ(s.id).e, ci, ch: c.title, tid: t.id, tt: t.title, t };
          used = true;
          (t.quiz || []).forEach(q => { if (okQ(q)) P.quiz.push({ q: q.q, options: q.options, answer: q.answer, explain: q.explain || '', src }); });
          (t.games || []).forEach(gm => {
            if (!gm || !gm.type) return;
            if (gm.type === 'truefalse') (gm.items || []).forEach(it => { if (Array.isArray(it) && typeof it[0] === 'string' && typeof it[1] === 'boolean') P.tf.push({ text: it[0], val: it[1], why: it[2] || '', src }); });
            else if (gm.type === 'speed') {
              const items = (gm.items || []).filter(it => it && typeof it.q === 'string' && it.a != null && String(it.a).trim());
              items.forEach(it => {
                const a = String(it.a), na = norm(a), wrong = new Map();
                items.forEach(o => { const s2 = String(o.a); if (norm(s2) !== na) wrong.set(norm(s2), s2); });
                if (it.check && /^\d+$/.test(a.trim())) { const v = +a; [v + 1, v - 1, v + 2, v + 10, v - 10].forEach(x => { if (x >= 0 && x !== v) wrong.set(String(x), String(x)); }); }
                if (wrong.size) P.speed.push({ q: it.q, a, wrong: [...wrong.values()], src });
              });
            } else if (gm.type === 'match') {
              const pairs = (gm.pairs || []).filter(p => Array.isArray(p) && p.length >= 2 && String(p[0]).trim() && String(p[1]).trim()).map(p => [String(p[0]), String(p[1])]);
              if (pairs.length >= 3) P.match.push({ pairs, title: gm.title || '', src });
            } else if (gm.type === 'sort') {
              const buckets = (gm.buckets || []).map(String);
              const items = (gm.items || []).filter(it => Array.isArray(it) && String(it[0]).trim() && Number.isInteger(it[1]) && it[1] >= 0 && it[1] < buckets.length).map(it => [String(it[0]), it[1]]);
              // an item text that appears in two buckets of one game would be ambiguous: drop such games
              const seen = new Map(); let clash = false; items.forEach(it => { const k = norm(it[0]); if (seen.has(k) && seen.get(k) !== it[1]) clash = true; seen.set(k, it[1]); });
              const uniq = []; const u2 = new Set(); items.forEach(it => { const k = norm(it[0]); if (!u2.has(k)) { u2.add(k); uniq.push(it); } });
              if (!clash && buckets.length >= 2 && uniq.length >= 4) P.sort.push({ buckets, items: uniq, title: gm.title || '', src });
            } else if (gm.type === 'order') {
              const items = (gm.items || []).map(String).filter(x => x.trim());
              if (items.length >= 3 && new Set(items.map(norm)).size === items.length) P.order.push({ items, prompt: gm.prompt || '', title: gm.title || '', src });
            }
          });
        });
      });
      if (used) P.subjects.push(s);
    });
    P.multi = P.subjects.length > 1;
    return P;
  }

  // Round-robin: across subjects when several, otherwise across topics, so every game mixes concepts.
  function spread(list, n, multi) {
    const by = new Map();
    SH(list).forEach(x => { const k = multi ? x.src.sid : x.src.tid; if (!by.has(k)) by.set(k, []); by.get(k).push(x); });
    const qs = SH([...by.values()]), out = [];
    while (out.length < n && qs.some(a => a.length)) for (const a of qs) if (a.length && out.length < n) out.push(a.pop());
    return out;
  }
  const spreadGames = (games, n) => spread(games, n, false);

  function memPairs(P) {
    const pick = (maxLen, want) => {
      const lists = SH(P.match).map(g => ({ tid: g.src.tid, title: g.title, src: g.src, ps: SH(g.pairs.filter(p => p[0].length <= maxLen && p[1].length <= maxLen)) }));
      const used = new Set(), out = []; let strict = true;
      for (;;) {
        let got = false; const topics = new Set();
        for (const L of lists) {
          if (out.length >= want) break;
          if (strict && topics.has(L.tid)) continue;
          while (L.ps.length) {
            const p = L.ps.shift(), a = norm(p[0]), b = norm(p[1]);
            if (a === b || used.has(a) || used.has(b)) continue;
            used.add(a); used.add(b); out.push({ l: p[0], r: p[1], src: L.src, title: L.title }); topics.add(L.tid); got = true; break;
          }
        }
        if (out.length >= want) break;
        if (!got) { if (strict) strict = false; else break; }
      }
      return out;
    };
    let r = pick(16, 8); if (r.length >= 8) return { pairs: r, cols: 4 };
    r = pick(40, 6); if (r.length >= 6) return { pairs: r, cols: 3 };
    r = pick(70, 6); if (r.length >= 6) return { pairs: r, cols: 3, small: true };
    return null;
  }
  const bucketsBig = g => g.buckets.map((b, k) => g.items.filter(it => it[1] === k).length).filter(n => n >= 3).length;
  const oddGames = P => P.sort.filter(g => bucketsBig(g) >= 2);

  /* ---------------- shared UI ---------------- */
  const srcTag = src => `<div class="arc-src">${src.se} ${E(src.sname)} · ${E(src.tt)}</div>`;
  function askQ(box, q, cb) {
    const ord = SH(q.options.map((_, k) => k));
    box.innerHTML = `${srcTag(q.src)}<div class="arc-qt">${E(q.q)} ${say(q.q)}</div><div class="arc-opts">${ord.map((k, j) => `<button class="opt arc-opt" data-k="${k}"><span class="arc-l">${'ABCD'[j]}</span><span class="arc-ot">${E(q.options[k])}</span></button>`).join('')}</div><div class="arc-x"></div>`;
    restart(box, 'arc-in');
    let done = false;
    box.querySelectorAll('.arc-opt').forEach(b => b.onclick = () => {
      if (done || b.disabled) return; done = true;
      const k = +b.dataset.k, ok = k === q.answer;
      box.querySelectorAll('.arc-opt').forEach(x => { x.disabled = true; if (+x.dataset.k === q.answer) x.classList.add('right'); });
      if (!ok) b.classList.add('wrong');
      S(ok ? 'correct' : 'wrong');
      cb(ok, k);
    });
    return {
      hide: ks => ks.forEach(k => { const b = box.querySelector(`.arc-opt[data-k="${k}"]`); if (b) { b.disabled = true; b.classList.add('arc-gone'); } }),
      x: box.querySelector('.arc-x') };
  }
  const explainHTML = (q, ok) => `<div class="arc-exp ${ok ? 'good' : 'bad'}"><b>${ok ? '🎉 Correct!' : `🤔 The answer is: ${E(q.options[q.answer])}`}</b>${q.explain ? `<p>${E(q.explain)}</p>` : ''}</div>`;
  const qMiss = q => ({ q: q.q, a: q.options[q.answer] });
  function floatText(parent, text, cls) {
    const s = document.createElement('span'); s.className = 'arc-float ' + (cls || ''); s.textContent = text; parent.appendChild(s);
    setTimeout(() => s.remove(), 1000);
  }

  /* ================= 1. Boss Battle ================= */
  function boss(st, P, ctx, fin) {
    const sids = [...new Set(P.quiz.map(q => q.src.sid))];
    const B = sids.length === 1 ? (BOSSES[sids[0]] || BOSSES._) : BOSSES._;
    const qs = spread(P.quiz, 40, P.multi);
    const MAX = 150, BASE = 10; let hp = MAX, hearts = 3, combo = 0, best = 0, hits = 0, asked = 0, i = 0; const missed = [];
    const me = (ST.profile && ST.profile.avatar) || '🦸';
    st.innerHTML = `<div class="arc-arena arc-bossar"><div class="arc-bstats"><div class="arc-hearts"></div><div class="arc-combo"></div></div>
      <div class="arc-bossface"><span class="arc-bemoji">${B[0]}</span></div><div class="arc-bname">${E(B[1])}</div>
      <div class="arc-hp"><i></i></div><div class="arc-hpt">HP <b>${MAX}</b> / ${MAX}</div><div class="arc-hero">${me}</div><span class="arc-shot">💥</span></div>
      <div class="card arc-qcard"></div>`;
    const ar = st.querySelector('.arc-bossar'), face = st.querySelector('.arc-bossface'), hpI = st.querySelector('.arc-hp i'), hpT = st.querySelector('.arc-hpt b'),
      hEl = st.querySelector('.arc-hearts'), cEl = st.querySelector('.arc-combo'), qc = st.querySelector('.arc-qcard'), shot = st.querySelector('.arc-shot');
    const draw = () => { hEl.textContent = '❤️'.repeat(hearts) + '🤍'.repeat(3 - hearts); hpI.style.transform = `scaleX(${hp / MAX})`; hpT.textContent = hp;
      hpI.classList.toggle('low', hp <= MAX * .3); cEl.textContent = combo >= 2 ? `🔥 Combo ×${combo}` : ''; };
    const end = win => {
      const stars = win ? (hearts === 3 ? 3 : 2) : (hp <= MAX / 2 ? 1 : 0);
      fin({ title: win ? `You beat ${B[1]}!` : hearts <= 0 ? `${B[1]} won this time` : `${B[1]} escaped!`, scoreText: `${hits} hits from ${asked} questions`, stars,
        lines: [`🔥 Best combo ×${best}`, `❤️ Hearts left: ${hearts}`, `🩸 Boss HP left: ${hp}`], missed });
    };
    const next = () => {
      if (i >= qs.length) return end(false);
      const q = qs[i++]; asked++;
      const h = askQ(qc, q, ok => {
        if (ok) {
          combo++; best = Math.max(best, combo); hits++;
          const mult = combo >= 6 ? 3 : combo >= 3 ? 2 : 1, dmg = BASE * mult; hp = Math.max(0, hp - dmg);
          restart(shot, 'go'); ctx.t(() => { restart(face, 'arc-hit'); floatText(face, `−${dmg}`, mult > 1 ? 'big' : ''); S('coin'); draw(); if (mult > 1) restart(cEl, 'arc-pop'); }, 280);
          h.x.innerHTML = `<div class="arc-exp good"><b>${mult > 1 ? `🔥 Combo ×${mult} hit!` : '💥 Direct hit!'}</b></div>`;
          ctx.t(() => { if (hp <= 0) { face.classList.add('arc-ko'); S('unlock'); ctx.t(() => end(true), 1100); } else next(); }, 1300);
        } else {
          combo = 0; hearts--; missed.push(qMiss(q));
          restart(ar, 'arc-atk'); restart(st, 'arc-quake'); draw();
          h.x.innerHTML = explainHTML(q, false) + `<button class="btn mint arc-next">${hearts > 0 ? 'Continue ▶' : 'See results ▶'}</button>`;
          h.x.querySelector('.arc-next').onclick = () => { S('tap'); hearts > 0 ? next() : end(false); };
          ctx.t(() => h.x.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 150);
        }
      });
    };
    draw(); next();
  }

  /* ================= 2. Lightning Round ================= */
  function lightning(st, P, ctx, fin, key) {
    const all = [...P.tf.map(x => ({ k: 'tf', ...x })), ...P.speed.map(x => ({ k: 'sp', ...x }))];
    let items = SH(all), idx = 0, score = 0, streak = 0, best = 0, right = 0, wrong = 0, lock = true, t0 = 0, iv = 0, cur = null; const missed = [];
    const SC = TS(), UNTIMED = SC === 0, NQ = 20, DUR = 60000 * (SC || 1); let used = 0, last = 0;
    st.innerHTML = `<div class="arc-arena arc-light arc-lv1"><div class="arc-lines"></div><div class="arc-lhud"><span>${UNTIMED ? '📝' : '⏱'} <b class="arc-time">${UNTIMED ? '1/' + NQ : DUR / 1000}</b></span><span class="arc-lvl">Speed 1</span><span>⚡ <b class="arc-score">0</b></span></div>
      <div class="arc-tbar"><i></i></div><div class="arc-lcard"></div><div class="arc-lbtns"></div><div class="arc-count">3</div></div>`;
    const ar = st.querySelector('.arc-light'), tm = st.querySelector('.arc-time'), sc = st.querySelector('.arc-score'), bar = st.querySelector('.arc-tbar i'),
      card = st.querySelector('.arc-lcard'), btns = st.querySelector('.arc-lbtns'), cnt = st.querySelector('.arc-count'), lvl = st.querySelector('.arc-lvl');
    const level = () => { const l = streak >= 8 ? 3 : streak >= 4 ? 2 : 1; ar.classList.remove('arc-lv1', 'arc-lv2', 'arc-lv3'); ar.classList.add('arc-lv' + l); lvl.textContent = 'Speed ' + l; return l; };
    const show = () => {
      if (idx >= items.length) { items = SH(all); idx = 0; }
      cur = items[idx++];
      if (cur.k === 'tf') {
        card.innerHTML = `${srcTag(cur.src)}<div class="arc-lq">${E(cur.text)}</div>`;
        btns.className = 'arc-lbtns tf'; btns.innerHTML = `<button class="arc-lb yes" data-v="1">✅ True</button><button class="arc-lb no" data-v="0">❌ False</button>`;
      } else {
        const opts = SH([cur.a, ...SH(cur.wrong).slice(0, 2)]);
        card.innerHTML = `${srcTag(cur.src)}<div class="arc-lq">${E(cur.q)}</div>`;
        btns.className = 'arc-lbtns sp'; btns.innerHTML = opts.map(o => `<button class="arc-lb" data-a="${E(o)}">${E(o)}</button>`).join('');
      }
      restart(card, 'arc-zoom'); lock = false;
      btns.querySelectorAll('.arc-lb').forEach(b => b.onclick = () => answer(b));
    };
    const answer = b => {
      if (lock) return; lock = true;
      const ok = cur.k === 'tf' ? (b.dataset.v === '1') === cur.val : b.dataset.a === cur.a;
      if (ok) {
        right++; streak++; best = Math.max(best, streak); const pts = level(); score += pts; sc.textContent = score; S('coin');
        b.classList.add('ok'); floatText(ar, `+${pts}`, 'pts'); after(230);
      } else {
        wrong++; streak = 0; level(); S('wrong'); b.classList.add('bad'); restart(card, 'shake');
        if (cur.k === 'tf') { missed.push({ q: cur.text, a: cur.val ? 'TRUE' : 'FALSE' }); btns.querySelector(`[data-v="${cur.val ? 1 : 0}"]`).classList.add('ok');
          card.insertAdjacentHTML('beforeend', `<div class="arc-lwhy"><b>${cur.val ? 'TRUE' : 'FALSE'}.</b> ${E(cur.why)}</div>`); }
        else { missed.push({ q: cur.q, a: cur.a }); btns.querySelectorAll('.arc-lb').forEach(x => { if (x.dataset.a === cur.a) x.classList.add('ok'); }); }
        after(cur.k === 'tf' && cur.why ? 1500 : 900);
      }
    };
    const after = ms => { if (UNTIMED && right + wrong >= NQ) { ctx.t(end, ms); return; } if (UNTIMED) tm.textContent = `${right + wrong + 1}/${NQ}`; ctx.t(show, ms); };
    const end = () => {
      lock = true; ctx.clearIv(iv);
      let hi = 0; try { hi = +localStorage.getItem('arc_hi_' + key) || 0; } catch (e) {}
      const isHi = SC === 1 && score > hi; if (isHi) { try { localStorage.setItem('arc_hi_' + key, String(score)); } catch (e) {} }
      fin({ title: isHi && score > 0 ? '🏆 New high score!' : 'Time up!', scoreText: `${score} points`, stars: score >= 30 ? 3 : score >= 15 ? 2 : score >= 5 ? 1 : 0,
        lines: [`✅ ${right} right · ❌ ${wrong} wrong`, `🔥 Best streak ${best}`, `🏆 Best score: ${Math.max(hi, score)}`], missed });
    };
    const tick = () => {
      const n = Date.now(); if (!HOLD()) used += n - last; last = n;
      const left = Math.max(0, DUR - used); tm.textContent = Math.ceil(left / 1000); bar.style.transform = `scaleX(${left / DUR})`;
      ar.classList.toggle('hot', left <= 10000); if (window.A11Y) A11Y.timerTick(st, Math.ceil(left / 1000));
      if (left <= 0) end();
    };
    let n = 3; S('tap');
    const count = () => {
      n--; if (n > 0) { cnt.textContent = n; restart(cnt, 'arc-pop'); S('tap'); ctx.t(count, 700); return; }
      cnt.textContent = 'GO!'; restart(cnt, 'arc-pop'); S('unlock'); ctx.t(() => cnt.remove(), 500);
      t0 = last = Date.now(); if (!UNTIMED) iv = ctx.iv(tick, 100); else bar.parentElement.style.visibility = 'hidden'; show();
    };
    restart(cnt, 'arc-pop'); ctx.t(count, 700);
  }

  /* ================= 3. Memory Flip ================= */
  function memory(st, P, ctx, fin) {
    const M = memPairs(P), N = M.pairs.length;
    const cards = SH(M.pairs.flatMap((p, i) => [{ pid: i, side: 'L', t: p.l }, { pid: i, side: 'R', t: p.r }]));
    let open = [], moves = 0, found = 0, lock = false;
    st.innerHTML = `<div class="card arc-memhd"><span>🃏 Moves <b class="arc-mv">0</b></span><span>✨ Pairs <b class="arc-pf">0</b>/${N}</span></div>
      <p class="arc-hint">Flip a <b class="arc-cL">purple</b> card and a <b class="arc-cR">green</b> card that go together.</p>
      <div class="arc-mgrid c${M.cols}${M.small ? ' small' : ''}" style="--cols:${M.cols}">${cards.map((c, i) => {
        const L = c.t.length, fs = L > 40 ? 'xs' : L > 22 ? 's' : L > 12 ? 'm' : 'l';
        return `<button class="arc-mc arc-side-${c.side}" data-i="${i}" aria-label="Card ${i + 1}"><span class="arc-mi"><span class="arc-mf">${c.side === 'L' ? '🔮' : '🍀'}</span><span class="arc-mb arc-fs-${fs}">${E(c.t)}</span></span></button>`; }).join('')}</div>
      <div class="arc-mlog"></div>`;
    const mv = st.querySelector('.arc-mv'), pf = st.querySelector('.arc-pf'), log = st.querySelector('.arc-mlog');
    st.querySelectorAll('.arc-mc').forEach(b => b.onclick = () => {
      const c = cards[+b.dataset.i];
      if (lock || b.classList.contains('flip') || b.classList.contains('done')) return;
      b.classList.add('flip'); S('tap'); open.push([b, c]); CUE(`Card ${+b.dataset.i + 1}: ${c.t}`);
      if (open.length < 2) return;
      moves++; mv.textContent = moves; lock = true;
      const [[b1, c1], [b2, c2]] = open; open = [];
      if (c1.pid === c2.pid && c1.side !== c2.side) {
        found++; pf.textContent = found;
        ctx.t(() => { b1.classList.add('done'); b2.classList.add('done'); S('coin'); lock = false;
          const p = M.pairs[c1.pid];
          log.innerHTML = `<div class="arc-mline arc-in">✅ <b>${E(p.l)}</b> ↔ <b>${E(p.r)}</b><small>${p.src.se} ${E(p.src.tt)}</small></div>`;
          if (found === N) { S('unlock'); ctx.t(() => fin({ title: 'All pairs found!', scoreText: `${moves} moves for ${N} pairs`,
            stars: moves <= N + 3 ? 3 : moves <= 2 * N + 2 ? 2 : 1, lines: [`🧠 Perfect game would be ${N} moves`], missed: [] }), 900); }
        }, 380);
      } else {
        ctx.t(() => { restart(b1, 'arc-no'); restart(b2, 'arc-no'); S('wrong'); }, 600);
        ctx.t(() => { b1.classList.remove('flip', 'arc-no'); b2.classList.remove('flip', 'arc-no'); lock = false; }, 1150);
      }
    });
  }

  /* ================= 4. Sort Storm ================= */
  function storm(st, P, ctx, fin) {
    const games = spreadGames(P.sort, 4);
    const rounds = games.map(g => ({ g, items: SH(g.items).slice(0, 6) }));
    const total = rounds.reduce((a, r) => a + r.items.length, 0);
    let r = -1, k = 0, right = 0, active = null; const missed = [];
    st.innerHTML = `<div class="arc-round card"></div><div class="arc-sky"><span class="arc-cl c1">☁️</span><span class="arc-cl c2">☁️</span><div class="arc-drop"></div><div class="arc-ground"></div><div class="arc-sintro"></div></div><div class="arc-bks"></div><div class="arc-sfb"></div>`;
    const rd = st.querySelector('.arc-round'), sky = st.querySelector('.arc-sky'), drop = st.querySelector('.arc-drop'), bks = st.querySelector('.arc-bks'),
      fb = st.querySelector('.arc-sfb'), intro = st.querySelector('.arc-sintro');
    const nextRound = () => {
      r++; k = 0;
      if (r >= rounds.length) return fin({ title: right === total ? 'Perfect storm!' : 'Storm over!', scoreText: `${right} / ${total} caught`,
        stars: right / total >= .85 ? 3 : right / total >= .6 ? 2 : right / total >= .3 ? 1 : 0, lines: [`🌪️ ${rounds.length} round${rounds.length > 1 ? 's' : ''}`], missed });
      const R = rounds[r];
      rd.innerHTML = `${srcTag(R.g.src)}<b>Round ${r + 1} of ${rounds.length}: ${E(R.g.title)}</b>`;
      bks.style.setProperty('--n', R.g.buckets.length);
      bks.innerHTML = R.g.buckets.map((b, j) => `<button class="arc-bk b${j}" data-k="${j}"><span>🧺</span>${E(b)}</button>`).join('');
      bks.querySelectorAll('.arc-bk').forEach(b => b.onclick = () => tapB(b));
      drop.style.display = 'none'; fb.textContent = '';
      intro.innerHTML = `<b>Round ${r + 1}</b><span>Tap the right basket before it lands!</span>`; intro.style.display = ''; restart(intro, 'arc-pop'); S('unlock');
      ctx.t(() => { intro.style.display = 'none'; fall(); }, 1600);
    };
    const fall = () => {
      const R = rounds[r]; if (k >= R.items.length) return nextRound();
      const SC = TS(), it = R.items[k++], dur = Math.max(2400, 7000 * Math.pow(.85, r) * Math.pow(.95, k - 1)) * (SC || 1);
      drop.className = 'arc-drop'; drop.textContent = it[0]; drop.style.display = ''; drop.style.transition = 'none'; drop.style.transform = 'translate(-50%,0)';
      const maxY = sky.clientHeight - drop.offsetHeight - 14; let acc = 0, lastTs = performance.now();
      active = { it, y: 0, done: false };
      if (!SC) return;                                   // no timer: the item waits at the top for an answer
      const step = ts => {
        if (!active || active.done) return;
        const n = ts || performance.now(); if (!HOLD()) acc += Math.max(0, n - lastTs); lastTs = n;
        const y = Math.min(maxY, (acc / dur) * maxY); active.y = y;
        drop.style.transform = `translate(-50%,${y}px)`;
        if (y >= maxY) { land(); return; }
        ctx.raf(step);
      };
      ctx.raf(step);
    };
    const land = () => {
      const a = active; a.done = true; S('wrong'); missed.push({ q: a.it[0], a: rounds[r].g.buckets[a.it[1]] });
      drop.classList.add('splat'); fb.innerHTML = `⏰ Too slow! <b>${E(a.it[0])}</b> goes in <b>${E(rounds[r].g.buckets[a.it[1]])}</b>`;
      const ok = bks.querySelector(`[data-k="${a.it[1]}"]`); if (ok) restart(ok, 'hint');
      ctx.t(fall, 1500);
    };
    const tapB = b => {
      const a = active; if (!a || a.done) return; a.done = true;
      const good = +b.dataset.k === a.it[1];
      if (good) {
        right++; S('coin'); fb.innerHTML = `✅ <b>${E(a.it[0])}</b> → <b>${E(rounds[r].g.buckets[a.it[1]])}</b>`;
        const sr = sky.getBoundingClientRect(), br = b.getBoundingClientRect();
        const dx = br.left + br.width / 2 - (sr.left + sr.width / 2), dy = br.top + br.height / 2 - sr.top - drop.offsetHeight / 2;
        drop.style.transition = 'transform .32s ease-in, opacity .32s'; drop.style.transform = `translate(calc(-50% + ${dx}px),${dy}px) scale(.3)`; drop.classList.add('caught');
        ctx.t(() => restart(b, 'arc-bounce'), 300); ctx.t(fall, 620);
      } else {
        S('wrong'); missed.push({ q: a.it[0], a: rounds[r].g.buckets[a.it[1]] }); restart(b, 'shake'); drop.classList.add('splat');
        fb.innerHTML = `❌ <b>${E(a.it[0])}</b> goes in <b>${E(rounds[r].g.buckets[a.it[1]])}</b>`;
        const ok = bks.querySelector(`[data-k="${a.it[1]}"]`); if (ok) restart(ok, 'hint');
        ctx.t(fall, 1500);
      }
    };
    nextRound();
  }

  /* ================= 5. Odd One Out ================= */
  function odd(st, P, ctx, fin) {
    const games = SH(spreadGames(oddGames(P), 99)), ROUNDS = 8, rounds = [], seen = new Set();
    for (let tries = 0; rounds.length < ROUNDS && tries < 200; tries++) {
      const g = games[tries % games.length];
      const big = g.buckets.map((b, j) => j).filter(j => g.items.filter(it => it[1] === j).length >= 3);
      const A = big[rnd(big.length)], others = g.buckets.map((b, j) => j).filter(j => j !== A && g.items.some(it => it[1] === j));
      if (!others.length) continue;
      const B = others[rnd(others.length)];
      const three = SH(g.items.filter(it => it[1] === A)).slice(0, 3), bi = g.items.filter(it => it[1] === B), o = bi[rnd(bi.length)];
      const key = g.src.tid + '|' + three.map(x => x[0]).sort().join('|') + '|' + o[0];
      if (seen.has(key)) continue; seen.add(key);
      rounds.push({ g, A, B, odd: o[0], tiles: SH([...three.map(x => x[0]), o[0]]) });
    }
    let i = 0, right = 0; const missed = [];
    const next = () => {
      if (i >= rounds.length) return fin({ title: right === rounds.length ? 'Sharp eyes!' : 'Well spotted!', scoreText: `${right} / ${rounds.length} spotted`,
        stars: right / rounds.length >= .85 ? 3 : right / rounds.length >= .6 ? 2 : right ? 1 : 0, lines: [], missed });
      const R = rounds[i++]; toTop();
      st.innerHTML = `<div class="card arc-oddc arc-in"><span class="tag">Round ${i} of ${rounds.length}</span>${srcTag(R.g.src)}<h3>Which one doesn't belong?</h3>
        <div class="arc-tiles">${R.tiles.map((t, j) => `<button class="arc-tile t${j}" data-t="${j}">${E(t)}</button>`).join('')}</div><div class="arc-x"></div></div>`;
      const x = st.querySelector('.arc-x');
      st.querySelectorAll('.arc-tile').forEach(b => b.onclick = () => {
        if (st.querySelector('.arc-tiles.lock')) return; st.querySelector('.arc-tiles').classList.add('lock');
        const ok = R.tiles[+b.dataset.t] === R.odd;
        st.querySelectorAll('.arc-tile').forEach(t => { if (R.tiles[+t.dataset.t] === R.odd) t.classList.add('odd'); else t.classList.add('same'); });
        if (ok) { right++; S('correct'); } else { S('wrong'); restart(b, 'shake'); missed.push({ q: R.tiles.filter(t => t !== R.odd).join(', ') + ', ' + R.odd, a: `${R.odd} (${R.g.buckets[R.B]})` }); }
        x.innerHTML = `<div class="arc-exp ${ok ? 'good' : 'bad'}"><b>${ok ? '🎯 You got it!' : '🤔 Not that one.'}</b><p><b>${E(R.odd)}</b> is <b>${E(R.g.buckets[R.B])}</b>. The other three are <b>${E(R.g.buckets[R.A])}</b>.</p></div><button class="btn mint arc-next">${i < rounds.length ? 'Next ▶' : 'See results ▶'}</button>`;
        x.querySelector('.arc-next').onclick = () => { S('tap'); next(); };
      });
    };
    next();
  }

  /* ================= 6. Chain Order ================= */
  function sortable(list, onTap) {
    let drag = null, sel = null;
    const flip = (els, fn) => {
      const before = new Map(els.map(e => [e, e.getBoundingClientRect().top])); fn();
      els.forEach(e => { if (e === (drag && drag.row)) return; const d = before.get(e) - e.getBoundingClientRect().top; if (!d) return;
        e.style.transition = 'none'; e.style.transform = `translateY(${d}px)`; void e.offsetWidth; e.style.transition = 'transform .2s ease'; e.style.transform = ''; });
    };
    const clearSel = () => { if (sel) sel.classList.remove('sel'); sel = null; };
    const tap = row => {
      if (!sel) { sel = row; row.classList.add('sel'); S('tap'); return; }
      if (sel === row) { clearSel(); return; }
      const a = sel, b = row; clearSel();
      flip([...list.children], () => { const ph = document.createElement('div'); list.insertBefore(ph, a); list.insertBefore(a, b); list.insertBefore(b, ph); ph.remove(); });
      S('tap'); onTap();
    };
    list.addEventListener('pointerdown', e => {
      const row = e.target.closest('.arc-row'); if (!row || list.classList.contains('lock') || e.target.closest('button')) return;
      if (e.pointerType === 'touch' && !e.target.closest('.arc-grip')) { drag = { row, tapOnly: true, y0: e.clientY }; return; }
      e.preventDefault(); drag = { row, y0: e.clientY, moved: false };
      try { row.setPointerCapture(e.pointerId); } catch (er) {}
    });
    list.addEventListener('pointermove', e => {
      if (!drag || drag.tapOnly) return;
      let dy = e.clientY - drag.y0; const r = drag.row;
      if (!drag.moved) { if (Math.abs(dy) < 6) return; drag.moved = true; r.classList.add('drag'); r.style.transition = 'none'; clearSel(); }
      const nx = r.nextElementSibling, pv = r.previousElementSibling;
      if (dy > 0 && nx && dy > nx.offsetHeight / 2) { const top = r.offsetTop; flip([nx], () => list.insertBefore(nx, r)); drag.y0 += r.offsetTop - top; S('tap'); }
      else if (dy < 0 && pv && -dy > pv.offsetHeight / 2) { const top = r.offsetTop; flip([pv], () => list.insertBefore(r, pv)); drag.y0 += r.offsetTop - top; S('tap'); }
      dy = e.clientY - drag.y0; r.style.transform = `translateY(${dy}px)`;
    });
    const up = e => {
      if (!drag) return; const d = drag; drag = null;
      if (d.tapOnly) { if (e.type === 'pointerup' && Math.abs(e.clientY - d.y0) < 10) tap(d.row); return; }
      if (!d.moved) { if (e.type === 'pointerup') tap(d.row); return; }
      d.row.classList.remove('drag'); d.row.style.transition = 'transform .18s ease'; d.row.style.transform = ''; onTap();
    };
    list.addEventListener('pointerup', up); list.addEventListener('pointercancel', up);
  }
  function chain(st, P, ctx, fin) {
    const games = spreadGames(P.order, 3), LIMIT = 45; let r = 0, total = 0, perfect = 0; const missed = [];
    const max = games.length * 25;
    const round = () => {
      if (r >= games.length) return fin({ title: perfect === games.length ? 'Unbreakable chain!' : 'Chains complete!', scoreText: `${total} / ${max} points`,
        stars: total / max >= .7 ? 3 : total / max >= .45 ? 2 : total > 0 ? 1 : 0, lines: [`🧩 ${perfect} of ${games.length} chains right first time`], missed });
      const g = games[r++]; let order = SH(g.items.map((t, i) => i)); for (let z = 0; z < 6 && order.every((v, j) => v === j); z++) order = SH(order);
      if (order.every((v, j) => v === j)) order.reverse();
      let fails = 0; const SC = TS(), LIM = Math.round(LIMIT * (SC || 1)); let used = 0, lastT = Date.now(), iv = 0; toTop();
      st.innerHTML = `<div class="card arc-chain arc-in"><div class="arc-chd"><span class="tag">Chain ${r} of ${games.length}</span><span class="arc-tmr">${SC ? `⏱ <b>${LIM}</b>s bonus` : 'No timer'}</span></div>${srcTag(g.src)}
        <h3>${E(g.title)}</h3>${g.prompt ? `<p class="sub">${E(g.prompt)}</p>` : ''}<p class="arc-hint">Drag ⠿ to move a step, or tap two steps to swap them.</p>
        <div class="arc-list">${order.map(i => `<div class="arc-row" data-i="${i}"><span class="arc-grip" aria-hidden="true">⠿</span><span class="arc-rt">${E(g.items[i])}</span><span class="arc-mvb"><button type="button" class="arc-mvup">▲</button><button type="button" class="arc-mvdn">▼</button></span></div>`).join('')}</div>
        <div class="arc-x"></div><button class="btn arc-check">✔ Check order</button></div>`;
      const list = st.querySelector('.arc-list'), x = st.querySelector('.arc-x'), chk = st.querySelector('.arc-check'), tb = st.querySelector('.arc-tmr b');
      const left = () => { const n = Date.now(); if (SC && !HOLD()) used += n - lastT; lastT = n; return Math.max(0, LIM - Math.floor(used / 1000)); };
      if (SC) iv = ctx.iv(() => { const l = left(); tb.textContent = l; if (l <= 10) st.querySelector('.arc-tmr').classList.add('hot'); if (!l) ctx.clearIv(iv); }, 250);
      const reset = () => { list.querySelectorAll('.arc-row').forEach(rw => rw.classList.remove('good', 'bad')); x.innerHTML = ''; };
      sortable(list, reset);
      /* keyboard / screen-reader / Listen-mode alternative to dragging: ▲ ▼ buttons on every step */
      list.addEventListener('click', e => {
        const b = e.target.closest('.arc-mvup,.arc-mvdn'); if (!b) return; e.stopPropagation();
        if (list.classList.contains('lock')) return;
        const row = b.closest('.arc-row'), up = b.classList.contains('arc-mvup'), sib = up ? row.previousElementSibling : row.nextElementSibling;
        if (!sib) { CUE(`${g.items[+row.dataset.i]} is already ${up ? 'first' : 'last'}.`); return; }
        if (up) list.insertBefore(row, sib); else list.insertBefore(sib, row);
        S('tap'); reset(); b.focus();
        CUE(`${g.items[+row.dataset.i]}: now number ${[...list.children].indexOf(row) + 1} of ${list.children.length}.`);
      });
      const done = pts => {
        ctx.clearIv(iv); list.classList.add('lock'); chk.remove(); total += pts;
        x.insertAdjacentHTML('beforeend', `<button class="btn mint arc-next">${r < games.length ? 'Next chain ▶' : 'See results ▶'}</button>`);
        x.querySelector('.arc-next').onclick = () => { S('tap'); round(); };
      };
      chk.onclick = () => {
        const rows = [...list.querySelectorAll('.arc-row')], ok = rows.every((rw, j) => +rw.dataset.i === j);
        if (ok) {
          const bonus = Math.ceil(left() / 3), pts = Math.max(4, 10 + bonus - 2 * fails); if (!fails) perfect++;
          rows.forEach((rw, j) => { rw.classList.remove('bad'); ctx.t(() => rw.classList.add('good', 'arc-pop'), j * 90); }); S('unlock');
          x.innerHTML = `<div class="arc-exp good"><b>🎉 Perfect chain! +${pts} points</b><p>10 for the chain${bonus ? ` + ${bonus} time bonus` : ''}${fails ? ` − ${2 * fails} for retries` : ''}.</p></div>`;
          done(pts);
        } else {
          fails++; S('wrong');
          rows.forEach((rw, j) => { const g2 = +rw.dataset.i === j; rw.classList.toggle('good', g2); rw.classList.toggle('bad', !g2); if (!g2) restart(rw, 'shake'); });
          if (fails >= 3) {
            const fl = [...list.children], before = new Map(fl.map(e => [e, e.getBoundingClientRect().top]));
            fl.slice().sort((a, b) => a.dataset.i - b.dataset.i).forEach(e => list.appendChild(e));
            fl.forEach(e => { const d = before.get(e) - e.getBoundingClientRect().top; e.classList.remove('bad'); e.classList.add('good'); if (d) { e.style.transition = 'none'; e.style.transform = `translateY(${d}px)`; void e.offsetWidth; e.style.transition = 'transform .5s ease'; e.style.transform = ''; } });
            missed.push({ q: g.title, a: g.items.join(' → ') });
            x.innerHTML = `<div class="arc-exp bad"><b>Here is the right order.</b><p>Read it once more, top to bottom.</p></div>`; done(0);
          } else x.innerHTML = `<div class="arc-exp bad"><b>Not yet!</b><p>Green steps are in the right place. Fix the red ones. (${3 - fails} ${3 - fails === 1 ? 'try' : 'tries'} left)</p></div>`;
        }
      };
    };
    round();
  }

  /* ================= 7. Quiz Show ================= */
  const LADDER = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000], SAFE = [4, 9];
  const LV = { core: 0, important: 1, advanced: 2 };
  const coins = n => '🪙 ' + n.toLocaleString('en-IN');
  function quizshow(st, P, ctx, fin) {
    const cand = spread(P.quiz, P.quiz.length, P.multi);
    const lvl = q => { const l = q.src.t.revise && q.src.t.revise.level; return l in LV ? LV[l] : 1; };
    const main = cand.slice(0, 10).map((q, j) => [q, j]).sort((a, b) => lvl(a[0]) - lvl(b[0]) || a[1] - b[1]).map(x => x[0]);
    const spares = cand.slice(10);
    let i = 0, used = { fifty: false, gappu: false, skip: false }, cur = null, h = null; const missed = [];
    const safe = () => { let s = 0; SAFE.forEach(j => { if (i > j) s = LADDER[j]; }); return s; };
    const end = (won, lost) => fin({ title: won === 10 ? '👑 Quiz Show champion!' : lost ? 'Game over!' : 'Well played!', scoreText: coins(lost ? safe() : won ? LADDER[won - 1] : 0),
      stars: won >= 10 ? 3 : won >= 5 ? 2 : won >= 2 ? 1 : 0, lines: [`🎯 ${won} of 10 questions climbed`, lost ? `🛟 You keep your safe level: ${coins(safe())}` : ''].filter(Boolean), missed });
    const render = () => {
      cur = main[i]; toTop();
      st.innerHTML = `<div class="arc-ladder">${LADDER.map((v, j) => `<span class="${j < i ? 'won' : j === i ? 'now' : ''} ${SAFE.includes(j) ? 'safe' : ''}" title="${coins(v)}">${j + 1}</span>`).join('')}</div>
        <div class="card arc-show"><div class="arc-for"><span>Question ${i + 1}</span><b>for ${coins(LADDER[i])}</b></div>
        <div class="arc-lifes"><button class="arc-life" data-l="fifty" ${used.fifty ? 'disabled data-used="1"' : ''}>50:50</button><button class="arc-life" data-l="gappu" ${used.gappu ? 'disabled data-used="1"' : ''}>🐥 Ask Gappu</button><button class="arc-life" data-l="skip" ${used.skip ? 'disabled data-used="1"' : ''}>⏭️ Skip</button></div>
        <div class="arc-gappu"></div><div class="arc-qb"></div></div>`;
      const qb = st.querySelector('.arc-qb'), gp = st.querySelector('.arc-gappu');
      h = askQ(qb, cur, ok => {
        st.querySelectorAll('.arc-life').forEach(b => b.disabled = true);
        if (ok) {
          i++; const lad = st.querySelectorAll('.arc-ladder span'); lad[i - 1].classList.add('won', 'arc-pop');
          h.x.innerHTML = `<div class="arc-exp good"><b>🎉 Correct! You have ${coins(LADDER[i - 1])}</b></div>`; S('coin');
          if (i >= 10) { S('unlock'); ctx.t(() => end(10, false), 1400); }
          else ctx.t(render, 1300);
        } else {
          missed.push(qMiss(cur));
          h.x.innerHTML = explainHTML(cur, false) + `<button class="btn mint arc-next">See results ▶</button>`;
          h.x.querySelector('.arc-next').onclick = () => { S('tap'); end(i, true); };
          ctx.t(() => h.x.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 150);
        }
      });
      st.querySelectorAll('.arc-life').forEach(b => b.onclick = () => {
        const l = b.dataset.l; if (used[l]) return;
        if (l === 'fifty') {
          const wrongs = SH(cur.options.map((_, k) => k).filter(k => k !== cur.answer)), n = Math.min(2, wrongs.length - 1);
          if (n < 1) { toast('Only two options here. Save your 50:50!'); return; }
          used.fifty = true; b.disabled = true; b.dataset.used = '1'; h.hide(wrongs.slice(0, n)); S('unlock');
        } else if (l === 'gappu') {
          const t = cur.src.t, tip = (t.revise && t.revise.summary) || (t.learn && t.learn.points && t.learn.points[0]);
          if (!tip) { toast('Gappu has no note for this one.'); return; }
          used.gappu = true; b.disabled = true; b.dataset.used = '1'; S('unlock');
          gp.innerHTML = `<div class="arc-bubble arc-in"><span>🐥</span><div><b>Gappu remembers from “${E(t.title)}”:</b><p>${E(tip)}</p></div></div>`;
        } else if (l === 'skip') {
          if (!spares.length) { toast('No other question to swap in.'); return; }
          used.skip = true; S('tap');
          const lv = lvl(cur); let j = spares.findIndex(q => lvl(q) === lv); if (j < 0) j = 0;
          main[i] = spares.splice(j, 1)[0]; render();
        }
      });
    };
    render();
  }

  /* ================= 8. Snakes & Ladders (classic 10×10 board, 1–100) =================
     Rows go left→right, then right→left (boustrophedon). Learning twist: landing on a ladder's foot → answer right to
     climb; landing on a snake's head → answer right to escape. Exact-roll rule: you must land on 100 exactly — a roll
     that would go past 100 means you stay where you are. The board (slBoard) is shared with the live Game Rooms
     (js/live.js). LADDERS / SNAKES: KEEP IN SYNC with studyverse._live_board() in supabase/migrations/20261109_live_games.sql */
  const LADDERS = { 3: 22, 8: 30, 20: 41, 28: 76, 36: 57, 50: 69, 63: 82, 71: 92, 79: 98 };
  const SNAKES = { 17: 7, 33: 12, 47: 26, 55: 35, 66: 45, 87: 24, 93: 73, 95: 74, 99: 80 };
  const SL_RULE = '🎯 You must land on 100 exactly. Roll too big? You stay where you are.';
  const cell = n => { const i = n - 1, r = Math.floor(i / 10), col = r % 2 ? 9 - i % 10 : i % 10; return { col, row: 9 - r }; };
  const ctr = n => { const c = cell(n); return [c.col * 100 + 50, c.row * 100 + 50]; };
  /* test hook: tests may queue dice values in window.SV_TEST_DICE */
  const roll6 = () => (Array.isArray(window.SV_TEST_DICE) && window.SV_TEST_DICE.length ? +window.SV_TEST_DICE.shift() : 1 + rnd(6));
  const f1 = v => Math.round(v * 10) / 10;
  function smooth(pts) {                                    // Catmull-Rom through points → cubic Bézier path
    let d = `M${f1(pts[0][0])} ${f1(pts[0][1])}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      d += ` C${f1(p1[0] + (p2[0] - p0[0]) / 6)} ${f1(p1[1] + (p2[1] - p0[1]) / 6)},${f1(p2[0] - (p3[0] - p1[0]) / 6)} ${f1(p2[1] - (p3[1] - p1[1]) / 6)},${f1(p2[0])} ${f1(p2[1])}`;
    }
    return d;
  }
  function ladderSVG(a, b) {
    const [x1, y1] = ctr(a), [x2, y2] = ctr(b), dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L, nx = -uy * 17, ny = ux * 17;
    const sx = x1 - ux * 22, sy = y1 - uy * 22, ex = x2 + ux * 22, ey = y2 + uy * 22, LL = L + 44;
    let rungs = ''; for (let d = 26; d < LL - 10; d += 40) { const px = sx + ux * d, py = sy + uy * d; rungs += `M${f1(px + nx)} ${f1(py + ny)}L${f1(px - nx)} ${f1(py - ny)}`; }
    const rails = `M${f1(sx + nx)} ${f1(sy + ny)}L${f1(ex + nx)} ${f1(ey + ny)}M${f1(sx - nx)} ${f1(sy - ny)}L${f1(ex - nx)} ${f1(ey - ny)}`;
    return `<g class="sl-lad"><path class="sh" d="${rails}${rungs}" transform="translate(5 7)"/><path class="rg" d="${rungs}"/><path class="rl" d="${rails}"/><path class="hl" d="${rails}"/></g>`;
  }
  const SNK_COL = [['#16a34a', '#bbf7d0'], ['#dc2626', '#fecaca'], ['#7c3aed', '#ddd6fe'], ['#ea580c', '#fed7aa'], ['#0891b2', '#a5f3fc'], ['#db2777', '#fbcfe8'], ['#65a30d', '#d9f99d'], ['#2563eb', '#bfdbfe'], ['#ca8a04', '#fef08a']];
  function snakeSVG(h, t, k) {
    const [x1, y1] = ctr(h), [x2, y2] = ctr(t), dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L;
    const waves = Math.max(1, Math.round(L / 230)), A = Math.min(34, 16 + L / 28), N = waves * 10, pts = [];
    for (let i = 0; i <= N; i++) { const s = i / N, off = Math.sin(s * waves * 2 * Math.PI) * A * Math.min(1, s * 5); pts.push([x1 + dx * s + nx * off, y1 + dy * s + ny * off]); }
    const [c1, c2] = SNK_COL[k % SNK_COL.length], W = [24, 21, 17, 11], seg = Math.ceil(N / 4);
    let body = '';
    for (let j = 0; j < 4; j++) { const part = pts.slice(j * seg, Math.min(N, (j + 1) * seg) + 1); if (part.length < 2) continue; const d = smooth(part);
      body += `<path d="${d}" stroke="#1f2937" stroke-width="${W[j] + 5}"/><path d="${d}" stroke="${c1}" stroke-width="${W[j]}"/><path d="${d}" stroke="${c2}" stroke-width="${Math.max(3, W[j] * .45)}" stroke-dasharray="7 15"/>`; }
    const ang = Math.atan2(pts[0][1] - pts[1][1], pts[0][0] - pts[1][0]) * 180 / Math.PI;
    return `<g class="sl-snk"><path class="sh" d="${smooth(pts)}" transform="translate(5 7)" stroke-width="26"/>${body}
      <g transform="translate(${f1(x1)} ${f1(y1)}) rotate(${f1(ang)})"><path d="M22 0 l14 -5 m-14 5 l14 5" class="tg"/><ellipse rx="25" ry="19" fill="${c1}" stroke="#1f2937" stroke-width="4"/>
      <circle cx="8" cy="-8" r="6.5" fill="#fff"/><circle cx="8" cy="8" r="6.5" fill="#fff"/><circle cx="10" cy="-8" r="3.2" fill="#111"/><circle cx="10" cy="8" r="3.2" fill="#111"/></g></g>`;
  }
  function boardSVG() {
    let sq = '';
    for (let n = 1; n <= 100; n++) {
      const c = cell(n), x = c.col * 100, y = c.row * 100, hue = (c.row * 37 + 20) % 360;
      const fill = n === 100 ? '#86efac' : `hsl(${hue} ${(c.row + c.col) % 2 ? 90 : 80}% ${(c.row + c.col) % 2 ? 90 : 82}%)`;
      sq += `<rect x="${x}" y="${y}" width="100" height="100" fill="${fill}"/><text x="${x + 7}" y="${y + 29}" class="sl-num">${n}</text>`;
    }
    sq += `<text x="${cell(100).col * 100 + 62}" y="${cell(100).row * 100 + 86}" class="sl-ico">🏆</text><text x="${cell(1).col * 100 + 62}" y="${cell(1).row * 100 + 80}" class="sl-ico sm">🚩</text>`;
    return `<svg viewBox="0 0 1000 1000" class="sl-svg" aria-hidden="true" focusable="false">${sq}${Object.entries(LADDERS).map(([a, b]) => ladderSVG(+a, b)).join('')}${Object.entries(SNAKES).map(([a, b], k) => snakeSVG(+a, b, k)).join('')}</svg>`;
  }
  /* the board, with one token per player. players: [{ icon }]. Returns helpers to move tokens.
     t(f, ms) is the timer to use (a game ctx's c.t, or setTimeout). */
  function slBoard(host, players, t) {
    t = t || ((f, ms) => setTimeout(f, ms));
    host.innerHTML = `<div class="sl-wrap" tabindex="-1"><div class="sl-board">${boardSVG()}${players.map((p, i) => `<div class="sl-tok" data-i="${i}" style="--k:${i}"><span>${E(p.icon)}</span></div>`).join('')}</div></div>
      <button type="button" class="sl-zoom" aria-pressed="false">🔍 Bigger board</button>`;
    const wrap = host.querySelector('.sl-wrap'), board = host.querySelector('.sl-board'), toks = [...host.querySelectorAll('.sl-tok')], zb = host.querySelector('.sl-zoom'), pos = players.map(() => 1);
    const n0 = players.length;
    toks.forEach((tk, i) => { const k = n0 === 1 ? 4 : n0 === 2 ? [3, 5][i] : i; tk.style.setProperty('--ox', ((k % 3) - 1) * 30 + '%'); tk.style.setProperty('--oy', (Math.floor(k / 3) - .5) * (n0 <= 3 ? 0 : 34) + '%'); });
    const focus = (i, now) => { if (!board.classList.contains('big')) return; const tk = toks[i]; if (!tk) return; const c = cell(pos[i]), w = board.clientWidth / 10;
      wrap.scrollTo({ left: Math.max(0, c.col * w - wrap.clientWidth / 2 + w / 2), top: Math.max(0, c.row * w - wrap.clientHeight / 2 + w / 2), behavior: now ? 'auto' : 'smooth' }); };
    const place = (i, n) => { pos[i] = n; const c = cell(n), tk = toks[i]; if (tk) tk.style.transform = `translate(${c.col * 100}%,${c.row * 100}%)`; };
    zb.onclick = () => { const on = !board.classList.contains('big'); wrap.style.height = on ? wrap.clientWidth + 'px' : ''; board.classList.toggle('big', on); zb.setAttribute('aria-pressed', on); zb.textContent = on ? '🔍 Whole board' : '🔍 Bigger board'; S('tap'); requestAnimationFrame(() => focus(+(host.dataset.focus || 0), true)); };
    const api = {
      place, focus, pos,
      active: i => { toks.forEach((tk, j) => tk.classList.toggle('on', j === i)); host.dataset.focus = i; },
      hop(i, to, cb) { const step = () => { if (pos[i] === to) { focus(i); return cb && cb(); } place(i, pos[i] + (to > pos[i] ? 1 : -1)); S('tap'); t(step, 170); }; step(); },
      slide(i, to, cb) { const tk = toks[i]; if (tk) tk.classList.add('slide'); place(i, to); focus(i); t(() => { if (tk) tk.classList.remove('slide'); cb && cb(); }, 700); },
      gone: (i, off) => { if (toks[i]) toks[i].classList.toggle('off', !!off); } };
    players.forEach((p, i) => place(i, 1));
    return api;
  }

  function snakes(st, P, ctx, fin) {
    let qs = spread(P.quiz, P.quiz.length, P.multi), qi = 0;
    const nextQ = () => { if (qi >= qs.length) { qs = spread(P.quiz, P.quiz.length, P.multi); qi = 0; } return qs[qi++]; };
    const MAXR = 50;
    const me = (ST.profile && ST.profile.avatar) || '🦁', pos = [1, 1], names = ['You', 'Robo'], icons = [me, '🤖'];
    let turn = 0, turns = 0, asked = 0, right = 0, busy = false, climbs = 0, dodges = 0; const missed = [];
    st.innerHTML = `<div class="card arc-slhd"><span class="p0">${me} You: <b class="arc-p0">1</b></span><span class="arc-turn">Your turn</span><span class="p1">🤖 Robo: <b class="arc-p1">1</b></span></div>
      <div class="sl-host"></div>
      <div class="arc-dicerow"><div class="arc-die" aria-hidden="true">🎲</div><button class="btn arc-roll">🎲 Roll the dice</button></div>
      <div class="arc-slog" aria-live="polite">🪜 Land on a ladder: answer right to climb. 🐍 Land on a snake's head: answer right to escape!</div>
      <p class="sl-rule">${SL_RULE}</p><div class="card arc-slq" style="display:none"></div>`;
    const B = slBoard(st.querySelector('.sl-host'), [{ icon: me }, { icon: '🤖' }], ctx.t);
    const die = st.querySelector('.arc-die'), roll = st.querySelector('.arc-roll'), log = st.querySelector('.arc-slog'), qbox = st.querySelector('.arc-slq'), tEl = st.querySelector('.arc-turn');
    const show = w => { st.querySelector('.arc-p' + w).textContent = pos[w]; };
    const sync = w => { pos[w] = B.pos[w]; show(w); };
    const end = () => {
      const won = pos[0] >= 100 || (pos[1] < 100 && pos[0] > pos[1]);
      fin({ title: won ? '🏆 You won the race!' : pos[1] >= 100 ? '🤖 Robo won this time' : '🤖 Robo is ahead this time', scoreText: `${right} / ${asked} answers right`,
        stars: won ? (asked && right / asked >= .7 ? 3 : 2) : right ? 1 : 0,
        lines: [`📍 You reached square ${pos[0]} · Robo reached ${pos[1]}`, `🪜 Ladders climbed: ${climbs} · 🐍 Snakes escaped: ${dodges}`, pos[0] < 100 && pos[1] < 100 ? `⏱ ${MAXR} rounds played — the one closest to 100 wins.` : ''].filter(Boolean), missed });
    };
    const after = () => {
      if (pos[0] >= 100 || pos[1] >= 100) { S(pos[0] >= 100 ? 'unlock' : 'wrong'); return ctx.t(end, 900); }
      turn = 1 - turn; if (turn === 0) turns++;
      if (turns >= MAXR) return ctx.t(end, 600);
      tEl.textContent = turn ? "Robo's turn" : 'Your turn'; tEl.classList.toggle('cpu', !!turn); B.active(turn);
      if (turn) ctx.t(doRoll, 900); else { busy = false; roll.disabled = false; }
    };
    const ask = (kind, cb) => {
      const q = nextQ(); asked++;
      qbox.style.display = ''; qbox.innerHTML = `<div class="arc-sltitle">${kind === 'lad' ? '🪜 Answer right to climb the ladder!' : '🐍 Answer right to escape the snake!'}</div><div class="arc-slqb"></div>`;
      const h = askQ(qbox.querySelector('.arc-slqb'), q, ok => {
        if (ok) { right++; h.x.innerHTML = `<div class="arc-exp good"><b>${kind === 'lad' ? '🎉 Correct! Up you go!' : '🎉 Correct! You escaped the snake!'}</b></div>`; ctx.t(() => { qbox.style.display = 'none'; cb(true); }, 1100); }
        else { missed.push(qMiss(q)); h.x.innerHTML = explainHTML(q, false) + `<button class="btn mint arc-next">Continue ▶</button>`;
          h.x.querySelector('.arc-next').onclick = () => { S('tap'); qbox.style.display = 'none'; cb(false); }; }
      });
      ctx.t(() => qbox.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 120);
    };
    const land = w => {
      const p = pos[w];
      if (LADDERS[p]) {
        if (w === 0) ask('lad', ok => { if (ok) { S('unlock'); climbs++; log.textContent = `🪜 You climbed from ${p} to ${LADDERS[p]}!`; B.slide(0, LADDERS[p], () => { sync(0); after(); }); } else { log.textContent = '🪜 Not this time — you stay on ' + p + '.'; after(); } });
        else { const ok = Math.random() < .6; log.textContent = ok ? `🤖 Robo answers… and climbs to ${LADDERS[p]}!` : '🤖 Robo answers… wrong! It stays.'; ok ? B.slide(1, LADDERS[p], () => { sync(1); after(); }) : after(); }
      } else if (SNAKES[p]) {
        if (w === 0) ask('snk', ok => { if (ok) { dodges++; log.textContent = '🐍 You escaped the snake!'; after(); } else { S('wrong'); log.textContent = `🐍 Down you slide from ${p} to ${SNAKES[p]}.`; B.slide(0, SNAKES[p], () => { sync(0); after(); }); } });
        else { const ok = Math.random() < .3; log.textContent = ok ? '🐍 Snake! 🤖 Robo answers the question correctly… and escapes!' : `🐍 Snake! 🤖 Robo answers wrong… and slides down from ${p} to ${SNAKES[p]}!`; ok ? after() : B.slide(1, SNAKES[p], () => { sync(1); after(); }); }
      } else after();
    };
    const doRoll = () => {
      const w = turn, v = roll6(); restart(die, 'roll'); S('tap');
      let f = 0; const spin = ctx.iv(() => { die.textContent = 1 + rnd(6); if (++f > 6) { ctx.clearIv(spin); die.textContent = v; restart(die, 'arc-pop');
        if (pos[w] + v > 100) { log.textContent = `${icons[w]} ${names[w]} rolled a ${v} — too big! ${w ? 'Robo needs' : 'You need'} exactly ${100 - pos[w]} to reach 100. ${w ? 'It stays' : 'You stay'} on ${pos[w]}.`; S('hmm'); return ctx.t(after, 1100); }
        log.textContent = `${icons[w]} ${names[w]} rolled a ${v}.`;
        B.hop(w, pos[w] + v, () => { sync(w); land(w); }); } }, 80);
    };
    roll.onclick = () => { if (busy || turn) return; busy = true; roll.disabled = true; doRoll(); };
    B.active(0);
  }

  /* ================= menu, results, open ================= */
  const GAMES = [
    { id: 'boss', e: '🏰', n: 'Boss Battle', d: 'Right answers hit the boss. Streaks hit harder!', ok: P => P.quiz.length >= 8, c: P => `${P.quiz.length} questions`, run: boss },
    { id: 'lightning', e: '⚡', n: 'Lightning Round', d: '60 seconds of true/false and speed facts.', ok: P => P.tf.length + P.speed.length >= 10, c: P => `${P.tf.length + P.speed.length} facts`, run: lightning },
    { id: 'memory', e: '🧠', n: 'Memory Flip', d: 'Flip cards to find the matching pairs.', ok: P => !!memPairs(P), c: P => `${P.match.reduce((a, g) => a + g.pairs.length, 0)} pairs`, run: memory },
    { id: 'storm', e: '🌪️', n: 'Sort Storm', d: 'Catch falling items in the right basket.', ok: P => P.sort.length >= 1, c: P => `${P.sort.length} sorting sets`, run: storm },
    { id: 'odd', e: '🔎', n: 'Odd One Out', d: 'Spot the one that does not belong.', ok: P => oddGames(P).length >= 1, c: P => `${oddGames(P).length} sets`, run: odd },
    { id: 'chain', e: '🧩', n: 'Chain Order', d: 'Drag the steps into the right order.', ok: P => P.order.length >= 1, c: P => `${P.order.length} chains`, run: chain },
    { id: 'quizshow', e: '🎯', n: 'Quiz Show', d: '10 questions up the coin ladder, with lifelines.', ok: P => P.quiz.length >= 11, c: P => `${P.quiz.length} questions`, run: quizshow },
    { id: 'snakes', e: '🐍', n: 'Snakes & Ladders', d: 'Race Robo to 100. Answer right to climb!', ok: P => P.quiz.length >= 8, c: () => 'vs Robo 🤖', run: snakes }];

  const A = { host: null, scope: null, P: null, ctx: null, seq: 0, key: '' };
  const toTop = () => { try { const m = A.host && A.host.closest('main'); if (m) m.scrollTop = 0; window.scrollTo(0, 0); } catch (e) {} };
  const stopGame = () => { if (A.ctx) { A.ctx.stop(); A.ctx = null; } };
  const scopeKey = s => `g${s.grade}${s.subject ? '-' + s.subject : ''}${s.chapter != null ? '-c' + s.chapter : ''}`;
  const hiOf = () => { try { return +localStorage.getItem('arc_hi_' + A.key) || 0; } catch (e) { return 0; } };

  function scopeLabel() {
    const s = A.scope, P = A.P;
    if (s.chapter != null && P.chapter) return `${P.subjects[0] ? SUBJ(P.subjects[0].id).e + ' ' + E(P.subjects[0].name) + ' · ' : ''}Chapter ${E(P.chapter.n || +s.chapter + 1)}: ${E(P.chapter.title)}`;
    if (s.subject) return `Grade ${E(s.grade)} · ${P.subjects[0] ? SUBJ(P.subjects[0].id).e + ' ' + E(P.subjects[0].name) : E(cap(s.subject))} · all chapters`;
    return `Grade ${E(s.grade)} · all subjects mixed ${P.subjects.map(x => SUBJ(x.id).e).join('')}`;
  }
  function menu() {
    stopGame(); const host = A.host, P = A.P; if (!host) return;
    const list = GAMES.filter(g => { try { return g.ok(P); } catch (e) { return false; } });
    host.innerHTML = `<div class="arc-menu"><div class="card arc-hdr"><div class="arc-hdr-e">🕹️</div><div><h2>Arcade</h2><p class="sub">${scopeLabel()}</p></div></div>
      ${list.length ? `<div class="arc-grid">${list.map((g, j) => `<button class="arc-card arc-c-${g.id}" data-g="${g.id}" style="animation-delay:${j * 0.05}s"><span class="arc-ce">${g.e}</span><b>${g.n}</b><span class="arc-cd">${g.d}</span><span class="arc-cc">${g.id === 'lightning' && hiOf() ? `🏆 Best ${hiOf()}` : g.c(P)}</span></button>`).join('')}</div>`
        : `<div class="card"><p class="sub">There is not enough here yet for arcade games. Try the whole subject, or all subjects.</p></div>`}</div>`;
    toTop();
    host.querySelectorAll('.arc-card').forEach(b => b.onclick = () => { S('tap'); start(GAMES.find(g => g.id === b.dataset.g)); });
  }
  function start(game) {
    stopGame(); const host = A.host; A.ctx = makeCtx(host); const ctx = A.ctx;
    host.innerHTML = `<div class="arc-game arc-g-${game.id}" data-game="${game.id}"><div class="arc-bar"><button class="arc-quit" aria-label="Back to arcade">← Arcade</button><b>${game.e} ${game.n}</b></div><div class="arc-stage"></div></div>`;
    host.querySelector('.arc-quit').onclick = () => { S('tap'); menu(); };
    toTop();
    const st = host.querySelector('.arc-stage');
    try { game.run(st, A.P, ctx, r => { if (ctx.dead) return; results(game, r); }, A.key); }
    catch (e) { console.error(e); st.innerHTML = '<div class="card"><p class="sub">This game could not start. Please try another one.</p></div>'; }
  }
  function results(game, r) {
    stopGame(); const host = A.host; if (!host || !host.isConnected) return;
    const stars = Math.max(0, Math.min(3, r.stars | 0)), xp = 5 + stars * 5;
    try { addXP(xp, `${game.n} done!`); } catch (e) {}
    const miss = (r.missed || []).slice(0, 8);
    const conf = stars >= 2 ? `<div class="confetti">${Array.from({ length: 16 }, (_, j) => `<span style="left:${(j * 6.3 + 3) % 100}%;animation-delay:${(j % 5) * .18}s">${['🎉', '⭐', '✨', '🎊'][j % 4]}</span>`).join('')}</div>` : '';
    host.innerHTML = `<div class="card arc-res" data-game="${game.id}">${conf}<div class="arc-res-e">${game.e}</div><h2>${E(r.title)}</h2><div class="arc-res-score">${E(r.scoreText)}</div>
      <div class="bigstars">${[0, 1, 2].map(j => `<span class="${j < stars ? 'on' : ''}" style="animation-delay:${.15 + j * .25}s">⭐</span>`).join('')}</div>
      <div class="arc-xp">+${xp} ⭐ XP</div>${(r.lines || []).map(l => `<div class="arc-rl">${E(l)}</div>`).join('')}
      ${miss.length ? `<details class="arc-miss"><summary>📝 Review what you missed (${miss.length})</summary>${miss.map(m => `<div class="arc-mrow"><span>${E(m.q)}</span><b>✔ ${E(m.a)}</b></div>`).join('')}</details>` : ''}
      <button class="btn mint arc-again">🔁 Play again</button><div style="height:10px"></div><button class="btn ghost arc-back">🕹️ Back to arcade</button></div>`;
    toTop(); S(stars >= 2 ? 'unlock' : 'coin');
    host.querySelector('.arc-again').onclick = () => { S('tap'); start(game); };
    host.querySelector('.arc-back').onclick = () => { S('tap'); menu(); };
  }

  async function open(host, scope) {
    stopGame();
    if (A.host && A.host !== host && A.host._arcCleanup) { try { A.host._arcCleanup(); } catch (e) {} }
    if (!host) return;
    scope = Object.assign({}, scope || {}); if (scope.grade == null) scope.grade = ST.profile && ST.profile.grade;
    const seq = ++A.seq; A.host = host; A.scope = scope; A.key = scopeKey(scope); A.P = null;
    host._arcCleanup = () => { if (A.host === host) stopGame(); };
    host.innerHTML = `<div class="card arc-load"><div class="arc-dice"><span>🎲</span><span>🎯</span><span>🧩</span></div><b>Setting up the arcade…</b><div class="arc-lbar"><i></i></div><small class="arc-lp"></small></div>`;
    const prog = (n, t) => { if (seq !== A.seq) return; const i = host.querySelector('.arc-lbar i'), p = host.querySelector('.arc-lp');
      if (i) i.style.transform = `scaleX(${t ? Math.max(.08, n / t) : 1})`; if (p) p.textContent = t > 1 ? `${n} of ${t} subjects loaded` : n ? 'Loaded!' : 'Loading…'; };
    let P;
    try { P = await buildPool(scope, prog); } catch (e) { console.error(e); P = null; }
    if (seq !== A.seq) return;
    if (!P) { host.innerHTML = '<div class="card"><p class="sub">Could not load games right now. Please check your connection and try again.</p></div>'; return; }
    A.P = P; menu();
  }

  window.Arcade = { open, pool: buildPool, okQ, slBoard, LADDERS, SNAKES, SL_RULE, roll6, askQ, BAD_OPT };
})();
