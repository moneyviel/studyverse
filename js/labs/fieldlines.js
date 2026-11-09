/* Knowtopia Concept Lab: fieldlines — electric charges, field lines, equipotentials, dipoles and Gauss's law
 * (Class 12 Physics ch. 1–2). k = 1/(4πε₀) = 9 × 10⁹ N m² C⁻², ε₀ = 8.854 × 10⁻¹² C² N⁻¹ m⁻².
 *
 * mode 'field'  : point charges on a 30 cm × 20 cm board (1 grid square = 1 cm). Drag charges (they snap to
 *                 1 cm), add + / − charges, change their size, and drag the probe P (or tap anywhere to move it).
 *                 Field lines (number ∝ |q|) and equipotentials (V = 0 in violet) are drawn live; E (magnitude and
 *                 direction) and V at P are shown: E = Σ kq/r² (vector sum), V = Σ kq/r.
 *                 P "clicks" onto a null point (E = 0) or the V = 0 line when the challenge asks for it.
 * mode 'dipole' : a dipole (±q, separation 2a) in a uniform field E. Drag it to turn it; see the forces ±qE,
 *                 torque τ = pE sin θ and potential energy U = −pE cos θ. Tap Release to watch it swing.
 * mode 'gauss'  : draw any closed curve (Gaussian surface) round some charges with your finger. Charges inside
 *                 glow; Φ = q_enc / ε₀ (charges outside add nothing).
 *
 * PARAMS (all optional)
 *   mode        'field' | 'dipole' | 'gauss'                                                   default 'field'
 *   charges     [{x, y, q, fixed}]   x, y in cm from the centre (x −14…14, y −9…9), q in units of `unit`
 *               default field: [{x:-4,y:0,q:1},{x:4,y:0,q:4}];  gauss: [{x:-8,y:3,q:2},{x:-4,y:-3,q:-1},{x:5,y:3,q:3},{x:9,y:-3,q:-2}]
 *   unit        'μC' | 'nC'   charge unit                                                         default 'μC'
 *   probe       [x, y]   start of the probe P in cm                                                default [0, 4]
 *   editable    boolean  field mode: show add / resize / delete buttons                           default true
 *   lines, equip boolean  start with field lines / equipotentials on                               default true, true
 *   q, a        dipole: charge (in `unit`) and half-separation a (cm)                              default 2, 2
 *   E0          dipole: uniform field in N/C                                                        default 1e5
 *   angle       dipole: starting angle θ between p and E (degrees)                                  default 30
 * Challenge (one target; if none is given a sensible one is generated):
 *   target      field:  {zeroE:true} find the null point | {zeroV:true} find a point with V = 0 |
 *                       {E:value} (N/C) or {V:value} (volts) at P
 *               dipole: {torque:'max'} | {torque:value} (N m) | {U:'min'|'max'} | {angle:deg}
 *               gauss:  {qenc:value} enclose this net charge (in `unit`) | {flux:0} zero net flux with charges inside
 *   challenge   string   challenge sentence (may be Hindi); else generated
 *   winText     string   optional win message
 */
