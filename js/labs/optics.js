/* StudyVerse Concept Lab: optics — ray diagrams for mirrors and lenses, and refraction through a glass slab.
 *
 * Mirrors/lenses: the child drags the object (or uses the slider) along the principal axis. Two
 * principal rays are drawn (one parallel to the axis, one through the pole / optical centre) and the
 * image appears where they meet (solid = real, dashed = virtual). Live values use the New Cartesian
 * sign convention: mirror 1/v + 1/u = 1/f, m = −v/u; lens 1/v − 1/u = 1/f, m = v/u.
 * Slab: the child drags the incident ray (or slider) to change the angle of incidence; Snell's law
 * n = sin i / sin r gives the refracted ray, the emergent ray is parallel to the incident ray and the
 * lateral shift is shown.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   mode       string  'plane' | 'concave' | 'convex' | 'convexlens' | 'concavelens' | 'slab'  default 'concave'
 *   modes      array   modes offered as tabs (first view = mode)        default ['concave','convex','plane']
 *   f          number  focal length size in cm (sign is set by the mode)                 default 15
 *   u          number  starting object distance in cm (size, object is on the left)      default 40
 *   range      [min,max] allowed object distance in cm                                    default [5,60]
 *   step       number  slider step in cm                                                  default 1
 *   goal       string  words joined by '-': real, virtual, magnified, diminished, same, erect, inverted,
 *                      infinity, v (|v| = target), gap (object–image distance = target, plane mirror),
 *                      r (angle of refraction = target, slab), none                     default 'real-magnified'
 *   target     number  number used by goals v / gap (cm) or r (degrees)                  default 30
 *   challenge  string  challenge text (any language); default made from goal
 *   winText    string  optional win message
 *   objectLabel string label on the object (e.g. 'Candle', 'मोमबत्ती')                  default 'Object'
 *   i          number  slab: starting angle of incidence in degrees                       default 30
 *   media      array   slab: [{name, n}] materials offered                default Glass 1.5, Water 1.33, Diamond 2.42
 *   t          number  slab: thickness in cm (for lateral shift)                          default 4
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = (v, d = 1) => { const r = Math.round(v * Math.pow(10, d)) / Math.pow(10, d); return (Object.is(r, -0) ? 0 : r).toString().replace('-', '−'); };
  const sgn = v => (v > 0 ? '+' : '') + fmt(v);
  const DEG = Math.PI / 180;
  const NAMES = { plane: 'Plane mirror', concave: 'Concave mirror', convex: 'Convex mirror', convexlens: 'Convex lens', concavelens: 'Concave lens', slab: 'Glass slab' };
  const SHORT = { plane: 'Plane', concave: 'Concave', convex: 'Convex', convexlens: 'Convex lens', concavelens: 'Concave lens', slab: 'Slab' };
  const AX = 108, W = 360, HT = 216;

  const CSS = `
.lb-optics-w{font-size:14px;color:#1b1f3a;-webkit-user-select:none;user-select:none}
.lb-optics-ch{font-weight:800;font-size:14px;margin-bottom:6px;line-height:1.25}
.lb-optics-tabs{display:flex;gap:5px;margin-bottom:6px;overflow-x:auto;scrollbar-width:none}
.lb-optics-t{flex:1 0 auto;min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:12.5px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:0 10px}
.lb-optics-t.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-optics-svg{width:100%;height:auto;display:block;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:18px;touch-action:none;cursor:grab}
.lb-optics-sl{display:flex;align-items:center;gap:8px;margin-top:6px;font-weight:800;font-size:13px}
.lb-optics-sl input{flex:1;accent-color:#8b5cf6;height:36px;min-width:0}
.lb-optics-sl b{min-width:64px;text-align:right;color:#3b82f6}
.lb-optics-out{background:#f6f4ff;border-radius:12px;padding:6px 10px;margin-top:4px;font-weight:800;font-size:13px;line-height:1.4}
.lb-optics-vals{display:flex;flex-wrap:wrap;gap:2px 12px;font-variant-numeric:tabular-nums}
.lb-optics-vals span{white-space:nowrap}
.lb-optics-nat{color:#8b5cf6}
.lb-optics-f{font-size:11.5px;color:#6b7090}
.lb-optics-media{display:flex;gap:5px;margin-top:6px}
.lb-optics-media .lb-optics-t{flex:1 1 0}
`;

  Labs.register('optics', {
    title: 'Ray optics lab',
    subjects: ['science', 'physics'],
    render(host, p, api) {
      // keys copied from `example` by the loader are ignored when the topic asks for a different mode/goal
      const ex = this.example || {};
      const diffMode = p.mode !== undefined && p.mode !== ex.mode;
      const diffGoal = diffMode || p.goal !== ex.goal || p.target !== ex.target;
      p = Object.assign({}, p);
      if (diffMode) ['modes', 'u', 'range', 'objectLabel', 'goal', 'target'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });
      if (diffGoal) ['challenge', 'winText'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });
      const ALL = Object.keys(NAMES);
      let modes = (Array.isArray(p.modes) ? p.modes : []).filter(m => ALL.includes(m));
      let mode = ALL.includes(p.mode) ? p.mode : (modes[0] || 'concave');
      if (!modes.includes(mode)) modes.unshift(mode);
      const F = +p.f > 0 ? +p.f : 15;
      let range = Array.isArray(p.range) && p.range.length === 2 && +p.range[0] > 0 && +p.range[1] > +p.range[0] ? p.range.map(Number) : [5, 60];
      const step = +p.step > 0 ? +p.step : 1;
      const clampU = v => Math.min(range[1], Math.max(range[0], Math.round(v / step) * step));
      let U = clampU(+p.u > 0 ? +p.u : 40);
      const media = (Array.isArray(p.media) && p.media.length ? p.media : [{ name: 'Glass', n: 1.5 }, { name: 'Water', n: 1.33 }, { name: 'Diamond', n: 2.42 }]).filter(m => m && +m.n >= 1);
      let med = 0;
      let I = Math.min(80, Math.max(0, +p.i >= 0 ? +p.i : 30));
      const thick = +p.t > 0 ? +p.t : 4;
      const goal = String(p.goal || (mode === 'slab' ? 'r' : mode === 'plane' ? 'gap' : 'none')).toLowerCase().split('-').filter(Boolean);
      const target = +p.target || (mode === 'plane' ? 40 : 30);
      const objLabel = String(p.objectLabel || 'Object');
      let touched = false, won = false;

      const DEFCH = () => {
        if (goal.includes('r')) return `Change the angle of incidence so the ray bends to ${fmt(target)}° inside the slab.`;
        if (goal.includes('gap')) return `Move the object so its image is ${fmt(target)} cm away from the object.`;
        if (goal.includes('v')) return `Move the object so the image forms ${fmt(target)} cm from the ${/lens/.test(mode) ? 'lens' : 'mirror'}.`;
        if (goal.includes('infinity')) return 'Move the object so the image forms at infinity (rays come out parallel).';
        if (goal.includes('none')) return 'Drag the object and watch how the image changes.';
        const words = goal.map(g => ({ same: 'same-size', erect: 'erect' }[g] || g)).join(', ');
        return `Drag the object to make a ${words} image.`;
      };

      host.innerHTML = `<style>${CSS}</style>
<div class="lb-optics-w">
  <div class="lb-optics-ch">🎯 Challenge: ${esc(p.challenge ? String(p.challenge) : DEFCH())}</div>
  ${modes.length > 1 ? `<div class="lb-optics-tabs">${modes.map(m => `<button class="lb-optics-t" data-mode="${m}">${SHORT[m]}</button>`).join('')}</div>` : ''}
  <svg class="lb-optics-svg" viewBox="0 0 ${W} ${HT}"></svg>
  <div class="lb-optics-media"></div>
  <div class="lb-optics-sl"><span class="lb-optics-sll"></span><input type="range"><b></b></div>
  <div class="lb-optics-out"></div>
</div>`;
      const svg = host.querySelector('svg'), out = host.querySelector('.lb-optics-out'), slider = host.querySelector('input'),
        slVal = host.querySelector('.lb-optics-sl b'), slLab = host.querySelector('.lb-optics-sll'), medEl = host.querySelector('.lb-optics-media');

      // ---- geometry for mirrors / lenses ----
      const geo = () => {
        const lens = /lens/.test(mode);
        const X0 = mode === 'plane' ? 200 : mode === 'concave' ? 240 : mode === 'convex' ? 240 : 176;
        const s = (X0 - 22) / range[1];
        const f = mode === 'plane' ? Infinity : (mode === 'concave' || mode === 'concavelens') ? -F : F;
        return { lens, X0, s, f };
      };
      function optics() {
        const g = geo(), u = -U;
        let v, m, inf = false;
        if (mode === 'plane') { v = U; m = 1; }
        else {
          const inv = g.lens ? 1 / g.f + 1 / u : 1 / g.f - 1 / u;
          if (Math.abs(inv) < 1e-9) { inf = true; v = Infinity; m = Infinity; }
          else { v = 1 / inv; m = g.lens ? v / u : -v / u; }
        }
        const real = !inf && (g.lens ? v > 0 : v < 0);
        return Object.assign(g, { u, v, m, inf, real });
      }

      const arrow = (x1, y1, x2, y2, col, dash, w = 3) => {
        const a = Math.atan2(y2 - y1, x2 - x1), hx = x2 - 9 * Math.cos(a), hy = y2 - 9 * Math.sin(a);
        return `<line x1="${x1}" y1="${y1}" x2="${hx}" y2="${hy}" stroke="${col}" stroke-width="${w}" stroke-linecap="round" ${dash ? 'stroke-dasharray="5 4"' : ''}/>` +
          `<path d="M${x2} ${y2} L${hx - 6 * Math.sin(a)} ${hy + 6 * Math.cos(a)} L${hx + 6 * Math.sin(a)} ${hy - 6 * Math.cos(a)}Z" fill="${col}" ${dash ? 'opacity=".7"' : ''}/>`;
      };
      const midArrow = (x1, y1, x2, y2, col) => {
        const a = Math.atan2(y2 - y1, x2 - x1), mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
        return `<path d="M${mx + 6 * Math.cos(a)} ${my + 6 * Math.sin(a)} L${mx - 5 * Math.cos(a) - 5 * Math.sin(a)} ${my - 5 * Math.sin(a) + 5 * Math.cos(a)} L${mx - 5 * Math.cos(a) + 5 * Math.sin(a)} ${my - 5 * Math.sin(a) - 5 * Math.cos(a)}Z" fill="${col}"/>`;
      };
      const ray = (x1, y1, x2, y2, col, dash) => `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${col}" stroke-width="${dash ? 1.8 : 2.4}" ${dash ? 'stroke-dasharray="4 4" opacity=".75"' : ''} stroke-linecap="round"/>`;

      function drawElement(o) {
        const X = o.X0;
        let el = '';
        const hatch = (side) => { let h = ''; for (let y = 22; y <= 194; y += 12) h += `<line x1="${X + side * 3}" y1="${y}" x2="${X + side * 11}" y2="${y - 7}" stroke="#9aa0c0" stroke-width="1.5"/>`; return h; };
        if (mode === 'plane') el = hatch(1) + `<line x1="${X}" y1="16" x2="${X}" y2="200" stroke="#3b82f6" stroke-width="4" stroke-linecap="round"/>`;
        else if (mode === 'concave') el = `<path d="M${X - 9} 16 Q${X + 9} ${AX} ${X - 9} 200" fill="none" stroke="#9aa0c0" stroke-width="10" stroke-dasharray="1.5 5" transform="translate(6 0)"/><path d="M${X - 9} 16 Q${X + 9} ${AX} ${X - 9} 200" fill="none" stroke="#3b82f6" stroke-width="4" stroke-linecap="round"/>`;
        else if (mode === 'convex') el = `<path d="M${X + 9} 16 Q${X - 9} ${AX} ${X + 9} 200" fill="none" stroke="#9aa0c0" stroke-width="10" stroke-dasharray="1.5 5" transform="translate(6 0)"/><path d="M${X + 9} 16 Q${X - 9} ${AX} ${X + 9} 200" fill="none" stroke="#3b82f6" stroke-width="4" stroke-linecap="round"/>`;
        else if (mode === 'convexlens') el = `<path d="M${X} 18 Q${X + 22} ${AX} ${X} 198 Q${X - 22} ${AX} ${X} 18Z" fill="rgba(59,130,246,.18)" stroke="#3b82f6" stroke-width="2.5"/>`;
        else el = `<path d="M${X - 9} 18 L${X + 9} 18 Q${X + 1} ${AX} ${X + 9} 198 L${X - 9} 198 Q${X - 1} ${AX} ${X - 9} 18Z" fill="rgba(59,130,246,.18)" stroke="#3b82f6" stroke-width="2.5"/>`;
        return el;
      }
      function drawRays() {
        const o = optics(), X0 = o.X0, s = o.s, hp = 34;
        const xo = X0 - U * s, yo = AX - hp;
        let bg = '', rays = '', fg = '';
        bg += `<line x1="0" y1="${AX}" x2="${W}" y2="${AX}" stroke="#c4c8e0" stroke-width="1.5"/>`;
        // focus / centre marks
        if (mode !== 'plane') {
          const pts = o.lens ? [[X0 - F * s, 'F₁'], [X0 + F * s, 'F₂'], [X0 - 2 * F * s, '2F₁'], [X0 + 2 * F * s, '2F₂']] :
            [[X0 + o.f * s, 'F'], [X0 + 2 * o.f * s, 'C']];
          pts.forEach(([x, l]) => { if (x > 4 && x < W - 4) bg += `<circle cx="${x}" cy="${AX}" r="3.5" fill="#6b7090"/><text x="${x}" y="${AX + 17}" text-anchor="middle" font-size="11" font-weight="800" fill="#6b7090">${l}</text>`; });
          bg += `<text x="${X0 + (o.lens ? 0 : -14)}" y="${AX + 17}" text-anchor="middle" font-size="11" font-weight="800" fill="#3b82f6">${o.lens ? 'O' : 'P'}</text>`;
        }
        // rays
        const H1 = [X0, yo], P0 = [X0, AX];
        let d1, d2;
        if (mode === 'plane') d1 = [-1, 0];
        else {
          const Fp = [X0 + o.f * s, AX], k = o.lens ? Math.sign(o.f) : -Math.sign(o.f);
          d1 = [k * (Fp[0] - H1[0]), k * (Fp[1] - H1[1])];
        }
        d2 = o.lens ? [X0 - xo, AX - yo] : [-(X0 - xo), AX - yo];
        const far = (pt, d) => { const L = Math.hypot(d[0], d[1]) || 1; return [pt[0] + d[0] / L * 900, pt[1] + d[1] / L * 900]; };
        const r1 = '#ff9f1c', r2 = '#8b5cf6';
        rays += ray(xo, yo, H1[0], H1[1], r1) + midArrow(xo, yo, H1[0], H1[1], r1);
        rays += ray(xo, yo, P0[0], P0[1], r2) + midArrow(xo, yo, P0[0], P0[1], r2);
        const e1 = far(H1, d1), e2 = far(P0, d2);
        rays += ray(H1[0], H1[1], e1[0], e1[1], r1) + ray(P0[0], P0[1], e2[0], e2[1], r2);
        const xi = o.inf ? NaN : X0 + o.v * s;
        const yi = AX - o.m * hp;
        if (!o.inf && !o.real) { rays += ray(H1[0], H1[1], xi, yi, r1, true) + ray(P0[0], P0[1], xi, yi, r2, true); }
        // object
        fg += `<g>${arrow(xo, AX, xo, yo, '#3b82f6', false, 4)}<circle cx="${xo}" cy="${AX}" r="17" fill="rgba(59,130,246,.14)" stroke="#3b82f6" stroke-width="2"/><text x="${xo}" y="${AX + 4.5}" text-anchor="middle" font-size="12" font-weight="800" fill="#3b82f6">↔</text>` +
          `<text x="${xo}" y="${yo - 7}" text-anchor="middle" font-size="11" font-weight="800" fill="#3b82f6">${esc(objLabel)}</text></g>`;
        // image
        let note = '';
        if (o.inf) note = 'Rays come out parallel → image at infinity';
        else if (xi < -2 || xi > W + 2) note = `Image is far away (v = ${fmt(o.v)} cm) →`;
        else {
          const yy = Math.max(6, Math.min(HT - 6, yi));
          fg += arrow(xi, AX, xi, yy, '#ff6b6b', !o.real, 4);
          fg += `<text x="${Math.max(24, Math.min(W - 24, xi))}" y="${yy < AX ? Math.max(12, yy - 6) : Math.min(HT - 4, yy + 15)}" text-anchor="middle" font-size="11" font-weight="800" fill="#ff6b6b" stroke="#f4f5ff" stroke-width="3" paint-order="stroke">Image</text>`;
          if (yy !== yi) note = 'Image is very large';
        }
        if (note) fg += `<rect x="8" y="${HT - 26}" width="${W - 16}" height="20" rx="8" fill="rgba(255,255,255,.85)"/><text x="${W / 2}" y="${HT - 12}" text-anchor="middle" font-size="11.5" font-weight="800" fill="#ff6b6b">${esc(note)}</text>`;
        svg.innerHTML = `<defs><clipPath id="lbopClip"><rect x="0" y="0" width="${W}" height="${HT}" rx="18"/></clipPath></defs><g clip-path="url(#lbopClip)">${bg}<g>${rays}</g>${drawElement(o)}${fg}</g>`;
        return o;
      }

      // ---- slab ----
      function drawSlab() {
        const n = +media[med].n, r = Math.asin(Math.sin(I * DEG) / n) / DEG;
        const top = 86, bot = 158, hx = 128, tpx = bot - top;
        const din = [Math.sin(I * DEG), Math.cos(I * DEG)];
        const start = [hx - din[0] * 140, top - din[1] * 140];
        const ex = hx + tpx * Math.tan(r * DEG);
        const endE = [ex + din[0] * 160, bot + din[1] * 160];
        const shiftPx = tpx * Math.sin((I - r) * DEG) / Math.cos(r * DEG);
        const shiftCm = thick * Math.sin((I - r) * DEG) / Math.cos(r * DEG);
        const gx = hx + tpx * Math.tan(I * DEG); // where incident line would cross bottom face
        let o = `<defs><clipPath id="lbopClip2"><rect x="0" y="0" width="${W}" height="${HT}" rx="18"/></clipPath><linearGradient id="lbopG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe9ff"/><stop offset="1" stop-color="#a9d6ff"/></linearGradient></defs><g clip-path="url(#lbopClip2)">`;
        o += `<rect x="-5" y="${top}" width="${W + 10}" height="${tpx}" fill="url(#lbopG)" stroke="#3b82f6" stroke-width="2"/>`;
        o += `<text x="${W - 10}" y="${top + 18}" text-anchor="end" font-size="12" font-weight="800" fill="#2563c9">${esc(media[med].name)} (n = ${fmt(n, 2)})</text><text x="${W - 10}" y="${top - 8}" text-anchor="end" font-size="12" font-weight="800" fill="#6b7090">Air</text>`;
        o += `<line x1="${hx}" y1="${top - 60}" x2="${hx}" y2="${top + 50}" stroke="#6b7090" stroke-width="1.5" stroke-dasharray="4 4"/>`;
        o += `<line x1="${ex}" y1="${bot - 40}" x2="${ex}" y2="${bot + 60}" stroke="#6b7090" stroke-width="1.5" stroke-dasharray="4 4"/>`;
        // incident extension (dashed) to show lateral shift
        o += ray(hx, top, gx + din[0] * 70, bot + din[1] * 70, '#ff9f1c', true);
        o += ray(start[0], start[1], hx, top, '#ff9f1c') + midArrow(start[0] + (hx - start[0]) * .3, start[1] + (top - start[1]) * .3, hx, top, '#ff9f1c');
        o += ray(hx, top, ex, bot, '#8b5cf6');
        o += ray(ex, bot, endE[0], endE[1], '#ff6b6b') + midArrow(ex, bot, ex + din[0] * 70, bot + din[1] * 70, '#ff6b6b');
        // angle arcs
        const arc = (cx, cy, a0, a1, rad, col) => { const p0 = [cx + rad * Math.sin(a0 * DEG), cy + rad * Math.cos(a0 * DEG)], p1 = [cx + rad * Math.sin(a1 * DEG), cy + rad * Math.cos(a1 * DEG)]; return `<path d="M${p0[0]} ${p0[1]} A${rad} ${rad} 0 0 ${a1 > a0 ? 0 : 1} ${p1[0]} ${p1[1]}" fill="none" stroke="${col}" stroke-width="2"/>`; };
        if (I > 2) {
          o += `<path d="M${hx} ${top - 30} A30 30 0 0 0 ${hx - 30 * Math.sin(I * DEG)} ${top - 30 * Math.cos(I * DEG)}" fill="none" stroke="#ff9f1c" stroke-width="2"/>`;
          o += `<text x="${hx - 12 - 8 * Math.sin(I * DEG)}" y="${top - 36}" text-anchor="end" font-size="12" font-weight="800" fill="#e8890c">i</text>`;
          o += arc(hx, top, 0, r, 34, '#8b5cf6') + `<text x="${hx + 6 + 26 * Math.sin(r * DEG / 2)}" y="${top + 46}" font-size="12" font-weight="800" fill="#8b5cf6">r</text>`;
          o += arc(ex, bot, 0, I, 30, '#ff6b6b') + `<text x="${ex + 6 + 28 * Math.sin(I * DEG / 2)}" y="${bot + 42}" font-size="12" font-weight="800" fill="#ff6b6b">e</text>`;
        }
        // lateral shift marker
        if (shiftPx > 4) {
          const q = [ex + din[0] * 40, bot + din[1] * 40];
          const nrm = [din[1], -din[0]];
          o += `<line x1="${q[0]}" y1="${q[1]}" x2="${q[0] + nrm[0] * shiftPx}" y2="${q[1] + nrm[1] * shiftPx}" stroke="#1b1f3a" stroke-width="1.5"/>`;
        }
        o += `<circle cx="${hx - din[0] * 62}" cy="${top - din[1] * 62}" r="13" fill="rgba(255,159,28,.18)" stroke="#ff9f1c" stroke-width="2"/></g>`;
        svg.innerHTML = o;
        return { n, r, shiftCm };
      }

      function setupSlider() {
        if (mode === 'slab') {
          slLab.textContent = 'Angle i'; slider.min = 0; slider.max = 80; slider.step = 1; slider.value = I;
          medEl.style.display = media.length > 1 ? 'flex' : 'none';
          medEl.innerHTML = media.map((m, k) => `<button class="lb-optics-t ${k === med ? 'on' : ''}" data-med="${k}">${esc(m.name)}</button>`).join('');
        } else {
          slLab.textContent = 'Distance'; slider.min = range[0]; slider.max = range[1]; slider.step = step; slider.value = U;
          medEl.style.display = 'none';
        }
        host.querySelectorAll('[data-mode]').forEach(b => b.classList.toggle('on', b.dataset.mode === mode));
      }

      function check(o) {
        if (won || !touched || goal.includes('none')) return;
        let ok = true, msg = '';
        if (mode === 'slab') {
          ok = goal.includes('r') && Math.abs(o.r - target) < 0.6;
          msg = `sin ${fmt(I, 0)}° ÷ sin ${fmt(o.r)}° = ${fmt(o.n, 2)} — the ray bends towards the normal in the denser medium.`;
        } else {
          const am = Math.abs(o.m);
          for (const g of goal) {
            if (g === 'real') ok = ok && o.real;
            else if (g === 'virtual') ok = ok && !o.inf && !o.real;
            else if (g === 'magnified') ok = ok && !o.inf && am > 1.02;
            else if (g === 'diminished') ok = ok && !o.inf && am < 0.98;
            else if (g === 'same') ok = ok && !o.inf && Math.abs(am - 1) < 0.02;
            else if (g === 'erect') ok = ok && !o.inf && o.m > 0;
            else if (g === 'inverted') ok = ok && !o.inf && o.m < 0;
            else if (g === 'infinity') ok = ok && o.inf;
            else if (g === 'v') ok = ok && !o.inf && Math.abs(Math.abs(o.v) - target) < 0.5;
            else if (g === 'gap') ok = ok && !o.inf && Math.abs(Math.abs(o.v - o.u) - target) < 0.5;
            else if (g === 'r') ok = false;
          }
          msg = o.inf ? `u = ${fmt(o.u)} cm = f, so the reflected/refracted rays are parallel: image at infinity.`
            : `u = ${fmt(o.u)} cm, v = ${sgn(o.v)} cm, m = ${sgn(o.m === 1 ? 1 : o.m)} → ${natural(o)} image.`;
        }
        if (ok) { won = true; api.sfx('correct'); api.win(p.winText ? String(p.winText) : msg); }
      }
      function natural(o) {
        if (o.inf) return 'highly enlarged, at infinity';
        const am = Math.abs(o.m);
        return [o.real ? 'real' : 'virtual', o.m < 0 ? 'inverted' : 'erect', Math.abs(am - 1) < 0.02 ? 'same size' : am > 1 ? 'magnified' : 'diminished'].join(', ');
      }

      function update() {
        if (mode === 'slab') {
          const o = drawSlab();
          slVal.textContent = `${fmt(I, 0)}°`;
          out.innerHTML = `<div class="lb-optics-vals"><span>i = ${fmt(I, 0)}°</span><span>r = ${fmt(o.r)}°</span><span>e = ${fmt(I, 0)}°</span><span>shift = ${fmt(o.shiftCm, 2)} cm</span></div>
<div class="lb-optics-nat">${I === 0 ? 'Along the normal: no bending.' : 'Bends towards the normal going in, away coming out.'}</div>
<div class="lb-optics-f">Snell's law: n = sin i ÷ sin r = ${fmt(Math.sin(I * DEG), 3)} ÷ ${fmt(Math.sin(o.r * DEG), 3)} = ${fmt(o.n, 2)} · slab ${fmt(thick)} cm thick</div>`;
          check(o); return;
        }
        const o = drawRays();
        slVal.textContent = `${fmt(U)} cm`;
        const fStr = mode === 'plane' ? '∞' : `${sgn(o.f)} cm`;
        out.innerHTML = `<div class="lb-optics-vals"><span>u = ${fmt(o.u)} cm</span><span>v = ${o.inf ? '∞' : sgn(o.v) + ' cm'}</span><span>f = ${fStr}</span><span>m = ${o.inf ? '∞' : sgn(o.m)}</span></div>
<div class="lb-optics-nat">${NAMES[mode]}: ${natural(o)}</div>
<div class="lb-optics-f">${mode === 'plane' ? 'Image is as far behind the mirror as the object is in front.' : o.lens ? '1/v − 1/u = 1/f · m = v/u (New Cartesian signs)' : '1/v + 1/u = 1/f · m = −v/u (New Cartesian signs)'}</div>`;
        check(o);
      }

      // ---- interaction ----
      let drag = false;
      const pt = e => { const m = svg.getScreenCTM(); if (!m) return null; const q = new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse()); return q; };
      function applyPointer(e) {
        const q = pt(e); if (!q) return;
        if (mode === 'slab') {
          const hx = 128, top = 86;
          if (q.y >= top - 2) return;
          const a = Math.atan2(hx - q.x, top - q.y) / DEG;
          const ni = Math.max(0, Math.min(80, Math.round(a)));
          if (ni !== I) { I = ni; slider.value = I; touched = true; update(); }
        } else {
          const g = geo();
          const nu = clampU((g.X0 - q.x) / g.s);
          if (nu !== U) { U = nu; slider.value = U; touched = true; update(); }
        }
      }
      const down = e => { drag = true; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); applyPointer(e); };
      const move = e => { if (drag) applyPointer(e); };
      const up = () => { drag = false; };
      svg.addEventListener('pointerdown', down); svg.addEventListener('pointermove', move);
      svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
      slider.addEventListener('input', () => { if (mode === 'slab') I = +slider.value; else U = +slider.value; touched = true; update(); });
      const onClick = e => {
        const b = e.target.closest('button'); if (!b) return;
        if (b.dataset.mode) { mode = b.dataset.mode; api.sfx('tap'); setupSlider(); update(); }
        else if (b.dataset.med !== undefined) { med = +b.dataset.med; touched = true; api.sfx('tap'); setupSlider(); update(); }
      };
      host.addEventListener('click', onClick);
      setupSlider(); update();
      return () => {
        svg.removeEventListener('pointerdown', down); svg.removeEventListener('pointermove', move);
        svg.removeEventListener('pointerup', up); svg.removeEventListener('pointercancel', up); host.removeEventListener('click', onClick);
      };
    },
    example: {
      mode: 'concave',
      modes: ['concave', 'convex', 'plane'],
      f: 15, u: 40, range: [5, 60],
      goal: 'real-magnified',
      objectLabel: 'Candle',
      challenge: 'Move the candle so the concave mirror forms a real, magnified image.'
    },
    examples: [
      { mode: 'plane', modes: ['plane'], u: 15, range: [5, 40], goal: 'gap', target: 50, objectLabel: 'Toy', challenge: 'Grade 7: Move the toy so its image is 50 cm away from the toy.' },
      { mode: 'convexlens', modes: ['convexlens', 'concavelens'], f: 10, u: 35, range: [4, 40], goal: 'same', objectLabel: 'Object', challenge: 'Grade 10: Where must the object be for the convex lens to make a same-size image?' },
      { mode: 'slab', modes: ['slab'], i: 20, goal: 'r', target: 30, challenge: 'Grade 10: Change the angle of incidence so the ray inside the glass makes 30° with the normal.' }
    ]
  });
})();
