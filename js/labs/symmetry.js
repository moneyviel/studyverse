/* StudyVerse Concept Lab: symmetry — "Symmetry studio"
 * Three hands-on ways to explore symmetry:
 *  mirror : paint squares on a grid; a mirror line (or two) reflects them. Either the mirror paints
 *           for you (auto) or you must complete the mirror image of a given half-picture yourself.
 *  rotate : drag to turn a shape over its faint outline; count how many times it fits in one turn.
 *  lines  : tap the dashed lines to test them as mirror lines (the shape is folded over the line).
 * Symmetry facts (lines, order) are COMPUTED from the shape's geometry, so they are always correct.
 *
 * PARAMS (all optional; defaults in brackets)
 *  mode      string  'mirror' | 'rotate' | 'lines'                                           ['mirror']
 *  line      string  mirror: 'vertical' | 'horizontal' | 'diagonal' | 'both' (vertical + horizontal) ['vertical']
 *  n         number  mirror: grid size n × n (4–12)                                          [10]
 *  auto      bool    mirror: true = the mirror paints the reflection for you (free design);
 *                    false = complete the picture yourself                                    [false]
 *  shape     array|string  mirror: given cells [[col,row],...] (0-based, row 0 = top) on one side of the line
 *                    [a half-heart]
 *                    rotate/lines: shape name: 'square','rectangle','triangle','isosceles','pentagon','hexagon',
 *                    'star','plus','pinwheel','parallelogram','kite','trapezium','A','H','E','M','T','X','Z','N','I'
 *                                                                                              ['square' / 'H']
 *  shapes    array   rotate/lines: list of shape names used by "New challenge"                [a mixed list]
 *  minCells  number  mirror with auto=true: squares to colour for the challenge              [12]
 *  colors    array   mirror with auto=true: paint colours (CSS colours)                     [mint, violet, sun, coral]
 *  challenge string  challenge text (English or Hindi); default is generated
 *  winText   string  message on success
 */
