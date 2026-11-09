/* ================= StudyVerse for Schools & Coaching (B2B) — js/inst.js =================
   1. Entry: after sign-in, rpc inst_me tells what the account is in. Institution admins and teachers land on the school
      console (full screen); if the account is also a parent, a picker asks "Parent Home or school console".
      Students' app is unchanged except a "🏫 School · Class 7-B" badge, a homework card (World / CA home) and a
      "My school" card on Me (opt-in leaderboard, join with a code). Parents are unchanged (Parent Hub keeps every link).
   2. Join codes: ?join=CODE (printed sheets / posters) or Me → "Join my school" → rpc inst_join.
      Parent emails from the school: ?pinvite=1&email=… opens "Create account" as Parent; rpc inst_claim links on sign-in.
   3. Admin console: Overview (seats by band, active %, class comparison), Classes & teachers, Students (roster, bulk upload
      CSV / paste → edge function institution-bulk, printable roll-number code sheet), Join codes, Orders (live quote →
      Request invoice → institution-notify emails the owner), printable invoice, School details.
   4. Owner panel (studyverse.admins): institutions, create + first admin invite, 30-day pilot for one class, orders,
      mark paid, seller GSTIN / state.
   Prices are decided on the server (rpc quote_order / create_order); this file only shows them. */
