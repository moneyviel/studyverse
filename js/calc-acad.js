/* ================= Calculator Academy — a free bonus course =================
   Teaches the desk (Basic), Scientific and Financial calculator in short missions. Each step asks the student to press
   the REAL keys of the on-screen calculator (js/calc.js); the mission follows the key presses through Calc.on() and moves
   on by itself when the right result appears. A coach strip inside the calculator panel shows the current step.
   - Levels: school students get Basic always, Scientific from Class 8, Financial from Class 11; CA students get all.
   - Spot-the-mistake quizzes, a 60-second "Beat the clock" round, badges, XP through addXP(), a progress bar and a
     certificate (image + text to share) when every mission open to the student is done.
   - Free: never counts toward the daily free-question limit (answer buttons are .cxa-opt, never button.opt[data-k]).
   - Entry points: a tile on World (above Brain Snacks) and CA Journey (after Brain Snacks / the plan bar), a card on
     school Me and CA Profile, and the 🎓 Learn button in the calculator.
   Content: js/calc-acad-data.js (window.CXA_DATA). Progress: ST.calcAcad = { m: {id: {s: stars, d, n}}, b: {badge: date}, best, cert }.
   window.CalcAcademy = { open, mission, badgeCount, progress } */
(function () {
  const D = document, X = window.CXA_DATA;
  if (!X) return;
  const tap = k => { try { sfx(k); } catch (e) {} };
  const say = m => { try { if (window.A11Y && A11Y.announce) A11Y.announce(m); } catch (e) {} };
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const A = () => { ST.calcAcad = ST.calcAcad || {}; const a = ST.calcAcad; a.m = a.m || {}; a.b = a.b || {}; a.best = a.best || 0; return a; };
  const P = () => (typeof ST !== 'undefined' && ST.profile) || {};
  const isCA = () => P().course === 'ca';
  const parent = () => { try { return !!(window.Cloud && Cloud.isParent && Cloud.isParent()); } catch (e) { return false; } };
  const levelOf = id => X.levels.find(l => l.id === id);
  const levelOpen = L => isCA() || (+P().grade || 0) >= L.minGrade;
  const mine = () => X.missions.filter(m => levelOpen(levelOf(m.level)));
  const isDone = m => !!A().m[m.id];
  function progress() { const ms = mine(), d = ms.filter(isDone).length; return { done: d, all: ms.length, pct: ms.length ? Math.round(d / ms.length * 100) : 0 }; }
  /* only the badges this student can win (their open levels) + the graduate badge */
  const avail = () => { const s = new Set(mine().map(m => m.badge).filter(Boolean)); s.add('grad'); return Object.keys(X.badges).filter(b => s.has(b) || A().b[b]); };
  function badgeCount() { const ids = avail(); return { have: ids.filter(b => A().b[b]).length, all: ids.length }; }
  const near = (a, b, tol) => typeof a === 'number' && isFinite(a) && Math.abs(a - b) <= (tol == null ? Math.max(1e-9, Math.abs(b) * 1e-9) : tol + 1e-12);
  const fmtN = v => (window.Calc && Calc.math ? (Math.abs(v) >= 1e12 || (v && Math.abs(v) < 1e-6) ? Calc.math.sciFmt(v) : Calc.math.fmt(v)) : String(v));
  const shuffle = a => (window.Games ? Games.shuffle(a) : a.slice().sort(() => Math.random() - .5));

  /* ---------- screen ---------- */
  function screen() {
    let s = D.getElementById('s-cxa');
    if (!s) { s = D.createElement('section'); s.className = 'screen'; s.id = 's-cxa'; D.querySelector('main').appendChild(s);
      new MutationObserver(() => { if (!s.classList.contains('active')) stop(); }).observe(s, { attributes: true, attributeFilter: ['class'] }); }
    return s;
  }
  let FROM = 'world';
  function goBack() { stop(); FROM === 'me' ? meScreen() : worldScreen(); }
  function open(o = {}) {
    stop(); style();
    if (o.from) FROM = o.from; else if (!o.keep) FROM = D.querySelector('nav button.on')?.dataset.s === 'me' ? 'me' : 'world';
    const el = screen(); show('cxa', FROM);
    const pr = progress(), bc = badgeCount(), ms = mine();
    el.innerHTML = `<button class="back" id="cxaBack">← ${FROM === 'me' ? (isCA() ? 'Profile' : 'Me') : 'Home'}</button>
      <div class="hello" role="heading" aria-level="1"><span aria-hidden="true">🧮</span> Calculator Academy <small>Free bonus · press real keys to learn</small></div>
      <div class="card cxa-hero"><div class="cxa-ptop"><b>${pr.done} of ${pr.all} missions</b><span>${pr.pct}%</span></div>
        <div class="cxa-bar" role="progressbar" aria-label="Academy progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pr.pct}"><i style="width:${pr.pct}%"></i></div>
        <p class="sub">Every mission uses the real calculator. Do each step and it ticks itself. No questions are counted from your daily free limit.</p>
        <h3 class="cxa-h3">Badges · ${bc.have} of ${bc.all}</h3>
        <div class="cxa-badges">${avail().map(id => [id, X.badges[id]]).map(([id, [e, n]]) => `<span class="cxa-bdg ${A().b[id] ? 'on' : ''}" title="${E(n)}"><b aria-hidden="true">${e}</b><small>${E(n)}</small><span class="sr-only">${A().b[id] ? 'earned' : 'not yet'}</span></span>`).join('')}</div>
        <button class="btn ghost" type="button" id="cxaCalc">🧮 Open the calculator to play freely</button></div>
      ${X.levels.map(L => { const open_ = levelOpen(L), list = X.missions.filter(m => m.level === L.id); const d = list.filter(isDone).length;
        return `<div class="card cxa-level ${open_ ? '' : 'locked'}"><h2><span aria-hidden="true">${L.emoji}</span> ${E(L.name)} <small>${open_ ? `${d} / ${list.length}` : `Opens in Class ${L.minGrade}`}</small></h2><p class="sub">${E(L.blurb)}</p>
          ${open_ ? `<div class="cxa-ms">${list.map(m => { const r = A().m[m.id]; return `<button class="cxa-m ${r ? 'done' : ''}" type="button" data-m="${m.id}" aria-label="${E(m.title)}${r ? `, done, ${r.s} of 3 stars` : ''}">
            <span class="cxa-me" aria-hidden="true">${m.emoji}</span><span class="cxa-mt"><b>${E(m.title)}</b><small>${m.kind === 'speed' ? '60-second speed round' : m.kind === 'spot' ? `${m.steps.length} puzzles` : `${m.steps.length} steps`}${m.badge ? ` · ${X.badges[m.badge][0]} badge` : ''}</small></span>
            <span class="cxa-st" aria-hidden="true">${r ? '★'.repeat(r.s) + '☆'.repeat(3 - r.s) : '▶'}</span></button>`; }).join('')}</div>` : `<p class="cxa-lock"><span aria-hidden="true">🔒</span> Unlocks when you are in Class ${L.minGrade} or above.</p>`}</div>`; }).join('')}
      <div class="card cxa-certc"><h2><span aria-hidden="true">🎓</span> Your certificate</h2>
        ${pr.done >= pr.all && pr.all ? `<p class="sub">You finished every mission. Well done!</p><button class="btn" type="button" id="cxaCert">🎓 Get my certificate</button>` : `<p class="sub">Finish all ${pr.all} missions to unlock it — ${pr.all - pr.done} to go.</p>`}</div>`;
    el.querySelector('#cxaBack').onclick = () => { tap('tap'); goBack(); };
    el.querySelector('#cxaCalc').onclick = () => Calc.open();
    el.querySelectorAll('[data-m]').forEach(b => b.onclick = () => { tap('open'); mission(b.dataset.m); });
    const c = el.querySelector('#cxaCert'); if (c) c.onclick = cert;
    window.scrollTo(0, 0);
  }

  /* ---------- a mission ---------- */
  let R = null, off = null, timer = 0;
  function stop() {
    if (off) { off(); off = null; } clearInterval(timer); timer = 0;
    if (R && window.Calc) { Calc.coach(null); Calc.hint([]); }
    R = null;
  }
  const cur = () => R && R.m.steps[R.i];
  const keyStep = s => s && !['info', 'quiz'].includes(s.do);
  function mission(id) {
    stop(); style();
    const m = X.missions.find(x => x.id === id); if (!m) return open({ keep: true });
    const el = screen(); if (!el.classList.contains('active')) show('cxa', FROM);
    if (m.kind === 'speed') return speed(m);
    R = { m, i: 0, misses: 0, hints: 0, quizWrong: 0, fresh: !isDone(m), msg: '', bad: false };
    if (m.kind !== 'spot') {
      Calc.reset();
      const firstKey = m.steps.find(keyStep);
      if (firstKey && firstKey.do === 'mode') Calc.setMode('basic'); else if (m.mode) Calc.setMode(m.mode);
      off = Calc.on(onEv);
    }
    render();
  }
  function render() {
    if (!R) return;
    const el = screen(), m = R.m, s = cur(), n = m.steps.length;
    const quizHTML = s && s.do === 'quiz' ? quizBox(s) : '';
    el.innerHTML = `<button class="back" id="cxaHome">← Calculator Academy</button>
      <div class="hello cxa-mh"><span aria-hidden="true">${m.emoji}</span> ${E(m.title)}</div>
      <div class="card cxa-story"><p>${E(m.story)}</p><div class="cxa-bar" role="progressbar" aria-label="Mission progress" aria-valuemin="0" aria-valuemax="${n}" aria-valuenow="${R.i}"><i style="width:${R.i / n * 100}%"></i></div></div>
      <div class="card cxa-step" id="cxaStep"><span class="tag">Step ${R.i + 1} of ${n}</span>
        ${s.do === 'quiz' ? quizHTML : `<p class="cxa-say">${E(s.say)}</p>`}
        <div id="cxaMsg" class="cxa-msg ${R.bad ? 'bad' : ''}" role="status" aria-live="polite">${R.msg ? E(R.msg) : ''}</div>
        ${s.do === 'info' ? '<button class="btn mint" type="button" id="cxaNext">Got it ▶</button>' : ''}
        ${keyStep(s) ? `<div class="cxa-row"><button class="btn ghost" type="button" id="cxaHint"><span aria-hidden="true">💡</span> Hint</button><button class="btn ghost" type="button" id="cxaOpen"><span aria-hidden="true">🧮</span> Show calculator</button></div>` : ''}</div>
      <ol class="card cxa-steps" aria-label="Steps">${m.steps.map((x, j) => `<li class="${j < R.i ? 'ok' : j === R.i ? 'now' : ''}"><span aria-hidden="true">${j < R.i ? '✅' : j === R.i ? '👉' : '•'}</span> ${E(x.do === 'quiz' ? 'Spot the mistake: ' + x.q : x.say)}${j < R.i ? '<span class="sr-only"> (done)</span>' : ''}</li>`).join('')}</ol>`;
    el.querySelector('#cxaHome').onclick = () => { tap('tap'); open({ keep: true }); };
    const nx = el.querySelector('#cxaNext'); if (nx) nx.onclick = () => advance();
    const hb = el.querySelector('#cxaHint'); if (hb) hb.onclick = () => giveHint();
    const ob = el.querySelector('#cxaOpen'); if (ob) ob.onclick = () => { Calc.open(); coach(); };
    if (s.do === 'quiz') wireQuiz(el, s);
    if (keyStep(s)) { Calc.open(); coach(); autoPass(s); }
    else if (window.Calc) { Calc.close(); Calc.coach(null); Calc.hint([]); }
    window.scrollTo(0, 0);
  }
  function giveHint() { const s = cur(); if (!R || !keyStep(s)) return; R.hints++; R.msg = s.hint || 'Look for the glowing keys on the calculator.'; R.bad = false; Calc.open(); Calc.hint(s.hl || []); render(); }
  function coach(extra) {
    if (!R) return; const s = cur(); if (!s || !keyStep(s)) return;
    const showSay = R.msg && !extra;
    const c = Calc.coach(`<div class="cxc-top"><span>${R.m.emoji} ${E(R.m.title)}</span><span>Step ${R.i + 1}/${R.m.steps.length}</span></div><div>${E(extra || s.say)}</div>${showSay ? `<div class="cxc-msg">${E(R.msg)}</div>` : ''}${extra ? '' : '<button type="button" class="cxc-hint" id="cxcHint"><span aria-hidden="true">💡</span> Hint</button>'}`);
    c.classList.toggle('cx-bad', !!R.bad && !extra); c.classList.toggle('cx-good', !!extra);
    const h = c.querySelector('#cxcHint'); if (h) h.onclick = giveHint;
  }
  /* a step that is already true (the calculator is already in that mode / angle) passes by itself */
  function autoPass(s) {
    let st; try { st = Calc.state(); } catch (e) { return; }
    if ((s.do === 'mode' && st.mode === s.mode) || (s.do === 'angle' && st.angle === s.unit) || (s.do === 'tool' && st.mode === 'fin' && st.tool === s.tool)) setTimeout(() => { if (R && cur() === s) passed(); }, 450);
    else if (s.do === 'tool' && st.mode !== 'fin') Calc.setMode('fin');
    else if (s.do === 'fin' && st.mode !== 'fin') Calc.setMode('fin');
  }
  function pass(s, ev) {
    switch (s.do) {
      case 'press': return ev.type === 'key' && s.keys.includes(ev.k) && (!s.mode || ev.mode === s.mode);
      case 'result': return ev.type === 'key' && ev.done && (!s.keys || s.keys.includes(ev.k)) && near(ev.value, s.value, s.tol);
      case 'value': return ev.type === 'key' && (!s.keys || s.keys.includes(ev.k)) && near(ev.value, s.value, s.tol);
      case 'mem': return ev.type === 'key' && ev.mode === 'basic' && near(ev.mem, s.value, s.tol);
      case 'mode': return ev.type === 'mode' && ev.mode === s.mode;
      case 'angle': return ev.type === 'key' && ev.k === 'angle' && ev.angle === s.unit;
      case 'tool': return ev.type === 'tool' && ev.tool === s.tool;
      case 'fin': return ev.type === 'fin' && ev.tool === s.tool && (!s.solve || ev.solve === s.solve) && near(ev.value, s.value, s.tol);
    }
    return false;
  }
  /* a finished attempt that is not right → a gentle nudge (and sometimes a rewind) */
  function miss(s, ev) {
    if (s.do === 'result' && ev.type === 'key' && ev.done && (!s.keys || s.keys.includes(ev.k))) return isFinite(ev.value) ? `Not yet — the calculator shows ${fmtN(ev.value)}. Press AC and try again.` : 'Oops, Error. Press AC and try again.';
    if (s.do === 'mem' && ev.type === 'key' && (ev.k === 'M+' || ev.k === 'M-')) return `Memory now holds ${fmtN(ev.mem)}, not ${fmtN(s.value)}. Press MC to empty it and the mission goes back to the first memory step.`;
    if (s.do === 'fin' && ev.type === 'fin' && ev.tool === s.tool && isFinite(ev.value)) return `You got ${Calc.math.fmt2(ev.value)}. Check the numbers you typed (and the signs), then try again.`;
    if (s.do === 'fin' && ev.type === 'fin' && ev.tool !== s.tool) return 'That was a different tool. Pick the one with the glowing button.';
    return '';
  }
  function onEv(ev) {
    if (!R || R.wait) return; const s = cur(); if (!s || !keyStep(s)) return;
    if (!D.getElementById('s-cxa')?.classList.contains('active')) { stop(); return; }
    if (pass(s, ev)) return passed();
    /* memory went wrong and the student pressed MC: start the memory part again */
    if (ev.type === 'key' && ev.k === 'MC' && s.do === 'mem') { const first = R.m.steps.findIndex(x => x.do === 'mem'); if (first >= 0 && first < R.i) { R.i = first; R.msg = 'Memory is empty. Let us do the memory steps again.'; R.bad = false; render(); return; } }
    const m = miss(s, ev);
    if (m) { R.misses++; R.msg = m; R.bad = true; tap('wrong');
      if (s.rewind != null && R.i > s.rewind) { R.i = s.rewind; R.msg = m.replace('Press AC and try again.', '') + ' GT is empty again — type the bills once more.'; }
      Calc.hint(s.hl || []); render(); }
  }
  function passed() {
    if (!R || R.wait) return; const s = cur(); R.wait = true;
    tap('correct'); R.paid = R.paid || {}; if (R.fresh && !R.paid[R.i]) { R.paid[R.i] = 1; try { addXP(2); } catch (e) {} }
    coach('✅ Nice! ' + (R.i + 1 < R.m.steps.length ? 'Next step…' : 'Mission complete!'));
    say('Correct!');
    const at = R.i; setTimeout(() => { if (R && R.i === at) advance(); }, 650);
  }
  function advance() { if (!R) return; R.wait = false; R.i++; R.msg = ''; R.bad = false; Calc.hint([]); if (R.i >= R.m.steps.length) finish(); else render(); }

  /* ---------- quiz (spot the mistake) — .cxa-opt buttons: never counted as daily free questions ---------- */
  function quizBox(s) {
    if (!R.order || R.orderFor !== R.i) { R.order = shuffle(s.opts.map((o, k) => k)); R.orderFor = R.i; R.ans = null; }
    return `<h2 class="cxa-q"><span aria-hidden="true">🔍</span> ${E(s.q)}</h2><div class="cxa-opts" role="group" aria-label="Choose the answer">${R.order.map(k => `<button type="button" class="cxa-opt ${R.ans != null ? (k === 0 ? 'right' : k === R.ans ? 'wrong' : '') : ''}" data-i="${k}" ${R.ans != null ? 'disabled' : ''}>${E(s.opts[k])}</button>`).join('')}</div>
      ${R.ans != null ? `<div class="explain ${R.ans === 0 ? 'good' : 'bad'}"><div class="verdict">${R.ans === 0 ? '🎉 Correct!' : '🤔 Not quite.'}</div><div class="why">${E(s.why)}</div></div><button class="btn mint" type="button" id="cxaQn">${R.i + 1 < R.m.steps.length ? 'Next ▶' : 'Finish ▶'}</button>` : ''}`;
  }
  function wireQuiz(el, s) {
    el.querySelectorAll('.cxa-opt').forEach(b => b.onclick = () => {
      if (R.ans != null) return; R.ans = +b.dataset.i;
      if (R.ans === 0) { tap('correct'); if (R.fresh) try { addXP(3); } catch (e) {} } else { tap('wrong'); R.misses++; R.quizWrong++; }
      render(); const q = D.getElementById('cxaQn'); if (q) q.focus();
    });
    const q = el.querySelector('#cxaQn'); if (q) q.onclick = () => { R.order = null; advance(); };
  }

  function award(id) {
    const a = A(); if (!id || a.b[id] || !X.badges[id]) return false;
    a.b[id] = today(); save(); const [e, n] = X.badges[id];
    setTimeout(() => { try { addXP(10, `New badge: ${e} ${n}`); tap('unlock'); } catch (x) {} }, 1300);
    return true;
  }
  function finish() {
    const m = R.m, a = A(), prev = a.m[m.id], qw = R.quizWrong, stars = R.misses + R.hints === 0 ? 3 : R.misses + R.hints <= 2 ? 2 : 1;
    a.m[m.id] = { s: Math.max(prev ? prev.s : 0, stars), d: today(), n: (prev ? prev.n : 0) + 1 }; save();
    try { addXP(prev ? 3 : 10, 'Mission complete!'); bumpStreak(); } catch (e) {}
    const got = m.kind === 'spot' ? (qw === 0 ? award(m.badge) : false) : award(m.badge);
    stop(); tap('unlock');
    const next = mine().find(x => !isDone(x)), pr = progress(), el = screen();
    el.innerHTML = `<button class="back" id="cxaHome">← Calculator Academy</button>
      <div class="card done-card cxa-done"><div class="confetti">${Array.from({ length: 14 }, (_, j) => `<span style="left:${(j * 7.3 + 3) % 100}%;animation-delay:${(j % 5) * .15}s">${['🎉', '⭐', '✨', '🧮'][j % 4]}</span>`).join('')}</div>
        <div class="gbig" aria-hidden="true">${m.emoji}</div><h2>Mission complete!</h2>
        <div class="bigstars" aria-label="${stars} of 3 stars">${[0, 1, 2].map(i => `<span class="${i < stars ? 'on' : ''}" style="animation-delay:${i * .25}s" aria-hidden="true">⭐</span>`).join('')}</div>
        <p class="sub">${E(m.done)}</p>
        ${got ? `<p class="cxa-newb"><span aria-hidden="true">${X.badges[m.badge][0]}</span> New badge: <b>${E(X.badges[m.badge][1])}</b></p>` : ''}
        ${m.kind === 'spot' && qw ? '<p class="sub">Get every puzzle right first time to win the 🔍 badge. Try again any time!</p>' : ''}
        <p class="sub">${pr.done} of ${pr.all} missions done · +${prev ? 3 : 10} ⭐${prev ? '' : ' (plus 2 for each step)'}</p>
        ${pr.done >= pr.all ? '<button class="btn" type="button" id="cxaCert">🎓 Get my certificate</button><div style="height:8px"></div>' : next ? `<button class="btn" type="button" id="cxaNextM">Next: ${E(next.title)} ▶</button><div style="height:8px"></div>` : ''}
        <button class="btn ghost" type="button" id="cxaAgain">Play again</button></div>`;
    el.querySelector('#cxaHome').onclick = () => open({ keep: true });
    el.querySelector('#cxaAgain').onclick = () => mission(m.id);
    const nb = el.querySelector('#cxaNextM'); if (nb) nb.onclick = () => mission(next.id);
    const cb = el.querySelector('#cxaCert'); if (cb) cb.onclick = cert;
    if (window.Calc) Calc.close();
    window.scrollTo(0, 0);
  }

  /* ---------- Beat the clock ---------- */
  function problem() {
    const g = isCA() ? 12 : (+P().grade || 6), r = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
    const kinds = g < 5 ? ['add2', 'mul1'] : ['mul', 'add3', 'pct', 'mul'];
    const k = kinds[r(0, kinds.length - 1)];
    if (k === 'add2') { const a = r(12, 99), b = r(12, 99); return { t: `${a} + ${b}`, v: a + b }; }
    if (k === 'mul1') { const a = r(12, 99), b = r(2, 9); return { t: `${a} × ${b}`, v: a * b }; }
    if (k === 'mul') { const a = r(12, 99), b = r(12, 99); return { t: `${a} × ${b}`, v: a * b }; }
    if (k === 'add3') { const a = r(105, 999), b = r(105, 999), c = r(105, 999); return { t: `${a} + ${b} + ${c}`, v: a + b + c }; }
    const p = [5, 10, 12, 15, 18, 20, 25][r(0, 6)], b = r(2, 40) * 100; return { t: `${p}% of ${b.toLocaleString('en-IN')}`, v: b * p / 100, tip: `${b} × ${p} %` };
  }
  function speed(m) {
    const el = screen(), secs0 = (() => { const sc = window.A11Y && A11Y.timeScale ? A11Y.timeScale() : 1; return sc ? Math.round(60 * sc) : 0; })();
    R = { m, i: 0, misses: 0, hints: 0, quizWrong: 0, fresh: !isDone(m), score: 0, n: 0, q: null, left: secs0, timed: !!secs0, started: false };
    el.innerHTML = `<button class="back" id="cxaHome">← Calculator Academy</button>
      <div class="hello cxa-mh"><span aria-hidden="true">⚡</span> Beat the clock</div>
      <div class="card cxa-story"><p>${E(m.story)}</p><p class="sub">${secs0 ? `You have ${secs0} seconds.` : 'No timer for you: answer 10 sums at your own pace.'} Best so far: <b>${A().best}</b>. Get 6 or more for the ⚡ Speed Demon badge.</p>
        <button class="btn" type="button" id="cxaGo">Ready? Start ▶</button></div>
      <div class="card cxa-speed" id="cxaSp" hidden><div class="cxa-sptop"><span>Score <b id="cxaSc">0</b></span><span id="cxaT" aria-live="off">${secs0 ? secs0 + ' s' : '1 / 10'}</span></div>
        <p class="cxa-prob" id="cxaPr" aria-live="polite"></p><p class="sub" id="cxaTip"></p><button class="btn ghost" type="button" id="cxaSkip">Skip this one</button></div>`;
    el.querySelector('#cxaHome').onclick = () => open({ keep: true });
    el.querySelector('#cxaGo').onclick = () => {
      el.querySelector('#cxaGo').closest('.card').hidden = true; el.querySelector('#cxaSp').hidden = false;
      Calc.reset(); Calc.setMode('basic'); Calc.open(); R.started = true; nextQ();
      off = Calc.on(ev => { if (!R || !R.q) return; if (ev.type === 'key' && ev.done && near(ev.value, R.q.v, 1e-6)) { R.score++; tap('coin'); el.querySelector('#cxaSc').textContent = R.score; nextQ(true); } });
      if (R.timed) timer = setInterval(() => { if (!R) return; R.left--; const t = el.querySelector('#cxaT'); if (t) t.textContent = R.left + ' s'; if (R.left <= 0) endSpeed(); }, 1000);
    };
    el.querySelector('#cxaSkip').onclick = () => nextQ(false);
  }
  function nextQ(right) {
    if (!R) return; const el = screen();
    if (R.q) R.n++;
    if (!R.timed && R.n >= 10) return endSpeed();
    R.q = problem();
    el.querySelector('#cxaPr').textContent = R.q.t + ' = ?';
    el.querySelector('#cxaTip').textContent = R.q.tip ? `Tip: type ${R.q.tip}` : 'Type it on the calculator and press =';
    if (!R.timed) el.querySelector('#cxaT').textContent = `${R.n + 1} / 10`;
    Calc.coach(`<div class="cxc-top"><span>⚡ Beat the clock</span><span>Score ${R.score}</span></div><div><b style="font-size:20px">${E(R.q.t)} = ?</b>${right ? ' ✅' : ''}</div>`);
  }
  function endSpeed() {
    if (!R) return; const m = R.m, score = R.score, a = A(), best = score > a.best; if (best) a.best = score;
    const okDone = R.timed ? score >= 3 : true, stars = score >= 8 ? 3 : score >= 5 ? 2 : 1, prev = a.m[m.id];
    if (okDone) a.m[m.id] = { s: Math.max(prev ? prev.s : 0, stars), d: today(), n: (prev ? prev.n : 0) + 1 };
    save();
    try { if (score) addXP(score * 3, 'Speed round!'); if (okDone) bumpStreak(); } catch (e) {}
    const got = (R.timed ? score >= 6 : score >= 8) ? award('speed') : false;
    stop(); Calc.close(); tap('unlock');
    const el = screen();
    el.innerHTML = `<button class="back" id="cxaHome">← Calculator Academy</button>
      <div class="card done-card cxa-done"><div class="gbig" aria-hidden="true">⚡</div><h2>${score} right!</h2>
        <p class="sub">${best ? '🏆 New best score!' : `Your best: ${a.best}`} · +${score * 3} ⭐</p>
        ${got ? `<p class="cxa-newb"><span aria-hidden="true">⚡</span> New badge: <b>Speed Demon</b></p>` : ''}
        ${okDone ? '' : '<p class="sub">Get at least 3 to complete this mission.</p>'}
        <button class="btn" type="button" id="cxaAgain">Play again ▶</button><div style="height:8px"></div><button class="btn ghost" type="button" id="cxaBackH">Back to the academy</button></div>`;
    el.querySelector('#cxaHome').onclick = el.querySelector('#cxaBackH').onclick = () => open({ keep: true });
    el.querySelector('#cxaAgain').onclick = () => mission(m.id);
  }

  /* ---------- certificate ---------- */
  function cert() {
    stop(); const pr = progress(); if (pr.done < pr.all) return open({ keep: true });
    const a = A(); if (!a.cert) { a.cert = today(); save(); }
    award('grad');
    const el = screen(), name = (P().name || 'Student').trim(), dt = new Date(a.cert + 'T00:00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
    const lv = X.levels.filter(levelOpen).map(L => L.name), bc = badgeCount();
    const text = `🎓 ${name} completed Calculator Academy on StudyVerse — ${pr.all} missions (${lv.join(', ')}) and ${bc.have} badges. ${dt}. study.moneyviel.com`;
    const cv = D.createElement('canvas'); cv.width = 1200; cv.height = 850; draw(cv, name, dt, pr.all, lv, Object.keys(X.badges).filter(b => a.b[b]).map(b => X.badges[b][0]));
    let url = ''; try { url = cv.toDataURL('image/png'); } catch (e) {}
    el.innerHTML = `<button class="back" id="cxaHome">← Calculator Academy</button>
      <div class="hello cxa-mh"><span aria-hidden="true">🎓</span> Your certificate</div>
      <div class="card cxa-cert">${url ? `<img src="${url}" alt="Certificate: ${E(name)} completed Calculator Academy, ${pr.all} missions, ${dt}" class="cxa-img">` : ''}
        <p class="sub" id="cxaCtext">${E(text)}</p>
        <div class="cxa-row"><button class="btn" type="button" id="cxaShare">📤 Share</button><button class="btn ghost" type="button" id="cxaDl">⬇️ Save image</button></div>
        <div style="height:8px"></div><button class="btn ghost" type="button" id="cxaCopy">📋 Copy text</button></div>`;
    el.querySelector('#cxaHome').onclick = () => open({ keep: true });
    const save_ = () => { const l = D.createElement('a'); l.href = url; l.download = `StudyVerse-Calculator-Academy-${name.replace(/\W+/g, '-')}.png`; D.body.appendChild(l); l.click(); l.remove(); };
    el.querySelector('#cxaDl').onclick = save_;
    el.querySelector('#cxaCopy').onclick = () => copy(text);
    el.querySelector('#cxaShare').onclick = () => {
      cv.toBlob(async b => {
        try { const f = new File([b], 'calculator-academy-certificate.png', { type: 'image/png' });
          if (navigator.canShare && navigator.canShare({ files: [f] })) { await navigator.share({ files: [f], title: 'My Calculator Academy certificate', text }); return; }
          if (navigator.share) { await navigator.share({ title: 'StudyVerse', text }); return; } } catch (e) { if (e && e.name === 'AbortError') return; }
        copy(text); save_();
      }, 'image/png');
    };
    tap('unlock'); window.scrollTo(0, 0);
  }
  async function copy(t) {
    try { await navigator.clipboard.writeText(t); toast('📋 Copied! Paste it to share.'); }
    catch (e) { const x = D.createElement('textarea'); x.value = t; x.setAttribute('readonly', ''); x.style.position = 'fixed'; x.style.opacity = '0'; D.body.appendChild(x); x.select(); try { D.execCommand('copy'); toast('📋 Copied! Paste it to share.'); } catch (e2) { toast('Could not copy on this phone'); } x.remove(); }
  }
  function draw(cv, name, dt, n, levels, badges) {
    const c = cv.getContext('2d'), W = cv.width, H = cv.height;
    c.fillStyle = '#FFFDF6'; c.fillRect(0, 0, W, H);
    c.strokeStyle = '#C9A76A'; c.lineWidth = 14; c.strokeRect(28, 28, W - 56, H - 56); c.lineWidth = 3; c.strokeRect(52, 52, W - 104, H - 104);
    c.textAlign = 'center'; c.fillStyle = '#8A6A2E'; c.font = '700 30px Nunito, Arial, sans-serif'; c.fillText('STUDYVERSE · CALCULATOR ACADEMY', W / 2, 135);
    c.fillStyle = '#15161C'; c.font = '800 66px "Baloo 2", Georgia, serif'; c.fillText('Certificate of Achievement', W / 2, 225);
    c.font = '400 30px Nunito, Arial, sans-serif'; c.fillStyle = '#575B66'; c.fillText('This is to certify that', W / 2, 300);
    c.fillStyle = '#5B0F1B'; let fs = 76; c.font = `800 ${fs}px "Baloo 2", Georgia, serif`; while (c.measureText(name).width > W - 260 && fs > 36) { fs -= 4; c.font = `800 ${fs}px "Baloo 2", Georgia, serif`; } c.fillText(name, W / 2, 390);
    c.strokeStyle = '#C9A76A'; c.lineWidth = 2; c.beginPath(); c.moveTo(W / 2 - 300, 412); c.lineTo(W / 2 + 300, 412); c.stroke();
    c.fillStyle = '#15161C'; c.font = '600 30px Nunito, Arial, sans-serif'; c.fillText(`has completed all ${n} missions`, W / 2, 470);
    c.font = '400 26px Nunito, Arial, sans-serif'; c.fillStyle = '#575B66'; c.fillText(levels.join(' · '), W / 2, 515);
    c.font = '44px "Noto Color Emoji", "Apple Color Emoji", "Segoe UI Emoji", sans-serif'; c.fillText(badges.slice(0, 14).join(' '), W / 2, 605);
    c.fillStyle = '#15161C'; c.font = '600 26px Nunito, Arial, sans-serif'; c.fillText(dt, W / 2 - 280, 720); c.fillText('🧮 StudyVerse', W / 2 + 280, 720);
    c.fillStyle = '#8A8E99'; c.font = '400 20px Nunito, Arial, sans-serif'; c.fillText('Date', W / 2 - 280, 752); c.fillText('study.moneyviel.com', W / 2 + 280, 752);
  }

  /* ---------- entry points (added whenever these screens are drawn) ---------- */
  const tileHTML = () => { const p = progress(); return `<button class="cxa-tile" type="button" id="cxaTile" aria-label="Calculator Academy: free bonus, ${p.done} of ${p.all} missions done"><span class="cxa-te" aria-hidden="true">🧮</span><span class="cxa-tt"><b>Calculator Academy</b><small>Free · ${p.done} of ${p.all} missions · press real keys to learn</small></span><span class="cxa-tg" aria-hidden="true">▶</span></button>`; };
  const cardHTML = ca => { const p = progress(), bc = badgeCount(); return `<div class="card cxa-mecard" id="cxaMe"><div class="cxa-meh"><span class="cxa-mee" aria-hidden="true">🧮</span><div>${ca ? '<h2 class="ca-h2s">Calculator Academy</h2>' : '<h3>Calculator Academy</h3>'}<p class="sub">Free bonus: ${p.done} of ${p.all} missions · ${bc.have} badges</p></div></div>
    <div class="cxa-bar" aria-hidden="true"><i style="width:${p.pct}%"></i></div><button class="btn" type="button" id="cxaMeGo">Learn every calculator ▶</button></div>`; };
  function inject() {
    if (!P().name || parent()) return;
    const ca = isCA();
    const w = D.getElementById('s-world');
    if (w && !ca && w.querySelector('#map') && !w.querySelector('#cxaTile')) {
      const snack = w.querySelector('#gkSnack'), anchor = snack || w.querySelector('#map');
      anchor.insertAdjacentHTML('beforebegin', tileHTML()); wireTile('world');
    }
    const c = D.getElementById('s-ca');
    if (c && ca) {
      const top = c.querySelector(':scope > .ca-top'), home = top && c.querySelector(':scope > .ca-journey');
      let t = c.querySelector(':scope > #cxaTile');
      if (home) {
        const after = c.querySelector(':scope > .sv-planbar') || c.querySelector(':scope > #gkSnack') || top;
        if (!t) { after.insertAdjacentHTML('afterend', tileHTML()); wireTile('world'); }
        else if (t.previousElementSibling !== after) after.after(t);
      } else if (t) t.remove();
      const prof = c.querySelector(':scope > .ca-prof');
      if (prof && !c.querySelector('#cxaMe')) { const gk = D.getElementById('meGk'), a = (gk && c.contains(gk) && gk.closest('.card')) || c.querySelector(':scope > .sv-planbar') || prof; a.insertAdjacentHTML('afterend', cardHTML(true)); wireCard(); }
    }
    const me = D.getElementById('s-me');
    if (me && !ca && me.querySelector('.statrow') && !me.querySelector('#cxaMe')) { const gk = D.getElementById('meGk'), a = (gk && me.contains(gk) && gk.closest('.card')) || me.querySelector('.statrow'); a.insertAdjacentHTML('afterend', cardHTML(false)); wireCard(); }
  }
  function wireTile(from) { const t = D.getElementById('cxaTile'); if (t) t.onclick = () => { tap('open'); open({ from }); }; }
  function wireCard() { const b = D.getElementById('cxaMeGo'); if (b) b.onclick = () => { tap('open'); open({ from: 'me' }); }; }

  let css = false;
  function style() {
    if (css) return; css = true; const s = D.createElement('style'); s.textContent = `
.cxa-tile{display:flex;align-items:center;gap:12px;width:100%;min-height:56px;margin:0 0 12px;padding:10px 14px;border:0;border-radius:18px;cursor:pointer;text-align:left;
 background:linear-gradient(135deg,#15161C,#2a2c35);color:#F4EAD8;box-shadow:0 4px 0 rgba(0,0,0,.25);font-family:inherit}
.cxa-te{font-size:30px;line-height:1}.cxa-tt{flex:1;display:flex;flex-direction:column;gap:2px}.cxa-tt b{font-size:16px}.cxa-tt small{font-size:12.5px;opacity:.85}
.cxa-tg{background:#C9A76A;color:#15161C;border-radius:999px;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-size:13px}
.cxa-tile:focus-visible,.cxa-m:focus-visible,.cxa-opt:focus-visible{outline:3px solid var(--sun,#ffc93c);outline-offset:2px}
.cxa-mecard .cxa-meh{display:flex;gap:12px;align-items:center;margin-bottom:8px}.cxa-mee{font-size:34px}.cxa-mecard h3,.cxa-mecard h2{margin:0}
.cxa-bar{height:10px;border-radius:9px;background:rgba(0,0,0,.08);overflow:hidden;margin:6px 0 10px}.cxa-bar i{display:block;height:100%;background:linear-gradient(90deg,#2ed3a5,#ffc93c);border-radius:9px;transition:width .4s}
.cxa-ptop{display:flex;justify-content:space-between;font-weight:800}
.cxa-h3{margin:12px 0 6px;font-size:16px}
.cxa-badges{display:grid;grid-template-columns:repeat(auto-fill,minmax(76px,1fr));gap:6px;margin-bottom:10px}
.cxa-bdg{display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 2px;border-radius:12px;background:rgba(0,0,0,.04);opacity:.45;filter:grayscale(1);text-align:center}
.cxa-bdg.on{opacity:1;filter:none;background:#fff4cc}.cxa-bdg b{font-size:24px;line-height:1.1}.cxa-bdg small{font-size:10.5px;line-height:1.2;font-weight:700}
.cxa-level h2{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin:0 0 4px}.cxa-level h2 small{margin-left:auto;font-size:13px;color:var(--muted,#5a6077)}
.cxa-level.locked{opacity:.75}.cxa-lock{font-weight:700;margin:6px 0 0}
.cxa-ms{display:grid;gap:8px;margin-top:8px}
.cxa-m{display:flex;align-items:center;gap:10px;min-height:56px;width:100%;padding:8px 12px;border-radius:14px;border:2px solid rgba(0,0,0,.08);background:#fff;cursor:pointer;text-align:left;font-family:inherit;color:inherit}
.cxa-m.done{border-color:#2ed3a5;background:#effcf7}.cxa-me{font-size:26px}.cxa-mt{flex:1;display:flex;flex-direction:column}.cxa-mt b{font-size:15px}.cxa-mt small{font-size:12.5px;color:var(--muted,#5a6077)}
.cxa-st{color:#e0a400;font-size:16px;letter-spacing:1px;white-space:nowrap}
.cxa-mh{font-size:22px}.cxa-story p{margin:0 0 6px}
.cxa-say{font-size:17px;font-weight:700;line-height:1.4;margin:8px 0}
.cxa-msg{min-height:0;font-weight:700;margin:4px 0 8px;color:#1f7a55}.cxa-msg:empty{display:none}.cxa-msg.bad{color:#b3261e}
.cxa-row{display:flex;gap:8px;flex-wrap:wrap}.cxa-row .btn{flex:1;min-width:140px}
.cxa-steps{list-style:none;padding:12px 14px!important;margin:0 0 12px}.cxa-steps li{padding:6px 0;border-bottom:1px solid rgba(0,0,0,.06);font-size:14px;line-height:1.35;color:var(--muted,#5a6077)}
.cxa-steps li.now{color:inherit;font-weight:800}.cxa-steps li.ok{color:#1f7a55}
.cxa-q{font-size:18px;line-height:1.35;margin:8px 0}
.cxa-opts{display:grid;gap:8px;margin:8px 0}
.cxa-opt{min-height:48px;padding:10px 12px;border-radius:14px;border:2px solid rgba(0,0,0,.12);background:#fff;font:700 15px/1.3 inherit;font-family:inherit;color:inherit;text-align:left;cursor:pointer}
.cxa-opt.right{border-color:#2ed3a5;background:#e7fbf3}.cxa-opt.wrong{border-color:#ff6b6b;background:#fff0f0}.cxa-opt:disabled{cursor:default}
.cxa-newb{font-size:18px;font-weight:800}
.cxa-speed .cxa-sptop{display:flex;justify-content:space-between;font-weight:800;font-size:16px}
.cxa-prob{font:800 34px/1.2 "Baloo 2",Nunito,sans-serif;text-align:center;margin:14px 0 4px}
.cxa-img{width:100%;height:auto;border-radius:10px;box-shadow:0 4px 14px rgba(0,0,0,.15);margin-bottom:8px}
html[data-age=pro]:not(.sv-hc) .cxa-m{background:#FFFDF8;border-color:#E2D6BE}html[data-age=pro]:not(.sv-hc) .cxa-m.done{border-color:#2E8B57;background:#F1F8F3}
html[data-age=pro]:not(.sv-hc) .cxa-bdg.on{background:#F4EAD8}
html.sv-hc .cxa-tile,html.sv-hc .cxa-m,html.sv-hc .cxa-opt{background:#fff;color:#000;border:3px solid #000}`;
    D.head.appendChild(s);
  }
  function start() {
    style();
    let t = 0; new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; try { inject(); } catch (e) {} }); }).observe(D.body, { childList: true, subtree: true });
    inject();
  }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', start) : start();
  window.CalcAcademy = { open, mission, badgeCount, progress, _data: X };
})();
