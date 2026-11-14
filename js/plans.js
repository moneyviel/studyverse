/* Knowtopia plans, free trial, daily free limit and payments.
   - New accounts get 24 hours of all school grades (studyverse.start_trial, called by js/cloud.js).
   - After that, free users get FREE_PER_DAY answered questions a day (school and CA counted separately).
     GK Explorer and the games stay free and are not counted.
   - Owner, paid plans, the trial and free-forever codes are unlimited.
   - Paying: Plans sheet → server function "studyverse-pay" creates a Razorpay order (prices and discount codes
     are checked on the server) → Razorpay checkout → the server verifies the payment and unlocks the course.
     One-time payment (no auto-renew); reminders before it ends. Prices are excl. GST (GST added as applicable).
   - The sheet shows ONLY the student's own plans: school = the plans of their class band (min_grade..max_grade,
     the server rejects a class outside the band); CA = the plans of their CA level (ST.ca.level → 'ca-<level>').
   Needs js/cloud.js (window.Cloud). Loads after app.js. */
(function () {
  const D = document, FREE_PER_DAY = 5;
  /* fallback when the plans table cannot be read — KEEP IN SYNC with studyverse.plans and pricing/index.html FALLBACK */
  const DEF_PLANS = [
    { id: 's15-month', course: 'school', label: 'School Class 1–5 · 1 month', months: 1, price_inr: 199, sort: 1, min_grade: 1, max_grade: 5 },
    { id: 's15-year', course: 'school', label: 'School Class 1–5 · 12 months', months: 12, price_inr: 1499, sort: 2, min_grade: 1, max_grade: 5 },
    { id: 's68-month', course: 'school', label: 'School Class 6–8 · 1 month', months: 1, price_inr: 249, sort: 3, min_grade: 6, max_grade: 8 },
    { id: 's68-year', course: 'school', label: 'School Class 6–8 · 12 months', months: 12, price_inr: 1999, sort: 4, min_grade: 6, max_grade: 8 },
    { id: 's910-month', course: 'school', label: 'School Class 9–10 · 1 month', months: 1, price_inr: 349, sort: 5, min_grade: 9, max_grade: 10 },
    { id: 's910-year', course: 'school', label: 'School Class 9–10 · 12 months', months: 12, price_inr: 2799, sort: 6, min_grade: 9, max_grade: 10 },
    { id: 's1112-month', course: 'school', label: 'School Class 11–12 · 1 month', months: 1, price_inr: 449, sort: 7, min_grade: 11, max_grade: 12 },
    { id: 's1112-year', course: 'school', label: 'School Class 11–12 · 12 months', months: 12, price_inr: 3499, sort: 8, min_grade: 11, max_grade: 12 },
    { id: 'ca-month', course: 'ca-foundation', label: 'CA Foundation · 1 month', months: 1, price_inr: 499, sort: 10 },
    { id: 'ca-4m', course: 'ca-foundation', label: 'CA Foundation · 4 months', months: 4, price_inr: 1799, sort: 11 },
    { id: 'cai-month', course: 'ca-inter', label: 'CA Intermediate · 1 month', months: 1, price_inr: 799, sort: 12 },
    { id: 'cai-4m', course: 'ca-inter', label: 'CA Intermediate · 4 months', months: 4, price_inr: 2999, sort: 13 },
    { id: 'caf-month', course: 'ca-final', label: 'CA Final · 1 month', months: 1, price_inr: 999, sort: 14 },
    { id: 'caf-4m', course: 'ca-final', label: 'CA Final · 4 months', months: 4, price_inr: 3799, sort: 15 },
  ];
  /* CA levels students can use now — KEEP IN SYNC with LIVE_LEVELS in js/ca.js (other levels show "Coming soon", no buy button) */
  const CA_LIVE = ['foundation', 'inter', 'final'];
  const CA_NAME = { foundation: 'CA Foundation', inter: 'CA Intermediate', final: 'CA Final' };
  const GST = 'Prices are + GST as applicable.';
  let plans = DEF_PLANS;
  /* Play Store build (TWA): never point to the web pricing page there. Remembered once seen. */
  try { if ((D.referrer || '').startsWith('android-app://')) localStorage.setItem('sv_play', '1'); } catch (e) {}
  window.SV_PLAY = (D.referrer || '').startsWith('android-app://') || (() => { try { return localStorage.getItem('sv_play') === '1'; } catch (e) { return false; } })();
  /* Play build (Play anti-steering): NO pay/buy buttons, plan names or prices anywhere — the Plans sheet shows only the
     current plan status, the paywall only says to come back tomorrow, and the Me "Plans & subscribe" button (js/cloud.js) is hidden. */
  if (window.SV_PLAY) { const s = D.createElement('style'); s.id = 'svPlayCss'; s.textContent = '[data-cl="plans"]{display:none!important}'; (D.head || D.documentElement).appendChild(s); }
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const say = m => { try { toast(m); } catch (e) {} };
  const C = () => window.Cloud;
  const parent = () => !!(C() && C().isParent && C().isParent());          // parent accounts never see plans, bars or the paywall
  const signedIn = () => !!(C() && C().signedIn());
  const owner = () => { try { return localStorage.getItem('sv_owner') === '1' || (C() && C().admin()); } catch (e) { return false; } };
  const caLevel = () => { try { const l = ST.ca && ST.ca.level; return CA_NAME[l] ? l : 'foundation'; } catch (e) { return 'foundation'; } };
  const caCourse = () => 'ca-' + caLevel(), caName = () => CA_NAME[caLevel()];
  const gradeNow = () => { try { return +ST.profile.grade || 0; } catch (e) { return 0; } };
  const band = p => { const d = DEF_PLANS.find(x => x.id === p.id) || {}; return [+(p.min_grade || d.min_grade) || 0, +(p.max_grade || d.max_grade) || 0]; };
  const inBand = (p, g) => { const [a, b] = band(p); return g >= a && g <= b; };
  const savePct = (p, all) => { const m = all.find(x => +x.months === 1 && x.course === p.course && (p.course !== 'school' || band(x)[0] === band(p)[0]));
    return m && +p.months > 1 ? Math.round(100 * (1 - p.price_inr / (m.price_inr * p.months))) : 0; };
  const kindNow = () => { try { return ST.profile && ST.profile.course === 'ca' ? 'ca' : 'school'; } catch (e) { return 'school'; } };
  const rows = () => { try { return JSON.parse(localStorage.getItem('sv_access') || '[]') || []; } catch (e) { return []; } };
  const live = a => !a.valid_until || new Date(a.valid_until) > new Date();
  const dt = d => new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
  const left = d => { const ms = new Date(d) - Date.now(); if (ms <= 0) return '0m'; const h = Math.floor(ms / 36e5), m = Math.floor(ms % 36e5 / 6e4); return h >= 48 ? Math.ceil(ms / 864e5) + ' days' : (h ? h + 'h ' : '') + m + 'm'; };

  /* what this account can use right now, for 'school' or 'ca' */
  function access(kind) {
    if (owner()) return { full: true, why: 'owner' };
    const r = rows().filter(live);
    /* the free trial is only shown when the student has neither a free-forever code nor a paid plan */
    const lock = (() => { try { return localStorage.getItem('sv_lock'); } catch (e) { return null; } })(), paid = r.filter(a => /paid/.test(a.note || ''));
    const noTrial = (row) => { const own = paid.find(a => a.course === row.course) || paid[0];
      return lock ? { full: true, why: 'code', course: lock } : { full: true, why: 'paid', until: own.valid_until, course: own.course }; };
    if (kind === 'ca') { const c = r.find(a => a.course === caCourse()); if (!c) return { full: false };
      const w = /trial/.test(c.note || '') ? 'trial' : /code/.test(c.note || '') ? 'code' : 'paid';
      if (w === 'trial' && (lock || paid.length)) return noTrial(c);
      return { full: true, until: c.valid_until, why: w, course: c.course }; }
    const all = r.find(a => a.course === 'school-all');
    if (all) { const w = /trial/.test(all.note || '') ? 'trial' : 'paid'; if (w === 'trial' && (lock || paid.length)) return noTrial(all); return { full: true, until: all.valid_until, why: w, course: all.course }; }
    let g = 0; try { g = +ST.profile.grade; } catch (e) {}
    const mine = r.find(a => a.course === 'school-g' + g);          // a school plan or code covers ONE class
    if (mine) return { full: true, until: mine.valid_until, why: /paid/.test(mine.note || '') ? 'paid' : 'code', course: mine.course };
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
    if (b.closest('#gkOpts') || b.classList.contains('arc-opt') || b.classList.contains('lv-opt')) return;   // GK Explorer, games and Game Rooms stay free
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
.sv-planbar p{margin:0;font-size:14px;line-height:1.35}.sv-planbar button{flex:none;border:0;border-radius:10px;padding:9px 12px;min-height:44px;font-weight:700;background:#C9A76A;color:#15161C;cursor:pointer}`;
  function style() { if (D.getElementById('svPlanCss')) return; const s = D.createElement('style'); s.id = 'svPlanCss'; s.textContent = css; D.head.appendChild(s); }

  function paywall(kind) {
    if (parent()) return;
    style();
    if (window.SV_PLAY) {
      const el = C().sheet(`<h3 id="clT">That's today's ${FREE_PER_DAY} free questions 🎯</h3><p>You've used today's ${FREE_PER_DAY} free questions. Come back tomorrow.</p><button class="btn" type="button" id="pwLater">OK</button>`);
      el.querySelector('#pwLater').onclick = C().closeSheet; return;
    }
    const el = C().sheet(`<h3 id="clT">That's today's ${FREE_PER_DAY} free questions 🎯</h3>
      <p>Great work! Come back tomorrow for ${FREE_PER_DAY} more, or subscribe for unlimited practice, tests and every ${kind === 'ca' ? caName() + ' paper' : 'subject of your class'}.</p>
      <button class="btn" type="button" id="pwPlans">See plans</button><div style="height:8px"></div><button class="btn ghost" type="button" id="pwLater">Maybe later</button>`);
    el.querySelector('#pwPlans').onclick = () => open(kind);
    el.querySelector('#pwLater').onclick = C().closeSheet;
  }

  async function loadPlans() {
    try { const r = await C().rest('plans?select=id,course,label,months,price_inr,sort,min_grade,max_grade&active=eq.true&order=sort'); if (Array.isArray(r) && r.length && r.every(p => p && p.id && +p.price_inr > 0)) plans = r; } catch (e) {}
  }
  /* a free-forever code on the account (cloud.js keeps it in sv_lock, e.g. 'school-g1' / 'ca-foundation') */
  const planName = (a, kind) => { const c = a.course || ''; return /^school-g\d+$/.test(c) ? 'Class ' + c.slice(8) : /^ca-/.test(c) ? (CA_NAME[c.slice(3)] || caName()) : kind === 'ca' ? caName() : 'school'; };
  const lockName = () => { let c = null; try { c = localStorage.getItem('sv_lock'); } catch (e) {} if (!c) return '';
    return c.startsWith('school-g') ? 'Grade ' + c.slice(8) : c === 'ca-foundation' ? 'CA Foundation' : c.replace(/^ca-/, 'CA ').replace(/-/g, ' '); };
  function statusLine(kind) {
    const a = access(kind);
    if (a.why === 'owner') return 'Owner account — everything is unlocked.';
    if (a.why === 'trial') return kind === 'ca' ? `🎁 Free trial: <b>${left(a.until)}</b> left — all of ${caName()} is open.` : `🎁 Free trial: <b>${left(a.until)}</b> left — all classes are open.${window.SV_PLAY ? '' : ' After that, only the class you subscribe to.'}`;
    if (a.why === 'code') return `🎟️ ${lockName() ? `<b>${lockName()}</b> is free for you forever with your code.` : 'Free access with your code.'}`;
    if (a.full) return `✅ Your ${planName(a, kind)} plan is active${a.until ? ` till <b>${dt(a.until)}</b>` : ''}.`;
    return `Free plan: <b>${Math.min(FREE_PER_DAY, Math.max(0, FREE_PER_DAY - used(kind)))} of ${FREE_PER_DAY}</b> questions left today.${a.trialEnded ? ' Your free trial has ended.' : ''}`;
  }

  let quote = null;                                   // { code, percent }
  async function open(kind) {
    style(); kind = kind || kindNow();
    if (!signedIn()) { C().open('in'); return; }
    if (parent()) return;
    if (window.SV_PLAY) {                             // Play build: status only — no plans, prices or buy buttons
      const el = C().sheet(`<h3 id="clT">Your plan</h3><div class="pl-st" role="status">${statusLine(kind)}</div><button class="btn ghost" type="button" id="plX">Close</button>`);
      el.querySelector('#plX').onclick = C().closeSheet; return;
    }
    await loadPlans();
    let saved = null; try { saved = localStorage.getItem('sv_disc'); } catch (e) {}
    if (saved && (!quote || quote.code !== saved)) {          // the code saved in Me → Have a code? is used here automatically
      try { const r = await C().rest('rpc/quote', { method: 'POST', body: { p_code: saved } }); quote = r && r.ok ? { code: saved, percent: r.percent } : null; } catch (e) { quote = null; }
    }
    if (!saved) quote = null;
    const cls = gradeNow(), lvl = caLevel();
    const price = p => quote && quote.percent ? Math.round(p.price_inr * (100 - quote.percent) / 100) : p.price_inr;
    const btn = (p, all) => { const f = price(p), m = +p.months, sv = savePct(p, all);
      return `<button class="pl-buy ${m > 1 ? 'yr' : ''}" type="button" data-plan="${esc(p.id)}">${f !== p.price_inr ? `<span class="pl-old">₹${p.price_inr.toLocaleString('en-IN')}</span>` : ''}₹${f.toLocaleString('en-IN')} <small>${m === 1 ? '1 month' : m + ' months'}${sv > 0 ? ` · Save ${sv}%` : ''}</small></button>`; };
    let card;
    if (kind === 'ca') {                              // only the student's own CA level
      const ps = plans.filter(p => p.course === 'ca-' + lvl).sort((a, b) => a.months - b.months);
      const live = CA_LIVE.includes(lvl);
      card = `<div class="pl-card"><h4>${CA_NAME[lvl]}</h4>${live
        ? `<p class="cl-small">All papers: unlimited fresh questions, mock tests, answer checking. 4 months = one exam attempt season.</p>${ps.length ? `<div class="pl-row">${ps.map(p => btn(p, ps)).join('')}</div>` : '<p class="cl-small">Plans are not available right now.</p>'}`
        : `<p class="cl-small"><b>Coming soon.</b> ${CA_NAME[lvl]} lessons are being prepared — plans open when they are ready.</p>`}</div>`;
    } else {                                          // only the plans of the student's class band
      const ps = plans.filter(p => p.course === 'school' && cls && inBand(p, cls)).sort((a, b) => a.months - b.months);
      card = `<div class="pl-card"><h4>School — Class ${cls || ''}</h4>${ps.length
        ? `<p class="cl-small">Everything in Class ${cls}: unlimited questions, tests, games and analysis. Only your class is included.</p><div class="pl-row">${ps.map(p => btn(p, ps)).join('')}</div>`
        : '<p class="cl-small">Choose your class in <b>Me</b> first to see its plans.</p>'}</div>`;
    }
    let lk = null; try { lk = localStorage.getItem('sv_lock'); } catch (e) {}
    const freeHere = !!lk && (kind === 'ca' ? lk === 'ca-' + lvl : lk === 'school-g' + cls);
    if (freeHere) card = `<div class="pl-card"><h4>${esc(lockName())}</h4><p class="cl-small">✅ Free for you forever with your code — nothing to buy here.</p></div>`;
    const el = C().sheet(`<h3 id="clT">Plans</h3><div class="pl-st" role="status">${statusLine(kind)}</div>
      ${card}<p class="cl-small pl-gst">${GST}</p>
      ${freeHere ? '' : quote && quote.percent ? `<div class="cl-ok">🎟️ ${quote.percent}% off with your code ${esc(quote.code)} ✓</div>` : `<p class="cl-small">🎟️ Have a free or discount code? <button type="button" class="cl-link" id="plCodeGo">Enter it in Me → Have a code?</button></p>`}
      <div class="cl-err" id="plErr" role="alert"></div>
      <p class="cl-small">One-time payment by Razorpay (UPI, cards, net banking). It does not renew by itself — we remind you before it ends.</p>
      ${window.SV_PLAY ? '' : '<p class="cl-small"><a href="pricing/" target="_blank" rel="noopener">See all plans on knowtopia.in/pricing</a></p>'}
      <button class="btn ghost" type="button" id="plX">Close</button>`);
    el.querySelector('#plX').onclick = C().closeSheet;
    const cg = el.querySelector('#plCodeGo');
    if (cg) cg.onclick = () => {
      C().closeSheet();
      try { (ST.profile && ST.profile.course === 'ca' && window.Ca && Ca.profile) ? Ca.profile() : meScreen(); } catch (e) {}
      setTimeout(() => { const c = D.getElementById('svCode'); if (c) { c.scrollIntoView({ block: 'center', behavior: 'smooth' }); const i = D.getElementById('clCode'); if (i) try { i.focus({ preventScroll: true }); } catch (e) {} } }, 350);
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
      const o = await C().call('/functions/v1/studyverse-pay', { method: 'POST', body: { action: 'order', plan: planId, code: quote ? quote.code : null, grade: gradeNow() || null } });
      if (o && o.error) throw new Error(o.error);
      if (o && o.paid) return done(o);                // 100% discount: unlocked without payment
      await loadRzp();
      const u = C().user() || {};
      const rz = new window.Razorpay({
        key: o.key_id, amount: o.amount, currency: 'INR', order_id: o.order_id, name: 'Knowtopia', description: o.label,
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

  /* ---------- plan bar: school World + Me; CA Journey home (under the greeting / Brain Snacks) + CA Profile ----------
     Never for parents. In the Play Store build (window.SV_PLAY) the bar shows the status only — no Subscribe / Renew button. */
  const btn = t => window.SV_PLAY ? '' : `<button type="button" data-pl>${t}</button>`;
  const leftLong = d => { const ms = new Date(d) - Date.now(); if (ms <= 0) return '0 min'; const h = Math.floor(ms / 36e5), m = Math.floor(ms % 36e5 / 6e4); return h >= 48 ? Math.ceil(ms / 864e5) + ' days' : (h ? h + ' h ' : '') + m + ' min'; };
  const freeLeft = kind => Math.min(FREE_PER_DAY, Math.max(0, FREE_PER_DAY - used(kind)));
  function barHTML(kind) {
    const a = access(kind);
    if (a.why === 'owner' || a.why === 'code') return '';
    if (a.why === 'trial') return `<p>🎁 <b>Free trial: ${left(a.until)} left.</b> Everything is unlocked.</p>${btn('Subscribe')}`;
    if (a.full) { const soon = a.until && new Date(a.until) - Date.now() < 7 * 864e5; return soon ? `<p>⏳ Your plan ends on <b>${dt(a.until)}</b>.</p>${btn('Renew')}` : ''; }
    return `<p><b>${freeLeft(kind)} of ${FREE_PER_DAY}</b> free questions left today.${a.trialEnded ? ' Trial ended.' : ''}</p>${btn('Subscribe')}`;
  }
  function caBarHTML() {                              // CA always shows where the student stands
    const a = access('ca');
    if (a.why === 'owner') return '<p>🔑 <b>Owner account</b> · everything is unlocked.</p>';
    if (a.why === 'code') return `<p>🎟️ <b>${lockName() || caName()}</b> · free access with your code${a.until ? ` till <b>${dt(a.until)}</b>` : ' — forever'}.</p>`;
    if (a.why === 'trial') return `<p>🎁 <b>Free trial — ${leftLong(a.until)} left.</b> All of ${caName()} is open.</p>${btn('Subscribe')}`;
    if (a.full) { const soon = a.until && new Date(a.until) - Date.now() < 7 * 864e5;
      return `<p>✅ <b>${planName(a, 'ca')}</b> · ${a.until ? `active till <b>${dt(a.until)}</b>` : 'active'}</p>${soon ? btn('Renew') : ''}`; }
    return `<p><b>Free plan</b> · ${freeLeft('ca')} of ${FREE_PER_DAY} questions left today</p>${btn('Subscribe')}`;
  }
  function place(sc, h, after) {
    let b = sc.querySelector(':scope > .sv-planbar');
    if (!h || !after) { if (b) b.remove(); return; }
    if (!b) { style(); b = D.createElement('div'); b.className = 'card sv-planbar'; b.setAttribute('role', 'region'); b.setAttribute('aria-label', 'Your plan'); }
    if (b.previousElementSibling !== after) after.after(b);
    if (b.dataset.h !== h) { b.dataset.h = h; b.innerHTML = h; const k = b.querySelector('[data-pl]'); if (k) k.onclick = () => open(); }
  }
  function bars() {
    if (!signedIn()) return;
    if (parent()) { D.querySelectorAll('.sv-planbar').forEach(b => b.remove()); return; }
    const kind = kindNow();
    D.querySelectorAll('#s-world > .sv-planbar').forEach(b => b.remove());   // the plan card lives on Me
    ['s-me'].forEach(id => {
      const sc = D.getElementById(id); if (!sc || !sc.firstElementChild) return;
      const h = kind === 'ca' ? '' : barHTML('school'); let b = sc.querySelector(':scope > .sv-planbar');
      if (!h) { if (b) b.remove(); return; }
      if (!b) { style(); b = D.createElement('div'); b.className = 'card sv-planbar'; b.setAttribute('role', 'region'); b.setAttribute('aria-label', 'Your plan'); const first = sc.querySelector(':scope > .card'); first ? first.after(b) : sc.prepend(b); }
      if (b.dataset.h !== h) { b.dataset.h = h; b.innerHTML = h; const k = b.querySelector('[data-pl]'); if (k) k.onclick = () => open(); }
    });
    const ca = D.getElementById('s-ca'); if (!ca) return;
    if (kind !== 'ca') { place(ca, '', null); return; }
    const top = ca.querySelector(':scope > .ca-top'), home = top && ca.querySelector(':scope > .ca-journey'), prof = ca.querySelector(':scope > .ca-prof');
    const snack = home ? ca.querySelector(':scope > #gkSnack') : null;
    place(ca, caBarHTML(), prof || null);
  }
  let warned = false;
  function remind() {
    if (!signedIn() || warned || parent()) return;
    const a = access(kindNow());
    if (a.why === 'trial' && a.until && new Date(a.until) - Date.now() < 3 * 36e5) { warned = true; say(window.SV_PLAY ? `Your free trial ends in ${left(a.until)}` : `Your free trial ends in ${left(a.until)} — subscribe to keep everything unlocked`); }
    else if (a.why === 'paid' && a.until && new Date(a.until) - Date.now() < 3 * 864e5) { warned = true; say(window.SV_PLAY ? `Your plan ends on ${dt(a.until)}` : `Your plan ends on ${dt(a.until)} — renew to keep learning without limits`); }
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