(function () {
  const K = 9e9, EPS0 = 8.854e-12;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const minus = s => String(s).replace(/-/g, '−');
  const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
  function sci(v, sig = 3) {
    if (!isFinite(v)) return '—';
    if (v === 0) return '0';
    const e = Math.floor(Math.log10(Math.abs(v)));
    if (e >= -2 && e < 4) return minus(+v.toPrecision(sig));
    let m = +(v / Math.pow(10, e)).toPrecision(sig), ee = e;
    if (Math.abs(m) >= 10) { m /= 10; ee++; }
    return minus(m) + ' × 10' + String(ee).split('').map(c => SUP[c]).join('');
  }
  const fmt = (v, dp = 1) => { let s = (+(+v).toFixed(dp)).toString(); if (s === '-0') s = '0'; return minus(s); };
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const deg = r => r * 180 / Math.PI, rad = d => d * Math.PI / 180;
  const sinD = d => { const t = ((d % 360) + 360) % 360; return t === 0 || t === 180 ? 0 : Math.sin(rad(d)); };
  const cosD = d => { const t = ((d % 360) + 360) % 360; return t === 90 || t === 270 ? 0 : Math.cos(rad(d)); };

  Labs.register('fieldlines', {
    title: 'Electric field lab',
    subjects: ['physics'],
    render(host, p, api) {
      const mode = ['field', 'dipole', 'gauss'].includes(p.mode) ? p.mode : 'field';
      const unit = p.unit === 'nC' ? 'nC' : 'μC', UC = unit === 'nC' ? 1e-9 : 1e-6;
      const W = 360, H = 240, PX = 12, OX = W / 2, OY = H / 2; // 12 px per cm
      let won = false, touched = false, raf = 0, customRound = false, dirty = true;
      const listeners = [];
      const on = (el, ev, fn, o) => { el.addEventListener(ev, fn, o); listeners.push([el, ev, fn, o]); };
      const css = `
.lb-fieldlines-w{font-size:13.5px;color:#1b1f3a}
.lb-fieldlines-ch{font-weight:800;font-size:14px;margin-bottom:5px;line-height:1.3}
.lb-fieldlines-cv{width:100%;height:auto;display:block;border-radius:16px;border:1.5px solid #e6e8f7;touch-action:none;user-select:none;-webkit-user-select:none;box-sizing:border-box;background:#fbfbff}
.lb-fieldlines-chips{display:flex;flex-wrap:wrap;gap:4px;margin-top:5px}
.lb-fieldlines-chip{flex:1 1 auto;border-radius:10px;padding:3px 6px;font-weight:800;font-size:12.5px;text-align:center;background:#f1f2fb;white-space:nowrap}
.lb-fieldlines-chip b{font-size:13.5px}
.lb-fieldlines-f{margin-top:4px;background:#f6f4ff;border-radius:11px;padding:4px 8px;font-weight:700;font-size:12.5px;line-height:1.4;text-align:center}
.lb-fieldlines-f b{color:#5b33c9}
.lb-fieldlines-row{display:flex;gap:5px;margin-top:5px}
.lb-fieldlines-b{flex:1;min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 4px;white-space:nowrap}
.lb-fieldlines-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-fieldlines-b.pos{color:#e04848}.lb-fieldlines-b.neg{color:#2f6fd6}
.lb-fieldlines-b.go{background:#2ed3a5;color:#08372a;box-shadow:0 3px 0 #1ea383}
.lb-fieldlines-b:active{transform:translateY(2px)}
.lb-fieldlines-b:disabled{opacity:.45}
.lb-fieldlines-msg{font-size:12.5px;font-weight:700;color:#6b7090;margin-top:4px;min-height:16px;text-align:center;line-height:1.3}`;
      function shell(controls) {
        host.innerHTML = `<style>${css}</style><div class="lb-fieldlines-w"><div class="lb-fieldlines-ch">🎯 Challenge: <span class="lb-fieldlines-cht"></span></div><canvas class="lb-fieldlines-cv"></canvas>${controls}<div class="lb-fieldlines-msg"></div></div>`;
      }
      const $ = s => host.querySelector(s);
      const setCh = t => { $('.lb-fieldlines-cht').textContent = t; };
      const msg = t => { $('.lb-fieldlines-msg').innerHTML = t; };
      const out = (k, v) => { const el = host.querySelector(`[data-o="${k}"]`); if (el) el.innerHTML = v; };
      function win(t) { if (won) return; won = true; api.sfx('correct'); api.win(p.winText && !customRound ? p.winText : t); }
      let cv, ctx;
      function setupCanvas() {
        cv = $('.lb-fieldlines-cv'); const dpr = Math.min(3, window.devicePixelRatio || 1);
        cv.width = W * dpr; cv.height = H * dpr; ctx = cv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      }
      const ptr = e => { const r = cv.getBoundingClientRect(); return { x: (e.clientX - r.left) * W / r.width, y: (e.clientY - r.top) * H / r.height }; };
      function dragOn(start, move, end) {
        let dr = false;
        on(cv, 'pointerdown', e => { const pt = ptr(e); dr = start(pt) !== false; if (dr) { touched = true; cv.setPointerCapture && cv.setPointerCapture(e.pointerId); move(pt); e.preventDefault(); } });
        on(cv, 'pointermove', e => { if (dr) move(ptr(e)); });
        const up = () => { if (dr) { dr = false; end && end(); } };
        on(cv, 'pointerup', up); on(cv, 'pointercancel', up);
      }
      const cleanup = () => { cancelAnimationFrame(raf); listeners.forEach(([el, ev, fn, o]) => el.removeEventListener(ev, fn, o)); };
      const loop = fn => { const f = () => { fn(); raf = requestAnimationFrame(f); }; raf = requestAnimationFrame(f); };

      function grid() {
        ctx.fillStyle = '#fbfbff'; ctx.fillRect(0, 0, W, H);
        ctx.lineWidth = 1;
        for (let i = -15; i <= 15; i++) { ctx.strokeStyle = i === 0 ? '#dfe2f5' : i % 5 ? '#f1f2fb' : '#e6e8f7'; ctx.beginPath(); ctx.moveTo(OX + i * PX + 0.5, 0); ctx.lineTo(OX + i * PX + 0.5, H); ctx.stroke(); }
        for (let i = -10; i <= 10; i++) { ctx.strokeStyle = i === 0 ? '#dfe2f5' : i % 5 ? '#f1f2fb' : '#e6e8f7'; ctx.beginPath(); ctx.moveTo(0, OY + i * PX + 0.5); ctx.lineTo(W, OY + i * PX + 0.5); ctx.stroke(); }
        ctx.fillStyle = '#a3a8c3'; ctx.font = '700 9.5px Nunito, sans-serif'; ctx.textAlign = 'right'; ctx.fillText('1 square = 1 cm', W - 6, H - 6);
      }
      function arrowHead(x, y, ang, size, col) {
        ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(x + Math.cos(ang) * size, y + Math.sin(ang) * size);
        ctx.lineTo(x + Math.cos(ang + 2.5) * size * 0.8, y + Math.sin(ang + 2.5) * size * 0.8); ctx.lineTo(x + Math.cos(ang - 2.5) * size * 0.8, y + Math.sin(ang - 2.5) * size * 0.8); ctx.closePath(); ctx.fill();
      }
      function arrow(x1, y1, x2, y2, col, w = 3) {
        const L = Math.hypot(x2 - x1, y2 - y1); if (L < 2) return; const a = Math.atan2(y2 - y1, x2 - x1), hl = Math.min(11, L * 0.5);
        ctx.strokeStyle = col; ctx.lineWidth = w; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2 - Math.cos(a) * hl * 0.6, y2 - Math.sin(a) * hl * 0.6); ctx.stroke();
        arrowHead(x2 - Math.cos(a) * hl * 0.35, y2 - Math.sin(a) * hl * 0.35, a, hl, col);
      }
      function label(t, x, y, col, size = 12, align = 'center') {
        ctx.font = `900 ${size}px Nunito, sans-serif`; ctx.textAlign = align; ctx.lineWidth = 3.5; ctx.strokeStyle = 'rgba(255,255,255,.95)'; ctx.lineJoin = 'round'; ctx.strokeText(t, x, y); ctx.fillStyle = col; ctx.fillText(t, x, y);
      }
      function drawCharge(c, glow) {
        const x = OX + c.x * PX, y = OY - c.y * PX, pos = c.q > 0, r = 11 + Math.min(5, Math.abs(c.q));
        if (glow) { ctx.fillStyle = 'rgba(255,201,60,.45)'; ctx.beginPath(); ctx.arc(x, y, r + 9, 0, 7); ctx.fill(); }
        const gr = ctx.createRadialGradient(x - r * 0.35, y - r * 0.35, 2, x, y, r);
        gr.addColorStop(0, pos ? '#ffb3b3' : '#b9d4ff'); gr.addColorStop(1, pos ? '#ff5252' : '#2f6fd6');
        ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
        ctx.lineWidth = c.sel ? 3.5 : 2; ctx.strokeStyle = c.sel ? '#ffc93c' : '#fff'; ctx.stroke();
        ctx.fillStyle = '#fff'; ctx.font = '900 16px Nunito, sans-serif'; ctx.textAlign = 'center'; ctx.fillText(pos ? '+' : '−', x, y + 5.5);
        label(`${pos ? '+' : '−'}${+Math.abs(c.q).toFixed(2)} ${unit}`, x, y + r + 12, pos ? '#d64545' : '#2f6fd6', 10.5);
        if (c.fixed) { ctx.fillStyle = '#6b7090'; ctx.font = '10px sans-serif'; ctx.fillText('📌', x + r - 2, y - r + 4); }
      }
      // physics (positions in px → metres)
      const toM = px => px / PX / 100;
      function fieldAt(Q, x, y) { // x,y in px; returns E (N/C) components in screen axes (y down) and V
        let ex = 0, ey = 0, v = 0;
        for (const c of Q) { const dx = toM(x - (OX + c.x * PX)), dy = toM(y - (OY - c.y * PX)), r2 = dx * dx + dy * dy, r = Math.sqrt(r2); if (r < 1e-9) return { ex: NaN, ey: NaN, v: NaN }; const kq = K * c.q * UC; ex += kq * dx / (r2 * r); ey += kq * dy / (r2 * r); v += kq / r; }
        return { ex, ey, v };
      }
      function traceLines(Q) {
        const lines = [];
        const total = Q.reduce((a, c) => Math.max(a, Math.abs(c.q)), 0) || 1, L = Math.min(8, 24 / total);
        const dir = (x, y, sgn) => { const f = fieldAt(Q, x, y); const m = Math.hypot(f.ex, f.ey); return m > 0 && isFinite(m) ? [sgn * f.ex / m, sgn * f.ey / m] : null; };
        const pxQ = Q.map(c => ({ x: OX + c.x * PX, y: OY - c.y * PX, q: c.q }));
        const run = (c, sgn) => {
          const n = Math.max(3, Math.round(L * Math.abs(c.q)));
          for (let i = 0; i < n; i++) {
            const a = (i + 0.5) / n * 2 * Math.PI; let x = c.x + Math.cos(a) * 11, y = c.y + Math.sin(a) * 11;
            const pts = [[x, y]]; let endQ = null;
            for (let s = 0; s < 500; s++) {
              const d1 = dir(x, y, sgn); if (!d1) break;
              const d2 = dir(x + d1[0] * 1.6, y + d1[1] * 1.6, sgn); if (!d2) break;
              x += d2[0] * 3.2; y += d2[1] * 3.2; pts.push([x, y]);
              if (x < -30 || x > W + 30 || y < -30 || y > H + 30) break;
              const hit = pxQ.find(o => o !== c && Math.hypot(o.x - x, o.y - y) < 9); if (hit) { endQ = hit; break; }
            }
            lines.push({ pts, sgn, endQ });
          }
        };
        pxQ.filter(c => c.q > 0).forEach(c => run(c, 1));
        pxQ.filter(c => c.q < 0).forEach(c => { const before = lines.length; run(c, -1); for (let i = lines.length - 1; i >= before; i--) if (lines[i].endQ && lines[i].endQ.q > 0) lines.splice(i, 1); });
        return lines;
      }
      function drawLines(lines) {
        ctx.lineWidth = 1.6; ctx.strokeStyle = 'rgba(139,92,246,.62)'; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        for (const l of lines) {
          ctx.beginPath(); l.pts.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.stroke();
          const k = Math.min(l.pts.length - 2, 14); if (k > 1) { const [x1, y1] = l.pts[k], [x0, y0] = l.pts[k - 1]; let a = Math.atan2(y1 - y0, x1 - x0); if (l.sgn < 0) a += Math.PI; arrowHead(x1, y1, a, 6, 'rgba(110,60,230,.85)'); }
        }
      }
      function drawEquip(Q) {
        const st = 4, nx = W / st + 1, ny = H / st + 1, V = new Float64Array(nx * ny);
        for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) V[j * nx + i] = fieldAt(Q, i * st + 0.01, j * st + 0.013).v;
        const qm = Q.reduce((a, c) => Math.max(a, Math.abs(c.q)), 0); if (!qm) return;
        const levels = [];
        [1.5, 2.5, 4, 6.5, 10].forEach(rc => { const v = K * qm * UC / (rc / 100); levels.push(v, -v); });
        if (Q.some(c => c.q > 0) && Q.some(c => c.q < 0)) levels.push(0);
        for (const lv of levels) {
          ctx.strokeStyle = lv === 0 ? 'rgba(139,92,246,.95)' : lv > 0 ? 'rgba(255,107,107,.55)' : 'rgba(59,130,246,.55)';
          ctx.lineWidth = lv === 0 ? 2.2 : 1.4; ctx.setLineDash(lv === 0 ? [6, 4] : [3, 3]); ctx.beginPath();
          for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
            const a = V[j * nx + i], b = V[j * nx + i + 1], c = V[(j + 1) * nx + i + 1], d = V[(j + 1) * nx + i];
            if (![a, b, c, d].every(isFinite)) continue;
            const pts = [], x = i * st, y = j * st;
            const e = (v1, v2, x1, y1, x2, y2) => { if ((v1 - lv) * (v2 - lv) < 0) { const t = (lv - v1) / (v2 - v1); pts.push([x1 + (x2 - x1) * t, y1 + (y2 - y1) * t]); } };
            e(a, b, x, y, x + st, y); e(b, c, x + st, y, x + st, y + st); e(c, d, x + st, y + st, x, y + st); e(d, a, x, y + st, x, y);
            if (pts.length >= 2) { ctx.moveTo(pts[0][0], pts[0][1]); ctx.lineTo(pts[1][0], pts[1][1]); }
            if (pts.length === 4) { ctx.moveTo(pts[2][0], pts[2][1]); ctx.lineTo(pts[3][0], pts[3][1]); }
          }
          ctx.stroke();
        }
        ctx.setLineDash([]);
      }

      if (mode === 'dipole') return dipole();
      if (mode === 'gauss') return gauss();
      return field();

      // ================= field =================
      function field() {
        const src = Array.isArray(p.charges) && p.charges.length ? p.charges : [{ x: -4, y: 0, q: 1 }, { x: 4, y: 0, q: 4 }];
        const Q = src.slice(0, 6).filter(c => isFinite(+c.q) && +c.q !== 0).map(c => ({ x: clamp(Math.round(+c.x || 0), -14, 14), y: clamp(Math.round(+c.y || 0), -9, 9), q: +c.q, fixed: !!c.fixed, sel: false }));
        const editable = p.editable !== false;
        let showL = p.lines !== false, showE = p.equip !== false;
        const pr = Array.isArray(p.probe) && p.probe.length === 2 ? p.probe.map(Number) : [0, 4];
        let P = { x: OX + clamp(pr[0], -14, 14) * PX, y: OY - clamp(pr[1], -9, 9) * PX };
        const tg = p.target || {};
        let target = tg.zeroE ? 'zeroE' : tg.zeroV ? 'zeroV' : isFinite(+tg.E) ? 'E' : isFinite(+tg.V) ? 'V' : null;
        let tval = target === 'E' ? +tg.E : target === 'V' ? +tg.V : 0;
        if (!target) { const mixed = Q.some(c => c.q > 0) && Q.some(c => c.q < 0); target = mixed ? 'zeroV' : 'zeroE'; }
        const genText = () => target === 'zeroE' ? 'Move the probe P to the neutral point, where the net electric field E = 0.' : target === 'zeroV' ? 'Move the probe P to a point where the electric potential V = 0.' : target === 'E' ? `Find a point where the field has magnitude E = ${sci(tval, 2)} N/C.` : `Find a point where the potential is V = ${sci(tval, 2)} V.`;
        shell(`<div class="lb-fieldlines-chips"><div class="lb-fieldlines-chip" style="background:#f3edff;color:#5b33c9">E = <b data-o="E"></b></div><div class="lb-fieldlines-chip" style="background:#fff5d6;color:#9a6a00">V = <b data-o="V"></b></div></div>
${editable ? `<div class="lb-fieldlines-row"><button class="lb-fieldlines-b pos" data-a="addp">+ charge</button><button class="lb-fieldlines-b neg" data-a="addn">− charge</button><button class="lb-fieldlines-b" data-a="up">q ▲</button><button class="lb-fieldlines-b" data-a="dn">q ▼</button><button class="lb-fieldlines-b" data-a="del">🗑</button></div>` : ''}
<div class="lb-fieldlines-row"><button class="lb-fieldlines-b" data-a="lines">Field lines</button><button class="lb-fieldlines-b" data-a="equip">Equipotentials</button></div>`);
        setCh(p.challenge || genText());
        setupCanvas();
        let lines = [], sel = null;
        function nullNear(x, y) { // Newton on E = 0 starting at (x, y), px
          for (let it = 0; it < 40; it++) {
            const h = 0.05, f = fieldAt(Q, x, y), fx1 = fieldAt(Q, x + h, y), fy1 = fieldAt(Q, x, y + h);
            const a = (fx1.ex - f.ex) / h, b = (fy1.ex - f.ex) / h, c = (fx1.ey - f.ey) / h, d = (fy1.ey - f.ey) / h, det = a * d - b * c;
            if (!isFinite(det) || det === 0) return null;
            const dx = (d * f.ex - b * f.ey) / det, dy = (-c * f.ex + a * f.ey) / det;
            x -= clamp(dx, -6, 6); y -= clamp(dy, -6, 6);
            if (Math.hypot(dx, dy) < 1e-7) return { x, y };
          }
          return null;
        }
        function zeroVNear(x, y) {
          for (let it = 0; it < 30; it++) {
            const h = 0.05, f = fieldAt(Q, x, y), gx = (fieldAt(Q, x + h, y).v - f.v) / h, gy = (fieldAt(Q, x, y + h).v - f.v) / h, g2 = gx * gx + gy * gy;
            if (!isFinite(g2) || g2 === 0) return null;
            const dx = f.v * gx / g2, dy = f.v * gy / g2; x -= clamp(dx, -6, 6); y -= clamp(dy, -6, 6);
            if (Math.hypot(dx, dy) < 1e-7) return { x, y };
          }
          return null;
        }
        const scaleE = () => { let m = 0; for (const c of Q) { const r = toM(Math.hypot(P.x - (OX + c.x * PX), P.y - (OY - c.y * PX))); m = Math.max(m, K * Math.abs(c.q) * UC / (r * r)); } return m; };
        const scaleV = () => { let m = 0; for (const c of Q) { const r = toM(Math.hypot(P.x - (OX + c.x * PX), P.y - (OY - c.y * PX))); m = Math.max(m, K * Math.abs(c.q) * UC / r); } return m; };
        let snapped = false;
        function placeProbe(x, y) {
          x = clamp(x, 4, W - 4); y = clamp(y, 4, H - 4);
          snapped = false;
          if (target === 'zeroE' || target === 'zeroV') {
            const r = target === 'zeroE' ? nullNear(x, y) : zeroVNear(x, y);
            if (r && Math.hypot(r.x - x, r.y - y) < 13 && r.x > 0 && r.x < W && r.y > 0 && r.y < H && Q.every(c => Math.hypot(r.x - (OX + c.x * PX), r.y - (OY - c.y * PX)) > 14)) { x = r.x; y = r.y; snapped = true; }
          }
          if (!snapped) { x = Math.round(x / 3) * 3; y = Math.round(y / 3) * 3; }
          if (Q.some(c => Math.hypot(x - (OX + c.x * PX), y - (OY - c.y * PX)) < 6)) return;
          P = { x, y };
        }
        function draw() {
          if (dirty) { lines = showL ? traceLines(Q) : []; dirty = false; }
          grid();
          if (showE) drawEquip(Q);
          if (showL) drawLines(lines);
          Q.forEach(c => drawCharge(c));
          const f = fieldAt(Q, P.x, P.y), E = Math.hypot(f.ex, f.ey);
          // probe
          ctx.fillStyle = 'rgba(255,201,60,.25)'; ctx.beginPath(); ctx.arc(P.x, P.y, 17, 0, 7); ctx.fill();
          const Es = scaleE(), zeroE = snapped && target === 'zeroE';
          if (!zeroE && E > 0 && isFinite(E)) { const L = clamp(14 + 16 * Math.log10(1 + 9 * E / (Es || 1)), 16, 46); arrow(P.x, P.y, P.x + f.ex / E * L, P.y + f.ey / E * L, '#1b1f3a', 3); }
          ctx.fillStyle = '#ffc93c'; ctx.strokeStyle = '#1b1f3a'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(P.x, P.y, 6.5, 0, 7); ctx.fill(); ctx.stroke();
          label('P', P.x - 11, P.y - 9, '#9a6a00', 12);
          const zeroV = snapped && target === 'zeroV';
          const ang = deg(Math.atan2(-f.ey, f.ex));
          out('E', zeroE ? '0 N/C (neutral point)' : `${sci(E)} N/C${E > 0 ? ` at ${fmt((ang + 360) % 360, 0)}°` : ''}`);
          out('V', zeroV ? '0 V' : `${sci(f.v)} V`);
          const sx = fmt((P.x - OX) / PX, 1), sy = fmt((OY - P.y) / PX, 1);
          if (touched && !won) {
            if (zeroE) { msg(`✔ At (${sx}, ${sy}) cm the fields cancel`); win(`Neutral point at (${sx} cm, ${sy} cm): the fields kq/r² of the charges are equal and opposite, so E = 0`); }
            else if (zeroV) { msg(`✔ V = 0 at (${sx}, ${sy}) cm`); win(`V = Σ kq/r = 0 at (${sx} cm, ${sy} cm) — but E there is ${sci(E)} N/C, not zero!`); }
            else if (target === 'E' && Math.abs(E - tval) <= 0.02 * Math.abs(tval)) { msg('✔'); win(`E = ${sci(E)} N/C at (${sx}, ${sy}) cm`); }
            else if (target === 'V' && Math.abs(f.v - tval) <= 0.02 * Math.max(Math.abs(tval), scaleV() * 0.02)) { msg('✔'); win(`V = ${sci(f.v)} V at (${sx}, ${sy}) cm`); }
          }
          host.querySelector('[data-a="lines"]').classList.toggle('on', showL);
          host.querySelector('[data-a="equip"]').classList.toggle('on', showE);
          if (editable) { ['up', 'dn', 'del'].forEach(k => { host.querySelector(`[data-a="${k}"]`).disabled = !sel; }); host.querySelector('[data-a="addp"]').disabled = host.querySelector('[data-a="addn"]').disabled = Q.length >= 5; }
        }
        let drag = null, moved = false;
        dragOn(pt => {
          moved = false;
          const hitQ = Q.map(c => [c, Math.hypot(pt.x - (OX + c.x * PX), pt.y - (OY - c.y * PX))]).filter(([, d]) => d < 22).sort((a, b) => a[1] - b[1])[0];
          if (Math.hypot(pt.x - P.x, pt.y - P.y) < 24 && (!hitQ || Math.hypot(pt.x - P.x, pt.y - P.y) < hitQ[1])) { drag = 'P'; return; }
          if (hitQ) { Q.forEach(c => { c.sel = false; }); sel = hitQ[0]; sel.sel = true; drag = sel.fixed ? null : sel; api.sfx('tap'); if (!drag) { draw(); return false; } return; }
          drag = 'P';
        }, pt => {
          if (drag === 'P') { placeProbe(pt.x, pt.y); draw(); return; }
          const nx = clamp(Math.round((pt.x - OX) / PX), -14, 14), ny = clamp(Math.round((OY - pt.y) / PX), -9, 9);
          if ((nx !== drag.x || ny !== drag.y) && !Q.some(c => c !== drag && c.x === nx && c.y === ny) && Math.hypot(OX + nx * PX - P.x, OY - ny * PX - P.y) > 8) { drag.x = nx; drag.y = ny; dirty = true; moved = true; placeProbe(P.x, P.y); draw(); }
        }, () => { if (drag === 'P') placeProbe(P.x, P.y); drag = null; draw(); });
        on(host, 'click', e => {
          const b = e.target.closest('[data-a]'); if (!b || b.disabled) return;
          const a = b.dataset.a; api.sfx('tap');
          if (a === 'lines') showL = !showL;
          else if (a === 'equip') showE = !showE;
          else if (a === 'addp' || a === 'addn') {
            const spots = [[0, -6], [-8, 5], [8, 5], [-10, -5], [10, -5], [0, 7], [-6, -7], [6, -7]];
            const s = spots.find(([x, y]) => !Q.some(c => Math.abs(c.x - x) < 2 && Math.abs(c.y - y) < 2)) || [0, 0];
            Q.forEach(c => { c.sel = false; }); sel = { x: s[0], y: s[1], q: a === 'addp' ? 1 : -1, sel: true }; Q.push(sel);
          } else if (sel && (a === 'up' || a === 'dn')) { const m = clamp(Math.abs(sel.q) + (a === 'up' ? 1 : -1), 1, 9); sel.q = Math.sign(sel.q) * m; }
          else if (sel && a === 'del') { if (Q.length <= 1) { msg('Keep at least one charge'); return; } Q.splice(Q.indexOf(sel), 1); sel = null; }
          touched = true; dirty = true; placeProbe(P.x, P.y); draw();
        });
        draw();
        msg('Drag P (or tap anywhere). Drag charges to move them.');
        return cleanup;
      }

      // ================= dipole =================
      function dipole() {
        const q = +p.q > 0 ? +p.q : 2, a = +p.a > 0 ? clamp(+p.a, 0.5, 6) : 2, E0 = +p.E0 > 0 ? +p.E0 : 1e5;
        const pm = q * UC * 2 * a / 100; // dipole moment, C m
        let th = isFinite(+p.angle) ? Math.round(+p.angle) : 30, w = 0, released = false;
        const tg = p.target || {};
        let target = tg.torque === 'max' ? { torque: 'max' } : isFinite(+tg.torque) ? { torque: +tg.torque } : tg.U === 'min' || tg.U === 'max' ? { U: tg.U } : isFinite(+tg.angle) ? { angle: +tg.angle } : { torque: 'max' };
        const genText = () => target.torque === 'max' ? 'Turn the dipole so that the torque on it is maximum.' : target.torque != null ? `Turn the dipole so that the torque is ${sci(target.torque)} N m.` : target.U === 'min' ? 'Put the dipole in stable equilibrium (minimum potential energy).' : target.U === 'max' ? 'Put the dipole in unstable equilibrium (maximum potential energy, τ = 0).' : `Turn the dipole to θ = ${target.angle}° with the field.`;
        shell(`<div class="lb-fieldlines-chips"><div class="lb-fieldlines-chip" style="background:#fff5d6;color:#9a6a00">θ = <b data-o="th"></b></div><div class="lb-fieldlines-chip" style="background:#f3edff;color:#5b33c9">τ = <b data-o="tau"></b></div><div class="lb-fieldlines-chip" style="background:#d9f7ee;color:#0f7a5c">U = <b data-o="U"></b></div></div>
<div class="lb-fieldlines-f">p = q × 2a = <b>${sci(pm)} C m</b> · τ = pE sin θ · U = −pE cos θ · net force = 0</div>
<div class="lb-fieldlines-row"><button class="lb-fieldlines-b" data-a="m">◀ 1°</button><button class="lb-fieldlines-b go" data-a="rel">Release ▶</button><button class="lb-fieldlines-b" data-a="p">1° ▶</button></div>`);
        setCh(p.challenge || genText());
        setupCanvas();
        const R = clamp(40 + a * 12, 52, 96); // drawn half-length in px (not to scale with the board)
        let last = performance.now();
        const norm = d => ((Math.round(d) % 360) + 360) % 360;
        function check(fromDrag) {
          if (!touched || won) return;
          const t = norm(th), tau = pm * E0 * sinD(t);
          let ok = false;
          if (target.torque === 'max') ok = t === 90 || t === 270;
          else if (target.torque != null) ok = Math.abs(Math.abs(tau) - target.torque) <= 0.01 * target.torque;
          else if (target.U === 'min') ok = t === 0;
          else if (target.U === 'max') ok = t === 180;
          else ok = t === norm(target.angle) || (360 - t) === norm(target.angle);
          if (ok) { msg('✔'); win(`θ = ${t}°: τ = pE sin θ = ${sci(Math.abs(tau))} N m, U = −pE cos θ = ${sci(-pm * E0 * cosD(t))} J${t === 0 ? ' — stable equilibrium' : t === 180 ? ' — unstable equilibrium' : t === 90 || t === 270 ? ' — maximum torque pE' : ''}`); }
          void fromDrag;
        }
        function draw() {
          const now = performance.now(), dt = Math.min(0.033, (now - last) / 1000); last = now;
          if (released) {
            const wn2 = 18; // ω₀² for drawing (rad/s²)
            w += (-wn2 * Math.sin(rad(th)) - 1.1 * w) * dt; th += deg(w * dt);
            if (Math.abs(w) < 0.02 && Math.abs(Math.sin(rad(th))) < 0.004) { released = false; w = 0; th = norm(th); host.querySelector('[data-a="rel"]').disabled = false; check(false); }
          }
          ctx.fillStyle = '#fbfbff'; ctx.fillRect(0, 0, W, H);
          // uniform field lines
          for (let i = 0; i < 7; i++) { const y = 18 + i * 34; ctx.strokeStyle = 'rgba(59,130,246,.35)'; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(6, y); ctx.lineTo(W - 6, y); ctx.stroke(); for (let k = 0; k < 4; k++) arrowHead(40 + k * 92, y, 0, 6, 'rgba(59,130,246,.55)'); }
          label(`E = ${sci(E0)} N/C →`, W - 8, H - 8, '#2f6fd6', 11, 'right');
          const c = Math.cos(rad(th)), s = Math.sin(rad(th));
          const px = OX + c * R, py = OY - s * R, nx = OX - c * R, ny = OY + s * R;
          // angle arc between p and E
          ctx.strokeStyle = '#ffc93c'; ctx.lineWidth = 3; ctx.beginPath(); const t = norm(th); ctx.arc(OX, OY, 34, 0, -rad(t), t <= 180 ? true : false); ctx.stroke();
          ctx.setLineDash([4, 4]); ctx.strokeStyle = '#9a6a00'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(OX, OY); ctx.lineTo(OX + R + 30, OY); ctx.stroke(); ctx.setLineDash([]);
          label('θ', OX + 46 * Math.cos(-rad(t <= 180 ? t / 2 : (t + 360) / 2)), OY + 46 * Math.sin(-rad(t <= 180 ? t / 2 : (t + 360) / 2)) + 4, '#9a6a00', 12);
          // rod and p arrow
          ctx.strokeStyle = '#6b7090'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(nx, ny); ctx.lineTo(px, py); ctx.stroke();
          arrow(OX - c * R * 0.45, OY + s * R * 0.45, OX + c * R * 0.45, OY - s * R * 0.45, '#8b5cf6', 3.5);
          label('p', OX + c * R * 0.5 - s * 14, OY - s * R * 0.5 - c * 14 + 4, '#5b33c9', 13);
          // forces qE
          const F = 46; arrow(px, py, px + F, py, '#e04848', 3.5); arrow(nx, ny, nx - F, ny, '#2f6fd6', 3.5);
          label('qE', px + F + 4, py - 6, '#e04848', 11, 'left'); label('−qE', nx - F - 4, ny - 6, '#2f6fd6', 11, 'right');
          drawCharge({ x: (px - OX) / PX, y: (OY - py) / PX, q: q }); drawCharge({ x: (nx - OX) / PX, y: (OY - ny) / PX, q: -q });
          // torque sense
          const tau = pm * E0 * sinD(th);
          if (Math.abs(Math.sin(rad(th))) > 0.02) { ctx.strokeStyle = 'rgba(46,211,165,.9)'; ctx.lineWidth = 3; const r2 = 16, cw = tau > 0; ctx.beginPath(); ctx.arc(OX, OY, r2, -2.4, 0.4); ctx.stroke(); arrowHead(OX + r2 * Math.cos(cw ? 0.4 : -2.4), OY + r2 * Math.sin(cw ? 0.4 : -2.4), cw ? 0.4 + Math.PI / 2 : -2.4 - Math.PI / 2, 7, 'rgba(46,211,165,1)'); }
          out('th', norm(th) + '°'); out('tau', `${sci(Math.abs(tau))} N m ${Math.abs(tau) < 1e-12 ? '' : tau > 0 ? '↻' : '↺'}`); out('U', `${sci(-pm * E0 * cosD(th))} J`);
        }
        dragOn(pt => { if (released) return false; }, pt => { const d = deg(Math.atan2(OY - pt.y, pt.x - OX)); const d0 = norm(th); const cand = [d, d + 180].map(norm); th = Math.abs(((cand[0] - d0 + 540) % 360) - 180) <= Math.abs(((cand[1] - d0 + 540) % 360) - 180) ? cand[0] : cand[1]; check(true); }, () => {});
        on(host, 'click', e => {
          const b = e.target.closest('[data-a]'); if (!b || b.disabled) return;
          touched = true; api.sfx('tap');
          if (b.dataset.a === 'rel') { released = true; w = 0; b.disabled = true; msg('The torque turns p towards E…'); return; }
          if (released) return;
          th = norm(th + (b.dataset.a === 'p' ? 1 : -1)); check(true);
        });
        loop(draw);
        msg('Drag the dipole to turn it');
        return cleanup;
      }

      // ================= gauss =================
      function gauss() {
        const src = Array.isArray(p.charges) && p.charges.length ? p.charges : [{ x: -8, y: 3, q: 2 }, { x: -4, y: -3, q: -1 }, { x: 5, y: 3, q: 3 }, { x: 9, y: -3, q: -2 }];
        const Q = src.slice(0, 6).filter(c => isFinite(+c.q) && +c.q !== 0).map(c => ({ x: clamp(+c.x || 0, -14, 14), y: clamp(+c.y || 0, -9, 9), q: +c.q }));
        const tg = p.target || {};
        let target = isFinite(+tg.qenc) ? { qenc: +tg.qenc } : isFinite(+tg.flux) && +tg.flux === 0 ? { flux0: true } : null;
        if (!target) {
          // pick a net charge that some pair can make but no single charge equals
          const sums = new Set(); for (let i = 0; i < Q.length; i++) for (let j = i + 1; j < Q.length; j++) sums.add(+(Q[i].q + Q[j].q).toFixed(6));
          const pick = [...sums].find(v => v !== 0 && !Q.some(c => c.q === v));
          target = pick != null ? { qenc: pick } : { qenc: Q[0].q };
        }
        const genText = () => target.flux0 ? 'Draw a closed surface around some charges so that the net flux through it is zero.' : `Draw a closed surface (loop) whose net flux is Φ = ${fmt(target.qenc, 2)} ${unit} / ε₀.`;
        const total = Q.reduce((a, c) => Math.max(a, Math.abs(c.q)), 0) || 1, LPU = Math.min(8, 24 / total);
        shell(`<div class="lb-fieldlines-chips"><div class="lb-fieldlines-chip" style="background:#fff5d6;color:#9a6a00">q<sub>enc</sub> = <b data-o="q"></b></div><div class="lb-fieldlines-chip" style="background:#f3edff;color:#5b33c9">Φ = <b data-o="phi"></b></div></div>
<div class="lb-fieldlines-f" data-o="f">Gauss's law: Φ = ∮ E·dS = q<sub>enc</sub> / ε₀</div>
<div class="lb-fieldlines-row"><button class="lb-fieldlines-b" data-a="clear">Clear</button><button class="lb-fieldlines-b" data-a="lines">Field lines</button></div>`);
        setCh(p.challenge || genText());
        setupCanvas();
        let showL = true, lines = traceLines(Q), path = [], closed = false;
        const inside = (x, y) => { let c = false; for (let i = 0, j = path.length - 1; i < path.length; j = i++) { const [xi, yi] = path[i], [xj, yj] = path[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; } return c; };
        const cpos = c => [OX + c.x * PX, OY - c.y * PX];
        function draw() {
          grid();
          if (path.length > 1) {
            ctx.beginPath(); path.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); if (closed) ctx.closePath();
            if (closed) { ctx.fillStyle = 'rgba(46,211,165,.14)'; ctx.fill(); }
            ctx.strokeStyle = '#0fae84'; ctx.lineWidth = 3; ctx.setLineDash(closed ? [] : [6, 4]); ctx.stroke(); ctx.setLineDash([]);
          }
          if (showL) drawLines(lines);
          const ins = closed ? Q.filter(c => inside(...cpos(c))) : [];
          Q.forEach(c => drawCharge(c, ins.includes(c)));
          const qe = +ins.reduce((a, c) => a + c.q, 0).toFixed(6);
          out('q', closed ? `${fmt(qe, 2)} ${unit}` : '—');
          out('phi', closed ? `${sci(qe * UC / EPS0)} N m²/C` : '—');
          if (closed) out('f', `Φ = q<sub>enc</sub> / ε₀ = ${fmt(qe, 2)} × 10${unit === 'nC' ? '⁻⁹' : '⁻⁶'} / 8.854 × 10⁻¹² · net field lines out = ${fmt(LPU * qe, 0)} (${fmt(LPU, 1)} per ${unit})`);
          return { ins, qe };
        }
        function finish() {
          if (path.length < 8) { path = []; closed = false; msg('Draw a bigger loop'); draw(); return; }
          const [x0, y0] = path[0], [x1, y1] = path[path.length - 1];
          let span = 0; path.forEach(([x, y]) => { span = Math.max(span, Math.hypot(x - x0, y - y0)); });
          if (Math.hypot(x1 - x0, y1 - y0) > Math.max(40, span * 0.6)) msg('Tip: end your loop near where you started');
          closed = true;
          // the surface must not pass through a charge
          const thru = Q.some(c => { const [cx, cy] = cpos(c); return path.some(([x, y], i) => { const [x2, y2] = path[(i + 1) % path.length]; const dx = x2 - x, dy = y2 - y, L2 = dx * dx + dy * dy || 1; const t = clamp(((cx - x) * dx + (cy - y) * dy) / L2, 0, 1); return Math.hypot(x + dx * t - cx, y + dy * t - cy) < 9; }); });
          if (thru) { msg('The surface must not pass through a charge — draw again'); api.sfx('hmm'); closed = false; path = []; draw(); return; }
          const { ins, qe } = draw();
          if (won) return;
          if (target.flux0 ? ins.length > 0 && Math.abs(qe) < 1e-9 : Math.abs(qe - target.qenc) < 1e-9) { msg(`✔ q_enc = ${fmt(qe, 2)} ${unit}`); win(`Charges inside: ${ins.map(c => (c.q > 0 ? '+' : '−') + Math.abs(c.q)).join(', ')} ${unit} → Φ = q_enc/ε₀ = ${sci(qe * UC / EPS0)} N m²/C. Charges outside add nothing to the net flux.`); }
          else msg(ins.length ? `q_enc = ${fmt(qe, 2)} ${unit} — not yet` : 'No charge inside: Φ = 0');
        }
        dragOn(pt => { path = [[pt.x, pt.y]]; closed = false; }, pt => { const l = path[path.length - 1]; if (Math.hypot(pt.x - l[0], pt.y - l[1]) >= 3) { path.push([clamp(pt.x, 1, W - 1), clamp(pt.y, 1, H - 1)]); draw(); } }, finish);
        on(host, 'click', e => { const b = e.target.closest('[data-a]'); if (!b) return; api.sfx('tap'); if (b.dataset.a === 'clear') { path = []; closed = false; out('f', "Gauss's law: Φ = ∮ E·dS = q<sub>enc</sub> / ε₀"); msg('Draw a loop with your finger'); } else { showL = !showL; b.classList.toggle('on', showL); } draw(); });
        host.querySelector('[data-a="lines"]').classList.add('on');
        draw();
        msg('Draw a closed loop with your finger');
        return cleanup;
      }
    },
    example: { mode: 'field', charges: [{ x: -5, y: 0, q: 1 }, { x: 4, y: 0, q: 4 }], probe: [0, 4], target: { zeroE: true }, challenge: 'Charges +1 μC and +4 μC are 9 cm apart. Find the neutral point where E = 0.' },
    examples: [
      { mode: 'field', charges: [{ x: -5, y: 0, q: 2 }, { x: 5, y: 0, q: -1 }], probe: [0, 5], target: { zeroV: true }, editable: false, challenge: 'Find a point where the potential due to +2 μC and −1 μC is zero. Is E zero there too?' },
      { mode: 'dipole', q: 2, a: 2, E0: 1e5, angle: 30, target: { torque: 'max' }, challenge: 'एकसमान क्षेत्र में द्विध्रुव को ऐसे घुमाइए कि बल-आघूर्ण (torque) अधिकतम हो।' },
      { mode: 'gauss', charges: [{ x: -8, y: 3, q: 2 }, { x: -4, y: -3, q: -1 }, { x: 5, y: 3, q: 3 }, { x: 9, y: -3, q: -2 }], target: { qenc: 1 }, challenge: 'Draw a closed surface with net flux Φ = (1 μC)/ε₀.' }
    ]
  });
})();
