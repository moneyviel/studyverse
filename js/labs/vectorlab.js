/* StudyVerse Concept Lab: vectorlab — vectors, projectile motion and relative velocity (Class 11 Physics ch. 3/4,
 * Class 11/12 Maths vectors). NCERT notation: R = √(A² + B² + 2AB cos θ), tan α = B sin θ / (A + B cos θ),
 * R = u² sin 2θ / g, H = u² sin²θ / 2g, T = 2u sin θ / g.
 *
 * mode 'add'       : drag the heads of vectors A, B (and C …) on a grid; switch triangle / parallelogram law;
 *                    the resultant R, its magnitude and direction update live (op 'sub' shows A − B).
 * mode 'resolve'   : drag the head of A (snaps to 0.5-unit length and 5° steps); its components along x and y
 *                    (or along tilted axes x′, y′) are drawn and computed: Aₓ = A cos θ, Aᵧ = A sin θ.
 *                    incline:true → a block on an incline: slide the incline angle and watch mg sin φ and
 *                    mg cos φ.
 * mode 'projectile': slide the launch speed u and angle θ, tap Launch; the ball flies with live vₓ, vᵧ arrows;
 *                    range, max height and time of flight from the formulas (optional launch height h0).
 * mode 'relative'  : scene 'rain' — walk at speed v_m in vertical rain v_r; tilt the umbrella to the apparent
 *                    rain direction (tan θ = v_m / v_r). scene 'river' — steer a boat across a river:
 *                    t = d / (v cos α), drift = (u − v sin α) t.
 *
 * PARAMS (all optional)
 *   mode        'add' | 'resolve' | 'projectile' | 'relative'                                 default 'add'
 *   unit        string  unit of vector magnitudes, e.g. 'N', 'm', 'm/s'                       default '' (add/resolve)
 *   — add —
 *   vectors     [{x,y,label,color,fixed}]  2–3 starting vectors (grid units); fixed:true = not draggable
 *               default [{x:3,y:1,label:'A'},{x:1,y:3,label:'B'}]
 *   law         'parallelogram' | 'triangle'   starting law (toggle button shown for 2 vectors) default 'parallelogram'
 *   op          'add' | 'sub'   R = A + B or R = A − B                                     default 'add'
 *   view        [xmin,xmax,ymin,ymax] grid window (3:2 looks best)       default [-3,9,-1.5,5.5] (sub: [-6,6,-3.5,3.5])
 *   snap        number  grid snap for heads                                                 default 0.5
 *   — resolve —
 *   vector      {x,y,label}   starting vector                                             default {x:3,y:2,label:'A'}
 *   axisAngle   number  tilt of the x′ axis in degrees (0 = ordinary x, y)                  default 0
 *   incline     boolean block-on-incline scene (weight resolved along / perpendicular)      default false
 *   mass, g     numbers incline: mass in kg and g in m/s²                                   default 2, 10
 *   angle       number  incline: starting angle φ in degrees                                default 20
 *   — projectile —
 *   speed, angle  starting u (m/s) and θ (degrees)                                         default 20, 30
 *   speedRange  [min,max]  u slider                                                         default [5,30]
 *   angleRange  [min,max]  θ slider (degrees)                                               default [5,85] (h0>0: [0,85])
 *   g           number  m/s²                                                                default 9.8
 *   h0          number  launch height above the ground in m                                 default 0
 *   — relative —
 *   scene       'rain' | 'river'                                                            default 'rain'
 *   rain        number  rain speed v_r (vertical), m/s                                      default 6
 *   wind        number  horizontal velocity of the rain (+ = direction of walking), m/s     default 0
 *   walk        number  starting walking speed v_m                                          default 0
 *   walkRange   [min,max]  walking-speed slider                                             default [0,10]
 *   river       number  river speed u, m/s (flows left → right)                             default 3
 *   width       number  river width d, m                                                    default 100
 *   boat        number  starting boat speed v in still water, m/s                           default 5
 *   boatRange   [min,max]  boat-speed slider                                                default [1,10]
 *   heading     number  starting heading α from straight across, degrees (+ = upstream)     default 0
 * Challenge (one target; if none is given a sensible one is generated for the mode):
 *   target      add:        {R, theta} resultant magnitude and direction (θ from +x, degrees) or {x,y} tip of R
 *               resolve:    {x, y} components (either or both) or {R, theta};  incline: {along} or {perp} (N)
 *               projectile: {range} (both:true → hit it with two different angles) | {height} | {hit:[x,y]}
 *               rain:       {walk} — walk at this speed and tilt the umbrella correctly | {angle} — walk so the rain
 *                           appears at this angle from the vertical
 *               river:      {drift:0} reach the point opposite | {time:'min'} cross in the least time | {land:x} land
 *                           x m downstream
 *   challenge   string  challenge sentence (may be Hindi); else generated
 *   winText     string  optional win message
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const minus = s => String(s).replace(/-/g, '−');
  const fmt = (v, dp = 2) => { if (!isFinite(v)) return '—'; let s = (+v.toFixed(dp)).toString(); if (s === '-0') s = '0'; return minus(s); };
  const deg = r => r * 180 / Math.PI, rad = d => d * Math.PI / 180;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const clean = v => +(+v).toFixed(9);
  const arr2 = (a, d) => Array.isArray(a) && a.length === 2 && isFinite(+a[0]) && isFinite(+a[1]) && +a[0] < +a[1] ? a.map(Number) : d;
  const COLS = ['#3b82f6', '#ff6b6b', '#2ed3a5', '#ffc93c'];
  const dirAngle = (x, y) => { let a = deg(Math.atan2(y, x)); if (a < 0) a += 360; return a; };

  function arrow(x1, y1, x2, y2, col, w = 3.5, extra = '') {
    const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy);
    if (L < 1) return '';
    const ux = dx / L, uy = dy / L, hl = Math.min(13, L * 0.45), hw = hl * 0.55;
    const bx = x2 - ux * hl, by = y2 - uy * hl;
    return `<g ${extra}><line x1="${x1}" y1="${y1}" x2="${bx}" y2="${by}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/><path d="M${x2} ${y2}L${bx - uy * hw} ${by + ux * hw}L${bx + uy * hw} ${by - ux * hw}Z" fill="${col}" stroke="${col}" stroke-width="1" stroke-linejoin="round"/></g>`;
  }
  const txt = (x, y, t, col, size = 12, anchor = 'middle', extra = '') => `<text x="${x}" y="${y}" font-size="${size}" font-weight="900" fill="${col}" text-anchor="${anchor}" paint-order="stroke" stroke="#fff" stroke-width="3.5" stroke-linejoin="round" ${extra}>${t}</text>`;

  Labs.register('vectorlab', {
    title: 'Vector lab',
    subjects: ['physics', 'maths'],
    render(host, p, api) {
      const mode = ['add', 'resolve', 'projectile', 'relative'].includes(p.mode) ? p.mode : 'add';
      const unit = p.unit != null ? String(p.unit) : '';
      const U = unit ? ' ' + esc(unit) : '';
      let won = false, touched = false, raf = 0, customRound = false;
      const listeners = [];
      const on = (el, ev, fn) => { el.addEventListener(ev, fn); listeners.push([el, ev, fn]); };
      const cleanup = () => { cancelAnimationFrame(raf); listeners.forEach(([el, ev, fn]) => el.removeEventListener(ev, fn)); };
      const css = `
.lb-vectorlab-w{font-size:13.5px;color:#1b1f3a}
.lb-vectorlab-ch{font-weight:800;font-size:14px;margin-bottom:5px;line-height:1.3}
.lb-vectorlab-svg{width:100%;height:auto;display:block;background:#fbfbff;border:1.5px solid #e6e8f7;border-radius:16px;touch-action:none;user-select:none;-webkit-user-select:none;box-sizing:border-box}
.lb-vectorlab-chips{display:flex;flex-wrap:wrap;gap:4px;margin-top:5px}
.lb-vectorlab-chip{flex:1 1 auto;border-radius:10px;padding:3px 6px;font-weight:800;font-size:12.5px;text-align:center;background:#f1f2fb;white-space:nowrap}
.lb-vectorlab-chip b{font-size:14px}
.lb-vectorlab-f{margin-top:4px;background:#f6f4ff;border-radius:11px;padding:4px 8px;font-weight:700;font-size:12.5px;line-height:1.4;text-align:center}
.lb-vectorlab-f b{color:#5b33c9}
.lb-vectorlab-row{display:flex;gap:5px;margin-top:5px;align-items:center}
.lb-vectorlab-b{flex:1;min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 6px}
.lb-vectorlab-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-vectorlab-b.go{background:#2ed3a5;color:#08372a;box-shadow:0 3px 0 #1ea383}
.lb-vectorlab-b:active{transform:translateY(2px)}
.lb-vectorlab-b:disabled{opacity:.5}
.lb-vectorlab-sl{display:flex;align-items:center;gap:7px;font-weight:800;font-size:13px}
.lb-vectorlab-sl span{min-width:86px;white-space:nowrap}
.lb-vectorlab-sl input{flex:1;min-width:0;-webkit-appearance:none;appearance:none;height:32px;background:transparent;cursor:pointer}
.lb-vectorlab-sl input::-webkit-slider-runnable-track{height:8px;border-radius:8px;background:#e3e6f6}
.lb-vectorlab-sl input::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:26px;border-radius:50%;background:#8b5cf6;margin-top:-9px;border:3px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.3)}
.lb-vectorlab-sl input::-moz-range-track{height:8px;border-radius:8px;background:#e3e6f6}
.lb-vectorlab-sl input::-moz-range-thumb{width:20px;height:20px;border-radius:50%;background:#8b5cf6;border:3px solid #fff}
.lb-vectorlab-msg{font-size:12.5px;font-weight:700;color:#6b7090;margin-top:4px;min-height:16px;text-align:center;line-height:1.3}`;
      const W = 360;
      function shell(H, controls) {
        host.innerHTML = `<style>${css}</style><div class="lb-vectorlab-w"><div class="lb-vectorlab-ch">🎯 Challenge: <span class="lb-vectorlab-cht"></span></div>
<svg class="lb-vectorlab-svg" viewBox="0 0 ${W} ${H}"><g class="lb-vectorlab-bg"></g><g class="lb-vectorlab-dyn"></g></svg>${controls}<div class="lb-vectorlab-msg"></div></div>`;
      }
      const $ = s => host.querySelector(s);
      const setCh = t => { $('.lb-vectorlab-cht').textContent = t; };
      const msg = t => { $('.lb-vectorlab-msg').innerHTML = t; };
      const out = (k, v) => { const el = host.querySelector(`[data-o="${k}"]`); if (el) el.innerHTML = v; };
      function win(t) { if (won) return; won = true; api.sfx('correct'); api.win(p.winText && !customRound ? p.winText : t); }
      function newRound(text) { customRound = true; won = false; api.resetWin(); setCh(text); api.sfx('tap'); }
      function svgPt(e, svg, H) { const r = svg.getBoundingClientRect(); return { x: (e.clientX - r.left) * W / r.width, y: (e.clientY - r.top) * H / r.height }; }
      function dragOn(svg, H, start, move, end) {
        let dr = false;
        on(svg, 'pointerdown', e => { const pt = svgPt(e, svg, H); dr = start(pt) !== false; if (dr) { touched = true; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); move(pt); e.preventDefault(); } });
        on(svg, 'pointermove', e => { if (dr) move(svgPt(e, svg, H)); });
        const up = () => { if (dr) { dr = false; end && end(); } };
        on(svg, 'pointerup', up); on(svg, 'pointercancel', up);
      }
      const slider = (key, label, min, max, step, val) => `<label class="lb-vectorlab-sl"><span>${label} <b data-o="${key}"></b></span><input type="range" data-k="${key}" min="${min}" max="${max}" step="${step}" value="${val}"></label>`;
      function gridBg(view, s, ox, oy, H, rot = 0) {
        const [x0, x1, y0, y1] = view; let g = '';
        if (!rot) {
          for (let x = Math.ceil(x0); x <= x1; x++) g += `<line x1="${ox + x * s}" y1="0" x2="${ox + x * s}" y2="${H}" stroke="${x ? '#eceefa' : '#1b1f3a'}" stroke-width="${x ? 1 : 1.3}"/>`;
          for (let y = Math.ceil(y0); y <= y1; y++) g += `<line x1="0" y1="${oy - y * s}" x2="${W}" y2="${oy - y * s}" stroke="${y ? '#eceefa' : '#1b1f3a'}" stroke-width="${y ? 1 : 1.3}"/>`;
          for (let x = Math.ceil(x0); x <= x1; x++) if (x && x % 2 === 0 && ox + x * s > 8 && ox + x * s < W - 8) g += txt(ox + x * s, oy + 12, minus(x), '#8a8fae', 9.5);
          for (let y = Math.ceil(y0); y <= y1; y++) if (y && y % 2 === 0 && oy - y * s > 8 && oy - y * s < H - 6) g += txt(ox - 5, oy - y * s + 3.5, minus(y), '#8a8fae', 9.5, 'end');
          g += txt(W - 8, oy - 5, 'x', '#1b1f3a', 11, 'end') + txt(ox + 8, 12, 'y', '#1b1f3a', 11, 'start');
        } else {
          const R = 16;
          g += `<g transform="rotate(${-rot} ${ox} ${oy})">`;
          for (let k = -R; k <= R; k++) g += `<line x1="${ox + k * s}" y1="${oy - R * s}" x2="${ox + k * s}" y2="${oy + R * s}" stroke="${k ? '#eceefa' : '#1b1f3a'}" stroke-width="${k ? 1 : 1.3}"/><line x1="${ox - R * s}" y1="${oy - k * s}" x2="${ox + R * s}" y2="${oy - k * s}" stroke="${k ? '#eceefa' : '#1b1f3a'}" stroke-width="${k ? 1 : 1.3}"/>`;
          g += '</g>';
          const ex = ox + Math.cos(rad(rot)) * (W * 0.47), ey = oy - Math.sin(rad(rot)) * (W * 0.47);
          g += txt(ex, ey - 5, 'x′', '#1b1f3a', 11.5) + txt(ox - Math.sin(rad(rot)) * 108 + 10, oy - Math.cos(rad(rot)) * 108, 'y′', '#1b1f3a', 11.5);
        }
        return g;
      }

      if (mode === 'add') return addMode();
      if (mode === 'resolve') return p.incline ? inclineMode() : resolveMode();
      if (mode === 'projectile') return projectile();
      return p.scene === 'river' ? river() : rain();

      // =============== add ===============
      function addMode() {
        const op = p.op === 'sub' ? 'sub' : 'add';
        const snap = +p.snap > 0 ? +p.snap : 0.5;
        const view = Array.isArray(p.view) && p.view.length === 4 && p.view.every(v => isFinite(+v)) && +p.view[0] < +p.view[1] && +p.view[2] < +p.view[3] ? p.view.map(Number) : (op === 'sub' ? [-6, 6, -3.5, 3.5] : [-3, 9, -1.5, 5.5]);
        const s = W / (view[1] - view[0]), H = Math.round(Math.min(250, Math.max(160, (view[3] - view[2]) * s)));
        const ox = -view[0] * s, oy = H + view[2] * s;
        const vin = Array.isArray(p.vectors) && p.vectors.length >= 2 ? p.vectors.slice(0, 3) : [{ x: 3, y: 1, label: 'A' }, { x: 1, y: 3, label: 'B' }];
        const V = vin.map((v, i) => ({ x: isFinite(+v.x) ? +v.x : 1, y: isFinite(+v.y) ? +v.y : 1, label: v.label != null ? String(v.label) : 'ABC'[i], col: v.color || COLS[i], fixed: !!v.fixed }));
        const two = V.length === 2;
        let law = !two || p.law === 'triangle' ? 'triangle' : 'parallelogram';
        const tg = p.target || {};
        let target = null; // {x,y} of R's tip or {R,theta}
        if (isFinite(+tg.x) && isFinite(+tg.y)) target = { x: +tg.x, y: +tg.y };
        else if (isFinite(+tg.R) && isFinite(+tg.theta)) target = { R: +tg.R, theta: +tg.theta };
        if (!target) target = op === 'sub' ? { x: -2, y: 4 } : { R: 5, theta: 36.87 };
        const tTip = () => target.R != null ? { x: target.R * Math.cos(rad(target.theta)), y: target.R * Math.sin(rad(target.theta)) } : target;
        const sym = op === 'sub' ? '−' : '+';
        const Rname = two ? `${esc(V[0].label)} ${sym} ${esc(V[1].label)}` : 'R';
        const genText = () => { const t = tTip(); const R = Math.hypot(t.x, t.y); return `Drag the vector heads to make the resultant R = ${fmt(R)}${unit ? ' ' + unit : ''} at θ = ${fmt(dirAngle(t.x, t.y), 1)}° to the x-axis.`; };
        shell(H, `<div class="lb-vectorlab-chips">${V.map((v, i) => `<div class="lb-vectorlab-chip" style="color:${v.col};background:${v.col}1f">|${esc(v.label)}| = <b data-o="m${i}"></b></div>`).join('')}${two ? `<div class="lb-vectorlab-chip" style="background:#fff5d6;color:#9a6a00">${op === 'sub' ? `θ(${esc(V[0].label)}, −${esc(V[1].label)})` : 'θ'} = <b data-o="th"></b></div>` : ''}<div class="lb-vectorlab-chip" style="background:#f3edff;color:#5b33c9">|R| = <b data-o="R"></b></div></div>
<div class="lb-vectorlab-f" data-o="f"></div>
<div class="lb-vectorlab-row">${two ? `<button class="lb-vectorlab-b" data-law="triangle">Triangle law</button><button class="lb-vectorlab-b" data-law="parallelogram">Parallelogram</button>` : ''}<button class="lb-vectorlab-b" data-act="new">New</button></div>`);
        setCh(p.challenge || genText());
        const svg = $('.lb-vectorlab-svg'), dyn = $('.lb-vectorlab-dyn');
        $('.lb-vectorlab-bg').innerHTML = gridBg(view, s, ox, oy, H);
        const P = (x, y) => [ox + x * s, oy - y * s];
        const eff = () => V.map((v, i) => i > 0 && op === 'sub' ? { x: -v.x, y: -v.y } : v); // vectors actually added
        function tails() { // tail position (world) of each drawn vector
          const e = eff(); const t = [];
          let cx = 0, cy = 0;
          V.forEach((v, i) => { if (law === 'parallelogram' || i === 0) t.push({ x: 0, y: 0 }); else { t.push({ x: cx, y: cy }); } cx += e[i].x; cy += e[i].y; });
          return t;
        }
        function draw() {
          const e = eff(), T = tails();
          const Rx = e.reduce((a, v) => a + v.x, 0), Ry = e.reduce((a, v) => a + v.y, 0), R = Math.hypot(Rx, Ry);
          let g = '';
          const tt = tTip(), [tx, ty] = P(tt.x, tt.y);
          g += `<line x1="${ox}" y1="${oy}" x2="${tx}" y2="${ty}" stroke="#8b5cf6" stroke-width="2.5" stroke-dasharray="3 6" stroke-linecap="round" opacity=".7"/><text x="${tx}" y="${ty + 6}" font-size="19" text-anchor="middle">⭐</text>`;
          if (law === 'parallelogram' && two) {
            const [ax, ay] = P(e[0].x, e[0].y), [bx, by] = P(e[1].x, e[1].y), [rx, ry] = P(Rx, Ry);
            g += `<path d="M${ox} ${oy}L${ax} ${ay}L${rx} ${ry}L${bx} ${by}Z" fill="#8b5cf6" fill-opacity=".06"/>`;
            g += `<line x1="${ax}" y1="${ay}" x2="${rx}" y2="${ry}" stroke="${V[1].col}" stroke-width="2" stroke-dasharray="5 5"/><line x1="${bx}" y1="${by}" x2="${rx}" y2="${ry}" stroke="${V[0].col}" stroke-width="2" stroke-dasharray="5 5"/>`;
            if (op === 'sub') { const [qx, qy] = P(V[1].x, V[1].y); g += arrow(ox, oy, qx, qy, V[1].col, 2.5, 'opacity=".35"'); }
          }
          if (two && law === 'triangle' && op === 'sub') { const [qx, qy] = P(V[1].x, V[1].y); g += arrow(ox, oy, qx, qy, V[1].col, 2.5, 'opacity=".35"') + txt(qx + 10, qy, esc(V[1].label), V[1].col, 11, 'start', 'opacity=".6"'); }
          // angle θ between A and B (both from the tail)
          if (two) {
            const a1 = Math.atan2(e[0].y, e[0].x), a2 = Math.atan2(e[1].y, e[1].x);
            let dA = a2 - a1; while (dA > Math.PI) dA -= 2 * Math.PI; while (dA < -Math.PI) dA += 2 * Math.PI;
            if (law === 'parallelogram' && Math.hypot(e[0].x, e[0].y) > 0 && Math.hypot(e[1].x, e[1].y) > 0 && Math.abs(dA) > 0.05) {
              const r = 22, sx = ox + r * Math.cos(a1), sy = oy - r * Math.sin(a1), ex2 = ox + r * Math.cos(a1 + dA), ey2 = oy - r * Math.sin(a1 + dA);
              g += `<path d="M${sx} ${sy}A${r} ${r} 0 0 ${dA > 0 ? 0 : 1} ${ex2} ${ey2}" fill="none" stroke="#ffc93c" stroke-width="3"/>`;
              const mid = a1 + dA / 2; g += txt(ox + 34 * Math.cos(mid), oy - 34 * Math.sin(mid) + 4, 'θ', '#b8860b', 12);
            }
          }
          const [rx, ry] = P(Rx, Ry);
          g += arrow(ox, oy, rx, ry, '#8b5cf6', 5);
          if (R > 0.4) g += txt((ox + rx) / 2 + (Ry >= 0 ? 10 : -10) * (Rx >= 0 ? 1 : -1), (oy + ry) / 2 - 6, 'R', '#5b33c9', 13);
          V.forEach((v, i) => {
            const t = T[i], [x1, y1] = P(t.x, t.y), [x2, y2] = P(t.x + e[i].x, t.y + e[i].y);
            g += arrow(x1, y1, x2, y2, v.col, 4);
            const nx = -(y2 - y1), ny = x2 - x1, nl = Math.hypot(nx, ny) || 1;
            g += txt((x1 + x2) / 2 + nx / nl * 11, (y1 + y2) / 2 + ny / nl * 11 + 4, (i > 0 && op === 'sub' ? '−' : '') + esc(v.label), v.col, 12.5);
            if (!v.fixed) g += `<circle cx="${x2}" cy="${y2}" r="16" fill="${v.col}" fill-opacity=".16"/><circle cx="${x2}" cy="${y2}" r="6" fill="#fff" stroke="${v.col}" stroke-width="3"/>`;
          });
          dyn.innerHTML = g;
          V.forEach((v, i) => out('m' + i, fmt(Math.hypot(v.x, v.y)) + U));
          out('R', fmt(R) + U);
          const dirR = R > 1e-9 ? dirAngle(Rx, Ry) : 0;
          if (two) {
            const A = Math.hypot(e[0].x, e[0].y), B = Math.hypot(e[1].x, e[1].y);
            const th = A && B ? deg(Math.acos(clamp((e[0].x * e[1].x + e[0].y * e[1].y) / (A * B), -1, 1))) : 0;
            out('th', fmt(th, 1) + '°');
            const alpha = A + B * Math.cos(rad(th)) === 0 && B * Math.sin(rad(th)) === 0 ? 0 : deg(Math.atan2(B * Math.sin(rad(th)), A + B * Math.cos(rad(th))));
            out('f', `R = √(A² + B² + 2AB cos θ) = √(${fmt(A * A)} + ${fmt(B * B)} + ${fmt(2 * A * B * Math.cos(rad(th)))}) = <b>${fmt(R)}</b>${U}<br>tan α = B sin θ / (A + B cos θ) → α = <b>${fmt(alpha, 1)}°</b> from ${esc(V[0].label)} · R at <b>${fmt(dirR, 1)}°</b> to x`);
          } else out('f', `R = (${fmt(Rx)}, ${fmt(Ry)}) · |R| = √(Rₓ² + Rᵧ²) = <b>${fmt(R)}</b>${U} at <b>${fmt(dirR, 1)}°</b> to x`);
          host.querySelectorAll('[data-law]').forEach(b => b.classList.toggle('on', b.dataset.law === law));
          if (touched && !won) {
            const ok = target.R != null
              ? Math.abs(R - target.R) <= Math.max(0.02 * target.R, 0.12) && Math.abs(((dirR - ((target.theta % 360) + 360) % 360) + 540) % 360 - 180) <= 2.5
              : Math.abs(Rx - target.x) < 1e-6 && Math.abs(Ry - target.y) < 1e-6;
            if (ok) { msg(`✔ R = ${fmt(R)}${unit ? ' ' + unit : ''} at ${fmt(dirR, 1)}°`); win(`Resultant ${Rname} = ${fmt(R)}${unit ? ' ' + unit : ''} at ${fmt(dirR, 1)}° to the x-axis — R = √(A² + B² + 2AB cos θ)`); }
          }
        }
        let dragI = -1;
        dragOn(svg, H, pt => {
          const e = eff(), T = tails(); let best = -1, bd = 34;
          V.forEach((v, i) => { if (v.fixed) return; const [hx, hy] = P(T[i].x + e[i].x, T[i].y + e[i].y); const d = Math.hypot(pt.x - hx, pt.y - hy); if (d < bd) { bd = d; best = i; } });
          dragI = best; return best >= 0;
        }, pt => {
          const T = tails(), t = T[dragI];
          let wx = (pt.x - ox) / s, wy = (oy - pt.y) / s;
          wx = clamp(wx, view[0], view[1]); wy = clamp(wy, view[2], view[3]);
          let vx = clean(Math.round((wx - t.x) / snap) * snap), vy = clean(Math.round((wy - t.y) / snap) * snap);
          if (dragI > 0 && op === 'sub') { vx = -vx; vy = -vy; }
          if (vx === V[dragI].x && vy === V[dragI].y) return;
          V[dragI].x = vx; V[dragI].y = vy; draw();
        });
        on(host, 'click', e => {
          const l = e.target.closest('[data-law]'); if (l) { law = l.dataset.law; api.sfx('tap'); draw(); return; }
          const b = e.target.closest('[data-act]');
          if (b) {
            for (let k = 0; k < 50; k++) {
              const x = Math.round((view[0] + 1 + Math.random() * (view[1] - view[0] - 2)) / snap) * snap, y = Math.round((view[2] + 1 + Math.random() * (view[3] - view[2] - 2)) / snap) * snap;
              if (Math.hypot(x, y) >= 2.5) { target = { x: clean(x), y: clean(y) }; break; }
            }
            newRound(genText()); msg(''); draw();
          }
        });
        draw();
        msg('Drag the ○ heads of the vectors');
        return cleanup;
      }

      // =============== resolve ===============
      function resolveMode() {
        const H = 240, s = 30, ox = 180, oy = 125;
        const rot = isFinite(+p.axisAngle) ? clamp(+p.axisAngle, -80, 80) : 0;
        const v0 = p.vector || {};
        const label = esc(v0.label != null ? v0.label : 'A');
        // polar state relative to the x′ axis
        let mag = Math.hypot(+v0.x || 3, +v0.y || 2), ang = dirAngle(isFinite(+v0.x) ? +v0.x : 3, isFinite(+v0.y) ? +v0.y : 2) - rot;
        mag = Math.round(mag * 2) / 2; ang = Math.round(ang / 5) * 5;
        const tg = p.target || {};
        let target = (isFinite(+tg.x) || isFinite(+tg.y)) ? { x: isFinite(+tg.x) ? +tg.x : null, y: isFinite(+tg.y) ? +tg.y : null } : isFinite(+tg.R) && isFinite(+tg.theta) ? { R: +tg.R, theta: +tg.theta } : { x: 4.33, y: 2.5 };
        const xs = rot ? 'x′' : 'x', ys = rot ? 'y′' : 'y';
        const genText = () => target.R != null ? `Make ${label} = ${fmt(target.R)}${unit ? ' ' + unit : ''} at θ = ${fmt(target.theta, 1)}° to the ${xs}-axis and read off its components.` : `Drag ${label} so that ${target.x != null ? `${label}${xs === 'x' ? 'ₓ' : 'ₓ′'} = ${fmt(target.x)}` : ''}${target.x != null && target.y != null ? ' and ' : ''}${target.y != null ? `${label}${ys === 'y' ? 'ᵧ' : 'ᵧ′'} = ${fmt(target.y)}` : ''}${unit ? ' ' + unit : ''}.`;
        shell(H, `<div class="lb-vectorlab-chips"><div class="lb-vectorlab-chip" style="background:#f3edff;color:#5b33c9">|${label}| = <b data-o="m"></b></div><div class="lb-vectorlab-chip" style="background:#fff5d6;color:#9a6a00">θ = <b data-o="th"></b></div><div class="lb-vectorlab-chip" style="background:#e0ecff;color:#2f6fd6">${label}<sub>${xs}</sub> = <b data-o="ax"></b></div><div class="lb-vectorlab-chip" style="background:#ffe9e9;color:#d64545">${label}<sub>${ys}</sub> = <b data-o="ay"></b></div></div>
<div class="lb-vectorlab-f" data-o="f"></div><div class="lb-vectorlab-row"><button class="lb-vectorlab-b" data-act="new">New challenge</button></div>`);
        setCh(p.challenge || genText());
        const svg = $('.lb-vectorlab-svg'), dyn = $('.lb-vectorlab-dyn');
        $('.lb-vectorlab-bg').innerHTML = gridBg([-6, 6, -4, 4], s, ox, oy, H, rot);
        const ex = [Math.cos(rad(rot)), -Math.sin(rad(rot))], ey = [-Math.sin(rad(rot)), -Math.cos(rad(rot))]; // screen unit vectors of x′ and y′ (x′ turned +90°)
        function draw() {
          const ax = mag * Math.cos(rad(ang)), ay = mag * Math.sin(rad(ang));
          const hx = ox + (ax * ex[0] + ay * ey[0]) * s, hy = oy + (ax * ex[1] + ay * ey[1]) * s;
          const px = ox + ax * ex[0] * s, py = oy + ax * ex[1] * s, qx = ox + ay * ey[0] * s, qy = oy + ay * ey[1] * s;
          let g = `<line x1="${hx}" y1="${hy}" x2="${px}" y2="${py}" stroke="#6b7090" stroke-width="1.5" stroke-dasharray="4 4"/><line x1="${hx}" y1="${hy}" x2="${qx}" y2="${qy}" stroke="#6b7090" stroke-width="1.5" stroke-dasharray="4 4"/>`;
          g += arrow(ox, oy, px, py, '#3b82f6', 4.5) + arrow(ox, oy, qx, qy, '#ff6b6b', 4.5);
          if (Math.abs(ax) > 0.3) g += txt((ox + px) / 2 - ey[0] * (ay >= 0 ? 12 : -12), (oy + py) / 2 - ey[1] * (ay >= 0 ? 12 : -12) + 4, `${label}${rot ? 'ₓ′' : 'ₓ'}`, '#2f6fd6', 12);
          if (Math.abs(ay) > 0.3) g += txt((ox + qx) / 2 - ex[0] * (ax >= 0 ? 14 : -14), (oy + qy) / 2 - ex[1] * (ax >= 0 ? 14 : -14) + 4, `${label}${rot ? 'ᵧ′' : 'ᵧ'}`, '#d64545', 12);
          const a0 = -rad(rot), a1 = -rad(rot + ang); const r = 24;
          if (Math.abs(ang) > 2) { let sweep = ang > 0 ? 0 : 1; g += `<path d="M${ox + r * Math.cos(a0)} ${oy + r * Math.sin(a0)}A${r} ${r} 0 ${Math.abs(ang) > 180 ? 1 : 0} ${sweep} ${ox + r * Math.cos(a1)} ${oy + r * Math.sin(a1)}" fill="none" stroke="#ffc93c" stroke-width="3"/>`; const m = -rad(rot + ang / 2); g += txt(ox + 36 * Math.cos(m), oy + 36 * Math.sin(m) + 4, 'θ', '#b8860b', 12); }
          g += arrow(ox, oy, hx, hy, '#8b5cf6', 5) + txt(hx + (hx > ox ? 12 : -12), hy - 8, label, '#5b33c9', 13);
          g += `<circle cx="${hx}" cy="${hy}" r="17" fill="#8b5cf6" fill-opacity=".16"/><circle cx="${hx}" cy="${hy}" r="6" fill="#fff" stroke="#8b5cf6" stroke-width="3"/>`;
          dyn.innerHTML = g;
          const A = clean(ax), B = clean(ay);
          out('m', fmt(mag) + U); out('th', fmt(ang, 0) + '°'); out('ax', fmt(A) + U); out('ay', fmt(B) + U);
          out('f', `${label}<sub>${xs}</sub> = ${label} cos θ = ${fmt(mag)} × ${fmt(Math.cos(rad(ang)), 3)} = <b>${fmt(A)}</b> · ${label}<sub>${ys}</sub> = ${label} sin θ = <b>${fmt(B)}</b><br>Check: √(${label}<sub>${xs}</sub>² + ${label}<sub>${ys}</sub>²) = <b>${fmt(Math.hypot(A, B))}</b>${U}`);
          if (touched && !won) {
            const ok = target.R != null ? Math.abs(mag - target.R) < 1e-6 && Math.abs((((ang - target.theta) % 360) + 540) % 360 - 180) < 1e-6
              : (target.x == null || Math.abs(A - target.x) <= 0.011) && (target.y == null || Math.abs(B - target.y) <= 0.011);
            if (ok) { msg(`✔ ${label} = ${fmt(mag)} at ${fmt(ang, 0)}°`); win(`${label} = ${fmt(mag)}${unit ? ' ' + unit : ''} at ${fmt(ang, 0)}°: ${label}${xs === 'x' ? 'ₓ' : 'ₓ′'} = ${label} cos θ = ${fmt(A)}, ${label}${ys === 'y' ? 'ᵧ' : 'ᵧ′'} = ${label} sin θ = ${fmt(B)}`); }
          }
        }
        dragOn(svg, H, () => true, pt => {
          const dx = pt.x - ox, dy = pt.y - oy;
          const lx = dx * ex[0] + dy * ex[1], ly = dx * ey[0] + dy * ey[1]; // components along x′, y′ (px)
          let m = Math.round(Math.hypot(lx, ly) / s * 2) / 2; m = clamp(m, 0.5, 7);
          let a = Math.round(deg(Math.atan2(ly, lx)) / 5) * 5; if (a < 0) a += 360; if (a >= 360) a -= 360;
          if (m !== mag || a !== ang) { mag = m; ang = a; draw(); }
        });
        on(host, 'click', e => {
          if (!e.target.closest('[data-act]')) return;
          const R = 2 + Math.round(Math.random() * 4) / 2, th = [15, 30, 45, 60, 120, 135, 150, 210, 240, 300, 330][Math.floor(Math.random() * 11)];
          target = { x: clean(+(R * Math.cos(rad(th))).toFixed(2)), y: clean(+(R * Math.sin(rad(th))).toFixed(2)) };
          newRound(genText()); msg(''); draw();
        });
        draw(); msg('Drag the head of ' + label + ' (it clicks every 0.5 and 5°)');
        return cleanup;
      }

      // =============== incline ===============
      function inclineMode() {
        const H = 230, m = +p.mass > 0 ? +p.mass : 2, g0 = +p.g > 0 ? +p.g : 10, Wt = m * g0;
        let phi = isFinite(+p.angle) ? clamp(Math.round(+p.angle), 0, 70) : 20;
        const tg = p.target || {};
        let target = isFinite(+tg.along) ? { along: +tg.along } : isFinite(+tg.perp) ? { perp: +tg.perp } : { along: Wt / 2 };
        const genText = () => target.along != null ? `Tilt the incline so that the component of the weight along it, mg sin φ, is ${fmt(target.along)} N.` : `Tilt the incline so that the normal component mg cos φ is ${fmt(target.perp)} N.`;
        shell(H, `<div class="lb-vectorlab-chips"><div class="lb-vectorlab-chip" style="background:#f3edff;color:#5b33c9">mg = <b>${fmt(Wt)} N</b></div><div class="lb-vectorlab-chip" style="background:#e0ecff;color:#2f6fd6">mg sin φ = <b data-o="al"></b></div><div class="lb-vectorlab-chip" style="background:#ffe9e9;color:#d64545">mg cos φ = <b data-o="pe"></b></div></div>
<div class="lb-vectorlab-f" data-o="f"></div>${slider('phi', 'φ =', 0, 70, 1, phi)}`);
        setCh(p.challenge || genText());
        const dyn = $('.lb-vectorlab-dyn');
        function draw() {
          const c = Math.cos(rad(phi)), sn = Math.sin(rad(phi));
          const Ax = 24, Ay = 172; // bottom-left corner of the wedge (px)
          const base = phi > 0 ? Math.min(310, 150 / Math.tan(rad(phi))) : 310, top = base * Math.tan(rad(phi));
          let g = `<rect x="0" y="${Ay}" width="${W}" height="${H - Ay}" fill="#e9f8f2"/><line x1="0" y1="${Ay}" x2="${W}" y2="${Ay}" stroke="#2ea37f" stroke-width="2"/><path d="M${Ax} ${Ay}L${Ax + base} ${Ay}L${Ax + base} ${Ay - top}Z" fill="#ffe7b0" stroke="#d4a43a" stroke-width="2" stroke-linejoin="round"/>`;
          if (phi > 1) g += `<path d="M${Ax + 46} ${Ay}A46 46 0 0 0 ${Ax + 46 * c} ${Ay - 46 * sn}" fill="none" stroke="#b8860b" stroke-width="2.5"/>` + txt(Ax + 52, Ay + 15, `φ = ${phi}°`, '#9a6a00', 12, 'start');
          // block at 55% along the incline
          const bx = Ax + 0.55 * base, by = Ay - 0.55 * top, bw = 46, bh = 30;
          const nX = -sn, nY = -c; // outward normal (screen)
          const cx = bx + nX * bh / 2, cy = by + nY * bh / 2;
          const blk = `<g transform="translate(${cx} ${cy}) rotate(${-phi})"><rect x="${-bw / 2}" y="${-bh / 2}" width="${bw}" height="${bh}" rx="6" fill="#8b5cf6" stroke="#5b33c9" stroke-width="2"/><text y="5" font-size="12" font-weight="900" fill="#fff" text-anchor="middle">${fmt(m)} kg</text></g>`;
          const k = Math.min(80, H - 8 - cy) / Wt; // px per N for the weight arrow
          const wx = cx, wy = cy + Wt * k;
          const al = Wt * sn, pe = Wt * c;
          const ax = cx - c * al * k, ay = cy + sn * al * k; // along: down the slope (towards the bottom-left)
          const px = cx + sn * pe * k, py = cy + c * pe * k;  // into the surface
          g += `<line x1="${wx}" y1="${wy}" x2="${ax}" y2="${ay}" stroke="#6b7090" stroke-dasharray="4 4"/><line x1="${wx}" y1="${wy}" x2="${px}" y2="${py}" stroke="#6b7090" stroke-dasharray="4 4"/>`;
          g += arrow(cx, cy, wx, wy, '#1b1f3a', 4.5) + txt(wx - 8, wy + 2, 'mg', '#1b1f3a', 12, 'end');
          if (al * k > 6) g += arrow(cx, cy, ax, ay, '#3b82f6', 4) + txt(ax - 6, ay - 8, 'mg sin φ', '#2f6fd6', 11, 'end');
          if (pe * k > 6) g += arrow(cx, cy, px, py, '#ff6b6b', 4) + txt(px + 8, py + 4, 'mg cos φ', '#d64545', 11, 'start');
                    dyn.innerHTML = g + blk.replace('fill="#8b5cf6"', 'fill="#8b5cf6" fill-opacity=".88"');
          out('phi', phi + '°'); out('al', fmt(al) + ' N'); out('pe', fmt(pe) + ' N');
          out('f', `mg sin φ = ${fmt(Wt)} × sin ${phi}° = <b>${fmt(al)} N</b> (down the slope) · mg cos φ = <b>${fmt(pe)} N</b> (into the surface)`);
          if (touched && !won) {
            const v = target.along != null ? al : pe, t = target.along != null ? target.along : target.perp;
            if (Math.abs(v - t) <= Math.max(0.005 * Wt, 0.01)) { msg(`✔ φ = ${phi}°`); win(`At φ = ${phi}°: mg sin φ = ${fmt(al)} N along the incline and mg cos φ = ${fmt(pe)} N into it (mg = ${fmt(Wt)} N)`); }
          }
        }
        const sl = host.querySelector('input[data-k="phi"]');
        on(sl, 'input', () => { touched = true; phi = +sl.value; draw(); });
        draw(); msg('Slide φ to tilt the incline');
        return cleanup;
      }

      // =============== projectile ===============
      function projectile() {
        const H = 222, g0 = +p.g > 0 ? +p.g : 9.8, h0 = +p.h0 > 0 ? +p.h0 : 0;
        const ur = arr2(p.speedRange, [5, 30]), ar = arr2(p.angleRange, h0 > 0 ? [0, 85] : [5, 85]);
        let u = clamp(isFinite(+p.speed) ? +p.speed : 20, ur[0], ur[1]), th = clamp(isFinite(+p.angle) ? +p.angle : 30, ar[0], ar[1]);
        const tg = p.target || {};
        let target = isFinite(+tg.range) ? { range: +tg.range, both: !!tg.both } : isFinite(+tg.height) ? { height: +tg.height } : Array.isArray(tg.hit) && tg.hit.length === 2 ? { hit: tg.hit.map(Number) } : null;
        if (!target) target = { range: h0 > 0 ? Math.round(flight(ur[1] * 0.6, 30).R) : 30, both: h0 === 0 };
        const hits = []; // angles that achieved the range
        function flight(u, th) {
          const vx = u * Math.cos(rad(th)), vy = u * Math.sin(rad(th));
          const T = (vy + Math.sqrt(vy * vy + 2 * g0 * h0)) / g0;
          return { vx, vy, T, R: vx * T, H: h0 + vy * vy / (2 * g0) };
        }
        // world window with equal scales
        let xMax = 1, yMax = 1;
        for (let a = ar[0]; a <= ar[1]; a += 1) { const f = flight(ur[1], a); xMax = Math.max(xMax, f.R); yMax = Math.max(yMax, f.H); }
        if (target.range) xMax = Math.max(xMax, target.range * 1.1);
        if (target.hit) { xMax = Math.max(xMax, target.hit[0] * 1.1); yMax = Math.max(yMax, target.hit[1] * 1.1); }
        if (target.height) yMax = Math.max(yMax, target.height * 1.1);
        const GX = 16, GY = H - 22, s = Math.min((W - GX - 12) / xMax, (GY - 18) / yMax);
        const P = (x, y) => [GX + x * s, GY - y * s];
        const genText = () => target.range != null ? (target.both ? `Hit the flag at ${fmt(target.range, 1)} m with TWO different launch angles.` : `Land the ball on the flag at ${fmt(target.range, 1)} m.`) : target.height != null ? `Launch so the ball rises to a maximum height of exactly ${fmt(target.height, 1)} m.` : `Send the ball through the ring at (${fmt(target.hit[0], 1)} m, ${fmt(target.hit[1], 1)} m).`;
        shell(H, `<div class="lb-vectorlab-chips"><div class="lb-vectorlab-chip" style="background:#e0ecff;color:#2f6fd6">T = <b data-o="T"></b></div><div class="lb-vectorlab-chip" style="background:#ffe9e9;color:#d64545">H = <b data-o="H"></b></div><div class="lb-vectorlab-chip" style="background:#d9f7ee;color:#0f7a5c">R = <b data-o="R"></b></div></div>
<div class="lb-vectorlab-f" data-o="f"></div>
<div class="lb-vectorlab-row" style="gap:8px"><div style="flex:1">${slider('u', 'u =', ur[0], ur[1], 0.5, u)}${slider('th', 'θ =', ar[0], ar[1], 1, th)}</div><button class="lb-vectorlab-b go" data-act="go" style="flex:0 0 84px;min-height:58px;font-size:15px">🚀 Launch</button></div>`);
        setCh(p.challenge || genText());
        const dyn = $('.lb-vectorlab-dyn');
        // background: ground, distance ticks, cliff
        let bg = `<rect x="0" y="${GY}" width="${W}" height="${H - GY}" fill="#dff5e9"/><line x1="0" y1="${GY}" x2="${W}" y2="${GY}" stroke="#2ea37f" stroke-width="2"/>`;
        const step = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500].find(v => v * s >= 42) || 1000;
        for (let x = 0; GX + x * s < W - 6; x += step) bg += `<line x1="${GX + x * s}" y1="${GY}" x2="${GX + x * s}" y2="${GY + 5}" stroke="#2ea37f" stroke-width="1.5"/>` + txt(GX + x * s, GY + 16, x + (x === 0 ? '' : ''), '#3d7f68', 9.5);
        bg += txt(W - 6, GY + 16, 'm', '#3d7f68', 9.5, 'end');
        if (h0 > 0) bg += `<rect x="0" y="${GY - h0 * s}" width="${GX}" height="${h0 * s}" fill="#c9b18a" stroke="#9c845d"/>` + txt(GX + 4, GY - h0 * s / 2, `h = ${fmt(h0)} m`, '#7a6440', 10, 'start');
        $('.lb-vectorlab-bg').innerHTML = bg;
        const trails = [];
        let fly = null; // {t0, f, u, th}
        function trajPath(f, uu, tt, upto) {
          let d = ''; const n = 80;
          for (let i = 0; i <= n; i++) { const t = upto * i / n, x = f.vx * t, y = h0 + f.vy * t - 0.5 * g0 * t * t; const [px, py] = P(x, Math.max(0, y)); d += (i ? 'L' : 'M') + px.toFixed(1) + ' ' + py.toFixed(1); }
          return d;
        }
        function goalSvg() {
          if (target.range != null) { const [fx, fy] = P(target.range, 0); return `<line x1="${fx}" y1="${fy}" x2="${fx}" y2="${fy - 30}" stroke="#1b1f3a" stroke-width="2"/><path d="M${fx} ${fy - 30}L${fx + 18} ${fy - 24}L${fx} ${fy - 18}Z" fill="#ff6b6b"/><ellipse cx="${fx}" cy="${fy}" rx="${Math.max(5, Math.max(0.5, target.range * 0.015) * s)}" ry="3" fill="#ff6b6b" opacity=".5"/>`; }
          if (target.height != null) { const [, hy] = P(0, target.height); return `<line x1="0" y1="${hy}" x2="${W}" y2="${hy}" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="6 5"/>` + txt(W - 6, hy - 4, `${fmt(target.height, 1)} m`, '#d64545', 10.5, 'end'); }
          const [hx, hy] = P(target.hit[0], target.hit[1]); return `<circle cx="${hx}" cy="${hy}" r="10" fill="none" stroke="#ff6b6b" stroke-width="4"/><circle cx="${hx}" cy="${hy}" r="10" fill="none" stroke="#ffc93c" stroke-width="1.5" stroke-dasharray="3 3"/>`;
        }
        function draw(now) {
          const f = flight(u, th);
          let g = goalSvg();
          trails.forEach((t, i) => { g += `<path d="${t}" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="2 4" opacity="${0.25 + 0.15 * i}"/>`; });
          const [lx, ly] = P(0, h0);
          // launcher
          g += `<g transform="translate(${lx} ${ly}) rotate(${-th})"><rect x="-4" y="-6" width="34" height="12" rx="5" fill="#1b1f3a"/></g><circle cx="${lx}" cy="${ly}" r="8" fill="#6b7090"/>`;
          if (!fly) {
            const ar0 = 24; g += `<path d="M${lx + ar0 + 14} ${ly}A${ar0 + 14} ${ar0 + 14} 0 0 0 ${lx + (ar0 + 14) * Math.cos(rad(th))} ${ly - (ar0 + 14) * Math.sin(rad(th))}" fill="none" stroke="#ffc93c" stroke-width="2.5"/>` + txt(lx + 48 * Math.cos(rad(th / 2)) + 6, ly - 48 * Math.sin(rad(th / 2)) + 4, 'θ', '#b8860b', 12);
            g += arrow(lx, ly, lx + u * 2.2 * Math.cos(rad(th)), ly - u * 2.2 * Math.sin(rad(th)), '#8b5cf6', 3) + txt(lx + u * 2.2 * Math.cos(rad(th)) + 8, ly - u * 2.2 * Math.sin(rad(th)) - 2, 'u', '#5b33c9', 12, 'start');
          } else {
            const dur = clamp(fly.f.T, 1.2, 3) * 1000, t = Math.min(fly.f.T, (now - fly.t0) / dur * fly.f.T);
            const x = fly.f.vx * t, y = h0 + fly.f.vy * t - 0.5 * g0 * t * t, vy = fly.f.vy - g0 * t;
            g += `<path d="${trajPath(fly.f, fly.u, fly.th, t)}" fill="none" stroke="#8b5cf6" stroke-width="3" stroke-linecap="round"/>`;
            const [bx, by] = P(x, Math.max(0, y)), k = 1.8;
            g += arrow(bx, by, bx + fly.f.vx * k, by, '#3b82f6', 3) + arrow(bx, by, bx, by - vy * k, '#ff6b6b', 3);
            g += `<circle cx="${bx}" cy="${by}" r="7" fill="#ffc93c" stroke="#1b1f3a" stroke-width="2"/>`;
            g += txt(bx + fly.f.vx * k + 4, by + 4, `vₓ ${fmt(fly.f.vx, 1)}`, '#2f6fd6', 10, 'start') + txt(bx + 6, by - vy * k + (vy > 0 ? -2 : 12), `vᵧ ${fmt(vy, 1)}`, '#d64545', 10, 'start');
            if (t >= fly.f.T) land(fly);
          }
          dyn.innerHTML = g;
          out('u', fmt(u, 1) + ' m/s'); out('th', fmt(th, 0) + '°');
          out('T', fmt(f.T) + ' s'); out('H', fmt(f.H) + ' m'); out('R', fmt(f.R) + ' m');
          out('f', h0 > 0 ? `From height h: y = h + u sin θ·t − ½gt² → T = <b>${fmt(f.T)} s</b>, R = u cos θ·T = <b>${fmt(f.R)} m</b> (g = ${fmt(g0)} m/s²)`
            : `R = u² sin 2θ / g = ${fmt(u * u)} × ${fmt(Math.sin(rad(2 * th)), 3)} / ${fmt(g0)} · H = u² sin²θ / 2g · T = 2u sin θ / g`);
        }
        function land(fl) {
          trails.push(trajPath(fl.f, fl.u, fl.th, fl.f.T)); if (trails.length > 3) trails.shift();
          fly = null; host.querySelector('[data-act="go"]').disabled = false;
          const f = fl.f;
          if (won) return draw(0);
          if (target.range != null) {
            const tol = Math.max(0.5, target.range * 0.015);
            if (Math.abs(f.R - target.range) <= tol) {
              api.sfx('coin');
              if (!target.both) { msg(`✔ R = ${fmt(f.R)} m`); win(`u = ${fmt(fl.u, 1)} m/s at ${fl.th}° gives R = u² sin 2θ / g = ${fmt(f.R)} m`); }
              else {
                const h = hits.find(h => Math.abs(h.th - fl.th) >= 3 && h.u === fl.u);
                hits.push({ th: fl.th, u: fl.u });
                if (!h) msg(`🎯 Hit at θ = ${fl.th}°! Keep u = ${fmt(fl.u, 1)} m/s and find a different angle`);
                else { msg(`✔ ${h.th}° and ${fl.th}° both hit`); win(`Both θ = ${h.th}° and θ = ${fl.th}° land at ${fmt(target.range, 1)} m — sin 2θ = sin (180° − 2θ), so θ and (90° − θ) give the same range for the same u`); }
              }
            } else msg(f.R < target.range ? `Short by ${fmt(target.range - f.R, 1)} m` : `Too far by ${fmt(f.R - target.range, 1)} m`);
          } else if (target.height != null) {
            if (Math.abs(f.H - target.height) <= Math.max(0.1, target.height * 0.015)) { msg(`✔ H = ${fmt(f.H)} m`); win(`H = u² sin²θ / 2g = ${fmt(f.H)} m with u = ${fmt(fl.u, 1)} m/s, θ = ${fl.th}°`); }
            else msg(`H = ${fmt(f.H, 1)} m — ${f.H < target.height ? 'higher!' : 'lower!'}`);
          } else {
            let best = 1e9; for (let i = 0; i <= 400; i++) { const t = f.T * i / 400; best = Math.min(best, Math.hypot(f.vx * t - target.hit[0], h0 + f.vy * t - 0.5 * g0 * t * t - target.hit[1])); }
            if (best <= Math.max(0.4, xMax * 0.012)) { msg('✔ Through the ring!'); win(`Through the ring at (${fmt(target.hit[0], 1)}, ${fmt(target.hit[1], 1)}) m with u = ${fmt(fl.u, 1)} m/s, θ = ${fl.th}°`); }
            else msg(`Missed the ring by ${fmt(best, 1)} m`);
          }
          draw(0);
        }
        const loop = now => { draw(now); if (fly) raf = requestAnimationFrame(loop); };
        on(host, 'input', e => { const k = e.target.dataset && e.target.dataset.k; if (!k) return; touched = true; if (k === 'u') u = +e.target.value; else th = +e.target.value; if (!fly) draw(0); });
        on(host, 'click', e => {
          const b = e.target.closest('[data-act="go"]'); if (!b || fly) return;
          touched = true; b.disabled = true; api.sfx('tap');
          fly = { t0: performance.now(), f: flight(u, th), u, th }; raf = requestAnimationFrame(loop);
        });
        draw(0); msg('Set u and θ, then Launch');
        return cleanup;
      }

      // =============== relative: rain ===============
      function rain() {
        const H = 230, vr = +p.rain > 0 ? +p.rain : 6, wind = isFinite(+p.wind) ? +p.wind : 0;
        const wr = arr2(p.walkRange, [0, 10]);
        let vm = clamp(isFinite(+p.walk) ? +p.walk : 0, wr[0], wr[1]), um = 0;
        const tg = p.target || {};
        let target = isFinite(+tg.walk) ? { walk: +tg.walk } : isFinite(+tg.angle) ? { angle: +tg.angle } : { walk: 4 };
        const appAngle = v => deg(Math.atan2(v - wind, vr)); // + = rain comes from in front (tilt umbrella forward)
        const genText = () => target.walk != null ? `Walk at ${fmt(target.walk, 1)} m/s through rain falling at ${fmt(vr, 1)} m/s${wind ? ` (wind ${fmt(wind, 1)} m/s)` : ''}. Tilt the umbrella to stay dry.` : `How fast must you walk so that the rain appears to fall at ${fmt(target.angle, 0)}° to the vertical? Tilt the umbrella to match.`;
        shell(H, `<div class="lb-vectorlab-chips"><div class="lb-vectorlab-chip" style="background:#e0ecff;color:#2f6fd6">v<sub>r</sub> = <b>${fmt(vr, 1)} m/s ↓</b></div><div class="lb-vectorlab-chip" style="background:#ffe9e9;color:#d64545">v<sub>m</sub> = <b data-o="vm2"></b></div><div class="lb-vectorlab-chip" style="background:#f3edff;color:#5b33c9">|v<sub>rm</sub>| = <b data-o="vrm"></b></div></div>
<div class="lb-vectorlab-f" data-o="f"></div>${slider('vm', 'walk v<sub>m</sub> =', wr[0], wr[1], 0.5, vm)}${slider('um', 'umbrella', -60, 60, 1, um)}`);
        setCh(p.challenge || genText());
        const svg = $('.lb-vectorlab-svg'), dyn = $('.lb-vectorlab-dyn');
        $('.lb-vectorlab-bg').innerHTML = `<rect x="0" y="0" width="200" height="${H}" fill="#eaf2ff"/><rect x="0" y="${H - 26}" width="200" height="26" fill="#cfe9dc"/><line x1="200" y1="0" x2="200" y2="${H}" stroke="#e6e8f7" stroke-width="2"/>` + txt(280, 18, 'velocity triangle', '#6b7090', 11);
        const drops = Array.from({ length: 34 }, () => ({ x: Math.random() * 200, y: Math.random() * H }));
        let last = performance.now();
        const HX = 100, HY = 120; // hand position
        function draw(now) {
          const dt = Math.min(0.05, (now - last) / 1000); last = now;
          const rx = wind - vm, ry = vr; // rain velocity relative to man (x: + forward, y: down)
          const k = 22; // px per (m/s) for drops
          let g = '';
          drops.forEach(d => { d.x += rx * k * dt; d.y += ry * k * dt; if (d.y > H - 26) { d.y -= H - 26; d.x = Math.random() * 230 - 15; } if (d.x < -15) d.x += 230; if (d.x > 215) d.x -= 230; const L = 11 / Math.hypot(rx, ry); g += `<line x1="${d.x}" y1="${d.y}" x2="${d.x - rx * L}" y2="${d.y - ry * L}" stroke="#3b82f6" stroke-width="1.8" stroke-linecap="round" opacity=".6"/>`; });
          // man (facing right = walking direction)
          const sw = vm > 0 ? Math.sin(now / 1000 * (3 + vm)) * 10 : 0;
          g += `<g stroke="#1b1f3a" stroke-width="4" stroke-linecap="round" fill="none"><line x1="92" y1="150" x2="${92 - sw}" y2="${H - 28}"/><line x1="92" y1="150" x2="${92 + sw}" y2="${H - 28}"/><line x1="92" y1="112" x2="92" y2="150"/><line x1="92" y1="122" x2="${HX}" y2="${HY + 8}"/></g><circle cx="92" cy="101" r="10" fill="#ffd8b0" stroke="#1b1f3a" stroke-width="2.5"/>`;
          // umbrella: shaft from hand along tilt um (+ = forward)
          const ux = Math.sin(rad(um)), uy = -Math.cos(rad(um));
          const tx = HX + ux * 52, ty = HY + uy * 52;
          g += `<line x1="${HX}" y1="${HY + 10}" x2="${tx}" y2="${ty}" stroke="#1b1f3a" stroke-width="3"/>`;
          g += `<g transform="translate(${tx} ${ty}) rotate(${um})"><path d="M-46 12 Q0 -26 46 12 Q34 6 23 12 Q11 6 0 12 Q-11 6 -23 12 Q-34 6 -46 12Z" fill="#ff6b6b" stroke="#d64545" stroke-width="2"/></g>`;
          g += `<circle cx="${HX}" cy="${HY + 10}" r="18" fill="#8b5cf6" fill-opacity=".12"/>`;
          g += txt(170, H - 9, 'walk →', '#3d7f68', 11, 'middle');
          // velocity triangle (right panel): v_r down, −v_m, v_rm
          const s2 = Math.min(11, 150 / Math.max(vr, 1), 70 / Math.max(1, Math.abs(wind - vm), Math.abs(wind) + 0.1));
          const ox = 285 - (wind - vm) * s2 / 2, oy = 40;
          const ax = ox + wind * s2, ay = oy + vr * s2, bx = ax - vm * s2, by = ay;
          g += arrow(ox, oy, ax, ay, '#3b82f6', 4) + txt(ox + wind * s2 / 2 - 10, oy + vr * s2 / 2, 'v<tspan font-size="9" dy="3">r</tspan>', '#2f6fd6', 13, 'end');
          if (Math.abs(vm) * s2 > 2) g += arrow(ax, ay, bx, by, '#ff6b6b', 4) + txt((ax + bx) / 2, ay + 17, '−v<tspan font-size="9" dy="3">m</tspan>', '#d64545', 13);
          g += arrow(ox, oy, bx, by, '#8b5cf6', 4.5);
          const A = appAngle(vm);
          if (Math.abs(A) > 0.5) { g += `<path d="M${ox} ${oy + 30}A30 30 0 0 ${A > 0 ? 1 : 0} ${ox - 30 * Math.sin(rad(A))} ${oy + 30 * Math.cos(rad(A))}" fill="none" stroke="#ffc93c" stroke-width="2.5"/>`; }
          g += txt((ox + bx) / 2 + (A > 0 ? -12 : 12), (oy + by) / 2 + 22, 'v<tspan font-size="9" dy="3">rm</tspan>', '#5b33c9', 13, A > 0 ? 'end' : 'start');
          g += txt(285, H - 10, `θ = ${fmt(Math.abs(A), 1)}° ${Math.abs(A) < 0.05 ? '' : A > 0 ? 'from front' : 'from behind'}`, '#9a6a00', 11.5);
          dyn.innerHTML = g;
          const rel = Math.hypot(wind - vm, vr);
          out('vm', fmt(vm, 1) + ' m/s'); out('vm2', fmt(vm, 1) + ' m/s →'); out('um', (um > 0 ? um + '° fwd' : um < 0 ? -um + '° back' : '0°'));
          out('vrm', fmt(rel) + ' m/s');
          out('f', `v<sub>rm</sub> = v<sub>r</sub> − v<sub>m</sub> · tan θ = ${wind ? '(v<sub>m</sub> − wind)' : 'v<sub>m</sub>'} / v<sub>r</sub> = ${fmt(vm - wind, 1)} / ${fmt(vr, 1)} → θ = <b>${fmt(Math.abs(A), 1)}°</b> · umbrella ${Math.abs(um - A) <= 1.5 ? '<b style="color:#0f7a5c">✔ dry</b>' : '<b style="color:#d64545">getting wet</b>'}`);
          if (touched && !won) {
            const okWalk = target.walk != null ? Math.abs(vm - target.walk) < 1e-9 : Math.abs(Math.abs(A) - target.angle) <= 1;
            if (okWalk && Math.abs(um - A) <= 1.5) { msg('✔ Dry!'); win(`Walking at ${fmt(vm, 1)} m/s, the rain hits you at θ = tan⁻¹(${fmt(vm - wind, 1)} / ${fmt(vr, 1)}) = ${fmt(Math.abs(A), 1)}° from the vertical — tilt the umbrella ${A >= 0 ? 'forward' : 'backward'} by that angle`); }
            else if (okWalk && target.walk != null) msg(`Right speed! Now tilt the umbrella (rain arrives at ${fmt(Math.abs(A), 1)}°)`);
          }
          raf = requestAnimationFrame(draw);
        }
        on(host, 'input', e => { const k = e.target.dataset && e.target.dataset.k; if (!k) return; touched = true; if (k === 'vm') vm = +e.target.value; else um = +e.target.value; });
        dragOn(svg, H, pt => pt.x < 200 && pt.y < HY + 40, pt => { um = clamp(Math.round(deg(Math.atan2(pt.x - HX, HY - pt.y))), -60, 60); host.querySelector('input[data-k="um"]').value = um; });
        raf = requestAnimationFrame(draw);
        msg('Walk faster and tilt the umbrella (slider or drag)');
        return cleanup;
      }

      // =============== relative: river ===============
      function river() {
        const H = 236, u = isFinite(+p.river) ? Math.max(0, +p.river) : 3, d = +p.width > 0 ? +p.width : 100;
        const br = arr2(p.boatRange, [1, 10]);
        let v = clamp(isFinite(+p.boat) ? +p.boat : 5, br[0], br[1]), al = clamp(isFinite(+p.heading) ? Math.round(+p.heading) : 0, -80, 80);
        const tg = p.target || {};
        let target = isFinite(+tg.drift) ? { drift: +tg.drift } : tg.time === 'min' ? { time: 'min' } : isFinite(+tg.land) ? { land: +tg.land } : (u < br[1] ? { drift: 0 } : { time: 'min' });
        const genText = () => target.drift != null ? (target.drift === 0 ? `Steer the boat (river ${fmt(u, 1)} m/s) so it reaches the point directly opposite.` : `Land ${fmt(target.drift, 1)} m downstream.`) : target.time === 'min' ? `Cross the ${fmt(d, 0)} m river in the shortest possible time.` : `Land exactly ${fmt(target.land, 1)} m downstream of the start.`;
        shell(H, `<div class="lb-vectorlab-chips"><div class="lb-vectorlab-chip" style="background:#e0ecff;color:#2f6fd6">t = <b data-o="t"></b></div><div class="lb-vectorlab-chip" style="background:#ffe9e9;color:#d64545">drift = <b data-o="dr"></b></div><div class="lb-vectorlab-chip" style="background:#f3edff;color:#5b33c9">|v<sub>R</sub>| = <b data-o="vR"></b></div></div>
<div class="lb-vectorlab-f" data-o="f"></div>
<div class="lb-vectorlab-row" style="gap:8px"><div style="flex:1">${slider('v', 'boat v =', br[0], br[1], 0.5, v)}${slider('al', 'heading α =', -80, 80, 1, al)}</div><button class="lb-vectorlab-b go" data-act="go" style="flex:0 0 72px;min-height:58px;font-size:15px">⛵ Go</button></div>`);
        setCh(p.challenge || genText());
        const dyn = $('.lb-vectorlab-dyn');
        const BT = 34, BB = H - 34, SX = 150; // banks and start x
        const s = (BB - BT) / d;
        let bg = `<rect x="0" y="0" width="${W}" height="${BT}" fill="#dff5e9"/><rect x="0" y="${BB}" width="${W}" height="${H - BB}" fill="#dff5e9"/><rect x="0" y="${BT}" width="${W}" height="${BB - BT}" fill="#cfe6ff"/>`;
        bg += `<line x1="${SX}" y1="${BT}" x2="${SX}" y2="${BB}" stroke="#6b7090" stroke-dasharray="3 5"/>` + txt(SX, BT - 18, 'B (opposite)', '#3d7f68', 10) + `<circle cx="${SX}" cy="${BT}" r="4" fill="#3d7f68"/>` + txt(SX, H - 10, 'start A', '#3d7f68', 10) + txt(W - 6, (BT + BB) / 2 - 20, `d = ${fmt(d, 0)} m`, '#2f6fd6', 10.5, 'end');
        $('.lb-vectorlab-bg').innerHTML = bg;
        let go = null, flowT = 0, last = performance.now();
        const calc = () => { const vy = v * Math.cos(rad(al)), vx = u - v * Math.sin(rad(al)); const t = d / vy; return { vx, vy, t, drift: vx * t, vR: Math.hypot(vx, vy) }; };
        function draw(now) {
          const dt = Math.min(0.05, (now - last) / 1000); last = now; flowT += dt;
          const c = calc();
          let g = '';
          for (let i = 0; i < 4; i++) for (let j = 0; j < 5; j++) { const x = ((j * 90 + flowT * u * 14 + i * 37) % 450) - 45, y = BT + 22 + i * (BB - BT - 30) / 3; g += `<path d="M${x} ${y}q8 -5 16 0t16 0" fill="none" stroke="#7fb3f0" stroke-width="2" stroke-linecap="round"/>`; }
          if (target.land != null || (target.drift != null && target.drift !== 0)) { const tx = SX + (target.land != null ? target.land : target.drift) * s; g += `<line x1="${tx}" y1="${BT - 14}" x2="${tx}" y2="${BT}" stroke="#1b1f3a" stroke-width="2"/><path d="M${tx} ${BT - 14}l14 4l-14 4Z" fill="#ff6b6b"/>`; }
          else if (target.drift === 0) g += `<path d="M${SX} ${BT - 14}l14 4l-14 4Z" fill="#ff6b6b"/><line x1="${SX}" y1="${BT - 14}" x2="${SX}" y2="${BT}" stroke="#1b1f3a" stroke-width="2"/>`;
          const ex = SX + c.drift * s;
          g += `<line x1="${SX}" y1="${BB}" x2="${ex}" y2="${BT}" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="5 5" opacity="${go ? 0.9 : 0.35}"/>`;
          // boat
          let bx = SX, by = BB;
          if (go) { const tt = Math.min(go.c.t, (now - go.t0) / go.dur * go.c.t); bx = SX + go.c.vx * tt * s; by = BB - go.c.vy * tt * s; if (tt >= go.c.t) finish(); }
          const k = 9;
          if (!go) {
            g += arrow(SX, BB, SX - v * Math.sin(rad(al)) * k, BB - v * Math.cos(rad(al)) * k, '#3b82f6', 3.5) + txt(SX - v * Math.sin(rad(al)) * k - 8, BB - v * Math.cos(rad(al)) * k, 'v', '#2f6fd6', 12, 'end');
            g += arrow(SX - v * Math.sin(rad(al)) * k, BB - v * Math.cos(rad(al)) * k, SX + c.vx * k, BB - c.vy * k, '#ff6b6b', 3.5) + txt((SX - v * Math.sin(rad(al)) * k + SX + c.vx * k) / 2, BB - c.vy * k - 7, 'u', '#d64545', 12);
            g += arrow(SX, BB, SX + c.vx * k, BB - c.vy * k, '#8b5cf6', 4) + txt(SX + c.vx * k + 8, BB - c.vy * k + 14, 'v<tspan font-size="9" dy="3">R</tspan>', '#5b33c9', 12, 'start');
          }
          g += `<g transform="translate(${bx} ${by}) rotate(${-al})"><path d="M0 -15 Q9 -4 7 12 L-7 12 Q-9 -4 0 -15Z" fill="#ffc93c" stroke="#b8860b" stroke-width="2"/></g>`;
          if (Math.abs(al) > 0.5 && !go) g += txt(SX + (al > 0 ? 20 : -20), BB + 16, `α = ${Math.abs(al)}° ${al > 0 ? 'upstream' : 'downstream'}`, '#9a6a00', 10.5, al > 0 ? 'start' : 'end');
          g += txt(26, BT + 16, `u = ${fmt(u, 1)} m/s →`, '#2f6fd6', 10.5, 'start');
          dyn.innerHTML = g;
          out('v', fmt(v, 1) + ' m/s'); out('al', al + '°'); out('t', fmt(c.t, 1) + ' s'); out('dr', fmt(c.drift, 1) + ' m'); out('vR', fmt(c.vR) + ' m/s');
          out('f', `t = d / (v cos α) = ${fmt(d, 0)} / ${fmt(c.vy)} = <b>${fmt(c.t, 1)} s</b> · drift = (u − v sin α)·t = <b>${fmt(c.drift, 1)} m</b>`);
          raf = requestAnimationFrame(draw);
        }
        function finish() {
          const c = go.c, a0 = go.al; go = null; host.querySelector('[data-act="go"]').disabled = false;
          if (won) return;
          const tol = Math.max(0.5, d * 0.01);
          let ok = false, why = '';
          if (target.time === 'min') { ok = a0 === 0; why = ok ? `Heading straight across gives the least time t = d / v = ${fmt(c.t, 1)} s (drift ${fmt(c.drift, 1)} m)` : 'Not the fastest — which heading uses all of v to cross?'; }
          else { const want = target.land != null ? target.land : target.drift; ok = Math.abs(c.drift - want) <= tol; why = ok ? (want === 0 ? `sin α = u / v = ${fmt(u, 1)} / ${fmt(v, 1)} → α ≈ ${a0}° upstream; t = ${fmt(c.t, 1)} s` : `Landed ${fmt(c.drift, 1)} m downstream in ${fmt(c.t, 1)} s`) : `Landed ${fmt(c.drift, 1)} m ${c.drift >= 0 ? 'downstream' : 'upstream'} — try again`; }
          msg((ok ? '✔ ' : '') + why);
          if (ok) win(why); else api.sfx('hmm');
        }
        on(host, 'input', e => { const k = e.target.dataset && e.target.dataset.k; if (!k || go) return; touched = true; if (k === 'v') v = +e.target.value; else al = +e.target.value; });
        on(host, 'click', e => { const b = e.target.closest('[data-act="go"]'); if (!b || go) return; const c = calc(); if (!(c.vy > 0)) return; touched = true; b.disabled = true; api.sfx('tap'); go = { t0: performance.now(), c, al, dur: 2200 }; });
        raf = requestAnimationFrame(draw);
        msg('Set the boat speed and heading, then Go');
        return cleanup;
      }
    },
    example: { mode: 'add', unit: 'N', vectors: [{ x: 3, y: 0, label: 'A', fixed: true }, { x: 1, y: 2, label: 'B' }], law: 'parallelogram', target: { R: 5, theta: 36.87 }, challenge: 'A force A = 3 N acts along x. Drag force B so that the resultant is 5 N at 36.9° to the x-axis.' },
    examples: [
      { mode: 'projectile', speed: 20, angle: 30, speedRange: [5, 30], g: 9.8, target: { range: 30, both: true }, challenge: 'Hit the flag at 30 m with TWO different launch angles (keep u the same).' },
      { mode: 'relative', scene: 'rain', rain: 6, target: { walk: 4 }, challenge: 'बारिश 6 m/s से सीधी नीचे गिर रही है। 4 m/s से चलते हुए छाता कितने कोण पर झुकाएँ?' },
      { mode: 'resolve', incline: true, mass: 2, g: 10, angle: 15, target: { along: 10 }, challenge: 'A 2 kg block rests on an incline (g = 10 m/s²). Tilt it so that the pull down the slope, mg sin φ, is 10 N.' }
    ]
  });
})();
