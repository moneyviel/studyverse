/* StudyVerse plans, free trial, daily free limit and payments.
   - New accounts get 24 hours of all school grades (studyverse.start_trial, called by js/cloud.js).
   - After that, free users get FREE_PER_DAY answered questions a day (school and CA counted separately).
     GK Explorer and the games stay free and are not counted.
   - Owner, paid plans, the trial and free-forever codes are unlimited.
   - Paying: Plans sheet → server function "studyverse-pay" creates a Razorpay order (prices and discount codes
     are checked on the server) → Razorpay checkout → the server verifies the payment and unlocks the course.
     One-time payment for 1 or 12 months (no auto-renew); reminders before it ends.
   Needs js/cloud.js (window.Cloud). Loads after app.js. */
(function () {
  const D = document, FREE_PER_DAY = 5;
  const DEF_PLANS = [
    { id: 'school-month', course: 'school-all', label: 'School · 1 month', months: 1, price_inr: 149, sort: 1 },
    { id: 'school-year', course: 'school-all', label: 'School · 12 months', months: 12, price_inr: 999, sort: 2 },
    { id: 'ca-month', course: 'ca-foundation', label: 'CA Foundation · 1 month', months: 1, price_inr: 299, sort: 3 },
    { id: 'ca-year', course: 'ca-foundation', label: 'CA Foundation · 12 months', months: 12, price_inr: 1999, sort: 4 },
  ];
  let plans = DEF_PLANS;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const say = m => { try { toast(m); } catch (e) {} };
  const C = () => window.Cloud;
  const parent = () => !!(C() && C().isParent && C().isParent());          // parent accounts never see plans, bars or the paywall
  const signedIn = () => !!(C() && C().signedIn());
  const owner = () => { try { return localStorage.getItem('sv_owner') === '1' || (C() && C().admin()); } catch (e) { return false; } };
  const kindNow = () => { try { return ST.profile && ST.profile.course === 'ca' ? 'ca' : 'school'; } catch (e) { return 'school'; } };
  const rows = () => { try { return JSON.parse(localStorage.getItem('sv_access') || '[]') || []; } catch (e) { return []; } };
  const live = a => !a.valid_until || new Date(a.valid_until) > new Date();
  const dt = d => new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
  const left = d => { const ms = new Date(d) - Date.now(); if (ms <= 0) return '0m'; const h = Math.floor(ms / 36e5), m = Math.floor(ms % 36e5 / 6e4); return h >= 48 ? Math.ceil(ms / 864e5) + ' days' : (h ? h + 'h ' : '') + m + 'm'; };

  /* what this account can use right now, for 'school' or 'ca' */
  function access(kind) {
    if (owner()) return { full: true, why: 'owner' };
    const r = rows().filter(live);
    if (kind === 'ca') { const c = r.find(a => a.course === 'ca-foundation'); return c ? { full: true, until: c.valid_until, why: /code/.test(c.note || '') ? 'code' : 'paid' } : { full: false }; }
    const all = r.find(a => a.course === 'school-all');
    if (all) return { full: true, until: all.valid_until, why: /trial/.test(all.note || '') ? 'trial' : 'paid' };
    if (r.some(a => /^school-g/.test(a.course))) return { full: true, why: 'code' };
    const ended = rows().find(a => a.course === 'school-all');
    return { full: false, trialEnded: !!(ended && /trial/.test(ended.note || '')) };
  }

  /* ---------- daily free questions ---------- */
  const today = () => { const d = new Date(); return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate(); };
  function used(kind) { try { const u = ST.dayq || {}; return u.d === today() ? (u[kind] || 0) : 0; } catch (e) { return 0; } }
  function count(kind) { try { if (!ST.dayq || ST.dayq.d !== today()) ST.dayq = { d: today() }; ST.dayq[kind] = (ST.dayq[kind] || 0) + 1; save(); } catch (e) {} }

  D.addEventListener('click', e => {
    const b = e.target.closest && e.target.closest('button.opt[data-k]');
    if (!b || b.disabled || !signedIn() || parent()) return;
    if (b.closest('#gkOpts') || b.classList.contains('arc-opt')) return;          // GK Explorer and games stay free
    const box = b.closest('#tOpts');                                               // tests: count each question once
    if (box && box.dataset.svc) return;
    const kind = kindNow();
    if (access(kind).full) return;
    if (used(kind) >= FREE_PER_DAY) { e.preventDefault(); e.stopImmediatePropagation(); paywall(kind); return; }
    if (box) box.dataset.svc = 1;
    count(kind); bars();
    const n = FREE_PER_DAY - used(kind);
    if (n === 1) setTimeout(() => say('1 free question left today'), 600);
  }, true);

  /* ---------- sheets ---------- */
  const css = `.pl-card{border:1.5px solid #e2d6bd;border-radius:14px;padding:12px 14px;margin:10px 0;background:#fff}
.pl-card h4{margin:0 0 6px;font-size:16px}.pl-row{display:flex;gap:8px;flex-wrap:wrap}
.pl-buy{flex:1;min-width:130px;border:0;border-radius:12px;padding:12px;font-weight:700;font-size:15px;cursor:pointer;background:#15161C;color:#F4EAD8}
.pl-buy.yr{background:#C9A76A;color:#15161C}.pl-buy small{display:block;font-weight:500;font-size:12px;opacity:.85}
.pl-old{text-decoration:line-through;opacity:.6;font-weight:500;margin-right:4px}
.pl-st{background:#F4EAD8;border-radius:12px;padding:10px 12px;font-size:14px;margin:8px 0}
.sv-planbar{display:flex;align-items:center;gap:10px;justify-content:space-between;padding:10px 14px!important}
.sv-planbar p{margin:0;font-size:14px;line-height:1.35}.sv-planbar button{flex:none;border:0;border-radius:10px;padding:9px 12px;font-weight:700;background:#C9A76A;color:#15161C;cursor:pointer}`;
  function style() { if (D.getElementById('svPlanCss')) return; const s = D.createElement('style'); s.id = 'svPlanCss'; s.textContent = css; D.head.appendChild(s); }

  function paywall(kind) {
    if (parent()) return;
    style();
    const el = C().sheet(`<h3 id="clT">That's today's ${FREE_PER_DAY} free questions 🎯</h3>
      <p>Great work! Come back tomorrow for ${FREE_PER_DAY} more, or subscribe for unlimited practice, tests and every ${kind === 'ca' ? 'CA Foundation paper' : 'grade'}.</p>
      <button class="btn" type="button" id="pwPlans">See plans</button><div style="height:8px"></div><button class="btn ghost" type="button" id="pwLater">Maybe later</button>`);
    el.querySelector('#pwPlans').onclick = () => open(kind);
    el.querySelector('#pwLater').onclick = C().closeSheet;
  }

  async function loadPlans() {
    try { const r = await C().rest('plans?select=id,course,label,months,price_inr,sort&active=eq.true&order=sort'); if (Array.isArray(r) && r.length) plans = r; } catch (e) {}
  }
  function statusLine(kind) {
    const a = access(kind);
    if (a.why === 'owner') return 'Owner account — everything is unlocked.';
    if (a.why === 'trial') return `🎁 Free trial: <b>${left(a.until)}</b> left — everything in school is unlocked.`;
    if (a.why === 'code') return '🎟️ Free access with your code.';
    if (a.full) return `✅ Your ${kind === 'ca' ? 'CA Foundation' : 'school'} plan is active till <b>${dt(a.until)}</b>.`;
    return `Free plan: <b>${Math.max(0, FREE_PER_DAY - used(kind))} of ${FREE_PER_DAY}</b> questions left today.${a.trialEnded ? ' Your free trial has ended.' : ''}`;
  }

  let quote = null;                                   // { code, percent }
  async function open(kind) {
    style(); kind = kind || kindNow();
    if (!signedIn()) { C().open('in'); return; }
    if (parent()) return;
    await loadPlans();
    const groups = [['school-all', 'School — all classes 1–12', 'Unlimited questions, tests, games and analysis for every grade.'], ['ca-foundation', 'CA Foundation', 'All 4 papers: unlimited fresh questions, mock tests, answer checking.']];
    if (kind === 'ca') groups.reverse();
    const price = p => quote && quote.percent ? Math.round(p.price_inr * (100 - quote.percent) / 100) : p.price_inr;
    const btn = p => { const f = price(p); const per = p.months === 12 ? ` · ₹${Math.round(f / 12)}/month` : '';
      return `<button class="pl-buy ${p.months === 12 ? 'yr' : ''}" type="button" data-plan="${esc(p.id)}">${f !== p.price_inr ? `<span class="pl-old">₹${p.price_inr}</span>` : ''}₹${f.toLocaleString('en-IN')} <small>${p.months === 12 ? '12 months' : '1 month'}${per}</small></button>`; };
    const el = C().sheet(`<h3 id="clT">Plans</h3><div class="pl-st" role="status">${statusLine(kind)}</div>
      ${groups.map(([c, t, d]) => { const ps = plans.filter(p => p.course === c); return ps.length ? `<div class="pl-card"><h4>${t}</h4><p class="cl-small">${d}</p><div class="pl-row">${ps.map(btn).join('')}</div></div>` : ''; }).join('')}
      <form id="plCodeF" class="cl-row" novalidate style="margin-top:6px"><input class="cl-in" id="plCode" placeholder="Discount code" autocapitalize="characters" maxlength="24" style="flex:2;min-width:140px;margin:0" value="${esc(quote ? quote.code : (localStorage.getItem('sv_disc') || ''))}"><button class="btn ghost" type="submit" style="flex:1">Apply</button></form>
      <div class="cl-err" id="plErr" role="alert"></div>${quote && quote.percent ? `<div class="cl-ok">${quote.percent}% off with ${esc(quote.code)} ✓</div>` : ''}
      <p class="cl-small">One-time payment by Razorpay (UPI, cards, net banking). It does not renew by itself — we remind you before it ends. Prices include taxes.</p>
      <button class="btn ghost" type="button" id="plX">Close</button>`);
    el.querySelector('#plX').onclick = C().closeSheet;
    el.querySelector('#plCodeF').onsubmit = async e => {
      e.preventDefault(); const er = el.querySelector('#plErr'), code = el.querySelector('#plCode').value.trim().toUpperCase(); er.textContent = '';
      if (!code) { quote = null; open(kind); return; }
      try { const r = await C().rest('rpc/quote', { method: 'POST', body: { p_code: code } }); if (!r || !r.ok) { er.textContent = (r && r.msg) || 'This code is not valid.'; return; } quote = { code, percent: r.percent }; open(kind); }
      catch (err) { er.textContent = C().errText(err); }
    };
    el.querySelectorAll('[data-plan]').forEach(b => b.onclick = () => pay(b.dataset.plan, kind, b));
  }

  function loadRzp() {
    if (window.Razorpay) return Promise.resolve();
    return new Promise((res, rej) => { const s = D.createElement('script'); s.src = 'https://checkout.razorpay.com/v1/checkout.js'; s.onload = res; s.onerror = () => rej(new Error('Could not open the payment page. Please check your internet.')); D.head.appendChild(s); });
  }
  async function pay(planId, kind, b) {
    const er = D.getElementById('plErr'); if (er) er.textContent = '';
    b.disabled = true; const label = b.innerHTML; b.textContent = 'Please wait…';
    try {
      const o = await C().call('/functions/v1/studyverse-pay', { method: 'POST', body: { action: 'order', plan: planId, code: quote ? quote.code : null } });
      if (o && o.error) throw new Error(o.error);
      if (o && o.paid) return done(o);                // 100% discount: unlocked without payment
      await loadRzp();
      const u = C().user() || {};
      const rz = new window.Razorpay({
        key: o.key_id, amount: o.amount, currency: 'INR', order_id: o.order_id, name: 'StudyVerse', description: o.label,
        prefill: { email: u.email || '' }, notes: { plan: planId }, theme: { color: '#8A6A2E' },
        handler: async r => {
          try {
            const v = await C().call('/functions/v1/studyverse-pay', { method: 'POST', body: { action: 'verify', order_id: r.razorpay_order_id, payment_id: r.razorpay_payment_id, signature: r.razorpay_signature } });
            if (v && v.error) throw new Error(v.error); done(v);
          } catch (e) { msg('Payment received but not yet confirmed: ' + e.message + ' Please contact support with your payment ID ' + r.razorpay_payment_id + '.'); }
        },
        modal: { ondismiss: () => { b.disabled = false; b.innerHTML = label; } },
      });
      rz.on('payment.failed', r => { b.disabled = false; b.innerHTML = label; if (er) er.textContent = 'Payment failed: ' + ((r && r.error && r.error.description) || 'please try again.'); });
      rz.open();
    } catch (e) { b.disabled = false; b.innerHTML = label; if (er) er.textContent = /not set up|not configured/i.test(e.message) ? 'Payments are being set up — please try again soon.' : C().errText(e); }
  }
  async function done(v) {
    quote = null; try { localStorage.removeItem('sv_disc'); } catch (e) {}
    await C().refreshAccess();
    msg(`🎉 Payment successful! ${esc(v.label || 'Your plan')} is active till ${v.until ? dt(v.until) : 'the end of the period'}. Enjoy unlimited learning.`, true);
    bars();
  }
  function msg(t, ok) { const el = C().sheet(`<h3 id="clT">${ok ? 'Thank you!' : 'Payment'}</h3><p>${t}</p><button class="btn" type="button" id="plOk">OK</button>`); el.querySelector('#plOk').onclick = C().closeSheet; }

  /* ---------- plan bar on World and Me, reminders ---------- */
  function barHTML(kind) {
    const a = access(kind);
    if (a.why === 'owner' || a.why === 'code') return '';
    if (a.why === 'trial') return `<p>🎁 <b>Free trial: ${left(a.until)} left.</b> Everything is unlocked.</p><button type="button" data-pl>Subscribe</button>`;
    if (a.full) { const soon = a.until && new Date(a.until) - Date.now() < 7 * 864e5; return soon ? `<p>⏳ Your plan ends on <b>${dt(a.until)}</b>.</p><button type="button" data-pl>Renew</button>` : ''; }
    return `<p><b>${Math.max(0, FREE_PER_DAY - used(kind))} of ${FREE_PER_DAY}</b> free questions left today.${a.trialEnded ? ' Trial ended.' : ''}</p><button type="button" data-pl>Subscribe</button>`;
  }
  function bars() {
    if (!signedIn()) return;
    if (parent()) { D.querySelectorAll('.sv-planbar').forEach(b => b.remove()); return; }
    ['s-world', 's-me'].forEach(id => {
      const sc = D.getElementById(id); if (!sc || !sc.firstElementChild) return;
      const h = barHTML(kindNow()); let b = sc.querySelector(':scope > .sv-planbar');
      if (!h) { if (b) b.remove(); return; }
      if (!b) { style(); b = D.createElement('div'); b.className = 'card sv-planbar'; const first = sc.querySelector(':scope > .card'); first ? first.after(b) : sc.prepend(b); }
      if (b.dataset.h !== h) { b.dataset.h = h; b.innerHTML = h; b.querySelector('[data-pl]').onclick = () => open(); }
    });
  }
  let warned = false;
  function remind() {
    if (!signedIn() || warned || parent()) return;
    const a = access(kindNow());
    if (a.why === 'trial' && a.until && new Date(a.until) - Date.now() < 3 * 36e5) { warned = true; say(`Your free trial ends in ${left(a.until)} — subscribe to keep everything unlocked`); }
    else if (a.why === 'paid' && a.until && new Date(a.until) - Date.now() < 3 * 864e5) { warned = true; say(`Your plan ends on ${dt(a.until)} — renew to keep learning without limits`); }
  }

  function start() {
    let t = 0;
    new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; bars(); }); }).observe(D.body, { childList: true, subtree: true });
    addEventListener('sv-access', () => { bars(); remind(); });
    setInterval(() => { bars(); remind(); }, 60000);
    setTimeout(() => { bars(); remind(); }, 1500);
  }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', start) : start();

  window.Plans = { open, access, used: k => used(k || kindNow()), FREE_PER_DAY };
})();
