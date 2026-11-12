/* Owner switcher — only for the owner account. A small 🔑 button on every screen opens one sheet that jumps straight
   into any course: every school grade, every JEE track and every CA level. Students never see it. */
(function () {
  const D = document;
  const admin = () => { try { return !!(window.Cloud && Cloud.admin && Cloud.admin() && !localStorage.getItem('sv_demo')); } catch (e) { return false; } };
  const tap = k => { try { sfx(k || 'tap'); } catch (e) {} };
  const look = () => { try { if (window.Look) Look.apply(); } catch (e) {} };
  const where = () => {
    const p = ST.profile || {}, j = ST.jee || {};
    if (p.course === 'ca') return 'ca:' + ((ST.ca && ST.ca.level) || 'foundation');
    if (j.track && j.home) return 'jee:' + j.track + ':' + (j.track === 'full' ? '' : (j.cls || ''));
    return 'g:' + (p.grade || 0);
  };
  const LEVELS = [['foundation', 'Foundation'], ['inter', 'Intermediate'], ['final', 'Final']];
  const JEE = [['found', 9, '🌱 Foundation · Class 9'], ['found', 10, '🌱 Foundation · Class 10'], ['main', 11, '🚀 Main · Class 11'], ['main', 12, '🚀 Main · Class 12'], ['full', null, '⚡ Full syllabus · Dropper']];

  function toGrade(g) {
    const p = ST.profile; if (!p) return;
    const fin = () => { p.course = null; if (ST.jee) ST.jee.home = false; setGrade(g); save(); look(); toast(`Grade ${g}`); worldScreen(); };
    if (g >= 11 && !p.stream) { pickStream(g, (stream, subjects) => { p.stream = stream; p.subjects = subjects; fin(); }, () => open()); return; }
    if (g < 11) { p.stream = null; p.subjects = null; }
    fin();
  }
  function toJee(track, cls) {
    if (!window.Jee) return;
    if (!ST.jee) ST.jee = { units: {}, mist: [] };
    const j = ST.jee; j.units = j.units || {}; j.mist = j.mist || [];
    j.track = track; j.cls = cls; j.who = track === 'full' ? 'drop' : 'c' + cls;
    const r = Jee.elig(track === 'full' ? { status: 'passed', first: 2026 } : { status: 'school', cls }); j.elig = { xii: r.xii, main: r.main, adv: r.adv };
    j.home = true; j.since = j.since || Date.now(); if (ST.profile) ST.profile.course = null; save(); look(); Jee.home();
  }
  function toCA(level) {
    if (!window.Ca) return;
    ST.ca = Object.assign({}, ST.ca || {}, { level }); ST.profile.course = 'ca'; save(); look();
    try { Ca.home(); } catch (e) { Ca.setup(1); }
  }

  function open() {
    if (!admin()) return;
    close();
    const now = where(), on = k => k === now ? ' on' : '';
    const sh = D.createElement('div'); sh.className = 'sheet ob-sheet'; sh.id = 'obSheet';
    sh.setAttribute('role', 'dialog'); sh.setAttribute('aria-modal', 'true'); sh.setAttribute('aria-label', 'Owner: open any course');
    sh.innerHTML = `<div class="sheet-in"><div class="sheet-grab"></div>
      <div class="ob-h"><h2>🔑 Open any course</h2><button type="button" class="ob-x" data-close aria-label="Close">✕</button></div>
      <p class="sub">Owner only. Jump in as a student of any grade or course — your progress in each course stays as it is.</p>
      <h3>🏫 School · Grade</h3><div class="ob-g">${Array.from({ length: 12 }, (_, i) => `<button type="button" class="ob-b${on('g:' + (i + 1))}" data-g="${i + 1}">${i + 1}</button>`).join('')}</div>
      <h3>🎯 JEE Main</h3><div class="ob-l">${JEE.map(([t, c, n]) => `<button type="button" class="ob-b${on('jee:' + t + ':' + (c || ''))}" data-jt="${t}" data-jc="${c || ''}">${n}</button>`).join('')}</div>
      <h3>📊 CA</h3><div class="ob-l">${LEVELS.map(([k, n]) => `<button type="button" class="ob-b${on('ca:' + k)}" data-ca="${k}">CA ${n}</button>`).join('')}</div>
      <div class="ob-l" style="margin-top:12px">${window.Parent && Parent.open ? '<button type="button" class="ob-b ghost" data-x="parent">👪 Parent Hub (test)</button>' : ''}<button type="button" class="ob-b ghost" data-x="me">⚙️ Me &amp; owner tools</button></div></div>`;
    D.body.appendChild(sh);
    sh.addEventListener('click', e => { if (e.target === sh) close(); });
    sh.querySelectorAll('[data-close]').forEach(b => b.onclick = close);
    sh.querySelectorAll('[data-g]').forEach(b => b.onclick = () => { tap('open'); close(); toGrade(+b.dataset.g); });
    sh.querySelectorAll('[data-jt]').forEach(b => b.onclick = () => { tap('open'); close(); toJee(b.dataset.jt, b.dataset.jc ? +b.dataset.jc : null); });
    sh.querySelectorAll('[data-ca]').forEach(b => b.onclick = () => { tap('open'); close(); toCA(b.dataset.ca); });
    sh.querySelectorAll('[data-x]').forEach(b => b.onclick = () => { tap('open'); close(); if (b.dataset.x === 'parent') Parent.open(); else meScreen(); });
    requestAnimationFrame(() => sh.classList.add('show'));
  }
  function close() { const s = D.getElementById('obSheet'); if (s) { s.classList.remove('show'); setTimeout(() => s.remove(), 200); } }

  function style() {
    if (D.getElementById('obCss')) return;
    const st = D.createElement('style'); st.id = 'obCss';
    st.textContent = `.ob-key{position:fixed;right:max(12px,calc(50% - 208px));bottom:calc(150px + env(safe-area-inset-bottom));z-index:5;width:42px;height:42px;border-radius:50%;border:2px solid #fff;background:linear-gradient(135deg,#facc15,#f59e0b);font-size:20px;box-shadow:0 4px 14px #0005;cursor:pointer}
      .ob-sheet .sheet-in{max-height:86vh;overflow:auto}.ob-h{display:flex;align-items:center;justify-content:space-between}.ob-h h2{margin:0}.ob-x{border:0;background:none;font-size:20px;cursor:pointer}
      .ob-sheet h3{margin:14px 0 6px}.ob-g{display:grid;grid-template-columns:repeat(6,1fr);gap:6px}.ob-l{display:flex;flex-wrap:wrap;gap:6px}
      .ob-b{border:2px solid #c4b5fd;background:#f5f3ff;color:#4c1d95;border-radius:12px;padding:9px 10px;font-weight:800;cursor:pointer;min-width:0}.ob-b.on{background:#6d28d9;color:#fff;border-color:#6d28d9}.ob-b.ghost{background:#fff;border-color:#e2e8f0;color:#334155}body:has(#obSheet) .ob-key,body:has(.asksheet.show) .ob-key,body:has(.sheet.show) .ob-key{display:none}`;
    D.head.appendChild(st);
  }
  function paint() {
    const has = D.getElementById('obKey');
    const showIt = admin() && ST.profile && !D.querySelector('#s-onboard.active');
    if (!showIt) { if (has) has.remove(); return; }
    if (has) return;
    style(); const b = D.createElement('button'); b.id = 'obKey'; b.type = 'button'; b.className = 'ob-key'; b.title = 'Owner: open any course'; b.setAttribute('aria-label', 'Owner: open any course'); b.textContent = '🔑';
    b.onclick = () => { tap('open'); open(); }; D.body.appendChild(b);
  }
  setInterval(paint, 1500); window.addEventListener('sv-access', paint); D.addEventListener('DOMContentLoaded', paint); setTimeout(paint, 500);
  window.OwnerBar = { open, paint };
})();
