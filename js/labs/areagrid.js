/* StudyVerse Concept Lab: areagrid — "Area & perimeter grid"
 * The child drags corner handles to resize shapes on a square grid (or paints squares).
 * Area (by counting squares and by formula) and perimeter update live.
 *
 * PARAMS (all optional; defaults in brackets)
 *  mode          string  'rect' | 'lshape' | 'paint' | 'triangle' | 'parallelogram'           ['rect']
 *                        rect          = rectangle/square, drag the corner
 *                        lshape        = rectangle with a corner cut out, drag both corners
 *                        paint         = tap/drag squares to colour any shape
 *                        triangle      = drag the base end and the top corner (area = ½ × b × h)
 *                        parallelogram = drag the base end and the top corner (area = b × h)
 *  grid          array   [columns, rows]                                                       [[12,8]]
 *  size          array   starting shape: rect [w,h]; lshape [W,H,cutW,cutH];
 *                        triangle [base,height,apexX]; parallelogram [base,height,shift]       [mode-specific]
 *  cells         array   paint mode: starting painted squares as [col,row] (0-based, row 0 = top) [[]]
 *  unit          string  'cm' | 'm' (any length unit)                                          ['cm']
 *  count         bool    number the squares inside the shape to show counting                 [true]
 *  targetArea    number  challenge area (square units)                                        [mode-specific]
 *  targetPerimeter number challenge perimeter (rect/lshape/paint only)                        [mode-specific]
 *  challenge     string  challenge text (English or Hindi); default is generated
 *  winText       string  message on success
 */
