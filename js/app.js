/* ================= StudyVerse app ================= */
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const BOARDS = [
  { id: 'cbse', name: 'CBSE', live: true }, { id: 'icse', name: 'ICSE', live: false },
  { id: 'state', name: 'State Board', live: false }, { id: 'cambridge', name: 'Cambridge', live: false }, { id: 'ib', name: 'IB', live: false }
];
const AVATARS = ['🦁', '🐯', '🦊', '🐼', '🐨', '🐸', '🦄', '🐙', '🦉', '🐬', '🚀', '⭐'];
const MAX_GRADE = 10;

/* ---------- saved progress (on this phone until logins arrive) ---------- */
let ST = { profile: null, xp: 0, streak: { n: 0, last: '' }, topics: {}, mistakes: {}, qstats: {} };
try { const s = JSON.parse(localStorage.getItem('sv_state') || 'null'); if (s) ST = Object.assign(ST, s); } catch (e) {}
const save = () => { try { localStorage.setItem('sv_state', JSON.stringify(ST)); } catch (e) {} };
const today = () => new Date().toISOString().slice(0, 10);

let CUR = null;               // curriculum.json
const DATA = {};              // "g6/maths" -> subject content or null
let NAV = {};                 // where we are: {subject, chapter, topic}

function toast(m) { const t = $('#toast'); t.textContent = m; t.classList.add('show'); clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove('show'), 1900); }
function hud() { $('#xp').textContent = ST.xp; $('#streak').textContent = ST.streak.n || 0; }
function addXP(n, msg) { ST.xp += n; save(); hud(); if (msg) toast(`${msg}  +${n} ⭐`); }
function bumpStreak() { const d = today(); if (ST.streak.last === d) return; const y = new Date(Date.now() - 864e5).toISOString().slice(0, 10); ST.streak.n = ST.streak.last === y ? ST.streak.n + 1 : 1; ST.streak.last = d; save(); hud(); }

function show(id, navKey) {
  document.querySelectorAll('.screen').forEach(e => e.classList.remove('active'));
  $('#s-' + id).classList.add('active');
  document.querySelectorAll('nav button').forEach(b => b.classList.toggle('on', b.dataset.s === navKey));
  $('nav').style.display = id === 'topic' || id === 'onboard' ? 'none' : '';
  $('header').style.display = id === 'onboard' ? 'none' : '';
  window.scrollTo(0, 0);
}

async function loadJSON(p) { const r = await fetch(p, { cache: 'no-cache' }); if (!r.ok) throw new Error(r.status); return r.json(); }
async function subjectData(g, sid) {
  const k = `g${g}/${sid}`; if (k in DATA) return DATA[k];
  try { DATA[k] = await loadJSON(`content/${k}.json`); } catch (e) { DATA[k] = null; }
  return DATA[k];
}
const curSubjects = g => (CUR?.grades?.[g]?.subjects || []);
const topicStars = id => ST.topics[id]?.stars || 0;
function subjectPct(d) { if (!d) return 0; let t = 0, n = 0; d.chapters.forEach(c => c.topics.forEach(tp => { n++; if (topicStars(tp.id)) t++; })); return n ? t / n * 100 : 0; }
const chapterDone = c => c.topics.every(t => topicStars(t.id) > 0);

