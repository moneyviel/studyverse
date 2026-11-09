/* ================= Insights: "My analysis" gauges + student Dashboard =================
   What this file adds
   1. Lightweight recording (no change to old saves; everything new lives in ST.ins):
        ST.ins = { v:1,
          att: [[minuteStamp, qid, ok 1/0, conf 0-3], …]   last 2000 answers (conf: 0 none · 1 sure · 2 think so · 3 guessing)
          day: { 'YYYY-MM-DD': { a: answers, r: right, x: XP, s: active seconds, q: quests, sj: { sid: [answers, right, seconds] } } }
          tl:  [{ k: test key, d, ts, pct, ready, mix: {solid, luck, gap, mis} }]   every test, not only the latest
          tt:  { topicId: seconds spent in the topic player } }
      Answers are caught by watching writes to ST.qstats (every quiz, practice, revision and test already writes there),
      tests by watching writes to ST.tests, XP by wrapping addXP, and time by a 15-second heartbeat that only counts
      while the app is visible and the student touched it in the last minute. Old saves are back-filled once from
      ST.topics (quest dates) and ST.tests (last test of each chapter).
   2. Strength score (0–100) — see STRENGTH below and the "How is this calculated?" sheet.
   3. My analysis (Me screen + full screen) and the Dashboard (Me screen, world-map shortcut), all drillable:
      subject → chapter → topic → the questions you got wrong (with steps).
   Charts are plain SVG; every chart has a one-line summary and a table version (for screen readers and the
   "Table" toggle). Results are cached until something new is recorded.
   4. The Dashboard itself is drawn by js/dashboard.js (SVDash). This file turns its model into the generic
      data shape below; any other module can draw the same dashboard with its own data:

   ================= Generic dashboard API (for js/ca.js and others) =================
     const dash = Insights.dashboardFor(hostElement, { mode: 'ca', data, onStart, onLeaf, leafLabel, startLabel, filters });
       → draws into hostElement (keeps its own filters/drill state on the element); call again with a NEW data
         object when the data changes (results are cached per data object), or dash.refresh() to repaint.
     Insights.dashboardTile(data, { label, id }) → HTML string of the compact tile (a <button data-dk-open>);
         wire its click yourself. SVDash.sampleData('ca'|'school') returns demo data in this shape.
     opts: mode 'school' | 'ca' (only changes small styling) · onStart() for the empty-state button ·
           onLeaf(path) adds an "Open …" button when the student drills to a level-3 item (path = [id1, id2, id3]) ·
           filters: initial { period: '7'|'30'|'90'|'all'|'custom', from, to, scope: [id1, id2?], compare: bool }.
     data = {
       title: 'Dashboard', subtitle: 'CA Foundation', rootName: 'All papers',   // header texts (optional)
       levels: ['Paper', 'Chapter', 'Unit'],          // names of the 3 drill levels (school: Subject, Chapter, Topic)
       tree: [ { id, name, score?, enough?,           // level 1 (paper / subject); score = strength 0–100 if you have
                 children: [ { id, name, score?,      //   your own model (else it is computed: smoothed MCQ accuracy,
                   children: [ { id, name, score?, note?,   //   70%, blended with self-check marks, 30%); enough:false = "no data yet"
                     questions?: { [qid]: { q: 'question text', a: 'correct answer text', explain?: '…' } } } ] } ] } ],
       events: [ { t: msTimestamp, path: [id1, id2, id3], qid?: 'any id',   // ids must exist in tree
                   ok: 1 | 0 | null,                  // MCQ right / wrong / skipped (null = skipped)
                   conf?: 0|1|2|3,                    // 0 none · 1 sure · 2 think so · 3 guessing → confidence matrix
                   secs?: seconds spent,              // used for time when days[] has no time for this level
                   kind?: 'mcq' | 'write',            // 'write' = written answer marked by self-check:
                   score?, max?, skills?: ['tag'] } ],//   score/max feeds "Self-check" KPI and the skills chart
       days?: { 'YYYY-MM-DD': { secs, xp?, by?: { id1: secs } } },   // day keys as the app's today() (UTC ISO date)
       tests?: [ { t | d: 'YYYY-MM-DD', name, pct: 0–100, path?: [id1, id2?] } ],   // chapter tests, mock tests
       testLabel?: 'Mock tests',  skills?: { tag: 'Readable name' },
       streak?: { n, best? },  overall?: { score },  nextTest?: { name, date: 'YYYY-MM-DD' },
       minEvents?: 8,  answered?: total answers known (for the empty state when events were not tracked)
     }
     Everything else (KPIs and their change vs the previous period, sparklines, readiness, trend, stacked
     correct/wrong/skipped, breakdown, radar, mastery donut, heatmap, streak calendar, time of day, confidence,
     skills, tests, sortable table, question list) is derived from this. */
