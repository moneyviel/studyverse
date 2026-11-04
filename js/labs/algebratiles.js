/* StudyVerse Concept Lab: algebratiles — area model for products and algebraic identities.
 *
 * Sliders change a and b (and x). The square/rectangle is split into coloured parts drawn on a unit
 * grid (so parts can be counted), each part is labelled, and the identity is shown with the numbers
 * substituted. Tap a part to highlight its term. For (a+b)(a−b) the cut piece can be moved
 * ("Rearrange") to turn a² − b² into an (a+b) × (a−b) rectangle.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   identity  'sq_sum' (a+b)² | 'sq_diff' (a−b)² | 'diff_sq' (a+b)(a−b) | 'xab' (x+a)(x+b)       default 'sq_sum'
 *   a, b      number   starting whole-number values                                            default 4, 2
 *   x         number   starting x for 'xab'                                                     default 3
 *   aRange    [min,max]   slider range for a                                                    default [1,8]
 *   bRange    [min,max]   slider range for b                                                    default [1,6]
 *   xRange    [min,max]   slider range for x ('xab')                                            default [1,7]
 *   names     [string,string]  letters shown for a and b                                       default ['a','b']
 *   fix       {a?:n, b?:n, x?:n}  values locked for the challenge (that slider is hidden)       default none
 * Challenge (if none is given one is generated for the identity):
 *   target    number   the whole shape's area must equal this (e.g. 49 for (a+b)²)
 *   match     [s, p]   'xab' only: make (x+a)(x+b) = x² + s·x + p  (a + b = s, ab = p)
 *   rearrange boolean  'diff_sq': also need to tap Rearrange (default true for diff_sq)
 *   challenge string   challenge sentence
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const C = { big: '#8b5cf6', mid: '#2ed3a5', small: '#ffc93c', cut: '#ff6b6b', blue: '#3b82f6' };

  Labs.register('algebratiles', {
    title: 'Algebra tiles',
    subjects: ['maths'],
    render(host, p, api) {
      const id = ['sq_sum', 'sq_diff', 'diff_sq', 'xab'].includes(p.identity) ? p.identity : 'sq_sum';
      const pr = (r, d) => Array.isArray(r) && r.length === 2 && +r[0] >= 1 && +r[0] < +r[1] && +r[1] <= 12 ? r.map(Math.round) : d;
      const RG = { a: pr(p.aRange, [1, 8]), b: pr(p.bRange, [1, 6]), x: pr(p.xRange, [1, 7]) };
      if (id === 'sq_diff' || id === 'diff_sq') RG.a[0] = Math.max(2, RG.a[0]);
      const NA = Array.isArray(p.names) && p.names[0] ? String(p.names[0]) : 'a', NB = Array.isArray(p.names) && p.names[1] ? String(p.names[1]) : 'b';
      const fix = p.fix && typeof p.fix === 'object' ? p.fix : {};
      const cl = (k, v) => Math.max(RG[k][0], Math.min(RG[k][1], Math.round(isFinite(+v) ? +v : RG[k][0])));
      const v = { a: cl('a', fix.a ?? p.a ?? 4), b: cl('b', fix.b ?? p.b ?? 2), x: cl('x', fix.x ?? p.x ?? 3) };
      const needAgtB = id === 'sq_diff' || id === 'diff_sq';
      const fixB = () => { if (needAgtB && v.b >= v.a) v.b = Math.max(1, v.a - 1); };
      fixB();
      let rearr = false, won = false, hi = null;

      const area = () => id === 'sq_sum' ? (v.a + v.b) ** 2 : id === 'sq_diff' ? (v.a - v.b) ** 2 : id === 'diff_sq' ? v.a * v.a - v.b * v.b : (v.x + v.a) * (v.x + v.b);
      // challenge
      let ch;
      if (id === 'xab' && Array.isArray(p.match) && p.match.length === 2) ch = { kind: 'match', s: +p.match[0], p: +p.match[1] };
      else if (isFinite(+p.target) && p.target !== null && p.target !== '') ch = { kind: 'target', t: +p.target };
      else ch = id === 'sq_sum' ? { kind: 'target', t: 49 } : id === 'sq_diff' ? { kind: 'target', t: 9 } : id === 'diff_sq' ? { kind: 'target', t: 33 } : { kind: 'match', s: 5, p: 6 };
      const needRe = id === 'diff_sq' && p.rearrange !== false;
      const exprName = id === 'sq_sum' ? `(${NA} + ${NB})²` : id === 'sq_diff' ? `(${NA} − ${NB})²` : id === 'diff_sq' ? `${NA}² − ${NB}²` : `(x + ${NA})(x + ${NB})`;
      const chText = p.challenge || (ch.kind === 'match' ? `Make (x + ${NA})(x + ${NB}) = x² + ${ch.s}x + ${ch.p}.` : `Make ${exprName} = ${ch.t}${needRe ? ', then tap Rearrange' : ''}.`);
      const shown = ['x', 'a', 'b'].filter(k => (k !== 'x' || id === 'xab') && !(k in fix));

      host.innerHTML = `
<style>
.lb-algebratiles-w input[type=range]{-webkit-appearance:none;appearance:none;height:32px;background:transparent;cursor:pointer}.lb-algebratiles-w input[type=range]::-webkit-slider-runnable-track{height:8px;border-radius:8px;background:#e3e6f6}.lb-algebratiles-w input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;border-radius:50%;background:var(--c,#8b5cf6);margin-top:-8px;border:3px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.3)}.lb-algebratiles-w input[type=range]::-moz-range-track{height:8px;border-radius:8px;background:#e3e6f6}.lb-algebratiles-w input[type=range]::-moz-range-thumb{width:18px;height:18px;border-radius:50%;background:var(--c,#8b5cf6);border:3px solid #fff}
.lb-algebratiles-w{font-size:14px;color:#1b1f3a}
.lb-algebratiles-ch{font-weight:800;font-size:14px;margin-bottom:5px;line-height:1.25}
.lb-algebratiles-svg{width:100%;height:auto;display:block;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:16px}
.lb-algebratiles-pc{cursor:pointer;transition:opacity .2s}
.lb-algebratiles-mv{transition:transform .9s cubic-bezier(.5,0,.3,1.2);transform-box:view-box;transform-origin:0 0}
.lb-algebratiles-f{margin-top:5px;background:#f6f4ff;border-radius:12px;padding:6px 9px;font-weight:800;line-height:1.45;text-align:center}
.lb-algebratiles-f .big{font-family:'Baloo 2',Nunito,sans-serif;font-size:17px}
.lb-algebratiles-f .num{font-size:13px;color:#6b7090}
.lb-algebratiles-f span[data-t]{border-radius:6px;padding:0 2px;transition:background .2s}
.lb-algebratiles-f span.on{background:#fff2b8}
.lb-algebratiles-sl{display:flex;gap:10px;margin-top:4px;align-items:center}
.lb-algebratiles-sl label{flex:1;display:flex;align-items:center;gap:5px;font-weight:800;min-height:40px;min-width:0;font-size:15px}
.lb-algebratiles-sl input{flex:1;min-width:0}
.lb-algebratiles-b{min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#ff6b6b;color:#fff;box-shadow:0 3px 0 #d94848;padding:0 12px;white-space:nowrap}
.lb-algebratiles-b:active{transform:translateY(2px);box-shadow:0 1px 0 #d94848}
</style>
<div class="lb-algebratiles-w">
  <div class="lb-algebratiles-ch">🎯 Challenge: ${esc(chText)}</div>
  <svg class="lb-algebratiles-svg" viewBox="0 0 360 250"></svg>
  <div class="lb-algebratiles-f"></div>
  <div class="lb-algebratiles-sl">${shown.map(k => `<label style="color:${k === 'x' ? C.big : k === 'a' ? '#7c4dee' : '#c98a00'}">${esc(k === 'a' ? NA : k === 'b' ? NB : 'x')}<input type="range" data-k="${k}" min="${RG[k][0]}" max="${RG[k][1]}" step="1" value="${v[k]}" style="--c:${k === 'b' ? '#ffb400' : k === 'a' ? '#2ed3a5' : C.big}"><span data-v="${k}"></span></label>`).join('')}
  ${id === 'diff_sq' ? '<button class="lb-algebratiles-b" data-a="re">Rearrange ↻</button>' : ''}</div>
</div>`;
      const $ = s => host.querySelector(s);
      const svg = $('.lb-algebratiles-svg'), F = $('.lb-algebratiles-f');

      // draw a rectangle part with unit grid and label
      function part(key, x, y, w, h, u, col, label, extra = '') {
        let g = `<g class="lb-algebratiles-pc" data-t="${key}" ${extra}><rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${col}" stroke="#fff" stroke-width="2.5" rx="3"/>`;
        if (u >= 7) {
          let gl = '';
          for (let i = 1; i < Math.round(w / u); i++) gl += `M${x + i * u} ${y}V${y + h}`;
          for (let j = 1; j < Math.round(h / u); j++) gl += `M${x} ${y + j * u}H${x + w}`;
          if (gl) g += `<path d="${gl}" stroke="#fff" stroke-opacity=".45" stroke-width="1"/>`;
        }
        if (label && w > 18 && h > 14) {
          const fs = Math.max(10, Math.min(16, Math.min(w / (label.length * 0.6), h * 0.5)));
          g += `<text x="${x + w / 2}" y="${y + h / 2 + fs * 0.35}" text-anchor="middle" font-size="${fs}" font-weight="800" fill="#1b1f3a" paint-order="stroke" stroke="#fff" stroke-width="3">${esc(label)}</text>`;
        }
        return g + '</g>';
      }
      const side = (x1, y1, x2, y2, t, vert, col = '#1b1f3a') => {
        const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
        return `<path d="M${x1} ${y1}L${x2} ${y2}" stroke="${col}" stroke-width="2" marker-start="" /><text x="${vert ? mx - 6 : mx}" y="${vert ? my + 4 : my - 5}" text-anchor="${vert ? 'end' : 'middle'}" font-size="12.5" font-weight="800" fill="${col}">${esc(t)}</text>`;
      };

      function draw() {
        const a = v.a, b = v.b, x = v.x;
        let g = '', f1 = '', f2 = '';
        const T = (k, s) => `<span data-t="${k}" class="${hi === k ? 'on' : ''}">${s}</span>`;
        if (id === 'sq_sum') {
          const S = a + b, u = Math.min(210 / S, 280 / S), X0 = 66 + (280 - S * u) / 2, Y0 = 26;
          g += part('a2', X0, Y0, a * u, a * u, u, C.big, `${NA}²`) + part('ab', X0 + a * u, Y0, b * u, a * u, u, C.mid, `${NA}${NB}`)
            + part('ab', X0, Y0 + a * u, a * u, b * u, u, C.mid, `${NA}${NB}`) + part('b2', X0 + a * u, Y0 + a * u, b * u, b * u, u, C.small, `${NB}²`);
          g += side(X0, Y0 - 8, X0 + a * u, Y0 - 8, `${NA} = ${a}`) + side(X0 + a * u, Y0 - 8, X0 + S * u, Y0 - 8, `${b}`) + side(X0 - 8, Y0, X0 - 8, Y0 + a * u, `${a}`, true) + side(X0 - 8, Y0 + a * u, X0 - 8, Y0 + S * u, `${NB} = ${b}`, true);
          f1 = `(${NA} + ${NB})² = ${T('a2', NA + '²')} + ${T('ab', `2${NA}${NB}`)} + ${T('b2', NB + '²')}`;
          f2 = `(${a} + ${b})² = ${T('a2', a * a)} + ${T('ab', `2×${a * b}`)} + ${T('b2', b * b)} = <b>${S * S}</b>`;
        } else if (id === 'sq_diff') {
          const u = Math.min(210 / a, 250 / a), X0 = 72 + (250 - a * u) / 2, Y0 = 26, d = a - b;
          g += part('d2', X0, Y0, d * u, d * u, u, C.big, `(${NA}−${NB})²`);
          g += part('ab', X0 + d * u, Y0, b * u, d * u, u, C.cut, '', 'opacity=".8"') + part('ab', X0, Y0 + d * u, d * u, b * u, u, C.cut, '', 'opacity=".8"');
          g += part('b2', X0 + d * u, Y0 + d * u, b * u, b * u, u, '#c2410c', `${NB}²`);
          g += `<rect x="${X0 + d * u}" y="${Y0}" width="${b * u}" height="${a * u}" fill="none" stroke="#ff6b6b" stroke-width="2.5" stroke-dasharray="6 4" rx="3"/><rect x="${X0}" y="${Y0 + d * u}" width="${a * u}" height="${b * u}" fill="none" stroke="#ff6b6b" stroke-width="2.5" stroke-dasharray="6 4" rx="3"/>`;
          g += `<rect x="${X0}" y="${Y0}" width="${a * u}" height="${a * u}" fill="none" stroke="#1b1f3a" stroke-width="2" rx="3"/>`;
          g += side(X0, Y0 - 8, X0 + a * u, Y0 - 8, `${NA} = ${a}`) + side(X0 - 8, Y0, X0 - 8, Y0 + d * u, `${NA}−${NB} = ${d}`, true) + side(X0 - 8, Y0 + d * u, X0 - 8, Y0 + a * u, `${NB} = ${b}`, true);
          g += `<text x="${X0 + a * u + 6}" y="${Y0 + 12}" font-size="10.5" font-weight="800" fill="#ff6b6b">strip ${NA}×${NB}</text>`;
          f1 = `(${NA} − ${NB})² = ${NA}² − ${T('ab', `2${NA}${NB}`)} + ${T('b2', NB + '²')}`;
          f2 = `(${a} − ${b})² = ${a * a} − ${T('ab', `2×${a * b}`)} + ${T('b2', b * b)} = <b>${d * d}</b> <span style="font-size:11px">(${NB}² was cut away twice, so add it back)</span>`;
        } else if (id === 'diff_sq') {
          const d = a - b, u = Math.min(205 / a, 280 / (a + b)), X0 = 70 + (280 - (a + b) * u) / 2, Y0 = 28;
          const y1 = Y0 + d * u;
          g += part('p1', X0, Y0, a * u, d * u, u, C.big, `${NA}×(${NA}−${NB})`);
          const tx = X0 + a * u + y1 + b * u, ty = Y0 - X0;
          g += `<g class="lb-algebratiles-mv" style="transform:${rearr ? `translate(${tx}px,${ty}px) rotate(90deg)` : 'none'}">${part('p2', X0, y1, d * u, b * u, u, C.mid, `${NB}×(${NA}−${NB})`)}</g>`;
          if (!rearr) g += `<rect x="${X0 + d * u}" y="${y1}" width="${b * u}" height="${b * u}" fill="#fff" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="5 4" rx="3"/><text x="${X0 + d * u + b * u / 2}" y="${y1 + b * u / 2 + 4}" text-anchor="middle" font-size="11" font-weight="800" fill="#ff6b6b">${b * u > 40 ? `${NB}² cut` : '✂'}</text>`;
          if (rearr) g += `<rect x="${X0}" y="${Y0}" width="${a * u}" height="${a * u}" fill="none" stroke="#b5bae0" stroke-width="1.5" stroke-dasharray="4 4" rx="3"/><text x="${X0 + a * u / 2}" y="${Y0 + a * u - 8}" text-anchor="middle" font-size="11" font-weight="800" fill="#9aa0c8">was ${NA}² − ${NB}²</text>`;
          if (rearr) g += side(X0, Y0 - 8, X0 + (a + b) * u, Y0 - 8, `${NA} + ${NB} = ${a + b}`, false, '#3b82f6') + side(X0 - 8, Y0, X0 - 8, Y0 + d * u, `${NA}−${NB} = ${d}`, true, '#3b82f6');
          else g += side(X0, Y0 - 8, X0 + a * u, Y0 - 8, `${NA} = ${a}`) + side(X0 - 8, Y0, X0 - 8, Y0 + a * u, `${a}`, true);
          f1 = `${NA}² − ${NB}² = ${T('p1', `(${NA} + ${NB})`)}${T('p2', `(${NA} − ${NB})`)}`;
          f2 = `${a * a} − ${b * b} = (${a} + ${b}) × (${a} − ${b}) = ${a + b} × ${d} = <b>${a * a - b * b}</b>`;
        } else {
          const W = x + a, H = x + b, u = Math.min(205 / H, 280 / W), X0 = 66 + (280 - W * u) / 2, Y0 = 26;
          g += part('x2', X0, Y0, x * u, x * u, u, C.big, 'x²') + part('ax', X0 + x * u, Y0, a * u, x * u, u, C.mid, `${NA}x`)
            + part('bx', X0, Y0 + x * u, x * u, b * u, u, C.blue, `${NB}x`) + part('ab', X0 + x * u, Y0 + x * u, a * u, b * u, u, C.small, `${NA}${NB}`);
          g += side(X0, Y0 - 8, X0 + x * u, Y0 - 8, `x = ${x}`) + side(X0 + x * u, Y0 - 8, X0 + W * u, Y0 - 8, `${NA} = ${a}`) + side(X0 - 8, Y0, X0 - 8, Y0 + x * u, `x`, true) + side(X0 - 8, Y0 + x * u, X0 - 8, Y0 + H * u, `${NB} = ${b}`, true);
          const cx = k => (k === 1 ? '' : k) + 'x';
          f1 = `(x + ${a})(x + ${b}) = ${T('x2', 'x²')} + ${T('ax', cx(a))} + ${T('bx', cx(b))} + ${T('ab', a * b)}`;
          f2 = `<span style="font-family:'Baloo 2',Nunito;font-size:16px;color:#1b1f3a">= x² + ${cx(a + b)} + ${a * b}</span><br>x = ${x}: ${T('x2', x * x)} + ${T('ax', a * x)} + ${T('bx', b * x)} + ${T('ab', a * b)} = <b>${W * H}</b> = ${W} × ${H}`;
        }
        svg.innerHTML = g;
        if (hi) svg.querySelectorAll('.lb-algebratiles-pc').forEach(e => { e.style.opacity = e.dataset.t === hi ? 1 : 0.35; });
        F.innerHTML = `<div class="big">${f1}</div><div class="num">${f2}</div>`;
        host.querySelectorAll('[data-v]').forEach(e => { e.textContent = v[e.dataset.v]; });
        const rb = $('[data-a="re"]'); if (rb) rb.textContent = rearr ? 'Put back ↺' : 'Rearrange ↻';
      }
      function check() {
        if (won) return;
        let ok = false, msg = '';
        if (ch.kind === 'match') { ok = v.a + v.b === ch.s && v.a * v.b === ch.p; msg = `(x + ${v.a})(x + ${v.b}) = x² + ${ch.s}x + ${ch.p}: the numbers add to ${ch.s} and multiply to ${ch.p}.`; }
        else {
          ok = area() === ch.t && (!needRe || rearr) && Object.keys(fix).every(k => v[k] === +fix[k]);
          msg = id === 'sq_sum' ? `(${v.a} + ${v.b})² = ${v.a * v.a} + ${2 * v.a * v.b} + ${v.b * v.b} = ${ch.t}` : id === 'sq_diff' ? `(${v.a} − ${v.b})² = ${v.a * v.a} − ${2 * v.a * v.b} + ${v.b * v.b} = ${ch.t}`
            : id === 'diff_sq' ? `${v.a}² − ${v.b}² = (${v.a} + ${v.b})(${v.a} − ${v.b}) = ${v.a + v.b} × ${v.a - v.b} = ${ch.t}` : `(${v.x} + ${v.a})(${v.x} + ${v.b}) = ${ch.t}`;
        }
        if (ok) { won = true; api.sfx('correct'); api.win(msg); }
      }
      function onInput(e) {
        const k = e.target.dataset && e.target.dataset.k; if (!k) return;
        v[k] = cl(k, e.target.value);
        if (needAgtB) {
          if (k === 'a' && v.b >= v.a) { v.b = v.a - 1; const bi = $('[data-k="b"]'); if (bi) bi.value = v.b; }
          if (k === 'b' && v.b >= v.a) { v.b = v.a - 1; e.target.value = v.b; }
        }
        draw(); check();
      }
      function onClick(e) {
        const b = e.target.closest('[data-a="re"]');
        if (b) { rearr = !rearr; api.sfx('tap'); draw(); check(); return; }
        const pc = e.target.closest('[data-t]');
        if (pc && pc.dataset.t) { hi = hi === pc.dataset.t ? null : pc.dataset.t; api.sfx('tap'); draw(); }
      }
      host.addEventListener('input', onInput);
      host.addEventListener('click', onClick);
      draw();
      return () => { host.removeEventListener('input', onInput); host.removeEventListener('click', onClick); };
    },
    example: { identity: 'sq_sum', a: 4, b: 2, x: 3, aRange: [1, 8], bRange: [1, 6], xRange: [1, 7], names: ['a', 'b'] },
    examples: [
      { identity: 'xab', x: 3, a: 1, b: 1, match: [5, 6], challenge: 'Find a and b so (x + a)(x + b) = x² + 5x + 6.' },
      { identity: 'diff_sq', a: 6, b: 2, target: 33, challenge: 'Make a² − b² = 33, then Rearrange to see (a + b)(a − b).' },
      { identity: 'sq_diff', a: 6, b: 1, target: 16, fix: { a: 7 }, challenge: 'With a = 7, make (a − b)² = 16. What is b?' }
    ]
  });
})();
