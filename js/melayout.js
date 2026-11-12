/* ================= Me page layout (js/melayout.js) =================
   Many modules add their own cards to Me (school #s-me and the CA profile in #s-ca). Instead of moving those cards
   (modules re-place them), this file only ORDERS them visually with CSS flex order and adds short section headings:
     Profile → 🏆 My progress → 📚 My learning → 👨‍👩‍👧 Account & family → ⚙️ Settings → ⚖️ Help & legal → 🛠️ Owner → Start over */
(function () {
  'use strict';
  const D = document;
  const SECT = [['prog', 10, '🏆 My progress'], ['learn', 20, '📚 My learning'], ['acct', 30, '👨‍👩‍👧 Account & family'], ['set', 40, '⚙️ Settings'], ['help', 50, '⚖️ Help & legal'], ['own', 60, '🛠️ Owner tools']];
  const ORDER = [
    ['.mecard, .ca-prof', 1], ['.statrow', 2], ['.sv-planbar', 3], ['.pv-goal', 4], ['.pv-mission', 5], ['#gkSnack', 6],
    ['#rwMe', 11], ['.me-badges', 12], ['.in-badge', 13], ['.gk-mecard', 14], ['.in-hw', 15],
    ['#meGrade', 21], ['#meStreamC', 22],
    ['#svCloud', 31], ['#svCode', 32], ['.pv-me', 33], ['.in-me', 34],
    ['#cxSet', 41], ['#meSound', 42], ['#caPhUse', 43],
    ['#lgCard', 51],
    ['.in-own', 61], ['#svCodes', 62], ['.od-me', 63], ['#caOwner', 64],
    ['#meResetC', 90], ['#meOut', 95]];
  const scope = s => ORDER.map(([q, n]) => q.split(',').map(x => `${s} > ${x.trim()}`).join(',') + `{order:${n}}`).join('');
  function style() {
    if (D.getElementById('meLayCss')) return;
    D.head.insertAdjacentHTML('beforeend', `<style id="meLayCss">
      #s-me.me-lay,#s-ca.me-lay{display:flex;flex-direction:column}#s-me.me-lay>*,#s-ca.me-lay>*{order:25}
      ${scope('#s-me.me-lay')}${scope('#s-ca.me-lay')}
      ${SECT.map(([k, n]) => `#s-me.me-lay>.me-h-${k},#s-ca.me-lay>.me-h-${k}{order:${n}}`).join('')}
      .me-lay>.me-h{margin:20px 6px 0;font-size:13px;font-weight:900;letter-spacing:.06em;text-transform:uppercase;color:#fff;opacity:.85;text-shadow:0 1px 2px rgba(0,0,0,.35)}
      .me-lay #svCloud [data-cl="out"]{display:none}.me-out .btn{width:100%}
      .me-lay>.me-h:empty{display:none}.me-lay>.card{margin-top:10px}.me-lay>.me-danger{margin-top:28px;opacity:.9}
    </style>`);
  }
  const has = (h, q) => !!h.querySelector(q.split(',').map(x => ':scope > ' + x.trim()).join(','));
  function lay(h) {
    if (!h || !h.firstElementChild) return;
    const prof = h.id === 's-me' || !!h.querySelector(':scope > .ca-prof');
    h.classList.toggle('me-lay', prof);
    if (!prof) { h.querySelectorAll(':scope > .me-h, :scope > #meOut').forEach(x => x.remove()); return; }
    out(h);
    SECT.forEach(([k, n, t]) => {
      const lo = n, hi = n + 9, any = k === 'learn' ? true : ORDER.some(([q, o]) => o > lo && o <= hi && has(h, q));
      let e = h.querySelector(`:scope > .me-h-${k}`);
      if (any && !e) { e = D.createElement('div'); e.className = `me-h me-h-${k}`; e.setAttribute('role', 'heading'); e.setAttribute('aria-level', '2'); e.textContent = t; h.appendChild(e); }
      else if (!any && e) e.remove();
    });
  }
  /* 🚪 Sign out: its own card at the very end of Me (two taps, like before) */
  function out(h) {
    const C = window.Cloud, on = !!(C && C.signedIn && C.signedIn());
    let c = h.querySelector(':scope > #meOut');
    if (!on) { if (c) c.remove(); return; }
    if (c) return;
    c = D.createElement('div'); c.className = 'card me-out'; c.id = 'meOut';
    c.innerHTML = `<h3>🚪 Sign out</h3><p class="sub">${(C.email && C.email()) ? 'Signed in as ' + C.email().replace(/[<>&"]/g, '') + '. ' : ''}Your progress stays safe in your account.</p><button class="btn ghost" type="button">Sign out</button>`;
    const b = c.querySelector('button');
    b.onclick = () => { if (!b.dataset.sure) { b.dataset.sure = 1; b.textContent = 'Tap again to sign out'; return; } b.disabled = true; b.textContent = 'Signing out…'; try { C.signOut(); } catch (e) {} };
    h.appendChild(c);
  }
  let t = 0;
  function run() { t = 0; style(); ['s-me', 's-ca'].forEach(id => lay(D.getElementById(id))); }
  function boot() {
    new MutationObserver(() => { if (!t) t = requestAnimationFrame(run); }).observe(D.querySelector('main') || D.body, { childList: true, subtree: true });
    run();
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
})();
