/* ================= 📅 Exam countdown planner — js/exam.js =================
   Home: the 📊 Dashboard tab (top card). School: above the dashboard drawn by js/insights.js (#s-insights);
   CA: above the CA dashboard (#cdHost, js/ca-tools.js). Added by watching the DOM — those files are not edited.
   Also: ONE small banner on the World / CA home, only when the exam is 0–7 days away.

   The student sets an exam date (school: term or annual exam, one subject or all subjects, optionally "up to
   chapter N"; CA: the attempt month — Jan / May / Sep — then the exact date, saved in ST.ca.exam like the CA
   home countdown). The plan is worked out again from progress every time it is shown, so it adapts by itself:
     tasks   school: learn chunks (≤3 topics of a chapter, open the first unfinished topic) for chapters not done,
                     🎯 chapter test for weak chapters (stars < 2, readiness < 60 % or accuracy < 60 %)
             CA:     units not complete (open the unit), weak complete units (accuracy < 60 % → MCQ tab)
     days    today … exam-1: study days, then revision day(s) (revision sheets of the weakest chapters / CA unit
             Revise tab) and a 🏆 mock test the day before the exam
     today   2–3 tasks (kept fixed for the day; ticked automatically when finished, read from progress)
     behind  "I'm behind" re-spreads what is left: weak and started chapters and exam favourites first,
             at most 3 a day; the rest goes to "If you have time".
   State: ST.examPlan = { school: {date, kind, scope, upto, grade, set, snap, done, day, keep, focus, rewd},
                          ca: {attempt, set, snap, done, day, keep, focus, rewd} }  (CA date = ST.ca.exam) */