(function () {
  'use strict';
  const D = document, LS = localStorage, SS = sessionStorage;
  const SITE = 'https://study.moneyviel.com/';
  const C = () => window.Cloud || null;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const say = m => { try { toast(m); } catch (e) {} };
  const one = r => Array.isArray(r) ? r[0] : r;
  const rpc = (n, b) => C().rest('rpc/' + n, { method: 'POST', body: b || {} });
  const fn = (n, b) => C().call('/functions/v1/' + n, { method: 'POST', body: b });
  const jget = (k, d, st = LS) => { try { const v = JSON.parse(st.getItem(k)); return v == null ? d : v; } catch (e) { return d; } };
  const jset = (k, v, st = LS) => { try { v == null ? st.removeItem(k) : st.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const S = () => { try { return ST; } catch (e) { return null; } };
  const signedIn = () => !!(C() && C().signedIn() && !LS.getItem('sv_demo'));
  const uid = () => { const u = C() && C().user(); return u ? u.id : null; };
  const errT = e => (e && e.status != null && C()) ? C().errText(e) : ((e && e.message) || 'Something went wrong.');
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  const pad2 = n => String(n).padStart(2, '0');
  const dk = t => { const d = new Date(t); return `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`; };
  const todayK = () => dk(Date.now());
  const fmtD = iso => iso ? new Date(String(iso).length === 10 ? iso + 'T12:00:00' : iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : '';
  const inr = (n, dec) => '₹' + Number(n || 0).toLocaleString('en-IN', { minimumFractionDigits: dec ? 2 : 0, maximumFractionDigits: 2 });
  const BANDS = [['1-5', 'Class 1–5', 100], ['6-8', 'Class 6–8', 125], ['9-10', 'Class 9–10', 175], ['11-12', 'Class 11–12', 225], ['ca', 'CA Foundation coaching', 250]];
  const bandOf = course => course === 'ca-foundation' ? 'ca' : (g => g <= 5 ? '1-5' : g <= 8 ? '6-8' : g <= 10 ? '9-10' : '11-12')(+String(course || '').slice(8));
  const STATES = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'];
  const stateOpts = cur => `<option value="">— Choose —</option>${STATES.map(s => `<option${s === cur ? ' selected' : ''}>${esc(s)}</option>`).join('')}`;
  const ay = () => { const d = new Date(), y = d.getMonth() >= 3 ? d.getFullYear() : d.getFullYear() - 1; return [y, y + 1].map(a => `${a}-${pad2((a + 1) % 100)}`); };

  /* ================= pure helpers (unit-tested) ================= */
  /* CSV or pasted rows (comma or tab). With a header row the columns are found by name; without one the order is
     name, class, section, roll no, student email, parent email. Class: 1–12 or "CA". */
  function splitLine(line, sep) {
    const out = []; let cur = '', q = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (q) { if (ch === '"' && line[i + 1] === '"') { cur += '"'; i++; } else if (ch === '"') q = false; else cur += ch; }
      else if (ch === '"') q = true; else if (ch === sep) { out.push(cur); cur = ''; } else cur += ch;
    }
    out.push(cur); return out.map(x => x.trim());
  }
  function parseRows(text) {
    const lines = String(text || '').replace(/^﻿/, '').split(/\r?\n/).map((l, i) => ({ l, n: i + 1 })).filter(x => x.l.trim());
    if (!lines.length) return { rows: [], errors: [{ line: 0, msg: 'The list is empty.' }] };
    const sep = lines[0].l.includes('\t') ? '\t' : lines[0].l.includes(';') && !lines[0].l.includes(',') ? ';' : ',';
    let cols = { name: 0, class: 1, section: 2, roll: 3, email: 4, parent_email: 5 }, body = lines;
    const h = splitLine(lines[0].l, sep).map(x => x.toLowerCase());
    if (h.some(x => /name/.test(x)) && h.some(x => /class|grade|std|batch/.test(x))) {
      const find = re => h.findIndex(re);
      cols = { name: find(x => /name/.test(x) && !/parent|guardian|father|mother/.test(x)), class: find(x => /class|grade|std/.test(x)), section: find(x => /section|batch|div/.test(x)),
        roll: find(x => /roll/.test(x)), email: find(x => /mail/.test(x) && !/parent|guardian|father|mother/.test(x)), parent_email: find(x => /parent|guardian|father|mother/.test(x)) };
      if (cols.class < 0) cols.class = find(x => /batch/.test(x));
      body = lines.slice(1);
    }
    const rows = [], errors = [];
    if (body.length > 500) errors.push({ line: 0, msg: `Up to 500 students per upload (this list has ${body.length}).` });
    body.slice(0, 500).forEach(({ l, n }) => {
      const c = splitLine(l, sep), g = k => cols[k] >= 0 ? (c[cols[k]] || '').trim() : '';
      const r = { line: n, name: g('name').replace(/\s+/g, ' ').slice(0, 60), class: g('class').replace(/^class\s*/i, '').trim(), section: g('section').slice(0, 40), roll: g('roll').slice(0, 20), email: g('email').toLowerCase(), parent_email: g('parent_email').toLowerCase() };
      const why = [];
      if (!r.name) why.push('name is missing');
      if (/^ca(\b|[\s-])|^ca$/i.test(r.class)) r.class = 'CA'; else if (!/^([1-9]|1[0-2])$/.test(r.class)) why.push('class must be 1 to 12 or CA');
      if (r.email && !EMAIL_RE.test(r.email)) why.push('student email does not look right');
      if (r.parent_email && !EMAIL_RE.test(r.parent_email)) why.push('parent email does not look right');
      if (r.email && r.email === r.parent_email) why.push('parent email is the same as the student email');
      if (why.length) errors.push({ line: n, msg: why.join(', ') }); else rows.push(r);
    });
    return { rows, errors };
  }
  /* Indian-format amount in words: 1,30,500 → "One Lakh Thirty Thousand Five Hundred" */
  function words(num) {
    const a = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'];
    const b = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];
    const two = x => x < 20 ? a[x] : b[Math.floor(x / 10)] + (x % 10 ? '-' + a[x % 10] : '');
    const three = x => (x >= 100 ? a[Math.floor(x / 100)] + ' Hundred' + (x % 100 ? ' ' + two(x % 100) : '') : two(x));
    const w = n => { if (!n) return 'Zero'; const cr = Math.floor(n / 1e7), lk = Math.floor(n / 1e5) % 100, th = Math.floor(n / 1e3) % 100, rest = n % 1000, out = [];
      if (cr) out.push(w(cr) + ' Crore'); if (lk) out.push(two(lk) + ' Lakh'); if (th) out.push(two(th) + ' Thousand'); if (rest) out.push(three(rest)); return out.join(' '); };
    const rs = Math.floor(Math.round(num * 100) / 100), ps = Math.round((num - rs) * 100);
    return `Indian Rupees ${w(rs)}${ps ? ' and ' + two(ps) + ' Paise' : ''} Only`;
  }

  /* ================= styles ================= */
  const css = `
.in-hub .pv-top h1{display:flex;flex-direction:column;line-height:1.15}.in-sub{font-size:12.5px;font-weight:600;opacity:.85;font-family:Nunito,system-ui,sans-serif}
.in-tabs{position:sticky;top:64px;z-index:1;background:#F6F0E4;margin:0 -14px;padding:10px 14px 6px}
.in-cls{display:grid;grid-template-columns:1fr auto;text-align:left;cursor:pointer;min-height:64px;font:inherit;color:#15161C;width:100%}.in-cls b{font-size:18px}.in-cls .pv-mut{grid-column:1}.in-go{grid-row:1/span 2;grid-column:2;align-self:center;font-size:26px;color:#8A6A2E}
.in-name{background:none;border:0;padding:6px 2px;min-height:44px;font:inherit;font-weight:800;color:#5B0F1B;text-decoration:underline;text-underline-offset:2px;cursor:pointer;text-align:left}
.in-names{display:flex;flex-wrap:wrap;gap:0 10px}
.in-quad{position:relative;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px;padding:0 0 22px 22px}.in-q .in-name{overflow-wrap:anywhere}
.in-q{border-radius:14px;padding:10px 12px;border:1px solid #eadfca;min-width:0}.in-q h4{margin:0 0 4px!important;display:flex;justify-content:space-between;gap:6px;align-items:center}.in-q p{font-size:12.5px!important;margin:0 0 4px!important}
.in-q.star{background:#e8f5ec}.in-q.coast{background:#eef4fb}.in-q.hard{background:#fff4dc}.in-q.risk{background:#fbe9ea}
.in-ax{position:absolute;font-size:12px;font-weight:800;color:#5d5a55}.in-ax.y{left:-14px;top:50%;transform:rotate(-90deg) translateX(50%);transform-origin:left top;white-space:nowrap}.in-ax.x{bottom:0;right:4px}
.in-why{margin:2px 0 4px;padding-left:18px}.in-why li{border:0!important;padding:2px 0!important;font-size:14px}
.in-dist{display:flex;height:16px;border-radius:9px;overflow:hidden;gap:2px;margin:6px 0 8px;background:#f1eadc}.in-dist i{display:block;height:100%}
.in-dist .ok,.pv-sw.in-ok{background:#2e9a5c}.in-dist .warn,.pv-sw.in-warn{background:#d9a227}.in-dist .bad,.pv-sw.in-bad{background:#c0392b}.in-dist .none,.pv-sw.in-none{background:#cfc6b4}
.in-hscroll{overflow-x:auto;max-width:100%;border-radius:10px}.in-hscroll:focus-visible{outline:3px solid #1a5fd0}
.in-heat{border-collapse:separate;border-spacing:2px;font-size:12px}.in-heat th[scope=row]{position:sticky;left:0;background:#fff;text-align:left;white-space:nowrap;z-index:1;padding-right:6px}
.in-heat thead th{font-size:11px;color:#5d5a55;font-weight:700;padding:2px}.in-hc{width:30px;min-width:30px;height:30px;text-align:center;border-radius:6px;font-weight:800}
.in-hc.m0{background:#fff;border:1px solid #e3d9c4;color:#a39b8b}.in-hc.m1{background:#e3f1e7;color:#1d4d30}.in-hc.m2{background:#8fcfa6;color:#0f3a22}.in-hc.m3{background:#17603a;color:#fff}
.in-keys{columns:2;font-size:12.5px;margin:4px 0;padding-left:22px}
.in-tbl{width:100%;border-collapse:collapse;font-size:13.5px}.in-tbl th,.in-tbl td{text-align:left;padding:6px 6px;border-top:1px solid #f0e8d8;vertical-align:middle}.in-tbl th{color:#5d5a55;font-size:12.5px;white-space:nowrap}
.in-mini{display:inline-block;width:50px;vertical-align:middle}
.in-lbl{display:block;font-weight:700;font-size:13px;margin:8px 0 4px}
.in-badge{display:flex;align-items:center;gap:8px;margin:6px 0 10px;padding:8px 12px;border-radius:12px;background:#F4EAD8;color:#5B0F1B;font-weight:800;font-size:14.5px;border:1px solid #e2d3b5}
.card.in-hw{border-left:5px solid #2a6fb0}.in-hwi{display:flex;gap:10px;align-items:center;justify-content:space-between;padding:8px 0;border-top:1px solid rgba(0,0,0,.08)}.in-hwi:first-of-type{border-top:0}
.in-hwi .btn{flex:none;min-height:44px;width:auto;padding:0 16px}.in-hwi small{display:block;opacity:.75}.in-late{color:#B71C2C;font-weight:800}
.in-me .pv-row .btn{flex:1 1 180px}.in-sw{display:flex;align-items:center;gap:10px;min-height:44px;font-size:14.5px;cursor:pointer}.in-sw input{width:22px;height:22px}
.in-band{display:grid;grid-template-columns:1fr auto;gap:2px 8px;align-items:center;padding:8px 0;border-top:1px solid #f0e8d8}.in-band:first-child{border-top:0}.in-band .pv-sbar{grid-column:1/-1}
.in-qt{width:100%;border-collapse:collapse;font-size:14px;margin:6px 0}.in-qt td,.in-qt th{padding:5px 4px;border-top:1px solid #f0e8d8;text-align:right}.in-qt td:first-child,.in-qt th:first-child{text-align:left}.in-qt tr.tot td{font-weight:800;font-size:16px;border-top:2px solid #15161C}
.in-num{display:grid;grid-template-columns:1fr 110px;gap:6px 10px;align-items:center}.in-num label{font-weight:700;font-size:14px}.in-num small{display:block;font-weight:600;color:#5d5a55}
.in-codes{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}.in-code{border:2px dashed #C9A76A;border-radius:12px;padding:8px;text-align:center;background:#FBF7EF}.in-code b{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:20px;letter-spacing:2px;color:#5B0F1B}
.in-pill{display:inline-block;font-weight:800;font-size:12.5px;padding:2px 8px;border-radius:999px;background:#F4EAD8;color:#5B0F1B}.in-pill.ok{background:#e8f5ec;color:#1d5e36}.in-pill.warn{background:#fff4dc;color:#6b4a06}.in-pill.bad{background:#fbe9ea;color:#7a0f1a}
.in-inv{font-size:13.5px}.in-inv h2{font-size:22px!important}.in-inv table{width:100%;border-collapse:collapse;margin:8px 0}.in-inv th,.in-inv td{border:1px solid #e2d6bd;padding:6px;text-align:left;vertical-align:top}.in-inv td.r,.in-inv th.r{text-align:right}
.in-inv .two{display:grid;grid-template-columns:1fr 1fr;gap:10px}.in-inv .box{border:1px solid #e2d6bd;border-radius:10px;padding:8px 10px}.in-inv .box h4{margin:0 0 4px!important;font-size:12px;text-transform:uppercase;color:#5d5a55;letter-spacing:.04em}
textarea.pv-in{min-height:120px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px}
.in-err{color:#B71C2C;font-size:13.5px}.in-ok{color:#1d5e36;font-weight:800}
.in-staff{display:flex;flex-wrap:wrap;gap:6px}.in-chipb{min-height:44px;padding:0 12px;border-radius:999px;border:1.5px solid #C9A76A;background:#fff;font:inherit;font-weight:700;cursor:pointer;color:#15161C}.in-chipb[aria-pressed=true]{background:#15161C;color:#F4EAD8;border-color:#15161C}
@media (max-width:420px){.in-inv .two{grid-template-columns:1fr}.in-keys{columns:1}.in-q{padding:8px}.in-q p{display:none}}
.in-hub .pv-body{grid-template-columns:minmax(0,1fr)}.in-hub .pv-card{min-width:0}
@media (min-width:900px){.in-hub .pv-body>.in-wide{column-span:all}}
@media print{#pvPrint.in-print{font-family:system-ui,Arial,sans-serif!important;font-size:11pt}#pvPrint.in-print table{width:100%;border-collapse:collapse;margin:6pt 0}#pvPrint.in-print th,#pvPrint.in-print td{border:1px solid #999;padding:4pt;text-align:left;vertical-align:top}
#pvPrint.in-print td.r,#pvPrint.in-print th.r{text-align:right}#pvPrint.in-print .two{display:grid;grid-template-columns:1fr 1fr;gap:8pt}#pvPrint.in-print .box{border:1px solid #999;padding:6pt}#pvPrint.in-print .box h4{margin:0 0 3pt;font-size:9pt;text-transform:uppercase}
#pvPrint.in-print .in-codes{display:grid;grid-template-columns:repeat(3,1fr);gap:6pt}#pvPrint.in-print .in-code{border:1.5px dashed #555;padding:8pt;break-inside:avoid;text-align:center}#pvPrint.in-print .in-code b{font-size:16pt;letter-spacing:2pt;display:block}
#pvPrint.in-print .in-poster{text-align:center;padding-top:30mm}#pvPrint.in-print .in-poster b{font-size:54pt;letter-spacing:6pt;display:block;margin:10mm 0}
#pvPrint.in-print .in-sign{display:flex;justify-content:space-between;margin-top:24mm}#pvPrint.in-print .in-sign span{border-top:1px solid #000;padding-top:3pt;width:40%;text-align:center}
#pvPrint.in-print .in-pill{border:1px solid #999;background:none}}`;
  function style() { if (window.Parent && Parent.lib) Parent.lib.style(); if (D.getElementById('inCss')) return; const s = D.createElement('style'); s.id = 'inCss'; s.textContent = css; D.head.appendChild(s); }

  /* ================= memberships ================= */
  const MK = 'sv_inst';
  let me = null, booted = null;
  function cached() { const c = jget(MK, null); return c && c.uid === uid() ? c.d : null; }
  async function refreshMe() {
    try { const r = one(await rpc('inst_me')); if (r && Array.isArray(r.memberships)) { me = r; jset(MK, { uid: uid(), d: r, at: Date.now() }); } }
    catch (e) { if (!me) me = cached(); }
    return me;
  }
  const mem = () => (me && me.memberships) || [];
  const studentM = () => mem().filter(m => m.role === 'student');
  const staffM = () => mem().filter(m => m.role === 'admin' || m.role === 'teacher');

  /* ================= student side ================= */
  let hw = jget('sv_hw', null);   // { uid, at, list }
  const myHw = () => hw && hw.uid === uid() ? hw.list || [] : [];
  async function pullHw() {
    if (!signedIn() || !studentM().length) return;
    try { const r = await rpc('my_homework'); if (Array.isArray(r)) { hw = { uid: uid(), at: Date.now(), list: r }; jset('sv_hw', hw); paint(); } } catch (e) {}
  }
  const tMatch = (t, id) => { if (!id) return false; const m = /^(\d+)-([a-z]+)-(\d+)$/.exec(t);
    if (m) { const x = /^g(\d+)-([a-z]+)-(\d+)/.exec(id); return !!x && +x[1] === +m[1] && x[2] === m[2] && +x[3] === +m[3]; }
    return id === t || id.startsWith(t + '-'); };
  const hwDoneLocal = h => { const s = S(); return !!(h.done_at || (s && s.hwDone && s.hwDone[h.id])); };
  /* done = `need` answers in the chapter / unit since the homework was set (or a finished quest for "practise the chapter") */
  function hwCheck() {
    const s = S(); if (!s || !s.profile) return;
    myHw().forEach(h => {
      if (h.done_at) return;
      if (s.hwDone && s.hwDone[h.id]) { if (!h._sent) { h._sent = 1; rpc('homework_done', { p_id: h.id }).then(() => { h.done_at = new Date().toISOString(); jset('sv_hw', hw); }, () => { h._sent = 0; }); } return; }
      const setMin = Math.floor(new Date(h.set_at || 0).getTime() / 6e4) || 0, sd = dk(setMin * 6e4);
      const count = l => { let n = 0; if (Array.isArray(l)) for (let i = l.length - 1; i >= 0; i--) { const x = l[i]; if (!Array.isArray(x) || x[0] < setMin) break; if (tMatch(h.target, String(x[1] || '').split('#')[0])) n++; } return n; };
      const n = Math.max(count(s.ans) + count(s.ca && s.ca.mlog), count(s.ins && s.ins.att));
      const quest = h.kind === 'chapter' && Object.entries(s.topics || {}).some(([tid, t]) => t && t.last && t.last >= sd && tMatch(h.target, tid));
      if (n >= (+h.need || 3) || quest) {
        if (!s.hwDone || typeof s.hwDone !== 'object') s.hwDone = {}; s.hwDone[h.id] = todayK(); try { save(); } catch (e) {}
        say('Homework done ✓ Your teacher can see it'); h._sent = 1;
        rpc('homework_done', { p_id: h.id }).then(() => { h.done_at = new Date().toISOString(); jset('sv_hw', hw); paint(); }, () => { h._sent = 0; });
      }
    });
  }
  async function openHw(h) {
    const s = S(); const m = /^(\d+)-([a-z]+)-(\d+)$/.exec(h.target);
    if (!m) { if (window.Ca && Ca.unit) Ca.unit(h.target.split('-').length > 3 ? h.target : h.target, 'mcq'); return; }
    if (s && s.profile && +m[1] !== +s.profile.grade) { say(`This homework is for Class ${m[1]}.`); return; }
    try {
      const d = await subjectData(+m[1], m[2]), ci = d ? d.chapters.findIndex(x => +x.n === +m[3]) : -1;
      if (ci < 0) { say('This chapter is coming soon.'); return; }
      (window.chapterScreen || chapterScreen)(m[2], ci);
    } catch (e) { say('Could not open the chapter. Please try again.'); }
  }
  function badgeHTML() { const m = studentM()[0]; return m ? `<span aria-hidden="true">🏫</span><span>${esc(m.name)} · ${/^ca-/.test(m.course || '') ? esc(m.class_name) : 'Class ' + esc(m.class_name)}</span>` : ''; }
  function hwHTML() {
    const list = myHw(), today = todayK(), s = S(); if (!list.length || !s || !s.profile) return '';
    const isCa = s.profile.course === 'ca', mine = list.filter(h => /^\d+-/.test(h.target) !== isCa);
    const open = mine.filter(h => !hwDoneLocal(h) && h.due_date >= dk(Date.now() - 7 * 864e5)), done = mine.filter(hwDoneLocal);
    if (!open.length && !done.length) return '';
    return `<h3>📝 Homework from your teacher</h3>${open.slice(0, 4).map(h => `<div class="in-hwi"><div><b>${esc(h.title)}</b><small>${esc(h.subject || '')}${h.subject ? ' · ' : ''}${h.due_date < today ? `<span class="in-late">was due ${esc(fmtD(h.due_date))}</span>` : h.due_date === today ? 'due today' : 'due ' + esc(fmtD(h.due_date))}</small></div><button type="button" class="btn" data-inhw="${esc(h.id)}">Start ▶</button></div>`).join('')}
      ${done.length ? `<p class="sub" style="margin:8px 0 0">✅ Done: ${done.slice(0, 3).map(h => esc(h.title)).join(', ')}${done.length > 3 ? ` +${done.length - 3}` : ''}</p>` : ''}`;
  }
  function place(host, after, cls, html, wire) {
    let b = host.querySelector(':scope > .' + cls);
    if (!html) { if (b) b.remove(); return; }
    if (!b) { style(); b = D.createElement('div'); b.className = cls === 'in-badge' ? 'in-badge' : 'card ' + cls; if (cls === 'in-badge') b.setAttribute('role', 'note'); }
    if (after) { if (after.nextElementSibling !== b) after.after(b); } else if (!b.isConnected) host.prepend(b);
    if (b.dataset.h !== html) { b.dataset.h = html; b.innerHTML = html; if (wire) wire(b); }
  }
  const wireHw = b => b.querySelectorAll('[data-inhw]').forEach(x => x.onclick = () => { const h = myHw().find(y => y.id === x.dataset.inhw); if (h) openHw(h); });
  function meHTML() {
    const ms = studentM(), lb = ms.some(m => m.lb_opt);
    if (staffM().length && !ms.length) return `<h3>🏫 School console</h3><p class="sub">${esc(staffM().map(m => m.name).filter((v, i, a) => a.indexOf(v) === i).join(', '))}</p><div class="pv-row"><button class="btn" type="button" data-incons>Open school console</button></div>`;
    if (ms.length) return `<h3>🏫 My school</h3>${ms.map(m => `<p class="sub" style="margin:0 0 4px"><b>${esc(m.name)}</b> · ${/^ca-/.test(m.course || '') ? esc(m.class_name) : 'Class ' + esc(m.class_name)}</p>`).join('')}
      <label class="in-sw"><input type="checkbox" id="inLb"${lb ? ' checked' : ''}> Show my first name on the class leaderboard</label>
      <button class="cl-link" type="button" data-injoin>Join another class with a code</button>`;
    return `<h3>🏫 School or coaching class</h3><p class="sub">Did your teacher give you a class code? Join your class to get homework and your school's plan.</p>
      <div class="pv-row"><button class="btn ghost" type="button" data-injoin>Enter class code</button></div>`;
  }
  function wireMe(b) {
    b.querySelectorAll('[data-injoin]').forEach(x => x.onclick = () => joinSheet(''));
    b.querySelectorAll('[data-incons]').forEach(x => x.onclick = () => { SS.removeItem('sv_inst_app'); consoleOpen(null, true); });
    const lb = b.querySelector('#inLb');
    if (lb) lb.onchange = async () => { lb.disabled = true; try { const r = one(await rpc('inst_set_leaderboard', { p_on: lb.checked })); if (!r || !r.ok) throw 0; mem().forEach(m => { if (m.role === 'student') m.lb_opt = lb.checked; }); jset(MK, { uid: uid(), d: me, at: Date.now() }); say(lb.checked ? 'You are on the class leaderboard' : 'Leaderboard is off'); } catch (e) { lb.checked = !lb.checked; say('Could not save. Please try again.'); } finally { lb.disabled = false; } };
  }
  function ownerHTML() { return `<h3>🏫 Schools &amp; coaching (owner)</h3><p class="sub">Institutions, pilots, orders and invoices.</p><button class="btn" type="button" id="inOwnerGo">Open schools panel</button>`; }
  function paint() {
    if (!signedIn() || (C().isParent && C().isParent())) return;
    try { hwCheck(); } catch (e) {}
    const w = D.getElementById('s-world');
    if (w && w.querySelector('#worldTitle')) {
      place(w, w.querySelector('#worldTitle'), 'in-badge', badgeHTML());
      place(w, w.querySelector(':scope > .in-badge') || w.querySelector('#worldTitle'), 'in-hw', hwHTML(), wireHw);
    }
    const ca = D.getElementById('s-ca');
    if (ca && ca.querySelector('.ca-journey')) {
      const firstCard = ca.querySelector(':scope > .card:not(.in-hw):not(.pv-goal)');
      place(ca, firstCard, 'in-badge', badgeHTML());
      place(ca, ca.querySelector(':scope > .in-badge') || firstCard, 'in-hw', hwHTML(), wireHw);
    } else if (ca) ca.querySelectorAll(':scope > .in-hw, :scope > .in-badge').forEach(x => { if (!ca.querySelector('.ca-prof')) x.remove(); });
    const meS = D.getElementById('s-me');
    const hosts = [meS && meS.firstElementChild ? meS : null, ca && ca.querySelector('.ca-prof') ? ca : null].filter(Boolean);
    hosts.forEach(h => {
      place(h, h.querySelector(':scope > .pv-me') || D.getElementById('svCode') || h.querySelector(':scope > .statrow'), 'in-me', meHTML(), wireMe);
      if (C().admin()) place(h, h.querySelector(':scope > .in-me'), 'in-own', ownerHTML(), b => { b.querySelector('#inOwnerGo').onclick = () => owner(); });
    });
  }

  /* ---------- join with a code ---------- */
  function joinSheet(code) {
    if (!signedIn()) { jset('sv_join', String(code || '')); C() && C().open('in'); return; }
    style();
    const el = C().sheet(`<h3 id="clT">🏫 Join your class</h3><p>Enter the 8-letter code from your school or teacher.</p>
      <form id="inJF" novalidate><label for="inJC">Class code</label><input class="cl-in pv-code-in" id="inJC" maxlength="9" autocapitalize="characters" autocomplete="off" spellcheck="false" value="${esc(code || '')}" placeholder="ABCD2345">
      <label for="inJN">Your name (as in the class register)</label><input class="cl-in" id="inJN" maxlength="60" autocomplete="name" value="${esc((S() && S().profile && S().profile.name) || '')}">
      <label for="inJR">Roll number (optional)</label><input class="cl-in" id="inJR" maxlength="20" inputmode="numeric" autocomplete="off">
      <div class="cl-err" id="inJE" role="alert"></div><button class="btn" type="submit" id="inJGo">Join</button></form><div style="height:8px"></div><button class="btn ghost" type="button" id="inJX">Cancel</button>`);
    el.querySelector('#inJX').onclick = C().closeSheet;
    el.querySelector('#inJF').onsubmit = async ev => {
      ev.preventDefault(); const e = el.querySelector('#inJE'), go = el.querySelector('#inJGo');
      const c = el.querySelector('#inJC').value.toUpperCase().replace(/[\s-]/g, ''), n = el.querySelector('#inJN').value.trim(), r = el.querySelector('#inJR').value.trim();
      e.textContent = ''; if (!/^[A-Z0-9]{8}$/.test(c)) { e.textContent = 'The code has 8 letters or numbers.'; return; }
      go.disabled = true;
      try {
        const res = one(await rpc('inst_join', { p_code: c, p_name: n || null, p_roll: r || null }));
        if (!res || !res.ok) { e.textContent = (res && res.msg) || 'This code is not valid.'; return; }
        jset('sv_join', null); C().closeSheet();
        say(res.role === 'teacher' ? `Welcome to ${res.institution} ✓` : `Joined ${res.institution} · ${res.class} ✓`);
        try { C().refreshAccess && C().refreshAccess(); } catch (x) {}
        await refreshMe(); pullHw(); paint(); if (res.role === 'teacher') route(true);
      } catch (x) { e.textContent = errT(x); }
      finally { go.disabled = false; }
    };
  }

  /* ================= entry & routing ================= */
  function route(force) {
    const st = staffM(); if (!st.length) return;
    if (C().isParent && C().isParent()) {
      parentButton();
      if (force || !SS.getItem('sv_inst_pick')) { SS.setItem('sv_inst_pick', '1'); picker(); }
      return;
    }
    if (!force && SS.getItem('sv_inst_app')) return;     // chose "use the student app" in this tab
    consoleOpen(null, true);
  }
  function picker() {
    style();
    const el = C().sheet(`<h3 id="clT">Where do you want to go?</h3><p>Your account is a parent and works at a school.</p>
      <button class="cl-pick" type="button" data-pk="parent"><b>👨‍👩‍👧 Parent Home</b><small>Your children's progress</small></button>
      <button class="cl-pick" type="button" data-pk="school"><b>🏫 School console</b><small>${esc(staffM().map(m => m.name).filter((v, i, a) => a.indexOf(v) === i).join(', '))}</small></button>`);
    el.querySelectorAll('[data-pk]').forEach(b => b.onclick = () => { C().closeSheet(); if (b.dataset.pk === 'school') consoleOpen(null, true); });
  }
  function parentButton() {               // a way back to the console from Parent Home
    const a = D.getElementById('pvAcct'); if (!a || a.querySelector('#inToConsole')) return;
    const b = D.createElement('button'); b.className = 'pv-btn'; b.type = 'button'; b.id = 'inToConsole'; b.style.marginTop = '8px'; b.textContent = '🏫 Open school console';
    b.onclick = () => consoleOpen(null, true); a.querySelector('#pvOut') ? a.querySelector('#pvOut').before(b) : a.appendChild(b);
  }

  async function boot() {
    if (!signedIn()) { booted = null; return; }
    const u = uid(); if (!u || booted === u) return;
    if (C().role && C().role() == null) return;          // wait until cloud.js knows the account's role
    booted = u;
    me = cached(); paint();
    try { const r = one(await rpc('inst_claim')); if (r && r.linked > 0) { say(`Linked to ${r.linked} child${r.linked > 1 ? 'ren' : ''} from school ✓`); const b = D.getElementById('pvRef'); if (b) setTimeout(() => b.click(), 300); } } catch (e) {}
    await refreshMe(); paint(); pullHw();
    const j = jget('sv_join', null); if (j != null && !(C().isParent && C().isParent())) { jset('sv_join', null); joinSheet(j); }
    route();
  }

  /* ================= school console (admin + teacher) ================= */
  let hub = null, ctx = null, tab = 'overview', pinned = false, cache = {};
  function consoleOpen(instId, pin) {
    if (!signedIn()) return;
    style(); pinned = !!pin;
    const st = staffM(); if (!st.length && !C().admin()) return;
    const insts = {}; st.forEach(m => { const x = insts[m.institution_id] || (insts[m.institution_id] = { id: m.institution_id, name: m.name, type: m.type, status: m.status, admin: false, classes: [] }); if (m.role === 'admin') x.admin = true; (m.classes || []).forEach(c => { if (!x.classes.some(y => y.id === c.id)) x.classes.push(c); }); });
    if (instId && !insts[instId] && C().admin()) insts[instId] = { id: instId, name: 'Institution', admin: true, classes: [], owner: true };
    const list = Object.values(insts); if (!list.length) return;
    ctx = { list, inst: insts[instId] || (ctx && insts[ctx.inst.id]) || list.find(x => x.admin) || list[0] };
    if (!hub) { hub = D.createElement('div'); hub.className = 'sheet pv-hub in-hub'; hub.id = 'inHub'; hub.setAttribute('role', 'dialog'); hub.setAttribute('aria-modal', 'true'); hub.setAttribute('aria-labelledby', 'inT'); D.body.appendChild(hub); }
    hub.toggleAttribute('data-pinned', pinned); hub.toggleAttribute('data-nonav', pinned);
    hub.classList.add('show');
    tab = ctx.inst.admin ? (tab || 'overview') : 'classes';
    if (!ctx.inst.admin) tab = 'classes';
    cache = {}; render();
  }
  function consoleClose() { if (hub) hub.classList.remove('show'); }
  const ATABS = [['overview', 'Overview'], ['classes', 'Classes & teachers'], ['students', 'Students'], ['codes', 'Join codes'], ['orders', 'Orders & invoices'], ['details', 'School details']];
  function render() {
    const I = ctx.inst, tabs = I.admin ? ATABS : [['classes', 'My classes']];
    hub.innerHTML = `<div class="pv-wrap"><div class="pv-top">${pinned ? '<span class="pv-logo" aria-hidden="true">Study<b>Verse</b></span>' : '<button class="pv-back" type="button" id="inBack">← Back</button>'}
      <h1 id="inT"><span>🏫 ${esc(I.name)}</span><small class="in-sub">${I.admin ? 'Admin console' : 'Teacher'}${I.owner ? ' · owner view' : ''}</small></h1><button class="pv-ref" type="button" id="inRef" aria-label="Refresh">⟳</button></div>
      ${ctx.list.length > 1 ? `<label class="in-lbl" for="inPick">Institution</label><select id="inPick" class="pv-in">${ctx.list.map(x => `<option value="${esc(x.id)}"${x === I ? ' selected' : ''}>${esc(x.name)}${x.admin ? ' (admin)' : ''}</option>`).join('')}</select>` : ''}
      <div class="pv-tabs in-tabs" role="tablist" aria-label="Console sections">${tabs.map(([k, n]) => `<button type="button" role="tab" id="int-${k}" aria-controls="inBody" aria-selected="${k === tab}" class="pv-tab${k === tab ? ' on' : ''}" data-tab="${k}">${n}</button>`).join('')}</div>
      <div id="inBody" class="pv-body" role="tabpanel" aria-labelledby="int-${tab}"><p class="pv-load" role="status">Loading…</p></div>
      <section class="pv-card" id="inAcct"><h3>👤 Your account</h3><p>${esc(C().email())}</p><div class="pv-row">${pinned && !(C().isParent && C().isParent()) ? '<button class="pv-btn ghost" type="button" id="inApp">Use the student app</button>' : ''}${pinned && C().isParent && C().isParent() ? '<button class="pv-btn ghost" type="button" id="inPar">Open Parent Home</button>' : ''}<button class="pv-btn ghost" type="button" id="inOut">Sign out</button></div>
        <p class="pv-note" style="margin-top:10px">Help: <a href="mailto:support@moneyviel.com">support@moneyviel.com</a></p></section></div>`;
    const bk = hub.querySelector('#inBack'); if (bk) bk.onclick = consoleClose;
    hub.querySelector('#inRef').onclick = () => { cache = {}; refreshMe().then(() => consoleOpen(ctx.inst.id, pinned)); };
    const pk = hub.querySelector('#inPick'); if (pk) pk.onchange = () => { ctx.inst = ctx.list.find(x => x.id === pk.value); tab = ctx.inst.admin ? 'overview' : 'classes'; cache = {}; render(); };
    hub.querySelectorAll('[data-tab]').forEach(b => b.onclick = () => { tab = b.dataset.tab; render(); const t = hub.querySelector('#int-' + tab); if (t) t.focus(); });
    const ap = hub.querySelector('#inApp'); if (ap) ap.onclick = () => { SS.setItem('sv_inst_app', '1'); pinned = false; consoleClose(); say('Tap Me → School console to come back'); };
    const pp = hub.querySelector('#inPar'); if (pp) pp.onclick = consoleClose;
    const out = hub.querySelector('#inOut'); out.onclick = () => { if (!out.dataset.sure) { out.dataset.sure = 1; out.textContent = 'Tap again to sign out'; return; } out.disabled = true; jset(MK, null); jset('sv_hw', null); C().signOut(); };
    const body = hub.querySelector('#inBody');
    ({ overview: tOverview, classes: tClasses, students: tStudents, codes: tCodes, orders: tOrders, details: tDetails })[tab](body).catch(e => { body.innerHTML = `<div class="pv-card"><h2>Could not load</h2><p>${esc(errT(e))}</p></div>`; });
  }
  const I = () => ctx.inst;
  async function get(key, f) { if (!(key in cache)) cache[key] = await f(); return cache[key]; }
  const overviewData = () => get('ov', async () => { const r = one(await rpc('inst_overview', { p_inst: I().id })); if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not load.'); if (r.institution) { I().name = r.institution.name; } return r; });
  const rosterData = () => get('ro', async () => { const r = one(await rpc('inst_roster', { p_inst: I().id })); if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not load.'); return r; });
  const classesData = () => get('cl', async () => { const r = await C().rest(`inst_classes?select=*&institution_id=eq.${I().id}&order=course,section`); return Array.isArray(r) ? r : []; });
  const teachList = cls => cls.map(c => Object.assign({ inst: I().name }, c));
  function openTeach(classId) {
    const go = cls => { consoleClose(); window.Teach && Teach.open(teachList(cls), { classId, list: !classId, inst: I(), back: () => { hub.classList.add('show'); } }); };
    if (I().admin) classesData().then(go, e => say(errT(e))); else go(I().classes);
  }

  /* ---------- Overview ---------- */
  async function tOverview(body) {
    const o = await overviewData(), i = o.institution, act = o.students ? Math.round(o.active7 / o.students * 100) : 0;
    const status = i.status === 'active' ? ['ok', `Active · seats till ${fmtD(o.paid_until)}`] : i.status === 'pilot' ? (i.pilot_until && new Date(i.pilot_until) > new Date() ? ['warn', `Free pilot · ${esc(o.pilot_class || '')} till ${fmtD(i.pilot_until)}`] : ['warn', 'Not active yet — order seats or ask for a free pilot']) : ['bad', 'Expired — order seats to continue'];
    body.innerHTML = `<section class="pv-card" aria-labelledby="inOv"><h3 id="inOv">At a glance</h3><p><span class="in-pill ${status[0]}" id="inStatus">${status[1]}</span></p>
        <div class="pv-kpis"><div><b>${o.students}</b><span>Students</span></div><div><b>${o.teachers}</b><span>Teachers</span></div><div><b>${o.classes}</b><span>Classes</span></div>
          <div><b id="inAct">${act}%</b><span>Active in 7 days<br><small>${o.active7} of ${o.students}</small></span></div></div></section>
      <section class="pv-card" aria-labelledby="inSeats"><h3 id="inSeats">🎟️ Seats by class group</h3><div id="inSeatList">${o.seats.filter(s => s.total || s.students || s.pilot).map(s => `<div class="in-band"><b>${esc(s.label)}</b><span>${s.used} of ${s.total} seats used${s.pilot ? ` · ${s.pilot} on pilot` : ''}${s.students > s.used + s.pilot ? ` · <span class="in-err">${s.students - s.used - s.pilot} without a seat</span>` : ''}</span>
        <span class="pv-sbar" aria-hidden="true"><i style="width:${s.total ? Math.min(100, s.used / s.total * 100) : 0}%"></i></span></div>`).join('') || '<p class="pv-empty">No students or seats yet.</p>'}</div>
        <p class="pv-note">A student gets the app as soon as there is a free seat for their class group. Order more in “Orders &amp; invoices”.</p></section>
      <section class="pv-card" aria-labelledby="inTd"><h3 id="inTd">🧑‍🏫 Teacher dashboard</h3><p class="pv-mut">See any class: mastery heatmap, weak topics, homework, early warnings and reports.</p><button class="pv-btn" type="button" id="inTeach">Open teacher dashboard</button></section>
      <section class="pv-card" aria-labelledby="inCmp"><h3 id="inCmp">📊 Compare classes and sections</h3><p class="pv-mut">Activity, accuracy, time, readiness and homework side by side. For admins only.</p><button class="pv-btn ghost" type="button" id="inCmpGo">Compare classes</button><div id="inCmpOut"></div></section>`;
    body.querySelector('#inTeach').onclick = () => openTeach(null);
    body.querySelector('#inCmpGo').onclick = async () => {
      const out = body.querySelector('#inCmpOut'), btn = body.querySelector('#inCmpGo'); btn.disabled = true; out.innerHTML = '<p class="pv-load" role="status">Working it out…</p>';
      try {
        const cls = await classesData(), list = [];
        for (const c of cls) { const r = one(await rpc('class_progress', { p_class: c.id })); if (!r || !r.ok) continue; const Ms = []; for (const s of r.students || []) Ms.push(await Teach.lib.metrics(s, r.homework)); list.push({ cls: c, Ms }); }
        const rows = Teach.lib.compare(list), pc = v => v == null ? '–' : Math.round(v) + '%';
        out.innerHTML = rows.length ? `<div class="in-hscroll" tabindex="0" role="region" aria-label="Class comparison"><table class="in-tbl" id="inCmpT"><thead><tr><th scope="col">Class</th><th scope="col">Students</th><th scope="col">Active (week)</th><th scope="col">Correct</th><th scope="col">Time / student</th><th scope="col">Readiness</th><th scope="col">Homework</th></tr></thead>
          <tbody>${rows.map(r => `<tr><td><b>${esc(r.cls.name)}</b></td><td>${r.n}</td><td>${r.n ? Math.round(r.activeWeek / r.n * 100) + '%' : '–'}</td><td>${pc(r.acc7)}</td><td>${Math.round(r.avgMin7)} min</td><td>${r.avgReadiness == null ? '–' : Math.round(r.avgReadiness)}</td><td>${pc(r.hwRate)}</td></tr>`).join('')}</tbody></table></div>` : '<p class="pv-empty">No classes yet.</p>';
      } catch (e) { out.innerHTML = `<p class="in-err">${esc(errT(e))}</p>`; }
      finally { btn.disabled = false; }
    };
  }

  /* ---------- Classes & teachers ---------- */
  async function tClasses(body) {
    if (!I().admin) {
      const cls = I().classes;
      body.innerHTML = `<section class="pv-card"><h3>Your classes</h3>${cls.length ? cls.map(c => `<button class="pv-card in-cls" type="button" data-cls="${esc(c.id)}"><b>${esc(c.name)}</b><span class="pv-mut">${/^ca-/.test(c.course) ? 'CA Foundation batch' : 'Class ' + esc(c.grade)}</span><span class="in-go" aria-hidden="true">›</span></button>`).join('') : '<p class="pv-empty">No classes yet. Ask your school admin to add you to a class.</p>'}</section>
        <section class="pv-card"><h3>Class join code</h3><p class="pv-mut">Make a code your students type in their app (Me → School or coaching class).</p>
          <label class="in-lbl" for="inTcC">Class</label><select id="inTcC" class="pv-in">${cls.map(c => `<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('')}</select><button class="pv-btn" type="button" id="inTcGo"${cls.length ? '' : ' disabled'}>Make code</button><div id="inTcOut"></div></section>`;
      body.querySelectorAll('[data-cls]').forEach(b => b.onclick = () => openTeach(b.dataset.cls));
      body.querySelector('#inTcGo').onclick = () => makeCode(body.querySelector('#inTcC').value, 'student', body.querySelector('#inTcOut'));
      return;
    }
    const [cls, ro] = await Promise.all([classesData(), rosterData()]);
    const staff = ro.staff || [], n = id => (ro.students || []).filter(s => s.class_id === id).length;
    const teachers = staff.filter(s => s.role === 'teacher' || s.role === 'admin').filter((s, i, a) => a.findIndex(x => x.user_id === s.user_id) === i);
    body.innerHTML = `<section class="pv-card" aria-labelledby="inAc"><h3 id="inAc">➕ Add a class or batch</h3><form id="inAcF" class="pv-form" novalidate>
        <div class="pv-row"><div class="pv-f"><label for="inAcK">Type</label><select id="inAcK" class="pv-in"><option value="class">School class</option><option value="batch">CA Foundation batch</option></select></div>
          <div class="pv-f" id="inAcGW"><label for="inAcG">Class</label><select id="inAcG" class="pv-in">${Array.from({ length: 12 }, (_, i) => `<option>${i + 1}</option>`).join('')}</select></div>
          <div class="pv-f"><label for="inAcS" id="inAcSL">Section</label><input id="inAcS" class="pv-in" maxlength="40" placeholder="A"></div></div>
        <p class="pv-err" id="inAcE" role="alert"></p><button class="pv-btn" type="submit">Add</button></form></section>
      <section class="pv-card in-wide" aria-labelledby="inCl"><h3 id="inCl">Classes</h3>${cls.length ? `<ul class="pv-list" id="inClL">${cls.map(c => `<li><div style="display:flex;justify-content:space-between;gap:8px;align-items:center"><b>${esc(c.name)}</b><span class="pv-mut">${n(c.id)} student${n(c.id) === 1 ? '' : 's'}</span>
          <span style="display:flex;gap:6px"><button class="pv-btn ghost" style="width:auto" type="button" data-open="${esc(c.id)}">Open</button>${n(c.id) ? '' : `<button class="pv-x" type="button" data-del="${esc(c.id)}" aria-label="Delete ${esc(c.name)}">✕</button>`}</span></div>
          ${teachers.length ? `<div class="in-staff" role="group" aria-label="Teachers of ${esc(c.name)}">${teachers.map(t => `<button type="button" class="in-chipb" aria-pressed="${t.classes.includes(c.id)}" data-tc="${esc(c.id)}" data-tu="${esc(t.user_id)}">${esc(t.name || t.email)}</button>`).join('')}</div>` : ''}</li>`).join('')}</ul>
          <p class="pv-note">Tap a teacher's name to add or remove them from a class.</p>` : '<p class="pv-empty">No classes yet.</p>'}</section>
      <section class="pv-card" aria-labelledby="inIv"><h3 id="inIv">✉️ Invite a teacher or admin</h3><p class="pv-mut">We email them a link to set a password. They land on this console.</p>
        <form id="inIvF" class="pv-form" novalidate><label for="inIvE">Email</label><input id="inIvE" class="pv-in" type="email" maxlength="120" autocomplete="off" autocapitalize="none">
          <label for="inIvN">Name</label><input id="inIvN" class="pv-in" maxlength="60" autocomplete="off">
          <div class="pv-row"><div class="pv-f"><label for="inIvR">Role</label><select id="inIvR" class="pv-in"><option value="teacher">Teacher</option><option value="admin">Admin</option></select></div>
            <div class="pv-f"><label for="inIvC">First class (teachers)</label><select id="inIvC" class="pv-in"><option value="">—</option>${cls.map(c => `<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('')}</select></div></div>
          <p class="pv-err" id="inIvX" role="alert"></p><button class="pv-btn" type="submit">Send invite</button></form>
        <p class="pv-mut" style="margin-top:10px">Or make a teacher code (they sign up and enter it): <button class="cl-link" type="button" id="inTCode">Make teacher code</button></p><div id="inTCodeOut"></div></section>
      <section class="pv-card" aria-labelledby="inSt"><h3 id="inSt">Staff</h3><ul class="pv-list">${staff.map(s => `<li style="display:flex;justify-content:space-between;align-items:center;gap:8px"><span><b>${esc(s.name || s.email)}</b> <span class="pv-mut">${esc(s.email)} · ${s.role}</span></span>${s.user_id === uid() ? '' : `<button class="pv-x" type="button" data-rm="${esc(s.user_id)}" data-role="${s.role}" aria-label="Remove ${esc(s.email)} as ${s.role}">✕</button>`}</li>`).join('') || '<li class="pv-empty">No staff yet.</li>'}</ul></section>`;
    const kind = body.querySelector('#inAcK'); kind.onchange = () => { const b = kind.value === 'batch'; body.querySelector('#inAcGW').hidden = b; body.querySelector('#inAcSL').textContent = b ? 'Batch name' : 'Section'; body.querySelector('#inAcS').placeholder = b ? 'Morning' : 'A'; };
    body.querySelector('#inAcF').onsubmit = async ev => { ev.preventDefault(); const e = body.querySelector('#inAcE');
      try { const r = one(await rpc('inst_save_class', { p_inst: I().id, p_id: null, p_kind: kind.value, p_grade: +body.querySelector('#inAcG').value, p_section: body.querySelector('#inAcS').value.trim() || (kind.value === 'batch' ? '' : 'A') }));
        if (!r || !r.ok) { e.textContent = (r && r.msg) || 'Could not add.'; return; } say(`${r.name} added ✓`); cache = {}; await refreshMe(); render(); } catch (x) { e.textContent = errT(x); } };
    body.querySelectorAll('[data-open]').forEach(b => b.onclick = () => openTeach(b.dataset.open));
    body.querySelectorAll('[data-del]').forEach(b => b.onclick = async () => { if (!b.dataset.sure) { b.dataset.sure = 1; b.textContent = 'Sure?'; return; }
      try { const r = one(await rpc('inst_delete_class', { p_id: b.dataset.del })); if (!r || !r.ok) say((r && r.msg) || 'Could not delete.'); else { say('Class deleted'); cache = {}; render(); } } catch (x) { say(errT(x)); } });
    body.querySelectorAll('[data-tc]').forEach(b => b.onclick = async () => { const on = b.getAttribute('aria-pressed') !== 'true'; b.disabled = true;
      try { const r = one(await rpc('inst_assign_teacher', { p_class: b.dataset.tc, p_user: b.dataset.tu, p_on: on })); if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not save.'); b.setAttribute('aria-pressed', String(on)); delete cache.ro; say(on ? 'Teacher added to the class' : 'Teacher removed from the class'); }
      catch (x) { say(errT(x)); } finally { b.disabled = false; } });
    body.querySelector('#inIvF').onsubmit = async ev => { ev.preventDefault(); const e = body.querySelector('#inIvX'), em = body.querySelector('#inIvE').value.trim().toLowerCase(), role = body.querySelector('#inIvR').value, c = body.querySelector('#inIvC').value;
      e.textContent = ''; if (!EMAIL_RE.test(em)) { e.textContent = 'Please enter a valid email.'; return; }
      const btn = ev.target.querySelector('[type=submit]'); btn.disabled = true; btn.textContent = 'Sending…';
      try { const r = await fn('institution-bulk', { action: 'staff', institution_id: I().id, email: em, role, name: body.querySelector('#inIvN').value.trim(), class_ids: c ? [c] : [] });
        if (!r || !r.ok) { e.textContent = (r && r.msg) || 'Could not send.'; return; } say(r.created ? `Invite sent to ${em} ✓` : `${em} added ✓ (they already had an account)`); cache = {}; render(); }
      catch (x) { e.textContent = errT(x); } finally { btn.disabled = false; btn.textContent = 'Send invite'; } };
    body.querySelector('#inTCode').onclick = () => makeCode(null, 'teacher', body.querySelector('#inTCodeOut'));
    body.querySelectorAll('[data-rm]').forEach(b => b.onclick = () => removeMember(b, b.dataset.rm, b.dataset.role));
  }
  async function removeMember(b, user, role) {
    if (!b.dataset.sure) { b.dataset.sure = 1; b.textContent = 'Sure?'; b.setAttribute('aria-label', 'Tap again to remove'); return; }
    b.disabled = true;
    try { const r = one(await rpc('inst_remove_member', { p_inst: I().id, p_user: user, p_role: role })); if (!r || !r.ok) { say((r && r.msg) || 'Could not remove.'); b.disabled = false; return; } say('Removed'); cache = {}; render(); }
    catch (x) { say(errT(x)); b.disabled = false; }
  }
  async function makeCode(classId, role, out) {
    out.innerHTML = '<p class="pv-load">Making the code…</p>';
    try {
      const r = one(await rpc('inst_create_code', { p_inst: I().id, p_class: classId || null, p_role: role, p_days: role === 'teacher' ? 7 : 30, p_max: role === 'teacher' ? 20 : 200 }));
      if (!r || !r.ok) { out.innerHTML = `<p class="in-err">${esc((r && r.msg) || 'Could not make a code.')}</p>`; return; }
      const link = `${SITE}?join=${r.code}`;
      out.innerHTML = `<div class="pv-bigcode" aria-label="Code ${esc(r.code.split('').join(' '))}">${esc(r.code)}</div><p class="cl-small">Works for ${role === 'teacher' ? '7 days, up to 20 teachers' : '30 days, up to 200 students'}. Link: ${esc(link)}</p>
        <div class="pv-row"><button class="pv-btn ghost" type="button" data-cp>Copy link</button><a class="pv-btn pv-wa" href="https://wa.me/?text=${encodeURIComponent(`Join ${I().name} on StudyVerse: open ${link} and create your account (code ${r.code}).`)}" target="_blank" rel="noopener">Share on WhatsApp</a>${role === 'student' ? '<button class="pv-btn ghost" type="button" data-poster>Print poster</button>' : ''}</div>`;
      out.querySelector('[data-cp]').onclick = () => { try { navigator.clipboard.writeText(link).then(() => say('Link copied'), () => say(link)); } catch (x) { say(link); } };
      const po = out.querySelector('[data-poster]'); if (po) po.onclick = () => posterPrint(r.code, classId);
      delete cache.codes;
    } catch (e) { out.innerHTML = `<p class="in-err">${esc(errT(e))}</p>`; }
  }
  function printHTML(html) {
    let p = D.getElementById('pvPrint'); if (!p) { p = D.createElement('div'); p.id = 'pvPrint'; D.body.appendChild(p); }
    p.className = 'in-print'; p.innerHTML = html;
    const done = () => { p.remove(); removeEventListener('afterprint', done); }; addEventListener('afterprint', done);
    try { window.print(); } catch (e) {}
  }
  async function posterPrint(code, classId) {
    const cls = (await classesData().catch(() => [])).find(c => c.id === classId) || I().classes.find(c => c.id === classId) || {};
    printHTML(`<div class="in-poster"><h1>${esc(I().name)}</h1><h2>Join ${esc(cls.name || 'your class')} on StudyVerse</h2><p>1. Open <b>study.moneyviel.com</b> on your phone and create your account.</p><p>2. Go to <b>Me → School or coaching class → Enter class code</b>.</p><b>${esc(code)}</b><p>Or open study.moneyviel.com/?join=${esc(code)}</p></div>`);
  }

  /* ---------- Students: roster + bulk upload ---------- */
  async function tStudents(body) {
    const [cls, ro] = await Promise.all([classesData(), rosterData()]);
    const S_ = ro.students || [], opt = cur => cls.map(c => `<option value="${esc(c.id)}"${c.id === cur ? ' selected' : ''}>${esc(c.name)}</option>`).join('');
    body.innerHTML = `<section class="pv-card" aria-labelledby="inBu"><h3 id="inBu">⬆️ Add students in bulk</h3>
        <p class="pv-mut">Paste from Excel / Google Sheets or choose a CSV file. Columns: <b>name, class, section, roll no, student email (optional), parent email (optional)</b>. Class is 1–12, or CA for CA Foundation (section = batch name).</p>
        <p class="pv-mut">With a student email we create the account and email a link to set a password. Without one you get a printable sheet of roll-number codes. A parent email gets an invite to Parent Hub.</p>
        <label class="in-lbl" for="inBuT">Student list</label><textarea id="inBuT" class="pv-in" rows="6" spellcheck="false" placeholder="name,class,section,roll,email,parent email&#10;Riya Sharma,7,B,12,,riya.mum@gmail.com&#10;Kabir Singh,7,B,13,kabir@gmail.com,"></textarea>
        <label class="in-lbl" for="inBuF">Or choose a CSV file</label><input id="inBuF" type="file" accept=".csv,.txt,text/csv" class="pv-in">
        <div class="pv-row"><button class="pv-btn ghost" type="button" id="inBuChk">Check the list</button><button class="pv-btn" type="button" id="inBuGo" disabled>Add students</button></div>
        <div id="inBuOut" aria-live="polite"></div></section>
      ${ro.pending && ro.pending.length ? `<section class="pv-card" aria-labelledby="inPd"><h3 id="inPd">⏳ Roll-number codes not used yet (${ro.pending.length})</h3><button class="pv-btn ghost" type="button" id="inPdPr">Print code sheet again</button></section>` : ''}
      <section class="pv-card in-wide" aria-labelledby="inRo"><h3 id="inRo">👩‍🎓 Students (${S_.length})</h3>${S_.length ? `<div class="in-hscroll" tabindex="0" role="region" aria-label="Students"><table class="in-tbl" id="inRoT"><thead><tr><th scope="col">Name</th><th scope="col">Roll</th><th scope="col">Class</th><th scope="col">Seat</th><th scope="col">Parent</th><th scope="col">Last active</th><th scope="col"><span class="sr-only">Remove</span></th></tr></thead>
        <tbody>${S_.map(s => `<tr><td><b>${esc(s.name)}</b><br><small class="pv-mut">${esc(s.email || '')}</small></td><td>${esc(s.roll_no || '')}</td><td><label class="sr-only" for="mv-${esc(s.user_id)}">Class of ${esc(s.name)}</label><select class="pv-in" id="mv-${esc(s.user_id)}" data-mv="${esc(s.user_id)}" style="min-width:110px">${opt(s.class_id)}</select></td>
          <td>${s.seat === 'paid' ? '<span class="in-pill ok">Seat</span>' : s.seat === 'pilot' ? '<span class="in-pill warn">Pilot</span>' : '<span class="in-pill bad">No seat</span>'}</td><td>${s.parents ? '✓' : '–'}</td><td>${s.last_active ? esc(fmtD(s.last_active)) : 'never'}</td>
          <td><button class="pv-x" type="button" data-rm="${esc(s.user_id)}" aria-label="Remove ${esc(s.name)} from the school">✕</button></td></tr>`).join('')}</tbody></table></div><p class="pv-note">Removing a student from the school never removes their parent's Parent Hub link or their own progress.</p>` : '<p class="pv-empty">No students yet. Add them above or share a class code.</p>'}</section>`;
    let parsed = null;
    const out = body.querySelector('#inBuOut'), go = body.querySelector('#inBuGo'), ta = body.querySelector('#inBuT');
    const check = () => {
      parsed = parseRows(ta.value); const r = parsed;
      go.disabled = !r.rows.length || r.errors.some(e => e.line === 0);
      const em = r.rows.filter(x => x.email).length, pe = r.rows.filter(x => x.parent_email).length;
      out.innerHTML = `<p class="${r.rows.length ? 'in-ok' : 'in-err'}" id="inBuSum">${r.rows.length} student${r.rows.length === 1 ? '' : 's'} ready · ${em} with email (account + invite) · ${r.rows.length - em} roll-number codes · ${pe} parent invite${pe === 1 ? '' : 's'}</p>
        ${r.errors.length ? `<p class="in-err">Please fix ${r.errors.length} line${r.errors.length === 1 ? '' : 's'} (they will be skipped):</p><ul class="in-err" id="inBuErr">${r.errors.slice(0, 20).map(e => `<li>${e.line ? 'Line ' + e.line + ': ' : ''}${esc(e.msg)}</li>`).join('')}</ul>` : ''}
        ${r.rows.length ? `<details class="pv-tbl"><summary>Preview</summary><table><thead><tr><th>Name</th><th>Class</th><th>Section</th><th>Roll</th><th>Email</th><th>Parent</th></tr></thead><tbody>${r.rows.slice(0, 50).map(x => `<tr><td>${esc(x.name)}</td><td>${esc(x.class)}</td><td>${esc(x.section)}</td><td>${esc(x.roll)}</td><td>${esc(x.email)}</td><td>${esc(x.parent_email)}</td></tr>`).join('')}</tbody></table></details>` : ''}`;
    };
    body.querySelector('#inBuChk').onclick = check;
    ta.oninput = () => { go.disabled = true; };
    body.querySelector('#inBuF').onchange = e => { const f = e.target.files && e.target.files[0]; if (!f) return; if (f.size > 1e6) { out.innerHTML = '<p class="in-err">The file is too big (max 1 MB).</p>'; return; } const rd = new FileReader(); rd.onload = () => { ta.value = String(rd.result || ''); check(); }; rd.readAsText(f); };
    go.onclick = async () => {
      if (!parsed || !parsed.rows.length) return;
      go.disabled = true; go.textContent = 'Adding…';
      try {
        const r = await fn('institution-bulk', { action: 'bulk', institution_id: I().id, rows: parsed.rows.map(x => ({ name: x.name, class: x.class, section: x.section, roll: x.roll, email: x.email, parent_email: x.parent_email })) });
        if (!r || !r.ok) { out.innerHTML = `<p class="in-err" role="alert">${esc((r && r.msg) || 'Could not add the students.')}</p>`; return; }
        const codes = r.codes || [], added = r.added || [], failed = r.failed || [];
        out.innerHTML = `<p class="in-ok" id="inBuDone">Done: ${added.length} account${added.length === 1 ? '' : 's'} by email · ${codes.length} roll-number code${codes.length === 1 ? '' : 's'} · ${r.parent_emails || 0} parent email${r.parent_emails === 1 ? '' : 's'}${r.classes_created ? ` · ${r.classes_created} new class${r.classes_created === 1 ? '' : 'es'}` : ''}</p>
          ${failed.length ? `<ul class="in-err">${failed.map(f => `<li>Row ${f.row}: ${esc(f.msg)}</li>`).join('')}</ul>` : ''}
          ${codes.length ? `<div class="in-codes" id="inBuCodes">${codes.slice(0, 12).map(c => `<div class="in-code"><small>${esc(c.class_name)}${c.roll ? ' · Roll ' + esc(c.roll) : ''}</small><br>${esc(c.name)}<b>${esc(c.code)}</b></div>`).join('')}</div>${codes.length > 12 ? `<p class="pv-mut">…and ${codes.length - 12} more on the printed sheet.</p>` : ''}<button class="pv-btn" type="button" id="inBuPr">Print code sheet</button>` : ''}`;
        const pr = out.querySelector('#inBuPr'); if (pr) pr.onclick = () => sheetPrint(codes);
        ta.value = ''; delete cache.ro; delete cache.cl;
      } catch (e) { out.innerHTML = `<p class="in-err" role="alert">${esc(errT(e))}</p>`; }
      finally { go.textContent = 'Add students'; go.disabled = true; }
    };
    const pd = body.querySelector('#inPdPr'); if (pd) pd.onclick = () => sheetPrint(ro.pending.map(p => ({ code: p.code, name: p.name, roll: p.roll_no, class_name: (cls.find(c => c.id === p.class_id) || {}).name || '' })));
    body.querySelectorAll('[data-mv]').forEach(sel => sel.onchange = async () => { sel.disabled = true;
      try { const r = one(await rpc('inst_move_student', { p_inst: I().id, p_user: sel.dataset.mv, p_class: sel.value })); if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not move.'); say('Moved ✓'); delete cache.ro; } catch (x) { say(errT(x)); } finally { sel.disabled = false; } });
    body.querySelectorAll('[data-rm]').forEach(b => b.onclick = () => removeMember(b, b.dataset.rm, 'student'));
  }
  function sheetPrint(codes) {
    printHTML(`<h1>${esc(I().name)} — StudyVerse student codes</h1><p class="pp-d">Cut along the lines. Each student: open <b>study.moneyviel.com</b> → create an account → Me → School or coaching class → enter the code. Each code works once, for 60 days.</p>
      <div class="in-codes">${codes.map(c => `<div class="in-code"><small>${esc(c.class_name)}${c.roll ? ' · Roll ' + esc(c.roll) : ''}</small><br>${esc(c.name)}<b>${esc(c.code)}</b><small>study.moneyviel.com/?join=${esc(c.code)}</small></div>`).join('')}</div>`);
  }

  /* ---------- Join codes ---------- */
  async function tCodes(body) {
    const cls = await classesData();
    const codes = await get('codes', async () => { const r = await C().rest(`join_codes?select=*&institution_id=eq.${I().id}&roll_no=is.null&order=created_at.desc&limit=100`); return Array.isArray(r) ? r : []; });
    const nm = id => (cls.find(c => c.id === id) || {}).name || '';
    body.innerHTML = `<section class="pv-card" aria-labelledby="inMc"><h3 id="inMc">🔑 New class code</h3><p class="pv-mut">One code for a whole class. Students type it in their app and join that class.</p>
        <label class="in-lbl" for="inMcC">Class</label><select id="inMcC" class="pv-in">${cls.map(c => `<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('')}</select>
        <button class="pv-btn" type="button" id="inMcGo"${cls.length ? '' : ' disabled'}>Make class code</button><div id="inMcOut"></div></section>
      <section class="pv-card" aria-labelledby="inCd"><h3 id="inCd">Codes</h3>${codes.length ? `<ul class="pv-list" id="inCdL">${codes.map(j => { const live = j.active && new Date(j.expires_at) > new Date() && j.used < j.max_uses;
        return `<li style="display:flex;justify-content:space-between;gap:8px;align-items:center"><span><b style="font-family:ui-monospace,Menlo,monospace;letter-spacing:1px">${esc(j.code)}</b> · ${j.role === 'teacher' ? 'Teachers' : esc(nm(j.class_id))}<br><span class="pv-mut">Used ${j.used}/${j.max_uses} · till ${esc(fmtD(j.expires_at))}</span> ${live ? '<span class="in-pill ok">Active</span>' : '<span class="in-pill">Stopped</span>'}</span>
          ${live ? `<button class="pv-btn ghost" style="width:auto" type="button" data-stop="${esc(j.code)}">Stop</button>` : ''}</li>`; }).join('')}</ul>` : '<p class="pv-empty">No codes yet.</p>'}</section>`;
    body.querySelector('#inMcGo').onclick = () => makeCode(body.querySelector('#inMcC').value, 'student', body.querySelector('#inMcOut'));
    body.querySelectorAll('[data-stop]').forEach(b => b.onclick = async () => { try { const r = one(await rpc('inst_revoke_code', { p_code: b.dataset.stop })); if (r && r.ok) { say('Code stopped'); delete cache.codes; render(); } else say((r && r.msg) || 'Could not stop.'); } catch (x) { say(errT(x)); } });
  }

  /* ---------- Orders & invoices ---------- */
  async function tOrders(body) {
    const o = await overviewData();
    const orders = await get('orders', async () => { const r = await C().rest(`seat_orders?select=*&institution_id=eq.${I().id}&order=created_at.desc&limit=50`); return Array.isArray(r) ? r : []; });
    const need = {}; o.seats.forEach(s => { need[s.band] = Math.max(0, s.students - s.total); });
    const years = ay();
    body.innerHTML = `<section class="pv-card" aria-labelledby="inOb"><h3 id="inOb">🛒 Order seats</h3>
        <p class="pv-mut">Price per student per month, billed for 10 months of the academic year (April–March). Minimum 30 students. Discount on the whole order: 100+ students 10%, 500+ 20%, 1000+ 30%.</p>
        <form id="inObF" novalidate><div class="in-num">${BANDS.map(([b, l, r]) => `<label for="inQ-${b}">${esc(l)}<small>₹${r} / student / month</small></label><input id="inQ-${b}" class="pv-in" type="number" min="0" max="100000" inputmode="numeric" data-band="${b}" value="${need[b] || ''}" placeholder="0">`).join('')}</div>
          <label class="in-lbl" for="inAy">Academic year</label><select id="inAy" class="pv-in">${years.map(y => `<option>${y}</option>`).join('')}</select>
          <div id="inQuote" aria-live="polite"><p class="pv-mut">Enter the number of students.</p></div>
          <p class="pv-err" id="inObE" role="alert"></p><button class="pv-btn" type="submit" id="inObGo" disabled>Request invoice</button></form>
        <p class="pv-note">We email you the invoice and payment details. Seats switch on as soon as we confirm the payment.</p></section>
      <section class="pv-card" aria-labelledby="inOl"><h3 id="inOl">Your orders</h3>${orders.length ? `<ul class="pv-list" id="inOlL">${orders.map(x => `<li><div style="display:flex;justify-content:space-between;gap:8px;align-items:center;flex-wrap:wrap"><span><b>${esc(x.invoice_no || 'Draft')}</b> · ${x.students} students · ${inr(x.total)}<br><span class="pv-mut">${esc(x.academic_year)} · ${esc(fmtD(x.created_at))}</span> ${statusPill(x.status)}</span>
        <span style="display:flex;gap:6px">${x.status !== 'cancelled' && x.status !== 'draft' ? `<button class="pv-btn ghost" style="width:auto" type="button" data-inv="${esc(x.id)}">View invoice</button>` : ''}${x.status === 'invoiced' || x.status === 'draft' ? `<button class="pv-btn ghost danger" style="width:auto" type="button" data-cancel="${esc(x.id)}">Cancel</button>` : ''}</span></div></li>`).join('')}</ul>` : '<p class="pv-empty">No orders yet.</p>'}</section>`;
    const f = body.querySelector('#inObF'), qBox = body.querySelector('#inQuote'), go = body.querySelector('#inObGo');
    const lines = () => [...f.querySelectorAll('[data-band]')].map(i => ({ band: i.dataset.band, students: Math.max(0, Math.floor(+i.value || 0)) })).filter(x => x.students > 0);
    let t = 0, seq = 0;
    const quote = async () => {
      const L = lines(), my = ++seq; go.disabled = true;
      if (!L.length) { qBox.innerHTML = '<p class="pv-mut">Enter the number of students.</p>'; return; }
      qBox.innerHTML = '<p class="pv-mut">Working out the price…</p>';
      try {
        const q = one(await rpc('quote_order', { p_lines: L, p_inst: I().id })); if (my !== seq) return;
        if (!q || !q.ok) { qBox.innerHTML = `<p class="in-err" id="inQErr">${esc((q && q.msg) || 'Could not work out the price.')}</p>`; return; }
        qBox.innerHTML = quoteHTML(q); go.disabled = false;
      } catch (e) { if (my === seq) qBox.innerHTML = `<p class="in-err">${esc(errT(e))}</p>`; }
    };
    f.querySelectorAll('[data-band]').forEach(i => i.oninput = () => { clearTimeout(t); t = setTimeout(quote, 350); });
    if (lines().length) quote();
    f.onsubmit = async ev => {
      ev.preventDefault(); const e = body.querySelector('#inObE'); e.textContent = ''; go.disabled = true; go.textContent = 'Sending…';
      try {
        const r = one(await rpc('create_order', { p_inst: I().id, p_lines: lines(), p_ay: body.querySelector('#inAy').value, p_submit: true }));
        if (!r || !r.ok) { e.textContent = (r && r.msg) || 'Could not create the order.'; go.disabled = false; return; }
        let mailed = false, msg = '';
        try { const m = await fn('institution-notify', { order_id: r.order_id }); mailed = !!(m && m.mailed); msg = (m && m.msg) || ''; } catch (x) { msg = 'Your order is saved. Please write to support@moneyviel.com if you do not hear from us in a day.'; }
        say(mailed ? `Invoice ${r.invoice_no} requested ✓ We will email you` : 'Order saved ✓');
        delete cache.orders; await render();
        const b = hub.querySelector('#inBody'); if (b && msg) b.insertAdjacentHTML('afterbegin', `<p class="pv-card in-ok" role="status">${esc(msg)}</p>`);
      } catch (x) { e.textContent = errT(x); go.disabled = false; }
      finally { go.textContent = 'Request invoice'; }
    };
    body.querySelectorAll('[data-inv]').forEach(b => b.onclick = () => invoiceView(orders.find(x => x.id === b.dataset.inv), () => render()));
    body.querySelectorAll('[data-cancel]').forEach(b => b.onclick = async () => { if (!b.dataset.sure) { b.dataset.sure = 1; b.textContent = 'Sure?'; return; }
      try { const r = one(await rpc('cancel_order', { p_order: b.dataset.cancel })); if (r && r.ok) { say('Order cancelled'); delete cache.orders; render(); } else say((r && r.msg) || 'Could not cancel.'); } catch (x) { say(errT(x)); } });
  }
  const statusPill = s => `<span class="in-pill ${({ paid: 'ok', invoiced: 'warn', draft: '', cancelled: 'bad' })[s] || ''}">${({ paid: 'Paid', invoiced: 'Waiting for payment', draft: 'Draft', cancelled: 'Cancelled' })[s] || esc(s)}</span>`;
  function quoteHTML(q) {
    const g = q.gst || {};
    return `<table class="in-qt" id="inQt"><thead><tr><th>Class group</th><th>Students</th><th>Amount</th></tr></thead><tbody>
      ${q.lines.map(l => `<tr><td>${esc(l.label)}<br><small class="pv-mut">${l.students} × ₹${l.rate} × 10 months</small></td><td>${l.students}</td><td>${inr(l.amount)}</td></tr>`).join('')}
      <tr><td>Subtotal</td><td>${q.students}</td><td>${inr(q.subtotal)}</td></tr>
      ${q.discount_pct ? `<tr><td>Volume discount ${q.discount_pct}%</td><td></td><td>−${inr(q.discount_amt, 1)}</td></tr>` : ''}
      ${g.mode === 'intra' ? `<tr><td>CGST 9%</td><td></td><td>${inr(g.cgst, 1)}</td></tr><tr><td>SGST 9%</td><td></td><td>${inr(g.sgst, 1)}</td></tr>` : g.mode === 'inter' ? `<tr><td>IGST 18%</td><td></td><td>${inr(g.igst, 1)}</td></tr>` : ''}
      <tr class="tot"><td>Total</td><td></td><td id="inQTot">${inr(q.total, 1)}</td></tr></tbody></table>
      <p class="pv-mut">${g.mode === 'none' ? esc(g.note) + '. ' : ''}That is ${inr(q.per_student_month, 1)} per student per month after discount.${q.students < 100 ? ` Add ${100 - q.students} more for 10% off.` : q.students < 500 ? ` Add ${500 - q.students} more for 20% off.` : q.students < 1000 ? ` Add ${1000 - q.students} more for 30% off.` : ''}</p>`;
  }
  /* printable invoice / bill from the order's own snapshot (seller + buyer saved when the order was made) */
  function invoiceHTML(o) {
    const s = o.seller || {}, b = o.buyer || {}, g = o.gst || {}, paid = o.status === 'paid';
    const title = (paid ? '' : 'Proforma ') + (s.gstin ? 'Tax invoice' : 'Invoice');
    const ayS = String(o.academic_year || ''), period = ayS ? `April ${ayS.slice(0, 4)} – March ${+ayS.slice(0, 4) + 1}` : '';
    return `<div class="in-inv"><div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap"><div><h2 style="margin:0;color:#5B0F1B">${title}</h2><p style="margin:2px 0">No. <b id="inInvNo">${esc(o.invoice_no || '—')}</b> · Date ${esc(fmtD(o.invoiced_at || o.created_at))}</p></div>
      <div style="text-align:right"><b style="font-size:18px">Study<span style="color:#8A6A2E">Verse</span></b><br><small>for Schools &amp; Coaching</small></div></div>
      <div class="two"><div class="box"><h4>From (seller)</h4><b>${esc(s.name || 'MoneyViel')}, ${esc(s.city || 'Pune')}</b><br>Legal name: ${esc(s.legal_name || 'Mukesh Jhedu')}<br>${esc(s.address || '')}<br>${esc(s.email || 'support@moneyviel.com')}<br>${s.gstin ? 'GSTIN: ' + esc(s.gstin) : 'Not registered under GST'}</div>
        <div class="box"><h4>To (buyer)</h4><b>${esc(b.name || '')}</b><br>${[b.address, b.city, b.state, b.pincode].filter(Boolean).map(esc).join(', ')}<br>${b.gstin ? 'GSTIN: ' + esc(b.gstin) : 'GSTIN: —'}<br>${esc([b.contact_name, b.contact_phone, b.contact_email].filter(Boolean).join(' · '))}</div></div>
      <table><thead><tr><th>#</th><th>Description</th><th class="r">Students</th><th class="r">Rate / month</th><th class="r">Months</th><th class="r">Amount</th></tr></thead><tbody>
        ${(o.lines || []).map((l, i) => `<tr><td>${i + 1}</td><td>StudyVerse student access — ${esc(l.label)}<br><small>Academic year ${esc(ayS)} (${esc(period)})</small></td><td class="r">${l.students}</td><td class="r">${inr(l.rate, 1)}</td><td class="r">${l.months || 10}</td><td class="r">${inr(l.amount, 1)}</td></tr>`).join('')}
        <tr><td colspan="5" class="r">Subtotal</td><td class="r">${inr(o.subtotal, 1)}</td></tr>
        ${+o.discount_pct ? `<tr><td colspan="5" class="r">Volume discount (${o.discount_pct}% on ${o.students} students)</td><td class="r">−${inr(o.discount_amt, 1)}</td></tr>` : ''}
        <tr><td colspan="5" class="r">Taxable value</td><td class="r">${inr(o.taxable, 1)}</td></tr>
        ${g.mode === 'intra' ? `<tr><td colspan="5" class="r">CGST 9%</td><td class="r">${inr(g.cgst, 1)}</td></tr><tr><td colspan="5" class="r">SGST 9%</td><td class="r">${inr(g.sgst, 1)}</td></tr>`
          : g.mode === 'inter' ? `<tr><td colspan="5" class="r">IGST 18%</td><td class="r">${inr(g.igst, 1)}</td></tr>` : `<tr><td colspan="5" class="r" id="inInvGst">${esc(g.note || 'GST: not charged — supplier not registered under GST')}</td><td class="r">₹0.00</td></tr>`}
        <tr><th colspan="5" class="r">Total</th><th class="r" id="inInvTot">${inr(o.total, 1)}</th></tr></tbody></table>
      <p><b>Amount in words:</b> <span id="inInvW">${esc(words(+o.total))}</span></p>
      <p>${paid ? `<span class="in-pill ok">Paid</span> on ${esc(fmtD(o.paid_at))}${o.payment_ref ? ' · Ref ' + esc(o.payment_ref) : ''}` : 'Payment: bank transfer / UPI — details are sent by email. Seats switch on when the payment is received.'}</p>
      <p class="pv-note">Seats are valid till 31 March ${+ayS.slice(0, 4) + 1}. Computer-generated document. Questions: ${esc(s.email || 'support@moneyviel.com')}</p></div>`;
  }
  function invoiceView(o, backTo) {
    if (!o) return;
    const body = hub.querySelector('#inBody');
    body.innerHTML = `<section class="pv-card in-wide">${invoiceHTML(o)}<div class="pv-row" style="margin-top:10px"><button class="pv-btn" type="button" id="inInvPr">Print / Save PDF</button><button class="pv-btn ghost" type="button" id="inInvBk">Back</button></div></section>`;
    body.querySelector('#inInvPr').onclick = () => printHTML(invoiceHTML(o));
    body.querySelector('#inInvBk').onclick = backTo;
    hub.scrollTop = 0;
  }

  /* ---------- School details ---------- */
  async function tDetails(body) {
    const o = await overviewData(), i = o.institution;
    const f = (id, l, v, extra = '') => `<label class="in-lbl" for="inD-${id}">${l}</label><input id="inD-${id}" class="pv-in" value="${esc(v || '')}" ${extra}>`;
    body.innerHTML = `<section class="pv-card" aria-labelledby="inDt"><h3 id="inDt">🏫 School details</h3><p class="pv-mut">Printed on your invoices. GSTIN is optional.</p>
      <form id="inDF" novalidate>${f('name', 'Name', i.name, 'maxlength="120"')}${f('address', 'Address', i.address, 'maxlength="300" autocomplete="street-address"')}
        <div class="pv-row"><div class="pv-f">${f('city', 'City', i.city, 'maxlength="60"')}</div><div class="pv-f"><label class="in-lbl" for="inD-state">State</label><select id="inD-state" class="pv-in">${stateOpts(i.state)}</select></div></div>
        <div class="pv-row"><div class="pv-f">${f('pincode', 'PIN code', i.pincode, 'maxlength="10" inputmode="numeric"')}</div><div class="pv-f">${f('board', 'Board', i.board, 'maxlength="40" placeholder="CBSE"')}</div></div>
        ${f('gstin', 'GSTIN (optional)', i.gstin, 'maxlength="15" autocapitalize="characters" placeholder="27ABCDE1234F1Z5"')}
        ${f('contact_name', 'Contact person', i.contact_name, 'maxlength="80"')}<div class="pv-row"><div class="pv-f">${f('contact_phone', 'Phone', i.contact_phone, 'maxlength="20" inputmode="tel"')}</div><div class="pv-f">${f('contact_email', 'Email', i.contact_email, 'maxlength="120" type="email"')}</div></div>
        <p class="pv-err" id="inDE" role="alert"></p><button class="pv-btn" type="submit">Save</button></form></section>`;
    body.querySelector('#inDF').onsubmit = async ev => {
      ev.preventDefault(); const e = body.querySelector('#inDE'), v = k => body.querySelector('#inD-' + k).value.trim();
      const p = { name: v('name'), address: v('address'), city: v('city'), state: v('state'), pincode: v('pincode'), board: v('board'), gstin: v('gstin').toUpperCase(), contact_name: v('contact_name'), contact_phone: v('contact_phone'), contact_email: v('contact_email') };
      try { const r = one(await rpc('inst_update_details', { p_inst: I().id, p })); if (!r || !r.ok) { e.textContent = (r && r.msg) || 'Could not save.'; return; } say('Saved ✓'); delete cache.ov; I().name = p.name; } catch (x) { e.textContent = errT(x); }
    };
  }

  /* ================= owner panel ================= */
  let oh = null, otab = 'inst';
  function owner() {
    if (!C().admin()) return; style();
    if (!oh) { oh = D.createElement('div'); oh.className = 'sheet pv-hub in-hub'; oh.id = 'inOwner'; oh.setAttribute('role', 'dialog'); oh.setAttribute('aria-modal', 'true'); oh.setAttribute('aria-labelledby', 'inOT'); D.body.appendChild(oh); }
    oh.classList.add('show'); orender();
  }
  function orender() {
    const T = [['inst', 'Institutions'], ['orders', 'Orders'], ['billing', 'Seller & GST']];
    oh.innerHTML = `<div class="pv-wrap"><div class="pv-top"><button class="pv-back" type="button" id="inOBk">← Back</button><h1 id="inOT"><span>🏫 Schools (owner)</span></h1><button class="pv-ref" type="button" id="inORf" aria-label="Refresh">⟳</button></div>
      <div class="pv-tabs in-tabs" role="tablist" aria-label="Owner sections">${T.map(([k, n]) => `<button type="button" role="tab" id="ino-${k}" aria-selected="${k === otab}" class="pv-tab${k === otab ? ' on' : ''}" data-ot="${k}">${n}</button>`).join('')}</div><div id="inOBody" class="pv-body" role="tabpanel" aria-labelledby="ino-${otab}"><p class="pv-load">Loading…</p></div></div>`;
    oh.querySelector('#inOBk').onclick = () => oh.classList.remove('show');
    oh.querySelector('#inORf').onclick = orender;
    oh.querySelectorAll('[data-ot]').forEach(b => b.onclick = () => { otab = b.dataset.ot; orender(); });
    const body = oh.querySelector('#inOBody');
    ({ inst: oInst, orders: oOrders, billing: oBilling })[otab](body).catch(e => { body.innerHTML = `<div class="pv-card"><p class="in-err">${esc(errT(e))}</p></div>`; });
  }
  async function oInst(body) {
    const list = await rpc('owner_list_institutions') || [];
    body.innerHTML = `<section class="pv-card" aria-labelledby="inNi"><h3 id="inNi">➕ New institution</h3><form id="inNiF" novalidate>
        <label class="in-lbl" for="inNiN">Name</label><input id="inNiN" class="pv-in" maxlength="120">
        <div class="pv-row"><div class="pv-f"><label class="in-lbl" for="inNiT">Type</label><select id="inNiT" class="pv-in"><option value="school">School</option><option value="coaching">Coaching institute</option></select></div>
          <div class="pv-f"><label class="in-lbl" for="inNiC">City</label><input id="inNiC" class="pv-in" maxlength="60"></div></div>
        <div class="pv-row"><div class="pv-f"><label class="in-lbl" for="inNiS">State</label><select id="inNiS" class="pv-in">${stateOpts('')}</select></div><div class="pv-f"><label class="in-lbl" for="inNiB">Board</label><input id="inNiB" class="pv-in" maxlength="40" placeholder="CBSE"></div></div>
        <div class="pv-row"><div class="pv-f"><label class="in-lbl" for="inNiP">Contact phone</label><input id="inNiP" class="pv-in" maxlength="20" inputmode="tel"></div><div class="pv-f"><label class="in-lbl" for="inNiA">First admin's email (principal / owner)</label><input id="inNiA" class="pv-in" type="email" maxlength="120" autocapitalize="none"></div></div>
        <p class="pv-err" id="inNiE" role="alert"></p><button class="pv-btn" type="submit">Create institution</button></form></section>
      <section class="pv-card in-wide" aria-labelledby="inIl"><h3 id="inIl">Institutions (${list.length})</h3>${list.length ? `<ul class="pv-list" id="inIlL">${list.map(i => `<li><b>${esc(i.name)}</b> <span class="pv-mut">${esc(i.type)}${i.city ? ' · ' + esc(i.city) : ''}</span> <span class="in-pill ${i.status === 'active' ? 'ok' : i.status === 'pilot' ? 'warn' : 'bad'}">${esc(i.status)}</span><br>
        <span class="pv-mut">${i.students} students · admins: ${esc((i.admins || []).join(', ') || 'none')}${i.pilot_until ? ` · pilot ${esc(i.pilot_class || '')} till ${esc(fmtD(i.pilot_until))}` : ''}</span>
        <div class="pv-row" style="margin-top:6px"><button class="pv-btn ghost" type="button" data-console="${esc(i.id)}">Open console</button><button class="pv-btn ghost" type="button" data-pilot="${esc(i.id)}">Pilot…</button><button class="pv-btn ghost" type="button" data-admin="${esc(i.id)}">Invite admin</button></div><div data-box="${esc(i.id)}"></div></li>`).join('')}</ul>` : '<p class="pv-empty">No institutions yet.</p>'}</section>`;
    body.querySelector('#inNiF').onsubmit = async ev => {
      ev.preventDefault(); const e = body.querySelector('#inNiE'), v = id => body.querySelector('#' + id).value.trim(), adm = v('inNiA').toLowerCase();
      e.textContent = ''; if (v('inNiN').length < 2) { e.textContent = 'Enter the name.'; return; } if (adm && !EMAIL_RE.test(adm)) { e.textContent = 'Check the admin email.'; return; }
      try {
        const r = one(await rpc('owner_create_institution', { p: { name: v('inNiN'), type: v('inNiT'), city: v('inNiC'), state: v('inNiS'), board: v('inNiB'), contact_phone: v('inNiP'), contact_email: adm } }));
        if (!r || !r.ok) { e.textContent = (r && r.msg) || 'Could not create.'; return; }
        if (adm) { const m = await fn('institution-bulk', { action: 'staff', institution_id: r.id, email: adm, role: 'admin' }); if (!m || !m.ok) say('Institution created, but the admin invite failed: ' + ((m && m.msg) || '')); else say('Institution created and admin invited ✓'); }
        else say('Institution created ✓');
        orender();
      } catch (x) { e.textContent = errT(x); }
    };
    body.querySelectorAll('[data-console]').forEach(b => b.onclick = () => { const i = list.find(x => x.id === b.dataset.console); oh.classList.remove('show'); consoleOwner(i); });
    body.querySelectorAll('[data-pilot]').forEach(b => b.onclick = () => {
      const i = list.find(x => x.id === b.dataset.pilot), box = body.querySelector(`[data-box="${i.id}"]`);
      box.innerHTML = (i.classes || []).length ? `<div class="pv-form"><div class="pv-row"><div class="pv-f"><label class="in-lbl" for="pc-${esc(i.id)}">Pilot class (one)</label><select id="pc-${esc(i.id)}" class="pv-in">${i.classes.map(c => `<option value="${esc(c.id)}"${c.id === i.pilot_class_id ? ' selected' : ''}>${esc(c.name)}</option>`).join('')}</select></div>
        <div class="pv-f"><label class="in-lbl" for="pd-${esc(i.id)}">Days (max 30)</label><input id="pd-${esc(i.id)}" class="pv-in" type="number" min="1" max="30" value="30"></div></div>
        <div class="pv-row"><button class="pv-btn" type="button" data-pgo>Grant pilot</button>${i.pilot_until && new Date(i.pilot_until) > new Date() ? '<button class="pv-btn ghost danger" type="button" data-pend>End pilot</button>' : ''}</div><p class="pv-err" role="alert"></p></div>`
        : '<p class="pv-mut">Add a class first: open the console → Classes &amp; teachers.</p>';
      const g = box.querySelector('[data-pgo]'); if (g) g.onclick = async () => { const er = box.querySelector('.pv-err');
        try { const r = one(await rpc('owner_grant_pilot', { p_inst: i.id, p_class: box.querySelector('select').value, p_days: +box.querySelector('input').value })); if (!r || !r.ok) { er.textContent = (r && r.msg) || 'Could not grant.'; return; } say('Pilot granted ✓'); orender(); } catch (x) { er.textContent = errT(x); } };
      const en = box.querySelector('[data-pend]'); if (en) en.onclick = async () => { try { await rpc('owner_end_pilot', { p_inst: i.id }); say('Pilot ended'); orender(); } catch (x) { say(errT(x)); } };
    });
    body.querySelectorAll('[data-admin]').forEach(b => b.onclick = () => {
      const id = b.dataset.admin, box = body.querySelector(`[data-box="${id}"]`);
      box.innerHTML = `<div class="pv-form"><label class="in-lbl" for="ae-${esc(id)}">Admin email</label><input id="ae-${esc(id)}" class="pv-in" type="email" maxlength="120" autocapitalize="none"><button class="pv-btn" type="button" data-ago>Send invite</button><p class="pv-err" role="alert"></p></div>`;
      box.querySelector('[data-ago]').onclick = async () => { const er = box.querySelector('.pv-err'), em = box.querySelector('input').value.trim().toLowerCase(); if (!EMAIL_RE.test(em)) { er.textContent = 'Please enter a valid email.'; return; }
        try { const r = await fn('institution-bulk', { action: 'staff', institution_id: id, email: em, role: 'admin' }); if (!r || !r.ok) { er.textContent = (r && r.msg) || 'Could not send.'; return; } say('Admin invited ✓'); orender(); } catch (x) { er.textContent = errT(x); } };
    });
  }
  function consoleOwner(i) {             // the owner opens any institution's console (owner counts as admin on the server)
    style(); pinned = false;
    ctx = { list: [{ id: i.id, name: i.name, type: i.type, admin: true, owner: true, classes: i.classes || [] }] }; ctx.inst = ctx.list[0];
    if (!hub) { hub = D.createElement('div'); hub.className = 'sheet pv-hub in-hub'; hub.id = 'inHub'; hub.setAttribute('role', 'dialog'); hub.setAttribute('aria-modal', 'true'); hub.setAttribute('aria-labelledby', 'inT'); D.body.appendChild(hub); }
    hub.removeAttribute('data-pinned'); hub.removeAttribute('data-nonav'); hub.classList.add('show'); tab = 'overview'; cache = {}; render();
  }
  async function oOrders(body) {
    const list = await rpc('owner_list_orders') || [];
    body.innerHTML = `<section class="pv-card in-wide" aria-labelledby="inOo"><h3 id="inOo">Orders</h3>${list.length ? `<ul class="pv-list" id="inOoL">${list.map(o => `<li><b>${esc(o.invoice_no || '—')}</b> · ${esc(o.institution)} · ${o.students} students · <b>${inr(o.total, 1)}</b> ${statusPill(o.status)}<br>
      <span class="pv-mut">${esc(o.academic_year)} · requested ${esc(fmtD(o.invoiced_at || o.created_at))}${o.paid_at ? ' · paid ' + esc(fmtD(o.paid_at)) : ''}</span>
      <div class="pv-row" style="margin-top:6px"><button class="pv-btn ghost" type="button" data-oinv="${esc(o.id)}">View invoice</button>${o.status === 'invoiced' ? `<label class="sr-only" for="pr-${esc(o.id)}">Payment reference</label><input id="pr-${esc(o.id)}" class="pv-in" placeholder="Payment ref (UTR)" maxlength="80"><button class="pv-btn" type="button" data-paid="${esc(o.id)}">Mark paid</button>` : ''}</div></li>`).join('')}</ul>` : '<p class="pv-empty">No orders yet.</p>'}</section><div id="inOoInv"></div>`;
    body.querySelectorAll('[data-paid]').forEach(b => b.onclick = async () => {
      if (!b.dataset.sure) { b.dataset.sure = 1; b.textContent = 'Tap again: payment received'; return; }
      b.disabled = true;
      try { const r = one(await rpc('owner_mark_paid', { p_order: b.dataset.paid, p_ref: (body.querySelector('#pr-' + b.dataset.paid) || {}).value || null })); if (!r || !r.ok) { say((r && r.msg) || 'Could not mark paid.'); b.disabled = false; return; } say('Marked paid — seats are on ✓'); orender(); }
      catch (x) { say(errT(x)); b.disabled = false; }
    });
    body.querySelectorAll('[data-oinv]').forEach(b => b.onclick = () => { const o = list.find(x => x.id === b.dataset.oinv), box = body.querySelector('#inOoInv');
      box.innerHTML = `<section class="pv-card in-wide">${invoiceHTML(o)}<button class="pv-btn" type="button" id="inOoPr">Print / Save PDF</button></section>`; box.querySelector('#inOoPr').onclick = () => printHTML(invoiceHTML(o)); box.scrollIntoView({ block: 'start' }); });
  }
  async function oBilling(body) {
    const r = await C().rest('billing_config?select=*'), c = (Array.isArray(r) && r[0]) || {};
    body.innerHTML = `<section class="pv-card" aria-labelledby="inBl"><h3 id="inBl">Seller details &amp; GST</h3>
      <p>Seller: <b>${esc(c.seller_name || 'MoneyViel')}, ${esc(c.city || 'Pune')}</b> (legal name ${esc(c.legal_name || 'Mukesh Jhedu')})</p>
      <p class="pv-mut">While no GSTIN is set, invoices say “GST: not charged — supplier not registered under GST”. With a GSTIN, new orders add CGST + SGST 9% each (buyer in the same state) or IGST 18% (other states). Orders already made keep their numbers.</p>
      <form id="inBlF" novalidate><label class="in-lbl" for="inBlG">Seller GSTIN</label><input id="inBlG" class="pv-in" maxlength="15" autocapitalize="characters" value="${esc(c.gstin || '')}" placeholder="Leave empty while not registered">
        <label class="in-lbl" for="inBlS">Seller state</label><select id="inBlS" class="pv-in">${stateOpts(c.state || 'Maharashtra')}</select>
        <label class="in-lbl" for="inBlA">Address on invoices</label><input id="inBlA" class="pv-in" maxlength="300" value="${esc(c.address || '')}">
        <p class="pv-err" id="inBlE" role="alert"></p><button class="pv-btn" type="submit">Save</button></form></section>`;
    body.querySelector('#inBlF').onsubmit = async ev => { ev.preventDefault(); const e = body.querySelector('#inBlE');
      try { const x = one(await rpc('owner_set_billing', { p: { gstin: body.querySelector('#inBlG').value.trim().toUpperCase() || null, state: body.querySelector('#inBlS').value, address: body.querySelector('#inBlA').value.trim() } }));
        if (!x || !x.ok) { e.textContent = (x && x.msg) || 'Could not save.'; return; } say('Saved ✓'); } catch (y) { e.textContent = errT(y); } };
  }

  /* ================= start ================= */
  function start() {
    try {                                               // ?join=CODE and ?pinvite=1&email=… links
      const u = new URL(location.href), j = u.searchParams.get('join'), pi = u.searchParams.get('pinvite');
      if (j || pi) {
        const em = (u.searchParams.get('email') || '').trim().toLowerCase();
        ['join', 'pinvite', 'email'].forEach(k => u.searchParams.delete(k)); history.replaceState(history.state, '', u.pathname + u.search + u.hash);
        if (j && /^[A-Za-z0-9-]{8,9}$/.test(j)) jset('sv_join', j.toUpperCase().replace('-', ''));
        if (pi && !signedIn()) setTimeout(() => { if (C() && !C().signedIn()) { C().open('up', null, { email: em, role: 'parent' }); const s = D.querySelector('#svAuth .sheet-in h3'); if (s) s.insertAdjacentHTML('afterend', '<p class="cl-inv">🏫 Your child’s school invited you to Parent Hub. Create a <b>Parent</b> account with this email — your child appears by itself.</p>'); } }, 400);
      }
    } catch (e) {}
    let t = 0;
    new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; paint(); if (C() && C().isParent && C().isParent() && staffM().length) parentButton(); }); }).observe(D.body, { childList: true, subtree: true });
    setInterval(boot, 1500); setTimeout(boot, 600);
    setInterval(() => { if (D.visibilityState === 'visible') pullHw(); }, 5 * 6e4);
    addEventListener('sv-access', () => paint());
  }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', start) : start();

  window.Inst = { style, console: consoleOpen, owner, join: joinSheet, me: () => me, refresh: refreshMe, lib: { parseRows, words, invoiceHTML, bandOf } };
})();