/* ================= Onboarding ================= */
function onboard(step = 1, draft = {}) {
  show('onboard');
  const el = $('#s-onboard');
  if (step === 1) {
    el.innerHTML = `<div class="ob"><div class="ob-hero bob">🌏</div><h1>Welcome to <span>StudyVerse</span></h1><p>Every subject is a game. Every grade is a new world.</p>
      <div class="card"><h3>Which board is your school?</h3><div class="grid2">${BOARDS.map(b => `<button class="choice ${b.live ? '' : 'off'}" data-b="${b.id}">${b.name}${b.live ? '' : '<small>coming soon</small>'}</button>`).join('')}</div></div></div>`;
    el.querySelectorAll('.choice').forEach(b => b.onclick = () => { if (b.classList.contains('off')) { toast('Coming soon! Start with CBSE for now.'); return; } sfx('tap'); onboard(2, { ...draft, board: b.dataset.b }); });
  } else if (step === 2) {
    el.innerHTML = `<div class="ob"><div class="ob-hero">🎒</div><h1>Which grade are you in?</h1>
      <div class="card"><div class="grid5">${Array.from({ length: MAX_GRADE }, (_, i) => `<button class="choice big" data-g="${i + 1}"><b>${i + 1}</b><small>${Worlds.THEMES[i + 1].name}</small></button>`).join('')}</div></div>
      <button class="btn ghost" id="obBack">← Back</button></div>`;
    el.querySelectorAll('.choice').forEach(b => b.onclick = () => { sfx('tap'); onboard(3, { ...draft, grade: +b.dataset.g }); });
    $('#obBack').onclick = () => onboard(1, draft);
  } else {
    el.innerHTML = `<div class="ob"><div class="ob-hero">😊</div><h1>Pick your hero</h1>
      <div class="card"><div class="grid6">${AVATARS.map((a, i) => `<button class="choice av ${i === 0 ? 'sel' : ''}" data-a="${a}">${a}</button>`).join('')}</div>
      <input id="obName" maxlength="20" placeholder="Your first name" autocomplete="off"></div>
      <button class="btn" id="obGo">Enter my world ▶</button><div style="height:8px"></div><button class="btn ghost" id="obBack">← Back</button></div>`;
    let av = AVATARS[0];
    el.querySelectorAll('.av').forEach(b => b.onclick = () => { el.querySelectorAll('.av').forEach(x => x.classList.remove('sel')); b.classList.add('sel'); av = b.dataset.a; sfx('tap'); });
    $('#obBack').onclick = () => onboard(2, draft);
    $('#obGo').onclick = () => {
      const name = $('#obName').value.trim() || 'Explorer';
      ST.profile = { ...draft, name, avatar: av }; save(); sfx('unlock');
      setGrade(draft.grade); worldScreen();
    };
  }
}
function setGrade(g) { ST.profile.grade = g; save(); if (typeof SND !== 'undefined') { SND.myGrade = g; if (SND.playing && SND.choice === 'auto') startMusic(); } }

/* ================= Grade world ================= */
async function worldScreen() {
  show('world', 'world'); NAV = {};
  const g = ST.profile.grade, subs = curSubjects(g), th = Worlds.THEMES[g];
  $('#worldTitle').innerHTML = `${esc(ST.profile.avatar)} Hi ${esc(ST.profile.name)}! <small>Grade ${g} · ${esc(th.name)}</small>`;
  const map = $('#map'); map.classList.toggle('dark', !!th.dark);
  if (!subs.length) { map.innerHTML = `<div class="empty">Syllabus for Grade ${g} is loading soon.</div>`; return; }
  const datas = await Promise.all(subs.map(s => subjectData(g, s.id)));
  let curSet = false; let total = 0, done = 0;
  const nodes = subs.map((s, i) => {
    const d = datas[i], st = Worlds.SUBJECT_STYLE[s.id] || { e: '📘', c: '#ffc93c' }, pct = subjectPct(d);
    if (d) d.chapters.forEach(c => c.topics.forEach(t => { total++; if (topicStars(t.id)) done++; }));
    let state = !d ? 'soon' : pct >= 100 ? 'done' : 'open';
    if (state === 'open' && !curSet) { state = 'current'; curSet = true; }
    return { title: s.name, sub: d ? `${d.chapters.length} chapters` : (s.book || ''), emoji: st.e, color: st.c, state, pct };
  });
  $('#hudPct').textContent = total ? Math.round(done / total * 100) + '%' : '0%';
  $('#hudBar').style.width = (total ? done / total * 100 : 0) + '%';
  $('#hudName').textContent = `Grade ${g} journey`;
  Worlds.render(map, g, nodes, 'grade', i => {
    const s = subs[i];
    if (!datas[i]) { sfx('hmm'); toast(`${s.name} is being built — coming soon!`); return; }
    sfx('open'); subjectScreen(s.id);
  });
}

