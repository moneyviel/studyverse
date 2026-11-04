/* StudyVerse Concept Lab: numberline — "Number line jumper"
 * The child hops / drags a frog along a number line and sees the sum, the skip-count or the value live.
 *
 * PARAMS (all optional; missing ones fall back to sensible defaults)
 *  name        type             meaning                                                         default
 *  mode        string           'jump'  : addition / subtraction as hops from `start`              'jump'
 *                               'skip'  : skip counting by `step` (repeated addition, tables)
 *                               'place' : drag the frog to the value `target` (integers, negatives,
 *                                         fractions, decimals)
 *  min         number|string    left end of the line ("-10", "0", "3/4", "1 1/2" also allowed)      0
 *  max         number|string    right end of the line                                              10 (skip: auto)
 *  tick        number|string    gap between tick marks (1, 5, "1/4", 0.1 …)                         1
 *  start       number|string    where the frog starts                                              min (jump: 3)
 *  add         number|string    jump mode: amount to add (negative = subtract); target = start+add  5
 *  target      number|string    value the frog must land on (overrides start+add)                  auto
 *  step        number|string    skip mode: size of each hop                                        2
 *  hops        array            sizes of the hop buttons, e.g. [1, 5], ["1/4"] or [8, 4, 2, 1] (up to 8
 *                               sizes; with 4+ sizes the buttons get compact rows: − row, + row)    [tick] (+5×tick if 15+ ticks)
 *  marks       array            extra labelled points, also irrational ones: [{value, label}], e.g.
 *                               [{value: 'sqrt(2)', label: '√2'}, {value: 2.2360679, label: '√5'}].
 *                               value: a number, or text like '√2', 'sqrt(5)', '-√3', '2√3', 'π', '3/4'.
 *                               label: any text (default: the value to 3 places). Drawn as coral dots
 *                               on the line with the label below the tick numbers. Display only — the
 *                               frog's snapping and the challenge are unchanged.                    none
 *  labels      string           which ticks get numbers: 'auto' | 'all' | 'whole' | 'ends' | 'none' 'auto'
 *  format      string           label style: 'auto' | 'int' | 'fraction' | 'mixed' | 'decimal'      'auto'
 *  snap        number|string    drag snapping size                                                 tick
 *  showTarget  boolean          show a flag on the target (place mode default false)               true
 *  showDecimal boolean          also show the decimal value of a fraction in the readout           false
 *  drag        boolean          allow dragging the frog (skip mode default false: hops only)       true
 *  newChallenge boolean         show the "New challenge" button                                    true
 *  challenge   string           challenge text (any language); default is generated from params
 */
