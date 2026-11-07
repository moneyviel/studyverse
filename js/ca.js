/* ================= CA (Chartered Accountancy, ICAI) — professional course pilot =================
   A separate, professional interface inside StudyVerse ("pro" look band, see js/look.js).
   Screens (all inside <section id="s-ca">):
     home    — CA Journey: Foundation → Intermediate → Final, papers with progress rings, next unit,
               exam countdown, a daily line for the student, weak spots, group study
     paper   — chapters and units in ICAI order, progress, search within the paper
     unit    — Learn → Examples → On the job → MCQ → Write & self-check → Revise
     weak    — Weak spots & strengths (MCQ accuracy and self-check marks by unit and by skill)
     practice, group, profile — reached from the bottom navigation while in CA mode
   Content: content/ca/<level>/structure.json and unit files (schema in content/ca/README.md).
   Progress lives in ST.ca (localStorage via the app's save()). Written answers are stored as
   "submissions" shaped so they can later be sent to an AI checker (see Ca.submission). */
(function () {
  'use strict';
  const D = document;
  const LEVELS = [['foundation', 'Foundation'], ['inter', 'Intermediate'], ['final', 'Final']];
  const TABS = [['learn', 'Learn'], ['illus', 'Examples'], ['job', 'On the job'], ['mcq', 'MCQ'], ['write', 'Write'], ['revise', 'Revise']];
  const VTABS = TABS.concat([['viva', 'Viva']]);   // Viva (speak & revise) is extra practice — not needed to complete a unit
  const T = () => window.CaTools || null;           // js/ca-tools.js: dashboard, viva, MCQ builder, mock papers, notes, search
  const SKILL = { posting: 'Posting to ledger', balancing: 'Balancing accounts', classification: 'Classifying accounts', computation: 'Computation', presentation: 'Presentation & format',
    concept: 'Concept clarity', application: 'Applying concepts', rectification: 'Rectification entries', provision: 'Quoting the provision', analysis: 'Legal analysis', conclusion: 'Clear conclusion' };
  const cache = { st: {}, unit: {}, mot: null };
  const tap = k => { try { sfx(k); } catch (e) {} };
  const say = m => { try { if (window.A11Y) A11Y.announce(m); } catch (e) {} };
  const fmt = n => (n == null || n === '' ? '' : (typeof n === 'number' ? n.toLocaleString('en-IN', { maximumFractionDigits: 2 }) : String(n)));
  const isCA = () => !!(ST.profile && ST.profile.course === 'ca');
  const DEMO = () => { try { return !!localStorage.getItem('sv_demo'); } catch (e) { return false; } };  // temporary demo login: locked to its course
  const todayISO = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
  function C() {
    ST.ca = ST.ca || {}; const c = ST.ca;
    c.units = c.units || {}; c.mcq = c.mcq || {}; c.writes = c.writes || {}; c.group = c.group || []; c.level = c.level || 'foundation';
    return c;
  }
  async function structure(level) { if (!cache.st[level]) cache.st[level] = await loadJSON(`content/ca/${level}/structure.json`); return cache.st[level]; }
  async function allStructures() { return Promise.all(LEVELS.map(([k]) => structure(k).catch(() => null))); }
  function findUnit(st, uid) {
    for (const p of st.papers) for (const c of p.chapters) for (const u of c.units) if (u.id === uid) return { p, c, u };
    return null;
  }
  const levelOf = uid => ({ fnd: 'foundation', int: 'inter', fin: 'final' })[String(uid).split('-')[0]];
  async function unitData(uid) {
    if (cache.unit[uid]) return cache.unit[uid];
    const st = await structure(levelOf(uid)); const f = findUnit(st, uid);
    if (!f || f.u.status !== 'built') return null;
    cache.unit[uid] = await loadJSON(f.u.file); return cache.unit[uid];
  }
  async function motivation() { if (!cache.mot) { try { cache.mot = await loadJSON('content/ca/motivation.json'); } catch (e) { cache.mot = { general: ['Keep going.'] }; } } return cache.mot; }

  /* ---------- progress ---------- */
  const unitProg = uid => { const u = C().units[uid] || {}; return TABS.filter(([k]) => u[k]).length / TABS.length; };
  function markTab(uid, k) {
    const c = C(); const u = c.units[uid] = c.units[uid] || {};
    if (u[k]) return; u[k] = today(); u.t = today(); c.last = uid; save(); bumpStreak(); addXP(5);
    if (TABS.every(([t]) => u[t])) toast('Unit complete ✓');
  }
  function paperProg(p) { let n = 0, s = 0; p.chapters.forEach(c => c.units.forEach(u => { n++; s += unitProg(u.id); })); return n ? s / n : 0; }
  const builtCount = p => p.chapters.reduce((a, c) => a + c.units.filter(u => u.status === 'built').length, 0);
  const unitCount = p => p.chapters.reduce((a, c) => a + c.units.length, 0);
  function nextUnit(st) {
    let first = null;
    for (const p of st.papers) for (const c of p.chapters) for (const u of c.units) {
      if (u.status !== 'built') continue; if (!first) first = { p, c, u };
      if (unitProg(u.id) < 1) return { p, c, u };
    }
    return first;
  }
  function daysLeft() { const e = C().exam; if (!e) return null; const ms = new Date(e + 'T09:00:00') - new Date(todayISO() + 'T09:00:00'); return Math.round(ms / 864e5); }

  function recordAns(key, ok, ms) {
    const c = C(); const s = c.mcq[key] = c.mcq[key] || { s: 0, w: 0 }; s.s++; if (!ok) s.w++; s.last = today();
    s.ms = (s.ms || 0) + Math.min(ms || 0, 600000);
    c.mlog = c.mlog || []; c.mlog.push([Math.floor(Date.now() / 6e4), key, ok ? 1 : 0, Math.round(Math.min(ms || 0, 600000) / 100) / 10]);
    if (c.mlog.length > 1500) c.mlog.splice(0, c.mlog.length - 1500);
    save();
  }
  /* time studied: a 15-second heartbeat that only counts while the CA screen is visible and was touched in the last minute */
  let lastTouch = Date.now();
  ['pointerdown', 'keydown', 'scroll', 'input'].forEach(e => D.addEventListener(e, () => { lastTouch = Date.now(); }, { passive: true, capture: true }));
  setInterval(() => {
    try {
      if (D.hidden || !isCA() || Date.now() - lastTouch > 60000) return;
      const s = D.getElementById('s-ca'); if (!s || !s.classList.contains('active')) return;
      const c = C(); c.time = c.time || {}; const d = todayISO(); c.time[d] = (c.time[d] || 0) + 15;
      if (c.time[d] % 60 === 0) save();
    } catch (e) {}
  }, 15000);

  /* ---------- small UI helpers ---------- */
  function screen() {
    let s = D.getElementById('s-ca');
    if (!s) { s = D.createElement('section'); s.className = 'screen'; s.id = 's-ca'; D.querySelector('main').appendChild(s); }
    return s;
  }
  function ring(pct, size = 46, label = '') {
    const r = (size - 6) / 2, cf = 2 * Math.PI * r, v = Math.max(0, Math.min(1, pct));
    return `<svg class="ca-ring" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" role="img" aria-label="${esc(label || Math.round(v * 100) + '% done')}"><circle cx="${size / 2}" cy="${size / 2}" r="${r}" class="ca-ring-bg"/>${v > 0 ? '' : '<!--'}<circle cx="${size / 2}" cy="${size / 2}" r="${r}" class="ca-ring-fg" stroke-dasharray="${(cf * v).toFixed(1)} ${cf.toFixed(1)}" transform="rotate(-90 ${size / 2} ${size / 2})"/>${v > 0 ? '' : '-->'}<text x="50%" y="54%" text-anchor="middle" dominant-baseline="middle">${Math.round(v * 100)}%</text></svg>`;
  }
  const bar = pct => `<span class="ca-bar" aria-hidden="true"><i style="width:${Math.round(Math.max(0, Math.min(1, pct)) * 100)}%"></i></span>`;
  const patternChip = p => p.pattern ? `<span class="ca-chip ${p.pattern.mode}">${p.pattern.mode === 'objective' ? 'Objective (MCQ)' : 'Descriptive'} · ${p.pattern.marks} marks · ${p.pattern.hours} h${p.pattern.negative ? ' · −¼ per wrong' : ''}</span>` : (p.group ? `<span class="ca-chip">${esc(p.group)}</span>` : '');
  const paperLabel = p => `Paper ${String(p.key).replace('p', '')}`;
  const levelName = k => (LEVELS.find(l => l[0] === k) || [k, k])[1];

  /* ================= blocks: journal, ledger, trial balance, tables, legal answers ================= */
  function scroller(inner, label) { return `<div class="ca-scroll" role="region" tabindex="0" aria-label="${esc(label)}">${inner}</div>`; }
  function blockHTML(b) {
    const T = b.title ? `<div class="ca-btitle">${esc(b.title)}</div>` : '';
    if (b.t === 'p') return `<p class="ca-p">${esc(b.text)}</p>`;
    if (b.t === 'list') return `<ul class="ca-ul">${b.items.map(x => `<li>${esc(x)}</li>`).join('')}</ul>`;
    if (b.t === 'note') return `<p class="ca-note">${esc(b.text)}</p>`;
    if (b.t === 'wn') return `<div class="ca-wn"><b>${esc(b.title || 'Working note')}</b><p>${esc(b.text)}</p></div>`;
    if (b.t === 'legal') return `<div class="ca-legal">${T}${[['provision', 'Provision'], ['facts', 'Facts'], ['analysis', 'Analysis'], ['conclusion', 'Conclusion']].map(([k, n]) => `<div class="ca-lg ca-lg-${k}"><b>${n}</b><p>${esc(b[k])}</p></div>`).join('')}</div>`;
    if (b.t === 'journal') {
      const rows = b.entries.map(e => {
        const ls = e.lines.map((l, i) => l.dr != null
          ? `<tr class="ca-jdr"><td>${i === 0 ? esc(e.date) : ''}</td><td>${esc(l.ac)} <span class="ca-dr">Dr.</span></td><td></td><td class="n">${fmt(l.dr)}</td><td></td></tr>`
          : `<tr class="ca-jcr"><td></td><td class="ca-to">To ${esc(l.ac)}</td><td></td><td></td><td class="n">${fmt(l.cr)}</td></tr>`).join('');
        return `<tbody class="ca-je">${ls}<tr class="ca-narr"><td></td><td colspan="4">(${esc(e.narr)})</td></tr></tbody>`;
      }).join('');
      return `${T}${scroller(`<table class="ca-t ca-journal"><thead><tr><th scope="col">Date</th><th scope="col">Particulars</th><th scope="col">L.F.</th><th scope="col" class="n">Dr (₹)</th><th scope="col" class="n">Cr (₹)</th></tr></thead>${rows}</table>`, b.title || 'Journal')}`;
    }
    if (b.t === 'ledger') {
      const side = (rows, nm) => {
        const tot = rows.reduce((a, r) => a + r.amt, 0);
        return `<table class="ca-t ca-lside"><caption>${nm} side</caption><thead><tr><th scope="col">Date</th><th scope="col">Particulars</th><th scope="col">J.F.</th><th scope="col" class="n">₹</th></tr></thead><tbody>${rows.map(r => `<tr${r.bal ? ' class="ca-bal"' : ''}><td>${esc(r.date)}</td><td>${esc(r.part)}</td><td></td><td class="n">${fmt(r.amt)}</td></tr>`).join('')}</tbody>${b.open ? '' : `<tfoot><tr><td></td><td></td><td></td><td class="n">${fmt(tot)}</td></tr></tfoot>`}</table>`;
      };
      const nx = b.next ? `<div class="ca-lnext">${esc(b.next.date)} ${b.next.side === 'dr' ? 'To' : 'By'} Balance b/d ₹${fmt(b.next.amt)} (${b.next.side === 'dr' ? 'Dr' : 'Cr'})</div>` : '';
      return `<div class="ca-ledger" role="group" aria-label="${esc(b.ac)}"><div class="ca-lhead"><span>Dr.</span><b>${esc(b.ac)}</b><span>Cr.</span></div><div class="ca-lgrid">${side(b.dr, 'Debit')}${side(b.cr, 'Credit')}</div>${nx}</div>`;
    }
    if (b.t === 'tb') {
      const d = b.rows.reduce((a, r) => a + (r.dr || 0), 0), c = b.rows.reduce((a, r) => a + (r.cr || 0), 0);
      return `${T || `<div class="ca-btitle">Trial Balance as at ${esc(b.date)}</div>`}${scroller(`<table class="ca-t ca-tb"><thead><tr><th scope="col">Ledger account</th><th scope="col" class="n">Dr (₹)</th><th scope="col" class="n">Cr (₹)</th></tr></thead><tbody>${b.rows.map(r => `<tr><td>${esc(r.ac)}</td><td class="n">${fmt(r.dr)}</td><td class="n">${fmt(r.cr)}</td></tr>`).join('')}</tbody><tfoot><tr><td>Total${b.diff ? ' (does not agree)' : ''}</td><td class="n">${fmt(d)}</td><td class="n">${fmt(c)}</td></tr></tfoot></table>`, b.title || 'Trial balance')}`;
    }
    if (b.t === 'cashbook') {
      const side = (rows, nm) => `<table class="ca-t ca-lside ca-cbside"><caption>${nm}</caption><thead><tr><th scope="col">Date</th><th scope="col">Particulars</th><th scope="col">L.F.</th>${b.cols.map(c => `<th scope="col" class="n">${esc(c)} (₹)</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr${r.bal ? ' class="ca-bal"' : ''}><td>${esc(r.date)}</td><td>${esc(r.part)}</td><td>${esc(r.lf || '')}</td>${r.v.map(x => `<td class="n">${x ? fmt(x) : ''}</td>`).join('')}</tr>`).join('')}</tbody>
        <tfoot><tr><td></td><td>Total</td><td></td>${b.cols.map((c, i) => `<td class="n">${fmt(rows.reduce((a, r) => a + (r.v[i] || 0), 0))}</td>`).join('')}</tr></tfoot></table>`;
      const nx = b.next ? `<div class="ca-lnext">${esc(b.next.date)} To Balance b/d — ${b.cols.map((c, i) => b.balanced.includes(i) ? `${esc(c)} ₹${fmt(b.next.v[i])}` : '').filter(Boolean).join(' · ')}</div>` : '';
      return `${T}<div class="ca-ledger ca-cb"><div class="ca-lhead"><span>Dr.</span><b>Cash Book</b><span>Cr.</span></div><div class="ca-lgrid ca-cbgrid">${scroller(side(b.dr, 'Receipts (Dr)'), 'Receipts side')}${scroller(side(b.cr, 'Payments (Cr)'), 'Payments side')}</div>${nx}<p class="ca-note">Discount columns are totalled, not balanced.</p></div>`;
    }
    if (b.t === 'table') {
      const num = new Set(b.num || []);
      const last = b.total ? b.rows.length - 1 : -1;
      return `${T}${scroller(`<table class="ca-t"><thead><tr>${b.head.map((h, i) => `<th scope="col"${num.has(i) ? ' class="n"' : ''}>${esc(h)}</th>`).join('')}</tr></thead><tbody>${b.rows.map((r, ri) => `<tr${ri === last ? ' class="ca-tot"' : ''}>${r.map((x, i) => `<td${num.has(i) || /^[+−-]?[\d,]+(\.\d+)?$/.test(String(x)) ? ' class="n"' : ''}>${esc(x)}</td>`).join('')}</tr>`).join('')}</tbody></table>`, b.title || 'Table')}${b.note ? `<p class="ca-note">${esc(b.note)}</p>` : ''}`;
    }
    return '';
  }
  const blocks = list => (list || []).map(blockHTML).join('');
  const checksHTML = ch => ch && ch.length ? `<details class="ca-checks"><summary>✓ ${ch.length} figure${ch.length > 1 ? 's' : ''} machine-checked</summary><ul>${ch.map(c => `<li>${esc(c.label)}: <code>${esc(c.expr)}</code> = ${fmt(c.value)}</li>`).join('')}</ul></details>` : '';

  /* ================= navigation chrome ================= */
  const NAVLAB = { world: ['🧭', 'Journey'], practice: ['🎯', 'Practice'], cadash: ['📊', 'Dashboard'], squad: ['👥', 'Group'], me: ['👤', 'Profile'] };
  function navLabels() {
    const nav = D.querySelector('nav[aria-label="Main"]') || D.querySelector('nav');
    let db = D.getElementById('caNavDash');
    if (nav && !db) {
      const sq = nav.querySelector('button[data-s="squad"]');
      nav.insertAdjacentHTML(sq ? 'beforeend' : 'beforeend', `<button data-s="cadash" id="caNavDash" hidden><b aria-hidden="true">📊</b>Dashboard</button>`);
      db = D.getElementById('caNavDash'); if (sq) nav.insertBefore(db, sq);
      db.onclick = () => { if (T()) T().dashboard(); };
    }
    if (db) { db.hidden = !isCA(); db.dataset.caOrig = db.innerHTML; D.documentElement.classList.toggle('ca-nav5', isCA()); }
    D.querySelectorAll('nav button[data-s]').forEach(b => {
      if (!b.dataset.caOrig) b.dataset.caOrig = b.innerHTML;
      const L = NAVLAB[b.dataset.s];
      if (isCA() && L) b.innerHTML = `<b aria-hidden="true">${L[0]}</b>${L[1]}`; else b.innerHTML = b.dataset.caOrig;
    });
  }
  function open(navKey) { const s = screen(); navLabels(); show('ca', navKey); return s; }

  /* ================= HOME: CA Journey ================= */
  async function home() {
    const el = open('world'); const c = C();
    el.innerHTML = `<p class="ca-load">Loading your CA journey…</p>`;
    const sts = await allStructures(), mot = await motivation();
    const lvl = c.level, st = sts[LEVELS.findIndex(l => l[0] === lvl)] || sts[0];
    const nx = st && nextUnit(st);
    const dl = daysLeft();
    const h = new Date().getHours(), greet = h < 12 ? 'Good morning' : h < 17 ? 'Good afternoon' : 'Good evening';
    const line = dailyLine(mot, { dl, nx, st });
    el.innerHTML = `<div class="ca-top"><h1 class="ca-h1">${greet}, ${esc(ST.profile.name)}</h1><span class="ca-chip lvl">CA ${esc(levelName(lvl))}</span></div>
      <div class="card ca-mot"><span class="ca-k">Today</span><p>${esc(line)}</p></div>
      ${T() ? T().homeTiles() : ''}
      <div class="ca-row2">
        <div class="card ca-count" id="caCount">${countHTML(dl)}</div>
        ${nx ? `<button class="card ca-next" id="caNext" aria-label="Continue: ${esc(nx.u.title)}"><span class="ca-k">Continue</span><b>${esc(nx.u.title)}</b><small>${esc(paperLabel(nx.p))} · Ch ${nx.c.n} · Unit ${nx.u.n}</small>${bar(unitProg(nx.u.id))}<span class="ca-go">Resume ▶</span></button>` : ''}
      </div>
      <h2 class="ca-h2">Your CA journey</h2>
      <ol class="ca-journey">${LEVELS.map(([k, n], i) => { const s = sts[i]; if (!s) return ''; return `<li class="ca-lvl ${k === lvl ? 'cur' : ''}">
        <details ${k === lvl ? 'open' : ''}><summary><span class="ca-step">${i + 1}</span><span class="ca-lvln"><b>CA ${esc(n)}</b><small>${s.counts.papers} papers · ${s.counts.chapters} chapters · ${s.counts.built ? `${s.counts.built} of ${s.counts.units} units live` : 'coming soon'}</small></span></summary>
        <div class="ca-papers">${s.papers.map((p, pi) => paperCard(k, p, pi, s)).join('')}</div></details></li>`; }).join('')}</ol>
      <div class="card ca-weakmini" id="caWeakMini"></div>
      <div class="card"><h3>Study together</h3><p class="sub">Send a unit's MCQ set to friends. Everyone gets the same questions in the same order — compare scores and explain the misses to each other.</p><button class="btn ghost" id="caGrpGo">Open group study</button></div>`;
    el.querySelectorAll('[data-paper]').forEach(b => b.onclick = () => { tap('open'); paper(b.dataset.level, b.dataset.paper); });
    if (nx) D.getElementById('caNext').onclick = () => { tap('open'); unit(nx.u.id); };
    wireCount();
    D.getElementById('caGrpGo').onclick = groupScreen;
    weakMini(D.getElementById('caWeakMini'));
    if (T()) T().wireHome(el);
  }
  function paperCard(level, p, i, st) {
    const b = builtCount(p), n = unitCount(p), pr = paperProg(p);
    const rec = st.papers.findIndex(x => paperProg(x) < 1 && builtCount(x)) === i;
    return `<button class="ca-paper" data-level="${level}" data-paper="${p.id}" aria-label="${esc(paperLabel(p))}: ${esc(p.name)}. ${b} of ${n} units available. ${Math.round(pr * 100)}% done.">
      ${ring(pr, 46)}<span class="ca-pbody"><small>${esc(paperLabel(p))}${p.group ? ' · ' + esc(p.group) : ''}${rec ? ' · <em>Next up</em>' : ''}</small><b>${esc(p.name)}</b><span class="ca-pmeta">${p.chapters.length} chapters · ${b ? `${b}/${n} units live` : 'Coming soon'}</span></span><span class="ca-chev" aria-hidden="true">›</span></button>`;
  }
  function countHTML(dl) {
    if (dl == null) return `<span class="ca-k">Exam countdown</span><p class="sub">Set your exam date to see the days left and a weekly pace.</p><label class="ca-lab" for="caExam">Exam date</label><input type="date" id="caExam" class="ca-in" min="${todayISO()}"><button class="btn ghost" id="caExamSet">Save date</button>`;
    return `<span class="ca-k">Exam countdown</span><div class="ca-days"><b>${Math.max(0, dl)}</b><span>day${dl === 1 ? '' : 's'} to go</span></div><p class="sub">${esc(new Date(C().exam + 'T00:00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' }))}</p><button class="ca-link" id="caExamEdit">Change date</button>`;
  }
  function wireCount() {
    const box = D.getElementById('caCount'); if (!box) return;
    const set = D.getElementById('caExamSet'), ed = D.getElementById('caExamEdit');
    if (set) set.onclick = () => { const v = D.getElementById('caExam').value; if (!v) { toast('Pick a date first'); return; } C().exam = v; save(); box.innerHTML = countHTML(daysLeft()); wireCount(); say(`${daysLeft()} days to your exam`); };
    if (ed) ed.onclick = () => { box.innerHTML = countHTML(null); const i = D.getElementById('caExam'); i.value = C().exam || ''; wireCount(); i.focus(); };
  }
  function seededPick(list, salt) { if (!list || !list.length) return ''; let a = 0; for (const ch of salt) a = (a * 31 + ch.charCodeAt(0)) >>> 0; return list[a % list.length]; }
  function dailyLine(mot, { dl, nx, st }) {
    const c = C(), d = todayISO(), fill = s => s.replace('{days}', dl).replace('{unit}', nx ? nx.u.title : 'your next unit').replace('{streak}', ST.streak?.n || 0).replace('{weak}', weakest() || 'your weakest topic').replace('{paper}', nx ? nx.p.name : '');
    const lastDay = Object.values(c.units).map(u => u.t || '').sort().pop();
    const gap = lastDay ? Math.round((new Date(d) - new Date(lastDay)) / 864e5) : 0;
    let pool = mot.general;
    if (gap >= 3) pool = mot.comeback;
    else if (dl != null && dl >= 0 && dl <= 45) pool = mot.near;
    else if (weakest() && new Date().getDay() % 2) pool = mot.weak;
    else if ((ST.streak?.n || 0) >= 3 && new Date().getDay() === 1) pool = mot.streak;
    else if (dl != null && dl > 45 && new Date().getDay() === 0) pool = mot.far;
    else if (nx && new Date().getDay() % 3 === 0) pool = mot.next;
    return fill(seededPick(pool && pool.length ? pool : mot.general, d + (ST.profile?.name || '')));
  }

  /* ================= PAPER: chapters → units ================= */
  async function paper(level, pid, q = '') {
    const el = open('world'); const st = await structure(level); const p = st.papers.find(x => x.id === pid); if (!p) return home();
    C().paper = pid; save();
    let lastGroup = null;
    const groups = p.chapters.map(ch => {
      const g = [ch.part, ch.module, ch.sec && p.sections ? `Section ${ch.sec}: ${(p.sections.find(s => s.key === ch.sec) || {}).name || ''}` : ''].filter(Boolean).join(' · ');
      const head = g && g !== lastGroup ? `<h3 class="ca-group">${esc(g)}</h3>` : ''; lastGroup = g || lastGroup;
      const built = ch.units.filter(u => u.status === 'built').length, pr = ch.units.reduce((a, u) => a + unitProg(u.id), 0) / ch.units.length;
      const units = ch.units.map(u => `<li><button class="ca-urow ${u.status}" data-u="${u.id}" ${u.status === 'built' ? '' : 'aria-disabled="true"'} data-search="${esc((u.title + ' ' + (u.topics || []).join(' ')).toLowerCase())}">
          <span class="ca-un">${u.implicit ? '•' : u.n}</span><span class="ca-ub"><b>${esc(u.implicit ? 'Study the chapter' : 'Unit ' + u.n + ': ' + u.title)}</b>${u.topics ? `<small class="ca-topics">${esc(u.topics.slice(0, 6).join(' · '))}${u.topics.length > 6 ? ' …' : ''}</small>` : ''}${u.status === 'built' ? bar(unitProg(u.id)) : '<span class="ca-soon">Coming soon</span>'}</span></button></li>`).join('');
      return `${head}<details class="ca-ch" ${built ? 'open' : ''} data-search="${esc(ch.title.toLowerCase())}"><summary><span class="ca-chn">${ch.sec && p.sections ? ch.sec + '·' : ''}${ch.n}</span><span class="ca-chb"><b>${esc(ch.title)}</b><small>${ch.units.length} unit${ch.units.length > 1 ? 's' : ''}${built ? ` · ${built} live · ${Math.round(pr * 100)}% done` : ' · coming soon'}</small></span></summary><ul class="ca-units">${units}</ul></details>`;
    }).join('');
    const ed = (st.editions || {})[pid] || Object.entries(st.editions || {}).filter(([k]) => k.startsWith(pid)).map(([k, v]) => `${k.endsWith('-A') ? 'Section A' : k.endsWith('-B') ? 'Section B' : ''} ${v}`).join(' · ');
    el.innerHTML = `<button class="back" id="caBack">← CA Journey</button>
      <div class="card ca-phead"><span class="ca-k">CA ${esc(levelName(level))} · ${esc(paperLabel(p))}</span><h1 class="ca-h1">${esc(p.name)}</h1>
        <div class="ca-chips">${patternChip(p)}<span class="ca-chip">${p.chapters.length} chapters · ${unitCount(p)} units</span></div>
        ${p.pattern?.note ? `<p class="sub">${esc(p.pattern.note)}</p>` : ''}${p.note ? `<p class="sub">${esc(p.note)}</p>` : ''}${ed ? `<p class="ca-note">ICAI study material: ${esc(ed)}</p>` : ''}</div>
      <div class="gsearch ca-search"><span aria-hidden="true">🔍</span><input id="caQ" placeholder="Search chapters, units, topics…" autocomplete="off" aria-label="Search in this paper" value="${esc(q)}"></div>
      <p class="ca-none" id="caNone" hidden>No match in this paper.</p>
      <div id="caChs">${groups}</div>`;
    D.getElementById('caBack').onclick = home;
    el.querySelectorAll('.ca-urow').forEach(b => b.onclick = () => { if (b.classList.contains('built')) { tap('open'); unit(b.dataset.u); } else { tap('hmm'); toast('This unit is being written — coming soon'); } });
    const qi = D.getElementById('caQ'); qi.oninput = () => filterPaper(qi.value); if (q) filterPaper(q);
  }
  function filterPaper(v) {
    v = v.trim().toLowerCase(); let any = false;
    D.querySelectorAll('#caChs .ca-ch').forEach(ch => {
      const chHit = !v || ch.dataset.search.includes(v); let uHit = false;
      ch.querySelectorAll('.ca-urow').forEach(u => { const hit = !v || chHit || u.dataset.search.includes(v); u.parentElement.hidden = !hit; if (hit && v) uHit = true; });
      const show_ = !v || chHit || uHit; ch.hidden = !show_; if (v && show_) ch.open = true; if (show_) any = true;
    });
    D.querySelectorAll('#caChs .ca-group').forEach(g => { let n = g.nextElementSibling, vis = false; while (n && !n.classList.contains('ca-group')) { if (!n.hidden) vis = true; n = n.nextElementSibling; } g.hidden = !vis; });
    D.getElementById('caNone').hidden = any;
  }

  /* ================= UNIT ================= */
  let U = null;     // { uid, d, f, tab }
  async function unit(uid, tab) {
    const el = open('world');
    el.innerHTML = `<p class="ca-load">Opening unit…</p>`;
    const d = await unitData(uid); const st = await structure(levelOf(uid)); const f = findUnit(st, uid);
    if (!d || !f) { toast('This unit is not available yet'); return home(); }
    const c = C(); c.last = uid; c.level = levelOf(uid); save();
    U = { uid, d, f, tab: tab || firstOpenTab(uid) };
    renderUnit();
  }
  const firstOpenTab = uid => (TABS.find(([k]) => !(C().units[uid] || {})[k]) || TABS[0])[0];
  function renderUnit() {
    const { d, f, tab } = U, el = screen(), u = C().units[U.uid] || {};
    el.innerHTML = `<button class="back" id="caBack">← ${esc(paperLabel(f.p))} · ${esc(f.p.name)}</button>
      <div class="card ca-uhead"><span class="ca-k">Chapter ${f.c.n}: ${esc(f.c.title)} · Unit ${f.u.n}</span><h1 class="ca-h1">${esc(d.title)}</h1>
        <div class="ca-chips"><span class="ca-chip">${esc({ core: 'Core', moderate: 'Moderate', hard: 'Challenging' }[d.meta.difficulty] || d.meta.difficulty)}</span><span class="ca-chip">Learn ~${d.meta.minutes.learn} min · Practice ~${d.meta.minutes.practice} min</span>${u.write ? '' : ''}</div>
        <div class="ca-uprog">${bar(unitProg(U.uid))}<small>${Math.round(unitProg(U.uid) * 100)}% of this unit done</small></div>
        ${T() ? `<div class="ca-uacts"><button class="ca-link" id="caMyNote" aria-haspopup="dialog">📝 My notes${T().hasNote(U.uid) ? ' ✓' : ''}</button><button class="ca-link" id="caUSearch">🔍 Search</button></div>` : ''}</div>
      <div class="ca-tabs" role="tablist" aria-label="Unit sections">${VTABS.filter(([k]) => k !== 'viva' || (T() && (d.viva || []).length)).map(([k, n], i) => { const dn = k === 'viva' ? T().vivaDone(U.uid) : u[k]; return `<button role="tab" id="caTab-${k}" aria-controls="caPanel" aria-selected="${k === tab}" tabindex="${k === tab ? 0 : -1}" data-k="${k}" class="${dn ? 'done' : ''}${k === 'viva' ? ' ca-vtab' : ''}"><span class="ca-tn" aria-hidden="true">${dn ? '✓' : k === 'viva' ? '🎙' : i + 1}</span>${n}</button>`; }).join('')}</div>
      <div id="caPanel" role="tabpanel" aria-labelledby="caTab-${tab}" tabindex="-1"></div>`;
    D.getElementById('caBack').onclick = () => paper(levelOf(U.uid), f.p.id);
    el.querySelectorAll('.ca-tabs [role=tab]').forEach(b => b.onclick = () => { U.tab = b.dataset.k; tap('tap'); renderUnit(); const t = D.getElementById('caTab-' + U.tab); if (t) t.focus({ preventScroll: true }); });
    const sel = el.querySelector('.ca-tabs [aria-selected=true]'); if (sel && sel.scrollIntoView) sel.scrollIntoView({ block: 'nearest', inline: 'center' });
    const P = D.getElementById('caPanel');
    if (T()) { D.getElementById('caMyNote').onclick = () => T().noteSheet(U.uid, U.d.title); D.getElementById('caUSearch').onclick = () => T().search(''); }
    if (tab === 'viva' && T()) return T().vivaTab(P, U.uid, U.d);
    ({ learn: learnTab, illus: illusTab, job: jobTab, mcq: mcqTab, write: writeTab, revise: reviseTab })[tab](P);
    if (T()) T().applyHL(P, U.uid);
  }
  const saveBtn = (kind, id, title) => T() ? T().saveBtn(U.uid, kind, id, title) : '';
  function nextTabBtn(k) {
    const i = TABS.findIndex(t => t[0] === k), n = TABS[i + 1];
    return n ? `<button class="btn ca-nextbtn" data-next="${n[0]}">Done — next: ${n[1]} ▶</button>` : `<button class="btn ca-nextbtn" data-next="__end">Finish unit ✓</button>`;
  }
  function wireNext(P, k) {
    const b = P.querySelector('.ca-nextbtn'); if (!b) return;
    b.onclick = async () => {
      markTab(U.uid, k);
      if (b.dataset.next === '__end') { const st = await structure(levelOf(U.uid)); const nx = nextUnit(st); toast('Unit finished'); if (nx && nx.u.id !== U.uid) unit(nx.u.id); else paper(levelOf(U.uid), U.f.p.id); return; }
      U.tab = b.dataset.next; renderUnit(); window.scrollTo(0, 0);
    };
  }

  function learnTab(P) {
    const d = U.d;
    P.innerHTML = `<div class="card"><h2 class="ca-h2s">What you will be able to do</h2><ul class="ca-ul">${d.outcomes.map(o => `<li>${esc(o)}</li>`).join('')}</ul>
        ${U.f.u.topics ? `<details class="ca-icai"><summary>ICAI topics covered in this unit</summary><ul class="ca-tlist">${U.f.u.topics.map(t => `<li>${esc(t)}</li>`).join('')}</ul></details>` : ''}
        ${d.meta.exam_tip ? `<p class="ca-tip"><b>Exam tip</b> ${esc(d.meta.exam_tip)}</p>` : ''}</div>
      ${d.concepts.map((c, i) => `<article class="card ca-concept ca-hl" data-ref="concept:${esc(c.id)}" aria-labelledby="caC${i}"><div class="ca-khead"><span class="ca-k">Concept ${i + 1} of ${d.concepts.length}</span>${saveBtn('concept', c.id, c.title)}</div><h2 class="ca-h2s" id="caC${i}">${esc(c.title)}</h2>
        ${c.body.map(x => `<p class="ca-p">${esc(x)}</p>`).join('')}${blocks(c.blocks)}
        <div class="ca-analogy"><b>Think of it like this</b><p>${esc(c.analogy)}</p></div>
        <div class="ca-work"><b>Why it matters in real CA work</b><p>${esc(c.work)}</p></div></article>`).join('')}
      ${nextTabBtn('learn')}`;
    wireNext(P, 'learn');
  }
  function illusTab(P) {
    const d = U.d;
    P.innerHTML = `<p class="ca-intro">Try each one on paper first, then open the solution. Figures are presented the way ICAI expects them in the exam.</p>
      ${d.illustrations.map((x, i) => `<article class="card ca-ill ca-hl" data-ref="illus:${esc(x.id)}"><div class="ca-khead"><span class="ca-k">Illustration ${i + 1} · ${esc({ core: 'Core', moderate: 'Moderate', hard: 'Challenging' }[x.difficulty] || '')} · ~${x.minutes} min</span>${saveBtn('illus', x.id, x.title)}</div><h2 class="ca-h2s">${esc(x.title)}</h2>
        <p class="ca-q">${esc(x.q)}</p>${x.given ? `<details class="ca-given"><summary>Given data</summary>${blocks(x.given)}</details>` : ''}
        <button class="btn ghost ca-reveal" aria-expanded="false" aria-controls="caSol${i}">Show solution</button><div class="ca-sol" id="caSol${i}" hidden><h3 class="ca-h3">Solution</h3>${blocks(x.solution)}${checksHTML(x.checks)}</div></article>`).join('')}
      ${nextTabBtn('illus')}`;
    P.querySelectorAll('.ca-reveal').forEach(b => b.onclick = () => { const s = D.getElementById(b.getAttribute('aria-controls')); const o = s.hidden; s.hidden = !o; b.setAttribute('aria-expanded', String(o)); b.textContent = o ? 'Hide solution' : 'Show solution'; tap('tap'); });
    wireNext(P, 'illus');
  }
  function jobTab(P) {
    P.innerHTML = `<p class="ca-intro">How chartered accountants actually use this unit at work.</p>
      ${U.d.jobs.map((j, i) => `<article class="card ca-job"><span class="ca-role">${esc(j.role)}</span><h2 class="ca-h2s">${esc(j.title)}</h2><p class="ca-p"><b>Situation.</b> ${esc(j.situation)}</p>
        <h3 class="ca-h3">What you do</h3><ol class="ca-ol">${j.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol><p class="ca-take"><b>Takeaway</b> ${esc(j.takeaway)}</p>
        ${j.think ? `<div class="ca-think"><b>Think</b><p>${esc(j.think)}</p><button class="ca-link ca-thinkb" aria-expanded="false" aria-controls="caTh${i}">Show answer</button><p id="caTh${i}" hidden>${esc(j.answer)}</p></div>` : ''}</article>`).join('')}
      ${nextTabBtn('job')}`;
    P.querySelectorAll('.ca-thinkb').forEach(b => b.onclick = () => { const s = D.getElementById(b.getAttribute('aria-controls')); s.hidden = !s.hidden; b.setAttribute('aria-expanded', String(!s.hidden)); b.textContent = s.hidden ? 'Show answer' : 'Hide answer'; });
    wireNext(P, 'job');
  }

  /* ---------- MCQ runner (also used for practice and group study) ---------- */
  function rng(seed) { let a = 2166136261; for (const ch of String(seed)) a = Math.imul(a ^ ch.charCodeAt(0), 16777619) >>> 0; return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  function order(n, seed) { const r = rng(seed), a = Array.from({ length: n }, (_, i) => i); for (let i = n - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  function objectivePaper(uid) { return /^fnd-p[34]-/.test(uid); }
  function runMCQ(host, list, seed, done) {
    let i = 0, right = 0, wrong = 0, qt0 = Date.now(); const t0 = Date.now(), log = [];
    const render = () => {
      const { q, key } = list[i], ord = order(q.options.length, seed + key); qt0 = Date.now();
      host.innerHTML = `<div class="card ca-mcq"><div class="ca-mtop"><span class="ca-k">Question ${i + 1} of ${list.length}</span><span class="ca-k">${right} correct</span></div>${bar(i / list.length)}
        <h2 class="qtext ca-mq">${esc(q.q)}</h2><div class="ca-opts">${ord.map((k, j) => `<button class="opt" data-k="${k}"><span class="ca-ol">${'ABCD'[j]}</span> ${esc(q.options[k])}</button>`).join('')}</div><div id="caMx"></div></div>`;
      host.querySelectorAll('.opt').forEach(b => b.onclick = () => {
        const k = +b.dataset.k, ok = k === q.answer;
        host.querySelectorAll('.opt').forEach(x => { x.disabled = true; if (+x.dataset.k === q.answer) x.classList.add('right'); });
        if (!ok) b.classList.add('wrong');
        ok ? right++ : wrong++; tap(ok ? 'correct' : 'wrong'); const ms = Date.now() - qt0; log.push({ key, ok, ms, pick: k });
        recordAns(key, ok, ms); if (T()) T().reviseMark(key, ok);
        D.getElementById('caMx').innerHTML = `<div class="explain ${ok ? 'good' : 'bad'}"><div class="verdict">${ok ? 'Correct' : `Not quite — answer: ${esc(q.options[q.answer])}`}</div><div class="why">${esc(q.explain)}</div></div>
          <button class="btn ca-mnext" id="caMn">${i < list.length - 1 ? 'Next question ▶' : 'See result ▶'}</button>`;
        D.getElementById('caMn').onclick = () => { i++; if (i < list.length) render(); else done({ right, wrong, total: list.length, ms: Date.now() - t0, log }); };
        D.getElementById('caMn').focus({ preventScroll: true });
      });
    };
    render();
  }
  function mcqTab(P) {
    const d = U.d, list = d.mcqs.map(q => ({ q, key: `${U.uid}#${q.id}` }));
    const obj = objectivePaper(U.uid);
    const prev = list.filter(x => C().mcq[x.key]); const acc = prev.length ? Math.round(prev.reduce((a, x) => a + (C().mcq[x.key].s - C().mcq[x.key].w) / C().mcq[x.key].s, 0) / prev.length * 100) : null;
    P.innerHTML = `<div class="card"><h2 class="ca-h2s">${obj ? 'Exam-style MCQs' : 'Concept check'}</h2><p class="sub">${list.length} questions.${obj ? ' Scored like the exam: +1 for correct, −¼ for wrong.' : ' This paper is descriptive in the exam; these MCQs make sure the concepts behind your written answers are solid.'}${acc != null ? ` Your accuracy so far: ${acc}%.` : ''}</p>
      <button class="btn" id="caMgo">Start ▶</button></div><div id="caMhost"></div>${T() && (d.cases || []).length ? T().casesBlock(U.uid, d) : ''}`;
    if (T()) T().wireCases(P, U.uid, d);
    D.getElementById('caMgo').onclick = () => {
      P.querySelector('.card').remove(); const cb = P.querySelector('.ca-cases'); if (cb) cb.remove(); const seed = 'u' + Date.now().toString(36);
      runMCQ(D.getElementById('caMhost'), list, seed, r => {
        const score = obj ? r.right - r.wrong * 0.25 : r.right;
        D.getElementById('caMhost').innerHTML = `<div class="card ca-res"><h2 class="ca-h2s">${r.right} of ${r.total} correct</h2>${obj ? `<p class="sub">Exam score: ${fmt(score)} / ${r.total} (with negative marking)</p>` : ''}<p class="sub">Time: ${Math.round(r.ms / 1000)} s</p>
          ${r.log.filter(x => !x.ok).length ? `<h3 class="ca-h3">Review these</h3><ul class="ca-ul">${r.log.filter(x => !x.ok).map(x => `<li>${esc(list.find(l => l.key === x.key).q.q)}</li>`).join('')}</ul>` : '<p class="sub">All correct — excellent.</p>'}
          <div class="ca-btns"><button class="btn ghost" id="caMagain">Try again</button><button class="btn ghost" id="caMgrp">Challenge your study group</button></div></div>${nextTabBtn('mcq')}`;
        D.getElementById('caMagain').onclick = () => mcqTab(P);
        D.getElementById('caMgrp').onclick = () => groupCreate(U.uid, { seed, s: r.right, ms: r.ms, k: r.total });
        wireNext(P, 'mcq');
      });
    };
  }

  /* ---------- Write & self-check ---------- */
  function writeTab(P) {
    const d = U.d;
    P.innerHTML = `<p class="ca-intro">Write your answer as you would in the exam, then check it against the model answer and the step-wise marking scheme — the way an examiner marks.</p>
      ${d.questions.map((q, i) => { const h = C().writes[`${U.uid}#${q.id}`] || []; const best = h.length ? Math.max(...h.map(a => a.score)) : null;
        return `<button class="card ca-qrow" data-i="${i}"><span class="ca-qm">${fmt(q.marks)}<small>marks</small></span><span class="ca-qb"><b>Q${i + 1}. ${esc(q.q.length > 140 ? q.q.slice(0, 137) + '…' : q.q)}</b><small>~${q.minutes} min · ${esc(padName(q.pad))}${best != null ? ` · best ${fmt(best)}/${fmt(q.marks)}` : ''}</small></span><span class="ca-chev" aria-hidden="true">›</span></button>`; }).join('')}
      ${nextTabBtn('write')}`;
    P.querySelectorAll('.ca-qrow').forEach(b => b.onclick = () => { tap('open'); pad(P, d.questions[+b.dataset.i], +b.dataset.i); });
    wireNext(P, 'write');
  }
  const padName = k => ({ text: 'Written answer', journal: 'Journal entries', ledger: 'Ledger accounts', tb: 'Trial balance', table: 'Table / statement', legal: 'Legal answer' })[k] || 'Answer';
  const TEMPL = { journal: ['Date', 'Particulars', 'Dr/Cr', 'Amount (₹)'], ledger: ['Side (Dr/Cr)', 'Date', 'Particulars', 'Amount (₹)'], tb: ['Ledger account', 'Dr (₹)', 'Cr (₹)'], table: ['Column 1', 'Column 2', 'Amount (₹)'] };
  function pad(P, q, qi) {
    const key = `${U.uid}#${q.id}`; let secs = 0, timer = null, rows = [];
    const legalStarter = q.pad === 'legal' ? 'Provision:\n\nFacts:\n\nAnalysis:\n\nConclusion:\n' : '';
    const tcols = TEMPL[q.pad];
    P.innerHTML = `<button class="back" id="caPadBack">← All questions</button>
      <div class="card ca-pad"><div class="ca-mtop"><span class="ca-k">Q${qi + 1} · ${fmt(q.marks)} marks · suggested ${q.minutes} min</span><span class="ca-timer" id="caTimer" aria-live="off">00:00</span></div>
        <p class="ca-q">${esc(q.q)}</p>${q.given ? `<details class="ca-given" open><summary>Given</summary>${blocks(q.given)}</details>` : ''}
        <label class="ca-lab" for="caAns">Your answer</label>
        <textarea id="caAns" class="ca-ta" rows="10" placeholder="${q.pad === 'legal' ? 'Write under the four headings…' : 'Write your answer here… (working notes too)'}">${esc(legalStarter)}</textarea>
        <div class="ca-padbar"><span id="caWc">0 words</span><button class="ca-link" id="caTimerBtn">Start timer</button></div>
        ${tcols ? `<details class="ca-tbuild" id="caTb"><summary>Table builder (${esc(padName(q.pad))})</summary><div id="caTbBody"></div></details>` : ''}
        <button class="btn" id="caCheck">Check my answer ▶</button></div><div id="caSelf"></div>`;
    const ta = D.getElementById('caAns'), wc = () => { const n = (ta.value.replace(legalStarter, '').trim().match(/\S+/g) || []).length; D.getElementById('caWc').textContent = `${n} word${n === 1 ? '' : 's'}`; return n; };
    const tick = () => { secs++; const t = D.getElementById('caTimer'); if (!t) { clearInterval(timer); return; } t.textContent = `${String(Math.floor(secs / 60)).padStart(2, '0')}:${String(secs % 60).padStart(2, '0')}`; t.classList.toggle('over', secs > q.minutes * 60); };
    const startT = () => { if (timer) return; timer = setInterval(tick, 1000); D.getElementById('caTimerBtn').textContent = 'Pause timer'; };
    const stopT = () => { clearInterval(timer); timer = null; const b = D.getElementById('caTimerBtn'); if (b) b.textContent = 'Resume timer'; };
    D.getElementById('caTimerBtn').onclick = () => timer ? stopT() : startT();
    ta.oninput = () => { wc(); startT(); };
    D.getElementById('caPadBack').onclick = () => { stopT(); writeTab(P); };
    if (tcols) {
      rows = [Array(tcols.length).fill(''), Array(tcols.length).fill('')];
      const drawTb = () => {
        const amt = tcols.map((c, i) => /₹/.test(c) ? i : -1).filter(i => i >= 0);
        const tot = amt.map(i => rows.reduce((a, r) => a + (parseFloat(String(r[i]).replace(/,/g, '')) || 0), 0));
        let check = '';
        if (q.pad === 'journal' || q.pad === 'ledger') {
          const si = q.pad === 'journal' ? 2 : 0, ai = 3; let dr = 0, cr = 0;
          rows.forEach(r => { const v = parseFloat(String(r[ai]).replace(/,/g, '')) || 0; if (/^c/i.test(String(r[si]).trim())) cr += v; else if (/^d/i.test(String(r[si]).trim())) dr += v; });
          check = `<p class="ca-tbchk ${Math.abs(dr - cr) < .01 && dr ? 'ok' : ''}">Dr total ₹${fmt(dr)} · Cr total ₹${fmt(cr)}${q.pad === 'journal' ? (Math.abs(dr - cr) < .01 && dr ? ' — balanced' : ' — debits and credits must be equal') : ''}</p>`;
        } else if (q.pad === 'tb') check = `<p class="ca-tbchk ${Math.abs(tot[0] - tot[1]) < .01 && tot[0] ? 'ok' : ''}">Dr ₹${fmt(tot[0])} · Cr ₹${fmt(tot[1])}${Math.abs(tot[0] - tot[1]) < .01 && tot[0] ? ' — totals agree' : ''}</p>`;
        D.getElementById('caTbBody').innerHTML = `<div class="ca-scroll" role="region" tabindex="0" aria-label="Table builder"><table class="ca-t ca-tbt"><thead><tr>${tcols.map(c => `<th scope="col">${esc(c)}</th>`).join('')}<th><span class="sr-only">Remove</span></th></tr></thead><tbody>
          ${rows.map((r, ri) => `<tr>${r.map((v, ci) => `<td><input class="ca-cell" data-r="${ri}" data-c="${ci}" value="${esc(v)}" aria-label="Row ${ri + 1}, ${esc(tcols[ci])}" ${/₹/.test(tcols[ci]) ? 'inputmode="decimal"' : ''}></td>`).join('')}<td><button class="ca-x" data-del="${ri}" aria-label="Remove row ${ri + 1}">✕</button></td></tr>`).join('')}</tbody></table></div>
          ${check}<button class="btn ghost" id="caAddRow">+ Add row</button>`;
        D.querySelectorAll('#caTbBody .ca-cell').forEach(inp => inp.oninput = () => { rows[+inp.dataset.r][+inp.dataset.c] = inp.value; startT(); const pos = [inp.dataset.r, inp.dataset.c]; clearTimeout(drawTb.t); drawTb.t = setTimeout(() => { drawTb(); const n = D.querySelector(`#caTbBody .ca-cell[data-r="${pos[0]}"][data-c="${pos[1]}"]`); if (n) { n.focus(); n.setSelectionRange(n.value.length, n.value.length); } }, 700); });
        D.querySelectorAll('#caTbBody .ca-x').forEach(b => b.onclick = () => { rows.splice(+b.dataset.del, 1); if (!rows.length) rows.push(Array(tcols.length).fill('')); drawTb(); });
        D.getElementById('caAddRow').onclick = () => { rows.push(Array(tcols.length).fill('')); drawTb(); const l = D.querySelectorAll('#caTbBody tr'); const inp = l[l.length - 1]?.querySelector('input'); if (inp) inp.focus(); };
      };
      drawTb();
    }
    D.getElementById('caCheck').onclick = () => {
      stopT(); const words = wc();
      const answer = { text: ta.value.replace(legalStarter, '').trim() ? ta.value : '', table: tcols ? { cols: tcols, rows: rows.filter(r => r.some(x => String(x).trim())) } : null };
      if (!answer.text && !(answer.table && answer.table.rows.length)) toast('Nothing written — showing the model answer');
      selfCheck(D.getElementById('caSelf'), q, key, { answer, secs, words });
      D.getElementById('caSelf').scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
  }
  function selfCheck(host, q, key, att) {
    const ticks = {}; q.scheme.forEach(s => ticks[s.id] = 0);
    host.innerHTML = `<div class="card ca-model"><h2 class="ca-h2s">Model answer</h2>${blocks(q.model)}${checksHTML(q.checks)}</div>
      <div class="card ca-scheme"><h2 class="ca-h2s">Mark yourself like an examiner</h2><p class="sub">For each point, compare with your answer: full marks, half, or none. Be strict — examiners are.</p>
        <ol class="ca-pts">${q.scheme.map(s => `<li><div class="ca-pt"><span>${esc(s.pt)}</span><em>${fmt(s.m)} mark${s.m === 1 ? '' : 's'}</em></div>
          <div class="ca-seg" role="radiogroup" aria-label="${esc(s.pt)}">${[[1, 'Full'], [0.5, 'Half'], [0, 'None']].map(([v, n]) => `<button role="radio" aria-checked="${v === 0}" tabindex="${v === 0 ? 0 : -1}" data-s="${s.id}" data-v="${v}">${n}</button>`).join('')}</div></li>`).join('')}</ol>
        <div class="ca-score" aria-live="polite">Your score: <b id="caScore">0</b> / ${fmt(q.marks)}</div>
        <button class="btn" id="caSave">Save my score</button>
        <button class="btn ghost ca-ai" disabled aria-describedby="caAiNote">Send to AI examiner panel</button><p class="ca-note" id="caAiNote">Coming soon: your saved answer can be sent for an independent AI check.</p></div>
      <div class="card ca-exam"><h2 class="ca-h2s">Examiner remarks</h2><ul class="ca-ul">${q.remarks.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
        <h3 class="ca-h3">Common mistakes</h3><ul class="ca-ul ca-miss">${q.mistakes.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
        <h3 class="ca-h3">Presentation tips</h3><ul class="ca-ul">${q.tips.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
        ${hist(key, q)}</div>`;
    const calc = () => q.scheme.reduce((a, s) => a + s.m * ticks[s.id], 0);
    host.querySelectorAll('.ca-seg button').forEach(b => b.onclick = () => {
      ticks[b.dataset.s] = +b.dataset.v;
      b.parentElement.querySelectorAll('button').forEach(x => { const on = x === b; x.setAttribute('aria-checked', String(on)); x.tabIndex = on ? 0 : -1; });
      D.getElementById('caScore').textContent = fmt(Math.round(calc() * 100) / 100);
    });
    D.getElementById('caSave').onclick = () => {
      const score = Math.round(calc() * 100) / 100, c = C();
      const rec = { d: today(), score, max: q.marks, ticks: { ...ticks }, skills: q.scheme.map(s => [s.skill, s.m, s.m * ticks[s.id]]), secs: att.secs, words: att.words,
        text: (att.answer.text || '').slice(0, 6000), table: att.answer.table, status: 'self' };
      const h = c.writes[key] = c.writes[key] || []; h.push(rec); while (h.length > 5) h.shift();
      save(); markTab(U.uid, 'write'); addXP(Math.max(5, Math.round(score / q.marks * 20)));
      toast(`Saved: ${fmt(score)} / ${fmt(q.marks)}`); say(`Score saved, ${score} out of ${q.marks}`);
      const hb = host.querySelector('.ca-hist'); if (hb) hb.outerHTML = hist(key, q); else host.querySelector('.ca-exam').insertAdjacentHTML('beforeend', hist(key, q));
      D.getElementById('caSave').disabled = true; D.getElementById('caSave').textContent = 'Score saved ✓';
    };
  }
  function hist(key, q) {
    const h = C().writes[key] || []; if (!h.length) return '';
    return `<div class="ca-hist"><h3 class="ca-h3">Your attempts</h3><ul class="ca-ul">${h.slice().reverse().map(a => `<li>${esc(a.d)} — ${fmt(a.score)}/${fmt(a.max)}${a.secs ? ` in ${Math.round(a.secs / 60)} min` : ''}${a.words ? ` · ${a.words} words` : ''}</li>`).join('')}</ul></div>`;
  }

  function reviseTab(P) {
    const r = U.d.revision;
    P.innerHTML = `<div class="card ca-rev ca-hl" data-ref="rev:page"><div class="ca-khead"><h2 class="ca-h2s">One-page revision</h2>${saveBtn('rev', 'page', 'One-page revision: ' + U.d.title)}</div><ul class="ca-ul">${r.summary.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
        <h3 class="ca-h3">Must remember</h3><ul class="ca-ul ca-rem">${r.remember.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
        <h3 class="ca-h3">Traps</h3><ul class="ca-ul ca-miss">${r.traps.map(x => `<li>${esc(x)}</li>`).join('')}</ul></div>
      <div class="card"><h2 class="ca-h2s">Quick reference</h2><dl class="ca-qr">${U.d.quickref.map(x => `<div><dt>${esc(x.k)}</dt><dd>${esc(x.v)}</dd></div>`).join('')}</dl></div>
      <div class="ca-btns"><button class="btn ghost" id="caPrint">Print / save as PDF</button><button class="btn ghost" id="caShareU">Share this unit</button></div>
      ${nextTabBtn('revise')}`;
    D.getElementById('caPrint').onclick = () => window.print();
    D.getElementById('caShareU').onclick = () => share(`Study "${U.d.title}" (CA ${levelName(levelOf(U.uid))}) with me on StudyVerse`, link('cau', { u: U.uid }));
    wireNext(P, 'revise');
  }

  /* ================= Weak spots & strengths ================= */
  function weakData() {
    const c = C(), units = {}, skills = {};
    Object.entries(c.mcq).forEach(([k, v]) => { const uid = k.split('#')[0]; const u = units[uid] = units[uid] || { ms: 0, mw: 0, wg: 0, wm: 0 }; u.ms += v.s; u.mw += v.w; });
    Object.entries(c.writes).forEach(([k, h]) => { const uid = k.split('#')[0]; const a = h[h.length - 1]; if (!a) return; const u = units[uid] = units[uid] || { ms: 0, mw: 0, wg: 0, wm: 0 }; u.wg += a.score; u.wm += a.max;
      (a.skills || []).forEach(([sk, m, got]) => { const s = skills[sk] = skills[sk] || { m: 0, g: 0 }; s.m += m; s.g += got; }); });
    return { units, skills };
  }
  const pctOf = u => { const parts = []; if (u.ms) parts.push((u.ms - u.mw) / u.ms); if (u.wm) parts.push(u.wg / u.wm); return parts.length ? parts.reduce((a, b) => a + b, 0) / parts.length : null; };
  function weakest() { const { skills } = weakData(); const l = Object.entries(skills).filter(([, s]) => s.m >= 2).map(([k, s]) => [k, s.g / s.m]).sort((a, b) => a[1] - b[1]); return l.length && l[0][1] < .6 ? (SKILL[l[0][0]] || l[0][0]).toLowerCase() : null; }
  async function weakMini(box) {
    const { units, skills } = weakData(); const ids = Object.keys(units);
    if (!ids.length) { box.innerHTML = `<h3>Weak spots & strengths</h3><p class="sub">Answer some MCQs or self-check a written answer — your strong and weak areas will appear here.</p>`; return; }
    const names = {}; for (const uid of ids) { try { const st = await structure(levelOf(uid)); const f = findUnit(st, uid); if (f) names[uid] = f.u.title; } catch (e) {} }
    const rows = ids.map(id => [id, pctOf(units[id])]).filter(r => r[1] != null).sort((a, b) => a[1] - b[1]);
    box.innerHTML = `<h3>Weak spots & strengths</h3>${rows.slice(0, 3).map(([id, p]) => `<div class="ca-wrow"><span>${esc(names[id] || id)}</span><b class="${p < .6 ? 'w' : p >= .8 ? 's' : ''}">${Math.round(p * 100)}%</b></div>`).join('')}<button class="btn ghost" id="caWeakGo">See full analysis</button>`;
    D.getElementById('caWeakGo').onclick = weakScreen;
  }
  async function weakScreen() {
    const el = open('practice'); const { units, skills } = weakData();
    const names = {}; for (const uid of Object.keys(units)) { try { const f = findUnit(await structure(levelOf(uid)), uid); if (f) names[uid] = f.u.title; } catch (e) {} }
    const band = p => p == null ? ['', 'Not enough data'] : p < .6 ? ['w', 'Weak spot'] : p >= .8 ? ['s', 'Strength'] : ['m', 'Getting there'];
    const urows = Object.entries(units).map(([id, u]) => ({ id, u, p: pctOf(u) })).sort((a, b) => (a.p ?? 2) - (b.p ?? 2));
    const srows = Object.entries(skills).map(([k, s]) => ({ k, s, p: s.m ? s.g / s.m : null })).sort((a, b) => a.p - b.p);
    el.innerHTML = `<button class="back" id="caBack">← CA Journey</button><h1 class="ca-h1 ca-onDark">Weak spots & strengths</h1>
      <div class="card"><h2 class="ca-h2s">By unit</h2>${urows.length ? urows.map(r => { const [cl, lab] = band(r.p); return `<button class="ca-wunit" data-u="${r.id}"><span><b>${esc(names[r.id] || r.id)}</b><small>${r.u.ms ? `MCQ ${Math.round((r.u.ms - r.u.mw) / r.u.ms * 100)}% (${r.u.ms} answers)` : 'No MCQs yet'}${r.u.wm ? ` · Written ${fmt(r.u.wg)}/${fmt(r.u.wm)}` : ''}</small></span><em class="ca-band ${cl}">${lab}</em></button>`; }).join('') : '<p class="sub">No data yet.</p>'}</div>
      <div class="card"><h2 class="ca-h2s">By examiner skill</h2><p class="sub">From your self-checked written answers — which kinds of marks you are winning or losing.</p>
        ${srows.length ? srows.map(r => { const [cl, lab] = band(r.p); return `<div class="ca-skill"><span>${esc(SKILL[r.k] || r.k)}</span>${bar(r.p)}<b class="${cl}">${Math.round(r.p * 100)}%</b></div>`; }).join('') : '<p class="sub">Self-check a written answer to see this.</p>'}
        ${srows.length && srows[0].p < .6 ? `<p class="ca-tip"><b>Focus next</b> ${esc(SKILL[srows[0].k] || srows[0].k)} — practise one written question this week and mark it strictly.</p>` : ''}</div>`;
    D.getElementById('caBack').onclick = home;
    el.querySelectorAll('.ca-wunit').forEach(b => b.onclick = () => unit(b.dataset.u, 'mcq'));
  }

  /* ================= Practice (CA mode) ================= */
  async function practice() {
    if (T() && !practice.daily) return T().practiceHub();
    practice.daily = false;
    const el = open('practice'); const pool = [];
    for (const [k] of LEVELS) { let st; try { st = await structure(k); } catch (e) { continue; }
      for (const p of st.papers) for (const c of p.chapters) for (const u of c.units) { if (u.status !== 'built' || !C().units[u.id]) continue; const d = await unitData(u.id); if (!d) continue;
        d.mcqs.forEach(q => { const key = `${u.id}#${q.id}`, s = C().mcq[key] || { s: 0, w: 0 }; pool.push({ q, key, wgt: 1 + s.w * 4 - Math.min(s.s, 3) * .2 + Math.random() * 2 }); }); } }
    if (!pool.length) { el.innerHTML = `<div class="card"><h2 class="ca-h2s">Daily practice</h2><p class="sub">Open your first unit — its MCQs then join a daily mix that brings back the ones you got wrong.</p><button class="btn" id="caPgo">Go to CA Journey</button></div><div class="card" id="caWeakMini"></div>`; D.getElementById('caPgo').onclick = home; weakMini(D.getElementById('caWeakMini')); return; }
    pool.sort((a, b) => b.wgt - a.wgt); const list = pool.slice(0, 10);
    el.innerHTML = `${T() ? '<button class="back" id="caHubBack">← Practice</button>' : ''}<div class="card"><h2 class="ca-h2s">Daily practice</h2><p class="sub">${list.length} questions from units you have opened. The ones you missed before come first.</p><button class="btn" id="caPstart">Start ▶</button></div><div class="card" id="caWeakMini"></div><div id="caPhost"></div>`;
    weakMini(D.getElementById('caWeakMini')); const hb = D.getElementById('caHubBack'); if (hb) hb.onclick = practice;
    D.getElementById('caPstart').onclick = () => { el.querySelectorAll('.card').forEach(x => x.remove()); runMCQ(D.getElementById('caPhost'), list, 'p' + todayISO(), r => { bumpStreak();
      D.getElementById('caPhost').innerHTML = `<div class="card ca-res"><h2 class="ca-h2s">${r.right} of ${r.total} correct</h2><p class="sub">Come back tomorrow for a fresh mix.</p><button class="btn ghost" id="caPagain">Another round</button></div>`; D.getElementById('caPagain').onclick = () => { practice.daily = true; practice(); }; }); };
  }

  /* ================= Group study (everything lives in the link, like Duels) ================= */
  const b64e = o => btoa(unescape(encodeURIComponent(JSON.stringify(o)))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  const b64d = s => JSON.parse(decodeURIComponent(escape(atob(s.replace(/-/g, '+').replace(/_/g, '/')))));
  const link = (k, o) => `${location.origin}${location.pathname}#${k}=${b64e(o)}`;
  async function share(text, url) {
    try { if (navigator.share) { await navigator.share({ title: 'StudyVerse CA', text, url }); return; } } catch (e) { if (e && e.name === 'AbortError') return; }
    try { await navigator.clipboard.writeText(`${text} ${url}`); toast('Link copied — paste it in your group'); return; } catch (e) {}
    window.open(`https://wa.me/?text=${encodeURIComponent(text + ' ' + url)}`, '_blank');
  }
  async function groupScreen() {
    const el = open('squad'); const sts = await allStructures(); const built = [];
    sts.forEach(st => st && st.papers.forEach(p => p.chapters.forEach(c => c.units.forEach(u => { if (u.status === 'built') built.push({ p, c, u }); }))));
    const past = C().group.slice(-8).reverse();
    el.innerHTML = `<h1 class="ca-h1 ca-onDark">Group study</h1>
      <div class="card"><h2 class="ca-h2s">Challenge your study group</h2><p class="sub">Pick a unit, answer its MCQ set, then send the link. Friends get the same questions in the same order; their score comes back to you by link. No sign-in needed.</p>
        <label class="ca-lab" for="caGU">Unit</label><select id="caGU" class="ca-in">${built.map(b => `<option value="${b.u.id}">${esc(paperLabel(b.p))} · Ch ${b.c.n} · ${esc(b.u.title)}</option>`).join('')}</select>
        <button class="btn" id="caGStart">Set the score ▶</button></div>
      <div class="card"><h2 class="ca-h2s">How to study together</h2><ol class="ca-ol"><li>Everyone reads the same unit (share it from its Revise tab).</li><li>One person sets the MCQ score; others play the same set.</li><li>Meet (or call) and let each person explain one question they got wrong.</li><li>Each writes one descriptive answer and marks a friend's answer with the scheme.</li></ol></div>
      <div class="card"><h2 class="ca-h2s">Recent group results</h2>${past.length ? past.map(g => `<div class="ca-wrow"><span>${esc(g.title || g.u)} · ${esc(g.d)}</span><b>${g.s}/${g.k}${g.vs ? ` vs ${esc(g.vs.n)} ${g.vs.s}/${g.k}` : ''}</b></div>`).join('') : '<p class="sub">No group results yet.</p>'}</div>`;
    D.getElementById('caGStart').onclick = () => groupCreate(D.getElementById('caGU').value);
  }
  async function groupCreate(uid, played) {
    const d = await unitData(uid); if (!d) return;
    const list = d.mcqs.map(q => ({ q, key: `${uid}#${q.id}` }));
    const finish = (seed, s, ms, k) => {
      const id = Math.random().toString(36).slice(2, 10), me = { n: ST.profile?.name || 'Friend' };
      const url = link('cagrp', { v: 1, id, u: uid, seed, n: me.n, s, ms, k });
      C().group.push({ id, u: uid, title: d.title, d: today(), s, ms, k, own: true }); save();
      const el = open('squad');
      el.innerHTML = `<div class="card ca-res"><h2 class="ca-h2s">Your score: ${s}/${k}</h2><p class="sub">in ${Math.round(ms / 1000)} s. Send the set to your study group.</p><button class="btn" id="caGShare">Send to group</button><div style="height:8px"></div><button class="btn ghost" id="caGDone">Done</button></div>`;
      D.getElementById('caGShare').onclick = () => share(`${me.n} scored ${s}/${k} on "${d.title}" (CA). Same questions for you:`, url);
      D.getElementById('caGDone').onclick = groupScreen;
    };
    if (played) return finish(played.seed, played.s, played.ms, played.k);
    const el = open('squad'), seed = 'g' + Date.now().toString(36);
    el.innerHTML = `<div class="card"><h2 class="ca-h2s">${esc(d.title)}</h2><p class="sub">${list.length} questions. Your score and time will be in the link.</p><button class="btn" id="caGGo">Start ▶</button></div><div id="caGHost"></div>`;
    D.getElementById('caGGo').onclick = () => { el.querySelector('.card').remove(); runMCQ(D.getElementById('caGHost'), list, seed, r => finish(seed, r.right, r.ms, r.total)); };
  }
  async function groupAccept(o) {
    const d = await unitData(o.u); const el = open('squad');
    if (!ST.profile) D.documentElement.dataset.age = 'pro';
    D.querySelectorAll('nav').forEach(n => n.style.display = ST.profile ? '' : 'none');
    if (!d) { el.innerHTML = `<div class="card"><h2 class="ca-h2s">Group challenge</h2><p class="sub">This set is not available any more. Ask for a new link.</p></div>`; return; }
    const list = d.mcqs.map(q => ({ q, key: `${o.u}#${q.id}` }));
    el.innerHTML = `<div class="card"><span class="ca-k">Group study · CA</span><h2 class="ca-h2s">${esc(o.n)} challenged you on “${esc(d.title)}”</h2><p class="sub">${list.length} questions, same order for everyone. Their score stays hidden until you finish.</p>
      ${ST.profile ? '' : '<label class="ca-lab" for="caGName">Your name</label><input id="caGName" class="ca-in" maxlength="20" autocomplete="off">'}<button class="btn" id="caGGo">Start ▶</button></div><div id="caGHost"></div>`;
    D.getElementById('caGGo').onclick = () => {
      const nm = ST.profile ? ST.profile.name : (D.getElementById('caGName').value.trim() || 'Friend');
      el.querySelector('.card').remove();
      runMCQ(D.getElementById('caGHost'), list, o.seed, r => {
        const win = r.right > o.s || (r.right === o.s && r.ms < o.ms), tie = r.right === o.s && r.ms === o.ms;
        if (ST.profile) { C().group.push({ id: o.id, u: o.u, title: d.title, d: today(), s: r.right, ms: r.ms, k: r.total, vs: { n: o.n, s: o.s } }); save(); }
        const reply = link('cagrpr', { v: 1, id: o.id, u: o.u, n: nm, s: r.right, ms: r.ms, k: r.total, n0: o.n, s0: o.s, ms0: o.ms });
        D.getElementById('caGHost').innerHTML = `<div class="card ca-res"><h2 class="ca-h2s">${win ? 'You top this round' : tie ? 'A tie' : `${esc(o.n)} tops this round`}</h2>
          <div class="ca-vs"><div><b>${esc(nm)}</b><span>${r.right}/${r.total} · ${Math.round(r.ms / 1000)} s</span></div><div><b>${esc(o.n)}</b><span>${o.s}/${o.k} · ${Math.round(o.ms / 1000)} s</span></div></div>
          <p class="sub">Now discuss the questions either of you missed — that is where the learning is.</p><button class="btn" id="caGReply">Send my result to ${esc(o.n)}</button>
          ${ST.profile ? '' : '<div style="height:8px"></div><button class="btn ghost" id="caGJoin">Start CA on StudyVerse</button>'}</div>`;
        D.getElementById('caGReply').onclick = () => share(`I scored ${r.right}/${r.total} on "${d.title}" (you: ${o.s}/${o.k}).`, reply);
        const j = D.getElementById('caGJoin'); if (j) j.onclick = () => { location.hash = ''; D.querySelectorAll('nav').forEach(n => n.style.display = ''); caSetup(); };
      });
    };
  }
  function groupResult(o) {
    const g = C().group.find(x => x.id === o.id && x.own);
    if (g && !g.vs) { g.vs = { n: o.n, s: o.s }; save(); }
    const el = open('squad');
    el.innerHTML = `<div class="card ca-res"><span class="ca-k">Group study result</span><h2 class="ca-h2s">${esc(o.n)} scored ${o.s}/${o.k}</h2>
      <div class="ca-vs"><div><b>You</b><span>${o.s0}/${o.k} · ${Math.round(o.ms0 / 1000)} s</span></div><div><b>${esc(o.n)}</b><span>${o.s}/${o.k} · ${Math.round(o.ms / 1000)} s</span></div></div>
      <button class="btn" id="caGU2">Open the unit</button><div style="height:8px"></div><button class="btn ghost" id="caGBack">Group study</button></div>`;
    D.getElementById('caGU2').onclick = () => unit(o.u); D.getElementById('caGBack').onclick = groupScreen;
  }

  /* ================= Profile (CA mode) ================= */
  async function profile() {
    const el = open('me'); const c = C(), p = ST.profile;
    const nW = Object.values(c.writes).reduce((a, h) => a + h.length, 0), nM = Object.values(c.mcq).reduce((a, s) => a + s.s, 0), nU = Object.values(c.units).filter(u => TABS.every(([k]) => u[k])).length;
    el.innerHTML = `<div class="card ca-prof"><div class="ca-avatar" aria-hidden="true">${esc((p.name || 'C').trim()[0].toUpperCase())}</div><div><h1 class="ca-h1">${esc(p.name)}</h1><p class="sub">CA ${esc(levelName(c.level))} · ICAI</p></div></div>
      <div class="card statrow"><div><b>${nU}</b><span>Units done</span></div><div><b>${nM}</b><span>MCQs answered</span></div><div><b>${nW}</b><span>Answers self-checked</span></div></div>
      ${T() ? `<div class="card"><h2 class="ca-h2s">Your library</h2><div class="ca-btns"><button class="btn ghost" id="caPNotes">📚 My notes</button><button class="btn ghost" id="caPSearch">🔍 Search everything</button></div></div>` : ''}
      ${DEMO() ? '' : `<div class="card"><h2 class="ca-h2s">Current level</h2><div class="ca-seg ca-segw" role="radiogroup" aria-label="CA level">${LEVELS.map(([k, n]) => `<button role="radio" aria-checked="${k === c.level}" tabindex="${k === c.level ? 0 : -1}" data-l="${k}">${n}</button>`).join('')}</div></div>`}
      <div class="card"><h2 class="ca-h2s">Exam date</h2><label class="ca-lab" for="caExamP">Your next CA exam</label><input type="date" id="caExamP" class="ca-in" value="${esc(c.exam || '')}"><button class="btn ghost" id="caExamPS">Save</button></div>
      <div class="card"><h2 class="ca-h2s">Name</h2><label class="ca-lab" for="caNm">Shown on your journey and group results</label><input id="caNm" class="ca-in" maxlength="24" value="${esc(p.name)}" autocomplete="off"><button class="btn ghost" id="caNmS">Save</button></div>
      ${DEMO() ? '' : `<div class="card"><h2 class="ca-h2s">Switch course</h2><p class="sub">Your CA progress is kept if you switch.</p><button class="btn ghost" id="caToSchool">Go to school mode (Grades 1–12)</button></div>`}
      <div class="card"><button class="btn ghost" onclick="openSound()">Sound settings</button><div style="height:8px"></div><button class="btn ghost" id="caReset">Erase all progress</button></div>`;
    el.querySelectorAll('.ca-segw button').forEach(b => b.onclick = () => { c.level = b.dataset.l; save(); profile(); toast(`CA ${levelName(c.level)} selected`); });
    D.getElementById('caExamPS').onclick = () => { c.exam = D.getElementById('caExamP').value || null; save(); toast(c.exam ? 'Exam date saved' : 'Exam date cleared'); };
    D.getElementById('caNmS').onclick = () => { const v = D.getElementById('caNm').value.trim(); if (v) { p.name = v; save(); toast('Name saved'); } };
    if (!DEMO()) D.getElementById('caToSchool').onclick = toSchool;
    if (T()) { D.getElementById('caPNotes').onclick = () => T().notes(); D.getElementById('caPSearch').onclick = () => T().search(''); }
    D.getElementById('caReset').onclick = function () { if (this.dataset.sure) { localStorage.removeItem('sv_state'); location.reload(); } else { this.dataset.sure = 1; this.textContent = 'Tap again to erase everything'; } };
  }
  function toSchool() {
    const p = ST.profile; p.course = null; save(); navLabels(); D.querySelectorAll('nav button.on').forEach(b => b.classList.remove('on'));
    if (window.Look) Look.apply();
    if (!p.grade || !p.board) { onboardOrig(2, { board: p.board || 'cbse' }); return; }
    setGrade(p.grade); worldScreen();
  }

  /* ================= Setup: Professional courses → CA ================= */
  function caSetup(step = 1, draft = {}) {
    show('onboard'); const el = D.getElementById('s-onboard'); D.documentElement.dataset.age = 'pro';
    if (step === 1) {
      el.innerHTML = `<div class="ob ca-ob"><h1>CA — Chartered Accountancy</h1><p>Study material structure as per ICAI. Pick where you are in the journey.</p>
        <div class="card">${LEVELS.map(([k, n], i) => `<button class="choice ca-lvlpick" data-l="${k}"><b>${i + 1}. CA ${n}</b><small>${['4 papers · the entry level', '6 papers in two groups', '6 papers in two groups'][i]}</small></button>`).join('')}</div>
        <button class="btn ghost" id="caObBack">← Back</button></div>`;
      el.querySelectorAll('.ca-lvlpick').forEach(b => b.onclick = () => { tap('tap'); caSetup(2, { ...draft, level: b.dataset.l }); });
      D.getElementById('caObBack').onclick = () => { if (window.Look) Look.apply(); ST.profile ? (isCA() ? home() : meScreen()) : onboardOrig(1); };
    } else {
      el.innerHTML = `<div class="ob ca-ob"><h1>Almost there</h1>
        <div class="card"><label class="ca-lab" for="caObName">Your name</label><input id="caObName" class="ca-in" maxlength="24" autocomplete="off" value="${esc(ST.profile?.name || '')}">
        <label class="ca-lab" for="caObExam">Exam date (optional — you can set it later)</label><input type="date" id="caObExam" class="ca-in" min="${todayISO()}"></div>
        <button class="btn" id="caObGo">Start my CA journey ▶</button><div style="height:8px"></div><button class="btn ghost" id="caObBack">← Back</button></div>`;
      D.getElementById('caObBack').onclick = () => caSetup(1, draft);
      D.getElementById('caObGo').onclick = () => {
        const name = D.getElementById('caObName').value.trim() || 'Student';
        const prev = ST.profile || {};
        ST.profile = { ...prev, name, avatar: prev.avatar || '🎓', course: 'ca', grade: prev.grade || 12, board: prev.board || 'cbse' };
        const c = C(); c.level = draft.level || 'foundation'; const ex = D.getElementById('caObExam').value; if (ex) c.exam = ex;
        save(); tap('unlock'); if (window.Look) Look.apply(); home();
      };
    }
  }

  /* ================= hooks into the app ================= */
  const onboardOrig = onboard;
  onboard = function (step = 1, draft = {}) {
    const r = onboardOrig.apply(this, arguments);
    if (step === 1) {
      const card = (D.querySelector('#s-onboard .choice[data-b]') || {}).closest?.('.card') || D.querySelector('#s-onboard .ob .card');
      if (card && !D.getElementById('caEntry')) card.insertAdjacentHTML('afterend', `<div class="card ca-entry" id="caEntry"><h3>Professional courses</h3><button class="choice ca-entryb" id="caEntryB"><b>CA — Chartered Accountancy (ICAI)</b><small>Foundation · Intermediate · Final</small></button></div>`);
      const b = D.getElementById('caEntryB'); if (b) b.onclick = () => { tap('tap'); caSetup(1); };
    }
    return r;
  };
  const _world = worldScreen;
  worldScreen = async function () { if (isCA()) return home(); navLabels(); return _world.apply(this, arguments); };
  const _practice = practiceScreen;
  practiceScreen = async function () { if (isCA()) return practice(); navLabels(); return _practice.apply(this, arguments); };
  const _squad = squadScreen;
  squadScreen = function () { if (isCA()) return groupScreen(); navLabels(); return _squad.apply(this, arguments); };
  const _me = meScreen;
  meScreen = function () {
    if (isCA()) return profile();
    navLabels(); const r = _me.apply(this, arguments);
    const host = D.getElementById('s-me');
    if (host && !D.getElementById('caMeCard')) host.insertAdjacentHTML('beforeend', `<div class="card" id="caMeCard"><h3>Professional courses</h3><p class="sub">Preparing for CA (ICAI)? Switch to the professional CA interface — your school progress is kept.</p><button class="btn ghost" id="caMeGo">CA — Chartered Accountancy</button></div>`);
    const b = D.getElementById('caMeGo'); if (b) b.onclick = () => { if (ST.ca && ST.ca.level) { ST.profile.course = 'ca'; save(); if (window.Look) Look.apply(); home(); } else caSetup(1); };
    return r;
  };

  /* links: #cau=… (open a unit), #cagrp=… (group challenge), #cagrpr=… (result) */
  function route() {
    const m = /^#(cau|cagrp|cagrpr)=(.+)$/.exec(location.hash); if (!m) return false;
    let o; try { o = b64d(m[2]); } catch (e) { return false; }
    history.replaceState(null, '', location.pathname + location.search);
    if (m[1] === 'cau') { if (!isCA() && ST.profile) { /* school user: open the unit in CA view for this visit */ } unit(o.u); }
    else if (m[1] === 'cagrp') groupAccept(o); else groupResult(o);
    return true;
  }
  window.addEventListener('hashchange', route);
  function boot() {
    if (/^#(cau|cagrp|cagrpr)=/.test(location.hash)) { setTimeout(route, 80); return; }
    if (isCA()) { const s = D.querySelector('.screen.active'); if (!s || s.id === 's-world' || s.id === 's-onboard') home(); else navLabels(); }
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', () => setTimeout(boot, 0)); else setTimeout(boot, 0);

  window.Ca = { home, paper, unit, weak: weakScreen, group: groupScreen, setup: caSetup, profile, isCA,
    /* Shape of a written answer for a future AI checker panel (backend). */
    submission(uid, qid, i = -1) { const h = C().writes[`${uid}#${qid}`] || []; const a = h.at(i); if (!a) return null;
      return { schema: 'ca-submission/1', unit: uid, question: qid, marks: a.max, answer: { text: a.text, table: a.table }, self: { score: a.score, ticks: a.ticks }, meta: { secs: a.secs, words: a.words, date: a.d, app: 'studyverse' }, status: a.status }; },
    _blockHTML: blockHTML,
    /* internals shared with js/ca-tools.js */
    _: { C, LEVELS, TABS, SKILL, structure, allStructures, findUnit, levelOf, unitData, unitProg, paperProg, builtCount, unitCount, daysLeft, todayISO,
      screen, open, ring, bar, blocks, checksHTML, fmt, tap, say, paperLabel, levelName, rng, order, recordAns, weakData, pctOf, selfSchemeHTML: null,
      practiceDaily: () => { practice.daily = true; practice(); }, weakScreen, nextUnit, isCA } };
})();
