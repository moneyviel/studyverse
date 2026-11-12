/* ================= General Knowledge =================
   1. Brain Snacks: a swipeable row of daily cards on the home (world) screen:
      thought of the day, wow fact, GK bite (tap to reveal), on this day, word of the day.
      The picks depend only on the date and the child's grade, so everyone in a grade sees the
      same cards that day, and they work offline (content/gk/daily.json is in the service worker).
   2. GK Explorer: a free bonus section (big button on the snacks row + a card on Me) with
      21 topics, five ways to play (learn cards, quiz, speed round, true/false, fact streak),
      saved facts and search. Stars come from the app's own addXP().
   Content: content/gk/*.json, checked by tools/gk_validate.py. */
(function () {
  const BASE = 'content/gk/';
  const MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const G = () => { ST.gk = ST.gk || {}; const g = ST.gk; g.bm = g.bm || {}; g.seen = g.seen || {}; g.sel = g.sel || ['*']; g.best = g.best || 0; g.bestSpeed = g.bestSpeed || 0; return g; };
  const grade = () => (ST.profile && ST.profile.course === 'ca') ? 12 : (+(ST.profile && ST.profile.grade) || 6);   // CA students get the oldest-level cards
  const fits = (x, g = grade()) => x.g[0] <= g && g <= x.g[1];
  const shuffle = a => (window.Games ? Games.shuffle(a) : a.slice().sort(() => Math.random() - .5));
  const tap = k => { try { sfx(k); } catch (e) {} };
  let DAILY = null, INDEX = null; const CATS = {};
  async function daily() { if (!DAILY) DAILY = await loadJSON(BASE + 'daily.json'); return DAILY; }
  async function index() { if (!INDEX) INDEX = await loadJSON(BASE + 'index.json'); return INDEX; }
  async function cat(id) { if (!CATS[id]) CATS[id] = await loadJSON(BASE + id + '.json'); return CATS[id]; }
  const catMeta = id => (INDEX && INDEX.categories.find(c => c.id === id)) || { id, name: 'General Knowledge', emoji: '🧠' };

  /* ---------- the same pick for everyone on the same date ---------- */
  function rng(seed) {
    let a = 2166136261; for (const ch of String(seed)) a = Math.imul(a ^ ch.charCodeAt(0), 16777619) >>> 0;
    return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  function seeded(list, seed) { const r = rng(seed), a = list.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  function dayInfo(d = new Date()) {
    const y = d.getFullYear(), m = d.getMonth(), dd = d.getDate();
    return { n: Math.floor(Date.UTC(y, m, dd) / 864e5), key: `${String(m + 1).padStart(2, '0')}-${String(dd).padStart(2, '0')}`, label: `${DAYS[d.getDay()]} ${dd} ${MON[m].slice(0, 3)}`, long: `${dd} ${MON[m]}`, iso: `${y}-${String(m + 1).padStart(2, '0')}-${String(dd).padStart(2, '0')}` };
  }
  /* a fixed shuffled order per list, walked one step per day: no repeats until the list runs out */
  function pickDay(list, salt, day) { const pool = seeded(list, salt).filter(x => fits(x)); return pool.length ? pool[day % pool.length] : null; }

  /* ---------- share / copy ---------- */
  async function share(text) {
    const full = `${text}\n— from Knowtopia`;
    if (navigator.share) { try { await navigator.share({ title: 'Knowtopia', text: full }); return; } catch (e) { if (e && e.name === 'AbortError') return; } }
    try { await navigator.clipboard.writeText(full); toast('📋 Copied! Paste it to share.'); }
    catch (e) { const t = document.createElement('textarea'); t.value = full; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0'; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); toast('📋 Copied! Paste it to share.'); } catch (e2) { toast('Could not copy on this phone'); } t.remove(); }
  }
  const spkBtn = (scope, what) => `<button class="spk" data-ra="${scope}" aria-label="Read ${esc(what)} aloud">🔊</button>`;

  /* ================= 1. Brain Snacks ================= */
  async function snacks() {
    const ca = !!(ST.profile && ST.profile.course === 'ca');   // World (school) / CA Journey: just above the map / under the greeting
    const scr = document.getElementById(ca ? 's-ca' : 's-world'), top = ca && scr && scr.querySelector(':scope > .ca-journey') ? scr.querySelector(':scope > .ca-top') : null;
    const map = ca ? (top && top.nextElementSibling) : document.getElementById('map');
    if (!scr || !map || !ST.profile) return;
    let D; try { D = await daily(); } catch (e) { document.getElementById('gkSnack')?.remove(); return; }
    const t = dayInfo(), g = grade(), sig = `${t.iso}|${g}`;
    let box = document.getElementById('gkSnack');
    if (box && box.dataset.sig === sig && box.parentElement === scr) { box.classList.toggle('shut', !!G().shut); return; }
    const old = box && box.querySelector('.gk-row'), sx = old ? old.scrollLeft : 0;
    if (!box) { box = document.createElement('section'); box.id = 'gkSnack'; box.className = 'gk-snack'; box.setAttribute('aria-labelledby', 'gkSnackT'); map.before(box); }
    else if (box.nextElementSibling !== map) map.before(box);
    box.dataset.sig = sig;
    const th = pickDay(D.thoughts, 'thought', t.n), wow = pickDay(D.wow, 'wow', t.n), bite = pickDay(D.bites, 'bite', t.n), word = pickDay(D.words, 'word', t.n);
    const otd = D.otd[t.key];
    const cards = [];
    if (th) cards.push({ k: 'thought', e: '💭', h: 'Thought of the Day', body: `<p class="gk-big">${esc(th.t)}</p>${th.by ? `<p class="gk-by">— ${esc(th.by)}</p>` : ''}`, share: `💭 Thought of the Day: ${th.t}${th.by ? ` (${th.by})` : ''}`, more: null });
    if (wow) cards.push({ k: 'wow', e: '🤯', h: 'Wow Fact', body: `<p class="gk-big">${esc(wow.t)}</p>`, share: `🤯 Wow fact: ${wow.t}`, more: wow.c });
    if (bite) cards.push({ k: 'bite', e: '🧠', h: 'GK Bite', body: `<p class="gk-big">${esc(bite.q)}</p><div class="gk-ansbox"></div>`, share: `🧠 GK Bite: ${bite.q} (Answer: ${bite.a})`, more: bite.c, bite });
    if (otd) cards.push({ k: 'otd', e: '📅', h: `On This Day · ${t.long}`, body: `<p class="gk-year">${otd.y}</p><p class="gk-big">${esc(otd.t)}</p>`, share: `📅 On this day, ${t.long} ${otd.y}: ${otd.t}`, more: 'history' });
    if (word) cards.push({ k: 'word', e: '🔤', h: 'Word of the Day', body: `<p class="gk-word">${esc(word.w)} <i>${esc(word.p)}</i></p><p class="gk-mean">${esc(word.m)}</p><p class="gk-ex">“${esc(word.ex)}”</p>`, share: `🔤 Word of the Day: ${word.w} (${word.p}) — ${word.m}. Example: ${word.ex}`, more: 'languages' });
    box.innerHTML = `<div class="gk-sh"><button class="gk-tgl" id="gkTgl" aria-expanded="${G().shut ? 'false' : 'true'}" aria-controls="gkRow"><span class="gk-spark" aria-hidden="true">✨</span><span class="gk-tt"><b id="gkSnackT">Brain Snacks</b><small>${esc(t.label)} · ${cards.length} new</small></span><span class="gk-chev" aria-hidden="true">▾</span></button>
      <button class="gk-go" id="gkGo" aria-label="Open GK Explorer: general knowledge facts, quizzes and games"><span aria-hidden="true">🧭</span> GK Explorer</button></div>
      <div class="gk-row" id="gkRow" role="list" aria-label="Today's brain snacks. Swipe for more.">${cards.map((c, i) => `<article class="gkc gkc-${c.k}" role="listitem" aria-label="${esc(c.h)}, card ${i + 1} of ${cards.length + 1}" data-i="${i}">
        <div class="gkc-h"><span class="gkc-e" aria-hidden="true">${c.e}</span><span class="gkc-k">${esc(c.h)}</span>${spkBtn('.gkc', c.h)}</div>
        <div class="gkc-b">${c.body}</div>
        <div class="gkc-a ra-skip">${c.bite ? `<button class="gk-rev" data-i="${i}">👀 Tap to reveal</button>` : ''}<button class="gk-ic" data-share="${i}" aria-label="Share this ${esc(c.h)}"><span aria-hidden="true">📤</span></button><button class="gk-more" data-more="${esc(c.more || '')}">More like this ›</button></div></article>`).join('')}
        <article class="gkc gkc-explore" role="listitem" aria-label="GK Explorer, card ${cards.length + 1} of ${cards.length + 1}"><div class="gkc-h"><span class="gkc-e" aria-hidden="true">🧭</span><span class="gkc-k">GK Explorer</span></div>
        <div class="gkc-b"><p class="gk-big">900+ facts · 21 topics</p><p class="gk-mean">Space, India, animals, inventions, sports and more. Learn, quiz, speed round and fact streaks.</p></div>
        <div class="gkc-a ra-skip"><button class="gk-more gk-solid" data-more="">Start exploring ›</button></div></article></div>`;
    box.classList.toggle('shut', !!G().shut);
    const row = box.querySelector('.gk-row'); row.scrollLeft = sx;
    box.querySelector('#gkTgl').onclick = e => { const s = G(); s.shut = !s.shut; save(); box.classList.toggle('shut', s.shut); e.currentTarget.setAttribute('aria-expanded', String(!s.shut)); tap('tap'); };
    box.querySelector('#gkGo').onclick = () => { tap('open'); open(); };
    box.querySelectorAll('[data-share]').forEach(b => b.onclick = () => share(cards[+b.dataset.share].share));
    box.querySelectorAll('.gk-more').forEach(b => b.onclick = () => { tap('open'); const c = b.dataset.more; c ? open({ cat: c, mode: 'learn' }) : open(); });
    box.querySelectorAll('.gk-rev').forEach(b => b.onclick = () => {
      const c = cards[+b.dataset.i], a = b.closest('.gkc').querySelector('.gk-ansbox');
      a.innerHTML = `<p class="gk-ans"><span aria-hidden="true">✅</span> ${esc(c.bite.a)}</p><p class="gk-x">${esc(c.bite.x)}</p>`;
      a.setAttribute('role', 'status'); b.remove(); tap('coin');
      const s = G(); if (s.biteDay !== t.iso) { s.biteDay = t.iso; save(); addXP(2, 'GK Bite'); }
      if (window.A11Y && A11Y.announce) A11Y.announce(`Answer: ${c.bite.a}. ${c.bite.x}`);
    });
  }

  /* ================= 2. GK Explorer ================= */
  let RUNNING = null;                       // stops timers when leaving a mode
  const stopRun = () => { if (RUNNING) { clearInterval(RUNNING); RUNNING = null; } };
  function screen() {
    let s = document.getElementById('s-gk');
    if (!s) { s = document.createElement('section'); s.className = 'screen'; s.id = 's-gk'; document.querySelector('main').appendChild(s); }
    return s;
  }
  let FROM = 'world';
  async function open(o = {}) {
    stopRun();
    if (o.from) FROM = o.from; else if (!o.keep) FROM = 'practice';   // GK Explorer lives in Practice (tile there; Brain Snacks on World open it too)
    const el = screen(); show('gk', FROM);
    el.innerHTML = `<p class="note">Loading…</p>`;
    let I; try { I = await index(); } catch (e) { el.innerHTML = `<button class="back" id="gkBack">← Back</button><div class="card"><h2>GK Explorer</h2><p class="sub">Could not load the facts. Connect to the internet once, and they will be saved for offline use.</p></div>`; el.querySelector('#gkBack').onclick = goBack; return; }
    const s = G();
    if (o.cat) { s.sel = [o.cat]; save(); }
    if (o.mode) return run(o.mode);
    const nSaved = Object.keys(s.bm).length, total = I.categories.reduce((a, c) => a + c.nf, 0);
    const allOn = !s.sel.length || s.sel.includes('*');
    el.innerHTML = `<button class="back" id="gkBack">← ${FROM === 'me' ? 'Me' : FROM === 'world' ? 'Home' : 'Practice'}</button>
      <div class="hello" role="heading" aria-level="1"><span aria-hidden="true">🧭</span> GK Explorer <small>Free bonus · ${total} facts · picked for Grade ${grade()}</small></div>
      <div class="gsearch gk-search"><span aria-hidden="true">🔍</span><input id="gkQ" type="search" placeholder="Search GK… e.g. Everest, Moon, rupee" autocomplete="off" aria-label="Search general knowledge facts"></div><div id="gkRes" class="gs-res" aria-live="polite"></div>
      <div class="card"><h3>Choose how to play</h3><p class="sub">Topics: <b id="gkSelNow">${esc(selLabel())}</b> · change below</p><div class="gk-modes">
        <button class="gk-mode" data-m="learn"><b><span aria-hidden="true">📖</span> Learn cards</b><small>A fact, a simple why, and 🔊</small></button>
        <button class="gk-mode" data-m="quiz"><b><span aria-hidden="true">❓</span> Quiz</b><small>10 questions with explanations</small></button>
        <button class="gk-mode" data-m="speed"><b><span aria-hidden="true">⚡</span> Speed round</b><small>${speedSecs() ? `${speedSecs()} seconds. How many can you get?` : '15 quick questions, no timer'}${s.bestSpeed ? ` · best ${s.bestSpeed}` : ''}</small></button>
        <button class="gk-mode" data-m="tf"><b><span aria-hidden="true">✅</span> True or false</b><small>Is the answer right or not?</small></button>
        <button class="gk-mode" data-m="streak"><b><span aria-hidden="true">🔥</span> Fact streak</b><small>Keep going until a miss${s.best ? ` · best ${s.best}` : ''}</small></button>
        <button class="gk-mode" data-m="saved"><b><span aria-hidden="true">🔖</span> Saved facts</b><small>${nSaved ? `${nSaved} saved` : 'Tap 🔖 on any fact to save it'}</small></button></div></div>
      <div class="card"><h3>Pick topics</h3><p class="sub" id="gkSelSub">Tap one or more topics, or play them all mixed.</p>
        <div class="gk-cats" role="group" aria-labelledby="gkSelSub"><button class="gk-cat gk-all ${allOn ? 'on' : ''}" data-c="*" aria-pressed="${allOn}"><span aria-hidden="true">🌈</span> All mixed</button>
        ${I.categories.map(c => { const on = !allOn && s.sel.includes(c.id); return `<button class="gk-cat ${on ? 'on' : ''}" data-c="${c.id}" aria-pressed="${on}"><span aria-hidden="true">${c.emoji}</span> ${esc(c.name)}</button>`; }).join('')}</div></div>
      <p class="note">Facts are picked for your grade. Change your grade in Me.</p>`;
    el.querySelector('#gkBack').onclick = goBack;
    el.querySelectorAll('.gk-cat').forEach(b => b.onclick = () => {
      const c = b.dataset.c; let sel = s.sel.filter(x => x !== '*');
      if (c === '*') sel = ['*']; else sel = sel.includes(c) ? sel.filter(x => x !== c) : [...sel, c];
      if (!sel.length) sel = ['*']; s.sel = sel; save(); tap('tap');
      el.querySelectorAll('.gk-cat').forEach(x => { const on = x.dataset.c === '*' ? sel.includes('*') : sel.includes(x.dataset.c); x.classList.toggle('on', on); x.setAttribute('aria-pressed', String(on)); });
      const sn = el.querySelector('#gkSelNow'); if (sn) sn.textContent = selLabel();
    });
    el.querySelectorAll('.gk-mode').forEach(b => b.onclick = () => { tap('open'); run(b.dataset.m); });
    let tm; el.querySelector('#gkQ').oninput = e => { clearTimeout(tm); const v = e.target.value.trim(); tm = setTimeout(() => search(v), 250); };
  }
  function selLabel() { const s = G(); if (!s.sel.length || s.sel.includes('*')) return 'All mixed'; const n = s.sel.map(id => catMeta(id).name); return n.length > 2 ? `${n.length} topics` : n.join(' + '); }
  function goBack() { stopRun(); if (FROM === 'me') return meScreen(); if (FROM === 'world') return worldScreen(); try { (ST.profile && ST.profile.course === 'ca' && window.CaTools && CaTools.practiceHub) ? CaTools.practiceHub() : practiceScreen(); } catch (e) { worldScreen(); } }

  /* ---------- pools for the chosen topics, fitted to the grade ---------- */
  async function selected() { const I = await index(), s = G(); const ids = !s.sel.length || s.sel.includes('*') ? I.categories.map(c => c.id) : s.sel.filter(id => I.categories.some(c => c.id === id)); return Promise.all((ids.length ? ids : I.categories.map(c => c.id)).map(cat)); }
  function fitted(list, min) {
    const g = grade(), ok = list.filter(x => fits(x, g));
    if (ok.length >= min) return ok;
    /* very few items for this grade in these topics: add the nearest ones from the grades just above */
    const near = list.filter(x => !fits(x, g)).sort((a, b) => Math.abs(a.g[0] - g) - Math.abs(b.g[0] - g));
    return ok.concat(near.slice(0, Math.max(0, min - ok.length)));
  }
  async function factPool() { const cs = await selected(); return fitted(cs.flatMap(c => c.facts.map(f => ({ ...f, c: c.id }))), 12); }
  async function quizPool() { const cs = await selected(); return fitted(cs.flatMap(c => c.quiz.map(q => ({ ...q, c: c.id }))), 12); }
  const speedSecs = () => { const sc = window.A11Y && A11Y.timeScale ? A11Y.timeScale() : 1; return sc ? 60 * sc : 0; };

  function frame(title, sub) {
    const el = screen();
    el.innerHTML = `<button class="back" id="gkHome">← GK Explorer</button><div class="hello gk-mt">${title}${sub ? ` <small>${sub}</small>` : ''}</div><div id="gkBody"></div>`;
    el.querySelector('#gkHome').onclick = () => { tap('tap'); open({ keep: true }); };
    window.scrollTo(0, 0);
    return el.querySelector('#gkBody');
  }
  async function run(mode) {
    stopRun();
    if (mode === 'learn') return learn(await factPool(), 0, '📖 Learn cards');
    if (mode === 'saved') return saved();
    const pool = await quizPool();
    if (mode === 'quiz') return quiz(shuffle(pool).slice(0, 10));
    if (mode === 'speed') return speed(shuffle(pool));
    if (mode === 'tf') return tf(shuffle(pool).slice(0, 10));
    if (mode === 'streak') return streak(pool);
  }
  const tagOf = id => { const m = catMeta(id); return `<span class="tag"><span aria-hidden="true">${m.emoji}</span> ${esc(m.name)}</span>`; };

  /* ---------- Learn cards ---------- */
  function learn(list, start, title, keepOrder) {
    if (!list.length) { const b = frame(title); b.innerHTML = `<div class="card"><p class="sub">No facts here yet.</p></div>`; return; }
    if (!keepOrder) list = shuffle(list);
    let i = start || 0, fresh = 0;
    const b = frame(title, 'Swipe or tap Next');
    const draw = () => {
      const f = list[i], s = G(), on = !!s.bm[f.id];
      if (!s.seen[f.id]) { s.seen[f.id] = 1; fresh++; addXP(1); if (fresh % 10 === 0) toast(`${fresh} new facts learned! 🧠`); }
      b.innerHTML = `<div class="card gk-lc"><div class="gk-lt">${tagOf(f.c)}<span class="gk-n ra-skip">${i + 1} / ${list.length}</span></div>
        <h2 class="gk-fact">${esc(f.f)}</h2><p class="sub gk-exp">${esc(f.e)}</p>
        <div class="gk-acts ra-skip">${spkBtn('.gk-lc', 'this fact')}<button class="gk-ic gk-bm ${on ? 'on' : ''}" id="gkBm" aria-pressed="${on}" aria-label="Save this fact"><span aria-hidden="true">🔖</span></button><button class="gk-ic" id="gkSh" aria-label="Share this fact"><span aria-hidden="true">📤</span></button></div></div>
        <div class="tst-nav gk-nav"><button class="btn ghost" id="gkPrev" ${i ? '' : 'disabled'}>◀ Back</button><button class="btn" id="nx">${i < list.length - 1 ? 'Next ▶' : 'Finish ✓'}</button></div>`;
      b.querySelector('#gkBm').onclick = e => { const s2 = G(); if (s2.bm[f.id]) delete s2.bm[f.id]; else s2.bm[f.id] = 1; save(); const o = !!s2.bm[f.id]; e.currentTarget.classList.toggle('on', o); e.currentTarget.setAttribute('aria-pressed', String(o)); toast(o ? '🔖 Saved' : 'Removed from saved'); };
      b.querySelector('#gkSh').onclick = () => share(`🧠 ${f.f} ${f.e}`);
      b.querySelector('#gkPrev').onclick = () => { if (i) { i--; tap('tap'); draw(); } };
      b.querySelector('#nx').onclick = next;
    };
    const next = () => { if (i < list.length - 1) { i++; tap('tap'); draw(); } else { addXP(5, 'Fact cards done!'); open({ keep: true }); } };
    let x0 = null;
    b.ontouchstart = e => { x0 = e.touches[0].clientX; };
    b.ontouchend = e => { if (x0 == null) return; const dx = (e.changedTouches[0].clientX - x0) / (window.SV_ZF || 1); x0 = null; if (Math.abs(dx) > 60) { if (dx < 0) next(); else if (i) { i--; draw(); } } };
    draw();
  }
  async function saved() {
    const ids = Object.keys(G().bm), cs = [...new Set(ids.map(id => id.split('-')[0]))];
    const loaded = await Promise.all(cs.map(c => cat(c).catch(() => null)));
    const list = loaded.filter(Boolean).flatMap(c => c.facts.filter(f => G().bm[f.id]).map(f => ({ ...f, c: c.id })));
    if (!list.length) { const b = frame('🔖 Saved facts'); b.innerHTML = `<div class="card"><p class="sub">You have not saved any facts yet. In Learn cards, tap 🔖 to keep a fact here.</p><button class="btn" id="nx">📖 Start learning</button></div>`; b.querySelector('#nx').onclick = () => run('learn'); return; }
    learn(list, 0, '🔖 Saved facts', true);
  }

  /* ---------- Quiz (4 options, explanation) ---------- */
  function qCard(q, i, n, extra = '', ord, nav = '', prog) {
    return `<div class="card"><div class="tst-top">${tagOf(q.c)}<span class="gk-n ra-skip">${extra || `${i + 1} / ${n}`}</span></div>${n ? `<div class="progress"><i style="width:${(prog == null ? i / n : prog) * 100}%"></i></div>` : ''}
      <h2 class="qtext">${esc(q.q)} ${spk(q.q, 1)}</h2><div id="gkOpts">${(ord || shuffle(q.o.map((o, k) => k))).map(k => `<button class="opt" data-k="${k}">${esc(q.o[k])}</button>`).join('')}</div><div id="gkX"></div>${nav}</div>`;
  }
  /* ◀ Previous / Next ▶ for the 10-question quiz and true-or-false rounds: skip and come back, revisit answered
     questions (answer and explanation shown again), each scored once; Finish asks before leaving blanks. */
  function stepper(N, isDone, draw, finish) {
    const S = { i: 0 };
    S.nav = () => `<div class="tst-nav qnav"><button class="btn ghost" id="qPrev" ${S.i ? '' : 'disabled'} aria-label="Previous question">◀ Previous</button><button class="btn ${isDone(S.i) ? 'mint' : ''}" id="nx" aria-label="${S.i < N - 1 ? (isDone(S.i) ? 'Next question' : 'Skip to the next question') : 'Finish'}">${S.i < N - 1 ? 'Next ▶' : 'Finish ▶'}</button></div>`;
    S.go = j => { if (j < 0 || j >= N) return; S.i = j; draw(); window.scrollTo(0, 0); };
    S.end = () => { let left = 0, first = -1; for (let k = 0; k < N; k++) if (!isDone(k)) { left++; if (first < 0) first = k; }
      if (left && !confirm(`${left} question${left > 1 ? 's are' : ' is'} not answered yet. Finish anyway?`)) { S.go(first); return; } finish(); };
    S.wire = b => { b.querySelector('#qPrev').onclick = () => S.go(S.i - 1); b.querySelector('#nx').onclick = () => (S.i < N - 1 ? S.go(S.i + 1) : S.end()); };
    S.answered = b => { const nx = b.querySelector('#nx'); if (nx) { nx.classList.add('mint'); if (S.i < N - 1) nx.setAttribute('aria-label', 'Next question'); } };
    S.count = () => { let c = 0; for (let k = 0; k < N; k++) if (isDone(k)) c++; return c; };
    return S;
  }
  function explainBox(ok, q, nextLabel) {
    return `<div class="explain ${ok ? 'good' : 'bad'}"><div class="verdict">${ok ? '🎉 Correct!' : `🤔 Not quite — it's <b>${esc(q.o[q.a])}</b>`}</div><div class="why">${esc(q.x)} ${spkBtn('.explain', 'the explanation')}</div></div>
      <div class="xrow"><button class="btn mint" id="nx">${nextLabel}</button></div>`;
  }
  function quiz(list) {
    const b = frame('❓ GK Quiz'); let right = 0, over = false; const N = list.length;
    const st = list.map(q => ({ ord: shuffle(q.o.map((o, k) => k)), k: null }));
    const S = stepper(N, j => st[j].k !== null, () => draw(), () => done());
    const show = fresh => {
      const q = list[S.i], s = st[S.i], ok = s.k === q.a;
      b.querySelectorAll('.opt').forEach(x => { x.disabled = true; const k = +x.dataset.k; if (k === q.a) x.classList.add('right'); else if (k === s.k) x.classList.add('wrong'); });
      b.querySelector('#gkX').innerHTML = explainBox(ok, q, '').replace(/<div class="xrow">[\s\S]*$/, '');
      S.answered(b);
      if (fresh) setTimeout(() => b.querySelector('#gkX')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
    };
    const draw = () => {
      const q = list[S.i], s = st[S.i]; b.innerHTML = qCard(q, S.i, N, '', s.ord, S.nav(), S.count() / N); S.wire(b);
      if (s.k !== null) { show(false); return; }
      b.querySelectorAll('.opt').forEach(o => o.onclick = () => {
        if (s.k !== null || over) return;
        const k = +o.dataset.k, ok = k === q.a; s.k = k;
        if (ok) { right++; tap('correct'); addXP(5); } else tap('wrong');
        const pg = b.querySelector('.progress i'); if (pg) pg.style.width = S.count() / N * 100 + '%';
        show(true);
      });
    };
    const done = () => {
      if (over) return; over = true;
      tap('unlock'); bumpStreakSafe();
      b.innerHTML = `<div class="card done-card"><div class="gbig" aria-hidden="true">${right >= list.length * .8 ? '🏆' : right >= list.length / 2 ? '🌟' : '💪'}</div><h2>${right} / ${list.length} correct</h2><p class="sub">You earned ${right * 5} ⭐ in this quiz.</p>
        <button class="btn" id="nx">Play again ▶</button><div style="height:8px"></div><button class="btn ghost" id="gkBackH">Back to GK Explorer</button></div>`;
      b.querySelector('#nx').onclick = () => run('quiz'); b.querySelector('#gkBackH').onclick = () => open({ keep: true });
    };
    draw();
  }
  function bumpStreakSafe() { try { bumpStreak(); } catch (e) {} }

  /* ---------- Speed round (60 s; extra time / no timer follow the app's timer setting) ---------- */
  function speed(list) {
    const secs = speedSecs(), max = secs ? list.length : Math.min(15, list.length);
    const b = frame('⚡ Speed round', secs ? `${secs} seconds` : 'No timer: 15 questions');
    let i = 0, score = 0, left = secs, last = Date.now(), over = false;
    b.innerHTML = `<div class="card gk-speedtop"><div class="gk-clock" id="gkClock" role="timer" aria-live="off">${secs ? `⏱ ${secs}s` : '⏱ –'}</div><div class="gk-score" aria-live="polite">⭐ <b id="gkScore">0</b></div></div><div id="gkQ2"></div>`;
    const host = b.querySelector('#gkQ2');
    const draw = () => {
      if (over) return; if (i >= max) return end();
      const q = list[i]; host.innerHTML = qCard(q, i, 0, `#${i + 1}`);
      host.querySelectorAll('.opt').forEach(o => o.onclick = () => {
        if (over) return; const ok = +o.dataset.k === q.a;
        host.querySelectorAll('.opt').forEach(x => { x.disabled = true; if (+x.dataset.k === q.a) x.classList.add('right'); });
        if (ok) { score++; b.querySelector('#gkScore').textContent = score; tap('correct'); } else { o.classList.add('wrong'); tap('wrong'); }
        i++; setTimeout(draw, ok ? 350 : 900);
      });
    };
    const end = () => {
      if (over) return; over = true; stopRun();
      const s = G(), best = score > s.bestSpeed; if (best) { s.bestSpeed = score; save(); }
      if (score) addXP(score * 3, 'Speed round!'); tap('unlock');
      b.innerHTML = `<div class="card done-card"><div class="gbig" aria-hidden="true">⚡</div><h2>${score} correct</h2><p class="sub">${best ? '🏆 New best score!' : `Your best: ${s.bestSpeed}`}</p>
        <button class="btn" id="nx">Go again ▶</button><div style="height:8px"></div><button class="btn ghost" id="gkBackH">Back to GK Explorer</button></div>`;
      b.querySelector('#nx').onclick = () => run('speed'); b.querySelector('#gkBackH').onclick = () => open({ keep: true });
    };
    if (secs) RUNNING = setInterval(() => {
      const now = Date.now(), dt = (now - last) / 1000; last = now;
      if (!document.getElementById('s-gk')?.classList.contains('active') || !b.isConnected) { over = true; stopRun(); return; }
      if (window.A11Y && A11Y.holdClock && A11Y.holdClock()) return;
      left -= dt; const c = b.querySelector('#gkClock'); if (c) { c.textContent = `⏱ ${Math.max(0, Math.ceil(left))}s`; c.classList.toggle('low', left <= 10); }
      if (window.A11Y && A11Y.timerTick) A11Y.timerTick(b, Math.ceil(left));
      if (left <= 0) end();
    }, 250);
    draw();
  }

  /* ---------- True or false (built from the quiz bank: is this the right answer?) ---------- */
  function tfItem(q) { const truth = Math.random() < .5, wrong = q.o.filter((o, k) => k !== q.a); return { q, truth, shown: truth ? q.o[q.a] : wrong[Math.floor(Math.random() * wrong.length)] }; }
  function tfCard(it, extra) {
    return `<div class="card"><div class="tst-top">${tagOf(it.q.c)}<span class="gk-n ra-skip">${extra}</span></div><p class="gk-tfl">True or false?</p>
      <h2 class="qtext">${esc(it.q.q)} <span class="gk-tfa"><small>Answer:</small> ${esc(it.shown)}</span> ${spk(it.q.q + ' ' + it.shown)}</h2>
      <div class="tfbtns"><button class="btn tfb" data-v="1">✔ True</button><button class="btn tfb no" data-v="0">✘ False</button></div><div id="gkX"></div></div>`;
  }
  function tfAnswer(b, it, onDone, nextLabel) {
    b.querySelectorAll('.tfb').forEach(x => x.onclick = () => {
      const said = x.dataset.v === '1', ok = said === it.truth;
      b.querySelectorAll('.tfb').forEach(y => { y.disabled = true; y.classList.toggle('picked', y === x); });
      tap(ok ? 'correct' : 'wrong');
      const q = it.q;
      b.querySelector('#gkX').innerHTML = `<div class="explain ${ok ? 'good' : 'bad'}"><div class="verdict">${ok ? '🎉 Correct!' : '🤔 Not quite.'} It's ${it.truth ? 'true' : 'false'}: the answer is <b>${esc(q.o[q.a])}</b>.</div><div class="why">${esc(q.x)} ${spkBtn('.explain', 'the explanation')}</div></div>
        <div class="xrow"><button class="btn mint" id="nx">${nextLabel(ok)}</button></div>`;
      b.querySelector('#nx').onclick = () => onDone(ok);
      setTimeout(() => b.querySelector('#gkX')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
    });
  }
  function tf(list) {
    const b = frame('✅ True or false'); let right = 0, over = false; const N = list.length;
    const items = list.map(q => ({ it: tfItem(q), said: null }));
    const S = stepper(N, j => items[j].said !== null, () => draw(), () => done());
    const show = fresh => {
      const e = items[S.i], it = e.it, q = it.q, ok = e.said === it.truth;
      b.querySelectorAll('.tfb').forEach(y => { y.disabled = true; y.classList.toggle('picked', (y.dataset.v === '1') === e.said); });
      b.querySelector('#gkX').innerHTML = `<div class="explain ${ok ? 'good' : 'bad'}"><div class="verdict">${ok ? '🎉 Correct!' : '🤔 Not quite.'} It's ${it.truth ? 'true' : 'false'}: the answer is <b>${esc(q.o[q.a])}</b>.</div><div class="why">${esc(q.x)} ${spkBtn('.explain', 'the explanation')}</div></div>`;
      S.answered(b);
      if (fresh) setTimeout(() => b.querySelector('#gkX')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
    };
    const draw = () => {
      const e = items[S.i];
      b.innerHTML = tfCard(e.it, `${S.i + 1} / ${N}${e.said !== null ? ' · answered' : ''}`).replace(/<\/div>$/, S.nav() + '</div>'); S.wire(b);
      if (e.said !== null) { show(false); return; }
      b.querySelectorAll('.tfb').forEach(x => x.onclick = () => {
        if (e.said !== null || over) return;
        e.said = x.dataset.v === '1'; const ok = e.said === e.it.truth;
        if (ok) { right++; addXP(3); } tap(ok ? 'correct' : 'wrong');
        show(true);
      });
    };
    const done = () => {
      if (over) return; over = true;
      tap('unlock');
      b.innerHTML = `<div class="card done-card"><div class="gbig" aria-hidden="true">✅</div><h2>${right} / ${list.length} correct</h2><p class="sub">You earned ${right * 3} ⭐.</p><button class="btn" id="nx">Play again ▶</button><div style="height:8px"></div><button class="btn ghost" id="gkBackH">Back to GK Explorer</button></div>`;
      b.querySelector('#nx').onclick = () => run('tf'); b.querySelector('#gkBackH').onclick = () => open({ keep: true });
    };
    draw();
  }

  /* ---------- Fact streak: mixed quiz and true/false until the first miss ---------- */
  function streak(pool) {
    const b = frame('🔥 Fact streak', `Best: ${G().best}`); let n = 0, bag = shuffle(pool);
    const nextQ = () => { if (!bag.length) bag = shuffle(pool); return bag.pop(); };
    const draw = () => {
      const q = nextQ(), label = `🔥 ${n} in a row`;
      if (Math.random() < .5) {
        b.innerHTML = qCard(q, 0, 0, label);
        b.querySelectorAll('.opt').forEach(o => o.onclick = () => {
          const ok = +o.dataset.k === q.a;
          b.querySelectorAll('.opt').forEach(x => { x.disabled = true; if (+x.dataset.k === q.a) x.classList.add('right'); });
          if (!ok) o.classList.add('wrong'); tap(ok ? 'correct' : 'wrong');
          after(ok, q);
        });
      } else {
        const it = tfItem(q); b.innerHTML = tfCard(it, label);
        tfAnswer(b, it, ok => (ok ? draw() : end()), ok => (ok ? 'Keep going ▶' : 'See my streak ▶'));
        b.querySelectorAll('.tfb').forEach(x => { const f = x.onclick; x.onclick = () => { f(); if ((x.dataset.v === '1') === it.truth) { n++; addXP(2); } }; });
      }
    };
    const after = (ok, q) => {
      if (ok) { n++; addXP(2); }
      b.querySelector('#gkX').innerHTML = explainBox(ok, q, ok ? 'Keep going ▶' : 'See my streak ▶');
      b.querySelector('#nx').onclick = () => (ok ? draw() : end());
      setTimeout(() => b.querySelector('#gkX')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
    };
    const end = () => {
      const s = G(), best = n > s.best; if (best) { s.best = n; save(); }
      if (n >= 5) addXP(5, `${n}-fact streak!`); tap('unlock'); if (n) bumpStreakSafe();
      b.innerHTML = `<div class="card done-card"><div class="gbig" aria-hidden="true">🔥</div><h2>${n} in a row</h2><p class="sub">${best && n ? '🏆 New best streak!' : `Your best: ${s.best}`}</p><button class="btn" id="nx">Try again ▶</button><div style="height:8px"></div><button class="btn ghost" id="gkBackH">Back to GK Explorer</button></div>`;
      b.querySelector('#nx').onclick = () => run('streak'); b.querySelector('#gkBackH').onclick = () => open({ keep: true });
    };
    draw();
  }

  /* ---------- Search across all topics ---------- */
  const norm = s => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9ऀ-ॿ ]+/g, ' ');
  async function search(v) {
    const box = document.getElementById('gkRes'); if (!box) return;
    if (v.length < 2) { box.innerHTML = ''; return; }
    box.innerHTML = '<p class="sub gs-none">Searching…</p>';
    const I = await index(); const all = await Promise.all(I.categories.map(c => cat(c.id).catch(() => null)));
    const words = norm(v).split(/\s+/).filter(Boolean), g = grade();
    const hit = t => { const n = ' ' + norm(t) + ' '; return words.every(w => n.includes(w)); };
    const res = [];
    all.filter(Boolean).forEach(c => {
      c.facts.forEach(f => { if (hit(f.f + ' ' + f.e)) res.push({ t: 'f', it: { ...f, c: c.id }, c, s: (hit(f.f) ? 2 : 0) + (fits(f, g) ? 1 : 0) }); });
      c.quiz.forEach(q => { if (hit(q.q + ' ' + q.o[q.a])) res.push({ t: 'q', it: { ...q, c: c.id }, c, s: (fits(q, g) ? 1 : 0) }); });
    });
    if (document.getElementById('gkQ')?.value.trim() !== v) return;
    res.sort((a, b2) => b2.s - a.s);
    const top = res.slice(0, 15);
    box.innerHTML = top.length ? top.map((r, k) => `<button class="gs-hit gk-hit" data-k="${k}"><b>${r.t === 'f' ? esc(r.it.f) : `❓ ${esc(r.it.q)}`}</b><small><span aria-hidden="true">${r.c.emoji}</span> ${esc(r.c.name)}${r.t === 'q' ? ' · quiz question' : ''}</small></button>`).join('') + (res.length > 15 ? `<p class="sub gs-none">${res.length - 15} more… add another word to narrow it down.</p>` : '') : '<p class="sub gs-none">No facts found. Try another word.</p>';
    box.querySelectorAll('.gk-hit').forEach(bn => bn.onclick = () => {
      const r = top[+bn.dataset.k]; tap('open');
      if (r.t === 'f') { const list = r.c.facts.map(f => ({ ...f, c: r.c.id })); learn(list, list.findIndex(f => f.id === r.it.id), `📖 ${esc(r.c.name)}`, true); }
      else quiz([r.it]);
    });
  }

  /* keyboard: ← and → move through learn cards */
  document.addEventListener('keydown', e => {
    if (!document.getElementById('s-gk')?.classList.contains('active') || e.ctrlKey || e.metaKey || e.altKey) return;
    const a = document.activeElement; if (a && /^(input|textarea|select)$/i.test(a.tagName)) return;
    if (e.key === 'ArrowRight' && document.querySelector('#s-gk .gk-lc')) { document.getElementById('nx')?.click(); e.preventDefault(); }
    if (e.key === 'ArrowLeft' && document.querySelector('#s-gk .gk-lc')) { const p = document.getElementById('gkPrev'); if (p && !p.disabled) { p.click(); e.preventDefault(); } }
  });

  /* ---------- hooks: home screen snacks, and a card on Me ---------- */
  const _world = worldScreen;
  worldScreen = async function () { stopRun(); const r = await _world.apply(this, arguments); try { await snacks(); } catch (e) {} return r; };
  const _me = meScreen;
  meScreen = function () {
    stopRun(); const r = _me.apply(this, arguments);
    const host = document.getElementById('s-me');
    host && host.querySelectorAll(':scope > #gkSnack, :scope > .gk-mecard').forEach(x => x.remove());   // both live on World
    return r;
  };
  function meCard(host, anchorSel) {           // GK Explorer card on World (school) and the CA Journey, right after Brain Snacks
    if (!host || host.querySelector('#meGk')) return; document.getElementById('meGk')?.closest('.gk-mecard')?.remove();
    const anchor = host.querySelector(anchorSel || '.statrow') || host.firstElementChild;
    const html = `<div class="card gk-mecard"><div class="gk-meh"><span class="gk-mee" aria-hidden="true">🧭</span><div><h3>GK Explorer</h3><p class="sub">Free bonus: ${Object.keys(G().seen).length} facts learned · best streak ${G().best}</p></div></div><button class="btn" id="meGk">Explore general knowledge ▶</button></div>`;
    if (anchor) anchor.insertAdjacentHTML('afterend', html); else host.insertAdjacentHTML('beforeend', html);
    document.getElementById('meGk').onclick = () => { tap('open'); open({ from: 'me' }); };
  }
  /* 🧭 GK Explorer tile on Practice (school, after Mind Gym) and in the CA practice hub — and never as a second card on World */
  function practiceTile() {
    document.querySelectorAll('#s-world > .gk-mecard, #s-ca > .gk-mecard').forEach(x => x.remove());
    if (!ST.profile || (window.Cloud && Cloud.isParent && Cloud.isParent())) return;
    const sub = `${Object.keys(G().seen).length} facts learned · quizzes, speed rounds and fact streaks`;
    const p = document.getElementById('s-practice');
    if (p && p.classList.contains('active') && !p.querySelector(':scope > #gkTile')) {
      const after = p.querySelector(':scope > #mgTile') || p.querySelector(':scope > #phTile');
      if (after) after.insertAdjacentHTML('afterend', `<button type="button" class="card mg-tile gk-tile" id="gkTile"><span class="mg-te" aria-hidden="true">🧭</span><span class="mg-tt"><b>GK Explorer</b><small>${sub}</small></span><span class="mg-chev" aria-hidden="true">›</span></button>`);
    }
    const c = document.getElementById('s-ca'), hubs = c && c.classList.contains('active') ? c.querySelector(':scope > .ca-hubs') : null;
    if (hubs && !hubs.querySelector('#gkTile')) { const after = hubs.querySelector(':scope > #mgTile') || hubs.querySelector(':scope > #phTile'); if (after) after.insertAdjacentHTML('afterend', `<button type="button" class="card ca-hub" id="gkTile"><b class="ca-hube" aria-hidden="true">🧭</b><span><b>GK Explorer</b><small>${sub}</small></span></button>`); }
    const t = document.getElementById('gkTile'); if (t && !t.onclick) t.onclick = () => { tap('open'); open({ from: 'practice' }); };
  }
  if (!document.getElementById('gkTileCss')) document.head.insertAdjacentHTML('beforeend', '<style id="gkTileCss">.gk-tile{background:linear-gradient(135deg,#ff9a3c,#f5b700)!important;margin-top:10px}#s-ca .ca-hubs #gkTile{margin-bottom:10px}</style>');
  let pt = 0; new MutationObserver(() => { if (!pt) pt = requestAnimationFrame(() => { pt = 0; try { practiceTile(); } catch (e) {} }); }).observe(document.querySelector('main') || document.body, { childList: true, subtree: true });
  window.GK = { open, snacks, dayInfo, pickDay, meCard };
})();
