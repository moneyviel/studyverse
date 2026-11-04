/* StudyVerse Concept Lab: circlelab — "Circle lab"
 * The child drags points on a circle (and its radius handle) to explore the parts of a circle,
 * circumference and area, arc length and sector area, and the angle theorems.
 *
 * PARAMS (all optional; defaults in brackets)
 *  mode        string  'parts' | 'measure' | 'sector' | 'theorem'                         ['parts']
 *                      parts   = centre, radius, diameter, chord, arc, sector, segment, tangent
 *                      measure = drag the radius; live C = 2πr and A = πr²
 *                      sector  = drag the radius and the arc end; arc length and sector area
 *                      theorem = A, B, P on the circle; angle at centre = 2 × angle at circumference
 *  parts       array   parts mode: which part buttons to show
 *                      ['centre','radius','diameter','chord','arc','sector','segment','tangent']
 *  part        string  parts mode: part shown first                                         ['chord']
 *  find        array   parts mode quiz: parts the child must tap on a labelled-free circle,
 *                      e.g. ['chord','radius','sector'] (when given, this is the challenge)   [none]
 *  goal        string  parts: 'diameter' (make the longest chord) [default]
 *                      theorem: 'target' (make ∠AOB = target) [default] | 'semicircle' (make ∠APB = 90°)
 *  r           number  starting radius (measure/sector)                                    [7]
 *  rRange      array   [min, max] radius (measure/sector)                                   [[1,10]]
 *  step        number  radius step                                                          [0.5]
 *  pi          string|number  value of π used in working: '22/7' | 3.14 | 'pi'              ['22/7']
 *  unit        string  length unit                                                          ['cm']
 *  target      number  theorem: target ∠AOB in degrees                                      [100]
 *  targetC     number  measure: target circumference
 *  targetA     number  measure: target area                    (default targetC = 44)
 *  targetR     number  measure: target radius
 *  targetAngle number  sector: target sector angle in degrees                               [90]
 *  targetArc   number  sector: target arc length
 *  targetSector number sector: target sector area
 *  challenge   string  challenge text (English or Hindi); default is generated
 *  winText     string  message on success
 */