(function () {
  const C = { violet: '#8b5cf6', mint: '#2ed3a5', sun: '#ffc93c', coral: '#ff6b6b', blue: '#3b82f6', ink: '#1b1f3a', muted: '#6b7090' };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const lc = s => s.charAt(0).toLowerCase() + s.slice(1);
  const rad = d => d * Math.PI / 180, norm = a => ((a % 360) + 360) % 360;

  // ---------- shape library (unit coords, y up, centred at the origin) ----------
  const reg = (n, r = 1, rot = 90) => Array.from({ length: n }, (_, k) => [r * Math.cos(rad(rot + k * 360 / n)), r * Math.sin(rad(rot + k * 360 / n))]);
  const star = () => Array.from({ length: 10 }, (_, k) => { const r = k % 2 ? 0.42 : 1, a = 90 + k * 36; return [r * Math.cos(rad(a)), r * Math.sin(rad(a))]; });
  const rotP = (pts, a) => pts.map(([x, y]) => [x * Math.cos(rad(a)) - y * Math.sin(rad(a)), x * Math.sin(rad(a)) + y * Math.cos(rad(a))]);
  const SHAPES = {
    square: { name: 'Square', polys: [reg(4, 1, 45)] },
    rectangle: { name: 'Rectangle', polys: [[[-1, -.55], [1, -.55], [1, .55], [-1, .55]]] },
    triangle: { name: 'Equilateral triangle', polys: [reg(3, 1, 90)] },
    isosceles: { name: 'Isosceles triangle', polys: [[[-.6, -.8], [.6, -.8], [0, .95]]] },
    pentagon: { name: 'Regular pentagon', polys: [reg(5)] },
    hexagon: { name: 'Regular hexagon', polys: [reg(6, 1, 0)] },
    star: { name: 'Star', polys: [star()] },
    plus: { name: 'Plus sign', polys: [[[-.3, 1], [.3, 1], [.3, .3], [1, .3], [1, -.3], [.3, -.3], [.3, -1], [-.3, -1], [-.3, -.3], [-1, -.3], [-1, .3], [-.3, .3]]] },
    pinwheel: { name: 'Pinwheel', polys: [0, 90, 180, 270].map(a => rotP([[0, 0], [1, 0], [1, .5]], a)) },
    parallelogram: { name: 'Parallelogram', polys: [[[-1, -.5], [.4, -.5], [1, .5], [-.4, .5]]] },
    kite: { name: 'Kite', polys: [[[0, 1], [.55, .3], [0, -1], [-.55, .3]]] },
    trapezium: { name: 'Isosceles trapezium', polys: [[[-1, -.5], [1, -.5], [.5, .5], [-.5, .5]]] },
    A: { name: 'Letter A', strokes: [[[-.65, -1], [0, 1], [.65, -1]], [[-.37, -.15], [.37, -.15]]] },
    H: { name: 'Letter H', strokes: [[[-.6, -1], [-.6, 1]], [[.6, -1], [.6, 1]], [[-.6, 0], [.6, 0]]] },
    E: { name: 'Letter E', strokes: [[[.5, 1], [-.5, 1], [-.5, -1], [.5, -1]], [[-.5, 0], [.35, 0]]] },
    M: { name: 'Letter M', strokes: [[[-.7, -1], [-.7, 1], [0, 0], [.7, 1], [.7, -1]]] },
    T: { name: 'Letter T', strokes: [[[-.7, 1], [.7, 1]], [[0, 1], [0, -1]]] },
    X: { name: 'Letter X', strokes: [[[-.7, -1], [.7, 1]], [[-.7, 1], [.7, -1]]] },
    Z: { name: 'Letter Z', strokes: [[[-.7, 1], [.7, 1], [-.7, -1], [.7, -1]]] },
    N: { name: 'Letter N', strokes: [[[-.6, -1], [-.6, 1], [.6, -1], [.6, 1]]] },
    I: { name: 'Letter I', strokes: [[[-.45, 1], [.45, 1]], [[0, 1], [0, -1]], [[-.45, -1], [.45, -1]]] }
  };
  function segsOf(sh) {
    const out = [];
    (sh.polys || []).forEach(pl => pl.forEach((q, i) => out.push([q, pl[(i + 1) % pl.length]])));
    (sh.strokes || []).forEach(pl => { for (let i = 0; i + 1 < pl.length; i++) out.push([pl[i], pl[i + 1]]); });
    return out;
  }
  function sameSet(a, b) {
    const e = 1e-4, eqp = (p, q) => Math.abs(p[0] - q[0]) < e && Math.abs(p[1] - q[1]) < e;
    return a.length === b.length && a.every(s => b.some(t => (eqp(s[0], t[0]) && eqp(s[1], t[1])) || (eqp(s[0], t[1]) && eqp(s[1], t[0]))));
  }
  const reflectPt = (q, a) => { const c = Math.cos(rad(2 * a)), s = Math.sin(rad(2 * a)); return [q[0] * c + q[1] * s, q[0] * s - q[1] * c]; };
  function symInfo(sh) {
    const S = segsOf(sh), lines = [], fits = [];
    for (let a = 0; a < 180; a++) if (sameSet(S.map(sg => sg.map(q => reflectPt(q, a))), S)) lines.push(a);
    for (let a = 1; a <= 360; a++) if (sameSet(S.map(sg => rotP(sg, a)), S)) fits.push(a);
    return { lines, fits, order: fits.length };
  }

  const CSS = `
.lb-symmetry-w{font-size:14px;color:${C.ink}}
.lb-symmetry-ch{background:#fff6d8;border-radius:12px;padding:6px 6px 6px 11px;font-weight:800;font-size:14px;margin-bottom:8px;line-height:1.3;display:flex;align-items:center;gap:6px}
.lb-symmetry-ch span{flex:1}
.lb-symmetry-ch .lb-symmetry-b{flex-shrink:0;font-size:13px;padding:0 10px}
.lb-symmetry-svg{width:100%;height:auto;display:block;margin:0 auto;touch-action:none;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:18px;user-select:none;-webkit-user-select:none}
.lb-symmetry-svg.sq{max-width:272px}
.lb-symmetry-svg text{font-family:inherit;pointer-events:none}
.lb-symmetry-read{margin-top:8px;background:#f4f6ff;border-radius:12px;padding:7px 10px;font-weight:800;font-size:13.5px;line-height:1.4;min-height:22px}
.lb-symmetry-row{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap;align-items:center}
.lb-symmetry-b{min-height:40px;min-width:40px;border:none;border-radius:12px;background:#f1efff;color:${C.ink};font:inherit;font-weight:800;font-size:14px;padding:0 12px;cursor:pointer}
.lb-symmetry-b.go{background:${C.violet};color:#fff;margin-left:auto}
.lb-symmetry-b.on{outline:3px solid ${C.ink};outline-offset:-3px}
.lb-symmetry-b:active{transform:scale(.95)}
.lb-symmetry-sw{width:40px;height:40px;border-radius:50%;border:3px solid #fff;box-shadow:0 0 0 2px #e3e6f6;cursor:pointer;padding:0}
.lb-symmetry-sw.on{box-shadow:0 0 0 3px ${C.ink}}
.lb-symmetry-ord{display:flex;gap:4px;flex-wrap:nowrap;align-items:center;margin-top:8px}
.lb-symmetry-ord span{font-weight:800;font-size:13px;margin-right:2px}
.lb-symmetry-ord .lb-symmetry-b{min-width:32px;padding:0 4px;flex:1;max-width:44px}
@keyframes lbsymfit{0%{opacity:0}30%{opacity:1}100%{opacity:0}}
.lb-symmetry-flash{animation:lbsymfit 1s ease}
`;

  function render(host, p, api) {
    const mode = ['mirror', 'rotate', 'lines'].includes(p.mode) ? p.mode : 'mirror';
    let challengeText = p.challenge ? String(p.challenge) : null, won = false;
    host.innerHTML = `<style>${CSS}</style><div class="lb-symmetry-w"><div class="lb-symmetry-ch"><span></span>${mode !== 'lines' ? `<button class="lb-symmetry-b" data-reset aria-label="Start again">↺</button>` : ''}<button class="lb-symmetry-b go" data-new aria-label="New challenge">🔄 ${mode === 'mirror' ? 'Next' : 'New'}</button></div><svg class="lb-symmetry-svg"></svg><div class="lb-symmetry-read"></div><div class="lb-symmetry-ctl"></div></div>`;
    const svg = host.querySelector('svg'), rd = host.querySelector('.lb-symmetry-read'), ctl = host.querySelector('.lb-symmetry-ctl'), chEl = host.querySelector('.lb-symmetry-ch span');
    const showCh = t => { chEl.textContent = '🎯 Challenge: ' + (challengeText || t); };
    const win = m => { if (won) return; won = true; api.sfx('correct'); api.win(p.winText || m); };
    function svgXY(e) { const m = svg.getScreenCTM(); if (!m) return null; const q = svg.createSVGPoint(); q.x = e.clientX; q.y = e.clientY; const t = q.matrixTransform(m.inverse()); return [t.x, t.y]; }
    let cleanup = [];
    const on = (el, ev, fn) => { el.addEventListener(ev, fn); cleanup.push(() => el.removeEventListener(ev, fn)); };
    let timers = [];

    if (mode === 'mirror') {
      // ================= MIRROR GRID =================
      const n = Math.max(4, Math.min(12, Math.round(+p.n) || 10));
      const line = ['vertical', 'horizontal', 'diagonal', 'both'].includes(p.line) ? p.line : 'vertical';
      const auto = p.auto === true;
      const u = 280 / n, pad = 10, S = n * u + pad * 2;
      svg.setAttribute('viewBox', `0 0 ${S} ${S}`); svg.classList.add('sq');
      const images = (c, r) => {
        const out = [[c, r]];
        if (line === 'vertical') out.push([n - 1 - c, r]);
        if (line === 'horizontal') out.push([c, n - 1 - r]);
        if (line === 'diagonal') out.push([r, c]);
        if (line === 'both') out.push([n - 1 - c, r], [c, n - 1 - r], [n - 1 - c, n - 1 - r]);
        return out;
      };
      const key = (c, r) => c + ',' + r;
      // default half-heart (left half of a 10-wide heart), scaled to n
      const HEART = [[1, 2], [2, 2], [0, 3], [1, 3], [2, 3], [3, 3], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [1, 6], [2, 6], [3, 6], [4, 6], [2, 7], [3, 7], [4, 7], [3, 8], [4, 8]];
      let given = [];
      if (!auto) {
        let src = Array.isArray(p.shape) ? p.shape : null;
        if (!src) {
          src = n === 10 ? HEART : HEART.map(([c, r]) => [Math.round(c * n / 10), Math.round(r * n / 10)]);
          if (line === 'horizontal') src = src.map(([c, r]) => [r, c]);      // top half
          if (line === 'diagonal') src = src.map(([c, r]) => [c, r]).filter(([c, r]) => c < r); // below the diagonal
          if (line === 'both') src = src.filter(([c, r]) => r < n / 2);
        }
        given = [...new Set(src.filter(q => Array.isArray(q) && q[0] >= 0 && q[1] >= 0 && q[0] < n && q[1] < n).map(q => key(q[0], q[1])))];
      }
      const givenSet = new Set(given);
      const goalSet = new Set(); given.forEach(k => { const [c, r] = k.split(',').map(Number); images(c, r).forEach(q => goalSet.add(key(q[0], q[1]))); });
      const cols = Array.isArray(p.colors) && p.colors.length ? p.colors.map(String).slice(0, 5) : [C.mint, C.violet, C.sun, C.coral];
      let col = cols[0];
      const paint = new Map(); // key -> colour (child's squares)
      const minCells = Math.max(2, +p.minCells || 12);

      ctl.innerHTML = `<div class="lb-symmetry-row">${auto ? cols.map((c, i) => `<button class="lb-symmetry-sw ${i ? '' : 'on'}" data-c="${i}" style="background:${esc(c)}" aria-label="colour"></button>`).join('') + `<button class="lb-symmetry-sw" data-c="-1" style="background:#fff" aria-label="eraser" title="Eraser">✕</button>` : ''}</div>`;
      let curLine = line;
      function draw() {
        let s = '';
        for (let c = 0; c < n; c++) for (let r = 0; r < n; r++) {
          const k = key(c, r), x = pad + c * u, y = pad + r * u;
          const fill = givenSet.has(k) ? C.blue : paint.get(k);
          s += `<rect x="${x + 1}" y="${y + 1}" width="${u - 2}" height="${u - 2}" rx="${u * .18}" fill="${fill || '#fff'}" ${fill ? '' : 'stroke="#e3e6f6"'} />`;
        }
        const L0 = pad, L1 = pad + n * u, M = pad + n * u / 2;
        const ml = (x1, y1, x2, y2) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${C.coral}" stroke-width="3.5" stroke-dasharray="9 6" stroke-linecap="round"/>`;
        if (line === 'vertical' || line === 'both') s += ml(M, L0 - 4, M, L1 + 4);
        if (line === 'horizontal' || line === 'both') s += ml(L0 - 4, M, L1 + 4, M);
        if (line === 'diagonal') s += ml(L0 - 3, L0 - 3, L1 + 3, L1 + 3);
        svg.innerHTML = s;
        readout();
      }
      function readout() {
        if (auto) { const used = new Set(paint.values()).size; rd.innerHTML = `Coloured squares: <b style="color:${C.violet}">${paint.size}</b> · colours used: ${used}`; return; }
        let need = 0, wrong = 0; goalSet.forEach(k => { if (!givenSet.has(k) && !paint.has(k)) need++; }); paint.forEach((v, k) => { if (!goalSet.has(k)) wrong++; });
        rd.innerHTML = `Squares still to paint: <b style="color:${C.violet}">${need}</b>${wrong ? ` · <span style="color:${C.coral}">wrong squares: ${wrong}</span>` : ''}<br><span style="color:${C.muted}">Each blue square needs a twin, the same distance from the mirror.</span>`;
      }
      function check() {
        if (auto) { if (paint.size >= minCells && new Set(paint.values()).size >= 2) win(`Beautiful! A symmetric design with ${paint.size} squares.`); return; }
        let ok = true; goalSet.forEach(k => { if (!givenSet.has(k) && !paint.has(k)) ok = false; }); paint.forEach((v, k) => { if (!goalSet.has(k)) ok = false; });
        if (ok && goal_nonempty()) win('Perfect mirror image! Both halves match exactly.');
      }
      const goal_nonempty = () => goalSet.size > givenSet.size;
      let painting = false, mode2 = true, last = null;
      function cellAt(q) { const c = Math.floor((q[0] - pad) / u), r = Math.floor((q[1] - pad) / u); return c >= 0 && r >= 0 && c < n && r < n ? [c, r] : null; }
      function apply(c, r) {
        const k = key(c, r); if (k === last) return; last = k;
        if (givenSet.has(k)) return;
        const targets = auto ? images(c, r) : [[c, r]];
        targets.forEach(([a, b]) => { const kk = key(a, b); if (givenSet.has(kk)) return; if (mode2 && col) paint.set(kk, auto ? col : C.violet); else paint.delete(kk); });
        draw();
      }
      on(svg, 'pointerdown', e => { const q = svgXY(e); const cr = q && cellAt(q); if (!cr) return; const k = key(cr[0], cr[1]); if (givenSet.has(k)) { api.sfx('hmm'); return; }
        mode2 = auto ? (col !== null && paint.get(k) !== col) : !paint.has(k); painting = true; last = null; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); apply(cr[0], cr[1]); api.sfx('tap'); e.preventDefault(); });
      on(svg, 'pointermove', e => { if (!painting) return; const q = svgXY(e); const cr = q && cellAt(q); if (cr) apply(cr[0], cr[1]); });
      const up = () => { if (!painting) return; painting = false; check(); };
      on(svg, 'pointerup', up); on(svg, 'pointercancel', up);
      ctl.querySelectorAll('[data-c]').forEach(b => on(b, 'click', () => { const i = +b.dataset.c; col = i < 0 ? null : cols[i]; ctl.querySelectorAll('[data-c]').forEach(x => x.classList.toggle('on', x === b)); api.sfx('tap'); }));
      on(host.querySelector('[data-reset]'), 'click', () => { paint.clear(); api.sfx('tap'); draw(); });
      // "New line" re-renders the lab with the next mirror line
      on(host.querySelector('[data-new]'), 'click', () => {
        const order = ['vertical', 'horizontal', 'diagonal', 'both'], nx = order[(order.indexOf(curLine) + 1) % order.length];
        api.resetWin && api.resetWin(); api.sfx('tap');
        cleanup.forEach(f => f()); cleanup = [];
        const np = Object.assign({}, p, { line: nx, challenge: null, shape: null });
        const c2 = render(host, np, api); cleanup.push(c2);
      });
      showCh(auto ? `Paint a symmetric design with at least ${minCells} squares and 2 colours` : `Complete the picture so it is symmetric about the ${line === 'both' ? 'two dashed lines' : line === 'diagonal' ? 'diagonal line' : line + ' line'}`);
      draw();
    } else {
      // ================= ROTATE / LINES =================
      const names = Object.keys(SHAPES);
      const pickName = v => SHAPES[v] ? v : null;
      let shapeName = pickName(p.shape) || (mode === 'rotate' ? 'square' : 'H');
      const pool = (Array.isArray(p.shapes) ? p.shapes.filter(pickName) : null) || (mode === 'rotate' ? ['square', 'triangle', 'rectangle', 'pinwheel', 'star', 'Z', 'hexagon', 'parallelogram', 'kite', 'plus'] : ['H', 'square', 'triangle', 'A', 'rectangle', 'X', 'pentagon', 'E', 'Z', 'kite', 'hexagon', 'parallelogram']);
      const W = 360, Hh = 220, cx = 180, cy = 110, K = 78;
      svg.setAttribute('viewBox', `0 0 ${W} ${Hh}`);
      let sh, info, rot = 0, fitsFound = new Set(), foundLines = new Set(), flash = null, lastRaw = null, total = 0;
      const toS = ([x, y]) => [cx + x * K, cy - y * K];
      const shapeSVG = (shape, tf, style) => {
        let s = '';
        (shape.polys || []).forEach(pl => { s += `<path d="M${pl.map(q => tf(q)).map(q => q[0].toFixed(1) + ' ' + q[1].toFixed(1)).join(' L')}Z" ${style.poly}/>`; });
        (shape.strokes || []).forEach(pl => { s += `<path d="M${pl.map(q => tf(q)).map(q => q[0].toFixed(1) + ' ' + q[1].toFixed(1)).join(' L')}" fill="none" stroke-linecap="round" stroke-linejoin="round" ${style.stroke}/>`; });
        return s;
      };
      function setShape(nm) { shapeName = nm; sh = SHAPES[nm]; info = symInfo(sh); rot = 0; total = 0; fitsFound = new Set(); foundLines = new Set(); }
      setShape(shapeName);
      const candidates = () => [...new Set([...info.lines, 0, 45, 90, 135])].sort((a, b) => a - b);

      if (mode === 'rotate') {
        const maxBtn = Math.max(8, info.order);
        ctl.innerHTML = `<div class="lb-symmetry-ord"><span>Order</span>${Array.from({ length: maxBtn }, (_, i) => `<button class="lb-symmetry-b" data-o="${i + 1}">${i + 1}</button>`).join('')}</div>`;
      } else {
        ctl.innerHTML = `<div class="lb-symmetry-row"><button class="lb-symmetry-b" data-done>✔ I found them all</button></div>`;
      }
      function draw() {
        let s = '';
        if (mode === 'rotate') {
          // dial showing fits found
          s += `<circle cx="${cx}" cy="${cy}" r="100" fill="none" stroke="#e3e6f6" stroke-width="2"/>`;
          fitsFound.forEach(a => { const q = [cx + 100 * Math.cos(rad(a)), cy - 100 * Math.sin(rad(a))]; s += `<circle cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="6" fill="${C.mint}" stroke="#fff" stroke-width="2"/>`; });
          s += shapeSVG(sh, toS, { poly: `fill="none" stroke="${C.muted}" stroke-width="2" stroke-dasharray="5 4"`, stroke: `stroke="#c9cdea" stroke-width="16"` });
          const tf = q => toS(rotP([q], rot)[0]);
          const fitNow = isFit(rot) && Math.abs(total) > 2;
          s += shapeSVG(sh, tf, { poly: `fill="${fitNow ? C.mint : C.violet}" fill-opacity=".55" stroke="${fitNow ? '#0f9d7a' : C.violet}" stroke-width="3" stroke-linejoin="round"`, stroke: `stroke="${fitNow ? '#0f9d7a' : C.violet}" stroke-width="12" stroke-opacity=".85"` });
          // marker so the turn is visible even for very symmetric shapes
          const mk = tf([.55, 0]); s += `<circle cx="${mk[0].toFixed(1)}" cy="${mk[1].toFixed(1)}" r="6" fill="${C.sun}" stroke="${C.ink}" stroke-width="1.5"/>`;
          s += `<circle cx="${cx}" cy="${cy}" r="4" fill="${C.ink}"/>`;
          const hq = [cx + 100 * Math.cos(rad(rot + 30)), cy - 100 * Math.sin(rad(rot + 30))];
          s += `<circle cx="${hq[0].toFixed(1)}" cy="${hq[1].toFixed(1)}" r="13" fill="${C.violet}" stroke="#fff" stroke-width="3"/><text x="${hq[0].toFixed(1)}" y="${(hq[1] + 5).toFixed(1)}" font-size="14" fill="#fff" font-weight="800" text-anchor="middle">⟲</text>`;
          if (fitNow && Math.abs(total) > 2) s += `<text x="${cx}" y="22" font-size="16" font-weight="800" fill="#0f9d7a" text-anchor="middle" class="lb-symmetry-flash">It fits! ✨</text>`;
          svg.innerHTML = s;
          rd.innerHTML = `${esc(sh.name)} · turned <b>${Math.round(Math.abs(total))}°</b> · fits found: <b style="color:#0f9d7a">${fitsFound.size}</b>${Math.abs(total) >= 359 ? ' · full turn done!' : ''}<br><span style="color:${C.muted}">Drag to turn. Count the fits in one full turn (360°).</span>`;
        } else {
          const cands = candidates();
          cands.forEach(a => {
            const d = [Math.cos(rad(a)), -Math.sin(rad(a))], ok = foundLines.has(a), isFl = flash && flash.a === a;
            const col = ok ? '#0f9d7a' : isFl ? C.coral : '#b9bedb';
            s += `<line x1="${(cx - d[0] * 104).toFixed(1)}" y1="${(cy - d[1] * 104).toFixed(1)}" x2="${(cx + d[0] * 104).toFixed(1)}" y2="${(cy + d[1] * 104).toFixed(1)}" stroke="${col}" stroke-width="${ok || isFl ? 3.5 : 2.5}" stroke-dasharray="${ok ? '0' : '8 6'}" stroke-linecap="round"/>`;
          });
          s += shapeSVG(sh, toS, { poly: `fill="${C.blue}" fill-opacity=".35" stroke="${C.blue}" stroke-width="3" stroke-linejoin="round"`, stroke: `stroke="${C.blue}" stroke-width="13" stroke-opacity=".8"` });
          if (flash) { // folded copy
            const tf = q => toS(reflectPt(q, flash.a));
            s += shapeSVG(sh, tf, { poly: `fill="${flash.ok ? C.mint : C.coral}" fill-opacity=".45" stroke="${flash.ok ? '#0f9d7a' : C.coral}" stroke-width="2.5" stroke-dasharray="5 3"`, stroke: `stroke="${flash.ok ? C.mint : C.coral}" stroke-width="7" stroke-opacity=".8"` });
          }
          svg.innerHTML = s;
          rd.innerHTML = flash ? (flash.ok ? `<span style="color:#0f9d7a">Yes! Folding on this line, the two halves match exactly.</span>` : `<span style="color:${C.coral}">No: the folded copy (red) does not sit on the shape.</span>`) + `<br>Lines found: <b>${foundLines.size}</b>`
            : `${esc(sh.name)} · lines found: <b style="color:#0f9d7a">${foundLines.size}</b><br><span style="color:${C.muted}">Tap a dashed line to fold the shape over it.</span>`;
        }
      }
      function isFit(r, tol = 3) { const x = norm(r); return info.fits.some(f => Math.min(Math.abs(norm(f) - x), 360 - Math.abs(norm(f) - x)) < tol); }
      function chText() { return mode === 'rotate' ? `Turn the ${lc(sh.name)} and find its order of rotational symmetry` : `Find all the lines of symmetry of the ${lc(sh.name)}`; }
      let drag = false;
      on(svg, 'pointerdown', e => {
        const q = svgXY(e); if (!q) return;
        if (mode === 'rotate') { drag = true; lastRaw = Math.atan2(cy - q[1], q[0] - cx) * 180 / Math.PI; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); e.preventDefault(); return; }
        // lines: nearest candidate line
        let best = null, bd = 16;
        candidates().forEach(a => { const d = Math.abs((q[0] - cx) * Math.sin(rad(a)) + (q[1] - cy) * Math.cos(rad(a))); const along = Math.abs((q[0] - cx) * Math.cos(rad(a)) - (q[1] - cy) * Math.sin(rad(a))); if (d < bd && along < 120) { bd = d; best = a; } });
        if (best == null) return;
        const ok = info.lines.includes(best);
        flash = { a: best, ok }; if (ok) { foundLines.add(best); api.sfx('correct'); } else api.sfx('wrong');
        draw(); timers.forEach(clearTimeout); timers = [setTimeout(() => { flash = null; if (svg.isConnected) draw(); }, 1500)];
        if (ok && foundLines.size === info.lines.length) win(`${sh.name} has ${info.lines.length} line${info.lines.length === 1 ? '' : 's'} of symmetry!`);
      });
      on(svg, 'pointermove', e => {
        if (!drag) return; const q = svgXY(e); if (!q) return;
        const raw = Math.atan2(cy - q[1], q[0] - cx) * 180 / Math.PI; let d = raw - lastRaw; if (d > 180) d -= 360; if (d < -180) d += 360; lastRaw = raw;
        total += d; rot = total;
        if (Math.abs(total) > 2) { const x = norm(rot); const f = info.fits.find(f => Math.min(Math.abs(norm(f) - x), 360 - Math.abs(norm(f) - x)) < 3);
          if (f != null && (f !== 360 || Math.abs(total) >= 357) && !fitsFound.has(f)) { fitsFound.add(f); api.sfx('coin'); } }
        draw();
      });
      const up = () => {
        if (!drag) return; drag = false;
        // magnet: on release, settle exactly onto a fitting position if close
        const x = norm(total); info.fits.forEach(f => { const df = ((norm(f) - x + 540) % 360) - 180; if (Math.abs(df) < 3) total += df; });
        rot = total; draw();
      };
      on(svg, 'pointerup', up); on(svg, 'pointercancel', up);
      if (mode === 'rotate') {
        ctl.querySelectorAll('[data-o]').forEach(b => on(b, 'click', () => {
          const v = +b.dataset.o;
          if (v === info.order) { api.sfx('correct'); win(`Order ${info.order}: the ${lc(sh.name)} fits its outline ${info.order} time${info.order > 1 ? 's' : ''} in one full turn${info.order > 1 ? ` (every ${360 / info.order}°)` : ' (only after a full 360° turn)'}.`); }
          else { api.sfx('hmm'); rd.innerHTML = `<span style="color:${C.coral}">Not ${v}. Turn it all the way round (360°) and count every fit, including the last one.</span>`; }
        }));
        on(host.querySelector('[data-reset]'), 'click', () => { rot = total = 0; fitsFound = new Set(); draw(); });
      } else on(ctl.querySelector('[data-done]'), 'click', () => {
        if (foundLines.size === info.lines.length) win(info.lines.length ? `Yes! The ${lc(sh.name)} has exactly ${info.lines.length} line${info.lines.length === 1 ? '' : 's'} of symmetry.` : `Right! The ${lc(sh.name)} has no line of symmetry.`);
        else { api.sfx('hmm'); rd.innerHTML = `<span style="color:${C.coral}">There ${info.lines.length - foundLines.size === 1 ? 'is' : 'are'} still more lines to find. Try the other dashed lines!</span>`; }
      });
      on(host.querySelector('[data-new]'), 'click', () => {
        const others = pool.filter(x => x !== shapeName); const nm = others[Math.floor(Math.random() * others.length)] || shapeName;
        challengeText = null; won = false; api.resetWin && api.resetWin(); api.sfx('tap');
        if (mode === 'rotate' && SHAPES[nm]) { const o = symInfo(SHAPES[nm]).order; if (o > 8) { /* never happens with library shapes */ } }
        setShape(nm); flash = null; showCh(chText()); draw();
      });
      showCh(chText()); draw();
    }
    return () => { cleanup.forEach(f => { try { f(); } catch (e) { } }); timers.forEach(clearTimeout); };
  }

  Labs.register('symmetry', {
    title: 'Symmetry studio',
    subjects: ['maths'],
    render,
    example: { mode: 'mirror', line: 'vertical', n: 10, auto: false },
    examples: [
      { mode: 'mirror', line: 'both', n: 10, auto: true, minCells: 12, challenge: 'Make a rangoli design with 2 mirror lines' },
      { mode: 'lines', shape: 'H', shapes: ['H', 'A', 'E', 'X', 'Z', 'M', 'T'] },
      { mode: 'rotate', shape: 'pinwheel' }
    ]
  });
})();
