/* ================= 🛡️ Activity guard (js/guard.js) =================
   1. svBusy(): true while a student is in the middle of something (a lesson/quiz, puzzle, game, Mind Gym round,
      CA practice…). Home tabs and lists are “safe”. js/app.js uses it so an app update never reloads mid-activity
      (that reload looked like a crash that jumped to the home page).
   2. Pull-to-refresh guard: the browser’s own pull-down refresh is switched off; our own pull-down does the same job
      on safe screens, but during an activity a tiny chip asks first: “Refreshing will exit this. Refresh · Cancel”.
   3. Update chip: when a new version is waiting, a tiny “✨ New version · Refresh” chip appears instead of a sudden reload. */
(function () {
  'use strict';
  const D = document;
  const SAFE = new Set(['world', 'practice', 'me', 'squad', 'subject', 'chapter', 'onboard']);
  function busy() {
    const a = D.querySelector('.screen.active'), id = a ? a.id.slice(2) : '';
    if (!id) return false;
    if (id === 'ca') return !!D.querySelector('#s-ca .ca-pad, #s-ca .ca-viva, #s-ca .ca-set, #s-ca .ca-mbar, #s-ca .ca-mcq, #s-ca .opt, #s-ca textarea');
    if (id === 'mind') return !!D.querySelector('#s-mind .mg-play, #s-mind .pl-card, #s-mind .pl-stage');
    if (id === 'play') return !!D.querySelector('#s-play .arc-game, #s-play .pz-grid, #s-play #pzGrid, #s-play .pz-board');
    if (SAFE.has(id)) return !!D.querySelector('.pz-grid, #pzGrid, .arc-game');
    return true;
  }
  window.svBusy = busy;

  function chip(html, buttons) {
    const old = D.getElementById('svChip'); if (old) old.remove();
    D.body.insertAdjacentHTML('beforeend', `<div id="svChip" class="sv-chip" role="alertdialog" aria-live="polite"><span>${html}</span>${buttons.map((b, i) => `<button type="button" data-i="${i}" class="${b.main ? 'main' : ''}">${b.t}</button>`).join('')}</div>`);
    const c = D.getElementById('svChip');
    c.querySelectorAll('button').forEach(b => b.onclick = () => { c.remove(); const f = buttons[+b.dataset.i].go; if (f) f(); });
    return c;
  }
  window.svChip = chip;
  window.svUpdateReady = () => chip('✨ New version ready', [{ t: 'Refresh', main: 1, go: reloadNow }, { t: 'Later' }]);

  /* ---- pull-down to refresh, with a check during activities ---- */
  let y0 = null, pulling = false, ind = null;
  const atTop = () => (window.scrollY || D.documentElement.scrollTop || 0) <= 0;
  const insideScroller = el => { for (let n = el; n && n !== D.body; n = n.parentElement) { if (n.scrollTop > 0) return true; } return false; };
  D.addEventListener('touchstart', e => {
    if (e.touches.length !== 1 || !atTop() || insideScroller(e.target) || D.getElementById('svChip')) { y0 = null; return; }
    y0 = e.touches[0].clientY; pulling = false;
  }, { passive: true });
  D.addEventListener('touchmove', e => {
    if (y0 == null) return; const dy = e.touches[0].clientY - y0;
    if (dy > 12 && atTop()) { pulling = true; if (!ind) { ind = D.createElement('div'); ind.className = 'sv-pull'; ind.textContent = '↻'; D.body.appendChild(ind); } ind.style.transform = `translate(-50%, ${Math.min(dy, 110) - 50}px) rotate(${dy * 3}deg)`; ind.classList.toggle('ready', dy > 100); }
  }, { passive: true });
  D.addEventListener('touchend', e => {
    if (y0 == null) return; const dy = (e.changedTouches[0] || {}).clientY - y0; y0 = null;
    if (ind) { ind.remove(); ind = null; }
    if (!pulling || dy < 100) return;
    // never reload on a pull alone (an accidental pull while scrolling used to restart the app): always ask first
    chip(busy() ? 'Refreshing will exit what you’re doing.' : 'Refresh Knowtopia?', [{ t: 'Refresh', main: 1, go: reloadNow }, { t: 'Cancel' }]);
  }, { passive: true });

  /* a refresh key / browser reload button during an activity: the browser shows its own small “Leave site?” check */
  window.addEventListener('beforeunload', e => { if (window.__svReloading) return; if (busy()) { e.preventDefault(); e.returnValue = ''; } });
  const reloadNow = () => { window.__svReloading = true; location.reload(); };
  window.svReload = reloadNow;

  D.head.insertAdjacentHTML('beforeend', `<style id="svGuardCss">
    html,body{overscroll-behavior-y:none}
    .sv-chip{position:fixed;left:50%;bottom:88px;transform:translateX(-50%);z-index:99999;display:flex;align-items:center;gap:6px;padding:8px 8px 8px 14px;border-radius:999px;background:#1f2540;color:#fff;font-size:13px;box-shadow:0 8px 24px rgba(0,0,0,.35);max-width:calc(100vw - 24px);animation:svIn .25s both}
    .sv-chip span{line-height:1.3}.sv-chip button{border:0;border-radius:999px;padding:6px 11px;font-size:13px;font-weight:800;background:rgba(255,255,255,.14);color:#fff;cursor:pointer;font-family:inherit;white-space:nowrap}.sv-chip button.main{background:#ffc43d;color:#2a1d00}
    .sv-pull{position:fixed;top:0;left:50%;z-index:99998;width:38px;height:38px;border-radius:50%;background:#fff;color:#6d4aff;display:grid;place-items:center;font-size:22px;font-weight:900;box-shadow:0 4px 14px rgba(0,0,0,.25)}.sv-pull.ready{background:#6d4aff;color:#fff}
    @keyframes svIn{from{opacity:0;transform:translate(-50%,10px)}}
  </style>`);
})();
