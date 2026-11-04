/* StudyVerse Concept Lab: anglemaker — "Angle maker"
 * The child drags a ray (anywhere on the picture works) and watches the angle,
 * its size in degrees and its type change live. +1°/−1° buttons give fine control.
 *
 * PARAMS (all optional; defaults in brackets)
 *  mode        string  'make' | 'pairs' | 'parallel'                                  ['make']
 *                      make     = one angle ∠AOB on a protractor
 *                      pairs    = two related angles (see `pair`)
 *                      parallel = two parallel lines cut by a transversal (8 angles)
 *  max         number  make mode: largest angle allowed, 180 (half protractor) or 360 (full) [360]
 *  start       number  starting angle in degrees                                       [mode-specific]
 *  target      number  challenge angle in degrees (make: ∠AOB; pairs/parallel: angle `ask`) [120]
 *  targetType  string  make mode alternative goal: 'acute'|'right'|'obtuse'|'straight'|'reflex'|'complete'
 *  tolerance   number  allowed error in degrees for the target                         [0]
 *  pair        string  pairs mode: 'complementary'|'supplementary'|'linear'|'vertical' ['supplementary']
 *  ask         number  which numbered angle the target is about:
 *                      pairs: 1 or 2 (vertical: 1–4) [2]; parallel: 1–8 [6]
 *  highlight   string  parallel mode first highlighted pair: 'corresponding'|'alternate'|'cointerior'|'vertical' ['corresponding']
 *  showAll     bool    parallel mode: show the value of all 8 angles                    [false]
 *  protractor  bool    make mode: show the protractor scale                             [true]
 *  labels      array   names of [arm point, vertex, moving arm point]                   [['A','O','B']]
 *  challenge   string  challenge text (English or Hindi); default is generated
 *  winText     string  message shown on success; default is generated
 */