(function () {
  const C = { violet: '#8b5cf6', mint: '#2ed3a5', sun: '#ffc93c', coral: '#ff6b6b', blue: '#3b82f6', ink: '#1b1f3a', muted: '#6b7090' };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const f2 = n => (Math.round(n * 100) / 100).toString();
  const rnd = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
  const CSS = `
.lb-areagrid-w{font-size:14px;color:${C.ink}}
.lb-areagrid-ch{background:#fff6d8;border-radius:12px;padding:6px 6px 6px 11px;font-weight:800;font-size:14px;margin-bottom:8px;line-height:1.3;display:flex;align-items:center;gap:6px}
.lb-areagrid-ch span{flex:1}
.lb-areagrid-ch .lb-areagrid-b{flex-shrink:0;font-size:13px;padding:0 10px}
.lb-areagrid-tip{grid-column:1/-1;color:${C.muted};font-weight:700;font-size:12px;line-height:1.35;padding:0 4px}
.lb-areagrid-svg{width:100%;height:auto;display:block;touch-action:none;background:#fbfbff;border-radius:18px;user-select:none;-webkit-user-select:none}
.lb-areagrid-svg text{font-family:inherit;pointer-events:none}
.lb-areagrid-read{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px}
.lb-areagrid-c{background:#f4f6ff;border-radius:12px;padding:6px 9px;font-weight:800;font-size:13px;line-height:1.35}
.lb-areagrid-c.wide{grid-column:1/-1}
.lb-areagrid-c small{display:block;color:${C.muted};font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.3px}
.lb-areagrid-c b{font-size:16px}
.lb-areagrid-row{display:flex;gap:6px;margin-top:8px;align-items:center}
.lb-areagrid-b{min-height:40px;border:none;border-radius:12px;background:#f1efff;color:${C.ink};font:inherit;font-weight:800;font-size:14px;padding:0 13px;cursor:pointer}
.lb-areagrid-b.go{background:${C.violet};color:#fff}
.lb-areagrid-b:active{transform:scale(.95)}
.lb-areagrid-tag{border-radius:999px;padding:4px 10px;font-weight:800;font-size:12px;color:#fff;background:${C.blue}}
`;

  function render(host, p, api) {
    const mode = ['rect', 'lshape', 'paint', 'triangle', 'parallelogram'].includes(p.mode) ? p.mode : 'rect';
    const cols = Array.isArray(p.grid) ? Math.max(4, Math.min(16, +p.grid[0] || 12)) : 12;
    const rows = Array.isArray(p.grid) ? Math.max(4, Math.min(12, +p.grid[1] || 8)) : 8;
    const unit = p.unit != null ? esc(p.unit) : 'cm', sq = `sq ${unit}`;
    const u = Math.min(28, 330 / cols, 236 / rows), pad = 12;
    const W = cols * u + pad * 2, H = rows * u + pad * 2;
    const X = c => pad + c * u, Y = r => pad + r * u;
    const sz = Array.isArray(p.size) ? p.size.map(Number) : [];
    const ox = 1, oy = 1, baseY = rows - 1; // anchors
    const cl = (v, a, b) => Math.max(a, Math.min(b, v));
    let w, h, cw, chh, b, ht, sh, cells = new Set();
    function initShape() {
      if (mode === 'rect') { w = cl(sz[0] || 4, 1, cols - 2); h = cl(sz[1] || 3, 1, rows - 2); }
      if (mode === 'lshape') { w = cl(sz[0] || 6, 2, cols - 2); h = cl(sz[1] || 5, 2, rows - 2); cw = cl(sz[2] || 3, 1, w - 1); chh = cl(sz[3] || 2, 1, h - 1); }
      if (mode === 'triangle') { b = cl(sz[0] || 6, 1, cols - 2); ht = cl(sz[1] || 4, 1, rows - 2); sh = cl(sz[2] != null ? sz[2] : 2, -1, cols - 2); }
      if (mode === 'parallelogram') { b = cl(sz[0] || 5, 1, cols - 4); ht = cl(sz[1] || 4, 1, rows - 2); sh = cl(sz[2] != null ? sz[2] : 2, -1, cols - 2 - b); }
      if (mode === 'paint') { cells = new Set((Array.isArray(p.cells) ? p.cells : []).filter(q => Array.isArray(q) && q[0] >= 0 && q[0] < cols && q[1] >= 0 && q[1] < rows).map(q => q[0] + ',' + q[1])); }
    }
    initShape();
    const defT = { rect: [12, 14], lshape: [20, 22], paint: [8, 12], triangle: [12, null], parallelogram: [12, null] }[mode];
    let tA = p.targetArea != null ? +p.targetArea : (p.targetPerimeter != null ? null : defT[0]);
    let tP = p.targetPerimeter != null ? +p.targetPerimeter : (p.targetArea != null ? null : defT[1]);
    if (mode === 'triangle' || mode === 'parallelogram') tP = null;
    let challengeText = p.challenge ? String(p.challenge) : null, won = false;

    host.innerHTML = `<style>${CSS}</style><div class="lb-areagrid-w"><div class="lb-areagrid-ch"><span></span><button class="lb-areagrid-b" data-reset aria-label="${mode === 'paint' ? 'Clear' : 'Reset'}">↺</button><button class="lb-areagrid-b go" data-new aria-label="New challenge">🔄 New</button></div>
      <svg class="lb-areagrid-svg" viewBox="0 0 ${W.toFixed(1)} ${H.toFixed(1)}"><g class="lb-areagrid-bg"></g><g class="lb-areagrid-fg"></g></svg>
      <div class="lb-areagrid-read"></div>
</div>`;
    const svg = host.querySelector('svg'), fg = host.querySelector('.lb-areagrid-fg'), rd = host.querySelector('.lb-areagrid-read'), chEl = host.querySelector('.lb-areagrid-ch span');
    let g = '';
    for (let i = 0; i <= cols; i++) g += `<line x1="${X(i)}" y1="${Y(0)}" x2="${X(i)}" y2="${Y(rows)}" stroke="#dfe3f5" stroke-width="1"/>`;
    for (let j = 0; j <= rows; j++) g += `<line x1="${X(0)}" y1="${Y(j)}" x2="${X(cols)}" y2="${Y(j)}" stroke="#dfe3f5" stroke-width="1"/>`;
    host.querySelector('.lb-areagrid-bg').innerHTML = g + `<text x="${W - pad - 2}" y="${H - 2}" font-size="9" font-weight="700" fill="${C.muted}" text-anchor="end">each square = 1 ${sq}</text>`;

    // ----- measures -----
    function measure() {
      if (mode === 'rect') return { area: w * h, per: 2 * (w + h) };
      if (mode === 'lshape') return { area: w * h - cw * chh, per: 2 * (w + h) };
      if (mode === 'triangle') { const s1 = Math.hypot(sh, ht), s2 = Math.hypot(b - sh, ht); return { area: b * ht / 2, per: b + s1 + s2, s1, s2 }; }
      if (mode === 'parallelogram') { const s1 = Math.hypot(sh, ht); return { area: b * ht, per: 2 * (b + s1), s1 }; }
      let per = 0; cells.forEach(k => { const [c, r] = k.split(',').map(Number); [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dx, dy]) => { if (!cells.has((c + dx) + ',' + (r + dy))) per++; }); });
      return { area: cells.size, per };
    }
    const isInt = v => Math.abs(v - Math.round(v)) < 1e-9;
    const fmtL = v => isInt(v) ? String(Math.round(v)) : '≈ ' + f2(v);

    // ----- draw -----
    function handle(x, y) { return `<circle cx="${x}" cy="${y}" r="20" fill="transparent"/><circle cx="${x}" cy="${y}" r="10" fill="${C.violet}" stroke="#fff" stroke-width="3" style="filter:drop-shadow(0 2px 2px rgba(80,60,180,.35))"/>`; }
    const T = (x, y, t, col = C.ink, size = 12, anchor = 'middle') => `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="${size}" font-weight="800" fill="${col}" text-anchor="${anchor}" stroke="#fbfbff" stroke-width="3" paint-order="stroke">${t}</text>`;
    function numCells(list) { if (p.count === false || list.length > 80) return ''; return list.map(([c, r], i) => `<text x="${X(c) + u / 2}" y="${Y(r) + u / 2 + 4}" font-size="${Math.min(11, u * .4)}" font-weight="700" fill="#7c6fd6" text-anchor="middle" opacity=".75">${i + 1}</text>`).join(''); }
    function draw() {
      let s = '';
      if (mode === 'rect' || mode === 'lshape') {
        const list = [];
        for (let r = 0; r < h; r++) for (let c = 0; c < w; c++) if (!(mode === 'lshape' && c >= w - cw && r < chh)) list.push([ox + c, oy + r]);
        if (mode === 'lshape') {
          s += `<rect x="${X(ox + w - cw)}" y="${Y(oy)}" width="${cw * u}" height="${chh * u}" fill="none" stroke="${C.coral}" stroke-width="1.5" stroke-dasharray="5 4"/>`;
          s += T(X(ox + w - cw / 2), Y(oy + chh / 2) + 4, `cut ${cw}×${chh}`, C.coral, 10);
          s += `<path d="M${X(ox)} ${Y(oy)} H${X(ox + w - cw)} V${Y(oy + chh)} H${X(ox + w)} V${Y(oy + h)} H${X(ox)}Z" fill="${C.mint}" fill-opacity=".35" stroke="${C.ink}" stroke-width="3" stroke-linejoin="round"/>`;
        } else s += `<rect x="${X(ox)}" y="${Y(oy)}" width="${w * u}" height="${h * u}" fill="${w === h ? C.sun : C.mint}" fill-opacity=".38" stroke="${C.ink}" stroke-width="3"/>`;
        s += numCells(list);
        // side labels
        if (mode === 'rect') s += T(X(ox) + w * u / 2, Y(oy) - 3, `${w} ${unit}`, C.blue) + T(X(ox) - 3, Y(oy) + h * u / 2 + 4, `${h}`, C.coral, 12, 'end');
        else s += T(X(ox) + (w - cw) * u / 2, Y(oy) - 3, `${w - cw}`, C.blue) + T(X(ox) + w * u / 2, Y(oy + h) + 13, `${w} ${unit}`, C.blue) + T(X(ox) - 3, Y(oy) + h * u / 2 + 4, `${h}`, C.coral, 12, 'end') + T(X(ox + w) + 4, Y(oy + chh) + (h - chh) * u / 2 + 4, `${h - chh}`, C.coral, 12, 'start');
        s += handle(X(ox + w), Y(oy + h));
        if (mode === 'lshape') s += handle(X(ox + w - cw), Y(oy + chh));
      } else if (mode === 'paint') {
        const list = [...cells].map(k => k.split(',').map(Number)).sort((a, b2) => a[1] - b2[1] || a[0] - b2[0]);
        list.forEach(([c, r]) => { s += `<rect x="${X(c) + 1}" y="${Y(r) + 1}" width="${u - 2}" height="${u - 2}" rx="4" fill="${C.mint}" fill-opacity=".75"/>`; });
        // outline (perimeter edges)
        let d = '';
        list.forEach(([c, r]) => {
          if (!cells.has(c + ',' + (r - 1))) d += `M${X(c)} ${Y(r)}H${X(c + 1)}`;
          if (!cells.has(c + ',' + (r + 1))) d += `M${X(c)} ${Y(r + 1)}H${X(c + 1)}`;
          if (!cells.has((c - 1) + ',' + r)) d += `M${X(c)} ${Y(r)}V${Y(r + 1)}`;
          if (!cells.has((c + 1) + ',' + r)) d += `M${X(c + 1)} ${Y(r)}V${Y(r + 1)}`;
        });
        s += `<path d="${d}" stroke="${C.coral}" stroke-width="3.5" stroke-linecap="round" fill="none"/>`;
        s += numCells(list);
      } else {
        // triangle / parallelogram: base on row line baseY, from ox to ox+b; top at y = baseY - ht
        const by = Y(baseY), ty = Y(baseY - ht);
        let pts;
        if (mode === 'triangle') pts = [[X(ox), by], [X(ox + b), by], [X(ox + sh), ty]];
        else pts = [[X(ox), by], [X(ox + b), by], [X(ox + b + sh), ty], [X(ox + sh), ty]];
        // bounding rectangle b × h (dashed) to compare
        if (mode === 'triangle') s += `<rect x="${X(ox + Math.min(0, sh))}" y="${ty}" width="${(Math.max(b, sh) - Math.min(0, sh)) * u}" height="${ht * u}" fill="none" stroke="${C.blue}" stroke-width="1.5" stroke-dasharray="5 4"/>`;
        s += `<path d="M${pts.map(q => q.join(' ')).join(' L')}Z" fill="${mode === 'triangle' ? C.sun : C.mint}" fill-opacity=".45" stroke="${C.ink}" stroke-width="3" stroke-linejoin="round"/>`;
        // height line
        const hx = X(ox + sh);
        s += `<line x1="${hx}" y1="${ty}" x2="${hx}" y2="${by}" stroke="${C.coral}" stroke-width="2" stroke-dasharray="4 3"/>`;
        s += `<path d="M${hx} ${by - 9} h${sh >= 0 && sh < b ? 9 : -9} v9" fill="none" stroke="${C.coral}" stroke-width="1.5"/>`;
        s += T(hx + (sh > b / 2 ? -6 : 6), (ty + by) / 2 + 4, `h = ${ht}`, C.coral, 12, sh > b / 2 ? 'end' : 'start');
        s += T(X(ox) + b * u / 2, by + 15, `b = ${b} ${unit}`, C.blue);
        s += handle(X(ox + b), by) + handle(X(ox + sh), ty);
      }
      fg.innerHTML = s;
      readout();
    }
    const cell = (l, v, wide) => `<div class="lb-areagrid-c ${wide ? 'wide' : ''}"><small>${l}</small>${v}</div>`;
    function readout() {
      const m = measure(); let hh = '';
      if (mode === 'rect') {
        hh = cell('Area', `<b style="color:#0f9d7a">${m.area} ${sq}</b><br>${w} × ${h} = ${m.area} squares`) + cell('Perimeter', `<b style="color:${C.coral}">${m.per} ${unit}</b><br>2 × (${w} + ${h}) = ${m.per}`);
        if (w === h) hh += cell('Shape', `A square! Area = side × side = ${w} × ${w}`, 1);
      } else if (mode === 'lshape') {
        hh = cell('Area', `<b style="color:#0f9d7a">${m.area} ${sq}</b><br>${w}×${h} − ${cw}×${chh} = ${w * h} − ${cw * chh}`) + cell('Perimeter', `<b style="color:${C.coral}">${m.per} ${unit}</b><br>${w - cw}+${chh}+${cw}+${h - chh}+${w}+${h}`);
      } else if (mode === 'paint') {
        hh = cell('Area', `<b style="color:#0f9d7a">${m.area} ${sq}</b><br>${m.area} squares coloured`) + cell('Perimeter', `<b style="color:${C.coral}">${m.per} ${unit}</b><br>count the red edges`);
      } else if (mode === 'triangle') {
        hh = cell('Area', `<b style="color:#b07d00">${f2(m.area)} ${sq}</b><br>½ × ${b} × ${ht} = ${f2(m.area)}`) + cell('Perimeter', `<b style="color:${C.coral}">${fmtL(m.per)} ${unit}</b><br>${b} + ${f2(m.s1)} + ${f2(m.s2)}`);
        hh += `<div class="lb-areagrid-tip">${sh >= 0 && sh <= b ? `The triangle is half of the dashed ${b} × ${ht} rectangle.` : 'Same base, same height: same area!'} Slide the top sideways: the area does not change.</div>`;
      } else {
        hh = cell('Area', `<b style="color:#0f9d7a">${m.area} ${sq}</b><br>b × h = ${b} × ${ht}`) + cell('Perimeter', `<b style="color:${C.coral}">${fmtL(m.per)} ${unit}</b><br>2 × (${b} + ${f2(m.s1)})`);
        hh += `<div class="lb-areagrid-tip">Cut the triangle off one end and move it to the other end: you get a ${b} × ${ht} rectangle.</div>`;
      }
      rd.innerHTML = hh;
    }

    // ----- challenge -----
    function chText() {
      if (challengeText) return challengeText;
      const what = { rect: 'a rectangle', lshape: 'an L-shape', paint: 'a shape', triangle: 'a triangle', parallelogram: 'a parallelogram' }[mode];
      if (tA != null && tP != null) return `Make ${what} with area ${tA} ${sq} and perimeter ${tP} ${unit}`;
      if (tA != null) return `Make ${what} with area ${tA} ${sq}`;
      return `Make ${what} with perimeter ${tP} ${unit}`;
    }
    function showCh() { chEl.textContent = '🎯 Challenge: ' + chText(); }
    function check() {
      if (won) return; const m = measure();
      const okA = tA == null || Math.abs(m.area - tA) < 1e-9, okP = tP == null || Math.abs(m.per - tP) < 1e-9;
      if (okA && okP && (tA != null || tP != null) && m.area > 0) {
        won = true; api.sfx('correct');
        api.win(p.winText || `Area = ${f2(m.area)} ${sq}${mode === 'triangle' || mode === 'parallelogram' ? '' : `, perimeter = ${m.per} ${unit}`}. You did it!`);
      }
    }

    // ----- interaction -----
    let drag = null, paintOn = true, lastCell = null;
    function svgXY(e) { const m = svg.getScreenCTM(); if (!m) return null; const q = svg.createSVGPoint(); q.x = e.clientX; q.y = e.clientY; const t = q.matrixTransform(m.inverse()); return [t.x, t.y]; }
    function handles() {
      if (mode === 'rect') return [['c', X(ox + w), Y(oy + h)]];
      if (mode === 'lshape') return [['c', X(ox + w), Y(oy + h)], ['n', X(ox + w - cw), Y(oy + chh)]];
      if (mode === 'triangle' || mode === 'parallelogram') return [['b', X(ox + b), Y(baseY)], ['t', X(ox + sh), Y(baseY - ht)]];
      return [];
    }
    function paintAt(q) {
      const c = Math.floor((q[0] - pad) / u), r = Math.floor((q[1] - pad) / u);
      if (c < 0 || r < 0 || c >= cols || r >= rows) return;
      const k = c + ',' + r; if (k === lastCell) return; lastCell = k;
      if (paintOn) cells.add(k); else cells.delete(k);
      draw();
    }
    function down(e) {
      const q = svgXY(e); if (!q) return;
      if (mode === 'paint') {
        const c = Math.floor((q[0] - pad) / u), r = Math.floor((q[1] - pad) / u);
        if (c < 0 || r < 0 || c >= cols || r >= rows) return;
        paintOn = !cells.has(c + ',' + r); lastCell = null; drag = 'paint';
        svg.setPointerCapture && svg.setPointerCapture(e.pointerId); paintAt(q); api.sfx('tap'); e.preventDefault(); return;
      }
      let best = null, bd = 34;
      handles().forEach(([k, hx, hy]) => { const d = Math.hypot(hx - q[0], hy - q[1]); if (d < bd) { bd = d; best = k; } });
      if (!best) return;
      drag = best; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); api.sfx('tap'); e.preventDefault();
    }
    function move(e) {
      if (!drag) return; const q = svgXY(e); if (!q) return;
      if (drag === 'paint') return paintAt(q);
      const gc = Math.round((q[0] - pad) / u), gr = Math.round((q[1] - pad) / u);
      const before = [w, h, cw, chh, b, ht, sh].join();
      if (mode === 'rect') { w = cl(gc - ox, 1, cols - ox); h = cl(gr - oy, 1, rows - oy); }
      else if (mode === 'lshape') {
        if (drag === 'c') { w = cl(gc - ox, 2, cols - ox); h = cl(gr - oy, 2, rows - oy); cw = Math.min(cw, w - 1); chh = Math.min(chh, h - 1); }
        else { cw = cl(ox + w - gc, 1, w - 1); chh = cl(gr - oy, 1, h - 1); }
      } else {
        if (drag === 'b') b = cl(gc - ox, 1, cols - ox - (mode === 'parallelogram' ? Math.max(0, sh) : 0));
        else { sh = cl(gc - ox, -ox, cols - ox - (mode === 'parallelogram' ? b : 0)); ht = cl(baseY - gr, 1, baseY); }
      }
      if ([w, h, cw, chh, b, ht, sh].join() !== before) draw();
    }
    function up() { if (!drag) return; drag = null; lastCell = null; check(); }
    svg.addEventListener('pointerdown', down); svg.addEventListener('pointermove', move); svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
    host.querySelector('[data-reset]').addEventListener('click', () => { if (mode === 'paint') cells = new Set(); else initShape(); api.sfx('tap'); draw(); });
    host.querySelector('[data-new]').addEventListener('click', () => {
      challengeText = null; won = false; api.resetWin && api.resetWin(); api.sfx('tap');
      const oA = tA, oP = tP;
      for (let k = 0; k < 20 && tA === oA && tP === oP; k++) {
        if (mode === 'rect' || mode === 'paint') { const a = rnd(1, Math.min(7, cols - 2)), c2 = rnd(1, Math.min(6, rows - 2)); tA = a * c2; tP = 2 * (a + c2); }
        else if (mode === 'lshape') { const A2 = rnd(3, Math.min(8, cols - 2)), B2 = rnd(3, Math.min(6, rows - 2)), c1 = rnd(1, A2 - 1), c2 = rnd(1, B2 - 1); tA = A2 * B2 - c1 * c2; tP = 2 * (A2 + B2); }
        else if (mode === 'triangle') { const bb = rnd(2, Math.min(9, cols - 2)), hh = rnd(2, rows - 2); tA = bb * hh / 2; tP = null; }
        else { const bb = rnd(2, Math.min(7, cols - 4)), hh = rnd(2, rows - 2); tA = bb * hh; tP = null; }
      }
      showCh();
    });
    showCh(); draw();
    return () => { svg.removeEventListener('pointerdown', down); svg.removeEventListener('pointermove', move); svg.removeEventListener('pointerup', up); svg.removeEventListener('pointercancel', up); };
  }

  Labs.register('areagrid', {
    title: 'Area & perimeter grid',
    subjects: ['maths'],
    render,
    example: { mode: 'rect', size: [4, 3], unit: 'cm', targetArea: 12, targetPerimeter: 16 },
    examples: [
      { mode: 'paint', cells: [[2, 2], [3, 2], [2, 3]], targetArea: 6, targetPerimeter: 12, challenge: 'Colour a shape with area 6 sq cm and perimeter 12 cm' },
      { mode: 'lshape', size: [6, 5, 3, 2], unit: 'm', targetArea: 20, targetPerimeter: 22 },
      { mode: 'triangle', size: [6, 4, 2], targetArea: 15, targetPerimeter: null }
    ]
  });
})();
