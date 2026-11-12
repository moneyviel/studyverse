/* ================= 🎲 Family Fun Zone (js/family.js) — inside Parent Hub =================
   Goal: parents and children play, learn and talk together — warm, never strict or scary.
     • 🎲 Family Quiz Night: pass-the-phone. Each child gets questions from THEIR syllabus (topics they studied first),
       grown-ups get general-knowledge questions. Everyone fills ONE Family Star Jar together (team play, no ranking).
       🆘 Ask the family (one per player) removes two wrong answers and starts a family chat. A wrong answer brings a
       gentle "teach-back" prompt (the child explains, or the child teaches the grown-up). ◀ Previous / Next ▶, and
       a look-back at every question at the end. Ends with a Talk Time question and a short parenting tip.
     • 🧠 Mind Gym for grown-ups (all challenges open + 🫶 Parenting Compass), 🌍 GK challenge, 💬 Talk Time cards.
   Uses only content already in the app: content/g<grade>/<subject>.json, content/gk/*.json, content/mind/pc-s.json.
   window.Family = { hubCard(host, kids) } */
(function () {
  'use strict';
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const pick = a => a[Math.floor(Math.random() * a.length)];
  const J = p => (window.loadJSON ? loadJSON(p) : fetch(p).then(r => { if (!r.ok) throw new Error(r.status); return r.json(); }));
  const cache = {}; const get = p => cache[p] || (cache[p] = J(p).catch(e => { delete cache[p]; throw e; }));

  const TIPS = ['Tonight, tell each child one thing they tried hard at — effort, not marks.', 'When your child gets something wrong, ask “What made you think that?” before explaining.', 'Let your child teach you something this week. Children love being the expert.',
    'Put phones away for 15 minutes a day and just talk. Small, regular chats build big trust.', 'Laugh at your own mistakes out loud — it shows your child mistakes are safe.', 'Say “I’m proud of how you kept going” more than “You’re so smart”.',
    'If you lose your temper, say sorry. It teaches your child how to repair a relationship.', 'Ask about their friends and feelings, not only about homework.', 'Make one rule together this week instead of announcing it.',
    'Notice and name a kind thing your child did today.', 'Before correcting, connect: a hug or a smile first, then the talk.', 'Tell your child about a time you failed and what you learned.'];
  const BADGES = [['🦁', 'Brave Guesser', 'tried every question without fear'], ['🧠', 'Quiz Champ', 'got the most right'], ['🤝', 'Team Player', 'asked the family for help'], ['📣', 'Super Teacher', 'helped explain an answer'], ['🌟', 'Star Learner', 'learned something new tonight']];

  /* ---------- question sources ---------- */
  async function gkPool(lo) {
    const idx = await get('content/gk/index.json'), cats = shuffle(idx.categories || []).slice(0, 4);
    const lists = await Promise.all(cats.map(c => get(`content/gk/${c.id}.json`).then(d => (d.quiz || []).map(q => Object.assign({ cat: c.name, ce: c.emoji }, q))).catch(() => [])));
    return shuffle([].concat(...lists).filter(q => q.g && q.g[1] >= lo && q.g[0] <= Math.max(lo, 12) && Array.isArray(q.o) && q.o.length >= 2));
  }
  const gkQ = (q, tag) => ({ q: q.q, o: q.o, a: q.a, x: q.x || '', tag: tag || `🌍 General knowledge · ${q.ce || ''} ${q.cat || ''}` });
  async function kidPool(k) {
    const st = (k.state && k.state.st) || {}, pr = st.profile || {}, g = +pr.grade;
    if (pr.course === 'ca') { try { const L = await caPool(st); if (L.length) return L; } catch (e) {} return (await gkPool(12)).map(q => gkQ(q)); }
    if (!g) return (await gkPool(12)).map(q => gkQ(q));
    const ids = Object.keys(st.topics || {}).filter(id => id.startsWith(`g${g}-`));
    const subj = {}; ids.forEach(id => { const s = id.split('-')[1]; (subj[s] = subj[s] || []).push(id); });
    let subs = Object.keys(subj);
    if (!subs.length) { try { const cur = await get('content/curriculum.json'); subs = ((cur.grades[g] || {}).subjects || []).map(s => s.id); } catch (e) {} }
    const out = [];
    for (const s of shuffle(subs).slice(0, 3)) {
      try {
        const d = await get(`content/g${g}/${s}.json`), studied = new Set(subj[s] || []);
        const tops = [].concat(...(d.chapters || []).map(c => (c.topics || []).map(t => ({ t, c }))));
        const mine = tops.filter(x => studied.has(x.t.id)), use = mine.length ? mine : tops.slice(0, 12);
        use.forEach(({ t, c }) => (t.quiz || []).forEach(q => { if (Array.isArray(q.options) && q.options.length >= 2 && q.answer != null)
          out.push({ q: q.q, o: q.options, a: q.answer, x: q.explain || '', tag: `📚 Grade ${g} ${E(subjLabel(s))} · ${E(c.title)}`, mine: studied.has(t.id) }); }));
      } catch (e) {}
    }
    if (!out.length) return (await gkPool(g)).map(q => gkQ(q, `🌍 General knowledge (Grade ${g})`));
    return shuffle(out).sort((a, b) => (b.mine ? 1 : 0) - (a.mine ? 1 : 0));
  }
  /* CA students: MCQs from the units they studied (or the first built units of their level) */
  async function caPool(st) {
    const ca = st.ca || {}, LV = { fnd: 'foundation', int: 'inter', fin: 'final' }, NM = { foundation: 'Foundation', inter: 'Intermediate', final: 'Final' };
    const done = Object.keys(ca.units || {}), lvl = ca.level || LV[(done[0] || '').split('-')[0]] || 'foundation';
    const str = await get(`content/ca/${lvl}/structure.json`), units = [];
    (str.papers || []).forEach(pp => (pp.chapters || []).forEach(ch => (ch.units || []).forEach(u => { if (u.status === 'built' && u.file) units.push({ u, pp, ch }); })));
    const mine = units.filter(x => done.includes(x.u.id)), use = shuffle(mine.length ? mine : units.slice(0, 8)).slice(0, 3), out = [];
    for (const { u, pp } of use) {
      try { const d = await get(u.file); (d.mcqs || []).forEach(q => { if (Array.isArray(q.options) && q.answer != null) out.push({ q: q.q, o: q.options, a: q.answer, x: q.explain || '', tag: `📘 CA ${NM[lvl]} · ${E(pp.name)} · ${E(u.title)}` }); }); } catch (e) {}
    }
    return shuffle(out);
  }
  const subjLabel = s => s.charAt(0).toUpperCase() + s.slice(1);

  /* ---------- sheet ---------- */
  let sheet = null;
  function open(html) {
    style();
    if (!sheet) { sheet = D.createElement('div'); sheet.className = 'fm-sheet'; sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-modal', 'true'); D.body.appendChild(sheet); }
    sheet.innerHTML = `<div class="fm-wrap">${html}</div>`; sheet.classList.add('show'); sheet.scrollTop = 0;
    const x = $1('[data-fmx]', sheet); if (x) x.onclick = close;
    return sheet;
  }
  const FK = 'sv_fm', keep = v => { try { sessionStorage.setItem(FK, JSON.stringify(v)); } catch (e) {} }, forget = () => { try { sessionStorage.removeItem(FK); } catch (e) {} };
  function close() { forget(); if (sheet) sheet.classList.remove('show'); try { if (window.speechSynthesis) speechSynthesis.cancel(); } catch (e) {} }
  const top = (t, back) => `<div class="fm-top"><button type="button" class="fm-back" ${back ? 'id="fmBack"' : 'data-fmx'}>← ${back ? E(back) : 'Parent Hub'}</button><h2>${t}</h2></div>`;

  /* ---------- 🎲 Family Quiz Night ---------- */
  const KIDE = ['🦊', '🐼', '🐯', '🐨', '🦄', '🐸'], ADE = ['🦉', '🐘', '🦚', '🐢'];
  function setup(kids) {
    keep({ v: 'setup' });
    const ad = [{ n: 'Me', e: '🦉' }];
    const draw = () => {
      const el = open(`${top('🎲 Family Quiz Night')}
        <div class="fm-card fm-hero"><div class="fm-big">🫙⭐</div><p><b>Play together, win together!</b> Pass the phone around. Children get questions from <b>their own syllabus</b>; grown-ups get <b>general knowledge</b>. Every right answer adds a star to ONE Family Star Jar.</p></div>
        <div class="fm-card"><h3>👨‍👩‍👧 Who is playing?</h3>
          <div class="fm-pl">${ad.map((a, i) => `<span class="fm-chip ad"><span>${a.e}</span><input value="${E(a.n)}" data-ad="${i}" aria-label="Grown-up name" maxlength="14">${i ? `<button type="button" data-rm="${i}" aria-label="Remove">✕</button>` : ''}</span>`).join('')}
            ${ad.length < 4 ? '<button type="button" class="fm-chip add" id="fmAddAd">＋ Grown-up</button>' : ''}</div>
          <div class="fm-pl">${kids.map((k, i) => { const p = ((k.state || {}).st || {}).profile || {}; return `<label class="fm-chip kid"><input type="checkbox" data-kid="${i}" checked><span>${KIDE[i % KIDE.length]}</span>${E(name(k))}<small>${p.course === 'ca' ? 'CA' : p.grade ? 'Grade ' + p.grade : ''}</small></label>`; }).join('') || '<p class="fm-mut">Add a child in Parent Hub to play with them. You can still play as grown-ups!</p>'}</div></div>
        <div class="fm-card"><h3>🔁 Rounds</h3><div class="fm-seg">${[3, 5, 7].map(n => `<button type="button" class="fm-sg${n === 3 ? ' on' : ''}" data-r="${n}">${n}</button>`).join('')}</div><p class="fm-mut">One round = one question for each player.</p></div>
        <button type="button" class="fm-btn" id="fmGo">Start the game ▶</button>`);
      el.querySelectorAll('[data-ad]').forEach(x => x.oninput = () => { ad[+x.dataset.ad].n = x.value.trim() || 'Me'; });
      el.querySelectorAll('[data-rm]').forEach(x => x.onclick = () => { ad.splice(+x.dataset.rm, 1); draw(); });
      const add = $1('#fmAddAd', el); if (add) add.onclick = () => { ad.push({ n: ['Mum', 'Dad', 'Nani', 'Dadu'][ad.length] || 'Grown-up', e: ADE[ad.length % ADE.length] }); draw(); };
      el.querySelectorAll('[data-r]').forEach(x => x.onclick = () => { el.querySelectorAll('[data-r]').forEach(y => y.classList.toggle('on', y === x)); });
      $1('#fmGo', el).onclick = async () => {
        const ks = [...el.querySelectorAll('[data-kid]')].filter(x => x.checked).map(x => kids[+x.dataset.kid]);
        const rounds = +$1('.fm-sg.on', el).dataset.r;
        const players = ad.map(a => ({ n: a.n, e: a.e, kid: null })).concat(ks.map((k, i) => ({ n: name(k), e: KIDE[kids.indexOf(k) % KIDE.length], kid: k })));
        $1('#fmGo', el).textContent = 'Getting questions…'; $1('#fmGo', el).disabled = true;
        try { await play(players, rounds, kids); } catch (e) { $1('#fmGo', el).textContent = 'Could not load questions — check internet and try again'; $1('#fmGo', el).disabled = false; }
      };
    };
    draw();
  }
  const name = k => (k && (k.name || (((k.state || {}).st || {}).profile || {}).name)) || 'Child';

  async function play(players, rounds, kids, saved) {
    let turns, t = 0, log = [];
    if (saved) { turns = saved.turns; t = saved.t; log = saved.log || []; }
    else {
      const pools = await Promise.all(players.map(p => p.kid ? kidPool(p.kid) : gkPool(10).then(L => L.map(q => gkQ(q)))));
      turns = []; for (let r = 0; r < rounds; r++) players.forEach((p, i) => { const q = pools[i][r % Math.max(1, pools[i].length)]; if (q) turns.push({ p: i, q }); });
      if (!turns.length) throw new Error('none');
      players.forEach(p => { p.right = 0; p.help = 0; p.teach = 0; p.life = 1; });
    }
    const snap = () => keep({ v: 'quiz', t, log, turns, players: players.map(p => ({ n: p.n, e: p.e, kid: p.kid ? 1 : null, right: p.right, help: p.help, teach: p.teach, life: p.life })) });
    const jar = () => { const n = log.filter(x => x.ok).length; return `<div class="fm-jar" aria-label="Family Star Jar: ${n} of ${turns.length} stars"><div class="fm-jarf" style="height:${Math.round(n / turns.length * 100)}%"></div><b>🫙 ${n} / ${turns.length} ⭐</b></div>`; };
    const pass = () => {
      if (t >= turns.length) return end();
      snap();
      const P = players[turns[t].p];
      const el = open(`${top('🎲 Family Quiz Night')}${jar()}<div class="fm-card fm-pass"><div class="fm-big">${P.e}</div><h2>Pass the phone to <b>${E(P.n)}</b></h2>
        <p class="fm-mut">Question ${t + 1} of ${turns.length}. Everyone else: cheer, don’t tell the answer — unless ${E(P.n)} asks the family!</p><button type="button" class="fm-btn" id="fmReady">I’m ready ▶</button>
        ${t ? '<button type="button" class="fm-btn ghost" id="fmPrev">◀ Look at the last question</button>' : ''}</div>`);
      $1('#fmReady', el).onclick = () => { S('open'); ask(); };
      const pv = $1('#fmPrev', el); if (pv) pv.onclick = () => review(t - 1, pass);
    };
    const ask = () => {
      const T = turns[t], P = players[T.p], q = T.q, ord = shuffle(q.o.map((_, i) => i));
      const el = open(`${top('🎲 Family Quiz Night')}${jar()}<div class="fm-card fm-q"><div class="fm-who"><span>${P.e}</span><b>${E(P.n)}’s question</b><small>${q.tag}</small></div>
        <p class="pl-q fm-qt">${E(q.q)}</p><div class="fm-opts">${ord.map(k => `<button type="button" class="fm-o sx-opt" data-k="${k}">${E(q.o[k])}</button>`).join('')}</div>
        ${P.life ? '<button type="button" class="fm-life" id="fmLife">🆘 Ask the family <small>(once per game)</small></button>' : ''}<div class="fm-fb" aria-live="polite"></div></div>`);
      const life = $1('#fmLife', el);
      if (life) life.onclick = () => { S('open'); P.life = 0; P.help++; const wrong = shuffle(ord.filter(k => k !== q.a)).slice(0, Math.max(0, q.o.length - 2));
        wrong.forEach(k => { const b = el.querySelector(`.fm-o[data-k="${k}"]`); b.disabled = true; b.classList.add('gone'); });
        life.outerHTML = `<p class="fm-tip">🤝 Two answers are gone. Talk it over together for a minute — then <b>${E(P.n)}</b> decides!</p>`; };
      el.querySelectorAll('.fm-o').forEach(b => b.onclick = () => {
        const k = +b.dataset.k, ok = k === q.a; S(ok ? 'right' : 'wrong');
        el.querySelectorAll('.fm-o').forEach(x => { x.disabled = true; if (+x.dataset.k === q.a) x.classList.add('ok'); });
        if (!ok) b.classList.add('no'); if (ok) P.right++;
        const lf = $1('#fmLife', el); if (lf) lf.remove();
        log[t] = { p: T.p, q, pick: k, ok };
        const kid = !!P.kid, others = players.filter((x, i) => i !== T.p), grown = players.filter(x => !x.kid), child = players.find(x => x.kid && x !== P);
        const moment = ok ? `🌟 A star for the Family Jar! Everyone, give ${E(P.n)} a high-five ✋`
          : kid ? `💛 No worries — mistakes help us learn! ${grown.length ? `${E(grown[0].n)}, gently ask: “What made you pick that?” ` : ''}Then read the answer together.`
          : child ? `🙌 Grown-ups learn too! <b>${E(child.n)}</b>, can you explain this one to ${E(P.n)}?` : '🙌 Grown-ups learn too! Read the answer together.';
        $1('.fm-fb', el).innerHTML = `<p class="fm-v ${ok ? 'ok' : 'no'}">${ok ? '✅ Correct!' : `💡 The answer is: ${E(q.o[q.a])}`}</p>${q.x ? `<p>${E(q.x)}</p>` : ''}<p class="fm-tip">${moment}</p>
          ${!ok ? `<button type="button" class="fm-btn ghost" id="fmTaught">📣 We talked it through!</button>` : ''}
          <div class="fm-nav">${t ? '<button type="button" class="fm-btn ghost" id="fmPrev2">◀ Previous</button>' : ''}<button type="button" class="fm-btn" id="fmNext">${t + 1 < turns.length ? 'Next player ▶' : 'Open the Star Jar ▶'}</button></div>`;
        const tg = $1('#fmTaught', el); if (tg) tg.onclick = () => { S('right'); others.forEach(o => { if (o.kid || !kid) o.teach++; }); P.teach++; tg.outerHTML = '<p class="fm-tip">🎉 Talking it through is the best kind of learning. Bonus hug!</p>'; };
        const p2 = $1('#fmPrev2', el); if (p2) p2.onclick = () => { const keep = sheet.firstElementChild; review(t - 1, () => { sheet.innerHTML = ''; sheet.appendChild(keep); sheet.classList.add('show'); sheet.scrollTop = 0; }); };
        $1('#fmNext', el).onclick = () => { S('tap'); t++; pass(); };
      });
    };
    const review = (j, backFn) => {
      const draw = j2 => {
        const L2 = log[j2], P2 = players[L2.p];
        const el = open(`${top('👀 Looking back', 'Back to the game')}<div class="fm-card fm-q"><div class="fm-who"><span>${P2.e}</span><b>${E(P2.n)}’s question</b><small>${L2.q.tag}</small></div>
          <p class="pl-q fm-qt">${E(L2.q.q)}</p><div class="fm-opts">${L2.q.o.map((o, k) => `<div class="fm-o ${k === L2.q.a ? 'ok' : k === L2.pick ? 'no' : ''}">${E(o)}</div>`).join('')}</div>
          ${L2.q.x ? `<p>${E(L2.q.x)}</p>` : ''}<div class="fm-nav">${j2 > 0 ? '<button type="button" class="fm-btn ghost" id="fmRp">◀ Previous</button>' : ''}<button type="button" class="fm-btn" id="fmRn">${log[j2 + 1] && j2 + 1 < t ? 'Next ▶' : 'Back to the game ▶'}</button></div></div>`);
        $1('#fmBack', el).onclick = () => backFn();
        const rp = $1('#fmRp', el); if (rp) rp.onclick = () => draw(j2 - 1);
        $1('#fmRn', el).onclick = () => { if (log[j2 + 1] && j2 + 1 < t) draw(j2 + 1); else backFn(); };
      };
      draw(j);
    };
    const end = async () => {
      forget();
      const n = log.filter(x => x.ok).length, pct = n / turns.length;
      let talk = []; try { talk = (await get('content/mind/pc-s.json')).talk || []; } catch (e) {}
      const most = Math.max(...players.map(p => p.right));
      const badge = p => p.teach ? BADGES[3] : p.help ? BADGES[2] : p.right === most && most > 0 ? BADGES[1] : p.right ? BADGES[4] : BADGES[0];
      const el = open(`${top('🎲 Family Quiz Night')}<div class="fm-card fm-end"><div class="fm-big">${pct >= .8 ? '🏆' : pct >= .5 ? '🌟' : '💖'}</div><h2>${pct >= .8 ? 'Super family!' : pct >= .5 ? 'Great teamwork!' : 'What a fun night of learning!'}</h2>
        ${jar()}<p>Your Family Star Jar has <b>${n} ⭐</b> from ${turns.length} questions.</p>
        <div class="fm-bad">${players.map(p => { const b = badge(p); return `<div><span>${p.e}</span><b>${E(p.n)}</b><small>${b[0]} ${b[1]} — ${b[2]}</small></div>`; }).join('')}</div></div>
        ${talk.length ? `<div class="fm-card fm-talk"><h3>💬 Keep talking</h3><p class="pl-q">${E(pick(talk))}</p><p class="fm-mut">Everyone answers — grown-ups too!</p></div>` : ''}
        <div class="fm-card fm-tipc"><h3>🫶 Tip for grown-ups</h3><p>${E(pick(TIPS))}</p></div>
        <button type="button" class="fm-btn ghost" id="fmAll">👀 Look back at every question</button><button type="button" class="fm-btn" id="fmAgain">Play again ▶</button><button type="button" class="fm-btn ghost" data-fmx>Back to Parent Hub</button>`);
      if (pct >= .5) S('unlock');
      $1('#fmAgain', el).onclick = () => setup(kids);
      $1('#fmAll', el).onclick = () => review(0, end);
    };
    pass();
  }

  /* ---------- 🌍 GK challenge for grown-ups ---------- */
  async function gkSolo() {
    keep({ v: 'gk' });
    const el = open(`${top('🌍 GK challenge')}<div class="fm-card"><p>Getting questions…</p></div>`);
    let L; try { L = (await gkPool(12)).slice(0, 10).map(q => gkQ(q)); } catch (e) { $1('.fm-card', el).innerHTML = '<p>Could not load. Check your internet.</p>'; return; }
    const ans = []; let i = 0;
    const draw = () => {
      if (i >= L.length) {
        const n = ans.filter((a, k) => a === L[k].a).length;
        const e2 = open(`${top('🌍 GK challenge')}<div class="fm-card fm-end"><div class="fm-big">${n >= 8 ? '🏆' : n >= 5 ? '🌟' : '📚'}</div><h2>${n} / ${L.length}</h2><p>Share one surprising fact you learned with your child tonight!</p></div>
          <button type="button" class="fm-btn ghost" id="fmRv">👀 Look back</button><button type="button" class="fm-btn" id="fmAg">Play again ▶</button><button type="button" class="fm-btn ghost" data-fmx>Back to Parent Hub</button>`);
        $1('#fmAg', e2).onclick = gkSolo; $1('#fmRv', e2).onclick = () => { i = 0; draw(); };
        return;
      }
      const q = L[i], done = ans[i] != null;
      const e = open(`${top('🌍 GK challenge')}<div class="fm-card fm-q"><div class="fm-who"><span>🌍</span><b>Question ${i + 1} of ${L.length}</b><small>${q.tag}</small></div>
        <p class="pl-q fm-qt">${E(q.q)}</p><div class="fm-opts">${q.o.map((o, k) => `<button type="button" class="fm-o sx-opt${done && k === q.a ? ' ok' : done && k === ans[i] ? ' no' : ''}" data-k="${k}" ${done ? 'disabled' : ''}>${E(o)}</button>`).join('')}</div>
        <div class="fm-fb">${done ? `${q.x ? `<p>${E(q.x)}</p>` : ''}` : ''}</div>
        <div class="fm-nav">${i ? '<button type="button" class="fm-btn ghost" id="fmP">◀ Previous</button>' : ''}${done ? `<button type="button" class="fm-btn" id="fmN">${i + 1 < L.length ? 'Next ▶' : 'See my score ▶'}</button>` : ''}</div></div>`);
      const p = $1('#fmP', e); if (p) p.onclick = () => { i--; draw(); };
      const nx = $1('#fmN', e); if (nx) nx.onclick = () => { i++; draw(); };
      if (!done) e.querySelectorAll('.fm-o').forEach(b => b.onclick = () => { ans[i] = +b.dataset.k; S(ans[i] === q.a ? 'right' : 'wrong'); draw(); });
    };
    draw();
  }

  /* ---------- 💬 Talk Time ---------- */
  async function talkTime(i0) {
    let L = []; try { L = (await get('content/mind/pc-s.json')).talk || []; } catch (e) {}
    let i = typeof i0 === 'number' && i0 < L.length ? i0 : Math.floor(Math.random() * Math.max(1, L.length));
    const draw = () => {
      keep({ v: 'talk', i });
      const el = open(`${top('💬 Talk Time')}<div class="fm-card fm-hero"><p>Ask one question at dinner, in the car or at bedtime. <b>Listen more than you talk</b> — and answer it yourself too!</p></div>
        <div class="fm-card fm-talk fm-flip"><div class="fm-big">💬</div><p class="pl-q">${E(L[i] || '')}</p><small>${i + 1} / ${L.length}</small></div>
        <div class="fm-nav"><button type="button" class="fm-btn ghost" id="fmTp" ${i ? '' : 'disabled'}>◀ Previous</button><button type="button" class="fm-btn" id="fmTn">Next ▶</button></div>`);
      $1('#fmTp', el).onclick = () => { if (i) { i--; draw(); } };
      $1('#fmTn', el).onclick = () => { i = (i + 1) % L.length; S('open'); draw(); };
    };
    draw();
  }

  /* ---------- Mind Gym / Parenting Compass for grown-ups (the app's own screens, Parent Hub steps aside) ---------- */
  function mindGym(id) {
    if (!window.MindGym) return;
    keep({ v: 'mg' });
    const hub = D.getElementById('pvHub'); if (hub) hub.classList.remove('show');
    MindGym.parent(true);
    if (id && window.MindPlay) MindPlay.hub(id); else MindGym.open();
  }

  /* ---------- the card in Parent Hub ---------- */
  function hubCard(host, kids) {
    style();
    if (!host || host.querySelector('.fm-hubcard')) return;
    const first = kids && kids.length ? host.querySelector('.pv-card') : null;
    (first ? h => first.insertAdjacentHTML('afterend', h) : h => host.insertAdjacentHTML('afterbegin', h))(`<div class="pv-card fm-hubcard"><h2>🎲 Family Fun Zone</h2><p class="fm-mut">Play, learn and talk together. Kind words and laughter build a bond that lasts.</p>
      <div class="fm-grid">
        <button type="button" class="fm-tile big" data-fm="quiz"><span>🎲</span><b>Family Quiz Night</b><small>Pass the phone · kids get their syllabus, grown-ups get GK · one family star jar</small></button>
        <button type="button" class="fm-tile" data-fm="pc"><span>🫶</span><b>Parenting Compass</b><small>Calm, kind and firm — real family moments</small></button>
        <button type="button" class="fm-tile" data-fm="mg"><span>🧠</span><b>Mind Gym for me</b><small>Puzzles and brain games</small></button>
        <button type="button" class="fm-tile" data-fm="gk"><span>🌍</span><b>GK challenge</b><small>10 quick questions</small></button>
        <button type="button" class="fm-tile" data-fm="talk"><span>💬</span><b>Talk Time</b><small>Questions that open hearts</small></button></div></div>`);
    host.querySelectorAll('[data-fm]').forEach(b => b.onclick = () => { S('open'); ({ quiz: () => setup(kids || []), pc: () => mindGym('pc'), mg: () => mindGym(), gk: gkSolo, talk: talkTime })[b.dataset.fm](); });
  }

  let css = false;
  function style() {
    if (css) return; css = true;
    D.head.insertAdjacentHTML('beforeend', `<style id="fmCss">
      .fm-sheet{position:fixed;inset:0;z-index:2147483000;background:linear-gradient(160deg,#fff4e6,#fde7f3 50%,#e8f0ff);overflow:auto;display:none;color:#1f2d33}.fm-sheet.show{display:block}
      .fm-wrap{max-width:560px;margin:0 auto;padding:14px 14px 40px}.fm-top{display:flex;align-items:center;gap:10px;margin-bottom:10px}.fm-top h2{margin:0;font-size:20px}
      .fm-back{border:0;border-radius:12px;padding:8px 12px;background:#fff;font-weight:800;cursor:pointer;font-family:inherit;box-shadow:0 2px 8px rgba(0,0,0,.08)}
      .fm-card{background:#fff;border-radius:20px;padding:14px 16px;margin:10px 0;box-shadow:0 6px 18px rgba(80,40,90,.1)}.fm-card h3{margin:0 0 8px}
      .fm-hero{background:linear-gradient(135deg,#ffd6e7,#ffe9b8)}.fm-big{font-size:44px;text-align:center}.fm-mut{color:#667;font-size:13px}
      .fm-btn{display:block;width:100%;border:0;border-radius:16px;padding:14px;margin:8px 0;background:linear-gradient(135deg,#e05297,#7b5cff);color:#fff;font-weight:900;font-size:16px;cursor:pointer;font-family:inherit}
      .fm-btn.ghost{background:#fff;color:#7b3a8f;box-shadow:inset 0 0 0 2px #e6d4f3}.fm-btn:disabled{opacity:.6}
      .fm-pl{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0}.fm-chip{display:flex;align-items:center;gap:6px;border-radius:999px;padding:6px 10px;background:#f3eefe;font-weight:800}
      .fm-chip input[type=text],.fm-chip input:not([type]){border:0;background:transparent;font:inherit;width:84px}.fm-chip.add{border:2px dashed #c9b6ec;background:#fff;cursor:pointer;font-family:inherit}
      .fm-chip button{border:0;background:transparent;cursor:pointer}.fm-chip.kid{background:#e6f7ef;cursor:pointer}.fm-chip small{font-weight:600;color:#557}
      .fm-seg{display:flex;gap:8px}.fm-sg{flex:1;border:0;border-radius:14px;padding:10px;font-weight:900;font-size:18px;background:#f3eefe;cursor:pointer;font-family:inherit}.fm-sg.on{background:#7b5cff;color:#fff}
      .fm-jar{position:relative;height:38px;border-radius:14px;background:#fff;overflow:hidden;box-shadow:inset 0 0 0 3px #f2c94c}.fm-jarf{position:absolute;left:0;bottom:0;width:100%;background:linear-gradient(0deg,#ffd166,#fff3c4);transition:height .6s}
      .fm-jar b{position:relative;display:grid;place-items:center;height:100%}.fm-pass{text-align:center}.fm-pass h2{margin:6px 0}
      .fm-who{display:flex;flex-wrap:wrap;align-items:center;gap:6px}.fm-who span{font-size:28px}.fm-who small{width:100%;color:#667}
      .fm-qt{font-size:18px;font-weight:800;line-height:1.4}.fm-opts{display:flex;flex-direction:column;gap:8px}
      .fm-o{border:0;border-radius:14px;padding:12px;background:#f6f3ff;font-weight:700;font-size:15px;text-align:left;cursor:pointer;font-family:inherit;color:#1f2d33;transition:opacity .4s}
      .fm-o.ok{background:#1e9e6a;color:#fff}.fm-o.no{background:#e45;color:#fff}.fm-o.gone{opacity:.25;text-decoration:line-through}
      .fm-life{margin-top:10px;border:0;border-radius:14px;padding:10px;background:#fff1c2;font-weight:800;cursor:pointer;width:100%;font-family:inherit}
      .fm-v{font-weight:900;font-size:17px}.fm-v.ok{color:#1e9e6a}.fm-v.no{color:#b5521b}.fm-tip{background:#fdf2fa;border-radius:12px;padding:10px;font-weight:700}
      .fm-nav{display:flex;gap:8px}.fm-nav .fm-btn{flex:1}.fm-bad{display:grid;gap:8px;margin-top:10px}.fm-bad div{display:flex;flex-wrap:wrap;gap:6px;align-items:center;background:#f8f5ff;border-radius:12px;padding:8px}
      .fm-bad span{font-size:24px}.fm-bad small{width:100%;color:#556}.fm-end{text-align:center}.fm-talk{text-align:center;background:linear-gradient(135deg,#e8f0ff,#f3e8ff)}.fm-flip{animation:fmFlip .4s}
      .fm-hubcard .fm-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.fm-tile{display:flex;flex-direction:column;gap:2px;align-items:flex-start;text-align:left;border:0;border-radius:16px;padding:12px;background:#f7f2ff;cursor:pointer;font-family:inherit;color:inherit}
      .fm-tile.big{grid-column:span 2;background:linear-gradient(135deg,#ffd6e7,#ffe9b8)}.fm-tile span{font-size:28px}.fm-tile small{color:#667}
      @keyframes fmFlip{from{transform:rotateY(80deg);opacity:0}}
    </style>`);
  }
  /* a refresh inside the Parent Hub reopens the same game / page (the hub calls this once it has loaded) */
  let resumed = false;
  function resume(kids) {
    if (resumed) return; resumed = true;
    let v = null; try { v = JSON.parse(sessionStorage.getItem(FK) || 'null'); } catch (e) {}
    if (!v) return;
    try {
      if (v.v === 'quiz' && v.turns) return play(v.players, 0, kids || [], v);
      if (v.v === 'setup') return setup(kids || []);
      if (v.v === 'gk') return gkSolo();
      if (v.v === 'talk') return talkTime(v.i);
      if (v.v === 'mg') { let h = null; try { h = JSON.parse(sessionStorage.getItem('sv_here') || 'null'); } catch (e) {} return mindGym(h && h.x === 'mindplay' && h.a ? h.a[0] : null); }
    } catch (e) { forget(); }
  }
  window.Family = { hubCard, open: kids => setup(kids || []), resume, forget };
})();
