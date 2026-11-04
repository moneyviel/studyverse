/* StudyVerse Concept Lab: fractionbar — "Fraction bars & pies"
 * The child slices wholes into equal parts, taps parts to shade them and sees the fraction change live.
 *
 * PARAMS (all optional)
 *  name        type            meaning                                                              default
 *  mode        string          'identify'   : shade a bar/pie to show `a`                           'identify'
 *                              'equivalent' : top bar shows `a`; re-slice the bottom bar and shade an
 *                                             equal amount (equivalent fraction)
 *                              'compare'    : shade `a` and `b`, then pick <, = or >
 *                              'add'        : bars for `a` and `b`; build the answer a + b
 *                              'subtract'   : bars for `a` and `b`; build the answer a − b
 *                              'collection' : put `total` objects into equal groups; pick `a` of them
 *  a           string|number   main fraction, e.g. "3/4", "1 1/2", 0.5                               "3/4"
 *  b           string|number   second fraction (compare / add / subtract)                            "1/2"
 *  shape       string          'bar' or 'pie' (identify & equivalent only)                           'bar'
 *  slice       boolean         child may change the number of parts with − / +                       identify/compare: false, others: true
 *  parts       number          starting number of parts in the child's bar                           identify: a's denominator, else 1 (equivalent: a's)
 *  den         number          equivalent mode: required denominator of the answer (e.g. 8 → ?/8)    any other denominator
 *  maxParts    number          largest number of parts allowed                                       12
 *  total       number          collection mode: number of objects                                    12
 *  item        string          collection object: 'apple' | 'star' | 'ball' | 'flower' | 'sweet' |
 *                              'mango' or any emoji                                                  'apple'
 *  itemName    string          word used in messages (any language)                                  'apples' etc.
 *  showDecimal boolean         also show the decimal value                                            false
 *  newChallenge boolean        show the "New" button                                                  true
 *  challenge   string          challenge text (any language); default generated                      auto
 */
