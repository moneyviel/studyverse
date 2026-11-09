/* Knowtopia Concept Lab: coordplane — "Coordinate plane"
 * The child taps the Cartesian plane to plot points (they snap to the grid) and drags them around.
 * Coordinates, quadrant, distance, midpoint, slope and the line through two points update live.
 *
 * PARAMS (all optional; defaults in brackets)
 *  xRange      array   [min, max] of x                                                    [[-6,6]]
 *  yRange      array   [min, max] of y                                                    [[-5,5]]
 *  step        number  snapping step: 1, 0.5 or 0.25                                       [1]
 *  task        string  challenge type:                                                     ['plot']
 *                      'plot'     = plot the points in `targets`
 *                      'quadrant' = plot `count` points in quadrant `quadrant`
 *                      'midpoint' = plot the midpoint of the two `given` points
 *                      'distance' = plot a point exactly `dist` units from given[0]
 *                      'slope'    = plot B so that line AB (A = given[0]) has slope `slope`
 *  targets     array   plot: [[x,y],...]                                    [[[3,2],[-2,4],[-4,-3],[2,-1]]]
 *  targetLabels array  plot: names for the targets                                         [['A','B','C',...]]
 *  given       array   fixed points shown on the plane [[x,y],...]                         [task-specific]
 *  givenLabels array   names of the fixed points                                           [['P','Q',...]]
 *  quadrant    number  quadrant task: 1–4                                                  [3]
 *  count       number  quadrant task: how many points                                      [2]
 *  dist        number  distance task: required distance                                    [5]
 *  slope       number|string  slope task: e.g. 2, -1, '2/3'                                ['1/2']
 *  maxPoints   number  most points the child can plot                                      [4, or targets length]
 *  show        array   readouts: 'coords','quadrant','distance','midpoint','line'          [task-specific]
 *  challenge   string  challenge text (English or Hindi); default is generated
 *  winText     string  message on success
 */
