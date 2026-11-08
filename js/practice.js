/* ================= Memory Garden · Quick 3 · Daily goal · Badges · Duels =================
   Spaced revision: every finished topic becomes a plant. Its next revision is due after
   1, 3, 7, 16, 35, 90, then 180 days. Doing well grows the plant (longer gap); struggling
   shrinks it (sooner). Overdue plants get thirsty 💧, then wilt 🥀.
   Duels: a friend link with 5 questions; no server needed (all data is in the link). */
(function () {
  const INT = [1, 3, 7, 16, 35, 90, 180];
  const PLANTS = ['🌱', '🌿', '🪴', '🌳', '🌸', '🌻', '🌻'];
  const STAGE = ['Seedling', 'Sprout', 'Growing', 'Strong', 'Blooming', 'Mastered', 'Mastered'];
  const GOAL = 50;                                   // daily XP goal
  const DAY = 864e5;
  const dstr = t => new Date(t).toISOString().slice(0, 10);
  const addDays = n => dstr(Date.now() + n * DAY);
  const daysLate = due => Math.floor((Date.parse(today()) - Date.parse(due)) / DAY);
  ST.mem = ST.mem || {}; ST.daily = ST.daily || { d: '', xp: 0, hit: '' }; ST.badges = ST.badges || {};
  ST.friends = ST.friends || {}; ST.duels = ST.duels || {}; ST.cnt = ST.cnt || { water: 0, duels: 0, wins: 0 };
  const parseTid = tid => { const m = /^g(\d+)-([a-z]+)-/.exec(tid); return m ? { g: +m[1], sid: m[2] } : null; };

  /* ---------- memory model ---------- */
  function schedule(tid, acc) {
    const m = ST.mem[tid] || { b: 0, n: 0 };
    if (acc >= 0.99) m.b = Math.min(m.b + 1, INT.length - 1);
    else if (acc < 0.5) m.b = Math.max(m.b - 1, 0);
    m.due = addDays(acc < 0.5 ? 1 : INT[m.b]); m.n = (m.n || 0) + 1; m.last = today();
    ST.mem[tid] = m;
  }
  function learned(tid, pct) {
    if (!ST.mem[tid]) ST.mem[tid] = { b: 0, n: 0, due: addDays(1), last: today() };
    else schedule(tid, pct);
    save(); checkBadges();
  }
  const dueList = (g = ST.profile?.grade) => Object.entries(ST.mem)
    .filter(([tid, m]) => m.due && m.due <= today() && (!g || tid.startsWith(`g${g}-`)))
    .sort((a, b) => a[1].due.localeCompare(b[1].due)).map(([tid]) => tid);
  function plant(tid) {
    const m = ST.mem[tid]; if (!m) return null;
    const late = daysLate(m.due);
    const state = late >= 3 ? 'wilt' : late >= 0 ? 'thirsty' : 'ok';
    const health = state === 'ok' ? 100 : Math.max(15, 85 - late * 12);
    return { e: state === 'wilt' ? '🥀' : PLANTS[m.b], state, health, stage: STAGE[m.b], b: m.b, due: m.due };
  }
  const badge = tid => { const p = plant(tid); if (!p) return '';
    return `<span class="gplant ${p.state}" title="${p.stage}">${p.e}${p.state !== 'ok' ? '<i>💧</i>' : ''}</span>`; };

  /* ---------- question loading ---------- */
  async function topicById(tid) {
    const p = parseTid(tid); if (!p) return null;
    const d = await subjectData(p.g, p.sid); if (!d) return null;
    for (const c of d.chapters) for (const t of c.topics) if (t.id === tid) return t;
    return null;
  }
  function pickQs(t, n) {
    const qs = (t.quiz || []).map((q, i) => { const st = ST.qstats[`${t.id}#${i}`] || { s: 0, w: 0 }; return { q, qid: `${t.id}#${i}`, k: st.w * 3 - st.s * .3 + Math.random() * 2 }; });
    return qs.sort((a, b) => b.k - a.k).slice(0, n).map(({ q, qid }) => ({ q, qid }));
  }
  async function revisionList(tids, perTopic, max) {
    const list = [];
    for (const tid of tids) { const t = await topicById(tid); if (t) list.push(...pickQs(t, perTopic)); if (list.length >= max) break; }
    return Games.shuffle(list.slice(0, max));            // interleave topics/subjects
  }
  /* run a revision round; afterwards reschedule each topic by its own accuracy */
  function runRevision(host, list, title, after) {
    RUN = null;
    const before = {}; list.forEach(x => { const s = ST.qstats[x.qid] || { s: 0, w: 0 }; before[x.qid] = s.w; });
    host.innerHTML = '';
    quizRunner(host, list, r => {
      const per = {};
      list.forEach(x => { const tid = x.qid.split('#')[0]; const w = (ST.qstats[x.qid]?.w || 0) - (before[x.qid] || 0);
        per[tid] = per[tid] || [0, 0]; per[tid][1]++; if (w === 0) per[tid][0]++; });
      const grown = []; Object.entries(per).forEach(([tid, [ok, n]]) => { const b0 = ST.mem[tid]?.b ?? 0; schedule(tid, ok / n); if (ST.mem[tid].b > b0) grown.push(tid); });
      ST.cnt.water = (ST.cnt.water || 0) + Object.keys(per).length; bumpStreak(); addXP(5 * r.right, null); save(); checkBadges();
      sfx('unlock');
      host.innerHTML = `<div class="card done-card"><div class="gbig">${grown.length ? '🌳' : '💧'}</div><h2>${esc(title)} done!</h2>
        <p class="sub">${r.right} of ${r.total} correct · +${5 * r.right} ⭐</p>
        <p class="sub">${grown.length ? `🌱 ${grown.length} plant${grown.length > 1 ? 's' : ''} grew stronger. They'll need water again later.` : 'Your plants are watered. Tricky ones will come back soon.'}</p>
        <div id="gAfter"></div><button class="btn" id="gBack">Continue ▶</button></div>`;
      $('#gBack').onclick = after || practiceScreen;
    });
  }

  /* ---------- daily goal ---------- */
  function dailyXP() { if (ST.daily.d !== today()) ST.daily = { d: today(), xp: 0, hit: ST.daily.hit }; return ST.daily.xp; }
  const _addXP = addXP;
  addXP = function (n, msg) {
    dailyXP(); const was = ST.daily.xp; ST.daily.xp += n; _addXP(n, msg);
    if (was < GOAL && ST.daily.xp >= GOAL) { ST.daily.hit = today(); bumpStreak(); save(); setTimeout(() => { sfx('unlock'); toast('🎯 Daily goal reached! Streak safe 🔥'); checkBadges(); }, 900); }
    ringUpdate();
  };
  const ring = (size = 46) => { const p = Math.min(1, dailyXP() / GOAL), r = size / 2 - 5, c = 2 * Math.PI * r;
    return `<svg class="goalring" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}"><circle cx="${size / 2}" cy="${size / 2}" r="${r}" fill="none" stroke="#ffffff33" stroke-width="6"/>
      <circle class="gr-arc" cx="${size / 2}" cy="${size / 2}" r="${r}" fill="none" stroke="${p >= 1 ? '#2ed3a5' : '#ffc93c'}" stroke-width="6" stroke-linecap="round" stroke-dasharray="${c}" stroke-dashoffset="${c * (1 - p)}" transform="rotate(-90 ${size / 2} ${size / 2})"/>
      <text x="50%" y="54%" text-anchor="middle" dominant-baseline="middle" font-size="${size / 3.6}" font-weight="800" fill="currentColor">${p >= 1 ? '✓' : Math.round(p * 100) + '%'}</text></svg>`; };
  function ringUpdate() { const h = document.getElementById('goalMini'); if (h) h.innerHTML = ring(40); }

  /* ---------- badges ---------- */
  const BADGES = [
    ['first', '🚀', 'First quest', () => Object.keys(ST.topics).length >= 1],
    ['q10', '📚', '10 quests', () => Object.keys(ST.topics).length >= 10],
    ['q50', '🏆', '50 quests', () => Object.keys(ST.topics).length >= 50],
    ['q100', '👑', '100 quests', () => Object.keys(ST.topics).length >= 100],
    ['star3', '🌟', 'First 3-star quest', () => Object.values(ST.topics).some(t => t.stars >= 3)],
    ['s3', '🔥', '3-day streak', () => (ST.streak.n || 0) >= 3],
    ['s7', '⚡', '7-day streak', () => (ST.streak.n || 0) >= 7],
    ['s30', '💎', '30-day streak', () => (ST.streak.n || 0) >= 30],
    ['w1', '💧', 'First watering', () => (ST.cnt.water || 0) >= 1],
    ['w25', '🌳', 'Gardener: 25 waterings', () => (ST.cnt.water || 0) >= 25],
    ['m1', '🌻', 'First mastered topic', () => Object.values(ST.mem).some(m => m.b >= 5)],
    ['goal', '🎯', 'Daily goal reached', () => !!ST.daily.hit],
    ['d1', '⚔️', 'First duel', () => (ST.cnt.duels || 0) >= 1],
    ['dw', '🥇', 'Duel winner', () => (ST.cnt.wins || 0) >= 1],
    ['dw10', '🏅', '10 duel wins', () => (ST.cnt.wins || 0) >= 10]];
  function checkBadges() {
    BADGES.forEach(([id, e, name, ok]) => { if (!ST.badges[id] && ok()) { ST.badges[id] = today(); save(); setTimeout(() => { sfx('unlock'); toast(`🏅 New badge: ${e} ${name}`); }, 1400); } });
  }
  const badgeGrid = () => `<div class="bgrid">${BADGES.map(([id, e, name]) => `<div class="bdg ${ST.badges[id] ? 'on' : ''}"><b>${e}</b><span>${esc(name)}</span></div>`).join('')}</div>`;

  /* ---------- Practice screen ---------- */
  window.practiceScreen = async function () {
    show('practice', 'practice'); RUN = null;
    const el = $('#s-practice'), g = ST.profile.grade, due = dueList(g);
    const mine = Object.keys(ST.mem).filter(t => t.startsWith(`g${g}-`));
    const mist = Object.keys(ST.qstats).filter(k => k.startsWith(`g${g}-`) && ST.qstats[k].w > 0).length;
    el.innerHTML = `<div class="card goalcard"><div class="gring">${ring(84)}</div><div><h2>Today's goal</h2>
        <p class="sub">${dailyXP()} / ${GOAL} ⭐ today · 🔥 ${ST.streak.n || 0}-day streak</p>
        <p class="sub small">Hit the goal every day to keep your streak alive.</p></div></div>
      <div class="card"><h2>🌱 Memory Garden</h2>
        ${mine.length ? `<p class="sub">${due.length ? `<b>${due.length}</b> plant${due.length > 1 ? 's are' : ' is'} thirsty. A quick revision waters ${due.length > 1 ? 'them' : 'it'} and makes the memory last longer.` : 'Every plant is watered. Come back tomorrow! 🌞'}</p>
          ${due.length ? `<button class="btn mint" id="pWater">💧 Water my garden (${Math.min(10, due.length * 2)} questions)</button>` : ''}
          <div class="garden" id="pGarden"></div>`
        : `<p class="sub">Finish a quest and it is planted here. Each plant needs watering (a few revision questions) after 1 day, then 3, 7, 16, 35 and 90 days. That's how memories become permanent.</p><button class="btn" id="pGo">Start a quest ▶</button>`}
      </div>
      <div class="card"><h3>⚡ Quick practice</h3>
        <button class="btn ghost" id="pMix">🎲 Mixed practice (10 questions)</button><div style="height:8px"></div>
        <button class="btn ghost" id="pMist" ${mist ? '' : 'disabled'}>🧬 Fix my mistakes${mist ? ` (${mist})` : ''}</button><div style="height:8px"></div>
        <button class="btn ghost" id="pDuel">⚔️ Duel a friend</button></div>
      <div class="card"><h3>🏅 Badges</h3>${badgeGrid()}</div><div id="pBody"></div>`;
    const body = () => { el.querySelectorAll('.card').forEach(c => c.remove()); return $('#pBody'); };
    if ($('#pGo')) $('#pGo').onclick = worldScreen;
    if ($('#pWater')) $('#pWater').onclick = async () => { const list = await revisionList(due, 2, 10); runRevision(body(), list, 'Watering'); };
    $('#pMix').onclick = async () => { const tids = Games.shuffle(mine.length ? mine : []).slice(0, 10); if (!tids.length) { toast('Finish a quest first!'); return; } const list = await revisionList(tids, 1, 10); runRevision(body(), list, 'Practice'); };
    $('#pMist').onclick = async () => { const ks = Object.keys(ST.qstats).filter(k => k.startsWith(`g${g}-`) && ST.qstats[k].w > 0).sort((a, b) => ST.qstats[b].w - ST.qstats[a].w).slice(0, 10);
      const list = []; for (const k of ks) { const [tid, i] = k.split('#'); const t = await topicById(tid); if (t && t.quiz[+i]) list.push({ q: t.quiz[+i], qid: k }); }
      if (!list.length) return; runRevision(body(), list, 'Mistake fixing'); };
    $('#pDuel').onclick = () => Duel.create(g);
    if ($('#pGarden')) renderGarden($('#pGarden'), mine);
  };
  async function renderGarden(host, tids) {
    const items = await Promise.all(tids.map(async tid => ({ tid, t: await topicById(tid), p: plant(tid), s: parseTid(tid).sid })));
    const by = {}; items.filter(x => x.t).forEach(x => (by[x.s] = by[x.s] || []).push(x));
    host.innerHTML = Object.entries(by).map(([sid, xs]) => `<div class="gsub"><b>${(Worlds.SUBJECT_STYLE[sid] || {}).e || '📘'} ${esc((curSubjects(ST.profile.grade).find(s => s.id === sid) || {}).name || sid)}</b>
      <div class="gbed">${xs.sort((a, b) => a.p.due.localeCompare(b.p.due)).map(x => `<div class="gcell ${x.p.state}" title="${esc(x.t.title)}"><span>${x.p.e}</span><i style="width:${x.p.health}%"></i><small>${esc(x.t.title)}</small></div>`).join('')}</div></div>`).join('');
  }

  /* ---------- Quick 3 (world banner + after a quest) ---------- */
  async function quick3(after) {
    const due = dueList(); if (!due.length) return;
    show('practice', 'practice'); const host = $('#s-practice'); host.innerHTML = '<div id="pBody"></div>';
    const list = await revisionList(due.slice(0, 3), 1, 3); runRevision($('#pBody'), list, 'Quick 3', after);
  }
  function worldBanner() {
    const hello = $('#worldTitle'); if (!hello || !ST.profile) return;
    if (!document.getElementById('goalMini')) hello.insertAdjacentHTML('beforeend', `<span id="goalMini" class="goalmini" title="Today's goal">${ring(40)}</span>`); else ringUpdate();
    document.getElementById('q3bar')?.remove();
    const due = dueList(); if (!due.length) return;
    hello.insertAdjacentHTML('afterend', `<div class="q3bar" id="q3bar"><span>💧 <b>${due.length}</b> topic${due.length > 1 ? 's are' : ' is'} getting thirsty</span><button id="q3go">⚡ Quick 3</button></div>`);
    $('#q3go').onclick = () => quick3(worldScreen);
  }
  const _world = worldScreen;
  worldScreen = async function () { await _world(); worldBanner(); };
  function doneExtra(host) {
    const due = dueList().filter(t => t !== RUN?.t?.id);
    host.innerHTML = `${due.length ? `<button class="btn mint" id="dQ3">⚡ Quick 3 revision (${Math.min(3, due.length)} thirsty)</button><div style="height:8px"></div>` : ''}
      <button class="btn ghost" id="dDuel">⚔️ Challenge a friend on this topic</button><div style="height:8px"></div>`;
    const back = () => chapterScreen(NAV.subject, NAV.chapter);
    if ($('#dQ3')) $('#dQ3').onclick = () => quick3(back);
    const tid = RUN?.t?.id; $('#dDuel').onclick = () => Duel.create(ST.profile.grade, tid);
  }

  /* ---------- Duels: everything lives in the link ---------- */
  const b64e = o => btoa(unescape(encodeURIComponent(JSON.stringify(o)))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  const b64d = s => JSON.parse(decodeURIComponent(escape(atob(s.replace(/-/g, '+').replace(/_/g, '/')))));
  const link = (k, o) => `${location.origin}${location.pathname}#${k}=${b64e(o)}`;
  async function share(text, url) {
    try { if (navigator.share) { await navigator.share({ title: 'StudyVerse duel', text, url }); return; } } catch (e) { if (e && e.name === 'AbortError') return; }
    try { await navigator.clipboard.writeText(`${text} ${url}`); toast('Link copied! Paste it to your friend'); } catch (e) {}
    window.open(`https://wa.me/?text=${encodeURIComponent(text + ' ' + url)}`, '_blank');
  }
  const me = () => ({ n: ST.profile?.name || 'Friend', a: ST.profile?.avatar || '🙂' });
  function record(f, myS, theirS, myMs, theirMs, id) {
    if (ST.duels[id]) return; ST.duels[id] = 1;
    const k = f.n + f.a, fr = ST.friends[k] || { n: f.n, a: f.a, w: 0, l: 0, d: 0 };
    const res = myS > theirS || (myS === theirS && myMs < theirMs) ? 'w' : myS === theirS && myMs === theirMs ? 'd' : 'l';
    fr[res]++; fr.last = today(); ST.friends[k] = fr; ST.cnt.duels = (ST.cnt.duels || 0) + 1; if (res === 'w') ST.cnt.wins = (ST.cnt.wins || 0) + 1;
    save(); checkBadges(); return res;
  }
  const secs = ms => (ms / 1000).toFixed(0) + 's';
  async function duelPool(g, tid) {
    let tids = tid ? [tid] : Object.keys(ST.topics).filter(t => t.startsWith(`g${g}-`));
    if (!tids.length) { const s = curSubjects(g)[0]; const d = s && await subjectData(g, s.id); if (d) tids = d.chapters[0].topics.map(t => t.id); }
    const pool = []; for (const t of Games.shuffle(tids).slice(0, 8)) { const tp = await topicById(t); if (tp) tp.quiz.forEach((q, i) => pool.push(`${tp.id}#${i}`)); }
    return Games.shuffle(pool).slice(0, 5);
  }
  async function loadList(qids) { const out = []; for (const k of qids) { const [tid, i] = k.split('#'); const t = await topicById(tid); if (t && t.quiz[+i]) out.push({ q: t.quiz[+i], qid: k }); } return out; }
  function play(host, list, done) { RUN = null; const t0 = Date.now(); quizRunner(host, list, r => done(r.right, Date.now() - t0)); }
  const Duel = {
    async create(g, tid) {
      const qids = await duelPool(g, tid); if (qids.length < 3) { toast('Finish a quest first to start a duel!'); return; }
      const list = await loadList(qids);
      show('practice', 'practice'); const host = $('#s-practice');
      host.innerHTML = `<div class="card duelcard"><div class="gbig">⚔️</div><h2>Set your score</h2><p class="sub">Answer ${list.length} questions. Then send the duel link to a friend. They play the same questions and you'll see who wins!</p><button class="btn" id="dGo">Start ▶</button></div><div id="pBody"></div>`;
      $('#dGo').onclick = () => { host.querySelector('.card').remove(); play($('#pBody'), list, (s, ms) => {
        const id = Math.random().toString(36).slice(2, 10), m = me();
        const url = link('duel', { v: 1, id, g, q: qids, n: m.n, a: m.a, s, ms });
        ST.duels['o' + id] = { s, ms, t: today() }; save();
        $('#pBody').innerHTML = `<div class="card done-card"><div class="gbig">${s >= list.length - 1 ? '🔥' : '💪'}</div><h2>You scored ${s}/${list.length}</h2><p class="sub">in ${secs(ms)}. Now challenge a friend!</p>
          <button class="btn" id="dShare">📤 Send duel on WhatsApp</button><div style="height:8px"></div><button class="btn ghost" id="dDone">Done</button></div>`;
        $('#dShare').onclick = () => share(`⚔️ ${m.n} ${m.a} scored ${s}/${list.length} on StudyVerse (Grade ${g}). Can you beat me?`, url);
        $('#dDone').onclick = practiceScreen; }); };
    },
    async accept(o) {
      show('practice', 'practice'); document.querySelectorAll('nav').forEach(n => n.style.display = ST.profile ? '' : 'none');
      const host = $('#s-practice'); const list = await loadList(o.q);
      if (!list.length) { host.innerHTML = `<div class="card"><h2>⚔️ Duel</h2><p class="sub">This duel's questions aren't available any more. Ask your friend for a new link.</p><button class="btn" id="dHome">Open StudyVerse</button></div>`; $('#dHome').onclick = () => { location.hash = ''; location.reload(); }; return; }
      host.innerHTML = `<div class="card duelcard"><div class="gbig">${esc(o.a)}⚔️</div><h2>${esc(o.n)} challenged you!</h2>
        <p class="sub">Grade ${o.g} · ${list.length} questions. Their score stays hidden until you finish.</p>
        ${ST.profile ? '' : '<input id="dName" maxlength="20" placeholder="Your first name" autocomplete="off">'}
        <button class="btn" id="dGo">Accept duel ▶</button></div><div id="pBody"></div>`;
      $('#dGo').onclick = () => {
        const nm = ST.profile ? null : ($('#dName').value.trim() || 'Friend');
        host.querySelector('.card').remove();
        play($('#pBody'), list, (s, ms) => {
          const m = ST.profile ? me() : { n: nm, a: '🙂' };
          const res = ST.profile ? record({ n: o.n, a: o.a }, s, o.s, ms, o.ms, 'r' + o.id) : (s > o.s || (s === o.s && ms < o.ms) ? 'w' : s === o.s && ms === o.ms ? 'd' : 'l');
          const reply = link('duelr', { v: 1, id: o.id, g: o.g, n: m.n, a: m.a, s, ms, n0: o.n, a0: o.a, s0: o.s, ms0: o.ms, k: list.length });
          sfx(res === 'w' ? 'unlock' : 'hmm');
          $('#pBody').innerHTML = `<div class="card done-card"><div class="gbig">${res === 'w' ? '🏆' : res === 'd' ? '🤝' : '💪'}</div>
            <h2>${res === 'w' ? 'You won!' : res === 'd' ? "It's a tie!" : `${esc(o.n)} wins this time`}</h2>
            <div class="vsrow"><div><b>${esc(m.a)} ${esc(m.n)}</b><span>${s}/${list.length} · ${secs(ms)}</span></div><div class="vsx">VS</div><div><b>${esc(o.a)} ${esc(o.n)}</b><span>${o.s}/${list.length} · ${secs(o.ms)}</span></div></div>
            <button class="btn" id="dReply">📤 Send my result to ${esc(o.n)}</button><div style="height:8px"></div>
            ${ST.profile ? '<button class="btn ghost" id="dBackC">⚔️ Challenge back</button>' : '<button class="btn ghost" id="dJoin">🚀 Join StudyVerse free</button>'}</div>`;
          $('#dReply').onclick = () => share(`${res === 'w' ? '🏆 I beat you' : res === 'd' ? '🤝 We tied' : '💪 You won'}! ${s}/${list.length} vs your ${o.s}/${list.length}. See the result:`, reply);
          if ($('#dBackC')) $('#dBackC').onclick = () => Duel.create(o.g, o.q[0].split('#')[0]);
          if ($('#dJoin')) $('#dJoin').onclick = () => { location.hash = ''; document.querySelectorAll('nav').forEach(n => n.style.display = ''); onboard(1); };
        });
      };
    },
    result(o) {
      show('practice', 'practice');
      const mine = ST.duels['o' + o.id];
      const myS = mine ? mine.s : o.s0, myMs = mine ? mine.ms : o.ms0;
      const res = record({ n: o.n, a: o.a }, myS, o.s, myMs, o.ms, 'x' + o.id + o.n) || '';
      const won = myS > o.s || (myS === o.s && myMs < o.ms), tie = myS === o.s && myMs === o.ms;
      $('#s-practice').innerHTML = `<div class="card done-card"><div class="gbig">${won ? '🏆' : tie ? '🤝' : '💪'}</div><h2>${won ? 'You won the duel!' : tie ? "It's a tie!" : `${esc(o.n)} won the duel`}</h2>
        <div class="vsrow"><div><b>${esc(ST.profile?.avatar || o.a0)} You</b><span>${myS}/${o.k} · ${secs(myMs)}</span></div><div class="vsx">VS</div><div><b>${esc(o.a)} ${esc(o.n)}</b><span>${o.s}/${o.k} · ${secs(o.ms)}</span></div></div>
        <button class="btn" id="dAgain">⚔️ Rematch</button><div style="height:8px"></div><button class="btn ghost" id="dSquad">See my squad</button></div>`;
      $('#dAgain').onclick = () => Duel.create(o.g); $('#dSquad').onclick = squadScreen;
    }
  };
  window.Duel = Duel;

  /* ---------- Squad: real friends from duels ---------- */
  window.squadScreen = function () {
    show('squad', 'squad');
    const fr = Object.values(ST.friends).sort((a, b) => (b.w - b.l) - (a.w - a.l));
    const m = me(), tot = { w: ST.cnt.wins || 0, d: ST.cnt.duels || 0 };
    $('#s-squad').innerHTML = `<div class="card"><h2>⚔️ My Squad</h2><p class="sub">Duel friends with a link: you both answer the same questions. Most correct wins; if it's a tie, the faster one wins.</p>
      <div class="statrow"><div><b>${tot.d}</b><span>Duels</span></div><div><b>${tot.w}</b><span>Wins</span></div><div><b>${ST.xp}</b><span>XP</span></div></div>
      <button class="btn" id="sqDuel">⚔️ Start a duel</button></div>
      <div class="card"><h3>🏆 Friends leaderboard</h3>${fr.length ? fr.map((f, i) => `<div class="row"><div class="rank">${i + 1}</div><div class="av">${esc(f.a)}</div><div class="nm">${esc(f.n)}</div><div class="xp">You ${f.w}–${f.l}${f.d ? ` (${f.d} tie)` : ''}</div></div>`).join('')
        : '<p class="sub">No duels yet. Send your first duel link on WhatsApp. Every friend who plays appears here.</p>'}</div>
      <p class="note">School leagues and weekly ranks arrive with logins.</p>`;
    $('#sqDuel').onclick = () => Duel.create(ST.profile.grade);
  };

  /* ---------- Me: badges ---------- */
  const _me = meScreen;
  meScreen = function () { _me(); const mc = $('#s-me .statrow'); if (mc) mc.insertAdjacentHTML('afterend', `<div class="card"><h3>🏅 Badges</h3>${badgeGrid()}</div>`); };

  /* ---------- open duel links ---------- */
  function route() {
    const h = location.hash; const m = /^#(duel|duelr)=(.+)$/.exec(h); if (!m) return false;
    let o; try { o = b64d(m[2]); } catch (e) { return false; }
    history.replaceState(null, '', location.pathname + location.search);
    const go = () => (m[1] === 'duel' ? Duel.accept(o) : Duel.result(o));
    (function wait(n) { if (typeof CUR !== 'undefined' && CUR && CUR.grades) go(); else if (n < 60) setTimeout(() => wait(n + 1), 100); })(0);
    return true;
  }
  window.addEventListener('hashchange', route);
  window.Garden = { learned, badge, plant, dueList, doneExtra, checkBadges, routeDuel: route, BADGES, GOAL, dailyXP };
  if (location.hash.startsWith('#duel')) setTimeout(route, 50);
  setTimeout(checkBadges, 1500);
})();