/* ================= Subject: chapter path ================= */
async function subjectScreen(sid) {
  const g = ST.profile.grade, d = await subjectData(g, sid), meta = curSubjects(g).find(s => s.id === sid);
  if (!d) return worldScreen();
  NAV = { subject: sid };
  show('subject', 'world');
  $('#subTitle').innerHTML = `${esc((Worlds.SUBJECT_STYLE[sid] || {}).e || '📘')} ${esc(meta?.name || sid)} <small>${esc(meta?.book || '')}</small>`;
  let curSet = false;
  const nodes = d.chapters.map(c => {
    const dn = chapterDone(c); let state = dn ? 'done' : 'open';
    if (!dn && !curSet) { state = 'current'; curSet = true; }
    const st = c.topics.length ? Math.round(c.topics.reduce((a, t) => a + topicStars(t.id), 0) / c.topics.length) : 0;
    return { title: c.title, sub: `${c.topics.length} quests`, emoji: c.emoji || '📘', color: (Worlds.SUBJECT_STYLE[sid] || {}).c || '#ffc93c', state, stars: st, num: c.n };
  });
  const map = $('#cmap'); map.classList.toggle('dark', !!Worlds.THEMES[g].dark);
  Worlds.render(map, g, nodes, 'chapter', i => { sfx('open'); chapterScreen(sid, i); });
}

/* ================= Chapter: list of topic quests ================= */
async function chapterScreen(sid, ci) {
  const g = ST.profile.grade, d = await subjectData(g, sid), c = d.chapters[ci];
  NAV = { subject: sid, chapter: ci };
  show('chapter', 'world');
  const el = $('#s-chapter');
  el.innerHTML = `<button class="back" id="chBack">← Chapters</button>
    <div class="card chead"><div class="cemoji">${esc(c.emoji || '📘')}</div><div><span class="tag">Chapter ${c.n}</span><h2>${esc(c.title)}</h2></div></div>
    ${c.topics.map((t, ti) => { const s = topicStars(t.id); return `<button class="tcard ${s ? 'done' : ''}" data-t="${ti}">
      <div class="tnum">${s ? '✓' : ti + 1}</div><div class="tbody"><b>${esc(t.title)}</b><span>${esc(t.learn?.hook || '')}</span></div>
      <div class="tstars">${'⭐'.repeat(s)}${'☆'.repeat(3 - s)}</div></button>`; }).join('')}`;
  $('#chBack').onclick = () => subjectScreen(sid);
  el.querySelectorAll('.tcard').forEach(b => b.onclick = () => { sfx('open'); playTopic(sid, ci, +b.dataset.t); });
}

/* ================= Topic player: Learn → Play → Quiz → Teach → Done ================= */
let RUN = null;
async function playTopic(sid, ci, ti) {
  const g = ST.profile.grade, d = await subjectData(g, sid), c = d.chapters[ci], t = c.topics[ti];
  NAV = { subject: sid, chapter: ci, topic: ti };
  const steps = [{ k: 'learn', label: 'Learn' }, ...(t.games || []).map((gm, i) => ({ k: 'game', i, label: 'Play' })), { k: 'quiz', label: 'Quiz' }, { k: 'teach', label: 'Teach' }];
  RUN = { sid, ci, ti, t, c, steps, at: 0, quiz: { right: 0, total: 0, mistakes: [] }, gameScore: [0, 0], taught: false };
  show('topic');
  renderStep();
}
function stepBar() {
  const seen = new Set(); const pills = RUN.steps.map((s, i) => { const lab = s.label; const show = !seen.has(lab) || s.k !== 'game'; seen.add(lab); return { lab, i, show }; });
  return `<div class="tbar"><button class="x" id="tClose">✕</button><div class="pills">${RUN.steps.map((s, i) => `<i class="${i < RUN.at ? 'done' : i === RUN.at ? 'on' : ''}"></i>`).join('')}</div><span class="stepname">${RUN.steps[RUN.at]?.label || 'Done'}</span></div>`;
}
function nextStep() { RUN.at++; renderStep(); }
function renderStep() {
  const el = $('#s-topic'); const s = RUN.steps[RUN.at];
  el.innerHTML = stepBar() + `<div id="stepBody"></div>`;
  $('#tClose').onclick = () => { chapterScreen(RUN.sid, RUN.ci); };
  const b = $('#stepBody');
  if (!s) return doneStep(b);
  if (s.k === 'learn') learnStep(b);
  else if (s.k === 'game') { b.innerHTML = `<div class="card game" id="gbox"></div>`; Games.play($('#gbox'), RUN.t.games[s.i], (r, tot) => { RUN.gameScore[0] += r; RUN.gameScore[1] += tot; addXP(Math.max(5, r * 2)); nextStep(); }); }
  else if (s.k === 'quiz') quizRunner(b, RUN.t.quiz.map((q, i) => ({ q, qid: `${RUN.t.id}#${i}` })), res => { RUN.quiz = res; nextStep(); });
  else if (s.k === 'teach') teachStep(b);
  window.scrollTo(0, 0);
}

