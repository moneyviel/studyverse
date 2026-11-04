/* StudyVerse Concept Lab: triangle — "Triangle explorer"
 * The child drags the 3 corners (A, B, C) on a square grid. Side lengths, angles, angle sum,
 * type of triangle, area/perimeter, Pythagoras squares, exterior angle and the triangle
 * inequality all update live.
 *
 * PARAMS (all optional; defaults in brackets)
 *  points      array   starting corners in grid units [[x,y],[x,y],[x,y]] (y goes up)    [[2,1],[10,2],[5,7]]
 *  grid        array   [columns, rows] of the grid                                         [[12,8]]
 *  snap        bool    corners snap to grid points (lengths shown exactly, e.g. √13)        [true]
 *  unit        string  length unit label                                                   ['cm']
 *  show        array   which readouts/drawings to show, any of:
 *                      'sides','angles','sum','class','area','perimeter','pythag','exterior','inequality'
 *                                                                                           [['sides','angles','sum','class']]
 *  goal        string  challenge goal: 'right'|'acute'|'obtuse'|'isosceles'|'scalene'|'equilateral'
 *                      |'right isosceles'|'area'|'flat' (flat = corners in a line, not a triangle) ['right']
 *  targetArea  number  for goal 'area': area to make (in square units)                    [12]
 *  goals       array   list of goals the "New challenge" button cycles through
 *                      (strings as above, or numbers = target area)        [['right','obtuse','isosceles','acute','scalene','right isosceles']]
 *  labels      array   names of the corners                                                [['A','B','C']]
 *  challenge   string  challenge text (English or Hindi); default is generated
 *  winText     string  message on success; default is generated
 */
