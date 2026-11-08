/* ================= Tests · Confidence check · Revision cards & sheets =================
   Chapter tests and subject mock tests use only reviewed quiz questions. For every answer the student
   says how sure they were. The report separates real understanding from lucky guesses and from
   confident misconceptions, then sends weak topics back to the lesson and into the Memory Garden. */
(function () {
  const CONF = [['sure', '😎', 'Sure'], ['think', '🤔', 'Think so'], ['guess', '🎲', 'Guessing']];
  const STATUS = {
    mis: { e: '🔴', n: 'Misconception', d: 'You were sure, but wrong. Re-learn this first.', r: 0 },
    gap: { e: '🟠', n: 'Gap', d: 'Not understood yet. Read the lesson again.', r: 1 },
    luck: { e: '🟡', n: 'Lucky', d: 'Right, but by guessing. Revise to make it solid.', r: 2 },
    solid: { e: '🟢', n: 'Understood', d: 'You know this. Keep it fresh with revision.', r: 3 } };
  ST.tests = ST.tests || {};
  const testKey = (g, sid, ci) => `g${g}-${sid}${ci == null ? '' : '-' + ci}`;

  /* ---------- revision card ---------- */
  const LV = { core: ['Core', '#2ed3a5'], important: ['Exam favourite', '#ff9f43'], advanced: ['Challenge', '#8b5cf6'] };
  function revCard(t, opts = {}) {
    const r = t.revise, li = a => (a || []).map(x => `<li>${esc(x)}</li>`).join('');
    const lv = r && LV[r.level];
    const body = r ? `<p class="rv-sum">${esc(r.summary)}</p>
        <div class="rv-sec"><b>🎯 Focus on</b><ul>${li(r.focus)}</ul></div>
        <div class="rv-sec rem"><b>📌 Must remember</b><ul>${li(r.remember)}</ul></div>
        <div class="rv-sec trap"><b>⚠️ Common traps</b><ul>${li(r.traps)}</ul></div>`
      : `<div class="rv-sec"><b>🧠 Key points</b><ul>${li((t.learn || {}).points)}</ul></div>`;
    return `<div class="rvcard" data-tid="${esc(t.id)}"><div class="rv-top"><h3>${opts.num ? `<span class="rv-n">${opts.num}</span>` : '📝'} ${esc(t.title)}</h3>${lv ? `<span class="rv-lv" style="background:${lv[1]}">${lv[0]}</span>` : ''}</div>
      <div class="rv-body">${body}</div>${opts.status ? `<div class="rv-st">${STATUS[opts.status].e} ${STATUS[opts.status].n}</div>` : ''}
      <div class="rv-acts ra-skip"><button class="spk rv-spk" data-ra=".rvcard" aria-label="Read aloud">🔊</button>${opts.open ? '<button class="btn ghost rv-open">📖 Open lesson</button>' : ''}</div></div>`;
  }
  function showCardModal(t, sid, ci, ti) {
    let m = document.getElementById('rvModal');
    if (!m) { document.body.insertAdjacentHTML('beforeend', '<div class="asksheet" id="rvModal"><div class="ask-in rv-modal"><div class="ask-head"><b>📝 Revision card</b><button class="ask-x" id="rvX">✕</button></div><div class="ask-log" id="rvBody"></div></div></div>'); m = document.getElementById('rvModal'); document.getElementById('rvX').onclick = () => m.classList.remove('show'); m.onclick = e => { if (e.target === m) m.classList.remove('show'); }; }
    document.getElementById('rvBody').innerHTML = revCard(t, { open: true });
    const ob = m.querySelector('.rv-open'); if (ob) ob.onclick = () => { m.classList.remove('show'); playTopic(sid, ci, ti); };
    m.classList.add('show');
  }

  /* ---------- chapter revision sheet ---------- */
  async function sheet(sid, ci) {
    const g = ST.profile.grade, d = await subjectData(g, sid), c = d.chapters[ci];
    show('chapter', 'world'); const el = $('#s-chapter');
    const last = ST.tests[testKey(g, sid, ci)];
    const weak = new Set(last ? Object.entries(last.topics || {}).filter(([, s]) => s !== 'solid').map(([k]) => k) : []);
    el.innerHTML = `<button class="back" id="rsBack">← Chapter</button>
      <div class="card chead"><div class="cemoji">📝</div><div><span class="tag">Revision sheet</span><h2>${esc(c.title)}</h2><p class="sub">${c.topics.length} topics · read it in 5 minutes before a test</p></div></div>
      <div class="rv-filter">${[['all', 'All'], ['core', 'Core'], ['important', 'Exam favourites'], ['advanced', 'Challenge'], ['weak', `My weak ones${weak.size ? ` (${weak.size})` : ''}`]].map(([k, n], i) => `<button class="${i ? '' : 'on'}" data-f="${k}">${n}</button>`).join('')}</div>
      <div id="rsList">${c.topics.map((t, i) => revCard(t, { num: i + 1, open: true, status: last && last.topics ? last.topics[t.id] : null })).join('')}</div>
      <div class="card"><button class="btn" id="rsTest">🎯 Test this chapter now</button><div style="height:8px"></div><button class="btn ghost" onclick="window.print()">🖨️ Print / save as PDF</button></div>`;
    $('#rsBack').onclick = () => chapterScreen(sid, ci);
    $('#rsTest').onclick = () => run('chapter', sid, ci);
    el.querySelectorAll('.rv-open').forEach(b => b.onclick = () => { const ti = c.topics.findIndex(t => t.id === b.closest('.rvcard').dataset.tid); playTopic(sid, ci, ti); });
    el.querySelectorAll('.rv-filter button').forEach(b => b.onclick = () => {
      el.querySelectorAll('.rv-filter button').forEach(x => x.classList.toggle('on', x === b)); const f = b.dataset.f;
      el.querySelectorAll('#rsList .rvcard').forEach(card => { const t = c.topics.find(x => x.id === card.dataset.tid); const lvl = t.revise && t.revise.level;
        card.style.display = f === 'all' || (f === 'weak' ? weak.has(t.id) : lvl === f) ? '' : 'none'; });
    });
  }

  /* ---------- building a test ---------- */
  function pick(topics, total) {
    const per = Math.max(1, Math.ceil(total / topics.length)), list = [];
    topics.forEach(t => Games.shuffle(t.quiz.map((q, i) => i)).slice(0, per).forEach(i => list.push({ q: t.quiz[i], qid: `${t.id}#${i}`, t })));
    return Games.shuffle(list).slice(0, total);
  }
  async function run(kind, sid, ci) {
    const g = ST.profile.grade, d = await subjectData(g, sid); if (!d) return;
    RUN = null;
    let topics, title, total;
    if (kind === 'chapter') { topics = d.chapters[ci].topics.map((t, ti) => ({ ...t, ci, ti })); title = d.chapters[ci].title; total = Math.min(20, Math.max(10, topics.length * 2)); }
    else { topics = []; d.chapters.forEach((c, i) => c.topics.forEach((t, ti) => topics.push({ ...t, ci: i, ti }))); title = (curSubjects(g).find(s => s.id === sid) || {}).name || sid; total = 25;
      if (topics.length > total) { const w = t => (t.revise && t.revise.level === 'important' ? 2 : 1) + Math.random(); topics = topics.sort((a, b) => w(b) - w(a)).slice(0, total); } }
    const list = pick(topics, total);
    show('practice', 'practice'); const el = $('#s-practice');
    el.innerHTML = `<div class="card tst-intro"><div class="gbig">${kind === 'chapter' ? '🎯' : '🏆'}</div><h2>${kind === 'chapter' ? 'Chapter test' : 'Mock test'}</h2><p class="sub">${esc(title)} · ${list.length} questions</p>
      <div class="tst-how"><b>How it works</b><p>Answer each question, then tell us how sure you are: 😎 Sure, 🤔 Think so, or 🎲 Guessing. Be honest! Your report will show what you really understand, what you got lucky on, and what to re-learn.</p></div>
      <button class="btn" id="tGo">Start ▶</button><div style="height:8px"></div><button class="btn ghost" id="tBack">Back</button></div>`;
    $('#tBack').onclick = () => kind === 'chapter' ? chapterScreen(sid, ci) : subjectScreen(sid);
    $('#tGo').onclick = () => runner(el, list, res => report(el, kind, sid, ci, title, list, res));
  }
  function runner(el, list, done) {
    /* exam-style: move freely, change answers, mark for review, bookmark; submit at the end */
    let i = 0; const ans = list.map(() => ({ chosen: null, conf: null, mark: false })); const t0 = Date.now();
    let onQ = -1, onT = 0; const lap = () => { if (onQ >= 0 && ans[onQ]) ans[onQ].ms = (ans[onQ].ms || 0) + (Date.now() - onT); onQ = -1; };   // time on each question (Parent Hub log only)
    ST.bm = ST.bm || {};
    const render = () => {
      lap(); onQ = i; onT = Date.now();
      const { q, qid } = list[i]; const a = ans[i]; a.order = a.order || Games.shuffle(q.options.map((o, k) => k));
      el.innerHTML = `<div class="card"><div class="tst-top"><span class="tag">Question ${i + 1} of ${list.length}</span>
        <span class="tst-time" id="tTime"></span><button class="tst-ic ${ST.bm[qid] ? 'on' : ''}" id="tBm" aria-label="Bookmark this question">🔖</button><button class="tst-ic" id="tPalBtn" aria-label="All questions">▦</button></div>
        <div class="progress"><i style="width:${ans.filter(x => x.chosen !== null).length / list.length * 100}%"></i></div>
        <h2 class="qtext">${esc(q.q)} <button class="spk" data-opts="1" aria-label="Read aloud">🔊</button></h2>
        <div id="tOpts">${a.order.map(k => `<button class="opt ${a.chosen === k ? 'sel' : ''}" data-k="${k}">${esc(q.options[k])}</button>`).join('')}</div>
        <div class="tst-conf ${a.chosen !== null ? 'show' : ''}" id="tConf"><b>How sure are you?</b><div>${CONF.map(([k, e, n]) => `<button data-c="${k}" class="${a.conf === k ? 'on' : ''}"><span>${e}</span>${n}</button>`).join('')}</div></div>
        <div class="tst-nav"><button class="btn ghost" id="tPrev" ${i ? '' : 'disabled'} aria-label="Previous question">◀ Previous</button><button class="btn ghost tst-mark ${a.mark ? 'on' : ''}" id="tMark">${a.mark ? '🚩 Marked' : '🏳️ Review later'}</button><button class="btn" id="tNext" aria-label="${i < list.length - 1 ? 'Next question' : 'Submit the test'}">${i < list.length - 1 ? 'Next ▶' : 'Submit ✔'}</button></div>
        <div class="tst-pal" id="tPal" hidden>${list.map((x, k) => `<button data-k="${k}" class="${k === i ? 'cur ' : ''}${ans[k].chosen !== null ? 'done ' : ''}${ans[k].mark ? 'mark' : ''}">${k + 1}</button>`).join('')}<small>🟣 answered · 🚩 marked · ⚪ not answered</small></div></div>`;
      const tick = () => { const s = Math.round((Date.now() - t0) / 1000), tt = document.getElementById('tTime'); if (tt) tt.textContent = `⏱ ${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; };
      tick(); clearInterval(runner.iv); runner.iv = setInterval(tick, 1000);
      el.querySelectorAll('#tOpts .opt').forEach(b => b.onclick = () => { a.chosen = +b.dataset.k; if (!a.conf) a.conf = null; el.querySelectorAll('#tOpts .opt').forEach(x => x.classList.toggle('sel', x === b)); sfx('tap'); document.getElementById('tConf').classList.add('show'); });
      el.querySelectorAll('#tConf button').forEach(b => b.onclick = () => { a.conf = b.dataset.c; el.querySelectorAll('#tConf button').forEach(x => x.classList.toggle('on', x === b)); sfx('tap'); if (i < list.length - 1) setTimeout(() => { i++; render(); }, 250); });
      $('#tPrev').onclick = () => { if (i) { i--; render(); } };
      $('#tMark').onclick = () => { a.mark = !a.mark; render(); };
      $('#tBm').onclick = () => { if (ST.bm[qid]) delete ST.bm[qid]; else ST.bm[qid] = today(); save(); render(); toast(ST.bm[qid] ? '🔖 Bookmarked' : 'Bookmark removed'); };
      $('#tPalBtn').onclick = () => { const p = $('#tPal'); p.hidden = !p.hidden; };
      el.querySelectorAll('#tPal button').forEach(b => b.onclick = () => { i = +b.dataset.k; render(); });
      $('#tNext').onclick = () => {
        if (a.chosen !== null && !a.conf) a.conf = 'think';
        if (i < list.length - 1) { i++; render(); return; }
        const left = ans.filter(x => x.chosen === null).length, marked = ans.filter(x => x.mark).length;
        if ((left || marked) && !confirm(`${left ? left + ' unanswered' : ''}${left && marked ? ' and ' : ''}${marked ? marked + ' marked for review' : ''}. Submit anyway?`)) { $('#tPal').hidden = false; return; }
        clearInterval(runner.iv); lap();
        const res = ans.map((x, k) => { const q = list[k].q; const ok = x.chosen === q.answer;
          if (x.chosen !== null && typeof logAns === 'function') logAns(list[k].qid, ok, (x.ms || 0) / 1000);
          const qs = ST.qstats[list[k].qid] || { s: 0, w: 0 }; qs.s++; if (!ok) { qs.w++; if (q.mistake) ST.mistakes[q.mistake] = (ST.mistakes[q.mistake] || 0) + 1; } ST.qstats[list[k].qid] = qs;
          const r = { ok, chosen: x.chosen, conf: x.chosen === null ? 'guess' : (x.conf || 'think'), skipped: x.chosen === null };
          if (window.Insights) Insights.conf(list[k].qid, r.conf, ok);   /* per-answer confidence for js/insights.js */
          return r; });
        save(); done({ res, secs: Math.round((Date.now() - t0) / 1000) });
      };
    };
    render();
  }
  const cls = r => r.ok ? (r.conf === 'guess' ? 'luck' : 'solid') : (r.conf === 'sure' ? 'mis' : 'gap');
  function report(el, kind, sid, ci, title, list, { res, secs }) {
    const g = ST.profile.grade, right = res.filter(r => r.ok).length, pct = Math.round(right / res.length * 100);
    const per = {};
    list.forEach((x, i) => { const c = cls(res[i]); const p = per[x.t.id] = per[x.t.id] || { t: x.t, n: 0, ok: 0, worst: 'solid' }; p.n++; if (res[i].ok) p.ok++; if (STATUS[c].r < STATUS[p.worst].r) p.worst = c; });
    const counts = { solid: 0, luck: 0, gap: 0, mis: 0 }; res.forEach(r => counts[cls(r)]++);
    const ready = Math.round((counts.solid * 1 + counts.luck * .4) / res.length * 100);
    const topicsStatus = {}; Object.values(per).forEach(p => topicsStatus[p.t.id] = p.worst);
    ST.tests[testKey(g, sid, kind === 'chapter' ? ci : null)] = { d: today(), pct, ready, topics: topicsStatus };
    Object.values(per).forEach(p => { if (p.worst !== 'solid') { const m = ST.mem[p.t.id] || { b: 0, n: 0 }; m.b = Math.max(0, (m.b || 0) - (p.worst === 'mis' ? 2 : 1)); m.due = today(); ST.mem[p.t.id] = m; } });
    addXP(right * 3 + (pct >= 90 ? 20 : 0), null); bumpStreak(); save(); sfx(pct >= 60 ? 'unlock' : 'hmm');
    const rows = Object.values(per).sort((a, b) => STATUS[a.worst].r - STATUS[b.worst].r);
    el.innerHTML = `<div class="card done-card tst-rep"><div class="gbig">${pct >= 90 ? '🏆' : pct >= 70 ? '🌟' : pct >= 40 ? '💪' : '📚'}</div>
      <h2>${esc(title)}</h2><p class="sub">${right} of ${res.length} correct · ${pct}% · ⏱ ${Math.floor(secs / 60)}m ${secs % 60}s</p>
      <div class="ready"><div class="ready-bar"><i style="width:${ready}%"></i></div><b>Exam readiness: ${ready}%</b><small>Only answers you were sure of, or fairly sure of, count fully. Lucky guesses count a little.</small></div>
      <div class="tst-mix">${['solid', 'luck', 'gap', 'mis'].map(k => `<div class="${k}"><b>${counts[k]}</b><span>${STATUS[k].e} ${STATUS[k].n}</span></div>`).join('')}</div></div>
      <div class="card"><h3>📋 Topic by topic</h3><p class="sub">Red and orange topics are now in your Memory Garden for revision today.</p>
      ${rows.map(p => `<div class="tst-row ${p.worst}" data-tid="${esc(p.t.id)}"><div><b>${STATUS[p.worst].e} ${esc(p.t.title)}</b><small>${p.ok}/${p.n} · ${STATUS[p.worst].d}</small></div>
        <div class="tst-acts">${p.worst !== 'solid' ? '<button class="rl">📖 Re-learn</button>' : ''}<button class="rc">📝 Card</button></div></div>`).join('')}</div>
      <div class="card"><h3>🔍 Review your answers</h3>${list.map((x, i) => { const r = res[i], q = x.q; return `<div class="tst-rev ${r.ok ? 'ok' : 'no'}"><b>${i + 1}. ${esc(q.q)}</b>
        <p>${r.ok ? '✅' : '❌'} You: ${r.skipped ? '<i>skipped</i>' : esc(q.options[r.chosen])} <small>(${CONF.find(c => c[0] === r.conf)[1]})</small>${r.ok ? '' : `<br>✔ Correct: <b>${esc(q.options[q.answer])}</b>`}</p><p class="why">${esc(q.explain || '')}</p>${(q.steps || []).length ? `<ol class="tst-sol">${q.steps.map(x => `<li>${esc(x)}</li>`).join('')}</ol>` : ''}</div>`; }).join('')}</div>
      <div class="card"><button class="btn" id="trAgain">🔁 Take another test</button><div style="height:8px"></div><button class="btn ghost" id="trBack">Done</button></div>`;
    el.querySelectorAll('.tst-row').forEach(row => { const p = per[row.dataset.tid];
      const rl = row.querySelector('.rl'); if (rl) rl.onclick = () => playTopic(sid, p.t.ci, p.t.ti);
      row.querySelector('.rc').onclick = () => showCardModal(p.t, sid, p.t.ci, p.t.ti); });
    $('#trAgain').onclick = () => run(kind, sid, ci);
    $('#trBack').onclick = () => kind === 'chapter' ? chapterScreen(sid, ci) : subjectScreen(sid);
    if (window.Garden) Garden.checkBadges();
  }

  /* ---------- hooks into existing screens ---------- */
  const _chapter = chapterScreen;
  chapterScreen = async function (sid, ci) {
    await _chapter(sid, ci);
    const g = ST.profile.grade, last = ST.tests[testKey(g, sid, ci)];
    const head = document.querySelector('#s-chapter .chead'); if (!head) return;
    head.insertAdjacentHTML('afterend', `<div class="ch-tools">${last ? `<div class="ch-ready"><span>Readiness</span><div class="ready-bar"><i style="width:${last.ready}%"></i></div><b>${last.ready}%</b></div>` : ''}
      <div class="ch-btns"><button id="chSheet">📝 Revision sheet</button><button id="chTest">🎯 Chapter test</button><button id="chArc">🕹️ Games</button></div></div>`);
    $('#chSheet').onclick = () => sheet(sid, ci); $('#chTest').onclick = () => run('chapter', sid, ci);
    $('#chArc').onclick = () => arcade({ grade: g, subject: sid, chapter: ci });
  };
  const _subject = subjectScreen;
  subjectScreen = async function (sid) {
    await _subject(sid);
    const g = ST.profile.grade; document.getElementById('subTools')?.remove();
    $('#subTitle').insertAdjacentHTML('afterend', `<div class="ch-btns sub-btns" id="subTools"><button id="sbMock">🏆 Mock test</button><button id="sbArc">🕹️ Games</button><button id="sbAsk">🐥 Ask a doubt</button></div>`);
    $('#sbMock').onclick = () => run('mock', sid); $('#sbArc').onclick = () => arcade({ grade: g, subject: sid }); $('#sbAsk').onclick = () => window.Ask && Ask.open();
  };
  const _practice = practiceScreen;
  practiceScreen = async function () {
    await _practice();
    const el = $('#s-practice'), g = ST.profile.grade;
    const first = el.querySelector('.card'); if (!first) return;
    first.insertAdjacentHTML('afterend', `<div class="card"><h3>🕹️ Games & tests</h3><p class="sub">Mix concepts across all your subjects, or test yourself honestly.</p>
      <button class="btn" id="pArc">🕹️ Arcade: all subjects</button><div style="height:8px"></div>
      <div class="ch-btns">${curSubjects(g).map(s => `<button data-s="${s.id}">🏆 ${esc(s.name)}</button>`).join('')}</div><small class="sub">Tap a subject for its mock test</small></div>`);
    $('#pArc').onclick = () => arcade({ grade: g });
    el.querySelectorAll('.ch-btns button[data-s]').forEach(b => b.onclick = () => run('mock', b.dataset.s));
  };
  function arcade(scope) {
    show('practice', 'practice'); RUN = null;
    const el = $('#s-practice'); el.innerHTML = '<button class="back" id="arcBack">← Back</button><div id="arcHost"></div>';
    $('#arcBack').onclick = () => scope.chapter != null ? chapterScreen(scope.subject, scope.chapter) : scope.subject ? subjectScreen(scope.subject) : practiceScreen();
    if (window.Arcade) Arcade.open($('#arcHost'), scope); else $('#arcHost').innerHTML = '<div class="card"><p class="sub">Games are loading. Please try again in a moment.</p></div>';
  }
  window.Tests = { run, sheet, revCard, showCardModal, arcade };
})();
