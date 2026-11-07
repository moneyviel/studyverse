/* StudyVerse desk calculator — a "physical" calculator (like the 12-digit ones CA students carry) in a slide-up panel.
   - Small 🧮 button (bottom-left) opens/closes it from any screen; the panel floats above the app, so the student
     can keep reading the question underneath and go back and forth between screens without losing anything.
   - Desk-calculator behaviour: immediate execution (left to right), %, √, ±, 00, M+ M− MR MC, GT (grand total), AC / C.
   - Paper roll: every calculation is printed on a tape that is kept across screens and visits (localStorage sv_calc);
     tap a tape line to reuse its result. Indian (1,00,000) or international grouping.
   window.Calc = { open, close, toggle } */
(function () {
  const D = document, KEY = 'sv_calc', MAXD = 12;
  let S = { cur: '0', acc: null, op: null, fresh: true, mem: 0, gt: 0, tape: [], grp: 'in', open: false, lastOp: null, lastVal: null, err: false };
  try { Object.assign(S, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch (e) {}
  S.open = false;
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify({ ...S, tape: S.tape.slice(-200) })); } catch (e) {} };

  // ---- number helpers (round to 12 significant digits to avoid 0.1 + 0.2 = 0.30000000000000004) ----
  const clean = x => { if (!isFinite(x)) return NaN; const r = +x.toPrecision(15); return Object.is(r, -0) ? 0 : r; };
  // fit to a 12-digit display like a Casio desk calculator: drop (truncate) decimals that do not fit
  function fit(x) { const neg = x < 0, a = Math.abs(x); const intD = Math.floor(a).toString().length; if (intD > MAXD) return NaN;
    const dec = Math.max(0, MAXD - intD), f = Math.pow(10, dec); let t = Math.floor(+(a * f).toPrecision(15)) / f; t = +t.toFixed(dec); return neg ? -t : t; }
  function fmt(x, g = S.grp) {
    if (typeof x === 'string') x = +x;
    if (!isFinite(x)) return 'Error';
    x = fit(clean(x)); if (!isFinite(x)) return 'Error';
    let s = x.toFixed(Math.max(0, MAXD - Math.floor(Math.abs(x)).toString().length)).replace(/(\.\d*?)0+$/, '$1').replace(/\.$/, '');
    const neg = s[0] === '-'; if (neg) s = s.slice(1);
    let [i, d] = s.split('.');
    if (g === 'in') { const last3 = i.slice(-3), rest = i.slice(0, -3); i = (rest ? rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' : '') + last3; }
    else i = i.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return (neg ? '−' : '') + i + (d != null ? '.' + d : '');
  }
  const fmtEntry = s => { // keep what the student is typing (e.g. trailing "." or "0.50")
    const neg = s[0] === '-'; let t = neg ? s.slice(1) : s; let [i, d] = t.split('.');
    i = fmt(+i || 0).replace('−', ''); return (neg ? '−' : '') + i + (t.includes('.') ? '.' + (d || '') : '');
  };
  const SYM = { '+': '+', '-': '−', '*': '×', '/': '÷' };
  const apply = (a, op, b) => op === '+' ? a + b : op === '-' ? a - b : op === '*' ? a * b : op === '/' ? (b === 0 ? NaN : a / b) : b;

  function print(line, cls) { S.tape.push({ t: line, c: cls || '' }); if (S.tape.length > 200) S.tape.splice(0, S.tape.length - 200); }
  function setErr() { S.err = true; S.cur = 'Error'; S.acc = null; S.op = null; S.fresh = true; print('Error', 'err'); }

  // ---- key handling ----
  function digit(k) {
    if (S.err) return;
    if (S.fresh) { S.cur = '0'; S.fresh = false; }
    const digits = S.cur.replace(/[-.]/g, '').length;
    if (k === '.') { if (!S.cur.includes('.')) S.cur += '.'; return; }
    if (digits + k.length > MAXD) return;
    S.cur = S.cur === '0' ? (k === '00' ? '0' : k) : S.cur === '-0' ? '-' + k : S.cur + k;
  }
  const val = () => +S.cur;
  function operator(op) {
    if (S.err) return;
    if (S.op && !S.fresh) {            // chain: 12 + 5 +  → running total 17 shown
      const b = val(); print(`${fmt(b)} ${SYM[op]}`);
      const r = clean(apply(S.acc, S.op, b)); if (isNaN(r)) return setErr();
      S.acc = r; S.cur = String(r);
    } else if (S.op && S.fresh) {      // operator changed before the next number
      const l = S.tape[S.tape.length - 1]; if (l) l.t = l.t.replace(/[+−×÷]$/, SYM[op]);
    } else { S.acc = val(); print(`${fmt(S.acc)} ${SYM[op]}`); }
    S.op = op; S.fresh = true;
  }
  function equals() {
    if (S.err) return;
    let a, op, b;
    if (S.op && S.fresh && S.op === '/') {   // a ÷ =  →  1/a (reciprocal), as on Casio desk calculators; further = keeps dividing by a
      a = 1; op = '/'; b = S.acc; S.lastOp = '/'; S.lastVal = b; print('=');
    } else if (S.op) { a = S.acc; op = S.op; b = val(); S.lastOp = op; S.lastVal = b; print(S.fresh ? '=' : `${fmt(b)} =`); }
    else if (S.lastOp) { a = val(); op = S.lastOp; b = S.lastVal; print(`${fmt(a)} ${SYM[op]} ${fmt(b)} =`); } // repeat last operation, like a desk calculator
    else return;
    const r = clean(apply(a, op, b)); if (isNaN(r)) return setErr();
    print(fmt(r), 'res'); S.gt = clean(S.gt + r); S.cur = String(r); S.acc = null; S.op = null; S.fresh = true;
  }
  function percent() { // desk-calculator %: a×b% = a·b/100 ; a+b% = a + a·b/100 ; a−b% = a − a·b/100 ; a÷b% = a/b·100
    if (S.err) return;
    const b = val();
    if (!S.op) { const r = clean(b / 100); print(`${fmt(b)} % = ${fmt(r)}`); S.cur = String(r); S.fresh = true; return; }
    const a = S.acc, op = S.op; let r;
    if (op === '*') r = a * b / 100; else if (op === '+') r = a + a * b / 100; else if (op === '-') r = a - a * b / 100; else r = b === 0 ? NaN : a / b * 100;
    r = clean(r); print(`${fmt(b)} % =`); if (isNaN(r)) return setErr();
    print(fmt(r), 'res'); S.gt = clean(S.gt + r); S.cur = String(r); S.acc = null; S.op = null; S.fresh = true;
  }
  function sqrt() { if (S.err) return; const x = val(); if (x < 0) return setErr(); const r = clean(Math.sqrt(x)); print(`√${fmt(x)} = ${fmt(r)}`); S.cur = String(r); S.fresh = true; }
  function neg() { if (S.err) return; if (S.cur === '0') return; S.cur = S.cur[0] === '-' ? S.cur.slice(1) : '-' + S.cur; }
  function back() { if (S.err || S.fresh) return; S.cur = S.cur.length > 1 && S.cur !== '-0' ? S.cur.slice(0, -1) : '0'; if (S.cur === '-') S.cur = '0'; }
  function clearEntry() { S.err = false; S.cur = '0'; S.fresh = false; }
  function allClear() { S.err = false; S.cur = '0'; S.acc = null; S.op = null; S.fresh = true; S.lastOp = null; print('— AC —', 'sep'); }
  function mem(k) {
    if (S.err && k !== 'MC') return;
    if (k === 'M+') { if (S.op && !S.fresh) equals(); S.mem = clean(S.mem + val()); print(`M+ ${fmt(val())}`, 'mem'); S.fresh = true; }
    if (k === 'M-') { if (S.op && !S.fresh) equals(); S.mem = clean(S.mem - val()); print(`M− ${fmt(val())}`, 'mem'); S.fresh = true; }
    if (k === 'MR') { S.cur = String(S.mem); S.fresh = true; S.err = false; }
    if (k === 'MC') { S.mem = 0; print('MC', 'mem'); }
    if (k === 'GT') { S.cur = String(S.gt); S.fresh = true; print(`GT = ${fmt(S.gt)}`, 'res'); S.gt = 0; }
  }
  function press(k) {
    if (/^(\d|00|\.)$/.test(k)) digit(k);
    else if ('+-*/'.includes(k) && k.length === 1) operator(k);
    else if (k === '=') equals(); else if (k === '%') percent(); else if (k === 'sqrt') sqrt(); else if (k === 'neg') neg();
    else if (k === 'back') back(); else if (k === 'C') clearEntry(); else if (k === 'AC') allClear(); else mem(k);
    save(); paint(k);
  }

  // ---- UI ----
  const KEYS = [
    ['MC', 'MC', 'kf'], ['MR', 'MR', 'kf'], ['M-', 'M−', 'kf'], ['M+', 'M+', 'kf'], ['GT', 'GT', 'kf'],
    ['sqrt', '√', 'kf'], ['%', '%', 'kf'], ['neg', '±', 'kf'], ['back', '⌫', 'kf'], ['AC', 'AC', 'kc'],
    ['7', '7'], ['8', '8'], ['9', '9'], ['/', '÷', 'ko'], ['C', 'C', 'kc'],
    ['4', '4'], ['5', '5'], ['6', '6'], ['*', '×', 'ko'], ['-', '−', 'ko'],
    ['1', '1'], ['2', '2'], ['3', '3'], ['+', '+', 'ko kt'], ['=', '=', 'ke kt'],
    ['0', '0'], ['00', '00'], ['.', '.']];
  const LABEL = { MC: 'Memory clear', MR: 'Memory recall', 'M-': 'Memory minus', 'M+': 'Memory plus', GT: 'Grand total', sqrt: 'Square root', '%': 'Percent', neg: 'Change sign', back: 'Delete last digit', AC: 'All clear', C: 'Clear entry', '/': 'Divide', '*': 'Multiply', '-': 'Minus', '+': 'Plus', '=': 'Equals', '.': 'Decimal point' };
  let fab, panel;
  function build() {
    const st = D.createElement('style'); st.textContent = CSS; D.head.appendChild(st);
    fab = D.createElement('button'); fab.id = 'calcFab'; fab.type = 'button'; fab.setAttribute('aria-label', 'Calculator'); fab.setAttribute('aria-expanded', 'false');
    fab.innerHTML = '<span aria-hidden="true">🧮</span>'; fab.onclick = toggle; D.body.appendChild(fab);
    panel = D.createElement('section'); panel.id = 'calcPanel'; panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'Calculator'); panel.hidden = true;
    panel.innerHTML = `<div class="cx-body">
      <div class="cx-top"><span class="cx-brand">StudyVerse <b>CX-12</b></span>
        <button type="button" class="cx-mini" id="cxTapeBtn" aria-pressed="false">🧾 Roll</button>
        <button type="button" class="cx-mini" id="cxGrp" title="Number grouping">1,00,000</button>
        <button type="button" class="cx-close" id="cxClose" aria-label="Close calculator">✕</button></div>
      <div class="cx-tape" id="cxTape" hidden aria-label="Paper roll — tap a result to use it"></div>
      <div class="cx-lcd"><div class="cx-ind"><span id="cxM">M</span><span id="cxOp"></span><span id="cxGT">GT</span><span id="cxE">E</span></div>
        <output class="cx-num" id="cxNum" aria-live="polite">0</output></div>
      <div class="cx-keys">${KEYS.map(([k, t, c]) => `<button type="button" class="cx-k ${c || 'kn'}" data-k="${k}" aria-label="${LABEL[k] || t}">${t}</button>`).join('')}</div></div>`;
    D.body.appendChild(panel);
    panel.querySelectorAll('.cx-k').forEach(b => b.addEventListener('click', () => { press(b.dataset.k); if (navigator.vibrate) try { navigator.vibrate(8); } catch (e) {} }));
    panel.querySelector('#cxClose').onclick = close;
    panel.querySelector('#cxGrp').onclick = () => { S.grp = S.grp === 'in' ? 'intl' : 'in'; save(); paint(); };
    panel.querySelector('#cxTapeBtn').onclick = () => { const t = panel.querySelector('#cxTape'); t.hidden = !t.hidden; panel.querySelector('#cxTapeBtn').setAttribute('aria-pressed', String(!t.hidden)); paint(); };
    panel.querySelector('#cxTape').addEventListener('click', e => {
      const b = e.target.closest('[data-v]'); if (b) { S.cur = b.dataset.v; S.fresh = true; S.err = false; save(); paint(); }
      if (e.target.id === 'cxTapeClr') { S.tape = []; save(); paint(); }
    });
    D.addEventListener('keydown', e => {
      if (panel.hidden || e.ctrlKey || e.metaKey || e.altKey) return;
      const a = D.activeElement; if (a && /^(input|textarea|select)$/i.test(a.tagName)) return;
      const m = { Enter: '=', '=': '=', Backspace: 'back', Escape: null, Delete: 'C', '%': '%', x: '*', X: '*' }[e.key];
      if (e.key === 'Escape') { close(); e.stopPropagation(); return; }
      const k = m || (/^[0-9.+\-*/]$/.test(e.key) ? e.key : null);
      if (k) { press(k); e.preventDefault(); e.stopPropagation(); }
    }, true);
  }
  function paint(k) {
    if (!panel) return;
    const shown = S.err ? 'Error' : S.fresh ? fmt(S.cur) : fmtEntry(S.cur);
    const n = panel.querySelector('#cxNum'); n.textContent = shown; n.classList.toggle('long', shown.length > 14);
    panel.querySelector('#cxM').classList.toggle('on', S.mem !== 0);
    panel.querySelector('#cxGT').classList.toggle('on', S.gt !== 0);
    panel.querySelector('#cxE').classList.toggle('on', !!S.err);
    panel.querySelector('#cxOp').textContent = S.op ? SYM[S.op] : '';
    panel.querySelector('#cxGrp').textContent = S.grp === 'in' ? '1,00,000' : '100,000';
    const t = panel.querySelector('#cxTape');
    if (!t.hidden) {
      t.innerHTML = (S.tape.length ? S.tape.map(l => l.c === 'res' ? `<button type="button" class="cx-tl res" data-v="${(l.t.replace(/[^\d.−-]/g, '').replace('−', '-'))}">${l.t}</button>` : `<div class="cx-tl ${l.c}">${l.t}</div>`).join('') : '<div class="cx-tl sep">Your calculations will print here</div>')
        + (S.tape.length ? '<button type="button" class="cx-mini" id="cxTapeClr">Clear roll</button>' : '');
      t.scrollTop = t.scrollHeight;
    }
  }
  function open() {
    if (!panel) build();
    panel.hidden = false; S.open = true; fab.setAttribute('aria-expanded', 'true'); fab.classList.add('on'); paint();
    D.body.classList.add('cx-open');
    setTimeout(() => { const b = panel.querySelector('[data-k="="]'); if (b && D.activeElement === fab) b.focus(); }, 30);
  }
  function close() { if (!panel) return; panel.hidden = true; S.open = false; fab.setAttribute('aria-expanded', 'false'); fab.classList.remove('on'); D.body.classList.remove('cx-open'); }
  function toggle() { panel && !panel.hidden ? close() : open(); }
  // show the button for Grade 4 and above and for professional courses (not for the youngest children)
  function visible() {
    try { const p = (window.ST && ST.profile) || JSON.parse(localStorage.getItem('sv_state') || '{}').profile; return !!p && (p.course === 'ca' || +p.grade >= 4); } catch (e) { return false; }
  }
  function sync() { if (!fab) return; const v = visible(); fab.hidden = !v; if (!v) close(); }

  const CSS = `
#calcFab{position:fixed;left:12px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:960;width:44px;height:44px;border-radius:12px;border:1.5px solid #C9A76A;
 background:#15161C;color:#fff;font-size:22px;line-height:1;box-shadow:0 4px 14px rgba(0,0,0,.35);opacity:.8;cursor:pointer;display:flex;align-items:center;justify-content:center}
#calcFab:hover,#calcFab:focus-visible,#calcFab.on{opacity:1}#calcFab.on{background:#C9A76A}
#calcFab[hidden]{display:none}
#calcPanel{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(76px + env(safe-area-inset-bottom));z-index:970;width:min(360px,calc(100vw - 16px));
 font-family:Inter,system-ui,sans-serif;filter:drop-shadow(0 12px 28px rgba(0,0,0,.45));animation:cxIn .18s ease-out}
@keyframes cxIn{from{transform:translate(-50%,16px);opacity:0}to{transform:translate(-50%,0);opacity:1}}
@media (prefers-reduced-motion:reduce){#calcPanel{animation:none}}
.cx-body{background:linear-gradient(180deg,#2a2c35,#1b1c23);border-radius:18px;padding:10px 10px 12px;border:1px solid #3a3c47;box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}
.cx-top{display:flex;align-items:center;gap:6px;margin:0 2px 8px}
.cx-brand{flex:1;color:#b9bcc8;font-size:11px;letter-spacing:.06em;text-transform:uppercase}.cx-brand b{color:#C9A76A}
.cx-mini{background:#34363f;color:#e8e3d6;border:1px solid #4a4c57;border-radius:8px;font:600 11px Inter,system-ui,sans-serif;padding:5px 8px;cursor:pointer}
.cx-mini[aria-pressed=true]{background:#C9A76A;color:#15161C}
.cx-close{background:none;border:0;color:#e8e3d6;font-size:18px;width:34px;height:30px;cursor:pointer}
.cx-lcd{background:linear-gradient(180deg,#c9d3b6,#b7c3a1);border-radius:10px;padding:6px 10px 8px;box-shadow:inset 0 2px 6px rgba(0,0,0,.35);border:2px solid #0f1014}
.cx-ind{display:flex;gap:10px;height:14px;font:700 10px Inter,system-ui,sans-serif;color:rgba(30,36,22,.18)}.cx-ind .on{color:#1e2416}#cxOp{color:#1e2416;margin-left:auto;min-width:10px}
.cx-num{display:block;text-align:right;font:500 34px/1.15 "Courier New",ui-monospace,monospace;color:#1e2416;letter-spacing:.02em;white-space:nowrap;overflow:hidden;font-variant-numeric:tabular-nums}
.cx-num.long{font-size:24px;line-height:1.6}
.cx-keys{display:grid;grid-template-columns:repeat(5,1fr);grid-auto-rows:44px;gap:7px;margin-top:10px}
.cx-k{border:0;border-radius:10px;font:600 18px Inter,system-ui,sans-serif;cursor:pointer;box-shadow:0 3px 0 rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.18);transition:transform .05s,box-shadow .05s;touch-action:manipulation}
.cx-k:active{transform:translateY(2px);box-shadow:0 1px 0 rgba(0,0,0,.45)}
.cx-k.kn{background:#f2efe7;color:#15161C}.cx-k.kf{background:#4a4d59;color:#f2efe7;font-size:14px}.cx-k.ko{background:#C9A76A;color:#15161C;font-size:22px}
.cx-k.kc{background:#B71C2C;color:#fff;font-size:15px}.cx-k.ke{background:#2E8B57;color:#fff;font-size:24px}
.cx-k.kt{grid-row:span 2}
.cx-keys .cx-k[data-k="0"]{grid-column:1}
.cx-k:focus-visible,.cx-mini:focus-visible,.cx-close:focus-visible{outline:3px solid #C9A76A;outline-offset:2px}
.cx-tape{background:#fffdf6;border-radius:8px;max-height:140px;overflow:auto;margin:0 2px 8px;padding:6px 10px;font:14px "Courier New",ui-monospace,monospace;color:#2b2b2b;
 background-image:repeating-linear-gradient(#fffdf6 0 21px,#efe9d8 21px 22px);box-shadow:inset 0 -6px 8px -6px rgba(0,0,0,.2)}
.cx-tl{text-align:right;line-height:22px;white-space:nowrap}.cx-tl.res{display:block;width:100%;background:none;border:0;font:700 14px "Courier New",monospace;color:#5B0F1B;text-align:right;cursor:pointer;line-height:22px;border-bottom:1px dashed #C9A76A}
.cx-tl.sep{color:#999;text-align:center}.cx-tl.mem{color:#2A7F8F}.cx-tl.err{color:#B71C2C}
.cx-tape .cx-mini{display:block;margin:6px 0 2px auto;background:#efe9d8;color:#5B0F1B;border-color:#d9cfb5}
@media (forced-colors:active){.cx-k,.cx-lcd,.cx-body{border:1px solid CanvasText}}`;

  function init() { build(); paint(); sync(); setInterval(sync, 1500); D.addEventListener('visibilitychange', sync); }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', init) : init();
  window.Calc = { open, close, toggle, _press: press, _state: () => S, _fmt: fmt };
})();