(function () {
  const C = { violet: '#8b5cf6', mint: '#2ed3a5', sun: '#ffc93c', coral: '#ff6b6b', blue: '#3b82f6', ink: '#1b1f3a', muted: '#6b7090' };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const f2 = n => (Math.round(n * 100) / 100).toString();
  const rad = d => d * Math.PI / 180, norm = a => ((a % 360) + 360) % 360;
  const NAMES = { centre: 'Centre', radius: 'Radius', diameter: 'Diameter', chord: 'Chord', arc: 'Arc', sector: 'Sector', segment: 'Segment', tangent: 'Tangent' };
  const DEFS = {
    centre: 'The centre O is the same distance from every point on the circle.',
    radius: 'A radius joins the centre to a point on the circle. All radii are equal.',
    diameter: 'A diameter is a chord through the centre. Diameter = 2 × radius.',
    chord: 'A chord joins two points on the circle. The longest chord is the diameter.',
    arc: 'An arc is a part of the circle. The shorter one is the minor arc.',
    sector: 'A sector is the region between two radii and an arc (like a pizza slice).',
    segment: 'A segment is the region between a chord and an arc.',
    tangent: 'A tangent touches the circle at only one point. It is ⟂ to the radius there.'
  };
  const CSS = `
.lb-circlelab-w{font-size:14px;color:${C.ink}}
.lb-circlelab-ch{background:#fff6d8;border-radius:12px;padding:6px 6px 6px 11px;font-weight:800;font-size:14px;margin-bottom:8px;line-height:1.3;display:flex;align-items:center;gap:8px}
.lb-circlelab-ch span{flex:1}
.lb-circlelab-ch .lb-circlelab-b{flex-shrink:0;font-size:13px;padding:0 10px}
.lb-circlelab-svg{width:100%;height:auto;display:block;touch-action:none;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:18px;user-select:none;-webkit-user-select:none}
.lb-circlelab-svg text{font-family:inherit;pointer-events:none}
.lb-circlelab-chips{display:flex;gap:5px;overflow-x:auto;margin-bottom:8px;padding-bottom:2px;scrollbar-width:none}
.lb-circlelab-chips::-webkit-scrollbar{display:none}
.lb-circlelab-b{min-height:40px;border:none;border-radius:12px;background:#f1efff;color:${C.ink};font:inherit;font-weight:800;font-size:13px;padding:0 11px;cursor:pointer}
.lb-circlelab-chips .lb-circlelab-b{min-height:40px;font-size:12.5px;padding:0 10px;flex-shrink:0}
.lb-circlelab-b.on{background:${C.violet};color:#fff}
.lb-circlelab-b.go{background:${C.violet};color:#fff}
.lb-circlelab-b:active{transform:scale(.95)}
.lb-circlelab-read{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px}
.lb-circlelab-c{background:#f4f6ff;border-radius:12px;padding:6px 9px;font-weight:800;font-size:13px;line-height:1.35}
.lb-circlelab-c.wide{grid-column:1/-1}
.lb-circlelab-c small{display:block;color:${C.muted};font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.3px}
.lb-circlelab-row{display:flex;gap:6px;margin-top:8px}
@keyframes lbcirclepulse{50%{r:9}}
.lb-circlelab-pulse{animation:lbcirclepulse 1.2s ease-in-out infinite}
`;

  function render(host, p, api) {
    const mode = ['parts', 'measure', 'sector', 'theorem'].includes(p.mode) ? p.mode : 'parts';
    const unitS = p.unit != null ? esc(p.unit) : "cm";
    const piMode = p.pi === 'pi' ? 'pi' : (p.pi === 3.14 || p.pi === '3.14') ? '3.14' : '22/7';
    const PI = piMode === 'pi' ? Math.PI : piMode === '3.14' ? 3.14 : 22 / 7;
    const piS = piMode === 'pi' ? 'π' : piMode;
    const rr = Array.isArray(p.rRange) && p.rRange.length === 2 ? [Math.max(0.1, +p.rRange[0] || 1), Math.max(+p.rRange[1] || 10, (+p.rRange[0] || 1) + 1)] : [1, 10];
    const step = +p.step > 0 ? +p.step : 0.5;
    let r = Math.max(rr[0], Math.min(rr[1], +p.r || 7));
    let challengeText = p.challenge ? String(p.challenge) : null, won = false;

    const cx = 180, cy = mode === 'measure' ? 98 : 129, H = mode === 'measure' ? 236 : 256;
    const RP = mode === 'parts' || mode === 'theorem' ? 100 : 0; // fixed pixel radius
    const scale = mode === 'measure' ? 88 / rr[1] : 100 / rr[1];
    const Rpx = () => RP || r * scale;
    const at = (a, R) => [cx + (R == null ? Rpx() : R) * Math.cos(rad(a)), cy - (R == null ? Rpx() : R) * Math.sin(rad(a))];
    const F = q => q[0].toFixed(1) + ' ' + q[1].toFixed(1);

    // state
    const partList = (Array.isArray(p.parts) && p.parts.length ? p.parts : Object.keys(NAMES)).filter(k => NAMES[k]);
    let part = NAMES[p.part] ? p.part : (partList.includes('chord') ? 'chord' : partList[0]);
    const findList = Array.isArray(p.find) ? p.find.filter(k => NAMES[k]) : [];
    let quiz = mode === 'parts' && findList.length > 0, qi = 0, found = new Set();
    let A = mode === 'theorem' ? 200 : mode === 'sector' ? 0 : 210, B = mode === 'theorem' ? 340 : mode === 'sector' ? 120 : 330, Pa = 90;
    let goal = p.goal || (mode === 'theorem' ? 'target' : 'diameter');
    let target = +p.target || 100;
    let mGoal = p.targetR != null ? ['r', +p.targetR] : p.targetA != null ? ['A', +p.targetA] : p.targetC != null ? ['C', +p.targetC] : ['C', 44];
    let sGoal = p.targetArc != null ? ['arc', +p.targetArc] : p.targetSector != null ? ['area', +p.targetSector] : ['angle', p.targetAngle != null ? +p.targetAngle : 90];

    host.innerHTML = `<style>${CSS}</style><div class="lb-circlelab-w">
      <div class="lb-circlelab-ch"><span></span><button class="lb-circlelab-b go" data-new aria-label="New challenge">🔄 New</button></div>
      ${mode === 'parts' ? `<div class="lb-circlelab-chips">${quiz ? '<button class="lb-circlelab-b" data-p="quiz">Quiz ❓</button>' : ''}${partList.map(k => `<button class="lb-circlelab-b" data-p="${k}">${NAMES[k]}</button>`).join('')}</div>` : ''}
      <svg class="lb-circlelab-svg" viewBox="0 0 360 ${H}"></svg>
      <div class="lb-circlelab-read"></div>
</div>`;
    const svg = host.querySelector('svg'), rd = host.querySelector('.lb-circlelab-read'), chEl = host.querySelector('.lb-circlelab-ch span');

    // ----- helpers -----
    function arcD(a0, a1, R) { const s = norm(a1 - a0); if (s < 0.01) return ''; if (s > 359.99) return `M${cx + R} ${cy} A${R} ${R} 0 1 0 ${cx - R} ${cy} A${R} ${R} 0 1 0 ${cx + R} ${cy}`; return `M${F(at(a0, R))} A${R} ${R} 0 ${s > 180 ? 1 : 0} 0 ${F(at(a1, R))}`; }
    function wedgeAt(V, R, a0, a1) { const s = norm(a1 - a0), p0 = [V[0] + R * Math.cos(rad(a0)), V[1] - R * Math.sin(rad(a0))], p1 = [V[0] + R * Math.cos(rad(a1)), V[1] - R * Math.sin(rad(a1))]; return `M${F(V)} L${F(p0)} A${R} ${R} 0 ${s > 180 ? 1 : 0} 0 ${F(p1)}Z`; }
    const dirTo = (V, Q) => norm(Math.atan2(-(Q[1] - V[1]), Q[0] - V[0]) * 180 / Math.PI);
    const ln = (a, b, col, w = 3.5, extra = '') => `<line x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}" stroke="${col}" stroke-width="${w}" stroke-linecap="round" ${extra}/>`;
    const dot = (q, col = C.violet) => `<circle cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="11" fill="${col}" stroke="#fff" stroke-width="3" style="filter:drop-shadow(0 2px 2px rgba(80,60,180,.35))"/>`;
    const txt = (q, t, col = C.ink, size = 14) => `<text x="${q[0].toFixed(1)}" y="${(q[1] + size / 3).toFixed(1)}" font-size="${size}" font-weight="800" fill="${col}" text-anchor="middle" stroke="#fff" stroke-width="3.5" paint-order="stroke">${t}</text>`;
    const minorArc = () => { const d = norm(B - A); return d <= 180 ? [A, B, d] : [B, A, 360 - d]; };
    const cell = (label, val, wide) => `<div class="lb-circlelab-c ${wide ? 'wide' : ''}"><small>${label}</small>${val}</div>`;
    const chordLen = th => 2 * Math.sin(rad(th) / 2); // in radii

    // ----- draw -----
    function draw() {
      let s = '';
      const R = Rpx();
      s += `<circle cx="${cx}" cy="${cy}" r="${R.toFixed(1)}" fill="#fff" stroke="${C.ink}" stroke-width="3"/>`;
      if (mode === 'parts') s += quiz ? drawQuiz() : drawPart();
      else if (mode === 'measure') {
        const E = at(30);
        s += ln([cx, cy], E, C.violet) + ln(at(180), at(0), C.blue, 2, 'stroke-dasharray="6 5"');
        if (R >= 48) s += txt(at(30, R / 2).map((v, i) => v + (i ? -12 : -4)), `r = ${f2(r)}`, C.violet, 13) + txt([cx - R / 2, cy + 16], `d = ${f2(2 * r)}`, C.blue, 12);
        else s += txt([at(30)[0] + 26, at(30)[1] - 20], `r = ${f2(r)}`, C.violet, 13);
        s += `<circle cx="${cx}" cy="${cy}" r="4" fill="${C.ink}"/>` + dot(E);
        // C ≈ π × d strip: how many diameters fit round the circle
        const k = 300 / (2 * Math.PI * 88), dpx = 2 * R * k, by = 212, x0 = 15;
        s += `<text x="${x0}" y="${by - 12}" font-size="11.5" font-weight="800" fill="${C.muted}">Circle unrolled: C = ${piS} × d (about 3.14 diameters)</text>`;
        const total = Math.PI * dpx;
        s += `<rect x="${x0}" y="${by}" width="${total.toFixed(1)}" height="12" rx="6" fill="${C.mint}" opacity=".35"/>`;
        for (let i = 0; i < 3; i++) s += `<rect x="${(x0 + i * dpx + 1).toFixed(1)}" y="${by + 1}" width="${(dpx - 2).toFixed(1)}" height="10" rx="5" fill="${C.blue}" opacity=".8"/>`;
        s += `<text x="${(x0 + total + 6).toFixed(1)}" y="${by + 10}" font-size="11" font-weight="800" fill="#0f9d7a">${f2(2 * PI * r)}</text>`;
      } else if (mode === 'sector') {
        const th = norm(B - A) || 360;
        s += `<path d="${th >= 360 ? `M${cx} ${cy} ` + arcD(0, 360, R) : wedgeAt([cx, cy], R, A, B)}" fill="${C.sun}" fill-opacity=".45"/>`;
        s += `<path d="${arcD(A, A + th, R)}" fill="none" stroke="${C.coral}" stroke-width="6" stroke-linecap="round"/>`;
        s += ln([cx, cy], at(A), C.violet) + ln([cx, cy], at(B), C.violet);
        s += `<path d="${arcD(A, A + th, 22).replace(/^M/, 'M')}" fill="none" stroke="${C.ink}" stroke-width="2"/>`;
        s += txt(at(A + th / 2, th < 40 ? 44 : 38), `${Math.round(th)}°`, C.ink, 13);
        s += `<circle cx="${cx}" cy="${cy}" r="4" fill="${C.ink}"/>` + dot(at(A), C.blue) + dot(at(B));
        s += txt([at(A)[0] - 6, at(A)[1] + 22], `r = ${f2(r)}`, C.blue, 12);
      } else {
        // theorem
        const [s0, s1] = arcNotP(), x = norm(s1 - s0);
        const Ap = at(A), Bp = at(B), Pp = at(Pa), O = [cx, cy];
        s += `<path d="${arcD(s0, s1, R)}" fill="none" stroke="${C.coral}" stroke-width="6" stroke-linecap="round" opacity=".8"/>`;
        s += `<path d="${wedgeAt(O, 26, s0, s1)}" fill="${C.violet}" fill-opacity=".3"/>`;
        const pa0 = dirTo(Pp, Bp), pa1 = dirTo(Pp, Ap); let st = pa0, en = pa1; if (norm(en - st) > 180) { st = pa1; en = pa0; }
        const inscribed = x / 2;
        if (Math.abs(inscribed - 90) < 0.01) { const u1 = unit(Pp, Ap), u2 = unit(Pp, Bp), q = 12; s += `<path d="M${Pp[0] + u1[0] * q} ${Pp[1] + u1[1] * q} L${Pp[0] + (u1[0] + u2[0]) * q} ${Pp[1] + (u1[1] + u2[1]) * q} L${Pp[0] + u2[0] * q} ${Pp[1] + u2[1] * q}" fill="none" stroke="#0f9d7a" stroke-width="2.5"/>`; }
        else s += `<path d="${wedgeAt(Pp, 26, st, en)}" fill="${C.mint}" fill-opacity=".45"/>`;
        s += ln(O, Ap, C.violet, 3) + ln(O, Bp, C.violet, 3) + ln(Pp, Ap, '#0f9d7a', 3) + ln(Pp, Bp, '#0f9d7a', 3);
        const mo = s0 + x / 2; s += txt(at(mo, 46), `${Math.round(x)}°`, '#6d3fe0', 13);
        const mp = st + norm(en - st) / 2; s += txt([Pp[0] + 46 * Math.cos(rad(mp)), Pp[1] - 46 * Math.sin(rad(mp))], `${f2(inscribed)}°`, '#0f9d7a', 13);
        s += `<circle cx="${cx}" cy="${cy}" r="4" fill="${C.ink}"/>` + txt(at(mo + 180, 16), 'O', C.ink, 13);
        [[Ap, 'A', A], [Bp, 'B', B], [Pp, 'P', Pa]].forEach(([q, n, a]) => { s += dot(q, n === 'P' ? '#0f9d7a' : C.violet) + txt(at(a, 119), n, C.ink, 14); });
      }
      svg.innerHTML = s;
      readout();
    }
    function unit(V, Q) { const dx = Q[0] - V[0], dy = Q[1] - V[1], l = Math.hypot(dx, dy) || 1; return [dx / l, dy / l]; }
    function arcNotP() { // arc from A to B (CCW) that does not contain P
      const ab = norm(B - A), ap = norm(Pa - A);
      return ap > ab ? [A, B] : [B, A];
    }
    function drawPart() {
      let s = ''; const O = [cx, cy], Ap = at(A), Bp = at(B), [m0, m1, th] = minorArc();
      switch (part) {
        case 'centre': s += `<circle class="lb-circlelab-pulse" cx="${cx}" cy="${cy}" r="6" fill="${C.coral}"/>` + txt([cx, cy + 22], 'O', C.ink); for (let a = 0; a < 360; a += 45) s += ln(O, at(a, 96), '#c9c3f7', 1.5, 'stroke-dasharray="3 4"'); return s;
        case 'radius': s += ln(O, Ap, C.violet, 4) + txt(at(A, 50).map((v, i) => v + (i ? -10 : 0)), 'r', C.violet); break;
        case 'diameter': { const D = at(A + 180); s += ln(D, Ap, C.blue, 4) + txt(at(A + 90, 18), 'd = 2r', C.blue, 12) + dot(D, C.blue) + txt(at(A + 180, 122), 'A′'); break; }
        case 'chord': s += ln(Ap, Bp, C.coral, 4); break;
        case 'arc': s += `<path d="${arcD(m0, m1, 100)}" fill="none" stroke="${C.coral}" stroke-width="8" stroke-linecap="round"/><path d="${arcD(m1, m0 + 360, 100)}" fill="none" stroke="${C.blue}" stroke-width="3" stroke-dasharray="8 6"/>` + txt(at(m0 + th / 2, 80), 'minor', C.coral, 12) + txt(at(m0 + th / 2 + 180, 80), 'major', C.blue, 12); break;
        case 'sector': s += `<path d="${wedgeAt(O, 100, m0, m1)}" fill="${C.sun}" fill-opacity=".6" stroke="${C.ink}" stroke-width="2"/>`; break;
        case 'segment': s += `<path d="M${F(at(m0))} A100 100 0 0 0 ${F(at(m1))}Z" fill="${C.mint}" fill-opacity=".55"/>` + ln(Ap, Bp, C.ink, 2.5); break;
        case 'tangent': { const t1 = [Ap[0] + 140 * Math.cos(rad(A + 90)), Ap[1] - 140 * Math.sin(rad(A + 90))], t2 = [Ap[0] - 140 * Math.cos(rad(A + 90)), Ap[1] + 140 * Math.sin(rad(A + 90))];
          s += ln(O, Ap, C.violet, 2.5, 'stroke-dasharray="6 5"') + ln(t1, t2, C.coral, 4);
          const u1 = unit(Ap, O), u2 = [Math.cos(rad(A + 90)), -Math.sin(rad(A + 90))], q = 12;
          s += `<path d="M${Ap[0] + u1[0] * q} ${Ap[1] + u1[1] * q} L${Ap[0] + (u1[0] + u2[0]) * q} ${Ap[1] + (u1[1] + u2[1]) * q} L${Ap[0] + u2[0] * q} ${Ap[1] + u2[1] * q}" fill="none" stroke="${C.ink}" stroke-width="2"/>`; break; }
      }
      s += `<circle cx="${cx}" cy="${cy}" r="4" fill="${C.ink}"/>` + txt([cx, cy + 20], 'O', C.ink, 13);
      s += dot(Ap) + txt(at(A, 122), 'A');
      if (['chord', 'arc', 'sector', 'segment'].includes(part)) s += dot(Bp) + txt(at(B, 122), 'B');
      return s;
    }
    // quiz layout: all parts shown, unlabelled, each tappable
    const QZ = { diameter: [150, 330], radius: [62], chord: [190, 270], sector: [5, 45], arc: [95, 132], tangent: [300] };
    function drawQuiz() {
      const O = [cx, cy], hit = (k, d, extra = '') => `<g data-part="${k}" style="cursor:pointer">${d}${extra}</g>`;
      const col = k => found.has(k) ? '#0f9d7a' : C.ink, fill = (k, c) => found.has(k) ? '#a8ecd6' : c;
      let s = '';
      s += hit('sector', `<path d="${wedgeAt(O, 100, QZ.sector[0], QZ.sector[1])}" fill="${fill('sector', '#ffe7a3')}" stroke="${col('sector')}" stroke-width="2"/>`);
      s += hit('segment', `<path d="M${F(at(QZ.chord[0]))} A100 100 0 0 0 ${F(at(QZ.chord[1]))}Z" fill="${fill('segment', '#d8f5ec')}"/>`);
      s += hit('chord', ln(at(QZ.chord[0]), at(QZ.chord[1]), col('chord'), 3.5) + ln(at(QZ.chord[0]), at(QZ.chord[1]), 'transparent', 12));
      s += hit('diameter', ln(at(QZ.diameter[0]), at(QZ.diameter[1]), col('diameter'), 3.5) + ln(at(QZ.diameter[0]), at(QZ.diameter[1]), 'transparent', 18));
      s += hit('radius', ln(O, at(QZ.radius[0]), col('radius'), 3.5) + ln(O, at(QZ.radius[0]), 'transparent', 18));
      s += hit('arc', `<path d="${arcD(QZ.arc[0], QZ.arc[1], 100)}" fill="none" stroke="${found.has('arc') ? '#0f9d7a' : C.coral}" stroke-width="7" stroke-linecap="round"/><path d="${arcD(QZ.arc[0], QZ.arc[1], 100)}" fill="none" stroke="transparent" stroke-width="22"/>`);
      const T = at(QZ.tangent[0]), td = [Math.cos(rad(QZ.tangent[0] + 90)), -Math.sin(rad(QZ.tangent[0] + 90))];
      const t1 = [T[0] + td[0] * 75, T[1] + td[1] * 75], t2 = [T[0] - td[0] * 60, T[1] - td[1] * 60];
      s += hit('tangent', ln(t1, t2, col('tangent'), 3.5) + ln(t1, t2, 'transparent', 18));
      s += hit('centre', `<circle cx="${cx}" cy="${cy}" r="16" fill="transparent"/><circle cx="${cx}" cy="${cy}" r="5.5" fill="${col('centre')}"/>`);
      found.forEach(k => { const pos = { centre: [cx + 14, cy + 20], radius: at(QZ.radius[0], 60).map((v, i) => v + (i ? 0 : 22)), diameter: at(QZ.diameter[0], 62).map((v, i) => v + (i ? -10 : 0)), chord: at((QZ.chord[0] + QZ.chord[1]) / 2, 64), segment: at((QZ.chord[0] + QZ.chord[1]) / 2, 90), sector: at(25, 62), arc: at(113, 116), tangent: T.map((v, i) => v + td[i] * 64 + (i ? -12 : 0)) }[k]; s += txt(pos, NAMES[k] + ' ✓', '#0f9d7a', 11); });
      return s;
    }

    // ----- readout -----
    function readout() {
      let h = '';
      if (mode === 'parts') {
        if (quiz) {
          h = qi < findList.length ? cell('Find it', `Tap the <span style="color:${C.violet}">${NAMES[findList[qi]].toUpperCase()}</span> on the circle (${qi + 1}/${findList.length})`, 1) : cell('Well done', 'You found every part!', 1);
        } else {
          const [, , th] = minorArc(), RR = 5; // the parts view uses a 5 cm radius for its numbers
          let st = '';
          if (part === 'radius' || part === 'diameter' || part === 'centre') st = `If r = ${RR} ${unitS}, diameter d = 2r = ${2 * RR} ${unitS}`;
          if (part === 'chord' || part === 'segment') st = `If r = ${RR} ${unitS}: chord AB = ${f2(RR * chordLen(th))} ${unitS}, diameter = ${2 * RR} ${unitS}`;
          if (part === 'arc' || part === 'sector') st = `Minor arc AB = ${Math.round(th)}°, major arc = ${360 - Math.round(th)}° (total 360°)`;
          if (part === 'tangent') st = 'Radius ⟂ tangent: they meet at 90°';
          h = cell(NAMES[part], `${DEFS[part]}<br><span style="color:${C.violet}">${st}</span>`, 1);
        }
      } else if (mode === 'measure') {
        h = cell('Radius & diameter', `r = ${f2(r)} ${unitS} · d = 2r = ${f2(2 * r)} ${unitS}`, 1);
        h += cell('Circumference', `C = 2 × ${piS} × ${f2(r)}<br>= <b style="color:#0f9d7a">${f2(2 * PI * r)} ${unitS}</b>`);
        h += cell('Area', `A = ${piS} × ${f2(r)} × ${f2(r)}<br>= <b style="color:${C.violet}">${f2(PI * r * r)} sq ${unitS}</b>`);
      } else if (mode === 'sector') {
        const th = norm(B - A) || 360;
        h = cell('Sector angle', `θ = ${Math.round(th)}° <span style="color:${C.muted}">(${fracOf(th)} of circle)</span>`, 1);
        h += cell('Arc length', `θ/360 × 2${piS === 'π' ? 'π' : ' × ' + piS + ' × '}r = <b style="color:${C.coral}">${f2(th / 360 * 2 * PI * r)} ${unitS}</b>`, 1);
        h += cell('Sector area', `θ/360 × ${piS === 'π' ? 'π' : piS + ' × '}r² = <b style="color:#b07d00">${f2(th / 360 * PI * r * r)} sq ${unitS}</b>`, 1);
      } else {
        const [s0, s1] = arcNotP(), x = norm(s1 - s0);
        h = cell('At centre', `∠AOB = <b style="color:#6d3fe0">${Math.round(x)}°</b>${x > 180 ? ' (reflex)' : ''}`) + cell('At circumference', `∠APB = <b style="color:#0f9d7a">${f2(x / 2)}°</b>`);
        h += cell('Theorem', Math.round(x) === 180 ? 'AB is a diameter: the angle in a semicircle is 90°!' : `∠AOB = 2 × ∠APB, so ${Math.round(x)}° = 2 × ${f2(x / 2)}°. Move P along the arc: ∠APB stays the same!`, 1);
      }
      rd.innerHTML = h;
    }
    function fracOf(th) { const g = (a, b) => b ? g(b, a % b) : a, t = Math.round(th), k = g(t, 360); return `${t / k}/${360 / k}`; }

    // ----- challenge -----
    function chText() {
      if (challengeText) return challengeText;
      if (mode === 'parts') return quiz ? `Find ${findList.length} parts of the circle` : 'Drag A and B to make the longest possible chord';
      if (mode === 'measure') return mGoal[0] === 'r' ? `Make a circle of radius ${mGoal[1]} ${unitS}` : mGoal[0] === 'A' ? `Make a circle with area ${mGoal[1]} sq ${unitS} (${piS === 'π' ? 'π' : 'π = ' + piS})` : `Make a circle with circumference ${mGoal[1]} ${unitS} (${piS === 'π' ? 'π' : 'π = ' + piS})`;
      if (mode === 'sector') return sGoal[0] === 'angle' ? `Make a sector of ${sGoal[1]}° (${fracOf(sGoal[1])} of the circle)` : sGoal[0] === 'arc' ? `Make an arc of length ${sGoal[1]} ${unitS}` : `Make a sector of area ${sGoal[1]} sq ${unitS}`;
      return goal === 'semicircle' ? 'Make ∠APB = 90°. Where must A and B be?' : `Make ∠AOB = ${target}°. What is ∠APB?`;
    }
    function showCh() { chEl.textContent = '🎯 Challenge: ' + chText(); }
    function win(msg) { if (won) return; won = true; api.sfx('correct'); api.win(p.winText || msg); }
    const near = (a, b, rel = 0.01) => Math.abs(a - b) <= Math.max(1e-6, Math.abs(b) * rel);
    function check() {
      if (mode === 'parts' && !quiz) { const [, , th] = minorArc(); if (part === 'chord' || part === 'segment' || part === 'arc' || part === 'sector') if (Math.round(th) === 180) win('The chord passes through the centre: it is a diameter, the longest chord!'); }
      else if (mode === 'measure') {
        const v = mGoal[0] === 'r' ? r : mGoal[0] === 'A' ? PI * r * r : 2 * PI * r;
        if (near(v, mGoal[1])) win(`r = ${f2(r)} ${unitS}: C = ${f2(2 * PI * r)} ${unitS}, A = ${f2(PI * r * r)} sq ${unitS}`);
      } else if (mode === 'sector') {
        const th = norm(B - A) || 360, v = sGoal[0] === 'angle' ? th : sGoal[0] === 'arc' ? th / 360 * 2 * PI * r : th / 360 * PI * r * r;
        if (near(v, sGoal[1])) win(`θ = ${Math.round(th)}°, r = ${f2(r)}: arc = ${f2(th / 360 * 2 * PI * r)} ${unitS}, sector area = ${f2(th / 360 * PI * r * r)} sq ${unitS}`);
      } else if (mode === 'theorem') {
        const [s0, s1] = arcNotP(), x = Math.round(norm(s1 - s0));
        if (goal === 'semicircle' ? x === 180 : x === target) win(x === 180 ? 'AB is a diameter, so ∠APB = 90°: the angle in a semicircle is a right angle!' : `∠AOB = ${x}° and ∠APB = ${f2(x / 2)}°: the angle at the centre is double!`);
      }
    }

    // ----- interaction -----
    let drag = null;
    function svgXY(e) { const m = svg.getScreenCTM(); if (!m) return null; const q = svg.createSVGPoint(); q.x = e.clientX; q.y = e.clientY; const t = q.matrixTransform(m.inverse()); return [t.x, t.y]; }
    function handles() {
      if (mode === 'parts') { if (quiz) return []; const h = [['A', at(A)]]; if (['chord', 'arc', 'sector', 'segment'].includes(part)) h.push(['B', at(B)]); if (part === 'diameter') h.push(['A2', at(A + 180)]); return part === 'centre' ? [] : h; }
      if (mode === 'measure') return [['R', at(30)]];
      if (mode === 'sector') return [['R', at(A)], ['B', at(B)]];
      return [['A', at(A)], ['B', at(B)], ['P', at(Pa)]];
    }
    function down(e) {
      const q = svgXY(e); if (!q) return;
      if (quiz) {
        const g = e.target.closest && e.target.closest('[data-part]'); if (!g || qi >= findList.length) return;
        const k = g.getAttribute('data-part');
        if (k === findList[qi]) { found.add(k); qi++; api.sfx('correct'); draw(); if (qi >= findList.length) win(p.winText || `You found all ${findList.length} parts of the circle!`); }
        else { api.sfx('wrong'); const was = rd.innerHTML; rd.innerHTML = cell('Not that one', `That is ${/^[aeiou]/i.test(NAMES[k]) ? 'an' : 'a'} ${NAMES[k].toLowerCase()}. ${DEFS[k]}`, 1); setTimeout(() => { if (rd.isConnected) readout(); }, 1600); }
        return;
      }
      let best = null, bd = 36;
      handles().forEach(([k, hq]) => { const d = Math.hypot(hq[0] - q[0], hq[1] - q[1]); if (d < bd) { bd = d; best = k; } });
      if (!best) return;
      drag = best; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); api.sfx('tap'); e.preventDefault();
    }
    function move(e) {
      if (!drag) return; const q = svgXY(e); if (!q) return;
      const a = norm(Math.atan2(cy - q[1], q[0] - cx) * 180 / Math.PI);
      if (drag === 'R') {
        const along = mode === 'measure' ? (q[0] - cx) * Math.cos(rad(30)) + (cy - q[1]) * Math.sin(rad(30)) : (q[0] - cx) * Math.cos(rad(A)) + (cy - q[1]) * Math.sin(rad(A));
        r = Math.max(rr[0], Math.min(rr[1], Math.round(along / scale / step) * step));
        r = Math.round(r * 1000) / 1000;
      } else if (mode === 'theorem') {
        const v = Math.round(a / 2) * 2 % 360;
        const others = { A: [B, Pa], B: [A, Pa], P: [A, B] }[drag];
        if (others.some(o => Math.min(norm(v - o), norm(o - v)) < 6)) return; // keep points apart
        if (drag === 'A') A = v; else if (drag === 'B') B = v; else Pa = v;
      } else if (mode === 'sector') { B = Math.round(a) % 360; }
      else { const v = Math.round(a); if (drag === 'A') A = v; else if (drag === 'A2') A = norm(v + 180); else { if (norm(v - A) === 0) return; B = v; } }
      draw();
    }
    function up() { if (!drag) return; drag = null; check(); }
    svg.addEventListener('pointerdown', down); svg.addEventListener('pointermove', move); svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);

    host.querySelectorAll('[data-p]').forEach(b => b.addEventListener('click', () => {
      const k = b.dataset.p; quiz = k === 'quiz'; if (!quiz) part = k; api.sfx('tap'); syncChips(); draw();
    }));
    function syncChips() { host.querySelectorAll('[data-p]').forEach(b => b.classList.toggle('on', quiz ? b.dataset.p === 'quiz' : b.dataset.p === part)); }
    host.querySelector('[data-new]').addEventListener('click', () => {
      challengeText = null; won = false; api.resetWin && api.resetWin(); api.sfx('tap');
      const pick = arr => arr[Math.floor(Math.random() * arr.length)];
      if (mode === 'parts') {
        if (findList.length) { quiz = true; qi = 0; found = new Set(); findList.sort(() => Math.random() - .5); }
        else { part = 'chord'; A = pick([200, 220, 240]); B = pick([300, 320, 340]); }
        syncChips();
      } else if (mode === 'measure') {
        const steps = Math.round((rr[1] - rr[0]) / step), rv = Math.round((rr[0] + step * Math.floor(Math.random() * (steps + 1))) * 1000) / 1000;
        const kind = pick(['C', 'A', 'r']); mGoal = [kind, kind === 'r' ? rv : kind === 'C' ? +f2(2 * PI * rv) : +f2(PI * rv * rv)];
      } else if (mode === 'sector') {
        const k = pick(['angle', 'arc', 'area']), th = pick([30, 45, 60, 90, 120, 180, 270]);
        sGoal = [k, k === 'angle' ? th : k === 'arc' ? +f2(th / 360 * 2 * PI * r) : +f2(th / 360 * PI * r * r)];
      } else { goal = 'target'; target = pick([40, 60, 80, 100, 120, 140, 160, 180]); }
      showCh(); draw();
    });
    syncChips(); showCh(); draw();
    return () => { svg.removeEventListener('pointerdown', down); svg.removeEventListener('pointermove', move); svg.removeEventListener('pointerup', up); svg.removeEventListener('pointercancel', up); };
  }

  Labs.register('circlelab', {
    title: 'Circle lab',
    subjects: ['maths'],
    render,
    example: { mode: 'parts', part: 'chord' },
    examples: [
      { mode: 'parts', find: ['centre', 'radius', 'chord', 'diameter', 'arc', 'sector', 'segment', 'tangent'], challenge: 'Tap each part of the circle when asked' },
      { mode: 'measure', r: 3.5, rRange: [1, 10], step: 0.5, pi: '22/7', targetC: 44 },
      { mode: 'theorem', goal: 'semicircle' }
    ]
  });
})();
