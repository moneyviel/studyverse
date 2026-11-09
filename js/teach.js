/* ================= StudyVerse Teacher dashboard (Schools & Coaching) =================
   Opened from the school console (js/inst.js). One full-screen page (.sheet.pv-hub, like Parent Hub):
   class list → class page with tabs Overview · Students · Insights · Homework · Leaderboard · Reports, and a
   per-student page with the SAME cards as Parent Hub (window.Parent.lib — js/parent.js, unchanged analysis).
   Data: rpc class_progress(class) → every student's synced progress (studyverse.progress.state.st), homework and
   completions; rpc class_leaderboard (opt-in, first names). Nothing is invented: every number comes from synced progress.
   Pure maths lives in Teach.lib (metrics → classInsights) so it is unit-tested with hand-checked fixtures.
   Labels like "Need attention" are for teachers only; students never see them. */
(function () {
  'use strict';
  const D = document, DAY = 864e5;
  const P = () => (window.Parent && Parent.lib) || null;
  const C = () => window.Cloud || null;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const say = m => { try { toast(m); } catch (e) {} };
  const one = r => Array.isArray(r) ? r[0] : r;
  const rpc = (n, b) => C().rest('rpc/' + n, { method: 'POST', body: b || {} });
  const pct = (r, a) => a ? r / a * 100 : null;
  const pctS = v => v == null ? '–' : Math.round(v) + '%';
  const median = a => { if (!a.length) return null; const b = a.slice().sort((x, y) => x - y), m = b.length >> 1; return b.length % 2 ? b[m] : (b[m - 1] + b[m]) / 2; };
  const mean = a => a.length ? a.reduce((x, y) => x + y, 0) / a.length : null;
  const fmtMin = m => { m = Math.round(m || 0); return m < 60 ? `${m} min` : `${Math.floor(m / 60)} h${m % 60 ? ' ' + (m % 60) + ' min' : ''}`; };
  const first = n => String(n || 'Student').trim().split(/\s+/)[0];
  const pad2 = n => String(n).padStart(2, '0');
  const dk = t => { const d = new Date(t); return `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`; };
  const todayK = () => dk(Date.now());
  const fmtDate = k => new Date(k + 'T12:00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });

  /* ================= metrics for one student (from synced ST, via Parent Hub's analysis) ================= */
  async function metrics(row, homework) {
    const L = P(), k = { name: row.name, state: row.state ? { st: row.state } : null, controls: {} };
    const A = await L.analyse(k), X = A.has ? await L.deep(A) : null, R = X ? L.readinessOf(A, X, {}) : null;
    const M = { id: row.user_id, name: row.name || 'Student', first: first(row.name), roll: row.roll_no || '', parents: +row.parents || 0, updated_at: row.updated_at, has: A.has, A, X, R };
    const today = todayK(), hwRows = Array.isArray(homework) ? homework : [], done = row.hw || {};
    const due = hwRows.filter(h => h.due_date <= today || done[h.id]);
    M.hw = { assigned: due.length, done: due.filter(h => done[h.id]).length, missed: hwRows.filter(h => h.due_date < today && !done[h.id]).map(h => h.title) };
    if (!A.has) return Object.assign(M, { m7: 0, mP7: 0, m14: 0, mP14: 0, a7: 0, r7: 0, aP7: 0, rP7: 0, a14: 0, r14: 0, aP14: 0, rP14: 0, active14: 0, sinceDays: null, prevRun: 0, todayActive: false, careless: 0, concept: 0, readiness: null, chapters: {}, tod: [] });
    const s = A.s, d28 = L.daysBack(28), l7 = d28.slice(21), p7 = d28.slice(14, 21), l14 = d28.slice(14), p14 = d28.slice(0, 14);
    const mins = ds => ds.reduce((t, d) => t + L.minutesOn(s, d), 0);
    const ans = ds => ds.reduce((o, d) => { const x = L.answersOn(s, d, A._caDays); o.a += x.a; o.r += x.r; return o; }, { a: 0, r: 0 });
    const w7 = ans(l7), wp7 = ans(p7), w14 = ans(l14), wp14 = ans(p14);
    let prevRun = 0;
    if (A.lastDay) { const end = new Date(A.lastDay + 'T12:00:00').getTime(); for (let i = 0; i < 7; i++) if (A._active(dk(end - i * DAY))) prevRun++; }
    const chapters = {};
    (X.mastery ? X.mastery.all : []).forEach(x => { chapters[x.id] = { n: x.n, acc: x.acc, st: x.st, title: x.title, sub: x.sub }; });
    return Object.assign(M, { m7: mins(l7), mP7: mins(p7), m14: mins(l14), mP14: mins(p14), a7: w7.a, r7: w7.r, aP7: wp7.a, rP7: wp7.r, a14: w14.a, r14: w14.r, aP14: wp14.a, rP14: wp14.r,
      active14: l14.filter(A._active).length, sinceDays: A.sinceDays, prevRun, todayActive: A._active(today),
      careless: X.mist.careless, concept: X.mist.concept, readiness: R ? R.score : null, chapters, tod: X.time.rows, written: X.writes && X.writes.n ? X.writes.avg : null });
  }

  /* ================= class insights: pure, from metrics only =================
     Effort vs Results: students with 10+ answers in the last 14 days. Effort is high when time in the last 14 days is at
       least the class median (and never below 30 min); results are good at 70%+ correct in those 14 days.
     Early warning: time this week under half of last week (last week 30+ min) · accuracy down 15+ points (10+ answers each
       week) · homework past its due date not done · regular studier (4+ of 7 days) now 2+ days without study.
     Rising stars: accuracy up 5+ points, last 14 days vs the 14 before (10+ answers each).
     Learning gaps: a chapter where 3+ students have 4+ answers and at least half of them are under 60%.
     Peer tutors: same class; tutor 85%+ in 8+ answers, learner under 60% in 4+ answers; each student in one pair at most.
     Consistency = active days in the last 14 ÷ 14. Readiness bands as Parent Hub: 80+ ready, 60–79 getting there. */
  function classInsights(Ms, opt = {}) {
    const O = {}, has = Ms.filter(m => m.has);
    const a7 = Ms.reduce((t, m) => t + m.a7, 0), r7 = Ms.reduce((t, m) => t + m.r7, 0);
    const hwA = Ms.reduce((t, m) => t + m.hw.assigned, 0), hwD = Ms.reduce((t, m) => t + m.hw.done, 0);
    const rd = Ms.map(m => m.readiness).filter(v => v != null);
    O.overview = { n: Ms.length, withData: has.length, activeToday: Ms.filter(m => m.todayActive).length, activeWeek: Ms.filter(m => m.m7 >= 1 || m.a7 > 0).length,
      acc7: pct(r7, a7), answers7: a7, avgMin7: Ms.length ? Ms.reduce((t, m) => t + m.m7, 0) / Ms.length : 0, avgReadiness: rd.length ? mean(rd) : null, hwRate: hwA ? hwD / hwA * 100 : null, hwAssigned: hwA, hwDone: hwD,
      avgCons: Ms.length ? mean(Ms.map(m => m.active14 / 14 * 100)) : null };
    // quadrants
    const elig = has.filter(m => m.a14 >= 10), cut = Math.max(30, median(elig.map(m => m.m14)) || 0);
    O.quad = { cut, star: [], hard: [], coast: [], risk: [], nodata: Ms.filter(m => !elig.includes(m)) };
    elig.forEach(m => { const hi = m.m14 >= cut, good = pct(m.r14, m.a14) >= 70; O.quad[hi ? (good ? 'star' : 'hard') : (good ? 'coast' : 'risk')].push(m); });
    // early warning
    O.warn = [];
    Ms.forEach(m => {
      const why = [], acc = pct(m.r7, m.a7), accP = pct(m.rP7, m.aP7);
      if (m.mP7 >= 30 && m.m7 < m.mP7 * 0.5) why.push(['time', `Study time fell from ${fmtMin(m.mP7)} last week to ${fmtMin(m.m7)} this week.`]);
      if (m.a7 >= 10 && m.aP7 >= 10 && accP - acc >= 15) why.push(['acc', `Accuracy fell from ${pctS(accP)} to ${pctS(acc)}.`]);
      if (m.hw.missed.length) why.push(['hw', `Missed homework: ${m.hw.missed.slice(0, 2).map(t => '“' + t + '”').join(', ')}${m.hw.missed.length > 2 ? ` and ${m.hw.missed.length - 2} more` : ''}.`]);
      if (m.sinceDays != null && m.sinceDays >= 2 && m.prevRun >= 4) why.push(['streak', `Was studying regularly, but no study for ${m.sinceDays} days.`]);
      if (!why.length) return;
      const k = why.map(w => w[0]);
      const act = k.includes('hw') ? 'Have a short, friendly check-in about the homework and agree a smaller first step.'
        : k.includes('acc') ? 'Re-teach the weak chapter in a 5-minute 1-to-1, or pair with a peer tutor below.'
        : 'Send a friendly nudge; if a parent is linked, they see the same dip in Parent Hub.';
      O.warn.push({ m, why, action: act });
    });
    O.warn.sort((a, b) => b.why.length - a.why.length || a.m.name.localeCompare(b.m.name));
    // rising stars
    O.rising = has.filter(m => m.a14 >= 10 && m.aP14 >= 10).map(m => ({ m, before: pct(m.rP14, m.aP14), now: pct(m.r14, m.a14) }))
      .filter(x => x.now - x.before >= 5).sort((a, b) => (b.now - b.before) - (a.now - a.before) || a.m.name.localeCompare(b.m.name)).slice(0, 3);
    // learning gaps (chapters / units)
    const ch = {};
    Ms.forEach(m => Object.entries(m.chapters || {}).forEach(([id, c]) => { if (c.n >= 4 && c.acc != null) { const g = ch[id] || (ch[id] = { id, title: c.title, sub: c.sub, att: [], weak: [] }); g.att.push({ m, c }); if (c.acc < 60) g.weak.push({ m, c }); } }));
    O.gaps = Object.values(ch).filter(g => g.att.length >= 3 && g.weak.length / g.att.length >= 0.5)
      .map(g => Object.assign(g, { pct: g.weak.length / g.att.length * 100, avg: mean(g.att.map(x => x.c.acc)) })).sort((a, b) => b.pct - a.pct || b.weak.length - a.weak.length || a.avg - b.avg).slice(0, 8);
    // peer tutors: gap chapters first, then any chapter
    const used = new Set(), pairs = [], order = O.gaps.map(g => g.id).concat(Object.keys(ch).filter(id => !O.gaps.some(g => g.id === id)).sort());
    order.forEach(id => {
      const all = Ms.map(m => ({ m, c: (m.chapters || {})[id] })).filter(x => x.c && x.c.acc != null);
      const strong = all.filter(x => x.c.n >= 8 && x.c.acc >= 85).sort((a, b) => b.c.acc - a.c.acc || a.m.name.localeCompare(b.m.name));
      const help = all.filter(x => x.c.n >= 4 && x.c.acc < 60).sort((a, b) => a.c.acc - b.c.acc || a.m.name.localeCompare(b.m.name));
      for (const t of strong) { if (pairs.length >= 8) break; if (used.has(t.m.id)) continue; const l = help.find(h => !used.has(h.m.id) && h.m.id !== t.m.id); if (!l) break;
        used.add(t.m.id); used.add(l.m.id); pairs.push({ id, title: t.c.title, sub: t.c.sub, tutor: t.m, tacc: t.c.acc, learner: l.m, lacc: l.c.acc }); }
    });
    O.pairs = pairs;
    // readiness distribution
    O.ready = { ready: 0, getting: 0, needs: 0, none: 0 };
    Ms.forEach(m => { const v = m.readiness; O.ready[v == null ? 'none' : v >= 80 ? 'ready' : v >= 60 ? 'getting' : 'needs']++; });
    // time of day
    const B = (P() && P().BUCKETS) || [['morning', 'Morning', '5 am–12 noon'], ['afternoon', 'Afternoon', '12–5 pm'], ['evening', 'Evening', '5–9 pm'], ['night', 'Night', '9 pm–5 am']];
    O.tod = B.map(([key, name, range]) => { let a = 0, r = 0, who = 0; Ms.forEach(m => { const x = (m.tod || []).find(t => t.key === key); if (x && x.a) { a += x.a; r += x.r; who++; } }); return { key, name, range, a, r, who, acc: pct(r, a) }; });
    O.todBest = O.tod.filter(t => t.a >= 20).sort((a, b) => b.acc - a.acc || b.a - a.a)[0] || null;
    // per-student tables
    O.rows = Ms.map(m => ({ m, cons: Math.round(m.active14 / 14 * 100), acc7: pct(m.r7, m.a7), mist: m.careless + m.concept, carelessPct: m.careless + m.concept ? Math.round(m.careless / (m.careless + m.concept) * 100) : null,
      hwRate: m.hw.assigned ? Math.round(m.hw.done / m.hw.assigned * 100) : null }));
    return O;
  }

  /* compare classes / sections (admin): one overview row per class */
  function compare(list) { return list.map(({ cls, Ms }) => Object.assign({ cls }, classInsights(Ms).overview)); }

  function toCSV(cls, Ms, O) {
    const q = v => { const s = v == null ? '' : String(v); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
    const quad = id => ['star', 'hard', 'coast', 'risk'].find(k => O.quad[k].some(m => m.id === id)) || 'not enough data';
    const QN = { star: 'Star', hard: 'Working hard - needs help', coast: 'Coasting talent', risk: 'Needs attention' };
    const head = ['Roll', 'Name', 'Minutes this week', 'Minutes last week', 'Questions this week', 'Correct % this week', 'Active days (14)', 'Consistency %', 'Readiness', 'Careless slips', 'Concept gaps', 'Homework done', 'Homework set', 'Parents linked', 'Group'];
    const rows = O.rows.map(({ m, cons, acc7 }) => [m.roll, m.name, Math.round(m.m7), Math.round(m.mP7), m.a7, acc7 == null ? '' : Math.round(acc7), m.active14, cons, m.readiness == null ? '' : m.readiness, m.careless, m.concept, m.hw.done, m.hw.assigned, m.parents, QN[quad(m.id)] || quad(m.id)]);
    return [['Class', cls.name], ['Exported', new Date().toISOString().slice(0, 10)], [], head, ...rows].map(r => r.map(q).join(',')).join('\r\n');
  }

  /* ================= UI ================= */
  let hub = null, classes = [], cur = null, data = null, Ms = [], O = null, tab = 'overview', back = null, inst = null, loading = 0, subj = '';
  const QL = { star: ['⭐ Stars', 'Lots of practice and good results. Give stretch work.'], coast: ['🌱 Coasting talents', 'Good results with little practice. A challenge goal keeps them growing.'],
    hard: ['💪 Working hard — need help', 'Putting in time but results are low. Re-teach the concept; effort is there.'], risk: ['🔔 Need attention', 'Little practice and low results. A check-in and a small daily target help most.'] };

  function css() { if (window.Inst && Inst.style) Inst.style(); else if (P()) P().style(); }
  function open(list, opt = {}) {
    if (!C() || !C().signedIn()) return;
    css(); if (P()) P().style();
    classes = (list || []).slice(); inst = opt.inst || null; back = opt.back || null;
    if (!hub) { hub = D.createElement('div'); hub.className = 'sheet pv-hub in-hub'; hub.id = 'tcHub'; hub.setAttribute('role', 'dialog'); hub.setAttribute('aria-modal', 'true'); hub.setAttribute('aria-labelledby', 'tcT'); D.body.appendChild(hub); }
    hub.toggleAttribute('data-pinned', !!opt.pinned); hub.toggleAttribute('data-nonav', !!opt.pinned);
    hub.classList.add('show'); hub.scrollTop = 0;
    if (opt.classId) { const c = classes.find(x => x.id === opt.classId); if (c) return openClass(c); }
    if (classes.length === 1 && !opt.list) return openClass(classes[0]);
    listView();
  }
  function close() { if (hub) hub.classList.remove('show'); if (back) back(); }
  function frame(title, body, onBack, backLabel) {
    hub.innerHTML = `<div class="pv-wrap"><div class="pv-top"><button class="pv-back" type="button" id="tcBack">${esc(backLabel || '← Back')}</button><h1 id="tcT">${title}</h1><button class="pv-ref" type="button" id="tcRef" aria-label="Refresh">⟳</button></div>${body}</div>`;
    hub.querySelector('#tcBack').onclick = onBack || close;
    hub.scrollTop = 0;
  }
  function listView() {
    cur = null;
    frame('🧑‍🏫 My classes', `<div class="pv-body">${classes.length ? classes.map((c, i) => `<button class="pv-card in-cls" type="button" data-i="${i}"><b>${esc(c.name)}</b><span class="pv-mut">${/^ca-/.test(c.course) ? 'CA Foundation batch' : 'Class ' + esc(c.grade)}${c.inst ? ' · ' + esc(c.inst) : ''}</span><span class="in-go" aria-hidden="true">›</span></button>`).join('')
      : '<div class="pv-card"><h2>No classes yet</h2><p>Ask your school admin to add you to a class.</p></div>'}</div>`, close, back ? '← Console' : '✕ Close');
    hub.querySelector('#tcRef').onclick = listView;
    hub.querySelectorAll('[data-i]').forEach(b => b.onclick = () => openClass(classes[+b.dataset.i]));
  }
  async function load(c) {
    const r = one(await rpc('class_progress', { p_class: c.id }));
    if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not load the class.');
    return r;
  }
  async function openClass(c, keepTab) {
    cur = c; if (!keepTab) { tab = 'overview'; subj = ''; }
    const my = ++loading;
    frame(esc(c.name), '<p class="pv-load" role="status">Loading the class…</p>', classes.length > 1 ? listView : close, classes.length > 1 ? '← Classes' : (back ? '← Console' : '✕ Close'));
    try {
      data = await load(c);
      const rows = data.students || [];
      Ms = []; for (const r of rows) Ms.push(await metrics(r, data.homework));
      if (my !== loading) return;
      O = classInsights(Ms);
      render();
    } catch (e) {
      if (my !== loading) return;
      hub.querySelector('.pv-wrap').insertAdjacentHTML('beforeend', `<div class="pv-card"><h2>Could not load</h2><p>${esc(e.status != null ? C().errText(e) : e.message)}</p><button class="pv-btn" type="button" id="tcRetry">Try again</button></div>`);
      hub.querySelector('.pv-load') && hub.querySelector('.pv-load').remove();
      hub.querySelector('#tcRetry').onclick = () => openClass(c, true);
    }
  }
  const TABS = [['overview', 'Overview'], ['students', 'Students'], ['insights', 'Insights'], ['homework', 'Homework'], ['board', 'Leaderboard'], ['reports', 'Reports']];
  const isCA = () => !!(cur && /^ca-/.test(cur.course));
  function render() {
    const c = cur, sch = data.institution ? data.institution.name : '';
    frame(`<span>${esc(c.name)}</span><small class="in-sub">${esc(sch)} · ${Ms.length} student${Ms.length === 1 ? '' : 's'}</small>`,
      `<div class="pv-tabs in-tabs" role="tablist" aria-label="Class sections">${TABS.map(([k, n]) => `<button type="button" role="tab" id="tct-${k}" aria-controls="tcBody" aria-selected="${k === tab}" class="pv-tab${k === tab ? ' on' : ''}" data-tab="${k}">${n}</button>`).join('')}</div>
       <div id="tcBody" class="pv-body" role="tabpanel" aria-labelledby="tct-${tab}"></div>`, classes.length > 1 ? listView : close, classes.length > 1 ? '← Classes' : (back ? '← Console' : '✕ Close'));
    hub.querySelector('#tcRef').onclick = () => openClass(c, true);
    hub.querySelectorAll('[data-tab]').forEach(b => b.onclick = () => { tab = b.dataset.tab; render(); const t = hub.querySelector('#tct-' + tab); if (t) t.focus(); });
    const body = hub.querySelector('#tcBody');
    if (!Ms.length && tab !== 'homework' && tab !== 'reports') { body.innerHTML = `<div class="pv-card"><h2>No students yet</h2><p>Share the class join code, or ask the admin to upload the student list.</p></div>`; return; }
    ({ overview, students, insights, homework, board: leaderboard, reports })[tab](body);
  }

  /* ---------- Overview ---------- */
  function kpi(v, l) { return `<div><b>${v}</b><span>${l}</span></div>`; }
  function overview(body) {
    const v = O.overview, R = O.ready, tot = Ms.length || 1;
    const bar = (n, cls, lab) => n ? `<i class="${cls}" style="width:${n / tot * 100}%" title="${lab}: ${n}"></i>` : '';
    body.innerHTML = `<section class="pv-card" aria-labelledby="tcOv"><h3 id="tcOv">Today and this week</h3>
        <div class="pv-kpis">${kpi(`${v.activeToday}/${v.n}`, 'Active today')}${kpi(`${v.activeWeek}/${v.n}`, 'Active this week')}${kpi(pctS(v.acc7), `Average correct<br><small>${v.answers7} answers</small>`)}
          ${kpi(fmtMin(v.avgMin7), 'Average time<br>per student this week')}${kpi(v.avgReadiness == null ? '–' : Math.round(v.avgReadiness), 'Average readiness<br><small>out of 100</small>')}${kpi(pctS(v.hwRate), `Homework done<br><small>${v.hwDone} of ${v.hwAssigned}</small>`)}</div>
        <p class="pv-note">Only students who have used the app while signed in show data (${v.withData} of ${v.n}).</p></section>
      <section class="pv-card" aria-labelledby="tcRd"><h3 id="tcRd">🎓 Exam readiness of the class</h3>
        <div class="in-dist" role="img" aria-label="Ready ${R.ready}, getting there ${R.getting}, needs work ${R.needs}, no data ${R.none}">${bar(R.ready, 'ok', 'Ready')}${bar(R.getting, 'warn', 'Getting there')}${bar(R.needs, 'bad', 'Needs work')}${bar(R.none, 'none', 'No data')}</div>
        <ul class="pv-leg"><li><i class="pv-sw sq in-ok"></i>Ready (80+) <b id="tcRdR">${R.ready}</b></li><li><i class="pv-sw sq in-warn"></i>Getting there (60–79) <b>${R.getting}</b></li><li><i class="pv-sw sq in-bad"></i>Needs work (under 60) <b>${R.needs}</b></li><li><i class="pv-sw sq in-none"></i>No data <b>${R.none}</b></li></ul>
        <p class="pv-note">Same score as Parent Hub: 40% syllabus covered + 35% accuracy + 15% consistency + 10% recency.</p></section>
      ${gapsHTML(5)}${todHTML()}`;
    wireNames(body);
  }
  function gapsHTML(n) {
    return `<section class="pv-card" aria-labelledby="tcGp"><h3 id="tcGp">📌 Weak topics for the class (learning gaps)</h3>
      ${O.gaps.length ? `<ul class="pv-list" id="tcGaps">${O.gaps.slice(0, n).map(g => `<li><b>${esc(g.title)}</b>${g.sub ? ` <span class="pv-mut">${esc(g.sub)}</span>` : ''}<br>
        <span class="pv-st bad">${g.weak.length} of ${g.att.length} under 60%</span> <span class="pv-mut">class average ${pctS(g.avg)}</span><br><span class="pv-mut">💡 Re-teach this ${isCA() ? 'unit' : 'chapter'} in class, then set it as homework.</span></li>`).join('')}</ul>`
        : '<p class="pv-empty">No chapter where most of the class is weak. 🎉 (Shows when 3+ students have 4+ answers in a chapter.)</p>'}</section>`;
  }
  function todHTML() {
    const max = Math.max(1, ...O.tod.map(t => t.a));
    return `<section class="pv-card" aria-labelledby="tcTd"><h3 id="tcTd">⏰ When the class studies</h3>
      ${O.todBest ? `<p id="tcTdBest">Best results in the <b>${esc(O.todBest.name)}</b> (${esc(O.todBest.range)}): ${pctS(O.todBest.acc)} correct.</p>` : '<p class="pv-mut">Not enough answers yet to compare times of day.</p>'}
      <ul class="pv-list pv-tod">${O.tod.map(t => `<li><span class="pv-gt"><b>${esc(t.name)}</b><span class="pv-mut">${esc(t.range)}</span></span><span class="pv-sbar" aria-hidden="true"><i style="width:${Math.round(t.a / max * 100)}%"></i></span>
        <span class="pv-todv">${t.a ? `${pctS(t.acc)} correct<br><small>${t.a} answers · ${t.who} student${t.who === 1 ? '' : 's'}</small>` : '<small>no answers</small>'}</span></li>`).join('')}</ul><p class="pv-note">Last 60 days.</p></section>`;
  }
  const nameBtn = m => `<button type="button" class="in-name" data-sid="${esc(m.id)}">${esc(m.name)}</button>`;
  function wireNames(root) { root.querySelectorAll('[data-sid]').forEach(b => b.onclick = () => student(Ms.find(m => m.id === b.dataset.sid))); }

  /* ---------- Students: heatmap + list ---------- */
  function students(body) {
    const groups = (Ms.find(m => m.X && m.X.mastery) || {}).X;
    const G = groups ? groups.mastery.groups : [];
    if (!subj && G[0]) subj = G.slice().sort((a, b) => b.started - a.started)[0].name;
    const g = G.find(x => x.name === subj) || G[0];
    const MS = P().MST, items = g ? g.items : [];
    const cell = (m, it) => { const c = (m.chapters || {})[it.id]; const st = c ? c.st : 0, acc = c && c.acc != null ? Math.round(c.acc) : null;
      return `<td class="in-hc ${MS[st][1]}" title="${esc(m.name)} — ${esc(it.title)}: ${MS[st][0]}${acc != null ? `, ${acc}%` : ''}"><span aria-hidden="true">${MS[st][2]}</span><span class="sr-only">${MS[st][0]}${acc != null ? `, ${acc}% correct` : ''}</span></td>`; };
    body.innerHTML = `<section class="pv-card in-wide" aria-labelledby="tcHm"><h3 id="tcHm">🗺️ Mastery heatmap</h3>
      ${G.length ? `<label for="tcSubj" class="in-lbl">${isCA() ? 'Paper' : 'Subject'}</label><select id="tcSubj" class="pv-in">${G.map(x => `<option${x === g ? ' selected' : ''}>${esc(x.name)}</option>`).join('')}</select>
      <ul class="pv-leg pv-mleg">${MS.map(([n, cls, ic]) => `<li><span class="pv-chip ${cls} mini" aria-hidden="true">${ic}</span>${n}</li>`).join('')}</ul>
      <div class="in-hscroll" tabindex="0" role="region" aria-label="Heatmap, scrolls sideways"><table class="in-heat" id="tcHeat"><caption class="sr-only">Mastery by student and ${isCA() ? 'unit' : 'chapter'}</caption>
        <thead><tr><th scope="col">Student</th>${items.map((it, i) => `<th scope="col" title="${esc(it.title)}"><span>${isCA() ? 'U' : 'Ch'}${i + 1}</span></th>`).join('')}</tr></thead>
        <tbody>${Ms.map(m => `<tr><th scope="row">${nameBtn(m)}</th>${items.map(it => cell(m, it)).join('')}</tr>`).join('')}</tbody></table></div>
      <details class="pv-tbl"><summary>${isCA() ? 'Unit' : 'Chapter'} names</summary><ol class="in-keys">${items.map(it => `<li>${esc(it.title)}</li>`).join('')}</ol></details>`
      : '<p class="pv-empty">The heatmap fills in after students answer questions.</p>'}</section>
      <section class="pv-card in-wide" aria-labelledby="tcSl"><h3 id="tcSl">👩‍🎓 Students</h3><div class="in-hscroll" tabindex="0" role="region" aria-label="Student table"><table class="in-tbl" id="tcStu">
        <thead><tr><th scope="col">Roll</th><th scope="col">Name</th><th scope="col">This week</th><th scope="col">Correct</th><th scope="col">Readiness</th><th scope="col">Homework</th><th scope="col">Parent</th></tr></thead>
        <tbody>${O.rows.map(({ m, acc7, hwRate }) => `<tr><td>${esc(m.roll)}</td><td>${nameBtn(m)}</td><td>${fmtMin(m.m7)}</td><td>${pctS(acc7)}</td><td>${m.readiness == null ? '–' : m.readiness}</td><td>${hwRate == null ? '–' : hwRate + '%'}</td><td>${m.parents ? '✓' : '–'}</td></tr>`).join('')}</tbody></table></div>
        <p class="pv-note">Tap a name for the full report (same as Parent Hub).</p></section>`;
    const s = body.querySelector('#tcSubj'); if (s) s.onchange = () => { subj = s.value; students(body); };
    wireNames(body);
  }

  /* ---------- Insights ---------- */
  function insights(body) {
    const Q = O.quad, cell = k => `<div class="in-q ${k}" id="tcQ-${k}"><h4>${QL[k][0]} <span class="pv-pill">${Q[k].length}</span></h4><p class="pv-mut">${QL[k][1]}</p><div class="in-names">${Q[k].map(nameBtn).join('') || '<span class="pv-mut">—</span>'}</div></div>`;
    body.innerHTML = `<section class="pv-card in-wide" aria-labelledby="tcEr"><h3 id="tcEr">🧭 Effort vs results</h3>
        <p class="pv-mut">Effort = study time in the last 14 days (high = ${fmtMin(Q.cut)} or more, the class middle). Results = ${'70%'}+ correct in those 14 days. For teachers only.</p>
        <div class="in-quad" role="group" aria-label="Effort versus results"><span class="in-ax y" aria-hidden="true">Results ↑</span>${cell('coast')}${cell('star')}${cell('risk')}${cell('hard')}<span class="in-ax x" aria-hidden="true">Effort →</span></div>
        ${Q.nodata.length ? `<p class="pv-note">Not enough answers yet (under 10 in 14 days): ${Q.nodata.map(m => esc(m.name)).join(', ')}.</p>` : ''}</section>
      <section class="pv-card" aria-labelledby="tcWn"><h3 id="tcWn">🔔 Early warning</h3>
        ${O.warn.length ? `<ul class="pv-list" id="tcWarn">${O.warn.map(w => `<li>${nameBtn(w.m)}<ul class="in-why">${w.why.map(x => `<li>${esc(x[1])}</li>`).join('')}</ul><span class="pv-mut">💡 ${esc(w.action)}</span></li>`).join('')}</ul>` : '<p class="pv-empty">No warnings — everyone is on track. ✅</p>'}
        <p class="pv-note">Looks at the last 2 weeks: drop in time or accuracy, missed homework, a broken study habit.</p></section>
      <section class="pv-card" aria-labelledby="tcRs"><h3 id="tcRs">🚀 Rising stars</h3>
        ${O.rising.length ? `<ul class="pv-list pv-gl1" id="tcRise">${O.rising.map(x => `<li><span class="pv-gt">${nameBtn(x.m)}</span><span class="pv-pill">${Math.round(x.before)}% → ${Math.round(x.now)}%</span></li>`).join('')}</ul><p class="pv-mut">A word of praise in class goes a long way.</p>` : '<p class="pv-empty">Shows students whose accuracy rose 5+ points over the last 2 weeks.</p>'}</section>
      ${gapsHTML(8)}
      <section class="pv-card" aria-labelledby="tcPt"><h3 id="tcPt">🤝 Peer-tutor pairs</h3>
        ${O.pairs.length ? `<ul class="pv-list" id="tcPairs">${O.pairs.map(p => `<li>${nameBtn(p.tutor)} <span class="pv-mut">(${Math.round(p.tacc)}%)</span> helps ${nameBtn(p.learner)} <span class="pv-mut">(${Math.round(p.lacc)}%)</span><br><span class="pv-mut">in <b>${esc(p.title)}</b></span></li>`).join('')}</ul>` : '<p class="pv-empty">No pairs yet — needs a student with 85%+ and one under 60% in the same chapter.</p>'}</section>
      <section class="pv-card in-wide" aria-labelledby="tcCc"><h3 id="tcCc">🔍 Careless or concept? · consistency</h3><div class="in-hscroll" tabindex="0" role="region" aria-label="Mistakes and consistency table"><table class="in-tbl" id="tcCcT">
        <thead><tr><th scope="col">Name</th><th scope="col">⚡ Careless slips</th><th scope="col">🧩 Concept gaps</th><th scope="col">Consistency</th>${isCA() ? '<th scope="col">Written answers</th>' : ''}</tr></thead>
        <tbody>${O.rows.map(({ m, cons }) => `<tr><td>${nameBtn(m)}</td><td>${m.careless}</td><td>${m.concept}</td><td><span class="pv-sbar in-mini" aria-hidden="true"><i style="width:${cons}%"></i></span> ${cons}%</td>${isCA() ? `<td>${pctS(m.written)}</td>` : ''}</tr>`).join('')}</tbody></table></div>
        <p class="pv-note">Careless = fast and wrong; concept = slow and wrong, or wrong 3+ times (last 60 days, as in Parent Hub). Consistency = days studied in the last 14.</p></section>`;
    wireNames(body);
  }

  /* ---------- Homework ---------- */
  async function targets() {
    const L = P();
    if (isCA()) { const st = await L.caStructure('foundation'); return st ? st.papers.map(pp => ({ name: pp.name, items: pp.chapters.flatMap(ch => ch.units.map(u => ({ id: u.id, title: u.title, sub: pp.name }))) })) : []; }
    const cu = await L.curriculum(), g = cu && cu.grades && cu.grades[cur.grade];
    return g ? g.subjects.map(sj => ({ name: sj.name, items: (sj.chapters || []).map(ch => ({ id: `${cur.grade}-${sj.id}-${+ch.n}`, title: ch.title, sub: sj.name })) })) : [];
  }
  async function homework(body) {
    const hw = data.homework || [], today = todayK();
    const sug = O.gaps.slice(0, 5);
    body.innerHTML = `<section class="pv-card" aria-labelledby="tcHw"><h3 id="tcHw">📝 Set homework</h3>
        <p class="pv-mut">Students see it on their home screen with a “Start” button. It is done after ${isCA() ? '5 MCQs' : '3 answers (5 for a quiz)'} in that ${isCA() ? 'unit' : 'chapter'}.</p>
        <form id="tcHwF" class="pv-form" novalidate>
          <label for="tcHwT">${isCA() ? 'Unit' : 'Chapter'}</label><select id="tcHwT" class="pv-in"><option value="">Loading…</option></select>
          <div class="pv-row"><div class="pv-f"><label for="tcHwK">Type</label><select id="tcHwK" class="pv-in">${isCA() ? '<option value="mcq">MCQ set (5 questions)</option>' : '<option value="chapter">Practise the chapter (3 answers)</option><option value="quiz">Chapter quiz (5 answers)</option>'}</select></div>
            <div class="pv-f"><label for="tcHwD">Due date</label><input id="tcHwD" class="pv-in" type="date" min="${today}" value="${dk(Date.now() + 3 * DAY)}"></div></div>
          <p class="pv-err" id="tcHwE" role="alert"></p><button class="pv-btn" type="submit">Set homework</button></form></section>
      <section class="pv-card" aria-labelledby="tcHl"><h3 id="tcHl">Homework list</h3>
        ${hw.length ? `<ul class="pv-list" id="tcHwL">${hw.map(h => { const done = Ms.filter(m => (data.students.find(s => s.user_id === m.id) || {}).hw && data.students.find(s => s.user_id === m.id).hw[h.id]);
          const miss = h.due_date < today ? Ms.filter(m => !done.includes(m)) : [];
          return `<li class="pv-exam"><div><b>${esc(h.title)}</b> <span class="pv-mut">${esc(h.subject || '')} · due ${esc(fmtDate(h.due_date))}</span><br>
            <span class="pv-st ${done.length === Ms.length ? 'ok' : 'warn'}">${done.length} of ${Ms.length} done</span>${miss.length ? `<br><span class="pv-mut">Not done: ${miss.map(m => esc(m.first)).join(', ')}</span>` : ''}</div>
            <button class="pv-x" type="button" data-hwdel="${esc(h.id)}" aria-label="Delete homework ${esc(h.title)}">✕</button></li>`; }).join('')}</ul>` : '<p class="pv-empty">No homework set yet.</p>'}</section>`;
    const sel = body.querySelector('#tcHwT'), T = await targets();
    if (!sel.isConnected) return;
    sel.innerHTML = `<option value="">— Choose —</option>${sug.length ? `<optgroup label="Suggested (class is weak)">${sug.map(g => `<option value="${esc(g.id)}">${esc(g.title)}</option>`).join('')}</optgroup>` : ''}${T.map(g => `<optgroup label="${esc(g.name)}">${g.items.map(i => `<option value="${esc(i.id)}">${esc(i.title)}</option>`).join('')}</optgroup>`).join('')}`;
    const find = id => { for (const g of T) for (const i of g.items) if (i.id === id) return i; const gp = O.gaps.find(g => g.id === id); return gp ? { id, title: gp.title, sub: gp.sub } : null; };
    body.querySelector('#tcHwF').onsubmit = async ev => {
      ev.preventDefault(); const e = body.querySelector('#tcHwE'), it = find(sel.value), kind = body.querySelector('#tcHwK').value, due = body.querySelector('#tcHwD').value;
      e.textContent = ''; if (!it) { e.textContent = isCA() ? 'Choose a unit.' : 'Choose a chapter.'; return; }
      if (!/^\d{4}-\d\d-\d\d$/.test(due) || due < today) { e.textContent = 'Choose a due date from today.'; return; }
      const btn = ev.target.querySelector('button[type=submit]'); btn.disabled = true;
      try {
        const r = one(await rpc('inst_set_homework', { p_class: cur.id, p_kind: kind, p_target: it.id, p_title: (kind === 'quiz' ? 'Quiz: ' : '') + it.title, p_subject: it.sub || '', p_due: due, p_need: kind === 'chapter' ? 3 : 5 }));
        if (!r || !r.ok) { e.textContent = (r && r.msg) || 'Could not save.'; btn.disabled = false; return; }
        say('Homework set ✓'); openClass(cur, true);
      } catch (x) { e.textContent = C().errText(x); btn.disabled = false; }
    };
    body.querySelectorAll('[data-hwdel]').forEach(b => b.onclick = async () => {
      if (!b.dataset.sure) { b.dataset.sure = 1; b.textContent = 'Sure?'; return; }
      try { const r = one(await rpc('inst_delete_homework', { p_id: b.dataset.hwdel })); if (r && r.ok) { say('Homework deleted'); openClass(cur, true); } else say((r && r.msg) || 'Could not delete.'); } catch (x) { say(C().errText(x)); }
    });
  }

  /* ---------- Leaderboard ---------- */
  async function leaderboard(body) {
    body.innerHTML = `<section class="pv-card" aria-labelledby="tcLb"><h3 id="tcLb">🏆 Class leaderboard</h3><p class="pv-mut">Only students who switched it on in their app (Me → My school). First names only. Correct answers in the last 7 days.</p><div id="tcLbL"><p class="pv-load">Loading…</p></div></section>`;
    try {
      const r = one(await rpc('class_leaderboard', { p_class: cur.id })), rows = r && r.ok ? r.rows || [] : [];
      const box = body.querySelector('#tcLbL'); if (!box) return;
      box.innerHTML = rows.length ? `<ol class="pv-ol in-lb">${rows.map(x => `<li><b>${esc(x.name)}</b> <span class="pv-pill">${x.score} ✓</span></li>`).join('')}</ol>` : `<p class="pv-empty">No one has joined the leaderboard yet (${Ms.filter(m => (data.students.find(s => s.user_id === m.id) || {}).lb_opt).length} opted in).</p>`;
    } catch (e) { const box = body.querySelector('#tcLbL'); if (box) box.textContent = C().errText(e); }
  }

  /* ---------- Reports ---------- */
  function reports(body) {
    body.innerHTML = `<section class="pv-card" aria-labelledby="tcRp"><h3 id="tcRp">📄 Class report</h3><p class="pv-mut">Download the numbers for every student, or print a one-page class summary.</p>
        <div class="pv-row"><button class="pv-btn" type="button" id="tcCsv">Download CSV</button><button class="pv-btn ghost" type="button" id="tcPdf">Print / Save PDF</button></div></section>
      <section class="pv-card" aria-labelledby="tcPtm"><h3 id="tcPtm">🤝 Parent-teacher meeting report</h3><p class="pv-mut">One page per student, kind and simple, to share at the meeting.</p>
        <label for="tcPtmS" class="in-lbl">Student</label><select id="tcPtmS" class="pv-in">${Ms.map(m => `<option value="${esc(m.id)}">${esc(m.name)}${m.roll ? ' (Roll ' + esc(m.roll) + ')' : ''}</option>`).join('')}</select>
        <label for="tcPtmN" class="in-lbl">Teacher's note (optional, printed)</label><textarea id="tcPtmN" class="pv-in" rows="3" maxlength="600" placeholder="e.g. Riya participates well in class."></textarea>
        <button class="pv-btn" type="button" id="tcPtmGo"${Ms.length ? '' : ' disabled'}>Print PTM report</button></section>`;
    body.querySelector('#tcCsv').onclick = () => {
      const blob = new Blob(['﻿' + toCSV(cur, Ms, O)], { type: 'text/csv;charset=utf-8' }), a = D.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = `StudyVerse-${cur.name.replace(/[^A-Za-z0-9-]+/g, '_')}-${todayK()}.csv`; D.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
      say('CSV downloaded');
    };
    body.querySelector('#tcPdf').onclick = () => printHTML(classReportHTML());
    body.querySelector('#tcPtmGo').onclick = () => { const m = Ms.find(x => x.id === body.querySelector('#tcPtmS').value); if (m) printHTML(ptmHTML(m, body.querySelector('#tcPtmN').value.trim())); };
  }
  function printHTML(html) {
    let p = D.getElementById('pvPrint'); if (!p) { p = D.createElement('div'); p.id = 'pvPrint'; D.body.appendChild(p); }   // Parent Hub's print rules show only #pvPrint
    p.className = 'in-print'; p.innerHTML = html;
    const done = () => { p.remove(); removeEventListener('afterprint', done); }; addEventListener('afterprint', done);
    try { window.print(); } catch (e) {}
  }
  function classReportHTML() {
    const v = O.overview, sch = data.institution ? data.institution.name : '';
    return `<h1>${esc(sch)} — Class ${esc(cur.name)}</h1><p class="pp-d">StudyVerse class report · ${esc(new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' }))}</p>
      <p>${v.n} students · active this week ${v.activeWeek} · average correct ${pctS(v.acc7)} · average time ${fmtMin(v.avgMin7)} per student · homework done ${pctS(v.hwRate)} · average readiness ${v.avgReadiness == null ? '–' : Math.round(v.avgReadiness)}</p>
      ${O.gaps.length ? `<h3>Topics to re-teach</h3><ul>${O.gaps.slice(0, 5).map(g => `<li>${esc(g.title)} — ${g.weak.length} of ${g.att.length} students under 60%</li>`).join('')}</ul>` : ''}
      <table class="in-ptbl"><thead><tr><th>Roll</th><th>Name</th><th>Time (week)</th><th>Correct</th><th>Days (14)</th><th>Readiness</th><th>Homework</th></tr></thead>
      <tbody>${O.rows.map(({ m, acc7, hwRate }) => `<tr><td>${esc(m.roll)}</td><td>${esc(m.name)}</td><td>${fmtMin(m.m7)}</td><td>${pctS(acc7)}</td><td>${m.active14}</td><td>${m.readiness == null ? '–' : m.readiness}</td><td>${hwRate == null ? '–' : hwRate + '%'}</td></tr>`).join('')}</tbody></table>
      <p class="pp-f">study.moneyviel.com · StudyVerse for Schools</p>`;
  }
  function ptmHTML(m, note) {
    const A = m.A, sch = data.institution ? data.institution.name : '', sug = A.has ? P().suggestions(A) : [], acc = pct(m.r14, m.a14), accP = pct(m.rP14, m.aP14);
    const mins28 = m.m14 + m.mP14, hw = m.hw.assigned ? `${m.hw.done} of ${m.hw.assigned}` : 'none set yet';
    return `<h1>Parent-teacher meeting</h1><h2>${esc(m.name)} · ${esc(cur.name)}${m.roll ? ' · Roll ' + esc(m.roll) : ''}</h2>
      <p class="pp-d">${esc(sch)} · ${esc(new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' }))} · last 4 weeks</p>
      ${!A.has ? '<p>No study data yet. The report fills in once the student uses StudyVerse while signed in.</p>' : `
      <table class="in-ptbl"><tbody>
        <tr><th>Study time</th><td>${fmtMin(mins28)} in 4 weeks (${fmtMin(m.m7)} this week)</td></tr>
        <tr><th>Days studied</th><td>${m.active14} of the last 14 days</td></tr>
        <tr><th>Correct answers</th><td>${pctS(acc)} in the last 2 weeks${accP != null ? ` (before: ${pctS(accP)})` : ''}</td></tr>
        <tr><th>Exam readiness</th><td>${m.readiness == null ? '–' : m.readiness + ' / 100'}</td></tr>
        <tr><th>Homework done</th><td>${hw}</td></tr>
        <tr><th>Mistakes</th><td>${m.careless + m.concept ? `${m.careless} quick slips · ${m.concept} need more practice` : 'not enough data yet'}</td></tr></tbody></table>
      <h3>Doing well 🌟</h3><ul>${A.best.length ? A.best.map(g => `<li>${esc(g.title)}${g.sub ? ' (' + esc(g.sub) + ')' : ''} — ${pctS(g.acc)}</li>`).join('') : '<li>Keeps practising — strengths show after a few more quizzes.</li>'}</ul>
      <h3>Next steps 🌱</h3><ul>${A.weak.length ? A.weak.map(g => `<li>Practise ${esc(g.title)}${g.sub ? ' (' + esc(g.sub) + ')' : ''} — now ${pctS(g.acc)}</li>`).join('') : ''}${sug.slice(0, 2).map(x => `<li>${x}</li>`).join('')}</ul>`}
      ${note ? `<h3>Teacher's note</h3><p>${esc(note)}</p>` : ''}
      <p class="in-sign"><span>Teacher</span><span>Parent</span></p>
      <p class="pp-f">study.moneyviel.com · Parents can follow day-to-day progress free in Parent Hub.</p>`;
  }

  /* ---------- per-student page: the same cards as Parent Hub ---------- */
  function student(m) {
    if (!m) return;
    const L = P(), A = m.A, X = m.X;
    frame(`<span>${esc(m.name)}</span><small class="in-sub">${esc(cur.name)}${m.roll ? ' · Roll ' + esc(m.roll) : ''}</small>`, `<div class="pv-body" id="tcStuB">${!A.has ? `<div class="pv-card"><h2>No data yet</h2><p>${esc(m.name)}'s progress shows here after they study with the app while signed in.</p></div>` :
      `<section class="pv-card" aria-labelledby="tcSw"><h3 id="tcSw">This week</h3>${A.weekMin > 0 ? L.chartSVG(A) : '<p class="pv-empty">No study time in the last 7 days.</p>'}
        <div class="pv-kpis">${kpi(fmtMin(A.weekMin), 'Total time')}${kpi(A.daysActive + '/7', 'Days active')}${kpi(pctS(A.accW), 'Correct')}${kpi(A.qw.a, 'Questions')}${kpi(m.hw.assigned ? m.hw.done + '/' + m.hw.assigned : '–', 'Homework done')}${kpi(m.parents ? '✓ Linked' : 'Not yet', 'Parent Hub')}</div></section>
      ${L.readinessHTML(A, m.R)}${L.trendHTML(A, X.trend)}${L.masteryHTML(A, X.mastery)}${L.mistakeHTML(A, X)}${L.timeHTML(A, X)}${L.winsHTML(A, X)}${L.writesHTML(A, X)}`}
      <section class="pv-card"><button class="pv-btn" type="button" id="tcStuPtm">Print PTM report</button></section></div>`, () => render(), '← ' + cur.name);
    hub.querySelector('#tcRef').onclick = () => openClass(cur, true);
    const ch = hub.querySelector('#pvCheer'); if (ch) ch.remove();              // the parent's WhatsApp cheer button is for parents
    hub.querySelector('#tcStuPtm').onclick = () => printHTML(ptmHTML(m, ''));
  }

  window.Teach = { open, close, lib: { metrics, classInsights, compare, toCSV }, _state: () => ({ Ms, O, cur }) };
})();