(function () {
  const C = { violet: '#8b5cf6', mint: '#2ed3a5', sun: '#ffc93c', coral: '#ff6b6b', blue: '#3b82f6', ink: '#1b1f3a', muted: '#6b7090' };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
  const nf = v => { const r = Math.round(v * 1000) / 1000; return (r < 0 ? '−' : '') + Math.abs(r); };
  const pt = (q, k) => `(${nf(q[0])}, ${nf(q[1])})`;
  const QN = ['', 'I', 'II', 'III', 'IV'];
  const quadOf = q => q[0] === 0 && q[1] === 0 ? 'origin' : q[0] === 0 ? 'y-axis' : q[1] === 0 ? 'x-axis' : q[0] > 0 ? (q[1] > 0 ? 1 : 4) : (q[1] > 0 ? 2 : 3);
  const quadTxt = q => { const v = quadOf(q); return typeof v === 'number' ? 'Quadrant ' + QN[v] : v === 'origin' ? 'the origin' : 'on the ' + v; };
  function frac(n, d) { if (d === 0) return null; if (d < 0) { n = -n; d = -d; } const g = gcd(n, d); n /= g; d /= g; return d === 1 ? nf(n) : `${n < 0 ? '−' : ''}${Math.abs(n)}/${d}`; }
  function parseSlope(s) {
    if (typeof s === 'number' && isFinite(s)) { let d = 1; while (Math.abs(s * d - Math.round(s * d)) > 1e-9 && d < 1000) d *= 10; return [Math.round(s * d), d]; }
    const m = String(s).trim().replace('−', '-').match(/^(-?\d+)\s*\/\s*(-?\d+)$/); if (m && +m[2] !== 0) return [+m[1], +m[2]];
    const v = parseFloat(s); return isFinite(v) ? parseSlope(v) : [1, 2];
  }
  const CSS = `
.lb-coordplane-w{font-size:14px;color:${C.ink}}
.lb-coordplane-ch{background:#fff6d8;border-radius:12px;padding:6px 6px 6px 11px;font-weight:800;font-size:14px;margin-bottom:8px;line-height:1.3;display:flex;align-items:center;gap:6px}
.lb-coordplane-ch span{flex:1}
.lb-coordplane-ch .lb-coordplane-b{flex-shrink:0;font-size:13px;padding:0 10px}
.lb-coordplane-svg{width:100%;height:auto;display:block;touch-action:none;background:#fbfbff;border-radius:18px;user-select:none;-webkit-user-select:none}
.lb-coordplane-svg text{font-family:inherit;pointer-events:none}
.lb-coordplane-read{margin-top:8px;display:flex;flex-direction:column;gap:5px}
.lb-coordplane-pts{display:flex;flex-wrap:wrap;gap:5px}
.lb-coordplane-p{background:#f1efff;border-radius:999px;padding:4px 10px;font-weight:800;font-size:12.5px}
.lb-coordplane-c{background:#f4f6ff;border-radius:12px;padding:6px 10px;font-weight:800;font-size:13px;line-height:1.4}
.lb-coordplane-c small{color:${C.muted};font-size:11px;text-transform:uppercase;letter-spacing:.3px;margin-right:4px}
.lb-coordplane-row{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}
.lb-coordplane-b{min-height:40px;border:none;border-radius:12px;background:#f1efff;color:${C.ink};font:inherit;font-weight:800;font-size:14px;padding:0 13px;cursor:pointer}
.lb-coordplane-b.on{background:${C.ink};color:#fff}
.lb-coordplane-b.go{background:${C.violet};color:#fff}
.lb-coordplane-b:active{transform:scale(.95)}
`;

  function render(host, p, api) {
    const rng = (v, d) => Array.isArray(v) && v.length === 2 && isFinite(v[0]) && isFinite(v[1]) && +v[1] > +v[0] ? [Math.max(-20, +v[0]), Math.min(20, +v[1])] : d;
    const xr = rng(p.xRange, [-6, 6]), yr = rng(p.yRange, [-5, 5]);
    const step = [1, 0.5, 0.25].includes(+p.step) ? +p.step : 1, K = Math.round(1 / step);
    let task = ['plot', 'quadrant', 'midpoint', 'distance', 'slope'].includes(p.task) ? p.task : 'plot';
    const inR = q => q[0] >= xr[0] && q[0] <= xr[1] && q[1] >= yr[0] && q[1] <= yr[1];
    const okPts = a => Array.isArray(a) ? a.filter(q => Array.isArray(q) && q.length === 2 && isFinite(q[0]) && isFinite(q[1])).map(q => [+q[0], +q[1]]).filter(inR) : null;
    let targets = okPts(p.targets) || [[3, 2], [-2, 4], [-4, -3], [2, -1]].filter(inR);
    let given = okPts(p.given) || (task === 'midpoint' ? [[-4, -1], [2, 3]] : task === 'distance' ? [[0, 0]] : task === 'slope' ? [[-2, -1]] : []).filter(inR);
    let quadrant = Math.min(4, Math.max(1, +p.quadrant || 3)), count = Math.max(1, +p.count || 2);
    let dist = +p.dist > 0 ? +p.dist : 5, slope = parseSlope(p.slope != null ? p.slope : '1/2');
    const maxPts = Math.max(1, +p.maxPoints || (task === 'plot' ? Math.max(4, targets.length) : task === 'quadrant' ? Math.max(4, count) : 3));
    const show = new Set(Array.isArray(p.show) ? p.show : task === 'midpoint' ? ['coords', 'midpoint'] : task === 'distance' ? ['coords', 'distance'] : task === 'slope' ? ['coords', 'line'] : ['coords', 'quadrant']);
    const tLabels = Array.isArray(p.targetLabels) ? p.targetLabels.map(String) : 'ABCDEFGHIJKL'.split('');
    const gLabels = Array.isArray(p.givenLabels) ? p.givenLabels.map(String) : (task === 'slope' || task === 'distance' ? ['A', 'P', 'Q'] : ['P', 'Q', 'R', 'S']);
    const uLabels = task === 'slope' ? ['B', 'C', 'D', 'E', 'F'] : 'ABCDEFGHIJKL'.split('').filter(l => !gLabels.slice(0, given.length).includes(l));
    let challengeText = p.challenge ? String(p.challenge) : null, won = false;
    let pts = []; // child's points

    const xs = xr[1] - xr[0], ys = yr[1] - yr[0];
    const cell = Math.min(330 / xs, 228 / ys);
    const pw = xs * cell, ph = ys * cell, W = 360, H = Math.round(ph + 20);
    const x0 = (W - pw) / 2, y0 = 10;
    const SX = x => x0 + (x - xr[0]) * cell, SY = y => y0 + (yr[1] - y) * cell;
    const cid = 'lbcp' + Math.random().toString(36).slice(2, 8);

    host.innerHTML = `<style>${CSS}</style><div class="lb-coordplane-w"><div class="lb-coordplane-ch"><span></span><button class="lb-coordplane-b go" data-new aria-label="New challenge">🔄 New</button></div>
      <svg class="lb-coordplane-svg" viewBox="0 0 ${W} ${H}"><defs><clipPath id="${cid}"><rect x="${x0}" y="${y0}" width="${pw}" height="${ph}"/></clipPath></defs><g class="bg"></g><g class="fg"></g></svg>
      <div class="lb-coordplane-read"></div>
      <div class="lb-coordplane-row"><button class="lb-coordplane-b" data-undo>Undo</button><button class="lb-coordplane-b" data-clear>Clear</button></div></div>`;
    const svg = host.querySelector('svg'), fg = svg.querySelector('.fg'), rd = host.querySelector('.lb-coordplane-read'), chEl = host.querySelector('.lb-coordplane-ch span');

    // background grid + axes
    (function () {
      let s = `<rect x="${x0}" y="${y0}" width="${pw}" height="${ph}" fill="#fff"/>`;
      // quadrant tints
      const ox = Math.min(Math.max(SX(0), x0), x0 + pw), oy = Math.min(Math.max(SY(0), y0), y0 + ph);
      const tint = [[ox, y0, x0 + pw - ox, oy - y0, '#eefbf6'], [x0, y0, ox - x0, oy - y0, '#f3f0ff'], [x0, oy, ox - x0, y0 + ph - oy, '#fff7e0'], [ox, oy, x0 + pw - ox, y0 + ph - oy, '#ffefef']];
      tint.forEach(t => { if (t[2] > 0 && t[3] > 0) s += `<rect x="${t[0]}" y="${t[1]}" width="${t[2]}" height="${t[3]}" fill="${t[4]}"/>`; });
      for (let x = Math.ceil(xr[0]); x <= xr[1]; x++) s += `<line x1="${SX(x)}" y1="${y0}" x2="${SX(x)}" y2="${y0 + ph}" stroke="#dfe3f5" stroke-width="1"/>`;
      for (let y = Math.ceil(yr[0]); y <= yr[1]; y++) s += `<line x1="${x0}" y1="${SY(y)}" x2="${x0 + pw}" y2="${SY(y)}" stroke="#dfe3f5" stroke-width="1"/>`;
      if (xr[0] <= 0 && xr[1] >= 0) s += `<line x1="${SX(0)}" y1="${y0}" x2="${SX(0)}" y2="${y0 + ph}" stroke="${C.ink}" stroke-width="2"/>`;
      if (yr[0] <= 0 && yr[1] >= 0) s += `<line x1="${x0}" y1="${SY(0)}" x2="${x0 + pw}" y2="${SY(0)}" stroke="${C.ink}" stroke-width="2"/>`;
      const ax = Math.min(Math.max(SY(0), y0), y0 + ph), ay = Math.min(Math.max(SX(0), x0), x0 + pw);
      const every = Math.max(1, Math.ceil(xs / 14));
      for (let x = Math.ceil(xr[0]); x <= xr[1]; x++) if (x !== 0 && x % every === 0) s += `<text x="${SX(x)}" y="${Math.min(ax + 12, y0 + ph - 2)}" font-size="9.5" font-weight="700" fill="${C.muted}" text-anchor="middle">${nf(x)}</text>`;
      for (let y = Math.ceil(yr[0]); y <= yr[1]; y++) if (y !== 0 && y % every === 0) s += `<text x="${Math.max(ay - 4, x0 + 9)}" y="${SY(y) + 3.5}" font-size="9.5" font-weight="700" fill="${C.muted}" text-anchor="end">${nf(y)}</text>`;
      if (xr[0] <= 0 && xr[1] >= 0 && yr[0] <= 0 && yr[1] >= 0) s += `<text x="${SX(0) - 4}" y="${SY(0) + 12}" font-size="9.5" font-weight="700" fill="${C.muted}" text-anchor="end">0</text>`;
      s += `<text x="${x0 + pw - 4}" y="${ax - 5}" font-size="12" font-weight="800" fill="${C.ink}" text-anchor="end">x</text><text x="${ay + 6}" y="${y0 + 12}" font-size="12" font-weight="800" fill="${C.ink}">y</text>`;
      // quadrant names
      const qpos = [[x0 + pw - 14, y0 + 16, 1], [x0 + 16, y0 + 16, 2], [x0 + 18, y0 + ph - 8, 3], [x0 + pw - 16, y0 + ph - 8, 4]];
      qpos.forEach(([x, y, q]) => { const inQ = (q === 1 && xr[1] > 0 && yr[1] > 0) || (q === 2 && xr[0] < 0 && yr[1] > 0) || (q === 3 && xr[0] < 0 && yr[0] < 0) || (q === 4 && xr[1] > 0 && yr[0] < 0); if (inQ) s += `<text x="${x}" y="${y}" font-size="12" font-weight="800" fill="#b9bedb" text-anchor="middle">${QN[q]}</text>`; });
      svg.querySelector('.bg').innerHTML = s;
    })();

    const all = () => given.map((q, i) => ({ q, l: gLabels[i] || 'P' + (i + 1), g: true })).concat(pts.map((q, i) => ({ q, l: labelFor(q, i), g: false })));
    function labelFor(q, i) { if (task === 'plot') { const t = targets.findIndex(tq => tq[0] === q[0] && tq[1] === q[1]); if (t >= 0) return tLabels[t] || '?'; } return uLabels[i] || '?'; }
    const pair = () => { const a = all(); return a.length >= 2 ? [a[a.length - 2], a[a.length - 1]] : null; };

    function draw() {
      let s = '';
      const pr = pair();
      if (pr) {
        const [A, B] = pr, a = A.q, b = B.q;
        if (show.has('line') && !(a[0] === b[0] && a[1] === b[1])) {
          const dx = b[0] - a[0], dy = b[1] - a[1], L = 100;
          s += `<line clip-path="url(#${cid})" x1="${SX(a[0] - dx * L)}" y1="${SY(a[1] - dy * L)}" x2="${SX(a[0] + dx * L)}" y2="${SY(a[1] + dy * L)}" stroke="${C.violet}" stroke-width="2.5" opacity=".75"/>`;
          // rise/run steps
          s += `<path d="M${SX(a[0])} ${SY(a[1])} H${SX(b[0])} V${SY(b[1])}" fill="none" stroke="${C.sun}" stroke-width="2.5" stroke-dasharray="5 4"/>`;
          s += lab((SX(a[0]) + SX(b[0])) / 2, SY(a[1]) + (dy > 0 ? 13 : -6), `run ${nf(dx)}`, '#b07d00', 10.5) + lab(SX(b[0]) + (dx > 0 ? 5 : -5), (SY(a[1]) + SY(b[1])) / 2 + 4, `rise ${nf(dy)}`, '#b07d00', 10.5, dx > 0 ? 'start' : 'end');
        }
        if (show.has('distance')) {
          s += `<path d="M${SX(a[0])} ${SY(a[1])} H${SX(b[0])} V${SY(b[1])}" fill="none" stroke="${C.blue}" stroke-width="2" stroke-dasharray="4 4"/>`;
          s += `<line x1="${SX(a[0])}" y1="${SY(a[1])}" x2="${SX(b[0])}" y2="${SY(b[1])}" stroke="${C.coral}" stroke-width="3"/>`;
          const dx = b[0] - a[0], dy = b[1] - a[1];
          if (dx) s += lab((SX(a[0]) + SX(b[0])) / 2, SY(a[1]) + (dy > 0 ? 13 : -6), nf(Math.abs(dx)), C.blue, 11);
          if (dy) s += lab(SX(b[0]) + (dx >= 0 ? 6 : -6), (SY(a[1]) + SY(b[1])) / 2 + 4, nf(Math.abs(dy)), C.blue, 11, dx >= 0 ? 'start' : 'end');
        }
        if (show.has('midpoint')) {
          const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
          if (!show.has('distance')) s += `<line x1="${SX(a[0])}" y1="${SY(a[1])}" x2="${SX(b[0])}" y2="${SY(b[1])}" stroke="${C.mint}" stroke-width="3"/>`;
          if (task !== 'midpoint') s += `<rect x="${SX(m[0]) - 6}" y="${SY(m[1]) - 6}" width="12" height="12" rx="3" fill="${C.mint}" stroke="#fff" stroke-width="2" transform="rotate(45 ${SX(m[0])} ${SY(m[1])})"/>` + lab(SX(m[0]) + 9, SY(m[1]) - 8, 'M', '#0f9d7a', 12, 'start');
        }
      }
      if (task === 'distance' && given[0]) { // faint circle hint of radius dist
        s += `<circle clip-path="url(#${cid})" cx="${SX(given[0][0])}" cy="${SY(given[0][1])}" r="${dist * cell}" fill="none" stroke="${C.coral}" stroke-width="1.2" stroke-dasharray="3 5" opacity=".55"/>`;
      }
      all().forEach(({ q, l, g }) => {
        const x = SX(q[0]), y = SY(q[1]);
        const good = !g && task === 'plot' && targets.some(t => t[0] === q[0] && t[1] === q[1]);
        const col = g ? C.ink : good ? '#0f9d7a' : C.violet;
        if (!g) s += `<circle cx="${x}" cy="${y}" r="20" fill="transparent"/>`;
        s += `<circle cx="${x}" cy="${y}" r="${g ? 6 : 8}" fill="${col}" stroke="#fff" stroke-width="2.5" style="filter:drop-shadow(0 1px 2px rgba(0,0,0,.25))"/>`;
        if (show.has('coords') || g) {
          const right = x < x0 + pw - 70, up = y > y0 + 16;
          s += lab(x + (right ? 10 : -10), y + (up ? -9 : 18), `${esc(l)}${pt(q)}`, col, 11.5, right ? 'start' : 'end');
        } else s += lab(x + 10, y - 9, esc(l), col, 12, 'start');
      });
      fg.innerHTML = s;
      readout();
    }
    function lab(x, y, t, col, size = 11, anchor = 'middle') { return `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="${size}" font-weight="800" fill="${col}" text-anchor="${anchor}" stroke="#fff" stroke-width="3" paint-order="stroke">${t}</text>`; }
    function surd(n2) { // n2 = d² (scaled by K² so integer)
      const v = Math.round(n2 * K * K); let out = 1, inn = v;
      for (let f = 2; f * f <= inn; f++) while (inn % (f * f) === 0) { inn /= f * f; out *= f; }
      // value = out√inn / K
      const val = Math.sqrt(n2);
      if (inn === 1) return nf(out / K);
      const coef = out / K; return `${coef === 1 ? '' : nf(coef)}√${inn} ≈ ${nf(Math.round(val * 100) / 100)}`;
    }
    function readout() {
      let h = '';
      const a = all();
      if (a.length) h += `<div class="lb-coordplane-pts">${a.map(({ q, l, g }) => `<span class="lb-coordplane-p" style="${g ? 'background:#eceef8' : ''}">${esc(l)}${pt(q)}${show.has('quadrant') ? ` · ${quadTxt(q)}` : ''}</span>`).join('')}</div>`;
      else h += `<div class="lb-coordplane-c" style="color:${C.muted}">Tap the grid to plot a point. Drag a point to move it.</div>`;
      const pr = pair();
      if (pr) {
        const [A, B] = pr, x1 = A.q[0], y1 = A.q[1], x2 = B.q[0], y2 = B.q[1], dx = x2 - x1, dy = y2 - y1, nm = A.l + B.l;
        if (show.has('distance')) h += `<div class="lb-coordplane-c"><small>Distance</small>${esc(nm)} = √(${nf(dx)}² + ${nf(dy)}²) = √${nf(dx * dx + dy * dy)} = <b style="color:${C.coral}">${surd(dx * dx + dy * dy)}</b></div>`;
        if (show.has('midpoint')) h += `<div class="lb-coordplane-c"><small>Midpoint</small>((${nf(x1)} + ${nf(x2)})/2, (${nf(y1)} + ${nf(y2)})/2) = <b style="color:#0f9d7a">${pt([(x1 + x2) / 2, (y1 + y2) / 2])}</b></div>`;
        if (show.has('line')) {
          const DX = Math.round(dx * K), DY = Math.round(dy * K);
          if (DX === 0 && DY === 0) h += `<div class="lb-coordplane-c"><small>Line</small>Pick two different points.</div>`;
          else if (DX === 0) h += `<div class="lb-coordplane-c"><small>Line ${esc(nm)}</small>vertical line <b style="color:${C.violet}">x = ${nf(x1)}</b> (slope undefined)</div>`;
          else {
            const m = frac(DY, DX), cN = Math.round(y1 * K) * DX - DY * Math.round(x1 * K), cD = K * DX, c = frac(cN, cD);
            const eq = DY === 0 ? `y = ${c}` : `y = ${m === '1' ? '' : m === '−1' ? '−' : m}x ${cN === 0 ? '' : (cN / cD > 0 ? '+ ' + c : '− ' + c.replace('−', ''))}`;
            h += `<div class="lb-coordplane-c"><small>Slope</small>m = rise/run = ${nf(dy)}/${nf(dx)} = <b style="color:${C.violet}">${m}</b> &nbsp;<small>Line</small><b>${eq.trim()}</b></div>`;
          }
        }
      }
      rd.innerHTML = h;
    }

    // ----- challenge -----
    function chText() {
      if (challengeText) return challengeText;
      if (task === 'plot') return 'Plot ' + targets.map((t, i) => `${tLabels[i] || ''}${pt(t)}`).join(', ');
      if (task === 'quadrant') return `Plot ${count} point${count > 1 ? 's' : ''} in Quadrant ${QN[quadrant]}`;
      if (task === 'midpoint') return `Plot the midpoint of ${gLabels[0]}${pt(given[0])} and ${gLabels[1]}${pt(given[1])}`;
      if (task === 'distance') return `Plot a point exactly ${nf(dist)} units from ${gLabels[0]}${pt(given[0])}`;
      return `Plot B so that line AB has slope ${frac(slope[0], slope[1])}`;
    }
    function showCh() { chEl.textContent = '🎯 Challenge: ' + chText(); }
    function check() {
      if (won) return;
      const has = t => pts.some(q => q[0] === t[0] && q[1] === t[1]);
      let ok = false, msg = '';
      if (task === 'plot') { ok = targets.length > 0 && targets.every(has); msg = `All ${targets.length} points plotted correctly! x first (across), then y (up/down).`; }
      else if (task === 'quadrant') { const n = pts.filter(q => quadOf(q) === quadrant).length; ok = n >= count; msg = `In Quadrant ${QN[quadrant]}, x is ${quadrant === 1 || quadrant === 4 ? 'positive' : 'negative'} and y is ${quadrant <= 2 ? 'positive' : 'negative'}.`; }
      else if (task === 'midpoint' && given.length >= 2) { const m = [(given[0][0] + given[1][0]) / 2, (given[0][1] + given[1][1]) / 2]; ok = has(m); msg = `Midpoint = ${pt(m)}: average the x's and the y's.`; }
      else if (task === 'distance' && given[0]) { const g = given[0]; const q = pts.find(q => Math.abs((q[0] - g[0]) ** 2 + (q[1] - g[1]) ** 2 - dist * dist) < 1e-9); ok = !!q; if (q) msg = `√(${nf(q[0] - g[0])}² + ${nf(q[1] - g[1])}²) = √${nf(dist * dist)} = ${nf(dist)}. Well done!`; }
      else if (task === 'slope' && given[0]) { const g = given[0]; const q = pts.find(q => { const DX = Math.round((q[0] - g[0]) * K), DY = Math.round((q[1] - g[1]) * K); return DX !== 0 && DY * slope[1] === slope[0] * DX; }); ok = !!q; if (q) msg = `Rise ${nf(q[1] - g[1])} over run ${nf(q[0] - g[0])} gives slope ${frac(slope[0], slope[1])}!`; }
      if (ok) { won = true; api.sfx('correct'); api.win(p.winText || msg); }
    }

    // ----- interaction -----
    let drag = -1, moved = false;
    function svgXY(e) { const m = svg.getScreenCTM(); if (!m) return null; const q = svg.createSVGPoint(); q.x = e.clientX; q.y = e.clientY; const t = q.matrixTransform(m.inverse()); return [t.x, t.y]; }
    const snapQ = s => { let x = xr[0] + (s[0] - x0) / cell, y = yr[1] - (s[1] - y0) / cell; x = Math.round(x / step) * step; y = Math.round(y / step) * step; return [Math.max(xr[0], Math.min(xr[1], +x.toFixed(3))), Math.max(yr[0], Math.min(yr[1], +y.toFixed(3)))]; };
    const occupied = (q, skip) => all().some((o, i) => o.q[0] === q[0] && o.q[1] === q[1] && !(skip != null && !o.g && i - given.length === skip));
    function down(e) {
      const s = svgXY(e); if (!s) return;
      if (s[0] < x0 - 12 || s[0] > x0 + pw + 12 || s[1] < y0 - 12 || s[1] > y0 + ph + 12) return;
      let best = -1, bd = 22;
      pts.forEach((q, i) => { const d = Math.hypot(SX(q[0]) - s[0], SY(q[1]) - s[1]); if (d < bd) { bd = d; best = i; } });
      if (best < 0) {
        const q = snapQ(s); if (occupied(q)) return;
        if (pts.length >= maxPts) { api.sfx('hmm'); rd.insertAdjacentHTML('afterbegin', `<div class="lb-coordplane-c" style="color:${C.coral}">That's ${maxPts} points. Drag one, or tap Undo.</div>`); return; }
        pts.push(q); best = pts.length - 1; api.sfx('tap'); draw();
      }
      drag = best; moved = false; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); e.preventDefault();
    }
    function move(e) {
      if (drag < 0) return; const s = svgXY(e); if (!s) return; const q = snapQ(s);
      if ((q[0] !== pts[drag][0] || q[1] !== pts[drag][1]) && !occupied(q, drag)) { pts[drag] = q; moved = true; draw(); }
    }
    function up() { if (drag < 0) return; drag = -1; check(); }
    svg.addEventListener('pointerdown', down); svg.addEventListener('pointermove', move); svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
    host.querySelector('[data-undo]').addEventListener('click', () => { pts.pop(); api.sfx('tap'); draw(); });
    host.querySelector('[data-clear]').addEventListener('click', () => { pts = []; api.sfx('tap'); draw(); });
    const ri = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
    const rpt = () => [ri(Math.ceil(xr[0]), Math.floor(xr[1])), ri(Math.ceil(yr[0]), Math.floor(yr[1]))];
    host.querySelector('[data-new]').addEventListener('click', () => {
      challengeText = null; won = false; api.resetWin && api.resetWin(); api.sfx('tap'); pts = [];
      if (task === 'plot') { const n = Math.max(1, Math.min(4, targets.length || 3)), seen = new Set(); targets = []; while (targets.length < n) { const q = rpt(); const k = q.join(); if (!seen.has(k)) { seen.add(k); targets.push(q); } } }
      else if (task === 'quadrant') { const avail = [1, 2, 3, 4].filter(q => (q === 1 ? xr[1] > 0 && yr[1] > 0 : q === 2 ? xr[0] < 0 && yr[1] > 0 : q === 3 ? xr[0] < 0 && yr[0] < 0 : xr[1] > 0 && yr[0] < 0)); quadrant = avail[ri(0, avail.length - 1)] || 1; count = ri(1, 3); }
      else if (task === 'midpoint') { let a, b, k = 0; do { a = rpt(); b = rpt(); k++; } while (k < 50 && (((a[0] + b[0]) / 2) % step !== 0 || ((a[1] + b[1]) / 2) % step !== 0 || (a[0] === b[0] && a[1] === b[1]))); given = [a, b]; }
      else if (task === 'distance') { const triples = [[3, 4, 5], [6, 8, 10], [5, 12, 13]]; const fit = triples.filter(t => t[1] <= Math.min(xs, ys)); const t = fit[ri(0, fit.length - 1)] || [3, 4, 5]; dist = t[2]; given = [[Math.round((xr[0] + xr[1]) / 2), Math.round((yr[0] + yr[1]) / 2)]]; }
      else { const opts = [[1, 1], [2, 1], [-1, 1], [1, 2], [-2, 3], [3, 2], [-1, 2], [0, 1]]; slope = opts[ri(0, opts.length - 1)]; given = [[ri(Math.ceil(xr[0]), Math.ceil(xr[0]) + 2), ri(Math.ceil(yr[0]), Math.ceil(yr[0]) + 2)]]; }
      showCh(); draw();
    });
    showCh(); draw();
    return () => { svg.removeEventListener('pointerdown', down); svg.removeEventListener('pointermove', move); svg.removeEventListener('pointerup', up); svg.removeEventListener('pointercancel', up); };
  }

  Labs.register('coordplane', {
    title: 'Coordinate plane',
    subjects: ['maths'],
    render,
    example: { task: 'plot', xRange: [-6, 6], yRange: [-5, 5], targets: [[3, 2], [-2, 4], [-4, -3]] },
    examples: [
      { task: 'quadrant', quadrant: 2, count: 2, show: ['coords', 'quadrant'] },
      { task: 'distance', given: [[-2, -1]], dist: 5, show: ['coords', 'distance'] },
      { task: 'slope', given: [[-3, -2]], slope: '2/3', show: ['coords', 'line'] }
    ]
  });
})();
