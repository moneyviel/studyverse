/* ================= 🧠 Mind Gym (js/mindgym.js) =================
   Five fun thinking-skill practices, opened from a tile in the Practice tab (school and CA):
     🧠 Brain Power (IQ-style puzzles)   💛 Heart Smarts (feelings)   🤝 People Skills (getting along)
     🌱 Bounce-Back (setbacks)           💡 Idea Spark (curiosity and creativity)
   Questions: content/mind/<test>.json (made by tools/mind/gen_iq.py and tools/mind/build.py).
   Band by age: j = Grades 1–3 (pictures, big buttons), m = Grades 4–8 (quests), s = Grades 9–12 (missions),
   p = CA (workplace scenarios; Brain Power uses the s puzzles).
   Engagement rule: 20 questions per practice are open at the start, and every 2 finished topics (CA: units)
   open 10 more in every practice. The owner account sees everything.
   Answers are checked by the app only — students can never mark themselves right.
   This is fun practice: no IQ number, no labels, no medical or psychological claims (see NOTE).
   Progress: ST.mind = { seen: {qid: 1|0 (last answer right)}, log: {test: [1,0,…last 40]}, rounds: {test: n} }
   window.MindGym = { open } */
(function () {
  'use strict';
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const STx = () => { try { return ST; } catch (e) { return null; } };
  const isCA = () => { const s = STx(); return !!(s && s.profile && s.profile.course === 'ca'); };
  const isParent = () => { try { return !!(window.Cloud && Cloud.isParent && Cloud.isParent()); } catch (e) { return false; } };
  const isOwner = () => { try { return !!(window.Cloud && Cloud.admin && Cloud.admin()); } catch (e) { return false; } };
  const persist = () => { try { save(); } catch (e) {} };

  const TESTS = [
    { id: 'iq', e: '🧠', n: 'Brainstorm Arena', d: 'Logic, patterns and picture puzzles', col: '#6d4aff' },
    { id: 'eq', e: '🧭', n: 'Heart Compass', d: 'Read and handle feelings, yours and others’', col: '#d99a00' },
    { id: 'sq', e: '🪐', n: 'Friendship Galaxy', d: 'Get along, team up and play fair', col: '#1e9e6a' },
    { id: 'aq', e: '🚀', n: 'Rise-Again Rocket', d: 'Bounce back when things go wrong', col: '#ff7a1a' },
    { id: 'cq', e: '💡', n: 'Idea Factory', d: 'Curiosity and creative ideas', col: '#e0408f' }];
  const T = id => TESTS.find(t => t.id === id);
  const START = 20, PER = 10, STEP = 2, ROUND = { j: 6, m: 8, s: 10, p: 10 };
  const NOTE = 'Mind Gym is fun practice to grow thinking skills. Ratings show how you are doing in these practice questions only. It is not an IQ test or a medical or psychological assessment, and it never labels anyone. Feelings and people questions follow widely used school social-emotional learning ideas.';
  const LOOK = { j: { tag: 'Picture puzzles and stories', round: 'game' }, m: { tag: 'Quests for sharp minds', round: 'quest' },
    s: { tag: 'Missions to level up', round: 'mission' }, p: { tag: 'Workplace and study scenarios', round: 'set' } };
  const KIND = { series: 'Number & letter series', picture: 'Picture patterns', odd: 'Odd one out', 'odd-pic': 'Odd one out', 'odd-word': 'Odd one out', machine: 'Number machines',
    letters: 'Number & letter series', code: 'Secret codes', direction: 'Directions', calendar: 'Calendar & clocks', clock: 'Calendar & clocks', rank: 'Ranking & ages', age: 'Ranking & ages',
    grid: 'Number grids', analogy: 'Analogies', mirror: 'Mirror & water images', water: 'Mirror & water images', 'p-series': 'Figure series', 'p-odd': 'Odd figure out',
    'p-analogy': 'Figure analogies', paper: 'Paper folding', count: 'Counting figures', dice: 'Dice', matrix: 'Figure matrix', symmetry: 'Symmetry' };
  const PICK = new Set(['mirror', 'water', 'series', 'odd', 'analogy', 'paper', 'count', 'dice', 'matrix', 'symmetry']);
  const skillOf = q => q.pic ? KIND[(['series', 'odd', 'analogy'].includes(q.k) ? 'p-' : '') + q.k] || 'Pictures' : KIND[q.k] || 'Thinking';
  /* qualitative rating for each practice */
  const LEVELS = [['Warming up', 0], ['Explorer', 1], ['Rising star', 2], ['Pro', 3], ['Champion', 4]];
  const SAY = {
    iq: ['Play a few rounds to get your rating.', 'You are learning the tricks. Read each “why” to spot the pattern faster.', 'Good spotting! You find most patterns. Try the picture puzzles too.', 'Sharp thinker! You crack patterns and pictures quickly.', 'Puzzle champion! Patterns, codes and pictures can’t hide from you.'],
    eq: ['Play a few rounds to get your rating.', 'You are learning to name feelings. Keep reading the “why”.', 'You often pick the calm, kind choice. Nice!', 'You read feelings well and handle them wisely.', 'Feelings expert! You stay calm and help others feel understood.'],
    sq: ['Play a few rounds to get your rating.', 'You are learning how friends and teams work.', 'You often choose fair and friendly. Great teammate!', 'You include others and solve fights fairly.', 'Super teammate! People can count on you to be fair and kind.'],
    aq: ['Play a few rounds to get your rating.', 'You are learning to bounce back. Every try counts!', 'You usually look for a plan when things go wrong.', 'You turn setbacks into steps forward.', 'Comeback champion! You learn from every fall and rise again.'],
    cq: ['Play a few rounds to get your rating.', 'You are starting to ask “what if?”. Keep wondering!', 'Your ideas are getting fresh and useful.', 'Creative thinker! You find new uses and smart solutions.', 'Idea champion! Curious, inventive and practical.'] };

  function band() {
    const s = STx(); if (!s || !s.profile) return 'm';
    if (isCA()) return 'p';
    const g = +s.profile.grade || 5; return g <= 3 ? 'j' : g <= 8 ? 'm' : 's';
  }
  const qBand = (test, b) => test === 'iq' && b === 'p' ? 's' : b;
  function M() { const s = STx(); s.mind = s.mind && typeof s.mind === 'object' ? s.mind : {}; const m = s.mind; ['seen', 'log', 'rounds', 'kinds', 'hist', 'total'].forEach(k => { m[k] = m[k] || {}; }); return m; }

  /* finished learning steps — only REAL learning counts, so tapping through can't unlock anything:
     school: a topic counts once its quiz earned ⭐⭐ or more (70%+ correct)
     CA: a unit counts once Learn is done and its MCQs were answered with 60%+ correct (latest answer to each question) */
  function caUnitPassed(s, uid) {
    const c = s.ca || {}, last = {};
    Object.entries(c.mcq || {}).forEach(([k, v]) => { if (k.startsWith(uid + '#')) last[k] = v && v.s > v.w; });
    (c.mlog || []).forEach(x => { if (x && typeof x[1] === 'string' && x[1].startsWith(uid + '#')) last[x[1]] = !!x[2]; });
    const n = Object.keys(last).length; if (n < 3) return false;
    return Object.values(last).filter(Boolean).length / n >= 0.6;
  }
  function steps() {
    const s = STx(); if (!s) return 0;
    if (isCA()) { const u = (s.ca && s.ca.units) || {}; return Object.keys(u).filter(k => u[k] && u[k].learn && u[k].mcq && caUnitPassed(s, k)).length; }
    return Object.keys(s.topics || {}).filter(k => s.topics[k] && s.topics[k].stars >= 2).length;
  }
  const stepWord = n => (isCA() ? 'unit' : 'topic') + (n === 1 ? '' : 's') + (isCA() ? ' (60%+ in its MCQs)' : ' with ⭐⭐');

  /* question banks, in a fixed mixed order (so each new pack has a mix of puzzle types) */
  const BANK = {};
  const hash = s => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };
  const okQ = q => q && q.id && Array.isArray(q.o) && q.o.length === 4 && q.a >= 0 && q.a < 4;
  async function bank(test) {
    if (!BANK[test]) {
      const d = await loadJSON(`content/mind/${test}.json`); let L = (d.questions || []).filter(okQ);
      if (test === 'iq') {
        try { const p = await loadJSON('content/mind/pics.json'); if (window.MindPics) { MindPics.init(p); L = L.concat((p.questions || []).filter(q => okQ(q) && PICK.has(q.k)).map(q => Object.assign(q, { pic: true }))); } } catch (e) {}
      }
      BANK[test] = L.sort((a, b) => hash(a.id) - hash(b.id));
    }
    return BANK[test];
  }
  async function pool(test) { const b = qBand(test, band()); return (await bank(test)).filter(q => q.b === b); }
  function openCount(total) { if (isOwner()) return total; return Math.min(total, START + PER * Math.floor(steps() / STEP)); }
  function nextUnlock(total) {
    if (isOwner() || openCount(total) >= total) return null;
    const need = STEP - (steps() % STEP); return { need, gets: Math.min(PER, total - openCount(total)) };
  }

  /* how many challenges exist per practice and age band (content/mind/counts.json, tiny) — for reminders outside Mind Gym */
  let COUNTS = null, countsP = null;
  const loadCounts = () => countsP || (countsP = loadJSON('content/mind/counts.json').then(c => { COUNTS = c; return c; }).catch(() => { countsP = null; return null; }));
  function unlockInfo() {
    if (!COUNTS || isOwner()) return null;
    const b = band(), shut = TESTS.map(t => (COUNTS[t.id] || {})[qBand(t.id, b)] || 0).filter(n => openCount(n) < n);
    if (!shut.length) return null;
    const need = STEP - (steps() % STEP); return { need, gets: Math.min(PER, Math.max(...shut) - openCount(Math.max(...shut))) };
  }
  const goLearn = () => { try { if (isCA() && window.Ca) Ca.home(); else worldScreen(); } catch (e) {} };

  /* rating from the last 40 answers (words and stars, never an IQ-style number) */
  function level(test) {
    const l = M().log[test] || [];
    const pct = l.length ? Math.round(l.filter(Boolean).length / l.length * 100) : 0;
    if (l.length < 10) return { i: 0, n: LEVELS[0][0], pct, few: true };
    const i = pct >= 85 ? 4 : pct >= 70 ? 3 : pct >= 50 ? 2 : 1;
    return { i, n: LEVELS[i][0], pct };
  }
  const stars = i => '★'.repeat(i + (i ? 0 : 0)) + '☆'.repeat(4 - i);
  const BADGE = ['✨', '🧭', '⭐', '🌟', '🏆'];

  /* ---------- screen ---------- */
  function screen() {
    let s = D.getElementById('s-mind');
    if (!s) { $1('main').insertAdjacentHTML('beforeend', '<section class="screen" id="s-mind"></section>'); s = D.getElementById('s-mind'); }
    return s;
  }
  const backToPractice = () => { if (isCA() && window.CaTools && CaTools.practiceHub) CaTools.practiceHub(); else practiceScreen(); };

  /* five-point "skills star" chart: one point per practice */
  function radar(info) {
    const cx = 110, cy = 105, R = 78, pt = (i, f) => { const a = -Math.PI / 2 + i * 2 * Math.PI / 5; return [cx + Math.cos(a) * R * f, cy + Math.sin(a) * R * f]; };
    const ring = f => info.map((_, i) => pt(i, f).join(',')).join(' ');
    const val = info.map((x, i) => pt(i, Math.max(.06, (x.lv.few ? 0 : x.lv.pct) / 100)).join(',')).join(' ');
    return `<svg viewBox="0 0 220 215" class="mg-radar" role="img" aria-label="Skills star: ${info.map(x => `${x.t.n} ${x.lv.few ? 'not rated yet' : x.lv.pct + '%'}`).join(', ')}">
      ${[.25, .5, .75, 1].map(f => `<polygon points="${ring(f)}" class="mg-rr"/>`).join('')}${info.map((_, i) => `<line x1="${cx}" y1="${cy}" x2="${pt(i, 1)[0]}" y2="${pt(i, 1)[1]}" class="mg-rr"/>`).join('')}
      <polygon points="${val}" class="mg-rv"/>${info.map((x, i) => { const [px, py] = pt(i, 1.17); return `<text x="${px}" y="${py + 6}" text-anchor="middle" font-size="18">${x.t.e}</text>`; }).join('')}</svg>`;
  }

  async function open() {
    style(); const el = screen(); show('mind', 'practice'); window.scrollTo(0, 0);
    const b = band(), lk = LOOK[b];
    el.innerHTML = `<div class="mg-root mg-${b}"><button class="back" id="mgBack">← Practice</button><div class="hello mg-hello" role="heading" aria-level="1"><span aria-hidden="true">🧠</span> Mind Gym <small>${E(lk.tag)}</small></div><div class="card mg-wait">Loading…</div></div>`;
    $1('#mgBack').onclick = () => { S('tap'); backToPractice(); };
    let info;
    try { info = await Promise.all(TESTS.map(async t => { const p = await pool(t.id); return { t, total: p.length, open: openCount(p.length), lv: level(t.id), nx: nextUnlock(p.length) }; })); }
    catch (e) { $1('.mg-wait', el).textContent = 'Could not load Mind Gym. Check your internet and try again.'; return; }
    const st = steps(), nx = info.map(i => i.nx).filter(Boolean)[0];
    const prog = nx ? `<div class="card mg-unlock"><b>🔓 Finish ${nx.need} more ${stepWord(nx.need)} to unlock ${nx.gets} new challenges in every practice.</b><div class="mg-bar"><i style="width:${Math.round(((STEP - nx.need) / STEP) * 100)}%"></i></div><small>Learning opens new challenges. ${st} ${stepWord(st)} finished so far.</small></div>` : '';
    $1('.mg-wait', el).outerHTML = `${prog}
      <div class="mg-list">${info.map(i => `<button type="button" class="card mg-test" data-t="${i.t.id}" style="--c:${i.t.col}">
        <span class="mg-e" aria-hidden="true">${i.t.e}</span><span class="mg-tt"><b>${E(i.t.n)}</b><small>${E(i.t.d)}</small>
        <small class="mg-meta">${BADGE[i.lv.i]} ${E(i.lv.n)} · ${i.open} of ${i.total} challenges open</small></span><span class="mg-chev" aria-hidden="true">›</span></button>`).join('')}</div>
      <div class="card mg-sc"><h3><span aria-hidden="true">📊</span> My scorecard</h3>
        <div class="mg-scwrap">${radar(info)}<div class="mg-scl">${info.map(i => `<button type="button" class="mg-scr" data-sc="${i.t.id}" style="--c:${i.t.col}"><span>${i.t.e} <b>${E(i.t.n)}</b></span><span class="mg-st" aria-label="${i.lv.i} of 4 stars">${stars(i.lv.i)}</span><small>${BADGE[i.lv.i]} ${E(i.lv.n)}${i.lv.few ? '' : ' · ' + i.lv.pct + '%'}</small></button>`).join('')}</div></div>
        <p class="sub mg-lvl">Ratings: ✨ Warming up → 🧭 Explorer → ⭐ Rising star → 🌟 Pro → 🏆 Champion, from your last 40 answers. Tap any practice for its full scorecard.</p></div>
      <div class="card mg-note">ℹ️ ${E(NOTE)}</div>`;
    el.querySelectorAll('[data-t]').forEach(x => x.onclick = () => { S('open'); go(x.dataset.t); });
    el.querySelectorAll('[data-sc]').forEach(x => x.onclick = () => { S('open'); card(x.dataset.sc); });
  }

  /* Brainstorm Arena: choose mixed, logic or pictures */
  async function iqMenu() {
    style(); const el = screen(), b = band(), all = await pool('iq'), op = all.slice(0, openCount(all.length)); show('mind', 'practice'); window.scrollTo(0, 0);
    const n = f => op.filter(f).length;
    el.innerHTML = `<div class="mg-root mg-${b}" style="--c:${T('iq').col}"><button class="back" id="mgQuit">← Mind Gym</button>
      <div class="hello mg-hello" role="heading" aria-level="1"><span aria-hidden="true">🧠</span> Brainstorm Arena <small>Pick your challenge</small></div>
      ${window.MindPlay ? `<button type="button" class="card mg-play-hub" id="mgPlay"><span class="mg-e" aria-hidden="true">${{ j: '🎪', m: '🗺️', s: '🧪', p: '🧪' }[b]}</span><span class="mg-tt"><b>${{ j: 'Brain Carnival', m: 'Brain Quest', s: 'Brain Lab', p: 'Brain Lab' }[b]}</b><small>${b === 'j' ? 'Memory, number towers, seesaws, magic boxes and more!' : 'Hands-on games: memory, balance, pyramids, wheels, cube folding, anagrams + a timed test'}</small></span><span class="mg-chev" aria-hidden="true">›</span></button>` : ''}
      <div class="mg-list">${[['mix', '🎲', 'Mix it up', 'A bit of everything', n(() => 1)], ['pic', '🖼️', 'Picture puzzles', 'Mirrors, paper folding, dice, shapes and more', n(q => q.pic)], ['logic', '🔢', 'Logic & numbers', 'Series, codes, directions and riddles', n(q => !q.pic)]]
        .map(([id, e, t, d, c]) => `<button type="button" class="card mg-test" data-m="${id}" style="--c:${T('iq').col}"><span class="mg-e" aria-hidden="true">${e}</span><span class="mg-tt"><b>${t}</b><small>${d}</small><small class="mg-meta">${c} challenges open</small></span><span class="mg-chev" aria-hidden="true">›</span></button>`).join('')}</div>
      <button class="btn ghost" type="button" id="mgSc">📊 Brainstorm Arena scorecard</button></div>`;
    $1('#mgQuit').onclick = () => { S('tap'); open(); };
    $1('#mgSc').onclick = () => { S('open'); card('iq'); };
    const ph = $1('#mgPlay'); if (ph) ph.onclick = () => { S('open'); MindPlay.hub(); };
    el.querySelectorAll('[data-m]').forEach(x => x.onclick = () => { S('open'); round('iq', x.dataset.m); });
  }

  /* Heart Compass: games, scenario questions, scorecard */
  function eqMenu() {
    style(); const el = screen(), b = band(), t = T('eq'); show('mind', 'practice'); window.scrollTo(0, 0);
    const th = { j: ['🎈', 'Feelings Fair', 'Face detective, feeling thermometer, bubble breathing and more!'], m: ['🧭', 'Heart Quest', 'Read faces, chat with friends, choose your path, calm your breath'], s: ['💠', 'Heart Lab', 'Six hands-on emotional-intelligence games + a timed Heart Check'], p: ['💠', 'Heart Lab', 'Six hands-on emotional-intelligence games + a timed Heart Check'] }[b];
    el.innerHTML = `<div class="mg-root mg-${b}" style="--c:${t.col}"><button class="back" id="mgQuit">← Mind Gym</button>
      <div class="hello mg-hello" role="heading" aria-level="1"><span aria-hidden="true">🧭</span> Heart Compass <small>Feelings, empathy and wise choices</small></div>
      <button type="button" class="card mg-play-hub hp-hubcard" id="mgHeart"><span class="mg-e" aria-hidden="true">${th[0]}</span><span class="mg-tt"><b>${th[1]}</b><small>${th[2]}</small></span><span class="mg-chev" aria-hidden="true">›</span></button>
      <div class="mg-list"><button type="button" class="card mg-test" id="mgScen" style="--c:${t.col}"><span class="mg-e" aria-hidden="true">💭</span><span class="mg-tt"><b>What would you do?</b><small>Real-life situations — pick the wisest, kindest choice</small></span><span class="mg-chev" aria-hidden="true">›</span></button></div>
      <button class="btn ghost" type="button" id="mgSc">📊 Heart Compass scorecard</button></div>`;
    $1('#mgQuit').onclick = () => { S('tap'); open(); };
    $1('#mgHeart').onclick = () => { S('open'); MindPlay.hub('eq'); };
    $1('#mgScen').onclick = () => { S('open'); round('eq'); };
    $1('#mgSc').onclick = () => { S('open'); card('eq'); };
  }
  const go = id => id === 'iq' ? iqMenu() : id === 'eq' && window.HeartPlay ? eqMenu() : SX[id] && window.SuitesUI ? suiteMenu(id) : round(id);
  /* Friendship Galaxy / Rise-Again Rocket / Idea Factory: games hub, scenario questions, scorecard */
  const SX = { sq: { e: '🪐', n: 'Friendship Galaxy', sub: 'Fairness, teamwork and kind, brave words', th: { j: ['🪐', 'Friendship Planet', 'Fair sharing, team helpers, kind words and more!'], m: ['🌌', 'Galaxy Quest', 'Five friendship missions + a timed Galaxy Expedition'], s: ['🛰️', 'Social Lab', 'Five hands-on people-skills games + a timed check'] } },
    aq: { e: '🚀', n: 'Rise-Again Rocket', sub: 'Bounce back, keep going, plan your way up', th: { j: ['🚀', 'Rocket Park', 'Rocket launches, “not yet” thoughts, feel-better tools!'], m: ['🌋', 'Rise Quest', 'Five never-give-up missions + a timed Summit Expedition'], s: ['🧗', 'Resilience Lab', 'Five hands-on resilience games + a timed check'] } },
    cq: { e: '💡', n: 'Idea Factory', sub: 'Imagine, connect and invent', th: { j: ['🎨', 'Idea Playground', 'Riddles, word glue, clever new uses and more!'], m: ['🏭', 'Invention Quest', 'Five inventor missions + a timed Inventor Expedition'], s: ['🧠', 'Innovation Lab', 'Five hands-on creativity games + a timed check'] } } };
  function suiteMenu(id) {
    style(); const el = screen(), b = band(), t = T(id), c = SX[id], th = c.th[b === 'p' ? 's' : b]; show('mind', 'practice'); window.scrollTo(0, 0);
    el.innerHTML = `<div class="mg-root mg-${b}" style="--c:${t.col}"><button class="back" id="mgQuit">← Mind Gym</button>
      <div class="hello mg-hello" role="heading" aria-level="1"><span aria-hidden="true">${c.e}</span> ${E(c.n)} <small>${E(c.sub)}</small></div>
      <button type="button" class="card mg-play-hub" id="mgHub"><span class="mg-e" aria-hidden="true">${th[0]}</span><span class="mg-tt"><b>${E(th[1])}</b><small>${E(th[2])}</small></span><span class="mg-chev" aria-hidden="true">›</span></button>
      <div class="mg-list"><button type="button" class="card mg-test" id="mgScen" style="--c:${t.col}"><span class="mg-e" aria-hidden="true">💭</span><span class="mg-tt"><b>What would you do?</b><small>Real-life situations — pick the wisest choice</small></span><span class="mg-chev" aria-hidden="true">›</span></button></div>
      <button class="btn ghost" type="button" id="mgSc">📊 ${E(c.n)} scorecard</button></div>`;
    $1('#mgQuit').onclick = () => { S('tap'); open(); };
    $1('#mgHub').onclick = () => { S('open'); MindPlay.hub(id); };
    $1('#mgScen').onclick = () => { S('open'); round(id); };
    $1('#mgSc').onclick = () => { S('open'); card(id); };
  }
  /* Heart Wheel: five skills as petals (longer petal = stronger), plus a zone gauge — words, never an EQ number */
  const HSK = [['Know my feelings', '🪞', '#ff7a59'], ['Manage my feelings', '🫧', '#3cbf7f'], ['Read others', '🕵️', '#2b8cff'], ['Connect & care', '💬', '#e0408f'], ['Choose wisely', '🛤️', '#ffb400']];
  const ZONES = [['🌱 Growing', '#f4a261'], ['🌿 Building', '#ffd166'], ['🌳 Strong', '#8ad17c'], ['🌟 Shining', '#2fbf71']];
  function heartWheel(K) {
    const cx = 110, cy = 110, r0 = 26, R = 78;
    const wedge = (i, f, col) => { const a0 = (-90 + i * 72 + 2) * Math.PI / 180, a1 = (-90 + (i + 1) * 72 - 2) * Math.PI / 180, r1 = r0 + (R - r0) * f;
      const P = (r, a) => `${(cx + r * Math.cos(a)).toFixed(1)},${(cy + r * Math.sin(a)).toFixed(1)}`;
      return `<path d="M${P(r0, a0)} L${P(r1, a0)} A${r1} ${r1} 0 0 1 ${P(r1, a1)} L${P(r0, a1)} A${r0} ${r0} 0 0 0 ${P(r0, a0)}Z" fill="${col}"/>`; };
    const pct = k => { const v = K[k]; return v && v[1] ? v[0] / v[1] : 0; };
    return `<svg viewBox="0 0 220 220" class="mg-hwheel" role="img" aria-label="Heart wheel: ${HSK.map(([k]) => `${k} ${K[k] && K[k][1] ? Math.round(pct(k) * 100) + '%' : 'not played yet'}`).join(', ')}">
      ${HSK.map(([k, , c], i) => wedge(i, 1, c + '22')).join('')}${HSK.map(([k, , c], i) => wedge(i, Math.max(.04, pct(k)), c)).join('')}
      <circle cx="${cx}" cy="${cy}" r="${r0 - 3}" fill="#fff"/><text x="${cx}" y="${cy + 8}" text-anchor="middle" font-size="22">💗</text>
      ${HSK.map(([k, e], i) => { const a = (-90 + i * 72 + 36) * Math.PI / 180; return `<text x="${(cx + 96 * Math.cos(a)).toFixed(1)}" y="${(cy + 96 * Math.sin(a) + 6).toFixed(1)}" text-anchor="middle" font-size="16">${e}</text>`; }).join('')}</svg>`;
  }
  function gauge(f) {
    const z = f >= .85 ? 3 : f >= .7 ? 2 : f >= .5 ? 1 : 0, ang = -90 + 180 * Math.max(0, Math.min(1, f));
    const arc = (i, col) => { const a0 = Math.PI * (1 + i / 4), a1 = Math.PI * (1 + (i + 1) / 4), P = a => `${(100 + 80 * Math.cos(a)).toFixed(1)},${(100 + 80 * Math.sin(a)).toFixed(1)}`;
      return `<path d="M${P(a0)} A80 80 0 0 1 ${P(a1)}" stroke="${col}" stroke-width="22" fill="none"/>`; };
    return `<div class="mg-gauge"><svg viewBox="0 0 200 112" aria-hidden="true">${ZONES.map(([, c], i) => arc(i, c)).join('')}<g style="transform:rotate(${ang}deg);transform-origin:100px 100px;transition:transform 1s"><line x1="100" y1="100" x2="100" y2="34" stroke="#1f2d33" stroke-width="4" stroke-linecap="round"/></g><circle cx="100" cy="100" r="8" fill="#1f2d33"/></svg><b>${ZONES[z][0]}</b></div>`;
  }

  /* full scorecard for one practice */
  function card(test) {
    style(); const el = screen(), t = T(test), b = band(), m = M(), lv = level(test), l = m.log[test] || [], h = m.hist[test] || [], K = m.kinds[test] || {}; show('mind', 'practice'); window.scrollTo(0, 0);
    const best = h.length ? Math.max(...h) : 0, tot = m.total[test] || 0;
    const spark = h.length > 1 ? `<svg viewBox="0 0 200 60" class="mg-spark" role="img" aria-label="Round scores: ${h.join('%, ')}%"><polyline points="${h.map((v, i) => `${(i * 196 / (h.length - 1) + 2).toFixed(1)},${(56 - v * .52).toFixed(1)}`).join(' ')}" fill="none" stroke="${t.col}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>${h.map((v, i) => `<circle cx="${(i * 196 / (h.length - 1) + 2).toFixed(1)}" cy="${(56 - v * .52).toFixed(1)}" r="3" fill="${t.col}"/>`).join('')}</svg>` : '<p class="sub">Play two rounds to see your progress line.</p>';
    const skills = Object.entries(K).filter(([, v]) => v[1] >= 1).sort((a, b) => b[1][1] - a[1][1]);
    const strong = skills.filter(([, v]) => v[1] >= 3).sort((a, b) => b[1][0] / b[1][1] - a[1][0] / a[1][1]);
    el.innerHTML = `<div class="mg-root mg-${b}" style="--c:${t.col}"><button class="back" id="mgQuit">← Mind Gym</button>
      <div class="card mg-hero"><div class="mg-big" aria-hidden="true">${t.e}</div><h2>${E(t.n)} scorecard</h2>
        <div class="mg-badge"><span class="mg-st big" aria-label="${lv.i} of 4 stars">${stars(lv.i)}</span><b>${BADGE[lv.i]} ${E(lv.n)}</b></div><p>${E(SAY[test][lv.i])}</p></div>
      <div class="mg-tiles"><div class="card"><b>${lv.few ? '—' : lv.pct + '%'}</b><small>Recent accuracy</small></div><div class="card"><b>${tot}</b><small>Challenges done</small></div><div class="card"><b>${m.rounds[test] || 0}</b><small>Rounds played</small></div><div class="card"><b>${h.length ? best + '%' : '—'}</b><small>Best round</small></div></div>
      <div class="card"><h3>📈 My rounds</h3>${spark}</div>
      <div class="card"><h3>🟢 Last ${l.length} answers</h3>${l.length ? `<div class="mg-dots">${l.map(v => `<i class="${v ? 'y' : 'n'}"></i>`).join('')}</div>` : '<p class="sub">No answers yet.</p>'}</div>
      ${test === 'eq' && skills.length ? (() => { const tot = skills.reduce((a, [, v]) => [a[0] + v[0], a[1] + v[1]], [0, 0]); return `<div class="card"><h3>💗 Heart Wheel</h3><div class="mg-hw">${heartWheel(K)}${gauge(tot[1] ? tot[0] / tot[1] : 0)}</div>
        ${HSK.map(([k, e, c]) => { const v = K[k]; return `<div class="mg-row"><span>${e} ${E(k)}</span><div class="mg-bar"><i style="width:${v && v[1] ? Math.round(v[0] / v[1] * 100) : 0}%;background:${c}"></i></div><b>${v && v[1] ? ZONES[(v[0] / v[1]) >= .85 ? 3 : (v[0] / v[1]) >= .7 ? 2 : (v[0] / v[1]) >= .5 ? 1 : 0][0].split(' ')[0] : '—'}</b></div>`; }).join('')}
        <p class="sub mg-lvl">Zones: 🌱 Growing → 🌿 Building → 🌳 Strong → 🌟 Shining, from your Heart Compass games. Longer petals = stronger skills.</p></div>`; })() : ''}
      ${test === 'eq' && (m.htests || []).length ? `<div class="card"><h3>⏱️ Timed check results</h3><div class="mg-tiles2">${m.htests.slice(-6).map(x => `<span><b>${x.pct}%</b><small>${new Date(x.at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}</small></span>`).join('')}</div></div>` : ''}
      ${(test === 'iq' || SX[test]) && skills.length ? `<div class="card"><h3>🧩 Skills</h3>${skills.map(([k, v]) => `<div class="mg-row"><span>${E(k)}</span><div class="mg-bar"><i style="width:${Math.round(v[0] / v[1] * 100)}%;background:${t.col}"></i></div><b>${v[0]}/${v[1]}</b></div>`).join('')}
        ${strong.length > 1 ? `<p class="sub mg-lvl">💪 Strongest: ${E(strong[0][0])} · 🎯 Practise more: ${E(strong[strong.length - 1][0])}</p>` : ''}</div>` : ''}
      ${SX[test] && (m[test + 'tests'] || []).length ? `<div class="card"><h3>⏱️ Timed check results</h3><div class="mg-tiles2">${m[test + 'tests'].slice(-6).map(x => `<span><b>${x.pct}%</b><small>${new Date(x.at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}</small></span>`).join('')}</div></div>` : ''}
      ${test === 'iq' && (m.btests || []).length ? `<div class="card"><h3>⏱️ Timed test results</h3><div class="mg-tiles2">${m.btests.slice(-6).map(x => `<span><b>${x.pct}%</b><small>${new Date(x.at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}</small></span>`).join('')}</div>
        ${(() => { const last = m.btests[m.btests.length - 1].sec; return Object.entries(last).map(([k, v]) => `<div class="mg-row"><span>${E(k)}</span><div class="mg-bar"><i style="width:${v}%;background:${t.col}"></i></div><b>${v}%</b></div>`).join(''); })()}<p class="sub mg-lvl">Bars show your latest timed test, skill by skill.</p></div>` : ''}
      <button class="btn" type="button" id="mgGo">Play ${E(t.n)} ▶</button>
      <div class="card mg-note">ℹ️ ${E(NOTE)}</div></div>`;
    $1('#mgQuit').onclick = () => { S('tap'); open(); };
    $1('#mgGo').onclick = () => { S('open'); go(test); };
  }

  /* ---------- a round ---------- */
  function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  function confetti(host) {
    const c = D.createElement('div'); c.className = 'mg-conf'; c.setAttribute('aria-hidden', 'true');
    c.innerHTML = Array.from({ length: 14 }, (_, i) => `<i style="--dx:${Math.round(Math.cos(i / 14 * 6.28) * (60 + Math.random() * 50))}px;--dy:${Math.round(Math.sin(i / 14 * 6.28) * (50 + Math.random() * 40) - 30)}px">${['⭐', '✨', '🎉', '💫'][i % 4]}</i>`).join('');
    host.appendChild(c); setTimeout(() => c.remove(), 1100);
  }
  async function round(test, mode) {
    style(); const el = screen(), t = T(test), b = band(), lk = LOOK[b], m = M(); show('mind', 'practice');
    const all = await pool(test);
    let open_ = all.slice(0, openCount(all.length));
    if (mode === 'pic') open_ = open_.filter(q => q.pic); else if (mode === 'logic') open_ = open_.filter(q => !q.pic);
    if (!open_.length) { toast('Finish more topics to open these challenges'); return; }
    const n = Math.min(ROUND[b], open_.length);
    const fresh = shuffle(open_.filter(q => !(q.id in m.seen)));
    const missed = shuffle(open_.filter(q => m.seen[q.id] === 0));
    const rest = shuffle(open_.filter(q => m.seen[q.id] === 1));
    const list = fresh.concat(missed, rest).slice(0, n);
    const ranOut = fresh.length < n, more = ranOut ? (await loadCounts(), unlockInfo()) : null;
    let i = 0, right = 0;
    const draw = () => {
      const q = list[i], order = shuffle([0, 1, 2, 3]), pic = !!(q.pic && window.MindPics), big = pic && !MindPics.textOpts(q);
      const optHTML = k => pic ? MindPics.opt(q, k) : E(q.o[k]);
      el.innerHTML = `<div class="mg-root mg-${b}" style="--c:${t.col}"><button class="back" id="mgQuit">← ${test === 'iq' ? 'Brainstorm Arena' : 'Mind Gym'}</button>
        <div class="card mg-play"><div class="mg-top"><span>${t.e} ${E(t.n)}</span><span>${i + 1} / ${list.length}</span></div>
          <div class="mg-bar"><i style="width:${Math.round(i / list.length * 100)}%;background:${t.col}"></i></div>
          ${i === 0 && ranOut ? `<div class="mg-out">🔁 You’ve seen every open challenge here, so some come back for practice.${more ? ` <b>Finish ${more.need} more ${stepWord(more.need)} to unlock ${more.gets} fresh ones!</b> <button type="button" class="mg-learn">📚 Go to my next ${isCA() ? 'unit' : 'topic'}</button>` : ''}</div>` : ''}
          <h3 class="mg-q${!pic && (q.k === 'picture' || q.k === 'odd-pic') ? ' pic' : ''}">${E(q.q)}</h3>${pic ? MindPics.stem(q) : ''}
          <div class="mg-opts${big || (!pic && q.k === 'odd-pic') ? ' picg' : ''}">${order.map((k, x) => `<button type="button" class="mg-o${pic || q.k === 'odd-pic' || q.k === 'picture' ? ' pic' : ''}" data-k="${k}"${pic && big ? ` aria-label="Option ${'ABCD'[x]}"` : ''}>${optHTML(k)}</button>`).join('')}</div>
          <div class="mg-fb" aria-live="polite"></div></div></div>`;
      if (pic) MindPics.wire(el);
      const lg = $1('.mg-learn', el); if (lg) lg.onclick = () => { S('open'); goLearn(); };
      $1('#mgQuit').onclick = () => { S('tap'); if (i > 0 || el.querySelector('.mg-o:disabled')) finish(true); else (test === 'iq' ? iqMenu() : open()); };
      el.querySelectorAll('.mg-o').forEach(btn => btn.onclick = () => {
        const k = +btn.dataset.k, ok = k === q.a;
        el.querySelectorAll('.mg-o').forEach(x => { x.disabled = true; if (+x.dataset.k === q.a) x.classList.add('ok'); });
        if (!ok) btn.classList.add('no'); else confetti(btn);
        S(ok ? 'right' : 'wrong'); if (ok) right++;
        m.seen[q.id] = ok ? 1 : 0; const L = m.log[test] = (m.log[test] || []); L.push(ok ? 1 : 0); if (L.length > 40) L.splice(0, L.length - 40);
        m.total[test] = (m.total[test] || 0) + 1;
        if (test === 'iq') { const sk = skillOf(q), K = m.kinds.iq = m.kinds.iq || {}; K[sk] = K[sk] || [0, 0]; K[sk][1]++; if (ok) K[sk][0]++; }
        persist();
        const scen = test !== 'iq';
        $1('.mg-fb', el).innerHTML = `<p class="mg-v ${ok ? 'ok' : 'no'}">${ok ? (scen ? '✅ Best choice!' : '✅ Correct!') : (scen ? '💭 There’s a better choice.' : '❌ Not quite.')}</p><p>${scen && !ok ? `<b>Best: ${E(q.o[q.a])}.</b> ` : ''}${E(q.why)}</p>
          ${pic ? '<button class="btn ghost mg-showme" type="button">▶ Show me</button><div class="mg-anim"></div>' : ''}
          <button class="btn" type="button" id="mgNext">${i + 1 < list.length ? 'Next ▶' : 'See my result'}</button>`;
        const sm = $1('.mg-showme', el); if (sm) sm.onclick = () => { S('open'); MindPics.show(q, $1('.mg-anim', el)); sm.textContent = '↻ Show me again'; };
        const nb = $1('#mgNext'); nb.focus({ preventScroll: true }); nb.onclick = () => { S('tap'); i++; if (i < list.length) draw(); else finish(false); };
      });
    };
    const finish = early => {
      const done = early ? i + (el.querySelector('.mg-o:disabled') ? 1 : 0) : list.length;
      if (!done) { open(); return; }
      m.rounds[test] = (m.rounds[test] || 0) + 1;
      const H = m.hist[test] = (m.hist[test] || []); H.push(Math.round(right / done * 100)); if (H.length > 20) H.splice(0, H.length - 20);
      persist();
      if (right) { try { addXP(right * 2); } catch (e) {} }
      const lv = level(test);
      const msg = right === done ? 'Perfect round! 🎉' : right >= done * 0.7 ? 'Great thinking!' : right >= done * 0.4 ? 'Good effort — every round makes you sharper.' : 'Nice try! Read the explanations and try another round.';
      el.innerHTML = `<div class="mg-root mg-${b}"><div class="card mg-done" style="--c:${t.col}"><div class="mg-big" aria-hidden="true">${t.e}</div><h2>${E(msg)}</h2>
        <p class="sub">${right} of ${done} ${test === 'iq' ? 'correct' : 'best choices'}${right ? ` · +${right * 2} ⭐` : ''}</p>
        ${more ? `<div class="mg-out">🔓 Finish <b>${more.need} more ${stepWord(more.need)}</b> to unlock <b>${more.gets} fresh challenges</b>. <button type="button" class="mg-learn">📚 Go to my next ${isCA() ? 'unit' : 'topic'}</button></div>` : ''}
        <div class="mg-badge"><span class="mg-st big">${stars(lv.i)}</span><b>${BADGE[lv.i]} ${E(lv.n)}</b></div><p class="sub">${E(SAY[test][lv.i])}</p>
        <button class="btn" type="button" id="mgAgain">Another ${E(lk.round)} ▶</button><div style="height:8px"></div><button class="btn ghost" type="button" id="mgCard">📊 My scorecard</button><div style="height:8px"></div><button class="btn ghost" type="button" id="mgHome">← Mind Gym</button></div></div>`;
      if (right === done) confetti($1('.mg-done', el));
      $1('#mgAgain').onclick = () => { S('open'); round(test, mode); };
      const lg2 = $1('.mg-learn', el); if (lg2) lg2.onclick = () => { S('open'); goLearn(); };
      $1('#mgCard').onclick = () => { S('open'); card(test); };
      $1('#mgHome').onclick = () => { S('tap'); open(); };
    };
    draw();
  }

  /* ---------- tile in the Practice tab ---------- */
  const tileSub = () => { const u = unlockInfo(); return u ? `🔓 ${u.need} more ${stepWord(u.need)} → ${u.gets} new challenges` : 'Brainstorm Arena, Heart Compass and more'; };
  /* 🔔 in-app reminders: after a topic/unit is finished, celebrate new challenges or say how close the next pack is */
  function watch() {
    const s = STx(); if (!s || !s.profile || isParent() || !COUNTS) return;
    const m = M(), now = steps();
    if (m.lastSteps == null || now < m.lastSteps) { m.lastSteps = now; persist(); return; }
    if (now === m.lastSteps) return;
    const before = m.lastSteps; m.lastSteps = now; persist();
    const opened = Math.floor(now / STEP) > Math.floor(before / STEP), u = unlockInfo();
    const shutBefore = TESTS.some(t => { const n = (COUNTS[t.id] || {})[qBand(t.id, band())] || 0; return START + PER * Math.floor(before / STEP) < n; });
    if (opened && shutBefore) nudge(`🔓 <b>New Mind Gym challenges unlocked!</b> Fresh puzzles and questions are waiting.`, 'Play now', () => open());
    else if (u && u.need === 1) nudge(`🎯 Just <b>1 more ${isCA() ? 'unit' : 'topic'}</b> to unlock ${u.gets} new Mind Gym challenges!`, null, null);
    const t = D.getElementById('mgTile'); if (t) { const sm = t.querySelector('small'); if (sm) sm.innerHTML = tileSub(); }
  }
  function nudge(html, btn, go) {
    style(); const old = D.getElementById('mgNudge'); if (old) old.remove();
    D.body.insertAdjacentHTML('beforeend', `<div id="mgNudge" class="mg-nudge" role="status"><span>${html}</span>${btn ? `<button type="button" class="mg-ng">${E(btn)} ▶</button>` : ''}<button type="button" class="mg-nx" aria-label="Close">✕</button></div>`);
    const n = D.getElementById('mgNudge'); S('right');
    if (btn) n.querySelector('.mg-ng').onclick = () => { n.remove(); S('open'); go(); };
    n.querySelector('.mg-nx').onclick = () => n.remove();
    setTimeout(() => { if (n.isConnected) n.remove(); }, 9000);
  }
  function place() {
    const s = STx(); if (!s || !s.profile || isParent()) return;
    const p = D.getElementById('s-practice');
    if (p && p.classList.contains('active') && !isCA() && !p.querySelector(':scope > #mgTile')) {
      const after = p.querySelector(':scope > #phTile');
      if (after) { after.insertAdjacentHTML('afterend', `<button type="button" class="card mg-tile" id="mgTile" aria-label="Mind Gym: thinking-skill challenges"><span class="mg-te" aria-hidden="true">🧠</span><span class="mg-tt"><b>Mind Gym</b><small>${tileSub()}</small></span><span class="mg-chev" aria-hidden="true">›</span></button>`); wire(); }
    }
    const c = D.getElementById('s-ca');
    if (c && isCA() && c.classList.contains('active')) {
      const hubs = c.querySelector(':scope > .ca-hubs');
      const after = hubs && hubs.querySelector(':scope > #phTile');
      if (after && !hubs.querySelector('#mgTile')) { after.insertAdjacentHTML('afterend', `<button type="button" class="card ca-hub" id="mgTile"><b class="ca-hube" aria-hidden="true">🧠</b><span><b>Mind Gym</b><small>${unlockInfo() ? tileSub() : 'Thinking, people and workplace skills'}</small></span><span class="ca-chev" aria-hidden="true">›</span></button>`); wire(); }
    }
  }
  function wire() { const t = D.getElementById('mgTile'); if (t) t.onclick = () => { S('open'); open(); }; }

  let css = false;
  function style() {
    if (css) return; css = true;
    D.head.insertAdjacentHTML('beforeend', `<style id="mgCss">
      .mg-tile{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:none;cursor:pointer;background:linear-gradient(135deg,#0f8f8a,#2bb3a3);color:#fff;font-family:inherit}
      .mg-tile .mg-te{font-size:34px}.mg-tile .mg-tt{flex:1;display:flex;flex-direction:column}.mg-tile b{font-size:19px}.mg-tile small{opacity:.92;font-size:13px}
      .mg-chev{font-size:24px;opacity:.7}.ca-hubs .mg-tile,.ca-hubs #mgTile{margin-bottom:10px}
      .mg-list{display:flex;flex-direction:column;gap:10px;margin-bottom:12px}
      .mg-test{display:flex;align-items:center;gap:12px;width:100%;text-align:left;cursor:pointer;font-family:inherit;border:2px solid transparent;border-left:6px solid var(--c);margin:0}
      .mg-test .mg-e{font-size:32px}.mg-test .mg-tt{flex:1;display:flex;flex-direction:column;gap:2px}.mg-test b{font-size:17px}.mg-test small{color:var(--muted,#666);font-size:13px}.mg-test .mg-meta{font-weight:700;color:var(--c)}
      .mg-bar{height:8px;border-radius:9px;background:rgba(0,0,0,.08);overflow:hidden;margin:8px 0}.mg-bar i{display:block;height:100%;border-radius:9px;background:#2bb3a3;transition:width .3s}
      .mg-unlock b{display:block;font-size:15px}.mg-unlock small{color:var(--muted,#666)}
      .mg-row{display:grid;grid-template-columns:minmax(120px,1fr) 2fr 42px;align-items:center;gap:8px;font-size:14px}.mg-row .mg-bar{margin:6px 0}.mg-row b{text-align:right}
      .mg-lvl{font-size:12px;margin-top:8px}.mg-note{font-size:12.5px;color:var(--muted,#555);line-height:1.45;margin-bottom:20px}
      .mg-top{display:flex;justify-content:space-between;font-weight:800;font-size:14px;color:var(--c)}
      .mg-q{font-size:19px;line-height:1.4;margin:10px 0 14px;white-space:pre-wrap;word-break:break-word}.mg-q.pic{font-size:30px;line-height:1.5}
      .mg-opts{display:grid;grid-template-columns:1fr;gap:10px}.mg-o{border:2px solid rgba(0,0,0,.12);border-radius:14px;background:#fff;color:#1f2d33;padding:13px 14px;font-size:16px;text-align:left;cursor:pointer;font-family:inherit;line-height:1.35}
      .mg-o.pic{font-size:34px;text-align:center;padding:8px}.mg-j .mg-opts:has(.pic){grid-template-columns:1fr 1fr}
      .mg-o:hover:not(:disabled){border-color:var(--c)}.mg-o.ok{border-color:#1e9e6a;background:#e6f7ef}.mg-o.no{border-color:#d33;background:#fdeaea}.mg-o:disabled{cursor:default;opacity:1}
      .mg-fb p{margin:10px 0 0;line-height:1.45}.mg-v{font-weight:900;font-size:17px}.mg-v.ok{color:#1e9e6a}.mg-v.no{color:#b5541d}.mg-fb .btn{margin-top:12px}
      .mg-out{margin:8px 0 10px;padding:10px 12px;border-radius:12px;background:#fff6dc;color:#5a4300;font-size:14px;line-height:1.4}
      .mg-learn{display:block;margin-top:8px;border:0;border-radius:999px;background:#ffc43d;color:#3a2a00;font-weight:800;font-size:14px;padding:8px 14px;cursor:pointer;font-family:inherit}
      .mg-nudge{position:fixed;left:12px;right:12px;bottom:84px;z-index:60;display:flex;align-items:center;gap:8px;padding:12px 12px 12px 14px;border-radius:16px;background:linear-gradient(135deg,#6d4aff,#e0408f);color:#fff;box-shadow:0 10px 30px rgba(0,0,0,.3);animation:mpPop .45s both;max-width:520px;margin:0 auto}
      .mg-nudge span{flex:1;font-size:14px;line-height:1.35}.mg-ng{border:0;border-radius:999px;background:#fff;color:#6d4aff;font-weight:900;padding:8px 12px;cursor:pointer;white-space:nowrap;font-family:inherit}.mg-nx{border:0;background:transparent;color:#fff;font-size:18px;cursor:pointer;padding:4px}
      .mg-play-hub{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:0;cursor:pointer;font-family:inherit;color:#fff;background:linear-gradient(135deg,#ff5fa2,#ffb13d);margin-bottom:10px;animation:mpPop .5s both}
      .mg-m .mg-play-hub{background:linear-gradient(135deg,#0f8f8a,#2b6cff)}.mg-s .mg-play-hub,.mg-p .mg-play-hub{background:linear-gradient(135deg,#1d2440,#3a2f7a)}
      .mg-play-hub .mg-e{font-size:38px}.mg-play-hub .mg-tt{flex:1;display:flex;flex-direction:column}.mg-play-hub b{font-size:19px}.mg-play-hub small{opacity:.9}
      .mg-tiles2{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}.mg-tiles2 span{display:flex;flex-direction:column;align-items:center;padding:6px 10px;border-radius:10px;background:rgba(0,0,0,.04)}.mg-tiles2 b{color:var(--c)}.mg-tiles2 small{font-size:11px;color:var(--muted,#666)}
      .hp-hubcard{background:linear-gradient(135deg,#ff7eb3,#ffd166)}.mg-m .hp-hubcard{background:linear-gradient(135deg,#ff7a59,#8e44ad)}.mg-s .hp-hubcard,.mg-p .hp-hubcard{background:linear-gradient(135deg,#3b1d4a,#0f3d4a)}
      .mg-hw{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:6px}.mg-hwheel{width:200px}.mg-gauge{display:flex;flex-direction:column;align-items:center;width:170px}.mg-gauge svg{width:170px}.mg-gauge b{font-size:18px}
      .mg-done{text-align:center;position:relative}.mg-big{font-size:56px}
      .mg-scwrap{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center}.mg-radar{width:200px;max-width:48%;min-width:170px}
      .mg-rr{fill:none;stroke:rgba(0,0,0,.12);stroke-width:1}.mg-rv{fill:rgba(109,74,255,.25);stroke:#6d4aff;stroke-width:2.5;stroke-linejoin:round;animation:mpPop .6s both}
      .mg-scl{flex:1;min-width:170px;display:flex;flex-direction:column;gap:6px}.mg-scr{display:grid;grid-template-columns:1fr auto;gap:0 8px;text-align:left;border:0;border-left:5px solid var(--c);border-radius:12px;background:rgba(0,0,0,.035);padding:7px 10px;cursor:pointer;font:inherit;color:inherit}
      .mg-scr small{grid-column:1/-1;color:var(--muted,#666);font-size:12px}.mg-st{color:#ffb400;letter-spacing:1px;font-size:15px}.mg-st.big{font-size:28px}
      .mg-hero{text-align:center}.mg-badge{display:flex;flex-direction:column;align-items:center;gap:2px;margin:6px 0}.mg-badge b{font-size:20px;color:var(--c)}
      .mg-tiles{display:grid;grid-template-columns:1fr 1fr;gap:10px}.mg-tiles .card{margin:0;text-align:center}.mg-tiles b{display:block;font-size:24px;color:var(--c)}.mg-tiles small{color:var(--muted,#666)}
      .mg-spark{width:100%;height:70px}.mg-dots{display:flex;flex-wrap:wrap;gap:4px}.mg-dots i{width:12px;height:12px;border-radius:50%}.mg-dots .y{background:#1e9e6a}.mg-dots .n{background:#e3a3a3}
      .mg-conf{position:absolute;left:50%;top:50%;pointer-events:none;z-index:5}.mg-conf i{position:absolute;font-style:normal;font-size:18px;animation:mgBurst 1s ease-out forwards}
      .mg-o{position:relative}.mg-o.no{animation:mgShake .4s}
      @keyframes mgBurst{from{transform:translate(0,0) scale(.4);opacity:1}to{transform:translate(var(--dx),var(--dy)) scale(1.1);opacity:0}}
      @keyframes mgShake{25%{transform:translateX(-6px)}50%{transform:translateX(6px)}75%{transform:translateX(-3px)}}
      @keyframes mpPop{from{transform:scale(.4);opacity:0}to{transform:none;opacity:1}}
      .mg-j .mg-q{font-size:21px}.mg-j .mg-o{font-size:18px;padding:15px;border-radius:18px}.mg-j .mg-test b{font-size:18px}
      .mg-s .mg-test,.mg-p .mg-test{border-left-width:4px}.mg-p .mg-o{border-radius:10px}
      .mg-o:focus-visible,.mg-test:focus-visible,.mg-tile:focus-visible{outline:3px solid #2b6cff;outline-offset:2px}
    </style>`);
  }

  function boot() {
    style();
    let t = 0; new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; try { place(); watch(); } catch (e) {} }); }).observe(D.body, { childList: true, subtree: true });
    loadCounts().then(() => { try { const x = D.getElementById('mgTile'); if (x) x.remove(); place(); watch(); } catch (e) {} });
    place();
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
  /* used by js/mindplay.js (brain games) */
  function record(test, kind, ok) {
    const m = M(), L = m.log[test] = (m.log[test] || []); L.push(ok ? 1 : 0); if (L.length > 40) L.splice(0, L.length - 40);
    m.total[test] = (m.total[test] || 0) + 1;
    const K = m.kinds[test] = m.kinds[test] || {}; K[kind] = K[kind] || [0, 0]; K[kind][1]++; if (ok) K[kind][0]++; persist();
  }
  window.MindGym = { open, card, iqMenu, eqMenu, suiteMenu, round, record, state: M, _steps: steps, _band: band, _owner: isOwner, _isCA: isCA, _screen: screen, _show: () => { style(); show('mind', 'practice'); } };
})();