(function () {
  'use strict';
  const DAY = 864e5, MAX_ATT = 2000, MIN_SUBJ = 5, MIN_ALL = 8;
  const dkey = t => new Date(t).toISOString().slice(0, 10);
  const dnum = d => Date.parse(d + 'T00:00:00Z');
  const addD = (d, n) => dkey(dnum(d) + n * DAY);
  const fmtD = d => new Date(dnum(d)).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' });
  const fmtDur = s => { const m = Math.round((s || 0) / 60); return m < 60 ? `${m} min` : `${Math.floor(m / 60)} h ${m % 60} min`; };
  const pctS = v => v == null ? '–' : Math.round(v) + '%';
  const parseQ = qid => { const m = /^g(\d+)-([a-z]+)-/.exec(qid || ''); return m ? { g: +m[1], sid: m[2] } : null; };
  const CONF_CODE = { sure: 1, think: 2, guess: 3 };
  const SE = sid => (Worlds.SUBJECT_STYLE[sid] || {}).e || '📘';

  /* ---------------- 1. state + migration ---------------- */
  function initState() {
    const I = ST.ins && ST.ins.v ? ST.ins : (ST.ins = { v: 1 });
    I.att = Array.isArray(I.att) ? I.att : []; I.day = I.day || {}; I.tl = Array.isArray(I.tl) ? I.tl : []; I.tt = I.tt || {};
    if (!I.mig) {               // one-time back-fill from data that older versions already kept
      I.mig = 1;
      Object.values(ST.topics || {}).forEach(t => { if (t && t.last) { const d = dayRec(t.last); d.q = (d.q || 0) + 1; } });
      Object.entries(ST.tests || {}).forEach(([k, t]) => { if (t && t.d) I.tl.push({ k, d: t.d, ts: dnum(t.d), pct: t.pct, ready: t.ready, mix: null }); });
    }
    return I;
  }
  function dayRec(d) { const I = ST.ins; return I.day[d] || (I.day[d] = { a: 0, r: 0, x: 0, s: 0, q: 0, sj: {} }); }
  const I = initState();
  let ver = 0;                 // bumps on every new record → cache key

  /* answers: watch writes to ST.qstats */
  const shadow = {};
  Object.entries(ST.qstats || {}).forEach(([k, v]) => { shadow[k] = [v.s || 0, v.w || 0]; });
  function recAnswer(qid, v) {
    const sh = shadow[qid] || [0, 0], ds = (v.s || 0) - sh[0], dw = Math.max(0, (v.w || 0) - sh[1]);
    shadow[qid] = [v.s || 0, v.w || 0]; if (ds <= 0) return;
    const now = Math.floor(Date.now() / 6e4), d = dayRec(today()), p = parseQ(qid);
    for (let i = 0; i < ds; i++) I.att.push([now, qid, i < ds - dw ? 1 : 0, 0]);
    if (I.att.length > MAX_ATT) I.att.splice(0, I.att.length - MAX_ATT);
    d.a += ds; d.r += ds - dw;
    if (p) { const s = d.sj[p.sid] || (d.sj[p.sid] = [0, 0, 0]); s[0] += ds; s[1] += ds - dw; }
    ver++;
  }
  if (ST.qstats && !ST.qstats.__ins) {
    const raw = ST.qstats;
    ST.qstats = new Proxy(raw, { set(o, k, v) { o[k] = v; try { if (v && typeof v === 'object') recAnswer(k, v); } catch (e) {} return true; },
      get(o, k) { return k === '__ins' ? true : o[k]; } });
  }
  /* confidence for test answers (called from js/tests.js right after each answer is scored) */
  let pend = [];
  function conf(qid, c, ok) {
    const code = CONF_CODE[c] || 0, lim = Math.floor(Date.now() / 6e4) - 3;
    for (let i = I.att.length - 1; i >= 0 && I.att[i][0] >= lim; i--) if (I.att[i][1] === qid && !I.att[i][3]) { I.att[i][3] = code; break; }
    pend.push(ok ? (c === 'guess' ? 'luck' : 'solid') : (c === 'sure' ? 'mis' : 'gap')); ver++;
  }
  /* tests: keep every result, not only the latest per chapter */
  if (ST.tests && !ST.tests.__ins) {
    const raw = ST.tests;
    ST.tests = new Proxy(raw, { set(o, k, v) { o[k] = v; try {
        const mix = { solid: 0, luck: 0, gap: 0, mis: 0 }; pend.forEach(x => mix[x]++);
        I.tl.push({ k, d: v.d || today(), ts: Date.now(), pct: v.pct, ready: v.ready, mix: pend.length ? mix : null }); pend = [];
        if (I.tl.length > 300) I.tl.splice(0, I.tl.length - 300); ver++;
      } catch (e) {} return true; },
      get(o, k) { return k === '__ins' ? true : o[k]; } });
  }
  /* XP per day */
  const _addXP = addXP;
  addXP = function (n) { try { dayRec(today()).x += +n || 0; ver++; } catch (e) {} return _addXP.apply(this, arguments); };
  /* quests per day: doneStep writes ST.topics[tid].last = today, then calls bumpStreak */
  const qSeen = new Set(Object.entries(ST.topics || {}).map(([k, t]) => k + (t && t.last)));
  function checkQuests() { Object.entries(ST.topics || {}).forEach(([k, t]) => { const key = k + (t && t.last); if (t && t.last === today() && !qSeen.has(key)) { qSeen.add(key); dayRec(today()).q++; ver++; } }); }
  const _bump = bumpStreak;
  bumpStreak = function () { try { checkQuests(); } catch (e) {} return _bump.apply(this, arguments); };
  /* active time: 15-second heartbeat */
  let lastInput = Date.now();
  ['pointerdown', 'keydown', 'scroll', 'touchstart'].forEach(e => window.addEventListener(e, () => { lastInput = Date.now(); }, { passive: true, capture: true }));
  setInterval(() => {
    if (!ST.profile || document.visibilityState !== 'visible' || Date.now() - lastInput > 60000) return;
    const d = dayRec(today()); d.s += 15;
    let sid = null, tid = null;
    try { const sc = (document.querySelector('.screen.active') || {}).id; const run = typeof RUN !== 'undefined' ? RUN : null;
      if (sc === 's-topic' && run && run.t) { tid = run.t.id; sid = run.sid; } else if (/s-(subject|chapter|topic)/.test(sc) && NAV && NAV.subject) sid = NAV.subject; } catch (e) {}
    if (sid) { const s = d.sj[sid] || (d.sj[sid] = [0, 0, 0]); s[2] = (s[2] || 0) + 15; }
    if (tid) I.tt[tid] = (I.tt[tid] || 0) + 15;
    checkQuests();
  }, 15000);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') { checkQuests(); save(); } });

  /* ---------------- 2. STRENGTH ----------------
     Topic strength (0–100) = weighted average of the parts we have data for (weights re-scaled if a part is missing):
       • Accuracy   50% — share of right answers; recent answers count more (an answer's weight halves every 21 days;
                          answers from before this tracking existed count as 30 days old). A small "50%" prior stops
                          one lucky answer from looking perfect: acc = (Σ w·right + 0.25) / (Σ w + 0.5).
       • Test       20% — latest chapter/mock test result for the topic: understood 1 · lucky 0.5 · gap 0.2 · misconception 0.
       • Confidence 15% — honesty check from tests: 1 − (sure-but-wrong + ½ × lucky guesses) / answers rated.
       • Memory     15% — Memory Garden: (0.6 + 0.08 × growth stage up to 5); if a review is overdue it drops 10% per day late (min 40%).
     Chapter = topic strengths averaged (topics with more answers count more, up to 10).
     Subject = 85% × average topic strength + 15% × coverage (share of the subject's topics you have practised).
     Overall = subject strengths averaged, each weighted by √(answers).
     Bands: under 40 Very weak · 40–59 Weak · 60–79 Strong · 80+ Very strong.
     "Not enough data": a subject needs 5 answers, the overall gauge 8 answers (or one test). */
  const BANDS = [[0, 'Very weak', '#d03b3b', 'vw'], [40, 'Weak', '#ec835a', 'w'], [60, 'Strong', '#7cc96f', 's'], [80, 'Very strong', '#0ca30c', 'vs']];
  const band = v => v == null ? null : BANDS.filter(b => v >= b[0]).pop();
  const W = { acc: .5, test: .2, cal: .15, mem: .15 };
  const TEST_VAL = { solid: 1, luck: .5, gap: .2, mis: 0 };
  const STATUS = { mis: '🔴 Misconception', gap: '🟠 Gap', luck: '🟡 Lucky', solid: '🟢 Understood' };

  /* ---------------- structure (per grade, cached) ---------------- */
  let STRUCT = null;
  async function structure() {
    const g = ST.profile.grade, subs = curSubjects(g), key = g + ':' + subs.map(s => s.id).join(',');
    if (STRUCT && STRUCT.key === key) return STRUCT;
    const datas = await Promise.all(subs.map(s => subjectData(g, s.id)));
    const S = { key, g, subs: [], Q: {}, T: {} };
    subs.forEach((s, i) => { const d = datas[i]; if (!d) return;
      const sub = { sid: s.id, name: s.name, chapters: [] };
      d.chapters.forEach((c, ci) => { const ch = { sid: s.id, ci, c, title: c.title, n: c.n, topics: [] };
        c.topics.forEach((t, ti) => { const T = { t, id: t.id, title: t.title, sid: s.id, ci, ti, ch, qn: (t.quiz || []).length };
          S.T[t.id] = T; ch.topics.push(T); (t.quiz || []).forEach((q, k) => { S.Q[`${t.id}#${k}`] = { q, T, k }; }); });
        sub.chapters.push(ch); });
      S.subs.push(sub); });
    return (STRUCT = S);
  }

  /* ---------------- model (cached until something new is recorded) ---------------- */
  let MC = { sig: '', m: null };
  async function model() {
    const S = await structure();
    const sig = [S.key, ver, I.att.length, Object.keys(ST.qstats).length, Object.keys(ST.mem || {}).length, Object.keys(ST.topics).length, I.tl.length, today()].join('|');
    if (MC.sig === sig) return MC.m;
    const g = S.g, td = today(), nowMin = Date.now() / 6e4;
    const pre = `g${g}-`;
    /* per-question dated attempts */
    const byQ = {};
    I.att.forEach(a => { if (a[1].startsWith(pre)) (byQ[a[1]] = byQ[a[1]] || []).push(a); });
    /* latest test status per topic */
    const tst = {};
    Object.entries(ST.tests || {}).forEach(([k, t]) => { if (!k.startsWith(pre) || !t || !t.topics) return;
      Object.entries(t.topics).forEach(([tid, st]) => { if (!tst[tid] || (t.d || '') >= tst[tid].d) tst[tid] = { st, d: t.d || '' }; }); });
    const topics = [], chapters = [], subjects = [];
    let allAns = 0;
    S.subs.forEach(sub => {
      let sAns = 0, sRight = 0, sCov = 0, sN = 0, sw = 0, sws = 0; const sChaps = [];
      sub.chapters.forEach(ch => {
        let cw = 0, cws = 0, cAns = 0, cRight = 0, cDone = 0, cLast = '', cCov = 0; const cTopics = [];
        ch.topics.forEach(T => {
          let ans = 0, wrong = 0, wSum = 0, wOk = 0, last = '', nConf = 0, mis = 0, luck = 0; const wrongQs = [];
          for (let k = 0; k < T.qn; k++) {
            const qid = `${T.id}#${k}`, qs = ST.qstats[qid]; if (!qs || !qs.s) continue;
            ans += qs.s; wrong += qs.w || 0;
            const at = byQ[qid] || []; let dOk = 0, dN = at.length, lastWrong = '';
            at.forEach(a => { const age = Math.max(0, (nowMin - a[0]) / 1440), w = Math.pow(.5, age / 21); wSum += w; if (a[2]) { wOk += w; dOk++; } else lastWrong = dkey(a[0] * 6e4);
              const dd = dkey(a[0] * 6e4); if (dd > last) last = dd;
              if (a[3]) { nConf++; if (!a[2] && a[3] === 1) mis++; if (a[2] && a[3] === 3) luck++; } });
            const legN = Math.max(0, qs.s - dN), legW = Math.min(legN, Math.max(0, (qs.w || 0) - (dN - dOk))), lw = Math.pow(.5, 30 / 21);
            wSum += legN * lw; wOk += (legN - legW) * lw;
            if (qs.w) wrongQs.push({ qid, k, s: qs.s, w: qs.w, last: lastWrong });
          }
          const tp = ST.topics[T.id], mem = (ST.mem || {})[T.id], test = tst[T.id];
          if (tp && tp.last && tp.last > last) last = tp.last;
          if (mem && mem.last && mem.last > last) last = mem.last;
          const comp = {};
          if (ans) comp.acc = (wOk + .25) / (wSum + .5);
          if (test) comp.test = TEST_VAL[test.st] ?? .5;
          if (nConf) comp.cal = Math.max(0, 1 - (mis + .5 * luck) / nConf);
          let late = null;
          if (mem && mem.due) { late = Math.floor((dnum(td) - dnum(mem.due)) / DAY); comp.mem = (.6 + .08 * Math.min(mem.b || 0, 5)) * (late > 0 ? Math.max(.4, 1 - .1 * late) : 1); }
          let score = null;
          if (comp.acc != null || comp.test != null) { let s = 0, w = 0; Object.entries(comp).forEach(([k, v]) => { s += W[k] * v; w += W[k]; }); score = s / w * 100; }
          const enough = ans >= 2 || !!test;
          /* what needs improvement, and how urgently */
          const why = [];
          if (test && test.st === 'mis') why.push({ k: 'mis', p: 100, txt: 'Sure but wrong in a test' });
          if (test && test.st === 'gap') why.push({ k: 'gap', p: 80, txt: 'Not understood in a test' });
          if (mis && !(test && test.st === 'mis')) why.push({ k: 'mis', p: 85, txt: `${mis} sure-but-wrong answer${mis > 1 ? 's' : ''}` });
          if (ans >= 3 && comp.acc != null && comp.acc < .6) why.push({ k: 'acc', p: 50 + Math.round((.6 - comp.acc) * 100), txt: `Low accuracy: ${Math.round((ans - wrong) / ans * 100)}%` });
          if (late != null && late > 0) why.push({ k: 'due', p: 55 + Math.min(30, late * 4), txt: `Review overdue by ${late} day${late > 1 ? 's' : ''}` });
          else if (late === 0) why.push({ k: 'due', p: 40, txt: 'Review due today' });
          if ((test && test.st === 'luck') || luck) why.push({ k: 'luck', p: 45, txt: luck ? `${luck} lucky guess${luck > 1 ? 'es' : ''}` : 'Lucky guesses in a test' });
          why.sort((a, b) => b.p - a.p);
          const prio = why.length ? why[0].p + why.slice(1).reduce((s, x) => s + x.p * .1, 0) : 0;
          const rec = { T, id: T.id, sid: sub.sid, ci: ch.ci, ti: T.ti, ans, wrong, acc: ans ? (ans - wrong) / ans * 100 : null, comp, score, enough, late, test: test && test.st, mis, luck, nConf, last, why, prio, wrongQs, done: !!tp, secs: I.tt[T.id] || 0,
            mastered: score != null && score >= 80 && ans >= 4 };
          topics.push(rec); cTopics.push(rec);
          cAns += ans; cRight += ans - wrong; if (tp) cDone++; if (last > cLast) cLast = last;
          if (score != null) { const w = Math.min(ans, 10) + (test ? 3 : 0) || 1; cw += w; cws += w * score; cCov++; }
        });
        const cScore = cw ? cws / cw : null;
        const crec = { ch, sid: sub.sid, ci: ch.ci, title: ch.title, n: ch.topics.length, topics: cTopics, ans: cAns, acc: cAns ? cRight / cAns * 100 : null, done: cDone, cov: cCov, score: cScore, last: cLast,
          enough: cAns >= 3 || cTopics.some(t => t.test), weakN: cTopics.filter(t => t.why.length).length };
        chapters.push(crec); sChaps.push(crec);
        sAns += cAns; sRight += cRight; sCov += cCov; sN += ch.topics.length; sw += cw; sws += cws;
      });
      const mean = sw ? sws / sw : null, cov = sN ? sCov / sN : 0;
      const hasTest = sChaps.some(c => c.topics.some(t => t.test));
      subjects.push({ sid: sub.sid, name: sub.name, chapters: sChaps, ans: sAns, acc: sAns ? sRight / sAns * 100 : null, mean, cov, n: sN,
        score: mean == null ? null : .85 * mean + 15 * cov, enough: sAns >= MIN_SUBJ || hasTest, need: Math.max(0, MIN_SUBJ - sAns) });
      allAns += sAns;
    });
    let ow = 0, ows = 0; subjects.forEach(s => { if (s.enough && s.score != null) { const w = Math.sqrt(Math.max(1, s.ans)); ow += w; ows += w * s.score; } });
    const anyTest = topics.some(t => t.test);
    const overall = { score: ow ? ows / ow : null, ans: allAns, enough: (allAns >= MIN_ALL || anyTest) && ow > 0, need: Math.max(0, MIN_ALL - allAns) };
    const improve = topics.filter(t => t.why.length).sort((a, b) => b.prio - a.prio);
    const weakCh = chapters.filter(c => c.enough && ((c.score != null && c.score < 60) || c.weakN >= 2)).sort((a, b) => (a.score ?? 100) - (b.score ?? 100));
    const m = { S, g, topics, chapters, subjects, overall, improve, weakCh, byQ, pre };
    MC = { sig, m }; return m;
  }

  /* ---------------- 3. small UI helpers ---------------- */
  const subjName = (m, sid) => (m.subjects.find(s => s.sid === sid) || {}).name || sid;
  function arcPath(cx, cy, r, v0, v1) {
    const p = v => { const a = Math.PI * (1 - v / 100); return [cx + r * Math.cos(a), cy - r * Math.sin(a)]; };
    const [x0, y0] = p(v0), [x1, y1] = p(v1);
    return `M${x0.toFixed(1)},${y0.toFixed(1)} A${r},${r} 0 0 1 ${x1.toFixed(1)},${y1.toFixed(1)}`;
  }
  function gauge(score, enough, opts = {}) {
    const b = enough ? band(score) : null, big = !!opts.big;
    const lbl = opts.label || 'Strength';
    const aria = enough && score != null ? `${lbl}: ${Math.round(score)} out of 100, ${b[1]}` : `${lbl}: not enough data yet`;
    const segs = BANDS.map((x, i) => `<path d="${arcPath(100, 100, 78, x[0] + (i ? .8 : 0), (BANDS[i + 1] || [100])[0] - (i < 3 ? .8 : 0))}" stroke="${x[2]}" stroke-width="20" fill="none" class="ins-g-${x[3]}"/>`).join('');
    const needle = enough && score != null ? `<g class="ins-needle" style="transform:rotate(${(Math.max(0, Math.min(100, score)) * 1.8 - 90).toFixed(1)}deg)"><path d="M100,30 L104.5,100 L95.5,100 Z" class="ins-ndl"/></g><circle cx="100" cy="100" r="8" class="ins-hub"/>` : '';
    const txt = enough && score != null ? `<text x="100" y="${big ? 92 : 90}" text-anchor="middle" class="ins-gnum">${Math.round(score)}</text>` : `<text x="100" y="88" text-anchor="middle" class="ins-gna">?</text>`;
    return `<svg class="ins-gauge ${enough ? '' : 'na'}" viewBox="0 0 200 112" role="img" aria-label="${esc(aria)}">${segs}${needle}${enough && score != null ? '' : txt}</svg>
      <div class="ins-gl ${b ? 'b-' + b[3] : 'b-na'}">${b ? `<b>${Math.round(score)}</b> <span>${b[1]}</span>` : `<span>${opts.naText || 'Not enough data yet'}</span>`}</div>`;
  }
  const bandChip = v => { const b = band(v); return b ? `<span class="ins-chip b-${b[3]}">${b[1]}</span>` : '<span class="ins-chip b-na">New</span>'; };
  const meter = v => `<i class="ins-meter" aria-hidden="true"><i style="width:${Math.max(3, Math.round(v || 0))}%;background:${(band(v) || BANDS[0])[2]}"></i></i>`;
  const legend = () => `<div class="ins-legend" aria-hidden="true">${BANDS.map(b => `<span><i style="background:${b[2]}"></i>${b[1]}</span>`).join('')}</div>`;

  /* ---------------- 4. routing inside #s-insights ---------------- */
  let STACK = [];
  function host() {
    let s = document.getElementById('s-insights');
    if (!s) { document.querySelector('main').insertAdjacentHTML('beforeend', '<section class="screen" id="s-insights"></section>'); s = document.getElementById('s-insights'); }
    return s;
  }
  function open(route, replace) { if (replace && STACK.length) STACK[STACK.length - 1] = route; else STACK.push(route); return render(); }
  function back() { const from = STACK.length === 1 && STACK[0].from; STACK.pop(); if (!STACK.length) return from === 'world' ? worldScreen() : meScreen(); render(); }
  function root(route) { STACK = [route]; return render(); }
  async function render() {
    const r = STACK[STACK.length - 1]; if (!r) return meScreen();
    const el = host(); show('insights', STACK[0] && STACK[0].tab ? 'cadash' : 'me');   // opened from the centre 📊 tab: that tab stays lit
    const m = await model();
    const backTxt = STACK.length > 1 ? '← Back' : r.from === 'world' ? '← Home' : '← Me';
    if (r.v === 'dash' && window.SVDash) {      /* the premium dashboard (js/dashboard.js) keeps its own state on one persistent host */
      const tabRoot = STACK.length === 1 && STACK[0].tab;
      el.innerHTML = tabRoot ? '' : `<button class="back" id="insBack">${backTxt}</button>`; if (!tabRoot) $('#insBack').onclick = back;
      el.appendChild(DASH_HOST);
      el.insertAdjacentHTML('beforeend', `<div class="card" id="insCard"><h3>📊 My analysis</h3><div id="insBody">${overallBlock(m, false)}${m.overall.ans ? `<h4 class="ins-h4">By subject</h4>${gaugeGrid(m)}` : ''}<h4 class="ins-h4">🛠️ Needs improvement</h4>${improveList(m, 3)}
        <div style="height:8px"></div><button class="btn ghost" data-go="analysis">See my full analysis ▶</button></div></div>`);
      { const b = el.querySelector('#insBody');
        b.querySelectorAll('[data-go]').forEach(x => x.onclick = () => { rememberY(); goData(x.dataset); });
        b.querySelectorAll('[data-how]').forEach(x => x.onclick = howSheet);
        b.querySelectorAll('[data-act]').forEach(x => x.onclick = e => { e.stopPropagation(); act(m, x.dataset); }); }
      SVDash.render(DASH_HOST, { mode: 'school', data: dashData(m), onStart: () => worldScreen(), startLabel: 'Start a quest',
        onLeaf: path => { rememberY(); open({ v: 'topic', tid: path[2] }); }, leafLabel: 'Lesson & practice' });
      window.scrollTo(0, r.y || 0); return;
    }
    let html = '';
    try {
      if (r.v === 'analysis') html = viewAnalysis(m, r);
      else if (r.v === 'dash') html = viewDash(m, r);
      else if (r.v === 'subject') html = viewSubject(m, r.sid, r);
      else if (r.v === 'chapter') html = viewChapter(m, r.sid, r.ci);
      else if (r.v === 'topic') html = viewTopic(m, r.tid);
      else if (r.v === 'qs') html = viewQList(m, r);
      else if (r.v === 'list') html = viewTopicList(m, r);
    } catch (e) { console.error(e); html = '<div class="card"><p class="sub">Something went wrong showing this page.</p></div>'; }
    el.innerHTML = `<button class="back" id="insBack">${backTxt}</button>${html}`;
    $('#insBack').onclick = back;
    wire(el, m, r);
    window.scrollTo(0, r.y || 0);
  }

  /* ---------------- views ---------------- */
  function gaugeGrid(m) {
    return `<div class="ins-ggrid">${m.subjects.map(s => `<button class="ins-gcell" data-go="subject" data-sid="${s.sid}" aria-label="${esc(s.name)}: ${s.enough && s.score != null ? Math.round(s.score) + ' out of 100, ' + band(s.score)[1] : 'not enough data yet'}. Open details">
      <span class="ins-gname"><span aria-hidden="true">${SE(s.sid)}</span> ${esc(s.name)}</span>${gauge(s.score, s.enough && s.score != null, { naText: s.need ? `${s.need} more answer${s.need > 1 ? 's' : ''} needed` : 'Not enough data yet' })}</button>`).join('')}</div>`;
  }
  function overallBlock(m, big) {
    const o = m.overall;
    return `<div class="ins-overall">${gauge(o.score, o.enough, { big, label: 'Overall strength', naText: 'Not enough data yet' })}${legend()}
      ${o.enough ? '' : `<p class="sub ins-na">Answer ${o.need || 'a few'} more question${o.need === 1 ? '' : 's'} (or take one chapter test) and your gauges will appear.</p>`}
      <button class="ins-how" data-how="1"><span aria-hidden="true">ⓘ</span> How is this calculated?</button></div>`;
  }
  function actBtns(rec) {
    const t = rec.T.t, hasGen = window.Gen && Gen.has(t.id, t.title, ST.profile.grade, rec.sid);
    return `<div class="ins-acts"><button data-act="lesson" data-tid="${esc(rec.id)}">📖 Lesson</button><button data-act="practice" data-tid="${esc(rec.id)}" ${rec.T.qn ? '' : 'disabled'}>🎯 Practise</button>
      <button data-act="card" data-tid="${esc(rec.id)}">📝 Card</button>${hasGen ? `<button data-act="gen" data-tid="${esc(rec.id)}">♾️ Endless</button>` : ''}</div>`;
  }
  function improveRow(m, t, i) {
    return `<div class="ins-imp" data-tid="${esc(t.id)}"><button class="ins-imp-main" data-go="topic" data-tid="${esc(t.id)}"><span class="ins-rank">${i + 1}</span>
      <span class="ins-imp-b"><b>${esc(t.T.title)}</b><small>${SE(t.sid)} ${esc(subjName(m, t.sid))} · ${esc(t.T.ch.title)}</small>
      <span class="ins-why">${t.why.slice(0, 3).map(w => `<em class="w-${w.k}">${esc(w.txt)}</em>`).join('')}</span></span><span class="chgo" aria-hidden="true">›</span></button>${actBtns(t)}</div>`;
  }
  function improveList(m, max, sid, page) {   /* max: short preview with a 'see all' link · page: full list, paged */
    const list = m.improve.filter(t => !sid || t.sid === sid), weak = m.weakCh.filter(c => !sid || c.sid === sid);
    if (!list.length && !weak.length) return `<p class="sub">${m.overall.ans ? 'Nothing needs fixing right now. Great work! Keep practising to stay strong. 🌟' : 'Nothing yet. Finish a quest and answer some questions — anything that needs work will show up here.'}</p>`;
    const shown = list.slice(0, max || page || list.length), chN = max ? 3 : Math.max(5, Math.round((page || 10) / 2));
    return `${weak.length ? `<h4 class="ins-h4">Chapters to strengthen</h4>${weak.slice(0, chN).map(c => `<button class="ins-chrow" data-go="chapter" data-sid="${c.sid}" data-ci="${c.ci}"><span class="ins-chm"><b>${esc(c.title)}</b><small>${SE(c.sid)} ${esc(subjName(m, c.sid))} · ${c.weakN} topic${c.weakN === 1 ? '' : 's'} need work · ${pctS(c.acc)} correct</small>${meter(c.score)}</span>${bandChip(c.score)}</button>`).join('')}` : ''}
      ${shown.length ? `<h4 class="ins-h4">Topics to fix, most urgent first</h4>${shown.map((t, i) => improveRow(m, t, i)).join('')}` : ''}
      ${max && list.length > max ? `<button class="btn ghost" data-go="analysis">See all ${list.length} topics to fix ▶</button>` : ''}
      ${page && (list.length > page || weak.length > chN) ? `<button class="btn ghost" data-more="1">Show more (${Math.max(0, list.length - page)} topics left) ▼</button>` : ''}`;
  }
  function viewAnalysis(m, r) {
    return `<div class="card"><h2>📊 My analysis</h2>${overallBlock(m, true)}</div>
      <div class="card"><h3>By subject</h3><p class="sub">Tap a subject to see its chapters, topics and the questions you got wrong.</p>${gaugeGrid(m)}</div>
      <div class="card"><h3>🛠️ What needs improvement</h3>${improveList(m, 0, null, r.n || 10)}</div>
      <button class="btn" data-go="dash">📈 Open my dashboard</button><div style="height:14px"></div>`;
  }
  function viewSubject(m, sid, r) {
    const s = m.subjects.find(x => x.sid === sid); if (!s) return '<div class="card"><p class="sub">Subject not found.</p></div>';
    return `<div class="card"><span class="tag">Subject</span><h2>${SE(sid)} ${esc(s.name)}</h2>
        <div class="ins-overall">${gauge(s.score, s.enough && s.score != null, { big: true, label: s.name + ' strength', naText: s.need ? `${s.need} more answer${s.need > 1 ? 's' : ''} needed` : 'Not enough data yet' })}${legend()}</div>
        <div class="statrow ins-mini"><div><b>${pctS(s.acc)}</b><span>Correct</span></div><div><b>${s.ans}</b><span>Answers</span></div><div><b>${Math.round(s.cov * 100)}%</b><span>Covered</span></div></div></div>
      <div class="card"><h3>🛠️ Needs improvement</h3>${improveList(m, 0, sid, r.n || 5)}</div>
      <div class="card"><h3>Chapters</h3>${s.chapters.map(c => `<button class="ins-chrow" data-go="chapter" data-sid="${sid}" data-ci="${c.ci}"><span class="ins-chm"><b>${c.ch.n}. ${esc(c.title)}</b>
        <small>${c.done}/${c.n} topics · ${c.ans ? `${pctS(c.acc)} correct · ${c.ans} answers` : 'not practised yet'}${c.last ? ' · last ' + fmtD(c.last) : ''}</small>${meter(c.score)}</span>${c.enough ? bandChip(c.score) : '<span class="ins-chip b-na">New</span>'}</button>`).join('')}</div>`;
  }
  function viewChapter(m, sid, ci) {
    const c = m.chapters.find(x => x.sid === sid && x.ci === ci); if (!c) return '';
    return `<div class="card chead"><div class="cemoji">${esc(c.ch.c.emoji || '📘')}</div><div><span class="tag">${SE(sid)} ${esc(subjName(m, sid))} · Chapter ${c.ch.n}</span><h2>${esc(c.title)}</h2>
        <p class="sub">${c.enough && c.score != null ? `Strength ${Math.round(c.score)} · ${band(c.score)[1]}` : 'Not enough data yet'} · ${pctS(c.acc)} correct</p></div></div>
      <div class="ins-acts wide"><button data-act="sheet" data-sid="${sid}" data-ci="${ci}">📝 Revision sheet</button><button data-act="ctest" data-sid="${sid}" data-ci="${ci}">🎯 Chapter test</button><button data-act="chapter" data-sid="${sid}" data-ci="${ci}">📖 Open chapter</button></div>
      <div class="card"><h3>Topics</h3>${c.topics.map(t => `<button class="ins-chrow" data-go="topic" data-tid="${esc(t.id)}"><span class="ins-chm"><b>${esc(t.T.title)}</b>
        <small>${t.ans ? `${pctS(t.acc)} correct · ${t.ans} answers` : t.done ? 'done, no quiz answers yet' : 'not started'}${t.wrongQs.length ? ` · ${t.wrongQs.length} wrong question${t.wrongQs.length > 1 ? 's' : ''}` : ''}</small>
        ${t.why.length ? `<span class="ins-why">${t.why.slice(0, 2).map(w => `<em class="w-${w.k}">${esc(w.txt)}</em>`).join('')}</span>` : ''}${meter(t.score)}</span>${t.enough ? bandChip(t.score) : '<span class="ins-chip b-na">New</span>'}</button>`).join('')}</div>`;
  }
  function compRow(name, v, note) { return `<div class="ins-comp"><span>${name}</span>${v == null ? '<b class="na">no data</b>' : `<i class="ins-meter"><i style="width:${Math.round(v * 100)}%"></i></i><b>${Math.round(v * 100)}%</b>`}<small>${note}</small></div>`; }
  function qCard(m, w, i) {
    const x = m.S.Q[w.qid]; if (!x) return '';
    const q = x.q;
    return `<details class="ins-q"><summary><b>${i + 1}. ${esc(q.q)}</b><small>Wrong ${w.w} of ${w.s} time${w.s > 1 ? 's' : ''}${w.last ? ' · last wrong ' + fmtD(w.last) : ''}</small></summary>
      <div class="ins-qa"><p>✔ Correct answer: <b>${esc(q.options[q.answer])}</b></p>${q.explain ? `<p class="why">${esc(q.explain)}</p>` : ''}
      ${(q.steps || []).length ? `<ol class="tst-sol">${q.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol>` : ''}${q.mistake ? `<p class="ins-mist">🔍 Common mistake: ${esc(q.mistake)}</p>` : ''}</div></details>`;
  }
  function viewTopic(m, tid) {
    const t = m.topics.find(x => x.id === tid); if (!t) return '<div class="card"><p class="sub">Topic not found.</p></div>';
    const wq = t.wrongQs.slice().sort((a, b) => b.w / b.s - a.w / a.s);
    return `<div class="card"><span class="tag">${SE(t.sid)} ${esc(subjName(m, t.sid))} · ${esc(t.T.ch.title)}</span><h2>${esc(t.T.title)}</h2>
        <div class="ins-trow">${bandChip(t.enough ? t.score : null)}<span>${t.score != null && t.enough ? `Strength <b>${Math.round(t.score)}</b>/100` : 'Not enough data yet'}</span></div>
        ${t.why.length ? `<span class="ins-why">${t.why.map(w => `<em class="w-${w.k}">${esc(w.txt)}</em>`).join('')}</span>` : ''}
        ${actBtns(t)}</div>
      <div class="card"><h3>How strong is this topic?</h3>
        ${compRow('Accuracy', t.comp.acc, t.ans ? `${t.ans - t.wrong} of ${t.ans} right; recent answers count more` : 'answer the quiz to measure')}
        ${compRow('Test', t.comp.test, t.test ? STATUS[t.test] : 'take a chapter test')}
        ${compRow('Confidence', t.comp.cal, t.nConf ? `${t.mis} sure-but-wrong · ${t.luck} lucky guess${t.luck === 1 ? '' : 'es'}` : 'rated in chapter tests')}
        ${compRow('Memory', t.comp.mem, t.late == null ? 'not in your Memory Garden yet' : t.late > 0 ? `review overdue by ${t.late} day${t.late > 1 ? 's' : ''}` : t.late === 0 ? 'review due today' : 'watered, review later')}
        ${t.secs ? `<p class="sub" style="margin-top:8px">⏱ ${fmtDur(t.secs)} spent in lessons${t.last ? ` · last practised ${fmtD(t.last)}` : ''}</p>` : t.last ? `<p class="sub" style="margin-top:8px">Last practised ${fmtD(t.last)}</p>` : ''}</div>
      <div class="card"><h3>❌ Questions you got wrong</h3>${wq.length ? `<p class="sub">Tap a question to see the answer and the steps.</p>${wq.map((w, i) => qCard(m, w, i)).join('')}` : '<p class="sub">No wrong answers here. 🎉</p>'}</div>`;
  }
  function viewQList(m, r) {
    /* questions answered in a time bucket / heatmap day / confidence cell, grouped by topic */
    const list = attIn(m, r.from, r.to, r.sid).filter(a => !r.cell || cellOf(a) === r.cell);
    const by = {};
    list.forEach(a => { const x = m.S.Q[a[1]]; if (!x) return; const g = by[x.T.id] = by[x.T.id] || { T: x.T, n: 0, ok: 0, wrong: {} }; g.n++; if (a[2]) g.ok++; else g.wrong[a[1]] = (g.wrong[a[1]] || 0) + 1; });
    const groups = Object.values(by).sort((a, b) => (a.ok / a.n) - (b.ok / b.n));
    const right = list.filter(a => a[2]).length;
    return `<div class="card"><h2>${esc(r.title || 'Answers')}</h2><p class="sub">${list.length ? `${list.length} answer${list.length > 1 ? 's' : ''} · ${right} right (${Math.round(right / list.length * 100)}%)` : 'No answers here.'}</p></div>
      ${groups.map(gp => `<div class="card"><button class="ins-chrow" data-go="topic" data-tid="${esc(gp.T.id)}"><span class="ins-chm"><b>${esc(gp.T.title)}</b><small>${SE(gp.T.sid)} ${esc(subjName(m, gp.T.sid))} · ${gp.ok}/${gp.n} right</small>${meter(gp.ok / gp.n * 100)}</span><span class="chgo" aria-hidden="true">›</span></button>
        ${Object.entries(gp.wrong).map(([qid, n], i) => qCard(m, { qid, w: n, s: n, last: '' }, i).replace(/Wrong \d+ of \d+ times?/, `Wrong ${n} time${n > 1 ? 's' : ''} here`)).join('')}</div>`).join('')}`;
  }
  function viewTopicList(m, r) {
    const list = r.kind === 'mastered' ? m.topics.filter(t => t.mastered).sort((a, b) => b.score - a.score) : m.topics.filter(t => t.enough).sort((a, b) => (a.score ?? 0) - (b.score ?? 0));
    return `<div class="card"><h2>${r.kind === 'mastered' ? '🏅 Topics mastered' : 'Topics'}</h2><p class="sub">${r.kind === 'mastered' ? 'Strength 80 or more, with at least 4 answers.' : ''} ${list.length} topic${list.length === 1 ? '' : 's'}.</p>
      ${list.length ? list.map(t => `<button class="ins-chrow" data-go="topic" data-tid="${esc(t.id)}"><span class="ins-chm"><b>${esc(t.T.title)}</b><small>${SE(t.sid)} ${esc(subjName(m, t.sid))} · ${pctS(t.acc)} correct</small>${meter(t.score)}</span>${bandChip(t.score)}</button>`).join('') : '<p class="sub">None yet. Keep practising!</p>'}</div>`;
  }

  /* ---------------- dashboard ---------------- */
  const DS = { range: '30', sid: '', view: {}, sort: 'score', dir: 1, tf: 'going', metric: 'acc', rows: 12 };
  function rangeStart() { return DS.range === 'all' ? '0000-00-00' : addD(today(), -(+DS.range - 1)); }
  function attIn(m, from, to, sid) {
    const f = from || '0000', t = to || '9999';
    return I.att.filter(a => a[1].startsWith(m.pre) && (!sid || a[1].startsWith(`${m.pre}${sid}-`)) && (() => { const d = dkey(a[0] * 6e4); return d >= f && d <= t; })());
  }
  const cellOf = a => !a[3] ? null : (a[2] ? (a[3] === 1 ? 'solid' : a[3] === 2 ? 'fair' : 'luck') : (a[3] === 1 ? 'mis' : 'gap'));
  function days(from) { return Object.entries(I.day).filter(([d]) => d >= from && d <= today()); }
  function chartCard(id, title, summary, svg, table, extra = '') {
    const tbl = DS.view[id] === 'table';
    return `<div class="card ins-chart" id="ic-${id}"><div class="ins-ch-top"><h3 id="ich-${id}">${title}</h3><button class="ins-tgl" data-view="${id}" aria-pressed="${tbl}">${tbl ? '📈 Chart' : '☰ Table'}</button></div>
      ${extra}<p class="ins-sum" id="ics-${id}">${summary}</p>
      <div class="ins-svgw" ${tbl ? 'hidden' : ''}>${svg}</div>
      <div class="${tbl ? 'ins-tblw' : 'sr-only'}">${table}</div></div>`;
  }
  const tableHTML = (cap, heads, rows) => `<table class="ins-tbl"><caption class="sr-only">${esc(cap)}</caption><thead><tr>${heads.map(h => `<th scope="col">${h}</th>`).join('')}</tr></thead><tbody>${rows.length ? rows.join('') : `<tr><td colspan="${heads.length}">No data yet</td></tr>`}</tbody></table>`;

  function trendData(m) {
    const from = rangeStart(), list = attIn(m, DS.range === 'all' ? null : from, null, DS.sid);
    const buckets = [];
    if (DS.range === 'all') {
      if (!list.length) return [];
      const first = dkey(list[0][0] * 6e4), span = (dnum(today()) - dnum(first)) / DAY;
      const step = span > 180 ? 30 : span > 35 ? 7 : 1;
      for (let i = Math.ceil((span + 1) / step) - 1; i >= 0; i--) { const to = addD(today(), -i * step); buckets.push({ from: addD(to, -(step - 1)), to, n: 0, ok: 0, step }); }
    } else for (let i = +DS.range - 1; i >= 0; i--) { const d = addD(today(), -i); buckets.push({ from: d, to: d, n: 0, ok: 0, step: 1 }); }
    list.forEach(a => { const d = dkey(a[0] * 6e4); const b = buckets.find(x => d >= x.from && d <= x.to); if (b) { b.n++; if (a[2]) b.ok++; } });
    return buckets;
  }
  /* bigger text sizes: narrower viewBox, so chart text grows with the Aa setting instead of shrinking with the width */
  const TF = () => ({ L: 1.12, XL: 1.25, XXL: 1.4 })[document.documentElement.dataset.ts] || 1;
  const bLabel = b => b.step === 1 ? fmtD(b.from) : `${fmtD(b.from)}–${fmtD(b.to)}`;
  function lineChart(bks) {
    const W0 = Math.round(320 / TF()), H0 = 170, L = 34, R = 12, T = 12, B = 28, pw = W0 - L - R, ph = H0 - T - B;
    const pts = bks.map((b, i) => b.n ? { b, x: L + (bks.length > 1 ? i / (bks.length - 1) : .5) * pw, y: T + ph * (1 - b.ok / b.n), v: Math.round(b.ok / b.n * 100) } : null).filter(Boolean);
    const grid = [0, 40, 60, 80, 100].map(v => `<line x1="${L}" x2="${W0 - R}" y1="${T + ph * (1 - v / 100)}" y2="${T + ph * (1 - v / 100)}" class="ins-grid${v === 0 ? ' base' : ''}"/><text x="${L - 6}" y="${T + ph * (1 - v / 100) + 4}" text-anchor="end" class="ins-ax">${v}%</text>`).join('');
    const xl = bks.length ? [0, Math.floor((bks.length - 1) / 2), bks.length - 1].filter((v, i, a) => a.indexOf(v) === i).map(i => `<text x="${L + (bks.length > 1 ? i / (bks.length - 1) : .5) * pw}" y="${H0 - 8}" text-anchor="${i === 0 && bks.length > 1 ? 'start' : i === bks.length - 1 && bks.length > 1 ? 'end' : 'middle'}" class="ins-ax">${fmtD(bks[i].from)}</text>`).join('') : '';
    const path = pts.length > 1 ? `<path d="${pts.map((p, i) => (i ? 'L' : 'M') + p.x.toFixed(1) + ',' + p.y.toFixed(1)).join(' ')}" class="ins-line"/>` : '';
    const dots = pts.map(p => `<g class="ins-hit" tabindex="0" role="button" data-q="trend" data-from="${p.b.from}" data-to="${p.b.to}" aria-label="${esc(bLabel(p.b))}: ${p.v}% correct, ${p.b.n} answers. Open"><title>${esc(bLabel(p.b))}: ${p.v}% (${p.b.n} answers)</title><circle cx="${p.x}" cy="${p.y}" r="14" class="ins-hitc"/><circle cx="${p.x}" cy="${p.y}" r="4.5" class="ins-dot"/></g>`).join('');
    return `<svg viewBox="0 0 ${W0} ${H0}" class="ins-svg" role="group" aria-label="Accuracy over time">${grid}${xl}${path}${dots}</svg>`;
  }
  function hbars(rows, unit, kind) {
    /* rows: [{label, v (0–100 or raw), txt, go:{…}}] horizontal bars, label above each bar */
    if (!rows.length) return '';
    const W0 = Math.round(320 / TF()), rh = 40, H0 = rows.length * rh + 6, max = unit === '%' ? 100 : Math.max(1, ...rows.map(r => r.v));
    return `<svg viewBox="0 0 ${W0} ${H0}" class="ins-svg" role="group" aria-label="${esc(kind)}">${rows.map((r, i) => { const y = i * rh + 4, w = Math.max(3, (W0 - 60) * (r.v || 0) / max);
      return `<g class="ins-hit" tabindex="0" role="button" ${Object.entries(r.go).map(([k, v]) => `data-${k}="${esc(v)}"`).join(' ')} aria-label="${esc(r.label)}: ${esc(r.txt)}. Open"><title>${esc(r.label)}: ${esc(r.txt)}</title>
        <rect x="0" y="${y}" width="${W0}" height="${rh - 2}" class="ins-hitr"/><text x="0" y="${y + 13}" class="ins-bl">${esc(r.label.length > Math.round(34 / TF()) ? r.label.slice(0, Math.round(33 / TF())) + '…' : r.label)}</text>
        <rect x="0" y="${y + 19}" width="${W0 - 60}" height="12" rx="4" class="ins-track"/><rect x="0" y="${y + 19}" width="${w.toFixed(1)}" height="12" rx="4" class="ins-bar" ${r.color ? `style="fill:${r.color}"` : ''}/>
        <text x="${W0}" y="${y + 30}" text-anchor="end" class="ins-bv">${esc(r.txt)}</text></g>`; }).join('')}</svg>`;
  }
  function heatmap(m) {
    const td = today(), weeks = DS.range === '7' ? 2 : DS.range === '30' ? 5 : (() => { const ds = Object.keys(I.day).filter(d => I.day[d].a || I.day[d].s || I.day[d].q).sort(); const f = ds[0] || td; return Math.max(5, Math.min(26, Math.ceil(((dnum(td) - dnum(f)) / DAY + 1) / 7) + 1)); })();
    const endDow = new Date(dnum(td)).getUTCDay(), start = addD(td, -(weeks * 7 - 1) + (6 - endDow));
    const from = rangeStart(), cs = 15, gap = 3, L = 28, T = 16, Wd = L + weeks * (cs + gap), Hd = T + 7 * (cs + gap);
    const act = d => { const x = I.day[d]; if (!x) return { v: 0, x: null }; let a = x.a, s = x.s, xp = x.x; if (DS.sid) { const sj = x.sj[DS.sid] || [0, 0, 0]; a = sj[0]; s = sj[2] || 0; xp = null; } return { v: a + Math.round(s / 60) + (DS.sid ? 0 : (x.q || 0) * 3), a, s, xp, q: x.q }; };
    const lvl = v => v <= 0 ? 0 : v < 5 ? 1 : v < 12 ? 2 : v < 25 ? 3 : 4;
    let cells = '', rows = [], activeDays = 0;
    for (let w = 0; w < weeks; w++) for (let dw = 0; dw < 7; dw++) {
      const d = addD(start, w * 7 + dw); if (d > td) continue;
      const x = act(d), inR = d >= from, l = inR ? lvl(x.v) : 0, xx = L + w * (cs + gap), yy = T + dw * (cs + gap);
      const desc = `${fmtD(d)}: ${x.a || 0} answers, ${fmtDur(x.s || 0)}${x.xp != null && x.xp ? `, ${x.xp} XP` : ''}`;
      if (inR && x.v > 0) { activeDays++; rows.push(`<tr><td>${fmtD(d)}</td><td>${x.a || 0}</td><td>${fmtDur(x.s || 0)}</td><td>${x.xp ?? '–'}</td></tr>`); }
      cells += inR && x.v > 0 ? `<g class="ins-hit" tabindex="0" role="button" data-q="day" data-from="${d}" data-to="${d}" aria-label="${esc(desc)}. Open"><title>${esc(desc)}</title><rect x="${xx}" y="${yy}" width="${cs}" height="${cs}" rx="3" class="ins-hm l${l}${d === td ? ' td' : ''}"/></g>`
        : `<rect x="${xx}" y="${yy}" width="${cs}" height="${cs}" rx="3" class="ins-hm ${inR ? 'l0' : 'out'}${d === td ? ' td' : ''}"><title>${esc(desc)}</title></rect>`;
    }
    const dl = ['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((x, i) => i % 2 ? `<text x="${L - 8}" y="${T + i * (cs + gap) + 12}" text-anchor="end" class="ins-ax">${x}</text>` : '').join('');
    const ml = []; for (let w = 0; w < weeks; w++) { const d = addD(start, w * 7); if (w === 0 || d.slice(8) <= '07') ml.push(`<text x="${L + w * (cs + gap)}" y="11" class="ins-ax">${new Date(dnum(d)).toLocaleDateString('en-IN', { month: 'short', timeZone: 'UTC' })}</text>`); }
    const svg = `<svg viewBox="0 0 ${Math.max(Wd, 140)} ${Hd}" class="ins-svg ins-hmsvg" style="max-width:${Math.max(Wd, 140) * 1.6}px" role="group" aria-label="Activity calendar">${ml.join('')}${dl}${cells}</svg>
      <div class="ins-hmkey" aria-hidden="true">Less ${[0, 1, 2, 3, 4].map(l => `<i class="ins-hm l${l}"></i>`).join('')} More</div>`;
    return { svg, rows: rows.reverse(), activeDays };
  }
  function radar(items) {
    /* items: [{label, v, go}] v = strength 0–100 */
    const f = TF(), n = items.length, W0 = Math.round(320 / f), cx = W0 / 2, R = Math.round(76 / f), cy = R + 42, H0 = 2 * R + 80;
    const pt = (i, r) => { const a = -Math.PI / 2 + i * 2 * Math.PI / n; return [cx + r * Math.cos(a), cy + r * Math.sin(a)]; };
    const ring = v => `<polygon points="${items.map((x, i) => pt(i, R * v / 100).map(z => z.toFixed(1)).join(',')).join(' ')}" class="ins-rring${v === 100 ? ' out' : ''}"/>`;
    const poly = `<polygon points="${items.map((x, i) => pt(i, R * (x.v || 0) / 100).map(z => z.toFixed(1)).join(',')).join(' ')}" class="ins-rpoly"/>`;
    const spokes = items.map((x, i) => { const [x1, y1] = pt(i, R); return `<line x1="${cx}" y1="${cy}" x2="${x1}" y2="${y1}" class="ins-grid"/>`; }).join('');
    const labels = items.map((x, i) => { const [lx, ly] = pt(i, R + 22), [px, py] = pt(i, R * (x.v || 0) / 100), anc = Math.abs(lx - cx) < 8 ? 'middle' : lx > cx ? 'start' : 'end';
      const mx = Math.round(11 / f), lab = x.label.length > mx ? x.label.slice(0, mx - 1) + '…' : x.label;
      return `<g class="ins-hit" tabindex="0" role="button" ${Object.entries(x.go).map(([k, v]) => `data-${k}="${esc(v)}"`).join(' ')} aria-label="${esc(x.label)}: strength ${x.v == null ? 'not enough data' : Math.round(x.v)}. Open"><title>${esc(x.label)}: ${x.v == null ? '–' : Math.round(x.v)}</title>
        <circle cx="${px}" cy="${py}" r="13" class="ins-hitc"/><circle cx="${px}" cy="${py}" r="4.5" class="ins-dot"/><text x="${lx}" y="${ly + 4}" text-anchor="${anc}" class="ins-bl rl">${esc(lab)}</text><text x="${lx}" y="${ly + 17}" text-anchor="${anc}" class="ins-ax">${x.v == null ? '–' : Math.round(x.v)}</text></g>`; }).join('');
    const rl = [40, 60, 80].map(v => `<text x="${cx + 3}" y="${cy - R * v / 100 - 2}" class="ins-ax sm">${v}</text>`).join('');
    return `<svg viewBox="0 0 ${W0} ${H0}" class="ins-svg" role="group" aria-label="Strength radar">${ring(100)}${ring(80)}${ring(60)}${ring(40)}${spokes}${rl}${poly}${labels}</svg>`;
  }
  const CELLS = { solid: ['😎 Sure', '✅ Right', 'Solid', 'c-solid'], fair: ['🤔 Think so', '✅ Right', 'Fairly solid', 'c-fair'], luck: ['🎲 Guess', '✅ Right', 'Lucky', 'c-luck'],
    mis: ['😎 Sure', '❌ Wrong', 'Misconception', 'c-mis'], gap: ['🤔 / 🎲', '❌ Wrong', 'Gap', 'c-gap'] };
  function matrix(cnt) {
    const cell = (k, colspan) => `<button class="ins-mx ${CELLS[k][3]}" data-q="cell" data-cell="${k}" ${cnt[k] ? '' : 'disabled'} aria-label="${CELLS[k][1].slice(2)} and ${CELLS[k][0].replace(/[^\w /]/g, '').trim()}: ${cnt[k]} answers, ${CELLS[k][2]}"${colspan ? ' style="grid-column:span 2"' : ''}><b>${cnt[k]}</b><span>${CELLS[k][2]}</span></button>`;
    return `<div class="ins-mxg" aria-hidden="false"><span></span><span class="ins-mxh">😎 Sure</span><span class="ins-mxh">🤔 Think so</span><span class="ins-mxh">🎲 Guessing</span>
      <span class="ins-mxr">✅ Right</span>${cell('solid')}${cell('fair')}${cell('luck')}
      <span class="ins-mxr">❌ Wrong</span>${cell('mis')}${cell('gap', 1)}</div>`;
  }

  function viewDash(m) {
    const from = rangeStart(), rlabel = DS.range === 'all' ? 'all time' : `last ${DS.range} days`, sid = DS.sid;
    const subsel = sid ? m.subjects.find(s => s.sid === sid) : null;
    const dd = days(from);
    const sum = k => dd.reduce((s, [, x]) => s + (sid ? ((x.sj[sid] || [])[k === 'a' ? 0 : k === 'r' ? 1 : 2] || 0) : (x[k] || 0)), 0);
    const att = attIn(m, DS.range === 'all' ? null : from, null, sid);
    let accBox; if (DS.range === 'all') { const ts = m.topics.filter(t => !sid || t.sid === sid); const a = ts.reduce((s, t) => s + t.ans, 0), w = ts.reduce((s, t) => s + t.wrong, 0); accBox = a ? (a - w) / a * 100 : null; }
    else accBox = att.length ? att.filter(a => a[2]).length / att.length * 100 : null;
    const tests = I.tl.filter(t => t.k.startsWith(m.pre) && t.d >= from && (!sid || t.k.startsWith(`${m.pre}${sid}`)));
    const mastered = m.topics.filter(t => t.mastered && (!sid || t.sid === sid)).length;
    const xpR = DS.range === 'all' && !sid ? ST.xp : sum('x');
    const box = (id, big, lbl, sub) => `<button class="ins-box" data-box="${id}"><b>${big}</b><span>${lbl}</span>${sub ? `<small>${sub}</small>` : ''}</button>`;
    const boxes = `<div class="ins-boxes">${box('xp', sid ? '–' : xpR, 'XP', sid ? 'all subjects only' : DS.range === 'all' ? 'total' : rlabel)}${box('streak', (ST.streak.n || 0) + '🔥', 'Day streak', ST.streak.last ? 'last active ' + fmtD(ST.streak.last) : '')}
      ${box('acc', pctS(accBox), 'Accuracy', rlabel)}${box('mastered', mastered, 'Topics mastered', 'strength 80+')}${box('tests', tests.length, 'Tests taken', rlabel)}${box('time', fmtDur(sum('s')), 'Active time', rlabel)}</div>`;

    /* trend */
    const bks = trendData(m), withD = bks.filter(b => b.n);
    const tSum = withD.length ? (() => { const acc = xs => { const n = xs.reduce((a, b) => a + b.n, 0); return Math.round(xs.reduce((a, b) => a + b.ok, 0) / n * 100); };
      if (withD.length < 2) return `${acc(withD)}% correct on ${bLabel(withD[0])}.`;
      const h = Math.floor(withD.length / 2), fv = acc(withD.slice(0, h)), lv = acc(withD.slice(h)), all = acc(withD);
      return `${all}% correct overall. Earlier ${fv}%, more recently ${lv}% — ${lv > fv ? `up ${lv - fv} points 📈` : lv < fv ? `down ${fv - lv} points` : 'steady'}. Tap a point to see those answers.`; })() : `No answers in the ${rlabel} yet.`;
    const trend = chartCard('trend', '📈 Accuracy over time', tSum, withD.length ? lineChart(bks) : '',
      tableHTML('Accuracy over time', ['Period', 'Answers', 'Correct'], withD.map(b => `<tr><td><button class="ins-tlink" data-q="trend" data-from="${b.from}" data-to="${b.to}">${esc(bLabel(b))}</button></td><td>${b.n}</td><td>${Math.round(b.ok / b.n * 100)}%</td></tr>`)));

    /* subject (or chapter) bars, metric switch */
    const met = DS.metric;
    const unitRows = sid ? subsel.chapters.map(c => ({ c, key: { go: 'chapter', sid, ci: c.ci }, label: `${c.ch.n}. ${c.title}`, pre: `${m.pre}${sid}-`, ci: c.ci })) : m.subjects.map(s => ({ s, key: { go: 'subject', sid: s.sid }, label: s.name, pre: `${m.pre}${s.sid}-` }));
    const qCh = {}; if (sid) subsel.chapters.forEach(c => c.topics.forEach(t => { qCh[t.id] = c.ci; }));
    const barRows = unitRows.map(u => {
      let a = 0, ok = 0, secs = 0;
      att.forEach(x => { if (!x[1].startsWith(u.pre)) return; if (sid && qCh[x[1].split('#')[0]] !== u.ci) return; a++; if (x[2]) ok++; });
      if (!sid) dd.forEach(([, x]) => { secs += ((x.sj[u.s.sid] || [])[2] || 0); }); else u.c.topics.forEach(t => { secs += t.secs; });
      const sc = sid ? u.c.score : u.s.score, en = sid ? u.c.enough : u.s.enough;
      return { u, a, acc: a ? ok / a * 100 : null, secs, sc: en ? sc : null };
    });
    const mv = r => met === 'acc' ? r.acc : met === 'time' ? r.secs : r.a;
    const mtxt = r => met === 'acc' ? (r.acc == null ? 'no answers' : `${Math.round(r.acc)}% of ${r.a}`) : met === 'time' ? fmtDur(r.secs) : `${r.a} answers`;
    const shownBars = barRows.filter(r => met === 'acc' ? r.acc != null : mv(r) > 0);
    const best = shownBars.slice().sort((a, b) => mv(b) - mv(a));
    const bSum = shownBars.length ? `${met === 'acc' ? 'Highest accuracy' : met === 'time' ? 'Most time' : 'Most answers'}: ${best[0].u.label} (${mtxt(best[0])})${best.length > 1 ? `; lowest: ${best[best.length - 1].u.label} (${mtxt(best[best.length - 1])})` : ''}.${met === 'time' && !sid ? ' Time counts lessons opened from a subject.' : ''}${met === 'time' && sid ? ' Time spent in lessons (all time).' : ''}` : `No data in the ${rlabel} yet.`;
    const metSw = `<div class="ins-seg sm" role="group" aria-label="Measure">${[['acc', 'Accuracy'], ['ans', 'Answers'], ['time', 'Time']].map(([k, n]) => `<button data-metric="${k}" aria-pressed="${met === k}" class="${met === k ? 'on' : ''}">${n}</button>`).join('')}</div>`;
    const bars = chartCard('bars', sid ? `📊 ${esc(subsel.name)}: chapters` : '📊 Subjects', bSum,
      hbars(shownBars.map(r => ({ label: r.u.label, v: met === 'acc' ? r.acc : mv(r), txt: mtxt(r), go: r.u.key, color: met === 'acc' ? (band(r.acc) || BANDS[0])[2] : null })), met === 'acc' ? '%' : '', 'Bars'),
      tableHTML(sid ? 'Chapters' : 'Subjects', [sid ? 'Chapter' : 'Subject', 'Answers', 'Accuracy', 'Time'], barRows.map(r => `<tr><td><button class="ins-tlink" ${Object.entries(r.u.key).map(([k, v]) => `data-${k}="${esc(v)}"`).join(' ')}>${esc(r.u.label)}</button></td><td>${r.a}</td><td>${pctS(r.acc)}</td><td>${fmtDur(r.secs)}</td></tr>`)), metSw);

    /* heatmap */
    const hm = heatmap(m);
    const heat = chartCard('heat', '🗓️ Activity calendar', hm.activeDays ? `You were active on ${hm.activeDays} day${hm.activeDays > 1 ? 's' : ''} in the ${rlabel}. Darker squares mean more practice.` : `No activity in the ${rlabel} yet.`, hm.svg,
      tableHTML('Active days', ['Day', 'Answers', 'Time', 'XP'], hm.rows));

    /* radar */
    const rItems = (sid ? subsel.chapters.map(c => ({ label: `${c.ch.n}. ${c.title}`, v: c.enough ? c.score : null, go: { go: 'chapter', sid, ci: c.ci } })) : m.subjects.map(s => ({ label: s.name, v: s.enough ? s.score : null, go: { go: 'subject', sid: s.sid } })));
    const rKnown = rItems.filter(x => x.v != null);
    const rad = chartCard('radar', '🕸️ Strength by ' + (sid ? 'chapter' : 'subject'),
      rKnown.length ? `Strongest: ${rKnown.slice().sort((a, b) => b.v - a.v)[0].label} (${Math.round(rKnown.slice().sort((a, b) => b.v - a.v)[0].v)}). ${rKnown.length < rItems.length ? `${rItems.length - rKnown.length} not enough data yet.` : ''}` : 'Not enough data yet. Answer a few questions in each subject.',
      rKnown.length >= 3 && rKnown.length <= 12 ? radar(rKnown) : hbars(rKnown.map(x => ({ label: x.label, v: x.v, txt: String(Math.round(x.v)), go: x.go, color: band(x.v)[2] })), '%', 'Strength'),
      tableHTML('Strength', [sid ? 'Chapter' : 'Subject', 'Strength', 'Band'], rItems.map(x => `<tr><td><button class="ins-tlink" ${Object.entries(x.go).map(([k, v]) => `data-${k}="${esc(v)}"`).join(' ')}>${esc(x.label)}</button></td><td>${x.v == null ? '–' : Math.round(x.v)}</td><td>${x.v == null ? 'Not enough data' : band(x.v)[1]}</td></tr>`)));

    /* confidence matrix */
    const cnt = { solid: 0, fair: 0, luck: 0, mis: 0, gap: 0 }; att.forEach(a => { const c = cellOf(a); if (c) cnt[c]++; });
    const rated = Object.values(cnt).reduce((a, b) => a + b, 0);
    const conf = chartCard('conf', '🎯 Confidence vs correct', rated ? `${rated} test answers rated. ${cnt.mis ? `${cnt.mis} sure-but-wrong (misconceptions) — fix these first.` : 'No sure-but-wrong answers. 👍'} ${cnt.luck ? `${cnt.luck} lucky guesses.` : ''}` : 'Take a chapter test and rate how sure you are — this grid shows what you really know.',
      matrix(cnt), tableHTML('Confidence vs correct', ['Result', 'Count'], Object.entries(cnt).map(([k, v]) => `<tr><td>${CELLS[k][1].slice(2)} · ${esc(CELLS[k][0].replace(/[^\w /]/g, '').trim())} (${CELLS[k][2]})</td><td>${v}</td></tr>`)));

    /* chapters table */
    const chs = m.chapters.filter(c => !sid || c.sid === sid).filter(c => DS.tf === 'all' || (DS.tf === 'weak' ? c.enough && ((c.score ?? 100) < 60 || c.weakN >= 2) : DS.tf === 'new' ? !c.ans && !c.done : DS.tf === 'done' ? c.done === c.n : c.ans || c.done));
    const keyF = { title: c => c.title.toLowerCase(), progress: c => c.done / c.n, acc: c => c.acc ?? (DS.dir > 0 ? 999 : -1), score: c => c.enough && c.score != null ? c.score : (DS.dir > 0 ? 999 : -1), last: c => c.last || '' }[DS.sort];
    chs.sort((a, b) => { const x = keyF(a), y = keyF(b); return (x < y ? -1 : x > y ? 1 : 0) * DS.dir; });
    const th = (k, n) => `<th scope="col" aria-sort="${DS.sort === k ? (DS.dir > 0 ? 'ascending' : 'descending') : 'none'}"><button class="ins-sort" data-sort="${k}">${n}${DS.sort === k ? (DS.dir > 0 ? ' ▲' : ' ▼') : ''}</button></th>`;
    const tbl = `<div class="card" id="ic-table"><h3>📋 Chapters</h3><div class="ins-seg sm wrap" role="group" aria-label="Show">${[['all', 'All'], ['weak', 'Weak'], ['going', 'Practised'], ['new', 'Not started'], ['done', 'Completed']].map(([k, n]) => `<button data-tf="${k}" aria-pressed="${DS.tf === k}" class="${DS.tf === k ? 'on' : ''}">${n}</button>`).join('')}</div>
      <p class="ins-sum">${chs.length} chapter${chs.length === 1 ? '' : 's'}${DS.sort === 'score' && DS.dir > 0 ? ', weakest first' : ''}. Tap a column to sort, tap a chapter to open it.</p>
      <div class="ins-tblscroll"><table class="ins-tbl ins-ctbl"><caption class="sr-only">Chapters with progress, accuracy, strength and last practised date</caption><thead><tr>${th('title', 'Chapter')}${th('progress', 'Done')}${th('acc', 'Correct')}${th('score', 'Strength')}${th('last', 'Last')}</tr></thead>
      <tbody>${chs.length ? chs.slice(0, DS.rows).map(c => `<tr><td><button class="ins-tlink" data-go="chapter" data-sid="${c.sid}" data-ci="${c.ci}">${esc(c.title)}</button>${sid ? '' : `<small>${SE(c.sid)} ${esc(subjName(m, c.sid))}</small>`}</td><td>${c.done}/${c.n}</td><td>${pctS(c.acc)}</td><td>${c.enough && c.score != null ? `<span class="ins-dotb" style="background:${band(c.score)[2]}" aria-hidden="true"></span>${Math.round(c.score)}` : '–'}</td><td>${c.last ? fmtD(c.last) : '–'}</td></tr>`).join('') : '<tr><td colspan="5">No chapters match.</td></tr>'}</tbody></table></div>${chs.length > DS.rows ? `<button class="btn ghost" data-rows="1">Show all ${chs.length} chapters ▼</button>` : ''}</div>`;

    /* test history */
    const tlist = I.tl.filter(t => t.k.startsWith(m.pre) && (!sid || t.k.startsWith(`${m.pre}${sid}`))).filter(t => t.d >= from).slice(-12).reverse();
    const tname = k => { const x = /^g\d+-([a-z]+)(?:-(\d+))?$/.exec(k); if (!x) return k; const s = m.subjects.find(z => z.sid === x[1]); return x[2] == null ? `${s ? s.name : x[1]} · mock test` : `${s ? s.name : x[1]} · ${(s && s.chapters[+x[2]] ? s.chapters[+x[2]].title : 'chapter ' + (+x[2] + 1))}`; };
    const tk = k => { const x = /^g\d+-([a-z]+)(?:-(\d+))?$/.exec(k); return x ? (x[2] == null ? `data-go="subject" data-sid="${x[1]}"` : `data-go="chapter" data-sid="${x[1]}" data-ci="${x[2]}"`) : ''; };
    const testsCard = `<div class="card" id="ic-tests"><h3>🧾 Tests</h3>${tlist.length ? `<div class="ins-tblscroll"><table class="ins-tbl"><caption class="sr-only">Test history</caption><thead><tr><th scope="col">Test</th><th scope="col">Date</th><th scope="col">Score</th><th scope="col">Ready</th></tr></thead><tbody>
      ${tlist.map(t => `<tr><td><button class="ins-tlink" ${tk(t.k)}>${esc(tname(t.k))}</button>${t.mix ? `<small>🟢${t.mix.solid} 🟡${t.mix.luck} 🟠${t.mix.gap} 🔴${t.mix.mis}</small>` : ''}</td><td>${fmtD(t.d)}</td><td>${t.pct ?? '–'}%</td><td>${t.ready ?? '–'}%</td></tr>`).join('')}</tbody></table></div>` : `<p class="sub">No tests in the ${rlabel}. Try a chapter test!</p>`}</div>`;

    const empty = !m.overall.ans && !Object.keys(I.day).some(d => I.day[d].a || I.day[d].s || I.day[d].q);
    return `<div class="card ins-dhead"><h2>📈 My dashboard</h2>
        <div class="ins-seg" role="group" aria-label="Time range">${[['7', '7 days'], ['30', '30 days'], ['all', 'All time']].map(([k, n]) => `<button data-range="${k}" aria-pressed="${DS.range === k}" class="${DS.range === k ? 'on' : ''}">${n}</button>`).join('')}</div>
        <div class="ins-seg sm wrap ins-subf" role="group" aria-label="Subject">${[['', 'All subjects'], ...m.subjects.map(s => [s.sid, `${SE(s.sid)} ${s.name}`])].map(([k, n]) => `<button data-sf="${k}" aria-pressed="${DS.sid === k}" class="${DS.sid === k ? 'on' : ''}">${esc(n)}</button>`).join('')}</div></div>
      ${empty ? '<div class="card ins-empty"><div class="gbig" aria-hidden="true">🌱</div><h3>Your dashboard is waiting</h3><p class="sub">Finish your first quest or answer a few practice questions. Your charts, streak and strengths will appear here.</p><button class="btn" id="insStart">Start a quest ▶</button></div>' : ''}
      ${boxes}${empty ? '' : trend + bars + heat + rad + conf + tbl + testsCard}`;
  }

  /* ---------------- events ---------------- */
  function goData(ds) {
    if (ds.go === 'subject') return open({ v: 'subject', sid: ds.sid });
    if (ds.go === 'chapter') return open({ v: 'chapter', sid: ds.sid, ci: +ds.ci });
    if (ds.go === 'topic') return open({ v: 'topic', tid: ds.tid });
    if (ds.go === 'analysis') return open({ v: 'analysis' });
    if (ds.go === 'dash') return open({ v: 'dash' });
  }
  function rememberY() { const r = STACK[STACK.length - 1]; if (r) r.y = window.scrollY; }
  function rerender(focusSel) { rememberY(); render().then(() => { if (focusSel) { const f = document.querySelector(focusSel); if (f) f.focus({ preventScroll: true }); } }); }
  function wire(el, m, r) {
    el.querySelectorAll('[data-go]').forEach(b => b.onclick = () => { rememberY(); goData(b.dataset); });
    el.querySelectorAll('[data-how]').forEach(b => b.onclick = howSheet);
    el.querySelectorAll('[data-more]').forEach(b => b.onclick = () => { const n0 = r.n || (r.v === 'subject' ? 5 : 10); r.n = n0 + 10; rememberY(); render().then(() => { const x = document.querySelectorAll('#s-insights .ins-imp')[n0]; if (x) { const f = x.querySelector('button'); if (f) f.focus({ preventScroll: true }); } }); });
    el.querySelectorAll('[data-act]').forEach(b => b.onclick = e => { e.stopPropagation(); rememberY(); act(m, b.dataset); });
    el.querySelectorAll('[data-q]').forEach(g => {
      const go = () => { rememberY(); const d = g.dataset;
        if (d.q === 'cell') return open({ v: 'qs', from: DS.range === 'all' ? null : rangeStart(), to: null, sid: DS.sid, cell: d.cell, title: `${CELLS[d.cell][2]}: ${CELLS[d.cell][1].slice(2)} + ${CELLS[d.cell][0].replace(/[^\w /]/g, '').trim()}` });
        open({ v: 'qs', from: d.from, to: d.to, sid: DS.sid, title: d.from === d.to ? `Answers on ${fmtD(d.from)}` : `Answers ${fmtD(d.from)}–${fmtD(d.to)}` }); };
      g.onclick = go; if (g.tagName.toLowerCase() === 'g') g.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } };
    });
    el.querySelectorAll('svg [data-go]').forEach(g => g.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); rememberY(); goData(g.dataset); } });
    if (r.v !== 'dash') return;
    el.querySelectorAll('[data-range]').forEach(b => b.onclick = () => { DS.range = b.dataset.range; rerender(`[data-range="${DS.range}"]`); });
    el.querySelectorAll('[data-sf]').forEach(b => b.onclick = () => { DS.sid = b.dataset.sf; rerender(`[data-sf="${DS.sid}"]`); });
    el.querySelectorAll('[data-metric]').forEach(b => b.onclick = () => { DS.metric = b.dataset.metric; rerender(`[data-metric="${DS.metric}"]`); });
    el.querySelectorAll('[data-view]').forEach(b => b.onclick = () => { const id = b.dataset.view; DS.view[id] = DS.view[id] === 'table' ? 'chart' : 'table'; rerender(`[data-view="${id}"]`); });
    el.querySelectorAll('[data-rows]').forEach(b => b.onclick = () => { DS.rows = 999; rerender('#ic-table tbody tr:nth-child(13) .ins-tlink'); });
    el.querySelectorAll('[data-tf]').forEach(b => b.onclick = () => { DS.tf = b.dataset.tf; DS.rows = 12; rerender(`[data-tf="${DS.tf}"]`); });
    el.querySelectorAll('[data-sort]').forEach(b => b.onclick = () => { const k = b.dataset.sort; if (DS.sort === k) DS.dir *= -1; else { DS.sort = k; DS.dir = k === 'title' ? 1 : k === 'score' || k === 'acc' ? 1 : -1; } rerender(`[data-sort="${k}"]`); });
    el.querySelectorAll('[data-box]').forEach(b => b.onclick = () => { const k = b.dataset.box;
      if (k === 'mastered') { rememberY(); return open({ v: 'list', kind: 'mastered' }); }
      const tgt = { xp: 'heat', streak: 'heat', acc: 'trend', tests: 'tests', time: 'bars' }[k];
      if (k === 'time' && DS.metric !== 'time') { DS.metric = 'time'; rememberY(); return render().then(() => scrollTo('bars')); }
      scrollTo(tgt); });
    const st = $('#insStart'); if (st) st.onclick = worldScreen;
  }
  function scrollTo(id) { const c = document.getElementById('ic-' + id); if (!c) return; c.scrollIntoView({ behavior: UX && UX.rmOn && UX.rmOn() ? 'auto' : 'smooth', block: 'start' }); c.classList.add('ins-flash'); setTimeout(() => c.classList.remove('ins-flash'), 1200); const h = c.querySelector('h3'); if (h) { h.tabIndex = -1; h.focus({ preventScroll: true }); } }

  function act(m, d) {
    const rec = d.tid ? m.topics.find(t => t.id === d.tid) : null;
    if (d.act === 'lesson' && rec) return playTopic(rec.sid, rec.ci, rec.ti);
    if (d.act === 'card' && rec && window.Tests) return Tests.showCardModal(rec.T.t, rec.sid, rec.ci, rec.ti);
    if (d.act === 'practice' && rec) return practiseTopic(rec);
    if (d.act === 'gen' && rec && window.Gen) {
      NAV = { subject: rec.sid, chapter: rec.ci, topic: rec.ti }; RUN = null;
      show('practice', 'practice'); const h = $('#s-practice'); h.innerHTML = '<button class="back" id="insGB">← My analysis</button><div id="insGen"></div>';
      $('#insGB').onclick = render; Gen.open($('#insGen'), rec.T.t, { onExit: render }); return;
    }
    if (d.act === 'sheet' && window.Tests) return Tests.sheet(d.sid, +d.ci);
    if (d.act === 'ctest' && window.Tests) return Tests.run('chapter', d.sid, +d.ci);
    if (d.act === 'chapter') return chapterScreen(d.sid, +d.ci);
  }
  function practiseTopic(rec) {
    const t = rec.T.t;
    const list = (t.quiz || []).map((q, i) => { const s = ST.qstats[`${t.id}#${i}`] || { s: 0, w: 0 }; return { q, qid: `${t.id}#${i}`, k: (s.w || 0) * 3 - (s.s || 0) * .3 + Math.random() }; })
      .sort((a, b) => b.k - a.k).slice(0, 8).map(({ q, qid }) => ({ q, qid }));
    if (!list.length) return;
    RUN = null; show('practice', 'practice');
    const h = $('#s-practice'); h.innerHTML = '<div id="pBody"></div>';
    quizRunner($('#pBody'), list, r => {
      bumpStreak(); sfx(r.right / r.total >= .7 ? 'unlock' : 'hmm');
      $('#pBody').innerHTML = `<div class="card done-card"><div class="gbig">${r.right === r.total ? '🌟' : '💪'}</div><h2>${esc(t.title)}</h2><p class="sub">${r.right} of ${r.total} correct</p>
        <button class="btn" id="insPA">🔁 Practise again</button><div style="height:8px"></div><button class="btn ghost" id="insPB">Back to my analysis</button></div>`;
      $('#insPA').onclick = () => model().then(mm => practiseTopic(mm.topics.find(x => x.id === rec.id) || rec));
      $('#insPB').onclick = () => render();
    });
  }

  /* ---------------- "How is this calculated?" ---------------- */
  function howSheet() {
    let s = document.getElementById('insHow');
    if (!s) {
      document.body.insertAdjacentHTML('beforeend', `<div class="sheet" id="insHow" role="dialog" aria-modal="true" aria-labelledby="insHowT"><div class="sheet-in ins-howin"><div class="sheet-grab"></div>
        <h2 id="insHowT"><span aria-hidden="true">ⓘ</span> How is my strength calculated?</h2>
        <p class="sub">Every topic gets a score from 0 to 100. It mixes four things:</p>
        <ol class="ins-howl">
          <li><b>Right answers (half the score).</b> How many quiz, practice and test answers you got right. Answers from the last few weeks count more than old ones.</li>
          <li><b>Tests (one fifth).</b> Your latest chapter or mock test for that topic: understood is best, a lucky guess counts half, a mistake counts little.</li>
          <li><b>Being honest about how sure you are.</b> In tests, being "sure" but wrong, or getting it right by guessing, lowers the score a little.</li>
          <li><b>Memory.</b> Topics you revise on time in the Memory Garden stay strong. If a revision is late, the score drops a bit each day.</li></ol>
        <p class="sub">A <b>subject</b> score is the average of its topics, plus a little extra for how much of the subject you have covered. The <b>overall</b> score averages your subjects.</p>
        ${legend()}<p class="sub">Under 40 = Very weak · 40–59 = Weak · 60–79 = Strong · 80 and above = Very strong.</p>
        <p class="sub">You need at least ${MIN_SUBJ} answers in a subject (or one test) before its gauge shows a score.</p>
        <button class="btn ghost" data-close="1" id="insHowX">Close</button></div></div>`);
      s = document.getElementById('insHow');
      $('#insHowX').onclick = () => s.classList.remove('show');
      s.addEventListener('click', e => { if (e.target === s) s.classList.remove('show'); });
    }
    s.classList.add('show');
  }

  /* ---------------- adapter: model → generic dashboard data (see the API notes at the top) ---------------- */
  const DASH_HOST = document.createElement('div'); DASH_HOST.className = 'ins-dashhost';
  const DD = new WeakMap();
  function dashData(m) {
    if (DD.has(m)) return DD.get(m);
    const g = m.g, td = today(), yd = addD(td, -1);
    const tree = m.subjects.map(s => ({ id: s.sid, name: s.name, score: s.enough ? s.score : null, enough: !!(s.enough && s.score != null),
      children: s.chapters.map(c => ({ id: `${s.sid}:${c.ci}`, name: `${c.ch.n}. ${c.title}`, score: c.enough ? c.score : null, enough: !!(c.enough && c.score != null),
        children: c.topics.map(t => { const qs = {}; for (let k = 0; k < t.T.qn; k++) { const x = m.S.Q[`${t.id}#${k}`]; if (x && x.q) qs[`${t.id}#${k}`] = { q: x.q.q, a: (x.q.options || [])[x.q.answer], explain: x.q.explain }; }
          return { id: t.id, name: t.T.title, score: t.enough ? t.score : null, enough: !!(t.enough && t.score != null), questions: qs }; }) })) }));
    const events = [];
    I.att.forEach(a => { const x = m.S.Q[a[1]]; if (!x) return; events.push({ t: a[0] * 6e4, path: [x.T.sid, `${x.T.sid}:${x.T.ci}`, x.T.id], qid: a[1], ok: a[2], conf: a[3] }); });
    const days = {}; Object.entries(I.day).forEach(([d, v]) => { const by = {}; Object.entries(v.sj || {}).forEach(([sid, a]) => { if (a[2]) by[sid] = a[2]; }); days[d] = { secs: v.s || 0, xp: v.x || 0, a: v.a || 0, by }; });
    const tests = I.tl.filter(t => t.k.startsWith(m.pre)).map(t => { const x = /^g\d+-([a-z]+)(?:-(\d+))?$/.exec(t.k); if (!x) return null; const s = m.subjects.find(z => z.sid === x[1]); if (!s) return null;
      const ch = x[2] != null ? s.chapters[+x[2]] : null;
      return { d: t.d, t: t.ts, pct: t.pct, name: ch ? `${s.name} · ${ch.title}` : `${s.name} · mock test`, path: ch ? [s.sid, `${s.sid}:${ch.ci}`] : [s.sid] }; }).filter(t => t && t.pct != null);
    const data = { title: 'My dashboard', subtitle: `Grade ${g} · ${ST.profile.name || ''}`.replace(/ · $/, ''), rootName: 'All subjects', levels: ['Subject', 'Chapter', 'Topic'],
      tree, events, days, tests, testLabel: 'Test scores', overall: { score: m.overall.enough ? m.overall.score : null },
      streak: { n: ST.streak && (ST.streak.last === td || ST.streak.last === yd) ? ST.streak.n || 0 : 0 }, minEvents: MIN_ALL, answered: m.overall.ans };
    DD.set(m, data); return data;
  }
  function dashTile(where) {
    const id = where === 'world' ? 'insHome' : 'meDash';
    return model().then(m => { const box = document.getElementById(id); if (!box || !window.SVDash) return;
      box.innerHTML = SVDash.tile(dashData(m), { label: 'Dashboard' });
      const b = box.querySelector('[data-dk-open]'); if (b) b.onclick = () => { try { sfx('open'); } catch (e) {} root({ v: 'dash', from: where }); }; }).catch(e => console.error(e));
  }

  /* ---------------- Me screen + home shortcut ---------------- */
  const _me = meScreen;
  meScreen = function () {
    _me();
    const meEl = document.querySelector('#s-me'); if (!meEl || !ST.profile) return;
    /* Dashboard + My analysis live only in the centre 📊 Dashboard tab now (owner's request) */
    document.getElementById('anCard')?.remove(); document.getElementById('meDash')?.remove(); document.getElementById('insCard')?.remove();
  };
  const _world = worldScreen;
  worldScreen = async function () { await _world(); document.getElementById('insHome')?.remove(); };

  window.Insights = { conf, model, open: r => root(r), dashboard: o => root({ v: 'dash', from: 'world', tab: !!(o && o.tab) }),
    dashboardFor: (hostEl, opts) => window.SVDash ? SVDash.render(hostEl, Object.assign({ mode: 'ca' }, opts || {})) : null,
    dashboardTile: (data, o) => window.SVDash ? SVDash.tile(data, o) : '', dashData: () => model().then(dashData), analysis: () => root({ v: 'analysis' }), _ds: DS, _band: band };
})();
