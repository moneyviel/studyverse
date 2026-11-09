/* Knowtopia Concept Lab: unitcircle — trigonometric ratios on the unit circle + heights and distances.
 *
 * mode 'circle': the child drags the point P round a unit circle (or uses the slider / standard-angle
 *   buttons). The right triangle under P shows cos θ (base), sin θ (height) and tan θ (on the tangent
 *   line at (1, 0)); values update live, with exact values for 0°, 30°, 45°, 60°, 90° (and their
 *   relatives beyond 90° if maxAngle is 360).
 * mode 'heights': a tower / tree and an observer. Either the height is fixed and the child drags the
 *   observer along the ground (distance changes), or the distance is fixed and the angle slider
 *   changes the height. tan θ = height ÷ distance is shown with the numbers.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   mode        'circle' | 'heights'                                                          default 'circle'
 *   angle       number   starting angle in degrees                                            default 20
 *   maxAngle    90 | 360 largest angle in circle mode (90 = first-quadrant zoom)               default 90
 *   find        {fn:'sin'|'cos'|'tan', value:number}   circle challenge: find θ with fn θ = value
 *               default {fn:'sin', value:0.5}
 *   object      'tower' | 'tree' | 'building'   heights mode picture                             default 'tower'
 *   fixed       'height' | 'distance'   which length stays fixed in heights mode                 default 'height'
 *   height      number   object height in metres (fixed='height')                                default 30
 *   distance    number   observer's distance in metres (fixed='distance')                         default 20
 *   eye         number   observer's eye height in metres (0 = measure from the ground)            default 0
 *   dRange      [min,max]  draggable distance range in metres                     default [0.15×height, 2×height]
 *   target      {angle:n} | {height:n} | {distance:n}   heights challenge                       default {angle:60}
 *   unit        string   length unit                                                             default 'm'
 *   challenge   string   challenge sentence (else generated)
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const rad = d => d * Math.PI / 180;
  const f4 = v => (Math.abs(v) < 5e-5 ? 0 : v).toFixed(4).replace('-', '−');
  const r2 = v => String((Math.round(v * 100) / 100) || 0).replace('-', '−');
  const f1 = v => (Math.round(v * 10) / 10).toString();
  const EX = { 0: ['0', '1', '0'], 30: ['1/2', '√3/2', '1/√3'], 45: ['1/√2', '1/√2', '1'], 60: ['√3/2', '1/2', '√3'], 90: ['1', '0', 'not defined'] };
  function exact(th) { // exact [sin,cos,tan] strings for multiples of 30/45, else null
    th = ((th % 360) + 360) % 360;
    let ref = th, ss = 1, cs = 1;
    if (th > 90 && th <= 180) { ref = 180 - th; cs = -1; } else if (th > 180 && th <= 270) { ref = th - 180; ss = -1; cs = -1; } else if (th > 270) { ref = 360 - th; ss = -1; }
    const e = EX[ref]; if (!e) return null;
    const sg = (s, v) => (v === '0' || v === 'not defined' || s > 0) ? v : '−' + v;
    const ts = ss * cs;
    return [sg(ss, e[0]), sg(cs, e[1]), (ref === 90) ? 'not defined' : sg(ts, e[2])];
  }

  Labs.register('unitcircle', {
    title: 'Trig explorer',
    subjects: ['maths'],
    render(host, p, api) {
      const mode = p.mode === 'heights' ? 'heights' : 'circle';
      const unit = String(p.unit || 'm');
      let won = false, drag = false;
      const css = `
.lb-unitcircle-w{font-size:14px;color:#1b1f3a}
.lb-unitcircle-ch{font-weight:800;font-size:14px;margin-bottom:5px;line-height:1.25}
.lb-unitcircle-svg{width:100%;height:auto;display:block;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:16px;touch-action:none;user-select:none;-webkit-user-select:none}
.lb-unitcircle-svg.sky{background:linear-gradient(#dff1ff,#f4fbff 70%)}
.lb-unitcircle-vals{display:flex;gap:5px;margin-top:6px}
.lb-unitcircle-vals div{flex:1;border-radius:11px;text-align:center;padding:3px 2px;font-weight:800;font-size:11.5px;line-height:1.2}
.lb-unitcircle-vals b{display:block;font-family:'Baloo 2',Nunito,sans-serif;font-size:17px}
.lb-unitcircle-vals small{display:block;font-size:11px;color:#1b1f3a;opacity:.75;min-height:13px}
.lb-unitcircle-row{display:flex;gap:5px;margin-top:6px;align-items:center}
.lb-unitcircle-b{flex:1;min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0}
.lb-unitcircle-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-unitcircle-b:active{transform:translateY(2px)}
.lb-unitcircle-sl{display:flex;align-items:center;gap:8px;margin-top:4px;font-weight:800}
.lb-unitcircle-sl input{flex:1;min-width:0;-webkit-appearance:none;appearance:none;height:34px;background:transparent;cursor:pointer}
.lb-unitcircle-sl input::-webkit-slider-runnable-track{height:8px;border-radius:8px;background:#e3e6f6}
.lb-unitcircle-sl input::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:26px;border-radius:50%;background:#8b5cf6;margin-top:-9px;border:3px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.3)}
.lb-unitcircle-sl input::-moz-range-track{height:8px;border-radius:8px;background:#e3e6f6}
.lb-unitcircle-sl input::-moz-range-thumb{width:20px;height:20px;border-radius:50%;background:#8b5cf6;border:3px solid #fff}
.lb-unitcircle-info{margin-top:5px;background:#f6f4ff;border-radius:12px;padding:5px 9px;font-weight:700;font-size:13px;line-height:1.45;text-align:center}
.lb-unitcircle-info b{color:#8b5cf6}
.lb-unitcircle-msg{font-size:12.5px;font-weight:700;color:#6b7090;margin-top:3px;min-height:16px;text-align:center}`;

      if (mode === 'circle') return circle();
      return heights();

      // ================= circle mode =================
      function circle() {
        const full = +p.maxAngle === 360;
        const maxA = full ? 360 : 90;
        let th = Math.max(0, Math.min(maxA, Math.round(isFinite(+p.angle) ? +p.angle : 20)));
        const fnOk = ['sin', 'cos', 'tan'];
        let find = p.find && fnOk.includes(p.find.fn) && isFinite(+p.find.value) ? { fn: p.find.fn, value: +p.find.value } : { fn: 'sin', value: 0.5 };
        const valLabel = v => v < 0 ? '−' + valLabel0(-v) : valLabel0(v);
        const valLabel0 = v => { const m = { 0.5: '1/2', 1: '1', 0: '0' }; if (m[v] != null) return m[v]; if (Math.abs(v - Math.sqrt(3) / 2) < 1e-3) return '√3/2'; if (Math.abs(v - Math.SQRT1_2) < 1e-3) return '1/√2'; if (Math.abs(v - Math.sqrt(3)) < 1e-3) return '√3'; if (Math.abs(v - 1 / Math.sqrt(3)) < 1e-3) return '1/√3'; return String(v); };
        const chText = p.challenge || `Find the angle θ where ${find.fn} θ = ${valLabel(find.value)}.`;
        const W = 360, H = 250;
        const O = full ? { x: 128, y: 125 } : { x: 48, y: 222 }, R = full ? 100 : 180;
        const std = full ? [0, 30, 45, 60, 90, 120, 135, 150, 180, 270] : [0, 30, 45, 60, 90];
        host.innerHTML = `<style>${css}</style>
<div class="lb-unitcircle-w">
  <div class="lb-unitcircle-ch">🎯 Challenge: ${esc(chText)}</div>
  <svg class="lb-unitcircle-svg" viewBox="0 0 ${W} ${H}"></svg>
  <div class="lb-unitcircle-vals">
    <div style="background:#ffe3e3;color:#e04848">sin θ<b data-o="s"></b><small data-e="s"></small></div>
    <div style="background:#e0ecff;color:#2f6fd6">cos θ<b data-o="c"></b><small data-e="c"></small></div>
    <div style="background:#d9f7ee;color:#139c76">tan θ<b data-o="t"></b><small data-e="t"></small></div>
  </div>
  <div class="lb-unitcircle-sl">θ <input type="range" min="0" max="${maxA}" step="1" value="${th}"><span class="lb-unitcircle-deg"></span></div>
  <div class="lb-unitcircle-row">${std.filter(a => full ? [0, 30, 45, 60, 90, 120, 180, 270].includes(a) : true).map(a => `<button class="lb-unitcircle-b" data-ang="${a}" style="${full ? 'font-size:12px' : ''}">${a}°</button>`).join('')}</div>
  <div class="lb-unitcircle-msg"></div>
</div>`;
        const $ = s => host.querySelector(s);
        const svg = $('.lb-unitcircle-svg'), sl = $('.lb-unitcircle-sl input'), msg = $('.lb-unitcircle-msg');
        // static background
        let bg = '';
        if (full) {
          for (let k = -2; k <= 2; k++) { bg += `<line x1="${O.x + k * R / 2}" y1="15" x2="${O.x + k * R / 2}" y2="235" stroke="#e6e8f7"/><line x1="18" y1="${O.y + k * R / 2}" x2="238" y2="${O.y + k * R / 2}" stroke="#e6e8f7"/>`; }
          bg += `<line x1="16" y1="${O.y}" x2="242" y2="${O.y}" stroke="#1b1f3a" stroke-width="1.5"/><line x1="${O.x}" y1="12" x2="${O.x}" y2="238" stroke="#1b1f3a" stroke-width="1.5"/>`;
          bg += `<circle cx="${O.x}" cy="${O.y}" r="${R}" fill="none" stroke="#8b5cf6" stroke-width="2.5" stroke-opacity=".55"/>`;
          bg += `<text x="${O.x + R + 3}" y="${O.y + 13}" font-size="10" font-weight="800" fill="#6b7090">1</text><text x="${O.x - R - 12}" y="${O.y + 13}" font-size="10" font-weight="800" fill="#6b7090">−1</text><text x="${O.x + 4}" y="${O.y - R - 3}" font-size="10" font-weight="800" fill="#6b7090">1</text>`;
        } else {
          for (let k = 1; k <= 4; k++) { bg += `<line x1="${O.x + k * R / 4}" y1="${O.y - R - 8}" x2="${O.x + k * R / 4}" y2="${O.y}" stroke="#e6e8f7"/><line x1="${O.x}" y1="${O.y - k * R / 4}" x2="${O.x + R + 8}" y2="${O.y - k * R / 4}" stroke="#e6e8f7"/>`; }
          bg += `<line x1="${O.x - 10}" y1="${O.y}" x2="${O.x + R + 30}" y2="${O.y}" stroke="#1b1f3a" stroke-width="1.5"/><line x1="${O.x}" y1="${O.y + 10}" x2="${O.x}" y2="${O.y - R - 14}" stroke="#1b1f3a" stroke-width="1.5"/>`;
          bg += `<path d="M${O.x + R} ${O.y} A${R} ${R} 0 0 0 ${O.x} ${O.y - R}" fill="none" stroke="#8b5cf6" stroke-width="2.5" stroke-opacity=".55"/>`;
          bg += `<text x="${O.x + R - 3}" y="${O.y + 14}" font-size="11" font-weight="800" fill="#6b7090">1</text><text x="${O.x - 12}" y="${O.y - R + 4}" font-size="11" font-weight="800" fill="#6b7090">1</text><text x="${O.x - 13}" y="${O.y + 14}" font-size="11" font-weight="800" fill="#6b7090">O</text>`;
        }
        svg.innerHTML = `<g>${bg}</g><g class="lb-unitcircle-dyn"></g>`;
        const dyn = svg.querySelector('.lb-unitcircle-dyn');

        function draw() {
          const s = Math.sin(rad(th)), c = Math.cos(rad(th));
          const P = { x: O.x + R * c, y: O.y - R * s }, F = { x: P.x, y: O.y };
          let g = '';
          // tangent line at (1,0)
          const tanOk = Math.abs(c) > 1e-9;
          const t = tanOk ? s / c : Infinity;
          const tx = O.x + R, ty = O.y - R * t;
          const tTop = full ? 12 : 8, tBot = full ? 238 : O.y + 2;
          if (tanOk) {
            const yClamp = Math.max(tTop, Math.min(tBot, ty));
            g += `<line x1="${tx}" y1="${tTop}" x2="${tx}" y2="${full ? 238 : O.y}" stroke="#2ed3a5" stroke-width="1.2" stroke-dasharray="3 4"/>`;
            g += `<line x1="${O.x}" y1="${O.y}" x2="${tx}" y2="${yClamp === ty ? ty : yClamp}" stroke="#2ed3a5" stroke-width="1.6" stroke-dasharray="5 4" opacity=".9"/>`;
            g += `<line x1="${tx}" y1="${O.y}" x2="${tx}" y2="${yClamp}" stroke="#2ed3a5" stroke-width="5" stroke-linecap="round"/>`;
            const ta = full ? `x="${tx - 6}" text-anchor="end"` : `x="${tx + 6}"`;
            if (ty >= tTop && ty <= tBot) g += `<text ${ta} y="${(O.y + ty) / 2 + 4}" font-size="11.5" font-weight="900" fill="#139c76">tan</text>`;
            else g += `<text ${ta} y="${ty < tTop ? tTop + 10 : tBot - 4}" font-size="11.5" font-weight="900" fill="#139c76">tan ${ty < tTop ? '↑' : '↓'}</text>`;
          }
          // triangle
          g += `<path d="M${O.x} ${O.y} L${F.x} ${F.y} L${P.x} ${P.y} Z" fill="#8b5cf6" fill-opacity=".1"/>`;
          g += `<line x1="${O.x}" y1="${O.y}" x2="${F.x}" y2="${F.y}" stroke="#3b82f6" stroke-width="5" stroke-linecap="round"/>`;
          g += `<line x1="${F.x}" y1="${F.y}" x2="${P.x}" y2="${P.y}" stroke="#ff6b6b" stroke-width="5" stroke-linecap="round"/>`;
          g += `<line x1="${O.x}" y1="${O.y}" x2="${P.x}" y2="${P.y}" stroke="#1b1f3a" stroke-width="3" stroke-linecap="round"/>`;
          if (Math.abs(s) > 0.08 && Math.abs(c) > 0.08) { const d = 9, sx = c > 0 ? -1 : 1, sy = s > 0 ? -1 : 1; g += `<path d="M${F.x + sx * d} ${F.y} L${F.x + sx * d} ${F.y + sy * d} L${F.x} ${F.y + sy * d}" fill="none" stroke="#1b1f3a" stroke-width="1.3"/>`; }
          // angle arc
          const ar = full ? 24 : 34, large = th > 180 ? 1 : 0;
          if (th > 0 && th < 360) g += `<path d="M${O.x + ar} ${O.y} A${ar} ${ar} 0 ${large} 0 ${O.x + ar * c} ${O.y - ar * s}" fill="none" stroke="#ffc93c" stroke-width="3.5"/>`;
          const mid = rad(th / 2), lr = ar + 13;
          g += `<text x="${O.x + lr * Math.cos(mid)}" y="${O.y - lr * Math.sin(mid) + 4}" text-anchor="middle" font-size="12" font-weight="900" fill="#b8860b">θ</text>`;
          // labels
          if (Math.abs(c) > 0.12) g += `<text x="${(O.x + F.x) / 2}" y="${O.y + (s >= 0 ? 15 : -7)}" text-anchor="middle" font-size="11.5" font-weight="900" fill="#2f6fd6">cos</text>`;
          if (Math.abs(s) > 0.12) g += `<text x="${F.x + (c >= 0 ? -6 : 6)}" y="${(F.y + P.y) / 2 + 4}" text-anchor="${c >= 0 ? 'end' : 'start'}" font-size="11.5" font-weight="900" fill="#e04848">sin</text>`;
          g += `<text x="${(O.x + P.x) / 2 - 6 * s}" y="${(O.y + P.y) / 2 - 6 * c}" text-anchor="middle" font-size="11" font-weight="900" fill="#1b1f3a">1</text>`;
          g += `<circle cx="${P.x}" cy="${P.y}" r="20" fill="#8b5cf6" fill-opacity=".14" class="lb-unitcircle-h"/><circle cx="${P.x}" cy="${P.y}" r="10" fill="#8b5cf6" stroke="#fff" stroke-width="3" class="lb-unitcircle-h"/>`;
          const px = Math.min(W - 70, Math.max(4, P.x + 12)), py = Math.max(14, P.y - 12);
          g += `<text x="${px}" y="${py}" font-size="11" font-weight="800" fill="#5b33c9">P(${r2(c)}, ${r2(s)})</text>`;
          // side panel (quadrant mode) - identity
          const px2 = full ? 250 : 236;
          g += `<g transform="translate(${px2} ${full ? 30 : 26})"><text font-size="26" font-weight="900" fill="#1b1f3a" font-family="Nunito,sans-serif">θ = ${th}°</text>`
            + `<text y="22" font-size="10.5" font-weight="800" fill="#6b7090">sin²θ + cos²θ</text><text y="37" font-size="10.5" font-weight="800" fill="#6b7090">= ${f4(s * s)} + ${f4(c * c)}</text><text y="52" font-size="11" font-weight="900" fill="#1b1f3a">= 1 ✓</text>`
            + (tanOk ? `<text y="72" font-size="10.5" font-weight="800" fill="#6b7090">tan θ = sin θ ÷ cos θ</text>` : `<text y="72" font-size="10.5" font-weight="800" fill="#e04848">cos θ = 0 → tan undefined</text>`) + '</g>';
          dyn.innerHTML = g;
          const e = exact(th);
          host.querySelector('[data-o="s"]').textContent = f4(s);
          host.querySelector('[data-o="c"]').textContent = f4(c);
          host.querySelector('[data-o="t"]').textContent = tanOk ? (Math.abs(t) > 1e4 ? '∞' : f4(t)) : '∞';
          host.querySelector('[data-e="s"]').textContent = e ? '= ' + e[0] : '';
          host.querySelector('[data-e="c"]').textContent = e ? '= ' + e[1] : '';
          host.querySelector('[data-e="t"]').textContent = e ? (e[2] === 'not defined' ? 'not defined' : '= ' + e[2]) : '';
          host.querySelector('.lb-unitcircle-deg').textContent = th + '°';
          host.querySelectorAll('[data-ang]').forEach(b => b.classList.toggle('on', +b.dataset.ang === th));
          sl.value = th;
          check(s, c, t);
        }
        let touched = false;
        function check(s, c, t) {
          if (won || !touched) return;
          const v = find.fn === 'sin' ? s : find.fn === 'cos' ? c : t;
          if (isFinite(v) && Math.abs(v - find.value) < 0.004) {
            won = true; api.sfx('correct');
            const e = exact(th);
            msg.textContent = `${find.fn} ${th}° = ${e ? e[['sin', 'cos', 'tan'].indexOf(find.fn)] : f4(v)}`;
            api.win(`θ = ${th}°: ${find.fn} ${th}° = ${e ? e[['sin', 'cos', 'tan'].indexOf(find.fn)] + ' = ' : ''}${f4(v)}`);
          }
        }
        function setFromPointer(e) {
          touched = true;
          const r = svg.getBoundingClientRect();
          const x = (e.clientX - r.left) * W / r.width, y = (e.clientY - r.top) * H / r.height;
          let a = Math.atan2(O.y - y, x - O.x) * 180 / Math.PI;
          if (full) { if (a < 0) a += 360; } else a = Math.max(0, Math.min(90, a < -90 ? 90 : a));
          const na = Math.round(a);
          if (na !== th) { th = Math.min(maxA, na); draw(); }
        }
        const down = e => { drag = true; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); setFromPointer(e); };
        const move = e => { if (drag) setFromPointer(e); };
        const up = () => { drag = false; };
        svg.addEventListener('pointerdown', down); svg.addEventListener('pointermove', move); svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
        const onInput = e => { if (e.target === sl) { touched = true; th = +sl.value; draw(); } };
        const onClick = e => { const b = e.target.closest('[data-ang]'); if (b) { touched = true; th = +b.dataset.ang; api.sfx('tap'); draw(); } };
        host.addEventListener('input', onInput); host.addEventListener('click', onClick);
        draw();
        return () => { svg.removeEventListener('pointerdown', down); svg.removeEventListener('pointermove', move); svg.removeEventListener('pointerup', up); svg.removeEventListener('pointercancel', up); host.removeEventListener('input', onInput); host.removeEventListener('click', onClick); };
      }

      // ================= heights mode =================
      function heights() {
        const obj = ['tower', 'tree', 'building'].includes(p.object) ? p.object : 'tower';
        const fixed = p.fixed === 'distance' ? 'distance' : 'height';
        const eye = Math.max(0, +p.eye || 0);
        let Hh = Math.max(2, +p.height || 30), D = Math.max(1, +p.distance || 20);
        const dR = Array.isArray(p.dRange) && p.dRange.length === 2 && +p.dRange[0] > 0 && +p.dRange[0] < +p.dRange[1] ? p.dRange.map(Number) : [Math.round(Hh * 1.5) / 10, Hh * 2];
        let th; // degrees
        if (fixed === 'height') { D = Math.max(dR[0], Math.min(dR[1], D)); }
        else th = Math.max(5, Math.min(75, isFinite(+p.angle) ? +p.angle : 30));
        const rise = () => fixed === 'height' ? Hh - eye : D * Math.tan(rad(th));
        const curAngle = () => fixed === 'height' ? Math.atan((Hh - eye) / D) * 180 / Math.PI : th;
        const curH = () => fixed === 'height' ? Hh : eye + D * Math.tan(rad(th));
        let tg = p.target && typeof p.target === 'object' ? p.target : null;
        if (!tg || !(('angle' in tg) || ('height' in tg && fixed === 'distance') || ('distance' in tg && fixed === 'height'))) tg = fixed === 'height' ? { angle: 60 } : { angle: 45 };
        const objName = { tower: 'tower', tree: 'tree', building: 'building' }[obj];
        const chText = p.challenge || ('angle' in tg ? (fixed === 'height' ? `The ${objName} is ${Hh} ${unit} tall. Walk to where the angle of elevation is ${tg.angle}°.` : `Stand ${D} ${unit} away. Set the angle of elevation to ${tg.angle}°. How tall is the ${objName}?`)
          : 'height' in tg ? `You are ${D} ${unit} away. Find the angle at which the ${objName} is ${tg.height} ${unit} tall.` : `Stand ${tg.distance} ${unit} from the ${objName}. What is the angle of elevation?`);
        const W = 360, Hs = 236, G = 206, TX = 316;
        const hMax = fixed === 'height' ? Hh : eye + D * Math.tan(rad(75));
        let sc = Math.min(270 / dR[1], 175 / Hh);
        void hMax;
        host.innerHTML = `<style>${css}</style>
<div class="lb-unitcircle-w">
  <div class="lb-unitcircle-ch">🎯 Challenge: ${esc(chText)}</div>
  <svg class="lb-unitcircle-svg sky" viewBox="0 0 ${W} ${Hs}"></svg>
  <div class="lb-unitcircle-info"></div>
  ${fixed === 'distance' ? `<div class="lb-unitcircle-sl">θ <input type="range" min="5" max="75" step="1" value="${th}"><span class="lb-unitcircle-deg"></span></div>` : `<div class="lb-unitcircle-row"><button class="lb-unitcircle-b" data-step="-1">◀ 1 ${esc(unit)}</button><button class="lb-unitcircle-b" data-step="-0.1">◀ 0.1</button><button class="lb-unitcircle-b" data-step="0.1">0.1 ▶</button><button class="lb-unitcircle-b" data-step="1">1 ${esc(unit)} ▶</button></div>`}
  <div class="lb-unitcircle-msg">${fixed === 'height' ? 'Drag the child 🧒 along the ground' : 'Slide θ — watch the height h change'}</div>
</div>`;
        const $ = s => host.querySelector(s);
        const svg = $('.lb-unitcircle-svg'), info = $('.lb-unitcircle-info'), msg = $('.lb-unitcircle-msg');
        function objectSvg(h) {
          const top = G - h * sc, ph = h * sc;
          if (obj === 'tree') {
            const cr = Math.max(14, Math.min(40, ph * 0.3));
            return `<rect x="${TX - 5}" y="${top + cr}" width="10" height="${Math.max(0, ph - cr)}" fill="#8b5a2b" rx="2"/><ellipse cx="${TX}" cy="${top + cr}" rx="${cr * 0.85}" ry="${cr}" fill="#2ed3a5"/><ellipse cx="${TX - cr * 0.3}" cy="${top + cr * 0.75}" rx="${cr * 0.35}" ry="${cr * 0.4}" fill="#5fe0bb"/>`;
          }
          if (obj === 'building') {
            let g = `<rect x="${TX - 22}" y="${top}" width="44" height="${ph}" fill="#9aa5d6" rx="3"/>`;
            for (let y = top + 8; y < G - 12; y += 16) for (const x of [-14, 0, 14]) g += `<rect x="${TX + x - 4}" y="${y}" width="8" height="9" rx="1.5" fill="#fff8d6"/>`;
            return g;
          }
          let g = ''; const seg = Math.max(4, Math.round(ph / 18));
          for (let i = 0; i < seg; i++) { const y0 = top + i * ph / seg; const w0 = 8 + 10 * (i / seg), w1 = 8 + 10 * ((i + 1) / seg); g += `<path d="M${TX - w0} ${y0} L${TX + w0} ${y0} L${TX + w1} ${y0 + ph / seg} L${TX - w1} ${y0 + ph / seg} Z" fill="${i % 2 ? '#fff' : '#ff6b6b'}" stroke="#d94848" stroke-width=".8"/>`; }
          return g + `<circle cx="${TX}" cy="${top}" r="3.5" fill="#ffc93c" stroke="#d99a00"/>`;
        }
        function draw() {
          const a = curAngle(), h = curH(), d = D;
          if (fixed === 'distance') sc = Math.min(250 / D, 172 / Math.max(h, D * 0.6));
          const ox = TX - d * sc, ey = G - eye * sc, topY = G - h * sc;
          let g = `<rect x="0" y="${G}" width="${W}" height="${Hs - G}" fill="#a7e3b8"/><line x1="0" y1="${G}" x2="${W}" y2="${G}" stroke="#4caf6e" stroke-width="2"/>`;
          g += `<circle cx="40" cy="30" r="14" fill="#ffc93c" opacity=".9"/>`;
          g += objectSvg(h);
          // sight line & horizontal
          g += `<line x1="${ox}" y1="${ey}" x2="${TX}" y2="${ey}" stroke="#3b82f6" stroke-width="2.5" stroke-dasharray="6 4"/>`;
          g += `<line x1="${ox}" y1="${ey}" x2="${TX}" y2="${topY}" stroke="#ff6b6b" stroke-width="2.5"/>`;
          g += `<line x1="${TX}" y1="${ey}" x2="${TX}" y2="${topY}" stroke="#8b5cf6" stroke-width="3" stroke-dasharray="2 3"/>`;
          const ar = 30; g += `<path d="M${ox + ar} ${ey} A${ar} ${ar} 0 0 0 ${ox + ar * Math.cos(rad(a))} ${ey - ar * Math.sin(rad(a))}" fill="none" stroke="#ffc93c" stroke-width="4"/>`;
          g += `<text x="${ox + ar + 6}" y="${ey - 6}" font-size="12" font-weight="900" fill="#b8860b">${f1(a)}°</text>`;
          g += `<path d="M${TX - 8} ${ey} v-8 h8" fill="none" stroke="#1b1f3a" stroke-width="1.2"/>`;
          // labels
          g += `<text x="${(ox + TX) / 2}" y="${Math.min(Hs - 6, ey + 16)}" text-anchor="middle" font-size="12" font-weight="900" fill="#2f6fd6" paint-order="stroke" stroke="#fff" stroke-width="3">d = ${f1(d)} ${esc(unit)}</text>`;
          g += `<text x="${TX - 26}" y="${(ey + topY) / 2}" text-anchor="end" font-size="12" font-weight="900" fill="#6d3fe0" paint-order="stroke" stroke="#fff" stroke-width="3">h = ${f1(h)} ${esc(unit)}</text>`;
          // observer
          g += `<g class="lb-unitcircle-h" style="cursor:${fixed === 'height' ? 'grab' : 'default'}"><circle cx="${ox}" cy="${G - 16}" r="22" fill="#fff" opacity="${fixed === 'height' ? .5 : 0}"/><text x="${ox}" y="${G - 2}" text-anchor="middle" font-size="30">🧒</text></g>`;
          g += `<circle cx="${ox}" cy="${ey}" r="4" fill="#ff6b6b" stroke="#fff" stroke-width="1.5"/>`;
          svg.innerHTML = g;
          const tA = Math.tan(rad(a));
          info.innerHTML = `tan θ = <b>${eye ? '(h − ' + eye + ')' : 'h'} ÷ d</b> → tan ${f1(a)}° = ${f1(h - eye)} ÷ ${f1(d)} = <b>${tA.toFixed(3)}</b>` + (fixed === 'distance' ? `<br>h = ${eye ? eye + ' + ' : ''}d × tan θ = ${f1(d)} × ${tA.toFixed(3)} = <b>${f1(h)} ${esc(unit)}</b>` : `<br>d = ${eye ? '(h − ' + eye + ')' : 'h'} ÷ tan θ = <b>${f1(d)} ${esc(unit)}</b>`);
          const dg = $('.lb-unitcircle-deg'); if (dg) dg.textContent = th + '°';
          check(a, h, d);
        }
        let touched = false;
        function check(a, h, d) {
          if (won || !touched) return;
          let ok = false;
          if ('angle' in tg) ok = Math.abs(a - tg.angle) < (fixed === 'height' ? 0.15 : 0.01);
          else if ('height' in tg) ok = Math.abs(h - tg.height) <= Math.max(0.05, tg.height * 0.01);
          else ok = Math.abs(d - tg.distance) < 0.05;
          if (!ok) return;
          won = true; api.sfx('correct');
          const exactT = { 30: '1/√3', 45: '1', 60: '√3' }[Math.round(a)];
          const t = exactT && Math.abs(a - Math.round(a)) < 0.4 ? `tan ${Math.round(a)}° = ${exactT}` : `tan ${f1(a)}° ≈ ${Math.tan(rad(a)).toFixed(3)}`;
          const text = fixed === 'height' ? ('angle' in tg ? `At d = ${f1(d)} ${unit} the angle is ≈ ${tg.angle}°. ${t}, so d = ${f1(Hh - eye)} ÷ tan ${tg.angle}° ≈ ${((Hh - eye) / Math.tan(rad(tg.angle))).toFixed(2)} ${unit}.` : `At d = ${f1(d)} ${unit}: tan θ = ${f1(Hh - eye)} ÷ ${f1(d)}, so θ ≈ ${f1(a)}°.`)
            : `At θ = ${f1(a)}°, h = ${eye ? eye + ' + ' : ''}${f1(D)} × tan θ ≈ ${f1(h)} ${unit} (${t}).`;
          msg.textContent = 'You did it! 🎉';
          api.win(text);
        }
        function setD(nd) { touched = true; nd = Math.round(Math.max(dR[0], Math.min(dR[1], nd)) * 10) / 10; if (nd !== D) { D = nd; draw(); } }
        let cleanup;
        if (fixed === 'height') {
          const ptr = e => { const r = svg.getBoundingClientRect(); const x = (e.clientX - r.left) * W / r.width; setD((TX - x) / sc); };
          const down = e => { drag = true; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); ptr(e); };
          const move = e => { if (drag) ptr(e); };
          const up = () => { drag = false; };
          const onClick = e => { const b = e.target.closest('[data-step]'); if (b) { setD(D + (+b.dataset.step) * -1); api.sfx('tap'); } };
          svg.addEventListener('pointerdown', down); svg.addEventListener('pointermove', move); svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
          host.addEventListener('click', onClick);
          cleanup = () => { svg.removeEventListener('pointerdown', down); svg.removeEventListener('pointermove', move); svg.removeEventListener('pointerup', up); svg.removeEventListener('pointercancel', up); host.removeEventListener('click', onClick); };
        } else {
          svg.style.touchAction = 'pan-y';
          const onInput = e => { if (e.target.type === 'range') { touched = true; th = +e.target.value; draw(); } };
          host.addEventListener('input', onInput);
          cleanup = () => host.removeEventListener('input', onInput);
        }
        draw();
        return cleanup;
      }
    },
    example: { mode: 'circle', angle: 20, maxAngle: 90, find: { fn: 'sin', value: 0.5 }, object: 'tower', fixed: 'height', height: 30, distance: 20, eye: 0, unit: 'm' },
    examples: [
      { mode: 'circle', angle: 10, find: { fn: 'tan', value: 1 }, challenge: 'Find the angle where sin θ = cos θ (so tan θ = 1).' },
      { mode: 'heights', object: 'tower', fixed: 'height', height: 30, target: { angle: 60 }, challenge: 'A tower is 30 m tall. Walk to the point where the angle of elevation of its top is 60°.' },
      { mode: 'heights', object: 'tree', fixed: 'distance', distance: 20, angle: 25, target: { height: 20 }, challenge: 'You stand 20 m from a tree. At what angle of elevation is the tree 20 m tall?' }
    ]
  });
})();