(function () {
  const C = { violet: '#8b5cf6', mint: '#2ed3a5', sun: '#ffc93c', coral: '#ff6b6b', blue: '#3b82f6', ink: '#1b1f3a', muted: '#6b7090' };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const rad = d => d * Math.PI / 180;
  const pt = (cx, cy, r, a) => [cx + r * Math.cos(rad(a)), cy - r * Math.sin(rad(a))];
  const P = a => a[0].toFixed(1) + ' ' + a[1].toFixed(1);
  function arc(cx, cy, r, a0, a1) {
    const s = a1 - a0; if (s <= 0.01) return '';
    if (s >= 359.99) return `M${cx + r} ${cy} A${r} ${r} 0 1 0 ${cx - r} ${cy} A${r} ${r} 0 1 0 ${cx + r} ${cy}`;
    return `M${P(pt(cx, cy, r, a0))} A${r} ${r} 0 ${s > 180 ? 1 : 0} 0 ${P(pt(cx, cy, r, a1))}`;
  }
  function wedge(cx, cy, r, a0, a1) {
    const s = a1 - a0; if (s <= 0.01) return '';
    if (s >= 359.99) return arc(cx, cy, r, a0, a1) + 'Z';
    return `M${cx} ${cy} L${P(pt(cx, cy, r, a0))} A${r} ${r} 0 ${s > 180 ? 1 : 0} 0 ${P(pt(cx, cy, r, a1))}Z`;
  }
  const TYPES = {
    zero: ['Zero angle', '0°', C.muted], acute: ['Acute', 'less than 90°', C.mint], right: ['Right angle', 'exactly 90°', C.blue],
    obtuse: ['Obtuse', 'between 90° and 180°', C.sun], straight: ['Straight angle', 'exactly 180°', C.violet],
    reflex: ['Reflex', 'between 180° and 360°', C.coral], complete: ['Complete angle', 'exactly 360°', '#0f9d7a']
  };
  function angType(a) { a = Math.round(a); if (a <= 0) return 'zero'; if (a < 90) return 'acute'; if (a === 90) return 'right'; if (a < 180) return 'obtuse'; if (a === 180) return 'straight'; if (a < 360) return 'reflex'; return 'complete'; }
  const art = k => { const n = TYPES[k][0].toLowerCase().replace(/^(acute|obtuse|reflex)$/, '$1 angle'); return (/^[aeiou]/.test(n) ? 'an ' : 'a ') + n; };
  const norm = a => ((a % 360) + 360) % 360;
  const rnd = (a, b) => a + Math.floor(Math.random() * (b - a + 1));

  const CSS = `
.lb-anglemaker-w{font-size:14px;color:${C.ink}}
.lb-anglemaker-ch{background:#fff6d8;border-radius:12px;padding:6px 6px 6px 11px;font-weight:800;font-size:14px;margin-bottom:8px;line-height:1.3;display:flex;align-items:center;gap:8px}
.lb-anglemaker-ch span{flex:1}
.lb-anglemaker-ch .lb-anglemaker-b{flex-shrink:0;font-size:13px;padding:0 10px}
.lb-anglemaker-rr{display:flex;align-items:flex-start;gap:6px;margin-top:8px}
.lb-anglemaker-rr .lb-anglemaker-read{flex:1;margin-top:0}
.lb-anglemaker-nud{display:flex;gap:5px;flex-shrink:0}
.lb-anglemaker-svg{width:100%;height:auto;display:block;touch-action:none;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:18px;cursor:grab;user-select:none;-webkit-user-select:none}
.lb-anglemaker-svg text{font-family:inherit;pointer-events:none}
.lb-anglemaker-read{display:flex;align-items:center;gap:8px;margin-top:8px;flex-wrap:wrap}
.lb-anglemaker-big{font-size:20px;font-weight:800;min-width:96px}
.lb-anglemaker-pill{border-radius:999px;padding:5px 12px;font-weight:800;color:#fff;font-size:13px;transition:background .25s}
.lb-anglemaker-sub{color:${C.muted};font-weight:700;font-size:12.5px;flex-basis:100%;line-height:1.35}
.lb-anglemaker-row{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}
.lb-anglemaker-b{min-height:40px;min-width:44px;border:none;border-radius:12px;background:#f1efff;color:${C.ink};font:inherit;font-weight:800;font-size:14px;padding:0 12px;cursor:pointer}
.lb-anglemaker-b:active{transform:scale(.95)}
.lb-anglemaker-b.on{background:${C.violet};color:#fff}
.lb-anglemaker-b.go{background:${C.violet};color:#fff;margin-left:auto}
.lb-anglemaker-chips{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin-top:8px}
.lb-anglemaker-chips .lb-anglemaker-b{font-size:12px;min-height:40px;padding:0 4px;line-height:1.1}
.lb-anglemaker-eq{margin-top:6px;font-weight:800;font-size:13.5px;background:#f4f6ff;border-radius:12px;padding:7px 10px;line-height:1.4}
`;

  function render(host, p, api) {
    const mode = ['make', 'pairs', 'parallel'].includes(p.mode) ? p.mode : 'make';
    const L = Array.isArray(p.labels) && p.labels.length >= 3 ? p.labels.map(String) : ['A', 'O', 'B'];
    const tol = Math.max(0, +p.tolerance || 0);
    const pairKind = ['complementary', 'supplementary', 'linear', 'vertical'].includes(p.pair) ? p.pair : 'supplementary';
    const max = mode === 'make' ? (+p.max === 180 ? 180 : 360) : 0;
    let target = p.target != null && isFinite(+p.target) ? +p.target : null;
    let targetType = TYPES[p.targetType] ? p.targetType : null;
    let ask = +p.ask || (mode === 'parallel' ? 6 : pairKind === 'vertical' ? 3 : 2);
    let challengeText = p.challenge ? String(p.challenge) : null;
    let theta; // the one controlled quantity (degrees)
    let hl = ['corresponding', 'alternate', 'cointerior', 'vertical'].includes(p.highlight) ? p.highlight : 'corresponding', hlIdx = 0;

    // ----- geometry per mode -----
    let G;
    if (mode === 'make') {
      G = max === 180 ? { cx: 180, cy: 222, R: 152, arm: 168, H: 248 } : { cx: 180, cy: 128, R: 104, arm: 116, H: 256 };
      theta = p.start != null ? +p.start : 40;
      if (target == null && !targetType) target = 120;
      if (target != null) target = Math.max(0, Math.min(max, target));
    } else if (mode === 'pairs') {
      if (pairKind === 'complementary') { G = { cx: 70, cy: 222, lo: 0, hi: 90, arm: 190, H: 248 }; theta = p.start != null ? +p.start : 30; }
      else if (pairKind === 'vertical') { G = { cx: 180, cy: 128, lo: 10, hi: 170, arm: 150, H: 256 }; theta = p.start != null ? +p.start : 50; }
      else { G = { cx: 180, cy: 196, lo: 0, hi: 180, arm: 150, H: 240 }; theta = p.start != null ? +p.start : 60; }
      if (target == null) target = pairKind === 'complementary' ? 35 : pairKind === 'vertical' ? 70 : 110;
      ask = pairKind === 'vertical' ? Math.min(4, Math.max(1, ask)) : Math.min(2, Math.max(1, ask));
      const okR = pairKind === 'complementary' ? [0, 90] : pairKind === 'vertical' ? [10, 170] : [0, 180];
      if (!(target >= okR[0] && target <= okR[1])) target = pairKind === 'complementary' ? 35 : pairKind === 'vertical' ? 70 : 110;
    } else {
      G = { cx: 180, cy: 112, y1: 72, y2: 152, lo: 20, hi: 160, H: 224 };
      theta = p.start != null ? +p.start : 60;
      if (target == null || !(target >= 20 && target <= 160)) target = 65;
      ask = Math.min(8, Math.max(1, ask));
    }

    host.innerHTML = `<style>${CSS}</style><div class="lb-anglemaker-w">
      <div class="lb-anglemaker-ch"><span></span><button class="lb-anglemaker-b go" data-new aria-label="New challenge">🔄 New</button></div>
      <svg class="lb-anglemaker-svg" viewBox="0 0 360 ${G.H}"></svg>
      <div class="lb-anglemaker-rr"><div class="lb-anglemaker-read"></div>
        <div class="lb-anglemaker-nud"><button class="lb-anglemaker-b" data-n="-1" aria-label="minus 1 degree">−1°</button><button class="lb-anglemaker-b" data-n="1" aria-label="plus 1 degree">+1°</button></div></div>
      <div class="lb-anglemaker-eq" hidden></div>
      ${mode === 'parallel' ? `<div class="lb-anglemaker-chips">
        <button class="lb-anglemaker-b" data-h="corresponding">Corres&shy;ponding</button>
        <button class="lb-anglemaker-b" data-h="alternate">Alternate</button>
        <button class="lb-anglemaker-b" data-h="cointerior">Co-interior</button>
        <button class="lb-anglemaker-b" data-h="vertical">Vert. opp.</button></div>` : ''}</div>`;
    const svg = host.querySelector('svg'), chEl = host.querySelector('.lb-anglemaker-ch span'), rd = host.querySelector('.lb-anglemaker-read'), eqEl = host.querySelector('.lb-anglemaker-eq');

    // ----- challenge text -----
    function pairVal(n) { // pairs mode values
      if (pairKind === 'complementary') return n === 1 ? theta : 90 - theta;
      if (pairKind === 'vertical') return n % 2 === 1 ? theta : 180 - theta;
      return n === 1 ? theta : 180 - theta;
    }
    function parVal(n) { return (n === 2 || n === 3 || n === 6 || n === 7) ? theta : 180 - theta; }
    function defaultChallenge() {
      if (mode === 'make') return targetType ? `Make ${/^[ao]/.test(TYPES[targetType][0].toLowerCase()) ? 'an' : 'a'} ${TYPES[targetType][0].toLowerCase()}${targetType === 'acute' || targetType === 'obtuse' || targetType === 'reflex' ? ' angle' : ''}` : `Make ∠${L[0]}${L[1]}${L[2]} = ${target}°`;
      if (mode === 'pairs') {
        const nm = { complementary: 'complementary', supplementary: 'supplementary', linear: 'a linear pair', vertical: 'vertically opposite' }[pairKind];
        return `Make ∠${ask} = ${target}° (angles here are ${nm})`;
      }
      return `Make ∠${ask} = ${target}° by turning the transversal`;
    }
    function showChallenge() { chEl.textContent = '🎯 Challenge: ' + (challengeText || defaultChallenge()); }

    // ----- drawing -----
    const ns = 'http://www.w3.org/2000/svg';
    function draw() {
      let s = '';
      const tC = TYPES[angType(theta)];
      if (mode === 'make') {
        const { cx, cy, R, arm } = G;
        if (p.protractor !== false) {
          s += max === 180
            ? `<path d="M${cx - R} ${cy} A${R} ${R} 0 0 1 ${cx + R} ${cy}Z" fill="#fff" fill-opacity=".75" stroke="#c9c3f7" stroke-width="1.5"/>`
            : `<circle cx="${cx}" cy="${cy}" r="${R}" fill="#fff" fill-opacity=".75" stroke="#c9c3f7" stroke-width="1.5"/>`;
          for (let a = 0; a <= max; a += (max === 180 ? 1 : 5)) {
            if (a === 360) break;
            const len = a % 10 === 0 ? 11 : a % 5 === 0 ? 7 : 4;
            s += `<line x1="${P(pt(cx, cy, R, a)).split(' ')[0]}" y1="${pt(cx, cy, R, a)[1].toFixed(1)}" x2="${pt(cx, cy, R - len, a)[0].toFixed(1)}" y2="${pt(cx, cy, R - len, a)[1].toFixed(1)}" stroke="#a79cf2" stroke-width="${a % 10 === 0 ? 1.3 : .8}"/>`;
          }
          const step = max === 180 ? 10 : 30;
          for (let a = 0; a < (max === 180 ? 181 : 360); a += step) {
            const q = pt(cx, cy, R - 21, a);
            s += `<text x="${q[0].toFixed(1)}" y="${(q[1] + 3.5).toFixed(1)}" font-size="${max === 180 ? 9.5 : 10}" font-weight="700" fill="#7c6fd6" text-anchor="middle">${a}</text>`;
          }
        }
        // angle region
        const big = theta >= 359.5, rr = max === 180 ? 46 : 36;
        if (Math.round(theta) === 90) s += `<path d="M${cx + 22} ${cy} L${cx + 22} ${cy - 22} L${cx} ${cy - 22}" fill="${tC[2]}" fill-opacity=".25" stroke="${tC[2]}" stroke-width="2.5"/>`;
        else if (theta > 0.5) s += `<path d="${wedge(cx, cy, rr, 0, theta)}" fill="${tC[2]}" fill-opacity=".22"/><path d="${arc(cx, cy, rr, 0, theta)}" fill="none" stroke="${tC[2]}" stroke-width="3" stroke-linecap="round"/>`;
        if (theta > 0.5 && !big) { // little arrow head shows direction of turning
          const e = pt(cx, cy, rr, theta), d = theta + 90;
          s += `<path d="M${P(e)} l${(7 * Math.cos(rad(d - 150))).toFixed(1)} ${(-7 * Math.sin(rad(d - 150))).toFixed(1)} M${P(e)} l${(7 * Math.cos(rad(d + 150))).toFixed(1)} ${(-7 * Math.sin(rad(d + 150))).toFixed(1)}" stroke="${tC[2]}" stroke-width="2.5" stroke-linecap="round"/>`;
        }
        const lp = pt(cx, cy, rr + 20, theta > 0.5 ? theta / 2 : 10);
        s += `<text x="${lp[0].toFixed(1)}" y="${(lp[1] + 5).toFixed(1)}" font-size="15" font-weight="800" fill="${C.ink}" text-anchor="middle" stroke="#fff" stroke-width="4" paint-order="stroke">${Math.round(theta)}°</text>`;
        // arms
        const a1 = pt(cx, cy, arm, 0), b1 = pt(cx, cy, arm, theta);
        s += `<line x1="${cx}" y1="${cy}" x2="${a1[0]}" y2="${a1[1]}" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>`;
        s += `<line x1="${cx}" y1="${cy}" x2="${b1[0].toFixed(1)}" y2="${b1[1].toFixed(1)}" stroke="${C.violet}" stroke-width="4" stroke-linecap="round"/>`;
        s += `<circle cx="${cx}" cy="${cy}" r="5" fill="${C.ink}"/>`;
        s += lbl([cx - 12, cy + 19], L[1], C.ink);
        s += lbl([a1[0] - 6, a1[1] + 16], L[0], C.ink);
        s += handle(b1) + lbl(pt(cx, cy, arm + 18, theta), L[2], C.violet);
      } else if (mode === 'pairs') {
        const { cx, cy, arm } = G;
        if (pairKind === 'complementary') {
          const A = pt(cx, cy, 270, 0), Cc = pt(cx, cy, 196, 90), B = pt(cx, cy, arm, theta);
          s += `<path d="${wedge(cx, cy, 52, 0, theta)}" fill="${C.mint}" fill-opacity=".3"/><path d="${wedge(cx, cy, 70, theta, 90)}" fill="${C.sun}" fill-opacity=".35"/>`;
          s += `<path d="M${cx + 14} ${cy} L${cx + 14} ${cy - 14} L${cx} ${cy - 14}" fill="none" stroke="${C.muted}" stroke-width="1.5"/>`;
          s += ln([cx, cy], A, C.ink) + ln([cx, cy], Cc, C.ink) + ln([cx, cy], B, C.violet);
          s += num(pt(cx, cy, 120, theta / 2), '∠1', Math.round(theta), '#0f9d7a') + num(pt(cx, cy, 104, (theta + 90) / 2), '∠2', Math.round(90 - theta), '#b07d00');
          s += handle(B);
        } else if (pairKind === 'vertical') {
          const E1 = pt(cx, cy, 165, 0), E2 = pt(cx, cy, 165, 180), F1 = pt(cx, cy, arm, theta), F2 = pt(cx, cy, arm, theta + 180);
          s += `<path d="${wedge(cx, cy, 40, 0, theta)}" fill="${C.mint}" fill-opacity=".35"/><path d="${wedge(cx, cy, 40, 180, 180 + theta)}" fill="${C.mint}" fill-opacity=".35"/>`;
          s += `<path d="${wedge(cx, cy, 40, theta, 180)}" fill="${C.sun}" fill-opacity=".35"/><path d="${wedge(cx, cy, 40, 180 + theta, 360)}" fill="${C.sun}" fill-opacity=".35"/>`;
          s += ln(E1, E2, C.ink) + ln(F1, F2, C.violet);
          const v1 = Math.round(theta), v2 = 180 - v1;
          s += num(pt(cx, cy, 62, theta / 2), '∠1', v1, '#0f9d7a') + num(pt(cx, cy, 62, (theta + 180) / 2), '∠2', v2, '#b07d00');
          s += num(pt(cx, cy, 62, 180 + theta / 2), '∠3', v1, '#0f9d7a') + num(pt(cx, cy, 62, (theta + 540) / 2), '∠4', v2, '#b07d00');
          s += handle(F1) + handle(F2);
        } else {
          const E1 = pt(cx, cy, 165, 0), E2 = pt(cx, cy, 165, 180), B = pt(cx, cy, arm, theta);
          s += `<path d="${wedge(cx, cy, 46, 0, theta)}" fill="${C.mint}" fill-opacity=".3"/><path d="${wedge(cx, cy, 60, theta, 180)}" fill="${C.sun}" fill-opacity=".35"/>`;
          s += ln(E1, E2, C.ink) + ln([cx, cy], B, C.violet);
          s += num(pt(cx, cy, 120, theta / 2), '∠1', Math.round(theta), '#0f9d7a') + num(pt(cx, cy, 84, (theta + 180) / 2), '∠2', 180 - Math.round(theta), '#b07d00');
          s += handle(B);
        }
        s += `<circle cx="${cx}" cy="${cy}" r="5" fill="${C.ink}"/>`;
      } else {
        const { cx, cy, y1, y2 } = G, sn = Math.sin(rad(theta)), cs = Math.cos(rad(theta));
        const Pp = [cx + (cy - y1) / sn * cs, y1], Q = [cx + (cy - y2) / sn * cs, y2];
        const tt = Math.min(98 / sn, 150 / Math.max(Math.abs(cs), 1e-6)); const T1 = [cx + tt * cs, cy - tt * sn], T2 = [cx - tt * cs, cy + tt * sn]; // ends of transversal, kept inside the box
        const pairs = PAIRS[hl], pr = pairs[hlIdx % pairs.length];
        // region fills for highlighted pair
        const regions = n => { const top = n <= 4, at = top ? Pp : Q, k = (n - 1) % 4; // 0 TL,1 TR,2 BL,3 BR
          const rg = [[theta, 180], [0, theta], [180, 180 + theta], [180 + theta, 360]][k]; return wedge(at[0], at[1], 30, rg[0], rg[1]); };
        pr.forEach((n, i) => { s += `<path d="${regions(n)}" fill="${i ? C.sun : C.mint}" fill-opacity=".5"/>`; });
        s += ln([16, y1], [344, y1], C.ink) + ln([16, y2], [344, y2], C.ink);
        // arrow marks for parallel
        [y1, y2].forEach(y => { s += `<path d="M300 ${y - 6} l7 6 l-7 6" fill="none" stroke="${C.ink}" stroke-width="2.2" stroke-linecap="round"/>`; });
        s += `<text x="24" y="${y1 - 8}" font-size="12" font-weight="800" fill="${C.muted}">l</text><text x="24" y="${y2 - 8}" font-size="12" font-weight="800" fill="${C.muted}">m</text>`;
        s += ln(T1, T2, C.violet);
        for (let n = 1; n <= 8; n++) {
          const top = n <= 4, at = top ? Pp : Q, k = (n - 1) % 4;
          const mid = [(theta + 180) / 2, theta / 2, 180 + theta / 2, (180 + theta + 360) / 2][k];
          const q = pt(at[0], at[1], 22, mid), on = pr.includes(n), showV = on || p.showAll || n === 2;
          s += `<text x="${q[0].toFixed(1)}" y="${(q[1] + 4).toFixed(1)}" font-size="${on ? 13 : 11.5}" font-weight="800" fill="${on ? C.ink : C.muted}" text-anchor="middle" stroke="#fff" stroke-width="3" paint-order="stroke">${n}</text>`;
          if (showV) { const v = pt(at[0], at[1], 44, mid); s += `<text x="${v[0].toFixed(1)}" y="${(v[1] + 4).toFixed(1)}" font-size="11" font-weight="800" fill="${on ? (pr[0] === n ? '#0f9d7a' : '#9a6c00') : C.violet}" text-anchor="middle" stroke="#fff" stroke-width="3" paint-order="stroke">${Math.round(parVal(n))}°</text>`; }
        }
        s += `<circle cx="${Pp[0].toFixed(1)}" cy="${y1}" r="3.5" fill="${C.ink}"/><circle cx="${Q[0].toFixed(1)}" cy="${y2}" r="3.5" fill="${C.ink}"/>`;
        s += handle(T1) + handle(T2);
      }
      svg.innerHTML = s;
      readout();
    }
    function ln(a, b, col) { return `<line x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}" stroke="${col}" stroke-width="4" stroke-linecap="round"/>`; }
    function lbl(q, t, col) { return `<text x="${q[0].toFixed(1)}" y="${(q[1] + 5).toFixed(1)}" font-size="14" font-weight="800" fill="${col}" text-anchor="middle">${esc(t)}</text>`; }
    function num(q, name, v, col) { return `<text x="${q[0].toFixed(1)}" y="${(q[1]).toFixed(1)}" font-size="12" font-weight="800" fill="${col}" text-anchor="middle" stroke="#fff" stroke-width="3" paint-order="stroke">${name}<tspan x="${q[0].toFixed(1)}" dy="14" font-size="13">${v}°</tspan></text>`; }
    function handle(q) { return `<circle cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="13" fill="${C.violet}" stroke="#fff" stroke-width="3" style="filter:drop-shadow(0 2px 3px rgba(80,60,180,.35))"/><circle cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="4" fill="#fff"/>`; }

    const PAIRS = { corresponding: [[1, 5], [2, 6], [3, 7], [4, 8]], alternate: [[3, 6], [4, 5], [1, 8], [2, 7]], cointerior: [[3, 5], [4, 6]], vertical: [[1, 4], [2, 3], [5, 8], [6, 7]] };
    function readout() {
      const t = Math.round(theta);
      if (mode === 'make') {
        const ty = TYPES[angType(theta)];
        rd.innerHTML = `<span class="lb-anglemaker-big">∠${esc(L[0] + L[1] + L[2])} = ${t}°</span><span class="lb-anglemaker-pill" style="background:${ty[2]}">${ty[0]}</span>
          <span class="lb-anglemaker-sub">${ty[0]}: ${ty[1]}.${t > 180 && t < 360 ? ` The other side is 360° − ${t}° = ${360 - t}°.` : ''}</span>`;
        eqEl.hidden = true;
      } else if (mode === 'pairs') {
        const a = Math.round(pairVal(1)), b = Math.round(pairVal(2));
        rd.innerHTML = `<span class="lb-anglemaker-big" style="color:#0f9d7a">∠1 = ${a}°</span><span class="lb-anglemaker-big" style="color:#b07d00">∠2 = ${b}°</span>`;
        eqEl.hidden = false;
        eqEl.innerHTML = pairKind === 'complementary' ? `∠1 + ∠2 = ${a}° + ${b}° = 90°<br><span style="color:${C.muted}">Complementary angles add up to 90°.</span>`
          : pairKind === 'vertical' ? `∠1 = ∠3 = ${a}° and ∠2 = ∠4 = ${b}°<br><span style="color:${C.muted}">Vertically opposite angles are equal. ∠1 + ∠2 = 180° (linear pair).</span>`
            : `∠1 + ∠2 = ${a}° + ${b}° = 180°<br><span style="color:${C.muted}">${pairKind === 'linear' ? 'A linear pair: adjacent angles on a straight line add up to 180°.' : 'Supplementary angles add up to 180°.'}</span>`;
      } else {
        const pr = PAIRS[hl][hlIdx % PAIRS[hl].length], a = Math.round(parVal(pr[0])), b = Math.round(parVal(pr[1]));
        const rule = { corresponding: ['Corresponding angles', 'are equal'], alternate: [pr[0] >= 3 && pr[0] <= 4 ? 'Alternate interior angles' : 'Alternate exterior angles', 'are equal'], cointerior: ['Co-interior angles', 'add up to 180°'], vertical: ['Vertically opposite angles', 'are equal'] }[hl];
        rd.innerHTML = `<span class="lb-anglemaker-big" style="color:#0f9d7a">∠${pr[0]} = ${a}°</span><span class="lb-anglemaker-big" style="color:#9a6c00">∠${pr[1]} = ${b}°</span>`;
        eqEl.hidden = false;
        eqEl.innerHTML = `${hl === 'cointerior' ? `∠${pr[0]} + ∠${pr[1]} = ${a}° + ${b}° = 180°` : `∠${pr[0]} = ∠${pr[1]}`}<br><span style="color:${C.muted}">${rule[0]} ${rule[1]} (l ∥ m).</span>`;
        host.querySelectorAll('[data-h]').forEach(b => b.classList.toggle('on', b.dataset.h === hl));
      }
    }

    // ----- win check -----
    function check() {
      let ok = false, msg = p.winText;
      const t = Math.round(theta);
      if (mode === 'make') {
        if (targetType) { ok = angType(theta) === targetType; msg = msg || `${t}° is ${art(targetType)}: ${TYPES[targetType][1]}.`; }
        else { ok = Math.abs(t - target) <= tol; msg = msg || `∠${L[0]}${L[1]}${L[2]} = ${t}°. That is ${art(angType(t))}.`; }
      } else if (mode === 'pairs') {
        const v = Math.round(pairVal(ask)); ok = Math.abs(v - target) <= tol;
        msg = msg || (pairKind === 'complementary' ? `∠1 = ${Math.round(pairVal(1))}° and ∠2 = ${Math.round(pairVal(2))}°: together 90°.` : pairKind === 'vertical' ? `∠${ask} = ${v}°. Vertically opposite angles are equal!` : `∠1 = ${Math.round(pairVal(1))}° and ∠2 = ${Math.round(pairVal(2))}°: together 180°.`);
      } else {
        const v = Math.round(parVal(ask)); ok = Math.abs(v - target) <= tol;
        msg = msg || `∠${ask} = ${v}°. When ∠2 = ${t}°, every angle is ${t}° or ${180 - t}°.`;
      }
      if (ok && !won) { won = true; api.sfx('correct'); api.win(msg); }
    }
    let won = false;

    // ----- interaction -----
    function svgXY(e) { const m = svg.getScreenCTM(); if (!m) return null; const q = svg.createSVGPoint(); q.x = e.clientX; q.y = e.clientY; const r = q.matrixTransform(m.inverse()); return [r.x, r.y]; }
    function rawAngle(e) { const q = svgXY(e); if (!q) return null; const pv = mode === 'make' || mode === 'pairs' ? [G.cx, G.cy] : [G.cx, G.cy]; return norm(Math.atan2(pv[1] - q[1], q[0] - pv[0]) * 180 / Math.PI); }
    function clampRange(raw) {
      if (mode === 'pairs' && pairKind === 'vertical' || mode === 'parallel') { let a = raw % 180; return Math.max(G.lo, Math.min(G.hi, a)); }
      if (raw >= G.lo && raw <= G.hi) return raw;
      const dLo = Math.min(Math.abs(raw - G.lo), 360 - Math.abs(raw - G.lo)), dHi = Math.min(Math.abs(raw - G.hi), 360 - Math.abs(raw - G.hi));
      return dLo < dHi ? G.lo : G.hi;
    }
    let dragging = false, last = 0, acc = 0;
    function setFromRaw(raw, first) {
      if (mode === 'make') {
        if (max === 180) { theta = raw <= 180 ? raw : (raw > 270 ? 0 : 180); }
        else if (first) { acc = raw < 3 && theta > 300 ? 360 : raw; theta = acc; }
        else { let d = raw - last; if (d > 180) d -= 360; if (d < -180) d += 360; acc = Math.max(0, Math.min(360, acc + d)); theta = acc; }
        last = raw;
      } else theta = clampRange(raw);
      theta = Math.round(theta);
      draw();
    }
    function down(e) { const r = rawAngle(e); if (r == null) return; dragging = true; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); setFromRaw(r, true); api.sfx('tap'); e.preventDefault(); }
    function move(e) { if (!dragging) return; const r = rawAngle(e); if (r != null) setFromRaw(r, false); }
    function up() { if (!dragging) return; dragging = false; check(); }
    svg.addEventListener('pointerdown', down); svg.addEventListener('pointermove', move);
    svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);

    host.querySelectorAll('[data-n]').forEach(b => b.addEventListener('click', () => {
      const d = +b.dataset.n;
      if (mode === 'make') theta = Math.max(0, Math.min(max, theta + d));
      else theta = Math.max(G.lo, Math.min(G.hi, theta + d));
      draw(); check();
    }));
    host.querySelectorAll('[data-h]').forEach(b => b.addEventListener('click', () => {
      if (hl === b.dataset.h) hlIdx++; else { hl = b.dataset.h; hlIdx = 0; }
      api.sfx('tap'); draw();
    }));
    host.querySelector('[data-new]').addEventListener('click', () => {
      challengeText = null; won = false; api.resetWin && api.resetWin();
      if (mode === 'make') {
        if (targetType) { const keys = max === 180 ? ['acute', 'right', 'obtuse', 'straight'] : ['acute', 'right', 'obtuse', 'straight', 'reflex', 'complete']; let k; do k = keys[rnd(0, keys.length - 1)]; while (k === targetType); targetType = k; }
        else { let t; do t = rnd(1, Math.floor(max / 5) - 1) * 5; while (t === target); target = t; }
      } else if (mode === 'pairs') {
        ask = pairKind === 'vertical' ? rnd(1, 4) : rnd(1, 2);
        const lo = pairKind === 'complementary' ? 10 : 20, hi = pairKind === 'complementary' ? 80 : 160;
        target = rnd(lo / 5, hi / 5) * 5;
      } else { ask = rnd(1, 8); target = rnd(5, 31) * 5; }
      showChallenge(); api.sfx('tap');
    });

    showChallenge(); draw();
    return () => { svg.removeEventListener('pointerdown', down); svg.removeEventListener('pointermove', move); svg.removeEventListener('pointerup', up); svg.removeEventListener('pointercancel', up); };
  }

  Labs.register('anglemaker', {
    title: 'Angle maker',
    subjects: ['maths'],
    render,
    example: { mode: 'make', max: 360, target: 120 },
    examples: [
      { mode: 'make', max: 180, start: 30, targetType: 'right', challenge: 'Use the protractor to make a right angle' },
      { mode: 'pairs', pair: 'complementary', start: 30, target: 35, ask: 2 },
      { mode: 'parallel', start: 60, target: 115, ask: 6, highlight: 'cointerior' }
    ]
  });
})();