(function () {
  'use strict';
  const D = document;
  const tap = k => { try { sfx(k); } catch (e) {} };
  const say = m => { try { if (window.A11Y && A11Y.announce) A11Y.announce(m); } catch (e) {} };
  const isCA = () => !!(ST.profile && ST.profile.course === 'ca');
  const CAX = () => (window.Ca && Ca._) || null;
  const P = () => (ST.examPlan = ST.examPlan && typeof ST.examPlan === 'object' ? ST.examPlan : {});
  const localISO = (d = new Date()) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const dayN = iso => Math.round(Date.parse(iso + 'T12:00:00Z') / 864e5);
  const plusDays = (iso, n) => new Date((dayN(iso) + n) * 864e5).toISOString().slice(0, 10);
  const daysTo = iso => iso ? dayN(iso) - dayN(localISO()) : null;
  const niceDate = (iso, o) => new Date(iso + 'T00:00:00').toLocaleDateString('en-IN', o || { weekday: 'short', day: 'numeric', month: 'short' });
  const MAXDAY = 3;

  /* ---------- the plan this student has (null = none) ---------- */
  function cur() {
    if (!ST.profile) return null;
    if (isCA()) {
      const X = CAX(); if (!X) return null; const date = X.C().exam; if (!date) return null;
      const p = P(); p.ca = p.ca || { set: today() }; return Object.assign(p.ca, { date, ca: true });
    }
    const s = P().school; return s && s.date ? s : null;
  }
  const prep = sp => { sp.snap = sp.snap || {}; sp.done = sp.done || {}; delete sp.asg; return sp; };
  /* test / MCQ / mock tasks: done once the progress they watch has changed since the task was put on a day's list
     (sig = a short signature of that progress, snap = the signature saved when the task was given) */
  const changed = (sp, id, sig) => sp.snap[id] != null && sp.snap[id] !== sig;

  /* ---------- tasks ---------- */
  function rr(lists) { const out = [], L = lists.map(l => l.slice()); while (L.some(l => l.length)) L.forEach(l => { if (l.length) out.push(l.shift()); }); return out; }
  function weave(learn, weak) { const out = []; let i = 0, j = 0; while (i < learn.length || j < weak.length) { if (i < learn.length) out.push(learn[i++]); if (i < learn.length) out.push(learn[i++]); if (j < weak.length) out.push(weak[j++]); } return out; }
  function chScore(g, sid, ci, c) {           // 0..1 (lower = weaker) from stars, last chapter test and quiz accuracy
    const parts = [];
    const st = c.topics.reduce((a, t) => a + topicStars(t.id), 0) / Math.max(1, c.topics.length); parts.push(st / 3);
    const ts = ST.tests && ST.tests[`g${g}-${sid}-${ci}`]; if (ts) parts.push(ts.ready / 100);
    let s = 0, w = 0; c.topics.forEach(t => (t.quiz || []).forEach((q, i) => { const x = (ST.qstats || {})[`${t.id}#${i}`]; if (x) { s += x.s; w += x.w; } }));
    if (s >= 4) parts.push((s - w) / s);
    return Math.min(...parts);
  }
  async function schoolTasks(sp) {
    const g = ST.profile.grade, subs = curSubjects(g).filter(s => sp.scope === 'all' || s.id === sp.scope);
    const datas = await Promise.all(subs.map(s => subjectData(g, s.id)));
    const learnL = [], weakL = [], chs = [];
    subs.forEach((s, i) => {
      const d = datas[i]; if (!d) return; const L = [], W = [];
      d.chapters.forEach((c, ci) => {
        if (sp.upto && c.n > sp.upto) return;
        const score = chScore(g, s.id, ci, c), started = c.topics.some(t => topicStars(t.id));
        chs.push({ sid: s.id, sname: s.name, ci, c, score, done: chapterDone(c) });
        for (let k = 0; k < c.topics.length; k += 3) {
          const chunk = c.topics.slice(k, k + 3), fi = chunk.findIndex(t => !topicStars(t.id));
          L.push({ id: `L:${s.id}:${ci}:${k / 3}`, type: 'learn', e: '📖', sid: s.id, ci, ti: k + Math.max(0, fi), done: fi < 0, started,
            imp: chunk.some(t => t.revise && t.revise.level === 'important'),
            title: chunk[0].title + (chunk.length > 1 ? ` + ${chunk.length - 1} more` : ''), sub: `${s.name} · Ch ${c.n}: ${c.title}` });
        }
        if (chapterDone(c) && score < .6) {
          const id = `T:${s.id}:${ci}`, ts = ST.tests && ST.tests[`g${g}-${s.id}-${ci}`];
          let qn = 0; c.topics.forEach(t => (t.quiz || []).forEach((q, i) => { const x = (ST.qstats || {})[`${t.id}#${i}`]; if (x) qn += x.s; }));
          const sig = ts ? `${ts.d}|${ts.pct}|${ts.ready}|${qn}` : '-';
          W.push({ id, type: 'test', e: '🎯', sid: s.id, ci, weak: true, sig, done: !!ts && changed(sp, id, sig), title: `Chapter test: ${c.title}`, sub: `${s.name} · Ch ${c.n} · weak spot` });
        }
      });
      learnL.push(L); weakL.push(W);
    });
    return { tasks: weave(rr(learnL), rr(weakL)), chs, subs };
  }
  async function caTasks(sp) {
    const X = CAX(), c = X.C(), st = await X.structure(c.level), wd = X.weakData().units;
    const per = [], weak = [], units = [];
    st.papers.forEach(p => {
      const L = [];
      p.chapters.forEach(ch => ch.units.forEach(u => {
        if (u.status !== 'built') return;
        const prog = X.unitProg(u.id), pct = wd[u.id] ? X.pctOf(wd[u.id]) : null, lab = X.paperLabel(p);
        units.push({ uid: u.id, u, p, ch, pct, prog });
        L.push({ id: `U:${u.id}`, type: 'unit', e: '📘', uid: u.id, done: prog >= 1, started: prog > 0, title: u.title, sub: `${lab} · Ch ${ch.n} · Unit ${u.n}` });
        if (prog >= 1 && pct != null && pct < .6) {
          const id = `W:${u.id}`; let n = 0; Object.entries(c.mcq || {}).forEach(([k, v]) => { if (k.startsWith(u.id + '#')) n += v.s || 0; });
          weak.push({ id, type: 'weak', e: '🎯', uid: u.id, weak: true, sig: String(n), done: changed(sp, id, String(n)), title: `MCQs again: ${u.title}`, sub: `${lab} · Ch ${ch.n} · ${Math.round(pct * 100)}% so far` });
        }
      }));
      per.push(L);
    });
    return { tasks: weave(rr(per), weak), units };
  }
  const prio = t => (t.weak ? 0 : t.started ? 1 : t.imp ? 2 : 3);

  /* ---------- days: study … revision … mock … exam ---------- */
  function shape(dl) {
    const mock = dl >= 2 ? dl - 1 : dl === 1 ? 0 : null;
    const rev = dl >= 10 ? [dl - 3, dl - 2] : dl >= 4 ? [dl - 2] : [];
    const S = rev.length ? rev[0] : mock != null ? mock : Math.max(0, dl);
    return { mock, rev, S };
  }
  function dayType(i, sh) { return i < sh.S ? 'study' : sh.rev.includes(i) ? 'rev' : i === sh.mock ? 'mock' : 'study'; }

  async function build() {
    const sp = cur(); if (!sp) return null; prep(sp);
    const dl = daysTo(sp.date), sh = shape(Math.max(0, dl));
    const T = sp.ca ? await caTasks(sp) : await schoolTasks(sp);
    const all = T.tasks, byId = Object.fromEntries(all.map(t => [t.id, t]));
    let pending = all.filter(t => !t.done && !sp.done[t.id]);
    if (sp.focus) pending = pending.map((t, i) => [t, i]).sort((a, b) => prio(a[0]) - prio(b[0]) || a[1] - b[1]).map(x => x[0]);
    let extra = [];
    if (sp.focus && sh.S > 0 && pending.length > MAXDAY * sh.S) { extra = pending.slice(MAXDAY * sh.S); pending = pending.slice(0, MAXDAY * sh.S); }
    const perDay = sh.S > 0 ? Math.ceil(pending.length / sh.S) : 0;
    /* revision / mock tasks for a given day */
    const revTasks = d => sp.ca
      ? T.units.filter(x => x.prog > 0).sort((a, b) => (a.pct ?? 1) - (b.pct ?? 1)).slice(0, 2).map(x => ({ id: `R:${x.uid}:${d}`, type: 'rev', e: '📝', uid: x.uid, title: `Revise: ${x.u.title}`, sub: `${X_lab(x)} · read the Revise tab`, tapDone: true }))
      : T.chs.filter(x => x.c.topics.some(t => topicStars(t.id))).sort((a, b) => a.score - b.score).slice(0, 2).map(x => ({ id: `R:${x.sid}:${x.ci}:${d}`, type: 'rev', e: '📝', sid: x.sid, ci: x.ci, title: `Revision sheet: ${x.c.title}`, sub: `${x.sname} · Ch ${x.c.n}`, tapDone: true }));
    const mockTasks = () => {
      if (sp.ca) { const id = 'M:ca', sig = String((CAX().C().tests || []).filter(t => t.kind === 'mock').length); return [{ id, type: 'mock', e: '🏆', title: 'Mock paper (exam pattern)', sub: 'Full paper with the timer · do it like the real exam', sig, done: changed(sp, id, sig) }]; }
      const g = ST.profile.grade, sc = {}; T.chs.forEach(x => { (sc[x.sid] = sc[x.sid] || []).push(x.score); });
      return T.subs.filter(s => sc[s.id]).sort((a, b) => Math.min(...sc[a.id]) - Math.min(...sc[b.id])).slice(0, 2).map(s => { const id = `M:${s.id}`, ts = ST.tests && ST.tests[`g${g}-${s.id}`], sig = ts ? `${ts.d}|${ts.pct}|${ts.ready}` : '-';
        return { id, type: 'mock', e: '🏆', sid: s.id, title: `Mock test: ${s.name}`, sub: '25 questions · like the real exam', sig, done: changed(sp, id, sig) }; });
    };
    function X_lab(x) { try { return `${CAX().paperLabel(x.p)} · Ch ${x.ch.n}`; } catch (e) { return ''; } }
    /* today's list: fixed for the day once made */
    const tType = dl < 0 ? 'past' : dl === 0 ? 'exam' : dayType(0, sh);
    let day = sp.day && sp.day.d === today() ? sp.day : null;
    if (!day && dl > 0) {
      let items;
      const kept = sp.keep && sp.keep.d === today() ? sp.keep.items : [];      /* "I'm behind": today's finished tasks stay ticked */
      if (tType === 'study') { const fresh = pending.filter(t => !kept.some(k => k.id === t.id)); items = kept.concat(fresh.slice(0, Math.max(1, Math.max(2, Math.min(perDay, MAXDAY)) - kept.length))); }
      else if (tType === 'rev') items = revTasks(today()).concat(pending.slice(0, 1));
      else items = mockTasks();
      day = sp.day = { d: today(), items: items.map(t => ({ id: t.id, type: t.type, e: t.e, title: t.title, sub: t.sub, sid: t.sid, ci: t.ci, ti: t.ti, uid: t.uid, tapDone: !!t.tapDone })) };
      items.forEach(t => { if (t.sig != null && sp.snap[t.id] == null) sp.snap[t.id] = t.sig; });
      save();
    }
    /* tick: from progress (or tapped, for reading tasks); a task that left the list was finished */
    const mk = mockTasks(), mkById = Object.fromEntries(mk.map(t => [t.id, t]));
    const items = (day ? day.items : []).map(it => {
      const now = byId[it.id] || mkById[it.id];
      const done = !!sp.done[it.id] || (now ? !!now.done : it.type !== 'rev' && it.type !== 'mock');
      return Object.assign({}, it, now && it.type !== 'rev' ? { ti: now.ti } : {}, { done });
    });
    if (items.length && items.every(t => t.done) && sp.rewd !== today()) { sp.rewd = today(); addXP(10, "Today's plan done!"); }
    /* the days ahead (preview) */
    const ahead = []; let q = pending.filter(t => !items.some(x => x.id === t.id)), i = 1;
    const left = Math.max(1, sh.S - 1), per2 = Math.max(1, Math.ceil(q.length / left));
    for (; i < Math.max(0, dl) && ahead.length < 21; i++) {
      const ty = dayType(i, sh), d = plusDays(localISO(), i);
      if (ty === 'study') { const n = q.splice(0, per2); ahead.push({ d, ty, n: n.length, first: n[0] && n[0].title }); }
      else ahead.push({ d, ty, n: ty === 'mock' ? (sp.ca ? 1 : Math.min(2, T.subs.length)) : 2 });
    }
    const total = all.length, doneN = all.filter(t => t.done || sp.done[t.id]).length;
    return { sp, dl, sh, items, perDay, pending, extra, ahead, total, doneN, tType };
  }

  /* ---------- opening a task ---------- */
  function go(it, sp) {
    tap('open');
    if (it.tapDone) { sp.done[it.id] = today(); save(); }
    if (it.uid && window.Ca) { if (it.type === 'weak') return Ca.unit(it.uid, 'mcq'); if (it.type === 'rev') return Ca.unit(it.uid, 'revise'); return Ca.unit(it.uid); }
    if (it.type === 'mock') { if (sp.ca) return window.CaTools && CaTools.mocks(); return window.Tests && Tests.run('mock', it.sid); }
    if (it.type === 'test') return window.Tests && Tests.run('chapter', it.sid, it.ci);
    if (it.type === 'rev') return window.Tests && Tests.sheet(it.sid, it.ci);
    return playTopic(it.sid, it.ci, it.ti || 0);
  }

  /* ---------- styles ---------- */
  function css() {
    if (D.getElementById('exCss')) return;
    D.head.insertAdjacentHTML('beforeend', `<style id="exCss">
.ex-card h3{margin:0}.ex-top{display:flex;align-items:center;gap:12px}.ex-days{min-width:74px;text-align:center;border-radius:16px;background:#f1efff;padding:6px 4px;line-height:1}
.ex-days b{display:block;font-family:'Baloo 2';font-size:30px;color:var(--violet)}.ex-days span{font-size:11px;font-weight:800;color:var(--muted)}
.ex-what{flex:1;min-width:0}.ex-what small{display:block;color:var(--muted);font-weight:700;font-size:12.5px;margin-top:2px}
.ex-bar{height:8px;border-radius:9px;background:#e9ebf7;margin:10px 0 4px;overflow:hidden}.ex-bar i{display:block;height:100%;background:var(--mint);border-radius:9px}
.ex-note{font-size:12.5px;color:var(--muted);font-weight:700;margin:0 0 8px}
.ex-h{font:800 12px Nunito,sans-serif;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin:12px 0 6px}
.ex-task{display:flex;align-items:center;gap:10px;width:100%;text-align:left;border:2px solid #e3e6f6;background:#fff;border-radius:14px;padding:10px 12px;margin-bottom:8px;cursor:pointer;font:inherit;color:var(--ink);min-height:52px}
.ex-task .ex-ck{flex:0 0 26px;height:26px;border-radius:50%;border:2px solid #c9cde8;display:flex;align-items:center;justify-content:center;font-size:14px}
.ex-task .ex-tb{flex:1;min-width:0}.ex-task b{display:block;font-size:14.5px;line-height:1.25}.ex-task small{display:block;color:var(--muted);font-size:12px;font-weight:700;margin-top:1px}
.ex-task .ex-go{font-size:22px;opacity:.45}
.ex-task.done{background:#effcf6;border-color:#bfeedd}.ex-task.done b{text-decoration:line-through;text-decoration-color:rgba(0,0,0,.35)}.ex-task.done .ex-ck{background:var(--mint);border-color:var(--mint);color:#fff}
.ex-acts{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:4px}.ex-link{background:none;border:0;color:var(--violet);font:800 13px Nunito,sans-serif;cursor:pointer;padding:8px 4px;min-height:36px}
.ex-acts .btn{width:auto;flex:1;font-size:15px;padding:10px 12px}
.ex-card details{margin-top:8px}.ex-card summary{cursor:pointer;font-weight:800;font-size:13.5px;color:var(--violet);padding:6px 0}
.ex-day{display:flex;gap:8px;font-size:13px;padding:5px 0;border-top:1px solid #eef0f7}.ex-day span{flex:0 0 92px;font-weight:800;color:var(--muted)}.ex-day em{font-style:normal;font-weight:700}
.ex-chips{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 10px}.ex-chip{border:2px solid #e3e6f6;background:#fff;border-radius:999px;padding:7px 12px;font:800 13px Nunito,sans-serif;color:var(--ink);cursor:pointer;min-height:36px}
.ex-chip[aria-pressed=true]{background:var(--violet);border-color:var(--violet);color:#fff}
.ex-lab{display:block;font:800 12.5px Nunito,sans-serif;color:var(--muted);margin:8px 0 4px}
.ex-in{width:100%;border:2px solid #e3e6f6;border-radius:12px;padding:10px 12px;font:700 15px Nunito,sans-serif;color:var(--ink);background:#fff;margin-bottom:10px}
.ex-ban{display:flex;align-items:center;gap:8px;width:calc(100% - 24px);margin:0 12px 10px;border:0;border-radius:14px;padding:10px 14px;background:#fff6e0;color:var(--ink);font:800 14px Nunito,sans-serif;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.15);text-align:left;min-height:44px}
.ex-ban span{flex:1}.ex-ban i{font-style:normal;font-size:20px;opacity:.6}
#s-ca .ex-ban{width:100%;margin:0 0 12px}
</style>`);
  }

  /* ---------- the dashboard card ---------- */
  let wantFocus = false;
  function setupHTML(sp, ca) {
    if (ca) {
      const now = new Date(), opts = []; let y = now.getFullYear(), m = now.getMonth() + 1;
      while (opts.length < 3) { m++; if (m > 12) { m = 1; y++; } if ([1, 5, 9].includes(m)) opts.push([`${y}-${String(m).padStart(2, '0')}`, new Date(y, m - 1, 1).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })]); }
      const at = (P().ca || {}).attempt;
      return `<h3>📅 Exam countdown</h3><p class="sub" style="margin:4px 0 6px">Pick your CA attempt, then the date of your first paper. You get a daily plan up to the exam.</p>
        <span class="ex-lab" id="exAtL">Your attempt</span><div class="ex-chips" role="group" aria-labelledby="exAtL">${opts.map(([k, n]) => `<button type="button" class="ex-chip" data-at="${k}" aria-pressed="${at === k}">${esc(n)}</button>`).join('')}</div>
        <label class="ex-lab" for="exDate">Date of your first paper <small>(from the ICAI timetable)</small></label><input type="date" class="ex-in" id="exDate" min="${localISO()}" value="${esc(sp && sp.date || '')}">
        <div class="ex-acts"><button class="btn" id="exSave">Make my plan</button>${sp ? '<button class="ex-link" id="exCancel">Cancel</button>' : ''}</div>`;
    }
    const g = ST.profile.grade, subs = curSubjects(g), s0 = sp || {};
    return `<h3>📅 Exam countdown</h3><p class="sub" style="margin:4px 0 6px">Tell me when your exam is. I'll make a small plan for every day until then.</p>
      <span class="ex-lab" id="exKL">Which exam?</span><div class="ex-chips" role="group" aria-labelledby="exKL">${[['term', 'Term exam'], ['annual', 'Annual exam']].map(([k, n]) => `<button type="button" class="ex-chip" data-kind="${k}" aria-pressed="${(s0.kind || 'annual') === k}">${n}</button>`).join('')}</div>
      <span class="ex-lab" id="exSL">Subjects</span><div class="ex-chips" role="group" aria-labelledby="exSL"><button type="button" class="ex-chip" data-sc="all" aria-pressed="${(s0.scope || 'all') === 'all'}">All subjects</button>${subs.map(s => `<button type="button" class="ex-chip" data-sc="${esc(s.id)}" aria-pressed="${s0.scope === s.id}">${esc(s.name)}</button>`).join('')}</div>
      <label class="ex-lab" for="exUpto">Chapters in the exam</label><select class="ex-in" id="exUpto"><option value="">All chapters</option>${Array.from({ length: 20 }, (_, i) => i + 1).map(n => `<option value="${n}" ${s0.upto === n ? 'selected' : ''}>Chapters 1 to ${n}</option>`).join('')}</select>
      <label class="ex-lab" for="exDate">Exam date</label><input type="date" class="ex-in" id="exDate" min="${localISO()}" value="${esc(s0.date || '')}">
      <div class="ex-acts"><button class="btn" id="exSave">Make my plan</button>${sp ? '<button class="ex-link" id="exCancel">Cancel</button>' : ''}</div>`;
  }
  function wireSetup(box, sp, ca) {
    const pick = (sel, b) => box.querySelectorAll(sel).forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    box.querySelectorAll('[data-kind]').forEach(b => b.onclick = () => { tap('tap'); pick('[data-kind]', b); });
    box.querySelectorAll('[data-sc]').forEach(b => b.onclick = () => { tap('tap'); pick('[data-sc]', b); });
    box.querySelectorAll('[data-at]').forEach(b => b.onclick = () => { tap('tap'); pick('[data-at]', b); const i = box.querySelector('#exDate');
      if (!i.value || i.value.slice(0, 7) !== b.dataset.at) i.value = b.dataset.at + '-01'; i.focus(); });
    const cancel = box.querySelector('#exCancel'); if (cancel) cancel.onclick = () => { tap('tap'); fill(box); };
    box.querySelector('#exSave').onclick = () => {
      const v = box.querySelector('#exDate').value;
      if (!v) { toast('Pick the exam date first'); box.querySelector('#exDate').focus(); return; }
      if (daysTo(v) < 0) { toast('That date has passed — pick a future date'); return; }
      if (ca) {
        const X = CAX(); X.C().exam = v; const at = box.querySelector('[data-at][aria-pressed=true]');
        P().ca = { attempt: at ? at.dataset.at : v.slice(0, 7), set: today() };
      } else {
        const kind = (box.querySelector('[data-kind][aria-pressed=true]') || {}).dataset?.kind || 'annual';
        const scope = (box.querySelector('[data-sc][aria-pressed=true]') || {}).dataset?.sc || 'all';
        const upto = +box.querySelector('#exUpto').value || null;
        P().school = { date: v, kind, scope, upto, grade: ST.profile.grade, set: today() };
      }
      save(); tap('unlock'); toast('📅 Your plan is ready'); fill(box).then(() => say(`${daysTo(v)} days to your exam. Today's plan is ready.`));
    };
  }
  const kindName = sp => sp.ca ? `CA ${(() => { try { return CAX().levelName(CAX().C().level); } catch (e) { return 'Foundation'; } })()} exam` : `${sp.kind === 'term' ? 'Term' : 'Annual'} exam`;
  function scopeName(sp) { if (sp.ca) return sp.attempt ? new Date(sp.attempt + '-01T00:00:00').toLocaleDateString('en-IN', { month: 'long', year: 'numeric' }) + ' attempt' : '';
    if (sp.scope === 'all') return 'All subjects' + (sp.upto ? ` · Ch 1–${sp.upto}` : '');
    const s = curSubjects(ST.profile.grade).find(x => x.id === sp.scope); return (s ? s.name : sp.scope) + (sp.upto ? ` · Ch 1–${sp.upto}` : ''); }

  async function fill(box, editing) {
    css();
    const ca = isCA(), sp0 = cur();
    if (!sp0 || editing || (!ca && sp0.grade && sp0.grade !== ST.profile.grade)) { box.innerHTML = setupHTML(editing ? sp0 : null, ca); wireSetup(box, sp0, ca); return; }
    let m; try { m = await build(); } catch (e) { console.warn('exam plan', e); box.innerHTML = '<h3>📅 Exam countdown</h3><p class="sub">Could not make the plan right now. Please try again.</p>'; return; }
    if (!m || !box.isConnected) return;
    const { sp, dl, items, perDay, pending, extra, ahead, total, doneN, tType } = m;
    const head = `<div class="ex-top"><div class="ex-days" aria-hidden="true"><b>${Math.max(0, dl)}</b><span>${dl === 1 ? 'day left' : 'days left'}</span></div>
      <div class="ex-what"><h3>📅 ${esc(kindName(sp))}</h3><small>${esc(scopeName(sp))}</small><small>${esc(niceDate(sp.date, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }))}</small></div></div>
      <span class="sr-only">${dl} ${dl === 1 ? 'day' : 'days'} to your exam.</span>
      <div class="ex-bar" role="progressbar" aria-label="Plan done" aria-valuemin="0" aria-valuemax="${total}" aria-valuenow="${doneN}"><i style="width:${total ? Math.round(doneN / total * 100) : 0}%"></i></div>
      <p class="ex-note">${doneN} of ${total} study tasks done${sp.focus ? ' · 🎯 most important first' : ''}</p>`;
    if (tType === 'past') {
      box.innerHTML = head.replace(/<div class="ex-bar"[\s\S]*$/, '') + `<p class="sub" style="margin-top:8px">Your exam date has passed. How did it go? Set your next exam to get a new plan.</p><button class="btn" id="exNew">Set my next exam</button>`;
      box.querySelector('#exNew').onclick = () => { tap('tap'); fill(box, true); }; return;
    }
    const row = it => `<button type="button" class="ex-task ${it.done ? 'done' : ''}" data-tid="${esc(it.id)}" aria-label="${esc(it.title)}. ${esc(it.sub || '')}${it.done ? '. Done' : ''}">
        <span class="ex-ck" aria-hidden="true">${it.done ? '✓' : it.e}</span><span class="ex-tb"><b>${esc(it.title)}</b><small>${esc(it.sub || '')}</small></span><span class="ex-go" aria-hidden="true">›</span></button>`;
    const allDone = items.length && items.every(t => t.done);
    const bonus = allDone && tType === 'study' ? pending.find(t => !items.some(x => x.id === t.id)) : null, rows = items.concat(bonus ? [bonus] : []);
    const dayLab = { study: "Today's plan", rev: 'Today: revision day', mock: 'Today: mock test day' }[tType] || "Today's plan";
    let body = '';
    if (tType === 'exam') body = `<p class="sub" style="margin-top:8px">🍀 Exam day! Read your notes calmly, sleep well and do your best. You've got this.</p>`;
    else {
      body = `<div class="ex-h">${dayLab}${allDone ? ' · all done 🎉' : ''}</div><div id="exToday">${items.map(row).join('') || '<p class="sub">Nothing left to learn. Revise your weak spots and take a mock test.</p>'}</div>`;
      if (bonus) body += `<div class="ex-h">Great work! One more if you like</div>${row(bonus)}`;
      if (!sp.focus && perDay > MAXDAY) body += `<p class="ex-note">To cover everything you'd need about ${perDay} tasks a day. Tap “I'm behind” and I'll put the most important first.</p>`;
      if (ahead.length) body += `<details><summary>See the days ahead</summary>${ahead.map(a => `<div class="ex-day"><span>${esc(niceDate(a.d))}</span><em>${a.ty === 'rev' ? '📝 Revision day' : a.ty === 'mock' ? '🏆 Mock test' : a.n ? `${a.n} task${a.n > 1 ? 's' : ''}${a.first ? ' · ' + esc(a.first) : ''}` : 'Free / catch up'}</em></div>`).join('')}<div class="ex-day"><span>${esc(niceDate(sp.date))}</span><em>✏️ Exam</em></div></details>`;
      if (extra.length) body += `<details><summary>If you have time (${extra.length})</summary>${extra.slice(0, 30).map(t => `<div class="ex-day"><span>${t.e}</span><em>${esc(t.title)} <small>· ${esc(t.sub || '')}</small></em></div>`).join('')}</details>`;
    }
    const acts = `<div class="ex-acts" style="margin-top:10px">${tType !== 'exam' && !allDone ? '<button class="btn ghost" id="exBehind">😅 I\'m behind</button>' : ''}${sp.focus ? '<button class="ex-link" id="exFull">Show full plan</button>' : ''}<button class="ex-link" id="exEdit">Change exam</button></div>`;
    box.innerHTML = head + body + acts;
    box.querySelectorAll('[data-tid]').forEach(b => b.onclick = () => { const it = rows.find(x => x.id === b.dataset.tid); if (it) go(it, sp); });
    const on = (id, fn) => { const b = box.querySelector('#' + id); if (b) b.onclick = fn; };
    on('exBehind', () => { tap('tap'); sp.focus = true; sp.keep = { d: today(), items: (sp.day && sp.day.d === today() ? sp.day.items : []).filter(x => items.some(i => i.id === x.id && i.done)) }; sp.day = null; save(); fill(box).then(() => { toast('Plan rebalanced: most important first'); say("Plan rebalanced. Today's plan has the most important tasks first."); }); });
    on('exFull', () => { tap('tap'); sp.focus = false; sp.day = null; save(); fill(box); });
    on('exEdit', () => { tap('tap'); fill(box, true); });
    if (wantFocus) { wantFocus = false; setTimeout(() => { try { box.scrollIntoView({ block: 'start', behavior: 'smooth' }); const f = box.querySelector('.ex-task:not(.done)') || box; f.focus && f.focus({ preventScroll: true }); } catch (e) {} }, 60); }
  }

  /* ---------- banner (World / CA home, only 0–7 days before the exam) ---------- */
  function bannerHTML(dl) { return `<button type="button" class="ex-ban" data-exban="${dl}" aria-label="${dl === 0 ? 'Your exam is today' : `${dl} ${dl === 1 ? 'day' : 'days'} to your exam`}. Open today's plan"><span>📅 ${dl === 0 ? 'Exam today' : `${dl} ${dl === 1 ? 'day' : 'days'} to your exam`} · today's plan</span><i aria-hidden="true">›</i></button>`; }
  function openPlan() { tap('open'); wantFocus = true; if (isCA()) { if (window.CaTools) CaTools.dashboard(); } else if (window.Insights) Insights.dashboard({ tab: true }); }

  /* ---------- placing the card and the banner ---------- */
  const act = id => { const e = D.getElementById(id); return e && e.classList.contains('active') ? e : null; };
  function place() {
    if (!ST.profile) return;
    try { if (window.Cloud && Cloud.isParent && Cloud.isParent()) return; } catch (e) {}
    let w;
    /* dashboard card */
    if (!isCA() && (w = act('s-insights'))) {
      const host = w.querySelector(':scope > .ins-dashhost');
      if (host && !w.querySelector(':scope > #exCard')) { css(); host.insertAdjacentHTML('beforebegin', '<div class="card ex-card" id="exCard" role="region" aria-label="Exam countdown"></div>'); fill(w.querySelector('#exCard')); }
    }
    if (isCA() && (w = act('s-ca'))) {
      const host = w.querySelector('#cdHost');
      if (host && !w.querySelector('#exCard')) { css(); host.insertAdjacentHTML('beforebegin', '<div class="card ex-card" id="exCard" role="region" aria-label="Exam countdown"></div>'); fill(w.querySelector('#exCard')); }
    }
    /* banner */
    const sp = cur(), dl = sp ? daysTo(sp.date) : null, due = dl != null && dl >= 0 && dl <= 7;
    if (!isCA() && (w = act('s-world'))) {
      const map = D.getElementById('map'); let b = w.querySelector('[data-exban]');
      if (b && (!due || b.dataset.exban !== String(dl))) { b.remove(); b = null; }
      if (due && map && !b) { css(); const ref = w.querySelector(':scope > .hud') || map; ref.insertAdjacentHTML('beforebegin', bannerHTML(dl)); w.querySelector('[data-exban]').onclick = openPlan; }
    }
    if (isCA() && (w = act('s-ca'))) {
      const top = w.querySelector(':scope > .ca-top'), b = w.querySelector('[data-exban]');
      if (b && (!due || b.dataset.exban !== String(dl))) b.remove();
      else if (due && top && !b && w.querySelector('.ca-journey')) { css(); top.insertAdjacentHTML('afterend', bannerHTML(dl)); w.querySelector('[data-exban]').onclick = openPlan; }
    }
  }
  let t = 0;
  new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; try { place(); } catch (e) { console.warn(e); } }); }).observe(D.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });

  window.ExamPlan = { build, cur, openPlan, daysTo, _shape: shape };
})();