function learnStep(b) {
  const L = RUN.t.learn || {}, t = RUN.t;
  b.innerHTML = `<div class="card"><span class="tag">${esc(RUN.c.title)}</span><h2>${esc(t.title)}</h2>
      <div class="pet"><div class="face">🐣</div><div class="bubble">${esc(L.hook || '')}</div></div></div>
    <div class="card"><h3>💡 Big ideas</h3>${(L.points || []).map((p, i) => `<div class="point popin" style="animation-delay:${(i * .25).toFixed(2)}s"><span>${i + 1}</span>${esc(p)}</div>`).join('')}</div>
    ${t.lab === 'angle' ? `<div class="card"><h3>📐 Angle lab</h3><p class="sub">Drag the yellow dot.</p><div id="lab"></div></div>` : ''}
    ${L.example ? `<div class="card"><h3>🧠 Watch me solve</h3><div class="exq">${esc(L.example.q)}</div><div id="exSteps"></div>
      <button class="btn ghost" id="exBtn">Show step 1</button></div>` : ''}
    ${L.reallife ? `<div class="reallife card">🌍 <b>In real life:</b> ${esc(L.reallife)}</div>` : ''}
    <button class="btn mint" id="learnGo">${RUN.t.games?.length ? "Let's play ▶" : 'Start quiz ▶'}</button>`;
  if (t.lab === 'angle') angleLab($('#lab'));
  if (L.example) {
    const st = L.example.steps || []; let k = 0; const box = $('#exSteps'), btn = $('#exBtn');
    const reveal = () => {
      if (k < st.length) { box.insertAdjacentHTML('beforeend', `<div class="exstep popin">${k + 1}. ${esc(st[k])}</div>`); k++; sfx('tap'); btn.textContent = k < st.length ? `Show step ${k + 1}` : 'Show answer'; }
      else { box.insertAdjacentHTML('beforeend', `<div class="exans popin">✅ ${esc(L.example.answer)}</div>`); btn.remove(); sfx('coin'); }
    };
    if (!st.length) btn.textContent = 'Show answer';
    btn.onclick = reveal;
  }
  $('#learnGo').onclick = () => { addXP(5); nextStep(); };
}

