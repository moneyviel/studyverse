/* ================= StudyVerse worlds: one themed map per grade ================= */
(function () {
  const W = 400;
  const rnd = seed => { let s = seed; return () => { s = (s * 9301 + 49297) % 233280; return s / 233280; }; };
  const em = (x, y, e, size, cls = '', delay = 0, op = 1) =>
    `<text class="${cls}" style="animation-delay:${delay.toFixed(2)}s" x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="${size}" text-anchor="middle" opacity="${op}">${e}</text>`;
  const stars = (r, n, H, maxY, col = '#fff') => { let s = ''; for (let k = 0; k < n; k++) { const y = r() * maxY; s += `<circle class="twinkle" style="animation-delay:${(r() * 3).toFixed(2)}s" cx="${(r() * W).toFixed(1)}" cy="${y.toFixed(1)}" r="${(r() * 1.6 + .4).toFixed(2)}" fill="${col}"/>`; } return s; };
  const grad = (id, stops) => `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1">${stops.map(([o, c]) => `<stop offset="${o}" stop-color="${c}"/>`).join('')}</linearGradient>`;
  const cloud = (x, y, s, op = .8, cls = 'drift', delay = 0) => `<g class="${cls}" style="animation-delay:${delay}s" opacity="${op}"><ellipse cx="${x}" cy="${y}" rx="${40 * s}" ry="${14 * s}" fill="#fff"/><ellipse cx="${x - 18 * s}" cy="${y - 8 * s}" rx="${22 * s}" ry="${14 * s}" fill="#fff"/><ellipse cx="${x + 14 * s}" cy="${y - 10 * s}" rx="${24 * s}" ry="${16 * s}" fill="#fff"/></g>`;

  /* ---------- island bases (what each stop stands on) ---------- */
  const BASES = {
    block: (x, y, s, c) => `<g><rect x="${x - 58 * s}" y="${y - 6 * s}" width="${116 * s}" height="${34 * s}" rx="${8 * s}" fill="${shade(c, -25)}"/><path d="M${x - 58 * s} ${y - 6 * s} l${18 * s} ${-22 * s} h${116 * s} l${-18 * s} ${22 * s}z" fill="${shade(c, 15)}"/><path d="M${x + 58 * s} ${y - 6 * s} l${18 * s} ${-22 * s} v${34 * s} l${-18 * s} ${22 * s}z" fill="${shade(c, -40)}"/><circle cx="${x - 30 * s}" cy="${y - 17 * s}" r="${6 * s}" fill="${shade(c, 30)}"/><circle cx="${x + 30 * s}" cy="${y - 17 * s}" r="${6 * s}" fill="${shade(c, 30)}"/></g>`,
    cake: (x, y, s, c) => `<g><ellipse cx="${x}" cy="${y + 26 * s}" rx="${70 * s}" ry="${14 * s}" fill="rgba(0,0,0,.12)"/><rect x="${x - 62 * s}" y="${y - 10 * s}" width="${124 * s}" height="${34 * s}" rx="${10 * s}" fill="#f8bbd0"/><ellipse cx="${x}" cy="${y - 10 * s}" rx="${62 * s}" ry="${16 * s}" fill="${c}"/><path d="M${x - 62 * s} ${y - 8 * s} q${10 * s} ${18 * s} ${20 * s} 0 q${10 * s} ${22 * s} ${22 * s} 0 q${10 * s} ${16 * s} ${20 * s} 0 q${12 * s} ${20 * s} ${22 * s} 0 q${10 * s} ${18 * s} ${20 * s} 0 q${10 * s} ${14 * s} ${20 * s} 0" fill="#fff" opacity=".85"/></g>`,
    mound: (x, y, s, c) => `<g><ellipse cx="${x}" cy="${y + 16 * s}" rx="${72 * s}" ry="${20 * s}" fill="#1b5e20" opacity=".5"/><ellipse cx="${x}" cy="${y + 6 * s}" rx="${66 * s}" ry="${24 * s}" fill="#5d4037"/><ellipse cx="${x}" cy="${y}" rx="${62 * s}" ry="${22 * s}" fill="${c}"/><ellipse cx="${x - 20 * s}" cy="${y - 7 * s}" rx="${24 * s}" ry="${6 * s}" fill="#fff" opacity=".2"/>${em(x - 52 * s, y + 4 * s, '🌿', 18 * s)}${em(x + 52 * s, y + 4 * s, '🌿', 18 * s)}</g>`,
    coral: (x, y, s, c) => `<g><ellipse cx="${x}" cy="${y + 8 * s}" rx="${68 * s}" ry="${22 * s}" fill="#4a3a6a"/><ellipse cx="${x}" cy="${y}" rx="${62 * s}" ry="${20 * s}" fill="${c}"/>${em(x - 50 * s, y + 2 * s, '🪸', 22 * s, 'sway')}${em(x + 50 * s, y + 2 * s, '🪸', 20 * s, 'sway', .7)}${em(x + 36 * s, y + 14 * s, '🐚', 14 * s)}</g>`,
    dune: (x, y, s, c) => `<g><ellipse cx="${x}" cy="${y + 14 * s}" rx="${76 * s}" ry="${16 * s}" fill="rgba(120,60,0,.25)"/><path d="M${x - 72 * s} ${y + 14 * s} Q${x - 20 * s} ${y - 30 * s} ${x + 72 * s} ${y + 14 * s}z" fill="${shade(c, -15)}"/><path d="M${x - 72 * s} ${y + 14 * s} Q${x - 30 * s} ${y - 22 * s} ${x + 30 * s} ${y + 6 * s} Q${x + 50 * s} ${y + 10 * s} ${x + 72 * s} ${y + 14 * s}z" fill="${c}"/>${em(x + 54 * s, y + 6 * s, '🌵', 20 * s)}</g>`,
    isle: (x, y, s, c) => `<g><ellipse cx="${x}" cy="${y + 22 * s}" rx="${82 * s}" ry="${24 * s}" fill="#fff" opacity=".22"/><ellipse cx="${x}" cy="${y + 14 * s}" rx="${72 * s}" ry="${26 * s}" fill="#f6dc9a"/><ellipse cx="${x}" cy="${y + 6 * s}" rx="${66 * s}" ry="${24 * s}" fill="#c99a5b"/><ellipse cx="${x}" cy="${y}" rx="${62 * s}" ry="${22 * s}" fill="${c}"/><ellipse cx="${x - 18 * s}" cy="${y - 8 * s}" rx="${26 * s}" ry="${7 * s}" fill="#fff" opacity=".18"/>${em(x - 48 * s, y, '🌴', 20 * s)}</g>`,
    rock: (x, y, s, c) => `<g><path d="M${x - 70 * s} ${y + 4 * s} L${x - 50 * s} ${y + 34 * s} L${x + 46 * s} ${y + 38 * s} L${x + 70 * s} ${y + 4 * s}z" fill="#546e7a"/><ellipse cx="${x}" cy="${y + 2 * s}" rx="${70 * s}" ry="${18 * s}" fill="#eceff1"/><ellipse cx="${x}" cy="${y}" rx="${60 * s}" ry="${14 * s}" fill="${c}" opacity=".55"/>${em(x - 54 * s, y - 2 * s, '🌲', 18 * s)}${em(x + 56 * s, y, '🌲', 16 * s)}</g>`,
    hex: (x, y, s, c) => `<g filter="url(#glow)"><path d="M${x - 64 * s} ${y} L${x - 34 * s} ${y - 20 * s} L${x + 34 * s} ${y - 20 * s} L${x + 64 * s} ${y} L${x + 34 * s} ${y + 20 * s} L${x - 34 * s} ${y + 20 * s}z" fill="#0d1b3a" stroke="${c}" stroke-width="${3 * s}"/><path d="M${x - 64 * s} ${y} L${x - 64 * s} ${y + 10 * s} L${x - 34 * s} ${y + 30 * s} L${x + 34 * s} ${y + 30 * s} L${x + 64 * s} ${y + 10 * s} L${x + 64 * s} ${y}" fill="none" stroke="${c}" stroke-opacity=".5" stroke-width="${2 * s}"/></g>`,
    cloud: (x, y, s, c) => `<g class="bob2"><ellipse cx="${x}" cy="${y + 10 * s}" rx="${70 * s}" ry="${20 * s}" fill="#fff"/><ellipse cx="${x - 36 * s}" cy="${y}" rx="${32 * s}" ry="${20 * s}" fill="#fff"/><ellipse cx="${x + 30 * s}" cy="${y - 2 * s}" rx="${36 * s}" ry="${22 * s}" fill="#fff"/><ellipse cx="${x}" cy="${y + 2 * s}" rx="${48 * s}" ry="${16 * s}" fill="${c}" opacity=".35"/></g>`,
    planet: (x, y, s, c) => `<g><ellipse cx="${x}" cy="${y + 6 * s}" rx="${80 * s}" ry="${14 * s}" fill="none" stroke="${shade(c, 30)}" stroke-width="${4 * s}" opacity=".7"/><circle cx="${x}" cy="${y + 20 * s}" r="${38 * s}" fill="${shade(c, -20)}"/><circle cx="${x - 10 * s}" cy="${y + 10 * s}" r="${30 * s}" fill="${c}" opacity=".6"/><circle cx="${x + 14 * s}" cy="${y + 30 * s}" r="${6 * s}" fill="rgba(0,0,0,.2)"/><circle cx="${x - 16 * s}" cy="${y + 34 * s}" r="${4 * s}" fill="rgba(0,0,0,.2)"/><path d="M${x - 80 * s} ${y + 6 * s} A${80 * s} ${14 * s} 0 0 0 ${x + 80 * s} ${y + 6 * s}" fill="none" stroke="${shade(c, 30)}" stroke-width="${4 * s}"/></g>`
  };

  function shade(hex, pct) {
    const n = parseInt(hex.slice(1), 16); let r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    const f = v => Math.max(0, Math.min(255, Math.round(v + (pct / 100) * (pct > 0 ? 255 - v : v))));
    return '#' + [f(r), f(g), f(b)].map(v => v.toString(16).padStart(2, '0')).join('');
  }

  /* ---------- the 10 worlds ---------- */
  const THEMES = {
    1: { name: 'Toy Land', tag: 'Where every block is a lesson', base: 'block', text: '#2b2350', path: '#ff7aa8',
      bg: (H, r) => `${grad('bg', [[0, '#bfe9ff'], [.6, '#e8d5ff'], [1, '#ffe3f1']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>
        ${[...Array(6)].map((_, i) => cloud(r() * W, 60 + r() * (H - 120), .8 + r() * .6, .85, 'drift', -r() * 40)).join('')}
        ${[...Array(9)].map(() => em(r() * W, 40 + r() * (H - 60), ['🎈', '🧸', '🪀', '🎨', '🪁', '🚂', '⭐'][Math.floor(r() * 7)], 18 + r() * 14, 'bob', r() * 3, .9)).join('')}
        ${stars(r, 30, H, H, '#fff')}` },
    2: { name: 'Candy Meadows', tag: 'Sweet ideas everywhere', base: 'cake', text: '#4a1d3a', path: '#ff4fa3',
      bg: (H, r) => `${grad('bg', [[0, '#ffd6ec'], [.5, '#ffe9c7'], [1, '#d7f7e8']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>
        ${[0, 1, 2].map(i => { const cy = 220 + i * H / 3; return `<g opacity=".45">${['#ff6b6b', '#ffb74d', '#fff176', '#81c784', '#64b5f6', '#ba68c8'].map((c, k) => `<path d="M-40 ${cy} A${240 - k * 14} ${200 - k * 14} 0 0 1 440 ${cy}" fill="none" stroke="${c}" stroke-width="12"/>`).join('')}</g>`; }).join('')}
        ${[...Array(12)].map(() => em(r() * W, 40 + r() * (H - 60), ['🍭', '🍬', '🧁', '🍩', '🍦', '🍓', '💖'][Math.floor(r() * 7)], 18 + r() * 14, r() > .5 ? 'bob' : 'bob2', r() * 3)).join('')}` },
    3: { name: 'Jungle Explorer', tag: 'Swing through the wild', base: 'mound', text: '#0f2e14', path: '#ffd54f',
      bg: (H, r) => `${grad('bg', [[0, '#a5e88f'], [.4, '#3fa65a'], [1, '#14532d']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>
        ${[...Array(10)].map(() => { const x = r() * W, y = r() * H; return `<path d="M${x} ${y} q${20 + r() * 30} ${40} ${0} ${90 + r() * 60}" fill="none" stroke="#1b5e20" stroke-width="3" opacity=".5"/>`; }).join('')}
        ${[...Array(18)].map(() => `<ellipse class="sway" style="animation-delay:${(r() * 3).toFixed(2)}s" cx="${r() * W}" cy="${r() * H}" rx="${18 + r() * 22}" ry="${7 + r() * 6}" fill="${['#2e7d32', '#388e3c', '#43a047', '#1b5e20'][Math.floor(r() * 4)]}" opacity=".55" transform="rotate(${r() * 180})"/>`).join('')}
        ${[...Array(9)].map(() => em(r() * W, 40 + r() * (H - 60), ['🦜', '🐒', '🦋', '🐯', '🐘', '🌺', '🍌'][Math.floor(r() * 7)], 20 + r() * 12, 'bob', r() * 3)).join('')}` },
    4: { name: 'Coral Reef', tag: 'Dive deep into ideas', base: 'coral', text: '#062a40', path: '#7fffd4',
      bg: (H, r) => `${grad('bg', [[0, '#6fe6ff'], [.35, '#1ba3c6'], [1, '#063f6b']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>
        ${[...Array(6)].map((_, i) => `<path d="M${-50 + i * 90} 0 L${10 + i * 90} ${H}" stroke="#fff" stroke-opacity=".06" stroke-width="40"/>`).join('')}
        ${[...Array(26)].map(() => `<circle class="rise" style="animation-delay:${(-r() * 8).toFixed(2)}s;animation-duration:${(6 + r() * 6).toFixed(1)}s" cx="${r() * W}" cy="${H - r() * 80}" r="${2 + r() * 5}" fill="none" stroke="#fff" stroke-opacity=".6"/>`).join('')}
        ${[...Array(10)].map(() => em(r() * W, 40 + r() * (H - 60), ['🐠', '🐟', '🐡', '🐙', '🐢', '🦀', '🐬', '🪼'][Math.floor(r() * 8)], 20 + r() * 12, r() > .5 ? 'swim' : 'bob', -r() * 12)).join('')}
        ${[...Array(7)].map(() => { const x = r() * W, y = r() * H; return `<path class="sway" d="M${x} ${y} q-8 -20 0 -40 q8 -20 0 -40" stroke="#2e7d32" stroke-width="5" fill="none" opacity=".6"/>`; }).join('')}` },
    5: { name: 'Desert of Wonders', tag: 'Secrets buried in the sand', base: 'dune', text: '#3e2000', path: '#ff7043',
      bg: (H, r) => `${grad('bg', [[0, '#ffcf6b'], [.3, '#ffb36b'], [.6, '#f6c98a'], [1, '#e2a35a']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>
        <circle cx="320" cy="70" r="40" fill="#fff3b0" filter="url(#glow)"/>
        ${[...Array(5)].map((_, i) => { const y = 200 + i * (H - 200) / 5; return `<path d="M0 ${y} Q100 ${y - 40} 200 ${y} T400 ${y} V${y + 80} H0z" fill="#d9944a" opacity=".25"/>`; }).join('')}
        ${[...Array(4)].map(() => { const x = r() * W, y = 150 + r() * (H - 200), s = .6 + r() * .6; return `<path d="M${x - 40 * s} ${y} L${x} ${y - 50 * s} L${x + 40 * s} ${y}z" fill="#c98a3c" opacity=".55"/><path d="M${x} ${y - 50 * s} L${x + 40 * s} ${y} L${x + 12 * s} ${y}z" fill="#a86d2a" opacity=".55"/>`; }).join('')}
        ${[...Array(8)].map(() => em(r() * W, 40 + r() * (H - 60), ['🐪', '🌵', '🦂', '🏺', '🦎', '☀️'][Math.floor(r() * 6)], 18 + r() * 12, 'bob', r() * 3)).join('')}` },
    6: { name: 'Island Voyage', tag: 'Sail from island to island', base: 'isle', text: '#0a1030', path: '#ffc93c',
      bg: (H, r) => {
        let w = ''; for (let y = 60; y < H; y += 46) { const off = (y * 13) % 80; w += `<g transform="translate(${-off},${y})"><path class="wave ${y % 92 ? 'b' : ''}" d="M0 0 ${Array.from({ length: 7 }, () => 'q20 -8 40 0 t40 0').join(' ')}" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="2"/></g>`; }
        return `${grad('bg', [[0, '#22408f'], [.5, '#1570b8'], [.85, '#11a3c9'], [1, '#3fd6d0']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>${w}
        ${[...Array(20)].map(() => `<circle class="twinkle" style="animation-delay:${(r() * 3).toFixed(2)}s" cx="${r() * W}" cy="${r() * H}" r="1.6" fill="#fff"/>`).join('')}
        ${[...Array(7)].map(() => em(r() * W, 40 + r() * (H - 60), ['🐬', '🐠', '⛵', '🐋', '🦭'][Math.floor(r() * 5)], 18 + r() * 10, 'bob2', r() * 3)).join('')}
        ${cloud(80, 120, 1, .4, 'drift', -10)}${cloud(300, H / 2, 1.2, .35, 'drift', -25)}`;
      } },
    7: { name: 'Mountain Kingdom', tag: 'Climb higher every day', base: 'rock', text: '#10203a', path: '#ffd54f',
      bg: (H, r) => `${grad('bg', [[0, '#5b4b8a'], [.4, '#8fb3e0'], [1, '#d6ecff']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>
        ${[0, 1, 2, 3].map(i => { const y = 260 + i * (H - 260) / 4, c = ['#7986cb', '#5c6bc0', '#3f51b5', '#303f9f'][i]; return `<path d="M-20 ${y + 120} L60 ${y} L120 ${y + 60} L200 ${y - 30} L280 ${y + 50} L340 ${y - 10} L420 ${y + 100} V${y + 260} H-20z" fill="${c}" opacity=".35"/><path d="M200 ${y - 30} L182 ${y - 4} L194 ${y - 8} L206 ${y + 2} L218 ${y - 6}z" fill="#fff" opacity=".7"/>`; }).join('')}
        ${[...Array(40)].map(() => `<circle class="fall" style="animation-delay:${(-r() * 10).toFixed(2)}s;animation-duration:${(8 + r() * 8).toFixed(1)}s" cx="${r() * W}" cy="${r() * H}" r="${1 + r() * 2}" fill="#fff" opacity=".8"/>`).join('')}
        ${[...Array(6)].map(() => em(r() * W, 40 + r() * (H - 60), ['🦅', '🐐', '🏔️', '🦌', '❄️'][Math.floor(r() * 5)], 18 + r() * 12, 'bob', r() * 3)).join('')}` },
    8: { name: 'Cyber City', tag: 'Code the future', base: 'hex', text: '#e0f7ff', path: '#00e5ff', dark: true,
      bg: (H, r) => {
        let b = ''; for (let k = 0; k < 14; k++) { const bw = 30 + r() * 40, bx = r() * W, by = 120 + r() * (H - 120), bh = 60 + r() * 140; b += `<rect x="${bx}" y="${by}" width="${bw}" height="${bh}" fill="#0b1640" opacity=".9"/>`; for (let wy = by + 8; wy < by + bh - 8; wy += 14) for (let wx = bx + 6; wx < bx + bw - 6; wx += 12) if (r() > .55) b += `<rect class="${r() > .8 ? 'twinkle' : ''}" style="animation-delay:${(r() * 3).toFixed(2)}s" x="${wx}" y="${wy}" width="5" height="6" fill="${r() > .5 ? '#00e5ff' : '#ff4fd8'}" opacity=".8"/>`; }
        let g = ''; for (let y = 0; y < H; y += 40) g += `<line x1="0" y1="${y}" x2="${W}" y2="${y}" stroke="#00e5ff" stroke-opacity=".08"/>`; for (let x = 0; x < W; x += 40) g += `<line x1="${x}" y1="0" x2="${x}" y2="${H}" stroke="#ff4fd8" stroke-opacity=".06"/>`;
        return `${grad('bg', [[0, '#070b24'], [.5, '#120a3a'], [1, '#1b0f4d']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>${g}${b}
        ${[...Array(7)].map(() => em(r() * W, 40 + r() * (H - 60), ['🤖', '🛸', '💾', '🎮', '📡', '⚡'][Math.floor(r() * 6)], 18 + r() * 10, 'bob', r() * 3)).join('')}`;
      } },
    9: { name: 'Sky Port', tag: 'Ideas that fly', base: 'cloud', text: '#0b2545', path: '#ff8a65',
      bg: (H, r) => `${grad('bg', [[0, '#4facfe'], [.5, '#8fd3fe'], [1, '#e0f4ff']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>
        <circle cx="330" cy="80" r="34" fill="#fff59d" filter="url(#glow)"/>
        ${[...Array(10)].map((_, i) => cloud(r() * W, 60 + r() * (H - 100), .7 + r() * .8, .75, 'drift', -r() * 40)).join('')}
        ${[...Array(9)].map(() => em(r() * W, 40 + r() * (H - 60), ['✈️', '🎈', '🪂', '🛩️', '🕊️', '🚁'][Math.floor(r() * 6)], 18 + r() * 12, r() > .5 ? 'swim' : 'bob', -r() * 12)).join('')}` },
    10: { name: 'Space Station', tag: 'Your launchpad to the stars', base: 'planet', text: '#f0e6ff', path: '#c084fc', dark: true,
      bg: (H, r) => `${grad('bg', [[0, '#05010f'], [.5, '#1a0b3d'], [1, '#2b1a6b']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>
        ${[...Array(4)].map(() => `<ellipse cx="${r() * W}" cy="${r() * H}" rx="${80 + r() * 80}" ry="${40 + r() * 40}" fill="${['#8b5cf6', '#ec4899', '#3b82f6'][Math.floor(r() * 3)]}" opacity=".18" filter="url(#soft)"/>`).join('')}
        ${stars(r, 90, H, H)}
        <g class="shoot"><line x1="360" y1="20" x2="400" y2="0" stroke="#fff" stroke-width="2"/></g>
        ${[...Array(8)].map(() => em(r() * W, 40 + r() * (H - 60), ['🚀', '🛰️', '🪐', '🌙', '☄️', '👩‍🚀', '🌍'][Math.floor(r() * 7)], 18 + r() * 14, 'bob', r() * 3)).join('')}` },
    11: { name: 'Aurora Peaks', tag: 'Light up big ideas', base: 'rock', text: '#e6fff7', path: '#5ef2c2', dark: true,
      bg: (H, r) => `${grad('bg', [[0, '#020617'], [.45, '#0b2447'], [1, '#19376d']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>
        ${stars(r, 70, H, H)}
        ${[0, 1, 2, 3, 4].map(i => { const y = 80 + i * (H / 5.2), c = ['#34d399', '#22d3ee', '#a78bfa', '#34d399', '#f472b6'][i]; return `<path class="drift" style="animation-delay:${-i * 4}s" d="M-60 ${y} C80 ${y - 70} 180 ${y + 60} 300 ${y - 20} S460 ${y - 50} 520 ${y}" fill="none" stroke="${c}" stroke-width="${26 + r() * 20}" stroke-linecap="round" opacity=".16" filter="url(#soft)"/>`; }).join('')}
        ${[0, 1, 2].map(i => { const y = 300 + i * (H - 300) / 3; return `<path d="M-20 ${y + 140} L50 ${y + 20} L110 ${y + 80} L190 ${y - 10} L260 ${y + 70} L330 ${y + 5} L420 ${y + 120} V${y + 300} H-20z" fill="${['#0f2a4a', '#0c2240', '#091a33'][i]}" opacity=".85"/>`; }).join('')}
        ${[...Array(8)].map(() => em(r() * W, 40 + r() * (H - 60), ['🔭', '⚗️', '🧬', '📊', '🦉', '💡', '📐'][Math.floor(r() * 7)], 18 + r() * 12, 'bob', r() * 3, .9)).join('')}` },
    12: { name: 'Summit of Dreams', tag: 'Your final climb to the top', base: 'cloud', text: '#3b1d00', path: '#ff6f3c',
      bg: (H, r) => `${grad('bg', [[0, '#ffb86b'], [.35, '#ff8fa3'], [.7, '#c5a3ff'], [1, '#7aa7ff']])}<rect width="${W}" height="${H}" fill="url(#bg)"/>
        <circle cx="200" cy="120" r="60" fill="#fff4c2" filter="url(#glow)" opacity=".9"/>
        ${[...Array(12)].map(() => `<line x1="200" y1="120" x2="${200 + Math.cos(r() * 6.28) * 400}" y2="${120 + Math.sin(r() * 6.28) * 400}" stroke="#fff" stroke-opacity=".08" stroke-width="10"/>`).join('')}
        ${[...Array(7)].map(() => cloud(r() * W, 160 + r() * (H - 220), .7 + r() * .8, .7, 'drift', -r() * 40)).join('')}
        ${[...Array(9)].map(() => em(r() * W, 40 + r() * (H - 60), ['🎓', '🏆', '🚀', '🌄', '🎯', '📜', '⭐'][Math.floor(r() * 7)], 18 + r() * 14, 'bob', r() * 3)).join('')}` }

  };

  const SUBJECT_STYLE = {
    maths: { e: '🔢', c: '#ffc93c' }, english: { e: '📖', c: '#4fc3f7' }, hindi: { e: 'अ', c: '#ff8a65' }, sanskrit: { e: 'ॐ', c: '#ffb74d' },
    evs: { e: '🌳', c: '#81c784' }, science: { e: '🔬', c: '#4dd0e1' }, social: { e: '🏛️', c: '#ba68c8' }, history: { e: '🏰', c: '#a1887f' },
    geography: { e: '🌍', c: '#4db6ac' }, civics: { e: '⚖️', c: '#7986cb' }, economics: { e: '💰', c: '#aed581' },
    physics: { e: '⚛️', c: '#64b5f6' }, chemistry: { e: '⚗️', c: '#f06292' }, biology: { e: '🧬', c: '#81c784' }, accountancy: { e: '📒', c: '#ffb74d' },
    business: { e: '💼', c: '#4db6ac' }, polsci: { e: '🗳️', c: '#7986cb' }, psychology: { e: '🧠', c: '#ce93d8' }, sociology: { e: '👥', c: '#ffab91' }, cs: { e: '💻', c: '#90caf9' }
  };
  SUBJECT_STYLE.sanskrit.e = '📜';

  const DEFS = `<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><filter id="soft"><feGaussianBlur stdDeviation="18"/></filter><filter id="dim"><feColorMatrix type="saturate" values=".35"/></filter>`;

  /* nodes: [{title, sub, emoji, color, state:'done'|'current'|'open'|'soon', stars(0-3), pct(0-100)}] */
  function buildMap(grade, nodes, kind) {
    const th = THEMES[grade] || THEMES[6], r = rnd(grade * 101 + nodes.length * 7 + (kind === 'grade' ? 0 : 999));
    const gap = kind === 'grade' ? 200 : 150, top = 150;
    const H = top + nodes.length * gap + 90;
    const pts = nodes.map((n, i) => ({ x: i % 2 ? 282 : 118, y: H - 110 - i * gap }));
    let path = '';
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i], b = pts[i + 1], d = `M${a.x} ${a.y} C${a.x} ${a.y - gap * .55} ${b.x} ${b.y + gap * .55} ${b.x} ${b.y}`;
      const st = nodes[i].state;
      path += st === 'done'
        ? `<path d="${d}" fill="none" stroke="${th.path}" stroke-width="7" stroke-linecap="round" filter="url(#glow)"/>`
        : `<path class="${st === 'current' ? 'flow' : ''}" d="${d}" fill="none" stroke="${th.dark ? '#fff' : th.text}" stroke-opacity="${st === 'current' ? .8 : .3}" stroke-width="5" stroke-dasharray="4 11" stroke-linecap="round"/>`;
    }
    const sc = kind === 'grade' ? 1 : .78;
    const nodeSvg = nodes.map((n, i) => {
      const { x, y } = pts[i], soon = n.state === 'soon';
      const base = BASES[th.base](x, y, sc, n.color || '#ffc93c');
      const big = kind === 'grade' ? 46 : 34;
      const icon = /^[ऀ-ॿ]/.test(n.emoji)
        ? `<text x="${x}" y="${y - 22 * sc}" font-size="${big * .9}" font-weight="800" text-anchor="middle" fill="${n.color}" stroke="#fff" stroke-width="2" paint-order="stroke" font-family="'Baloo 2',sans-serif">${n.emoji}</text>`
        : `<text x="${x}" y="${y - 20 * sc}" font-size="${big}" text-anchor="middle">${n.emoji}</text>`;
      const ring = kind === 'grade' && !soon ? (() => { const R = 30, c = 2 * Math.PI * R, p = Math.max(0, Math.min(100, n.pct || 0)); return `<g transform="translate(${x + 58 * sc},${y - 54 * sc})"><circle r="${R / 1.6}" fill="#0a1030" opacity=".85"/><circle r="${R / 1.6}" fill="none" stroke="#2ed3a5" stroke-width="4" stroke-dasharray="${(c / 1.6) * p / 100} 999" transform="rotate(-90)"/><text y="4" font-size="10" font-weight="800" fill="#fff" text-anchor="middle">${Math.round(p)}%</text></g>`; })() : '';
      const starsTxt = kind === 'chapter' && n.stars ? `<text x="${x}" y="${y - 66 * sc}" font-size="15" text-anchor="middle">${'⭐'.repeat(n.stars)}${'☆'.repeat(3 - n.stars)}</text>` : '';
      const cur = n.state === 'current' ? `<circle class="pulse" cx="${x}" cy="${y}" r="${72 * sc}" fill="none" stroke="${th.path}" stroke-width="3"/>` : '';
      const badge = soon ? `<g transform="translate(${x + 50 * sc},${y - 50 * sc})"><rect x="-34" y="-11" width="68" height="20" rx="10" fill="#0a1030" stroke="#ffc93c"/><text y="3" font-size="9.5" font-weight="800" fill="#ffc93c" text-anchor="middle">SOON</text></g>` : '';
      const numBadge = kind === 'chapter' ? `<g transform="translate(${x - 56 * sc},${y - 46 * sc})"><circle r="13" fill="${n.state === 'done' ? '#2ed3a5' : '#fff'}" stroke="#0a1030" stroke-width="2"/><text y="4.5" font-size="12" font-weight="800" text-anchor="middle" fill="#0a1030">${n.state === 'done' ? '✓' : n.num}</text></g>` : '';
      const lw = kind === 'grade' ? 170 : 210;
      const label = `<g transform="translate(${x},${y + (kind === 'grade' ? 52 : 44)})"><rect x="${-lw / 2}" y="-14" width="${lw}" height="${n.sub ? 36 : 28}" rx="12" fill="${n.state === 'current' ? th.path : 'rgba(10,16,48,.82)'}" stroke="rgba(255,255,255,.35)"/>
        <text y="${n.sub ? 1 : 5}" font-family="'Baloo 2',Nunito,sans-serif" font-weight="800" font-size="${kind === 'grade' ? 15 : 12.5}" text-anchor="middle" fill="${n.state === 'current' ? '#0a1030' : '#fff'}">${esc(trim(n.title, kind === 'grade' ? 22 : 30))}</text>
        ${n.sub ? `<text y="15" font-size="9.5" font-weight="700" text-anchor="middle" fill="${n.state === 'current' ? '#0a1030' : '#c9d1ff'}">${esc(n.sub)}</text>` : ''}</g>`;
      return `<g class="node ${soon ? 'soon' : ''}" data-i="${i}" ${soon ? 'filter="url(#dim)"' : ''}>${cur}<g class="${n.state === 'current' ? 'bob' : ''}">${base}${icon}</g>${ring}${starsTxt}${badge}${numBadge}</g>${label}`;
    }).join('');
    const title = `<g transform="translate(200,52)"><rect x="-150" y="-30" width="300" height="56" rx="18" fill="rgba(10,16,48,.55)"/><text y="-4" font-family="'Baloo 2',sans-serif" font-weight="800" font-size="22" text-anchor="middle" fill="#fff">${esc(th.name)}</text><text y="16" font-size="11" font-weight="700" text-anchor="middle" fill="#ffe08a">Grade ${grade} · ${esc(th.tag)}</text></g>`;
    return { svg: `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg"><defs>${DEFS}</defs>${th.bg(H, r)}${path}${nodeSvg}${kind === 'grade' ? title : ''}</svg>`, H, pts };
  }
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const trim = (s, n) => (s.length > n ? s.slice(0, n - 1) + '…' : s);

  let uidCounter = 0;
  function render(el, grade, nodes, kind, onTap) {
    const m = buildMap(grade, nodes, kind);
    const uid = 'm' + (++uidCounter);
    el.innerHTML = m.svg.replace(/id="([\w-]+)"/g, `id="$1-${uid}"`).replace(/url\(#([\w-]+)\)/g, `url(#$1-${uid})`);
    el.querySelectorAll('.node').forEach(g => g.addEventListener('click', () => onTap(+g.dataset.i)));
    const cur = nodes.findIndex(n => n.state === 'current');
    requestAnimationFrame(() => {
      const sv = el.querySelector('svg'); const y = cur >= 0 ? m.pts[cur].y : m.H;
      el.scrollTop = y / m.H * sv.clientHeight - el.clientHeight * .55;
    });
  }

  window.Worlds = { THEMES, SUBJECT_STYLE, render, shade };
})();
