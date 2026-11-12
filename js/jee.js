/* JEE course (pilot) — JEE Main tracks for Class 9–12, droppers and eligible college students.
   Content: content/jee/<subject>/uNN.json (+ -practice.json). Real NTA questions carry year/date/shift; every
   practice question is our own, generated from a template and re-solved by an independent checker at build time.
   Progress is earned only by answering — nothing can be self-marked. */
(function () {
  const D = document, $ = s => D.querySelector(s);
  const tap = k => { try { sfx(k || 'tap'); } catch (e) {} };
  const J = () => { if (!ST.jee) ST.jee = { units: {}, mist: [] }; ST.jee.units = ST.jee.units || {}; ST.jee.mist = ST.jee.mist || []; return ST.jee; };
  const U = uid => { const j = J(); return j.units[uid] || (j.units[uid] = { cards: {}, ans: {}, tests: [] }); };
  const NOW = () => new Date();
  const EXAM = 2027, S1 = '2027-01-20', S2 = '2027-04-02';

  /* ---------- tiny math markup: ^{} _{} \f{a}{b} √{} ---------- */
  function mx(s) {
    s = String(s == null ? '' : s); let out = '', i = 0;
    const grp = j => { let d = 0, k = j; for (; k < s.length; k++) { if (s[k] === '{') d++; else if (s[k] === '}') { d--; if (!d) break; } } return [s.slice(j + 1, k), k + 1]; };
    while (i < s.length) {
      if (s.startsWith('\\f{', i)) { const [a, j] = grp(i + 2); const [b, k] = grp(j); out += `<span class="jx-fr"><span>${mx(a)}</span><span>${mx(b)}</span></span>`; i = k; continue; }
      if ((s[i] === '^' || s[i] === '_') && s[i + 1] === '{') { const [a, j] = grp(i + 1); out += s[i] === '^' ? `<sup>${mx(a)}</sup>` : `<sub>${mx(a)}</sub>`; i = j; continue; }
      if (s[i] === '√' && s[i + 1] === '{') { const [a, j] = grp(i + 1); out += `√<span class="jx-sq">${mx(a)}</span>`; i = j; continue; }
      out += s[i]; i++;
    }
    return out;
  }

  /* ---------- syllabus (NTA JEE Main 2027 = 2025/2026, unchanged) ---------- */
  const SUBJ = {
    phy: { n: 'Physics', e: '⚛️', c: '#6d5dfc', u: [['Units and Measurements', 11], ['Kinematics', 11], ['Laws of Motion', 11], ['Work, Energy and Power', 11], ['Rotational Motion', 11], ['Gravitation', 11], ['Properties of Solids and Liquids', 11], ['Thermodynamics', 11], ['Kinetic Theory of Gases', 11], ['Oscillations and Waves', 11], ['Electrostatics', 12], ['Current Electricity', 12], ['Magnetic Effects of Current and Magnetism', 12], ['Electromagnetic Induction and Alternating Currents', 12], ['Electromagnetic Waves', 12], ['Optics', 12], ['Dual Nature of Matter and Radiation', 12], ['Atoms and Nuclei', 12], ['Electronic Devices', 12], ['Experimental Skills', '11–12']] },
    chem: { n: 'Chemistry', e: '🧪', c: '#0ea5a4', u: [['Some Basic Concepts in Chemistry', 11], ['Atomic Structure', 11], ['Chemical Bonding and Molecular Structure', 11], ['Chemical Thermodynamics', 11], ['Solutions', 12], ['Equilibrium', 11], ['Redox Reactions and Electrochemistry', '11–12'], ['Chemical Kinetics', 12], ['Classification of Elements and Periodicity', 11], ['p-Block Elements', '11–12'], ['d- and f-Block Elements', 12], ['Coordination Compounds', 12], ['Purification and Characterisation of Organic Compounds', 11], ['Some Basic Principles of Organic Chemistry', 11], ['Hydrocarbons', 11], ['Organic Compounds Containing Halogens', 12], ['Organic Compounds Containing Oxygen', 12], ['Organic Compounds Containing Nitrogen', 12], ['Biomolecules', 12], ['Principles Related to Practical Chemistry', '11–12']] },
    math: { n: 'Mathematics', e: '📐', c: '#f97316', u: [['Sets, Relations and Functions', '11–12'], ['Complex Numbers and Quadratic Equations', 11], ['Matrices and Determinants', 12], ['Permutations and Combinations', 11], ['Binomial Theorem', 11], ['Sequence and Series', 11], ['Limit, Continuity and Differentiability', '11–12'], ['Integral Calculus', 12], ['Differential Equations', 12], ['Coordinate Geometry', 11], ['Three Dimensional Geometry', '11–12'], ['Vector Algebra', 12], ['Statistics and Probability', '11–12'], ['Trigonometry', 11]] },
  };
  const READY = { 'phy-u01': { pyq: 76, prac: 912 }, 'phy-u12': { pyq: 31, prac: 366 }, 'phy-u17': { pyq: 46, prac: 552 }, 'chem-u02': { pyq: 46, prac: 552 }, 'chem-u08': { pyq: 47, prac: 564 }, 'chem-u01': { pyq: 48, prac: 576 }, 'math-u06': { pyq: 39, prac: 468 }, 'math-u03': { pyq: 32, prac: 384 }, 'phy-u06': { pyq: 44, prac: 524 }, 'phy-u11': { pyq: 69, prac: 828 }, 'phy-u08': { pyq: 40, prac: 480 }, 'phy-u09': { pyq: 28, prac: 336 }, 'phy-u15': { pyq: 34, prac: 408 } };
  const uidOf = (s, i) => `${s}-u${String(i + 1).padStart(2, '0')}`;
  const unitName = uid => { const [s, n] = uid.split('-u'); return SUBJ[s].u[+n - 1][0]; };
  const FOUND = [ // Class 9–10 bridge chapters that lead into JEE units
    ['phy-u01', 'Measurement, units and significant figures'], ['f-motion', 'Motion (Class 9)'], ['f-force', 'Force and laws of motion (Class 9)'], ['f-grav', 'Gravitation (Class 9)'], ['f-work', 'Work and energy (Class 9)'],
    ['f-light', 'Light: reflection and refraction (Class 10)'], ['f-elec', 'Electricity (Class 10)'], ['f-mag', 'Magnetic effects of current (Class 10)'], ['f-atom', 'Atoms, molecules and the mole (Class 9)'], ['f-acid', 'Acids, bases and salts (Class 10)'],
    ['f-carbon', 'Carbon and its compounds (Class 10)'], ['f-poly', 'Polynomials and quadratic equations (Class 9–10)'], ['f-trig', 'Introduction to trigonometry (Class 10)'], ['f-coord', 'Coordinate geometry (Class 9–10)'], ['f-ap', 'Arithmetic progressions (Class 10)']];
  const TRACKS = { found: { n: 'JEE Foundation', e: '🌱', d: 'Class 9–10 · build the base, one concept at a time' }, main: { n: 'JEE Main track', e: '🚀', d: 'Class 11–12 · in step with your school chapters' }, full: { n: 'Full-power year', e: '⚡', d: 'Droppers & eligible college students · full syllabus, exam mode' } };

  /* ---------- eligibility (NTA JEE Main 2027 bulletin §3.1–3.3; JEE Advanced: 2026 rules, IIT Roorkee) ---------- */
  function elig(x) {
    const xii = x.status === 'school' ? EXAM + (12 - x.cls) : +x.first || 0, pass = x.status === 'school' ? xii : +(x.pass || x.first) || 0;
    const r = { xii, main: {}, adv: {}, notes: [] };
    if (!xii) return r;
    const mainYears = [pass, pass + 1, pass + 2].filter(y => y >= EXAM || x.status !== 'school');
    if (x.status === 'school' && xii > EXAM) { r.main = { ok: null, first: xii, years: [xii, xii + 1, xii + 2], why: `Your first chance is JEE Main ${xii} (the year you appear for Class XII). You can sit it in ${xii}, ${xii + 1} and ${xii + 2}.` }; }
    else if (pass >= EXAM - 2) r.main = { ok: true, years: [pass, pass + 1, pass + 2].filter(y => y >= EXAM), why: x.status === 'school' ? 'You appear for Class XII in 2027 — eligible for JEE Main 2027, and also 2028 and 2029.' : `Class XII passed in ${pass} — eligible for JEE Main ${[pass, pass + 1, pass + 2].filter(y => y >= EXAM).join(', ')}.` };
    else r.main = { ok: false, why: `Class XII was first passed in ${pass}. JEE Main 2027 accepts only those who passed in 2025 or 2026, or appear in 2027. Passing year = the year the result first said "pass"; improvement exams do not reset it.` };
    if (x.pcm === false) r.notes.push('B.E./B.Tech admission needs Physics and Mathematics in Class XII (with Chemistry, Biology, a technical vocational subject or similar as the third subject for most institutes) — check the institute you want.');
    // JEE Advanced (expected for the year you sit it, pattern of the 2026 rules)
    const advFirst = xii, advYears = [advFirst, advFirst + 1];
    if (x.status === 'school') r.adv = { ok: xii === EXAM ? true : null, years: advYears, why: `If you are in the top 2,50,000 of JEE Main, you can take JEE Advanced in ${advYears[0]} and ${advYears[1]} — two attempts, in consecutive years starting from your Class XII year.` };
    else {
      const left = advYears.filter(y => y >= EXAM);
      if (!left.length) r.adv = { ok: false, why: `JEE Advanced allows only the Class XII year and the next year (${advYears.join(' and ')}). Those are over.` };
      else if (x.iit) r.adv = { ok: false, why: 'A candidate who already accepted an IIT seat (reported online / joined) cannot appear again.' };
      else if ((+x.advTried || 0) >= 2) r.adv = { ok: false, why: 'Two attempts at JEE Advanced are already used.' };
      else {
        let ok = true, why = `JEE Advanced ${left.join(' / ')} — needs a top-2,50,000 JEE Main rank.`;
        if (x.dob) { const lim = new Date(`${left[0] - 25 + (x.relax ? -5 : 0)}-10-01`); if (new Date(x.dob) < lim) { ok = false; why = `Age rule: you must be born on or after 1 October ${left[0] - 25 + (x.relax ? -5 : 0)}${x.relax ? ' (SC/ST/PwD: 5-year relaxation applied)' : ''}.`; } }
        r.adv = { ok, years: left, why };
      }
    }
    r.notes.push('For IIT/NIT/IIIT seats (JoSAA) you also need 75% in Class XII (65% for SC/ST/PwD) or a place in the top 20 percentile of your board.');
    return r;
  }

  /* ---------- data ---------- */
  const CACHE = {};
  async function data(uid) {
    if (CACHE[uid]) return CACHE[uid];
    const [s, n] = uid.split('-'); const base = `content/jee/${s}/${n}`;
    const [a, b] = await Promise.all([loadJSON(base + '.json'), loadJSON(base + '-practice.json')]);
    const byId = {}; a.pyq.forEach(q => { q.kind = 'pyq'; byId[q.id] = q; }); b.items.forEach(q => { q.kind = 'prac'; byId[q.id] = q; });
    return (CACHE[uid] = { ...a, prac: b.items, byId });
  }

  /* ---------- screen ---------- */
  function screen(nav) {
    let s = D.getElementById('s-jee');
    if (!s) { s = D.createElement('section'); s.className = 'screen'; s.id = 's-jee'; D.querySelector('main').appendChild(s); }
    show('jee', nav || (NAVP ? 'practice' : 'world')); return s;
  }
  let NAVP = false;   // true while the student is inside the JEE Practice hub (bank, crash course) — keeps the Practice tab lit
  const here = (...a) => { try { Nav.here('jee', a); } catch (e) {} };
  const srcTag = s => `JEE Main ${s.y} · ${new Date(s.d + 'T00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })} · Shift ${s.sh}`;
  const pct = (a, b) => b ? Math.round(100 * a / b) : 0;

  function stats(uid, d) {
    const u = U(uid), ans = u.ans, ids = Object.keys(ans);
    const first = ids.filter(k => ans[k].f === 1).length, tried = ids.length;
    const topic = {}; ids.forEach(k => { const q = d && d.byId[k]; if (!q) return; const t = topic[q.t] || (topic[q.t] = { a: 0, r: 0 }); t.a++; if (ans[k].ok) t.r++; });
    const cardsOk = Object.keys(u.cards).length, best = Math.max(0, ...u.tests.map(t => t.pct));
    const prog = Math.round(30 * Math.min(1, cardsOk / ((d && d.cards && d.cards.length) || 10)) + 40 * Math.min(1, first / 60) + 30 * best / 100);
    return { first, tried, topic, cardsOk, best, prog, pyqDone: ids.filter(k => k[0] === 'p' && !k.includes('-v')).length };
  }

  /* ================= HOME ================= */
  function home() {
    NAVP = false; const j = J(); if (!j.track) return setup(1);
    here('home'); const el = screen();
    const tr = TRACKS[j.track], e = j.elig || {}, xii = (e.xii) || EXAM;
    const days = Math.ceil((new Date(S1) - NOW()) / 864e5);
    const mainChip = e.main ? (e.main.ok === true ? `<span class="jx-chip ok">JEE Main ${(e.main.years || [EXAM])[0]} ✓</span>` : e.main.ok === null ? `<span class="jx-chip">First JEE Main: ${e.main.first}</span>` : `<span class="jx-chip no">Not eligible for JEE Main 2027</span>`) : '';
    const advChip = e.adv && e.adv.ok !== undefined ? (e.adv.ok === false ? `<span class="jx-chip no">JEE Advanced ✗</span>` : `<span class="jx-chip ${e.adv.ok ? 'ok' : ''}">JEE Advanced ${(e.adv.years || []).join('/')}</span>`) : '';
    const LU = READY[j.last] ? j.last : 'phy-u01', st = stats(LU, CACHE[LU]);
    el.innerHTML = `<div class="jx">
      <div class="jx-hero"><div class="jx-ht"><span class="jx-badge">${tr.e} ${tr.n}</span><button class="jx-lnk" id="jxSwitch">Change</button></div>
        <h1>${esc(ST.profile && ST.profile.name ? ST.profile.name.split(' ')[0] + ', ' : '')}your road to JEE</h1>
        <p>${j.track === 'found' ? `Class ${j.cls} → your first JEE Main is in <b>January ${xii}</b>. Every concept you master now is one less to rush later.` : xii === EXAM && days > 0 ? `<b>${days} days</b> to JEE Main 2027 Session 1 (20 Jan). Session 2: 2–7 April.` : `Target: <b>JEE Main ${Math.max(EXAM, xii)}</b>.`}</p>
        <div class="jx-chips">${mainChip}${advChip}<button class="jx-chip lnk" id="jxElig">Check eligibility</button></div></div>
      <div class="jx-card jx-next"><div><small>Continue</small><b>${SUBJ[LU.split('-')[0]].e} ${esc(unitName(LU))}</b><span>${st.prog}% mastered · ${st.first} solved first time · ${READY[LU].pyq} real JEE questions</span></div><button class="jx-btn" id="jxGo">Open ▶</button></div>
      <details class="jx-sec" data-sec="path" ${secOpen('path', true)}><summary><h2 class="jx-h">${j.track === 'found' ? '🌱 Foundation path' : j.track === 'main' ? `🧭 Your path — Class ${j.cls} first` : '⚡ Full syllabus — recommended order'}</h2><small>${path(j).filter(x => READY[x[0]]).length}/${path(j).length} ready</small></summary>
      <div class="jx-path">${path(j).map(([uid, name, tag], i) => `<button class="jx-pu ${READY[uid] ? 'on' : ''}" data-u="${uid}"><span class="jx-pn">${i + 1}</span><span><b>${esc(name)}</b><small>${tag}</small></span><span class="jx-st">${READY[uid] ? 'Ready' : '🔨 Building'}</span></button>`).join('')}</div></details>
      <details class="jx-sec" data-sec="syl" ${secOpen('syl', false)}><summary><h2 class="jx-h">📚 Full JEE Main syllabus</h2><small>${Object.keys(READY).length}/${Object.values(SUBJ).reduce((a, x) => a + x.u.length, 0)} units ready</small></summary>
      <div class="jx-subs">${Object.entries(SUBJ).map(([k, s]) => `<details class="jx-sub" style="--c:${s.c}"><summary><span>${s.e}</span><b>${s.n}</b><small>${s.u.length} units · ${s.u.filter((_, i) => READY[uidOf(k, i)]).length} ready</small></summary>
        ${s.u.map((u, i) => { const id = uidOf(k, i); return `<button class="jx-ur ${READY[id] ? 'on' : ''}" data-u="${id}"><span>Unit ${i + 1}</span><b>${esc(u[0])}</b><small>Class ${u[1]}</small><em>${READY[id] ? 'Ready ▶' : 'Building'}</em></button>`; }).join('')}</details>`).join('')}</div></details>
      <button class="jx-card jx-adv" id="jxAdv"><span>🏔️</span><span><b>JEE Advanced</b><small>Paper 1 · Paper 2 — coming soon</small></span><em>Soon</em></button>
      <div class="jx-tools"><button id="jxPat">📋 Exam pattern</button><button id="jxMist">📕 Mistake book (${j.mist.length})</button><button id="jxSchool">🏫 School world</button></div>
      <p class="jx-fine">Real questions are from JEE Main papers, tagged with date and shift; all solutions and extra questions are written by StudyVerse. Rules: NTA JEE Main 2027 Information Bulletin.</p></div>`;
    el.querySelectorAll('details.jx-sec').forEach(d => d.ontoggle = () => { const u = J().ui || (J().ui = {}); u[d.dataset.sec] = d.open; save(); });
    $('#jxGo').onclick = () => { tap('open'); unit(LU); };
    $('#jxElig').onclick = () => { tap(); eligScreen(); };
    $('#jxSwitch').onclick = () => { tap(); setup(1, { again: true }); };
    $('#jxAdv').onclick = () => { tap(); advanced(); };
    $('#jxPat').onclick = () => { tap(); pattern(); };
    $('#jxMist').onclick = () => { tap(); mistakes(); };
    $('#jxSchool').onclick = () => { tap(); J().home = false; save(); toast('School world is home now — JEE stays in Practice and Me'); worldScreen(); };
    el.querySelectorAll('[data-u]').forEach(b => b.onclick = () => { const u = b.dataset.u; if (READY[u]) { tap('open'); unit(u); } else { tap(); toast('This unit is being built — Units and Measurements is ready now'); } });
    if (!CACHE[LU]) data(LU).then(() => { const g = $('#jxGo'); if (g && D.getElementById('s-jee').classList.contains('active')) { const s2 = stats(LU, CACHE[LU]); g.parentElement.querySelector('span').textContent = `${s2.prog}% mastered · ${s2.first} solved first time · ${READY[LU].pyq} real JEE questions`; } }).catch(() => {});
  }
  function secOpen(k, def) { const u = J().ui || {}; return (k in u ? u[k] : def) ? 'open' : ''; }
  function path(j) {
    if (j.track === 'found') return FOUND.map(([u, n]) => [u, n, u === 'phy-u01' ? 'Physics · starts at Class 9 level' : 'Foundation']);
    const all = []; Object.entries(SUBJ).forEach(([k, s]) => s.u.forEach((u, i) => all.push([uidOf(k, i), u[0], `${s.n} · Class ${u[1]}`, u[1], k, i])));
    if (j.track === 'main') { const c = String(j.cls); const mine = all.filter(x => String(x[3]).includes(c)); const rest = all.filter(x => !String(x[3]).includes(c)); return (c === '12' ? mine.concat(rest.map(x => [x[0], x[1], x[2] + ' · revise'])) : mine).map(x => x.slice(0, 3)); }
    const order = []; for (let i = 0; i < 20; i++) ['phy', 'math', 'chem'].forEach(k => { const x = all.find(y => y[4] === k && y[5] === i); if (x) order.push(x.slice(0, 3)); }); return order;
  }

  /* ================= SETUP / ELIGIBILITY ================= */
  const WHO = [['c9', 'Class 9', 'school', 9], ['c10', 'Class 10', 'school', 10], ['c11', 'Class 11', 'school', 11], ['c12', 'Class 12 (board exam in 2027)', 'school', 12], ['drop', 'Passed Class 12 — preparing full time', 'passed'], ['bsc', 'Doing B.Sc. / another college course', 'college'], ['grad', 'Already graduated', 'grad'], ['dip', '3-year diploma (AICTE / state board)', 'passed']];
  function setup(step, dr = {}) {
    const el = screen(); here('setup');
    const back = `<button class="jx-back" id="jxBack">← Back</button>`;
    if (step === 1) {
      el.innerHTML = `<div class="jx">${back}<div class="jx-hero sm"><h1>🎯 JEE course</h1><p>Tell us where you are. We set your track and check whether you can sit JEE Main and JEE Advanced.</p></div>
        <div class="jx-card"><h3>I am in…</h3>${WHO.map(w => `<button class="jx-opt" data-w="${w[0]}"><b>${w[1]}</b></button>`).join('')}</div></div>`;
      $('#jxBack').onclick = () => { tap(); if (dr.again || (ST.jee && ST.jee.track)) return home(); ST.profile ? meScreen() : onboard(1); };
      el.querySelectorAll('[data-w]').forEach(b => b.onclick = () => { tap(); const w = WHO.find(x => x[0] === b.dataset.w); setup(2, { ...dr, who: w[0], status: w[2], cls: w[3] }); });
      return;
    }
    if (step === 2) {
      const yrs = []; for (let y = EXAM; y >= 2018; y--) yrs.push(y);
      const school = dr.status === 'school';
      el.innerHTML = `<div class="jx">${back}<div class="jx-card"><h3>${school ? 'A few quick checks' : 'Your Class XII'}</h3>
        ${school ? '' : `<label class="jx-lab">Year you FIRST appeared for Class XII<select id="jxFirst">${yrs.map(y => `<option ${y === 2026 ? 'selected' : ''}>${y}</option>`).join('')}</select></label>
        <label class="jx-lab">Year your Class XII result first said "pass"<select id="jxPass"><option value="">Same year</option>${yrs.map(y => `<option>${y}</option>`).join('')}</select></label>`}
        <label class="jx-lab">Physics + Mathematics in Class XII?<select id="jxPcm"><option value="1">Yes (PCM)</option><option value="0">No / not yet chosen</option></select></label>
        ${school && dr.cls < 11 ? '' : `<label class="jx-lab">Date of birth (only for the JEE Advanced age rule — optional)<input type="date" id="jxDob"></label>
        <label class="jx-lab">Category<select id="jxCat"><option value="">General / EWS / OBC-NCL</option><option value="r">SC / ST / PwD (age relaxation)</option></select></label>`}
        ${school ? '' : `<label class="jx-lab">JEE Advanced attempts already taken<select id="jxAdvT"><option>0</option><option>1</option><option>2</option></select></label>
        <label class="jx-chk"><input type="checkbox" id="jxIit"> I have already accepted an IIT seat earlier</label>`}
        <button class="jx-btn wide" id="jxCalc">Check my eligibility ▶</button></div></div>`;
      $('#jxBack').onclick = () => setup(1, dr);
      $('#jxCalc').onclick = () => {
        const v = id => { const x = D.getElementById(id); return x ? (x.type === 'checkbox' ? x.checked : x.value) : ''; };
        const x = { status: dr.status === 'school' ? 'school' : 'passed', cls: dr.cls, first: v('jxFirst'), pass: v('jxPass'), pcm: v('jxPcm') === '1', dob: v('jxDob'), relax: v('jxCat') === 'r', advTried: v('jxAdvT'), iit: v('jxIit') };
        tap(); setup(3, { ...dr, x, r: elig(x) });
      };
      return;
    }
    if (step === 3) {
      const r = dr.r, tr = dr.status === 'school' ? (dr.cls <= 10 ? 'found' : 'main') : 'full';
      const blocked = r.main.ok === false;
      el.innerHTML = `<div class="jx">${back}<div class="jx-card"><h3>Your result</h3>${eligHTML(r)}</div>
        <div class="jx-card"><h3>${TRACKS[tr].e} ${TRACKS[tr].n}</h3><p class="jx-p">${TRACKS[tr].d}.${blocked ? ' You can still study the full course — it builds the same Physics, Chemistry and Maths that other entrance exams test — but you cannot sit JEE Main 2027.' : ''}</p>
        <button class="jx-btn wide" id="jxStart">${blocked ? 'Study the course anyway ▶' : 'Start my JEE journey ▶'}</button></div></div>`;
      $('#jxBack').onclick = () => setup(2, dr);
      $('#jxStart').onclick = () => {
        tap('unlock'); const j = J(); Object.assign(j, { track: tr, cls: dr.cls || null, who: dr.who, elig: { xii: r.xii, main: r.main, adv: r.adv }, home: true, since: j.since || Date.now() }); save();
        if (ST.profile) { if (dr.status !== 'school' && ST.profile.grade !== 12) toast('Your school world stays as it is'); return home(); }
        const g = dr.status === 'school' ? dr.cls : 12, d0 = { board: 'cbse', grade: g };   // new user: finish the normal sign-up (stream for 11–12, then name)
        if (g >= 11) pickStream(g, (stream, subjects) => onboard(3, { ...d0, stream, subjects }), () => setup(3, dr), 'cbse'); else onboard(3, { ...d0, stream: null, subjects: null });
      };
    }
  }
  function eligHTML(r) {
    const row = (t, o) => `<div class="jx-el ${o.ok === true ? 'ok' : o.ok === false ? 'no' : 'wait'}"><b>${o.ok === true ? '✅' : o.ok === false ? '⛔' : '⏳'} ${t}</b><p>${esc(o.why || '')}</p></div>`;
    return row('JEE Main', r.main) + row('JEE Advanced', r.adv) + (r.notes || []).map(n => `<p class="jx-note">ℹ️ ${esc(n)}</p>`).join('') +
      `<p class="jx-fine">JEE Main: NTA Information Bulletin 2027 (no age limit; Class XII passed in 2025/2026 or appearing in 2027). JEE Advanced: top 2,50,000 in JEE Main; the 2027 rules are not out yet, so this uses the 2026 pattern (two attempts in consecutive years from your Class XII year; age limit; no earlier IIT seat). Always confirm at jeemain.nta.nic.in and jeeadv.ac.in.</p>`;
  }
  function eligScreen() { const j = J(); setup(1, { again: true }); if (j.elig) { const el = $('#s-jee .jx'); el.insertAdjacentHTML('afterbegin', `<div class="jx-card"><h3>Saved result</h3>${eligHTML(Object.assign({ notes: [] }, j.elig))}</div>`); } }

  /* ================= UNIT ================= */
  let TOP; const TOP1 = { units: 'SI units', lc: 'Least count & instruments', sf: 'Significant figures', err: 'Errors', dim: 'Dimensions', dimapp: 'Dimensional analysis' };
  async function unit(uid, tab = 'learn') {
    const el = screen(); here('unit', uid, tab); J().last = uid; save();
    el.innerHTML = `<div class="jx"><p class="jx-p">Loading…</p></div>`;
    let d; try { d = await data(uid); } catch (e) { el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← JEE</button><div class="jx-card"><p>Could not load this unit. Check your connection and try again.</p></div></div>`; $('#jxBack').onclick = home; return; }
    TOP = d.topics || TOP1; const s = stats(uid, d), j = J();
    const tabs = [['learn', '📖 Learn'], ['lab', '🧪 Try it yourself'], ['pyq', '🏛️ Real JEE'], ['prac', '🎯 Practice'], ['test', '⏱️ Test'], ['vault', '🧾 Formulas']];
    el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← JEE home</button>
      <div class="jx-uh"><div class="jx-ring" style="--p:${s.prog}"><b>${s.prog}%</b></div><div><small>${SUBJ[d.subject || 'phy'].n} · Unit ${d.n || 1} · Class ${d.cls}</small><h1>${esc(d.title)}</h1><p>${s.cardsOk}/${d.cards.length} concepts checked · ${s.first} solved first time · best test ${s.best}%</p></div></div>
      <div class="jx-tabs" role="tablist">${tabs.map(([k, n]) => `<button role="tab" aria-selected="${k === tab}" data-t="${k}">${n}</button>`).join('')}</div><div id="jxBody"></div></div>`;
    $('#jxBack').onclick = () => { tap(); home(); };
    el.querySelectorAll('[data-t]').forEach(b => b.onclick = () => { tap(); unit(uid, b.dataset.t); });
    const body = $('#jxBody');
    ({ learn: learnTab, pyq: pyqTab, prac: pracTab, lab: labTab, test: testTab, vault: vaultTab })[tab](body, d, uid, s, j);
  }
  function learnTab(body, d, uid, s, j) {
    const u = U(uid), found = j.track === 'found';
    body.innerHTML = `<p class="jx-p">${esc(d.syllabus)}</p>${d.steps.map((st, i) => {
      const cs = st.cards.map(id => d.cards.find(c => c.id === id)).filter(c => !found || c.lvl === 'f' || i > 0);
      const done = st.cards.filter(id => u.cards[id]).length;
      return `<div class="jx-step"><div class="jx-sh"><span>${st.e}</span><b>Step ${i + 1} · ${esc(st.t)}</b><small>${done}/${st.cards.length} checked</small></div><p class="jx-p">${esc(st.note)}</p>
        ${cs.map(c => `<details class="jx-cc" data-c="${c.id}"><summary><span>${c.e}</span><b>${esc(c.t)}</b>${c.lvl === 'f' ? '<em class="f">Class 9+</em>' : '<em>JEE</em>'}${u.cards[c.id] ? '<i>✓</i>' : ''}</summary>
          <div class="jx-cb">${c.body.map(p => `<p>${mx(p)}</p>`).join('')}
          <div class="jx-qc"><b>Quick check</b><p>${mx(c.check.q)}</p>${c.check.o.map((o, k) => `<button class="jx-qo" data-k="${k}">${mx(o)}</button>`).join('')}<p class="jx-why" hidden></p></div></div></details>`).join('')}
        <button class="jx-btn ghost" data-pt="${st.need.join(',')}">Practise this step (${d.pyq.filter(q => st.need.includes(q.t)).length} real JEE questions) ▶</button></div>`;
    }).join('')}<div class="jx-card"><h3>⚠️ Traps examiners love</h3><ul class="jx-traps">${d.traps.map(t => `<li>${mx(t)}</li>`).join('')}</ul></div>`;
    body.querySelectorAll('.jx-cc').forEach(cc => {
      const c = d.cards.find(x => x.id === cc.dataset.c);
      cc.querySelectorAll('.jx-qo').forEach(b => b.onclick = () => {
        if (cc.dataset.done) return; const k = +b.dataset.k, ok = k === c.check.a; cc.dataset.done = 1;
        cc.querySelectorAll('.jx-qo').forEach((x, i) => { x.disabled = true; if (i === c.check.a) x.classList.add('ok'); else if (i === k) x.classList.add('no'); });
        const w = cc.querySelector('.jx-why'); w.hidden = false; w.innerHTML = (ok ? '✅ ' : '❌ ') + mx(c.check.why) + (ok ? '' : ' — read the card again and retry later.');
        tap(ok ? 'correct' : 'wrong'); if (ok) { U(uid).cards[c.id] = Date.now(); save(); }
        else setTimeout(() => { delete cc.dataset.done; cc.querySelectorAll('.jx-qo').forEach(x => { x.disabled = false; x.classList.remove('ok', 'no'); }); }, 4000);
      });
    });
    body.querySelectorAll('[data-pt]').forEach(b => b.onclick = () => { tap('open'); const ts = b.dataset.pt.split(','); run(uid, d.pyq.filter(q => ts.includes(q.t)).map(q => q.id), { title: 'Real JEE questions', back: () => unit(uid, 'learn') }); });
  }
  function pyqTab(body, d, uid) {
    const yrs = [...new Set(d.pyq.map(q => q.src.y + ' ' + q.src.s))];
    const ans = U(uid).ans;
    const byYear = {}; d.pyq.forEach(q => { const k = q.src.y; byYear[k] = (byYear[k] || 0) + 1; });
    const max = Math.max(...Object.values(byYear));
    body.innerHTML = `<div class="jx-card"><h3>📈 How often this unit appears</h3><div class="jx-bars">${Object.entries(byYear).map(([y, n]) => `<div><span style="height:${Math.round(70 * n / max)}px"></span><b>${n}</b><small>${y}</small></div>`).join('')}</div>
      <p class="jx-p">${d.pyq.length} questions from ${yrs.length} sessions — about ${(d.pyq.length / 53).toFixed(1)} per shift on average. Topic mix: ${Object.entries(d.pyq.reduce((m, q) => (m[q.t] = (m[q.t] || 0) + 1, m), {})).sort((a, b) => b[1] - a[1]).map(([t, n]) => `${TOP[t]} ${n}`).join(' · ')}.</p></div>
      <div class="jx-filt"><select id="jxY"><option value="">All sessions</option>${yrs.map(y => `<option>${y}</option>`).join('')}</select><select id="jxT"><option value="">All topics</option>${Object.entries(TOP).map(([k, n]) => `<option value="${k}">${n}</option>`).join('')}</select></div>
      <button class="jx-btn wide" id="jxRun">Solve these ▶</button><div class="jx-list" id="jxL"></div>`;
    const draw = () => {
      const y = $('#jxY').value, t = $('#jxT').value, L = d.pyq.filter(q => (!y || q.src.y + ' ' + q.src.s === y) && (!t || q.t === t));
      $('#jxL').innerHTML = L.map((q, i) => `<button class="jx-li" data-i="${q.id}"><span class="${ans[q.id] ? (ans[q.id].ok ? 'ok' : 'no') : ''}">${ans[q.id] ? (ans[q.id].ok ? '✓' : '✗') : i + 1}</span><span><small>${srcTag(q.src)} · ${TOP[q.t]}${q.n !== undefined ? ' · Numerical' : ''}</small>${mx(q.q.length > 120 ? q.q.slice(0, 117) + '…' : q.q)}</span></button>`).join('');
      $('#jxRun').textContent = `Solve these ${L.length} ▶`; $('#jxRun').onclick = () => { tap('open'); run(uid, L.map(q => q.id), { title: 'Real JEE questions', back: () => unit(uid, 'pyq') }); };
      $('#jxL').querySelectorAll('[data-i]').forEach(b => b.onclick = () => { tap('open'); const ids = L.map(q => q.id); run(uid, ids, { title: 'Real JEE questions', start: ids.indexOf(b.dataset.i), back: () => unit(uid, 'pyq') }); });
    };
    $('#jxY').onchange = draw; $('#jxT').onchange = draw; draw();
  }
  function pracTab(body, d, uid, s) {
    const ans = U(uid).ans, seen = d.prac.filter(q => ans[q.id]).length;
    const tp = s.topic;
    body.innerHTML = `<div class="jx-card"><h3>🎯 ${d.prac.length} practice questions</h3><p class="jx-p">Written by StudyVerse — 12 for every real JEE question, same idea, new numbers and new steps. Every answer was re-solved by an independent checker before it reached you.</p>
      <p class="jx-p">${seen} attempted.</p></div>
      <div class="jx-grid">${Object.entries(TOP).map(([k, n]) => { const t = tp[k]; return `<button class="jx-tile" data-k="${k}"><b>${n}</b><small>${d.prac.filter(q => q.t === k).length} questions${t ? ` · ${pct(t.r, t.a)}% right` : ''}</small></button>`; }).join('')}</div>
      <button class="jx-btn wide" id="jxMix">🔀 Smart mix — weakest topics first ▶</button>`;
    body.querySelectorAll('[data-k]').forEach(b => b.onclick = () => { tap('open'); const L = shuffle(d.prac.filter(q => q.t === b.dataset.k && !(ans[q.id] && ans[q.id].ok))).slice(0, 15); run(uid, L.map(q => q.id), { title: TOP[b.dataset.k], back: () => unit(uid, 'prac') }); });
    $('#jxMix').onclick = () => {
      tap('open'); const w = k => { const t = tp[k]; return t ? 1 - t.r / t.a : 0.6; };
      const L = shuffle(d.prac.filter(q => !(ans[q.id] && ans[q.id].ok))).sort((a, b) => w(b.t) - w(a.t) + (Math.random() - 0.5) * 0.4).slice(0, 15);
      run(uid, L.map(q => q.id), { title: 'Smart mix', back: () => unit(uid, 'prac') });
    };
  }
  function vaultTab(body, d) {
    body.innerHTML = `<div class="jx-card"><h3>🧾 Formula vault</h3>${d.formulas.map(([n, f]) => `<div class="jx-fv"><small>${esc(n)}</small><div>${mx(f)}</div></div>`).join('')}</div>`;
  }
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const k = Math.floor(Math.random() * (i + 1)); [a[i], a[k]] = [a[k], a[i]]; } return a; };

  /* ================= QUESTION RUNNER (prev/next, answered strip, step-by-step solutions) ================= */
  function run(uid, ids, o = {}) {
    const el = screen(); const d0 = CACHE[uid];
    const list = o.items ? o.items.slice() : (d0 ? ids.map(id => d0.byId[id]).filter(Boolean).map(q => ({ q, uid })) : []);
    if (!list.length) { toast('Nothing to practise here yet'); return; }
    let i = o.start > 0 ? o.start : 0; const S = list.map(() => ({}));
    const draw = () => {
      const it = list[i], q = it.q, s = S[i], num = q.n !== undefined, d = CACHE[it.uid]; uid = it.uid; TOP = d.topics || TOP1;
      const bm = (J().bm || []).includes(it.uid + '|' + q.id);
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← ${esc(o.title || 'Back')}</button>
        <div class="jx-strip">${list.length > 60 ? '' : list.map((x, k) => `<button data-j="${k}" class="${k === i ? 'cur ' : ''}${S[k].done ? (S[k].ok ? 'ok' : 'no') : ''}" aria-label="Question ${k + 1}">${k + 1}</button>`).join('')}</div>
        <div class="jx-card jx-q">${crumbs(it.uid, q)}<div class="jx-qt"><button class="jx-bm ${bm ? 'on' : ''}" id="jxBm" aria-label="Save this question">${bm ? '★' : '☆'}</button><span class="jx-tag ${q.kind}">${q.kind === 'pyq' ? '🏛️ ' + srcTag(q.src) : '🎯 StudyVerse practice'}</span><span class="jx-tag">${TOP[q.t]}${num ? ' · Numerical' : ''}</span></div>
          <div class="jx-qq">${mx(q.q)}</div>${q.fig ? `<div class="jx-figw">${q.fig}</div>` : ''}
          ${num ? `<div class="jx-num"><input id="jxN" inputmode="decimal" placeholder="Type your answer" ${s.done ? 'disabled' : ''} value="${s.v != null ? esc(s.v) : ''}"><small>Numerical answer — NTA rounds to the nearest integer</small></div>`
            : `<div class="jx-os">${q.o.map((x, k) => `<button class="jx-o ${s.done ? (k === q.a ? 'ok' : k === s.pick ? 'no' : '') : (k === s.pick ? 'sel' : '')}" data-k="${k}" ${s.done ? 'disabled' : ''}><i class="jx-on">${k + 1}</i><span>${mx(x)}</span></button>`).join('')}</div>`}
          ${s.done ? `<div class="jx-res ${s.ok ? 'ok' : 'no'}">${s.ok ? '✅ Correct' : `❌ Not quite — answer: ${num ? q.n : '(' + (q.a + 1) + ') ' + mx(q.o[q.a])}`}</div>
            <div class="jx-sol"><b>Step-by-step</b>${q.sol.slice(0, s.steps || 1).map((x, k) => `<p><i class="jx-sn">${k + 1}</i><span>${mx(x)}</span></p>`).join('')}
            ${(s.steps || 1) < q.sol.length ? `<button class="jx-btn ghost" id="jxStep">Next step (${(s.steps || 1) + 1}/${q.sol.length}) — try it yourself first</button>` : ''}</div>
            ${q.kind === 'pyq' && d.prac.some(x => x.like === q.id) ? `<button class="jx-btn ghost" id="jxSim">🔁 Try a similar question</button>` : ''}`
            : `<button class="jx-btn wide" id="jxCheck" ${num || s.pick != null ? '' : 'disabled'}>Check answer</button>`}
        </div>
        <div class="jx-nav"><button class="jx-btn ghost" id="jxPrev" ${i ? '' : 'disabled'}>◀ Previous</button><button class="jx-btn" id="jxNext">${i < list.length - 1 ? 'Next ▶' : 'Finish'}</button></div></div>`;
      $('#jxBack').onclick = () => { tap(); o.back ? o.back() : unit(uid); };
      wireCrumbs(el);
      $('#jxBm').onclick = () => { const b = J().bm || (J().bm = []), k = it.uid + '|' + q.id, x = b.indexOf(k); if (x < 0) { b.push(k); toast('⭐ Saved to your question bank'); } else b.splice(x, 1); save(); tap(); draw(); };
      el.querySelectorAll('[data-j]').forEach(b => b.onclick = () => { i = +b.dataset.j; draw(); });
      el.querySelectorAll('.jx-o:not([disabled])').forEach(b => b.onclick = () => { tap(); s.pick = +b.dataset.k; draw(); });
      const n = $('#jxN'); if (n && !s.done) { n.oninput = () => { s.v = n.value; }; n.onkeydown = e => { if (e.key === 'Enter') check(); }; }
      const c = $('#jxCheck'); if (c) c.onclick = check;
      const st = $('#jxStep'); if (st) st.onclick = () => { tap(); s.steps = (s.steps || 1) + 1; draw(); };
      const sm = $('#jxSim'); if (sm) sm.onclick = () => {
        tap('open'); const cands = d.prac.filter(x => x.like === q.id && !list.some(y => y.q === x)); if (!cands.length) return toast('You have seen all similar questions');
        list.splice(i + 1, 0, { q: cands[Math.floor(Math.random() * cands.length)], uid: it.uid }); S.splice(i + 1, 0, {}); i++; draw();
      };
      $('#jxPrev').onclick = () => { if (i) { i--; draw(); } };
      $('#jxNext').onclick = () => { if (i < list.length - 1) { i++; draw(); } else summary(); };
      function check() {
        if (s.done) return;
        let ok;
        if (num) { const v = parseFloat(String(s.v || '').replace(/[^0-9.\-]/g, '')); if (isNaN(v)) return toast('Type a number first'); ok = Math.round(v) === q.n; }
        else { if (s.pick == null) return; ok = s.pick === q.a; }
        s.done = 1; s.ok = ok; s.steps = 1; record(uid, q, ok); tap(ok ? 'correct' : 'wrong'); draw();
      }
    };
    const summary = () => {
      const done = S.filter(x => x.done).length, right = S.filter(x => x.ok).length;
      el.innerHTML = `<div class="jx"><div class="jx-card jx-sum"><h2>${right === done && done ? '🏆' : '📊'} ${right}/${done} correct</h2><p class="jx-p">${done < list.length ? `${list.length - done} left unanswered. ` : ''}Wrong ones are saved in your Mistake book — fix them later to clear them.</p>
        <button class="jx-btn wide" id="jxAgain">Back to the unit</button></div></div>`;
      $('#jxAgain').onclick = () => { tap(); o.back ? o.back() : unit(uid); };
    };
    draw();
  }
  function record(uid, q, ok) {
    const u = U(uid), a = u.ans[q.id] || (u.ans[q.id] = { n: 0 });
    a.n++; if (a.f === undefined) a.f = ok ? 1 : 0; a.ok = ok ? 1 : 0; a.t = Date.now();
    const m = J().mist, key = uid + '|' + q.id, k = m.indexOf(key);
    if (!ok && k < 0) m.push(key); if (ok && k >= 0) m.splice(k, 1);
    save();
  }
  async function mistakes() {
    const m = J().mist; if (!m.length) return toast('Your Mistake book is empty — great work');
    const items = [];
    for (const key of m) { const [u, id] = key.split('|'); if (!READY[u]) continue; try { const d = await data(u); if (d.byId[id]) items.push({ q: d.byId[id], uid: u }); } catch (e) {} }
    if (!items.length) return toast('Your Mistake book is empty — great work');
    run(items[0].uid, [], { items, title: 'Mistake book', back: NAVP ? practiceHub : home });
  }

  /* ================= NTA-STYLE TEST ================= */
  function testTab(body, d, uid) {
    const T = U(uid).tests;
    body.innerHTML = `<div class="jx-card"><h3>⏱️ Unit test — exactly like JEE Main</h3><ul class="jx-traps"><li>20 questions: 15 MCQ (Section A) + 5 numerical (Section B)</li><li>Marking: +4 correct, −1 wrong, 0 unanswered — in BOTH sections</li><li>Numerical answers are rounded to the nearest integer</li><li>48 minutes (JEE gives 3 h for 75 questions = 2.4 min each)</li><li>Question palette, mark for review, auto-submit at 0:00</li></ul>
      <button class="jx-btn wide" id="jxT1">Start test ▶</button>${T.length ? `<h3>Your attempts</h3>${T.slice(-5).reverse().map(t => `<div class="jx-ta"><b>${t.sc}/80</b><span>${t.pct}% · ${t.r} right · ${t.w} wrong · ${Math.round(t.sec / 60)} min</span><small>${new Date(t.at).toLocaleDateString('en-IN')}</small></div>`).join('')}` : ''}</div>`;
    $('#jxT1').onclick = () => { tap('open'); test(uid); };
  }
  function test(uid) {
    const d = CACHE[uid], el = screen(); here('unit', uid, 'test'); TOP = d.topics || TOP1;
    const mc = shuffle(d.pyq.filter(q => q.o)).slice(0, 9).concat(shuffle(d.prac.filter(q => q.o)).slice(0, 6));
    const nm = shuffle(d.pyq.filter(q => q.n !== undefined)).slice(0, 2).concat(shuffle(d.prac.filter(q => q.n !== undefined))).slice(0, 5);
    const list = shuffle(mc).concat(nm), S = list.map(() => ({ v: null, rev: false, seen: false }));
    let i = 0, left = 48 * 60, t0 = Date.now(), timer, armed = false, over = false;
    const fmt = s => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
    const stOf = s => s.v != null && s.v !== '' ? (s.rev ? 'ar' : 'a') : s.rev ? 'r' : s.seen ? 'na' : 'nv';
    const draw = () => {
      const q = list[i], s = S[i], num = q.n !== undefined; s.seen = true;
      el.innerHTML = `<div class="jx jx-test"><div class="jx-tbar"><b>Section ${num ? 'B · Numerical' : 'A · MCQ'}</b><span id="jxClock">⏱ ${fmt(left)}</span><button class="jx-btn ghost sm" id="jxSub">Submit</button></div>
        <div class="jx-pal">${list.map((x, k) => `<button data-j="${k}" class="p-${stOf(S[k])}${k === i ? ' cur' : ''}">${k + 1}</button>`).join('')}</div>
        <div class="jx-card jx-q"><div class="jx-qt"><span class="jx-tag">Q${i + 1} · +4 / −1</span></div><div class="jx-qq">${mx(q.q)}</div>${q.fig ? `<div class="jx-figw">${q.fig}</div>` : ''}
        ${num ? `<div class="jx-num"><input id="jxN" inputmode="decimal" placeholder="Enter a number" value="${s.v != null ? esc(s.v) : ''}"></div>` : `<div class="jx-os">${q.o.map((x, k) => `<button class="jx-o ${s.v === k ? 'sel' : ''}" data-k="${k}"><i class="jx-on">${k + 1}</i><span>${mx(x)}</span></button>`).join('')}</div>`}</div>
        <div class="jx-nav"><button class="jx-btn ghost" id="jxClr">Clear</button><button class="jx-btn ghost" id="jxRev">${s.rev ? 'Unmark' : 'Mark for review'}</button><button class="jx-btn" id="jxNx">Save & next ▶</button></div>
        <p class="jx-fine">Palette: grey not visited · red not answered · green answered · purple marked for review.</p></div>`;
      el.querySelectorAll('[data-j]').forEach(b => b.onclick = () => { i = +b.dataset.j; draw(); });
      el.querySelectorAll('.jx-o').forEach(b => b.onclick = () => { s.v = +b.dataset.k; draw(); });
      const n = $('#jxN'); if (n) n.oninput = () => { s.v = n.value.trim() === '' ? null : n.value; };
      $('#jxClr').onclick = () => { s.v = null; draw(); };
      $('#jxRev').onclick = () => { s.rev = !s.rev; draw(); };
      $('#jxNx').onclick = () => { if (i < list.length - 1) i++; draw(); };
      $('#jxSub').onclick = () => { const un = S.filter(x => x.v == null || x.v === '').length; if (un && !armed) { armed = true; const b = $('#jxSub'); b.textContent = `${un} unanswered — tap again to submit`; setTimeout(() => { armed = false; const c = $('#jxSub'); if (c) c.textContent = 'Submit'; }, 3500); return; } finish(); };
    };
    const finish = () => {
      if (over) return; over = true; clearInterval(timer); let r = 0, w = 0;
      const res = list.map((q, k) => { const v = S[k].v; if (v == null || v === '') return 0; const ok = q.n !== undefined ? Math.round(parseFloat(String(v).replace(/[^0-9.\-]/g, ''))) === q.n : v === q.a; ok ? r++ : w++; record(uid, q, ok); return ok ? 1 : -1; });
      const sc = 4 * r - w, sec = Math.round((Date.now() - t0) / 1000), p = Math.max(0, Math.round(100 * sc / 80));
      U(uid).tests.push({ sc, r, w, pct: p, sec, at: Date.now() }); save(); tap('unlock');
      el.innerHTML = `<div class="jx"><div class="jx-card jx-sum"><h2>${sc}/80</h2><p class="jx-p">${r} correct (+${4 * r}) · ${w} wrong (−${w}) · ${list.length - r - w} skipped · ${Math.round(sec / 60)} min</p>
        <p class="jx-p">${w > r / 2 ? '⚠️ Many negatives: in the real exam, skip a question unless you can rule out at least two options.' : r >= 16 ? '🔥 Exam-ready on this unit.' : 'Review each wrong answer below — the steps show where it went off.'}</p></div>
        ${list.map((q, k) => `<details class="jx-card jx-rv ${res[k] > 0 ? 'ok' : res[k] < 0 ? 'no' : ''}"><summary>Q${k + 1} · ${res[k] > 0 ? '✅ +4' : res[k] < 0 ? '❌ −1' : '— 0'} · ${TOP[q.t]}</summary><div class="jx-qq">${mx(q.q)}</div>${q.fig ? `<div class="jx-figw">${q.fig}</div>` : ''}
          <p><b>Answer:</b> ${q.n !== undefined ? q.n : '(' + (q.a + 1) + ') ' + mx(q.o[q.a])}${S[k].v != null && S[k].v !== '' ? ` · <b>You:</b> ${q.n !== undefined ? esc(S[k].v) : '(' + (S[k].v + 1) + ')'}` : ''}</p>
          <div class="jx-sol">${q.sol.map((x, n) => `<p><i class="jx-sn">${n + 1}</i><span>${mx(x)}</span></p>`).join('')}</div></details>`).join('')}
        <button class="jx-btn wide" id="jxDone">Back to the unit</button></div>`;
      $('#jxDone').onclick = () => unit(uid, 'test');
    };
    timer = setInterval(() => { left--; const c = $('#jxClock'); if (c) c.textContent = `⏱ ${fmt(left)}`; else if (!D.getElementById('s-jee').classList.contains('active')) clearInterval(timer); if (left <= 0) finish(); }, 1000);
    draw();
  }

  /* ================= LABS ================= */
  const DIM = { 'mass': [1, 0, 0, 0], 'length': [0, 1, 0, 0], 'time': [0, 0, 1, 0], 'current': [0, 0, 0, 1], 'velocity': [0, 1, -1, 0], 'force': [1, 1, -2, 0], 'energy': [1, 2, -2, 0], 'charge': [0, 0, 1, 1], 'G': [-1, 3, -2, 0], 'h': [1, 2, -1, 0], 'ε₀': [-1, -3, 4, 2], 'μ₀': [1, 1, -2, -2], 'B': [1, 0, -2, -1], 'E field': [1, 1, -3, -1], 'R': [1, 2, -3, -2], 'L (ind.)': [1, 2, -2, -2], 'C (cap.)': [-1, -2, 4, 2] };
  const NAMED = [['speed', [0, 1, -1, 0]], ['acceleration', [0, 1, -2, 0]], ['force', [1, 1, -2, 0]], ['energy / torque', [1, 2, -2, 0]], ['power', [1, 2, -3, 0]], ['momentum / impulse', [1, 1, -1, 0]], ['angular momentum / h', [1, 2, -1, 0]], ['pressure / energy density', [1, -1, -2, 0]], ['time', [0, 0, 1, 0]], ['frequency', [0, 0, -1, 0]], ['current', [0, 0, 0, 1]], ['charge', [0, 0, 1, 1]], ['resistance', [1, 2, -3, -2]], ['mass', [1, 0, 0, 0]], ['length', [0, 1, 0, 0]], ['pure number', [0, 0, 0, 0]], ['velocity²', [0, 2, -2, 0]], ['electric field', [1, 1, -3, -1]], ['current density', [0, -2, 0, 1]]];
  const GOALS = [['Make a SPEED using only ε₀ and μ₀', [0, 1, -1, 0], ['ε₀', 'μ₀']], ['Make a RESISTANCE using ε₀ and μ₀', [1, 2, -3, -2], ['ε₀', 'μ₀']], ['Make a TIME using L and R', [0, 0, 1, 0], ['L (ind.)', 'R']], ['Make a TIME using L and C', [0, 0, 1, 0], ['L (ind.)', 'C (cap.)']], ['Make an ENERGY DENSITY using ε₀ and E field', [1, -1, -2, 0], ['ε₀', 'E field']], ['Make a MASS using h, velocity and G (Planck mass)', [1, 0, 0, 0], ['h', 'velocity', 'G']], ['Make a FORCE using μ₀ and current', [1, 1, -2, 0], ['μ₀', 'current']], ['Make a CURRENT using ε₀, E field and time', [0, 0, 0, 1], ['ε₀', 'E field', 'time', 'length']]];
  const frac = p => { const n = Math.round(p * 2); return (n < 0 ? '−' : '') + (n % 2 ? `${Math.abs(n)}/2` : Math.abs(n / 2)); };
  const dimTxt = v => { const t = ['M', 'L', 'T', 'A'].map((s, k) => Math.abs(v[k]) > 1e-9 ? s + (v[k] === 1 ? '' : `<sup>${frac(v[k])}</sup>`) : '').join(''); return '[' + (t || 'M<sup>0</sup>L<sup>0</sup>T<sup>0</sup>') + ']'; };
  function labTab(body, d, uid) {
    if (d.labs && d.labs.length) {
      const L = { circuit: ['🔋 Circuit Playground', 'Change emf, internal resistance and resistors — watch the current flow, the bulb glow and the power curve. 6 missions.', () => circuitLab(uid)],
        bridge: ['🌉 Meter Bridge Lab', 'Slide the jockey, watch the galvanometer needle, find the null point and unmask the hidden resistor.', () => bridgeLab(uid)],
        photo: ['⚡ Photoelectric Lab', 'Pick a metal, tune the colour and brightness of light, push back with a retarding voltage — see which electrons escape. 5 missions.', () => photoLab(uid)],
        bohr: ['🪐 Bohr Atom Jumper', 'Make the electron jump between orbits of H, He⁺ or Li²⁺ and catch the photon it emits — colour, wavelength and series. 5 missions.', () => bohrLab(uid)],
        orbital: ['🧱 Orbital Builder', 'Pick n, l and m to see each orbital and its nodes, then fill boxes electron by electron with Aufbau, Pauli and Hund. 4 missions.', () => orbitalLab(uid)],
        orbit: ['🛰️ Orbit Launcher', 'Fire a satellite sideways from Earth, the Moon or Mars: watch it crash, circle, stretch into an ellipse or escape — with live orbital and escape speeds. 5 missions.', () => orbitLab(uid)],
        charges: ['⚡ Field Line Studio', 'Place two charges, change their size, sign and gap, and probe the field and potential anywhere: find null points, zero-potential points and dipole fields. 5 missions.', () => chargeLab(uid)],
        pv: ['🔥 P–V Process Lab', 'Take a gas through isothermal, adiabatic, isobaric and isochoric steps and watch Q, W and ΔU add up — build an engine, a fridge and a Carnot cycle. 5 missions.', () => pvLab(uid)],
        box: ['🫧 Molecule Box', 'Watch molecules fly and hit the walls. Change temperature, number and box size and see rms speed, kinetic energy and pressure respond. 5 missions.', () => boxLab(uid)],
        emw: ['🌊 EM Wave Builder', 'Watch the electric and magnetic fields of a light wave move together. Choose the travel direction, field directions, frequency and strength — see wavelength, B and intensity. 5 missions.', () => emLab(uid)],
        transform: ['🔀 Matrix Transformer', 'Drag four numbers and watch a matrix stretch, rotate, shear or flatten the plane — the area change is the determinant. 5 missions.', () => transformLab(uid)],
        planes: ['📐 Line Meeting Room', 'Tune two equations and see their lines cross once, run parallel or lie on top of each other, with D, Dx and Dy live. 4 missions.', () => planesLab(uid)],
        pattern: ['📈 Pattern Builder', 'Build A.P.s and G.P.s with sliders: bars for terms, a line for the running sum, and the infinite-sum line a G.P. creeps towards. 5 missions.', () => patternLab(uid)],
        tele: ['🔭 Telescoping Machine', 'See Gauss\'s staircase turn into a rectangle, then split fractions and cancel neighbours with ✂️ until only the ends survive. 4 missions.', () => teleLab(uid)],
        molemach: ['🥚 Mole Machine', 'Pour grams of water, CO₂, salt or glucose on a balance and watch moles, molecules, atoms and gas volume appear on the mole map. 5 missions.', () => moleLab(uid)],
        limit: ['⚖️ Limiting Reagent Kitchen', 'Drop molecules into the pot, press React and see which one runs out first — and what is left over. 5 missions.', () => limitLab(uid)],
        react: ['⚗️ Reaction Race', 'Watch A turn into B for zero, first and second order. Switch plots to find the straight line, spot the half-lives — then crack mystery reactions. 5 missions.', () => reactLab(uid)],
        arrh: ['🔥 Arrhenius Hill', 'Heat the molecules, lower the hill with a catalyst and see k, the half-life and the lucky collisions change by millions. 5 missions.', () => arrhLab(uid)],
        wave: ['🌊 Matter-Wave Explorer', 'Give an electron, proton, alpha or a cricket ball a speed and see how long its de Broglie wave is next to an atom.', () => waveLab(uid)] };
      body.innerHTML = `<p class="jx-p">Play first, then read: every slider here is a real formula from this unit.</p><div class="jx-grid">${d.labs.map(k => `<button class="jx-tile big" data-lab="${k}"><b>${L[k][0]}</b><small>${L[k][1]}</small></button>`).join('')}</div>`;
      body.querySelectorAll('[data-lab]').forEach(b => b.onclick = () => { tap('open'); L[b.dataset.lab][2](); });
      return;
    }
    body.innerHTML = `<div class="jx-grid"><button class="jx-tile big" id="jxLD"><b>🧬 Dimension Lab</b><small>Build quantities from ε₀, μ₀, h, G… and watch the dimensions change live. 8 challenges.</small></button>
      <button class="jx-tile big" id="jxLV"><b>📏 Vernier Simulator</b><small>Read a real-looking vernier, with and without zero error. Endless readings.</small></button>
      <button class="jx-tile big" id="jxLS"><b>🔩 Screw Gauge Simulator</b><small>Pitch, circular scale and zero error — read it like the lab.</small></button></div>`;
    $('#jxLD').onclick = () => { tap('open'); dimLab(uid, 0); };
    $('#jxLV').onclick = () => { tap('open'); vernier(uid); };
    $('#jxLS').onclick = () => { tap('open'); screwLab(uid); };
  }
  function dimLab(uid, g) {
    const el = screen(); const goal = GOALS[g % GOALS.length], pw = {}; let won = false;
    const draw = () => {
      const v = [0, 0, 0, 0]; Object.entries(pw).forEach(([k, p]) => DIM[k].forEach((x, i) => v[i] += x * p));
      const hit = NAMED.filter(n => n[1].every((x, i) => Math.abs(x - v[i]) < 1e-9)).map(n => n[0]);
      const ok = goal[1].every((x, i) => Math.abs(x - v[i]) < 1e-9) && Object.values(pw).some(p => p);
      if (ok && !won) { won = true; tap('correct'); }
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Labs</button><div class="jx-card"><h3>🧬 Dimension Lab · ${g % GOALS.length + 1}/${GOALS.length}</h3><p class="jx-goal">${goal[0]}</p>
        <div class="jx-dimout ${ok ? 'ok' : ''}"><div>${Object.entries(pw).filter(x => x[1]).map(([k, p]) => `${esc(k)}${p === 1 ? '' : `<sup>${frac(p)}</sup>`}`).join(' · ') || 'Tap + and − to multiply or divide'}</div><b>${dimTxt(v)}</b><small>${hit.length ? '= ' + hit.join(', ') : ''}</small></div>
        ${ok ? `<p class="jx-res ok">✅ Done! ${esc(goal[0].replace('Make a', 'You made a').replace('Make an', 'You made an'))}.</p><button class="jx-btn wide" id="jxNextG">Next challenge ▶</button>` : ''}
        <div class="jx-chipsel">${Object.keys(DIM).map(k => `<div class="jx-dc ${goal[2].includes(k) ? 'hint' : ''}"><button data-k="${esc(k)}" data-d="-1">−</button><span>${esc(k)}<small>${dimTxt(DIM[k])}</small><b>${pw[k] ? (pw[k] > 0 ? '×' : '÷') + frac(Math.abs(pw[k])) : ''}</b></span><button data-k="${esc(k)}" data-d="1">+</button></div>`).join('')}</div>
        <div class="jx-nav"><button class="jx-btn ghost" id="jxHalf">½ power (√)</button><button class="jx-btn ghost" id="jxReset">Reset</button></div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-k]').forEach(b => b.onclick = () => { tap(); const k = b.dataset.k; pw[k] = (pw[k] || 0) + (+b.dataset.d); won = false; draw(); });
      $('#jxReset').onclick = () => { Object.keys(pw).forEach(k => delete pw[k]); won = false; draw(); };
      $('#jxHalf').onclick = () => { Object.keys(pw).forEach(k => pw[k] = pw[k] / 2); won = false; draw(); };
      const n = $('#jxNextG'); if (n) n.onclick = () => dimLab(uid, g + 1);
    };
    draw();
  }
  function vernier(uid) {
    const el = screen(); let tries = 0, right = 0;
    const next = () => {
      const zero = Math.random() < 0.35 ? (1 + Math.floor(Math.random() * 6)) : 0;  // positive zero error in divisions (LC 0.1 mm)
      const L = 10 + Math.floor(Math.random() * 60) + Math.floor(Math.random() * 10) / 10;   // true length, mm
      draw({ zero, L, obs: Math.round((L + zero * 0.1) * 10) / 10 });
    };
    const svg = (pos) => {   // pos = vernier zero position in mm on the main scale
      const k = 16, x0 = 20, start = Math.max(0, Math.floor(pos) - 12), w = x0 * 2 + 40 * k;
      let s = `<svg viewBox="0 0 ${w} 150" width="${w}" height="150" style="width:${w}px;max-width:none;min-width:0" class="jx-vsvg" role="img" aria-label="Vernier scale"><rect x="0" y="0" width="${w}" height="70" fill="#f8f3e3"/><rect x="0" y="70" width="${w}" height="70" fill="#e7f0ff"/>`;
      for (let m = start; m <= start + 40; m++) { const x = x0 + (m - start) * k; if (x > w - 5) break; const h = m % 10 === 0 ? 30 : m % 5 === 0 ? 22 : 14; s += `<line x1="${x}" y1="70" x2="${x}" y2="${70 - h}" stroke="#222" stroke-width="1"/>`; if (m % 10 === 0) s += `<text x="${x}" y="22" font-size="13" font-weight="700" text-anchor="middle">${m / 10}</text>`; }
      for (let v = 0; v <= 10; v++) { const x = x0 + (pos - start + v * 0.9) * k; const h = v % 5 === 0 ? 26 : 16; s += `<line x1="${x}" y1="70" x2="${x}" y2="${70 + h}" stroke="#1d4ed8" stroke-width="1.2"/>`; if (v % 5 === 0) s += `<text x="${x}" y="${112}" font-size="11" text-anchor="middle" fill="#1d4ed8">${v}</text>`; }
      return s + `<text x="${w - 6}" y="64" font-size="10" text-anchor="end">main scale (cm)</text><text x="${w - 6}" y="134" font-size="10" text-anchor="end" fill="#1d4ed8">vernier (10 div = 9 mm)</text></svg>`;
    };
    const draw = st => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Labs</button><div class="jx-card"><h3>📏 Vernier Simulator</h3><p class="jx-p">Least count 0.1 mm (10 vernier divisions = 9 main divisions). ${st.zero ? `<b>This calliper has a positive zero error of ${st.zero} divisions.</b> Give the CORRECT length.` : 'No zero error.'}</p>
        <div class="jx-vbox" id="jxVB">${svg(st.obs)}</div><p class="jx-fine">Find the main-scale mark just left of the vernier 0, then the vernier line that lines up exactly with a main-scale line. Scroll sideways if needed.</p>
        <div class="jx-num"><input id="jxV" inputmode="decimal" placeholder="Correct length in mm"></div><div class="jx-nav"><button class="jx-btn" id="jxVC">Check</button><button class="jx-btn ghost" id="jxVN">New reading</button></div><p id="jxVR"></p><p class="jx-fine">Score: ${right}/${tries}</p></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      const vb = $('#jxVB'); if (vb) vb.scrollLeft = Math.max(0, (vb.scrollWidth - vb.clientWidth) * 0.35);
      $('#jxVN').onclick = () => { tap(); next(); };
      $('#jxVC').onclick = () => {
        const v = parseFloat($('#jxV').value); if (isNaN(v)) return toast('Type the length in mm');
        tries++; const ok = Math.abs(v - st.L) < 0.05; if (ok) right++; tap(ok ? 'correct' : 'wrong');
        const msr = Math.floor(st.obs + 1e-9), vc = Math.round((st.obs - msr) * 10);
        $('#jxVR').innerHTML = `${ok ? '✅' : '❌'} MSR = ${msr} mm, coinciding vernier division = ${vc} → observed ${st.obs.toFixed(1)} mm${st.zero ? ` − zero error ${(st.zero * 0.1).toFixed(1)} mm = <b>${st.L.toFixed(1)} mm</b>` : ` = <b>${st.L.toFixed(1)} mm</b>`}. <button class="jx-lnk" id="jxVN2">Next ▶</button>`;
        $('#jxVN2').onclick = () => { tap(); next(); };
      };
    };
    next();
  }
  function screwLab(uid) {
    const el = screen(); let tries = 0, right = 0;
    const next = () => {
      const pitch = Math.random() < 0.5 ? 0.5 : 1, N = pitch === 0.5 ? 50 : 100, lc = pitch / N;
      const z = Math.random() < 0.4 ? (Math.random() < 0.5 ? 1 : -1) * (2 + Math.floor(Math.random() * 5)) : 0;
      const lin = pitch === 0.5 ? (2 + Math.floor(Math.random() * 12)) * 0.5 : 1 + Math.floor(Math.random() * 7), c = 3 + Math.floor(Math.random() * (N - 6));
      draw({ pitch, N, lc, z, lin, c, obs: lin + c * lc, true_: lin + c * lc - z * lc });
    };
    const svg = st => {
      const marks = 7; let s = `<svg viewBox="0 0 520 170" width="520" height="170" style="width:520px;max-width:none;min-width:0" class="jx-vsvg" role="img" aria-label="Screw gauge scales"><rect x="0" y="40" width="300" height="60" fill="#eef2f7"/><line x1="0" y1="70" x2="300" y2="70" stroke="#111" stroke-width="2"/>`;
      const per = st.pitch === 0.5 ? 2 : 1, px = 24;   // linear scale: mm marks above, half-mm below
      for (let m = 0; m <= st.lin * per; m++) { const x = 20 + m * px / per * (st.pitch === 0.5 ? 1 : 1); const half = st.pitch === 0.5 && m % 2 === 1; s += `<line x1="${x}" y1="70" x2="${x}" y2="${half ? 82 : 56}" stroke="#111"/>`; if (!half && (m / per) % 5 === 0) s += `<text x="${x}" y="50" font-size="11" text-anchor="middle">${m / per}</text>`; }
      const xe = 20 + st.lin * px; s += `<rect x="${xe}" y="10" width="120" height="150" rx="10" fill="#dbe7ff" stroke="#1d4ed8"/>`;
      for (let k = -marks; k <= marks; k++) { const div = ((st.c + k) % st.N + st.N) % st.N; const y = 70 - k * 9; s += `<line x1="${xe}" y1="${y}" x2="${xe + (div % 5 === 0 ? 26 : 16)}" y2="${y}" stroke="#1d4ed8"/>`; if (div % 5 === 0) s += `<text x="${xe + 30}" y="${y + 4}" font-size="10" fill="#1d4ed8">${div}</text>`; }
      return s + `<text x="${xe + 60}" y="168" font-size="10" text-anchor="middle" fill="#1d4ed8">circular scale (${st.N} div)</text></svg>`;
    };
    const draw = st => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Labs</button><div class="jx-card"><h3>🔩 Screw Gauge Simulator</h3><p class="jx-p">Pitch ${st.pitch} mm, ${st.N} circular divisions → LC = ${st.lc} mm. ${st.z ? `With the studs touching, the circular zero is <b>${Math.abs(st.z)} divisions ${st.z > 0 ? 'below' : 'above'}</b> the reference line. Give the CORRECT reading.` : 'No zero error.'}</p>
        <div class="jx-vbox">${svg(st)}</div><p class="jx-fine">Linear scale: last fully visible mark${st.pitch === 0.5 ? ' (half-mm marks are below the line)' : ''}. Circular scale: the division on the reference line.</p>
        <div class="jx-num"><input id="jxV" inputmode="decimal" placeholder="Correct reading in mm"></div><div class="jx-nav"><button class="jx-btn" id="jxVC">Check</button><button class="jx-btn ghost" id="jxVN">New reading</button></div><p id="jxVR"></p><p class="jx-fine">Score: ${right}/${tries}</p></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      $('#jxVN').onclick = () => { tap(); next(); };
      $('#jxVC').onclick = () => {
        const v = parseFloat($('#jxV').value); if (isNaN(v)) return toast('Type the reading in mm');
        tries++; const ok = Math.abs(v - st.true_) < st.lc / 2; if (ok) right++; tap(ok ? 'correct' : 'wrong');
        $('#jxVR').innerHTML = `${ok ? '✅' : '❌'} ${st.lin} + ${st.c} × ${st.lc} = ${st.obs.toFixed(3)} mm${st.z ? `; zero error ${st.z > 0 ? '+' : '−'}${Math.abs(st.z)} × ${st.lc} → correct = <b>${st.true_.toFixed(3)} mm</b>` : ` = <b>${st.true_.toFixed(3)} mm</b>`}. <button class="jx-lnk" id="jxVN2">Next ▶</button>`;
        $('#jxVN2').onclick = () => { tap(); next(); };
      };
    };
    next();
  }


  /* ---------- Try it yourself: Current Electricity ---------- */
  function circuitLab(uid) {
    const el = screen(); const st = { E: 9, r: 1, R1: 5, R2: 4, R3: 4, top: 'mix' }; const done = U(uid).lab || (U(uid).lab = {});
    const MIS = [['maxp', 'Make the bulb + load take MAXIMUM power from the cell', x => Math.abs(x.Req - x.r) < 0.05 && x.r > 0],
      ['half', 'Make the terminal voltage exactly half of the emf', x => x.r > 0 && Math.abs(x.V - x.E / 2) < 0.05],
      ['two', 'Draw exactly 2 A from the cell', x => Math.abs(x.I - 2) < 0.01],
      ['six', 'Build an equivalent load of exactly 6 Ω using R₁ + (R₂ ∥ R₃)', x => x.top === 'mix' && Math.abs(x.Req - 6) < 0.01],
      ['eff', 'Get the efficiency above 90 %', x => x.eff > 0.9],
      ['dim', 'In SERIES, make R₁ (the bulb) the brightest of the three', x => x.top === 'series' && x.P1 > x.P2 && x.P1 > x.P3]];
    const calc = () => {
      const p2 = st.R2 * st.R3 / (st.R2 + st.R3 || 1);
      const Req = st.top === 'series' ? st.R1 + st.R2 + st.R3 : st.top === 'par' ? 1 / (1 / st.R1 + 1 / st.R2 + 1 / st.R3) : st.R1 + p2;
      const I = st.E / (Req + st.r), V = I * Req;
      let P1, P2, P3;
      if (st.top === 'series') { P1 = I * I * st.R1; P2 = I * I * st.R2; P3 = I * I * st.R3; }
      else if (st.top === 'par') { P1 = V * V / st.R1; P2 = V * V / st.R2; P3 = V * V / st.R3; }
      else { P1 = I * I * st.R1; const Vp = I * p2; P2 = Vp * Vp / st.R2; P3 = Vp * Vp / st.R3; }
      return { ...st, Req, I, V, P1, P2, P3, Pl: V * I, eff: Req / (Req + st.r) };
    };
    const curve = x => {   // load power vs load resistance, 0..30 Ω
      const pts = []; let mx = 0; for (let R = 0; R <= 30; R += 0.25) { const P = x.E * x.E * R / ((R + x.r) ** 2 || 1); mx = Math.max(mx, P); pts.push([R, P]); }
      const X = R => 30 + R / 30 * 270, Y = P => 110 - P / (mx || 1) * 95;
      return `<svg viewBox="0 0 310 130" class="jx-curve"><line x1="30" y1="110" x2="305" y2="110" stroke="#c4b5fd"/><line x1="30" y1="10" x2="30" y2="110" stroke="#c4b5fd"/>
        <polyline fill="none" stroke="#7c3aed" stroke-width="2.5" points="${pts.map(([R, P]) => X(R).toFixed(1) + ',' + Y(P).toFixed(1)).join(' ')}"/>
        ${x.r > 0 ? `<line x1="${X(x.r)}" y1="12" x2="${X(x.r)}" y2="110" stroke="#f59e0b" stroke-dasharray="4 3"/><text x="${X(x.r) + 3}" y="22" font-size="10" fill="#b45309">R = r</text>` : ''}
        <circle cx="${X(Math.min(30, x.Req))}" cy="${Y(x.Pl)}" r="6" fill="#db2777"/><text x="34" y="125" font-size="10" fill="#6b6795">load resistance (0–30 Ω) →</text><text x="2" y="14" font-size="10" fill="#6b6795">P</text></svg>`;
    };
    const schem = x => {
      const sp = Math.max(0.25, 4 / Math.max(0.05, x.I)), glow = Math.min(1, x.P1 / 40);
      const bulb = (cx, cy) => `<circle cx="${cx}" cy="${cy}" r="14" fill="rgba(255,200,40,${0.15 + glow * 0.85})" stroke="#92400e"/><circle cx="${cx}" cy="${cy}" r="${10 + glow * 16}" fill="rgba(255,220,80,${glow * 0.35})"/><text x="${cx}" y="${cy + 30}" font-size="11" text-anchor="middle">R₁ ${x.R1} Ω</text>`;
      const box = (cx, cy, lab) => `<rect x="${cx - 18}" y="${cy - 8}" width="36" height="16" rx="3" fill="#ede9fe" stroke="#5b21b6"/><text x="${cx}" y="${cy + 24}" font-size="11" text-anchor="middle">${lab}</text>`;
      let mid;
      if (x.top === 'series') mid = bulb(90, 40) + box(170, 40, `R₂ ${x.R2} Ω`) + box(240, 40, `R₃ ${x.R3} Ω`);
      else if (x.top === 'par') mid = `<line x1="60" y1="40" x2="60" y2="130"/><line x1="270" y1="40" x2="270" y2="130"/>` + bulb(165, 40) + box(165, 85, `R₂ ${x.R2} Ω`) + box(165, 125, `R₃ ${x.R3} Ω`) + `<line x1="60" y1="85" x2="147" y2="85"/><line x1="183" y1="85" x2="270" y2="85"/><line x1="60" y1="125" x2="147" y2="125"/><line x1="183" y1="125" x2="270" y2="125"/>`;
      else mid = bulb(90, 40) + `<line x1="180" y1="40" x2="180" y2="100"/><line x1="270" y1="40" x2="270" y2="100"/>` + box(225, 40, `R₂ ${x.R2} Ω`) + box(225, 100, `R₃ ${x.R3} Ω`) + `<line x1="180" y1="100" x2="207" y2="100"/><line x1="243" y1="100" x2="270" y2="100"/>`;
      return `<svg viewBox="0 0 330 200" class="jx-circ" stroke="#1e1b4b" stroke-width="2" font-family="sans-serif"><path id="jxLoop" d="M30 40 H300 V170 H30 Z" fill="none"/>
        <path d="M30 40 H300 V170 H30 Z" fill="none" stroke="#c4b5fd" stroke-width="3"/>${mid}
        <rect x="140" y="160" width="50" height="20" fill="#fff" stroke="none"/><line x1="150" y1="155" x2="150" y2="185"/><line x1="160" y1="162" x2="160" y2="178" stroke-width="4"/><text x="165" y="198" font-size="11" text-anchor="middle" stroke="none" fill="#1e1b4b">E ${x.E} V, r ${x.r} Ω</text>
        ${[0, 1, 2, 3, 4, 5, 6, 7].map(k => `<circle r="3.5" fill="#f59e0b" stroke="none"><animateMotion dur="${sp.toFixed(2)}s" begin="-${(sp * k / 8).toFixed(2)}s" repeatCount="indefinite"><mpath href="#jxLoop"/></animateMotion></circle>`).join('')}</svg>`;
    };
    const sl = (k, lab, mn, mxv, stp) => `<label class="jx-sl"><span>${lab} <b id="v_${k}">${st[k]}</b></span><input type="range" min="${mn}" max="${mxv}" step="${stp}" value="${st[k]}" data-k="${k}"></label>`;
    const draw = () => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🔋 Circuit Playground</h3>
        <div class="jx-seg3">${[['series', 'All in series'], ['par', 'All in parallel'], ['mix', 'R₁ + (R₂ ∥ R₃)']].map(([k, n]) => `<button data-top="${k}" class="${st.top === k ? 'on' : ''}">${n}</button>`).join('')}</div>
        <div id="jxSch"></div><div class="jx-read" id="jxRead"></div>
        ${sl('E', 'EMF E (V)', 1, 24, 1)}${sl('r', 'Internal r (Ω)', 0, 6, 0.5)}${sl('R1', 'R₁ — the bulb (Ω)', 1, 20, 1)}${sl('R2', 'R₂ (Ω)', 1, 20, 1)}${sl('R3', 'R₃ (Ω)', 1, 20, 1)}
        <h3 style="margin-top:12px">📈 Power to the load vs load resistance</h3><div id="jxCurve"></div>
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-top]').forEach(b => b.onclick = () => { tap(); st.top = b.dataset.top; draw(); });
      el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value; upd(); });
      upd();
    };
    const upd = () => {
      const x = calc(), f = v => (Math.round(v * 100) / 100).toString();
      $('#jxSch').innerHTML = schem(x); $('#jxCurve').innerHTML = curve(x);
      $('#jxRead').innerHTML = `<span>R<sub>eq</sub> <b>${f(x.Req)} Ω</b></span><span>I <b>${f(x.I)} A</b></span><span>V<sub>terminal</sub> <b>${f(x.V)} V</b></span><span>P<sub>load</sub> <b>${f(x.Pl)} W</b></span><span>Bulb <b>${f(x.P1)} W</b></span><span>Efficiency <b>${Math.round(x.eff * 100)} %</b></span>`;
      let fresh = false; MIS.forEach(([k, , t]) => { if (!done[k] && t(x)) { done[k] = Date.now(); fresh = true; } });
      if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([k, n]) => `<div class="jx-mis ${done[k] ? 'ok' : ''}">${done[k] ? '✅' : '⬜'} ${n}</div>`).join('');
    };
    draw();
  }
  function bridgeLab(uid) {
    const el = screen(); let X, R = 10, l = 50, tries = 0, right = 0;
    const fresh = () => { X = [2, 2.5, 3, 4, 5, 6, 7.5, 8, 9, 12, 15][Math.floor(Math.random() * 11)]; R = 10; l = 50; draw(); };
    const defl = () => { const vg = R / (X + R), vw = (100 - l) / 100; return Math.max(-1, Math.min(1, (vw - vg) * 4)); };   // + : needle right
    const draw = () => {
      const a = defl() * 60, nul = Math.abs(defl()) < 0.01;
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🌉 Meter Bridge Lab</h3>
        <p class="jx-p">A <b>hidden resistor X</b> sits in the left gap and a box R in the right gap. Slide the jockey until the galvanometer reads zero, then work out X.</p>
        <svg viewBox="0 0 320 190" class="jx-circ" font-family="sans-serif"><rect x="40" y="20" width="70" height="26" rx="5" fill="#fee2e2" stroke="#b91c1c"/><text x="75" y="38" text-anchor="middle" font-size="13" font-weight="700">X = ?</text>
          <rect x="210" y="20" width="70" height="26" rx="5" fill="#ede9fe" stroke="#5b21b6"/><text x="245" y="38" text-anchor="middle" font-size="13">R = ${R} Ω</text>
          <path d="M20 33 H40 M110 33 H210 M280 33 H300 M20 33 V130 M300 33 V130" stroke="#1e1b4b" stroke-width="2" fill="none"/>
          <line x1="20" y1="130" x2="300" y2="130" stroke="#92400e" stroke-width="4"/>${[0, 20, 40, 60, 80, 100].map(c => `<text x="${20 + c * 2.8}" y="148" text-anchor="middle" font-size="9" fill="#6b6795">${c}</text>`).join('')}
          <circle cx="160" cy="80" r="22" fill="#fff" stroke="#1e1b4b" stroke-width="2"/><text x="160" y="72" text-anchor="middle" font-size="9">G</text><line x1="160" y1="88" x2="${160 + 18 * Math.sin(a * Math.PI / 180)}" y2="${88 - 18 * Math.cos(a * Math.PI / 180)}" stroke="${nul ? '#16a34a' : '#dc2626'}" stroke-width="3"/>
          <path d="M160 33 V58 M160 102 Q ${(160 + 20 + l * 2.8) / 2} 120 ${20 + l * 2.8} 128" stroke="#1e1b4b" stroke-width="2" fill="none"/><polygon points="${20 + l * 2.8 - 5},120 ${20 + l * 2.8 + 5},120 ${20 + l * 2.8},130" fill="#1e1b4b"/>
          <text x="160" y="178" text-anchor="middle" font-size="12" fill="${nul ? '#16a34a' : '#4b4878'}">${nul ? '✔ Galvanometer reads ZERO — null point!' : 'jockey at ' + l + ' cm'}</text></svg>
        <label class="jx-sl"><span>Jockey position <b>${l} cm</b></span><input type="range" min="1" max="99" step="0.5" value="${l}" id="jxL"></label><div class="jx-seg3"><button id="jxLm">◀ 0.5 cm</button><button id="jxLp">0.5 cm ▶</button></div>
        <label class="jx-sl"><span>Resistance box R <b>${R} Ω</b></span><input type="range" min="1" max="20" step="1" value="${R}" id="jxR"></label>
        <div class="jx-num"><input id="jxX" inputmode="decimal" placeholder="Your value of X in Ω"></div><div class="jx-nav"><button class="jx-btn" id="jxC">Check X</button><button class="jx-btn ghost" id="jxN2">New hidden X</button></div>
        <p id="jxRes"></p><p class="jx-fine">Score ${right}/${tries}. Tip: \\f{X}{R} = \\f{l}{100 − l}. Change R to bring the null point near the middle — that is where the bridge is most accurate.</p></div></div>`;
      el.querySelector('.jx-fine').innerHTML = `Score ${right}/${tries}. Tip: ${mx('\\f{X}{R} = \\f{l}{100 − l}')}. Change R to bring the null point near the middle — that is where the bridge is most accurate.`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      $('#jxL').oninput = e => { l = +e.target.value; draw(); };
      $('#jxLm').onclick = () => { tap(); l = Math.max(1, l - 0.5); draw(); }; $('#jxLp').onclick = () => { tap(); l = Math.min(99, l + 0.5); draw(); };
      $('#jxR').oninput = e => { R = +e.target.value; draw(); };
      $('#jxN2').onclick = () => { tap(); fresh(); };
      $('#jxC').onclick = () => {
        const v = parseFloat($('#jxX').value); if (isNaN(v)) return toast('Type X first'); tries++;
        const ok = Math.abs(v - X) <= 0.05 * X; if (ok) right++; tap(ok ? 'correct' : 'wrong');
        const lb = 100 * X / (X + R);
        $('#jxRes').innerHTML = `${ok ? '✅ Spot on!' : '❌ Not yet.'} With R = ${R} Ω the null point is at ${(Math.round(lb * 10) / 10)} cm, so X = R ×  ${(Math.round(lb * 10) / 10)}/${(Math.round((100 - lb) * 10) / 10)} = <b>${X} Ω</b>.`;
      };
    };
    fresh();
  }


  /* ---------- Try it yourself: Dual Nature ---------- */
  const lamColor = l => l < 380 ? '#7c3aed' : l < 440 ? `hsl(${270 - (l - 380)},90%,55%)` : l < 490 ? `hsl(${230 - (l - 440) * 1.2},90%,50%)` : l < 570 ? `hsl(${170 - (l - 490) * 1.4},85%,45%)` : l < 620 ? `hsl(${55 - (l - 570) * 0.6},95%,50%)` : l <= 750 ? `hsl(${25 - (l - 620) * 0.19},90%,50%)` : '#7f1d1d';
  function photoLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {});
    const MET = [['Caesium', 1.9], ['Potassium', 2.3], ['Sodium', 2.75], ['Zinc', 4.3], ['Platinum', 5.65]];
    const st = { m: 2, lam: 600, I: 60, V: 0 };
    const MIS = [['thr', 'Find the colour where electrons JUST start to come out of sodium (within 0.1 eV)', x => x.m === 2 && x.K >= 0 && x.K < 0.1],
      ['stop', 'Make the current exactly zero with the smallest retarding voltage (V ≈ V₀)', x => x.K > 0.2 && x.V >= x.K - 0.05 && x.V <= x.K + 0.05],
      ['int', 'Show that brightness does not matter below threshold: 100 % intensity, zero current', x => x.I >= 100 && x.K < 0],
      ['zinc', 'Get electrons out of zinc', x => x.m === 3 && x.K > 0],
      ['two', 'Give the fastest electrons exactly 2 eV (±0.05)', x => Math.abs(x.K - 2) <= 0.05]];
    const calc = () => { const E = 1240 / st.lam, K = E - MET[st.m][1], cur = K <= 0 ? 0 : st.V >= K ? 0 : st.I * (1 - st.V / K); return { ...st, E, K, cur }; };
    const sl = (k, lab, mn, mxv, stp, u) => `<label class="jx-sl"><span>${lab} <b id="v_${k}">${st[k]}${u}</b></span><input type="range" min="${mn}" max="${mxv}" step="${stp}" value="${st[k]}" data-k="${k}"></label>`;
    el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>⚡ Photoelectric Lab</h3>
      <div class="jx-seg3" style="flex-wrap:wrap">${MET.map(([n, w], i) => `<button data-m="${i}" class="${i === st.m ? 'on' : ''}">${n}<br><small>φ ${w} eV</small></button>`).join('')}</div>
      <div id="jxPh"></div><div class="jx-read" id="jxRead"></div>
      ${sl('lam', 'Wavelength λ', 150, 750, 5, ' nm')}<div class="jx-spec"></div>${sl('I', 'Intensity', 0, 100, 5, ' %')}${sl('V', 'Retarding voltage', 0, 6, 0.05, ' V')}
      <h3 style="margin-top:12px">📈 Current vs retarding voltage</h3><div id="jxIV"></div><h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
    $('#jxBack').onclick = () => unit(uid, 'lab');
    el.querySelectorAll('[data-m]').forEach(b => b.onclick = () => { tap(); st.m = +b.dataset.m; el.querySelectorAll('[data-m]').forEach(x => x.classList.toggle('on', x === b)); upd(); });
    el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value + ({ lam: ' nm', I: ' %', V: ' V' })[i.dataset.k]; upd(); });
    const upd = () => {
      const x = calc(), f = v => (Math.round(v * 100) / 100), col = lamColor(st.lam), n = x.K > 0 ? Math.round(st.I / 12) : 0, sp = x.K > 0 ? Math.max(0.6, 3 / Math.sqrt(x.K + 0.05)) : 0;
      $('#jxPh').innerHTML = `<svg viewBox="0 0 320 150" class="jx-circ"><defs><linearGradient id="jxBeam" x1="0" x2="1"><stop offset="0" stop-color="${col}" stop-opacity="${0.15 + st.I / 130}"/><stop offset="1" stop-color="${col}" stop-opacity="0.05"/></linearGradient></defs>
        <rect x="40" y="20" width="14" height="110" fill="#94a3b8"/><text x="47" y="145" text-anchor="middle" font-size="10">${MET[st.m][0]}</text><rect x="270" y="20" width="10" height="110" fill="#64748b"/><text x="275" y="145" text-anchor="middle" font-size="10">collector</text>
        <polygon points="160,0 210,0 54,90 54,60" fill="url(#jxBeam)"/>
        ${Array.from({ length: n }, (_, k) => `<circle r="3" fill="#2563eb"><animate attributeName="cx" values="56;${x.V >= x.K ? (56 + 190 * x.K / Math.max(x.V, 0.01)).toFixed(0) + ';56' : '268;268'}" dur="${sp}s" begin="-${(sp * k / n).toFixed(2)}s" repeatCount="indefinite"/><animate attributeName="cy" values="${30 + (k * 37) % 90};${30 + (k * 37) % 90}" dur="${sp}s" repeatCount="indefinite"/></circle>`).join('')}
        ${x.K <= 0 ? '<text x="160" y="80" text-anchor="middle" font-size="13" fill="#dc2626" font-weight="700">No electrons — photon energy below φ</text>' : ''}</svg>`;
      el.querySelector('.jx-spec').innerHTML = `<div style="height:10px;border-radius:6px;background:linear-gradient(90deg,#4c1d95 0%,#7c3aed 38%,#2563eb 48%,#16a34a 57%,#eab308 70%,#f97316 78%,#dc2626 92%,#7f1d1d 100%);position:relative"><span style="position:absolute;left:${(st.lam - 150) / 6}%;top:-4px;width:4px;height:18px;background:#111;border-radius:2px"></span></div><small class="jx-fine">UV ← visible (380–750 nm) → IR</small>`;
      $('#jxRead').innerHTML = `<span>Photon <b>${f(x.E)} eV</b></span><span>K<sub>max</sub> <b>${x.K > 0 ? f(x.K) + ' eV' : '—'}</b></span><span>V<sub>0</sub> <b>${x.K > 0 ? f(x.K) + ' V' : '—'}</b></span><span>Current <b>${f(x.cur)} μA</b></span><span>λ<sub>0</sub> <b>${Math.round(1240 / MET[st.m][1])} nm</b></span>`;
      const pts = []; for (let v = 0; v <= 6; v += 0.1) pts.push([v, x.K <= 0 ? 0 : v >= x.K ? 0 : st.I * (1 - v / x.K)]);
      $('#jxIV').innerHTML = `<svg viewBox="0 0 310 120" class="jx-curve"><line x1="30" y1="100" x2="305" y2="100" stroke="#c4b5fd"/><line x1="30" y1="5" x2="30" y2="100" stroke="#c4b5fd"/><polyline fill="none" stroke="#7c3aed" stroke-width="2.5" points="${pts.map(([v, i]) => (30 + v / 6 * 270).toFixed(1) + ',' + (100 - i * 0.9).toFixed(1)).join(' ')}"/><circle cx="${30 + st.V / 6 * 270}" cy="${100 - x.cur * 0.9}" r="5" fill="#db2777"/><text x="34" y="115" font-size="10" fill="#6b6795">retarding voltage 0 → 6 V</text></svg>`;
      let fresh = false; MIS.forEach(([k, , t]) => { if (!done['pe_' + k] && t(x)) { done['pe_' + k] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([k, n2]) => `<div class="jx-mis ${done['pe_' + k] ? 'ok' : ''}">${done['pe_' + k] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    upd();
  }
  function waveLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {});
    const PT = [['Electron', 9.11e-31, 1], ['Proton', 1.673e-27, 1], ['Alpha', 6.64e-27, 2], ['Neutron', 1.675e-27, 0], ['Cricket ball (160 g)', 0.16, 0]];
    const st = { p: 0, V: 100, v: 30 };
    const MIS = [['atom', 'Make an electron wave the size of an atom (0.1 nm, ±10 %)', x => x.p === 0 && Math.abs(x.lam - 1e-10) <= 1e-11], ['dg', 'Recreate Davisson–Germer: electron through 54 V', x => x.p === 0 && x.V === 54],
      ['ball', 'See why a cricket ball shows no wave nature (λ < 10^{−30} m)', x => x.p === 4 && x.lam < 1e-30], ['same', 'Give a proton a wavelength under 3 pm', x => x.p === 1 && x.lam < 3e-12]];
    const calc = () => { const [n, m, q] = PT[st.p]; const lam = q ? 6.626e-34 / Math.sqrt(2 * m * q * 1.602e-19 * st.V) : 6.626e-34 / (m * (st.p === 4 ? st.v : st.v * 1000)); return { ...st, lam }; };
    const fmtL = l => l >= 1e-9 ? (l * 1e9).toPrecision(3) + ' nm' : l >= 1e-12 ? (l * 1e12).toPrecision(3) + ' pm' : l >= 1e-15 ? (l * 1e15).toPrecision(3) + ' fm' : l.toExponential(2).replace('e', ' × 10^') + ' m';
    const draw = () => {
      const q = PT[st.p][2];
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🌊 Matter-Wave Explorer</h3>
        <div class="jx-seg3" style="flex-wrap:wrap">${PT.map(([n], i) => `<button data-p="${i}" class="${i === st.p ? 'on' : ''}">${n}</button>`).join('')}</div>
        <div id="jxW"></div><div class="jx-read" id="jxRead"></div>
        ${q ? `<label class="jx-sl"><span>Accelerating voltage <b id="v_V">${st.V} V</b></span><input type="range" min="1" max="10000" step="1" value="${st.V}" data-k="V"></label>`
            : `<label class="jx-sl"><span>Speed <b id="v_v">${st.v} ${st.p === 4 ? 'm/s' : 'km/s'}</b></span><input type="range" min="1" max="${st.p === 4 ? 45 : 3000}" step="1" value="${st.v}" data-k="v"></label>`}
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-p]').forEach(b => b.onclick = () => { tap(); st.p = +b.dataset.p; draw(); });
      el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value + (i.dataset.k === 'V' ? ' V' : st.p === 4 ? ' m/s' : ' km/s'); upd(); });
      upd();
    };
    const upd = () => {
      const x = calc(), lg = Math.log10(x.lam), pos = Math.max(0, Math.min(100, (lg + 36) / 30 * 100));
      const per = Math.max(6, Math.min(140, 40 * Math.pow(10, (lg + 10) / 3)));
      let path = 'M0 40'; for (let X = 0; X <= 300; X += 2) path += ` L${X} ${40 + 22 * Math.sin(2 * Math.PI * X / per)}`;
      $('#jxW').innerHTML = `<svg viewBox="0 0 300 80" class="jx-curve"><path d="${path}" fill="none" stroke="#7c3aed" stroke-width="2"/></svg>
        <div style="position:relative;height:46px;margin:8px 0 4px;background:linear-gradient(90deg,#fef3c7,#ede9fe,#dbeafe);border-radius:8px">
        ${[['ball', -33], ['nucleus', -15], ['atom', -10], ['X-ray', -10.5], ['light', -6.3]].map(([n, l]) => `<span style="position:absolute;left:${(l + 36) / 30 * 100}%;top:2px;font-size:9px;transform:translateX(-50%)">${n === 'X-ray' ? '' : n}</span>`).join('')}
        <span style="position:absolute;left:${pos}%;bottom:2px;transform:translateX(-50%);font-size:18px">▲</span></div><small class="jx-fine">${mx("log scale from 10^{−36} m to 10^{−6} m")}</small>`;
      $('#jxRead').innerHTML = `<span>λ <b>${fmtL(x.lam)}</b></span><span>${x.lam > 1e-11 && x.lam < 1e-9 ? '✅ diffracts from a crystal' : x.lam < 1e-30 ? '🚫 far too small to ever notice' : 'compare with atom ≈ 0.1 nm'}</span>`;
      let fresh = false; MIS.forEach(([k, , t]) => { if (!done['db_' + k] && t(x)) { done['db_' + k] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([k, n2]) => `<div class="jx-mis ${done['db_' + k] ? 'ok' : ''}">${done['db_' + k] ? '✅' : '⬜'} ${mx(n2)}</div>`).join('');
    };
    draw();
  }


  /* ---------- Try it yourself: Gravitation ---------- */
  function orbitLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {});
    const PL = { earth: ['🌍 Earth', 7.91, 6371, 84.4, '#2563eb'], moon: ['🌕 Moon', 1.68, 1737, 108.4, '#94a3b8'], mars: ['🔴 Mars', 3.55, 3390, 100.2, '#dc2626'] };
    const st = { p: 'earth', h: 1, v: 5.6 };
    const MIS = [['circ', 'Earth: put a satellite in a CIRCULAR orbit at height h = R (within 1 %)', x => x.p === 'earth' && Math.abs(x.h - 1) < 1e-9 && Math.abs(x.e) < 0.01],
      ['esc', 'Earth: launch from just above the surface (h ≤ 0.1R) and ESCAPE for ever', x => x.p === 'earth' && x.h <= 0.1 + 1e-9 && x.kind === 'escape'],
      ['ell', 'Make an ellipse whose far point is at least 3 times as far as its near point', x => x.kind === 'orbit' && x.ra >= 3 * x.rp],
      ['geo', 'Earth: build a GEOSTATIONARY orbit — circular, period 24 h (±2 %)', x => x.p === 'earth' && Math.abs(x.e) < 0.01 && Math.abs(x.T / 60 - 24) < 0.48],
      ['moon', 'Moon: get into any circular orbit (within 1 %)', x => x.p === 'moon' && x.kind === 'orbit' && Math.abs(x.e) < 0.01]];
    const calc = () => {
      const [, vs, Rkm, Tmin] = PL[st.p], r0 = 1 + st.h, u = st.v / vs, E = u * u / 2 - 1 / r0, L = r0 * u, e = Math.sqrt(Math.max(0, 1 + 2 * E * L * L));
      const vc = vs / Math.sqrt(r0), ve = vs * Math.sqrt(2 / r0);
      if (E >= 0) return { kind: 'escape', e, L, r0, u, vc, ve, E, T: Infinity, rp: L * L / (1 + e), ra: Infinity, ...st };
      const a = -1 / (2 * E), rp = a * (1 - e), ra = a * (1 + e);
      return { kind: rp < 1 ? 'crash' : 'orbit', e, L, r0, u, vc, ve, E, a, rp, ra, T: Tmin * Math.pow(a, 1.5), ...st };
    };
    const draw = () => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🛰️ Orbit Launcher</h3>
        <p class="jx-fine">Fire a satellite sideways from a tower. Too slow and it falls back; just right and it circles; fast enough and it escapes for ever.</p>
        <div class="jx-seg3">${Object.entries(PL).map(([k, p]) => `<button data-p="${k}" class="${k === st.p ? 'on' : ''}">${p[0]}</button>`).join('')}</div>
        <svg viewBox="-160 -160 320 320" class="jx-circ" id="jxOrb" style="max-width:340px;background:#0b1026;border-radius:16px"></svg><div class="jx-read" id="jxRead"></div>
        <label class="jx-sl"><span>Launch height h <b id="v_h">${st.h} R</b></span><input type="range" min="0.05" max="6" step="0.05" value="${st.h}" data-k="h"></label>
        <label class="jx-sl"><span>Launch speed (sideways) <b id="v_v">${st.v} km/s</b></span><input type="range" min="0" max="15" step="0.01" value="${st.v}" data-k="v"></label>
        <div class="jx-seg3"><button id="jxVc">Set circular speed</button><button id="jxVe">Set escape speed</button></div>
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-p]').forEach(b => b.onclick = () => { tap(); st.p = b.dataset.p; draw(); });
      el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value + (i.dataset.k === 'h' ? ' R' : ' km/s'); upd(); });
      $('#jxVc').onclick = () => { tap(); st.v = +calc().vc.toFixed(2); draw(); };
      $('#jxVe').onclick = () => { tap(); st.v = +(calc().ve + 0.01).toFixed(2); draw(); };
      upd();
    };
    const upd = () => {
      const x = calc(), col = PL[st.p][4], sc = 150 / Math.max(3, Math.min(14, x.kind === 'orbit' ? x.ra * 1.1 : x.r0 * 2.2));
      const out = x.u * x.u * x.r0 >= 1 ? 0 : Math.PI, pts = [];
      for (let k = 0; k <= 720; k++) { const th = k / 720 * 2 * Math.PI, den = 1 + x.e * Math.cos(th - out); if (den <= 1e-6) continue; const r = x.L * x.L / den; if (r > 40) continue;
        if (x.kind === 'crash' && r < 1) continue; pts.push([r * Math.cos(th) * sc, -r * Math.sin(th) * sc]); }
      const path = pts.map((p, k) => (k ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' ');
      $('#jxOrb').innerHTML = `${Array.from({ length: 40 }, (_, k) => `<circle cx="${(k * 97) % 320 - 160}" cy="${(k * 53) % 320 - 160}" r="0.8" fill="#fff" opacity=".5"/>`).join('')}
        <circle cx="0" cy="0" r="${sc}" fill="${col}"/><circle cx="0" cy="0" r="${sc}" fill="none" stroke="#fff" stroke-opacity=".25"/>
        <line x1="${sc}" y1="0" x2="${x.r0 * sc}" y2="0" stroke="#e5e7eb" stroke-width="2"/>
        <path d="${path}" fill="none" stroke="${x.kind === 'escape' ? '#f97316' : x.kind === 'crash' ? '#ef4444' : '#22c55e'}" stroke-width="2" stroke-dasharray="${x.kind === 'escape' ? '6 4' : ''}"/>
        <circle cx="${x.r0 * sc}" cy="0" r="5" fill="#fde047"/><line x1="${x.r0 * sc}" y1="0" x2="${x.r0 * sc}" y2="${-Math.min(60, 12 + st.v * 4)}" stroke="#fde047" stroke-width="2" marker-end="url(#ar)"/>
        <defs><marker id="ar" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#fde047"/></marker></defs>
        <text x="-150" y="-140" fill="#fff" font-size="12" font-weight="700">${x.kind === 'escape' ? '🚀 ESCAPES' : x.kind === 'crash' ? '💥 falls back and hits the ground' : x.e < 0.01 ? '⭕ circular orbit' : '🥚 elliptical orbit'}</text>`;
      const tt = m => m === Infinity ? '—' : m < 120 ? m.toFixed(0) + ' min' : (m / 60).toFixed(1) + ' h';
      $('#jxRead').innerHTML = `<span>v<sub>circular</sub> <b>${x.vc.toFixed(2)} km/s</b></span><span>v<sub>escape</sub> <b>${x.ve.toFixed(2)} km/s</b></span><span>total energy <b>${x.E >= 0 ? '≥ 0' : '< 0 (bound)'}</b></span>${x.kind === 'orbit' ? `<span>period <b>${tt(x.T)}</b></span><span>near/far <b>${(x.rp - 1).toFixed(2)}R / ${(x.ra - 1).toFixed(2)}R</b> (height)</span>` : ''}`;
      let fresh = false; MIS.forEach(([kk, , t]) => { if (!done['gv_' + kk] && t(x)) { done['gv_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['gv_' + kk] ? 'ok' : ''}">${done['gv_' + kk] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    draw();
  }

  /* ---------- Try it yourself: Electrostatics ---------- */
  function chargeLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {}), K = 9e9;
    const st = { a: 3, b: 1, d: 6, x: 5, y: 4 };
    const fieldAt = (x, y) => {   // x, y in cm → E (N/C) and V (volts)
      let ex = 0, ey = 0, v = 0, rmin = 1e9;
      [[st.a, -st.d / 2], [st.b, st.d / 2]].forEach(([q, cx]) => { if (!q) return; const dx = (x - cx) / 100, dy = y / 100, r = Math.hypot(dx, dy); rmin = Math.min(rmin, r * 100); if (r < 1e-9) return;
        const f = K * q * 1e-6 / (r * r * r); ex += f * dx; ey += f * dy; v += K * q * 1e-6 / r; });
      return { ex, ey, E: Math.hypot(ex, ey), v, rmin };
    };
    const ref = () => K * Math.max(Math.abs(st.a), Math.abs(st.b), 1) * 1e-6 / 1e-4;   // field of the bigger charge at 1 cm
    const MIS = [['null', 'Find a NULL point: put P where the field is zero (charges switched on)', x => st.a && st.b && x.rmin > 0.2 && x.E < 1e-6 * ref()],
      ['up', 'Make the field at P point straight UP (+y) with both charges switched on', x => st.a && st.b && st.y > 0 && Math.abs(x.ex) < 1e-6 * x.E && x.ey > 0],
      ['dip', 'Build a DIPOLE and put P on its equatorial line: the field there must be parallel to the axis', x => st.a && st.a === -st.b && st.x === 0 && st.y > 0],
      ['v0', 'With UNEQUAL charges, find a point where V = 0 but E ≠ 0', x => st.a && st.b && Math.abs(st.a) !== Math.abs(st.b) && x.rmin > 0.2 && Math.abs(x.v) < 1e-6 * ref() * 0.01 && x.E > 0],
      ['big', 'Get |E| at P above 5 × 10⁸ N/C while P stays at least 1 cm from every charge', x => x.rmin >= 1 - 1e-9 && x.E >= 5e8]];
    const sx = x => x * 10, sy = y => -y * 10;
    const draw = () => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>⚡ Field Line Studio</h3>
        <p class="jx-fine">Two point charges A and B sit on the x-axis. Set their charges and gap, then move the probe P (sliders, or tap the picture). Lines leave + charges and end on − charges.</p>
        <svg viewBox="-160 -120 320 240" class="jx-circ" id="jxEs" style="max-width:360px;background:#0f172a;border-radius:16px;touch-action:manipulation"></svg><div class="jx-read" id="jxRead"></div>
        <label class="jx-sl"><span>Charge A <b id="v_a">${st.a} μC</b></span><input type="range" min="-5" max="5" step="1" value="${st.a}" data-k="a"></label>
        <label class="jx-sl"><span>Charge B <b id="v_b">${st.b} μC</b></span><input type="range" min="-5" max="5" step="1" value="${st.b}" data-k="b"></label>
        <label class="jx-sl"><span>Gap A–B <b id="v_d">${st.d} cm</b></span><input type="range" min="2" max="12" step="1" value="${st.d}" data-k="d"></label>
        <label class="jx-sl"><span>Probe P: x <b id="v_x">${st.x} cm</b></span><input type="range" min="-15" max="15" step="0.5" value="${st.x}" data-k="x"></label>
        <label class="jx-sl"><span>Probe P: y <b id="v_y">${st.y} cm</b></span><input type="range" min="0" max="10" step="0.5" value="${st.y}" data-k="y"></label>
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      const unitOf = k => (k === 'a' || k === 'b') ? ' μC' : ' cm';
      el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value + unitOf(i.dataset.k); upd(); });
      $('#jxEs').onclick = ev => { const bb = ev.currentTarget.getBoundingClientRect(), X = ((ev.clientX - bb.left) / bb.width * 320 - 160) / 10, Y = -((ev.clientY - bb.top) / bb.height * 240 - 120) / 10;
        st.x = Math.max(-15, Math.min(15, Math.round(X * 2) / 2)); st.y = Math.max(0, Math.min(10, Math.round(Y * 2) / 2)); tap();
        ['x', 'y'].forEach(k => { const i = el.querySelector(`[data-k="${k}"]`); i.value = st[k]; $('#v_' + k).textContent = st[k] + ' cm'; }); upd(); };
      upd();
    };
    const lines = () => {
      const out = [], Q = [[st.a, -st.d / 2], [st.b, st.d / 2]];
      Q.forEach(([q, cx]) => { if (!q) return; const n = Math.min(24, 4 * Math.abs(q)), dir = q > 0 ? 1 : -1;
        if (dir < 0 && Q.some(([q2]) => q2 > 0)) return;   // lines from + charges already reach the − ones
        for (let k = 0; k < n; k++) { const th = 2 * Math.PI * (k + 0.5) / n; let x = cx + 0.3 * Math.cos(th), y = 0.3 * Math.sin(th); const pts = [[x, y]];
          for (let s = 0; s < 500; s++) { let ex = 0, ey = 0, hit = false;
            Q.forEach(([q2, c2]) => { if (!q2) return; const dx = x - c2, r = Math.hypot(dx, y); if (r < 0.25 && s > 2) hit = true; const f = q2 / (r * r * r); ex += f * dx; ey += f * y; });
            const m = Math.hypot(ex, ey); if (hit || !m) break; x += dir * 0.2 * ex / m; y += dir * 0.2 * ey / m; pts.push([x, y]); if (Math.abs(x) > 17 || Math.abs(y) > 13) break; }
          out.push(pts.map((p, i) => (i ? 'L' : 'M') + sx(p[0]).toFixed(1) + ' ' + sy(p[1]).toFixed(1)).join(' ')); } });
      return out;
    };
    const upd = () => {
      const x = fieldAt(st.x, st.y), col = q => q > 0 ? '#ef4444' : q < 0 ? '#3b82f6' : '#64748b';
      const L = 28, ux = x.E ? x.ex / x.E : 0, uy = x.E ? x.ey / x.E : 0;
      $('#jxEs').innerHTML = `<defs><marker id="esA" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#fde047"/></marker></defs>
        <line x1="-160" y1="0" x2="160" y2="0" stroke="#334155"/>${lines().map(d => `<path d="${d}" fill="none" stroke="#94a3b8" stroke-opacity=".55" stroke-width="1"/>`).join('')}
        ${[[st.a, -st.d / 2, 'A'], [st.b, st.d / 2, 'B']].map(([q, cx, n]) => `<circle cx="${sx(cx)}" cy="0" r="9" fill="${col(q)}"/><text x="${sx(cx)}" y="4" fill="#fff" font-size="10" text-anchor="middle" font-weight="700">${q > 0 ? '+' : q < 0 ? '−' : '0'}</text><text x="${sx(cx)}" y="22" fill="#cbd5e1" font-size="10" text-anchor="middle">${n}</text>`).join('')}
        <circle cx="${sx(st.x)}" cy="${sy(st.y)}" r="5" fill="#fde047"/><text x="${sx(st.x) + 7}" y="${sy(st.y) - 7}" fill="#fde047" font-size="11" font-weight="700">P</text>
        ${x.E ? `<line x1="${sx(st.x)}" y1="${sy(st.y)}" x2="${sx(st.x) + L * ux}" y2="${sy(st.y) - L * uy}" stroke="#fde047" stroke-width="2.5" marker-end="url(#esA)"/>` : ''}`;
      const f = v => { const a = Math.abs(v); if (a < 1e-3) return '0'; const e = Math.floor(Math.log10(a)), m = v / 10 ** e; return e >= -2 && e <= 3 ? v.toFixed(e < 1 ? 2 : 0) : m.toFixed(2) + ' × 10<sup>' + e + '</sup>'; };
      $('#jxRead').innerHTML = `<span>|E| at P <b>${x.E < 1e-6 * ref() ? '0 (null point!)' : f(x.E) + ' N/C'}</b></span><span>E<sub>x</sub>, E<sub>y</sub> <b>${f(x.ex)}, ${f(x.ey)}</b></span><span>V at P <b>${Math.abs(x.v) < 1e-8 * ref() ? '0' : f(x.v) + ' V'}</b></span>`;
      let fresh = false; MIS.forEach(([kk, , t]) => { if (!done['es_' + kk] && t(x)) { done['es_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['es_' + kk] ? 'ok' : ''}">${done['es_' + kk] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    draw();
  }

  /* ---------- Try it yourself: Thermodynamics ---------- */
  function pvLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {}), Rg = 8.314;
    const n = 100 / (Rg * 300);                       // start: 1 × 10⁵ Pa, 1 L, 300 K
    const st = { f: 3, kind: 'iso', k: 2, path: [], P: 1, V: 1 }, PU = 1e5, VU = 1e-3;
    const g = () => 1 + 2 / st.f, T = (P, V) => P * PU * V * VU / (n * Rg);
    const step = () => {   // apply one process with factor k
      const P0 = st.P, V0 = st.V, k = st.k, gm = g(); let P1, V1, W, pts = [];
      if (st.kind === 'iso') { V1 = V0 * k; P1 = P0 * V0 / V1; W = P0 * PU * V0 * VU * Math.log(k); }
      else if (st.kind === 'adia') { V1 = V0 * k; P1 = P0 * Math.pow(V0 / V1, gm); W = (P0 * V0 - P1 * V1) * PU * VU / (gm - 1); }
      else if (st.kind === 'bar') { V1 = V0 * k; P1 = P0; W = P0 * PU * (V1 - V0) * VU; }
      else { V1 = V0; P1 = P0 * k; W = 0; }
      for (let i = 0; i <= 40; i++) { const v = V0 + (V1 - V0) * i / 40; pts.push([v, st.kind === 'iso' ? P0 * V0 / v : st.kind === 'adia' ? P0 * Math.pow(V0 / v, gm) : st.kind === 'bar' ? P0 : P0 + (P1 - P0) * i / 40]); }
      const dU = n * st.f / 2 * Rg * (T(P1, V1) - T(P0, V0));
      st.path.push({ kind: st.kind, k, W, dU, Q: dU + W, pts }); st.P = P1; st.V = V1;
    };
    const tot = () => st.path.reduce((a, s) => ({ W: a.W + s.W, Q: a.Q + s.Q, dU: a.dU + s.dU }), { W: 0, Q: 0, dU: 0 });
    const closed = () => st.path.length >= 2 && Math.abs(st.P - 1) < 0.01 && Math.abs(st.V - 1) < 0.01;
    const MIS = [['iso2', 'Double the volume ISOTHERMALLY — and see that Q = W', x => x.path.some(s => s.kind === 'iso' && Math.abs(s.k - 2) < 1e-9)],
      ['hot', 'Raise the temperature by at least 50 % without giving the gas ANY heat', x => x.path.length && x.path.every(s => Math.abs(s.Q) < 1e-6) && T(x.P, x.V) >= 450 - 1e-6],
      ['engine', 'Build a closed cycle (back to the start) in which the gas does POSITIVE net work', x => closed() && tot().W > 1e-6],
      ['fridge', 'Build a closed cycle in which net work is done ON the gas', x => closed() && tot().W < -1e-6],
      ['carnot', 'Carnot cycle: close a loop using only isothermal and adiabatic steps, with net work > 0', x => closed() && tot().W > 1e-6 && x.path.every(s => s.kind === 'iso' || s.kind === 'adia')]];
    const NM = { iso: 'Isothermal', adia: 'Adiabatic', bar: 'Isobaric', chor: 'Isochoric' };
    const draw = () => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🔥 P–V Process Lab</h3>
        <p class="jx-fine">Start: 1 × 10⁵ Pa, 1 L, 300 K. Pick a process and a factor, then press <b>Apply</b>. The table keeps Q (heat in), W (work by gas) and ΔU for every step — check the first law Q = ΔU + W yourself.</p>
        <div class="jx-seg3"><button data-f="3" class="${st.f === 3 ? 'on' : ''}">Monoatomic</button><button data-f="5" class="${st.f === 5 ? 'on' : ''}">Diatomic</button></div>
        <svg viewBox="0 0 320 220" class="jx-circ" id="jxPV" style="max-width:360px;background:#fff7ed;border-radius:14px"></svg><div class="jx-read" id="jxRead"></div>
        <div class="jx-seg3" style="flex-wrap:wrap">${Object.entries(NM).map(([k, v]) => `<button data-kind="${k}" class="${k === st.kind ? 'on' : ''}">${v}</button>`).join('')}</div>
        <label class="jx-sl"><span id="jxKl">${st.kind === 'chor' ? 'Pressure × ' : 'Volume × '} <b id="v_k">${st.k}</b></span><input type="range" min="0.25" max="4" step="0.25" value="${st.k}" data-k="k"></label>
        <div class="jx-seg3"><button id="jxGo">➕ Apply step</button><button id="jxUndo">↩ Undo</button><button id="jxReset">⟲ Reset</button></div>
        <div id="jxTab"></div><h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-f]').forEach(b => b.onclick = () => { tap(); st.f = +b.dataset.f; st.path = []; st.P = 1; st.V = 1; draw(); });
      el.querySelectorAll('[data-kind]').forEach(b => b.onclick = () => { tap(); st.kind = b.dataset.kind; draw(); });
      el.querySelector('[data-k="k"]').oninput = e => { st.k = +e.target.value; $('#v_k').textContent = st.k; };
      $('#jxGo').onclick = () => { if (st.k === 1) return toast('Factor 1 changes nothing'); const nv = st.kind === 'chor' ? st.V : st.V * st.k; if (nv > 16 || nv < 1 / 16) return toast('That is off the chart — try a smaller factor'); tap(); step(); upd(); };
      $('#jxUndo').onclick = () => { const s = st.path.pop(); if (s) { st.P = s.pts[0][1]; st.V = s.pts[0][0]; } tap(); upd(); };
      $('#jxReset').onclick = () => { st.path = []; st.P = 1; st.V = 1; tap(); upd(); };
      upd();
    };
    const upd = () => {
      const all = st.path.flatMap(s => s.pts).concat([[1, 1], [st.V, st.P]]), Vm = Math.max(2, ...all.map(p => p[0])) * 1.1, Pm = Math.max(2, ...all.map(p => p[1])) * 1.1;
      const X = v => 34 + v / Vm * 276, Y = p => 196 - p / Pm * 180, col = { iso: '#2563eb', adia: '#dc2626', bar: '#16a34a', chor: '#9333ea' };
      $('#jxPV').innerHTML = `<line x1="34" y1="196" x2="314" y2="196" stroke="#78350f"/><line x1="34" y1="196" x2="34" y2="10" stroke="#78350f"/>
        <text x="284" y="214" font-size="11" fill="#78350f">V (L)</text><text x="4" y="14" font-size="11" fill="#78350f">P</text>
        ${st.path.map(s => `<path d="${s.pts.map((p, i) => (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1)).join(' ')}" fill="none" stroke="${col[s.kind]}" stroke-width="3"/>`).join('')}
        <circle cx="${X(1)}" cy="${Y(1)}" r="5" fill="#f59e0b"/><text x="${X(1) + 6}" y="${Y(1) - 6}" font-size="10" fill="#92400e">start</text><circle cx="${X(st.V)}" cy="${Y(st.P)}" r="5" fill="#111827"/>`;
      const t = tot(), J = v => (Math.abs(v) < 0.05 ? '0' : v.toFixed(1)) + ' J';
      $('#jxRead').innerHTML = `<span>now <b>${(st.P * 1).toFixed(3)} × 10⁵ Pa, ${st.V.toFixed(3)} L, ${T(st.P, st.V).toFixed(0)} K</b></span><span>total Q <b>${J(t.Q)}</b></span><span>total W <b>${J(t.W)}</b></span><span>total ΔU <b>${J(t.dU)}</b></span>${closed() ? '<span>✅ <b>back at the start — a closed cycle</b></span>' : ''}`;
      $('#jxTab').innerHTML = st.path.length ? `<div class="jx-fine" style="margin-top:6px">${st.path.map((s, i) => `${i + 1}. ${NM[s.kind]} ×${s.k}: Q ${J(s.Q)}, W ${J(s.W)}, ΔU ${J(s.dU)}`).join('<br>')}</div>` : '';
      let fresh = false; MIS.forEach(([kk, , tt]) => { if (!done['td_' + kk] && tt(st)) { done['td_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['td_' + kk] ? 'ok' : ''}">${done['td_' + kk] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    draw();
  }

  /* ---------- Try it yourself: Kinetic Theory of Gases ---------- */
  function boxLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {}), kB = 1.38e-23, Rg = 8.314;
    const GM = { He: 4, Ne: 20, N2: 28, O2: 32 }, st = { g: 'He', T: 300, N: 20, V: 2 };
    const vr = (g, T) => Math.sqrt(3 * Rg * T / (GM[g] * 1e-3)), P = () => st.N * st.T / st.V / (20 * 300 / 2);
    const MIS = [['dbl', 'Make He molecules move exactly TWICE as fast (v_rms) as at 300 K', x => x.g === 'He' && Math.abs(vr('He', x.T) / vr('He', 300) - 2) < 1e-9],
      ['p4', 'Make the pressure exactly 4 times the starting pressure', x => Math.abs(P() - 4) < 1e-9],
      ['twiceN', 'With TWICE as many molecules as at the start, get back the starting pressure', x => x.N === 40 && Math.abs(P() - 1) < 1e-9],
      ['o2he', 'Switch to O₂ and make its v_rms equal to helium\'s at 300 K', x => x.g === 'O2' && Math.abs(vr('O2', x.T) - vr('He', 300)) < 1e-6],
      ['ke', 'Make the average KE per molecule about 0.1 eV (within 3 %)', x => Math.abs(1.5 * kB * x.T / 1.6e-19 / 0.1 - 1) < 0.03]];
    let parts = [], raf = 0;
    const seed = () => { parts = Array.from({ length: st.N }, (_, i) => { const a = (i * 2.399) % (2 * Math.PI); return { x: 0.1 + 0.8 * ((i * 0.618) % 1), y: 0.1 + 0.8 * ((i * 0.381) % 1), a }; }); };
    const draw = () => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🫧 Molecule Box</h3>
        <p class="jx-fine">Molecules fly about and bounce off the walls. Hotter → faster; heavier → slower; more molecules or a smaller box → more hits on the walls (pressure). Start: 20 He molecules, 300 K, box 2 units.</p>
        <div class="jx-seg3" style="flex-wrap:wrap">${Object.keys(GM).map(k => `<button data-g="${k}" class="${k === st.g ? 'on' : ''}">${k.replace('2', '₂')}</button>`).join('')}</div>
        <svg viewBox="0 0 320 200" class="jx-circ" id="jxBox" style="max-width:360px;background:#0f172a;border-radius:14px"></svg><div class="jx-read" id="jxRead"></div>
        <label class="jx-sl"><span>Temperature <b id="v_T">${st.T} K</b></span><input type="range" min="100" max="2400" step="50" value="${st.T}" data-k="T"></label>
        <label class="jx-sl"><span>Molecules <b id="v_N">${st.N}</b></span><input type="range" min="10" max="60" step="5" value="${st.N}" data-k="N"></label>
        <label class="jx-sl"><span>Box volume <b id="v_V">${st.V}</b></span><input type="range" min="0.5" max="4" step="0.5" value="${st.V}" data-k="V"></label>
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => { cancelAnimationFrame(raf); unit(uid, 'lab'); };
      el.querySelectorAll('[data-g]').forEach(b => b.onclick = () => { tap(); st.g = b.dataset.g; cancelAnimationFrame(raf); draw(); });
      el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value + (i.dataset.k === 'T' ? ' K' : ''); if (i.dataset.k === 'N') seed(); upd(); });
      seed(); upd(); anim();
    };
    const anim = () => {
      const svg = $('#jxBox'); if (!svg || !document.body.contains(svg)) return;
      const W = 40 + st.V / 4 * 260, sp = vr(st.g, st.T) / 1370 * 0.012;
      parts.forEach(p => { p.x += Math.cos(p.a) * sp * 320 / W; p.y += Math.sin(p.a) * sp;
        if (p.x < 0 || p.x > 1) { p.a = Math.PI - p.a; p.x = Math.max(0, Math.min(1, p.x)); } if (p.y < 0 || p.y > 1) { p.a = -p.a; p.y = Math.max(0, Math.min(1, p.y)); } });
      svg.innerHTML = `<rect x="10" y="10" width="${W}" height="180" fill="none" stroke="#94a3b8" stroke-width="2"/><rect x="${10 + W}" y="10" width="8" height="180" fill="#64748b"/>
        ${parts.map(p => `<circle cx="${(10 + p.x * W).toFixed(1)}" cy="${(10 + p.y * 180).toFixed(1)}" r="${2.5 + GM[st.g] / 12}" fill="${st.T > 1200 ? '#f97316' : st.T > 600 ? '#facc15' : '#38bdf8'}"/>`).join('')}`;
      raf = requestAnimationFrame(anim);
    };
    const upd = () => {
      $('#jxRead').innerHTML = `<span>v<sub>rms</sub> <b>${vr(st.g, st.T).toFixed(0)} m/s</b></span><span>avg KE <b>${(1.5 * kB * st.T / 1.6e-19).toFixed(3)} eV</b></span><span>pressure <b>${P().toFixed(2)} × start</b></span>`;
      let fresh = false; MIS.forEach(([kk, , tt]) => { if (!done['kg_' + kk] && tt(st)) { done['kg_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['kg_' + kk] ? 'ok' : ''}">${done['kg_' + kk] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    draw();
  }

  /* ---------- Try it yourself: Electromagnetic Waves ---------- */
  function emLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {}), c = 3e8, e0 = 8.85e-12;
    const FQ = [1, 2, 5, 10, 20, 50, 60, 100, 200, 300, 500, 1000, 2000, 3000];
    const st = { fi: 3, E0: 100, dir: 1, E: 'y' }, AX = { y: [0, 1, 0], '-y': [0, -1, 0], z: [0, 0, 1], '-z': [0, 0, -1] };
    const cr = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
    const nm = v => (v[0] + v[1] + v[2] < 0 ? '−' : '+') + (v[0] ? 'x' : v[1] ? 'y' : 'z');
    const calc = () => { const f = FQ[st.fi] * 1e6, lam = c / f, B = cr([st.dir, 0, 0], AX[st.E]); return { f, lam, B, Bn: nm(B), B0: st.E0 / c, I: 0.5 * c * e0 * st.E0 * st.E0 }; };
    const MIS = [['lam5', 'Make a wave with wavelength exactly 5 m', x => Math.abs(x.lam - 5) < 1e-9],
      ['bz', 'Make the magnetic field point along +z', x => x.Bn === '+z'],
      ['bny', 'Send the wave towards −x with its magnetic field along −y', x => st.dir === -1 && x.Bn === '−y'],
      ['int', 'Tune the intensity to between 50 and 60 W/m²', x => x.I >= 50 && x.I <= 60],
      ['micro', 'Make it a MICROWAVE (λ between 1 mm and 30 cm)', x => x.lam > 1e-3 && x.lam < 0.3]];
    let ph = 0, raf = 0;
    const draw = () => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🌊 EM Wave Builder</h3>
        <p class="jx-fine">Red = electric field, blue = magnetic field. They are always at right angles to each other and to the direction of travel, and \\(\\vec E\\times\\vec B\\) points the way the wave goes.</p>
        <svg viewBox="0 0 320 180" class="jx-circ" id="jxEM" style="max-width:360px;background:#0f172a;border-radius:14px"></svg><div class="jx-read" id="jxRead"></div>
        <div class="jx-seg3"><button data-dir="1" class="${st.dir === 1 ? 'on' : ''}">Travel +x ➡</button><button data-dir="-1" class="${st.dir === -1 ? 'on' : ''}">⬅ Travel −x</button></div>
        <div class="jx-seg3" style="flex-wrap:wrap">${Object.keys(AX).map(k => `<button data-e="${k}" class="${k === st.E ? 'on' : ''}">E along ${k.replace('-', '−')}</button>`).join('')}</div>
        <label class="jx-sl"><span>Frequency <b id="v_f">${FQ[st.fi]} MHz</b></span><input type="range" min="0" max="${FQ.length - 1}" step="1" value="${st.fi}" data-k="fi"></label>
        <label class="jx-sl"><span>E amplitude <b id="v_E0">${st.E0} V/m</b></span><input type="range" min="50" max="1000" step="50" value="${st.E0}" data-k="E0"></label>
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      el.querySelector('.jx-fine').innerHTML = 'Red = electric field E, blue = magnetic field B. They are always at right angles to each other and to the direction of travel, and E × B points the way the wave goes.';
      $('#jxBack').onclick = () => { cancelAnimationFrame(raf); unit(uid, 'lab'); };
      el.querySelectorAll('[data-dir]').forEach(b => b.onclick = () => { tap(); st.dir = +b.dataset.dir; cancelAnimationFrame(raf); draw(); });
      el.querySelectorAll('[data-e]').forEach(b => b.onclick = () => { tap(); st.E = b.dataset.e; cancelAnimationFrame(raf); draw(); });
      el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_f').textContent = FQ[st.fi] + ' MHz'; $('#v_E0').textContent = st.E0 + ' V/m'; upd(); });
      upd(); anim();
    };
    const proj = v => [v[2] * -0.55, -v[1] - v[2] * 0.35];   // screen offset of a y/z direction (z drawn as a slanted depth axis)
    const anim = () => {
      const svg = $('#jxEM'); if (!svg || !document.body.contains(svg)) return;
      const x = calc(), Ed = AX[st.E], Bd = x.B, aE = 22 + st.E0 / 1000 * 30, aB = aE * 0.75, cyc = 2.5; ph += 0.06 * st.dir;
      const line = (d, a, col) => { let s = ''; for (let i = 0; i <= 120; i++) { const X = 20 + i * 2.4, v = Math.sin(2 * Math.PI * cyc * i / 120 - ph), p = proj(d); s += (i ? 'L' : 'M') + (X + p[0] * a * v).toFixed(1) + ' ' + (90 + p[1] * a * v).toFixed(1); } return `<path d="${s}" fill="none" stroke="${col}" stroke-width="2.2"/>`; };
      const arr = (d, col, lab) => { const p = proj(d); return `<line x1="290" y1="128" x2="${290 + p[0] * 24}" y2="${128 + p[1] * 24}" stroke="${col}" stroke-width="2.5"/><text x="${292 + p[0] * 30}" y="${131 + p[1] * 30}" fill="${col}" font-size="10">${lab}</text>`; };
      svg.innerHTML = `<line x1="10" y1="90" x2="310" y2="90" stroke="#475569"/><text x="${st.dir > 0 ? 292 : 12}" y="84" fill="#facc15" font-size="16">${st.dir > 0 ? '➡' : '⬅'}</text>
        ${line(Ed, aE, '#ef4444')}${line(Bd, aB, '#60a5fa')}${arr(Ed, '#ef4444', 'E')}${arr(Bd, '#60a5fa', 'B')}<text x="12" y="172" fill="#94a3b8" font-size="10">y up · z slanting into the page</text>`;
      raf = requestAnimationFrame(anim);
    };
    const upd = () => {
      const x = calc(), L = x.lam >= 1 ? x.lam.toFixed(2) + ' m' : x.lam >= 0.01 ? (x.lam * 100).toFixed(1) + ' cm' : (x.lam * 1000).toFixed(1) + ' mm';
      $('#jxRead').innerHTML = `<span>λ <b>${L}</b></span><span>B along <b>${x.Bn}</b></span><span>B₀ <b>${(x.B0 * 1e7).toFixed(2)} × 10⁻⁷ T</b></span><span>intensity <b>${x.I.toFixed(1)} W/m²</b></span>`;
      let fresh = false; MIS.forEach(([kk, , tt]) => { if (!done['em_' + kk] && tt(x)) { done['em_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['em_' + kk] ? 'ok' : ''}">${done['em_' + kk] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    draw();
  }

  /* ---------- Try it yourself: Matrices and Determinants ---------- */
  function transformLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {});
    const st = { a: 1, b: 0.5, c: 0, d: 1 };
    const MIS = [['squash', 'Squash the square flat — make the determinant 0', x => Math.abs(x.D) < 1e-9 && (x.a || x.b || x.c || x.d)],
      ['rot', 'Rotate the square by 90° (area stays 1)', x => x.a === 0 && x.b === -1 && x.c === 1 && x.d === 0],
      ['flip', 'Flip it over: get a NEGATIVE determinant', x => x.D < 0],
      ['four', 'Make the area exactly 4 times bigger', x => Math.abs(Math.abs(x.D) - 4) < 1e-9],
      ['shear', 'Shear it: slide the top sideways but keep the area 1', x => x.a === 1 && x.d === 1 && x.c === 0 && x.b !== 0]];
    const sl = (k) => `<label class="jx-sl"><span>${k} <b id="v_${k}">${st[k]}</b></span><input type="range" min="-3" max="3" step="0.5" value="${st[k]}" data-k="${k}"></label>`;
    el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🔀 Matrix Transformer</h3>
      <p class="jx-fine">A 2 × 2 matrix moves every point of the plane. Watch the grey unit square become the purple shape — its area is |det|.</p>
      <svg viewBox="-160 -160 320 320" class="jx-circ" id="jxT" style="max-width:330px"></svg><div class="jx-read" id="jxRead"></div>
      <div class="jx-f" id="jxM" style="text-align:center"></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 12px">${sl('a')}${sl('b')}${sl('c')}${sl('d')}</div>
      <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
    $('#jxBack').onclick = () => unit(uid, 'lab');
    el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value; upd(); });
    const upd = () => {
      const { a, b, c, d } = st, D = a * d - b * c, s = 34, P = (x, y) => [(a * x + b * y) * s, -(c * x + d * y) * s];
      const grid = [];
      for (let k = -4; k <= 4; k++) { const [x1, y1] = P(k, -4), [x2, y2] = P(k, 4), [x3, y3] = P(-4, k), [x4, y4] = P(4, k); grid.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"/><line x1="${x3}" y1="${y3}" x2="${x4}" y2="${y4}"/>`); }
      const sq = [[0, 0], [1, 0], [1, 1], [0, 1]].map(([x, y]) => P(x, y).join(',')).join(' '), [ix, iy] = P(1, 0), [jx, jy] = P(0, 1);
      $('#jxT').innerHTML = `<g stroke="#e9d5ff" stroke-width="1">${grid.join('')}</g><line x1="-160" y1="0" x2="160" y2="0" stroke="#94a3b8"/><line x1="0" y1="-160" x2="0" y2="160" stroke="#94a3b8"/>
        <rect x="0" y="${-s}" width="${s}" height="${s}" fill="#94a3b8" opacity=".35"/>
        <polygon points="${sq}" fill="${D < 0 ? '#f97316' : '#7c3aed'}" opacity=".55" stroke="${D < 0 ? '#c2410c' : '#5b21b6'}" stroke-width="2"/>
        <line x1="0" y1="0" x2="${ix}" y2="${iy}" stroke="#dc2626" stroke-width="3"/><line x1="0" y1="0" x2="${jx}" y2="${jy}" stroke="#16a34a" stroke-width="3"/>
        <text x="${ix + 4}" y="${iy}" font-size="12" fill="#dc2626">î → (${a}, ${c})</text><text x="${jx + 4}" y="${jy - 4}" font-size="12" fill="#16a34a">ĵ → (${b}, ${d})</text>`;
      $('#jxM').innerHTML = mx(`A = [[${a}, ${b}], [${c}, ${d}]]`);
      $('#jxRead').innerHTML = `<span>det A <b>${+D.toFixed(3)}</b></span><span>area × <b>${+Math.abs(D).toFixed(3)}</b></span><span>${D === 0 ? '⚠️ singular — no inverse' : D < 0 ? '🔄 orientation flipped' : '✅ invertible'}</span>`;
      const x = { ...st, D };
      let fresh = false; MIS.forEach(([kk, , t]) => { if (!done['mt_' + kk] && t(x)) { done['mt_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['mt_' + kk] ? 'ok' : ''}">${done['mt_' + kk] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    upd();
  }
  function planesLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {});
    const st = { a1: 1, b1: 1, c1: 4, a2: 1, b2: -1, c2: 0 };
    const MIS = [['uni', 'Make the two lines cross at exactly one point', x => x.kind === 'unique'],
      ['none', 'Make the system have NO solution (parallel lines)', x => x.kind === 'none'],
      ['inf', 'Make it have INFINITELY many solutions (same line)', x => x.kind === 'infinite'],
      ['pt', 'Make the lines meet at the point (2, 3)', x => x.kind === 'unique' && Math.abs(x.X - 2) < 1e-9 && Math.abs(x.Y - 3) < 1e-9]];
    const sl = (k, lab) => `<label class="jx-sl"><span>${lab} <b id="v_${k}">${st[k]}</b></span><input type="range" min="-6" max="6" step="1" value="${st[k]}" data-k="${k}"></label>`;
    el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>📐 Line Meeting Room</h3>
      <p class="jx-fine">Each equation ax + by = c is a line. D, D<sub>x</sub>, D<sub>y</sub> decide whether they meet once, never, or everywhere.</p>
      <svg viewBox="-150 -150 300 300" class="jx-circ" id="jxL" style="max-width:320px"></svg><div class="jx-f" id="jxEq" style="text-align:center"></div><div class="jx-read" id="jxRead"></div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px 10px"><b style="grid-column:1/4;color:#7c3aed">Line 1</b>${sl('a1', 'a₁')}${sl('b1', 'b₁')}${sl('c1', 'c₁')}<b style="grid-column:1/4;color:#f97316">Line 2</b>${sl('a2', 'a₂')}${sl('b2', 'b₂')}${sl('c2', 'c₂')}</div>
      <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
    $('#jxBack').onclick = () => unit(uid, 'lab');
    el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value; upd(); });
    const line = (a, b, c, col) => { const s = 20, pts = [];
      if (b !== 0) { for (const x of [-8, 8]) pts.push([x * s, -(c - a * x) / b * s]); } else if (a !== 0) { const x = c / a; pts.push([x * s, -160], [x * s, 160]); } else return '';
      return `<line x1="${pts[0][0]}" y1="${pts[0][1]}" x2="${pts[1][0]}" y2="${pts[1][1]}" stroke="${col}" stroke-width="3" opacity=".85"/>`; };
    const upd = () => {
      const { a1, b1, c1, a2, b2, c2 } = st, D = a1 * b2 - a2 * b1, Dx = c1 * b2 - c2 * b1, Dy = a1 * c2 - a2 * c1;
      const kind = D !== 0 ? 'unique' : (Dx !== 0 || Dy !== 0) ? 'none' : 'infinite', X = D ? Dx / D : NaN, Y = D ? Dy / D : NaN, s = 20;
      const g = []; for (let k = -7; k <= 7; k++) g.push(`<line x1="${k * s}" y1="-150" x2="${k * s}" y2="150"/><line x1="-150" y1="${k * s}" x2="150" y2="${k * s}"/>`);
      $('#jxL').innerHTML = `<g stroke="#f1f5f9">${g.join('')}</g><line x1="-150" y1="0" x2="150" y2="0" stroke="#94a3b8"/><line x1="0" y1="-150" x2="0" y2="150" stroke="#94a3b8"/>
        ${line(a1, b1, c1, '#7c3aed')}${line(a2, b2, c2, '#f97316')}${kind === 'unique' && Math.abs(X) < 8 && Math.abs(Y) < 8 ? `<circle cx="${X * s}" cy="${-Y * s}" r="6" fill="#16a34a" stroke="#fff" stroke-width="2"/>` : ''}`;
      const f = v => +v.toFixed(3);
      const lq = (a, b, c) => { const t = (k, v, first) => k === 0 ? '' : (first ? (k < 0 ? '−' : '') : (k < 0 ? ' − ' : ' + ')) + (Math.abs(k) === 1 ? '' : Math.abs(k)) + v; const L = (t(a, 'x', true) + t(b, 'y', a === 0)) || '0'; return L + ' = ' + String(c).replace('-', '−'); };
      $('#jxEq').innerHTML = `<span style="color:#7c3aed">${lq(a1, b1, c1)}</span> &nbsp; <span style="color:#f97316">${lq(a2, b2, c2)}</span>`;
      $('#jxRead').innerHTML = `<span>D <b>${D}</b></span><span>D<sub>x</sub> <b>${Dx}</b></span><span>D<sub>y</sub> <b>${Dy}</b></span><span><b>${kind === 'unique' ? `one point (${f(X)}, ${f(Y)})` : kind === 'none' ? 'no solution — parallel' : 'infinitely many — same line'}</b></span>`;
      const x = { kind, X, Y };
      let fresh = false; MIS.forEach(([kk, , t]) => { if (!done['pl_' + kk] && t(x)) { done['pl_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['pl_' + kk] ? 'ok' : ''}">${done['pl_' + kk] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    upd();
  }

  /* ---------- Try it yourself: Sequence and Series ---------- */
  const gcdJ = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
  const fracJ = (n, d) => { const g = gcdJ(n, d), s = d < 0 ? -1 : 1; return [s * n / g, s * d / g]; };
  const fShow = ([n, d]) => d === 1 ? String(n) : mx(`\\f{${n}}{${d}}`);
  function patternLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {});
    const st = { k: 'ap', a: 2, d: 3, r: 0.5, n: 10 };
    const term = i => st.k === 'ap' ? st.a + i * st.d : st.a * Math.pow(st.r, i);
    const MIS = [['t10', 'Build an A.P. whose 10th term is exactly 50', x => x.k === 'ap' && Math.abs(x.T[9] - 50) < 1e-9 && x.n >= 10],
      ['zero', 'Make an A.P. whose sum S_n is exactly 0 (n ≥ 4)', x => x.k === 'ap' && Math.abs(x.S) < 1e-9 && x.n >= 4 && x.T.some(v => v !== 0)],
      ['odd', 'Add the first n odd numbers — and discover the sum is n² (n ≥ 5)', x => x.k === 'ap' && x.a === 1 && x.d === 2 && x.n >= 5],
      ['two', 'Make an infinite G.P. with first term 1 add up to exactly 2', x => x.k === 'gp' && x.a === 1 && Math.abs(x.r - 0.5) < 1e-9],
      ['flip', 'Make a G.P. whose terms flip sign and still converge', x => x.k === 'gp' && x.r < 0 && x.r > -1]];
    const draw = () => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>📈 Pattern Builder</h3>
        <p class="jx-fine">Every bar is a term. Watch the running total (purple line) — and for a G.P. with |r| &lt; 1, see it hug the infinite-sum line.</p>
        <div class="jx-seg3"><button data-k="ap" class="${st.k === 'ap' ? 'on' : ''}">🪜 A.P. (add d)</button><button data-k="gp" class="${st.k === 'gp' ? 'on' : ''}">🌱 G.P. (multiply r)</button></div>
        <svg viewBox="0 0 320 200" class="jx-circ" id="jxBars"></svg><div class="jx-read" id="jxRead"></div>
        <label class="jx-sl"><span>First term a <b id="v_a">${st.a}</b></span><input type="range" min="-10" max="20" step="1" value="${st.a}" data-v="a"></label>
        ${st.k === 'ap' ? `<label class="jx-sl"><span>Common difference d <b id="v_d">${st.d}</b></span><input type="range" min="-6" max="8" step="0.5" value="${st.d}" data-v="d"></label>`
          : `<label class="jx-sl"><span>Common ratio r <b id="v_r">${st.r}</b></span><input type="range" min="-2" max="2" step="0.05" value="${st.r}" data-v="r"></label>`}
        <label class="jx-sl"><span>Number of terms n <b id="v_n">${st.n}</b></span><input type="range" min="1" max="20" step="1" value="${st.n}" data-v="n"></label>
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-k]').forEach(b => b.onclick = () => { tap(); st.k = b.dataset.k; draw(); });
      el.querySelectorAll('[data-v]').forEach(i => i.oninput = () => { st[i.dataset.v] = +i.value; $('#v_' + i.dataset.v).textContent = i.value; upd(); });
      upd();
    };
    const upd = () => {
      const T = Array.from({ length: st.n }, (_, i) => term(i)), C = T.reduce((acc, v) => (acc.push((acc.length ? acc[acc.length - 1] : 0) + v), acc), []), S = C[C.length - 1];
      const inf = st.k === 'gp' && Math.abs(st.r) < 1 ? st.a / (1 - st.r) : null;
      const all = [...T, ...C, 0, ...(inf !== null ? [inf] : [])], lo = Math.min(...all), hi = Math.max(...all), sy = v => 180 - (hi === lo ? 0.5 : (v - lo) / (hi - lo)) * 165, w = 290 / st.n;
      const f = v => Math.abs(v) >= 1e4 ? v.toExponential(2) : +v.toFixed(3);
      $('#jxBars').innerHTML = `<line x1="20" y1="${sy(0)}" x2="315" y2="${sy(0)}" stroke="#94a3b8"/>
        ${T.map((v, i) => `<rect x="${(22 + i * w).toFixed(1)}" y="${Math.min(sy(v), sy(0)).toFixed(1)}" width="${(w * 0.7).toFixed(1)}" height="${Math.abs(sy(v) - sy(0)).toFixed(1)}" rx="2" fill="${v >= 0 ? '#f97316' : '#0ea5e9'}"><title>a${i + 1} = ${f(v)}</title></rect>`).join('')}
        <polyline fill="none" stroke="#7c3aed" stroke-width="2.4" points="${C.map((v, i) => (22 + i * w + w * 0.35).toFixed(1) + ',' + sy(v).toFixed(1)).join(' ')}"/>
        ${inf !== null ? `<line x1="20" y1="${sy(inf)}" x2="315" y2="${sy(inf)}" stroke="#16a34a" stroke-dasharray="5 4"/><text x="312" y="${sy(inf) - 4}" text-anchor="end" font-size="10" fill="#16a34a">S∞ = ${f(inf)}</text>` : ''}
        <text x="24" y="12" font-size="10" fill="#7c3aed">— running sum S_k</text>`;
      $('#jxRead').innerHTML = `<span>a<sub>n</sub> <b>${f(T[T.length - 1])}</b></span><span>S<sub>n</sub> <b>${f(S)}</b></span>${st.k === 'ap' ? `<span>${mx('\\f{n}{2}(a + l)')} <b>${f(st.n / 2 * (T[0] + T[T.length - 1]))}</b></span>` : `<span>S<sub>∞</sub> <b>${inf !== null ? f(inf) : 'diverges'}</b></span>`}`;
      const x = { ...st, T, S };
      let fresh = false; MIS.forEach(([kk, , t]) => { if (!done['sq_' + kk] && t(x)) { done['sq_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['sq_' + kk] ? 'ok' : ''}">${done['sq_' + kk] ? '✅' : '⬜'} ${n2.replace('S_n', 'S<sub>n</sub>')}</div>`).join('');
    };
    draw();
  }
  function teleLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {});
    const SER = { gauss: ['Gauss staircase', 'k'], t1: ['\\f{1}{k(k + 1)}', 'tele'], t2: ['\\f{1}{k(k + 2)}', 'tele'], t4: ['\\f{k}{1 + 4k^{4}}', 'tele'] };
    const st = { s: 'gauss', n: 6, cut: 0 };
    const MIS = [['g', 'Gauss: show that 1 + 2 + … + 10 is half a 10 × 11 rectangle', x => x.s === 'gauss' && x.n === 10],
      ['nine', 'Make Σ 1/k(k+1) equal exactly 9/10', x => x.s === 't1' && x.n === 9 && x.cut >= x.n],
      ['cancel', 'Cancel every middle term of Σ 1/k(k+2) for n = 8', x => x.s === 't2' && x.n === 8 && x.cut >= x.n],
      ['jee', 'Crack the JEE favourite Σ k/(1+4k⁴) for n = 10 (answer 55/221)', x => x.s === 't4' && x.n === 10 && x.cut >= x.n]];
    const draw = () => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🔭 Telescoping Machine</h3>
        <p class="jx-fine">Split each term into two pieces, then press ✂️ to cancel neighbours — only the ends survive.</p>
        <div class="jx-seg3" style="flex-wrap:wrap">${Object.entries(SER).map(([k, v]) => `<button data-s="${k}" class="${k === st.s ? 'on' : ''}">${k === 'gauss' ? '🧱 Σk (Gauss)' : 'Σ ' + mx(v[0])}</button>`).join('')}</div>
        <div id="jxTel"></div><div class="jx-read" id="jxRead"></div>
        <label class="jx-sl"><span>n <b id="v_n">${st.n}</b></span><input type="range" min="2" max="12" step="1" value="${st.n}" id="jxN"></label>
        ${st.s === 'gauss' ? '' : '<div class="jx-seg3"><button id="jxCut">✂️ Cancel next pair</button><button id="jxAll">✂️✂️ Cancel all</button></div>'}
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-s]').forEach(b => b.onclick = () => { tap(); st.s = b.dataset.s; st.cut = 0; draw(); });
      $('#jxN').oninput = e => { st.n = +e.target.value; st.cut = 0; $('#v_n').textContent = st.n; upd(); };
      if ($('#jxCut')) { $('#jxCut').onclick = () => { tap(); st.cut = Math.min(st.n, st.cut + 1); upd(); }; $('#jxAll').onclick = () => { tap('open'); st.cut = st.n; upd(); }; }
      upd();
    };
    const upd = () => {
      const n = st.n; let html = '', total;
      if (st.s === 'gauss') {
        const c = 18, W = (n + 1) * c, H = n * c;
        html = `<svg viewBox="-4 -4 ${W + 8} ${H + 8}" class="jx-circ" style="max-width:${Math.min(320, W * 1.6)}px">${Array.from({ length: n }, (_, r) => Array.from({ length: n + 1 }, (_, k) => `<rect x="${k * c}" y="${r * c}" width="${c - 2}" height="${c - 2}" rx="3" fill="${k <= r ? '#f97316' : '#7c3aed'}" opacity="${k <= r ? 1 : 0.55}"/>`).join('')).join('')}</svg>
          <p class="jx-p">Orange staircase = 1 + 2 + … + ${n}. A second (purple) copy, flipped, fills a ${n} × ${n + 1} rectangle → sum = ${mx(`\\f{${n} × ${n + 1}}{2}`)} = <b>${n * (n + 1) / 2}</b>.</p>`;
        total = [n * (n + 1) / 2, 1];
      } else {
        const piece = k => st.s === 't1' ? [[1, k], [1, k + 1], 1] : st.s === 't2' ? [[1, k], [1, k + 2], 2] : [[1, 2 * k * k - 2 * k + 1], [1, 2 * k * k + 2 * k + 1], 4];
        const sh = st.s === 't2' ? 2 : 1, off = 'text-decoration:line-through;opacity:.4';
        const rows = Array.from({ length: n }, (_, i) => { const k = i + 1, [p, q, m] = piece(k), deadP = k > sh && k - sh <= st.cut, deadQ = k <= st.cut && k + sh <= n;
          return `<div class="jx-mis" style="display:flex;gap:6px;align-items:center;font-size:14px"><span style="min-width:30px">k=${k}</span>${m > 1 ? mx(`\\f{1}{${m}}`) + '(' : ''}<span style="${deadP ? off : 'color:#16a34a;font-weight:700'}">${fShow(p)}</span> − <span style="${deadQ ? off : 'color:#dc2626;font-weight:700'}">${fShow(q)}</span>${m > 1 ? ')' : ''}</div>`; });
        html = rows.join('');
        if (st.s === 't1') total = fracJ(n, n + 1);
        else if (st.s === 't2') total = fracJ(3 * (n + 1) * (n + 2) - 2 * (n + 2) - 2 * (n + 1), 4 * (n + 1) * (n + 2));
        else total = fracJ(2 * n * n + 2 * n, 4 * (2 * n * n + 2 * n + 1));
      }
      $('#jxTel').innerHTML = html;
      $('#jxRead').innerHTML = `<span>sum of ${n} terms <b>${st.s === 'gauss' || st.cut >= n ? fShow(total) : '✂️ cancel to see'}</b></span>${st.s === 't1' ? '<span>limit as n → ∞ <b>1</b></span>' : st.s === 't2' ? `<span>limit <b>${fShow([3, 4])}</b></span>` : st.s === 't4' ? `<span>limit <b>${fShow([1, 4])}</b></span>` : ''}`;
      const x = { ...st };
      let fresh = false; MIS.forEach(([kk, , t]) => { if (!done['tl_' + kk] && t(x)) { done['tl_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['tl_' + kk] ? 'ok' : ''}">${done['tl_' + kk] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    draw();
  }

  /* ---------- Try it yourself: Some Basic Concepts ---------- */
  const ATC = { H: '#e2e8f0', C: '#334155', O: '#ef4444', N: '#3b82f6', Na: '#a855f7', Cl: '#22c55e', S: '#eab308', Al: '#94a3b8', Fe: '#b45309', Ca: '#f97316' };
  const molSvg = (f, x, y, r = 5) => { const at = []; (f.match(/[A-Z][a-z]?\d*/g) || []).forEach(t => { const m = t.match(/([A-Z][a-z]?)(\d*)/); for (let i = 0; i < (+m[2] || 1); i++) at.push(m[1]); }); at.sort((p, q) => (p === 'H') - (q === 'H'));
    const n = at.length, ring = Math.max(0, n - 1); return at.map((e, i) => { const a = i ? (i - 1) / ring * 2 * Math.PI : 0, rr = i ? r * 1.6 : 0; return `<circle cx="${(x + rr * Math.cos(a)).toFixed(1)}" cy="${(y + rr * Math.sin(a)).toFixed(1)}" r="${i ? r * 0.8 : r}" fill="${ATC[e] || '#64748b'}" stroke="#1e1b4b" stroke-width=".6"/>`; }).join(''); };
  function moleLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {}), NA = 6.022e23;
    const SUB = [['H2O', 'Water', 18, 3, false], ['CO2', 'Carbon dioxide', 44, 3, true], ['NaCl', 'Salt', 58.5, 2, false], ['C6H12O6', 'Glucose', 180, 24, false], ['CH4', 'Methane', 16, 5, true], ['NH3', 'Ammonia', 17, 4, true], ['O2', 'Oxygen', 32, 2, true], ['Fe', 'Iron', 56, 1, false]];
    const st = { s: 0, g: 9 };
    const sub = f => f.replace(/(\d+)/g, '<sub>$1</sub>');
    const sci = v => { if (v === 0) return '0'; const e = Math.floor(Math.log10(v)); return e >= -2 && e <= 3 ? (+v.toPrecision(4)).toString() : (v / 10 ** e).toFixed(3) + ' × 10' + String(e).split('').map(ch => '⁰¹²³⁴⁵⁶⁷⁸⁹'['0123456789'.indexOf(ch)] || '⁻').join(''); };
    const MIS = [['one', 'Weigh out exactly 1 mole of water', x => x.s === 0 && Math.abs(x.n - 1) < 0.005],
      ['glu', 'Find the mass of 1 mole of glucose', x => x.s === 3 && Math.abs(x.n - 1) < 0.005],
      ['three', 'Get 3 N_A ATOMS from water', x => x.s === 0 && Math.abs(x.at - 3) < 0.01],
      ['stp', 'Fill a 22.4 L balloon with CO₂ at STP', x => x.s === 1 && Math.abs(x.V - 22.4) < 0.1],
      ['same', 'Atom twins: find the mass of CO₂ with as many atoms as 18 g of water', x => x.s === 1 && Math.abs(x.at - 3) < 0.01]];
    const draw = () => {
      const S = SUB[st.s];
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🥚 Mole Machine</h3>
        <p class="jx-fine">Pour grams onto the balance — the machine counts the moles, molecules and atoms for you.</p>
        <div class="jx-seg3" style="flex-wrap:wrap">${SUB.map((x, i) => `<button data-s="${i}" class="${i === st.s ? 'on' : ''}">${sub(x[0])}<br><small>${x[1]}</small></button>`).join('')}</div>
        <svg viewBox="0 0 320 170" class="jx-circ" id="jxBal"></svg><div class="jx-read" id="jxRead"></div>
        <label class="jx-sl"><span>Mass on the balance <b id="v_g">${st.g} g</b></span><input type="range" min="0" max="${Math.max(200, S[2] * 3)}" step="0.5" value="${st.g}" data-k="g"></label>
        <div class="jx-seg3"><button data-q="1">1 mol</button><button data-q="0.5">½ mol</button><button data-q="2">2 mol</button></div>
        <h3 style="margin-top:12px">🗺️ The mole map</h3><div id="jxMap"></div>
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-s]').forEach(b => b.onclick = () => { tap(); st.s = +b.dataset.s; st.g = Math.min(st.g, Math.max(200, SUB[st.s][2] * 3)); draw(); });
      el.querySelectorAll('[data-q]').forEach(b => b.onclick = () => { tap(); st.g = +(SUB[st.s][2] * +b.dataset.q).toFixed(1); draw(); });
      el.querySelector('input[type=range]').oninput = e => { st.g = +e.target.value; $('#v_g').textContent = st.g + ' g'; upd(); };
      upd();
    };
    const upd = () => {
      const [f, nm, M, A, gas] = SUB[st.s], n = st.g / M, x = { s: st.s, n, at: n * A, V: gas ? n * 22.4 : 0 };
      const k = Math.min(36, Math.round(n * 12)), tilt = Math.max(-12, Math.min(12, (n - 1) * 6));
      $('#jxBal').innerHTML = `<g transform="rotate(${tilt.toFixed(1)} 160 120)"><rect x="40" y="116" width="240" height="6" rx="3" fill="#64748b"/>
        ${Array.from({ length: k }, (_, i) => molSvg(f, 62 + (i % 12) * 18, 104 - Math.floor(i / 12) * 19, f.length > 4 ? 2.6 : 3.4)).join('')}</g>
        <polygon points="150,170 170,170 160,124" fill="#475569"/>
        <text x="160" y="16" text-anchor="middle" font-size="12" font-weight="700">${nm}: M = ${M} g mol⁻¹</text>
        <text x="160" y="32" text-anchor="middle" font-size="10" fill="#6b6795">each picture molecule ≈ ${sci(NA / 12)} real molecules</text>`;
      $('#jxRead').innerHTML = `<span>moles <b>${sci(n)}</b></span><span>molecules <b>${sci(n * NA)}</b></span><span>atoms <b>${sci(n * A * NA)}</b> = ${sci(n * A)} N<sub>A</sub></span>${gas ? `<span>volume at STP <b>${sci(n * 22.4)} L</b></span>` : ''}`;
      $('#jxMap').innerHTML = `<svg viewBox="0 0 320 130" class="jx-curve"><g font-size="11" text-anchor="middle">
        <rect x="120" y="50" width="80" height="34" rx="10" fill="#7c3aed"/><text x="160" y="72" fill="#fff" font-weight="700">${sci(n)} mol</text>
        <rect x="6" y="6" width="90" height="34" rx="10" fill="#ede9fe"/><text x="51" y="28">${sci(st.g)} g</text>
        <rect x="224" y="6" width="90" height="34" rx="10" fill="#ede9fe"/><text x="269" y="28">${sci(n * NA)}</text>
        <rect x="6" y="92" width="90" height="34" rx="10" fill="#ede9fe"/><text x="51" y="114">${gas ? sci(n * 22.4) + ' L' : 'not a gas'}</text>
        <rect x="224" y="92" width="90" height="34" rx="10" fill="#ede9fe"/><text x="269" y="114">${sci(n * A)} N_A atoms</text>
        <line x1="96" y1="30" x2="120" y2="56" stroke="#7c3aed"/><text x="96" y="52" font-size="9" fill="#7c3aed">÷ ${M}</text>
        <line x1="224" y1="30" x2="200" y2="56" stroke="#7c3aed"/><text x="230" y="52" font-size="9" fill="#7c3aed">× N_A</text>
        <line x1="96" y1="104" x2="120" y2="80" stroke="#7c3aed"/><text x="94" y="88" font-size="9" fill="#7c3aed">× 22.4</text>
        <line x1="224" y1="104" x2="200" y2="80" stroke="#7c3aed"/><text x="232" y="88" font-size="9" fill="#7c3aed">× ${A}</text></g></svg>`;
      let fresh = false; MIS.forEach(([kk, , t]) => { if (!done['mb_' + kk] && t(x)) { done['mb_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['mb_' + kk] ? 'ok' : ''}">${done['mb_' + kk] ? '✅' : '⬜'} ${n2.replace('N_A', 'N<sub>A</sub>')}</div>`).join('');
    };
    draw();
  }
  function limitLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {});
    const RX = [{ n: 'Water', A: ['H2', 2], B: ['O2', 1], P: [['H2O', 2]] }, { n: 'Ammonia', A: ['N2', 1], B: ['H2', 3], P: [['NH3', 2]] },
      { n: 'Burning methane', A: ['CH4', 1], B: ['O2', 2], P: [['CO2', 1], ['H2O', 2]] }, { n: 'Rust-proof alumina', A: ['Al', 4], B: ['O2', 3], P: [['Al2O3', 2]] }];
    const st = { r: 0, a: 6, b: 2, fired: false }, sub = f => f.replace(/(\d+)/g, '<sub>$1</sub>'), usub = f => f.replace(/\d/g, d => '₀₁₂₃₄₅₆₇₈₉'[d]), coef = c => c === 1 ? '' : c;
    const MIS = [['perfect', 'Perfect recipe: make water with nothing left over', x => x.r === 0 && x.fired && x.la === 0 && x.lb === 0 && x.ext > 0],
      ['nh3', 'Make exactly 6 molecules of NH₃', x => x.r === 1 && x.fired && x.made[0] === 6],
      ['olim', 'Burn methane where O₂ is the limiting reagent', x => x.r === 2 && x.fired && x.lim === 'B' && x.ext > 0],
      ['al', 'Make 4 units of Al₂O₃ with zero waste', x => x.r === 3 && x.fired && x.made[0] === 4 && x.la === 0 && x.lb === 0],
      ['all', 'Get a perfect zero-waste recipe for all four reactions', () => [0, 1, 2, 3].every(i => done['lr_z' + i])]];
    const calc = () => { const R = RX[st.r], ext = Math.floor(Math.min(st.a / R.A[1], st.b / R.B[1])); return { r: st.r, fired: st.fired, ext, la: st.a - ext * R.A[1], lb: st.b - ext * R.B[1], made: R.P.map(p => ext * p[1]), lim: st.a / R.A[1] < st.b / R.B[1] ? 'A' : st.a / R.A[1] > st.b / R.B[1] ? 'B' : '=' }; };
    const draw = () => {
      const R = RX[st.r];
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>⚖️ Limiting Reagent Kitchen</h3>
        <p class="jx-fine">Put molecules in the pot and press React. Whatever runs out first is the limiting reagent.</p>
        <div class="jx-seg3" style="flex-wrap:wrap">${RX.map((x, i) => `<button data-r="${i}" class="${i === st.r ? 'on' : ''}">${x.n}</button>`).join('')}</div>
        <div class="jx-f" style="text-align:center;font-size:16px">${coef(R.A[1])}${sub(R.A[0])} + ${coef(R.B[1])}${sub(R.B[0])} → ${R.P.map(p => coef(p[1]) + sub(p[0])).join(' + ')}</div>
        <svg viewBox="0 0 320 190" class="jx-circ" id="jxPot"></svg><div class="jx-read" id="jxRead"></div>
        <label class="jx-sl"><span>${usub(R.A[0])} molecules <b id="v_a">${st.a}</b></span><input type="range" min="0" max="12" step="1" value="${st.a}" data-k="a"></label>
        <label class="jx-sl"><span>${usub(R.B[0])} molecules <b id="v_b">${st.b}</b></span><input type="range" min="0" max="12" step="1" value="${st.b}" data-k="b"></label>
        <div class="jx-seg3"><button id="jxFire">🔥 React!</button></div>
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-r]').forEach(b => b.onclick = () => { tap(); st.r = +b.dataset.r; st.fired = false; draw(); });
      el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value; st.fired = false; upd(); });
      $('#jxFire').onclick = () => { tap('open'); st.fired = true; upd(); };
      upd();
    };
    const upd = () => {
      const R = RX[st.r], x = calc(), grid = (list, x0, y0) => list.map((f, i) => molSvg(f, x0 + (i % 5) * 27, y0 + Math.floor(i / 5) * 26, f.length > 3 ? 3.4 : 4.2)).join('');
      const left = st.fired ? [...Array(x.la).fill(R.A[0]), ...Array(x.lb).fill(R.B[0])] : [...Array(st.a).fill(R.A[0]), ...Array(st.b).fill(R.B[0])];
      const right = st.fired ? R.P.flatMap((p, j) => Array(x.made[j]).fill(p[0])) : [];
      $('#jxPot').innerHTML = `<rect x="4" y="22" width="150" height="160" rx="14" fill="#eff6ff" stroke="#93c5fd"/><rect x="166" y="22" width="150" height="160" rx="14" fill="#f0fdf4" stroke="#86efac"/>
        <text x="79" y="16" text-anchor="middle" font-size="11" font-weight="700">${st.fired ? 'left over' : 'reactants'}</text><text x="241" y="16" text-anchor="middle" font-size="11" font-weight="700">products</text>
        ${grid(left.slice(0, 30), 24, 42)}${grid(right.slice(0, 30), 186, 42)}
        ${!st.fired ? '<text x="241" y="105" text-anchor="middle" font-size="12" fill="#16a34a">press 🔥 React!</text>' : ''}`;
      const limTxt = x.lim === '=' ? 'none — perfect ratio' : sub((x.lim === 'A' ? R.A : R.B)[0]);
      $('#jxRead').innerHTML = st.fired ? `<span>limiting <b>${limTxt}</b></span><span>made <b>${R.P.map((p, j) => x.made[j] + ' ' + sub(p[0])).join(', ')}</b></span><span>left <b>${x.la} ${sub(R.A[0])}, ${x.lb} ${sub(R.B[0])}</b></span>`
        : `<span>ratio needed <b>${R.A[1]} : ${R.B[1]}</b></span><span>you have <b>${st.a} : ${st.b}</b></span>`;
      if (st.fired && x.ext > 0 && x.la === 0 && x.lb === 0 && !done['lr_z' + st.r]) { done['lr_z' + st.r] = Date.now(); save(); }
      let fresh = false; MIS.forEach(([kk, , t]) => { if (!done['lr_' + kk] && t(x)) { done['lr_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['lr_' + kk] ? 'ok' : ''}">${done['lr_' + kk] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    draw();
  }

  /* ---------- Try it yourself: Chemical Kinetics ---------- */
  function reactLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {});
    const st = { n: 1, A0: 1, k: 0.1, t: 0, run: false, plot: 'c', mys: false, mn: 1, solved: done.ck_solved || 0, sp: 1 };
    const KU = ['M s⁻¹', 's⁻¹', 'M⁻¹ s⁻¹'];
    const ord = () => st.mys ? st.mn : st.n;
    const conc = t => { const n = ord(), k = st.k, a = st.A0; return n === 0 ? Math.max(0, a - k * t) : n === 1 ? a * Math.exp(-k * t) : a / (1 + k * a * t); };
    const th = () => { const n = ord(); return n === 0 ? st.A0 / (2 * st.k) : n === 1 ? Math.LN2 / st.k : 1 / (st.k * st.A0); };
    const tmax = () => { const n = ord(); return n === 0 ? 1.15 * st.A0 / st.k : n === 1 ? Math.log(10) / st.k : 9 / (st.k * st.A0); };
    const halves = () => { const n = ord(), out = []; for (let m = 1; m <= 4; m++) { const t = n === 0 ? st.A0 * (1 - Math.pow(2, -m)) / st.k : n === 1 ? m * Math.LN2 / st.k : (Math.pow(2, m) - 1) / (st.k * st.A0); if (t <= tmax()) out.push(t); } return out; };
    const Y = { c: c => c, ln: c => Math.log(Math.max(c, 1e-3 * st.A0)), inv: c => 1 / Math.max(c, 1e-3 * st.A0) };
    const YL = { c: '[A] / M', ln: 'ln [A]', inv: '1 / [A]' };
    const MIS = [['three', 'Run a first-order reaction until only 12.5 % of A is left — count the half-lives', x => !x.mys && x.n === 1 && x.frac <= 0.125],
      ['zero', 'Make a zero-order reaction run out completely', x => !x.mys && x.n === 0 && x.frac === 0],
      ['line1', 'Find the plot that is a straight line for first order', x => !x.mys && x.n === 1 && x.plot === 'ln' && x.frac < 0.5],
      ['line2', 'Find the plot that is a straight line for second order', x => !x.mys && x.n === 2 && x.plot === 'inv' && x.frac < 0.5],
      ['myst', 'Detective: crack 3 mystery reactions (order hidden)', x => x.solved >= 3]];
    const pts = Array.from({ length: 70 }, (_, i) => [20 + ((i * 47) % 100) / 100 * 120, 40 + ((i * 71) % 100) / 100 * 90, (i * 0.618) % 1]);
    let raf = 0, last = 0;
    const draw = () => {
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>⚗️ Reaction Race</h3>
        <p class="jx-fine">Blue A molecules turn into orange B. Choose the order, press ▶ and watch the graph draw itself.</p>
        <div class="jx-seg3">${st.mys ? '<button class="on">🕵️ Mystery order</button>' : [0, 1, 2].map(n => `<button data-n="${n}" class="${n === st.n ? 'on' : ''}">${['Zero', 'First', 'Second'][n]} order</button>`).join('')}</div>
        <div style="display:flex;gap:8px;align-items:stretch;flex-wrap:wrap"><svg viewBox="0 0 160 150" id="jxBk" style="flex:1 1 140px;max-width:200px"></svg><div style="flex:2 1 220px"><svg viewBox="0 0 300 170" class="jx-curve" id="jxG"></svg></div></div>
        <div class="jx-seg3">${['c', 'ln', 'inv'].map(p => `<button data-p="${p}" class="${p === st.plot ? 'on' : ''}">${YL[p]} vs t</button>`).join('')}</div>
        <div class="jx-read" id="jxRead"></div>
        <label class="jx-sl"><span>[A]₀ <b id="v_A0">${st.A0} M</b></span><input type="range" min="0.2" max="2" step="0.1" value="${st.A0}" data-k="A0"></label>
        <label class="jx-sl"><span>Rate constant k <b id="v_k">${st.k} ${st.mys ? '' : KU[st.n]}</b></span><input type="range" min="0.02" max="0.5" step="0.01" value="${st.k}" data-k="k"></label>
        <div class="jx-seg3"><button id="jxGo">${st.run ? '⏸ Pause' : st.t > 0 && st.t >= tmax() ? '↺ Replay' : '▶ Start'}</button><button id="jxRs">⏮ Reset</button><button id="jxMy">${st.mys ? '🔓 Leave mystery' : '🕵️ Mystery reaction'}</button></div>
        <div id="jxGuess"></div>
        <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
      $('#jxBack').onclick = () => { cancelAnimationFrame(raf); unit(uid, 'lab'); };
      el.querySelectorAll('[data-n]').forEach(b => b.onclick = () => { tap(); st.n = +b.dataset.n; reset(); draw(); });
      el.querySelectorAll('[data-p]').forEach(b => b.onclick = () => { tap(); st.plot = b.dataset.p; el.querySelectorAll('[data-p]').forEach(x => x.classList.toggle('on', x === b)); upd(); });
      el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value + (i.dataset.k === 'A0' ? ' M' : st.mys ? '' : ' ' + KU[st.n]); reset(); upd(); });
      $('#jxGo').onclick = () => { tap(); if (st.t >= tmax()) st.t = 0; st.run = !st.run; $('#jxGo').textContent = st.run ? '⏸ Pause' : '▶ Start'; if (st.run) { last = 0; raf = requestAnimationFrame(loop); } };
      $('#jxRs').onclick = () => { tap(); reset(); $('#jxGo').textContent = '▶ Start'; upd(); };
      $('#jxMy').onclick = () => { tap('open'); st.mys = !st.mys; if (st.mys) { st.mn = Math.floor(Math.random() * 3); st.k = +(0.05 + Math.random() * 0.3).toFixed(2); } reset(); draw(); };
      upd();
    };
    const reset = () => { st.t = 0; st.run = false; cancelAnimationFrame(raf); };
    const loop = ts => {
      if (!document.body.contains(el) || !$('#jxG')) return;
      if (last) st.t = Math.min(tmax(), st.t + (ts - last) / 1000 * tmax() / 9);
      last = ts; upd();
      if (st.t >= tmax()) { st.run = false; const g = $('#jxGo'); if (g) g.textContent = '↺ Replay'; return; }
      if (st.run) raf = requestAnimationFrame(loop);
    };
    const upd = () => {
      const c = conc(st.t), frac = c / st.A0, n = ord(), T = tmax(), nA = Math.round(70 * frac);
      $('#jxBk').innerHTML = `<path d="M12 20 L12 140 Q12 146 18 146 L142 146 Q148 146 148 140 L148 20" fill="#eff6ff" stroke="#64748b" stroke-width="2"/>
        <rect x="14" y="${146 - 120 * 0.85}" width="132" height="${120 * 0.85 - 2}" fill="#dbeafe" opacity=".6"/>
        ${pts.map(([x, y, r], i) => `<circle cx="${(x + Math.sin(st.t * 3 + i) * 3).toFixed(1)}" cy="${(y + Math.cos(st.t * 2.3 + i) * 3).toFixed(1)}" r="4.2" fill="${i < nA ? '#2563eb' : '#f97316'}"/>`).join('')}
        <text x="80" y="14" text-anchor="middle" font-size="11" font-weight="700">A ${Math.round(frac * 100)}% · B ${100 - Math.round(frac * 100)}%</text>`;
      const N = 120, xs = Array.from({ length: N + 1 }, (_, i) => i / N * T), all = xs.map(t => Y[st.plot](conc(t)));
      const lo = Math.min(...all), hi = Math.max(...all), sy = v => 150 - (hi === lo ? 0.5 : (v - lo) / (hi - lo)) * 135, sx = t => 30 + t / T * 265;
      const seen = xs.filter(t => t <= st.t + 1e-9), line = seen.map(t => sx(t).toFixed(1) + ',' + sy(Y[st.plot](conc(t))).toFixed(1)).join(' ');
      let r2 = 0;
      if (seen.length > 8) { const ys = seen.map(t => Y[st.plot](conc(t))), mxv = seen.reduce((a, b) => a + b, 0) / seen.length, my = ys.reduce((a, b) => a + b, 0) / ys.length;
        let sxy = 0, sxx = 0, syy = 0; seen.forEach((t, i) => { sxy += (t - mxv) * (ys[i] - my); sxx += (t - mxv) ** 2; syy += (ys[i] - my) ** 2; }); r2 = syy < 1e-12 ? 1 : sxy * sxy / (sxx * syy); }
      const zeroEnd = n === 0 && st.plot !== 'c' && frac < 0.02;
      const straight = seen.length > 20 && r2 > 0.9995 && !zeroEnd;
      $('#jxG').innerHTML = `<line x1="30" y1="150" x2="297" y2="150" stroke="#c4b5fd"/><line x1="30" y1="10" x2="30" y2="150" stroke="#c4b5fd"/>
        ${st.plot === 'c' ? halves().map((h, i) => `<line x1="${sx(h)}" y1="12" x2="${sx(h)}" y2="150" stroke="#db2777" stroke-dasharray="3 3" opacity="${h <= st.t ? 0.9 : 0.25}"/><text x="${sx(h) + 2}" y="20" font-size="9" fill="#db2777" opacity="${h <= st.t ? 1 : 0.3}">t½ #${i + 1}</text>`).join('') : ''}
        <polyline fill="none" stroke="${straight ? '#16a34a' : '#7c3aed'}" stroke-width="2.6" points="${line}"/>
        ${seen.length ? `<circle cx="${sx(st.t)}" cy="${sy(Y[st.plot](c))}" r="4.5" fill="#db2777"/>` : ''}
        <text x="34" y="165" font-size="10" fill="#6b6795">time →  (y: ${YL[st.plot]})</text>
        ${straight ? '<text x="290" y="40" text-anchor="end" font-size="12" font-weight="700" fill="#16a34a">📏 Straight line!</text>' : seen.length > 20 ? '<text x="290" y="40" text-anchor="end" font-size="11" fill="#9333ea">curved</text>' : ''}`;
      const hs = halves(), gaps = hs.map((h, i) => (h - (i ? hs[i - 1] : 0)).toFixed(1));
      $('#jxRead').innerHTML = `<span>t <b>${st.t.toFixed(1)} s</b></span><span>[A] <b>${c.toFixed(3)} M</b></span><span>rate <b>${(st.k * Math.pow(c, n)).toFixed(4)} M s⁻¹</b></span>
        ${st.mys ? '<span>half-life gaps <b>' + (st.t >= (hs[1] || 1e9) ? gaps.slice(0, 3).join(' → ') + ' s' : 'run to see') + '</b></span>' : `<span>t½ <b>${th().toFixed(1)} s</b></span><span>half-life gaps <b>${gaps.slice(0, 3).join(' → ')} s</b></span>`}`;
      $('#jxGuess').innerHTML = st.mys ? `<p class="jx-p">🕵️ Which plot is straight? Then name the order:</p><div class="jx-seg3">${[0, 1, 2].map(g => `<button data-g="${g}">Order ${g}</button>`).join('')}</div><small class="jx-fine">Solved so far: ${st.solved}</small>` : '';
      el.querySelectorAll('[data-g]').forEach(b => b.onclick = () => {
        if (+b.dataset.g === st.mn) { st.solved++; done.ck_solved = st.solved; save(); tap('correct'); toast(`✅ Yes — order ${st.mn}! ${['[A] vs t', 'ln[A] vs t', '1/[A] vs t'][st.mn]} is straight.`); st.mn = Math.floor(Math.random() * 3); st.k = +(0.05 + Math.random() * 0.3).toFixed(2); reset(); draw(); }
        else { tap('wrong'); toast('Not quite — try the three plots and look for the green straight line.'); }
      });
      const x = { ...st, frac, n: st.n };
      let fresh = false; MIS.forEach(([k, , t]) => { if (!done['ck_' + k] && t(x)) { done['ck_' + k] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([k, n2]) => `<div class="jx-mis ${done['ck_' + k] ? 'ok' : ''}">${done['ck_' + k] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    draw();
  }
  function arrhLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {}), Rg = 8.314, A = 1e13;
    const st = { T: 300, Ea: 80, cat: false, d: 20 };
    const kOf = (Ea, T) => A * Math.exp(-Ea * 1000 / (Rg * T));
    const human = s => s < 1e-3 ? (s * 1e6).toPrecision(2) + ' μs' : s < 1 ? (s * 1e3).toPrecision(2) + ' ms' : s < 120 ? s.toPrecision(2) + ' s' : s < 7200 ? (s / 60).toPrecision(2) + ' min' : s < 172800 ? (s / 3600).toPrecision(2) + ' h' : s < 3.15e7 * 2 ? (s / 86400).toPrecision(3) + ' days' : s < 3.15e7 * 1e9 ? (s / 3.15e7).toPrecision(2) + ' years' : 'longer than the age of Earth';
    const sci = v => { const e = Math.floor(Math.log10(v)); return e >= -2 && e <= 2 ? v.toPrecision(3) : (v / 10 ** e).toFixed(2) + ' × 10' + String(e).split('').map(ch => '⁰¹²³⁴⁵⁶⁷⁸⁹'['0123456789'.indexOf(ch)] || '⁻').join(''); };
    const MIS = [['dbl', 'Find the Eₐ for which a 10 °C rise (298 → 308 K) exactly doubles k (ratio 2.00 ± 0.05)', x => x.T === 298 && Math.abs(x.r10 - 2) <= 0.05],
      ['fast', 'Without a catalyst, at 300 K, make the half-life shorter than 1 second', x => !x.cat && x.T === 300 && x.th < 1],
      ['year', 'At 300 K, find an Eₐ that makes the half-life about one year (½ to 2 years)', x => x.T === 300 && x.th > 1.58e7 && x.th < 6.3e7],
      ['cat', 'Switch on the catalyst and make the reaction at least 1000 times faster', x => x.cat && x.boost >= 1000],
      ['hot', 'Keep Eₐ, heat it up: 100 times faster than at 300 K', x => x.T > 300 && x.vs300 >= 100]];
    const sl = (k, lab, mn, mxv, stp, u) => `<label class="jx-sl"><span>${lab} <b id="v_${k}">${st[k]}${u}</b></span><input type="range" min="${mn}" max="${mxv}" step="${stp}" value="${st[k]}" data-k="${k}"></label>`;
    el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🔥 Arrhenius Hill</h3>
      <p class="jx-fine">Molecules must climb the energy hill Eₐ to react. Heat them up or lower the hill — and see how violently k changes.</p>
      <svg viewBox="0 0 320 170" class="jx-circ" id="jxHill"></svg><div class="jx-read" id="jxRead"></div>
      ${sl('T', 'Temperature T', 200, 800, 1, ' K')}${sl('Ea', 'Activation energy Eₐ', 10, 200, 0.5, ' kJ/mol')}
      <div class="jx-seg3"><button id="jxCat">${st.cat ? '🧪 Catalyst ON' : '🧪 Add catalyst'}</button></div><div id="jxCs"></div>
      <h3 style="margin-top:12px">🎲 Collisions that make it over the hill</h3><div id="jxFrac"></div>
      <h3 style="margin-top:12px">📈 ln k vs 1/T (the Arrhenius plot)</h3><svg viewBox="0 0 310 130" class="jx-curve" id="jxArr"></svg>
      <h3 style="margin-top:12px">🎯 Missions</h3><div id="jxMis"></div></div></div>`;
    $('#jxBack').onclick = () => unit(uid, 'lab');
    const bind = () => el.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { st[i.dataset.k] = +i.value; $('#v_' + i.dataset.k).textContent = i.value + ({ T: ' K', Ea: ' kJ/mol', d: ' kJ/mol' })[i.dataset.k]; upd(); });
    $('#jxCat').onclick = () => { tap(); st.cat = !st.cat; $('#jxCat').textContent = st.cat ? '🧪 Catalyst ON' : '🧪 Add catalyst'; $('#jxCs').innerHTML = st.cat ? sl('d', 'Catalyst lowers Eₐ by', 1, 60, 1, ' kJ/mol') : ''; bind(); upd(); };
    const upd = () => {
      const Ee = Math.max(1, st.Ea - (st.cat ? st.d : 0)), k = kOf(Ee, st.T), th = Math.LN2 / k, f = Math.exp(-Ee * 1000 / (Rg * st.T));
      const x = { ...st, k, th, r10: kOf(Ee, st.T + 10) / k, boost: st.cat ? k / kOf(st.Ea, st.T) : 1, vs300: k / kOf(Ee, 300) };
      const base = 120, sc = 0.45, top = base - st.Ea * sc, ctop = base - Ee * sc, prod = base + 20;
      const hill = (h, dash, col) => `<path d="M10 ${base} L80 ${base} C120 ${base} 130 ${h} 160 ${h} C190 ${h} 200 ${prod} 240 ${prod} L310 ${prod}" fill="none" stroke="${col}" stroke-width="3" ${dash ? 'stroke-dasharray="6 4"' : ''}/>`;
      const jig = Math.min(30, 4 + (st.T - 200) / 25);
      $('#jxHill').innerHTML = `${hill(top, false, '#7c3aed')}${st.cat ? hill(ctop, true, '#16a34a') : ''}
        <line x1="150" y1="${base}" x2="150" y2="${st.cat ? ctop : top}" stroke="#db2777" stroke-dasharray="2 3"/><text x="150" y="${base + 14}" text-anchor="middle" font-size="11" font-weight="700" fill="#db2777">Eₐ = ${Ee.toFixed(1)} kJ</text>
        ${Array.from({ length: 6 }, (_, i) => `<circle cx="${30 + i * 9}" cy="${base - 6}" r="5" fill="#2563eb"><animate attributeName="cy" values="${base - 6};${base - 6 - jig * (0.5 + (i % 3) / 3)};${base - 6}" dur="${(0.5 + 300 / st.T * (0.4 + i * 0.05)).toFixed(2)}s" repeatCount="indefinite"/></circle>`).join('')}
        ${f > 1e-4 ? `<circle r="5" fill="#f97316"><animateMotion dur="${Math.max(0.8, Math.min(6, -Math.log10(f) / 1.5)).toFixed(1)}s" repeatCount="indefinite" path="M60 ${base - 6} C120 ${base - 6} 130 ${(st.cat ? ctop : top) - 6} 160 ${(st.cat ? ctop : top) - 6} C190 ${(st.cat ? ctop : top) - 6} 200 ${prod - 6} 260 ${prod - 6}"/></circle>` : ''}
        <text x="40" y="${base + 18}" font-size="10" fill="#475569">reactants</text><text x="270" y="${prod + 16}" font-size="10" fill="#475569" text-anchor="middle">products</text>
        <text x="160" y="${Math.max(12, (st.cat ? Math.min(top, ctop) : top) - 8)}" text-anchor="middle" font-size="10" fill="#7c3aed">transition state</text>`;
      $('#jxRead').innerHTML = `<span>k <b>${sci(k)} s⁻¹</b></span><span>t½ <b>${human(th)}</b></span><span>k(T+10)/k(T) <b>${x.r10.toFixed(2)}</b></span>${st.cat ? `<span>catalyst boost <b>× ${sci(x.boost)}</b></span>` : ''}`;
      const lg = Math.log10(f), pos = Math.max(0, Math.min(100, (lg + 40) / 40 * 100));
      $('#jxFrac').innerHTML = `<div style="position:relative;height:30px;border-radius:8px;background:linear-gradient(90deg,#1e1b4b,#7c3aed,#f97316,#fde047)"><span style="position:absolute;left:${pos}%;top:-2px;transform:translateX(-50%);font-size:22px">▼</span></div>
        <small class="jx-fine">${mx('e^{−E_{a}/RT}')} = ${sci(f)} — about <b>1 collision in ${f > 0.5 ? '1' : sci(1 / f)}</b> has enough energy. (scale: 10⁻⁴⁰ → 1)</small>`;
      const Ts = [250, 300, 350, 400, 500, 600, 800], lk = T => Math.log(kOf(Ee, T)), xs = T => 30 + (1 / T - 1 / 800) / (1 / 250 - 1 / 800) * 270, lks = Ts.map(lk), lo = Math.min(...lks), hi = Math.max(...lks), ys = v => 115 - (v - lo) / (hi - lo || 1) * 100;
      $('#jxArr').innerHTML = `<line x1="30" y1="115" x2="302" y2="115" stroke="#c4b5fd"/><line x1="30" y1="10" x2="30" y2="115" stroke="#c4b5fd"/>
        <line x1="${xs(800)}" y1="${ys(lk(800))}" x2="${xs(250)}" y2="${ys(lk(250))}" stroke="#7c3aed" stroke-width="2.5"/>
        ${st.T >= 250 ? `<circle cx="${xs(st.T)}" cy="${ys(lk(st.T))}" r="5" fill="#db2777"/>` : ''}
        <text x="300" y="24" text-anchor="end" font-size="11" fill="#7c3aed">slope = −Eₐ/R = ${Math.round(-Ee * 1000 / Rg)} K</text><text x="34" y="127" font-size="10" fill="#6b6795">1/T → (hot on the left, cold on the right)</text>`;
      let fresh = false; MIS.forEach(([kk, , t]) => { if (!done['ar_' + kk] && t(x)) { done['ar_' + kk] = Date.now(); fresh = true; } }); if (fresh) { save(); tap('correct'); toast('🎯 Mission complete!'); }
      $('#jxMis').innerHTML = MIS.map(([kk, n2]) => `<div class="jx-mis ${done['ar_' + kk] ? 'ok' : ''}">${done['ar_' + kk] ? '✅' : '⬜'} ${n2}</div>`).join('');
    };
    bind(); upd();
  }

  /* ---------- Try it yourself: Atomic Structure ---------- */
  function bohrLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {}); const SER = { 1: 'Lyman', 2: 'Balmer', 3: 'Paschen', 4: 'Brackett', 5: 'Pfund' };
    const st = { Z: 1, n: 1, log: [] };
    const MIS = [['ha', 'Emit the red Hα line of hydrogen (656 nm)', x => x.Z === 1 && x.last && x.last.from === 3 && x.last.to === 2],
      ['ly', 'Emit any Lyman (ultraviolet) line from hydrogen', x => x.Z === 1 && x.last && x.last.to === 1 && x.last.from > 1],
      ['he', 'In He⁺, emit the line that matches hydrogen\'s Lyman-α (121.6 nm)', x => x.Z === 2 && x.last && x.last.from === 4 && x.last.to === 2],
      ['ion', 'Ionise hydrogen from the ground state (jump to ∞)', x => x.Z === 1 && x.ion],
      ['six', 'Collect all 6 different lines possible from n = 4 down to n = 1 in hydrogen', x => x.Z === 1 && new Set(x.log.filter(l => l.Z === 1 && l.from <= 4).map(l => l.from + '-' + l.to)).size >= 6]];
    const lamOf = (Z, a, b) => 1e7 / (109677 * Z * Z * (1 / (b * b) - 1 / (a * a)));
    const draw = () => {
      const R = n => 16 + n * 23;
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🪐 Bohr Atom Jumper</h3>
        <div class="jx-seg3">${[[1, 'H'], [2, 'He⁺'], [3, 'Li²⁺']].map(([z, n]) => `<button data-z="${z}" class="${st.Z === z ? 'on' : ''}">${n} (Z = ${z})</button>`).join('')}</div>
        <p class="jx-p">Electron is in <b>n = ${st.n}</b> (E = ${(-13.6 * st.Z * st.Z / st.n / st.n).toFixed(2)} eV). Tap an orbit to jump there — up absorbs, down emits.</p>
        <svg viewBox="0 0 320 320" class="jx-circ" id="jxAtom" style="touch-action:manipulation">${[6, 5, 4, 3, 2, 1].map(n => `<circle cx="160" cy="160" r="${R(n)}" fill="none" stroke="${n === st.n ? '#7c3aed' : '#c4b5fd'}" stroke-width="${n === st.n ? 3 : 1.5}"/><text x="${160 + R(n) * Math.cos(-0.35 - n * 0.32)}" y="${160 + R(n) * Math.sin(-0.35 - n * 0.32) - 3}" font-size="11" font-weight="700" fill="#6b6795" text-anchor="middle">n=${n}</text>`).join('')}
          <circle cx="160" cy="160" r="${6 + st.Z * 2}" fill="#dc2626"/><text x="160" y="164" text-anchor="middle" font-size="10" fill="#fff">+${st.Z}</text>
          <circle r="7" fill="#2563eb"><animateMotion dur="${(1 + st.n * 0.6).toFixed(1)}s" repeatCount="indefinite" path="M${160 + R(st.n)} 160 a${R(st.n)} ${R(st.n)} 0 1 1 -${2 * R(st.n)} 0 a${R(st.n)} ${R(st.n)} 0 1 1 ${2 * R(st.n)} 0"/></circle>
          ${st.last ? `<path d="M160 ${160 - R(st.last.from)} q 30 -10 60 0 t 60 0 t 60 0" stroke="${lamColor(st.last.lam)}" stroke-width="3" fill="none"/>` : ''}</svg>
        <p class="jx-fine" style="text-align:center">Orbits drawn evenly so they are easy to tap — real radii grow as n².</p>
        <div class="jx-seg3" style="flex-wrap:wrap">${[1, 2, 3, 4, 5, 6].map(n => `<button data-n="${n}" class="${n === st.n ? 'on' : ''}">n = ${n}</button>`).join('')}</div>
        <div class="jx-nav"><button class="jx-btn ghost" id="jxIon">Ionise (n → ∞)</button></div>
        <div class="jx-read">${st.last ? `<span>Photon <b>${st.last.E.toFixed(2)} eV</b></span><span>λ <b>${st.last.lam.toFixed(1)} nm</b></span><span>Series <b>${SER[st.last.to] || '—'}</b></span><span>${st.last.lam < 380 ? 'UV' : st.last.lam <= 750 ? 'visible' : 'IR'}</span>` : '<span>Jump down to see a photon</span>'}</div>
        <h3 style="margin-top:10px">🧾 Lines you made</h3><div class="jx-p">${st.log.slice(-8).map(l => `<span class="jx-tag" style="background:${lamColor(l.lam)};color:#fff">${['', 'H', 'He⁺', 'Li²⁺'][l.Z]} ${l.from}→${l.to} · ${l.lam.toFixed(0)} nm</span>`).join(' ') || '—'}</div>
        <h3 style="margin-top:10px">🎯 Missions</h3><div>${MIS.map(([k, n2]) => `<div class="jx-mis ${done['bo_' + k] ? 'ok' : ''}">${done['bo_' + k] ? '✅' : '⬜'} ${n2}</div>`).join('')}</div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-z]').forEach(b => b.onclick = () => { tap(); st.Z = +b.dataset.z; st.n = 1; st.last = null; st.ion = false; draw(); });
      const jump = to => {
        if (to === st.n) return; st.ion = false;
        if (to < st.n) { const lam = lamOf(st.Z, st.n, to); st.last = { from: st.n, to, lam, E: 1239.84 / lam, Z: st.Z }; st.log.push(st.last); tap('correct'); } else { st.last = null; tap(); }
        st.n = to; mark(); draw();
      };
      el.querySelectorAll('[data-n]').forEach(c2 => c2.onclick = () => jump(+c2.dataset.n));
      $('#jxAtom').onclick = ev => { const sv = $('#jxAtom'), bx = sv.getBoundingClientRect(), x = (ev.clientX - bx.left) / bx.width * 320 - 160, y = (ev.clientY - bx.top) / bx.height * 320 - 160, r = Math.hypot(x, y);
        const n = [1, 2, 3, 4, 5, 6].reduce((b, k) => Math.abs(R(k) - r) < Math.abs(R(b) - r) ? k : b, 1); if (Math.abs(R(n) - r) <= 14) jump(n); };
      $('#jxIon').onclick = () => { st.ion = st.n === 1; toast(`Ionisation energy from n = ${st.n}: ${(13.6 * st.Z * st.Z / st.n / st.n).toFixed(2)} eV`); mark(); st.n = 1; st.last = null; draw(); };
    };
    const mark = () => { let f = false; MIS.forEach(([k, , t]) => { if (!done['bo_' + k] && t(st)) { done['bo_' + k] = Date.now(); f = true; } }); if (f) { save(); toast('🎯 Mission complete!'); } };
    draw();
  }
  function orbitalLab(uid) {
    const el = screen(), done = U(uid).lab || (U(uid).lab = {}); const L = 'spdf';
    const ORD = ['1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d'];
    const st = { n: 2, l: 1, m: 0, fill: {}, count: 0 };
    const NM = { 6: 'C', 7: 'N', 8: 'O', 24: 'Cr', 26: 'Fe', 29: 'Cu', 10: 'Ne', 18: 'Ar' };
    const shape = (l, m) => {
      if (l === 0) return '<circle cx="80" cy="80" r="45" fill="#a78bfa" opacity=".7"/>';
      if (l === 1) { const rot = m === 0 ? 0 : m === 1 ? 90 : 45; return `<g transform="rotate(${rot} 80 80)"><ellipse cx="80" cy="45" rx="18" ry="32" fill="#7c3aed" opacity=".75"/><ellipse cx="80" cy="115" rx="18" ry="32" fill="#db2777" opacity=".75"/></g>`; }
      if (l === 2 && m === 0) return '<ellipse cx="80" cy="40" rx="15" ry="30" fill="#7c3aed" opacity=".75"/><ellipse cx="80" cy="120" rx="15" ry="30" fill="#7c3aed" opacity=".75"/><ellipse cx="80" cy="80" rx="40" ry="11" fill="#db2777" opacity=".7"/>';
      const rot = [0, 45, 0, 45, 0][m + 2]; return `<g transform="rotate(${rot} 80 80)">${[0, 90, 180, 270].map((a, k) => `<ellipse cx="80" cy="42" rx="13" ry="28" fill="${k % 2 ? '#db2777' : '#7c3aed'}" opacity=".75" transform="rotate(${a + 45} 80 80)"/>`).join('')}</g>`;
    };
    const cfg = () => ORD.filter(o => (st.fill[o] || []).some(Boolean)).map(o => `${o}<sup>${(st.fill[o] || []).flat().filter(Boolean).length}</sup>`).join(' ');
    const add = () => {   // next electron by Aufbau + Hund
      for (const o of ORD) { const nb = 2 * L.indexOf(o[1]) + 1, box = st.fill[o] || (st.fill[o] = Array.from({ length: nb }, () => [0, 0]));
        const up = box.findIndex(b => !b[0]); if (up >= 0) { box[up][0] = 1; st.count++; return; }
        const dn = box.findIndex(b => !b[1]); if (dn >= 0) { box[dn][1] = 1; st.count++; return; } }
    };
    const MIS = [['n', 'Build nitrogen (Z = 7): three unpaired 2p electrons (Hund)', () => st.count === 7], ['ne', 'Fill up to neon (Z = 10)', () => st.count === 10],
      ['cr', 'Make the chromium exception: move one 4s electron into 3d (tap 4s then 3d)', () => st.count === 24 && st.cr], ['view', 'Look at an orbital with 2 radial nodes', () => st.n - st.l - 1 === 2]];
    const draw = () => {
      const okq = st.l < st.n && Math.abs(st.m) <= st.l;
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🔭 Orbital viewer</h3>
        <div class="jx-qn">n <select id="qn">${[1, 2, 3, 4, 5].map(v => `<option ${v === st.n ? 'selected' : ''}>${v}</option>`).join('')}</select> l <select id="ql">${[0, 1, 2, 3].map(v => `<option ${v === st.l ? 'selected' : ''}>${v}</option>`).join('')}</select> m<sub>l</sub> <select id="qm">${[-3, -2, -1, 0, 1, 2, 3].map(v => `<option ${v === st.m ? 'selected' : ''}>${v}</option>`).join('')}</select></div>
        ${okq ? `<div style="display:flex;gap:12px;align-items:center"><svg viewBox="0 0 160 160" style="width:140px;flex:none">${st.l <= 2 ? shape(st.l, st.m) : '<text x="80" y="85" text-anchor="middle" font-size="13">f — complex shape</text>'}<line x1="10" y1="80" x2="150" y2="80" stroke="#cbd5e1"/><line x1="80" y1="10" x2="80" y2="150" stroke="#cbd5e1"/></svg>
          <div class="jx-p"><b>${st.n}${L[st.l]}</b> orbital<br>Radial nodes: <b>${st.n - st.l - 1}</b><br>Angular nodes: <b>${st.l}</b><br>Orbital angular momentum: ${mx(st.l ? `√{${st.l * (st.l + 1)}}\\f{h}{2π}` : '0')}<br>Orbitals in this subshell: <b>${2 * st.l + 1}</b></div></div>`
          : `<p class="jx-res no">❌ Not allowed: ${st.l >= st.n ? 'l must be less than n' : '|m<sub>l</sub>| must not exceed l'}.</p>`}</div>
        <div class="jx-card"><h3>🧱 Box filler — Z = ${st.count} ${NM[st.count] ? '(' + NM[st.count] + ')' : ''}</h3>
        <div class="jx-boxes">${ORD.slice(0, 7).map(o => { const nb = 2 * L.indexOf(o[1]) + 1, box = st.fill[o] || Array.from({ length: nb }, () => [0, 0]); return `<div class="jx-sub2" data-o="${o}"><small>${o}</small><div>${box.map(b => `<span>${b[0] ? '↑' : ''}${b[1] ? '↓' : ''}</span>`).join('')}</div></div>`; }).join('')}</div>
        <p class="jx-p">${cfg() || 'Empty — add electrons'}</p>
        <div class="jx-nav"><button class="jx-btn" id="jxAdd">+1 electron</button><button class="jx-btn ghost" id="jxAdd5">+5</button><button class="jx-btn ghost" id="jxClr">Reset</button></div>
        <h3 style="margin-top:10px">🎯 Missions</h3>${MIS.map(([k, n2]) => `<div class="jx-mis ${done['or_' + k] ? 'ok' : ''}">${done['or_' + k] ? '✅' : '⬜'} ${n2}</div>`).join('')}</div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      ['qn', 'ql', 'qm'].forEach(id => $('#' + id).onchange = () => { st.n = +$('#qn').value; st.l = +$('#ql').value; st.m = +$('#qm').value; mark(); draw(); });
      $('#jxAdd').onclick = () => { tap(); if (st.count < 30) add(); st.cr = false; mark(); draw(); };
      $('#jxAdd5').onclick = () => { tap(); for (let k = 0; k < 5 && st.count < 30; k++) add(); st.cr = false; mark(); draw(); };
      $('#jxClr').onclick = () => { st.fill = {}; st.count = 0; st.cr = false; draw(); };
      el.querySelectorAll('[data-o]').forEach(d => d.onclick = () => {
        if (d.dataset.o === '4s' && st.count === 24 && st.fill['4s'] && st.fill['4s'][0][1]) { st.pick = true; toast('Now tap 3d'); return; }
        if (d.dataset.o === '3d' && st.pick) { const box = st.fill['3d'], k = box.findIndex(b => !b[0]); if (k >= 0) { box[k][0] = 1; st.fill['4s'][0][1] = 0; st.cr = true; st.pick = false; tap('correct'); mark(); draw(); } }
      });
    };
    const mark = () => { let f = false; MIS.forEach(([k, , t]) => { if (!done['or_' + k] && t()) { done['or_' + k] = Date.now(); f = true; } }); if (f) { save(); toast('🎯 Mission complete!'); } };
    draw();
  }

  /* ================= INFO SCREENS ================= */
  function pattern() {
    const el = screen(); here('pattern');
    el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← JEE home</button><div class="jx-card"><h3>📋 JEE Main 2027 — Paper 1 (B.E./B.Tech.)</h3>
      <table class="jx-t"><tr><th>Subject</th><th>Section A (MCQ)</th><th>Section B (numerical)</th><th>Marks</th></tr><tr><td>Physics</td><td>20</td><td>5</td><td>100</td></tr><tr><td>Chemistry</td><td>20</td><td>5</td><td>100</td></tr><tr><td>Mathematics</td><td>20</td><td>5</td><td>100</td></tr><tr><th>Total</th><th>60</th><th>15</th><th>300</th></tr></table>
      <ul class="jx-traps"><li>Computer-based test, 3 hours; all 75 questions compulsory</li><li>+4 for correct, −1 for wrong in BOTH sections; 0 if unanswered</li><li>Numerical answers: rounded off to the nearest integer</li><li>Session 1: 20–28 January 2027 · Session 2: 2–7 April 2027 — your better score counts</li><li>Ties broken by Mathematics, then Physics, then Chemistry scores</li><li>JEE Advanced: top 2,50,000 of JEE Main Paper 1</li></ul>
      <p class="jx-fine">Source: NTA JEE (Main) 2027 Information Bulletin.</p></div></div>`;
    $('#jxBack').onclick = home;
  }
  function advanced() {
    const el = screen(); here('adv');
    el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← JEE home</button><div class="jx-hero sm adv"><h1>🏔️ JEE Advanced</h1><p>Coming soon. We are building it the same way: real past papers, our own step-by-step solutions, and extra questions verified by code.</p></div>
      ${['Paper 1', 'Paper 2'].map(p => `<div class="jx-card"><h3>${p} <em class="jx-soon">Coming soon</em></h3>${Object.values(SUBJ).map(s => `<div class="jx-li soon"><span>${s.e}</span><span><b>${s.n}</b><small>MCQ (one or more correct), numerical value, matching — chapter-wise practice and full papers</small></span></div>`).join('')}</div>`).join('')}
      <div class="jx-card"><h3>Chapters <em class="jx-soon">Coming soon</em></h3><p class="jx-p">JEE Advanced adds topics beyond JEE Main in each subject. Chapter lists will appear here as each is ready.</p></div></div>`;
    $('#jxBack').onclick = home;
  }

  /* ================= hooks ================= */
  let SKIP = false;
  const _world = worldScreen;
  worldScreen = function () { const j = ST.jee; if (j && j.track && j.home && !SKIP && ST.profile && !(ST.profile.course)) return home(); return _world.apply(this, arguments); };
  function ownerTools() {
    const ow = D.getElementById('caOwner');
    if (ow && !ow.querySelector('#jxOwn')) {
      const off = ow.querySelector('#caOwOff'), jj = ST.jee || {}, onJ = !!(jj.track && jj.home && !(ST.profile && ST.profile.course));
      if (off) off.insertAdjacentHTML('beforebegin', `<div id="jxOwn"><h3 class="ca-h3">JEE</h3><div class="ca-btns"><button class="btn ghost" id="jxOwOn" ${onJ ? 'disabled' : ''}>JEE mode</button><button class="btn ghost" id="jxOwOff" ${onJ ? '' : 'disabled'}>School world</button></div>
        <div class="ca-seg" role="radiogroup" aria-label="JEE track">${Object.entries(TRACKS).map(([k, t0]) => `<button role="radio" aria-checked="${jj.track === k}" data-jt="${k}">${t0.e} ${t0.n.replace('JEE ', '')}</button>`).join('')}</div><div style="height:10px"></div></div>`);
      const setT = k => { const j = J(); j.track = k; j.cls = k === 'found' ? 9 : k === 'main' ? (j.cls >= 11 && j.cls <= 12 ? j.cls : 11) : null; const r = elig(k === 'full' ? { status: 'passed', first: 2026 } : { status: 'school', cls: j.cls }); j.elig = { xii: r.xii, main: r.main, adv: r.adv }; };
      const go = () => { const j = J(); if (!j.track) setT('main'); j.home = true; if (ST.profile) ST.profile.course = null; save(); try { Look.apply(); } catch (e) {} home(); };
      ow.querySelector('#jxOwOn').onclick = () => { tap(); go(); };
      ow.querySelector('#jxOwOff').onclick = () => { tap(); J().home = false; save(); toast('School world is home now'); worldScreen(); };
      ow.querySelectorAll('[data-jt]').forEach(b => b.onclick = () => { tap(); setT(b.dataset.jt); go(); toast(TRACKS[b.dataset.jt].n + ' selected'); });
    }
  }
  function tile() {
    try { ownerTools(); } catch (e) {}
    if (!ST.profile || ST.profile.course || (window.Cloud && Cloud.isParent && Cloud.isParent())) return;
    const g = +ST.profile.grade || 0, j = ST.jee, own = !!(window.Cloud && Cloud.admin && Cloud.admin());
    if (g < 9 && !(j && j.track) && !own) return;
    const p = D.getElementById('s-practice');
    if (p && p.classList.contains('active') && !p.querySelector(':scope > #jeeTile')) {
      const first = p.querySelector(':scope > #phTile') || p.querySelector(':scope > .card');
      if (first) first.insertAdjacentHTML('beforebegin', `<button type="button" class="card mg-tile jx-tile0" id="jeeTile"><span class="mg-te" aria-hidden="true">🎯</span><span class="mg-tt"><b>JEE Main</b><small>${j && j.track ? TRACKS[j.track].n + ' · Units and Measurements ready' : 'Check eligibility and start your track'}</small></span><span class="mg-chev" aria-hidden="true">›</span></button>`);
    }
    const me = D.getElementById('s-me');
    if (me && me.classList.contains('active') && !me.querySelector('#jeeMe')) {
      const anchor = me.querySelector('[data-ms="b"]') || me.querySelector('.card:last-child');
      if (anchor) { anchor.insertAdjacentHTML('beforebegin', `<div class="card" id="jeeMe" data-ms="b"><h3>🎯 JEE course</h3><p class="sub">${j && j.track ? `${TRACKS[j.track].e} ${TRACKS[j.track].n}${j.home ? ' · your home screen' : ''}` : 'JEE Main for Class 9–12, droppers and eligible college students.'}</p>
        <div class="row"><button class="btn sm" id="jeeMeGo">${j && j.track ? 'Open JEE' : 'Start'}</button>${j && j.track ? `<button class="btn sm ghost" id="jeeMeHome">${j.home ? 'Make school world home' : 'Make JEE my home'}</button>` : ''}</div></div>`); }
    }
    const t = D.getElementById('jeeTile'); if (t && !t.onclick) t.onclick = () => { tap('open'); home(); };
    const g1 = D.getElementById('jeeMeGo'); if (g1 && !g1.onclick) g1.onclick = () => { tap('open'); home(); };
    const g2 = D.getElementById('jeeMeHome'); if (g2 && !g2.onclick) g2.onclick = () => { tap(); J().home = !J().home; save(); toast(J().home ? 'JEE is your home screen now' : 'School world is home now'); D.getElementById('jeeMe').remove(); tile(); };
  }
  let pt = 0; new MutationObserver(() => { if (!pt) pt = requestAnimationFrame(() => { pt = 0; try { tile(); } catch (e) {} }); }).observe(D.querySelector('main') || D.body, { childList: true, subtree: true });

  // onboarding: add JEE next to CA in "Professional courses"
  const _onb = onboard;
  onboard = function (step = 1) {
    const r = _onb.apply(this, arguments);
    if (step === 1) setTimeout(() => {
      const ca = D.getElementById('caEntry'); if (!ca || D.getElementById('jeeEntryB')) return;
      ca.insertAdjacentHTML('beforeend', `<button class="choice ca-entryb" id="jeeEntryB"><b>JEE Main — Engineering entrance (NTA)</b><small>Class 9–12 · droppers · eligible college students · eligibility check</small></button>`);
      D.getElementById('jeeEntryB').onclick = () => { tap(); setup(1); };
    }, 0);
    return r;
  };

  function reopen(v, ...a) { try { ({ home, unit, setup: () => setup(1, { again: true }), pattern, adv: advanced, bank: () => bank(), crash: (u, st) => crash(u, st || 0), practice: () => practiceHub() })[v](...a); } catch (e) { home(); } }

  if (!D.getElementById('jxCss')) D.head.insertAdjacentHTML('beforeend', `<style id="jxCss">
  #s-jee{padding:0}.jx{max-width:760px;margin:0 auto;padding:12px 12px 90px;color:#1b1840;font-size:15px}
  .jx h1{font-size:22px;margin:4px 0}.jx h2.jx-h{font-size:16px;margin:16px 0 8px;background:#fff;border-radius:12px;padding:8px 12px;display:inline-block;color:#2a1b7a}.jx h3{margin:0 0 8px;font-size:16px}
  .jx-hero{background:linear-gradient(135deg,#2a1b7a,#6d28d9 55%,#db2777);color:#fff;border-radius:20px;padding:16px;box-shadow:0 8px 24px #4c1d9540}
  .jx-hero p{margin:6px 0;opacity:.95}.jx-hero.sm{padding:14px}.jx-hero.adv{background:linear-gradient(135deg,#0f172a,#334155)}
  .jx-ht{display:flex;justify-content:space-between;align-items:center}.jx-badge{background:#ffffff26;border-radius:999px;padding:4px 10px;font-size:13px;font-weight:700}
  .jx-lnk{background:none;border:0;color:inherit;text-decoration:underline;cursor:pointer;font:inherit;padding:2px}
  .jx-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}.jx-chip{background:#ffffff26;border:1px solid #ffffff40;color:#fff;border-radius:999px;padding:4px 10px;font-size:12.5px;font-weight:700}
  .jx-chip.ok{background:#16a34a}.jx-chip.no{background:#dc2626}.jx-chip.lnk{cursor:pointer}
  .jx-card{background:#fff;border-radius:16px;padding:14px;margin:10px 0;box-shadow:0 2px 10px #1b184014;border:1px solid #ece9ff;display:block;width:100%;text-align:left;color:inherit;font:inherit;box-sizing:border-box}
  .jx-next{display:flex;align-items:center;gap:10px;justify-content:space-between}.jx-next small{display:block;color:#6b6795}.jx-next b{display:block;font-size:16px}.jx-next span{font-size:12.5px;color:#4b4878}
  .jx-btn{background:linear-gradient(135deg,#6d28d9,#db2777);color:#fff;border:0;border-radius:12px;padding:10px 14px;font-weight:800;font-size:14.5px;cursor:pointer}
  .jx-btn.wide{width:100%;margin-top:8px}.jx-btn.ghost{background:#f1edff;color:#4c1d95}.jx-btn.sm{padding:6px 10px;font-size:13px}.jx-btn:disabled{opacity:.45;cursor:default}
  .jx-back{background:#fff;border:0;color:#5b21b6;font-weight:800;font-size:14px;padding:7px 12px;border-radius:999px;cursor:pointer;margin:2px 0 6px;box-shadow:0 1px 4px #0002}
  .jx>.jx-fine,.jx>.jx-p,#jxBody>.jx-p{background:#ffffffeb;border-radius:12px;padding:8px 10px}.jx-uh{background:#fff;border-radius:16px;padding:12px}
  .jx-path{display:flex;flex-direction:column;gap:6px}.jx-pu{display:flex;align-items:center;gap:10px;background:#f6f4fc;border:1px solid #ece9ff;border-radius:12px;padding:9px 10px;text-align:left;cursor:pointer;font:inherit;color:#5a567f}
  .jx-pu.on{background:#fff;color:#1b1840;border-color:#a78bfa;box-shadow:0 2px 10px #6d28d922}.jx-pu b{display:block;font-size:14px}.jx-pu small{color:#6b6795;font-size:12px}
  .jx-pn{min-width:26px;height:26px;border-radius:50%;background:#f1edff;color:#5b21b6;display:grid;place-items:center;font-weight:800;font-size:12px}.jx-pu.on .jx-pn{background:#6d28d9;color:#fff}
  .jx-st{margin-left:auto;font-size:11.5px;font-weight:800;color:#7c3aed;white-space:nowrap}
  .jx-sub{background:#fff;border-radius:14px;margin:6px 0;border:1px solid #ece9ff;border-left:5px solid var(--c)}.jx-sub summary{display:flex;gap:8px;align-items:center;padding:12px;cursor:pointer;list-style:none}
  .jx-sub summary small{margin-left:auto;color:#6b6795;font-size:12px}.jx-ur{display:grid;grid-template-columns:52px 1fr auto;gap:2px 8px;width:100%;text-align:left;background:none;border:0;border-top:1px solid #f1eff9;padding:8px 12px;font:inherit;color:inherit;cursor:pointer;opacity:.7}
  .jx-ur.on{opacity:1}.jx-ur span{font-size:12px;color:#6b6795;grid-row:span 2}.jx-ur b{font-size:14px}.jx-ur small{font-size:11.5px;color:#6b6795}.jx-ur em{grid-row:1/3;grid-column:3;align-self:center;font-style:normal;font-size:12px;font-weight:800;color:#7c3aed}
  .jx-adv{display:flex;align-items:center;gap:10px;cursor:pointer}.jx-adv>span:first-child{font-size:26px}.jx-adv b{display:block}.jx-adv small{color:#6b6795}.jx-adv em,.jx-soon{margin-left:auto;background:#fef3c7;color:#92400e;border-radius:999px;padding:3px 9px;font-style:normal;font-size:12px;font-weight:800}
  .jx-tools{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.jx-tools button{background:#fff;border:1px solid #ece9ff;border-radius:12px;padding:10px 6px;font:inherit;font-size:13px;font-weight:700;color:#3b2a85;cursor:pointer}
  .jx-fine{font-size:12px;color:#6b6795;margin:8px 4px}.jx-p{color:#4b4878;margin:6px 0;line-height:1.5}.jx-note{font-size:13px;color:#4b4878;background:#f7f5ff;border-radius:10px;padding:8px}
  .jx-opt{display:block;width:100%;text-align:left;background:#f7f5ff;border:1px solid #e4dcff;border-radius:12px;padding:12px;margin:6px 0;font:inherit;color:inherit;cursor:pointer}
  .jx-lab{display:block;font-size:13.5px;font-weight:700;margin:10px 0;color:#3b2a85}.jx-lab select,.jx-lab input{display:block;width:100%;margin-top:5px;padding:9px;border-radius:10px;border:1px solid #d9d2ff;font:inherit;box-sizing:border-box}
  .jx-chk{display:flex;gap:8px;align-items:center;font-size:13.5px;margin:8px 0}
  .jx-el{border-radius:12px;padding:10px;margin:8px 0}.jx-el.ok{background:#ecfdf3}.jx-el.no{background:#fef2f2}.jx-el.wait{background:#fffbeb}.jx-el p{margin:4px 0 0;font-size:13.5px}
  .jx-uh{display:flex;gap:12px;align-items:center;margin:6px 0 10px}.jx-uh small{color:#6b6795}.jx-uh p{margin:0;font-size:12.5px;color:#4b4878}
  .jx-ring{--p:0;width:68px;height:68px;border-radius:50%;background:conic-gradient(#7c3aed calc(var(--p)*1%),#ece9ff 0);display:grid;place-items:center;flex:none}.jx-ring b{background:#fff;width:52px;height:52px;border-radius:50%;display:grid;place-items:center;font-size:14px}
  .jx-tabs{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}.jx-tabs button{flex:none;border:1px solid #e4dcff;background:#fff;border-radius:999px;padding:7px 12px;font:inherit;font-size:13.5px;font-weight:700;color:#4c1d95;cursor:pointer}
  .jx-tabs button[aria-selected=true]{background:#4c1d95;color:#fff;border-color:#4c1d95}
  .jx-step{background:#fff;border-radius:16px;padding:12px;margin:10px 0;border:1px solid #ece9ff}.jx-sh{display:flex;gap:8px;align-items:center}.jx-sh small{margin-left:auto;color:#6b6795;font-size:12px}
  .jx-cc{border:1px solid #efeafe;border-radius:12px;margin:8px 0;background:#fcfbff}.jx-cc summary{display:flex;gap:8px;align-items:center;padding:10px;cursor:pointer;list-style:none}
  .jx-cc summary em{font-style:normal;font-size:11px;font-weight:800;background:#ede9fe;color:#5b21b6;border-radius:999px;padding:2px 7px}.jx-cc summary em.f{background:#dcfce7;color:#166534}.jx-cc summary i{margin-left:auto;color:#16a34a;font-style:normal;font-weight:900}
  .jx-cb{padding:0 12px 12px;line-height:1.6}.jx-cb p{margin:8px 0}.jx-f{background:#f5f3ff;border-left:4px solid #7c3aed;border-radius:8px;padding:8px 10px;margin:6px 0;font-weight:700}
  .jx-t{border-collapse:collapse;width:100%;font-size:13.5px;margin:6px 0}.jx-t td,.jx-t th{border:1px solid #e9e5fb;padding:6px;text-align:left}.jx-t th{background:#f5f3ff}
  .jx-qc{background:#fff;border:1px dashed #c4b5fd;border-radius:12px;padding:10px;margin-top:10px}.jx-qo{display:block;width:100%;text-align:left;margin:5px 0;padding:8px 10px;border-radius:10px;border:1px solid #e4dcff;background:#faf9ff;font:inherit;cursor:pointer;color:inherit}
  .jx-qo.ok,.jx-o.ok{background:#dcfce7;border-color:#22c55e}.jx-qo.no,.jx-o.no{background:#fee2e2;border-color:#ef4444}.jx-why{font-size:13.5px}
  .jx-traps{margin:6px 0;padding-left:20px;line-height:1.55}.jx-traps li{margin:4px 0}
  .jx-bars{display:flex;gap:8px;align-items:flex-end;height:110px;padding-top:6px}.jx-bars div{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end}.jx-bars span{width:70%;background:linear-gradient(#a78bfa,#6d28d9);border-radius:6px 6px 0 0}.jx-bars b{font-size:12px}.jx-bars small{font-size:11px;color:#6b6795}
  .jx-filt{display:flex;gap:8px}.jx-filt select{flex:1;padding:9px;border-radius:10px;border:1px solid #d9d2ff;font:inherit;background:#fff}
  .jx-list{margin-top:8px}.jx-li{display:flex;gap:10px;width:100%;text-align:left;background:#fff;border:1px solid #ece9ff;border-radius:12px;padding:9px;margin:6px 0;font:inherit;color:inherit;cursor:pointer;line-height:1.45}
  .jx-li>span:first-child{min-width:28px;height:28px;border-radius:8px;background:#f1edff;display:grid;place-items:center;font-weight:800;font-size:12px;color:#5b21b6;flex:none}.jx-li>span.ok{background:#dcfce7;color:#166534}.jx-li>span.no{background:#fee2e2;color:#991b1b}
  .jx-li small{display:block;color:#6b6795;font-size:11.5px}.jx-li.soon{cursor:default;opacity:.8}
  .jx-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:8px 0}.jx-tile{background:#fff;border:1px solid #e4dcff;border-radius:14px;padding:12px;text-align:left;font:inherit;color:inherit;cursor:pointer}.jx-tile b{display:block}.jx-tile small{color:#6b6795;font-size:12px}
  .jx-tile.big{grid-column:span 2}
  .jx-strip{display:flex;gap:5px;overflow-x:auto;padding:4px 0 8px;scrollbar-width:thin}.jx-strip button{flex:none;width:32px;height:32px;border-radius:9px;border:1px solid #e4dcff;background:#fff;font-weight:800;font-size:12px;cursor:pointer;color:#4c1d95}
  .jx-strip .cur{outline:2px solid #7c3aed}.jx-strip .ok{background:#dcfce7;border-color:#22c55e}.jx-strip .no{background:#fee2e2;border-color:#ef4444}
  .jx-qt{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}.jx-tag{font-size:11.5px;font-weight:800;border-radius:999px;padding:3px 9px;background:#f1edff;color:#5b21b6}.jx-tag.pyq{background:#fff7ed;color:#9a3412}.jx-tag.prac{background:#ecfeff;color:#155e75}
  .jx-qq{font-size:15.5px;line-height:1.6}.jx-os{margin-top:10px}.jx-o{display:flex;gap:10px;align-items:center;width:100%;text-align:left;margin:6px 0;padding:10px;border-radius:12px;border:1.5px solid #e4dcff;background:#fff;font:inherit;color:inherit;cursor:pointer;line-height:1.45}
  .jx-o>.jx-on{font-style:normal;min-width:24px;height:24px;border-radius:50%;background:#f1edff;display:grid;place-items:center;font-size:12px;font-weight:800;flex:none}.jx-o.sel{border-color:#7c3aed;background:#f5f3ff}
  .jx-num input{width:100%;padding:12px;border-radius:12px;border:1.5px solid #d9d2ff;font:inherit;font-size:17px;box-sizing:border-box;margin-top:10px}.jx-num small{color:#6b6795;font-size:12px}
  .jx-res{margin:10px 0;font-weight:800;padding:8px 10px;border-radius:10px}.jx-res.ok{background:#dcfce7;color:#166534}.jx-res.no{background:#fee2e2;color:#991b1b}
  .jx-sol{background:#f8f7ff;border-radius:12px;padding:10px;margin:8px 0}.jx-sol p{display:flex;gap:8px;margin:8px 0;line-height:1.55}.jx-sol p>.jx-sn{font-style:normal;min-width:22px;height:22px;border-radius:50%;background:#7c3aed;color:#fff;display:grid;place-items:center;font-size:11px;font-weight:800;flex:none}
  .jx-nav{display:flex;gap:8px;justify-content:space-between;margin-top:10px}.jx-nav .jx-btn{flex:1}
  .jx-fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;margin:0 2px;font-size:.92em;line-height:1.15}.jx-fr>span:first-child{border-bottom:1.3px solid currentColor;padding:0 2px}.jx-fr>span:last-child{padding:0 2px}
  .jx-sq{border-top:1.3px solid currentColor;padding:0 1px}.jx sup,.jx sub{font-size:.72em}
  .jx-fv{border-bottom:1px solid #f1eff9;padding:8px 0}.jx-fv small{color:#6b6795;display:block}.jx-fv div{font-weight:700;font-size:15px;margin-top:3px}
  .jx-tbar{position:sticky;top:0;z-index:3;display:flex;gap:10px;align-items:center;justify-content:space-between;background:#1e1b4b;color:#fff;border-radius:12px;padding:8px 10px}.jx-tbar span{font-variant-numeric:tabular-nums;font-weight:800}
  .jx-pal{display:flex;flex-wrap:wrap;gap:5px;margin:10px 0}.jx-pal button{width:34px;height:34px;border-radius:8px;border:0;font-weight:800;cursor:pointer;background:#e5e7eb}
  .jx-pal .p-na{background:#fecaca}.jx-pal .p-a{background:#86efac}.jx-pal .p-r{background:#c4b5fd}.jx-pal .p-ar{background:#a78bfa;color:#fff}.jx-pal .cur{outline:2px solid #111}
  .jx-ta{display:flex;gap:8px;align-items:baseline;border-top:1px solid #f1eff9;padding:6px 0}.jx-ta span{font-size:13px;color:#4b4878}.jx-ta small{margin-left:auto;color:#6b6795}
  .jx-rv summary{cursor:pointer;font-weight:800}.jx-rv.ok{border-left:5px solid #22c55e}.jx-rv.no{border-left:5px solid #ef4444}.jx-sum{text-align:center}.jx-sum h2{font-size:28px;margin:4px 0}
  .jx-goal{font-weight:800;color:#5b21b6;font-size:16px}.jx-dimout{background:#1e1b4b;color:#fff;border-radius:14px;padding:12px;text-align:center;margin:8px 0}.jx-dimout.ok{background:#166534}.jx-dimout b{display:block;font-size:24px;margin:6px 0}.jx-dimout small{color:#ddd6fe}
  .jx-chipsel{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}.jx-dc{display:flex;align-items:center;gap:4px;background:#faf9ff;border:1px solid #e4dcff;border-radius:12px;padding:4px}.jx-dc.hint{border-color:#a78bfa;background:#f5f3ff}
  .jx-dc button{width:30px;height:30px;border-radius:8px;border:0;background:#ede9fe;font-weight:900;font-size:16px;cursor:pointer;color:#4c1d95}.jx-dc span{flex:1;font-size:13px;font-weight:700;text-align:center;line-height:1.2}.jx-dc small{display:block;font-weight:400;font-size:10.5px;color:#6b6795}.jx-dc b{display:block;color:#7c3aed;font-size:11px;min-height:12px}
  .jx-vbox{overflow-x:auto;border-radius:12px;border:1px solid #e4dcff;background:#fff}.jx-vsvg{min-width:600px;max-width:none!important;width:100%;height:auto;display:block}
.jx-crumb{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:0 0 8px}.jx-crumb button,.jx-tagb{border:1px solid #ddd6fe;background:#f5f3ff;color:#4c1d95;border-radius:999px;padding:3px 9px;font-weight:600;font-size:12px;font-family:inherit;cursor:pointer}.jx-crumb button:active,.jx-tagb:active{transform:scale(.96)}.jx-crumb i{color:#a78bfa;font-style:normal}.jx-bm{border:0;background:none;font-size:22px;color:#f59e0b;cursor:pointer;padding:0 6px 0 0;line-height:1}.jx-sheetbg{position:fixed;inset:0;background:#0f0a2a99;z-index:9999;display:flex;align-items:flex-end;justify-content:center;animation:jxf .18s}.jx-sheet.jx{padding:0;margin:0;}.jx-sheet{background:#fff;color:#1b1840;width:100%;max-width:640px;max-height:84vh;border-radius:22px 22px 0 0;display:flex;flex-direction:column;animation:jxu .22s ease-out;font-size:15px}@keyframes jxu{from{transform:translateY(40px);opacity:.4}}@keyframes jxf{from{opacity:0}}.jx-grab{width:44px;height:5px;border-radius:9px;background:#d4d4d8;margin:8px auto 0}.jx-sh-h{display:flex;justify-content:space-between;align-items:center;padding:8px 16px 0}.jx-sh-h h3{margin:0;font-size:18px}.jx-x{border:0;background:#f4f4f5;border-radius:50%;width:34px;height:34px;font-size:16px;cursor:pointer}.jx-sh-b{overflow:auto;padding:6px 16px 10px}.jx-sh-b h4{margin:12px 0 6px}.jx-sh-a{display:flex;gap:8px;padding:10px 16px calc(14px + env(safe-area-inset-bottom));border-top:1px solid #eee}.jx-sh-a .jx-btn{flex:1}.jx-pl{display:grid;gap:6px}.jx-pli{display:grid;grid-template-columns:28px 1fr auto;gap:8px;align-items:center;text-align:left;border:1px solid #eee;border-radius:12px;background:#fafafa;padding:8px;font:inherit;opacity:.6}.jx-pli.on{opacity:1;background:#f5f3ff;border-color:#ddd6fe;cursor:pointer}.jx-pli span{font-weight:800;color:#7c3aed}.jx-pli small{color:#6b6795}.jx-tp{display:grid;grid-template-columns:1fr 90px 54px;gap:8px;align-items:center;width:100%;border:0;background:#fafafa;border-radius:10px;padding:8px;margin:4px 0;text-align:left;font:inherit;cursor:pointer}.jx-bar{height:8px;background:#ede9fe;border-radius:9px;overflow:hidden}.jx-bar i{display:block;height:100%;background:linear-gradient(90deg,#7c3aed,#db2777)}.jx-pc{background:#faf5ff;border-radius:14px;padding:10px 12px;margin:8px 0}.jx-pc h4{margin:0 0 6px}.jx-pc p{margin:6px 0}.jx-qc{background:#fff;border-radius:12px;padding:8px;margin-top:8px}.jx-qco{display:grid;gap:6px;margin:6px 0}.jx-qco button{border:1px solid #ddd6fe;background:#fff;border-radius:10px;padding:8px;text-align:left;font:inherit;cursor:pointer}.jx-qco .ok{background:#dcfce7;border-color:#22c55e}.jx-qco .no{background:#fee2e2;border-color:#ef4444}.jx-qbf{background:#fff;border-radius:16px;padding:10px 12px;margin:12px 0}.jx-qbf summary{display:flex;gap:8px;align-items:center;font-weight:800;cursor:pointer}.jx-qbf summary b{background:#7c3aed;color:#fff;border-radius:999px;padding:1px 8px;font-size:12px}.jx-qbf summary span{margin-left:auto;color:#7c3aed;font-size:13px}.jx-qbf h5{margin:10px 0 4px;font-size:12px;color:#6b6795;text-transform:uppercase;letter-spacing:.04em}.jx-frow{display:flex;flex-wrap:wrap;gap:6px}.jx-fc{border:1px solid #ddd6fe;background:#fff;color:#3b2a8a;border-radius:999px;padding:6px 11px;font-weight:600;font-size:13px;font-family:inherit;cursor:pointer}.jx-fc small{margin-left:5px;color:#a78bfa}.jx-fc.on{background:#7c3aed;color:#fff;border-color:#7c3aed}.jx-fc.on small{color:#e9d5ff}.jx-sortr{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:6px 0}.jx-sortr span{color:#c4b5fd;font-size:13px}.jx-bi{background:#fff;border-radius:16px;padding:10px 12px;margin:8px 0;cursor:pointer;box-shadow:0 2px 8px #0000001a}.jx-bi:active{transform:scale(.99)}.jx-bt{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.jx-st2{margin-left:auto}.jx-bq{margin-top:6px;line-height:1.45}.jx-cu{display:grid;grid-template-columns:48px 1fr auto;gap:10px;align-items:center;width:100%;background:#fff;border:0;border-radius:16px;padding:10px 12px;margin:6px 0;text-align:left;font:inherit;cursor:pointer}.jx-cu small{display:block;color:#6b6795}.jx-cu em{font-style:normal;color:#7c3aed;font-weight:800}.jx-cring{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-weight:800;font-size:12px;color:#4c1d95;background:radial-gradient(#fff 58%,transparent 60%),conic-gradient(#7c3aed calc(var(--p)*1%),#ede9fe 0)}.jx-cstep{display:flex;gap:6px;overflow-x:auto;margin:8px 0}.jx-cstep button{flex:none;border:0;border-radius:999px;padding:7px 11px;background:#ffffff22;color:#e9d5ff;font-weight:700;font-size:13px;font-family:inherit;cursor:pointer}.jx-cstep .cur{background:#fff;color:#4c1d95}.jx-cstep .ok{background:#16a34a;color:#fff}.jx-idea{background:#fff;border-radius:16px;padding:10px 12px;margin:8px 0}.jx-idea summary{display:flex;flex-wrap:wrap;gap:6px;align-items:center;cursor:pointer}.jx-idea p{margin:8px 0;line-height:1.5}.jx-flips{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}.jx-flip{min-height:92px;border:0;border-radius:16px;background:linear-gradient(135deg,#4c1d95,#7c3aed);color:#fff;font-weight:700;font-size:15px;font-family:inherit;cursor:pointer;padding:10px;position:relative}.jx-flip .b{display:none;color:#1b1840}.jx-flip.on{background:#fff;box-shadow:inset 0 0 0 2px #7c3aed}.jx-flip.on .f{display:none}.jx-flip.on .b{display:block}.jx-trap{display:grid;grid-template-columns:24px 1fr auto;gap:8px;align-items:center;width:100%;border:0;background:#fff7ed;border-radius:14px;padding:10px;margin:6px 0;text-align:left;font:inherit;cursor:pointer}.jx-trap em{font-style:normal;color:#c2410c;font-weight:800;font-size:12px}.jx-trap.on{background:#dcfce7}.jx-trap.on em{color:#16a34a}.jx-mode{display:flex;background:#ffffff1a;border-radius:999px;padding:4px;margin:4px 0 10px}.jx-mode button{flex:1;border:0;border-radius:999px;padding:9px;font-weight:800;font-size:14px;font-family:inherit;background:none;color:#e9d5ff;cursor:pointer}.jx-mode .on{background:#fff;color:#4c1d95}.jx-kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:8px 0}.jx-kpi div{background:#fff;border-radius:14px;padding:8px;text-align:center}.jx-kpi b{display:block;font-size:20px;color:#4c1d95}.jx-kpi small{color:#6b6795}.jx-hub{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}.jx-ht2{border:0;border-radius:18px;background:#fff;padding:12px;text-align:left;font:inherit;cursor:pointer;display:flex;flex-direction:column;gap:3px;box-shadow:0 3px 10px #00000022}.jx-ht2 span{font-size:26px}.jx-ht2 small{color:#6b6795;line-height:1.3}.jx-ht2:active{transform:scale(.98)}.jx-sec>summary{list-style:none;display:flex;align-items:center;justify-content:space-between;gap:8px;cursor:pointer}.jx-sec>summary::-webkit-details-marker{display:none}.jx-sec>summary{background:#fff;border-radius:16px;padding:12px 14px;margin:14px 0 8px;box-shadow:0 2px 10px rgba(0,0,0,.12)}.jx-sec>summary h2{margin:0;background:none!important;padding:0!important;box-shadow:none!important;font-size:17px}.jx-sec>summary h2::before{content:'▸';display:inline-block;margin-right:6px;transition:transform .2s;color:#7c3aed}.jx-sec[open]>summary h2::before{transform:rotate(90deg)}.jx-sec>summary small{color:#7c3aed;font-weight:700;font-size:12px;white-space:nowrap}.jx-figw{margin:10px 0;text-align:center}.jx-figw svg{max-width:340px;width:100%;height:auto;color:#1e1b4b}.jx-circ{width:100%;max-width:420px;height:auto;display:block;margin:6px auto}.jx-curve{width:100%;height:auto}
  .jx-seg3{display:flex;gap:6px;margin:6px 0}.jx-seg3 button{flex:1 1 28%;border:1px solid #d9d2ff;background:#f7f5ff;border-radius:10px;padding:8px 4px;font:inherit;font-size:12.5px;font-weight:700;cursor:pointer;color:#4c1d95}.jx-seg3 .on{background:#4c1d95;color:#fff}
  .jx-read{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.jx-read span{background:#1e1b4b;color:#ddd6fe;border-radius:10px;padding:5px 8px;font-size:12px}.jx-read b{color:#fff}
  .jx-sl{display:block;margin:8px 0;font-size:13px;font-weight:700;color:#3b2a85}.jx-sl span{display:flex;justify-content:space-between}.jx-sl input{width:100%;accent-color:#7c3aed}
  .jx-mis{padding:7px 10px;border-radius:10px;background:#f7f5ff;margin:5px 0;font-size:13.5px}.jx-mis.ok{background:#dcfce7}
  .jx-qn{display:flex;gap:8px;align-items:center;font-weight:700;margin:6px 0}.jx-qn select{padding:6px;border-radius:8px;border:1px solid #d9d2ff}
  .jx-boxes{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.jx-sub2{text-align:center;cursor:pointer}.jx-sub2 small{display:block;font-weight:800;color:#5b21b6}.jx-sub2 div{display:flex}.jx-sub2 span{width:24px;height:26px;border:1.5px solid #7c3aed;display:grid;place-items:center;font-weight:900;font-size:13px;margin-left:-1.5px;background:#fff}
    .jx-tile0{background:linear-gradient(135deg,#6d28d9,#db2777)!important;color:#fff!important;margin-bottom:10px}.jx-tile0 small{color:#fce7f3!important}
  html[data-theme=dark] .jx{color:#ece9ff}html[data-theme=dark] .jx-card,html[data-theme=dark] .jx-step,html[data-theme=dark] .jx-pu,html[data-theme=dark] .jx-sub,html[data-theme=dark] .jx-li,html[data-theme=dark] .jx-tile,html[data-theme=dark] .jx-o,html[data-theme=dark] .jx-tools button{background:#1d1a3a;border-color:#2f2a5c;color:#ece9ff}
  </style>`);


  /* ================= JEE as the ACTIVE course: games, puzzles and live rooms ask JEE questions =================
     JEE is the active course when the student has a JEE track and made JEE their home (school world switched off).
     Used by js/playhub.js (Arcade), js/live.js (game rooms) and js/puzzles.js (word puzzles). */
  const active = () => { try { const j = ST.jee; return !!(j && j.track && j.home && !(ST.profile && ST.profile.course)); } catch (e) { return false; } };
  const SUP = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '−': '⁻', '-': '⁻', '+': '⁺', 'n': 'ⁿ', '(': '⁽', ')': '⁾', 'i': 'ⁱ' };
  const SUB = { '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉', '−': '₋', '+': '₊', 'a': 'ₐ', 'e': 'ₑ', 'o': 'ₒ', 'x': 'ₓ', 'n': 'ₙ', 'k': 'ₖ', 'm': 'ₘ', 'p': 'ₚ', 's': 'ₛ', 't': 'ₜ', 'i': 'ᵢ', 'r': 'ᵣ' };
  /* plain text for places that cannot draw maths (game cards): \f{a}{b} → (a)/(b), ^{2} → ², _{2} → ₂, √{x} → √(x) */
  function plain(s) {
    s = String(s == null ? '' : s).replace(/<[^>]+>/g, ' ');
    for (let k = 0; k < 8; k++) {
      const t = s.replace(/\\f\{([^{}]*)\}\{([^{}]*)\}/g, (_, a, b) => `${/^[\w.]+$/.test(a) ? a : '(' + a + ')'}/${/^[\w.]+$/.test(b) ? b : '(' + b + ')'}`)
        .replace(/\^\{([^{}]*)\}/g, (_, a) => [...a].every(c => SUP[c]) ? [...a].map(c => SUP[c]).join('') : `^(${a})`)
        .replace(/_\{([^{}]*)\}/g, (_, a) => [...a].every(c => SUB[c]) ? [...a].map(c => SUB[c]).join('') : `_${a}`)
        .replace(/√\{([^{}]*)\}/g, (_, a) => /^[\w.]+$/.test(a) ? '√' + a : `√(${a})`);
      if (t === s) break; s = t;
    }
    return s.replace(/\s+/g, ' ').trim();
  }
  function hashS(s) { let h = 2166136261; for (const c of String(s)) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; }
  /* a numeric-answer question as a 4-option card: the right value plus three believable, distinct wrong values */
  function numOpts(n, key) {
    const c = [n + 1, n - 1, n * 2, Math.round(n / 2), n + 10, n - 10, n * 10, n + 2, n - 2, Math.round(n * 1.5)].filter(x => x !== n && (n < 0 || x >= 0) && Number.isFinite(x));
    const seen = new Set([n]), pick = []; let h = hashS(key);
    while (pick.length < 3 && c.length) { const i = h % c.length; h = Math.imul(h ^ 0x9e3779b9, 2654435761) >>> 0; const x = c.splice(i, 1)[0]; if (!seen.has(x)) { seen.add(x); pick.push(x); } }
    if (pick.length < 3) return null;
    const opts = [n, ...pick].map(String), order = opts.map((o, i) => [hashS(key + o), i]).sort((a, b) => a[0] - b[0]).map(x => x[1]);
    return { options: order.map(i => opts[i]), answer: order.indexOf(0) };
  }
  const unitTitle = uid => { const [s, u] = uid.split('-'); const x = SUBJ[s] && SUBJ[s].u[+u.slice(1) - 1]; return x ? x[0] : uid; };
  /* every ready unit's questions (real JEE + practice) as plain 4-option cards, each tagged with its source */
  async function cards(sel) {
    const ids = Object.keys(READY).filter(u => !sel || !sel.length || sel.includes(u) || sel.includes(u.split('-')[0]));
    const out = [];
    for (const uid of ids) {
      let d; try { d = await data(uid); } catch (e) { continue; }
      const [s] = uid.split('-'), tops = d.topics || {};
      [...d.pyq, ...d.prac].forEach(q => {
        if (q.fig) return;
        let options = q.o, answer = q.a;
        if (!options) { const no = typeof q.n === 'number' ? numOpts(q.n, q.id) : null; if (!no) return; options = no.options; answer = no.answer; }
        if (!Array.isArray(options) || options.length < 2 || options.length > 4) return;
        const pq = plain(q.q), po = options.map(plain);
        if (!pq || po.some(o => !o) || new Set(po).size !== po.length) return;
        out.push({ q: pq, options: po, answer, explain: plain((q.sol || []).join(' ')), id: q.id, real: q.kind === 'pyq', uid,
          src: { sid: 'jee-' + s, sname: SUBJ[s].n, se: SUBJ[s].e, ci: 0, ch: unitTitle(uid), tid: uid, tt: tops[q.t] || '' } });
      });
    }
    return out;
  }
  async function arcadePool(prog, sel) {
    const P = { quiz: [], tf: [], speed: [], match: [], sort: [], order: [], subjects: Object.entries(SUBJ).map(([k, s]) => ({ id: 'jee-' + k, name: s.n })), chapter: null, multi: false };
    if (prog) prog(0, 1); const all = await cards(sel); if (prog) prog(1, 1);
    const ok = q => { try { return window.Arcade && Arcade.okQ ? Arcade.okQ(q) : true; } catch (e) { return true; } };
    for (let i = all.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [all[i], all[j]] = [all[j], all[i]]; }
    P.quiz = all.filter(ok).slice(0, 400); return P;
  }
  async function livePool(need, lvl) {
    const all = await cards(), want = lvl === 'easy' ? 1 : lvl === 'hard' ? 3 : lvl === 'moderate' ? 2 : 0;
    const by = {}; all.forEach(c => { (by[c.uid] = by[c.uid] || []).push(c); });
    const lists = Object.values(by).map(l => { for (let i = l.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [l[i], l[j]] = [l[j], l[i]]; } return l; });
    const out = []; while (out.length < need && lists.some(l => l.length)) for (const l of lists) if (l.length && out.length < need) { const c = l.pop(); out.push({ q: c.q, o: c.options, a: c.answer, s: `${c.src.se} ${c.src.sname} · ${c.src.ch}${c.real ? ' · real JEE' : ''}`.slice(0, 118), x: c.explain.slice(0, 580) }); }
    return out;
  }
  /* word puzzles: each ready unit is a "chapter" of key words + plain clues */
  function puzzleSubjects() {
    return Object.entries(SUBJ).map(([k, s]) => ({ id: 'jee-' + k, name: s.n, e: s.e, chs: s.u.map((u, i) => [uidOf(k, i), u[0], i + 1]).filter(x => READY[x[0]]).map(([uid, t, n]) => ({ n, title: t, sc: { k: 'j', u: uid } })) })).filter(x => x.chs.length);
  }
  const unitInfo = uid => { const [s, u] = uid.split('-'); return { title: unitTitle(uid), sub: `JEE Main · ${SUBJ[s].n} · Unit ${+u.slice(1)}`, emoji: SUBJ[s].e, sname: SUBJ[s].n }; };
  const lastUnit = () => { const j = ST.jee || {}; return READY[j.last] ? j.last : Object.keys(READY)[0]; };
  const filePath = uid => { const [s, n] = uid.split("-"); return `content/jee/${s}/${n}.json`; };

  /* ================= Subject › Unit › Topic chips + explanation pop-ups (every question shows where it is from) ================= */
  const subjOfU = uid => uid.split('-')[0];
  function crumbs(uid, q) {
    const s = subjOfU(uid), d = CACHE[uid], tn = (d && d.topics && d.topics[q.t]) || q.t;
    return `<div class="jx-crumb"><button data-pop="s:${s}">${SUBJ[s].e} ${SUBJ[s].n}</button><i>›</i><button data-pop="u:${uid}">Unit ${+uid.split('-u')[1]} · ${esc(unitName(uid))}</button><i>›</i><button data-pop="t:${uid}:${esc(q.t)}">🔎 ${esc(tn)}</button></div>`;
  }
  function wireCrumbs(root) { root.querySelectorAll('[data-pop]').forEach(b => b.onclick = e => { e.stopPropagation(); tap(); pop(b.dataset.pop); }); }
  function sheet(title, html, actions = []) {
    let m = D.getElementById('jxSheet'); if (m) m.remove();
    m = D.createElement('div'); m.id = 'jxSheet'; m.className = 'jx-sheetbg';
    m.innerHTML = `<div class="jx-sheet jx" role="dialog" aria-modal="true" aria-label="${esc(title)}"><div class="jx-grab"></div><div class="jx-sh-h"><h3>${title}</h3><button class="jx-x" aria-label="Close">✕</button></div><div class="jx-sh-b">${html}</div>
      ${actions.length ? `<div class="jx-sh-a">${actions.map((a, k) => `<button class="jx-btn ${k ? 'ghost' : ''}" data-act="${k}">${a[0]}</button>`).join('')}</div>` : ''}</div>`;
    D.body.appendChild(m);
    const close = () => m.remove();
    m.onclick = e => { if (e.target === m) close(); }; m.querySelector('.jx-x').onclick = close;
    m.querySelectorAll('[data-act]').forEach(b => b.onclick = () => { close(); actions[+b.dataset.act][1](); });
    return m;
  }
  async function pop(key) {
    const [k, a, b] = key.split(':');
    if (k === 's') {
      const S0 = SUBJ[a], ready = S0.u.map((u, i) => [uidOf(a, i), u]).filter(x => READY[x[0]]);
      sheet(`${S0.e} ${S0.n} in JEE Main`, `<p class="jx-p">${S0.u.length} units in the NTA syllabus · <b>${ready.length} ready</b> here with ${ready.reduce((t, x) => t + READY[x[0]].pyq, 0)} real JEE questions and ${ready.reduce((t, x) => t + READY[x[0]].prac, 0)} practice questions.</p>
        <div class="jx-pl">${S0.u.map((u, i) => { const id = uidOf(a, i); return `<button class="jx-pli ${READY[id] ? 'on' : ''}" data-u="${id}"><span>${i + 1}</span><b>${esc(u[0])}</b><small>${READY[id] ? READY[id].pyq + ' real Qs' : 'coming'}</small></button>`; }).join('')}</div>`,
        [['📚 Questions from this subject', () => bank({ subj: [a] })]]);
      D.querySelectorAll('#jxSheet [data-u]').forEach(x => x.onclick = () => { if (!READY[x.dataset.u]) return toast('This unit is being built'); D.getElementById('jxSheet').remove(); NAVP = false; unit(x.dataset.u); });
      return;
    }
    const d = await data(a);
    if (k === 'u') {
      const tp = Object.entries(d.topics || {}), cnt = t => d.pyq.filter(q => q.t === t).length;
      sheet(`${SUBJ[subjOfU(a)].e} ${esc(unitName(a))}`, `<p class="jx-fine">Class ${esc(String(d.cls || ''))} · NTA syllabus</p><p class="jx-p">${esc(d.syllabus || '')}</p>
        <h4>Topics and how often JEE asked them</h4>${tp.map(([t, n]) => `<button class="jx-tp" data-pt="${esc(t)}"><b>🔎 ${esc(n)}</b><span class="jx-bar"><i style="width:${Math.min(100, cnt(t) * 6)}%"></i></span><small>${cnt(t)} real</small></button>`).join('')}`,
        [['📖 Learn this unit', () => { NAVP = false; unit(a); }], ['📚 Questions from this unit', () => bank({ units: [a] })]]);
      D.querySelectorAll('#jxSheet [data-pt]').forEach(x => x.onclick = () => pop(`t:${a}:${x.dataset.pt}`));
      return;
    }
    const tn = (d.topics || {})[b] || b, cards = (d.cards || []).filter(c => c.topic === b);
    const real = d.pyq.filter(q => q.t === b);
    sheet(`🔎 ${esc(tn)}`, `<p class="jx-fine">${SUBJ[subjOfU(a)].e} ${SUBJ[subjOfU(a)].n} › ${esc(unitName(a))}</p>
      ${cards.length ? cards.map(c => `<div class="jx-pc"><h4>${c.e || '💡'} ${esc(c.t)}</h4>${c.body.map(x => `<p>${mx(x)}</p>`).join('')}
        ${c.check ? `<div class="jx-qc" data-a="${c.check.a}"><b>Quick check:</b> ${mx(c.check.q)}<div class="jx-qco">${c.check.o.map((o, j) => `<button data-o="${j}">${mx(o)}</button>`).join('')}</div><small class="jx-why" hidden>${mx(c.check.why)}</small></div>` : ''}</div>`).join('')
        : `<p class="jx-p">${esc(d.syllabus || '')}</p>`}
      <p class="jx-fine">JEE asked this topic <b>${real.length}</b> time${real.length === 1 ? '' : 's'} in 2024–2026 papers.</p>`,
      [['🎯 Practise this topic', () => bank({ units: [a], topics: [b] })], ['📖 Open the full lesson', () => { NAVP = false; unit(a); }]]);
    D.querySelectorAll('#jxSheet .jx-qc').forEach(box => box.querySelectorAll('[data-o]').forEach(bt => bt.onclick = () => {
      const ok = +bt.dataset.o === +box.dataset.a; bt.classList.add(ok ? 'ok' : 'no'); if (!ok) box.querySelector(`[data-o="${box.dataset.a}"]`).classList.add('ok'); box.querySelector('.jx-why').hidden = false; tap(ok ? 'correct' : 'wrong'); }));
  }

  /* ================= 📚 QUESTION BANK — every ready question, filtered any way ================= */
  const BK = { subj: [], units: [], topics: [], src: [], yr: [], diff: [], type: [], st: [], sort: 'smart', shown: 30 };
  async function allItems() {
    const out = [];
    for (const uid of Object.keys(READY)) { let d; try { d = await data(uid); } catch (e) { continue; } [...d.pyq, ...d.prac].forEach(q => out.push({ q, uid })); }
    return out;
  }
  const statusOf = it => { const a = U(it.uid).ans[it.q.id]; return (J().bm || []).includes(it.uid + '|' + it.q.id) ? 'bm' : !a ? 'new' : a.ok ? 'ok' : 'no'; };
  function bankFilter(all) {
    const f = BK, has = (arr, v) => !arr.length || arr.includes(v);
    let L = all.filter(it => has(f.subj, subjOfU(it.uid)) && has(f.units, it.uid) && (!f.topics.length || f.topics.includes(it.q.t))
      && has(f.src, it.q.kind) && (!f.yr.length || (it.q.kind === 'pyq' && f.yr.includes(String(it.q.src.y)))) && has(f.diff, String(it.q.diff || 2))
      && has(f.type, it.q.n !== undefined ? 'num' : 'mcq') && (!f.st.length || f.st.some(s0 => s0 === 'bm' ? (J().bm || []).includes(it.uid + '|' + it.q.id) : statusOf(it) === s0 || (s0 === 'new' && !U(it.uid).ans[it.q.id]))));
    if (f.sort === 'new') L = L.slice().sort((a, b) => (b.q.kind === 'pyq') - (a.q.kind === 'pyq') || String((b.q.src || {}).d || '').localeCompare(String((a.q.src || {}).d || '')));
    else if (f.sort === 'hard') L = L.slice().sort((a, b) => (b.q.diff || 2) - (a.q.diff || 2));
    else L = L.slice().sort((a, b) => (statusOf(a) === 'no' ? 0 : statusOf(a) === 'new' ? 1 : 2) - (statusOf(b) === 'no' ? 0 : statusOf(b) === 'new' ? 1 : 2) || (b.q.kind === 'pyq') - (a.q.kind === 'pyq'));
    return L;
  }
  async function bank(preset) {
    NAVP = true; const el = screen('practice'); here('bank');
    if (preset) { Object.assign(BK, { subj: [], units: [], topics: [], src: [], yr: [], diff: [], type: [], st: [], shown: 30 }, preset); }
    el.innerHTML = `<div class="jx"><p class="jx-p">Loading every question…</p></div>`;
    const all = await allItems(); const cnt = (pred) => all.filter(pred).length;
    const draw = () => {
      const L = bankFilter(all), units = Object.keys(READY).filter(u => !BK.subj.length || BK.subj.includes(subjOfU(u)));
      const tops = BK.units.length === 1 ? Object.entries((CACHE[BK.units[0]] || {}).topics || {}) : [];
      const chip = (grp, v, label, n) => `<button class="jx-fc ${BK[grp].includes(v) ? 'on' : ''}" data-g="${grp}" data-v="${esc(v)}">${label}${n != null ? `<small>${n}</small>` : ''}</button>`;
      const nF = ['subj', 'units', 'topics', 'src', 'yr', 'diff', 'type', 'st'].reduce((t, k) => t + BK[k].length, 0);
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Practice</button>
        <div class="jx-hero sm"><h1>📚 Question bank</h1><p>${all.length} questions · ${cnt(x => x.q.kind === 'pyq')} real JEE Main (2024–2026) · ${cnt(x => x.q.kind === 'prac')} similar practice. Every answer checked five ways.</p></div>
        <details class="jx-qbf" ${BK.open !== false ? 'open' : ''}><summary>🎛️ Filters ${nF ? `<b>${nF} on</b>` : ''}<span>${L.length} match</span></summary>
          <h5>Subject</h5><div class="jx-frow">${Object.entries(SUBJ).map(([k, s0]) => chip('subj', k, `${s0.e} ${s0.n}`, cnt(x => subjOfU(x.uid) === k))).join('')}</div>
          <h5>Unit</h5><div class="jx-frow">${units.map(u => chip('units', u, esc(unitName(u)), cnt(x => x.uid === u))).join('')}</div>
          ${tops.length ? `<h5>Topic</h5><div class="jx-frow">${tops.map(([t, n]) => chip('topics', t, esc(n))).join('')}</div>` : '<p class="jx-fine">Pick ONE unit to filter by topic.</p>'}
          <h5>Source</h5><div class="jx-frow">${chip('src', 'pyq', '🏛️ Real JEE Main')}${chip('src', 'prac', '🎯 Similar practice')}</div>
          <h5>Year (real questions)</h5><div class="jx-frow">${['2026', '2025', '2024'].map(y => chip('yr', y, y, cnt(x => x.q.kind === 'pyq' && String(x.q.src.y) === y))).join('')}</div>
          <h5>Difficulty</h5><div class="jx-frow">${chip('diff', '1', '🟢 Easy')}${chip('diff', '2', '🟡 Medium')}${chip('diff', '3', '🔴 Hard')}</div>
          <h5>Type</h5><div class="jx-frow">${chip('type', 'mcq', 'MCQ (4 options)')}${chip('type', 'num', 'Numerical')}</div>
          <h5>My status</h5><div class="jx-frow">${chip('st', 'new', '⚪ Not tried')}${chip('st', 'no', '❌ Got wrong')}${chip('st', 'ok', '✅ Solved')}${chip('st', 'bm', '⭐ Saved')}</div>
          <div class="jx-frow"><button class="jx-fc" id="jxClear">✖ Clear all</button></div></details>
        <div class="jx-sortr"><span>Sort</span>${[['smart', 'Smart (wrong first)'], ['new', 'Newest papers'], ['hard', 'Hardest first']].map(([k, n]) => `<button class="jx-fc ${BK.sort === k ? 'on' : ''}" data-sort="${k}">${n}</button>`).join('')}</div>
        <div class="jx-nav"><button class="jx-btn" id="jxSolveAll" ${L.length ? '' : 'disabled'}>▶ Solve these ${Math.min(L.length, 25)} in a row</button></div>
        <div class="jx-bl">${L.slice(0, BK.shown).map((it, k) => { const q = it.q, st = statusOf(it);
          return `<div class="jx-bi" data-k="${k}">${crumbs(it.uid, q)}<div class="jx-bt"><span class="jx-tag ${q.kind}">${q.kind === 'pyq' ? '🏛️ ' + srcTag(q.src) : '🎯 Practice'}</span><span class="jx-tag">${['', '🟢', '🟡', '🔴'][q.diff || 2]}${q.n !== undefined ? ' Numerical' : ' MCQ'}</span><span class="jx-st2 ${st}">${{ new: '', ok: '✅', no: '❌', bm: '⭐' }[st]}</span></div>
            <div class="jx-bq">${mx(q.q.length > 170 ? q.q.slice(0, 167) + '…' : q.q)}</div></div>`; }).join('') || '<p class="jx-p">No question matches — remove a filter.</p>'}</div>
        ${L.length > BK.shown ? `<button class="jx-btn ghost wide" id="jxMore">Show more (${L.length - BK.shown} left)</button>` : ''}</div>`;
      $('#jxBack').onclick = () => { tap(); practiceHub(); };
      wireCrumbs(el);
      el.querySelector('.jx-qbf').ontoggle = e => { BK.open = e.target.open; };
      el.querySelectorAll('[data-g]').forEach(b => b.onclick = () => { tap(); const g = b.dataset.g, v = b.dataset.v, a = BK[g], x = a.indexOf(v); if (x < 0) a.push(v); else a.splice(x, 1); if (g === 'units' || g === 'subj') BK.topics = []; BK.shown = 30; draw(); });
      el.querySelectorAll('[data-sort]').forEach(b => b.onclick = () => { tap(); BK.sort = b.dataset.sort; draw(); });
      $('#jxClear').onclick = () => { tap(); ['subj', 'units', 'topics', 'src', 'yr', 'diff', 'type', 'st'].forEach(k => BK[k] = []); draw(); };
      const mo = $('#jxMore'); if (mo) mo.onclick = () => { tap(); BK.shown += 30; draw(); };
      const back = () => bank();
      $('#jxSolveAll').onclick = () => { tap('open'); run(L[0].uid, [], { items: L.slice(0, 25), title: 'Question bank', back }); };
      el.querySelectorAll('.jx-bi').forEach(b => b.onclick = () => { tap('open'); const k = +b.dataset.k; run(L[k].uid, [], { items: L.slice(Math.max(0, k - 0), k + 25), title: 'Question bank', back }); });
    };
    draw();
  }

  /* ================= ⚡ CRASH COURSE — one fast, hands-on sprint per unit ================= */
  async function crash(uid, step = 0) {
    NAVP = true; const el = screen('practice'); here('crash', uid, step);
    if (!uid) {
      const C = J().crash || {};
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Practice</button><div class="jx-hero sm"><h1>⚡ Crash course</h1><p>Each unit in about 15 minutes: big ideas → formula flash cards → trap check → the real JEE questions that matter most. Made for the last weeks before the exam.</p></div>
        ${Object.entries(SUBJ).map(([k, s0]) => { const r = s0.u.map((u, i) => uidOf(k, i)).filter(u => READY[u]); return r.length ? `<details class="jx-sec" open><summary><h2 class="jx-h">${s0.e} ${s0.n}</h2><small>${r.filter(u => C[u] >= 4).length}/${r.length} sprinted</small></summary>
          ${r.map(u => `<button class="jx-cu" data-u="${u}"><span class="jx-cring" style="--p:${(C[u] || 0) * 25}">${C[u] >= 4 ? '✓' : (C[u] || 0) + '/4'}</span><span><b>${esc(unitName(u))}</b><small>${READY[u].pyq} real questions · ${(CACHE[u] && CACHE[u].formulas || []).length || ''} ${CACHE[u] ? 'formulas' : ''}</small></span><em>${C[u] >= 4 ? 'Again' : C[u] ? 'Continue' : 'Start'} ▶</em></button>`).join('')}</details>` : ''; }).join('')}</div>`;
      $('#jxBack').onclick = () => { tap(); practiceHub(); };
      el.querySelectorAll('[data-u]').forEach(b => b.onclick = () => { tap('open'); const c = (J().crash || {})[b.dataset.u] || 0; crash(b.dataset.u, c >= 4 ? 0 : c); });
      return;
    }
    const d = await data(uid), C = J().crash || (J().crash = {});
    const mark = n => { if ((C[uid] || 0) < n) { C[uid] = n; save(); } };
    const STEPS = ['💡 Big ideas', '🃏 Formula flips', '⚠️ Trap check', '🏛️ Must-do JEE'];
    const head = `<button class="jx-back" id="jxBack">← Crash course</button><div class="jx-cstep">${STEPS.map((n, k) => `<button data-st="${k}" class="${k === step ? 'cur' : k < (C[uid] || 0) ? 'ok' : ''}">${n}</button>`).join('')}</div><h2 class="jx-h">${SUBJ[subjOfU(uid)].e} ${esc(unitName(uid))}</h2>`;
    let body = '';
    if (step === 0) body = d.cards.map((c, k) => `<details class="jx-idea" ${k ? '' : 'open'}><summary>${c.e || '💡'} <b>${esc(c.t)}</b><button class="jx-tagb" data-pop="t:${uid}:${esc(c.topic)}">🔎 ${esc((d.topics || {})[c.topic] || '')}</button></summary>${c.body.map(x => `<p>${mx(x)}</p>`).join('')}</details>`).join('');
    else if (step === 1) body = `<p class="jx-fine">Say the formula in your head, then tap to flip.</p><div class="jx-flips">${d.formulas.map(([n, f]) => `<button class="jx-flip"><span class="f">${esc(n)}</span><span class="b">${mx(f)}</span></button>`).join('')}</div>`;
    else if (step === 2) body = `<p class="jx-fine">These catch most students. Tap each one once you are sure you will not fall for it.</p>${d.traps.map((t, k) => `<button class="jx-trap" data-k="${k}"><span>⚠️</span><span>${mx(t)}</span><em>Got it ✓</em></button>`).join('')}`;
    else {
      const freq = {}; d.pyq.forEach(q => freq[q.t] = (freq[q.t] || 0) + 1);
      const must = d.pyq.slice().sort((a, b) => (freq[b.t] - freq[a.t]) || (b.diff || 2) - (a.diff || 2)).filter((q, k, arr) => arr.findIndex(x => x.t === q.t) === k || k < 8).slice(0, 8);
      body = `<p class="jx-p">JEE keeps returning to these topics: ${Object.entries(freq).sort((a, b) => b[1] - a[1]).slice(0, 3).map(([t, n]) => `<button class="jx-tagb" data-pop="t:${uid}:${esc(t)}">🔎 ${esc((d.topics || {})[t] || t)} · ${n}×</button>`).join(' ')}</p>
        <p class="jx-fine">${must.length} real questions picked from the most-asked topics. Solve them, then the unit is sprinted.</p><button class="jx-btn wide" id="jxMust">▶ Solve the must-do questions</button>`;
      el.dataset.must = must.map(q => q.id).join(',');
    }
    el.innerHTML = `<div class="jx">${head}${body}<div class="jx-nav">${step ? '<button class="jx-btn ghost" id="jxPrevS">◀ Back</button>' : ''}${step < 3 ? '<button class="jx-btn" id="jxNextS">Next ▶</button>' : ''}</div></div>`;
    $('#jxBack').onclick = () => { tap(); crash(); };
    wireCrumbs(el);
    el.querySelectorAll('[data-st]').forEach(b => b.onclick = () => { tap(); crash(uid, +b.dataset.st); });
    el.querySelectorAll('.jx-flip').forEach(b => b.onclick = () => { tap(); b.classList.toggle('on'); });
    el.querySelectorAll('.jx-trap').forEach(b => b.onclick = () => { tap('correct'); b.classList.add('on'); });
    const nx = $('#jxNextS'); if (nx) nx.onclick = () => { tap(); mark(step + 1); crash(uid, step + 1); };
    const pv = $('#jxPrevS'); if (pv) pv.onclick = () => { tap(); crash(uid, step - 1); };
    const ms = $('#jxMust'); if (ms) ms.onclick = () => { tap('open'); mark(4); const ids = el.dataset.must.split(','); run(uid, ids, { title: 'Crash course', back: () => crash(uid, 3) }); };
  }

  /* ================= JEE PRACTICE HUB (Practice tab while JEE is the active course) ================= */
  async function practiceHub() {
    NAVP = true; const el = screen('practice'); here('practice');
    const j = J(), ready = Object.keys(READY), all = ready.reduce((t, u) => t + READY[u].pyq + READY[u].prac, 0);
    const done = ready.reduce((t, u) => t + Object.keys(U(u).ans).length, 0), wrong = j.mist.length, bm = (j.bm || []).length;
    el.innerHTML = `<div class="jx">
      <div class="jx-mode"><button class="on">🎯 JEE Main</button><button id="jxToSchool">🏫 ${ST.profile && ST.profile.grade ? 'Class ' + ST.profile.grade : 'School'}</button></div>
      <p class="jx-fine" style="margin-top:-4px">Games, puzzles and questions here come only from JEE Main. Switch to 🏫 for your school class.</p>
      <div class="jx-kpi"><div><b>${done}</b><small>solved</small></div><div><b>${wrong}</b><small>to fix</small></div><div><b>${bm}</b><small>saved</small></div><div><b>${all}</b><small>in bank</small></div></div>
      <div class="jx-hub">
        <button class="jx-ht2" id="jxQB"><span>📚</span><b>Question bank</b><small>${all} questions · filter by subject, unit, topic, year, difficulty</small></button>
        <button class="jx-ht2" id="jxCC"><span>⚡</span><b>Crash course</b><small>Each unit in 15 minutes: ideas, formula flips, traps, must-do JEE</small></button>
        <button class="jx-ht2" id="jxPlay"><span>🎮</span><b>Play</b><small>Quiz Show, Snakes, Boss Battle, crosswords — all with JEE questions</small></button>
        <button class="jx-ht2" id="jxMG"><span>🧠</span><b>Mind Gym</b><small>Reasoning, IQ and focus puzzles for exam days</small></button>
        <button class="jx-ht2" id="jxMB"><span>📕</span><b>Mistake book</b><small>${wrong ? wrong + ' questions to fix' : 'Empty — great work'}</small></button>
        <button class="jx-ht2" id="jxRooms"><span>🏁</span><b>Game rooms</b><small>Race friends live — everyone gets JEE questions</small></button>
      </div>
      <details class="jx-sec" data-sec="pu" ${secOpen('pu', true)}><summary><h2 class="jx-h">🎯 Practise by unit</h2><small>${ready.length} ready</small></summary>
        ${Object.entries(SUBJ).map(([k, s0]) => { const r = s0.u.map((u, i) => uidOf(k, i)).filter(u => READY[u]); return r.length ? `<details class="jx-sub" style="--c:${s0.c}" open><summary><span>${s0.e}</span><b>${s0.n}</b><small>${r.length} units</small></summary>
          ${r.map(u => { const a = U(u).ans, n = Object.keys(a).length, ok = Object.values(a).filter(x => x.ok).length; return `<button class="jx-ur on" data-u="${u}"><span>Unit ${+u.split('-u')[1]}</span><b>${esc(unitName(u))}</b><small>${n} tried · ${ok} right</small><em>Practise ▶</em></button>`; }).join('')}</details>` : ''; }).join('')}
      </details></div>`;
    el.querySelectorAll('details.jx-sec').forEach(dd => dd.ontoggle = () => { const u = J().ui || (J().ui = {}); u[dd.dataset.sec] = dd.open; save(); });
    $('#jxToSchool').onclick = () => { tap(); J().home = false; NAVP = false; save(); toast('School mode: games and puzzles now come from your class'); practiceScreen(); };
    $('#jxQB').onclick = () => { tap('open'); bank(); };
    $('#jxCC').onclick = () => { tap('open'); crash(); };
    $('#jxPlay').onclick = () => { tap('open'); if (window.PlayHub) PlayHub.open(); };
    $('#jxMG').onclick = () => { tap('open'); if (window.MindGym) MindGym.open(); };
    $('#jxMB').onclick = () => { tap(); mistakes(); };
    $('#jxRooms').onclick = () => { tap('open'); if (window.Live && Live.open) Live.open(); };
    el.querySelectorAll('[data-u]').forEach(b => b.onclick = () => { tap('open'); NAVP = false; unit(b.dataset.u, 'prac'); });
  }
  const _practiceJ = practiceScreen;
  practiceScreen = function () { if (active()) return practiceHub(); NAVP = false; return _practiceJ.apply(this, arguments); };

  window.Jee = { home, bank, crash, practiceHub, pop, unit, setup, reopen, elig, mx, data, _run: run, active, plain, cards, arcadePool, livePool, puzzleSubjects, unitInfo, lastUnit, path: filePath, READY };
})();
