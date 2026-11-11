/* ================= 🧠 Mind Gym (js/mindgym.js) =================
   Five fun thinking-skill practices, opened from a tile in the Practice tab (school and CA):
     🧠 Brain Power (IQ-style puzzles)   💛 Heart Smarts (feelings)   🤝 People Skills (getting along)
     🌱 Bounce-Back (setbacks)           💡 Idea Spark (curiosity and creativity)
   Questions: content/mind/<test>.json (made by tools/mind/gen_iq.py and tools/mind/build.py).
   Band by age: j = Grades 1–3 (pictures, big buttons), m = Grades 4–8 (quests), s = Grades 9–12 (missions),
   p = CA (workplace scenarios; Brain Power uses the s puzzles).
   Engagement rule: 20 questions per practice are open at the start, and every 2 finished topics (CA: units)
   open 10 more in every practice. The owner account sees everything.
   Answers are checked by the app only — students can never mark themselves right.
   This is fun practice: no IQ number, no labels, no medical or psychological claims (see NOTE).
   Progress: ST.mind = { seen: {qid: 1|0 (last answer right)}, log: {test: [1,0,…last 40]}, rounds: {test: n} }
   window.MindGym = { open } */
(function () {
  'use strict';
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const STx = () => { try { return ST; } catch (e) { return null; } };
  const isCA = () => { const s = STx(); return !!(s && s.profile && s.profile.course === 'ca'); };
  const isParent = () => { try { return !!(window.Cloud && Cloud.isParent && Cloud.isParent()); } catch (e) { return false; } };
  const isOwner = () => { try { return !!(window.Cloud && Cloud.admin && Cloud.admin()); } catch (e) { return false; } };
  const persist = () => { try { save(); } catch (e) {} };

  const TESTS = [
    { id: 'iq', e: '🧠', n: 'Brain Power', d: 'Patterns, number puzzles, codes and logic', col: '#6d4aff' },
    { id: 'eq', e: '💛', n: 'Heart Smarts', d: 'Understanding feelings, yours and other people’s', col: '#e0a100' },
    { id: 'sq', e: '🤝', n: 'People Skills', d: 'Friendship, teamwork and fairness', col: '#1e9e6a' },
    { id: 'aq', e: '🌱', n: 'Bounce-Back', d: 'Handling setbacks and trying again', col: '#2f8f3a' },
    { id: 'cq', e: '💡', n: 'Idea Spark', d: 'Curiosity and creative thinking', col: '#e0408f' }];
  const T = id => TESTS.find(t => t.id === id);
  const START = 20, PER = 10, STEP = 2, ROUND = { j: 6, m: 8, s: 10, p: 10 };
  const NOTE = 'Mind Gym is fun practice to grow thinking skills. It is not an IQ test or a medical or psychological assessment, and it never labels anyone. Feelings and people questions follow widely used school social-emotional learning ideas.';
  const LOOK = { j: { tag: 'Picture puzzles and stories', word: 'Play', round: 'game' }, m: { tag: 'Quests for sharp minds', word: 'Start quest', round: 'quest' },
    s: { tag: 'Missions to level up', word: 'Start mission', round: 'mission' }, p: { tag: 'Workplace and study scenarios', word: 'Start set', round: 'set' } };

  function band() {
    const s = STx(); if (!s || !s.profile) return 'm';
    if (isCA()) return 'p';
    const g = +s.profile.grade || 5; return g <= 3 ? 'j' : g <= 8 ? 'm' : 's';
  }
  const qBand = (test, b) => test === 'iq' && b === 'p' ? 's' : b;
  function M() { const s = STx(); s.mind = s.mind && typeof s.mind === 'object' ? s.mind : {}; const m = s.mind; m.seen = m.seen || {}; m.log = m.log || {}; m.rounds = m.rounds || {}; return m; }

  /* finished learning steps: school topics with a star; CA units with Learn and MCQ done */
  function steps() {
    const s = STx(); if (!s) return 0;
    if (isCA()) { const u = (s.ca && s.ca.units) || {}; return Object.keys(u).filter(k => u[k] && u[k].learn && u[k].mcq).length; }
    return Object.keys(s.topics || {}).filter(k => s.topics[k] && s.topics[k].stars > 0).length;
  }
  const stepWord = n => (isCA() ? 'unit' : 'topic') + (n === 1 ? '' : 's');

  /* question banks, in a fixed mixed order (so each new pack has a mix of puzzle types) */
  const BANK = {};
  const hash = s => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };
  async function bank(test) {
    if (!BANK[test]) {
      const d = await loadJSON(`content/mind/${test}.json`);
      BANK[test] = (d.questions || []).filter(q => q && q.id && Array.isArray(q.o) && q.o.length === 4 && q.a >= 0 && q.a < 4).sort((a, b) => hash(a.id) - hash(b.id));
    }
    return BANK[test];
  }
  async function pool(test) { const b = qBand(test, band()); return (await bank(test)).filter(q => q.b === b); }
  function openCount(total) { if (isOwner()) return total; return Math.min(total, START + PER * Math.floor(steps() / STEP)); }
  function nextUnlock(total) {
    if (isOwner() || openCount(total) >= total) return null;
    const need = STEP - (steps() % STEP); return { need, gets: Math.min(PER, total - openCount(total)) };
  }

  /* skill level from the last 40 answers (no numbers that look like an IQ score) */
  function level(test) {
    const l = M().log[test] || [];
    if (l.length < 10) return { k: 'start', n: 'Warming up', pct: l.length ? Math.round(l.filter(Boolean).length / l.length * 100) : 0, few: true };
    const p = Math.round(l.filter(Boolean).length / l.length * 100);
    const n = p >= 85 ? 'Champion' : p >= 70 ? 'Pro' : p >= 50 ? 'Rising star' : 'Explorer';
    return { k: n, n, pct: p };
  }
  const STARS = { 'Warming up': '✨', Explorer: '🧭', 'Rising star': '⭐', Pro: '🌟', Champion: '🏆' };

  /* ---------- screen ---------- */
  function screen() {
    let s = D.getElementById('s-mind');
    if (!s) { $1('main').insertAdjacentHTML('beforeend', '<section class="screen" id="s-mind"></section>'); s = D.getElementById('s-mind'); }
    return s;
  }
  const backToPractice = () => { if (isCA() && window.CaTools && CaTools.practiceHub) CaTools.practiceHub(); else practiceScreen(); };

  async function open() {
    style(); const el = screen(); show('mind', 'practice'); window.scrollTo(0, 0);
    const b = band(), lk = LOOK[b];
    el.innerHTML = `<div class="mg-root mg-${b}"><button class="back" id="mgBack">← Practice</button><div class="hello mg-hello" role="heading" aria-level="1"><span aria-hidden="true">🧠</span> Mind Gym <small>${E(lk.tag)}</small></div><div class="card mg-wait">Loading…</div></div>`;
    $1('#mgBack').onclick = () => { S('tap'); backToPractice(); };
    let info;
    try { info = await Promise.all(TESTS.map(async t => { const p = await pool(t.id); return { t, total: p.length, open: openCount(p.length), lv: level(t.id), nx: nextUnlock(p.length) }; })); }
    catch (e) { $1('.mg-wait', el).textContent = 'Could not load Mind Gym. Check your internet and try again.'; return; }
    const st = steps(), nx = info.map(i => i.nx).filter(Boolean)[0];
    const prog = nx ? `<div class="card mg-unlock"><b>🔓 Finish ${nx.need} more ${stepWord(nx.need)} to unlock ${nx.gets} new challenges in every practice.</b><div class="mg-bar"><i style="width:${Math.round(((STEP - nx.need) / STEP) * 100)}%"></i></div><small>Learning opens new challenges. ${st} ${stepWord(st)} finished so far.</small></div>` : '';
    $1('.mg-wait', el).outerHTML = `${prog}
      <div class="mg-list">${info.map(i => `<button type="button" class="card mg-test" data-t="${i.t.id}" style="--c:${i.t.col}">
        <span class="mg-e" aria-hidden="true">${i.t.e}</span><span class="mg-tt"><b>${E(i.t.n)}</b><small>${E(i.t.d)}</small>
        <small class="mg-meta">${STARS[i.lv.n] || ''} ${E(i.lv.n)} · ${i.open} of ${i.total} challenges open</small></span><span class="mg-chev" aria-hidden="true">›</span></button>`).join('')}</div>
      <div class="card"><h3><span aria-hidden="true">📊</span> My skill levels</h3>${info.map(i => `<div class="mg-row"><span>${i.t.e} ${E(i.t.n)}</span><div class="mg-bar"><i style="width:${i.lv.pct}%;background:${i.t.col}"></i></div><b>${i.lv.few ? '—' : i.lv.pct + '%'}</b></div>`).join('')}
        <p class="sub mg-lvl">Levels: 🧭 Explorer → ⭐ Rising star → 🌟 Pro → 🏆 Champion, based on your last 40 answers in each practice.</p></div>
      <div class="card mg-note">ℹ️ ${E(NOTE)}</div>`;
    el.querySelectorAll('[data-t]').forEach(x => x.onclick = () => { S('open'); round(x.dataset.t); });
  }

  /* ---------- a round ---------- */
  function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  async function round(test) {
    const el = screen(), t = T(test), b = band(), lk = LOOK[b], m = M();
    const all = await pool(test), open_ = all.slice(0, openCount(all.length));
    if (!open_.length) { toast('No challenges here yet'); return; }
    const n = Math.min(ROUND[b], open_.length);
    const fresh = shuffle(open_.filter(q => !(q.id in m.seen)));
    const missed = shuffle(open_.filter(q => m.seen[q.id] === 0));
    const rest = shuffle(open_.filter(q => m.seen[q.id] === 1));
    const list = fresh.concat(missed, rest).slice(0, n);
    let i = 0, right = 0;
    const draw = () => {
      const q = list[i], order = shuffle([0, 1, 2, 3]);
      el.innerHTML = `<div class="mg-root mg-${b}" style="--c:${t.col}"><button class="back" id="mgQuit">← Mind Gym</button>
        <div class="card mg-play"><div class="mg-top"><span>${t.e} ${E(t.n)}</span><span>${i + 1} / ${list.length}</span></div>
          <div class="mg-bar"><i style="width:${Math.round(i / list.length * 100)}%;background:${t.col}"></i></div>
          <h3 class="mg-q${q.k === 'picture' || q.k === 'odd-pic' ? ' pic' : ''}">${E(q.q)}</h3>
          <div class="mg-opts">${order.map(k => `<button type="button" class="mg-o${q.k === 'odd-pic' || q.k === 'picture' ? ' pic' : ''}" data-k="${k}">${E(q.o[k])}</button>`).join('')}</div>
          <div class="mg-fb" aria-live="polite"></div></div></div>`;
      $1('#mgQuit').onclick = () => { S('tap'); if (i > 0 || el.querySelector('.mg-o:disabled')) finish(true); else open(); };
      el.querySelectorAll('.mg-o').forEach(btn => btn.onclick = () => {
        const k = +btn.dataset.k, ok = k === q.a;
        el.querySelectorAll('.mg-o').forEach(x => { x.disabled = true; if (+x.dataset.k === q.a) x.classList.add('ok'); });
        if (!ok) btn.classList.add('no');
        S(ok ? 'right' : 'wrong'); if (ok) right++;
        m.seen[q.id] = ok ? 1 : 0; const L = m.log[test] = (m.log[test] || []); L.push(ok ? 1 : 0); if (L.length > 40) L.splice(0, L.length - 40); persist();
        const scen = test !== 'iq';
        $1('.mg-fb', el).innerHTML = `<p class="mg-v ${ok ? 'ok' : 'no'}">${ok ? (scen ? '✅ Best choice!' : '✅ Correct!') : (scen ? '💭 There’s a better choice.' : '❌ Not quite.')}</p><p>${scen && !ok ? `<b>Best: ${E(q.o[q.a])}.</b> ` : ''}${E(q.why)}</p>
          <button class="btn" type="button" id="mgNext">${i + 1 < list.length ? 'Next ▶' : 'See my result'}</button>`;
        const nb = $1('#mgNext'); nb.focus({ preventScroll: true }); nb.onclick = () => { S('tap'); i++; if (i < list.length) draw(); else finish(false); };
      });
    };
    const finish = early => {
      const done = early ? i + (el.querySelector('.mg-o:disabled') ? 1 : 0) : list.length;
      if (!done) { open(); return; }
      m.rounds[test] = (m.rounds[test] || 0) + 1; persist();
      if (right) { try { addXP(right * 2); } catch (e) {} }
      const lv = level(test);
      const msg = right === done ? 'Perfect round! 🎉' : right >= done * 0.7 ? 'Great thinking!' : right >= done * 0.4 ? 'Good effort — every round makes you sharper.' : 'Nice try! Read the explanations and try another round.';
      el.innerHTML = `<div class="mg-root mg-${b}"><div class="card mg-done" style="--c:${t.col}"><div class="mg-big" aria-hidden="true">${t.e}</div><h2>${E(msg)}</h2>
        <p class="sub">${right} of ${done} ${test === 'iq' ? 'correct' : 'best choices'}${right ? ` · +${right * 2} ⭐` : ''}</p>
        <p>${STARS[lv.n] || ''} ${E(t.n)} level: <b>${E(lv.n)}</b>${lv.few ? ' (play a few more to get your level)' : ''}</p>
        <button class="btn" type="button" id="mgAgain">Another ${E(lk.round)} ▶</button><div style="height:8px"></div><button class="btn ghost" type="button" id="mgHome">← Mind Gym</button></div></div>`;
      $1('#mgAgain').onclick = () => { S('open'); round(test); };
      $1('#mgHome').onclick = () => { S('tap'); open(); };
    };
    draw();
  }

  /* ---------- tile in the Practice tab ---------- */
  const tileSub = () => 'Brain Power, Heart Smarts and more · unlock by learning';
  function place() {
    const s = STx(); if (!s || !s.profile || isParent()) return;
    const p = D.getElementById('s-practice');
    if (p && p.classList.contains('active') && !isCA() && !p.querySelector(':scope > #mgTile')) {
      const after = p.querySelector(':scope > #cxaTile') || p.querySelector(':scope > #phTile');
      if (after) { after.insertAdjacentHTML('afterend', `<button type="button" class="card mg-tile" id="mgTile" aria-label="Mind Gym: thinking-skill challenges"><span class="mg-te" aria-hidden="true">🧠</span><span class="mg-tt"><b>Mind Gym</b><small>${tileSub()}</small></span><span class="mg-chev" aria-hidden="true">›</span></button>`); wire(); }
    }
    const c = D.getElementById('s-ca');
    if (c && isCA() && c.classList.contains('active')) {
      const hubs = c.querySelector(':scope > .ca-hubs');
      const after = hubs && (hubs.querySelector(':scope > #cxaTile') || hubs.querySelector(':scope > #phTile'));
      if (after && !hubs.querySelector('#mgTile')) { after.insertAdjacentHTML('afterend', `<button type="button" class="card ca-hub" id="mgTile"><b class="ca-hube" aria-hidden="true">🧠</b><span><b>Mind Gym</b><small>Thinking, people and workplace skills · unlock by learning</small></span><span class="ca-chev" aria-hidden="true">›</span></button>`); wire(); }
    }
  }
  function wire() { const t = D.getElementById('mgTile'); if (t) t.onclick = () => { S('open'); open(); }; }

  let css = false;
  function style() {
    if (css) return; css = true;
    D.head.insertAdjacentHTML('beforeend', `<style id="mgCss">
      .mg-tile{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:none;cursor:pointer;background:linear-gradient(135deg,#0f8f8a,#2bb3a3);color:#fff;font-family:inherit}
      .mg-tile .mg-te{font-size:34px}.mg-tile .mg-tt{flex:1;display:flex;flex-direction:column}.mg-tile b{font-size:19px}.mg-tile small{opacity:.92;font-size:13px}
      .mg-chev{font-size:24px;opacity:.7}.ca-hubs .mg-tile,.ca-hubs #mgTile{margin-bottom:10px}
      .mg-list{display:flex;flex-direction:column;gap:10px;margin-bottom:12px}
      .mg-test{display:flex;align-items:center;gap:12px;width:100%;text-align:left;cursor:pointer;font-family:inherit;border:2px solid transparent;border-left:6px solid var(--c);margin:0}
      .mg-test .mg-e{font-size:32px}.mg-test .mg-tt{flex:1;display:flex;flex-direction:column;gap:2px}.mg-test b{font-size:17px}.mg-test small{color:var(--muted,#666);font-size:13px}.mg-test .mg-meta{font-weight:700;color:var(--c)}
      .mg-bar{height:8px;border-radius:9px;background:rgba(0,0,0,.08);overflow:hidden;margin:8px 0}.mg-bar i{display:block;height:100%;border-radius:9px;background:#2bb3a3;transition:width .3s}
      .mg-unlock b{display:block;font-size:15px}.mg-unlock small{color:var(--muted,#666)}
      .mg-row{display:grid;grid-template-columns:minmax(120px,1fr) 2fr 42px;align-items:center;gap:8px;font-size:14px}.mg-row .mg-bar{margin:6px 0}.mg-row b{text-align:right}
      .mg-lvl{font-size:12px;margin-top:8px}.mg-note{font-size:12.5px;color:var(--muted,#555);line-height:1.45;margin-bottom:20px}
      .mg-top{display:flex;justify-content:space-between;font-weight:800;font-size:14px;color:var(--c)}
      .mg-q{font-size:19px;line-height:1.4;margin:10px 0 14px;white-space:pre-wrap;word-break:break-word}.mg-q.pic{font-size:30px;line-height:1.5}
      .mg-opts{display:grid;grid-template-columns:1fr;gap:10px}.mg-o{border:2px solid rgba(0,0,0,.12);border-radius:14px;background:#fff;color:#1f2d33;padding:13px 14px;font-size:16px;text-align:left;cursor:pointer;font-family:inherit;line-height:1.35}
      .mg-o.pic{font-size:34px;text-align:center;padding:8px}.mg-j .mg-opts:has(.pic){grid-template-columns:1fr 1fr}
      .mg-o:hover:not(:disabled){border-color:var(--c)}.mg-o.ok{border-color:#1e9e6a;background:#e6f7ef}.mg-o.no{border-color:#d33;background:#fdeaea}.mg-o:disabled{cursor:default;opacity:1}
      .mg-fb p{margin:10px 0 0;line-height:1.45}.mg-v{font-weight:900;font-size:17px}.mg-v.ok{color:#1e9e6a}.mg-v.no{color:#b5541d}.mg-fb .btn{margin-top:12px}
      .mg-done{text-align:center}.mg-big{font-size:56px}
      .mg-j .mg-q{font-size:21px}.mg-j .mg-o{font-size:18px;padding:15px;border-radius:18px}.mg-j .mg-test b{font-size:18px}
      .mg-s .mg-test,.mg-p .mg-test{border-left-width:4px}.mg-p .mg-o{border-radius:10px}
      .mg-o:focus-visible,.mg-test:focus-visible,.mg-tile:focus-visible{outline:3px solid #2b6cff;outline-offset:2px}
    </style>`);
  }

  function boot() {
    style();
    let t = 0; new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; try { place(); } catch (e) {} }); }).observe(D.body, { childList: true, subtree: true });
    place();
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
  window.MindGym = { open, _steps: steps, _band: band };
})();