(function () {
  const T = 'fractionbar';
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a || 1; };
  const lcm = (a, b) => a / gcd(a, b) * b;
  const red = q => { const g = gcd(q.n, q.d); return { n: q.n / g, d: q.d / g }; };
  const eq = (a, b) => a.n * b.d === b.n * a.d;
  function parseF(v, def) {
    if (v == null || v === '') return def;
    const s = String(v).trim().replace(/[−–]/g, '-');
    let m = s.match(/^(\d+)\s+(\d+)\/(\d+)$/); if (m && +m[3]) return { n: +m[1] * +m[3] + +m[2], d: +m[3] };
    m = s.match(/^(\d+)\/(\d+)$/); if (m && +m[2]) return { n: +m[1], d: +m[2] };
    const f = parseFloat(s); if (isFinite(f) && f >= 0) { let d = 1; while (Math.abs(Math.round(f * d) - f * d) > 1e-9 && d < 1000) d *= 10; return red({ n: Math.round(f * d), d }); }
    return def;
  }
  const ftxt = q => q.d === 1 ? String(q.n) : `${q.n}/${q.d}`;
  const fhtml = (q, col) => q.d === 1 ? `<b style="color:${col || 'inherit'}">${q.n}</b>` : `<span class="lb-fractionbar-fr" style="color:${col || 'inherit'}"><b>${q.n}</b><b>${q.d}</b></span>`;

  const ITEMS = {
    apple: '<circle cx="12" cy="14" r="9" fill="#ff6b6b"/><circle cx="8.5" cy="11" r="2.4" fill="#fff" opacity=".45"/><path d="M12 6q1-4 4-4" stroke="#7a4a1f" stroke-width="1.8" fill="none"/><path d="M13 5q4-3 7 0q-4 3-7 0" fill="#2ed3a5"/>',
    mango: '<path d="M5 15q0-10 10-10q6 1 6 8q-1 9-9 9q-7-1-7-7z" fill="#ffc93c" stroke="#f0a020" stroke-width="1.4"/><path d="M14 5q2-3 5-2q-2 3-5 2z" fill="#2ed3a5"/>',
    star: '<path d="M12 2l3 6.5 7 .8-5.2 4.8 1.5 7-6.3-3.6-6.3 3.6 1.5-7L2 9.3l7-.8z" fill="#ffc93c" stroke="#e0a400" stroke-width="1.2" stroke-linejoin="round"/>',
    ball: '<circle cx="12" cy="12" r="9.5" fill="#3b82f6"/><path d="M2.6 11q9.4 4 18.8 0M12 2.5q-4 9.5 0 19" stroke="#fff" stroke-width="1.6" fill="none"/>',
    flower: '<g fill="#ff8fb3"><circle cx="12" cy="6" r="4"/><circle cx="18" cy="11" r="4"/><circle cx="15.5" cy="18" r="4"/><circle cx="8.5" cy="18" r="4"/><circle cx="6" cy="11" r="4"/></g><circle cx="12" cy="12.5" r="3.6" fill="#ffc93c"/>',
    sweet: '<path d="M2 12l4-4v8zM22 12l-4-4v8z" fill="#ff6b6b"/><ellipse cx="12" cy="12" rx="7" ry="6" fill="#8b5cf6"/><path d="M8 9q4 6 8 0" stroke="#fff" stroke-width="1.5" fill="none" opacity=".6"/>'
  };
  const ITEMWORD = { apple: 'apples', mango: 'mangoes', star: 'stars', ball: 'balls', flower: 'flowers', sweet: 'sweets' };
  const itemSVG = (it, sz) => ITEMS[it] ? `<svg width="${sz}" height="${sz}" viewBox="0 0 24 24" aria-hidden="true">${ITEMS[it]}</svg>` : `<span style="font-size:${sz - 4}px;line-height:${sz}px">${esc(it)}</span>`;

  const CSS = `
  .lb-fractionbar-w{user-select:none;-webkit-user-select:none}
  .lb-fractionbar-ch{font-weight:800;font-size:14.5px;line-height:1.3;color:#1b1f3a;background:#f4f0ff;border-radius:14px;padding:9px 12px;margin-bottom:8px}
  .lb-fractionbar-stage{background:#fbfbff;border-radius:18px;box-shadow:inset 0 0 0 2px #eceefa;padding:6px 4px}
  .lb-fractionbar-svg{display:block;width:100%;height:auto;touch-action:manipulation}
  .lb-fractionbar-svg [data-k]{cursor:pointer}
  .lb-fractionbar-svg .pt{transition:fill .18s}
  .lb-fractionbar-eq{margin:8px 0 2px;text-align:center;font-weight:800;font-size:24px;color:#1b1f3a;min-height:40px;display:flex;align-items:center;justify-content:center;gap:7px;flex-wrap:wrap}
  .lb-fractionbar-fr{display:inline-flex;flex-direction:column;align-items:center;line-height:1;font-size:.8em;vertical-align:middle}
  .lb-fractionbar-fr b{display:block;padding:0 3px}.lb-fractionbar-fr b:first-child{border-bottom:2.5px solid currentColor;padding-bottom:2px;margin-bottom:1px}
  .lb-fractionbar-sub{text-align:center;color:#6b7090;font-weight:700;font-size:13px;min-height:18px}
  .lb-fractionbar-hint{text-align:center;font-weight:800;font-size:13.5px;color:#7c4ddb;min-height:20px;margin:4px 0 6px}
  .lb-fractionbar-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;align-items:center}
  .lb-fractionbar-s{height:44px;min-width:44px;border:none;border-radius:14px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 4px 0 #d3d7ef;padding:0 13px}
  .lb-fractionbar-s:active{transform:translateY(3px);box-shadow:0 1px 0 #d3d7ef}
  .lb-fractionbar-s.big{font-size:22px;min-width:54px;background:#8b5cf6;color:#fff;box-shadow:0 4px 0 #5b33c9}
  .lb-fractionbar-s.big:active{box-shadow:0 1px 0 #5b33c9}
  .lb-fractionbar-s.pick{background:#2ed3a5;box-shadow:0 4px 0 #1a9c78}
  .lb-fractionbar-sl{display:flex;align-items:center;gap:6px;background:#f4f0ff;border-radius:16px;padding:4px 6px;font-weight:800;font-size:14px;color:#5b33c9}
  .lb-fractionbar-sl .lb-fractionbar-s{height:40px;min-width:42px;font-size:20px;background:#fff;box-shadow:0 3px 0 #d9ccff}
  .lb-fractionbar-sl output{min-width:24px;text-align:center;font-size:18px}
  .lb-fractionbar-groups{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;padding:4px}
  .lb-fractionbar-g{border:2.5px dashed #c9cde6;border-radius:14px;padding:4px;display:flex;flex-wrap:wrap;justify-content:center;align-content:center;gap:1px;cursor:pointer;background:#fff;transition:background .2s,border-color .2s,transform .15s;min-height:40px}
  .lb-fractionbar-g.on{background:#efe8ff;border:2.5px solid #8b5cf6;transform:scale(1.04)}
  .lb-fractionbar-g.left{border-color:#ff6b6b;background:#fff3f3;cursor:default}
  .lb-fractionbar-g svg{display:block}
  `;

  Labs.register(T, {
    title: 'Fraction bars & pies',
    subjects: ['maths'],
    render(host, p, api) {
      const MODES = ['identify', 'equivalent', 'compare', 'add', 'subtract', 'collection'];
      const mode = MODES.includes(p.mode) ? p.mode : 'identify';
      const maxParts = Math.max(2, Math.min(24, +p.maxParts || 12));
      let A = red(parseF(p.a, { n: 3, d: 4 })), B = red(parseF(p.b, { n: 1, d: 2 }));
      // keep denominators drawable
      const fixF = q => (q.d > maxParts ? { n: 1, d: 2 } : q);
      A = fixF(A); B = fixF(B);
      if (mode === 'subtract' && A.n * B.d < B.n * A.d) { const t = A; A = B; B = t; }
      const shape = p.shape === 'pie' && (mode === 'identify' || mode === 'equivalent') ? 'pie' : 'bar';
      const slice = mode === 'compare' ? false : p.slice != null ? !!p.slice : mode !== 'identify';
      let total = Math.max(2, Math.min(36, Math.round(+p.total || 12)));
      const item = p.item || 'apple';
      const itemWord = p.itemName || ITEMWORD[item] || 'objects';
      let den = +p.den > 1 ? Math.round(+p.den) : 0;
      let customText = p.challenge ? String(p.challenge) : '';
      if (mode === 'collection' && total % A.d) total = A.d * Math.max(1, Math.round(total / A.d));

      // ---------- state ----------
      let parts, shaded, partsB, shadedB, groups, picked, symbol;
      const result = () => mode === 'add' ? red({ n: A.n * B.d + B.n * A.d, d: A.d * B.d }) : red({ n: A.n * B.d - B.n * A.d, d: A.d * B.d });
      function resetState() {
        shaded = new Set(); shadedB = new Set(); picked = new Set(); symbol = '';
        if (mode === 'identify') parts = +p.parts > 0 ? Math.min(maxParts, Math.round(+p.parts)) : (slice ? 1 : A.d);
        else if (mode === 'equivalent') parts = +p.parts > 0 ? Math.min(maxParts, Math.round(+p.parts)) : A.d;
        else if (mode === 'compare') { parts = A.d; partsB = B.d; }
        else parts = +p.parts > 0 && slice ? Math.min(maxParts, Math.round(+p.parts)) : (slice ? 1 : lcm(A.d, B.d));
        groups = 1;
      }
      resetState();

      function defaultText() {
        switch (mode) {
          case 'identify': return slice ? `Cut the ${shape === 'pie' ? 'pie' : 'bar'} into equal parts and shade ${ftxt(A)} of it` : `Shade ${ftxt(A)} of the ${shape === 'pie' ? 'pie' : 'bar'}`;
          case 'equivalent': return den ? `Cut the bottom ${shape === 'pie' ? 'pie' : 'bar'} into ${den} parts and shade the same amount as ${ftxt(A)}` : `Find a fraction equal to ${ftxt(A)} — use a different number of parts`;
          case 'compare': return `Shade ${ftxt(A)} and ${ftxt(B)}. Which is bigger?`;
          case 'add': return `Find ${ftxt(A)} + ${ftxt(B)}: slice the answer bar so both fit, then shade`;
          case 'subtract': return `Find ${ftxt(A)} − ${ftxt(B)}: slice the answer bar, then shade what is left`;
          default: return `Find ${ftxt(A)} of ${total} ${itemWord}: make equal groups, then tap groups`;
        }
      }

      host.innerHTML = `<style>${CSS}</style><div class="lb-fractionbar-w">
        <div class="lb-fractionbar-ch"></div>
        <div class="lb-fractionbar-stage"></div>
        <div class="lb-fractionbar-eq"></div>
        <div class="lb-fractionbar-sub"></div>
        <div class="lb-fractionbar-hint"></div>
        <div class="lb-fractionbar-row"></div></div>`;
      const $ = s => host.querySelector(s);
      const stage = $('.lb-fractionbar-stage'), eqEl = $('.lb-fractionbar-eq'), subEl = $('.lb-fractionbar-sub'), hintEl = $('.lb-fractionbar-hint'), rowEl = $('.lb-fractionbar-row'), chEl = $('.lb-fractionbar-ch');
      const hint = t => { hintEl.textContent = t || ''; };
      const COL = { a: '#8b5cf6', b: '#3b82f6', ans: '#2ed3a5', dA: '#6a3fd0', dB: '#2563c9', dAns: '#1a9c78', empty: '#ffffff' };

      // ---------- SVG helpers ----------
      const W = 360, LX = 56, BW = W - LX - 8;
      function svgFrac(q, x, y, col) {
        if (q.d === 1) return `<text x="${x}" y="${y + 6}" text-anchor="middle" font-size="20" font-weight="800" fill="${col}">${q.n}</text>`;
        return `<g fill="${col}" font-weight="800" text-anchor="middle"><text x="${x}" y="${y - 3}" font-size="16">${q.n}</text><line x1="${x - 13}" x2="${x + 13}" y1="${y + 1}" y2="${y + 1}" stroke="${col}" stroke-width="2.4"/><text x="${x}" y="${y + 17}" font-size="16">${q.d}</text></g>`;
      }
      // bar: wholes = how many whole bars side by side, per = parts per whole, isOn(i) shading, key for taps
      function bar(y, h, unitW, wholes, per, isOn, col, dark, key) {
        let s = '';
        const pw = unitW / per;
        for (let w = 0; w < wholes; w++) {
          const x0 = LX + w * unitW;
          for (let i = 0; i < per; i++) {
            const k = w * per + i, on = isOn(k);
            s += `<rect class="pt" ${key ? `data-k="${key}" data-i="${k}"` : ''} x="${(x0 + i * pw).toFixed(2)}" y="${y}" width="${pw.toFixed(2)}" height="${h}" fill="${on ? col : COL.empty}" stroke="${dark}" stroke-width="2"/>`;
          }
          s += `<rect x="${x0}" y="${y}" width="${unitW}" height="${h}" rx="3" fill="none" stroke="#1b1f3a" stroke-width="2.6" pointer-events="none"/>`;
        }
        return s;
      }
      function pie(cx, cy, r, per, isOn, col, dark, key) {
        let s = '';
        if (per === 1) return `<circle class="pt" ${key ? `data-k="${key}" data-i="0"` : ''} cx="${cx}" cy="${cy}" r="${r}" fill="${isOn(0) ? col : COL.empty}" stroke="${dark}" stroke-width="2.4"/>`;
        for (let i = 0; i < per; i++) {
          const a0 = -Math.PI / 2 + i * 2 * Math.PI / per, a1 = a0 + 2 * Math.PI / per;
          const x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0), x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
          s += `<path class="pt" ${key ? `data-k="${key}" data-i="${i}"` : ''} d="M${cx} ${cy}L${x0.toFixed(2)} ${y0.toFixed(2)}A${r} ${r} 0 ${per === 2 ? 0 : 0} 1 ${x1.toFixed(2)} ${y1.toFixed(2)}Z" fill="${isOn(i) ? col : COL.empty}" stroke="${dark}" stroke-width="2" stroke-linejoin="round"/>`;
        }
        return s + `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#1b1f3a" stroke-width="2.6" pointer-events="none"/>`;
      }
      const fill = (q) => k => k < q.n * 1; // first n parts shaded (for display bars, per = q.d)

      // ---------- drawing ----------
      function draw() {
        if (mode === 'collection') return drawCollection();
        let s = '', H = 0;
        const cur = { n: shaded.size, d: parts };
        if (mode === 'identify') {
          if (shape === 'pie') { H = 190; s += pie(W / 2, 95, 88, parts, k => shaded.has(k), COL.a, COL.dA, 'u'); }
          else { H = 92; s += svgFrac(cur, 28, 46, COL.dA) + bar(16, 60, BW, 1, parts, k => shaded.has(k), COL.a, COL.dA, 'u'); }
        } else if (mode === 'equivalent') {
          if (shape === 'pie') {
            H = 170;
            s += pie(92, 82, 74, A.d, k => k < A.n, COL.b, COL.dB) + pie(268, 82, 74, parts, k => shaded.has(k), COL.a, COL.dA, 'u');
            s += `<text x="180" y="92" text-anchor="middle" font-size="26" font-weight="800" fill="${eq(cur, A) && cur.n ? '#14a37f' : '#c0c4dc'}">${eq(cur, A) && cur.n ? '=' : '?'}</text>`;
          } else {
            H = 150;
            s += svgFrac(A, 28, 38, COL.dB) + bar(10, 52, BW, 1, A.d, k => k < A.n, COL.b, COL.dB);
            s += svgFrac(cur, 28, 110, COL.dA) + bar(82, 52, BW, 1, parts, k => shaded.has(k), COL.a, COL.dA, 'u');
            const gx = LX + BW * A.n / A.d;
            s += `<line x1="${gx}" x2="${gx}" y1="4" y2="${H - 4}" stroke="#ff6b6b" stroke-width="2.4" stroke-dasharray="5 4" pointer-events="none"/>`;
          }
        } else if (mode === 'compare') {
          H = 150; const curB = { n: shadedB.size, d: partsB };
          s += svgFrac(A, 28, 38, COL.dA) + bar(10, 52, BW, 1, A.d, k => shaded.has(k), COL.a, COL.dA, 'u');
          s += svgFrac(B, 28, 110, COL.dB) + bar(82, 52, BW, 1, B.d, k => shadedB.has(k), COL.b, COL.dB, 'v');
          if (shaded.size === A.n && shadedB.size === B.n) {
            // guide lines at the end of each amount (only meaningful when shaded from the left, so draw lengths)
            const xa = LX + BW * A.n / A.d, xb = LX + BW * B.n / B.d;
            s += `<line x1="${xa}" x2="${xa}" y1="4" y2="${H - 4}" stroke="${COL.dA}" stroke-width="2" stroke-dasharray="4 4" pointer-events="none"/>`;
            s += `<line x1="${xb}" x2="${xb}" y1="4" y2="${H - 4}" stroke="${COL.dB}" stroke-width="2" stroke-dasharray="4 4" pointer-events="none"/>`;
          }
        } else { // add / subtract
          const R = result();
          const wholes = Math.max(1, Math.ceil(Math.max(R.n / R.d, A.n / A.d, B.n / B.d) - 1e-9));
          const uw = BW / wholes;
          const wa = Math.max(1, Math.ceil(A.n / A.d - 1e-9)), wb = Math.max(1, Math.ceil(B.n / B.d - 1e-9));
          H = 222;
          s += svgFrac(A, 28, 30, COL.dA) + bar(6, 44, uw, wa, A.d, k => k < A.n, COL.a, COL.dA);
          s += svgFrac(B, 28, 84, COL.dB) + bar(60, 44, uw, wb, B.d, k => k < B.n, COL.b, COL.dB);
          // guide strip: a then b (add) or a with b taken off the end (subtract)
          const xa = uw * A.n / A.d, xb = uw * B.n / B.d, sy = 114;
          if (mode === 'add') {
            s += `<rect x="${LX}" y="${sy}" width="${xa}" height="12" rx="4" fill="${COL.a}" opacity=".85"/><rect x="${LX + xa}" y="${sy}" width="${xb}" height="12" rx="4" fill="${COL.b}" opacity=".85"/>`;
          } else {
            s += `<rect x="${LX}" y="${sy}" width="${xa - xb}" height="12" rx="4" fill="${COL.a}" opacity=".85"/><rect x="${LX + xa - xb}" y="${sy}" width="${xb}" height="12" rx="4" fill="url(#lbfbHatch)" stroke="${COL.dB}" stroke-width="1.4"/>`;
          }
          s += `<text x="28" y="${sy + 11}" text-anchor="middle" font-size="11" font-weight="800" fill="#6b7090">${mode === 'add' ? 'a + b' : 'a − b'}</text>`;
          const end = LX + (mode === 'add' ? xa + xb : xa - xb);
          s += `<line x1="${end}" x2="${end}" y1="${sy - 2}" y2="${H - 4}" stroke="#ff6b6b" stroke-width="2.4" stroke-dasharray="5 4" pointer-events="none"/>`;
          const cur2 = { n: shaded.size, d: parts };
          s += svgFrac(cur2, 28, 172, COL.dAns) + bar(140, 64, uw, wholes, parts, k => k < shaded.size, COL.ans, COL.dAns, 'u');
        }
        stage.innerHTML = `<svg class="lb-fractionbar-svg" viewBox="0 0 ${W} ${H}"><defs><pattern id="lbfbHatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#fff"/><line x1="0" y1="0" x2="0" y2="6" stroke="#3b82f6" stroke-width="2.5"/></pattern></defs>${s}</svg>`;
      }
      function drawCollection() {
        const per = Math.floor(total / groups), left = total - per * groups;
        const sz = total > 24 ? 20 : 24;
        const cols = Math.ceil(Math.sqrt(per)) || 1;
        let s = '<div class="lb-fractionbar-groups">';
        for (let g = 0; g < groups; g++) {
          s += `<div class="lb-fractionbar-g${picked.has(g) ? ' on' : ''}" data-g="${g}" style="width:${cols * (sz + 1) + 14}px">`;
          for (let i = 0; i < per; i++) s += itemSVG(item, sz);
          s += '</div>';
        }
        if (left) { s += `<div class="lb-fractionbar-g left" style="width:${Math.ceil(Math.sqrt(left)) * (sz + 1) + 14}px">`; for (let i = 0; i < left; i++) s += itemSVG(item, sz); s += '</div>'; }
        stage.innerHTML = s + '</div>';
      }

      // ---------- readouts ----------
      function readout() {
        let e = '', sub = '';
        const cur = { n: shaded.size, d: parts };
        const dec = q => p.showDecimal ? ` <span style="color:#6b7090;font-size:.75em">= ${+(q.n / q.d).toFixed(3)}</span>` : '';
        if (mode === 'identify') {
          e = `${fhtml(cur, COL.dA)}<span style="font-size:.7em;color:#6b7090">shaded</span>${cur.n ? dec(cur) : ''}`;
          sub = `${cur.n} of ${parts} equal part${parts > 1 ? 's' : ''}` + (cur.n && gcd(cur.n, cur.d) > 1 ? ` · simplest form ${ftxt(red(cur))}` : '');
        } else if (mode === 'equivalent') {
          const ok = cur.n > 0 && eq(cur, A);
          e = `${fhtml(A, COL.dB)}<span style="color:${ok ? '#14a37f' : '#c0c4dc'}">${ok ? '=' : (cur.n * A.d < A.n * cur.d ? '>' : '<')}</span>${fhtml(cur, COL.dA)}`;
          sub = ok ? (cur.d !== A.d ? `${A.n}×${cur.d / A.d >= 1 && cur.d % A.d === 0 ? cur.d / A.d : '…'} / ${A.d}×${cur.d % A.d === 0 ? cur.d / A.d : '…'} — same amount, more parts` : 'Same fraction — now try more parts!') : 'Line up the shading with the red dashed line';
          if (ok && cur.d % A.d !== 0) sub = 'Same amount, different parts!';
          if (ok && cur.d % A.d === 0 && cur.d !== A.d) sub = `Multiply top and bottom by ${cur.d / A.d}: ${A.n}×${cur.d / A.d} / ${A.d}×${cur.d / A.d} = ${cur.n}/${cur.d}`;
          if (ok && cur.d < A.d) sub = `Divide top and bottom by ${A.d / cur.d}: simplest form!`;
        } else if (mode === 'compare') {
          const curB = { n: shadedB.size, d: partsB };
          e = `${fhtml(cur, COL.dA)}<span style="color:#ff6b6b;min-width:22px">${symbol || '?'}</span>${fhtml(curB, COL.dB)}`;
          sub = shaded.size === A.n && shadedB.size === B.n ? 'Which bar has more shaded? Pick a sign.' : `Shade ${ftxt(A)} of the top bar and ${ftxt(B)} of the bottom bar`;
        } else if (mode === 'add' || mode === 'subtract') {
          e = `${fhtml(A, COL.dA)}<span>${mode === 'add' ? '+' : '−'}</span>${fhtml(B, COL.dB)}<span>=</span>${shaded.size ? fhtml(cur, COL.dAns) : `<span class="lb-fractionbar-fr" style="color:#c0c4dc"><b>?</b><b>${parts}</b></span>`}`;
          const L = lcm(A.d, B.d);
          sub = parts % A.d === 0 && parts % B.d === 0 ? `${ftxt(A)} = ${A.n * parts / A.d}/${parts},  ${ftxt(B)} = ${B.n * parts / B.d}/${parts}` : (A.d === B.d ? 'Same-size parts: just count them' : `Tip: pick parts that fit both ${A.d}ths and ${B.d}ths (like ${L})`);
          if (A.d === 2 || B.d === 2 || A.d === 3 || B.d === 3) sub = sub.replace(/(\d+)ths/g, (m, d) => ({ 2: 'halves', 3: 'thirds', 4: 'quarters' }[d] || d + 'ths'));
        } else {
          const per = Math.floor(total / groups), left = total - per * groups;
          const k = picked.size;
          e = `${groups > 1 ? fhtml({ n: k, d: groups }, COL.dA) : `<b>${k}</b>`}<span style="font-size:.7em">of ${total} =</span><b style="color:#14a37f">${k * per}</b><span style="font-size:.7em">${esc(itemWord)}</span>`;
          sub = left ? `${total} ${itemWord} do not make ${groups} equal groups — ${left} left over!` : `${groups} equal group${groups > 1 ? 's' : ''} of ${per}`;
        }
        eqEl.innerHTML = e; subEl.textContent = sub;
      }

      // ---------- controls ----------
      function buildRow() {
        let s = '';
        if (mode === 'collection') s += `<div class="lb-fractionbar-sl"><span>Groups</span><button class="lb-fractionbar-s" data-act="minus">−</button><output>${groups}</output><button class="lb-fractionbar-s" data-act="plus">+</button></div>`;
        else if (slice) s += `<div class="lb-fractionbar-sl"><span>Parts</span><button class="lb-fractionbar-s" data-act="minus">−</button><output>${parts}</output><button class="lb-fractionbar-s" data-act="plus">+</button></div>`;
        if (mode === 'compare') ['<', '=', '>'].forEach(c => { s += `<button class="lb-fractionbar-s big${symbol === c ? ' pick' : ''}" data-sym="${c}">${c === '<' ? '&lt;' : c === '>' ? '&gt;' : c}</button>`; });
        s += `<button class="lb-fractionbar-s" data-act="reset">↺</button>`;
        if (p.newChallenge !== false) s += `<button class="lb-fractionbar-s" data-act="new">✨ New</button>`;
        rowEl.innerHTML = s;
      }
      const setText = () => { chEl.textContent = '🎯 Challenge: ' + (customText || defaultText()); };
      function refresh() { draw(); readout(); buildRow(); }

      // ---------- win logic ----------
      let won = false;
      function win(msg) { if (won) return; won = true; api.sfx('correct'); hint('⭐ Brilliant!'); api.win(msg); }
      function check() {
        if (won) return;
        const cur = { n: shaded.size, d: parts };
        if (mode === 'identify') {
          if (cur.n && eq(cur, A) && (!slice || true) && (slice || parts === A.d)) win(`${ftxt(cur)} is shaded${ftxt(cur) !== ftxt(A) ? ' — the same as ' + ftxt(A) : ''}!`);
        } else if (mode === 'equivalent') {
          if (cur.n && eq(cur, A) && (den ? parts === den : parts !== A.d)) win(`${ftxt(A)} = ${ftxt(cur)} — equivalent fractions!`);
          else if (cur.n && eq(cur, A) && parts === A.d) hint('That is the same fraction. Change the number of parts!');
          else if (cur.n && eq(cur, A) && den && parts !== den) hint(`Equal! Now try it with ${den} parts.`);
        } else if (mode === 'add' || mode === 'subtract') {
          const R = result();
          if (cur.n && eq(cur, R) || (R.n === 0 && parts > 1 && shaded.size === 0 && touched)) {
            const simp = red(cur);
            win(`${ftxt(A)} ${mode === 'add' ? '+' : '−'} ${ftxt(B)} = ${ftxt(cur)}${ftxt(simp) !== ftxt(cur) ? ' = ' + ftxt(simp) : ''}${R.n > R.d ? ` = ${Math.floor(R.n / R.d)} ${R.n % R.d}/${R.d}` : ''}`);
          }
        } else if (mode === 'collection') {
          const per = total / groups;
          if (Number.isInteger(per) && picked.size && eq({ n: picked.size, d: groups }, A)) win(`${ftxt(A)} of ${total} = ${picked.size * per} ${itemWord}`);
        }
      }
      let touched = false;

      // ---------- events ----------
      stage.addEventListener('click', e => {
        if (mode === 'collection') {
          const g = e.target.closest('[data-g]'); if (!g) return;
          const i = +g.dataset.g; picked.has(i) ? picked.delete(i) : picked.add(i);
          api.sfx('tap'); hint(''); draw(); readout(); check(); return;
        }
        const el = e.target.closest('[data-k]'); if (!el) return;
        const i = +el.dataset.i, key = el.dataset.k;
        touched = true;
        if (mode === 'add' || mode === 'subtract') {
          // fill up to the tapped part (tap the last shaded part to un-shade it)
          const n2 = i + 1 === shaded.size ? i : i + 1; shaded = new Set(Array.from({ length: n2 }, (_, k) => k));
        } else {
          const set = key === 'v' ? shadedB : shaded;
          set.has(i) ? set.delete(i) : set.add(i);
        }
        api.sfx('tap'); hint(''); draw(); readout(); check();
      });
      rowEl.addEventListener('click', e => {
        const b = e.target.closest('button'); if (!b) return;
        const a = b.dataset.act;
        if (b.dataset.sym) {
          symbol = b.dataset.sym;
          if (shaded.size !== A.n || shadedB.size !== B.n) { api.sfx('hmm'); hint(`First shade ${ftxt(A)} and ${ftxt(B)}`); symbol = ''; refresh(); return; }
          const c = A.n * B.d - B.n * A.d; const right = c > 0 ? '>' : c < 0 ? '<' : '=';
          refresh();
          if (symbol === right) win(`${ftxt(A)} ${right} ${ftxt(B)}${c ? '' : ' — they are equal!'}`);
          else { api.sfx('wrong'); hint('Look again: which shaded part is longer?'); }
          return;
        }
        if (a === 'minus' || a === 'plus') {
          const d = a === 'plus' ? 1 : -1;
          if (mode === 'collection') {
            const g2 = groups + d; if (g2 < 1 || g2 > Math.min(12, total)) { api.sfx('wrong'); return; }
            groups = g2; picked = new Set();
          } else {
            const p2 = parts + d; if (p2 < 1 || p2 > maxParts) { api.sfx('wrong'); hint(p2 < 1 ? 'At least 1 part!' : `Max ${maxParts} parts`); return; }
            parts = p2; shaded = new Set();
          }
          api.sfx('tap'); hint(''); refresh(); check(); return;
        }
        if (a === 'reset') { resetState(); hint(''); refresh(); api.sfx('tap'); return; }
        if (a === 'new') { newChallenge(); }
      });
      function newChallenge() {
        const r = n => 1 + Math.floor(Math.random() * n);
        const dens = [2, 3, 4, 5, 6, 8, 10, 12].filter(d => d <= maxParts);
        const pickD = () => dens[Math.floor(Math.random() * dens.length)];
        const old = ftxt(A) + ftxt(B);
        for (let t = 0; t < 30; t++) {
          if (mode === 'collection') { const d = [2, 3, 4, 5, 6][Math.floor(Math.random() * 5)]; A = { n: r(d - 1), d }; total = d * (1 + r(Math.max(1, Math.floor(24 / d) - 1))); A = red(A); }
          else if (mode === 'add' || mode === 'subtract') {
            const same = A.d === B.d && Math.random() < 0.5; const d1 = pickD(), d2 = same ? d1 : [2, 3, 4, 6].filter(x => x <= maxParts)[Math.floor(Math.random() * 4)] || 2;
            A = red({ n: r(d1 - 1), d: d1 }); B = red({ n: r(d2 - 1), d: d2 });
            if (mode === 'subtract' && A.n * B.d < B.n * A.d) { const tt = A; A = B; B = tt; }
            if (lcm(A.d, B.d) > maxParts) continue;
            if (mode === 'subtract' && A.n * B.d === B.n * A.d) continue;
          } else {
            const d = pickD(); A = red({ n: r(d - 1), d }); const d2 = pickD(); B = red({ n: r(d2 - 1), d: d2 });
            if (mode === 'equivalent' && den) { if (den % A.d !== 0 || den === A.d) continue; }
            if (mode === 'equivalent' && A.d * 2 > maxParts && A.d % 2) continue;
          }
          if (A.d > 1 && ftxt(A) + ftxt(B) !== old) break;
        }
        customText = '';
        if (won) { won = false; api.resetWin && api.resetWin(); }
        resetState(); touched = false; setText(); hint(''); refresh(); api.sfx('tap');
      }

      setText(); refresh();
      return () => { };
    },
    example: {
      mode: 'identify', a: '3/4', shape: 'pie'
    },
    examples: [
      { mode: 'compare', a: '2/3', b: '3/5', shape: 'bar', challenge: 'Which is more cake: 2/3 or 3/5? Shade both, then pick a sign.' },
      { mode: 'equivalent', a: '2/3', shape: 'bar', slice: true, den: 6, challenge: 'Cut the bottom bar into 6 parts and shade as much as 2/3.' },
      { mode: 'add', a: '1/2', b: '1/3', shape: 'bar', challenge: 'Add 1/2 + 1/3. Cut the answer bar so both fractions fit!' },
      { mode: 'collection', a: '2/3', total: 12, item: 'mango', itemName: 'mangoes', shape: 'bar', challenge: 'Riya gives away 2/3 of 12 mangoes. How many is that?' }
    ]
  });
})();
