/* ================= Animated explainer pictures (shown after every answer) ================= */
(function () {
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const arcD = (cx, cy, r, a) => { const rad = a * Math.PI / 180, ex = cx + r * Math.cos(rad), ey = cy - r * Math.sin(rad); return `M${cx + r} ${cy} A${r} ${r} 0 ${a > 180 ? 1 : 0} 0 ${ex.toFixed(1)} ${ey.toFixed(1)}`; };

  function angle(v) {
    const a = Math.max(0, Math.min(360, v.deg)), cx = 160, cy = 118, L = 110;
    const name = a < 90 ? 'Acute' : a === 90 ? 'Right' : a < 180 ? 'Obtuse' : a === 180 ? 'Straight' : a < 360 ? 'Reflex' : 'Full turn';
    const col = a < 90 ? '#2ed3a5' : a === 90 ? '#3b82f6' : a < 180 ? '#ff9f43' : a === 180 ? '#8b5cf6' : '#ff6b6b';
    return `<svg viewBox="0 0 320 220">
      <path d="${arcD(cx, cy, 70, 90)}" fill="none" stroke="#2ed3a5" stroke-opacity=".22" stroke-width="10"/>
      <path d="M${cx} ${cy - 70} A70 70 0 0 0 ${cx - 70} ${cy}" fill="none" stroke="#ff9f43" stroke-opacity=".22" stroke-width="10"/>
      <path d="M${cx - 70} ${cy} A70 70 0 0 0 ${cx + 70} ${cy}" fill="none" stroke="#ff6b6b" stroke-opacity=".15" stroke-width="10"/>
      <line x1="${cx}" y1="${cy}" x2="${cx + L}" y2="${cy}" stroke="#1b1f3a" stroke-width="5" stroke-linecap="round"/>
      ${a > 0 ? `<path class="draw" pathLength="100" d="${arcD(cx, cy, 34, Math.min(a, 359.9))}" fill="none" stroke="${col}" stroke-width="8" stroke-linecap="round"/>` : ''}
      <g><line x1="${cx}" y1="${cy}" x2="${cx + L}" y2="${cy}" stroke="${col}" stroke-width="5" stroke-linecap="round"/>
        <animateTransform attributeName="transform" type="rotate" from="0 ${cx} ${cy}" to="${-a} ${cx} ${cy}" dur="1.6s" fill="freeze"/></g>
      <circle cx="${cx}" cy="${cy}" r="6" fill="#1b1f3a"/>
      <g class="late"><rect x="${cx - 80}" y="4" width="160" height="28" rx="14" fill="${col}"/><text x="${cx}" y="23" font-size="15" font-weight="800" fill="#fff" text-anchor="middle">${a}° · ${name}</text></g></svg>`;
  }

  function clock(v) {
    const cx = 160, cy = 108, R = 84; let t = '';
    for (let k = 0; k < 12; k++) { const a = k * 30 * Math.PI / 180; t += `<line x1="${cx + R * .86 * Math.sin(a)}" y1="${cy - R * .86 * Math.cos(a)}" x2="${cx + R * .97 * Math.sin(a)}" y2="${cy - R * .97 * Math.cos(a)}" stroke="#1b1f3a" stroke-width="${k % 3 ? 2 : 4}"/>`;
      t += `<text x="${cx + R * .72 * Math.sin(a)}" y="${cy - R * .72 * Math.cos(a) + 4}" font-size="11" font-weight="800" text-anchor="middle">${k || 12}</text>`; }
    const hDeg = (v.h % 12) * 30 + v.m * .5, mDeg = v.m * 6;
    const label = `${v.h}:${String(v.m).padStart(2, '0')}`;
    return `<svg viewBox="0 0 320 220"><circle cx="${cx}" cy="${cy}" r="${R}" fill="#fff" stroke="#1b1f3a" stroke-width="5"/>${t}
      <g><line x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy - 64}" stroke="#ff6b6b" stroke-width="4" stroke-linecap="round"/><animateTransform attributeName="transform" type="rotate" from="0 ${cx} ${cy}" to="${mDeg} ${cx} ${cy}" dur="1.6s" fill="freeze"/></g>
      <g><line x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy - 42}" stroke="#3b82f6" stroke-width="7" stroke-linecap="round"/><animateTransform attributeName="transform" type="rotate" from="0 ${cx} ${cy}" to="${hDeg} ${cx} ${cy}" dur="1.6s" fill="freeze"/></g>
      <circle cx="${cx}" cy="${cy}" r="6" fill="#1b1f3a"/>
      <g class="late"><rect x="250" y="20" width="62" height="30" rx="12" fill="#3b82f6"/><text x="281" y="40" font-size="15" font-weight="800" fill="#fff" text-anchor="middle">${label}</text>
      <text x="281" y="66" font-size="9.5" font-weight="700" fill="#3b82f6" text-anchor="middle">short = hour</text><text x="281" y="80" font-size="9.5" font-weight="700" fill="#ff6b6b" text-anchor="middle">long = minute</text></g></svg>`;
  }

  function count(v) {
    const n = Math.min(40, v.n), g = v.groups && v.groups > 1 ? v.groups : 1;
    const per = Math.ceil(n / g); let s = '', i = 0;
    const cols = g > 1 ? Math.min(per, 8) : Math.min(n, 8);
    const cell = 30, gw = cols * cell + 14;
    const perRow = g > 1 ? Math.max(1, Math.floor(300 / gw)) : 1;
    for (let gi = 0; gi < g; gi++) {
      const gx = 10 + (gi % perRow) * gw, rowsInGroup = Math.ceil(Math.min(per, n - gi * per) / cols);
      const gy = 10 + Math.floor(gi / perRow) * (Math.ceil(per / cols) * cell + 16);
      if (g > 1) s += `<rect x="${gx - 4}" y="${gy - 4}" width="${cols * cell + 6}" height="${rowsInGroup * cell + 6}" rx="10" fill="#fff" stroke="#c9cde6" stroke-dasharray="4 4"/>`;
      for (let k = 0; k < per && i < n; k++, i++) {
        s += `<text class="popin" style="animation-delay:${(i * .06).toFixed(2)}s" x="${gx + (k % cols) * cell + cell / 2}" y="${gy + Math.floor(k / cols) * cell + 22}" font-size="22" text-anchor="middle">${v.emoji}</text>`;
      }
    }
    const H = Math.max(80, 10 + Math.ceil(g / perRow) * (Math.ceil(per / cols) * cell + 16) + 34);
    return `<svg viewBox="0 0 320 ${H}">${s}<g class="late"><text x="160" y="${H - 8}" font-size="15" font-weight="800" text-anchor="middle" fill="#8b5cf6">${g > 1 ? `${g} groups of ${per} = ${n}` : `${n} in all`}</text></g></svg>`;
  }

  function fraction(v) {
    const d = v.den, nn = v.num, wholes = Math.max(1, Math.ceil(nn / d)); let s = '';
    const bw = 280, bh = 40;
    for (let w = 0; w < wholes; w++) {
      const y = 20 + w * 56;
      for (let k = 0; k < d; k++) {
        const filled = w * d + k < nn, x = 20 + k * bw / d;
        s += `<rect x="${x}" y="${y}" width="${bw / d}" height="${bh}" fill="${filled ? '#8b5cf6' : '#fff'}" stroke="#1b1f3a" stroke-width="2" ${filled ? `class="popin" style="animation-delay:${((w * d + k) * .12).toFixed(2)}s"` : ''}/>`;
      }
    }
    const H = 20 + wholes * 56 + 30;
    return `<svg viewBox="0 0 320 ${H}">${s}<g class="late"><text x="160" y="${H - 8}" font-size="16" font-weight="800" text-anchor="middle" fill="#8b5cf6">${nn}/${d} shaded</text></g></svg>`;
  }

  function numberline(v) {
    const a = v.from, b = v.to, span = b - a, x0 = 20, x1 = 300, X = n => x0 + (n - a) / span * (x1 - x0), y = 120;
    let s = `<line x1="${x0 - 8}" y1="${y}" x2="${x1 + 8}" y2="${y}" stroke="#1b1f3a" stroke-width="3"/>`;
    const step = span <= 20 ? 1 : span <= 40 ? 2 : 5;
    for (let n = a; n <= b; n += step) s += `<line x1="${X(n)}" y1="${y - 6}" x2="${X(n)}" y2="${y + 6}" stroke="#1b1f3a" stroke-width="2"/><text x="${X(n)}" y="${y + 22}" font-size="${span > 20 ? 8 : 10}" text-anchor="middle">${n}</text>`;
    (v.jumps || []).forEach(([p, q], i) => { const mx = (X(p) + X(q)) / 2, hgt = Math.min(70, 20 + Math.abs(X(q) - X(p)) / 3);
      s += `<path class="draw" style="animation-delay:${i * .5}s" pathLength="100" d="M${X(p)} ${y - 4} Q${mx} ${y - hgt * 2} ${X(q)} ${y - 4}" fill="none" stroke="#ff6b6b" stroke-width="4" stroke-linecap="round"/>
      <text class="late" x="${mx}" y="${y - hgt - 6}" font-size="12" font-weight="800" text-anchor="middle" fill="#ff6b6b">${q - p > 0 ? '+' : ''}${+(q - p).toFixed(2)}</text>`; });
    (v.marks || []).forEach((m, i) => s += `<circle class="popin" style="animation-delay:${(.3 + i * .3).toFixed(1)}s" cx="${X(m)}" cy="${y}" r="8" fill="#8b5cf6"/><text class="late" x="${X(m)}" y="${y + 40}" font-size="13" font-weight="800" text-anchor="middle" fill="#8b5cf6">${m}</text>`);
    return `<svg viewBox="0 0 320 175">${s}</svg>`;
  }

  function bars(v) {
    const items = v.items, max = Math.max(...items.map(i => i[1]), 1), bw = 260 / items.length;
    let s = `<line x1="30" y1="170" x2="300" y2="170" stroke="#1b1f3a" stroke-width="2"/>`;
    items.forEach(([lab, val], i) => { const h = val / max * 130, x = 36 + i * bw;
      s += `<rect class="grow" style="animation-delay:${(i * .15).toFixed(2)}s;transform-origin:${x + bw * .35}px 170px" x="${x}" y="${170 - h}" width="${bw * .7}" height="${h}" rx="5" fill="${['#8b5cf6', '#2ed3a5', '#ff9f43', '#3b82f6', '#ff6b6b', '#ffc93c', '#4dd0e1', '#ba68c8'][i % 8]}"/>
      <text class="late" x="${x + bw * .35}" y="${165 - h}" font-size="11" font-weight="800" text-anchor="middle">${val}</text>
      <text x="${x + bw * .35}" y="186" font-size="10" font-weight="700" text-anchor="middle">${esc(String(lab).slice(0, 8))}</text>`; });
    return `<svg viewBox="0 0 320 195">${s}</svg>`;
  }

  function compare(v) {
    const max = Math.max(v.a[1], v.b[1], 1), W = 220;
    const row = (lab, val, y, c, d) => `<text x="10" y="${y + 18}" font-size="13" font-weight="800">${esc(String(lab).slice(0, 10))}</text><rect class="growx" style="animation-delay:${d}s" x="88" y="${y}" width="${val / max * W}" height="28" rx="8" fill="${c}"/><text class="late" x="${92 + val / max * W}" y="${y + 19}" font-size="13" font-weight="800">${val}</text>`;
    return `<svg viewBox="0 0 340 110">${row(v.a[0], v.a[1], 14, '#8b5cf6', 0)}${row(v.b[0], v.b[1], 60, '#2ed3a5', .3)}</svg>`;
  }

  function shape(v) {
    const S = {
      circle: '<circle cx="160" cy="95" r="70"/>', triangle: '<path d="M160 20 L245 165 L75 165Z"/>', square: '<rect x="90" y="25" width="140" height="140"/>',
      rectangle: '<rect x="60" y="45" width="200" height="110"/>', pentagon: '<path d="M160 20 L235 75 L207 162 L113 162 L85 75Z"/>',
      hexagon: '<path d="M120 25 L200 25 L240 95 L200 165 L120 165 L80 95Z"/>',
      cube: '<path d="M100 60 L180 60 L180 150 L100 150Z M100 60 L140 25 L220 25 L180 60 M220 25 L220 115 L180 150"/>',
      cylinder: '<ellipse cx="160" cy="40" rx="60" ry="18"/><path d="M100 40 L100 150 A60 18 0 0 0 220 150 L220 40"/>',
      cone: '<path d="M160 20 L100 150 A60 18 0 0 0 220 150 Z"/>', sphere: '<circle cx="160" cy="95" r="70"/><ellipse cx="160" cy="95" rx="70" ry="20" stroke-dasharray="5 5"/>'
    };
    return `<svg viewBox="0 0 320 200"><g class="drawall" fill="rgba(139,92,246,.12)" stroke="#8b5cf6" stroke-width="4" stroke-linejoin="round">${S[v.name] || S.circle}</g>
      <text class="late" x="160" y="192" font-size="15" font-weight="800" text-anchor="middle" fill="#8b5cf6">${v.name[0].toUpperCase() + v.name.slice(1)}</text></svg>`;
  }

  const R = { angle, clock, count, fraction, numberline, bars, compare, shape };
  window.Visual = { render: v => { try { return v && R[v.kind] ? R[v.kind](v) : ''; } catch (e) { return ''; } } };
})();
