/* ================= Me page layout (js/melayout.js) =================
   Many modules add their own cards to Me (school #s-me and the CA profile in #s-ca). Instead of moving those cards
   (modules re-place them), this file only ORDERS them visually with CSS flex order and adds short section headings:
     Profile → 🏆 My progress → 📚 My learning → 👨‍👩‍👧 Account & family → ⚙️ Settings → ⚖️ Help & legal → 🛠️ Owner → Start over */
(function () {
  'use strict';
  const D = document;
  const SECT = [['prog', 10, '🏆 My progress'], ['learn', 20, '📚 My learning'], ['acct', 30, '👨‍👩‍👧 Account & family'], ['set', 40, '⚙️ Settings'], ['help', 50, '⚖️ Help & legal']];
  const ORDER = [
    ['.mecard, .ca-prof', 1], ['.statrow', 2], ['.sv-planbar', 3], ['.pv-goal', 4], ['.pv-mission', 5], ['#gkSnack', 6],
    ['#rwMe', 11], ['.me-badges', 12], ['.in-badge', 13], ['.gk-mecard', 14], ['.in-hw', 15],
    ['#meGrade', 21], ['#meStreamC', 22],
    ['#svCloud', 31], ['#svCode', 32], ['.pv-me', 33], ['.in-me', 34],
    ['#cxSet', 41], ['#meSound', 42], ['#caPhUse', 43],
    ['#lgCard', 51],
    ['.in-own', 61], ['#svCodes', 62], ['.od-me', 63], ['#caOwner', 64],
    ['#meResetC', 56], ['#meOut', 57]];
  const scope = s => ORDER.map(([q, n]) => q.split(',').map(x => `${s} > ${x.trim()}`).join(',') + `{order:${n}}`).join('');
  function style() {
    if (D.getElementById('meLayCss')) return;
    D.head.insertAdjacentHTML('beforeend', `<style id="meLayCss">
      #s-me.me-lay.active,#s-ca.me-lay.active{display:flex;flex-direction:column}#s-me.me-lay>*,#s-ca.me-lay>*{order:25}
      ${scope('#s-me.me-lay')}${scope('#s-ca.me-lay')}
      ${SECT.map(([k, n]) => `#s-me.me-lay>.me-h-${k},#s-ca.me-lay>.me-h-${k}{order:${n}}`).join('')}
      .me-lay>.me-h{margin:20px 6px 0;font-size:13px;font-weight:900;letter-spacing:.06em;text-transform:uppercase;color:#fff;opacity:.85;text-shadow:0 1px 2px rgba(0,0,0,.35)}
      .me-lay #svCloud [data-cl="out"]{display:none}.me-out .btn{width:100%}
      #s-me.me-lay>.me-sec,#s-ca.me-lay>.me-sec{order:0}.me-lay>.me-sec{display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;margin:14px 0 2px;padding:14px 16px;border:0;border-radius:18px;cursor:pointer;font:inherit;font-weight:900;font-size:17px;text-align:left;color:#fff;background:linear-gradient(135deg,#5b3fd1,#2b7de9);box-shadow:0 4px 14px rgba(0,0,0,.18)}
      #s-me.me-lay>.me-sec-b,#s-ca.me-lay>.me-sec-b{order:29;background:linear-gradient(135deg,#0f8f8a,#2bb3a3)}#s-me.me-lay>.me-sec-c,#s-ca.me-lay>.me-sec-c{order:59;background:linear-gradient(135deg,#37415e,#596580)}
      .me-sec small{display:block;font-weight:600;font-size:12px;opacity:.85}.me-sec .me-chev{font-size:20px;transition:transform .2s}.me-sec[aria-expanded="false"] .me-chev{transform:rotate(-90deg)}
      .me-lay.ma-shut>[data-ms="a"],.me-lay.mb-shut>[data-ms="b"],.me-lay.mc-shut>[data-ms="c"]{display:none!important}
      .me-lay>.card .btn,.me-lay>section .btn{padding:8px 14px;font-size:15px;border-radius:12px;box-shadow:0 3px 0 rgba(0,0,0,.18)}
      .me-lay>.card .btn.ghost{box-shadow:none}.me-lay>.card h3{margin-bottom:6px}
      .me-lay>.me-h:empty{display:none}.me-lay>.card{margin-top:10px}.me-lay>.me-danger{margin-top:28px;opacity:.9}
    </style>`);
  }
  const has = (h, q) => !!h.querySelector(q.split(',').map(x => ':scope > ' + x.trim()).join(','));
  function lay(h) {
    if (!h || !h.firstElementChild) return;
    const prof = h.id === 's-me' || !!h.querySelector(':scope > .ca-prof');
    h.classList.toggle('me-lay', prof);
    if (!prof) { h.querySelectorAll(':scope > .me-h, :scope > #meOut, :scope > .me-sec').forEach(x => x.remove()); h.classList.remove('ma-shut', 'mb-shut', 'mc-shut'); return; }
    out(h);
    secs(h);
    SECT.forEach(([k, n, t]) => {
      const lo = n, hi = n + 9, any = k === 'learn' ? true : ORDER.some(([q, o]) => o > lo && o <= hi && has(h, q));
      let e = h.querySelector(`:scope > .me-h-${k}`);
      if (any && !e) { e = D.createElement('div'); e.className = `me-h me-h-${k}`; e.setAttribute('role', 'heading'); e.setAttribute('aria-level', '2'); e.textContent = t; h.appendChild(e); }
      else if (!any && e) e.remove();
    });
  }
  /* two big sections that open and close: 🙋 About me & my progress (A) and ⚙️ Everything else (B) */
  const SK = 'sv_mesec', open_ = () => { try { return Object.assign({ a: true, b: false, c: false }, JSON.parse(localStorage.getItem(SK) || '{}')); } catch (e) { return { a: true, b: false, c: false }; } };
  const orderOf = el => { if (el.classList.contains('me-h')) return +(SECT.find(([k]) => el.classList.contains('me-h-' + k)) || [0, 25])[1];
    for (let i = ORDER.length - 1; i >= 0; i--) { const [q, n] = ORDER[i]; if (q.split(',').some(x => el.matches(x.trim()))) return n; }
    return el.classList.contains('nx-card') ? 23 : 25; };
  function secs(h) {
    const st = open_();
    const own = ORDER.some(([q, n]) => n >= 60 && n < 70 && has(h, q));
    [['a', '🙋 About me & my progress', 'Profile, progress, badges, cards and learning'], ['b', '🧰 My toolbox', 'Account, family, settings, help, legal and sign out'], ['c', '🛠️ Owner tools', 'Only you can see this: codes, schools, dashboard']].forEach(([k, t, sub]) => {
      let b = h.querySelector(`:scope > .me-sec-${k}`);
      if (k === 'c' && !own) { if (b) b.remove(); return; }
      if (!b) { b = D.createElement('button'); b.type = 'button'; b.className = `me-sec me-sec-${k}`; b.innerHTML = `<span>${t}<small>${sub}</small></span><span class="me-chev" aria-hidden="true">▾</span>`;
        b.onclick = () => { const o = open_(); o[k] = !o[k]; try { localStorage.setItem(SK, JSON.stringify(o)); } catch (e) {} paint(h); }; h.appendChild(b); }
    });
    [...h.children].forEach(el => { if (el.classList.contains('me-sec')) return; const n = orderOf(el); const ms = n < 29 ? 'a' : n < 59 ? 'b' : 'c'; if (el.dataset.ms !== ms) el.dataset.ms = ms; });
    paint(h, st);
  }
  function paint(h, st) {
    st = st || open_();
    h.classList.toggle('ma-shut', !st.a); h.classList.toggle('mb-shut', !st.b); h.classList.toggle('mc-shut', !st.c);
    ['a', 'b', 'c'].forEach(k => { const b = h.querySelector(`:scope > .me-sec-${k}`); if (b && b.getAttribute('aria-expanded') !== String(st[k])) b.setAttribute('aria-expanded', String(st[k])); });
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