(function () {
  const C = { violet: '#8b5cf6', mint: '#2ed3a5', sun: '#ffc93c', coral: '#ff6b6b', blue: '#3b82f6', ink: '#1b1f3a', muted: '#6b7090' };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const f2 = n => (Math.round(n * 100) / 100).toString();
  const deg = r => r * 180 / Math.PI;
  const GOALTXT = {
    right: 'Make a right-angled triangle', acute: 'Make an acute-angled triangle (all angles less than 90°)',
    obtuse: 'Make an obtuse-angled triangle', isosceles: 'Make an isosceles triangle (two equal sides)',
    scalene: 'Make a scalene triangle (no equal sides)', equilateral: 'Make an equilateral triangle (all sides equal)',
    'right isosceles': 'Make a right-angled isosceles triangle', flat: 'Drag the corners into one straight line. Is it still a triangle?'
  };
  const CSS = `
.lb-triangle-w{font-size:14px;color:${C.ink}}
.lb-triangle-ch{background:#fff6d8;border-radius:12px;padding:6px 6px 6px 11px;font-weight:800;font-size:14px;margin-bottom:8px;line-height:1.3;display:flex;align-items:center;gap:6px}
.lb-triangle-ch span{flex:1}
.lb-triangle-ch .lb-triangle-b{flex-shrink:0;font-size:13px;padding:0 10px}
.lb-triangle-stage{position:relative}
.lb-triangle-svg{width:100%;height:auto;display:block;touch-action:none;background:#fbfbff;border-radius:18px;user-select:none;-webkit-user-select:none}
.lb-triangle-svg text{font-family:inherit;pointer-events:none}
.lb-triangle-h{cursor:grab}
.lb-triangle-tags{display:flex;gap:4px;flex-wrap:wrap;margin-top:6px}
.lb-triangle-tag{border-radius:999px;padding:3px 9px;font-weight:800;font-size:11.5px;color:#fff;opacity:.93}
.lb-triangle-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:6px}
.lb-triangle-c{background:#f4f6ff;border-radius:12px;padding:6px 9px;font-weight:800;font-size:13px;line-height:1.35}
.lb-triangle-c.wide{grid-column:1/-1}
.lb-triangle-c small{display:block;color:${C.muted};font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.3px}
.lb-triangle-row{display:flex;gap:6px;margin-top:8px}
.lb-triangle-b{min-height:40px;border:none;border-radius:12px;background:#f1efff;color:${C.ink};font:inherit;font-weight:800;font-size:14px;padding:0 14px;cursor:pointer}
.lb-triangle-b.go{background:${C.violet};color:#fff}
.lb-triangle-b:active{transform:scale(.95)}
`;

  function render(host, p, api) {
    const grid = Array.isArray(p.grid) && p.grid.length === 2 ? [Math.max(4, Math.min(16, +p.grid[0] || 12)), Math.max(4, Math.min(14, +p.grid[1] || 8))] : [12, 8];
    const [cols, rows] = grid;
    const snap = p.snap !== false;
    const unit = p.unit != null ? String(p.unit) : 'cm';
    const show = new Set(Array.isArray(p.show) ? p.show : ['sides', 'angles', 'sum', 'class']);
    const L = Array.isArray(p.labels) && p.labels.length >= 3 ? p.labels.map(String) : ['A', 'B', 'C'];
    const startPts = (Array.isArray(p.points) && p.points.length === 3 && p.points.every(q => Array.isArray(q) && q.length === 2 && isFinite(q[0]) && isFinite(q[1])))
      ? p.points.map(q => [Math.max(0, Math.min(cols, +q[0])), Math.max(0, Math.min(rows, +q[1]))]) : [[2, 1], [10, 2], [5, 7]];
    let pts = startPts.map(q => q.slice());
    let goals = Array.isArray(p.goals) && p.goals.length ? p.goals.slice() : ['right', 'obtuse', 'isosceles', 'acute', 'scalene', 'right isosceles'];
    let goal = p.goal != null ? p.goal : (p.targetArea != null ? 'area' : 'right');
    if (typeof goal === 'number') { p.targetArea = goal; goal = 'area'; }
    if (goal === 'equilateral' && snap) goal = 'isosceles'; // impossible exactly on a square grid
    let targetArea = +p.targetArea || 12;
    let challengeText = p.challenge ? String(p.challenge) : null;
    let won = false, gi = -1;

    const u = Math.min(26, 316 / cols, 250 / rows), pad = 16;
    const W = cols * u + pad * 2, H = rows * u + pad * 2;
    const X = x => pad + x * u, Y = y => pad + (rows - y) * u;
    host.innerHTML = `<style>${CSS}</style><div class="lb-triangle-w">
      <div class="lb-triangle-ch"><span></span><button class="lb-triangle-b" data-reset aria-label="Reset">↺</button><button class="lb-triangle-b go" data-new aria-label="New challenge">🔄 New</button></div><div class="lb-triangle-stage">
      <svg class="lb-triangle-svg" viewBox="0 0 ${W.toFixed(1)} ${H.toFixed(1)}"><defs><clipPath id="lbtri-clip"><rect x="0" y="0" width="${W}" height="${H}" rx="18"/></clipPath></defs><g class="lb-triangle-bg"></g><g class="lb-triangle-fg" clip-path="url(#lbtri-clip)"></g></svg>
      <div class="lb-triangle-tags"></div></div><div class="lb-triangle-grid"></div></div>`;
    const svg = host.querySelector('svg'), fg = host.querySelector('.lb-triangle-fg'), tags = host.querySelector('.lb-triangle-tags'), gridEl = host.querySelector('.lb-triangle-grid'), chEl = host.querySelector('.lb-triangle-ch span');
    // unique clip id per instance
    const cid = 'lbtri' + Math.random().toString(36).slice(2, 8);
    svg.querySelector('clipPath').id = cid; fg.setAttribute('clip-path', `url(#${cid})`);
    // grid
    let g = '';
    for (let i = 0; i <= cols; i++) g += `<line x1="${X(i)}" y1="${Y(0)}" x2="${X(i)}" y2="${Y(rows)}" stroke="#e3e6f6" stroke-width="1"/>`;
    for (let j = 0; j <= rows; j++) g += `<line x1="${X(0)}" y1="${Y(j)}" x2="${X(cols)}" y2="${Y(j)}" stroke="#e3e6f6" stroke-width="1"/>`;
    if (snap) for (let i = 0; i <= cols; i++) for (let j = 0; j <= rows; j++) g += `<circle cx="${X(i)}" cy="${Y(j)}" r="1.4" fill="#c9cdea"/>`;
    host.querySelector('.lb-triangle-bg').innerHTML = g;

    // ----- maths -----
    function info() {
      const [A, B, Cc] = pts;
      const d2 = (P, Q) => (P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2;
      const s2 = { AB: d2(A, B), BC: d2(B, Cc), CA: d2(Cc, A) };
      const s = { AB: Math.sqrt(s2.AB), BC: Math.sqrt(s2.BC), CA: Math.sqrt(s2.CA) };
      const cross = (B[0] - A[0]) * (Cc[1] - A[1]) - (B[1] - A[1]) * (Cc[0] - A[0]);
      const area = Math.abs(cross) / 2;
      const flat = Math.abs(cross) < 1e-9;
      const ang = (V, P, Q) => { const ux = P[0] - V[0], uy = P[1] - V[1], vx = Q[0] - V[0], vy = Q[1] - V[1]; return deg(Math.atan2(Math.abs(ux * vy - uy * vx), ux * vx + uy * vy)); };
      const dot = (V, P, Q) => (P[0] - V[0]) * (Q[0] - V[0]) + (P[1] - V[1]) * (Q[1] - V[1]);
      const angs = [ang(A, B, Cc), ang(B, Cc, A), ang(Cc, A, B)];
      const dots = [dot(A, B, Cc), dot(B, Cc, A), dot(Cc, A, B)];
      const eq = (a, b) => snap ? Math.abs(a - b) < 1e-9 : Math.abs(Math.sqrt(a) - Math.sqrt(b)) <= 0.02 * Math.max(Math.sqrt(a), Math.sqrt(b));
      const nEq = (eq(s2.AB, s2.BC) ? 1 : 0) + (eq(s2.BC, s2.CA) ? 1 : 0) + (eq(s2.CA, s2.AB) ? 1 : 0);
      const bySide = flat ? null : nEq === 3 ? 'equilateral' : nEq >= 1 ? 'isosceles' : 'scalene';
      const isRight = i => snap ? Math.abs(dots[i]) < 1e-9 : Math.abs(angs[i] - 90) < 0.5;
      const rightAt = [0, 1, 2].find(isRight);
      const byAng = flat ? null : rightAt != null ? 'right' : dots.some(d => d < 0) ? 'obtuse' : 'acute';
      return { s, s2, area, flat, angs, bySide, byAng, rightAt, dots };
    }
    function fmtLen(sq) {
      if (!snap) return f2(Math.sqrt(sq));
      const r = Math.round(Math.sqrt(sq));
      if (r * r === Math.round(sq)) return String(r);
      // simplify √n = k√m
      let n = Math.round(sq), k = 1;
      for (let f = 2; f * f <= n; f++) while (n % (f * f) === 0) { n /= f * f; k *= f; }
      return `${k > 1 ? k : ''}√${n} ≈ ${f2(Math.sqrt(sq))}`;
    }
    function niceAngles(a) { // round so the shown values add to exactly 180
      if (a.every(v => Math.abs(v - Math.round(v)) < 1e-6)) return a.map(v => String(Math.round(v)));
      const t = a.map(v => v * 10), fl = t.map(Math.floor); let rem = 1800 - fl.reduce((x, y) => x + y, 0);
      const order = t.map((v, i) => [v - fl[i], i]).sort((x, y) => y[0] - x[0]);
      for (let k = 0; k < rem && k < 3; k++) fl[order[k][1]]++;
      return fl.map(v => (v / 10).toFixed(1));
    }

    // ----- drawing -----
    const SIDE_COL = { AB: C.blue, BC: C.coral, CA: '#0f9d7a' };
    function draw() {
      const I = info(), Pp = pts.map(q => [X(q[0]), Y(q[1])]);
      const cen = [(Pp[0][0] + Pp[1][0] + Pp[2][0]) / 3, (Pp[0][1] + Pp[1][1] + Pp[2][1]) / 3];
      let s = '';
      const sides = [['AB', 0, 1, 2], ['BC', 1, 2, 0], ['CA', 2, 0, 1]];
      // Pythagoras squares
      if (show.has('pythag') && I.byAng === 'right') {
        const cols2 = { AB: '#dbeafe', BC: '#ffe1e1', CA: '#d6f7ec' };
        sides.forEach(([nm, i, j, k]) => {
          const P = Pp[i], Q = Pp[j], R = Pp[k];
          let nx = -(Q[1] - P[1]), ny = Q[0] - P[0];
          const mx = (P[0] + Q[0]) / 2, my = (P[1] + Q[1]) / 2;
          if ((R[0] - mx) * nx + (R[1] - my) * ny > 0) { nx = -nx; ny = -ny; }
          const q3 = [Q[0] + nx, Q[1] + ny], q4 = [P[0] + nx, P[1] + ny];
          s += `<path d="M${P[0]} ${P[1]} L${Q[0]} ${Q[1]} L${q3[0]} ${q3[1]} L${q4[0]} ${q4[1]}Z" fill="${cols2[nm]}" stroke="${SIDE_COL[nm]}" stroke-width="1.5" stroke-dasharray="4 3"/>`;
          const sc = [(P[0] + Q[0] + q3[0] + q4[0]) / 4, (P[1] + Q[1] + q3[1] + q4[1]) / 4];
          s += `<text x="${sc[0].toFixed(1)}" y="${(sc[1] + 5).toFixed(1)}" font-size="14" font-weight="800" fill="${SIDE_COL[nm]}" text-anchor="middle">${f2(I.s2[nm])}</text>`;
        });
      }
      // exterior angle at C (extend BC beyond C)
      if (show.has('exterior') && !I.flat) {
        const B = Pp[1], Cp = Pp[2], A = Pp[0];
        const dx = Cp[0] - B[0], dy = Cp[1] - B[1], dl = Math.hypot(dx, dy) || 1;
        const E = [Cp[0] + dx / dl * 70, Cp[1] + dy / dl * 70];
        s += `<line x1="${Cp[0]}" y1="${Cp[1]}" x2="${E[0].toFixed(1)}" y2="${E[1].toFixed(1)}" stroke="${C.muted}" stroke-width="2.5" stroke-dasharray="6 5"/>`;
        const a1 = deg(Math.atan2(-(dy), dx)), a2 = deg(Math.atan2(-(A[1] - Cp[1]), A[0] - Cp[0]));
        let st = a1, en = a2; if (((a2 - a1) % 360 + 360) % 360 > 180) { st = a2; en = a1; }
        s += `<path d="${wedge(Cp[0], Cp[1], 24, st, en)}" fill="${C.sun}" fill-opacity=".55" stroke="#d9a400" stroke-width="1.5"/>`;
      }
      // triangle
      s += `<path d="M${Pp[0][0]} ${Pp[0][1]} L${Pp[1][0]} ${Pp[1][1]} L${Pp[2][0]} ${Pp[2][1]}Z" fill="${I.flat ? 'none' : C.violet}" fill-opacity=".14" stroke-linejoin="round"/>`;
      sides.forEach(([nm, i, j]) => { s += `<line x1="${Pp[i][0]}" y1="${Pp[i][1]}" x2="${Pp[j][0]}" y2="${Pp[j][1]}" stroke="${SIDE_COL[nm]}" stroke-width="3.5" stroke-linecap="round"/>`; });
      // angle marks
      if (!I.flat && (show.has('angles') || show.has('class'))) {
        const shown = niceAngles(I.angs);
        [0, 1, 2].forEach(i => {
          const V = Pp[i], P1 = Pp[(i + 1) % 3], P2 = Pp[(i + 2) % 3];
          const a1 = deg(Math.atan2(-(P1[1] - V[1]), P1[0] - V[0])), a2 = deg(Math.atan2(-(P2[1] - V[1]), P2[0] - V[0]));
          let st = a1, en = a2; if (((a2 - a1) % 360 + 360) % 360 > 180) { st = a2; en = a1; }
          if (I.rightAt === i) {
            const u1 = unitv(V, P1), u2 = unitv(V, P2), r = 11;
            s += `<path d="M${V[0] + u1[0] * r} ${V[1] + u1[1] * r} L${V[0] + (u1[0] + u2[0]) * r} ${V[1] + (u1[1] + u2[1]) * r} L${V[0] + u2[0] * r} ${V[1] + u2[1] * r}" fill="none" stroke="${C.ink}" stroke-width="1.8"/>`;
          } else s += `<path d="${wedge(V[0], V[1], 16, st, en)}" fill="${C.violet}" fill-opacity=".25"/>`;
          if (show.has('angles')) {
            const mid = st + (((en - st) % 360 + 360) % 360) / 2, rr = I.angs[i] < 35 ? 44 : 31;
            s += `<text x="${(V[0] + rr * Math.cos(mid * Math.PI / 180)).toFixed(1)}" y="${(V[1] - rr * Math.sin(mid * Math.PI / 180) + 4).toFixed(1)}" font-size="11.5" font-weight="800" fill="#6d3fe0" text-anchor="middle" stroke="#fff" stroke-width="3" paint-order="stroke">${shown[i]}°</text>`;
          }
        });
      }
      // side lengths
      if (show.has('sides') || show.has('inequality') || show.has('perimeter')) sides.forEach(([nm, i, j]) => {
        const m = [(Pp[i][0] + Pp[j][0]) / 2, (Pp[i][1] + Pp[j][1]) / 2];
        let ox = m[0] - cen[0], oy = m[1] - cen[1]; const ol = Math.hypot(ox, oy) || 1;
        if (I.flat) { ox = -(Pp[j][1] - Pp[i][1]); oy = Pp[j][0] - Pp[i][0]; }
        const ol2 = Math.hypot(ox, oy) || 1, off = show.has('pythag') && I.byAng === 'right' ? -14 : 14;
        const tx = m[0] + ox / ol2 * off, ty = m[1] + oy / ol2 * off;
        const t = snap ? fmtLen(I.s2[nm]).replace(/ ≈.*/, '') : f2(I.s[nm]);
        s += `<text x="${tx.toFixed(1)}" y="${(ty + 4).toFixed(1)}" font-size="12" font-weight="800" fill="${SIDE_COL[nm]}" text-anchor="middle" stroke="#fff" stroke-width="3.5" paint-order="stroke">${t}</text>`;
      });
      // corners
      pts.forEach((q, i) => {
        const V = Pp[i]; let ox = V[0] - cen[0], oy = V[1] - cen[1]; const ol = Math.hypot(ox, oy) || 1;
        s += `<circle class="lb-triangle-h" data-i="${i}" cx="${V[0]}" cy="${V[1]}" r="21" fill="transparent"/>`;
        s += `<circle cx="${V[0]}" cy="${V[1]}" r="9" fill="${C.violet}" stroke="#fff" stroke-width="3" pointer-events="none" style="filter:drop-shadow(0 2px 2px rgba(80,60,180,.35))"/>`;
        s += `<text x="${(V[0] + ox / ol * 20).toFixed(1)}" y="${(V[1] + oy / ol * 20 + 5).toFixed(1)}" font-size="15" font-weight="800" fill="${C.ink}" text-anchor="middle" stroke="#fff" stroke-width="3" paint-order="stroke">${esc(L[i])}</text>`;
      });
      fg.innerHTML = s;
      readout(I);
    }
    function unitv(V, P) { const dx = P[0] - V[0], dy = P[1] - V[1], l = Math.hypot(dx, dy) || 1; return [dx / l, dy / l]; }
    function wedge(cx, cy, r, a0, a1) {
      const sw = ((a1 - a0) % 360 + 360) % 360, p0 = [cx + r * Math.cos(a0 * Math.PI / 180), cy - r * Math.sin(a0 * Math.PI / 180)], p1 = [cx + r * Math.cos(a1 * Math.PI / 180), cy - r * Math.sin(a1 * Math.PI / 180)];
      return `M${cx} ${cy} L${p0[0].toFixed(1)} ${p0[1].toFixed(1)} A${r} ${r} 0 ${sw > 180 ? 1 : 0} 0 ${p1[0].toFixed(1)} ${p1[1].toFixed(1)}Z`;
    }
    const nm2 = (i, j) => L[i] + L[j];
    function readout(I) {
      const tg = [];
      if (I.flat) tg.push(['Not a triangle: corners in a line', C.coral]);
      else if (show.has('class')) {
        const sc = { equilateral: C.violet, isosceles: C.blue, scalene: C.muted }, ac = { right: C.blue, acute: '#0f9d7a', obtuse: '#d08a00' };
        tg.push([I.bySide[0].toUpperCase() + I.bySide.slice(1), sc[I.bySide]]);
        tg.push([I.byAng === 'right' ? 'Right-angled' : I.byAng === 'acute' ? 'Acute-angled' : 'Obtuse-angled', ac[I.byAng]]);
      }
      tags.innerHTML = tg.map(t => `<span class="lb-triangle-tag" style="background:${t[1]}">${esc(t[0])}</span>`).join('');
      const c = [];
      const u1 = esc(unit), sq = unit ? ` sq ${u1}` : ' sq units';
      if (show.has('sides')) c.push(['wide', 'Sides', `<span style="color:${C.blue}">${nm2(0, 1)} = ${fmtLen(I.s2.AB)}</span> · <span style="color:${C.coral}">${nm2(1, 2)} = ${fmtLen(I.s2.BC)}</span> · <span style="color:#0f9d7a">${nm2(2, 0)} = ${fmtLen(I.s2.CA)}</span> ${u1}`]);
      if (!I.flat && (show.has('angles') || show.has('sum'))) {
        const sh = niceAngles(I.angs);
        if (show.has('sum')) c.push(['wide', 'Angle sum', `∠${esc(L[0])} + ∠${esc(L[1])} + ∠${esc(L[2])} = ${sh[0]}° + ${sh[1]}° + ${sh[2]}° = <b style="color:${C.violet}">180°</b>`]);
        else c.push(['wide', 'Angles', `∠${esc(L[0])} = ${sh[0]}°, ∠${esc(L[1])} = ${sh[1]}°, ∠${esc(L[2])} = ${sh[2]}°`]);
      }
      if (show.has('area')) c.push(['', 'Area', `${f2(I.area)}${sq}`]);
      if (show.has('perimeter')) c.push(['', 'Perimeter', `${snap && [I.s2.AB, I.s2.BC, I.s2.CA].every(v => Number.isInteger(Math.sqrt(v))) ? '' : '≈ '}${f2(I.s.AB + I.s.BC + I.s.CA)} ${u1}`]);
      if (show.has('pythag')) {
        if (I.byAng === 'right') {
          const hyp = ['BC', 'CA', 'AB'][I.rightAt], legs = ['AB', 'BC', 'CA'].filter(k => k !== hyp);
          const nmK = k => ({ AB: nm2(0, 1), BC: nm2(1, 2), CA: nm2(2, 0) }[k]);
          c.push(['wide', 'Pythagoras', `${nmK(legs[0])}² + ${nmK(legs[1])}² = ${f2(I.s2[legs[0]])} + ${f2(I.s2[legs[1]])} = <b style="color:${C.violet}">${f2(I.s2[legs[0]] + I.s2[legs[1]])}</b> = ${nmK(hyp)}²`]);
        } else c.push(['wide', 'Pythagoras', `<span style="color:${C.muted}">Make a right angle to see the squares on the sides.</span>`]);
      }
      if (show.has('exterior') && !I.flat) {
        const sh = niceAngles(I.angs), ext = (180 - I.angs[2]);
        c.push(['wide', `Exterior angle at ${esc(L[2])}`, `<span style="color:#b07d00">${Number.isInteger(+sh[2]) ? 180 - sh[2] : (180 - sh[2]).toFixed(1)}°</span> = ∠${esc(L[0])} + ∠${esc(L[1])} = ${sh[0]}° + ${sh[1]}°`]);
      }
      if (show.has('inequality')) {
        const k = [['AB', 'BC', 'CA'], ['BC', 'CA', 'AB'], ['CA', 'AB', 'BC']], nmK = x => ({ AB: nm2(0, 1), BC: nm2(1, 2), CA: nm2(2, 0) }[x]);
        c.push(['wide', 'Sum of two sides vs third', k.map(([a, b, t]) => { const sm = I.s[a] + I.s[b], ok = sm - I.s[t] > 1e-9; return `${nmK(a)} + ${nmK(b)} = ${f2(sm)} ${ok ? '>' : '='} ${nmK(t)} = ${f2(I.s[t])} ${ok ? '✅' : '❌'}`; }).join('<br>')]);
      }
      gridEl.innerHTML = c.map(x => `<div class="lb-triangle-c ${x[0]}"><small>${x[1]}</small>${x[2]}</div>`).join('');
    }

    // ----- challenge -----
    function chText() {
      if (challengeText) return challengeText;
      if (goal === 'area') return `Make a triangle with area ${targetArea} sq ${unit || 'units'}`;
      return GOALTXT[goal] || GOALTXT.right;
    }
    function showCh() { chEl.textContent = '🎯 Challenge: ' + chText(); }
    function meets() { return evalGoal()[0]; }
    function check() {
      if (won) return;
      const [ok, msg] = evalGoal();
      if (ok) { won = true; api.sfx('correct'); api.win(p.winText || msg); }
    }
    function evalGoal() {
      const I = info(); let ok = false, msg;
      switch (goal) {
        case 'area': ok = !I.flat && Math.abs(I.area - targetArea) < 1e-6; msg = `Area = ${f2(I.area)} sq ${unit || 'units'}. Area = ½ × base × height.`; break;
        case 'flat': ok = I.flat; msg = `The corners are in a line, so two sides add up to exactly the third side. A triangle needs the sum of any two sides to be MORE than the third.`; break;
        case 'right isosceles': ok = I.byAng === 'right' && I.bySide === 'isosceles'; msg = `Right-angled and isosceles: the angles are 90°, 45° and 45°.`; break;
        case 'right': case 'acute': case 'obtuse': ok = I.byAng === goal; msg = goal === 'right' ? 'One angle is exactly 90°: a right-angled triangle!' : goal === 'acute' ? 'All three angles are less than 90°: an acute-angled triangle!' : 'One angle is more than 90°: an obtuse-angled triangle!'; break;
        default: ok = I.bySide === goal; msg = goal === 'isosceles' ? 'Two sides are equal, so the two angles opposite them are equal too!' : goal === 'equilateral' ? 'All sides equal, all angles 60°!' : 'All three sides are different: a scalene triangle!';
      }
      return [ok, msg];
    }

    // ----- dragging -----
    let drag = -1;
    function toGrid(e) {
      const m = svg.getScreenCTM(); if (!m) return null; const q = svg.createSVGPoint(); q.x = e.clientX; q.y = e.clientY; const r = q.matrixTransform(m.inverse());
      let x = (r.x - pad) / u, y = rows - (r.y - pad) / u;
      if (snap) { x = Math.round(x); y = Math.round(y); } else { x = Math.round(x * 10) / 10; y = Math.round(y * 10) / 10; }
      return [Math.max(0, Math.min(cols, x)), Math.max(0, Math.min(rows, y))];
    }
    function down(e) {
      const q = toGrid(e); if (!q) return;
      // pick nearest corner within reach
      let best = -1, bd = 1e9;
      pts.forEach((v, i) => { const d = Math.hypot(X(v[0]) - X(q[0]), Y(v[1]) - Y(q[1])); if (d < bd) { bd = d; best = i; } });
      const m = svg.getScreenCTM(), q2 = svg.createSVGPoint(); q2.x = e.clientX; q2.y = e.clientY; const r = q2.matrixTransform(m.inverse());
      const dd = Math.hypot(X(pts[best][0]) - r.x, Y(pts[best][1]) - r.y);
      if (dd > 34) return;
      drag = best; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); api.sfx('tap'); e.preventDefault();
    }
    function move(e) {
      if (drag < 0) return; const q = toGrid(e); if (!q) return;
      if (pts.some((v, i) => i !== drag && v[0] === q[0] && v[1] === q[1])) return;
      if (pts[drag][0] !== q[0] || pts[drag][1] !== q[1]) { pts[drag] = q; draw(); }
    }
    function up() { if (drag < 0) return; drag = -1; check(); }
    svg.addEventListener('pointerdown', down); svg.addEventListener('pointermove', move); svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
    host.querySelector('[data-reset]').addEventListener('click', () => { pts = startPts.map(q => q.slice()); draw(); api.sfx('tap'); });
    host.querySelector('[data-new]').addEventListener('click', () => {
      challengeText = null; won = false; api.resetWin && api.resetWin();
      // pick the next goal that the current triangle does NOT already meet (no free wins)
      for (let k = 0; k < goals.length; k++) {
        gi = (gi + 1) % goals.length; const gnext = goals[gi];
        if (typeof gnext === 'number') { targetArea = gnext; goal = 'area'; } else goal = (gnext === 'equilateral' && snap) ? 'isosceles' : String(gnext);
        if (goal === 'area' && typeof gnext !== 'number') targetArea = [6, 8, 10, 12, 15][Math.floor(Math.random() * 5)];
        if (!meets()) break;
      }
      showCh(); api.sfx('tap');
    });
    showCh(); draw();
    return () => { svg.removeEventListener('pointerdown', down); svg.removeEventListener('pointermove', move); svg.removeEventListener('pointerup', up); svg.removeEventListener('pointercancel', up); };
  }

  Labs.register('triangle', {
    title: 'Triangle explorer',
    subjects: ['maths'],
    render,
    example: { points: [[2, 1], [10, 2], [5, 7]], show: ['sides', 'angles', 'sum', 'class'], goal: 'right' },
    examples: [
      { points: [[4, 3], [7, 3], [4, 7]], grid: [12, 10], show: ['pythag', 'class'], goal: 'right', challenge: 'Find another right triangle and check: is the big square = the two small squares?' },
      { points: [[1, 1], [8, 1], [3, 5]], show: ['angles', 'exterior'], goal: 'obtuse', challenge: 'Make an obtuse triangle and check the exterior angle at C' },
      { points: [[1, 2], [6, 2], [3, 5]], show: ['inequality'], goal: 'flat', goals: ['flat', 'isosceles', 'scalene'] }
    ]
  });
})();