/* ---------- Quiz with animated explanation after every answer ---------- */
function quizRunner(b, list, done) {
  let i = 0, right = 0; const mistakes = [];
  const render = () => {
    const { q, qid } = list[i];
    const order = Games.shuffle(q.options.map((o, k) => k));
    b.innerHTML = `<div class="card"><span class="tag">Question ${i + 1} of ${list.length}</span><div class="progress"><i style="width:${i / list.length * 100}%"></i></div>
      <h2 class="qtext">${esc(q.q)}</h2><div id="qo">${order.map(k => `<button class="opt" data-k="${k}">${esc(q.options[k])}</button>`).join('')}</div><div id="qx"></div></div>`;
    b.querySelectorAll('.opt').forEach(btn => btn.onclick = () => {
      const k = +btn.dataset.k, ok = k === q.answer;
      b.querySelectorAll('.opt').forEach(x => { x.disabled = true; if (+x.dataset.k === q.answer) x.classList.add('right'); });
      const qs = ST.qstats[qid] || { s: 0, w: 0 }; qs.s++;
      if (ok) { right++; sfx('correct'); addXP(10); }
      else { btn.classList.add('wrong'); sfx('wrong'); qs.w++; mistakes.push(q.mistake); ST.mistakes[q.mistake] = (ST.mistakes[q.mistake] || 0) + 1; }
      ST.qstats[qid] = qs; save();
      const box = $('#qx');
      const draw = () => {
        box.innerHTML = `<div class="explain ${ok ? 'good' : 'bad'}"><div class="verdict">${ok ? '🎉 Correct!' : `🤔 Not quite — it's <b>${esc(q.options[q.answer])}</b>`}</div>
          ${q.visual ? `<div class="vis">${Visual.render(q.visual)}</div>` : `<div class="bigans popin">${esc(q.options[q.answer])}</div>`}
          <div class="why">${esc(q.explain)}</div>
          ${(q.steps || []).map((s, j) => `<div class="exstep popin" style="animation-delay:${(.4 + j * .45).toFixed(2)}s">${j + 1}. ${esc(s)}</div>`).join('')}</div>
          <div class="xrow">${q.visual ? '<button class="btn ghost" id="rep">🔁 Replay</button>' : ''}<button class="btn mint" id="nx">${i < list.length - 1 ? 'Next ▶' : 'Finish ▶'}</button></div>`;
        const rep = $('#rep'); if (rep) rep.onclick = draw;
        $('#nx').onclick = () => { i++; if (i < list.length) render(); else done({ right, total: list.length, mistakes }); };
        setTimeout(() => box.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 120);
      };
      draw();
    });
  };
  render();
}

/* ---------- Teach Gappu ---------- */
function teachStep(b) {
  const T = RUN.t.teach || {};
  b.innerHTML = `<div class="card"><span class="tag">Teach to learn</span><div class="pet"><div class="face" id="gf">🐣</div><div class="bubble" id="gs">${esc(T.ask)}</div></div>
    <textarea id="ans" placeholder="Explain in your own words…"></textarea><button class="btn" id="tBtn">Explain to Gappu 💬</button>
    <div style="height:8px"></div><button class="btn ghost" id="tSkip">Skip for now</button></div>`;
  let tries = 0;
  $('#tSkip').onclick = nextStep;
  $('#tBtn').onclick = () => {
    const txt = $('#ans').value.toLowerCase(); tries++;
    const hasWord = w => { w = String(w).toLowerCase().trim(); if (!w) return false;
      if (/[^\x00-\x7f]/.test(w)) return txt.includes(w); // Hindi/Sanskrit: match inside text
      const e = w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); return new RegExp(`(^|[^a-z0-9])${e}(s|es)?([^a-z0-9]|$)`).test(txt); };
    const miss = (T.must || []).filter(grp => !grp.some(hasWord));
    const f = $('#gf'), s = $('#gs');
    if (txt.trim().length < 6) { f.textContent = '🐣'; s.textContent = 'Hmm, tell me a little more please! 🥺'; return; }
    if (!miss.length) {
      f.textContent = '🐥'; s.textContent = T.praise; sfx('correct');
      if (!RUN.taught) { RUN.taught = true; addXP(25, 'Gappu learned from you!'); }
      $('#tBtn').textContent = 'Finish ▶'; $('#tBtn').onclick = nextStep; $('#tSkip').remove();
    } else {
      f.textContent = '🤔'; sfx('hmm');
      s.textContent = T.nudge + (tries >= 2 ? `  (Hint: try talking about “${miss[0][0]}”)` : '');
    }
  };
}

function doneStep(b) {
  const q = RUN.quiz, pct = q.total ? q.right / q.total : 0;
  const stars = pct >= .9 ? 3 : pct >= .7 ? 2 : pct >= .4 ? 1 : 1;
  const prev = ST.topics[RUN.t.id]?.stars || 0;
  ST.topics[RUN.t.id] = { stars: Math.max(prev, stars), last: today() }; bumpStreak(); save();
  sfx('unlock');
  const uniq = [...new Set(q.mistakes)];
  const c = RUN.c, nextTi = RUN.ti + 1 < c.topics.length ? RUN.ti + 1 : null;
  b.innerHTML = `<div class="card done-card"><div class="confetti">${Array.from('🎉⭐✨🎊🌟'.repeat(4)).map((e, i) => `<span style="left:${(i * 37) % 100}%;animation-delay:${(i % 7) * .12}s">${e}</span>`).join('')}</div>
    <h2>Quest complete!</h2><div class="bigstars">${[0, 1, 2].map(i => `<span class="${i < stars ? 'on' : ''}" style="animation-delay:${i * .25}s">⭐</span>`).join('')}</div>
    <p class="sub">Quiz: ${q.right} of ${q.total} correct${RUN.taught ? ' · You taught Gappu 🐥' : ''}</p>
    ${uniq.length ? `<h3>🧬 Your Mistake DNA</h3><p class="sub">We'll bring these back in Practice until they're fixed.</p>${uniq.map(m => `<div class="dna">🔍 ${esc(m)}</div>`).join('')}` : '<p class="sub">No mistakes. Superstar! 🌟</p>'}
    <div style="height:12px"></div>
    ${nextTi !== null ? `<button class="btn" id="dNext">Next quest: ${esc(c.topics[nextTi].title)} ▶</button><div style="height:8px"></div>` : ''}
    <button class="btn ghost" id="dBack">Back to chapter</button></div>`;
  if (nextTi !== null) $('#dNext').onclick = () => playTopic(RUN.sid, RUN.ci, nextTi);
  $('#dBack').onclick = () => chapterScreen(RUN.sid, RUN.ci);
}

/* ================= Practice: daily mix that targets mistakes ================= */
async function practiceScreen() {
  show('practice', 'practice');
  const el = $('#s-practice'), g = ST.profile.grade;
  const subs = curSubjects(g); const pool = [];
  for (const s of subs) { const d = await subjectData(g, s.id); if (!d) continue;
    d.chapters.forEach(c => c.topics.forEach(t => { if (!topicStars(t.id)) return; t.quiz.forEach((q, i) => { const qid = `${t.id}#${i}`, st = ST.qstats[qid] || { s: 0, w: 0 }; pool.push({ q, qid, wgt: 1 + st.w * 4 - Math.min(st.s, 3) * .2 }); }); })); }
  if (!pool.length) { el.innerHTML = `<div class="card"><h2>🎯 Daily Practice</h2><p class="sub">Finish your first quest and your daily practice mix appears here. It brings back the questions you found tricky until you master them.</p><button class="btn" id="pGo">Go to my world ▶</button></div>`; $('#pGo').onclick = worldScreen; return; }
  pool.sort((a, b) => b.wgt + Math.random() * 2 - (a.wgt + Math.random() * 2));
  const list = pool.slice(0, 10);
  const top = Object.entries(ST.mistakes).sort((a, b) => b[1] - a[1]).slice(0, 3);
  el.innerHTML = `<div class="card"><h2>🎯 Daily Practice</h2><p class="sub">${list.length} questions picked for you — tricky ones come first.</p>
    ${top.length ? `<h3>🧬 Fixing now</h3>${top.map(([m, n]) => `<div class="dna">🔍 ${esc(m)} <small>×${n}</small></div>`).join('')}` : ''}
    <div style="height:10px"></div><button class="btn" id="pStart">Start practice ▶</button></div><div id="pBody"></div>`;
  $('#pStart').onclick = () => { el.querySelector('.card').remove(); quizRunner($('#pBody'), list, r => {
    bumpStreak(); sfx('unlock');
    $('#pBody').innerHTML = `<div class="card done-card"><h2>Practice done! 💪</h2><p class="sub">${r.right} of ${r.total} correct. Come back tomorrow to keep your 🔥 streak.</p><button class="btn" id="pAgain">Another round</button></div>`;
    $('#pAgain').onclick = practiceScreen; }); };
}

/* ================= Squad (sample league until logins arrive) ================= */
function squadScreen() {
  show('squad', 'squad');
  const mates = [{ n: 'Aarav', e: '🐯', x: 420 }, { n: 'Diya', e: '🦊', x: 360 }, { n: 'Kabir', e: '🐼', x: 210 }, { n: 'Meera', e: '🐨', x: 140 }];
  const list = [...mates, { n: ST.profile.name + ' (you)', e: ST.profile.avatar, x: ST.xp, me: true }].sort((a, b) => b.x - a.x);
  const us = mates.reduce((s, m) => s + m.x, 0) + ST.xp, them = 1450;
  $('#s-squad').innerHTML = `<div class="card"><span class="tag">This week · School league</span>
    <div class="vs"><div><div class="big">🦁</div>Team Lions<br>${us} XP</div><div class="big">VS</div><div><div class="big">🦅</div>Team Eagles<br>${them} XP</div></div>
    <div class="bar2"><i style="width:${us / (us + them) * 100}%"></i></div><p class="sub" style="text-align:center">${us >= them ? '🎉 Lions are winning!' : `Lions need ${them - us} more XP!`}</p></div>
    <div class="card"><h3>🦁 Team Lions</h3>${list.map((m, i) => `<div class="row ${m.me ? 'me' : ''}"><div class="rank">${i + 1}</div><div class="av">${m.e}</div><div class="nm">${esc(m.n)}</div><div class="xp">${m.x} ⭐</div></div>`).join('')}</div>
    <p class="note">Sample squad. Real friends and school leagues arrive with logins.</p>`;
}

/* ================= Me / settings ================= */
function meScreen() {
  show('me', 'me');
  const p = ST.profile, done = Object.keys(ST.topics).length;
  $('#s-me').innerHTML = `<div class="card mecard"><div class="meav">${esc(p.avatar)}</div><div><h2>${esc(p.name)}</h2><p class="sub">Grade ${p.grade} · ${BOARDS.find(b => b.id === p.board)?.name || 'CBSE'}</p></div></div>
    <div class="card statrow"><div><b>${ST.xp}</b><span>XP</span></div><div><b>${ST.streak.n || 0}🔥</b><span>Streak</span></div><div><b>${done}</b><span>Quests</span></div></div>
    <div class="card"><h3>Change grade</h3><div class="grid5">${Array.from({ length: MAX_GRADE }, (_, i) => `<button class="choice ${p.grade === i + 1 ? 'sel' : ''}" data-g="${i + 1}"><b>${i + 1}</b></button>`).join('')}</div></div>
    <div class="card"><button class="btn ghost" onclick="openSound()">🎵 Sound & music</button><div style="height:8px"></div><button class="btn ghost" id="meReset">Start over</button></div>`;
  $('#s-me').querySelectorAll('.choice').forEach(b => b.onclick = () => { setGrade(+b.dataset.g); sfx('unlock'); toast(`Welcome to ${Worlds.THEMES[+b.dataset.g].name}!`); worldScreen(); });
  $('#meReset').onclick = () => { if ($('#meReset').dataset.sure) { localStorage.removeItem('sv_state'); location.reload(); } else { $('#meReset').dataset.sure = 1; $('#meReset').textContent = 'Tap again to erase all progress'; } };
}

/* ================= Angle lab (interactive) ================= */
function angleLab(host) {
  host.innerHTML = `<svg class="labsvg" viewBox="0 0 320 240"><path class="arc" fill="rgba(139,92,246,.18)" stroke="#8b5cf6" stroke-width="3"/>
    <line x1="160" y1="140" x2="290" y2="140" stroke="#1b1f3a" stroke-width="5" stroke-linecap="round"/><line class="ray" x1="160" y1="140" stroke="#1b1f3a" stroke-width="5" stroke-linecap="round"/>
    <circle cx="160" cy="140" r="7" fill="#1b1f3a"/><circle class="knob" r="17" fill="#ffc93c" stroke="#1b1f3a" stroke-width="3"/></svg>
    <div class="readout"><div class="deg"></div><div class="type"></div></div>`;
  const svg = host.querySelector('svg'), O = { x: 160, y: 140 }, R = 95; let drag = false, last = 45;
  const kinds = [[89.5, 'Acute', '#2ed3a5'], [90.5, 'Right', '#3b82f6'], [179.5, 'Obtuse', '#ff9f43'], [180.5, 'Straight', '#8b5cf6'], [359.5, 'Reflex', '#ff6b6b'], [361, 'Full turn', '#1b1f3a']];
  const draw = a => { const r = a * Math.PI / 180;
    host.querySelector('.knob').setAttribute('cx', O.x + R * Math.cos(r)); host.querySelector('.knob').setAttribute('cy', O.y - R * Math.sin(r));
    host.querySelector('.ray').setAttribute('x2', O.x + 130 * Math.cos(r)); host.querySelector('.ray').setAttribute('y2', O.y - 130 * Math.sin(r));
    const ex = O.x + 34 * Math.cos(r), ey = O.y - 34 * Math.sin(r);
    host.querySelector('.arc').setAttribute('d', `M${O.x},${O.y} L${O.x + 34},${O.y} A34,34 0 ${a > 180 ? 1 : 0} 0 ${ex},${ey} Z`);
    const k = kinds.find(k => a <= k[0]); host.querySelector('.deg').textContent = Math.round(a) + '°'; const ty = host.querySelector('.type'); ty.textContent = k[1]; ty.style.background = k[2]; };
  const move = e => { if (!drag) return; e.preventDefault(); const b = svg.getBoundingClientRect(); const p = { x: (e.clientX - b.left) * 320 / b.width, y: (e.clientY - b.top) * 240 / b.height };
    let a = Math.atan2(O.y - p.y, p.x - O.x) * 180 / Math.PI; if (a < 0) a += 360; if (last > 300 && a < 60) a = 360; if (last < 60 && a > 300) a = 0; [90, 180].forEach(s => { if (Math.abs(a - s) < 3) a = s; }); if (a < 1) a = 1; last = a; draw(a); };
  svg.addEventListener('pointerdown', e => { drag = true; svg.setPointerCapture(e.pointerId); move(e); });
  svg.addEventListener('pointermove', move); svg.addEventListener('pointerup', () => drag = false);
  draw(45);
}

/* ================= Install as an app ================= */
let deferredPrompt = null;
const isStandalone = () => window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
const inFrame = (() => { try { return window.self !== window.top; } catch (e) { return true; } })();
function showInstall() { if (isStandalone() || inFrame) return; try { if (sessionStorage.getItem('sv_noinst')) return; } catch (e) {} $('#installBar').style.display = 'flex'; }
function hideInstall() { $('#installBar').style.display = 'none'; try { sessionStorage.setItem('sv_noinst', '1'); } catch (e) {} }
window.addEventListener('beforeinstallprompt', e => { e.preventDefault(); deferredPrompt = e; showInstall(); });
window.addEventListener('appinstalled', () => { $('#installBar').style.display = 'none'; deferredPrompt = null; toast('🎉 StudyVerse installed!'); sfx('unlock'); });
async function installApp() {
  if (deferredPrompt) { deferredPrompt.prompt(); const r = await deferredPrompt.userChoice; deferredPrompt = null; if (r.outcome === 'accepted') $('#installBar').style.display = 'none'; return; }
  $('#instIntro').textContent = isIOS ? 'On iPhone/iPad, install from Safari in 3 taps:' : 'Your browser hides the install button. Do this:';
  $('#instSteps').innerHTML = isIOS ? '<li>Open this page in <b>Safari</b></li><li>Tap the <b>Share</b> button (square with ↑ arrow)</li><li>Tap <b>Add to Home Screen</b> → <b>Add</b></li>'
    : '<li>Open this page in <b>Google Chrome</b></li><li>Tap the <b>⋮</b> menu (top right)</li><li>Tap <b>Install app</b> → <b>Install</b></li>';
  $('#installSheet').classList.add('show');
}
if (!isStandalone() && !inFrame) setTimeout(() => { if (!deferredPrompt) showInstall(); }, 2500);
if ('serviceWorker' in navigator && !inFrame && (location.protocol === 'https:' || location.hostname === 'localhost')) window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));

/* ================= Start ================= */
(async function init() {
  hud();
  try { CUR = await loadJSON('content/curriculum.json'); } catch (e) { CUR = { grades: {} }; }
  if (!ST.profile) onboard(1); else { setGrade(ST.profile.grade); worldScreen(); }
})();