(function () {
  const T = 'numberline';
  const MINUS = '−';
  const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a || 1; };
  const lcm = (a, b) => a / gcd(a, b) * b;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  // parse "3", "-2.5", "3/4", "1 1/2", 0.25 → {n,d,kind}
  function parseQ(v) {
    if (v == null || v === '') return null;
    let s = String(v).trim().replace(/[−–]/g, '-');
    let m = s.match(/^(-?)(\d+)\s+(\d+)\/(\d+)$/);
    if (m) { const d = +m[4]; if (!d) return null; const n = (+m[2] * d + +m[3]) * (m[1] ? -1 : 1); return { n, d, kind: 'frac' }; }
    m = s.match(/^(-?\d+)\/(\d+)$/);
    if (m) { const d = +m[2]; if (!d) return null; return { n: +m[1], d, kind: 'frac' }; }
    m = s.match(/^(-?)(\d*)\.(\d+)$/);
    if (m) { const dec = Math.min(m[3].length, 3); const d = 10 ** dec; const n = Math.round(parseFloat(s) * d); return { n, d, kind: 'dec' }; }
    m = s.match(/^-?\d+$/);
    if (m) return { n: parseInt(s, 10), d: 1, kind: 'int' };
    const f = parseFloat(s); if (!isFinite(f)) return null;
    return { n: Math.round(f * 1000), d: 1000, kind: 'dec' };
  }

  const CSS = `
  .lb-numberline-w{user-select:none;-webkit-user-select:none}
  .lb-numberline-ch{font-weight:800;font-size:14.5px;line-height:1.3;color:#1b1f3a;background:#f4f0ff;border-radius:14px;padding:9px 12px;margin-bottom:8px}
  .lb-numberline-stage{background:linear-gradient(180deg,#eefaff 0%,#f7fdff 62%,#e9fbf4 62%,#f3fdf9 100%);border-radius:18px;padding:4px 2px;box-shadow:inset 0 0 0 2px #e3eefb}
  .lb-numberline-svg{display:block;width:100%;height:auto;touch-action:none;cursor:grab}
  .lb-numberline-svg.nodrag{cursor:default;touch-action:pan-y}
  .lb-numberline-eq{margin:8px 0 4px;text-align:center;font-weight:800;font-size:22px;color:#1b1f3a;min-height:34px;display:flex;align-items:center;justify-content:center;gap:6px;flex-wrap:wrap}
  .lb-numberline-eq .g{color:#14a37f}.lb-numberline-eq .r{color:#e04848}.lb-numberline-eq .v{color:#7c4ddb}
  .lb-numberline-fr{display:inline-flex;flex-direction:column;align-items:center;line-height:1;font-size:.72em;vertical-align:middle;margin:0 1px}
  .lb-numberline-fr b{display:block;padding:0 2px}.lb-numberline-fr b:first-child{border-bottom:2px solid currentColor;padding-bottom:1px}
  .lb-numberline-seq{text-align:center;color:#6b7090;font-weight:700;font-size:13px;min-height:18px;margin-bottom:6px}
  .lb-numberline-btns{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
  .lb-numberline-b{min-width:56px;height:46px;border:none;border-radius:14px;font-family:inherit;font-weight:800;font-size:18px;cursor:pointer;color:#fff;background:#2ed3a5;box-shadow:0 4px 0 #1a9c78;padding:0 12px;transition:transform .08s}
  .lb-numberline-b:active{transform:translateY(3px);box-shadow:0 1px 0 #1a9c78}
  .lb-numberline-b.m{background:#ff6b6b;box-shadow:0 4px 0 #d04545}
  .lb-numberline-b.m:active{box-shadow:0 1px 0 #d04545}
  .lb-numberline-b.s{background:#eef0fb;color:#1b1f3a;box-shadow:0 4px 0 #d3d7ef;font-size:14px}
  .lb-numberline-b.s:active{box-shadow:0 1px 0 #d3d7ef}
  .lb-numberline-b:disabled{opacity:.45}
  .lb-numberline-b.c{min-width:0;flex:1 1 0;max-width:72px;height:42px;font-size:15px;padding:0 3px}
  .lb-numberline-br{flex-basis:100%;height:0}
  .lb-numberline-hint{text-align:center;font-weight:800;font-size:13.5px;color:#7c4ddb;min-height:20px;margin:2px 0 6px;transition:opacity .2s}
  .lb-numberline-arc{fill:none;stroke-width:3;stroke-linecap:round;stroke-dasharray:var(--len);stroke-dashoffset:var(--len);animation:lbnlDraw .38s ease forwards}
  @keyframes lbnlDraw{to{stroke-dashoffset:0}}
  .lb-numberline-shake{animation:lbnlShake .35s}
  @keyframes lbnlShake{20%,60%{transform:translateX(-5px)}40%,80%{transform:translateX(5px)}}
  `;

  Labs.register(T, {
    title: 'Number line jumper',
    subjects: ['maths'],
    render(host, p, api) {
      const mode = ['jump', 'skip', 'place'].includes(p.mode) ? p.mode : 'jump';
      const uid = 'nl' + Math.random().toString(36).slice(2, 8);

      // ---------- parse params into integer units of 1/D ----------
      const raw = {
        min: parseQ(p.min) || { n: 0, d: 1, kind: 'int' },
        max: parseQ(p.max),
        tick: parseQ(p.tick),
        start: parseQ(p.start),
        add: parseQ(p.add),
        target: parseQ(p.target),
        step: parseQ(p.step),
        snap: parseQ(p.snap)
      };
      let hopsQ = (Array.isArray(p.hops) ? p.hops : (p.hops != null ? [p.hops] : [])).map(parseQ).filter(q => q && q.n > 0);
      const all = Object.values(raw).filter(Boolean).concat(hopsQ);
      let D = 1; all.forEach(q => { D = lcm(D, q.d); }); if (D > 1000) D = 1000;
      const K = q => Math.round(q.n * D / q.d);
      const anyFrac = all.some(q => q.kind === 'frac' && q.d > 1);
      const anyDec = all.some(q => q.kind === 'dec');

      let kmin = K(raw.min);
      let tickU = raw.tick ? Math.max(1, K(raw.tick)) : D;
      if (raw.tick && raw.tick.n <= 0) tickU = D;
      let stepU = raw.step ? Math.max(1, K(raw.step)) : 2 * D;
      let kmax;
      if (raw.max) kmax = K(raw.max);
      else if (mode === 'skip') kmax = kmin + stepU * 10;
      else kmax = kmin + 10 * D;
      if (kmax <= kmin) kmax = kmin + 10 * tickU;
      const span = kmax - kmin;
      const clampK = k => Math.max(kmin, Math.min(kmax, k));

      let fmt = p.format;
      if (!['int', 'fraction', 'mixed', 'decimal'].includes(fmt)) fmt = D === 1 ? 'int' : (anyFrac ? 'fraction' : (anyDec ? 'decimal' : 'fraction'));
      const decPlaces = Math.max(1, Math.ceil(Math.log10(D) - 1e-9));
      // ---- marks: labelled (possibly irrational) points, display only ----
      function markVal(v) {
        if (typeof v === 'number') return isFinite(v) ? v : NaN;
        const s0 = String(v == null ? '' : v).trim().replace(/[−–]/g, '-').replace(/\s+/g, '');
        let m = s0.match(/^(-?)(\d*\.?\d*)(?:√|sqrt)\(?(\d+(?:\.\d+)?)\)?$/i);
        if (m) return (m[1] ? -1 : 1) * (m[2] ? +m[2] : 1) * Math.sqrt(+m[3]);
        m = s0.match(/^(-?)(\d*\.?\d*)(?:π|pi)$/i);
        if (m) return (m[1] ? -1 : 1) * (m[2] ? +m[2] : 1) * Math.PI;
        const q = parseQ(s0); return q ? q.n / q.d : NaN;
      }
      const marks = (Array.isArray(p.marks) ? p.marks : []).map(mk => {
        const o = mk && typeof mk === 'object' ? mk : { value: mk };
        const v = markVal(o.value);
        return { v, k: v * D, label: o.label != null && o.label !== '' ? String(o.label) : String(+v.toFixed(3)).replace('-', MINUS) };
      }).filter(mk => isFinite(mk.v) && mk.k >= kmin - 1e-9 && mk.k <= kmax + 1e-9).sort((a, b) => a.v - b.v);

      // ---------- state ----------
      let start, target, snapU, hopsU;
      function setupChallenge(randomize) {
        if (!randomize) {
          if (mode === 'jump') {
            start = raw.start ? clampK(K(raw.start)) : clampK(kmin + 3 * D);
            if (raw.target) target = clampK(K(raw.target));
            else { const a = raw.add ? K(raw.add) : 5 * D; target = clampK(start + a); }
          } else if (mode === 'skip') {
            start = raw.start ? clampK(K(raw.start)) : kmin;
            if ((raw.target && clampK(K(raw.target)) <= start) || kmax - start < 2 * stepU) start = kmin;
            if (raw.target) target = clampK(K(raw.target));
            else { let n = Math.floor((kmax - start) / stepU); target = start + Math.max(1, Math.min(n, 6)) * stepU; }
          } else {
            start = raw.start ? clampK(K(raw.start)) : kmin;
            target = raw.target ? clampK(K(raw.target)) : clampK(kmin + Math.round(span / 2 / tickU) * tickU);
          }
        } else {
          const nT = Math.floor(span / tickU);
          const rnd = n => Math.floor(Math.random() * n);
          if (mode === 'jump') {
            let tries = 0;
            do { start = kmin + rnd(nT + 1) * tickU; target = kmin + rnd(nT + 1) * tickU; tries++; } while ((target === start || Math.abs(target - start) > span * 0.8) && tries < 50);
          } else if (mode === 'skip') {
            if (kmax - start < 2 * stepU) start = kmin;
            const n = Math.floor((kmax - start) / stepU);
            let t; let tries = 0; do { t = start + (2 + rnd(Math.max(1, n - 1))) * stepU; tries++; } while ((t > kmax || t === target) && tries < 30);
            if (t <= kmax) target = t;
          } else {
            let t; let tries = 0; do { t = kmin + rnd(nT + 1) * tickU; tries++; } while ((t === target || t === pos) && tries < 30);
            target = t;
          }
        }
        // snapping must be able to reach start and target
        snapU = raw.snap ? Math.max(1, K(raw.snap)) : tickU;
        snapU = gcd(gcd(snapU, target - kmin), gcd(start - kmin, snapU)) || 1;
        if (span / snapU > 400) snapU = gcd(snapU, tickU);
        // hop buttons
        if (mode === 'skip') hopsU = [stepU];
        else if (hopsQ.length) hopsU = [...new Set(hopsQ.map(K).filter(h => h > 0))].slice(0, 8);
        else { hopsU = [tickU]; if (span / tickU >= 15) hopsU.push(tickU * 5); if (span / tickU > 40) hopsU.push(tickU * 10); }
      }
      let pos = 0, hist = [], customText = p.challenge ? String(p.challenge) : '';
      setupChallenge(false);
      pos = start;

      // ---------- formatting ----------
      function parts(k) { // reduced fraction
        const g = gcd(k, D); return { n: k / g, d: D / g };
      }
      function txt(k) { // plain text
        const neg = k < 0, a = Math.abs(k); const q = parts(a); let s;
        if (fmt === 'int' || q.d === 1) s = String(q.n);
        else if (fmt === 'decimal') s = (a / D).toFixed(decPlaces);
        else if (fmt === 'mixed' && q.n > q.d) s = Math.floor(q.n / q.d) + ' ' + (q.n % q.d) + '/' + q.d;
        else s = q.n + '/' + q.d;
        return (neg ? MINUS : '') + s;
      }
      function html(k, cls) {
        const neg = k < 0, a = Math.abs(k); const q = parts(a); let s;
        const fr = (n, d) => `<span class="lb-numberline-fr"><b>${n}</b><b>${d}</b></span>`;
        if (fmt === 'int' || q.d === 1) s = String(q.n);
        else if (fmt === 'decimal') s = (a / D).toFixed(decPlaces);
        else if (fmt === 'mixed' && q.n > q.d) s = Math.floor(q.n / q.d) + fr(q.n % q.d, q.d);
        else s = fr(q.n, q.d);
        return `<span class="${cls || ''}">${neg ? MINUS : ''}${s}</span>`;
      }
      function paren(k, cls) { return k < 0 ? `<span class="${cls || ''}">(</span>${html(k, cls)}<span class="${cls || ''}">)</span>` : html(k, cls); }
      function defaultText() {
        if (mode === 'jump') {
          const d = target - start;
          return `Start at ${txt(start)}. Hop to show ${start < 0 ? '(' + txt(start) + ')' : txt(start)} ${d >= 0 ? '+' : MINUS} ${txt(Math.abs(d))}. Where do you land?`;
        }
        if (mode === 'skip') return `Skip count by ${txt(stepU)} from ${txt(start)} to reach ${txt(target)}. How many hops?`;
        return `Drag the frog to ${txt(target)}`;
      }

      // ---------- geometry ----------
      const W = 360, PX = 24, LY = 104;
      const X = k => PX + (k - kmin) / span * (W - 2 * PX);
      // mark labels sit in rows under the tick numbers; a mark goes to the 2nd row if it would overlap
      const markW = mk => Math.max(18, Array.from(mk.label).length * 7.4 + 10);
      { const lastEnd = [-1e9, -1e9]; marks.forEach(mk => { const x = X(mk.k), w = markW(mk); mk.row = x - w / 2 >= lastEnd[0] + 3 ? 0 : x - w / 2 >= lastEnd[1] + 3 ? 1 : 0; lastEnd[mk.row] = x + w / 2; }); }
      const H = 156 + (marks.length ? (marks.some(mk => mk.row) ? 38 : 20) : 0);
      const pxPerTick = (W - 2 * PX) / (span / tickU);
      // label spacing
      const labMode = ['all', 'whole', 'ends', 'none'].includes(p.labels) ? p.labels : 'auto';
      const longest = Math.max(txt(kmin).length, txt(kmax).length);
      const needPx = fmt === 'fraction' || fmt === 'mixed' ? 26 : Math.max(22, longest * 8.5 + 6);
      let labEvery = 1;
      if (labMode === 'auto') {
        const cands = fmt === 'int' ? [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000] : [1, 2, 4, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000];
        labEvery = cands.find(c => c * pxPerTick >= needPx) || 1000;
        // prefer labelling whole numbers when ticks are fractional
        if (tickU < D && D % tickU === 0 && labEvery * pxPerTick >= needPx && labEvery > 1) { const per = D / tickU; if (per * pxPerTick >= needPx && labEvery > per) labEvery = per; }
      }
      function isLabel(i, k) {
        if (labMode === 'none') return false;
        if (labMode === 'ends') return k === kmin || k === kmax;
        if (labMode === 'whole') return k % D === 0;
        if (labMode === 'all') return true;
        return kmin % tickU === 0 ? (k / tickU) % labEvery === 0 : i % labEvery === 0;
      }
      function labelSVG(k, x) {
        const neg = k < 0, a = Math.abs(k); const q = parts(a);
        const fracStyle = (fmt === 'fraction' || fmt === 'mixed') && q.d !== 1;
        const zero = k === 0;
        const col = zero ? '#1b1f3a' : (neg ? '#d04545' : '#1b1f3a');
        if (!fracStyle) return `<text x="${x}" y="${LY + 25}" text-anchor="middle" font-size="14" font-weight="800" fill="${col}">${esc(txt(k))}</text>`;
        let whole = '', n = q.n;
        if (fmt === 'mixed' && q.n > q.d) { whole = Math.floor(q.n / q.d); n = q.n % q.d; }
        const off = whole !== '' ? 5 : 0;
        return `<g fill="${col}" font-weight="800" text-anchor="middle">` +
          (neg ? `<text x="${x - 9 - off}" y="${LY + 31}" font-size="12">${MINUS}</text>` : '') +
          (whole !== '' ? `<text x="${x - 6}" y="${LY + 32}" font-size="14">${whole}</text>` : '') +
          `<text x="${x + off}" y="${LY + 22}" font-size="11">${n}</text>` +
          `<line x1="${x - 6 + off}" x2="${x + 6 + off}" y1="${LY + 26}" y2="${LY + 26}" stroke="${col}" stroke-width="1.6"/>` +
          `<text x="${x + off}" y="${LY + 37}" font-size="11">${q.d}</text></g>`;
      }

      // ---------- build DOM ----------
      host.innerHTML = `<style>${CSS}</style>
      <div class="lb-numberline-w">
        <div class="lb-numberline-ch"></div>
        <div class="lb-numberline-stage">
          <svg class="lb-numberline-svg${(mode === 'skip' && p.drag !== true) || p.drag === false ? ' nodrag' : ''}" viewBox="0 0 ${W} ${H}" role="img" aria-label="number line">
            <defs>
              <marker id="${uid}g" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#14a37f"/></marker>
              <marker id="${uid}r" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#e04848"/></marker>
            </defs>
            <g class="axis"></g><g class="tgt"></g><g class="arcs"></g><g class="frog"></g>
          </svg>
        </div>
        <div class="lb-numberline-eq"></div>
        <div class="lb-numberline-seq"></div>
        <div class="lb-numberline-hint"></div>
        <div class="lb-numberline-btns"></div>
      </div>`;
      const $ = s => host.querySelector(s);
      const svg = $('svg'), gAxis = $('.axis'), gTgt = $('.tgt'), gArcs = $('.arcs'), gFrog = $('.frog');
      const chEl = $('.lb-numberline-ch'), eqEl = $('.lb-numberline-eq'), seqEl = $('.lb-numberline-seq'), hintEl = $('.lb-numberline-hint'), btnEl = $('.lb-numberline-btns');
      const canDrag = !((mode === 'skip' && p.drag !== true) || p.drag === false);
      const showTarget = p.showTarget != null ? !!p.showTarget : mode !== 'place';

      function drawAxis() {
        let s = `<line x1="${PX - 14}" x2="${W - PX + 14}" y1="${LY}" y2="${LY}" stroke="#1b1f3a" stroke-width="3" stroke-linecap="round"/>`;
        s += `<path d="M${PX - 18} ${LY}l8 -6v12z" fill="#1b1f3a"/><path d="M${W - PX + 18} ${LY}l-8 -6v12z" fill="#1b1f3a"/>`;
        const n = Math.round(span / tickU);
        const drawMinor = pxPerTick >= 3;
        for (let i = 0; i <= n; i++) {
          const k = kmin + i * tickU; const x = X(k).toFixed(2);
          const lab = isLabel(i, k);
          const whole = k % D === 0;
          if (!drawMinor && !lab) continue;
          const h = lab ? 9 : (whole ? 7 : 5);
          s += `<line x1="${x}" x2="${x}" y1="${LY - h}" y2="${LY + h}" stroke="${k === 0 ? '#7c4ddb' : '#1b1f3a'}" stroke-width="${lab || whole ? 2.2 : 1.4}"/>`;
          if (lab) s += labelSVG(k, +x);
        }
        marks.forEach(mk => {
          const x = X(mk.k), ly = LY + 54 + mk.row * 18, w = markW(mk), lx = Math.max(w / 2 + 2, Math.min(W - w / 2 - 2, x));
          s += `<g class="mark"><line x1="${x.toFixed(2)}" x2="${x.toFixed(2)}" y1="${LY}" y2="${ly - 12}" stroke="#ff6b6b" stroke-width="1.4" stroke-dasharray="3 3"/>` +
            `<rect x="${(lx - w / 2).toFixed(1)}" y="${ly - 12}" width="${w.toFixed(1)}" height="17" rx="8" fill="#fff" stroke="#ff6b6b" stroke-width="1.6"/>` +
            `<text x="${lx.toFixed(1)}" y="${ly + 1}" text-anchor="middle" font-size="12.5" font-weight="800" fill="#d04545">${esc(mk.label)}</text>` +
            `<circle cx="${x.toFixed(2)}" cy="${LY}" r="5" fill="#ff6b6b" stroke="#fff" stroke-width="1.6"/></g>`;
        });
        gAxis.innerHTML = s;
      }
      function drawTarget() {
        if (!showTarget) { gTgt.innerHTML = ''; return; }
        const x = X(target);
        gTgt.innerHTML = `<circle cx="${x}" cy="${LY}" r="7" fill="#ffc93c" stroke="#e0a400" stroke-width="2"/>
          <line x1="${x}" x2="${x}" y1="${LY - 6}" y2="${LY - 46}" stroke="#b07d00" stroke-width="2.4"/>
          <path d="M${x} ${LY - 46}l18 6l-18 6z" fill="#ff6b6b"/>`;
      }
      const FROG = `<g class="body">
        <ellipse cx="0" cy="-2" rx="15" ry="4" fill="#000" opacity=".12"/>
        <ellipse cx="-9" cy="-4" rx="6" ry="3.5" fill="#1fae84"/><ellipse cx="9" cy="-4" rx="6" ry="3.5" fill="#1fae84"/>
        <ellipse cx="0" cy="-14" rx="14" ry="11" fill="#2ed3a5" stroke="#1a9c78" stroke-width="2"/>
        <ellipse cx="0" cy="-10" rx="8" ry="5.5" fill="#bff5e3"/>
        <circle cx="-7" cy="-25" r="6" fill="#2ed3a5" stroke="#1a9c78" stroke-width="2"/><circle cx="7" cy="-25" r="6" fill="#2ed3a5" stroke="#1a9c78" stroke-width="2"/>
        <circle cx="-7" cy="-25" r="3.6" fill="#fff"/><circle cx="7" cy="-25" r="3.6" fill="#fff"/>
        <circle cx="-6.4" cy="-25" r="1.9" fill="#1b1f3a"/><circle cx="7.6" cy="-25" r="1.9" fill="#1b1f3a"/>
        <path d="M-5 -16q5 4 10 0" stroke="#1b1f3a" stroke-width="1.8" fill="none" stroke-linecap="round"/>
        <circle cx="-9" cy="-15" r="1.8" fill="#ff9fb0" opacity=".8"/><circle cx="9" cy="-15" r="1.8" fill="#ff9fb0" opacity=".8"/>
      </g>`;
      gFrog.innerHTML = FROG;
      let frogX = X(pos), frogY = 0;
      const placeFrog = () => gFrog.setAttribute('transform', `translate(${frogX.toFixed(2)},${(LY - 1 + frogY).toFixed(2)})`);

      function arcSVG(a, b, idx) {
        const x1 = X(a), x2 = X(b), dx = Math.abs(x2 - x1);
        const h = Math.min(58, 14 + dx * 0.38);
        const y0 = LY - 6, cy = y0 - h * 2 + 6;
        const pos2 = b > a; const col = pos2 ? '#14a37f' : '#e04848';
        const len = Math.round(dx * 1.6 + h * 2);
        const label = (pos2 ? '+' : MINUS) + txt(Math.abs(b - a));
        const ly = y0 - h + 2;
        const mx = (x1 + x2) / 2;
        const showLab = dx > 12;
        return `<path class="lb-numberline-arc" style="--len:${len}" d="M${x1.toFixed(1)} ${y0} Q${mx.toFixed(1)} ${cy.toFixed(1)} ${x2.toFixed(1)} ${y0}" stroke="${col}" marker-end="url(#${uid}${pos2 ? 'g' : 'r'})"/>` +
          (showLab ? `<g><rect x="${(mx - label.length * 4 - 5).toFixed(1)}" y="${(ly - 13).toFixed(1)}" width="${label.length * 8 + 10}" height="17" rx="8" fill="#fff" stroke="${col}" stroke-width="1.5"/><text x="${mx.toFixed(1)}" y="${(ly - 0.5).toFixed(1)}" text-anchor="middle" font-size="12" font-weight="800" fill="${col}">${esc(label)}</text></g>` : '');
      }
      function drawArcs() { const H2 = hist.slice(-14); gArcs.innerHTML = H2.map((h, i) => arcSVG(h[0], h[1], i)).join(''); }

      function readout() {
        if (mode === 'jump') {
          if (!hist.length) { eqEl.innerHTML = `<span>Frog at</span>${html(pos, 'v')}`; seqEl.textContent = 'Tap a hop button or drag the frog'; return; }
          const d = pos - start;
          eqEl.innerHTML = `${paren(start)} <span class="${d >= 0 ? 'g' : 'r'}">${d >= 0 ? '+' : MINUS}</span> ${html(Math.abs(d), d >= 0 ? 'g' : 'r')} <span>=</span> ${html(pos, 'v')}`;
          const hs = hist.slice(-8).map(h => (h[1] > h[0] ? '+' : MINUS) + txt(Math.abs(h[1] - h[0])));
          seqEl.textContent = 'Hops: ' + (hist.length > 8 ? '… ' : '') + hs.join('  ');
        } else if (mode === 'skip') {
          const n = Math.round((pos - start) / stepU);
          const vals = [start]; hist.forEach(h => vals.push(h[1]));
          seqEl.textContent = (vals.length > 9 ? '… ' : '') + vals.slice(-9).map(txt).join(' → ');
          if (!hist.length) { eqEl.innerHTML = `<span>Frog at</span>${html(pos, 'v')}`; return; }
          if ((pos - start) % stepU === 0 && n >= 0) {
            eqEl.innerHTML = start === 0
              ? `<span class="g">${n}</span><span>hop${n === 1 ? '' : 's'} of</span>${html(stepU, 'g')}<span>=</span>${html(pos, 'v')}`
              : `${paren(start)}<span>+</span><span class="g">${n}</span><span>×</span>${html(stepU, 'g')}<span>=</span>${html(pos, 'v')}`;
          } else eqEl.innerHTML = `<span>Frog at</span>${html(pos, 'v')}`;
        } else {
          let extra = '';
          if (p.showDecimal && D > 1 && fmt !== 'decimal' && pos % D !== 0) {
            const v = pos / D; const s = Number.isInteger(v) ? String(v) : String(+v.toFixed(3));
            extra = `<span>=</span><span class="g">${(v < 0 ? MINUS : '') + s.replace('-', '')}</span>`;
          }
          eqEl.innerHTML = `<span>Frog at</span>${html(pos, 'v')}${extra}`;
          seqEl.textContent = canDrag ? 'Drag the frog along the line' : '';
        }
      }
      function setChallengeText() { chEl.textContent = '🎯 Challenge: ' + (customText || defaultText()); }

      // ---------- buttons ----------
      function buildButtons() {
        let s = '';
        if (mode === 'skip') {
          s += `<button class="lb-numberline-b m" data-h="${-stepU}" aria-label="back">${MINUS}${esc(txt(stepU))}</button>`;
          s += `<button class="lb-numberline-b" data-h="${stepU}" style="min-width:110px">Hop +${esc(txt(stepU))}</button>`;
        } else if (mode === 'jump' || !canDrag || p.hops) {
          const hs = hopsU.slice().sort((a, b) => b - a), many = hs.length > 3;
          // 4+ hop sizes: compact buttons, one row of − hops and one row of + hops
          const row = many ? '<span class="lb-numberline-br"></span>' : '';
          hs.forEach(h => { s += `<button class="lb-numberline-b m${many ? ' c' : ''}" data-h="${-h}">${MINUS}${esc(txt(h))}</button>`; });
          s += row;
          hs.slice().reverse().forEach(h => { s += `<button class="lb-numberline-b${many ? ' c' : ''}" data-h="${h}">+${esc(txt(h))}</button>`; });
          s += row;
        }
        s += `<button class="lb-numberline-b s" data-act="reset">↺ Reset</button>`;
        if (p.newChallenge !== false) s += `<button class="lb-numberline-b s" data-act="new">✨ New</button>`;
        btnEl.innerHTML = s;
      }

      // ---------- animation ----------
      let raf = 0, busy = false, won = false;
      function animateTo(k, done) {
        cancelAnimationFrame(raf);
        const x0 = frogX, x1 = X(k), dist = Math.abs(x1 - x0);
        const hh = Math.min(50, 10 + dist * 0.3);
        const t0 = performance.now(), dur = Math.min(520, 260 + dist * 1.2);
        busy = true;
        const stepF = now => {
          const t = Math.min(1, (now - t0) / dur);
          const e = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
          frogX = x0 + (x1 - x0) * e; frogY = -4 * hh * t * (1 - t);
          placeFrog();
          if (t < 1) raf = requestAnimationFrame(stepF); else { frogY = 0; placeFrog(); busy = false; done && done(); }
        };
        raf = requestAnimationFrame(stepF);
      }
      function hint(t) { hintEl.textContent = t || ''; }
      function shake() { const st = host.querySelector('.lb-numberline-stage'); st.classList.remove('lb-numberline-shake'); void st.offsetWidth; st.classList.add('lb-numberline-shake'); }

      function checkWin(final) {
        if (won || pos !== target) {
          if (!won && final && mode === 'place') {
            const d = target - pos; hint(d > 0 ? 'Not yet — go a bit to the right ➡' : 'Not yet — go a bit to the left ⬅'); api.sfx('hmm');
          }
          return;
        }
        if (mode !== 'place' && !hist.length) return;
        won = true;
        let msg;
        if (mode === 'jump') { const d = pos - start; msg = `${start < 0 ? '(' + txt(start) + ')' : txt(start)} ${d >= 0 ? '+' : MINUS} ${txt(Math.abs(d))} = ${txt(pos)}. You landed on ${txt(pos)}!`; }
        else if (mode === 'skip') { const n = Math.round((pos - start) / stepU); msg = `${n} hops of ${txt(stepU)} ${start ? 'from ' + txt(start) + ' ' : ''}= ${txt(pos)}!`; }
        else msg = `The frog is on ${txt(target)}!`;
        hint('⭐ Great hopping!');
        api.sfx('correct');
        api.win(msg);
      }

      function hop(h) {
        if (busy) return;
        const k = pos + h;
        if (k < kmin || k > kmax) { api.sfx('wrong'); hint('The line ends here!'); shake(); return; }
        api.sfx('tap'); hint('');
        const from = pos; pos = k; hist.push([from, k]); drawArcs(); readout();
        animateTo(k, () => checkWin(true));
      }
      function reset() {
        cancelAnimationFrame(raf); busy = false;
        pos = start; hist = []; frogX = X(pos); frogY = 0; placeFrog(); drawArcs(); readout(); hint('');
      }
      function newChallenge() {
        setupChallenge(true); customText = '';
        if (won) { won = false; api.resetWin && api.resetWin(); }
        drawTarget(); setChallengeText(); buildButtons(); reset(); api.sfx('tap');
      }
      btnEl.addEventListener('click', e => {
        const b = e.target.closest('button'); if (!b) return;
        if (b.dataset.act === 'reset') { reset(); return; }
        if (b.dataset.act === 'new') { newChallenge(); return; }
        hop(+b.dataset.h);
      });

      // ---------- dragging ----------
      let dragging = false, dragFrom = 0, lastSnap = 0;
      function toK(ev) {
        const r = svg.getBoundingClientRect();
        const vx = (ev.clientX - r.left) / r.width * W;
        const raw2 = kmin + (vx - PX) / (W - 2 * PX) * span;
        return clampK(kmin + Math.round((raw2 - kmin) / snapU) * snapU);
      }
      function onDown(ev) {
        if (!canDrag || busy) return;
        dragging = true; dragFrom = pos; lastSnap = pos;
        try { svg.setPointerCapture(ev.pointerId); } catch (e) { }
        onMove(ev); ev.preventDefault();
      }
      function onMove(ev) {
        if (!dragging) return;
        const k = toK(ev);
        const r = svg.getBoundingClientRect();
        frogX = Math.max(PX, Math.min(W - PX, (ev.clientX - r.left) / r.width * W)); frogY = -8; placeFrog();
        if (k !== lastSnap) { lastSnap = k; pos = k; readout(); }
      }
      function onUp() {
        if (!dragging) return; dragging = false;
        pos = lastSnap; frogY = 0;
        if (pos !== dragFrom) { hist.push([dragFrom, pos]); drawArcs(); api.sfx('tap'); }
        hint(''); readout();
        animateTo(pos, () => checkWin(true));
      }
      svg.addEventListener('pointerdown', onDown);
      svg.addEventListener('pointermove', onMove);
      svg.addEventListener('pointerup', onUp);
      svg.addEventListener('pointercancel', onUp);

      // ---------- go ----------
      drawAxis(); drawTarget(); setChallengeText(); buildButtons(); placeFrog(); drawArcs(); readout();
      return () => { cancelAnimationFrame(raf); };
    },
    example: {
      mode: 'jump', min: 0, max: 20, start: 7, add: 5
    },
    examples: [
      { mode: 'jump', min: -10, max: 10, start: 3, add: -7, challenge: 'Find 3 − 7 using hops. Can the frog go below zero?' },
      { mode: 'skip', min: 0, max: 50, start: 0, step: 5, target: 35, tick: 5, challenge: 'Skip count by 5s to reach 35. How many hops of 5 make 35?' },
      { mode: 'place', min: 0, max: 2, tick: '1/4', start: 0, target: '5/4', format: 'mixed', showDecimal: true, challenge: 'Drag the frog to 1¼ (five quarters).' },
      { mode: 'jump', min: 0, max: 16, start: 0, target: 15, hops: [8, 4, 2, 1], challenge: 'Reach 15 using each hop size 8, 4, 2 and 1 once.' },
      { mode: 'place', min: 0, max: 3.5, tick: 0.5, start: 0, target: 1.5, marks: [{ value: '√2', label: '√2' }, { value: 'sqrt(5)', label: '√5' }, { value: 'π', label: 'π' }], challenge: '√2 ≈ 1.41 and √5 ≈ 2.24 are marked. Drag the frog to 1.5 — is it between √2 and √5?' }
    ]
  });
})();
