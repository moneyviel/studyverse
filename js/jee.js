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
  const READY = { 'phy-u01': { pyq: 76, prac: 912 }, 'phy-u12': { pyq: 31, prac: 366 }, 'phy-u17': { pyq: 46, prac: 552 }, 'chem-u02': { pyq: 46, prac: 552 }, 'chem-u08': { pyq: 47, prac: 564 } };
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
  function screen() {
    let s = D.getElementById('s-jee');
    if (!s) { s = D.createElement('section'); s.className = 'screen'; s.id = 's-jee'; D.querySelector('main').appendChild(s); }
    show('jee', 'world'); return s;
  }
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
    const j = J(); if (!j.track) return setup(1);
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
      <h2 class="jx-h">${j.track === 'found' ? '🌱 Foundation path' : j.track === 'main' ? `🧭 Your path — Class ${j.cls} first` : '⚡ Full syllabus — recommended order'}</h2>
      <div class="jx-path">${path(j).map(([uid, name, tag], i) => `<button class="jx-pu ${READY[uid] ? 'on' : ''}" data-u="${uid}"><span class="jx-pn">${i + 1}</span><span><b>${esc(name)}</b><small>${tag}</small></span><span class="jx-st">${READY[uid] ? 'Ready' : '🔨 Building'}</span></button>`).join('')}</div>
      <h2 class="jx-h">📚 Full JEE Main syllabus</h2>
      <div class="jx-subs">${Object.entries(SUBJ).map(([k, s]) => `<details class="jx-sub" style="--c:${s.c}"><summary><span>${s.e}</span><b>${s.n}</b><small>${s.u.length} units · ${s.u.filter((_, i) => READY[uidOf(k, i)]).length} ready</small></summary>
        ${s.u.map((u, i) => { const id = uidOf(k, i); return `<button class="jx-ur ${READY[id] ? 'on' : ''}" data-u="${id}"><span>Unit ${i + 1}</span><b>${esc(u[0])}</b><small>Class ${u[1]}</small><em>${READY[id] ? 'Ready ▶' : 'Building'}</em></button>`; }).join('')}</details>`).join('')}</div>
      <button class="jx-card jx-adv" id="jxAdv"><span>🏔️</span><span><b>JEE Advanced</b><small>Paper 1 · Paper 2 — coming soon</small></span><em>Soon</em></button>
      <div class="jx-tools"><button id="jxPat">📋 Exam pattern</button><button id="jxMist">📕 Mistake book (${j.mist.length})</button><button id="jxSchool">🏫 School world</button></div>
      <p class="jx-fine">Real questions are from JEE Main papers, tagged with date and shift; all solutions and extra questions are written by StudyVerse. Rules: NTA JEE Main 2027 Information Bulletin.</p></div>`;
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
    const el = screen(); const d = CACHE[uid]; if (!d || !ids.length) { toast('Nothing to practise here yet'); return; }
    TOP = d.topics || TOP1;
    const list = ids.map(id => d.byId[id]).filter(Boolean); let i = o.start > 0 ? o.start : 0; const S = list.map(() => ({}));
    const draw = () => {
      const q = list[i], s = S[i], num = q.n !== undefined;
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← ${esc(o.title || 'Back')}</button>
        <div class="jx-strip">${list.map((x, k) => `<button data-j="${k}" class="${k === i ? 'cur ' : ''}${S[k].done ? (S[k].ok ? 'ok' : 'no') : ''}" aria-label="Question ${k + 1}">${k + 1}</button>`).join('')}</div>
        <div class="jx-card jx-q"><div class="jx-qt"><span class="jx-tag ${q.kind}">${q.kind === 'pyq' ? '🏛️ ' + srcTag(q.src) : '🎯 StudyVerse practice'}</span><span class="jx-tag">${TOP[q.t]}${num ? ' · Numerical' : ''}</span></div>
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
      el.querySelectorAll('[data-j]').forEach(b => b.onclick = () => { i = +b.dataset.j; draw(); });
      el.querySelectorAll('.jx-o:not([disabled])').forEach(b => b.onclick = () => { tap(); s.pick = +b.dataset.k; draw(); });
      const n = $('#jxN'); if (n && !s.done) { n.oninput = () => { s.v = n.value; }; n.onkeydown = e => { if (e.key === 'Enter') check(); }; }
      const c = $('#jxCheck'); if (c) c.onclick = check;
      const st = $('#jxStep'); if (st) st.onclick = () => { tap(); s.steps = (s.steps || 1) + 1; draw(); };
      const sm = $('#jxSim'); if (sm) sm.onclick = () => {
        tap('open'); const cands = d.prac.filter(x => x.like === q.id && !list.includes(x)); if (!cands.length) return toast('You have seen all similar questions');
        list.splice(i + 1, 0, cands[Math.floor(Math.random() * cands.length)]); S.splice(i + 1, 0, {}); i++; draw();
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
    const uid = m[0].split('|')[0]; await data(uid);
    run(uid, m.filter(x => x.startsWith(uid + '|')).map(x => x.split('|')[1]), { title: 'Mistake book', back: home });
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
        <label class="jx-sl"><span>Jockey position <b>${l} cm</b></span><input type="range" min="1" max="99" step="0.5" value="${l}" id="jxL"></label>
        <label class="jx-sl"><span>Resistance box R <b>${R} Ω</b></span><input type="range" min="1" max="20" step="1" value="${R}" id="jxR"></label>
        <div class="jx-num"><input id="jxX" inputmode="decimal" placeholder="Your value of X in Ω"></div><div class="jx-nav"><button class="jx-btn" id="jxC">Check X</button><button class="jx-btn ghost" id="jxN2">New hidden X</button></div>
        <p id="jxRes"></p><p class="jx-fine">Score ${right}/${tries}. Tip: \\f{X}{R} = \\f{l}{100 − l}. Change R to bring the null point near the middle — that is where the bridge is most accurate.</p></div></div>`;
      el.querySelector('.jx-fine').innerHTML = `Score ${right}/${tries}. Tip: ${mx('\\f{X}{R} = \\f{l}{100 − l}')}. Change R to bring the null point near the middle — that is where the bridge is most accurate.`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      $('#jxL').oninput = e => { l = +e.target.value; draw(); };
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
      const R = n => 18 + n * n * 3.6;
      el.innerHTML = `<div class="jx"><button class="jx-back" id="jxBack">← Try it yourself</button><div class="jx-card"><h3>🪐 Bohr Atom Jumper</h3>
        <div class="jx-seg3">${[[1, 'H'], [2, 'He⁺'], [3, 'Li²⁺']].map(([z, n]) => `<button data-z="${z}" class="${st.Z === z ? 'on' : ''}">${n} (Z = ${z})</button>`).join('')}</div>
        <p class="jx-p">Electron is in <b>n = ${st.n}</b> (E = ${(-13.6 * st.Z * st.Z / st.n / st.n).toFixed(2)} eV). Tap an orbit to jump there — up absorbs, down emits.</p>
        <svg viewBox="0 0 320 320" class="jx-circ" id="jxAtom">${[6, 5, 4, 3, 2, 1].map(n => `<circle cx="160" cy="160" r="${R(n)}" fill="none" stroke="${n === st.n ? '#7c3aed' : '#c4b5fd'}" stroke-width="${n === st.n ? 3 : 1.5}" data-n="${n}" style="cursor:pointer"/><text x="${160 + R(n) * 0.71 + 3}" y="${160 - R(n) * 0.71}" font-size="10" fill="#6b6795">n=${n}</text>`).join('')}
          <circle cx="160" cy="160" r="${6 + st.Z * 2}" fill="#dc2626"/><text x="160" y="164" text-anchor="middle" font-size="10" fill="#fff">+${st.Z}</text>
          <circle r="7" fill="#2563eb"><animateMotion dur="${(1 + st.n * 0.6).toFixed(1)}s" repeatCount="indefinite" path="M${160 + R(st.n)} 160 a${R(st.n)} ${R(st.n)} 0 1 1 -${2 * R(st.n)} 0 a${R(st.n)} ${R(st.n)} 0 1 1 ${2 * R(st.n)} 0"/></circle>
          ${st.last ? `<path d="M160 ${160 - R(st.last.from)} q 30 -10 60 0 t 60 0 t 60 0" stroke="${lamColor(st.last.lam)}" stroke-width="3" fill="none"/>` : ''}</svg>
        <div class="jx-nav"><button class="jx-btn ghost" id="jxIon">Ionise (n → ∞)</button></div>
        <div class="jx-read">${st.last ? `<span>Photon <b>${st.last.E.toFixed(2)} eV</b></span><span>λ <b>${st.last.lam.toFixed(1)} nm</b></span><span>Series <b>${SER[st.last.to] || '—'}</b></span><span>${st.last.lam < 380 ? 'UV' : st.last.lam <= 750 ? 'visible' : 'IR'}</span>` : '<span>Jump down to see a photon</span>'}</div>
        <h3 style="margin-top:10px">🧾 Lines you made</h3><div class="jx-p">${st.log.slice(-8).map(l => `<span class="jx-tag" style="background:${lamColor(l.lam)};color:#fff">${['', 'H', 'He⁺', 'Li²⁺'][l.Z]} ${l.from}→${l.to} · ${l.lam.toFixed(0)} nm</span>`).join(' ') || '—'}</div>
        <h3 style="margin-top:10px">🎯 Missions</h3><div>${MIS.map(([k, n2]) => `<div class="jx-mis ${done['bo_' + k] ? 'ok' : ''}">${done['bo_' + k] ? '✅' : '⬜'} ${n2}</div>`).join('')}</div></div></div>`;
      $('#jxBack').onclick = () => unit(uid, 'lab');
      el.querySelectorAll('[data-z]').forEach(b => b.onclick = () => { tap(); st.Z = +b.dataset.z; st.n = 1; st.last = null; st.ion = false; draw(); });
      el.querySelectorAll('[data-n]').forEach(c2 => c2.onclick = () => {
        const to = +c2.dataset.n; if (to === st.n) return; st.ion = false;
        if (to < st.n) { const lam = lamOf(st.Z, st.n, to); st.last = { from: st.n, to, lam, E: 1239.84 / lam, Z: st.Z }; st.log.push(st.last); tap('correct'); } else { st.last = null; tap(); }
        st.n = to; mark(); draw();
      });
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

  function reopen(v, ...a) { try { ({ home, unit, setup: () => setup(1, { again: true }), pattern, adv: advanced })[v](...a); } catch (e) { home(); } }

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
.jx-figw{margin:10px 0;text-align:center}.jx-figw svg{max-width:340px;width:100%;height:auto;color:#1e1b4b}.jx-circ{width:100%;max-width:420px;height:auto;display:block;margin:6px auto}.jx-curve{width:100%;height:auto}
  .jx-seg3{display:flex;gap:6px;margin:6px 0}.jx-seg3 button{flex:1 1 28%;border:1px solid #d9d2ff;background:#f7f5ff;border-radius:10px;padding:8px 4px;font:inherit;font-size:12.5px;font-weight:700;cursor:pointer;color:#4c1d95}.jx-seg3 .on{background:#4c1d95;color:#fff}
  .jx-read{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.jx-read span{background:#1e1b4b;color:#ddd6fe;border-radius:10px;padding:5px 8px;font-size:12px}.jx-read b{color:#fff}
  .jx-sl{display:block;margin:8px 0;font-size:13px;font-weight:700;color:#3b2a85}.jx-sl span{display:flex;justify-content:space-between}.jx-sl input{width:100%;accent-color:#7c3aed}
  .jx-mis{padding:7px 10px;border-radius:10px;background:#f7f5ff;margin:5px 0;font-size:13.5px}.jx-mis.ok{background:#dcfce7}
  .jx-qn{display:flex;gap:8px;align-items:center;font-weight:700;margin:6px 0}.jx-qn select{padding:6px;border-radius:8px;border:1px solid #d9d2ff}
  .jx-boxes{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.jx-sub2{text-align:center;cursor:pointer}.jx-sub2 small{display:block;font-weight:800;color:#5b21b6}.jx-sub2 div{display:flex}.jx-sub2 span{width:24px;height:26px;border:1.5px solid #7c3aed;display:grid;place-items:center;font-weight:900;font-size:13px;margin-left:-1.5px;background:#fff}
    .jx-tile0{background:linear-gradient(135deg,#6d28d9,#db2777)!important;color:#fff!important;margin-bottom:10px}.jx-tile0 small{color:#fce7f3!important}
  html[data-theme=dark] .jx{color:#ece9ff}html[data-theme=dark] .jx-card,html[data-theme=dark] .jx-step,html[data-theme=dark] .jx-pu,html[data-theme=dark] .jx-sub,html[data-theme=dark] .jx-li,html[data-theme=dark] .jx-tile,html[data-theme=dark] .jx-o,html[data-theme=dark] .jx-tools button{background:#1d1a3a;border-color:#2f2a5c;color:#ece9ff}
  </style>`);

  window.Jee = { home, unit, setup, reopen, elig, mx, data, _run: run };
})();
